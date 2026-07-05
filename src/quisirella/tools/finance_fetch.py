"""Fetch and parse Quisirella finance data from Google Sheets.

Writes structured JSON to data/finance_fetch/ for Cursor agents (finance-fetcher).
"""

from __future__ import annotations

import json
import re
from calendar import monthrange
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from quisirella.settings import (
    FINANCE_FETCH_DIR,
    GOOGLE_SHEET_ID,
    load_finance_sheet,
)
from quisirella.tools.google_sheets_client import sheets_service as _sheets_service

_MONTH_LABEL_RE = re.compile(
    r"Tháng\s*(\d{1,2})\s*/\s*(\d{4})", re.IGNORECASE
)


def col_letter_to_index(letter: str) -> int:
    """Convert column letter (A, K, M) to 0-based index."""
    idx = 0
    for ch in letter.upper():
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def parse_vnd(text: str | None) -> int | None:
    """Parse formatted VND like '73.900.000 đ' or '281.355.000 ₫' to integer."""
    if text is None:
        return None
    s = str(text).strip()
    if not s or s in ("-", "—", "n/a", "N/A"):
        return None
    # Percentages are not VND
    if "%" in s:
        return None
    # Keep digits only (drops đ, ₫, dots, commas, spaces)
    digits = re.sub(r"[^\d]", "", s)
    if not digits:
        return None
    return int(digits)


def parse_percent(text: str | None) -> float | None:
    if text is None:
        return None
    s = str(text).strip().replace("%", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_int(text: str | None) -> int | None:
    if text is None:
        return None
    s = str(text).strip()
    if not s:
        return None
    digits = re.sub(r"[^\d]", "", s)
    return int(digits) if digits else None


def _cell(rows: list[list], row_1based: int, col_letter: str) -> str | None:
    """Get cell value from sparse row list (0-based rows, A1 col letter)."""
    if row_1based < 1:
        return None
    row_idx = row_1based - 1
    if row_idx >= len(rows):
        return None
    col_idx = col_letter_to_index(col_letter)
    row = rows[row_idx]
    if col_idx >= len(row):
        return None
    val = row[col_idx]
    return str(val).strip() if val is not None and str(val).strip() else None


def _month_key_from_label(label: str) -> str | None:
    m = _MONTH_LABEL_RE.search(label)
    if not m:
        return None
    month, year = int(m.group(1)), int(m.group(2))
    return f"{year}-{month:02d}"


def list_archive_tab_names(cfg: dict | None = None) -> list[str]:
    """Generate tab names Tháng n/yyyy from archive_monthly_tabs config."""
    cfg = cfg or load_finance_sheet()
    arch = cfg["archive_monthly_tabs"]
    start_m, start_y = arch["from"]["month"], arch["from"]["year"]
    end_m, end_y = arch["to"]["month"], arch["to"]["year"]
    pattern = arch["pattern"]
    names: list[str] = []
    y, m = start_y, start_m
    while (y, m) <= (end_y, end_m):
        names.append(pattern.format(n=m, yyyy=y))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return names


def _find_ytd_value(rows: list[list], label_substr: str) -> tuple[int | None, str | None]:
    """Find value in column D where column C contains exact label."""
    for ri, row in enumerate(rows, start=1):
        if len(row) < 4:
            continue
        label_c = str(row[2]).strip()
        if label_substr.lower() in label_c.lower():
            v = parse_vnd(row[3])
            if v is not None:
                return v, f"D{ri}"
    return None, None


def parse_bao_gia_2026(rows: list[list], cfg: dict | None = None) -> dict[str, Any]:
    """Parse BÁO GIÁ 2026 grid into ytd + monthly metrics."""
    cfg = cfg or load_finance_sheet()
    mt = cfg["monthly_table"]
    cols = mt["columns"]
    ytd_labels = cfg.get("ytd_labels", {})

    ytd: dict[str, Any] = {}
    if ytd_labels.get("ros"):
        for ri, row in enumerate(rows, start=1):
            if row and ytd_labels["ros"].split("\n")[0] in str(row[0]):
                ytd["ros_pct"] = parse_percent(row[1] if len(row) > 1 else None)
                ytd["ros_source"] = f"B{ri}"
                break

    for key, label in ytd_labels.items():
        if key == "ros":
            continue
        val, src = _find_ytd_value(rows, label)
        if val is not None:
            ytd[key] = val
            ytd[f"{key}_source"] = src

    months: list[dict[str, Any]] = []
    first_row = mt["first_data_row"]
    totals_row = mt.get("totals_row", 10)

    for row_num in range(first_row, totals_row):
        label = _cell(rows, row_num, cols["month_label"])
        if not label or "Tháng" not in label:
            continue
        month_key = _month_key_from_label(label)
        entry: dict[str, Any] = {
            "month_key": month_key,
            "label": label,
            "source_row": row_num,
            "qty_sold_month": parse_int(_cell(rows, row_num, cols["qty_sold_month"])),
            "profit_actual": parse_vnd(_cell(rows, row_num, cols["profit_actual"])),
            "revenue_actual": parse_vnd(_cell(rows, row_num, cols["revenue_actual"])),
            "source_cells": {
                "qty_sold_month": f"{cols['qty_sold_month']}{row_num}",
                "profit_actual": f"{cols['profit_actual']}{row_num}",
                "revenue_actual": f"{cols['revenue_actual']}{row_num}",
            },
        }
        months.append(entry)

    # Totals row (row 10)
    totals: dict[str, Any] = {
        "source_row": totals_row,
        "qty_sold_month": parse_int(_cell(rows, totals_row, cols["qty_sold_month"])),
        "profit_actual": parse_vnd(_cell(rows, totals_row, cols["profit_actual"])),
        "revenue_actual": parse_vnd(_cell(rows, totals_row, cols["revenue_actual"])),
    }

    return {
        "tab": cfg["primary_tab"],
        "ytd": ytd,
        "months": months,
        "totals_row": totals,
        "parsed_at": datetime.now(timezone.utc).isoformat(),
    }


def parse_report(rows: list[list]) -> dict[str, Any]:
    """Parse REPORT tab key-value pairs."""
    metrics: dict[str, Any] = {}
    for ri, row in enumerate(rows, start=1):
        if len(row) < 2:
            continue
        key = str(row[0]).strip()
        if not key:
            continue
        val_raw = row[1]
        vnd = parse_vnd(val_raw)
        pct = parse_percent(val_raw) if vnd is None else None
        num = parse_int(val_raw) if vnd is None and pct is None else None
        metrics[key] = {
            "raw": val_raw,
            "vnd": vnd,
            "percent": pct,
            "number": num,
            "source": f"B{ri}",
        }
    return {"tab": "REPORT", "metrics": metrics}


def month_period_bounds(month_key: str) -> tuple[str, str]:
    """YYYY-MM -> (since, until) ISO dates for calendar month."""
    year, month = map(int, month_key.split("-"))
    last_day = monthrange(year, month)[1]
    return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day:02d}"


def _safe_tab_filename(tab_name: str) -> str:
    return tab_name.replace("/", "_").replace(" ", "_")


def fetch_finance(period: str | None = None) -> dict[str, Any]:
    """Fetch finance data and write JSON under data/finance_fetch/.

    Args:
        period: Optional YYYY-MM calendar month to highlight in manifest.

    Returns:
        Manifest dict (same content written to manifest.json).
    """
    if not GOOGLE_SHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID chưa cấu hình trong .env")

    cfg = load_finance_sheet()
    service = _sheets_service()
    out_dir = FINANCE_FETCH_DIR
    monthly_dir = out_dir / "monthly_tabs"
    out_dir.mkdir(parents=True, exist_ok=True)
    monthly_dir.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []
    files_written: list[dict[str, Any]] = []
    data_status = "ok"

    # --- BÁO GIÁ 2026 summary ---
    summary_range = cfg["summary_range"]
    try:
        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=summary_range,
                valueRenderOption="FORMATTED_VALUE",
            )
            .execute()
        )
        raw_rows = result.get("values", [])
        raw_path = out_dir / "bao_gia_2026_raw.json"
        raw_path.write_text(
            json.dumps({"range": summary_range, "rows": raw_rows}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        files_written.append(
            {"path": str(raw_path.relative_to(out_dir.parent.parent)), "content": "raw grid", "rows": len(raw_rows)}
        )

        parsed = parse_bao_gia_2026(raw_rows, cfg)
        summary_path = out_dir / "bao_gia_2026_summary.json"
        summary_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        files_written.append(
            {
                "path": str(summary_path.relative_to(out_dir.parent.parent)),
                "content": "parsed BÁO GIÁ 2026 metrics",
                "months": len(parsed.get("months", [])),
            }
        )
    except Exception as exc:
        errors.append(f"bao_gia_2026: {exc}")
        data_status = "unavailable"

    # --- REPORT ---
    try:
        report_range = cfg["report_range"]
        result = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=report_range,
                valueRenderOption="FORMATTED_VALUE",
            )
            .execute()
        )
        report_rows = result.get("values", [])
        report_parsed = parse_report(report_rows)
        report_path = out_dir / "report_summary.json"
        report_path.write_text(json.dumps(report_parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        files_written.append(
            {
                "path": str(report_path.relative_to(out_dir.parent.parent)),
                "content": "REPORT key metrics",
                "keys": len(report_parsed.get("metrics", {})),
            }
        )
    except Exception as exc:
        errors.append(f"report: {exc}")
        if data_status == "ok":
            data_status = "partial"

    # --- Archive monthly tabs ---
    existing_tabs: set[str] = set()
    try:
        meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
        existing_tabs = {s["properties"]["title"] for s in meta.get("sheets", [])}
    except Exception as exc:
        errors.append(f"list_tabs: {exc}")
        data_status = "partial" if data_status == "ok" else data_status

    archive_names = list_archive_tab_names(cfg)
    archived = 0
    for tab_name in archive_names:
        if tab_name not in existing_tabs:
            continue
        safe = _safe_tab_filename(tab_name)
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=GOOGLE_SHEET_ID,
                    range=f"'{tab_name}'!A:Z",
                    valueRenderOption="FORMATTED_VALUE",
                )
                .execute()
            )
            rows = result.get("values", [])
            tab_path = monthly_dir / f"{safe}.json"
            tab_path.write_text(
                json.dumps({"tab": tab_name, "rows": rows}, ensure_ascii=False),
                encoding="utf-8",
            )
            archived += 1
        except Exception as exc:
            errors.append(f"archive {tab_name}: {exc}")

    files_written.append(
        {
            "path": "data/finance_fetch/monthly_tabs/",
            "content": "raw monthly tab archive",
            "tabs": archived,
        }
    )

    if errors and data_status == "ok":
        data_status = "partial"

    date_range: dict[str, str] | None = None
    if period:
        since, until = month_period_bounds(period)
        date_range = {"since": since, "until": until, "month_key": period}

    manifest = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "spreadsheet_id": GOOGLE_SHEET_ID,
        "period": period,
        "date_range": date_range,
        "data_status": data_status,
        "files": files_written,
        "errors": errors or None,
        "archive_tabs_requested": len(archive_names),
        "archive_tabs_saved": archived,
    }

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return manifest

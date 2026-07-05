"""Google Sheets tools (service account auth).

The store owner shares the finance spreadsheet with the service account
email once; after that every run is non-interactive.
"""

from __future__ import annotations

import json
from pathlib import Path

from langchain.tools import tool

from quisirella.settings import GOOGLE_SHEET_ID, GOOGLE_SHEET_RANGES
from quisirella.tools.google_sheets_client import sheets_service as _sheets_service


@tool
def list_sheet_tabs() -> str:
    """Liệt kê tên các tab (sheet) trong Google Sheet tài chính của Quisirella."""
    service = _sheets_service()
    meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    return json.dumps({"spreadsheet": meta.get("properties", {}).get("title"), "tabs": tabs}, ensure_ascii=False)


@tool
def read_sheet_range(range_a1: str) -> str:
    """Đọc dữ liệu từ Google Sheet tài chính theo range A1 notation.

    Args:
        range_a1: Range cần đọc, ví dụ 'DoanhThu!A1:H100' hoặc 'ChiPhi!A:Z'.
    """
    service = _sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=GOOGLE_SHEET_ID, range=range_a1)
        .execute()
    )
    values = result.get("values", [])
    return json.dumps({"range": range_a1, "rows": values}, ensure_ascii=False)


@tool
def read_configured_finance_ranges() -> str:
    """Đọc các range tài chính từ config/finance_sheet.yaml (hoặc GOOGLE_SHEET_RANGES legacy .env)."""
    ranges: list[str] = list(GOOGLE_SHEET_RANGES)
    if not ranges:
        from quisirella.settings import load_finance_sheet

        cfg = load_finance_sheet()
        ranges = [cfg["summary_range"], cfg["report_range"]]
    if not ranges:
        return json.dumps(
            {"error": "Chưa cấu hình range — xem config/finance_sheet.yaml"},
            ensure_ascii=False,
        )
    service = _sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=GOOGLE_SHEET_ID, ranges=ranges)
        .execute()
    )
    payload = [
        {"range": vr.get("range"), "rows": vr.get("values", [])}
        for vr in result.get("valueRanges", [])
    ]
    return json.dumps(payload, ensure_ascii=False)


SHEETS_TOOLS = [list_sheet_tabs, read_sheet_range, read_configured_finance_ranges]

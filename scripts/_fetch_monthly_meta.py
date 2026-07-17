"""Fetch monthly Meta account spend (read-only)."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
from quisirella.settings import configure_utf8_stdio  # noqa: E402

load_dotenv(_ROOT / ".env")
configure_utf8_stdio()

TOKEN = os.getenv("META_ACCESS_TOKEN", "")
ACCT = "act_400356462876861"
FIELDS = "spend,impressions,reach,clicks,actions,cost_per_action_type"

MONTHS = [
    ("2026-01", "2026-01-01", "2026-01-31"),
    ("2026-02", "2026-02-01", "2026-02-28"),
    ("2026-03", "2026-03-01", "2026-03-31"),
    ("2026-04", "2026-04-01", "2026-04-30"),
    ("2026-05", "2026-05-01", "2026-05-31"),
    ("2026-06", "2026-06-01", "2026-06-30"),
]


def jul_mtd_range() -> tuple[str, str]:
    today = date.today()
    return today.replace(day=1).isoformat(), today.isoformat()


def messaging_started(actions: list | None) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == "onsite_conversion.messaging_conversation_started_7d":
            return int(a.get("value", 0))
    return 0


def fetch(since: str, until: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": since, "until": until}),
            "access_token": TOKEN,
        }
    )
    url = f"https://graph.facebook.com/v21.0/{ACCT}/insights?{params}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.loads(resp.read())
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload.get("data", [{}])[0]


def main() -> None:
    if not TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing")

    jul_since, jul_until = jul_mtd_range()
    months = [*MONTHS, ("2026-07", jul_since, jul_until)]

    rows = []
    for month_key, since, until in months:
        row = fetch(since, until)
        spend = float(row.get("spend", 0))
        mess = messaging_started(row.get("actions"))
        rows.append(
            {
                "month_key": month_key,
                "since": since,
                "until": until,
                "spend_vnd": round(spend),
                "messaging_started_7d": mess,
                "cost_per_message": round(spend / mess) if mess else None,
            }
        )

    out_dir = Path("data/meta_fetch")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "monthly_spend_2026.json"
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    jul_row = fetch(jul_since, jul_until)
    jul_path = out_dir / f"account_insights_{jul_since}_{jul_until}.json"
    jul_path.write_text(
        json.dumps({"data": [jul_row], "fetched_at": jul_until}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    manifest = {
        "months": rows,
        "jul_mtd": {"since": jul_since, "until": jul_until, "spend_vnd": rows[-1]["spend_vnd"]},
    }
    (out_dir / "fetch_manifest_roas_months.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

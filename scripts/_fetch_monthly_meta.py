"""Fetch monthly Meta account spend (read-only)."""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

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
    ("2026-07", "2026-07-01", "2026-07-06"),
]


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
    with urllib.request.urlopen(url) as resp:
        payload = json.loads(resp.read())
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload.get("data", [{}])[0]


def main() -> None:
    if not TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing")

    rows = []
    for month_key, since, until in MONTHS:
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

    out_path = Path("data/meta_fetch/monthly_spend_2026.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Jul MTD account raw
    jul_row = fetch("2026-07-01", "2026-07-06")
    jul_path = Path("data/meta_fetch/account_insights_2026-07-01_2026-07-06.json")
    jul_path.write_text(
        json.dumps({"data": [jul_row], "fetched_at": "2026-07-06"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

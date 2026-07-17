"""Fetch ad-level insights for phễu campaign (read-only).

Usage:
  python scripts/_fetch_pheu_ads.py                         # MTD (1st of month → today)
  python scripts/_fetch_pheu_ads.py 2026-07-07              # single day
  python scripts/_fetch_pheu_ads.py 2026-07-01 2026-07-07   # date range
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
from quisirella.settings import configure_utf8_stdio  # noqa: E402

load_dotenv(_ROOT / ".env")
configure_utf8_stdio()

TOKEN = os.getenv("META_ACCESS_TOKEN", "")
CID = "120253285175280110"
FIELDS = (
    "ad_id,ad_name,spend,impressions,reach,clicks,ctr,cpc,actions,cost_per_action_type"
)
CAMP_FIELDS = (
    "campaign_name,spend,impressions,clicks,ctr,actions,cost_per_action_type"
)


def parse_dates(argv: list[str] | None = None) -> tuple[str, str]:
    today = date.today()
    default_since = today.replace(day=1).isoformat()
    default_until = today.isoformat()

    parser = argparse.ArgumentParser(
        description="Fetch phễu campaign ad-level insights (Graph API, read-only)."
    )
    parser.add_argument(
        "dates",
        nargs="*",
        metavar="YYYY-MM-DD",
        help="one date (single day) or since until (range); default: current month MTD",
    )
    args = parser.parse_args(argv)

    if len(args.dates) == 0:
        return default_since, default_until
    if len(args.dates) == 1:
        d = args.dates[0]
        return d, d
    if len(args.dates) == 2:
        return args.dates[0], args.dates[1]
    parser.error("at most 2 dates: YYYY-MM-DD  OR  YYYY-MM-DD YYYY-MM-DD")


def api_get(path: str, params: dict) -> dict:
    params = {**params, "access_token": TOKEN}
    url = f"https://graph.facebook.com/v21.0/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.loads(resp.read())
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def action_val(actions: list | None, action_type: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return int(float(a.get("value", 0)))
    return 0


def row_metrics(row: dict) -> dict:
    started = action_val(
        row.get("actions"), "onsite_conversion.messaging_conversation_started_7d"
    )
    d3 = action_val(
        row.get("actions"), "onsite_conversion.messaging_user_depth_3_message_send"
    )
    spend = float(row.get("spend", 0))
    return {
        "spend_vnd": round(spend),
        "messaging_started_7d": started,
        "cost_per_message": round(spend / started) if started else None,
        "depth_3": d3,
        "engaged_rate_pct": round(d3 / started * 100, 1) if started else None,
        "impressions": int(row.get("impressions", 0) or 0),
        "clicks": int(row.get("clicks", 0) or 0),
        "ctr_pct": round(float(row.get("ctr", 0) or 0), 2),
    }


def fetch_adsets_and_creatives(out: Path, ads_payload: dict) -> None:
    adsets = api_get(
        f"{CID}/adsets",
        {
            "fields": "id,name,status,daily_budget,lifetime_budget,optimization_goal,created_time",
            "limit": 50,
        },
    )
    save(out / f"{CID}_adsets.json", adsets)
    if (adsets.get("paging") or {}).get("next"):
        print("WARN: adsets paging.next exists — may be truncated")

    creatives_by_ad: list[dict] = []
    for ad in ads_payload.get("data", []):
        ad_id = ad.get("id")
        if not ad_id:
            continue
        try:
            creative = api_get(
                ad_id,
                {"fields": "creative{id,name,object_type,thumbnail_url,object_story_spec}"},
            )
            creatives_by_ad.append(
                {
                    "ad_id": ad_id,
                    "ad_name": ad.get("name"),
                    "creative": creative.get("creative"),
                }
            )
        except RuntimeError as exc:
            creatives_by_ad.append({"ad_id": ad_id, "ad_name": ad.get("name"), "error": str(exc)})
    save(out / f"{CID}_creatives.json", {"data": creatives_by_ad})


def main(argv: list[str] | None = None) -> None:
    if not TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing")

    since, until = parse_dates(argv)
    out = Path("data/meta_fetch/active")
    time_range = json.dumps({"since": since, "until": until})

    ads = api_get(
        f"{CID}/ads",
        {"fields": "id,name,status,created_time,effective_status", "limit": 50},
    )
    save(out / f"{CID}_ads.json", ads)
    fetch_adsets_and_creatives(out, ads)

    ad_ins = api_get(
        f"{CID}/insights",
        {"fields": FIELDS, "level": "ad", "time_range": time_range},
    )
    save(out / f"{CID}_ad_insights.json", ad_ins)

    ad_daily = api_get(
        f"{CID}/insights",
        {
            "fields": FIELDS,
            "level": "ad",
            "time_range": time_range,
            "time_increment": "1",
        },
    )
    save(out / f"{CID}_ad_daily.json", ad_daily)

    for suffix, extra in [("_insights", {}), ("_daily", {"time_increment": "1"})]:
        payload = api_get(
            f"{CID}/insights",
            {"fields": CAMP_FIELDS, "time_range": time_range, **extra},
        )
        save(out / f"{CID}{suffix}.json", payload)

    placement = api_get(
        f"{CID}/insights",
        {
            "fields": "spend,impressions,clicks,actions",
            "time_range": time_range,
            "time_increment": "1",
            "breakdowns": "publisher_platform",
        },
    )
    save(out / f"{CID}_placement_daily.json", placement)

    day_only = api_get(
        f"{CID}/insights",
        {
            "fields": FIELDS,
            "level": "ad",
            "time_range": json.dumps({"since": until, "until": until}),
        },
    )
    save(out / f"{CID}_ad_insights_{until}.json", day_only)

    summary = {
        "since": since,
        "until": until,
        "day_snapshot": until,
        "ads_period": [],
        "ads_day": [],
    }
    for row in ad_ins.get("data", []):
        summary["ads_period"].append(
            {"ad_name": row.get("ad_name"), **row_metrics(row)}
        )
    for row in day_only.get("data", []):
        summary["ads_day"].append({"ad_name": row.get("ad_name"), **row_metrics(row)})

    manifest = Path(f"data/meta_fetch/fetch_manifest_{since}_{until}.json")
    save(manifest, summary)

    print(f"range: {since} → {until}")
    print("ADS:")
    for a in ads.get("data", []):
        print(
            f"  {a.get('id')} | {a.get('name')} | {a.get('status')} | "
            f"{(a.get('created_time') or '')[:10]}"
        )

    print("PERIOD ad metrics:")
    for row in ad_ins.get("data", []):
        spend = float(row.get("spend", 0))
        mess = action_val(
            row.get("actions"),
            "onsite_conversion.messaging_conversation_started_7d",
        )
        cpm = round(spend / mess) if mess else "n/a"
        print(f"  {row.get('ad_name')}: spend={round(spend)} mess={mess} cpm={cpm}")

    label = "DAILY by ad" if since != until else "DAY"
    print(f"{label} (last 4 days):" if since != until else f"{label} {until}:")
    by_name: dict[str, list] = defaultdict(list)
    for row in ad_daily.get("data", []):
        by_name[row.get("ad_name", "")].append(row)
    for name, rows in by_name.items():
        rows = sorted(rows, key=lambda x: x.get("date_start", ""))
        for r in rows[-4:]:
            spend = float(r.get("spend", 0))
            mess = action_val(
                r.get("actions"),
                "onsite_conversion.messaging_conversation_started_7d",
            )
            print(f"  {r.get('date_start')} | {name}: spend={round(spend)} mess={mess}")

    print(f"\nmanifest: {manifest}")


if __name__ == "__main__":
    main()

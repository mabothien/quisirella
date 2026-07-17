"""Fetch ACTIVE campaign insights (read-only) for Quisirella.

Usage:
  python scripts/_fetch_active_campaigns.py
  python scripts/_fetch_active_campaigns.py --since 2026-07-01 --until 2026-07-10
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
from quisirella.settings import configure_utf8_stdio  # noqa: E402

load_dotenv(_ROOT / ".env")
configure_utf8_stdio()

TOKEN = os.getenv("META_ACCESS_TOKEN", "")
ACCOUNT = "act_400356462876861"

CAMPAIGNS = [
    ("120253285175280110", "phieu_tinnhan"),
    ("120252531135370110", "profile_1806"),
    ("120252990977040110", "retarget"),
]

FIELDS = (
    "campaign_name,spend,impressions,reach,clicks,ctr,cpc,cpm,actions,cost_per_action_type"
)
ADSET_FIELDS = (
    "id,name,status,daily_budget,lifetime_budget,optimization_goal,targeting,created_time"
)
AD_FIELDS = "id,name,status,created_time,effective_status"
ADSET_INSIGHT_FIELDS = (
    "adset_name,adset_id,spend,impressions,clicks,ctr,cpc,actions,cost_per_action_type"
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    today = date.today()
    default_since = today.replace(day=1).isoformat()
    default_until = today.isoformat()
    parser = argparse.ArgumentParser(description="Fetch ACTIVE campaign insights (read-only).")
    parser.add_argument("--since", default=default_since, help="YYYY-MM-DD")
    parser.add_argument("--until", default=default_until, help="YYYY-MM-DD")
    return parser.parse_args(argv)


def verdict_window(since: str, until: str) -> tuple[str, str]:
    end = date.fromisoformat(until)
    start = date.fromisoformat(since)
    v_end = end
    v_start = max(start, end - timedelta(days=1))
    return v_start.isoformat(), v_end.isoformat()


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


def count_rows(payload: dict) -> int:
    return len(payload.get("data") or [])


def has_paging_next(payload: dict) -> bool:
    return bool((payload.get("paging") or {}).get("next"))


def fetch_campaign_insights(campaign_id: str, since: str, until: str, **extra) -> dict:
    return api_get(
        f"{campaign_id}/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": since, "until": until}),
            **extra,
        },
    )


def action_val(actions: list | None, action_type: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return int(float(a.get("value", 0)))
    return 0


def row_metrics(row: dict) -> dict:
    started = action_val(row.get("actions"), "onsite_conversion.messaging_conversation_started_7d")
    first = action_val(row.get("actions"), "onsite_conversion.messaging_first_reply")
    d3 = action_val(row.get("actions"), "onsite_conversion.messaging_user_depth_3_message_send")
    d5 = action_val(row.get("actions"), "onsite_conversion.messaging_user_depth_5_message_send")
    spend = float(row.get("spend", 0))
    clicks = int(row.get("clicks", 0) or 0)
    impressions = int(row.get("impressions", 0) or 0)
    link = action_val(row.get("actions"), "link_click")
    ctr = float(row.get("ctr", 0) or 0)
    return {
        "spend_vnd": round(spend),
        "messaging_started_7d": started,
        "cost_per_message": round(spend / started) if started else None,
        "messaging_first_reply": first,
        "depth_3": d3,
        "depth_5": d5,
        "reply_rate_pct": round(first / started * 100, 1) if started else None,
        "engaged_rate_pct": round(d3 / started * 100, 1) if started else None,
        "link_click": link,
        "ctr_pct": round(ctr, 2),
        "clicks": clicks,
        "impressions": impressions,
    }


def main(argv: list[str] | None = None) -> None:
    if not TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing")

    args = parse_args(argv)
    since, until = args.since, args.until
    verdict_since, verdict_until = verdict_window(since, until)
    time_range = json.dumps({"since": since, "until": until})

    out_dir = Path("data/meta_fetch/active")
    summary: dict = {
        "since": since,
        "until": until,
        "verdict_window": [verdict_since, verdict_until],
        "campaigns": [],
        "inventory": [],
    }

    for cid, label in CAMPAIGNS:
        period = fetch_campaign_insights(cid, since, until)
        save(out_dir / f"{cid}_insights.json", period)

        daily = fetch_campaign_insights(cid, since, until, time_increment="1")
        save(out_dir / f"{cid}_daily.json", daily)

        placement = api_get(
            f"{cid}/insights",
            {
                "fields": "spend,impressions,clicks,actions",
                "time_range": time_range,
                "time_increment": "1",
                "breakdowns": "publisher_platform",
            },
        )
        save(out_dir / f"{cid}_placement_daily.json", placement)

        adsets = api_get(f"{cid}/adsets", {"fields": ADSET_FIELDS, "limit": 50})
        save(out_dir / f"{cid}_adsets.json", adsets)

        ads = api_get(f"{cid}/ads", {"fields": AD_FIELDS, "limit": 50})
        save(out_dir / f"{cid}_ads.json", ads)

        adset_ins = api_get(
            f"{cid}/insights",
            {
                "fields": ADSET_INSIGHT_FIELDS,
                "level": "adset",
                "time_range": time_range,
            },
        )
        save(out_dir / f"{cid}_adset_insights.json", adset_ins)

        inv = {
            "id": cid,
            "label": label,
            "adsets_count": count_rows(adsets),
            "ads_count": count_rows(ads),
            "adset_names": [a.get("name") for a in adsets.get("data", [])],
            "ad_names": [a.get("name") for a in ads.get("data", [])],
            "paging_warning": has_paging_next(adsets) or has_paging_next(ads),
        }
        summary["inventory"].append(inv)

        period_row = period.get("data", [{}])[0]
        verdict_row = fetch_campaign_insights(cid, verdict_since, verdict_until).get("data", [{}])[0]
        summary["campaigns"].append(
            {
                "id": cid,
                "label": label,
                "period": row_metrics(period_row),
                "verdict_window": row_metrics(verdict_row),
                "adsets_count": inv["adsets_count"],
                "ads_count": inv["ads_count"],
            }
        )

    acct = api_get(
        f"{ACCOUNT}/insights",
        {"fields": FIELDS, "time_range": time_range},
    )
    save(Path(f"data/meta_fetch/account_insights_{since}_{until}.json"), acct)

    verdict_acct = api_get(
        f"{ACCOUNT}/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": verdict_since, "until": verdict_until}),
        },
    )
    period_acct = acct.get("data", [{}])[0]
    verdict_acct_row = verdict_acct.get("data", [{}])[0]
    summary["account"] = {
        "period": row_metrics(period_acct),
        "verdict_window": row_metrics(verdict_acct_row),
    }

    retarget_pl = json.loads(
        (out_dir / "120252990977040110_placement_daily.json").read_text(encoding="utf-8")
    )
    fb_timeline = []
    for row in retarget_pl.get("data", []):
        fb_timeline.append(
            {
                "date": row.get("date_start"),
                "platform": row.get("publisher_platform"),
                "spend_vnd": round(float(row.get("spend", 0))),
            }
        )
    summary["retarget_platform_daily"] = fb_timeline

    manifest_path = Path(f"data/meta_fetch/fetch_manifest_{since}_{until}.json")
    save(manifest_path, summary)

    print(f"range: {since} → {until}")
    print("INVENTORY:")
    for inv in summary["inventory"]:
        warn = " [PAGING — may need pagination]" if inv["paging_warning"] else ""
        print(
            f"  {inv['id']} ({inv['label']}): adsets={inv['adsets_count']} ads={inv['ads_count']}{warn}"
        )
        print(f"    adsets: {inv['adset_names']}")
        print(f"    ads: {inv['ad_names']}")
    print(f"\nmanifest: {manifest_path}")


if __name__ == "__main__":
    main()

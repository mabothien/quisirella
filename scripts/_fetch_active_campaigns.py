"""Fetch ACTIVE campaign insights (read-only) for Quisirella."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
from quisirella.settings import configure_utf8_stdio  # noqa: E402

load_dotenv(_ROOT / ".env")
configure_utf8_stdio()

TOKEN = os.getenv("META_ACCESS_TOKEN", "")
SINCE = "2026-07-01"
UNTIL = "2026-07-06"
VERDICT_SINCE = "2026-07-05"
VERDICT_UNTIL = "2026-07-06"

CAMPAIGNS = [
    ("120253285175280110", "phieu_tinnhan"),
    ("120252531135370110", "profile_1806"),
    ("120252990977040110", "retarget"),
]

FIELDS = (
    "campaign_name,spend,impressions,reach,clicks,ctr,cpc,cpm,actions,cost_per_action_type"
)


def api_get(path: str, params: dict) -> dict:
    params = {**params, "access_token": TOKEN}
    url = f"https://graph.facebook.com/v21.0/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as resp:
        payload = json.loads(resp.read())
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_campaign_insights(campaign_id: str, since: str, until: str) -> dict:
    payload = api_get(
        f"{campaign_id}/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": since, "until": until}),
        },
    )
    return payload


def fetch_daily(campaign_id: str) -> dict:
    return api_get(
        f"{campaign_id}/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": SINCE, "until": UNTIL}),
            "time_increment": "1",
        },
    )


def fetch_placement_daily(campaign_id: str) -> dict:
    return api_get(
        f"{campaign_id}/insights",
        {
            "fields": "spend,impressions,clicks,actions",
            "time_range": json.dumps({"since": SINCE, "until": UNTIL}),
            "time_increment": "1",
            "breakdowns": "publisher_platform",
        },
    )


def action_val(actions: list | None, action_type: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return int(a.get("value", 0))
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


def main() -> None:
    if not TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing")

    out_dir = Path("data/meta_fetch/active")
    summary = {"since": SINCE, "until": UNTIL, "verdict_window": [VERDICT_SINCE, VERDICT_UNTIL], "campaigns": []}

    for cid, _label in CAMPAIGNS:
        period = fetch_campaign_insights(cid, SINCE, UNTIL)
        save(out_dir / f"{cid}_insights.json", period)

        daily = fetch_daily(cid)
        save(out_dir / f"{cid}_daily.json", daily)

        placement = fetch_placement_daily(cid)
        save(out_dir / f"{cid}_placement_daily.json", placement)

        period_row = period.get("data", [{}])[0]
        verdict_payload = fetch_campaign_insights(cid, VERDICT_SINCE, VERDICT_UNTIL)
        verdict_row = verdict_payload.get("data", [{}])[0]

        summary["campaigns"].append(
            {
                "id": cid,
                "period": row_metrics(period_row),
                "verdict_window": row_metrics(verdict_row),
            }
        )

    acct = api_get(
        "act_400356462876861/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": SINCE, "until": UNTIL}),
        },
    )
    save(Path(f"data/meta_fetch/account_insights_{SINCE}_{UNTIL}.json"), acct)

    verdict_acct = api_get(
        "act_400356462876861/insights",
        {
            "fields": FIELDS,
            "time_range": json.dumps({"since": VERDICT_SINCE, "until": VERDICT_UNTIL}),
        },
    )

    period_acct = acct.get("data", [{}])[0]
    verdict_acct_row = verdict_acct.get("data", [{}])[0]
    summary["account"] = {
        "period": row_metrics(period_acct),
        "verdict_window": row_metrics(verdict_acct_row),
    }

    # Retarget IG/FB daily from placement
    retarget_pl = json.loads((out_dir / "120252990977040110_placement_daily.json").read_text(encoding="utf-8"))
    fb_timeline = []
    for row in retarget_pl.get("data", []):
        day = row.get("date_start")
        platform = row.get("publisher_platform")
        spend = float(row.get("spend", 0))
        fb_timeline.append({"date": day, "platform": platform, "spend_vnd": round(spend)})
    summary["retarget_platform_daily"] = fb_timeline

    manifest_path = Path(f"data/meta_fetch/fetch_manifest_{SINCE}_{UNTIL}.json")
    save(manifest_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

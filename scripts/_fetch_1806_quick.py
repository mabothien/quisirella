"""Quick read-only fetch for campaign 1806 (profile)."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
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
CID = "120252531135370110"
OUT = _ROOT / "data" / "meta_fetch" / "active"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://graph.facebook.com/v21.0"

errors: list[dict] = []
saved: list[dict] = []


def api_get(path: str, params: dict | None = None) -> dict:
    params = dict(params or {})
    params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=90) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except Exception:
            return {"error": {"message": body, "code": e.code}}


def save(name: str, data: dict) -> Path:
    path = OUT / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = len(data.get("data") or []) if isinstance(data.get("data"), list) else None
    keys = list(data.keys()) if isinstance(data, dict) else []
    saved.append({"path": str(path.relative_to(_ROOT)).replace("\\", "/"), "rows": rows, "keys": keys[:20]})
    return path


def record_error(payload: dict, context: str) -> bool:
    err = payload.get("error") if isinstance(payload, dict) else None
    if not err:
        return False
    errors.append({"context": context, **err})
    return True


def main() -> int:
    if not TOKEN:
        print("MISSING META_ACCESS_TOKEN")
        return 1

    details = api_get(
        CID,
        {
            "fields": (
                "id,name,status,effective_status,objective,created_time,updated_time,"
                "daily_budget,lifetime_budget,budget_remaining,start_time,stop_time,"
                "buying_type,special_ad_categories"
            ),
        },
    )
    if record_error(details, "campaign_details"):
        print("DETAILS_ERROR", json.dumps(details.get("error"), ensure_ascii=False))
    else:
        save(f"{CID}_details.json", details)
        print("NAME:", details.get("name"))
        print("STATUS:", details.get("status"), "/", details.get("effective_status"))
        print("OBJECTIVE:", details.get("objective"))
        print("CREATED:", details.get("created_time"))
        print("DAILY_BUDGET:", details.get("daily_budget"))

    adsets = api_get(
        f"{CID}/adsets",
        {
            "fields": (
                "id,name,status,effective_status,daily_budget,lifetime_budget,"
                "optimization_goal,billing_event,created_time,updated_time,targeting"
            ),
            "limit": 50,
        },
    )
    if record_error(adsets, "adsets"):
        print("ADSETS_ERROR", json.dumps(adsets.get("error"), ensure_ascii=False))
    else:
        save(f"{CID}_adsets.json", adsets)
        print("ADSETS:", len(adsets.get("data") or []))
        for a in adsets.get("data") or []:
            print(
                f"  adset {a.get('id')} | {a.get('name')} | "
                f"{a.get('status')}/{a.get('effective_status')} | "
                f"opt={a.get('optimization_goal')} | daily_budget={a.get('daily_budget')}"
            )

    ads = api_get(
        f"{CID}/ads",
        {
            "fields": (
                "id,name,status,effective_status,created_time,updated_time,adset_id,"
                "creative{id,name,title,body,image_url,thumbnail_url,object_story_spec,"
                "asset_feed_spec,image_hash}"
            ),
            "limit": 50,
        },
    )
    if record_error(ads, "ads"):
        print("ADS_ERROR", json.dumps(ads.get("error"), ensure_ascii=False))
        ads = {"data": []}
    else:
        save(f"{CID}_ads.json", ads)
        print("ADS:", len(ads.get("data") or []))
        for a in ads.get("data") or []:
            cr = a.get("creative") or {}
            body = (cr.get("body") or "")[:160]
            print(
                f"  ad {a.get('id')} | {a.get('name')} | "
                f"{a.get('status')}/{a.get('effective_status')}"
            )
            print(f"    title={cr.get('title')!r} body={body!r}")

    creatives_bundle: dict = {"campaign_id": CID, "ads": []}
    for a in ads.get("data") or []:
        cr = a.get("creative") or {}
        cid_cr = cr.get("id")
        detail = None
        if cid_cr:
            detail = api_get(
                cid_cr,
                {
                    "fields": (
                        "id,name,title,body,image_url,thumbnail_url,object_type,"
                        "object_story_spec,asset_feed_spec,url_tags,status"
                    ),
                },
            )
            if record_error(detail, f"creative:{cid_cr}"):
                detail = {"error": detail.get("error"), "id": cid_cr}
        creatives_bundle["ads"].append(
            {
                "ad_id": a.get("id"),
                "ad_name": a.get("name"),
                "status": a.get("status"),
                "effective_status": a.get("effective_status"),
                "creative_inline": cr,
                "creative_detail": detail,
            }
        )
    save(f"{CID}_creatives.json", creatives_bundle)

    until = date.today()
    since = until - timedelta(days=6)
    time_range = json.dumps({"since": since.isoformat(), "until": until.isoformat()})
    insight_fields = (
        "campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,"
        "actions,cost_per_action_type,unique_actions"
    )

    insights = api_get(
        f"{CID}/insights",
        {"fields": insight_fields, "time_range": time_range},
    )
    if record_error(insights, "insights_last_7d"):
        print("INSIGHTS_ERROR", json.dumps(insights.get("error"), ensure_ascii=False))
    else:
        save(f"{CID}_insights_last_7d_{since.isoformat()}_{until.isoformat()}.json", insights)
        save(f"{CID}_insights_last_7d.json", insights)
        rows = insights.get("data") or []
        print("INSIGHTS_ROWS:", len(rows), "range", since.isoformat(), until.isoformat())
        if rows:
            r = rows[0]
            print(
                "SPEND:", r.get("spend"),
                "FREQ:", r.get("frequency"),
                "IMPR:", r.get("impressions"),
                "REACH:", r.get("reach"),
            )
            print("ACTIONS:", json.dumps(r.get("actions") or [], ensure_ascii=False)[:1200])

    insights_preset = api_get(
        f"{CID}/insights",
        {"fields": insight_fields, "date_preset": "last_7d"},
    )
    if not record_error(insights_preset, "insights_last_7d_preset"):
        save(f"{CID}_insights_last_7d_preset.json", insights_preset)

    ad_insights = api_get(
        f"{CID}/insights",
        {
            "fields": (
                "ad_id,ad_name,spend,impressions,reach,frequency,clicks,ctr,"
                "actions,cost_per_action_type"
            ),
            "level": "ad",
            "time_range": time_range,
            "limit": 50,
        },
    )
    if record_error(ad_insights, "ad_insights_last_7d"):
        print("AD_INSIGHTS_ERROR", json.dumps(ad_insights.get("error"), ensure_ascii=False))
    else:
        save(f"{CID}_ad_insights_last_7d.json", ad_insights)
        print("AD_INSIGHTS:", len(ad_insights.get("data") or []))

    has_details = any(s["path"].endswith("_details.json") for s in saved)
    if errors and not has_details:
        data_status = "unavailable"
    elif errors:
        data_status = "partial"
    else:
        data_status = "ok"

    manifest = {
        "campaign_id": CID,
        "date_range": {
            "since": since.isoformat(),
            "until": until.isoformat(),
            "label": "last_7d",
        },
        "account": "act_400356462876861",
        "files_saved": saved,
        "errors": errors,
        "data_status": data_status,
    }
    print("---MANIFEST---")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if data_status != "unavailable" else 2


if __name__ == "__main__":
    raise SystemExit(main())

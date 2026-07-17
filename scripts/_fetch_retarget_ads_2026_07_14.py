"""Fetch Retarget campaign ads + creatives + insights (read-only). Today 2026-07-14."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
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
CID = "120252990977040110"
OUT = _ROOT / "data" / "meta_fetch" / "active"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://graph.facebook.com/v21.0"
errors: list[str] = []


def api_get(path: str, params: dict | None = None, paginate: bool = True) -> dict:
    params = dict(params or {})
    params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    all_data: list = []
    first: dict | None = None
    while url:
        try:
            with urllib.request.urlopen(url, timeout=90) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body)
            except Exception:
                err = {"error": {"message": body, "code": e.code}}
            raise RuntimeError(json.dumps(err, ensure_ascii=False)) from None
        if first is None:
            first = payload
        if "error" in payload:
            raise RuntimeError(json.dumps(payload, ensure_ascii=False))
        if not paginate:
            return payload
        data = payload.get("data")
        if data is None:
            return payload
        all_data.extend(data)
        paging = payload.get("paging") or {}
        url = paging.get("next")
    return {"data": all_data, "paging_exhausted": True}


def save(name: str, data) -> str:
    p = OUT / f"{CID}_{name}"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p.relative_to(_ROOT)).replace("\\", "/")


def main() -> int:
    if not TOKEN:
        print("META_ACCESS_TOKEN missing")
        return 1

    # 1) Campaign
    try:
        camp = api_get(
            CID,
            {
                "fields": "id,name,status,effective_status,objective,created_time,daily_budget,lifetime_budget"
            },
            paginate=False,
        )
        save("campaign.json", camp)
        print(
            "CAMPAIGN:",
            camp.get("id"),
            camp.get("name"),
            camp.get("status"),
            camp.get("effective_status"),
        )
    except Exception as e:
        errors.append(str(e))
        print("CAMPAIGN ERROR:", e)
        camp = {"error": str(e)}

    # 2) ALL ads
    try:
        ads = api_get(
            f"{CID}/ads",
            {
                "fields": (
                    "id,name,status,effective_status,created_time,updated_time,adset_id,"
                    "creative{id,name,object_type,object_story_spec,asset_feed_spec,"
                    "image_hash,image_url,thumbnail_url,title,body,call_to_action_type}"
                ),
                "limit": "100",
            },
        )
        save("ads.json", ads)
        print(f"ADS count: {len(ads.get('data', []))}")
        for a in ads.get("data", []):
            print(
                f"  {a['id']} | {a.get('status')} | {a.get('effective_status')} | {a.get('name')}"
            )
    except Exception as e:
        errors.append(str(e))
        print("ADS ERROR:", e)
        ads = {"data": []}

    # 3) Creatives / carousel cards
    creatives_out: dict = {"campaign_id": CID, "ads": []}
    for a in ads.get("data", []):
        entry: dict = {
            "ad_id": a["id"],
            "ad_name": a.get("name"),
            "status": a.get("status"),
            "effective_status": a.get("effective_status"),
            "created_time": a.get("created_time"),
            "creative_raw": a.get("creative"),
            "carousel_cards": [],
            "creative_type": None,
            "image_hashes": [],
        }
        cr = a.get("creative") or {}
        cid_cr = cr.get("id")
        full = cr
        if cid_cr:
            try:
                full = api_get(
                    cid_cr,
                    {
                        "fields": (
                            "id,name,object_type,status,thumbnail_url,image_hash,image_url,"
                            "title,body,call_to_action_type,object_story_spec,asset_feed_spec,url_tags"
                        )
                    },
                    paginate=False,
                )
                entry["creative_full"] = full
            except Exception as e:
                errors.append(f"creative {cid_cr}: {e}")
                entry["creative_error"] = str(e)

        oss = (full or {}).get("object_story_spec") or {}
        link_data = oss.get("link_data") or {}
        video_data = oss.get("video_data") or {}
        attachments = link_data.get("child_attachments") or []

        if attachments:
            entry["creative_type"] = "carousel"
            for i, att in enumerate(attachments):
                card = {
                    "index": i,
                    "name": att.get("name"),
                    "description": att.get("description"),
                    "link": att.get("link"),
                    "image_hash": att.get("image_hash"),
                    "picture": att.get("picture"),
                    "video_id": att.get("video_id"),
                    "call_to_action": att.get("call_to_action"),
                }
                entry["carousel_cards"].append(card)
                if att.get("image_hash"):
                    entry["image_hashes"].append(att["image_hash"])
        elif video_data:
            entry["creative_type"] = "video"
            entry["title"] = video_data.get("title") or (full or {}).get("title")
            entry["body"] = video_data.get("message") or (full or {}).get("body")
            if (full or {}).get("image_hash"):
                entry["image_hashes"].append(full["image_hash"])
        elif link_data:
            entry["creative_type"] = "link/single"
            entry["title"] = link_data.get("name") or (full or {}).get("title")
            entry["body"] = link_data.get("message") or (full or {}).get("body")
            if link_data.get("image_hash"):
                entry["image_hashes"].append(link_data["image_hash"])
            elif (full or {}).get("image_hash"):
                entry["image_hashes"].append(full["image_hash"])
        else:
            afs = (full or {}).get("asset_feed_spec") or {}
            if afs:
                entry["creative_type"] = "dynamic/asset_feed"
                entry["asset_feed_spec_summary"] = {
                    "titles": [t.get("text") for t in (afs.get("titles") or [])],
                    "bodies": [b.get("text") for b in (afs.get("bodies") or [])],
                    "images": [
                        {"hash": im.get("hash"), "url": im.get("url")}
                        for im in (afs.get("images") or [])
                    ],
                    "videos": afs.get("videos"),
                    "link_urls": afs.get("link_urls"),
                    "ad_formats": afs.get("ad_formats"),
                }
                entry["image_hashes"] = [
                    im.get("hash") for im in (afs.get("images") or []) if im.get("hash")
                ]
            else:
                entry["creative_type"] = (full or {}).get("object_type") or "unknown"
                if (full or {}).get("image_hash"):
                    entry["image_hashes"].append(full["image_hash"])
                entry["title"] = (full or {}).get("title")
                entry["body"] = (full or {}).get("body")

        creatives_out["ads"].append(entry)
        print(
            f"CREATIVE {a['id']}: type={entry['creative_type']} "
            f"cards={len(entry['carousel_cards'])} hashes={len(entry['image_hashes'])}"
        )

    save("creatives.json", creatives_out)

    # 4) Insights last 7d + today
    insight_fields = (
        "ad_id,ad_name,spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,"
        "actions,cost_per_action_type"
    )
    ranges = {
        "last_7d": ("2026-07-08", "2026-07-14"),
        "today": ("2026-07-14", "2026-07-14"),
    }
    insights_bundle: dict = {"campaign_id": CID, "ranges": {}}
    for label, (since, until) in ranges.items():
        try:
            payload = api_get(
                f"{CID}/insights",
                {
                    "level": "ad",
                    "time_range": json.dumps({"since": since, "until": until}),
                    "fields": insight_fields,
                    "limit": "100",
                },
            )
            fname = f"ad_insights_{label}_{since}_{until}.json"
            path = save(fname, {"since": since, "until": until, **payload})
            insights_bundle["ranges"][label] = {
                "since": since,
                "until": until,
                "file": path,
                "rows": len(payload.get("data", [])),
            }
            print(f"INSIGHTS {label}: {len(payload.get('data', []))} rows")
            for row in payload.get("data", []):
                acts = row.get("actions") or []
                mess = next(
                    (
                        int(float(a["value"]))
                        for a in acts
                        if a.get("action_type")
                        == "onsite_conversion.messaging_conversation_started_7d"
                    ),
                    0,
                )
                spend = float(row.get("spend") or 0)
                print(
                    f"  {row.get('ad_id')} spend={spend:.0f} mess={mess} "
                    f"ctr={row.get('ctr')} freq={row.get('frequency')} "
                    f"name={row.get('ad_name')}"
                )
        except Exception as e:
            errors.append(f"insights {label}: {e}")
            print(f"INSIGHTS {label} ERROR:", e)

    # Daily + placement (checklist)
    try:
        daily = api_get(
            f"{CID}/insights",
            {
                "level": "campaign",
                "time_increment": "1",
                "time_range": json.dumps({"since": "2026-07-08", "until": "2026-07-14"}),
                "fields": "spend,impressions,reach,frequency,clicks,ctr,actions,cost_per_action_type",
                "limit": "100",
            },
        )
        save("daily.json", daily)
        print("DAILY rows:", len(daily.get("data", [])))
    except Exception as e:
        errors.append(f"daily: {e}")
        print("DAILY ERROR:", e)

    try:
        place = api_get(
            f"{CID}/insights",
            {
                "level": "campaign",
                "time_increment": "1",
                "breakdowns": "publisher_platform",
                "time_range": json.dumps({"since": "2026-07-08", "until": "2026-07-14"}),
                "fields": "spend,impressions,reach,clicks,ctr,actions,cost_per_action_type",
                "limit": "200",
            },
        )
        save("placement_daily.json", place)
        print("PLACEMENT_DAILY rows:", len(place.get("data", [])))
    except Exception as e:
        errors.append(f"placement_daily: {e}")
        print("PLACEMENT ERROR:", e)

    try:
        adsets = api_get(
            f"{CID}/adsets",
            {
                "fields": (
                    "id,name,status,effective_status,daily_budget,lifetime_budget,"
                    "optimization_goal,billing_event,created_time"
                ),
                "limit": "50",
            },
        )
        save("adsets.json", adsets)
        print("ADSETS:", len(adsets.get("data", [])))
    except Exception as e:
        errors.append(f"adsets: {e}")
        print("ADSETS ERROR:", e)

    delivering = [
        a for a in ads.get("data", []) if a.get("effective_status") == "ACTIVE"
    ]
    token_expired = any(
        "190" in e or "Session has expired" in e or "Error validating access token" in e
        for e in errors
    )
    if token_expired:
        data_status = "unavailable"
    elif errors and ads.get("data"):
        data_status = "partial"
    elif errors and not ads.get("data"):
        data_status = "unavailable"
    else:
        data_status = "ok"

    if data_status == "unavailable" and token_expired:
        blocked = _ROOT / "data" / "run_meta_blocked" / "fetch_error.json"
        blocked.parent.mkdir(parents=True, exist_ok=True)
        blocked.write_text(
            json.dumps(
                {
                    "error": errors[0] if errors else "token expired",
                    "error_code": 190,
                    "action": "refresh META_ACCESS_TOKEN in .env then re-run",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    manifest = {
        "date_range": {
            "last_7d": ["2026-07-08", "2026-07-14"],
            "today": ["2026-07-14", "2026-07-14"],
        },
        "account": "act_400356462876861",
        "campaign_id": CID,
        "campaign_name": camp.get("name") if isinstance(camp, dict) else None,
        "campaign_role": "ban_retarget_30d",
        "data_status": data_status,
        "fetched_at": "2026-07-14",
        "ads_count": len(ads.get("data", [])),
        "delivering_now": [
            {
                "id": a["id"],
                "name": a.get("name"),
                "effective_status": a.get("effective_status"),
            }
            for a in delivering
        ],
        "files": sorted(
            str(p.relative_to(_ROOT)).replace("\\", "/")
            for p in OUT.glob(f"{CID}_*")
        ),
        "errors": errors if errors else "none",
        "insights_summary": insights_bundle,
    }
    man_path = OUT / f"fetch_manifest_retarget_{CID}_2026-07-14.json"
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nMANIFEST:", man_path)
    print("data_status:", data_status)
    print("errors:", errors if errors else "none")
    print("delivering_now:", len(delivering))
    return 0 if data_status != "unavailable" else 2


if __name__ == "__main__":
    raise SystemExit(main())

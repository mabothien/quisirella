"""One-shot Pheu 2-ad pair decision fetch (Graph API read-only). Today 2026-07-14."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
from quisirella.settings import configure_utf8_stdio  # noqa: E402

load_dotenv(_ROOT / ".env")
configure_utf8_stdio()

TOKEN = os.getenv("META_ACCESS_TOKEN", "")
ACCOUNT = "act_400356462876861"
CID = "120253285175280110"
API = "https://graph.facebook.com/v21.0"
OUT = _ROOT / "data/meta_fetch/active"

WINDOWS = {
    "today": ("2026-07-14", "2026-07-14", True),
    "yesterday": ("2026-07-13", "2026-07-13", False),
    "last_3d": ("2026-07-12", "2026-07-14", True),
    "last_7d": ("2026-07-08", "2026-07-14", True),
}

CAMP_FIELDS = (
    "campaign_name,campaign_id,spend,impressions,reach,frequency,"
    "clicks,ctr,cpc,cpm,actions,cost_per_action_type,inline_link_clicks"
)
AD_FIELDS = (
    "ad_id,ad_name,adset_id,adset_name,spend,impressions,reach,frequency,"
    "clicks,ctr,cpc,cpm,actions,cost_per_action_type,inline_link_clicks"
)


def api_get(path: str, params: dict) -> dict:
    params = {**params, "access_token": TOKEN}
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


def save(path: Path, data: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_blocked(err: dict) -> None:
    blocked = {
        "error": err.get("message", ""),
        "error_code": err.get("code"),
        "error_subcode": err.get("error_subcode"),
        "full_error": err,
        "action": (
            "Refresh META_ACCESS_TOKEN in .env (or Pipeboard token in "
            ".cursor/mcp.json), then re-run fetch."
        ),
        "account": ACCOUNT,
        "campaign_id": CID,
        "fetched_at": date.today().isoformat(),
        "purpose": "pheu_2ad_pair_decision",
    }
    save(_ROOT / "data/run_meta_blocked/fetch_error.json", blocked)
    print("BLOCKED:", json.dumps(blocked, ensure_ascii=False)[:800])


def action_val(actions, action_type: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return int(float(a.get("value", 0)))
    return 0


def link_clicks(row: dict) -> int:
    lc = action_val(row.get("actions"), "link_click")
    if lc:
        return lc
    return int(float(row.get("inline_link_clicks", 0) or 0))


def extract_metrics(row: dict) -> dict:
    spend = float(row.get("spend", 0) or 0)
    mess = action_val(
        row.get("actions"), "onsite_conversion.messaging_conversation_started_7d"
    )
    reach = int(float(row.get("reach", 0) or 0))
    impressions = int(float(row.get("impressions", 0) or 0))
    freq = row.get("frequency")
    freq_f = (
        float(freq)
        if freq not in (None, "")
        else (round(impressions / reach, 4) if reach else None)
    )
    return {
        "spend": round(spend, 2),
        "mess": mess,
        "cost_per_mess": round(spend / mess, 2) if mess else None,
        "frequency": freq_f,
        "reach": reach,
        "impressions": impressions,
        "ctr": float(row.get("ctr", 0) or 0),
        "link_click": link_clicks(row),
        "messaging_first_reply": action_val(
            row.get("actions"), "onsite_conversion.messaging_first_reply"
        ),
        "depth_2": action_val(
            row.get("actions"), "onsite_conversion.messaging_user_depth_2_message_send"
        ),
        "depth_3": action_val(
            row.get("actions"), "onsite_conversion.messaging_user_depth_3_message_send"
        ),
        "depth_5": action_val(
            row.get("actions"), "onsite_conversion.messaging_user_depth_5_message_send"
        ),
        "lead": action_val(row.get("actions"), "lead"),
    }


def body_snippet(creative):
    if not creative:
        return None
    if creative.get("body"):
        return str(creative["body"])[:500]
    oss = creative.get("object_story_spec") or {}
    for key in ("link_data", "video_data", "photo_data", "template_data"):
        block = oss.get(key) or {}
        msg = block.get("message")
        if msg:
            return msg[:500]
    afs = creative.get("asset_feed_spec") or {}
    bodies = afs.get("bodies") or []
    if bodies:
        texts = [b.get("text") for b in bodies if b.get("text")]
        if texts:
            return " | ".join(texts)[:500]
    return creative.get("name")


def main() -> int:
    if not TOKEN:
        print("META_ACCESS_TOKEN missing")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    errors = []
    files = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    me = api_get("me", {"fields": "id,name"})
    if "error" in me:
        write_blocked(me["error"])
        return 1
    print("ME OK:", me.get("id"), me.get("name"))

    ads = api_get(
        f"{CID}/ads",
        {"fields": "id,name,status,effective_status,created_time,adset_id", "limit": 50},
    )
    if "error" in ads:
        write_blocked(ads["error"])
        return 1
    save(OUT / f"{CID}_ads.json", ads)
    files.append({"path": f"data/meta_fetch/active/{CID}_ads.json", "content": "ads list", "rows": len(ads.get("data") or [])})

    adsets = api_get(
        f"{CID}/adsets",
        {
            "fields": "id,name,status,effective_status,created_time,daily_budget,lifetime_budget,optimization_goal",
            "limit": 50,
        },
    )
    if "error" in adsets:
        errors.append(f"adsets: {adsets['error']}")
    else:
        save(OUT / f"{CID}_adsets.json", adsets)
        files.append({"path": f"data/meta_fetch/active/{CID}_adsets.json", "content": "adsets list", "rows": len(adsets.get("data") or [])})

    ad_status = {a.get("id"): a for a in (ads.get("data") or [])}

    creatives_out = []
    for ad in ads.get("data") or []:
        ad_id = ad.get("id")
        if not ad_id:
            continue
        creative_payload = api_get(
            ad_id,
            {
                "fields": (
                    "id,name,status,effective_status,created_time,"
                    "creative{id,name,object_type,thumbnail_url,body,"
                    "object_story_spec,asset_feed_spec}"
                )
            },
        )
        if "error" in creative_payload:
            creatives_out.append({
                "ad_id": ad_id,
                "ad_name": ad.get("name"),
                "status": ad.get("status"),
                "effective_status": ad.get("effective_status"),
                "error": creative_payload["error"],
            })
            errors.append(f"creative {ad.get('name')}: {creative_payload['error']}")
            continue
        creative = creative_payload.get("creative") or {}
        snippet = body_snippet(creative)
        creatives_out.append({
            "ad_id": ad_id,
            "ad_name": ad.get("name"),
            "status": ad.get("status"),
            "effective_status": ad.get("effective_status"),
            "created_time": ad.get("created_time"),
            "creative_id": creative.get("id"),
            "creative_name": creative.get("name"),
            "body_snippet": snippet,
            "creative": creative,
        })

    save(OUT / f"{CID}_creatives.json", {"data": creatives_out, "fetched_at": fetched_at})
    files.append({"path": f"data/meta_fetch/active/{CID}_creatives.json", "content": "creatives + body snippets", "rows": len(creatives_out)})

    key_numbers = {
        "campaign_id": CID,
        "campaign_name": "Chien dich pheu - target tin nhan",
        "windows": {},
    }
    delivering_today = []

    for label, (since, until, is_partial) in WINDOWS.items():
        tr = json.dumps({"since": since, "until": until})
        camp = api_get(f"{CID}/insights", {"fields": CAMP_FIELDS, "time_range": tr})
        camp_path = OUT / f"{CID}_insights_{label}_{since}_{until}.json"
        save(camp_path, camp)
        if "error" in camp:
            errors.append(f"campaign {label}: {camp['error']}")
            camp_metrics = {"error": camp["error"]}
        else:
            rows = camp.get("data") or []
            row = rows[0] if rows else {}
            camp_metrics = extract_metrics(row) if row else {"note": "no_data"}
            files.append({"path": str(camp_path.relative_to(_ROOT)).replace("\\", "/"), "content": f"campaign insights {label}", "rows": len(rows)})

        ad_ins = api_get(f"{CID}/insights", {"fields": AD_FIELDS, "level": "ad", "time_range": tr})
        ad_path = OUT / f"{CID}_ad_insights_{label}_{since}_{until}.json"
        save(ad_path, ad_ins)
        ads_metrics = []
        if "error" in ad_ins:
            errors.append(f"ad {label}: {ad_ins['error']}")
        else:
            for row in ad_ins.get("data") or []:
                aid = row.get("ad_id")
                st = ad_status.get(aid, {})
                m = {
                    "ad_id": aid,
                    "ad_name": row.get("ad_name"),
                    "adset_id": row.get("adset_id"),
                    "adset_name": row.get("adset_name"),
                    "status": st.get("status"),
                    "effective_status": st.get("effective_status"),
                    "created_time": st.get("created_time"),
                    **extract_metrics(row),
                }
                ads_metrics.append(m)
                if label == "today" and m.get("spend", 0) > 0:
                    delivering_today.append({
                        "ad_id": aid,
                        "ad_name": row.get("ad_name"),
                        "spend": m["spend"],
                        "mess": m["mess"],
                        "effective_status": st.get("effective_status"),
                    })
            files.append({"path": str(ad_path.relative_to(_ROOT)).replace("\\", "/"), "content": f"ad insights {label}", "rows": len(ad_ins.get("data") or [])})

        key_numbers["windows"][label] = {
            "since": since,
            "until": until,
            "partial_day": is_partial,
            "campaign": camp_metrics,
            "ads": ads_metrics,
        }

    l7_since, l7_until, _ = WINDOWS["last_7d"]
    tr7 = json.dumps({"since": l7_since, "until": l7_until})

    camp7 = api_get(f"{CID}/insights", {"fields": CAMP_FIELDS, "time_range": tr7})
    save(OUT / f"{CID}_insights.json", camp7)
    files.append({"path": f"data/meta_fetch/active/{CID}_insights.json", "content": "campaign insights last_7d canonical", "rows": len(camp7.get("data") or [])})

    ad7 = api_get(f"{CID}/insights", {"fields": AD_FIELDS, "level": "ad", "time_range": tr7})
    save(OUT / f"{CID}_ad_insights.json", ad7)
    files.append({"path": f"data/meta_fetch/active/{CID}_ad_insights.json", "content": "ad insights last_7d canonical", "rows": len(ad7.get("data") or [])})

    daily = api_get(f"{CID}/insights", {"fields": CAMP_FIELDS, "time_range": tr7, "time_increment": "1"})
    save(OUT / f"{CID}_daily.json", daily)
    if "error" in daily:
        errors.append(f"daily: {daily['error']}")
    else:
        files.append({"path": f"data/meta_fetch/active/{CID}_daily.json", "content": "campaign daily last_7d", "rows": len(daily.get("data") or [])})

    ad_daily = api_get(f"{CID}/insights", {"fields": AD_FIELDS, "level": "ad", "time_range": tr7, "time_increment": "1"})
    save(OUT / f"{CID}_ad_daily.json", ad_daily)
    if "error" in ad_daily:
        errors.append(f"ad_daily: {ad_daily['error']}")
    else:
        files.append({"path": f"data/meta_fetch/active/{CID}_ad_daily.json", "content": "ad daily last_7d", "rows": len(ad_daily.get("data") or [])})

    placement = api_get(
        f"{CID}/insights",
        {
            "fields": "spend,impressions,reach,frequency,clicks,ctr,actions,cost_per_action_type",
            "time_range": tr7,
            "time_increment": "1",
            "breakdowns": "publisher_platform",
        },
    )
    save(OUT / f"{CID}_placement_daily.json", placement)
    if "error" in placement:
        errors.append(f"placement_daily: {placement['error']}")
    else:
        files.append({"path": f"data/meta_fetch/active/{CID}_placement_daily.json", "content": "placement daily publisher_platform", "rows": len(placement.get("data") or [])})

    data_status = "ok"
    if errors:
        data_status = "partial"
    for e in errors:
        s = str(e)
        if "190" in s or "Session has expired" in s or "463" in s:
            data_status = "unavailable"
            break

    active_creative_snips = []
    for c in creatives_out:
        if c.get("effective_status") in ("ACTIVE", "PENDING_REVIEW", "PREAPPROVED") or c.get("status") == "ACTIVE":
            active_creative_snips.append({
                "ad_id": c.get("ad_id"),
                "ad_name": c.get("ad_name"),
                "status": c.get("status"),
                "effective_status": c.get("effective_status"),
                "body_snippet": (c.get("body_snippet") or "")[:300],
            })

    decision_names = ("noi so", "nỗi sợ", "narrow", "return to love")
    all_snips_for_decision = []
    for c in creatives_out:
        name_l = (c.get("ad_name") or "").lower()
        if any(k in name_l for k in decision_names) or "sợ" in name_l or "so" in name_l:
            # include all ads that look like decision candidates; filter more tightly below via print
            all_snips_for_decision.append({
                "ad_id": c.get("ad_id"),
                "ad_name": c.get("ad_name"),
                "status": c.get("status"),
                "effective_status": c.get("effective_status"),
                "body_snippet": (c.get("body_snippet") or "")[:400],
            })

    # Prefer including every ad with creative snippet for analyst SKU check
    all_ad_snips = [{
        "ad_id": c.get("ad_id"),
        "ad_name": c.get("ad_name"),
        "status": c.get("status"),
        "effective_status": c.get("effective_status"),
        "body_snippet": (c.get("body_snippet") or "")[:400],
    } for c in creatives_out]

    camp_name = "Chiến dịch phễu - target tin nhắn"
    key_numbers["campaign_name"] = camp_name

    manifest = {
        "purpose": "2-ad pair decision: (A) Noi so + Noi so 3 vs (B) Noi so + T Narrow new; OOS Return to Love / Noi so 3 SKU check",
        "date_range": {
            "today": ["2026-07-14", "2026-07-14"],
            "yesterday": ["2026-07-13", "2026-07-13"],
            "last_3d": ["2026-07-12", "2026-07-14"],
            "last_7d": ["2026-07-08", "2026-07-14"],
        },
        "notes": {
            "today_partial": True,
            "last_3d_includes_today_partial": True,
            "last_7d_includes_today_partial": True,
        },
        "account": ACCOUNT,
        "campaign_id": CID,
        "campaign_name": camp_name,
        "data_status": data_status,
        "fetched_at": fetched_at,
        "source": "graph_api_v21",
        "ads_adsets": {
            "ads": [{
                "id": a.get("id"),
                "name": a.get("name"),
                "status": a.get("status"),
                "effective_status": a.get("effective_status"),
                "created_time": a.get("created_time"),
                "adset_id": a.get("adset_id"),
            } for a in (ads.get("data") or [])],
            "adsets": ([{
                "id": a.get("id"),
                "name": a.get("name"),
                "status": a.get("status"),
                "effective_status": a.get("effective_status"),
                "created_time": a.get("created_time"),
            } for a in (adsets.get("data") or [])] if "error" not in adsets else []),
        },
        "active_creative_snippets": active_creative_snips,
        "all_ad_creative_snippets": all_ad_snips,
        "delivering_today": delivering_today,
        "key_numbers": key_numbers,
        "files": files,
        "errors": errors if errors else "none",
    }
    manifest_path = _ROOT / "data/meta_fetch/fetch_manifest_pheu_2026-07-14_decision.json"
    save(manifest_path, manifest)

    print("MANIFEST", manifest_path)
    print("data_status", data_status)
    print("errors", errors if errors else "none")
    print("ADS:")
    for a in ads.get("data") or []:
        print(f"  {a.get('id')} | {a.get('name')} | {a.get('status')} | {a.get('effective_status')} | {(a.get('created_time') or '')[:10]}")
    print("DELIVERING TODAY:", json.dumps(delivering_today, ensure_ascii=False))
    for label, w in key_numbers["windows"].items():
        print(f"\n=== {label} {w['since']}->{w['until']} partial={w['partial_day']} ===")
        camp = w["campaign"]
        if isinstance(camp, dict) and "error" not in camp and "note" not in camp:
            print("  CAMP:", {k: camp.get(k) for k in ("spend","mess","cost_per_mess","frequency","reach","impressions","ctr","link_click")})
        else:
            print("  CAMP:", camp)
        for a in w.get("ads") or []:
            print(f"  AD {a.get('ad_name')}: spend={a.get('spend')} mess={a.get('mess')} cpm={a.get('cost_per_mess')} freq={a.get('frequency')} reach={a.get('reach')} imps={a.get('impressions')} ctr={a.get('ctr')} link={a.get('link_click')} status={a.get('effective_status')}")
    print("\nCREATIVE SNIPPETS:")
    for s in all_ad_snips:
        print(f"  {s['ad_name']} [{s['effective_status']}]: {(s.get('body_snippet') or '')[:220]}")
    return 0 if data_status != "unavailable" else 1


if __name__ == "__main__":
    raise SystemExit(main())

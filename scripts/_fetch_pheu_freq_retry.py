"""One-shot retry fetch for pheu frequency diagnosis (read-only Graph API)."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
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
ACCOUNT = "act_400356462876861"
PHEU_HINT = "120253285175280110"
API = "https://graph.facebook.com/v21.0"

CAMP_FIELDS = (
    "campaign_name,campaign_id,spend,impressions,reach,frequency,"
    "clicks,ctr,cpc,cpm,actions,cost_per_action_type"
)
AD_FIELDS_INSIGHTS = (
    "ad_id,ad_name,adset_id,adset_name,spend,impressions,reach,frequency,"
    "clicks,ctr,cpc,cpm,actions,cost_per_action_type"
)
ADSET_FIELDS_INSIGHTS = (
    "adset_id,adset_name,spend,impressions,reach,frequency,"
    "clicks,ctr,cpc,cpm,actions,cost_per_action_type"
)
RANGES = {
    "last_7d": ("2026-07-07", "2026-07-13"),
    "mtd": ("2026-07-01", "2026-07-13"),
    "verdict": ("2026-07-11", "2026-07-13"),
}


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
        "fetched_at": date.today().isoformat(),
    }
    save(_ROOT / "data/run_meta_blocked/fetch_error.json", blocked)
    print("BLOCKED:", json.dumps(blocked, ensure_ascii=False)[:500])


def action_val(actions: list | None, action_type: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == action_type:
            return int(float(a.get("value", 0)))
    return 0


def extract_key(row: dict) -> dict:
    spend = float(row.get("spend", 0) or 0)
    mess = action_val(
        row.get("actions"), "onsite_conversion.messaging_conversation_started_7d"
    )
    first = action_val(
        row.get("actions"), "onsite_conversion.messaging_first_reply"
    )
    d2 = action_val(
        row.get("actions"), "onsite_conversion.messaging_user_depth_2_message_send"
    )
    d3 = action_val(
        row.get("actions"), "onsite_conversion.messaging_user_depth_3_message_send"
    )
    d5 = action_val(
        row.get("actions"), "onsite_conversion.messaging_user_depth_5_message_send"
    )
    reach = int(float(row.get("reach", 0) or 0))
    impressions = int(float(row.get("impressions", 0) or 0))
    freq = row.get("frequency")
    freq_f = float(freq) if freq not in (None, "") else (
        round(impressions / reach, 4) if reach else None
    )
    return {
        "spend": round(spend, 2),
        "impressions": impressions,
        "reach": reach,
        "frequency": freq_f,
        "ctr": float(row.get("ctr", 0) or 0),
        "cpc": float(row.get("cpc", 0) or 0) if row.get("cpc") else None,
        "cpm": float(row.get("cpm", 0) or 0) if row.get("cpm") else None,
        "messaging_conversation_started_7d": mess,
        "messaging_first_reply": first,
        "depth_2": d2,
        "depth_3": d3,
        "depth_5": d5,
        "cost_per_mess": round(spend / mess, 2) if mess else None,
    }


def main() -> int:
    if not TOKEN:
        print("META_ACCESS_TOKEN missing")
        return 2

    out = _ROOT / "data/meta_fetch"
    active = out / "active"
    files: list[dict] = []
    errors: list[str] = []

    me = api_get("me", {"fields": "id,name"})
    if "error" in me:
        write_blocked(me["error"])
        return 1

    acct = api_get(ACCOUNT, {"fields": "id,name,account_status,currency"})
    if "error" in acct:
        write_blocked(acct["error"])
        return 1
    save(out / "account_info.json", acct)
    files.append({"path": "data/meta_fetch/account_info.json", "content": "account info", "keys": list(acct.keys())})

    camps = api_get(
        f"{ACCOUNT}/campaigns",
        {
            "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,created_time",
            "filtering": json.dumps(
                [{"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]}]
            ),
            "limit": 50,
        },
    )
    if "error" in camps:
        write_blocked(camps["error"])
        return 1
    save(out / "active_campaigns.json", camps)
    files.append(
        {
            "path": "data/meta_fetch/active_campaigns.json",
            "content": "ACTIVE campaigns list",
            "rows": len(camps.get("data") or []),
        }
    )

    pheu_id = None
    pheu_name = None
    for c in camps.get("data") or []:
        name = c.get("name") or ""
        cid = c.get("id")
        if cid == PHEU_HINT:
            pheu_id = cid
            pheu_name = name
            break
    if pheu_id is None:
        for c in camps.get("data") or []:
            name = (c.get("name") or "").lower()
            if "tin nhan" in name or "tinnhan" in name.replace(" ", "") or "tin nhắn" in (c.get("name") or "").lower():
                pheu_id = c.get("id")
                pheu_name = c.get("name")
                break
    if pheu_id is None:
        pheu_id = PHEU_HINT
        pheu_name = "(not in ACTIVE list — using hint ID)"

    print(f"PHEU_ID={pheu_id} NAME={pheu_name}")
    print("ACTIVE:")
    for c in camps.get("data") or []:
        print(f"  {c.get('id')} | {c.get('name')} | {c.get('effective_status')}")

    key_numbers: dict = {"campaign_id": pheu_id, "campaign_name": pheu_name, "ranges": {}}

    for label, (since, until) in RANGES.items():
        tr = json.dumps({"since": since, "until": until})
        payload = api_get(
            f"{pheu_id}/insights",
            {"fields": CAMP_FIELDS, "time_range": tr},
        )
        fname = active / f"{pheu_id}_insights_{label}_{since}_{until}.json"
        save(fname, payload)
        if "error" in payload:
            errors.append(f"{label} insights: {payload['error']}")
            key_numbers["ranges"][label] = {"error": payload["error"]}
        else:
            row = (payload.get("data") or [{}])[0]
            key_numbers["ranges"][label] = extract_key(row)
            files.append(
                {
                    "path": str(fname.relative_to(_ROOT)).replace("\\", "/"),
                    "content": f"pheu campaign insights {label}",
                    "rows": len(payload.get("data") or []),
                }
            )

    mtd_since, mtd_until = RANGES["mtd"]
    mtd_payload = api_get(
        f"{pheu_id}/insights",
        {
            "fields": CAMP_FIELDS,
            "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
        },
    )
    save(active / f"{pheu_id}_insights.json", mtd_payload)
    files.append(
        {
            "path": f"data/meta_fetch/active/{pheu_id}_insights.json",
            "content": "pheu campaign insights MTD (canonical)",
            "rows": len(mtd_payload.get("data") or []),
        }
    )

    daily = api_get(
        f"{pheu_id}/insights",
        {
            "fields": CAMP_FIELDS,
            "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
            "time_increment": "1",
        },
    )
    save(active / f"{pheu_id}_daily.json", daily)
    if "error" in daily:
        errors.append(f"daily: {daily['error']}")
    else:
        daily_keys = []
        for row in daily.get("data") or []:
            daily_keys.append({"date": row.get("date_start"), **extract_key(row)})
        key_numbers["daily"] = daily_keys
        files.append(
            {
                "path": f"data/meta_fetch/active/{pheu_id}_daily.json",
                "content": "pheu daily insights MTD (freq/reach/impressions/spend/mess)",
                "rows": len(daily.get("data") or []),
            }
        )

    l7_since, l7_until = RANGES["last_7d"]
    daily_l7 = api_get(
        f"{pheu_id}/insights",
        {
            "fields": CAMP_FIELDS,
            "time_range": json.dumps({"since": l7_since, "until": l7_until}),
            "time_increment": "1",
        },
    )
    save(active / f"{pheu_id}_daily_last7d.json", daily_l7)
    files.append(
        {
            "path": f"data/meta_fetch/active/{pheu_id}_daily_last7d.json",
            "content": "pheu daily last 7d",
            "rows": len(daily_l7.get("data") or []),
        }
    )

    placement = api_get(
        f"{pheu_id}/insights",
        {
            "fields": "spend,impressions,reach,frequency,clicks,ctr,actions,cost_per_action_type",
            "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
            "time_increment": "1",
            "breakdowns": "publisher_platform",
        },
    )
    save(active / f"{pheu_id}_placement_daily.json", placement)
    if "error" in placement:
        errors.append(f"placement_daily: {placement['error']}")
    else:
        files.append(
            {
                "path": f"data/meta_fetch/active/{pheu_id}_placement_daily.json",
                "content": "pheu placement daily (publisher_platform)",
                "rows": len(placement.get("data") or []),
            }
        )

    adsets = api_get(
        f"{pheu_id}/adsets",
        {
            "fields": "id,name,status,effective_status,daily_budget,lifetime_budget,optimization_goal,created_time",
            "limit": 50,
        },
    )
    save(active / f"{pheu_id}_adsets.json", adsets)
    files.append(
        {
            "path": f"data/meta_fetch/active/{pheu_id}_adsets.json",
            "content": "pheu adsets",
            "rows": len(adsets.get("data") or []),
        }
    )

    ads = api_get(
        f"{pheu_id}/ads",
        {
            "fields": "id,name,status,effective_status,created_time",
            "limit": 50,
        },
    )
    save(active / f"{pheu_id}_ads.json", ads)
    files.append(
        {
            "path": f"data/meta_fetch/active/{pheu_id}_ads.json",
            "content": "pheu ads list",
            "rows": len(ads.get("data") or []),
        }
    )

    # ad statuses for key numbers
    ad_status_map = {a.get("id"): a for a in (ads.get("data") or [])}

    key_numbers["adsets"] = {}
    for label, (since, until) in RANGES.items():
        adset_ins = api_get(
            f"{pheu_id}/insights",
            {
                "fields": ADSET_FIELDS_INSIGHTS,
                "level": "adset",
                "time_range": json.dumps({"since": since, "until": until}),
            },
        )
        fname = active / f"{pheu_id}_adset_insights_{label}.json"
        save(fname, adset_ins)
        if "error" in adset_ins:
            errors.append(f"adset {label}: {adset_ins['error']}")
        else:
            rows_out = []
            for row in adset_ins.get("data") or []:
                rows_out.append(
                    {
                        "adset_id": row.get("adset_id"),
                        "adset_name": row.get("adset_name"),
                        **extract_key(row),
                    }
                )
            key_numbers["adsets"][label] = rows_out
            files.append(
                {
                    "path": str(fname.relative_to(_ROOT)).replace("\\", "/"),
                    "content": f"pheu adset insights {label}",
                    "rows": len(adset_ins.get("data") or []),
                }
            )

    save(
        active / f"{pheu_id}_adset_insights.json",
        api_get(
            f"{pheu_id}/insights",
            {
                "fields": ADSET_FIELDS_INSIGHTS,
                "level": "adset",
                "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
            },
        ),
    )

    key_numbers["ads"] = {}
    for label, (since, until) in RANGES.items():
        ad_ins = api_get(
            f"{pheu_id}/insights",
            {
                "fields": AD_FIELDS_INSIGHTS,
                "level": "ad",
                "time_range": json.dumps({"since": since, "until": until}),
            },
        )
        fname = active / f"{pheu_id}_ad_insights_{label}.json"
        save(fname, ad_ins)
        if "error" in ad_ins:
            errors.append(f"ad {label}: {ad_ins['error']}")
        else:
            rows_out = []
            for row in ad_ins.get("data") or []:
                aid = row.get("ad_id")
                st = ad_status_map.get(aid, {})
                rows_out.append(
                    {
                        "ad_id": aid,
                        "ad_name": row.get("ad_name"),
                        "adset_name": row.get("adset_name"),
                        "status": st.get("status"),
                        "effective_status": st.get("effective_status"),
                        **extract_key(row),
                    }
                )
            key_numbers["ads"][label] = rows_out
            files.append(
                {
                    "path": str(fname.relative_to(_ROOT)).replace("\\", "/"),
                    "content": f"pheu ad insights {label}",
                    "rows": len(ad_ins.get("data") or []),
                }
            )

    ad_ins_mtd = api_get(
        f"{pheu_id}/insights",
        {
            "fields": AD_FIELDS_INSIGHTS,
            "level": "ad",
            "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
        },
    )
    save(active / f"{pheu_id}_ad_insights.json", ad_ins_mtd)
    files.append(
        {
            "path": f"data/meta_fetch/active/{pheu_id}_ad_insights.json",
            "content": "pheu ad insights MTD canonical",
            "rows": len(ad_ins_mtd.get("data") or []),
        }
    )

    ad_daily = api_get(
        f"{pheu_id}/insights",
        {
            "fields": AD_FIELDS_INSIGHTS,
            "level": "ad",
            "time_range": json.dumps({"since": mtd_since, "until": mtd_until}),
            "time_increment": "1",
        },
    )
    save(active / f"{pheu_id}_ad_daily.json", ad_daily)
    if "error" in ad_daily:
        errors.append(f"ad_daily: {ad_daily['error']}")
    else:
        files.append(
            {
                "path": f"data/meta_fetch/active/{pheu_id}_ad_daily.json",
                "content": "pheu ad daily MTD",
                "rows": len(ad_daily.get("data") or []),
            }
        )

    for label, (since, until) in RANGES.items():
        a_ins = api_get(
            f"{ACCOUNT}/insights",
            {
                "fields": CAMP_FIELDS,
                "time_range": json.dumps({"since": since, "until": until}),
            },
        )
        fname = out / f"account_insights_{label}_{since}_{until}.json"
        save(fname, a_ins)
        files.append(
            {
                "path": str(fname.relative_to(_ROOT)).replace("\\", "/"),
                "content": f"account insights {label}",
                "rows": len(a_ins.get("data") or []),
            }
        )

    data_status = "ok"
    if errors:
        data_status = "partial"
    for e in errors:
        if "190" in str(e) or "Session has expired" in str(e) or "463" in str(e):
            data_status = "unavailable"
            break

    manifest = {
        "date_range": {
            "last_7d": list(RANGES["last_7d"]),
            "mtd": list(RANGES["mtd"]),
            "verdict": list(RANGES["verdict"]),
            "today": "2026-07-13",
        },
        "account": ACCOUNT,
        "data_status": data_status,
        "pheu_campaign_id": pheu_id,
        "pheu_campaign_name": pheu_name,
        "active_campaigns": [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "effective_status": c.get("effective_status"),
            }
            for c in (camps.get("data") or [])
        ],
        "files": files,
        "key_numbers": key_numbers,
        "errors": errors or "none",
        "source": "graph_api_v21",
        "fetched_at": date.today().isoformat(),
    }
    save(out / "fetch_manifest_pheu_freq_2026-07-13.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if data_status != "unavailable" else 1


if __name__ == "__main__":
    raise SystemExit(main())

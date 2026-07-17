"""One-shot fresh Meta fetch for 2026-07-14 analysis (read-only Graph API)."""
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
ACCOUNT = "act_400356462876861"
OUT = _ROOT / "data" / "meta_fetch"
ACTIVE = OUT / "active"
BLOCKED = _ROOT / "data" / "run_meta_blocked"

RANGES = {
    "7d": ("2026-07-08", "2026-07-14"),
    "verdict": ("2026-07-12", "2026-07-13"),
    "mtd": ("2026-07-01", "2026-07-14"),
}
PRIMARY = RANGES["7d"]

EXPECTED = {
    "120253285175280110": "phieu_tinnhan",
    "120252531135370110": "profile_1806",
    "120252990977040110": "retarget",
}

INSIGHT_FIELDS = (
    "campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,"
    "actions,cost_per_action_type"
)
AD_INSIGHT_FIELDS = (
    "ad_id,ad_name,spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,"
    "actions,cost_per_action_type"
)
ADSET_INSIGHT_FIELDS = (
    "adset_id,adset_name,spend,impressions,reach,frequency,clicks,ctr,cpc,"
    "actions,cost_per_action_type"
)
ADSET_FIELDS = (
    "id,name,status,effective_status,daily_budget,lifetime_budget,"
    "optimization_goal,targeting,created_time"
)
AD_FIELDS = "id,name,status,effective_status,created_time,updated_time"
CAMP_DETAIL_FIELDS = (
    "id,name,status,effective_status,objective,daily_budget,lifetime_budget,"
    "created_time,updated_time,buying_type,special_ad_categories"
)

errors: list[str] = []
files: list[dict] = []


def api_get(path: str, params: dict) -> dict:
    params = {**params, "access_token": TOKEN}
    url = f"https://graph.facebook.com/v21.0/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=90) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except Exception:
            payload = {"error": {"message": body, "code": e.code}}
        err = payload.get("error") or {}
        raise RuntimeError(json.dumps(err, ensure_ascii=False)) from None
    if "error" in payload:
        raise RuntimeError(json.dumps(payload["error"], ensure_ascii=False))
    return payload


def save(path: Path, data) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    keys = list(data.keys()) if isinstance(data, dict) else type(data).__name__
    rows = len(data.get("data") or []) if isinstance(data, dict) else 0
    files.append(
        {
            "path": str(path.relative_to(_ROOT)).replace("\\", "/"),
            "rows": rows,
            "keys": keys,
            "content": path.name,
        }
    )
    return data


def action_val(actions, t: str) -> int:
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") == t:
            return int(float(a.get("value", 0)))
    return 0


def row_metrics(row: dict | None) -> dict | None:
    if not row:
        return None
    started = action_val(
        row.get("actions"), "onsite_conversion.messaging_conversation_started_7d"
    )
    spend = float(row.get("spend", 0) or 0)
    freq = row.get("frequency")
    return {
        "spend_vnd": round(spend),
        "messaging_started_7d": started,
        "cost_per_mess": round(spend / started) if started else None,
        "frequency": float(freq) if freq not in (None, "") else None,
        "ctr_pct": round(float(row.get("ctr", 0) or 0), 2),
        "link_click": action_val(row.get("actions"), "link_click"),
        "impressions": int(row.get("impressions", 0) or 0),
        "reach": int(row.get("reach", 0) or 0),
        "clicks": int(row.get("clicks", 0) or 0),
        "first_reply": action_val(
            row.get("actions"), "onsite_conversion.messaging_first_reply"
        ),
        "depth_3": action_val(
            row.get("actions"), "onsite_conversion.messaging_user_depth_3_message_send"
        ),
        "lead": action_val(row.get("actions"), "lead"),
    }


def is_token_error(err_obj: dict) -> bool:
    msg = (err_obj.get("message") or "").lower()
    return (
        err_obj.get("code") == 190
        or err_obj.get("error_subcode") == 463
        or "expired" in msg
        or "validating access token" in msg
    )


def fail_unavailable(err_obj: dict) -> None:
    save(
        BLOCKED / "fetch_error.json",
        {
            "error": err_obj.get("message"),
            "error_code": err_obj.get("code"),
            "error_subcode": err_obj.get("error_subcode"),
            "action": (
                "Refresh META_ACCESS_TOKEN in .env "
                "(or Pipeboard token in .cursor/mcp.json), then re-run fetch."
            ),
            "fetched_at": "2026-07-14",
        },
    )
    manifest = {
        "date_ranges": {
            "primary_7d": {"since": RANGES["7d"][0], "until": RANGES["7d"][1]},
            "verdict_window": {
                "since": RANGES["verdict"][0],
                "until": RANGES["verdict"][1],
            },
            "mtd": {"since": RANGES["mtd"][0], "until": RANGES["mtd"][1]},
        },
        "account": ACCOUNT,
        "data_status": "unavailable",
        "files": files,
        "errors": [err_obj],
        "campaigns": [],
    }
    save(OUT / "fetch_manifest_2026-07-08_2026-07-14.json", manifest)
    save(OUT / "fetch_manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    raise SystemExit(1)


def main() -> None:
    if not TOKEN:
        fail_unavailable({"message": "META_ACCESS_TOKEN missing", "code": None})

    try:
        camps = api_get(
            f"{ACCOUNT}/campaigns",
            {
                "fields": CAMP_DETAIL_FIELDS,
                "filtering": json.dumps(
                    [
                        {
                            "field": "effective_status",
                            "operator": "IN",
                            "value": ["ACTIVE"],
                        }
                    ]
                ),
                "limit": 50,
            },
        )
    except RuntimeError as e:
        try:
            err_obj = json.loads(str(e))
        except Exception:
            err_obj = {"message": str(e)}
        fail_unavailable(err_obj)

    save(OUT / "campaigns_active.json", camps)
    active = camps.get("data") or []
    print(f"ACTIVE count: {len(active)}")
    for c in active:
        print(f"  {c.get('id')} | {c.get('effective_status')} | {c.get('name')}")

    active_ids = {c["id"]: c for c in active}
    campaign_ids: list[tuple[str, str, str]] = []
    for cid, label in EXPECTED.items():
        if cid in active_ids:
            campaign_ids.append((cid, label, active_ids[cid].get("name") or ""))
        else:
            errors.append(f"MISSING_ACTIVE:{label}:{cid}")
            campaign_ids.append(
                (cid, label, "(not in ACTIVE list — fetching by expected id)")
            )

    expected_set = {c[0] for c in campaign_ids}
    for aid, crow in active_ids.items():
        if aid not in expected_set:
            errors.append(f"UNEXPECTED_ACTIVE:{aid}:{crow.get('name')}")
            campaign_ids.append((aid, "other_active", crow.get("name") or ""))

    for label, (since, until) in RANGES.items():
        tr = json.dumps({"since": since, "until": until})
        try:
            acct = api_get(
                f"{ACCOUNT}/insights",
                {
                    "fields": INSIGHT_FIELDS.replace("campaign_name,", ""),
                    "time_range": tr,
                },
            )
            save(OUT / f"account_insights_{label}_{since}_{until}.json", acct)
        except RuntimeError as e:
            try:
                err_obj = json.loads(str(e))
            except Exception:
                err_obj = {"message": str(e)}
            if is_token_error(err_obj):
                fail_unavailable(err_obj)
            errors.append(f"account_insights_{label}:{e}")

    tr7 = json.dumps({"since": PRIMARY[0], "until": PRIMARY[1]})
    for bd in ("age", "gender"):
        try:
            payload = api_get(
                f"{ACCOUNT}/insights",
                {
                    "fields": (
                        "spend,impressions,reach,clicks,ctr,actions,"
                        "cost_per_action_type"
                    ),
                    "time_range": tr7,
                    "breakdowns": bd,
                },
            )
            save(OUT / f"account_{bd}_7d.json", payload)
        except RuntimeError as e:
            errors.append(f"account_{bd}:{e}")

    summary_campaigns: list[dict] = []

    for cid, label, cname in campaign_ids:
        print(f"Fetching {cid} {label}")
        camp_summary: dict = {
            "id": cid,
            "label": label,
            "name": cname,
            "windows": {},
            "ads_active": [],
            "ad_insights": {},
            "errors": [],
        }

        try:
            details = api_get(cid, {"fields": CAMP_DETAIL_FIELDS})
            save(ACTIVE / f"{cid}_details.json", details)
        except RuntimeError as e:
            camp_summary["errors"].append(f"details:{e}")
            errors.append(f"{cid}_details:{e}")

        try:
            adsets = api_get(f"{cid}/adsets", {"fields": ADSET_FIELDS, "limit": 50})
            save(ACTIVE / f"{cid}_adsets.json", adsets)
        except RuntimeError as e:
            adsets = {"data": []}
            camp_summary["errors"].append(f"adsets:{e}")
            errors.append(f"{cid}_adsets:{e}")

        try:
            ads = api_get(f"{cid}/ads", {"fields": AD_FIELDS, "limit": 50})
            save(ACTIVE / f"{cid}_ads.json", ads)
            for a in ads.get("data") or []:
                if a.get("effective_status") == "ACTIVE" or a.get("status") == "ACTIVE":
                    camp_summary["ads_active"].append(
                        {
                            "id": a.get("id"),
                            "name": a.get("name"),
                            "effective_status": a.get("effective_status"),
                            "created_time": a.get("created_time"),
                        }
                    )
        except RuntimeError as e:
            ads = {"data": []}
            camp_summary["errors"].append(f"ads:{e}")
            errors.append(f"{cid}_ads:{e}")

        for wlabel, (since, until) in RANGES.items():
            tr = json.dumps({"since": since, "until": until})
            try:
                ins = api_get(
                    f"{cid}/insights",
                    {"fields": INSIGHT_FIELDS, "time_range": tr},
                )
                if wlabel == "7d":
                    save(ACTIVE / f"{cid}_insights.json", ins)
                save(ACTIVE / f"{cid}_insights_{wlabel}.json", ins)
                row = (ins.get("data") or [None])[0]
                camp_summary["windows"][wlabel] = row_metrics(row)
            except RuntimeError as e:
                try:
                    err_obj = json.loads(str(e))
                except Exception:
                    err_obj = {"message": str(e)}
                if is_token_error(err_obj):
                    fail_unavailable(err_obj)
                camp_summary["windows"][wlabel] = None
                camp_summary["errors"].append(f"insights_{wlabel}:{e}")
                errors.append(f"{cid}_insights_{wlabel}:{e}")

        for period_label, (since, until) in (("7d", PRIMARY), ("mtd", RANGES["mtd"])):
            tr = json.dumps({"since": since, "until": until})
            try:
                daily = api_get(
                    f"{cid}/insights",
                    {
                        "fields": INSIGHT_FIELDS,
                        "time_range": tr,
                        "time_increment": "1",
                    },
                )
                if period_label == "7d":
                    save(ACTIVE / f"{cid}_daily.json", daily)
                save(ACTIVE / f"{cid}_daily_{period_label}.json", daily)
            except RuntimeError as e:
                camp_summary["errors"].append(f"daily_{period_label}:{e}")
                errors.append(f"{cid}_daily_{period_label}:{e}")

            try:
                pld = api_get(
                    f"{cid}/insights",
                    {
                        "fields": (
                            "spend,impressions,reach,clicks,ctr,actions,frequency"
                        ),
                        "time_range": tr,
                        "time_increment": "1",
                        "breakdowns": "publisher_platform",
                    },
                )
                if period_label == "7d":
                    save(ACTIVE / f"{cid}_placement_daily.json", pld)
                save(ACTIVE / f"{cid}_placement_daily_{period_label}.json", pld)
            except RuntimeError as e:
                camp_summary["errors"].append(f"placement_daily_{period_label}:{e}")
                errors.append(f"{cid}_placement_daily_{period_label}:{e}")

        try:
            ai = api_get(
                f"{cid}/insights",
                {
                    "fields": ADSET_INSIGHT_FIELDS,
                    "level": "adset",
                    "time_range": tr7,
                },
            )
            save(ACTIVE / f"{cid}_adset_insights.json", ai)
        except RuntimeError as e:
            camp_summary["errors"].append(f"adset_insights:{e}")
            errors.append(f"{cid}_adset_insights:{e}")

        for wlabel, (since, until) in (
            ("7d", RANGES["7d"]),
            ("verdict", RANGES["verdict"]),
            ("mtd", RANGES["mtd"]),
        ):
            tr = json.dumps({"since": since, "until": until})
            try:
                ad_ins = api_get(
                    f"{cid}/insights",
                    {
                        "fields": AD_INSIGHT_FIELDS,
                        "level": "ad",
                        "time_range": tr,
                        "limit": 50,
                    },
                )
                fname = (
                    f"{cid}_ad_insights.json"
                    if wlabel == "7d"
                    else f"{cid}_ad_insights_{wlabel}.json"
                )
                save(ACTIVE / fname, ad_ins)
                ad_map = {a["id"]: a for a in (ads.get("data") or [])}
                ad_rows = []
                for r in ad_ins.get("data") or []:
                    aid = r.get("ad_id")
                    meta = ad_map.get(aid, {})
                    m = row_metrics(r) or {}
                    m["ad_id"] = aid
                    m["ad_name"] = r.get("ad_name")
                    m["effective_status"] = meta.get("effective_status")
                    m["created_time"] = meta.get("created_time")
                    ad_rows.append(m)
                camp_summary["ad_insights"][wlabel] = ad_rows
            except RuntimeError as e:
                camp_summary["errors"].append(f"ad_insights_{wlabel}:{e}")
                errors.append(f"{cid}_ad_insights_{wlabel}:{e}")

        summary_campaigns.append(camp_summary)

    new_ads_notes = []
    for cs in summary_campaigns:
        for a in cs.get("ads_active") or []:
            name = a.get("name") or ""
            lower = name.lower()
            if (
                "nỗi sợ 3" in lower
                or "noi so 3" in lower
                or "return to love" in lower
                or "nỗi sợ 3" in name
                or "Nỗi sợ 3" in name
            ):
                new_ads_notes.append({"campaign": cs["label"], "ad": a})
            if cs["label"] == "retarget":
                ct = a.get("created_time") or ""
                if ct.startswith("2026-07"):
                    new_ads_notes.append(
                        {
                            "campaign": cs["label"],
                            "ad": a,
                            "note": "created_july_2026",
                        }
                    )

    has_windows = any(c.get("windows") for c in summary_campaigns)
    if not errors:
        status = "ok"
    elif has_windows:
        status = "partial"
    else:
        status = "unavailable"

    account_metrics = {}
    for wlabel, (since, until) in RANGES.items():
        path = OUT / f"account_insights_{wlabel}_{since}_{until}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            row = (data.get("data") or [None])[0]
            account_metrics[wlabel] = row_metrics(row)

    manifest = {
        "fetched_at": "2026-07-14T10:30:00+07:00",
        "account": ACCOUNT,
        "date_ranges": {
            "primary_7d": {"since": RANGES["7d"][0], "until": RANGES["7d"][1]},
            "verdict_window": {
                "since": RANGES["verdict"][0],
                "until": RANGES["verdict"][1],
                "note": "last 2 full days (14 may be partial)",
            },
            "mtd": {"since": RANGES["mtd"][0], "until": RANGES["mtd"][1]},
        },
        "data_status": status,
        "active_campaigns_confirmed": [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "effective_status": c.get("effective_status"),
                "daily_budget": c.get("daily_budget"),
                "objective": c.get("objective"),
            }
            for c in active
        ],
        "account_metrics": account_metrics,
        "campaigns": summary_campaigns,
        "new_ads_notes": new_ads_notes,
        "files": files,
        "errors": errors if errors else None,
    }
    save(OUT / "fetch_manifest_2026-07-08_2026-07-14.json", manifest)
    save(OUT / "fetch_manifest.json", manifest)

    print("=== MANIFEST SUMMARY ===")
    print(f"data_status: {status}")
    print(f"errors: {errors if errors else 'none'}")
    print(f"files_saved: {len(files)}")
    for cs in summary_campaigns:
        print(f"--- {cs['id']} {cs['label']} {cs['name']}")
        for w, m in (cs.get("windows") or {}).items():
            print(f"  {w}: {m}")
        print(f"  ACTIVE ads: {len(cs.get('ads_active') or [])}")
        for a in cs.get("ads_active") or []:
            print(f"    {a.get('id')} | {a.get('name')} | {a.get('created_time')}")


if __name__ == "__main__":
    main()

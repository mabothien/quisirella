"""Validate fetch manifest and inventory counts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ACTIVE = [
    "120253285175280110",
    "120252531135370110",
    "120252990977040110",
]


def main() -> None:
    since, until = "2026-07-01", sys.argv[1] if len(sys.argv) > 1 else "2026-07-10"
    manifest_path = Path(f"data/meta_fetch/fetch_manifest_{since}_{until}.json")
    active = Path("data/meta_fetch/active")
    finance = Path("data/finance_fetch/bao_gia_2026_summary.json")

    checks: list[dict] = []
    ok = True

    if manifest_path.exists():
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
        checks.append(
            {
                "check": "manifest_date_range",
                "pass": m.get("since") == since and m.get("until") == until,
                "detail": f"{m.get('since')} → {m.get('until')}",
            }
        )
    else:
        checks.append({"check": "manifest_date_range", "pass": False, "detail": "missing"})
        ok = False

    for cid in ACTIVE:
        for suffix in ("_insights.json", "_adsets.json", "_ads.json", "_daily.json"):
            p = active / f"{cid}{suffix}"
            exists = p.exists()
            if not exists:
                ok = False
            row_count = 0
            if exists:
                payload = json.loads(p.read_text(encoding="utf-8"))
                row_count = len(payload.get("data") or [])
            checks.append(
                {
                    "check": f"{cid}{suffix}",
                    "pass": exists and row_count > 0,
                    "detail": f"rows={row_count}" if exists else "missing",
                }
            )

    pheu_adsets = active / "120253285175280110_adsets.json"
    if pheu_adsets.exists():
        n = len(json.loads(pheu_adsets.read_text(encoding="utf-8")).get("data") or [])
        checks.append(
            {
                "check": "pheu_adsets_count",
                "pass": n >= 1,
                "detail": f"adsets={n} (expect >=1; flag if AM has more after split)",
            }
        )

    checks.append(
        {
            "check": "finance_summary",
            "pass": finance.exists(),
            "detail": str(finance) if finance.exists() else "missing",
        }
    )

    for c in checks:
        if not c["pass"]:
            ok = False

    report = {"status": "ok" if ok else "partial", "checks": checks}
    out = Path("data/fetch_validation.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

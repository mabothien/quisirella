# DM Health Score (0-100) — Quisirella

Diem dinh luong **bo tro** verdict taxonomy (scale/hold/optimize/reduce/pause) — khong thay the verdict. Chi tinh khi co du lieu tu `data/meta_fetch/` hoac analyst table.

Nguon scoring: claude-ads `scoring-system.md`, adapt DM-first.

---

## Cong thuc

```
S = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
```

- PASS = 1, WARNING = 0.5, FAIL = 0, N/A = loai khoi mau so
- W_sev: Critical 5.0 | High 3.0 | Medium 1.5 | Low 0.5

---

## Trong so category (DM-first)

| Category | Weight | Checks chinh |
|---|---|---|
| Chi phi/tin nhan & funnel | 30% | chi phi/tin nhan vs nguong, engaged_rate, reply rate |
| Funnel depth & chat quality | 25% | depth_3/5, quality_mess (08) neu co |
| Creative diversity & fatigue | 20% | rubric Andromeda, CTR trend, frequency |
| Structure & pacing | 15% | learning phase, budget pacing, funnel_role dung |
| Placement & audience IG | 10% | FB spend <15%, instagram_* breakdown hop ly |

---

## Grade

| Grade | Score | Hanh dong |
|---|---|---|
| A | 90-100 | Toi uu nho |
| B | 75-89 | Co hoi cai thien |
| C | 60-74 | Can chu y |
| D | 40-59 | Van de ro |
| F | <40 | Can can thiep gap |

---

## Checks mau (theo campaign role)

### Phieu Tin nhan (top_middle)

| ID | Check | Pass | Warning | Fail |
|---|---|---|---|---|
| DM-01 | Chi phi/tin nhan | <25.000 | 25-50k | >50k |
| DM-02 | engaged_rate | ≥30% | 15-30% | <15% |
| DM-03 | Ty le tin nhan/link | ≥5% | 2-5% | <2% |
| DM-04 | Learning limited | <30% ad sets | 30-50% | >50% |
| DM-05 | Creative diversity rubric | ≥8/10 | 4-7 | <4 |
| DM-06 | FB spend share | <10% | 10-15% | >15% |

### Phieu Profile (top_only)

| ID | Check | Pass | Warning | Fail |
|---|---|---|---|---|
| PV-01 | Chi phi/visit | <1.200 | 1.2-2k | >2k |
| PV-02 | Dung chi phi/tin nhan de verdict | Khong penalize vi mess | — | Verdict sai role |
| PV-03 | Profile visit trend | On dinh/tang | Flat | Giam manh |

### Ban Retarget (bottom)

| ID | Check | Pass | Warning | Fail |
|---|---|---|---|---|
| RT-01 | CPM | ~80k ±20% | 80-120k | >120k |
| RT-02 | CTR (all) | >3% | 2-3% | <2% |
| RT-03 | Frequency/tuan | <3.5 | 3.5-5 | >5 |

---

## Quick Wins

```
IF severity IN (Critical, High) AND fix_time < 15 phut → flag Quick Win
Sort by: severity × estimated_impact DESC
```

Vi du Quisirella:
- Loai FB placement khoi ad set IG-only (neu spend >15%)
- Them 1 video 9:16 Reels vao ad set chi co static
- Cap nhat exclusion audience (neu co retarget overlap)

---

## Output trong bao cao

```markdown
## DM Health Score (bo tro)

**Score:** XX/100 (Grade: X)

| Category | Score | Weight |
|---|---|---|
| Chi phi/tin nhan & funnel | XX | 30% |
| Funnel depth | XX | 25% |
| Creative | XX | 20% |
| Structure | XX | 15% |
| Placement IG | XX | 10% |

**Quick Wins:** [list]
```

**Luu y:** Purchase/ROAS Meta khong vao score — ghi chu "khong tin cay, chot DM".

# Report Quality Gate — Quisirella output/

Run before writing any report to `output/01-06`. Deterministic checks first (fail fast, no judgment needed), rubric second. A report fails if **any dimension fails** — no averaging.

## Stage 1 — Deterministic checks

All must pass before proceeding. On failure: fix, don't ship.

| # | Check | Pass condition |
|---|---|---|
| D1 | Frontmatter complete | `title`, `generated_at`, `data_range`, `sources`, `data_status`, `ad_account_id` present (per `quisirella-meta-report-output.mdc`) |
| D2 | `data_status` valid | One of `ok` / `partial` / `unavailable`; matches reality (any failed fetch ⇒ not `ok`) |
| D3 | Number formatting | VND with dot separators (8.546.101), CTR one decimal with comma (3,57%), chi phí/tin nhắn integer |
| D4 | Traceability | Every metric exists in `data/meta_fetch/`, `data/finance_fetch/`, or the analyst's verbatim table — zero invented numbers |
| D5 | Account | `act_400356462876861` only |
| D6 | Purchase caveat | Any Meta purchase/ROAS figure carries "không phản ánh doanh thu thật (chốt DM)" |
| D7 | ROAS thuc (when finance) | ROAS thuc cites Sheet `revenue_actual` + Meta `spend` same month; Quảng cáo Sheet labeled reference-only |

## Stage 2 — Rubric (per-dimension pass/fail)

| Dimension | Pass condition | Fail examples |
|---|---|---|
| **KPI hierarchy** | Chi phí/tin nhắn is the primary metric for verdicts; funnel depth (first_reply, depth_3, depth_5) present for messaging campaigns | Verdict justified by CTR or purchase pixel alone |
| **IG-only** | Placement analysis covers `instagram_*` rows only; Facebook appears solely as "review loại FB"; creative advice follows `00-ig-ad-creative-guide.md` | Recommending creative changes based on Facebook Feed CTR |
| **Breakdown Effect** | No pause/reduce recommendation for a segment based only on higher average cost; recommendations framed as testable hypotheses; evaluation level stated (campaign vs ad set) | "Pause Reels vì CPA cao hơn Feed" without marginal/time-series reasoning |
| **Learning phase** | Campaigns/ad sets younger than ~7 days or without ~50 events carry a learning caveat; no definitive scale/pause verdict during learning | "Scale ngay" for a 3-day-old campaign without caveat |
| **Policy compliance** (only when report contains ad copy) | Copy follows `00-meta-ad-policy-ig.md`: no personal attributes, no counterfeit-adjacent wording, CTA matches DM flow | "Dành cho cô nàng sang chảnh..." in suggested caption |
| **Placement (degradation)** | Executive summary + verdicts at top; actionable recommendations at end; verdicts never buried mid-document | Key verdict only appears inside section 4 of 6 |
| **Relevance filter** | Meta recommendations labeled giữ/loại/cần kiểm chứng per `config/relevance_rules.yaml`; no cross-vertical benchmarks | Citing generic e-commerce CPM as a target |
| **Thinking gate** | Analysis applied thinking_framework.md — recommendations include measurement plan (GROW) | Recommendations with no way to verify success |
| **Health score** (when analyst provides) | DM Health Score section matches `health_score_dm.md`; supplements verdicts, does not replace funnel_role | Score contradicts verdict without explanation |

## Output of the gate

Append a short check summary when delivering (not into the report file itself):

```
Gate: D1-D6 pass. Rubric: KPI ✓, IG-only ✓, Breakdown ✓, Learning ✓ (phễu caveat added), Policy n/a, Placement ✓, Relevance ✓
```

If a dimension fails, name the fix applied before writing. Never write a failing report to `output/` — it becomes ground truth for Claude Projects and poisons every future consultation.

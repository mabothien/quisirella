# Subagent Handoff Contract — Quisirella Pipeline

Pipeline: `meta-fetcher` + `finance-fetcher` (parallel) → `meta-analyst` → `report-writer`. Each handoff is a structured artifact, never free prose containing numbers.

## Why: the telephone game problem

Supervisor/orchestrator architectures lose fidelity when agents paraphrase each other's output (LangGraph benchmarks: ~50% worse before optimization). For Quisirella the risk is concrete: "chi phi/tin nhan 16.799" becomes "~17k" becomes "17.000" in the final report — and `output/` is ground truth for Claude Projects.

**Rule: numbers cross agent boundaries only inside tables, verbatim. Downstream agents copy, never recompute.**

## Handoff 1: meta-fetcher → parent/analyst

Fetcher returns a **manifest**, not data:

```markdown
## Fetch manifest
- date_range: 2026-06-02 → 2026-07-01
- account: act_400356462876861
- files:
  | File | Content | Rows/keys |
  |---|---|---|
  | data/meta_fetch/account_insights.json | account 30d insights | 1 row |
  | data/meta_fetch/active/120253285175280110_insights.json | campaign phễu insights | 1 row |
- errors: none | <exact API error message>
- data_status: ok | partial | unavailable
```

Never paste raw JSON bodies into the response. The analyst greps/reads files itself.

## Handoff 1b: finance-fetcher → parent/analyst

```markdown
## Finance fetch manifest
- period: 2026-06
- date_range: 2026-06-01 → 2026-06-30
- files:
  | File | Content | Rows/keys |
  |---|---|---|
  | data/finance_fetch/bao_gia_2026_summary.json | parsed monthly + YTD | 7 months |
  | data/finance_fetch/manifest.json | fetch metadata | — |
- errors: none
- data_status: ok
```

Primary analyst source for revenue/profit: `bao_gia_2026_summary.json` → `months[]` where `month_key` matches period.

## Handoff 2: meta-analyst → report-writer

Analyst returns analysis with a **verbatim metrics table** as the single source of numbers.

Optional **RAG sources** (Phase C — **bắt buộc** khi có khuyến nghị policy/KPI):

```markdown
## RAG sources (policy only — not numeric)
| source_file | section_title | used_for |
|---|---|---|
| .cursor/rules/quisirella-meta-kpi.mdc | KPI hierarchy | primary metric chi phí/tin nhắn |
| output/06-active-campaigns-analysis.md | Verdicts | campaign phễu hold |
```

- List every `source_file` from `search-knowledge` chunks used for verdicts or recommendations.
- **Không** lấy số liệu từ RAG chunks — chỉ policy/context.
- Writer rejects analyst output if policy recommendations lack `rag_sources` rows.

```markdown
## Metrics (verbatim — writer copies these exactly)
| Campaign | ID | Spend | Tin nhắn | Chi phí/tin nhắn | Lead | CTR | data source |
|---|---|---|---|---|---|---|---|
| phễu - target tin nhắn | 120253285175280110 | 487.178 | 29 | 16.799 | 24 | 5,42% | active/120253285175280110_insights.json |

## Verdicts
| Campaign | Verdict | Evidence (1 line, cites table row) |

## Recommendations (testable hypotheses)
...

## Caveats
- learning phase status per campaign
- Breakdown Effect callouts
```

Requirements:

- Every number in the table traces to a file in `data/meta_fetch/` or `data/finance_fetch/` (last column).
- Verdicts reference table rows, not re-stated numbers.
- If a metric is missing from raw data: write `n/a`, never estimate.

## Handoff 3: report-writer → output/

- Writer copies numbers **only** from the analyst's metrics table.
- Writer formats per `.cursor/rules/quisirella-meta-report-output.mdc` (VND dots, CTR comma decimals) — formatting may change presentation, never value.
- Before writing: run the checks in `report-rubric.md`.

## Validation between agents (error propagation)

One agent's hallucination becomes the next agent's "fact". Checkpoints:

- Parent verifies fetcher's manifest files actually exist before invoking analyst.
- Writer rejects analyst output whose metrics table lacks data-source columns.
- Any `data_status: unavailable` propagates to the report frontmatter — it never silently becomes `ok`.

## When NOT to use the pipeline

Simple lookups — classify intent first per `config/intent_router.yaml`:

| Intent | Action |
|---|---|
| `finance_lookup` | `finance-fetcher` only — no Meta |
| `meta_lookup` / `cached_read` | Read `output/01` or `06` if fresh; else minimal fetch |
| `save_session` | Write `09` checkpoint — no fetch |
| `ig_organic_copy` | Rule only — no fetch |
| `full_business` / `ads_analysis` | Full pipeline below |

Full pipeline: `meta-fetcher` + `finance-fetcher` (parallel when `full_business`) → `meta-analyst` → `report-writer`. Do not add a 4th agent.

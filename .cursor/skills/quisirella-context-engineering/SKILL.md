---
name: quisirella-context-engineering
description: "Context engineering for the Quisirella Meta Ads workflow: subagent handoff contracts (verbatim metrics), filesystem-as-memory conventions for data/ and output/, session-log compression policy, and a report quality rubric. Use when orchestrating meta-fetcher/meta-analyst/report-writer, when output/07-session-log.md grows long, or when reviewing a report before writing to output/."
---

# Quisirella — Context Engineering

Operating principles for the Quisirella agent workflow (fetch → analyze → report). This skill is about **how the workflow runs**, not about Meta Ads domain knowledge (that lives in `src/quisirella/skill/` and `.cursor/rules/quisirella-*`).

Distilled and adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT) — skills: multi-agent-patterns, filesystem-context, context-compression, evaluation, context-degradation.

## When to Use

- Orchestrating the subagent pipeline: classify intent (`config/intent_router.yaml`) → `meta-fetcher` / `finance-fetcher` → `meta-analyst` → `report-writer`
- `output/07-session-log.md` has grown long and needs compaction
- Reviewing a report before writing to `output/01-06`
- Deciding whether a task needs a subagent at all

## Core Principles

### 1. Verbatim metrics across handoffs (telephone game)

Numbers degrade when paraphrased between agents. A supervisor that rewrites "chi phi/tin nhan 16.799 VND" as "~17k" corrupts the report downstream.

- Analyst → writer handoff is a **markdown table with exact numbers**, never prose descriptions of numbers.
- Writer copies numbers from the table; it never recomputes or rounds differently.
- Full contract: `references/subagent-handoff.md`.

### 2. Files over messages (scratch-pad pattern)

Raw API output does not belong in chat context.

- Fetcher writes raw JSON to `data/meta_fetch/` and returns **file paths + a few summary lines** (campaign IDs, date range, row counts).
- Anyone needing detail greps/reads the file — targeted retrieval, not full dumps.
- Conventions: `references/filesystem-memory.md`.

### 3. Compress the session log without losing the artifact trail

`output/07-session-log.md` is append-only via hooks. When it grows long, compact old entries into a monthly block — but decisions, final metrics, and file paths must survive **verbatim**. Artifact trail is the first thing lost in naive summarization. Policy: `references/filesystem-memory.md`.

### 4. Deterministic checks before judgment (report gate)

Before writing any report to `output/`:

1. **Deterministic first** (fail fast): frontmatter fields present, `data_status` valid, VND formatting, every number traceable to `data/meta_fetch/`.
2. **Rubric second** (per-dimension pass/fail): KPI hierarchy, IG-only, Breakdown Effect compliance, policy compliance.

A report fails if **any single dimension** fails — no averaging away problems. Full rubric: `references/report-rubric.md`.

### 5. Placement and priority (degradation defenses)

- **Lost-in-middle:** put the executive summary + verdicts at the **top** of every report and actionable recommendations at the **end**. Never bury verdicts mid-document.
- **Poisoning:** one fabricated number in `output/` gets re-cited forever (Claude Projects reads these files as ground truth). If an API call fails, write the error + `data_status: unavailable` — never a plausible-looking number. If a bad number is found, **remove it at the source file**, don't append corrections.
- **Clash:** when sources conflict, priority is fixed: `config/store_profile.yaml` = `config/campaign_strategy.yaml` (campaign verdicts) > `.cursor/rules/quisirella-*` > `src/quisirella/skill/` (generic Meta) > external benchmarks. Example: skill says optimize CPA; Quisirella KPI (chi phi/tin nhan) wins; Profile campaign uses cost/visit per campaign_strategy, not messaging CPA.
- **Distraction:** load only what the task needs. Don't read all of `output/` to answer one campaign question.

### 6. Subagents only when isolation pays

Multi-agent costs ~15x tokens vs single-agent. Use the pipeline for full analysis runs (fetch 30-day insights → diagnose → write reports). For simple questions ("chi phí/tin nhắn campaign phễu là bao nhiêu?"), the main agent reads `output/06` directly — no subagents. Three agents is the right count; do not add more.

## References

- `references/subagent-handoff.md` — Read when: launching or updating the fetcher/analyst/writer pipeline
- `references/filesystem-memory.md` — Read when: writing files to data/ or output/, or compacting the session log
- `references/report-rubric.md` — Read when: reviewing a report before writing to output/

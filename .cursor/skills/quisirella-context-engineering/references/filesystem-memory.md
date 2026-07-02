# Filesystem as Memory — Quisirella Conventions

The filesystem is the workflow's memory layer. Context windows hold working state; files hold everything durable.

## Directory contract

| Path | Role | Written by | Committed to git? |
|---|---|---|---|
| `data/meta_fetch/` | Raw API JSON (scratch/offload) | meta-fetcher | No (gitignored) |
| `data/meta_fetch/active/` | Per-campaign raw JSON | meta-fetcher | No |
| `output/00-*.md` | Stable knowledge base (Claude Projects) | human + agent | Yes |
| `output/01-06.md` | Periodic reports | report-writer | Yes |
| `output/07-session-log.md` | Session memory (hooks append) | hooks + agent | Yes |

## Scratch-pad rule (tool output offloading)

Any tool/API output larger than ~2000 tokens goes to a file; the response carries a reference:

```
[Saved to data/meta_fetch/active/1202..._insights.json — campaign phễu, 30d, actions include messaging_started=29]
```

Retrieval is targeted: `grep` for an action_type, `read` with line ranges. Never read a whole large JSON into context to extract one number.

## Four context failure modes → filesystem remedies

| Failure | Symptom | Remedy |
|---|---|---|
| Missing | Number needed but never fetched | Fetch and persist to `data/meta_fetch/` first; never estimate |
| Under-retrieved | Read the file but missed the field | Grep for exact action_type keys (`messaging_conversation_started_7d`) |
| Over-retrieved | Whole JSON dumped into context | Return references + summaries; read line ranges |
| Buried | Fact exists somewhere in output/ | Check `00-index-claude-knowledge.md` first, then targeted file |

## Session log compression policy (`output/07-session-log.md`)

Hooks append entries indefinitely. Compaction is the agent's job (manual, on request or when noticed), **not** the hooks'.

**Trigger:** entry section (below the `<!-- Entries appended below by hooks -->` marker) exceeds ~150 lines, or entries older than the current month exist.

**Method — anchored iterative summarization:**

1. Take all entries older than the current month.
2. Merge them into one block per month with mandatory sections (a section with nothing to report says "none" — empty sections signal silent loss):

```markdown
## Tổng hợp tháng YYYY-MM (compacted)

### Decisions
- 2026-07-02: verdict 1806 = reduce/pause; phễu = scale (chi phí/tin nhắn 16.799)

### Files created/updated
- output/06-active-campaigns-analysis.md (data_range 2026-06-02 → 2026-07-01)

### Key metrics snapshot
- account 30d: spend 8.546.101 VND, tin nhắn 165, chi phí/tin nhắn ~51.795

### Open items
- Điền competitor vào 00-competitive-ig-used-luxury.md
```

3. Replace the old entries with the block. Recent (current-month) entries stay untouched.
4. Optimize for tokens-per-task: if compaction would force re-reading reports to recover a decision, it was too aggressive.

**Never lose in compaction (artifact trail):** exact decision wording with numbers, file paths touched, data_range of reports, unresolved action items.

## Hygiene

- `data/meta_fetch/` is regenerated each fetch run — stale files may be overwritten; don't cite them without checking the date inside.
- Check file existence before reading cached paths (files move; fetches fail).
- Structured formats from the first write: JSON for data, markdown tables for logs. Format drift makes files unparseable.

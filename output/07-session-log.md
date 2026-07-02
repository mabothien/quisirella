---
title: Quisirella — Nhật ký phiên trao đổi Meta Ads
generated_at: 2026-07-02
purpose: session_memory
language: vi
---

# 07 — Session log

Nhật ký tự động từ Cursor hooks (`sessionStart`, `afterFileEdit` trên `output/`, `sessionEnd`, `stop`).

**Mục đích:** ghi nhớ quyết định, file đã cập nhật, và phiên phân tích — đọc trước khi tiếp tục tư vấn Meta Ads.

**Workflow liên quan:**

| Thành phần | Vai trò |
|---|---|
| `.cursor/rules/quisirella-analysis.mdc` | Router |
| `.cursor/rules/quisirella-meta-breakdown.mdc` | Breakdown Effect |
| `.cursor/agents/meta-fetcher.md` | Fetch read-only |
| `.cursor/agents/meta-analyst.md` | Diagnosis |
| `.cursor/agents/report-writer.md` | Ghi `output/01–06` |
| `src/quisirella/skill/SKILL.md` | Meta expert knowledge |
| `.cursor/skills/quisirella-context-engineering/SKILL.md` | Context engineering (handoff, memory, rubric) |

## Chính sách nén (compaction)

Khi phần entries (dưới marker) vượt **~150 dòng** hoặc có entries cũ hơn tháng hiện tại: gộp entries cũ thành 1 block `## Tổng hợp tháng YYYY-MM (compacted)` với 4 mục bắt buộc — **Decisions** (nguyên văn kèm số), **Files created/updated** (kèm data_range), **Key metrics snapshot**, **Open items**. Mục trống ghi "none". Entries tháng hiện tại giữ nguyên. Chi tiết: `.cursor/skills/quisirella-context-engineering/references/filesystem-memory.md`.

## Mục lục báo cáo chính

Xem [`00-index-claude-knowledge.md`](00-index-claude-knowledge.md) cho thứ tự đọc đầy đủ.

---

<!-- Entries appended below by hooks -->

## 2026-07-02 15:10:42 +0700

- **File updated:** `01-meta-ads-performance.md` (1 edit(s))

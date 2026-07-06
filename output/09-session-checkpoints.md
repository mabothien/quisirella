---
title: Quisirella — Session checkpoints (user-triggered)
generated_at: 2026-07-06
purpose: episodic_memory
language: vi
---

# 09 — Session checkpoints

**Chỉ ghi khi user nói "lưu phiên"** (intent `save_session`). Không auto-checkpoint ở `sessionEnd`.

Chat mới: hook `sessionStart` inject **checkpoint mới nhất** từ file này. Spec: `.cursor/rules/quisirella-session-memory.mdc`.

## Template (agent copy khi lưu)

```markdown
## Checkpoint YYYY-MM-DD HH:MM +07

- **User focus:** (1 dòng — từ user nếu có, vd. "lưu phiên — sunset 1806")
- **Decisions:** (verbatim, có số)
- **Key metrics:** (cite data/ hoặc output/ — không từ user paste)
- **Open items:** (việc còn dở)
- **Files touched:** (paths output/ hoặc data/)
- **Intent summary:** (intent đã chạy trong phiên)
```

<!-- Checkpoints appended below by agent on save_session -->

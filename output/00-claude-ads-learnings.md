---
title: Quisirella — Ban do hoc tu claude-ads (Meta DM-first)
generated_at: 2026-07-03
purpose: integration_reference
language: vi
---

# Ban do tich hop claude-ads → Quisirella

Tai lieu nay tom tat nhung gi da nhap tu [claude-ads](../claude-ads/) vao bo nao Quisirella — **chi Meta/Instagram, DM-first**. Khong cai `install.ps1`; kien thuc nam trong repo.

## Kien truc claude-ads (tham khao)

| Lop | claude-ads | Quisirella (sau upgrade) |
|---|---|---|
| Orchestrator | `ads/SKILL.md` + lenh `/ads` | `quisirella-analysis.mdc` + prompt mau |
| Domain knowledge | 22 sub-skills + `ads/references/` | `src/quisirella/skill/SKILL.md` + `references/` |
| Workflow | Khong co rieng | `.cursor/skills/quisirella-context-engineering/` |
| Subagents | 10 (6 audit + 4 creative) | **3** (fetcher → analyst → writer) |

## Da nhap (co file trong repo)

| Module claude-ads | File Quisirella | Ghi chu |
|---|---|---|
| 10-Principle Thinking Framework | `src/quisirella/skill/references/thinking_framework.md` | Mindset gate truoc moi phan tich |
| Andromeda + GEM + Lattice + creative diversity | `src/quisirella/skill/references/andromeda_creative.md` | Chi `instagram_*`, rubric 0-10 |
| Health Score 0-100 | `src/quisirella/skill/references/health_score_dm.md` | Trong so DM-first, bo tro verdict |
| Copy frameworks (6 khung) | `src/quisirella/skill/references/copy_frameworks_ig.md` | IG organic + ads, giong than thien |
| A/B test IF/THEN/BECAUSE | `src/quisirella/skill/references/ab_test_dm.md` | Metric = tin nhan, khong purchase |
| Unit economics + budget rules | `src/quisirella/skill/references/unit_economics_budget_dm.md` | 3x kill, 20% scale, 70/20/10 |
| Competitor Meta Ad Library | `src/quisirella/skill/references/competitor_meta_ig.md` | Used luxury VN |

## Co y thuc KHONG nhap

| claude-ads | Ly do |
|---|---|
| 22 sub-skills (`ads-google`, `ads-tiktok`...) | Quisirella chi Meta IG, 1 account |
| 10 agents audit song song | Da co pipeline 3 agent; MCP live fetch |
| Pixel/CAPI/EMQ/Purchase ROAS lam KPI | Chot DM — chi dung diagnostic |
| Benchmark e-commerce generic | Chi benchmark account Quisirella (`01`, `06`) |
| `install.ps1` → `~/.cursor/extensions/claude-ads/` | Project-native, khong goi doc lap |

## Rule con moi (Cursor)

| Rule | Khi nao |
|---|---|
| `quisirella-meta-creative-andromeda.mdc` | Creative fatigue, diversity, Andromeda |
| `quisirella-meta-competitor.mdc` | Meta Ad Library, competitive gap |

## Thu tu doc khi phan tich day du

1. `thinking_framework.md` (mindset)
2. `config/store_profile.yaml` + `campaign_strategy.yaml`
3. `src/quisirella/skill/SKILL.md` + `breakdown_effect.md`
4. Reference theo nhiem vu (andromeda / health_score / ab_test / unit_economics)
5. `output/06-active-campaigns-analysis.md` (benchmark noi bo)

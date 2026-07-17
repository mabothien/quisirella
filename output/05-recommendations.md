---
title: Đề xuất tối ưu — Quisirella
generated_at: 2026-07-14
data_range: 2026-07-08 đến 2026-07-14
verdict_window: 2026-07-12 đến 2026-07-13
sources: [meta_graph_api, store_profile.yaml, relevance_rules.yaml, campaign_strategy.yaml]
data_status: ok
ad_account_id: act_400356462876861
---

# 05 — Recommendations

> Dựa trên Meta ACTIVE PRIMARY 08–14/07/2026 (`verdict_window` **12–13/07**), store profile Quisirella, và luật lọc relevance. ACTIVE deep-dive: [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md).

> Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).

---

## Tóm tắt verdicts (verdict_window 12–13/07)

| Campaign | Verdict | Evidence |
|---|---|---|
| Phễu | **Giữ (gần scale)** | Window **16.856**/tin (17 mess / 286.556 spend) |
| 1806 | **Sunset watch** | Profile KPI; 206 link click window; hết ~18/07; quality mess n/a |
| Retarget | **Giữ** | Window **18.202**/tin; freq **1.142**;「chốt đơn」early (13/07) |

---

## Kế hoạch tuần 14–20/07 (P0–P2)

### P0 — Creative / delivery Phễu (làm ngay)

1. **Giữ**「Nỗi sợ」+「Nỗi sợ 3」ACTIVE.
2. **Check/pause**「Nỗi sợ 2」(`120253690578970110`) nếu vẫn delivering (PERIOD còn spend **98.731**; window **0**).
3. Ghi mess chất vào [`08-dm-quality-log`](08-dm-quality-log.md) hàng ngày (phục vụ sunset 1806).

### P1 — Sunset 1806 + scale Phễu có điều kiện

1. **Sunset 1806** khi quality gate đạt **HOẶC** lifetime end ~**18/07** (theo [`campaign_strategy.yaml`](../config/campaign_strategy.yaml)).
2. Realloc ~**70k**/ngày sang Phễu sau khi tắt 1806.
3. **Scale Phễu ≤20%** chỉ sau khi ổn định — **không** scale ngay (learning 43 mess/7d PERIOD &lt; 50).

### P2 — Retarget

1. **Giữ** Retarget (window cost **18.202**; freq **1.142** — dưới guard 40k / 3,5).
2. Review ad「chốt đơn」(ACTIVE từ 13/07) sau **7 ngày** → **20/07**.

---

## Measurement plan (GROW)

| Metric | Ngưỡng | Đọc lại |
|---|---|---|
| Phễu chi phí/tin nhắn | &lt; 25.000 VND | **16/07**, **18/07**, **20/07** |
| Retarget chi phí/tin nhắn (window) | &lt; 40.000 VND (guard) | **16/07**, **20/07** |
| Nỗi sợ 2 delivery (P0) | pause nếu còn delivering | **14–15/07** |
| Mess chất/ngày (manual) | ≥ 5 (sunset gate) | Daily → `08` |
| Sunset 1806 | quality gate **hoặc** ~18/07 | **18/07** |
|「chốt đơn」review | 7 ngày từ 13/07 | **20/07** |
| Scale Phễu | ổn định trước tăng ≤20% | **20/07** |

Copy / creative (nếu đổi): tuân [`00-meta-ad-policy-ig.md`](00-meta-ad-policy-ig.md) · [`00-ig-ad-creative-guide.md`](00-ig-ad-creative-guide.md).

---

## Tóm tắt hiệu suất PRIMARY (08–14/07)

| KPI | Giá trị | Đánh giá |
|---|---:|---|
| Tổng spend account | 1.601.653 VND | 7 ngày PRIMARY |
| Tin nhắn bắt đầu | 60 | 26.694 VND/tin (account) |
| Account window | 528.991 / 22 / **24.045** | — |
| Phễu (window) | **16.856**/tin | Best messaging — gần scale |
| Retarget (window) | 18.202/tin | Giữ — dưới guard 40k |
| Jul MTD spend / mess | 3.478.714 / 131 | 26.555 VND/tin |

---

## Ưu tiên thấp / loại

| Đề xuất generic | Verdict | Lý do |
|---|---|---|
| Scale Phễu ngay tuần này | **Loại** | Learning 43 mess/7d; scale chỉ sau ổn định ≤20% |
| Dùng cost/mess để đánh giá 1806 | **Loại** | `top_only` — Profile KPI |
| Pause Retarget vì “chưa đủ mess” | **Loại** | Window cost OK; freq 1.142; ad mới đang học |
| Purchase optimization | **Loại** | Chốt DM, pixel không tin cậy |

---

## Knowledge sources

| source_file | section / used_for |
|---|---|
| `.cursor/rules/quisirella-meta-kpi.mdc` | Chi phí/tin nhắn primary KPI; ngưỡng hold |
| `.cursor/rules/quisirella-meta-ig-platform.mdc` | Placement / creative IG |
| `config/campaign_strategy.yaml` | funnel_role; sunset 1806; legacy_aliases |
| `output/00-meta-ad-policy-ig.md` | Policy nếu đổi copy |
| `output/00-ig-ad-creative-guide.md` | Creative IG DM-first |

> Handoff không kèm `rag_sources` — P0–P2 là vận hành, không đề xuất caption/policy mới.

---

## Phụ lục

Nguồn: `data/meta_fetch/` fetch **14/07/2026** · deep-dive [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md) · `data/meta_fetch/fetch_manifest.json`

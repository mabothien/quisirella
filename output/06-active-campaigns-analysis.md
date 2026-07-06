---
title: Phân tích 3 chiến dịch ACTIVE — Quisirella
generated_at: 2026-07-06
data_range: 2026-07-01 đến 2026-07-06
verdict_window: 2026-07-05 đến 2026-07-06
sources: [meta_graph_api]
data_status: ok
ad_account_id: act_400356462876861
active_campaign_count: 3
---

# 06 — Phân tích 3 chiến dịch ACTIVE (01–06/07/2026)

Account `act_400356462876861`, kỳ **6 ngày** (01/07 → 06/07/2026). Đánh giá theo [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml) — **funnel_role**, không penalize Profile vì mess kém.

> Quisirella chốt đơn qua **Instagram DM** — KPI chính: **tin nhắn bắt đầu (7 ngày)**. Purchase Meta **không phản ánh doanh thu thật** (chốt DM).

**Mapping tên:** Ads Manager vẫn dùng tên cũ — map qua `legacy_aliases` trong strategy.

| Tên Ads Manager (API) | strategy_id | funnel_role | Objective thực tế |
|---|---|---|---|
| Chiến dịch phễu - target tin nhắn | `phieu_tinnhan_lal1` | top_middle | messaging |
| Chiến dịch Lượt tương tác mới - 1806 | `phieu_profile_1806` | top_only | `INSTAGRAM_PROFILE` — Lượt truy cập trang cá nhân IG |
| Chiến dịch Lượt tương tác - Bán - Bản sao | `ban_retarget_30d` | bottom | engagement/messaging |

Liên quan: [`03-finance-summary.md`](03-finance-summary.md) · [`05-recommendations.md`](05-recommendations.md) · [`01-meta-ads-performance.md`](01-meta-ads-performance.md)

---

## 1. Tóm tắt executive + verdicts

| Chỉ số (PERIOD 01–06/07) | Giá trị |
|---|---:|
| Campaign ACTIVE | **3** |
| Tổng spend (3 ACTIVE = account) | **1.399.459 VND** |
| Tổng tin nhắn bắt đầu | **62** |
| Chi phí/tin nhắn trung bình (account) | **22.572 VND** |

**Verdict theo `verdict_window` (05–06/07)** — dùng cho quyết định hành động:

| Campaign | funnel_role | Verdict | Lý do chính (window) |
|---|---|---|---|
| phễu tin nhắn | top_middle | **Giữ** | Chi phí/tin nhắn **22.652 VND** — dưới ngưỡng 25.000 VND |
| 1806 Profile | top_only | **Giữ** | Mess yếu **expected**; CTR **5,87%**, link click **124** (2 ngày) |
| Retarget | bottom | **Giữ** | IG-only; chi phí/tin nhắn **9.303 VND** excellent; engaged **85,7%** |

**Xếp hạng chi phí/tin nhắn (verdict_window):** Retarget (9.303) → phễu (22.652) → 1806 (n/a — Profile KPI)

---

## 2. Recency-first — phân tích hai lớp

| Lớp | Kỳ | Mục đích |
|---|---|---|
| **PERIOD** | 01–06/07/2026 | Bối cảnh 6 ngày — funnel depth, CTR, placement lịch sử |
| **VERDICT WINDOW** | 05–06/07/2026 | **Quyết định scale/giữ/giảm** — delivery gần nhất |

**Quy tắc:** Verdict và khuyến nghị **chỉ** dựa trên `verdict_window`. PERIOD dùng cho xu hướng.

**Retarget:** FB spend = 0 từ **04/07** (kể cả 06/07) → **không khuyên tắt Facebook** lần nữa.

---

## 3. Bảng PERIOD — 01–06/07/2026 (verbatim)

| Campaign | ID | funnel_role | Spend | Tin nhắn | Chi phí/tin nhắn | CTR | engaged_rate | Link click | Source |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| phễu tin nhắn | 120253285175280110 | top_middle | 730.810 | 35 | 20.880 | 4,67% | 48,6% | 77 | active/120253285175280110_insights.json |
| 1806 Profile | 120252531135370110 | top_only | 394.183 | 11 | 35.835 | 5,79% | 18,2% | 547 | active/120252531135370110_insights.json |
| Retarget | 120252990977040110 | bottom | 274.466 | 16 | 17.154 | 4,35% | 68,8% | 25 | active/120252990977040110_insights.json |
| Account | — | — | 1.399.459 | 62 | 22.572 | 5,08% | 48,4% | 649 | account_insights_2026-07-01_2026-07-06.json |

---

## 4. Bảng VERDICT WINDOW — 05–06/07/2026 (verbatim)

| Campaign | Spend | Tin nhắn | Chi phí/tin nhắn | engaged_rate |
|---|---:|---:|---:|---:|
| phễu | 158.567 | 7 | 22.652 | 42,9% |
| 1806 | 85.321 | 4 | n/a (profile KPI) | n/a |
| Retarget | 65.124 | 7 | **9.303** | **85,7%** |
| Account | 309.012 | 18 | 17.167 | 50,0% |

---

## 5. Timeline Facebook — Retarget (01–06/07)

Spend theo platform (VND, `120252990977040110_placement_daily.json`):

| Ngày | IG spend | FB spend |
|---|---:|---:|
| 01/07 | 18.139 | 37.295 |
| 02/07 | 23.162 | 33.004 |
| 03/07 | 30.332 | 11.899 |
| **04/07** | **55.511** | **0** |
| **05/07** | **53.574** | **0** |
| **06/07** | **11.550** | **0** |

→ **Facebook đã tắt từ 04/07.** 06/07 tiếp tục IG-only.

---

## 6. Funnel depth (PERIOD 01–06/07)

Notation: Started → First reply → Depth_3 → Depth_5

| Campaign | Started | First reply | Depth_3 | Depth_5 | Reply rate | Engaged rate |
|---|---:|---:|---:|---:|---:|---:|
| phễu tin nhắn | 35 | 22 | 17 | 4 | 62,9% | **48,6%** |
| 1806 Profile | 11 | 10 | 2 | 0 | 90,9% | 18,2% |
| Retarget | 16 | 9 | 11 | 1 | 56,2% | **68,8%** |

**Nhận xét:** Retarget engaged **68,8%** — tốt cho `bottom`. phễu **48,6%** — ổn cho `top_middle`. 1806 mess thấp **expected** — KPI là link click **547**, CTR **5,79%**.

---

## 7. Verdict chi tiết theo funnel_role

### 7.1 phễu tin nhắn — `top_middle`

| KPI | Ngưỡng | PERIOD | VERDICT WINDOW | Đạt? |
|---|---|---:|---:|---|
| Chi phí/tin nhắn | < 25.000 VND | 20.880 | **22.652** | **Có** |
| Engaged rate | — | 48,6% | 42,9% | Ổn |
| CTR | — | 4,67% | 4,38% | Ổn |

**Verdict: Giữ** — window **22.652 VND** dưới 25.000 VND. Volume **7 tin/2 ngày** — theo dõi nếu < 5 mess chất/ngày kéo dài 3 ngày.

---

### 7.2 1806 — `top_only`

| KPI | Ngưỡng | PERIOD | Ghi chú |
|---|---|---:|---|
| Chi phí/truy cập profile | < 1.200 VND | *Ads Manager* | KPI primary |
| Chi phí/tin nhắn | Loại trừ | 35.835 | **Expected thấp** |
| Link click | — | **547** | CTR **5,79%** |

**Verdict: Giữ** — đúng vai trò `top_only`. Window: **124 link click**, CTR **5,87%**.

**Sunset watch:** phễu < 25k × 3 ngày + ≥ 5 mess chất/ngày → pause 1806 per strategy.

---

### 7.3 Retarget — `bottom`

| KPI | Ngưỡng | PERIOD | VERDICT WINDOW | Đạt? |
|---|---|---:|---:|---|
| Chi phí/tin nhắn | tham chiếu | 17.154 | **9.303** | **Excellent** |
| Engaged rate | — | 68,8% | **85,7%** | Rất tốt |
| FB placement | IG-first | FB 01–03/07 | **IG-only 04–06/07** | Đã tối ưu |

**Verdict: Giữ** — campaign hiệu quả nhất trong window. Không khuyên tắt FB (đã off).

---

## 8. Unit economics tháng 7 (Sheet MTD)

> Sheet MTD (06/07) vs Meta **6 ngày** (01–06/07) — ROAS full month cần spend cả tháng.

| Chỉ số | Giá trị | Nguồn |
|---|---:|---|
| Doanh thu đạt (MTD) | **132.000.000 VND** | M9 |
| Lợi nhuận đạt (MTD) | **32.091.273 VND** | K9 |
| SL bán (MTD) | **8** | H9 |
| Meta spend (01–06/07) | **1.399.459 VND** | account_insights_2026-07-01_2026-07-06.json |
| Chi phí/đơn (partial) | **174.932 VND** | 1.399.459 / 8 |

Chi tiết finance + tỉ suất ads: [`03-finance-summary.md`](03-finance-summary.md).

---

## 9. Khuyến nghị hành động (recency-based)

### Ưu tiên (verdict_window 05–06/07)

1. **Retarget — Giữ IG-only** — chi phí/tin nhắn **9.303 VND**, engaged **85,7%**. Monitor < 20k.
2. **phễu — Giữ** — **22.652 VND**/tin nhắn; nếu volume mess < 5/ngày × 3 ngày → review creative.
3. **1806 — Giữ + sunset watch** — CTR/link click tốt; không penalize mess.

### Measurement plan (7 ngày)

| Metric | Campaign | Ngưỡng | Đọc lại |
|---|---|---|---|
| Chi phí/tin nhắn | phễu | < 25.000 VND | 13/07/2026 |
| Chi phí/tin nhắn | Retarget | < 20.000 VND | 13/07/2026 |
| FB spend | Retarget | = 0 | 13/07/2026 |
| Mess chất/ngày | phễu | ≥ 5 (manual) | 13/07/2026 |

---

## 10. Phụ lục nguồn dữ liệu

| File | Nội dung |
|---|---|
| `data/meta_fetch/active/120253285175280110_insights.json` | phễu 01–06/07 |
| `data/meta_fetch/active/120252531135370110_insights.json` | 1806 01–06/07 |
| `data/meta_fetch/active/120252990977040110_insights.json` | Retarget 01–06/07 |
| `data/meta_fetch/active/*_daily.json` | Daily per campaign |
| `data/meta_fetch/active/120252990977040110_placement_daily.json` | Retarget platform/day |
| `data/meta_fetch/account_insights_2026-07-01_2026-07-06.json` | Account 6 ngày |
| `data/meta_fetch/fetch_manifest_2026-07-01_2026-07-06.json` | Manifest + metrics parsed |

Strategy: [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml)

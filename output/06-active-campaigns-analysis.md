---
title: Phân tích 3 chiến dịch ACTIVE — Quisirella
generated_at: 2026-07-06
data_range: 2026-07-01 đến 2026-07-06
verdict_window: 2026-07-05 đến 2026-07-06
ad_level_snapshot: 2026-07-08
ad_level_data_range: 2026-07-01 đến 2026-07-07
ad_level_refresh: full-day 07/07 (fetch 08/07)
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

#### 7.1.1 Ad-level — test 2 quảng cáo song song (refresh full-day 07/07)

> **Bối cảnh:** Cùng ad set `Nhóm quảng cáo Lượt tương tác mới` — test 7 ngày theo checkpoint 09. Fetch lại **08/07** — số 07/07 là **cả ngày** (không còn partial).

**Ads ACTIVE:**

| Ad | ad_id | Format | Created | CTA | SKU / concept |
|---|---|---|---|---|---|
| Nỗi sợ | 120253285175260110 | Static 1 ảnh | 29/06/2026 | `INSTAGRAM_MESSAGE` | Giáo dục fake — generic Tiffany/Bvlgari |
| Nỗi sợ 2 | 120253603203850110 | Carousel 3 slide | 06/07/2026 17:22 | `INSTAGRAM_MESSAGE` | Tiffany T True narrow vàng hồng **size 51.5** |

**Bảng PERIOD ad-level — 01–07/07/2026 (verbatim, refresh 08/07)**

| Ad | Spend | Imp | Clicks | CTR | Tin nhắn | Chi phí/tin nhắn | depth_3 | engaged_rate | Source |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Nỗi sợ | 785.708 | 10.276 | 483 | 4,70% | 40 | **19.643** | 21 | 52,5% | `ad_insights.json` |
| Nỗi sợ 2 | 197.439 | 2.776 | 87 | 3,13% | 1 | 197.439 | 1 | n/a (n=1) | `ad_insights.json` |
| Ad set total | 983.147 | 13.052 | 570 | 4,37% | 41 | 23.979 | 22 | 53,7% | `insights.json` |

**Bảng VERDICT WINDOW ad-level — 06–07/07/2026 (verbatim)**

| Ad | Spend | Tin nhắn | Chi phí/tin nhắn | engaged_rate |
|---|---:|---:|---:|---:|
| Nỗi sợ | 75.191 | 8 | **9.399** | 50,0% |
| Nỗi sợ 2 | 197.439 | 1 | 197.439 | n/a (n=1) |

**Ngày 07/07 — full day (verbatim)**

| Ad | Spend | Imp | Clicks | CTR | Tin nhắn | Chi phí/tin nhắn | % spend ad set | Source |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Nỗi sợ | 376 | 5 | 0 | 0% | 1 | 376 | **0,3%** | `ad_insights_2026-07-07.json` |
| Nỗi sợ 2 | 122.697 | 1.636 | 57 | 3,48% | 1 | 122.697 | **99,7%** | `ad_insights_2026-07-07.json` |
| Ad set | 123.073 | — | — | — | 2 | 61.537 | 100% | tổng 2 ad |

**Timeline spend/ngày**

| Ngày | Nỗi sợ spend | Nỗi sợ mess | Nỗi sợ 2 spend | Nỗi sợ 2 mess | % Nỗi sợ 2 |
|---|---:|---:|---:|---:|---:|
| 01/07 | 151.836 | 8 | — | — | — |
| 02/07 | 135.765 | 2 | — | — | — |
| 03/07 | 130.132 | 5 | — | — | — |
| 04/07 | 154.510 | 13 | — | — | — |
| 05/07 | 138.274 | 4 | — | — | — |
| **06/07** | 74.815 | 7 | **74.742** | 0 | **50,0%** |
| **07/07** | **376** | 1 | **122.697** | 1 | **99,7%** |

**Funnel depth ad-level (period 01–07/07):** Started → First reply → Depth_3 → Depth_5

| Ad | Started | First reply | Depth_3 | Depth_5 | Reply rate | Engaged rate |
|---|---:|---:|---:|---:|---:|---:|
| Nỗi sợ | 40 | 24 | 21 | 5 | 60,0% | 52,5% |
| Nỗi sợ 2 | 1 | 1 | 1 | 0 | 100% (n=1) | n/a |

**Chẩn đoán 07/07 (full day):**

- Pattern **xác nhận** sau refresh: Meta explore carousel — không phải artifact partial-day (「Nỗi sợ 2」tăng từ 51k → **123k** spend).
- **「Nỗi sợ」bị throttle cả ngày** — 376 VND / 5 imp; ad cũ vẫn period **19.643**/tin < 25k.
- **「Nỗi sợ 2」KPI xấu ngày 2:** 2 ngày live = **197.439 VND / 1 mess**; 07/07 chủ yếu `video_view` (71) — Meta học engagement trước mess.
- Ad set 07/07: **61.537 VND/mess** (2 mess) — ngày kém do exploration; **không** đánh giá campaign từ 1 ngày.

**Verdict ad-level (`top_middle`) — refresh 08/07:**

| Ad | Verdict | Lý do |
|---|---|---|
| Nỗi sợ | **Giữ** | Period **19.643**/tin; starvation 07/07 = learning side-effect |
| Nỗi sợ 2 | **Giữ (test) + yellow flag** | Ngày 2/7; CPA **197k** — theo dõi 09–10/07; pause **chỉ khi hết hàng T 51.5** |
| Ad set | **Giữ test** | Còn **5 ngày** đến review 13/07; nếu「Nỗi sợ 2」>60% spend × 3 ngày + CPA >75k → cân nhắc tách ad set |

**Measurement plan ad-level (đọc lại 13/07/2026):**

| Metric | Ngưỡng | Ghi chú |
|---|---|---|
| Chi phí/tin nhắn per ad | < 25.000 VND | Winner sau 7 ngày |
| % spend split | Ghi nhận | Không force 50/50 |
| Mess chất manual (SKU 51.5) | Ghi `08-dm-quality-log` | Success signal cho carousel |
| Inventory T 51.5 | Còn hàng | Pause「Nỗi sợ 2」ngay khi hết |

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
| Chi phí/tin nhắn | phễu (campaign) | < 25.000 VND | 13/07/2026 |
| Chi phí/tin nhắn | phễu per ad (Nỗi sợ / Nỗi sợ 2) | < 25.000 VND | 13/07/2026 |
| Chi phí/tin nhắn | Retarget | < 20.000 VND | 13/07/2026 |
| FB spend | Retarget | = 0 | 13/07/2026 |
| Mess chất/ngày | phễu | ≥ 5 (manual) | 13/07/2026 |
| % spend split ad-level | phễu | Ghi nhận | Daily đến 13/07 |

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
| `data/meta_fetch/active/120253285175280110_ads.json` | phễu — danh sách ad (2 ACTIVE) |
| `data/meta_fetch/active/120253285175280110_ad_insights.json` | phễu — ad-level period 01–07/07 |
| `data/meta_fetch/active/120253285175280110_ad_insights_2026-07-07.json` | phễu — ad-level full day 07/07 |
| `data/meta_fetch/active/120253285175280110_ad_daily.json` | phễu — ad-level daily 01–07/07 |
| `data/meta_fetch/active/120253285175280110_creatives.json` | phễu — creative per ad |
| `data/meta_fetch/active/120253285175280110_adsets.json` | phễu — ad set config |
| `data/meta_fetch/fetch_manifest_2026-07-01_2026-07-07.json` | Manifest ad-level 07/07 |

Strategy: [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml)

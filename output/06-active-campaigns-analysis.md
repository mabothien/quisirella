---
title: Phân tích 3 chiến dịch ACTIVE — Quisirella
generated_at: 2026-07-03
data_range: 2026-06-30 đến 2026-07-02
sources: [meta_graph_api]
data_status: ok
ad_account_id: act_400356462876861
active_campaign_count: 3
analysis_window: 3_days
---

# 06 — Phân tích 3 chiến dịch ACTIVE (3 ngày)

Account `act_400356462876861`, kỳ **3 ngày** (30/06 → 02/07/2026). Đánh giá theo [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml) và [`00-campaign-strategy.md`](00-campaign-strategy.md) — **funnel_role**, không penalize Profile vì mess kém.

> Quisirella chốt đơn qua **Instagram DM** — KPI chính: **tin nhắn bắt đầu (7 ngày)**. Purchase Meta không phản ánh doanh thu thật (chốt DM).

**Caveat:** Kỳ 3 ngày — tất cả campaign đang **learning phase** (< 50 mess/tuần). Verdict mang tính sơ bộ, chưa đủ data để scale/pause dứt khoát.

**Mapping tên:** Ads Manager vẫn dùng tên cũ — map qua `legacy_aliases` trong strategy.

| Tên Ads Manager (API) | strategy_id | funnel_role | Objective thực tế (adset) |
|---|---|---|---|
| Chiến dịch phễu - target tin nhắn | `phieu_tinnhan_lal1` | top_middle | messaging |
| Chiến dịch Lượt tương tác mới - 1806 | `phieu_profile_1806` | top_only | `destination_type: INSTAGRAM_PROFILE` — Lượt truy cập trang cá nhân IG |
| Chiến dịch Lượt tương tác - Bán - Bản sao | `ban_retarget_30d` | bottom | engagement/messaging |

> **Lưu ý metric 1806:** Objective cấp campaign hiển thị `OUTCOME_ENGAGEMENT` (nhóm ODAX), nhưng cấp **adset** có `optimization_goal: PROFILE_AND_PAGE_ENGAGEMENT` + `destination_type: INSTAGRAM_PROFILE` → **đúng là chiến dịch Lượt truy cập trang cá nhân IG** như thiết kế. Metric "Lượt truy cập trang cá nhân IG" là **cột Ads Manager** — API không expose riêng, chỉ có `link_click` (proxy). Số visit chính xác lấy từ Ads Manager (manual).

---

## 1. Tóm tắt executive

| Chỉ số | Giá trị |
|---|---:|
| Campaign ACTIVE | **3** |
| Tổng spend (3 ACTIVE) | **803.675 VND** |
| Tổng tin nhắn bắt đầu | **35** |
| Chi phí/tin nhắn trung bình (gộp) | **22.962 VND** |
| Tổng lead Meta | 34 |
| Purchase Meta (pixel) | 1 |
| **Đơn chốt (manual)** | **3** |
| Engaged mess proxy (depth_3/phễu) | **50%** (10/20) |

**Xếp hạng theo chi phí/tin nhắn** (KPI primary — chỉ áp dụng full cho top_middle & bottom):

| Tiêu chí | #1 | #2 | #3 |
|---|---|---|---|
| Chi phí/tin nhắn | Bán (17.031) | phễu (20.979) | 1806 (42.755) |
| CTR | 1806 (5,23%) | phễu (5,05%) | Bán (4,28%) |
| Volume tin nhắn | phễu (20) | Bán (10) | 1806 (5) |
| Funnel depth_3 rate | phễu (50%) | Bán (20%) | 1806 (20%) |

**Kết luận nhanh:**

- **phễu tin nhắn** (`top_middle`): Chi phí/tin nhắn **20.979 VND** — dưới ngưỡng strategy < 25.000 VND. Funnel sâu (reply 80%, depth_3 50%). **Hold** — chờ thêm data learning.
- **1806** (`top_only`): **Đúng vai trò Profile Visit** (`destination_type: INSTAGRAM_PROFILE`). Chi phí/lượt truy cập **769 VND** (Ads Manager, 278 visit) — **dưới ngưỡng < 1.200 VND**. Mess kém là **expected**, không penalize. **Hold** — đang hoàn thành vai trò mồi pixel giá rẻ.
- **Bán retarget** (`bottom`): Chi phí/tin nhắn **17.031 VND** tốt nhất; CPM **68.757** trong ngưỡng ~80k. **Hold** — nhưng **66,7% spend vào Facebook Feed** cần review (IG-first store).

---

## 2. Bảng so sánh side-by-side (verbatim)

| Chỉ số | phễu - target tin nhắn | Bán - Bản sao | 1806 |
|---|---:|---:|---:|
| strategy_id | `phieu_tinnhan_lal1` | `ban_retarget_30d` | `phieu_profile_1806` |
| funnel_role | top_middle | bottom | top_only |
| ID | `120253285175280110` | `120252990977040110` | `120252531135370110` |
| **Spend** | 419.588 | 170.311 | 213.776 |
| % spend 3 ACTIVE | 52,2% | 21,2% | 26,6% |
| Impressions | 5.387 | 2.477 | 4.975 |
| Reach | 3.390 | 1.440 | 4.237 |
| Frequency | 1,59 | 1,72 | 1,17 |
| Clicks | 272 | 106 | 260 |
| **CTR** | **5,05%** | 4,28% | **5,23%** |
| CPC | 1.543 | 1.607 | 822 |
| CPM | 77.889 | 68.757 | 42.970 |
| **Tin nhắn bắt đầu** | **20** | **10** | **5** |
| **Chi phí/tin nhắn** | **20.979** | **17.031** | **42.755** |
| Lead Meta | 20 | 13 | 1 |
| Chi phí/lead | 20.979 | 13.101 | 213.776 |
| Purchase Meta | 1 | 0 | 0 |
| Link click | 54 | 19 | 262 |
| **Lượt truy cập profile IG (AM)** | — | — | **278** |
| Chi phí/truy cập profile (AM) | — | — | **769** |
| Engaged rate (depth_3) | **50%** | 20% | 20% |
| Post save | 1 | 0 | 3 |
| Video view | 8 | 163 | 25 |

*Nguồn: `data/meta_fetch/active/{id}_insights.json`. Lượt truy cập profile IG chính xác = cột Ads Manager (manual); API chỉ có link_click proxy.*

---

## 3. Funnel depth (3 ngày)

| Campaign | Started | First reply | Depth_2 | Depth_3 | Depth_5 | Reply rate | Depth_3 rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| phễu tin nhắn | 20 | 16 | 16 | 10 | 1 | **80%** | **50%** |
| Bán retarget | 10 | 5 | 8 | 2 | 1 | 50% | 20% |
| 1806 | 5 | 4 | 3 | 1 | 0 | 80% | 20% |

**Nhận xét:** phễu có funnel sâu nhất (depth_3 rate 50%) — phù hợp vai trò **top_middle** lọc ý định mua. Bán retarget depth_3 thấp hơn nhưng vẫn trong learning — cần theo dõi thêm khi frequency tăng.

---

## 4. Phân tích theo funnel_role

### 4.1 phễu tin nhắn — `top_middle` (máy kiếm khách mới)

**KPI strategy:**

| KPI | Ngưỡng | Thực tế 3 ngày | Đạt? |
|---|---|---:|---|
| Chi phí/tin nhắn | < 25.000 VND | **20.979** | Có (sơ bộ) |
| Mess/tuần (learning) | ≥ 50 | ~47 (20 mess × 7/3) | Gần ngưỡng |
| Quality mess rate | > 40% | **90%** (18/20 — 30/6+1/7; 2/7 N/A) | **Đạt** |
| Engaged mess (depth_3 proxy) | — | **50%** (10/20) | Proxy tự động API |
| Đơn chốt (kỳ) | — | **3** | manual — Business FB |

**Mess chất lượng theo ngày** (manual — user, nguồn DM; chi tiết: [`08-dm-quality-log.md`](08-dm-quality-log.md)):

| Ngày | Tin nhắn (API) | Mess chất (manual) | depth_3 (proxy) | Chi phí/mess | ≥ 5 chất? | < 25k/mess? |
|---|---:|---:|---:|---:|---|---|
| 30/06 | 10 | **10** | 5 | 13.207 | Đạt | Đạt |
| 01/07 | 8 | **8** | 4 | 18.980 | Đạt | Đạt |
| 02/07 | 2 | **N/A** | 1 | 67.839* | N/A | Không đạt* |

*\*02/7: mess chất không xác định được — data nằm ở Business FB "đã chuyển đổi", không API được. Attribution mess API có thể tăng sau 1–2 ngày.*

**Sunset Profile (điều kiện phễu):** **2/3 ngày đạt** (30/6 + 1/7). 2/7 mess chất **N/A** → **chưa kích hoạt sunset** — theo dõi 3/7.

**Điểm mạnh:** Chi phí/tin nhắn dưới target; CTR 5,05%; reply rate 80%; 100% spend trên Instagram (placement).

**Placement IG (3 ngày):**

| Placement | Spend | Tin nhắn | Chi phí/tin nhắn |
|---|---:|---:|---:|
| instagram feed | 266.758 | 11 | 24.233 |
| instagram reels | 74.004 | 3 | 24.668 |
| instagram stories | 78.826 | 6 | **13.138** |

**Giả thuyết testable:** Stories có chi phí/tin nhắn thấp nhất trên IG — có thể tăng tỷ trọng creative Stories *nếu* marginal efficiency duy trì sau 7 ngày (không pause Feed/Reels chỉ vì CPA trung bình cao hơn).

**Verdict: `hold`** — KPI primary đạt nhưng learning phase; chưa đủ 7 ngày học máy. Không scale mạnh trước khi có ≥ 50 mess/tuần ổn định.

---

### 4.2 1806 — `top_only` (mồi pixel / Profile Visit)

**Objective xác nhận (cấp adset):** `optimization_goal: PROFILE_AND_PAGE_ENGAGEMENT`, `destination_type: INSTAGRAM_PROFILE` → **đúng chiến dịch Lượt truy cập trang cá nhân IG**. Đã chạy từ **18/06** (~15 ngày, quá cửa sổ tạm 7–10 ngày).

**Lượt truy cập trang cá nhân IG theo ngày:**

| Ngày | Lượt truy cập (Ads Manager) | Spend | Chi phí/truy cập (AM) |
|---|---:|---:|---:|
| 30/06 | **60** | 54.607 | **910** |
| 01/07 | **128** | 87.441 | **683** |
| 02/07 | **90** | 71.728 | **797** |
| **Tổng** | **278** | 213.776 | **769** |

> Nguồn visit: Ads Manager (manual, user). API `link_click` = 262 (proxy, thấp hơn ~6%).

**KPI strategy (Profile Visit):**

| KPI | Ngưỡng | Thực tế 3 ngày | Đạt? |
|---|---|---:|---|
| Chi phí/truy cập | < 1.200 VND | **769** (AM) | **Đạt** |
| Chi phí/tin nhắn | Loại trừ | 42.755 | Expected — không penalize |
| Mess chất lượng | Không kỳ vọng | — | — |

**Chẩn đoán:** Campaign **đang hoàn thành đúng vai trò `top_only`** — traffic rẻ về trang IG (769đ/visit, dưới ngưỡng 1.200đ), nuôi pixel/LAL. Mess ít (5) là **đúng thiết kế**, không phải lỗi.

**Sunset check (strategy):** phễu đạt < 25k/mess + ≥ 5 mess chất **2 ngày liên tiếp** (30/6, 1/7). Ngày 2/7 chưa đủ → **chưa kích hoạt sunset**. 1806 vẫn **hold** song song.

**Verdict: `hold`** — 1806 đạt KPI riêng (visit < 1.200đ), không có lý do hiệu suất để tắt. Lý do tắt duy nhất = **hết vai trò tạm** khi phễu tin nhắn tự đứng được (sunset). Đã quá `max_days: 10` → cân nhắc sunset ngay khi xác nhận phễu ổn định + đủ mess chất.

---

### 4.3 Bán retarget — `bottom` (chốt đơn)

**KPI strategy:**

| KPI | Ngưỡng | Thực tế 3 ngày | Đạt? |
|---|---|---:|---|
| CPM | ~80.000 VND | **68.757** | Có |
| CTR | > 3% | **4,28%** | Có |
| Tần suất | < 3,5/tuần | 1,72 (3 ngày) | Có (sơ bộ) |
| Coc inquiry rate | > 20% | *manual — n/a* | Chưa có |

**Điểm mạnh:** Chi phí/tin nhắn **17.031 VND** — thấp nhất trong 3 campaign; CPM trong ngưỡng chấp nhận cho tệp nhỏ.

**Red flag — Facebook placement:**

| Platform | Spend | % spend | Tin nhắn |
|---|---:|---:|---:|
| **facebook feed** | **113.484** | **66,7%** | 4 |
| instagram feed | 35.060 | 20,6% | 4 |
| instagram reels | 10.034 | 5,9% | 1 |
| instagram stories | 11.733 | 6,9% | 1 |

**66,7% spend vào Facebook Feed** — vượt ngưỡng cảnh báo 15% cho store IG-first. Chi phí/tin nhắn FB: **28.371 VND** vs IG (6 mess): **9.471 VND**.

**Giả thuyết testable:** Review loại Facebook placement hoặc giảm budget FB — IG rows hiệu quả mess hơn cho retarget. Không pause campaign (hàng cao cần nhiều chạm).

**Verdict: `hold`** + **optimize placement** — giữ budget tổng, ưu tiên IG Feed/Reels/Stories.

---

## 5. Phân bổ ngân sách vs strategy

| Campaign | % spend thực tế (3 ngày) | % strategy (daily) | Ghi chú |
|---|---:|---:|---|
| phễu tin nhắn | 52,2% | 52,5% | Khớp |
| 1806 (Profile) | 26,6% | 26% | Khớp — visit 769đ đạt target |
| Bán retarget | 21,2% | 19% | Gần khớp |

Tổng phễu acquisition (phễu + 1806): **78,8%** vs strategy 70% — hơi lệch vì retarget spend thấp trong 3 ngày.

---

## 6. Verdict tổng hợp

| Campaign | funnel_role | Verdict | Hành động cụ thể |
|---|---|---|---|
| phễu tin nhắn | top_middle | **hold** | Giữ ~140k/ngày; sunset 2/3 ngày đạt — chờ 3/7 xác nhận; quality 90% |
| 1806 | top_only | **hold** | Đạt visit 769đ (AM), đúng vai trò mồi pixel; giữ song song đến sunset |
| Bán retarget | bottom | **hold** | Giữ 50k/ngày; review loại FB Feed (66,7% spend); không pause |

**Sunset Profile:** **Chưa kích hoạt** — 30/6 + 1/7 đạt cả 2 điều kiện. 2/7 mess chất **N/A** (Business FB). Cần **3 ngày liên tiếp** → theo dõi **3/7**.

**Đơn chốt kỳ:** **3 đơn** (manual — Business FB "đã chuyển đổi"). Chốt phụ thuộc khách — không dùng làm KPI campaign.

**Learning phase:** Cả 3 campaign — caveat bắt buộc trước mọi quyết định scale/pause.

---

## 7. KPI manual + proxy tự động

| Metric | Campaign | Giá trị | Nguồn | Trạng thái |
|---|---|---|---|---|
| quality_mess_per_day | phễu | 30/6: **10**, 1/7: **8**, 2/7: **N/A** | user (DM) | 2/3 ngày |
| quality_mess_rate | phễu | **90%** (18/20 — 2/7 loại trừ) | user | Đạt > 40% |
| engaged_rate (depth_3) | phễu | **50%** (10/20) | Meta API | Proxy tự động |
| profile_visit (AM) | 1806 | 30/6: **60**, 1/7: **128**, 2/7: **90** | user (AM) | 3/3 ngày |
| cost_per_visit (AM) | 1806 | **769** VND | tính từ AM | Đạt < 1.200 |
| orders_closed | account | **3** | Business FB | manual |
| coc_inquiry_rate | retarget | n/a | user (DM) | Chưa có |

Chi tiết ghi hàng ngày: [`08-dm-quality-log.md`](08-dm-quality-log.md)

---

## 8. Phụ lục nguồn dữ liệu

| File | Nội dung |
|---|---|
| `data/meta_fetch/active/campaigns_status.json` | Mapping ID + objective/destination adset |
| `data/meta_fetch/active/{id}_daily.json` | Breakdown theo ngày (time_increment=1) |
| `data/meta_fetch/active/120253285175280110_insights.json` | phễu insights 3d |
| `data/meta_fetch/active/120252531135370110_insights.json` | 1806 insights 3d |
| `data/meta_fetch/active/120252990977040110_insights.json` | Bán insights 3d |
| `data/meta_fetch/active/{id}_placement.json` | Placement breakdown |
| `data/meta_fetch/active/{id}_adsets.json` | Adset level |

Strategy reference: [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml) · [`00-campaign-strategy.md`](00-campaign-strategy.md) · [`08-dm-quality-log.md`](08-dm-quality-log.md)

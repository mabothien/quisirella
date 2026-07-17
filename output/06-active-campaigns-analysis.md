---
title: Phân tích 3 chiến dịch ACTIVE — Quisirella
generated_at: 2026-07-14
data_range: 2026-07-08 đến 2026-07-14
verdict_window: 2026-07-12 đến 2026-07-13
sources: [meta_graph_api]
data_status: ok
ad_account_id: act_400356462876861
active_campaign_count: 3
---

# 06 — Phân tích 3 chiến dịch ACTIVE (08–14/07/2026)

Account `act_400356462876861`, kỳ PRIMARY **7 ngày** (08/07 → 14/07/2026). Đánh giá theo [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml) — **funnel_role**, không penalize Profile vì mess kém.

> Quisirella chốt đơn qua **Instagram DM** — KPI chính: **tin nhắn bắt đầu (7 ngày)**. Purchase Meta **không phản ánh doanh thu thật** (chốt DM).

**Mapping tên:** Ads Manager vẫn dùng tên cũ — map qua `legacy_aliases` trong strategy.

| Tên Ads Manager (API) | strategy_id | funnel_role | Objective thực tế |
|---|---|---|---|
| Chiến dịch phễu - target tin nhắn | `phieu_tinnhan_lal1` | top_middle | messaging |
| Chiến dịch Lượt tương tác mới - 1806 | `phieu_profile_1806` | top_only | `INSTAGRAM_PROFILE` — Lượt truy cập trang cá nhân IG |
| Chiến dịch Lượt tương tác - Bán - Bản sao | `ban_retarget_30d` | bottom | engagement/messaging |

Liên quan: [`05-recommendations.md`](05-recommendations.md) · [`01-meta-ads-performance.md`](01-meta-ads-performance.md)

---

## 1. Tóm tắt executive + verdicts

| Chỉ số (PERIOD 08–14/07) | Giá trị |
|---|---:|
| Campaign ACTIVE | **3** |
| Tổng spend account | **1.601.653 VND** |
| Tổng tin nhắn bắt đầu | **60** |
| Chi phí/tin nhắn trung bình (account) | **26.694 VND** |
| Frequency (account) | **1.70** |

**Verdict theo `verdict_window` (12–13/07)** — dùng cho quyết định hành động:

| Campaign | funnel_role | Verdict | Lý do chính (window) |
|---|---|---|---|
| phễu tin nhắn | top_middle | **Giữ (gần scale)** | Chi phí/tin nhắn **16.856 VND** — dưới ngưỡng 25.000 VND |
| 1806 Profile | top_only | **Sunset watch** | Hết ~18/07; quality mess n/a; **0** mess window (expected) |
| Retarget | bottom | **Giữ** | Chi phí/tin **18.202 VND**; freq **1.142**; ad「chốt đơn」early |

**Xếp hạng chi phí/tin nhắn (verdict_window):** Phễu (16.856) → Retarget (18.202) → Account (24.045) → 1806 (n/a — Profile KPI)

---

## 2. Recency-first — phân tích hai lớp

| Lớp | Kỳ | Mục đích |
|---|---|---|
| **PERIOD** | 08–14/07/2026 | Bối cảnh 7 ngày — CTR, freq, ad-level |
| **VERDICT WINDOW** | 12–13/07/2026 | **Quyết định scale/giữ/giảm** — delivery gần nhất |

**Quy tắc:** Verdict và khuyến nghị **chỉ** dựa trên `verdict_window`. PERIOD dùng cho xu hướng.

**Jul MTD 01–14 (tham chiếu):** spend **3.478.714** · mess **131** · chi phí/tin **26.555**.

---

## 3. Bảng PERIOD — 08–14/07/2026 (verbatim)

| Campaign | ID | funnel_role | Spend | Tin nhắn | Chi phí/tin nhắn | Freq | CTR | Link click |
|---|---|---|---:|---:|---:|---:|---:|---:|
| phễu tin nhắn | 120253285175280110 | top_middle | 868.095 | 43 | 20.188 | 1.872 | 4,14% | 73 |
| 1806 Profile | 120252531135370110 | top_only | 437.439 | 3 | n/a (profile) | 1.260 | 6,38% | 586 |
| Retarget | 120252990977040110 | bottom | 296.119 | 14 | 21.151 | 1.323 | 3,08% | 21 |
| Account | — | — | 1.601.653 | 60 | 26.694 | 1.70 | — | — |

---

## 4. Bảng VERDICT WINDOW — 12–13/07/2026 (verbatim)

| Campaign | Spend | Tin nhắn | Chi phí/tin nhắn | Freq | CTR | Link click | Ghi chú |
|---|---:|---:|---:|---:|---:|---:|---|
| phễu | 286.556 | 17 | **16.856** | 1.347 | 3,56% | 20 | Dưới ngưỡng 25k |
| 1806 | 151.426 | 0 | n/a (profile KPI) | 1.093 | 6,57% | 206 | top_only — không dùng cost/mess |
| Retarget | 91.009 | 5 | **18.202** | 1.142 | 2,73% | 7 | Freq thấp; giữ |
| Account | 528.991 | 22 | **24.045** | — | — | — | — |

---

## 5. MTD theo campaign (tham chiếu)

| Campaign | Spend | Tin nhắn | Chi phí/tin nhắn | Freq | CTR | Link click |
|---|---:|---:|---:|---:|---:|---:|
| phễu | 1.851.242 | 84 | 22.039 | 2.447 | — | — |
| 1806 | 965.380 | 14 | n/a (profile) | 1.533 | 5,98% | 1.299 |
| Retarget | 662.092 | 33 | 20.063 | 1.620 | — | — |
| Account | 3.478.714 | 131 | 26.555 | — | — | — |

---

## 6. Placement — IG-only (recency)

| Campaign | Trạng thái placement (verdict window) | Khuyến nghị |
|---|---|---|
| Phễu | Delivery messaging / IG (theo fetch ACTIVE) | Giữ |
| Retarget | Delivery retarget | Giữ — review「chốt đơn」sau 7 ngày từ 13/07 |
| 1806 | Profile IG | Sunset watch — hết ~18/07 |

> Không khuyến nghị “tắt Facebook” khi không có bằng chứng spend FB trên window trong handoff.

---

## 7. Deep-dive theo campaign

### 7.1 phễu — `top_middle` (`120253285175280110`)

#### 7.1.1 Ad-level (verbatim)

| Ad | Status | PERIOD spend / mess / cost | WINDOW spend / mess / cost |
|---|---|---:|---:|
| Nỗi sợ | **ACTIVE** | 626.439 / 31 / **20.208** | 219.318 / 12 / **18.276** |
| Nỗi sợ 3 | **ACTIVE** (created 13/07) | 75.344 / 4 / **18.836** | 67.238 / 4 / **16.810** |
| Nỗi sợ 2 (`120253690578970110`) | kiểm tra delivery | 98.731 / 4 / **24.683** | **0** — flag check/pause nếu còn delivering |

#### 7.1.2 Chẩn đoán

- **Winner:**「Nỗi sợ」— PERIOD **20.208**/tin; window **18.276**/tin (12 mess).
- **Nỗi sợ 3:** mới (13/07) — cost window **16.810** (n=4) tốt nhưng **learning caveat** (ad &lt; ~7 ngày; mẫu nhỏ) — **giữ**, chưa scale trên ad này.
- **Nỗi sợ 2:** PERIOD còn spend (**98.731** / 4 / **24.683**) nhưng window **0** — **P0: check/pause nếu vẫn delivering**.
- **Learning (campaign):** 43 mess/7 ngày PERIOD &lt; 50 → **giữ, gần scale** — chưa scale dứt khoát; scale ≤20% chỉ khi ổn định.

**Verdict campaign: Giữ (gần scale)** — window cost/mess **16.856** &lt; 25.000.

---

### 7.2 1806 — `top_only` (`120252531135370110`)

| KPI | Ngưỡng | PERIOD | VERDICT WINDOW | Ghi chú |
|---|---|---:|---:|---|
| Chi phí/tin nhắn | Loại trừ | n/a | n/a | **Expected — không dùng làm primary** |
| Link click | — | **586** | **206** | CTR PERIOD **6,38%** · window **6,57%** |
| Spend | — | 437.439 | 151.426 | Profile delivery |
| Mess | — | 3 | 0 | Không penalize |
| Freq | — | 1.260 | 1.093 | — |

**Verdict: Sunset watch** — đúng vai trò `top_only`. Quality mess **n/a**. Lifetime end ~**18/07**.

**Sunset (P1):** IF quality gate đạt **HOẶC** lifetime end ~18/07 → pause 1806; realloc ~70k sang Phễu. Cần cập nhật `08-dm-quality-log`.

---

### 7.3 Retarget — `bottom` (`120252990977040110`)

| KPI | Ngưỡng | PERIOD | VERDICT WINDOW | Đạt? |
|---|---|---:|---:|---|
| Chi phí/tin nhắn | tham chiếu / guard 40k | 21.151 | **18.202** | OK — dưới 40k |
| Frequency | guard &gt; 3,5 | 1.323 | **1.142** | OK |

#### Ad-level

| Ad | Status | PERIOD | WINDOW | Ghi chú |
|---|---|---:|---:|---|
| chốt đơn | **ACTIVE** (13/07) | 19.551 / 1 / **19.551** | 15.854 / 1 / **15.854** | Early — learning caveat |
| cũ còn hàng | **PAUSED** | — | — | Giữ PAUSED |

**Verdict: Giữ** — freq window **1.142**; review「chốt đơn」sau **7 ngày** kể từ 13/07 (≈20/07).

---

## 8. Khuyến nghị hành động — tuần 14–20/07 (P0–P2)

### P0 — Creative / delivery Phễu (làm ngay)

1. **Giữ**「Nỗi sợ」+「Nỗi sợ 3」ACTIVE.
2. **Check/pause**「Nỗi sợ 2」(`120253690578970110`) nếu vẫn delivering (window spend = 0 nhưng PERIOD còn chi).
3. Ghi **mess chất** vào [`08-dm-quality-log`](08-dm-quality-log.md) hàng ngày (phục vụ sunset 1806).

### P1 — Sunset 1806 + scale Phễu có điều kiện

1. **Sunset 1806** khi quality gate đạt **HOẶC** lifetime end ~**18/07**.
2. Realloc ~**70k**/ngày sang Phễu sau khi tắt 1806.
3. **Scale Phễu ≤20%** chỉ sau khi ổn định (cost/mess window dưới 25k + learning ổn) — **không** scale ngay.

### P2 — Retarget

1. **Giữ** Retarget (window cost **18.202**; freq **1.142**).
2. Review ad「chốt đơn」sau **7 ngày** từ 13/07.

### Measurement plan (GROW)

| Metric | Campaign | Ngưỡng | Đọc lại |
|---|---|---|---|
| Chi phí/tin nhắn | phễu | &lt; 25.000 VND | **16/07**, **18/07**, **20/07** |
| Chi phí/tin nhắn | Retarget window | &lt; 40.000 VND | **16/07**, **20/07** |
| Nỗi sợ 2 delivery | phễu | pause nếu còn delivering | **14–15/07** |
| Nỗi sợ 3 (learning) | phễu | giữ; đánh giá sau ≥7 ngày live | **20/07** |
| Mess chất/ngày | phễu (manual) | ≥ 5 (sunset gate) | Daily → 08 |
| Sunset 1806 | profile | quality gate **hoặc** ~18/07 | **18/07** |
|「chốt đơn」review | Retarget | 7 ngày từ 13/07 | **20/07** |
| Learning / scale Phễu | phễu | ổn định trước scale ≤20% | **20/07** |

Policy (nếu sửa copy/creative): [`00-meta-ad-policy-ig.md`](00-meta-ad-policy-ig.md) · [`00-ig-ad-creative-guide.md`](00-ig-ad-creative-guide.md).

---

## 9. Knowledge sources (rule / strategy — không có policy copy mới trong handoff)

| source_file | used_for |
|---|---|
| `.cursor/rules/quisirella-meta-kpi.mdc` | Primary KPI chi phí/tin nhắn; ngưỡng 25k; learning |
| `.cursor/rules/quisirella-meta-ig-platform.mdc` | Placement / creative IG |
| `.cursor/rules/quisirella-meta-breakdown.mdc` | Không pause chỉ vì average CPA |
| `config/campaign_strategy.yaml` | funnel_role; sunset 1806; legacy_aliases; learning ~50 |
| `output/00-meta-ad-policy-ig.md` | Tham chiếu nếu đổi copy |
| `output/00-ig-ad-creative-guide.md` | Tham chiếu creative IG DM-first |

> Analyst handoff không kèm bảng `rag_sources` — khuyến nghị P0–P2 là vận hành (giữ/pause/sunset/scale), không phải đề xuất copy policy mới.

---

## 10. Phụ lục nguồn dữ liệu

| File | Nội dung |
|---|---|
| `data/meta_fetch/account_insights_7d_2026-07-08_2026-07-14.json` | Account PRIMARY 7d |
| `data/meta_fetch/account_insights_mtd_2026-07-01_2026-07-14.json` | Account Jul MTD |
| `data/meta_fetch/account_insights_verdict_2026-07-12_2026-07-13.json` | Account verdict window |
| `data/meta_fetch/active/120253285175280110_insights*.json` | phễu |
| `data/meta_fetch/active/120252531135370110_insights*.json` | 1806 |
| `data/meta_fetch/active/120252990977040110_insights*.json` | Retarget |
| `data/meta_fetch/active/*_ad_insights*.json` | Ad-level |
| `data/meta_fetch/fetch_manifest.json` | Manifest fetch |

Strategy: [`config/campaign_strategy.yaml`](../config/campaign_strategy.yaml)

**Unit economics tháng:** không cập nhật trong báo cáo này — handoff không có finance Sheet (`sources: meta_graph_api` only). Xem [`03-finance-summary.md`](03-finance-summary.md) nếu cần số cũ.

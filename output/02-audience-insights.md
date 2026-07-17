---
title: Phân tích tệp khách hàng — Quisirella
generated_at: 2026-07-13
data_range: 2026-07-07 đến 2026-07-13
sources: [meta_graph_api]
data_status: partial
ad_account_id: act_400356462876861
---

# 02 — Audience insights (PRIMARY 07–13/07)

> **Lưu ý:** Fetch PRIMARY **chưa** gồm breakdown tuổi/giới account-level → `data_status: partial`. Phần dưới dùng **placement / platform từ ACTIVE** + khung tier Quisirella. Breakdown tuổi/giới archive giữ tham chiếu — không dùng cho quyết định budget.

---

## Khung đối chiếu 3 phân khúc giá Quisirella

| Phân khúc | Giá (VND) | Sản phẩm chủ yếu | Audience kỳ vọng |
|---|---|---|---|
| Tier 1 | 2 – 4 triệu | Bạc Justin Davis, Tiffany Elsa Peretti | Nữ 22–35, quan tâm silver jewelry / street-luxury, Instagram-native |
| Tier 2 | 4 – 10 triệu | Justin Davis, Tiffany 1837/RTT, Bvlgari Save the Children | Nữ 25–40, có thu nhập ổn định, mua hàng hiệu secondhand có chủ đích |
| Tier 3 | 10 triệu+ | Bạc/vàng/kim cương Tiffany HardWear, RTT, Bvlgari | Nữ 28–45, AOV cao, quyết định mua chậm, cần trust (ảnh chi tiết, authentic) |

---

## Placement — ACTIVE campaigns (PRIMARY / verdict window)

### Retarget (`120252990977040110`) — bottom

| Trạng thái | Ghi chú |
|---|---|
| **IG-only** | FB spend = **0** trong verdict window (và từ 04/07) |
| Chi phí/tin PERIOD | **30.200 VND** |
| Chi phí/tin window 11–12 | **32.425 VND** |
| Engaged rate PERIOD | **60,0%** |

**Insight:** Đã IG-only — **không khuyên tắt Facebook** lần nữa. Theo dõi cost window (P3 trong [`05`](05-recommendations.md)).

### Phễu (`120253285175280110`) — top_middle

| Chỉ số | PERIOD 07–13 | Window 11–12 |
|---|---:|---:|
| Spend | 841.469 | 278.707 |
| Tin nhắn | 36 | 15 |
| Chi phí/tin | 23.374 | **18.580** |
| Engaged | 30,6% | — |

**Insight:** Delivery tập trung IG (policy Quisirella). Adset HardWear **PAUSED** từ 11/07 — spend window = 「Nỗi sợ」ACTIVE.

### 1806 Profile (`120252531135370110`) — top_only

Campaign `top_only` — KPI profile visit. PERIOD: CTR **6,13%**, **575** link click · Window: **211** link click. Không đánh giá bằng chi phí/tin nhắn.

---

## Archive — breakdown account 30 ngày (06/02–01/07) — tham chiếu only

> Dữ liệu cũ, **không** dùng cho verdict PRIMARY 07–13.

**Tuổi (archive):** 66% spend vào **25–34** — khớp Tier 1–2.

**Giới (archive):** Nữ 64,8% spend — tệp chính phù hợp trang sức nữ; nam 33,8% CPC thấp hơn — có thể quà tặng / Justin Davis.

---

## Khuyến nghị audience (13/07)

1. **Giữ IG-first** — Retarget FB = 0; không mở lại FB.
2. **Không mở rộng nam mass** — giữ creative phụ cả hai giới tính, không loại nam.
3. **HardWear / Tier 3** — quyết định re-enable trong adset ACTIVE (không tạo adset mới) nếu còn SKU — xem [`06`](06-active-campaigns-analysis.md) §P0.

---

## Phụ lục

| File | Nội dung |
|---|---|
| `data/meta_fetch/active/120253285175280110_placement_daily.json` | phễu placement |
| `data/meta_fetch/active/120252990977040110_placement_daily.json` | Retarget placement |
| `config/store_profile.yaml` | Tier giá + audience |

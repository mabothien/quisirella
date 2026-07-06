---
title: Đề xuất tối ưu — Quisirella
generated_at: 2026-07-06
data_range: 2026-07-01 đến 2026-07-05
sources: [meta_graph_api, store_profile.yaml, relevance_rules.yaml]
data_status: ok
ad_account_id: act_400356462876861
---

# 05 — Recommendations

> Dựa trên dữ liệu Meta ACTIVE 01–05/07/2026, store profile Quisirella, và luật lọc relevance. Finance MTD: [`03-finance-summary.md`](03-finance-summary.md). ACTIVE deep-dive: [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md).

> Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).

---

## Ưu tiên 3–5 ngày tới (cập nhật 2026-07-06, verdict_window 04–05/07)

Recency-based — verdict từ cửa sổ **04–05/07**, không từ full period khi latest days khác:

1. **Retarget — Giữ IG-only**
   - FB **đã tắt từ 04/07** (FB spend = 0 ngày 04 + 05) → **không khuyên tắt lại**.
   - **Monitor:** chi phí/tin nhắn IG duy trì (window: **13.636 VND**); engaged rate **87,5%**.

2. **phễu — Giữ**
   - Window chi phí/tin nhắn **17.222 VND** — dưới ngưỡng 25.000 VND.
   - **IF** dip ngày 05/07 kéo dài ≥ 3 ngày **THEN** review creative (format, CTA DM) — **không** pause placement IG chỉ vì CPA breakdown trung bình.

3. **1806 — Giữ + sunset watch**
   - Mess yếu **expected** (`top_only`) — đánh giá CTR **5,80%** + link click **537**, không penalize messaging.
   - **IF** phễu < 25k/tin nhắn × 3 ngày + ≥ 5 mess chất/ngày **THEN** pause 1806 per [`campaign_strategy.yaml`](../config/campaign_strategy.yaml) sunset.

### Measurement plan (đọc lại 13/07/2026)

| Metric | Ngưỡng | Ghi chú |
|---|---|---|
| phễu chi phí/tin nhắn | < 25.000 VND | verdict_window baseline 17.222 |
| Retarget chi phí/tin nhắn | < 20.000 VND | window 13.636 |
| Retarget FB spend | = 0 | xác nhận IG-only duy trì |
| Sunset 1806 | phễu 3 ngày đạt | manual mess chất từ DM |

---

## Tóm tắt hiệu suất kỳ ACTIVE (01–05/07)

| KPI | Giá trị | Đánh giá |
|---|---:|---|
| Tổng spend (3 ACTIVE) | 1.359.282 VND | 5 ngày |
| Tin nhắn bắt đầu | 56 | ~24.273 VND/tin nhắn (account) |
| Campaign tốt nhất (tin nhắn, period) | Retarget | 18.780 VND/tin nhắn |
| Campaign tốt nhất (tin nhắn, window) | Retarget | **13.636 VND/tin nhắn** |
| Profile visit proxy | 1806 | 537 link click, CTR 5,80% |

---

## Ưu tiên cao (làm ngay)

### 1. Scale campaign "phễu - target tin nhắn"

- **Lý do:** Chi phí/tin nhắn **16.799 VND** — thấp nhất trong các campaign active; CTR **5,42%** cao nhất.
- **Hành động:** Tăng lifetime budget (hiện 4,2M, đã spend 487k) hoặc duplicate structure sang sản phẩm mới.
- **Creative:** Giữ format phễu → CTA tin nhắn; ảnh macro chi tiết (khóa, tem, khắc chữ).

### 2. Review campaign "1806" (2,79M spend)

- **Lý do:** Chi tiêu lớn nhất nhưng chi phí/tin nhắn **55.790 VND** — cao gấp ~3,3× campaign phễu.
- **Hành động:** So sánh adset/ad trong campaign; pause adset kém; chuyển budget sang phễu hoặc Bán - Bản sao (25.777 VND/tin nhắn).

### 3. Giảm hoặc pause Traffic campaigns

- **Lý do:** "Lưu lượng truy cập mới" spend **2,77M** (32% tổng) với chi phí/tin nhắn **138.523 VND**.
- **Hành động:** Pause nếu không còn mục tiêu traffic; chuyển ngân sách sang engagement/tin nhắn.

### 4. Creative & trust (core positioning)

- Tiếp tục ảnh **macro chi tiết** — lợi thế conversion online cho hàng 2tr+.
- Caption: brand, line (Elsa Peretti / RTT / Justin Davis), chất liệu, **100% authentic**. Xem [`00-meta-ad-policy-ig.md`](00-meta-ad-policy-ig.md) · [`00-ig-ad-creative-guide.md`](00-ig-ad-creative-guide.md).

---

## Ưu tiên trung bình

### 5. Tối ưu placement: tăng Reels, review Stories

| Placement | CPC | Hành động |
|---|---:|---|
| Instagram Reels | 1.014 | **Tăng** — video ngắn macro sản phẩm, giá, CTA DM |
| Instagram Feed | 1.533 | **Giữ** — carousel chi tiết cho Tier 2–3 |
| Instagram Stories | 1.808 | **Review** — 37% spend IG nhưng CTR thấp nhất (2,77%) |
| Facebook | — | **Không khuyên tắt Retarget** — đã IG-only từ 04/07 |

### 6. Phân bổ ngân sách theo tier giá

| Tier | Hành động gợi ý | Audience signal |
|---|---|---|
| 2–4tr (Tier 1) | Reels lifestyle + giá entry; interest silver/street-luxury | 18–24 + 25–34 |
| 4–10tr (Tier 2) | Feed carousel chi tiết; retarget engage 7–14 ngày | 25–34 (core 66% spend) |
| 10tr+ (Tier 3) | Narrow interest Tiffany/Bvlgari; warm audience DM | Test thêm 35–44 (CTR 4,01%) |

### 7. Audience

- **Giữ:** nữ 25–34 (66% spend, phù hợp Tier 1–2).
- **Test:** adset riêng nữ 35–44 với creative trust (Tier 2–3).
- **Nam (34% spend):** giữ một phần cho Justin Davis / quà tặng, không scale mass.

### 8. Đo lường ROAS đúng cách

- Ghi doanh thu từng đơn vào Google Sheet kèm nguồn lead (campaign/ad).
- **ROAS thực = doanh thu Sheet / Meta spend cùng tháng** — không dùng purchase Meta làm KPI.
- Tháng 7: Sheet MTD 132M VND, Meta chỉ 5 ngày → xem [`03-finance-summary.md`](03-finance-summary.md).

---

## Ưu tiên thấp / dài hạn

- Fetch Meta spend **full tháng 7** → cập nhật ROAS thực trong file 03.
- Lưu snapshot hàng tháng (`data/quisirella.db`) để so sánh MoM.
- Khi có `ANTHROPIC_API_KEY`: chạy `python -m quisirella run` pipeline agent tự động.

---

## Không nên làm

- Khuyên **tắt Facebook** cho Retarget khi FB spend = 0 từ 04/07.
- Penalize 1806 vì mess kém — đúng vai trò `top_only` Profile Visit.
- Tin ROAS pixel làm KPI — chốt DM.
- So sánh CPM với benchmark e-commerce giá rẻ.
- Dùng chiến lược catalog/DPA restock — hàng 1-của-1.
- Pause placement segment chỉ vì CPA trung bình cao hơn (Breakdown Effect).

---

## Checklist tháng tới

- [ ] Monitor phễu chi phí/tin nhắn < 25k (window 17.222)
- [ ] Xác nhận Retarget IG-only duy trì (FB = 0)
- [ ] Theo dõi sunset 1806 khi phễu 3 ngày đạt
- [ ] Fetch Meta spend full tháng 7 → ROAS thực
- [ ] Ghi mess chất lượng vào [`08-dm-quality-log.md`](08-dm-quality-log.md)

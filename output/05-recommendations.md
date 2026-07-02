---
title: Đề xuất tối ưu — Quisirella
generated_at: 2026-07-02
data_range: 2026-06-02 đến 2026-07-01
sources: [meta_graph_api, store_profile.yaml, relevance_rules.yaml]
data_status: ok
---

# 05 — Recommendations

> Dựa trên dữ liệu Meta thật (8,55 triệu VND spend / 30 ngày), store profile Quisirella, và luật lọc relevance. Finance (ROAS thực) chờ Google Sheets.

---

## Tóm tắt hiệu suất kỳ này

| KPI | Giá trị | Đánh giá |
|---|---:|---|
| Tổng spend | 8.546.101 VND | — |
| Tin nhắn bắt đầu | 165 | ~51.795 VND/tin nhắn (account) |
| Campaign tốt nhất (tin nhắn) | phễu - target tin nhắn | 16.799 VND/tin nhắn |
| Campaign kém nhất (tin nhắn) | Lưu lượng truy cập mới | 138.523 VND/tin nhắn |
| Placement tốt nhất (IG) | Reels | CPC 1.014, CTR 4,23% |
| Core audience | Nữ 25–34 | 66% spend |

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
- Caption: brand, line (Elsa Peretti / RTT / Justin Davis), chất liệu, **100% authentic**.

---

## Ưu tiên trung bình

### 5. Tối ưu placement: tăng Reels, review Stories

| Placement | CPC | Hành động |
|---|---:|---|
| Instagram Reels | 1.014 | **Tăng** — video ngắn macro sản phẩm, giá, CTA DM |
| Instagram Feed | 1.533 | **Giữ** — carousel chi tiết cho Tier 2–3 |
| Instagram Stories | 1.808 | **Review** — 37% spend IG nhưng CTR thấp nhất (2,77%) |
| Facebook | — | **Giảm/loại** — chỉ 2,8% spend, không scale |

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
- **ROAS thực = doanh thu Sheet / 8,55M spend** — không dùng 3 purchase Meta làm KPI.

---

## Ưu tiên thấp / dài hạn

- Tích hợp **Google Sheets** → file 03 ROAS thực tự động.
- Lưu snapshot hàng tháng (`data/quisirella.db`) để so sánh MoM.
- Khi có `ANTHROPIC_API_KEY`: chạy `python -m quisirella run` pipeline agent tự động.

---

## Không nên làm

- Scale "1806" chỉ vì spend lớn — hiệu quả tin nhắn thấp hơn phễu.
- Tin ROAS pixel (3 purchase / 2,8M chi phí) làm KPI.
- So sánh CPM 49.764 VND với benchmark e-commerce giá rẻ.
- Dùng chiến lược catalog/DPA restock — hàng 1-của-1.
- Mở rộng mass audience giá rẻ — không khớp AOV 2tr+.

---

## Checklist tháng tới

- [ ] Scale campaign phễu, monitor chi phí/tin nhắn < 20k
- [ ] Pause Traffic campaign nếu vẫn > 100k/tin nhắn
- [ ] A/B Reels vs Stories với cùng sản phẩm
- [ ] Test adset nữ 35–44 cho Tier 2–3
- [ ] Ghi 165 tin nhắn → ? đơn chốt vào Sheet → tính ROAS thực

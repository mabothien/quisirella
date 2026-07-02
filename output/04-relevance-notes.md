---
title: Ghi chú lọc relevance — Quisirella
generated_at: 2026-07-02
data_range: 2026-06-02 đến 2026-07-01
sources: [relevance_rules.yaml, meta_graph_api]
data_status: ok
---

# 04 — Relevance notes

## Bối cảnh

Áp dụng luật lọc từ [`config/relevance_rules.yaml`](config/relevance_rules.yaml) lên **dữ liệu Meta thật** kỳ 2026-06-02 → 2026-07-01 (account `act_400356462876861`).

---

## Nhận định từ data thực + verdict

| Nhận định / insight | Verdict | Lý do |
|---|---|---|
| CPM trung bình account ~49.764 VND | **Giữ (context)** | Luxury jewelry secondhand VN — CPM cao hơn e-commerce giá rẻ là bình thường, không so benchmark Shopee |
| Campaign Traffic chiếm 32,4% spend, chi phí/tin nhắn 138k | **Cần kiểm chứng → Loại** | Quisirella chốt DM; traffic objective không tối ưu funnel tin nhắn |
| Campaign "phễu - target tin nhắn": chi phí/tin nhắn 16.799 VND | **Giữ** | Khớp mục tiêu conversion DM, hiệu quả tốt nhất trong kỳ |
| Instagram Reels: CPC 1.014, CTR 4,23% (thấp nhất CPC trên IG) | **Giữ** | Placement relevant cho showcase visual luxury trên IG |
| Instagram Stories: 37% spend IG, CTR 2,77% (thấp nhất) | **Giữ (cần tối ưu)** | Placement relevant nhưng creative/budget cần review |
| Facebook placement ~2,8% spend | **Cần kiểm chứng** | Volume nhỏ — có thể loại để tập trung IG nếu không cải thiện |
| Audience 25–34 chiếm 66% spend | **Giữ** | Khớp Tier 1–2, keep_criteria nữ 18–45 luxury |
| Audience nam 34% spend, CPC thấp hơn nữ | **Giữ (cần kiểm chứng)** | Có thể quà tặng / Justin Davis — không mở rộng mass |
| 3 purchase Meta, ROAS pixel ~2,8M/purchase | **Loại** | discard_criteria: pixel không tin cậy với chốt DM |
| Scale campaign "1806" vì spend lớn nhất (2,79M) | **Cần kiểm chứng** | Chi phí/tin nhắn 55.790 — cao gấp 3× campaign phễu |
| Benchmark CTR e-commerce mass-market VN (~1–2%) | **Loại** | irrelevant_verticals: CTR account 3,57% — so sánh không meaningful |
| Đề xuất catalog ads / DPA restock | **Loại** | Hàng 1-của-1, không restock |
| Đề xuất giảm giá / flash sale hàng loạt | **Loại** | Không phù hợp positioning authentic luxury secondhand |
| Lookalike rộng để tăng volume impressions | **Cần kiểm chứng** | Reach 85k/30 ngày đủ cho 1-của-1; volume không phải KPI chính |

---

## Insight Meta thường gặp (chưa fetch recommendations API)

| Nhận định Meta (dạng chung) | Verdict | Lý do |
|---|---|---|
| "Tăng ngân sách campaign ROAS cao" | **Giữ** | Chỉ khi ROAS tính từ doanh thu Sheet, không pixel |
| "Mở rộng audience Lookalike rộng" | **Cần kiểm chứng** | Hàng 1-của-1 |
| Benchmark fast fashion / Shopee CTR | **Loại** | irrelevant_verticals |
| Insight placement Reels vs Feed trên Instagram | **Giữ** | Data xác nhận Reels hiệu quả hơn Stories |
| Audience nữ 25–40 quan tâm luxury accessories | **Giữ** | Data xác nhận 25–34 là core spend |

---

## Vertical Quisirella (reference)

**Relevant:** jewelry, luxury, secondhand/resale, accessories cao cấp, Instagram high-AOV.

**Irrelevant:** fast fashion, FMCG, gaming, bảo hiểm, trang sức mỹ ký dưới 500k.

---

## Chỉ số đưa vào file 05 (đã lọc)

1. Scale / giữ campaign **phễu - target tin nhắn** (chi phí/tin nhắn thấp nhất)
2. Review giảm **Stories** hoặc cải thiện creative Stories
3. Tăng tỷ trọng **Reels** (CPC thấp nhất trên IG)
4. Cân nhắc pause/giảm **Traffic** campaigns (chi phí/tin nhắn 138k)
5. Giữ targeting **25–34 nữ**, test thêm **35–44** cho Tier 2–3

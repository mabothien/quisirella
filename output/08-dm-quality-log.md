---
title: Quisirella — Sổ ghi DM chất lượng + đơn chốt
generated_at: 2026-07-03
purpose: dm_quality_and_orders_ledger
sources: [manual_user, meta_graph_api_proxy]
---

# 08 — Sổ ghi DM chất lượng + đơn chốt

Sổ ghi tay hợp nhất: **mess chất lượng** + **đơn chốt** + **doanh thu**. Agent đọc file này khi phân tích sunset, quality KPI, ROAS thực.

## Taxonomy — mess chất lượng

**Tính là chất lượng** (hỏi tư vấn sản phẩm):
- Hỏi size / fit
- Hỏi chất liệu / authentic / tem
- Hỏi ship / đóng gói
- Hỏi cọc / thanh toán / giữ hàng
- Nhắn ≥ 2 lượt tư vấn (không chỉ 1 câu)

**Không tính là chất lượng** (nhưng vẫn ghi riêng):
- **Chỉ hỏi giá rồi im lặng** → ghi vào cột **"Hỏi giá rồi im"** (theo dõi tỷ lệ khách chỉ quan tâm giá)
- Spam, comment đào → bỏ qua
- Tin nhắn không liên quan mua hàng → bỏ qua

## Proxy tự động (Meta API)

| Metric API | Ý nghĩa | Công thức |
|---|---|---|
| `messaging_user_depth_3_message_send` | Engaged mess (hội thoại ≥ 3 lượt) | `engaged_rate = depth_3 / messaging_started` |

Proxy **không thay** mess chất tay — dùng đối chiếu khi số tay thiếu (vd. 2/7 N/A do Business FB "đã chuyển đổi").

## Mục tiêu kinh doanh

Tối đa **mess chất lượng** (khách có xu hướng tư vấn), **không** chạy theo volume. Chốt đơn phụ thuộc khách — không đặt KPI tỷ lệ chốt cứng cho campaign.

---

## Bảng ghi hàng ngày

| Ngày | Campaign | Mess API | Hỏi giá rồi im | Mess chất (tay) | depth_3 (proxy) | Đơn chốt | Doanh thu VND | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-06-30 | phễu tin nhắn | 10 | 0 | 10 | 5 | — | — | |
| 2026-07-01 | phễu tin nhắn | 8 | 0 | 8 | 4 | — | — | |
| 2026-07-02 | phễu tin nhắn | 2 | N/A | N/A | 1 | — | — | Mess chất + hỏi giá N/A — data Business FB "đã chuyển đổi" |
| 2026-06-30 → 2026-07-02 | *account* | 35 | — | 18 (2 ngày) | — | **3** | *chưa có* | Kỳ 3 ngày — 3 đơn chốt (user) |

> **Kiểm tra chéo:** `Mess API ≈ Hỏi giá rồi im + Mess chất + (khác)`. Cột "Hỏi giá rồi im" giúp thấy rõ tỷ lệ khách chỉ hỏi giá — không tính vào chất lượng.

---

## Profile visit 1806 (Ads Manager — manual)

| Ngày | Visit (AM) | Spend | Chi phí/visit |
|---|---:|---:|---:|
| 2026-06-30 | 60 | 54.607 | 910 |
| 2026-07-01 | 128 | 87.441 | 683 |
| 2026-07-02 | 90 | 71.728 | 797 |
| **Tổng** | **278** | 213.776 | **769** |

---

## Hướng dẫn ghi (user / agent)

1. Cuối mỗi ngày: điền 1 dòng cho campaign phễu — đếm **Mess chất** (hỏi tư vấn) và **Hỏi giá rồi im** riêng từ DM.
2. Khi chốt đơn: ghi vào cột Đơn chốt + Doanh thu (hoặc dòng tổng kỳ).
3. Agent: đọc file này trước khi đánh giá sunset hoặc quality_mess_rate.
4. Nếu ngày N/A (Business FB): ghi `N/A` + lý do; dùng depth_3 proxy làm tham chiếu.

Liên kết: [`00-campaign-strategy.md`](00-campaign-strategy.md) · [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md)

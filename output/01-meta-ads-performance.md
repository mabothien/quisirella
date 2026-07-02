---
title: Hiệu suất Meta Ads — Quisirella
generated_at: 2026-07-02
data_range: 2026-06-02 đến 2026-07-01
sources: [meta_graph_api]
data_status: ok
ad_account_id: act_400356462876861
---

# 01 — Hiệu suất Meta Ads (30 ngày)

## Tổng quan account

| Chỉ số | Giá trị |
|---|---:|
| Ad account | `act_400356462876861` (quisirella) |
| Khoảng thời gian | 2026-06-02 → 2026-07-01 |
| Tổng chi tiêu (spend) | **8.546.101 VND** |
| Impressions | 171.733 |
| Reach | 85.413 |
| Clicks | 6.128 |
| CTR | 3,57% |
| CPC | 1.395 VND |
| CPM | 49.764 VND |
| Tin nhắn bắt đầu (7 ngày) | 165 |
| Chi phí / tin nhắn bắt đầu | 51.795 VND |
| Lead (Meta) | 103 |
| Chi phí / lead | 82.972 VND |
| Purchase (Meta pixel) | 3 |
| Chi phí / purchase (Meta) | ~2.848.700 VND |

**Nhận xét nhanh:** Phần lớn ngân sách đi vào campaign **Lượt tương tác** và **Lưu lượng truy cập** (objective engagement/traffic), không phải campaign tin nhắn thuần. Campaign **"phễu - target tin nhắn"** mới (29/6) có hiệu quả tin nhắn tốt nhất trong các campaign đang chạy.

---

## Campaigns có chi tiêu trong kỳ (8 campaigns)

| Campaign | Trạng thái | Mục tiêu | Chi tiêu (VND) | Impressions | Clicks | CTR | CPC | Tin nhắn bắt đầu | Chi phí/tin nhắn |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Chiến dịch Lượt tương tác mới - 1806 | **ACTIVE** | Engagement | 2.789.505 | 65.311 | 2.720 | 4,16% | 1.026 | 50 | 55.790 |
| Chiến dịch Lưu lượng truy cập mới | PAUSED | Traffic | 2.770.468 | 68.157 | 2.107 | 3,09% | 1.315 | 20 | 138.523 |
| Chiến dịch Lượt tương tác mới - 2905 | PAUSED | Engagement | 1.665.199 | 20.221 | 561 | 2,77% | 2.968 | 45 | 37.004 |
| Chiến dịch phễu - target tin nhắn | **ACTIVE** | Engagement | 487.178 | 5.845 | 317 | 5,42% | 1.537 | **29** | **16.799** |
| Chiến dịch Lượt tương tác - Bán - Bản sao | **ACTIVE** | Engagement | 412.431 | 5.464 | 219 | 4,01% | 1.883 | 16 | 25.777 |
| Chiến dịch Lượt tương tác mới - 1806 - Bản sao | PAUSED | Engagement | 177.101 | 3.495 | 133 | 3,81% | 1.332 | 1 | 177.101 |
| Chiến dịch Lượt tương tác mới - 2905 - Bản sao | PAUSED | Engagement | 197.482 | 2.705 | 36 | 1,33% | 5.486 | 1 | 197.482 |
| Chiến dịch Lượt tương tác - Bán | PAUSED | Engagement | 46.737 | 535 | 35 | 6,54% | 1.335 | 3 | 15.579 |

---

## Campaigns đang ACTIVE (3)

> Phân tích chi tiết: [`output/06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md)

| Campaign | Ngân sách | Ghi chú |
|---|---|---|
| Chiến dịch phễu - target tin nhắn | Lifetime 4.200.000 VND | Mới nhất (29/6), CTR cao nhất (5,42%), chi phí/tin nhắn thấp nhất (16.799) |
| Chiến dịch Lượt tương tác - Bán - Bản sao | — | 16 lead + 16 tin nhắn, chi phí/tin nhắn 25.777 |
| Chiến dịch Lượt tương tác mới - 1806 | Lifetime 3.950.000 VND | Chi tiêu lớn nhất (2,79M), ~71% lifetime đã dùng, chi phí/tin nhắn 55.790 |

---

## Phân bổ chi tiêu theo loại campaign

| Nhóm | Chi tiêu (VND) | % tổng | Ghi chú |
|---|---:|---:|---|
| Engagement (Lượt tương tác / phễu) | 5.775.633 | 67,6% | Phù hợp mục tiêu IG DM |
| Traffic (Lưu lượng truy cập) | 2.770.468 | 32,4% | Chi phí/tin nhắn cao (138k) — cân nhắc giảm |

---

## KPI conversion (Quisirella context)

Quisirella chốt đơn chủ yếu qua **Instagram DM**, không qua pixel. Do đó:

- **Tin nhắn bắt đầu (7 ngày)** là proxy conversion quan trọng hơn purchase Meta (chỉ 3).
- **Lead Meta** (103) bao gồm cả lead form/messaging — cần đối chiếu Sheet để biết bao nhiêu thành đơn thật.
- ROAS Meta (~2,8M/purchase) **không phản ánh thực tế** — xem file 03.

---

## Lưu ý tracking

- 3 purchase Meta trong kỳ có thể là event tự động, không đại diện toàn bộ doanh thu.
- Ưu tiên theo dõi: tin nhắn bắt đầu → DM chốt → ghi Sheet (khi tích hợp).

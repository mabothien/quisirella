---
title: Tổng hợp tài chính — Quisirella
generated_at: 2026-07-02
data_range: 2026-06-02 đến 2026-07-01
sources: [meta_graph_api, google_sheets — chưa tích hợp]
data_status: partial
---

# 03 — Finance summary

## Trạng thái

**Google Sheets chưa được tích hợp** (`GOOGLE_SHEET_ID` chưa cấu hình). Không có doanh thu thật, COGS, hay lợi nhuận gộp.

**Ad spend Meta** đã lấy được từ Graph API.

---

## ROAS thực vs ROAS Meta

| Chỉ số | Công thức | Kỳ này |
|---|---|---:|
| **Ad spend (Meta)** | Từ insights API | **8.546.101 VND** |
| Doanh thu thật | Từ Google Sheet | _chưa có_ |
| Purchase Meta (pixel) | 3 events | _không tin cậy_ |
| Doanh thu Meta ước tính (3 × AOV giả định) | — | _không tính_ |
| **ROAS thực** | Doanh thu Sheet / spend | _chưa tính được_ |
| Gross profit | Doanh thu − COGS | _chưa có_ |

---

## Proxy conversion từ Meta (chưa phải doanh thu)

| Chỉ số | Giá trị | Chi phí đơn vị |
|---|---:|---:|
| Tin nhắn bắt đầu (7 ngày) | 165 | 51.795 VND/tin nhắn |
| Lead Meta | 103 | 82.972 VND/lead |
| Purchase Meta | 3 | ~2.848.700 VND/purchase |

**Ví dụ tính ROAS thực (khi có Sheet):**

Nếu kỳ này chốt **5 đơn** qua DM với doanh thu trung bình **6 triệu VND/đơn** (= 30 triệu VND):

- ROAS thực = 30.000.000 / 8.546.101 = **3,51×**
- Chi phí marketing / đơn = 8.546.101 / 5 = **1.709.220 VND**

_(Số liệu ví dụ — thay bằng số thật từ Sheet.)_

---

## Phân bổ chi tiêu theo loại mục tiêu

| Loại campaign | Spend (VND) | % | Ghi chú |
|---|---:|---:|---|
| Engagement / tin nhắn | 5.775.633 | 67,6% | Phù hợp funnel DM |
| Traffic | 2.770.468 | 32,4% | Chi phí/tin nhắn cao — xem xét cắt giảm |

---

## Lưu ý cho Quisirella

- Mỗi SKU là **1-của-1** — doanh thu tháng phụ thuộc số món bán, không phải volume ổn định.
- **8,5 triệu VND ad spend / 30 ngày** cần đối chiếu số đơn chốt thực tế qua DM để đánh giá hiệu quả.
- Khi tích hợp Sheet: map từng đơn với tier giá (2–4tr / 4–10tr / 10tr+) và nguồn lead (campaign/ad).

---

## Việc cần làm để hoàn thiện file này

1. Tạo Google Cloud service account + share Sheet tài chính
2. Điền `.env`: `GOOGLE_SHEET_ID`, `GOOGLE_SHEET_RANGES`
3. Ghi doanh thu từng đơn kèm: ngày, SKU, tier, nguồn DM/campaign
4. Chạy lại báo cáo để tính ROAS thực và gross profit

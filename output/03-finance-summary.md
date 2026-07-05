---
title: Tổng hợp tài chính — Quisirella
generated_at: 2026-07-05
data_range: 2026-06-01 đến 2026-06-30
sources: [google_sheets, meta_graph_api]
data_status: partial
ad_account_id: act_400356462876861
---

# 03 — Finance summary

## Trạng thái

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| **Google Sheets** | ok | `finance-fetcher` → `data/finance_fetch/bao_gia_2026_summary.json` |
| **Meta Ads API** | partial | Cần `meta-fetcher` với `period: 2026-06` — token Graph trong `.env` hết hạn tại thời điểm test |

---

## Tháng 6/2026 — Sheet (BÁO GIÁ 2026)

Nguồn: `data/finance_fetch/bao_gia_2026_summary.json` — cells M8, K8, H8.

| Chỉ số | Giá trị | Nguồn |
|---|---|---:|
| **Doanh thu đạt được** | **218.500.000 VND** | M8 |
| **Lợi nhuận đạt được** | **45.647.766 VND** | K8 |
| **Số lượng bán theo tháng** | **31** | H8 |
| Quảng cáo (Sheet YTD ref) | 44.597.147 VND | D8 — *không dùng cho ROAS* |

---

## ROAS thực vs Meta spend

| Chỉ số | Công thức | Tháng 6/2026 |
|---|---|---:|
| Meta spend | `data/meta_fetch/` (calendar month) | _chưa fetch — cần meta-fetcher_ |
| Doanh thu Sheet | M8 | **218.500.000 VND** |
| **ROAS thực** | Doanh thu / Meta spend | _chưa tính_ |
| **Chi phí/đơn** | Meta spend / 31 đơn | _chưa tính_ |

**Ví dụ** (khi có Meta spend): nếu spend tháng 6 = 8.000.000 VND → ROAS = 218.500.000 / 8.000.000 = **27,31×**; chi phí/đơn = 258.065 VND.

---

## YTD 2026 (Sheet — tham chiếu)

| Chỉ số | Giá trị | Cell |
|---|---|---:|
| Doanh thu đạt được YTD | 1.247.050.000 VND | D6 |
| Lợi nhuận đạt được YTD | 404.513.885 VND | D4 |
| ROS | 32,44% | B2 |
| Hàng tồn kho | 230.529.778 VND | D7 |

---

## Lưu ý Quisirella

- Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).
- Dòng **Quảng cáo** trên Sheet chỉ để tham chiếu — **ROAS dùng Meta API spend**.
- SKU **1-của-1** — doanh thu tháng biến động; không benchmark như e-commerce volume.
- **Không có** campaign-level ROAS từ Sheet — chỉ account-level.

---

## Pipeline đã dùng

```bash
python -m quisirella fetch-finance --month 2026-06
# meta-fetcher: get_insights time_range 2026-06-01 → 2026-06-30 (chạy qua Cursor MCP)
```

Raw archive: `data/finance_fetch/monthly_tabs/` (21 tab Tháng 11/2024 → 7/2026).

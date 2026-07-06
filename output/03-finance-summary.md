---
title: Tổng hợp tài chính — Quisirella
generated_at: 2026-07-06
data_range: 2026-07-01 đến 2026-07-06
sources: [google_sheets, meta_graph_api]
data_status: partial
profit_target_monthly_vnd: 70000000
ad_account_id: act_400356462876861
---

# 03 — Finance summary

## Trạng thái

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| **Google Sheets** | ok | `finance-fetcher` → `bao_gia_2026_summary.json` (fetch **2026-07-06 11:49**) |
| **Meta Ads API** | partial | Spend **01–06/07** (6 ngày) — calendar month T7 chưa hết |

> Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).

---

## Tháng 7/2026 — Sheet MTD (BÁO GIÁ 2026)

Nguồn: `data/finance_fetch/bao_gia_2026_summary.json` — cells M9, K9, H9. Sheet = **Tháng 7/2026 MTD** tại thời điểm fetch 06/07.

| Chỉ số | Giá trị | Nguồn |
|---|---|---:|
| **Doanh thu đạt được** | **132.000.000 VND** | M9 |
| **Lợi nhuận đạt được** | **32.091.273 VND** | K9 |
| **Số lượng bán theo tháng** | **8** | H9 |
| Quảng cáo (Sheet YTD ref) | 44.597.147 VND | D8 — *không dùng cho ROAS* |

---

## ROAS thực vs Meta spend

| Chỉ số | Công thức | Tháng 7/2026 |
|---|---|---:|
| Meta spend | `monthly_spend_2026.json` (01–06/07) | **1.399.459 VND** |
| Doanh thu Sheet | M9 (MTD) | **132.000.000 VND** |
| **Doanh thu / chi phí ads** | Doanh thu / Meta spend | **94,4×** *(partial — khác kỳ)* |
| **Chi phí/đơn** | Meta spend / SL bán | **174.799 VND** *(partial)* |
| Tin nhắn (7 ngày) | account insights | **61** |
| Chi phí/tin nhắn | spend / mess | **22.924 VND** |

**Lưu ý:** Sheet MTD vs Meta 6 ngày — **không** coi 94× là ROAS tháng. Pace spend T7: **~7,2 triệu**/tháng (1.398.394 × 31÷6).

---

## Target lợi nhuận 70 triệu/tháng — tiến độ T7

| Chỉ số | Giá trị | Ghi chú |
|---|---:|---|
| Target | **70.000.000 VND** | Mục tiêu kinh doanh |
| Lợi nhuận MTD (06/07) | **32.091.273 VND** | K9 — **45,8%** target |
| Ngày trong tháng | 6 / 31 | ~19% tháng |
| Còn thiếu | **37.908.727 VND** | Cần thêm ~10 đơn nếu giữ ~4M lãi/đơn |
| Meta spend MTD (01–06/07) | **1.399.459 VND** | account + 3 ACTIVE |
| Meta spend pace | ~**7,2 triệu**/tháng | thấp hơn T6 (8,5M) |
| Chi phí/tin nhắn MTD | **22.924 VND** | T6 full tháng: **54.505** |

**Nhận xét:** Nhịp lợi nhuận **đang trên target theo lịch**, nhưng mẫu nhỏ (8 đơn) — không kết luận sớm.

---

## Tỉ suất quảng cáo vs lợi nhuận — 2026 (Sheet + Meta API)

Nguồn Meta: `data/meta_fetch/monthly_spend_2026.json` — calendar month T1–T6, T7 = **01–06/07**.

| Tháng | Lợi nhuận (K) | Doanh thu (M) | Đơn | Meta spend | Tin nhắn | CP mess | **Ads/LN** | **DT/CP ads** | LN sau ads* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T1 | 55.545.203 | 192.500.000 | 40 | 6.014.036 | 167 | 36.012 | **10,8%** | 32,0× | 49,5M |
| T2 | 52.007.073 | 180.185.000 | 37 | 6.783.585 | 245 | 27.688 | **13,0%** | 26,6× | 45,2M |
| T3 | 94.282.940 | 335.525.000 | 46 | 7.745.086 | 176 | 44.006 | **8,2%** | 43,3× | 86,5M |
| T4 | 75.597.540 | 178.600.000 | 23 | 7.776.496 | 162 | 48.003 | **10,3%** | 23,0× | 67,8M |
| T5 | 61.081.014 | 67.840.000 | 34 | 8.059.708 | 162 | 49.751 | **13,2%** | 8,4× | 53,0M |
| T6 | 45.647.766 | 218.500.000 | 31 | 8.502.842 | 156 | 54.505 | **18,6%** | 25,7× | 37,1M |
| T7 MTD | 32.091.273 | 132.000.000 | 8 | 1.398.394 | 61 | 22.924 | 4,4%† | 94,4×† | 30,7M |

\* LN sau ads = lợi nhuận Sheet − Meta spend (tham chiếu, chưa trừ chi phí khác).  
† T7 partial — không so sánh trực tiếp với tháng full.

**Xu hướng spend:** 6,0M (T1) → 8,5M (T6), tăng dần ~+42% trong 6 tháng. T7 pace ~7,2M — **thấp hơn T6**.

### Kết luận tỉ suất (số thật API)

| Câu hỏi | Trả lời |
|---|---|
| **Tỉ suất ads/lợi nhuận đã tối ưu?** | **Ở mức hợp lý** — dao động **8–19%** LN; target 70M với ~8M ads = **11,4%**. T6 cao nhất (18,6%) vì **LN thấp**, không vì spend spike lớn (+4% vs T5). T7 CP mess **22.924** — tốt nhất 6 tháng qua. |
| **Doanh thu phụ thuộc ngân sách ads?** | **Không tuyến tính.** T3: LN **94M** (CP mess 44k); T6: LN **46M** (CP mess 55k, spend cao nhất). T2 CP mess **tốt nhất** (28k) nhưng LN chỉ 52M. **Mix SKU + số đơn** quyết định, không phải spend. |
| **Tăng budget để đạt 70M?** | **Chưa.** Spend đã tăng T1→T6 mà T6 LN yếu nhất. T7 funnel hiệu quả hơn — **giữ ~7–8M**, tối ưu chốt DM + inventory trước khi scale. |
| **Insight bất ngờ** | Tháng **CP mess cao** (T3–T6) vẫn có thể LN cao nếu **đơn lớn/margin tốt** — đừng cắt ads chỉ vì CP mess khi inventory premium còn. |

> **Attribution:** Đơn Sheet không map 1-1 ngày click ads. Bảng trên là **tham chiếu kinh doanh**, không phải causal ROAS.

---

## So sánh với kỳ trước (tham chiếu)

| Chỉ số | Tháng 6/2026 | Tháng 7 MTD (06/07) |
|---|---:|---:|
| Doanh thu đạt | 218.500.000 VND | 132.000.000 VND |
| Lợi nhuận đạt | 45.647.766 VND | 32.091.273 VND |
| SL bán | 31 | 8 |
| Meta spend | 8.502.842 VND | 1.398.394 VND *(01–06/07)* |
| Chi phí/tin nhắn | 54.505 VND | **22.924 VND** |

SKU **1-của-1** — doanh thu tháng biến động; không benchmark như e-commerce volume.

---

## YTD 2026 (Sheet — tham chiếu)

| Chỉ số | Giá trị | Cell |
|---|---|---:|
| Doanh thu đạt được YTD | 1.305.150.000 VND | D6 |
| Lợi nhuận đạt được YTD | 416.252.809 VND | D4 |
| ROS | 31,89% | B2 |
| Hàng tồn kho | 246.124.002 VND | D7 |

---

## Liên kết phân tích ACTIVE

Chi tiết campaign + unit economics partial: [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md)

| Campaign | Spend 01–06/07 | Tin nhắn | Chi phí/tin nhắn |
|---|---:|---:|---:|
| phễu tin nhắn | 730.810 | 35 | 20.880 |
| 1806 Profile | 394.183 | 11 | 35.835 |
| Retarget | 274.466 | 16 | 17.154 |
| **Account** | **1.399.459** | **62** | **22.572** |

---

## Lưu ý Quisirella

- Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).
- Dòng **Quảng cáo** trên Sheet chỉ để tham chiếu — **ROAS dùng Meta API spend**.
- **Không có** campaign-level ROAS từ Sheet — chỉ account-level.

---

## Pipeline đã dùng

```bash
python -m quisirella fetch-finance --month 2026-07
python scripts/_fetch_monthly_meta.py   # account calendar month insights
```

Raw: `data/finance_fetch/bao_gia_2026_summary.json` · Meta: `data/meta_fetch/monthly_spend_2026.json` · `account_insights_2026-07-01_2026-07-06.json`

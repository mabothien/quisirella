---
title: Tổng hợp tài chính — Quisirella
generated_at: 2026-07-13
data_range: 2026-07-01 đến 2026-07-13
sources: [google_sheets, meta_graph_api]
data_status: ok
profit_target_monthly_vnd: 70000000
ad_account_id: act_400356462876861
---

# 03 — Finance summary

## Trạng thái

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| **Google Sheets** | ok | `fetch-finance --month 2026-07` → `bao_gia_2026_summary.json` (fetch **2026-07-13**) |
| **Meta Ads API** | ok | MTD 01–13/07 — `account_insights_2026-07-01_2026-07-13.json`; PRIMARY 07–13 |

> Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM). **Doanh thu / chi phí ads** = M ÷ Meta spend — *không* gọi "ROAS Meta".

---

## Executive summary — T7 MTD (01–13/07)

| Chỉ số | Giá trị | Nhận xét |
|---|---:|---|
| **Doanh thu / chi phí ads** | **73,91×** † | Partial month — không dùng để scale |
| Meta spend MTD | **3.212.508 VND** | Pace ~7,7M/tháng (13/31) |
| Doanh thu Sheet (M9) | **237.450.000 VND** | Mẫu nhỏ (9 đơn) |
| Lợi nhuận Sheet (K9) | **59.376.565 VND** | 84,8% target 70M |
| Chi phí/đơn (ads) | **356.945 VND** | 3.212.508 / 9 |
| Chi phí/tin nhắn MTD | **27.225 VND** | 118 tin nhắn |
| LN sau ads | **56.164.057 VND** | K9 − Meta spend |

† **T7 partial** — không dùng 73,91× để scale budget.

**Verdict:** Quảng cáo **đáng tiền** — LN sau ads **56.164.057 VND** MTD; giữ budget pace ~7–8M/tháng; đọc lại **31/07** calendar month. Chi tiết ACTIVE: [`06`](06-active-campaigns-analysis.md).

---

## Tháng 7/2026 — Sheet MTD (BÁO GIÁ 2026)

Nguồn: `data/finance_fetch/bao_gia_2026_summary.json` — cells M9, K9, H9. Fetch **13/07/2026**.

| Chỉ số | Giá trị | Nguồn |
|---|---|---:|
| **Doanh thu đạt được** | **237.450.000 VND** | M9 |
| **Lợi nhuận đạt được** | **59.376.565 VND** | K9 |
| **Số lượng bán theo tháng** | **9** | H9 |
| Quảng cáo (Sheet YTD ref) | 52.020.577 VND | D8 — *không dùng cho ROAS* |

**Ghi chú kinh doanh:** T7 có **đơn lớn, biên lợi nhuận cao** — AOV cao trên 9 đơn. Doanh thu mạnh nhưng **mẫu nhỏ**; không dùng làm baseline scale ads.

---

## ROAS thực vs Meta spend — T7 MTD

| Chỉ số | Công thức | Tháng 7/2026 (01–13/07) |
|---|---|---:|
| Meta spend | `account_insights_2026-07-01_2026-07-13.json` | **3.212.508 VND** |
| Doanh thu Sheet | M9 (MTD) | **237.450.000 VND** |
| **Doanh thu / chi phí ads** | Doanh thu / Meta spend | **73,91×** *(partial)* |
| **Chi phí/đơn** | Meta spend / SL bán | **356.945 VND** |
| Tin nhắn (7 ngày) | account insights MTD | **118** |
| Chi phí/tin nhắn | spend / mess | **27.225 VND** |
| Lợi nhuận − ads | K9 − Meta spend | **56.164.057 VND** |

**Lưu ý:** 9 đơn — SKU 1-của-1; không coi DT/CP raw là signal scale. Dòng **Quảng cáo** Sheet chỉ tham chiếu.

---

## So sánh — T7 vs 3 tháng gần nhất (T4, T5, T6)

Nguồn Sheet: `bao_gia_2026_summary.json` (M, K, H). Meta T4–T6: `monthly_spend_2026.json` / archive insights.

| Tháng | Doanh thu (M) | Lợi nhuận (K) | Đơn (H) | Meta spend | **DT/CP ads** | LN sau ads* |
|---|---:|---:|---:|---:|---:|---:|
| **T4** | 178.600.000 | 75.597.540 | 23 | 7.776.496 | **22,9×** | 67,8M |
| **T5** | 67.840.000 | 61.081.014 | 34 | 8.059.708 | **8,4×** | 53,0M |
| **T6** | 218.500.000 | 45.647.766 | 31 | 8.502.842 | **25,7×** | 37,1M |
| **T7 MTD** | 237.450.000 | 59.376.565 | 9 | 3.212.508 | **73,91×**† | 56,2M |

\* LN sau ads = lợi nhuận Sheet − Meta spend (tham chiếu).  
† T7 partial (13/31 ngày) — không so sánh trực tiếp DT/CP raw với tháng full.

**TB có trọng số T4–T6:** Doanh thu **464.940.000** ÷ Spend **24.339.046** = **~19,1×**.

### Chẩn đoán

1. **T7 doanh thu mạnh** (237,45M) trên 9 đơn — AOV cao; không kết luận scale.
2. **LN MTD 59,4M** đã gần target 70M với ~42% tháng — pace tốt nhưng mẫu nhỏ.
3. **Không scale budget** vì DT/CP 73,91× raw — chờ đủ tháng + đủ đơn.

---

## Target lợi nhuận 70 triệu/tháng — tiến độ T7

| Chỉ số | Giá trị | Ghi chú |
|---|---:|---|
| Target | **70.000.000 VND** | Mục tiêu kinh doanh |
| Lợi nhuận MTD (13/07) | **59.376.565 VND** | K9 — **84,8%** target |
| Ngày trong tháng | 13 / 31 | ~42% tháng |
| Còn thiếu | **10.623.435 VND** | Pace LN **trên** target theo lịch |
| Meta spend MTD | **3.212.508 VND** | pace ~7,7M/tháng |
| Chi phí/tin nhắn MTD | **27.225 VND** | Account-level |

---

## ACTIVE campaigns — Meta PRIMARY 07–13/07

| Campaign | Spend | Tin nhắn | Chi phí/tin nhắn | funnel_role |
|---|---:|---:|---:|---|
| phễu tin nhắn | 841.469 | 36 | **23.374** | top_middle |
| Retarget Bán | 302.001 | 10 | **30.200** | bottom |
| 1806 Profile | 437.817 | 3 | n/a (profile) | top_only |
| **Account PRIMARY** | **1.581.287** | **49** | **32.271** | — |

Chi tiết campaign: [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md) · Performance: [`01`](01-meta-ads-performance.md).

---

## YTD 2026 (Sheet — tham chiếu)

| Chỉ số | Giá trị | Cell |
|---|---|---:|
| Doanh thu đạt được YTD | 1.410.600.000 VND | D6 |
| Lợi nhuận đạt được YTD | 443.538.101 VND | D4 |
| ROS | 31,44% | B2 |
| Hàng tồn kho | 216.948.324 VND | D7 |

---

## Measurement plan

| Metric | Ngưỡng | Đọc lại |
|---|---|---|
| DT/CP ads (calendar month) | So sánh vs TB T4–T6 (~19×) | **31/07/2026** |
| Lợi nhuận Sheet vs target 70M | ≥70M | 31/07/2026 |
| Chi phí/tin nhắn account | <25k (phễu+retarget) | **16/07**, **19/07** |
| LN sau ads | Ghi nhận trend | 31/07/2026 |

---

## Lưu ý Quisirella

- Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).
- Dòng **Quảng cáo** trên Sheet chỉ tham chiếu — **ROAS dùng Meta API spend**.
- **Không có** campaign-level ROAS từ Sheet — account-level + campaign spend drill.
- Đơn chốt DM **không** map 1-1 calendar month với ngày click ads.

---

## Pipeline đã dùng

```bash
python -m quisirella fetch-finance --month 2026-07
# meta-fetcher → data/meta_fetch/ (PRIMARY 07–13 + MTD 01–13)
```

**Raw:** `data/finance_fetch/bao_gia_2026_summary.json` · `data/finance_fetch/manifest.json`  
**Meta:** `data/meta_fetch/account_insights_2026-07-01_2026-07-13.json` · `data/meta_fetch/account_insights_2026-07-07_2026-07-13.json` · `data/meta_fetch/fetch_manifest_2026-07-07_2026-07-13.json`

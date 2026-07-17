---
title: Ghi chú lọc relevance — Quisirella
generated_at: 2026-07-13
data_range: 2026-07-07 đến 2026-07-13
sources: [relevance_rules.yaml, meta_graph_api, google_sheets]
data_status: ok
ad_account_id: act_400356462876861
---

# 04 — Relevance notes

## Bối cảnh

Áp dụng luật lọc từ [`config/relevance_rules.yaml`](../config/relevance_rules.yaml) lên **dữ liệu Meta thật** kỳ PRIMARY 07–13/07/2026 (account `act_400356462876861`), 3 campaign ACTIVE + finance T7 MTD.

---

## Nhận định từ data thực + verdict (13/07)

| Nhận định / insight | Verdict | Lý do |
|---|---|---|
| Phễu chi phí/tin 23.374 (PERIOD) / **18.580** (window 11–12) | **Giữ** | Dưới ngưỡng 25k; recency tốt |
| Phễu learning <50 mess/7d | **Giữ — không scale** | Learning caveat — P1 |
| Retarget 30.200 (PERIOD) / 32.425 (window) | **Giữ — watch cost** | Window >30k; IG-only FB=0 |
| Retarget FB spend = 0 | **Giữ** | Đã IG-only — không khuyên tắt lại |
| 1806 mess n/a KPI | **Giữ (context)** | `top_only` — KPI profile visit |
| 1806 CTR 6,13%, 575 link click PERIOD | **Giữ + sunset watch** | Đúng vai trò awareness |
| HardWear ADSET_PAUSED (last spend 10/07) | **Cần quyết định** | Re-enable nếu còn SKU (P0) |
| Carousel「Nỗi sợ 2」CPA 47.570 | **Loại / PAUSED** | Giữ tắt |
| Account PRIMARY 32.271/tin | **Giữ (context)** | Bị kéo bởi 1806 + Retarget watch |
| Jul MTD chi phí/tin 27.225 | **Giữ** | Account MTD tham chiếu |
| DT/CP Sheet 73,91× (partial) | **Cần kiểm chứng** | 9 đơn AOV cao — không scale signal |
| Purchase Meta trong insights | **Loại** | discard_criteria: pixel không tin cậy DM |
| Benchmark e-commerce mass-market | **Loại** | irrelevant_verticals |
| Catalog / DPA restock | **Loại** | Hàng 1-của-1 |
| Scale 1806 vì spend cao | **Loại** | Profile campaign — không so mess |
| Mở lại Facebook Retarget | **Loại** | IG-only đang chạy |
| Traffic objective campaigns | **Loại** | PAUSED, không spend PRIMARY |

---

## Insight Meta thường gặp — lọc theo Quisirella

| Insight generic | Verdict | Ghi chú |
|---|---|---|
| "Tăng budget khi ROAS cao" | **Cần kiểm chứng** | Sheet ≠ pixel; partial month 73,91× |
| "Thêm placement Facebook" | **Loại** (Retarget) | IG-only; FB=0 |
| "Giảm CPM bằng audience rộng" | **Loại** | Luxury secondhand — quality > volume |
| "Lookalike 10% để scale" | **Cần kiểm chứng** | Chỉ khi learning ≥50 mess/7d + sunset clear |
| "Pause segment vì CPA cao hơn trung bình" | **Cần kiểm chứng** | Breakdown Effect — không pause chỉ vì average |

---

## Phụ lục

| File | Nội dung |
|---|---|
| `config/relevance_rules.yaml` | Luật lọc |
| `data/meta_fetch/active/*_insights.json` | Campaign PRIMARY |
| `data/finance_fetch/bao_gia_2026_summary.json` | Sheet T7 |
| `output/06-active-campaigns-analysis.md` | Verdicts chi tiết |

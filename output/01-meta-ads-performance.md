---
title: Hiệu suất Meta Ads — Quisirella
generated_at: 2026-07-13
data_range: 2026-07-07 đến 2026-07-13
sources: [meta_graph_api]
data_status: ok
ad_account_id: act_400356462876861
---

# 01 — Hiệu suất Meta Ads (PRIMARY 07–13/07)

## Tóm tắt executive

| Campaign | funnel_role | Verdict | Chi phí/tin (PERIOD) | Chi phí/tin (window 11–12) |
|---|---|---|---:|---:|
| Phễu tin nhắn | top_middle | **Giữ** | 23.374 | **18.580** |
| 1806 Profile | top_only | **Giữ + sunset watch** | n/a (profile KPI) | n/a |
| Retarget Bán | bottom | **Giữ — theo dõi cost** | 30.200 | 32.425 |

**Account PERIOD 07–13:** spend **1.581.287 VND** · 49 tin nhắn · **32.271 VND**/tin.  
**Jul MTD 01–13 (tham chiếu):** spend **3.212.508 VND** · 118 tin nhắn · **27.225 VND**/tin.

Deep-dive ACTIVE: [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md).

> Purchase Meta **không phản ánh doanh thu thật** (chốt qua Instagram DM).

---

## Tổng quan account — PERIOD 07–13/07

| Chỉ số | Giá trị |
|---|---:|
| Ad account | `act_400356462876861` (quisirella) |
| Khoảng thời gian PRIMARY | 2026-07-07 → 2026-07-13 |
| Tổng chi tiêu (spend) | **1.581.287 VND** |
| Tin nhắn bắt đầu (7 ngày) | **49** |
| Chi phí / tin nhắn bắt đầu | **32.271 VND** |
| CTR | 4,77% |
| Engaged rate | 36,7% |
| Link click | 676 |

---

## 3 campaign ACTIVE — PERIOD 07–13/07

| Campaign | ID | funnel_role | Chi tiêu (VND) | Tin nhắn | Chi phí/tin nhắn | CTR | Engaged | Link click | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Chiến dịch phễu - target tin nhắn | 120253285175280110 | top_middle | 841.469 | 36 | **23.374** | 4,20% | 30,6% | 79 | **Giữ** |
| Chiến dịch Lượt tương tác mới - 1806 | 120252531135370110 | top_only | 437.817 | 3 | n/a (profile) | 6,13% | n/a | 575 | **Giữ + sunset watch** |
| Chiến dịch Lượt tương tác - Bán - Bản sao | 120252990977040110 | bottom | 302.001 | 10 | **30.200** | 3,10% | 60,0% | 22 | **Giữ — watch cost** |

**Verdict window (11–12/07):** Phễu **18.580**/tin → Retarget **32.425**/tin → 1806 (profile KPI, 211 link click).

---

## Jul MTD 01–13/07 (tham chiếu calendar)

| Chỉ số | Giá trị |
|---|---:|
| Meta spend | **3.212.508 VND** |
| Tin nhắn bắt đầu | **118** |
| Chi phí/tin nhắn | **27.225 VND** |

Finance Sheet + ROAS thực: [`03-finance-summary.md`](03-finance-summary.md).

---

## Phễu — cấu trúc inventory (fetch 13/07)

| Loại | Trạng thái | Ghi chú |
|---|---|---|
| Ad sets | **2** | ACTIVE: Lượt tương tác mới · PAUSED: nỗi sợ 2 (HardWear) |
| Ads | 3 | Nỗi sợ ACTIVE · HardWear ADSET_PAUSED (last spend 10/07) · carousel PAUSED |

Ad-level winner PERIOD: **「Nỗi sợ」19.731 VND/tin** (28 mess). Xem §7.1 [`06`](06-active-campaigns-analysis.md).

---

## Campaigns PAUSED (không chi tiêu trong kỳ PRIMARY)

Các campaign cũ (Traffic, 2905, Bản sao…) **PAUSED** — không spend PRIMARY. Không đưa vào benchmark ACTIVE.

---

## Finance cross-ref (T7 MTD)

| Chỉ số T7 MTD | Giá trị |
|---|---:|
| Doanh thu Sheet | 237.450.000 VND |
| Meta spend | 3.212.508 VND |
| Doanh thu / chi phí ads | **73,91×** *(partial)* |

Chi tiết: [`03-finance-summary.md`](03-finance-summary.md)

---

## Phụ lục nguồn

| File | Nội dung |
|---|---|
| `data/meta_fetch/account_insights_2026-07-07_2026-07-13.json` | Account PRIMARY |
| `data/meta_fetch/account_insights_2026-07-01_2026-07-13.json` | Account Jul MTD |
| `data/meta_fetch/active/*_insights.json` | Campaign insights |
| `data/meta_fetch/fetch_manifest_2026-07-07_2026-07-13.json` | Manifest fetch |

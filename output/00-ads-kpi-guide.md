---
title: Quisirella — Hướng dẫn đọc KPI Meta Ads
generated_at: 2026-07-02
purpose: claude_projects_knowledge_base
sources: [store_profile.yaml, meta_ads_analysis_rules]
---

# Hướng dẫn đọc KPI Meta Ads cho Quisirella

Quisirella chốt qua **Instagram DM** — đọc ads theo logic này, không theo shop e-commerce thông thường.

**Nền tảng:** Chỉ đánh giá placement **Instagram** (Feed, Reels, Stories). Policy & creative: `00-meta-ad-policy-ig.md`, `00-ig-ad-creative-guide.md`.

## Thứ tự ưu tiên KPI

| Ưu tiên | KPI | Ghi chú |
|---|---|---|
| **1 — Primary** | Tin nhắn bắt đầu (7 ngày) | `messaging_conversation_started_7d` |
| | Chi phí/tin nhắn | spend ÷ tin nhắn — **KPI vàng** |
| **2 — Secondary** | Lead Meta | Chi phí/lead |
| | Funnel depth | first_reply → depth_2 → depth_3 → depth_5 |
| **3 — Diagnostic** | CTR, CPC, CPM, reach, frequency | Không dùng làm KPI duy nhất |
| **4 — Engagement** | post_save, link_click | Chỉ meaningful khi so với tin nhắn |
| **5 — Deprioritize** | Purchase, ROAS Meta | Không tin cậy — ghi chú "chốt DM" |

## Công thức

```
Chi phí/tin nhắn     = spend / messaging_started_7d
Tỷ lệ tin nhắn/link  = messaging_started / link_click
Reply rate           = first_reply / messaging_started
Depth_3 rate         = depth_3 / messaging_started  (= engaged_rate — proxy mess chat luong)
Frequency            = impressions / reach
```

## Đo mess chất lượng (2 lớp)

| Lớp | Nguồn | Metric | Khi nào dùng |
|---|---|---|---|
| **Tự động** | Meta API | `engaged_rate = depth_3 / started` | Mọi lần fetch — proxy hội thoại tư vấn |
| **Thủ công** | [`08-dm-quality-log.md`](08-dm-quality-log.md) | mess chất, đơn chốt, doanh thu | Sunset, quality rate chính xác |

**Mục tiêu:** Tối đa mess chất lượng (khách tư vấn size/ship/cọc) — **không** volume. Chốt đơn phụ thuộc khách.

Chi tiết taxonomy: [`00-campaign-strategy.md`](00-campaign-strategy.md) · sổ ghi: [`08-dm-quality-log.md`](08-dm-quality-log.md).

## Benchmark tham khảo (account Quisirella)

| Mức | Chi phí/tin nhắn |
|---|---|
| Tốt | < 20.000 VND |
| Trung bình account | ~52.000 VND |
| Kém | > 55.000 VND |

CPM/CPC luxury jewelry VN **cao hơn** e-commerce giá rẻ — không so benchmark Shopee/FMCG.

## Red flags

| Tín hiệu | Ý nghĩa |
|---|---|
| link_click cao, tin nhắn thấp (<5%) | Campaign tối ưu click, không phải funnel DM |
| Chi phí/tin nhắn > 50k | Cần review |
| Lifetime budget > 70% spent | Sắp hết ngân sách |
| Facebook > 15% spend (ACTIVE) | IG-first — review loại FB |
| Frequency > 2.5 / 30 ngày | Có thể ad fatigue |

## Verdict khi tư vấn campaign

| Verdict | Khi nào |
|---|---|
| **scale** | Chi phí/tin nhắn thấp, funnel sâu, còn budget |
| **hold** | Ổn định, chưa đủ data |
| **optimize** | Tiềm năng nhưng placement/creative cần sửa |
| **reduce** | Chi tiêu cao, DM kém |
| **pause** | Không phù hợp DM, hết budget |
| **discard_insight** | Benchmark Meta không relevant — xem `00-relevance-filter.md` |

## Phân loại campaign

| Loại | Đánh giá chính |
|---|---|
| **DM funnel** (phễu, tin nhắn) | Chi phí/tin nhắn, depth_3 |
| **Product push** (Bán, Tiffany cụ thể) | Lead, depth_5 |
| **Engagement/reach** (link_click >> tin nhắn) | Reach, post_save — **không scale nếu DM kém** |

**Chi tiết 3 campaign hiện tại:** xem [`00-campaign-strategy.md`](00-campaign-strategy.md) — KPI theo `funnel_role` (Profile = cost/visit, không penalize mess kém).

Số liệu thực tế kỳ gần nhất: xem `01-meta-ads-performance.md` và `06-active-campaigns-analysis.md`.

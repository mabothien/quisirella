---
title: Quisirella — Chỉ mục knowledge base cho Claude
generated_at: 2026-07-02
purpose: claude_projects_knowledge_base
language: vi
---

# Chỉ mục — Claude AI nên đọc file nào?

Upload **toàn bộ** `output/*.md` lên Claude Project.

| Nhiệm vụ | File đọc trước |
|---|---|
| Tư vấn Meta Ads / campaign | Phần A (context) → [`00-campaign-strategy.md`](00-campaign-strategy.md) → Phần B (báo cáo) |
| **Viết/sửa caption Story/Post IG organic** | [`00-ig-organic-copy-guide.md`](00-ig-organic-copy-guide.md) + [`00-brands-channels.md`](00-brands-channels.md) |
| Viết copy **quảng cáo** Meta | [`00-ig-ad-creative-guide.md`](00-ig-ad-creative-guide.md) + [`00-meta-ad-policy-ig.md`](00-meta-ad-policy-ig.md) |

## Phần A — Context cửa hàng (đọc trước, ít thay đổi)

| # | File | Nội dung |
|---|---|---|
| 1 | [`00-business-overview.md`](00-business-overview.md) | Quisirella là gì, triết lý, nguồn hàng, đặc thù 1-của-1, chốt DM |
| 2 | [`00-brands-channels.md`](00-brands-channels.md) | Tiffany/Bvlgari trong ads vs Justin Davis IG organic |
| 3 | [`00-audience-pricing.md`](00-audience-pricing.md) | Khách hàng (nữ/nam), 3 phân khúc giá |
| 4 | [`00-ads-kpi-guide.md`](00-ads-kpi-guide.md) | Cách đọc chỉ số Meta Ads đúng cho Quisirella |
| 5 | [`00-campaign-strategy.md`](00-campaign-strategy.md) | **Mục đích 3 chiến dịch**, KPI theo vai trò, sunset Profile |
| 6 | [`00-meta-ad-policy-ig.md`](00-meta-ad-policy-ig.md) | Checklist Meta Ad Standards — IG, pre-owned luxury |
| 7 | [`00-ig-ad-creative-guide.md`](00-ig-ad-creative-guide.md) | Creative & copy quảng cáo Instagram (CTA DM) |
| 8 | [`00-ig-organic-copy-guide.md`](00-ig-organic-copy-guide.md) | **Rule + prompt** viết caption Story/Post IG organic (Claude & Cursor) |
| 9 | [`00-competitive-ig-used-luxury.md`](00-competitive-ig-used-luxury.md) | Competitive intel used luxury IG (qualitative) |
| 10 | [`00-claude-ads-learnings.md`](00-claude-ads-learnings.md) | Bản đồ tích hợp claude-ads → Quisirella (Meta DM-first) |
| 11 | [`00-relevance-filter.md`](00-relevance-filter.md) | Insight Meta nào giữ / loại |

## Phần B — Báo cáo ads (cập nhật định kỳ)

| # | File | Nội dung |
|---|---|---|
| 12 | [`01-meta-ads-performance.md`](01-meta-ads-performance.md) | Hiệu suất account 30 ngày |
| 13 | [`02-audience-insights.md`](02-audience-insights.md) | Breakdown tuổi/giới/placement (IG rows) |
| 14 | [`03-finance-summary.md`](03-finance-summary.md) | Ad spend, ROAS thực (khi có Sheet) |
| 15 | [`04-relevance-notes.md`](04-relevance-notes.md) | Verdict insight từng kỳ |
| 16 | [`05-recommendations.md`](05-recommendations.md) | Đề xuất tối ưu kỳ này |
| 17 | [`06-active-campaigns-analysis.md`](06-active-campaigns-analysis.md) | Deep-dive campaigns ACTIVE |

## Phần C — Nhật ký & sổ đo lường (Cursor / Claude)

| # | File | Nội dung |
|---|---|---|
| 18 | [`07-session-log.md`](07-session-log.md) | Hook audit trail — file edits, session metadata (tự động) |
| 19 | [`08-dm-quality-log.md`](08-dm-quality-log.md) | **Sổ ghi mess chất + đơn chốt + doanh thu** (manual + depth_3 proxy) |
| 20 | [`09-session-checkpoints.md`](09-session-checkpoints.md) | **Checkpoint user *lưu phiên*** — episodic memory chat mới (ưu tiên đọc trước khi tiếp tục) |

## Quy tắc khi tư vấn

1. **Luôn** đọc Phần A trước — không tư vấn generic e-commerce.
2. **Campaign analysis:** đọc `00-campaign-strategy.md` — đánh giá theo `funnel_role`, không penalize Profile vì mess kém. Mess chất/đơn: đọc `08-dm-quality-log.md`.
3. **Chỉ Instagram** — placement breakdown, creative, CTA; Facebook chỉ để review loại.
4. KPI chính: **chi phí/tin nhắn**, không phải purchase Meta.
5. Copy/creative tuân **Meta Ad Standards** — xem `00-meta-ad-policy-ig.md`.
6. Caption **organic** Story/Post → **bắt buộc** tuân [`00-ig-organic-copy-guide.md`](00-ig-organic-copy-guide.md) (rule + prompt mẫu); copy **ads** → `00-ig-ad-creative-guide.md`.
7. Competitive chỉ từ **used luxury IG** — không benchmark ngành khác.
8. **Không** đề xuất quảng cáo Justin Davis (chỉ bán IG organic).
9. **Không** loại bỏ targeting nam — phủ cả nữ và nam.
10. Khi có mâu thuẫn giữa pixel ROAS và business context → tin business context + DM.

## Meta Ads account

- Ad account: `act_400356462876861` (quisirella)
- Nền tảng bán: Instagram · Thị trường: Việt Nam · Tiền tệ: VND

**Skill references (repo):** `src/quisirella/skill/references/` — thinking_framework, andromeda_creative, health_score_dm, ab_test_dm, unit_economics_budget_dm, copy_frameworks_ig, competitor_meta_ig

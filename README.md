# Quisirella - Hệ thống quản lý Meta Ads

Cửa hàng trang sức đồ hiệu secondhand **Quisirella** (Tiffany & Co., Bvlgari, Justin Davis — bán trên Instagram).

**Mục đích:** thu thập dữ liệu Meta Ads, phân tích theo đặc thù cửa hàng, xuất file **Markdown** vào `output/` để upload lên [Claude Projects](https://claude.ai/) làm knowledge base.

---

## Workflow chính (khuyến nghị): Cursor + Meta MCP

Không cần `ANTHROPIC_API_KEY`, không cần `META_ACCESS_TOKEN`, không cần chạy Python agent.

### Setup Meta Ads MCP trong Cursor

**MCP chính:** [Pipeboard Meta Ads MCP](https://github.com/pipeboard-co/meta-ads-mcp) remote (`meta-ads.mcp.pipeboard.co`).

1. Kết nối Meta tại [pipeboard.co](https://pipeboard.co) → **Connection Successful**
2. Lấy API token tại [pipeboard.co/api-tokens](https://pipeboard.co/api-tokens)
3. Copy [`.cursor/mcp.json.example`](.cursor/mcp.json.example) → `.cursor/mcp.json`, thay `YOUR_PIPEBOARD_TOKEN`
4. Reload Cursor → MCP server `meta-ads` phải hiện **Connected**

**Read-only:** [`.cursor/permissions.json`](.cursor/permissions.json) — chỉ tool đọc Pipeboard trong mcpAllowlist; tool ghi bị chặn qua `autoRun.block_instructions`.

**Breakdown placement/age/gender:** dùng Pipeboard `get_insights` + `breakdown` (PoC: [`docs/mcp-poc-placement-breakdown.md`](docs/mcp-poc-placement-breakdown.md)).

**Backup fabrica (local token):** [`.cursor/mcp.json.fabrica`](.cursor/mcp.json.fabrica) — `@0xfabrica/mcp-meta-ads` nếu Pipeboard down.

**Lưu ý:** Token Pipeboard (`pk_...`) nằm trong `.cursor/mcp.json` (gitignored). Dữ liệu đi qua hạ tầng Pipeboard — không phải Graph API first-party trực tiếp từ máy bạn.

Meta MCP chính thức (`https://mcp.facebook.com/ads`) **không chạy được trên Cursor** với app tự cấu hình (DCR + redirect `cursor://` bị chặn).

### Bước 2 — Phân tích bằng Cursor AI

Trong chat Cursor, gửi prompt ví dụ:

```
Lấy insights Meta Ads 30 ngày gần nhất cho Quisirella.
Phân tích theo config/store_profile.yaml, config/campaign_strategy.yaml, lọc theo config/relevance_rules.yaml.
Chỉ dùng tool read-only. Ghi file 01-05 vào output/
```

Cursor rule [`.cursor/rules/quisirella-analysis.mdc`](.cursor/rules/quisirella-analysis.mdc) (router) tự hướng dẫn AI làm đúng workflow. Bộ rules expert:

| Rule | File | Nội dung |
|---|---|---|
| Router | `quisirella-analysis.mdc` | alwaysApply — config, safety, prompt mẫu |
| KPI | `quisirella-meta-kpi.mdc` | KPI hierarchy, red flags, verdict taxonomy |
| Data fetch | `quisirella-meta-data-fetch.mdc` | Checklist API/MCP read-only |
| Campaign | `quisirella-meta-campaign-analysis.mdc` | Framework phân tích campaign 6 bước |
| Audience | `quisirella-meta-audience-placement.mdc` | Breakdown × tier giá, placement IG-first |
| Output | `quisirella-meta-report-output.mdc` | Format Markdown `output/01-06` |

**Prompt mở rộng — phân tích ACTIVE campaigns:**

```
Phân tích các campaign ACTIVE trên act_400356462876861.
Đọc config/campaign_strategy.yaml — đánh giá theo funnel_role.
So sánh chi phí/tin nhắn, funnel depth, placement. Verdict scale/giữ/giảm/pause.
Ghi output/06-active-campaigns-analysis.md
```

### Bước 3 — Upload lên Claude Projects

Upload toàn bộ `output/*.md`. Claude đọc **theo thứ tự** trong [`output/00-index-claude-knowledge.md`](output/00-index-claude-knowledge.md).

**Phần A — Context cửa hàng (đọc trước):**

| File | Nội dung |
|---|---|
| `00-index-claude-knowledge.md` | Chỉ mục — Claude bắt đầu tại đây |
| `00-business-overview.md` | Business, triết lý, 1-của-1, chốt DM |
| `00-brands-channels.md` | Tiffany/Bvlgari ads vs Justin Davis IG organic |
| `00-audience-pricing.md` | Khách hàng nữ/nam, 3 phân khúc giá |
| `00-ads-kpi-guide.md` | Cách đọc KPI Meta Ads cho Quisirella |
| `00-campaign-strategy.md` | Mục đích 3 chiến dịch, KPI theo vai trò, sunset |
| `00-relevance-filter.md` | Insight Meta giữ / loại |

**Phần B — Báo cáo ads (cập nhật định kỳ):**

| File | Nội dung |
|---|---|
| `01-meta-ads-performance.md` | Spend, CPM, CPC, CTR, campaigns |
| `02-audience-insights.md` | Tệp khách × 3 phân khúc giá |
| `03-finance-summary.md` | Tài chính (khi có Google Sheets) |
| `04-relevance-notes.md` | Nhận định Meta đã loại (kỳ này) |
| `05-recommendations.md` | Đề xuất tối ưu (kỳ này) |
| `06-active-campaigns-analysis.md` | Deep-dive campaigns ACTIVE |

---

## Workflow nâng cao (tùy chọn): Pipeline Python tự động

Cần khi có `ANTHROPIC_API_KEY` và muốn chạy `python -m quisirella run` không qua Cursor.

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\pip install -e . --no-deps
copy .env.example .env
# Điền ANTHROPIC_API_KEY (+ META_ACCESS_TOKEN nếu chạy Meta MCP từ Python CLI)
```

Pipeline LangGraph: supervisor + 5 subagent (meta_ads, finance, audience, relevance, writer). Chi tiết trong `src/quisirella/`.

---

## Cấu hình cửa hàng

Sửa trực tiếp khi Quisirella thay đổi:

- [`config/store_profile.yaml`](config/store_profile.yaml) — thương hiệu, phân khúc giá, triết lý
- [`config/campaign_strategy.yaml`](config/campaign_strategy.yaml) — mục đích 3 chiến dịch, KPI theo vai trò, sunset
- [`config/relevance_rules.yaml`](config/relevance_rules.yaml) — lọc benchmark Meta sai ngành

---

## Cấu trúc project

```
.cursor/
  mcp.json.example       # Template MCP (copy → mcp.json, điền secrets)
  mcp.json                # Local only — gitignored
  rules/                  # 6 Cursor rules phân tích Meta Ads expert-level
config/                 # store_profile.yaml, campaign_strategy.yaml, relevance_rules.yaml
output/                 # Markdown cho Claude Projects
src/quisirella/         # Pipeline Python (tùy chọn)
```

---

## Tích hợp sau (chưa bật)

- **Google Sheets** — doanh thu, ROAS thực (`GOOGLE_SHEET_ID` trong `.env`)
- **Anthropic API** — chạy pipeline agent tự động

---

## An toàn

- Chỉ đọc dữ liệu Meta Ads (không tạo/sửa/bật chiến dịch qua MCP)
- Quyết định thay đổi quảng cáo luôn trong Ads Manager

# Quisirella - Hệ thống quản lý Meta Ads

Cửa hàng trang sức đồ hiệu secondhand **Quisirella** (Tiffany & Co., Bvlgari, Justin Davis — bán trên Instagram).

**Mục đích:** thu thập dữ liệu Meta Ads, phân tích theo đặc thù cửa hàng, xuất file **Markdown** vào `output/` để upload lên [Claude Projects](https://claude.ai/) làm knowledge base.

---

## Workflow chính (khuyến nghị): Cursor + Meta MCP

Không cần `ANTHROPIC_API_KEY`, không cần `META_ACCESS_TOKEN`, không cần chạy Python agent.

### Setup Meta Ads MCP trong Cursor

Meta MCP chính thức (`https://mcp.facebook.com/ads`) **không login OAuth được từ Cursor** (lỗi `Dynamic registration is not available`). Dùng **System User token** + MCP stdio:

1. Copy [`.cursor/mcp.json.example`](.cursor/mcp.json.example) → `.cursor/mcp.json`
2. Điền `META_APP_ID`, `META_APP_SECRET`, `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` (dạng `act_...`)
3. Reload Cursor → MCP server `meta-ads` phải hiện **Connected**

Token lấy từ: Meta Business Settings → System Users → Generate token → scope **`ads_read`** → gán ad account Quisirella.

**Kiểm tra token** (PowerShell):

```powershell
curl.exe -s "https://graph.facebook.com/v21.0/act_YOUR_ID?fields=name,account_status&access_token=YOUR_TOKEN"
```

Nếu lỗi `#200 ads_read permission` → token thiếu quyền hoặc chưa gán ad account cho System User. Token phải có scope `ads_read` (debug: `debug_token` không được chỉ có `pages_show_list`).

Package MCP: [`@0xfabrica/mcp-meta-ads`](https://github.com/0xfabrica/mcp-meta-ads) (stdio, không cần OAuth browser).

### Bước 2 — Phân tích bằng Cursor AI

Trong chat Cursor, gửi prompt ví dụ:

```
Lấy insights Meta Ads 30 ngày gần nhất cho Quisirella.
Phân tích theo config/store_profile.yaml, lọc theo config/relevance_rules.yaml.
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
- [`config/relevance_rules.yaml`](config/relevance_rules.yaml) — lọc benchmark Meta sai ngành

---

## Cấu trúc project

```
.cursor/
  mcp.json.example       # Template MCP (copy → mcp.json, điền secrets)
  mcp.json                # Local only — gitignored
  rules/                  # 6 Cursor rules phân tích Meta Ads expert-level
config/                 # store_profile.yaml, relevance_rules.yaml
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

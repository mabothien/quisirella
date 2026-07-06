# Quisirella - Hệ thống quản lý Meta Ads

Cửa hàng trang sức đồ hiệu secondhand **Quisirella** (Tiffany & Co., Bvlgari, Justin Davis — bán trên Instagram, chốt đơn qua DM).

**Mục đích:** thu thập dữ liệu **Meta Ads** + **doanh thu Google Sheet**, phân tích theo đặc thù cửa hàng, xuất file **Markdown** vào `output/` (và dùng trực tiếp trong Cursor).

---

## Workflow chính (khuyến nghị): Cursor + Meta MCP

Không cần `META_ACCESS_TOKEN` riêng khi dùng Pipeboard MCP trong Cursor.

### Setup Meta Ads MCP trong Cursor

**MCP chính:** [Pipeboard Meta Ads MCP](https://github.com/pipeboard-co/meta-ads-mcp) remote (`meta-ads.mcp.pipeboard.co`).

1. Kết nối Meta tại [pipeboard.co](https://pipeboard.co) → **Connection Successful**
2. Lấy API token tại [pipeboard.co/api-tokens](https://pipeboard.co/api-tokens)
3. Copy [`.cursor/mcp.json.example`](.cursor/mcp.json.example) → `.cursor/mcp.json`, thay `YOUR_PIPEBOARD_TOKEN`
4. Reload Cursor → MCP server `meta-ads` phải hiện **Connected**

**Read-only:** [`.cursor/permissions.json`](.cursor/permissions.json) — chỉ tool đọc Pipeboard; tool ghi Meta bị chặn qua hooks.

**Breakdown placement/age/gender:** Pipeboard `get_insights` + `breakdown` (PoC: [`docs/mcp-poc-placement-breakdown.md`](docs/mcp-poc-placement-breakdown.md)).

**Backup fabrica (local token):** [`.cursor/mcp.json.fabrica`](.cursor/mcp.json.fabrica) nếu Pipeboard down.

**Lưu ý:** Token Pipeboard (`pk_...`) trong `.cursor/mcp.json` (gitignored).

### Google Sheets — doanh thu (đã tích hợp)

Doanh thu/lợi nhuận chốt DM nằm trên Sheet — **nguồn ground truth** cho kinh doanh (Meta không đọc được DM).

1. Copy [`.env.example`](.env.example) → `.env`, điền `GOOGLE_SHEET_ID`
2. Đặt `credentials/service_account.json` (service account Google)
3. Share Sheet **Viewer** cho email trong service account
4. Mapping cell: [`config/finance_sheet.yaml`](config/finance_sheet.yaml) — tab **BÁO GIÁ 2026**

```powershell
pip install -e .
python -m quisirella fetch-finance --month 2026-07
```

Dữ liệu parse → `data/finance_fetch/bao_gia_2026_summary.json`. Router intent `finance_lookup` chỉ cần Sheet; ghép với Meta spend ở intent `full_business` (xem `quisirella-meta-finance.mdc`).

### Phân tích bằng Cursor AI

Trong chat, gõ tự nhiên — ví dụ:

```
lợi nhuận tháng 7 bao nhiêu
```

```
phân tích tình hình kinh doanh tháng 6
```

```
lưu phiên
```

Router: [`config/intent_router.yaml`](config/intent_router.yaml) + [`.cursor/rules/quisirella-analysis.mdc`](.cursor/rules/quisirella-analysis.mdc) — classify intent → pipeline subagent (finance-fetcher, meta-fetcher, meta-analyst, report-writer).

| Rule | File | Nội dung |
|---|---|---|
| Router | `quisirella-analysis.mdc` | Intent routing, safety, prompt mẫu |
| Finance | `quisirella-meta-finance.mdc` | Sheet = doanh thu; Meta = ads |
| Session memory | `quisirella-session-memory.mdc` | Checkpoint *lưu phiên* → `output/09` |
| KPI | `quisirella-meta-kpi.mdc` | KPI hierarchy, red flags |
| Campaign | `quisirella-meta-campaign-analysis.mdc` | Framework phân tích ACTIVE |

### Upload lên Claude Projects (tùy chọn)

Upload `output/*.md`. Đọc theo [`output/00-index-claude-knowledge.md`](output/00-index-claude-knowledge.md).

**Phần B — Báo cáo (cập nhật định kỳ):**

| File | Nội dung |
|---|---|
| `01-meta-ads-performance.md` | Hiệu suất account |
| `02-audience-insights.md` | Breakdown audience/placement |
| `03-finance-summary.md` | Sheet + Meta spend, unit economics |
| `04-relevance-notes.md` | Insight Meta đã lọc |
| `05-recommendations.md` | Đề xuất tối ưu |
| `06-active-campaigns-analysis.md` | Deep-dive campaigns ACTIVE |
| `09-session-checkpoints.md` | Checkpoint user *lưu phiên* |

---

## Phase B/C — Semantic router + Advanced RAG (local)

Intent routing và tra cứu knowledge base chạy **local** — không cần OpenAI API.

```powershell
pip install -e ".[dev]"
python -m quisirella index-intents
python -m quisirella index-knowledge
python -m quisirella route-intent "loi nhuan thang 7"
python -m quisirella search-knowledge "chi phi tin nhan pheu"
python -m quisirella eval-rag
```

**Phase C retrieval:** hybrid BM25 + E5 dense → cross-encoder rerank → `grade` (ok/low). Cursor agent rewrite/retry khi `grade: low` (không cần API). Headless: `search-knowledge --retry` + `RAG_LLM_PROVIDER` (none/ollama/anthropic).

- **Embedding:** `intfloat/multilingual-e5-small` · **Reranker:** `BAAI/bge-reranker-v2-m3`
- **HF token:** đặt `HF_TOKEN` trong `.env` ([tạo token read](https://huggingface.co/settings/tokens)) — tải model nhanh hơn
- **Incremental index:** `index-knowledge --incremental`
- **Golden eval:** `eval-rag` hoặc `pytest tests/test_rag_retrieval.py -q` (models load once per process)

Index: `data/intent_index/`, `data/knowledge_index/` (gitignored). Lần đầu tải model HuggingFace (~470MB embedding + ~400MB reranker).

---

## CLI hỗ trợ

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .
copy .env.example .env
# Điền GOOGLE_SHEET_ID + credentials/service_account.json
```

| Lệnh | Mô tả |
|---|---|
| `fetch-finance --month YYYY-MM` | Doanh thu/lợi nhuận từ Google Sheet |
| `index-intents` | Rebuild semantic intent index |
| `index-knowledge` | Rebuild RAG knowledge index (`--incremental` optional) |
| `route-intent "..."` | Intent shortlist (JSON) |
| `search-knowledge "..."` | Hybrid retrieve + rerank (`--retry` CRAG) |
| `eval-rag` | Golden query evaluation |

---

## Cấu hình cửa hàng

- [`config/store_profile.yaml`](config/store_profile.yaml) — thương hiệu, phân khúc giá
- [`config/campaign_strategy.yaml`](config/campaign_strategy.yaml) — 3 chiến dịch, KPI, sunset
- [`config/relevance_rules.yaml`](config/relevance_rules.yaml) — lọc benchmark Meta
- [`config/finance_sheet.yaml`](config/finance_sheet.yaml) — mapping Sheet BÁO GIÁ 2026
- [`config/intent_router.yaml`](config/intent_router.yaml) — intents, guards, pipelines

---

## Cấu trúc project

```
.cursor/
  mcp.json.example       # Template MCP (copy → mcp.json)
  rules/                 # Router + rules Meta Ads expert-level
  agents/                # meta-fetcher, finance-fetcher, meta-analyst, report-writer
  hooks/                 # Session memory, MCP write guard
config/                  # store, campaign, finance_sheet, intent_router
data/
  finance_fetch/         # JSON từ Google Sheet (gitignored)
  meta_fetch/            # JSON từ Meta API (gitignored)
  intent_index/          # Vector index intents (gitignored)
  knowledge_index/       # Vector index RAG (gitignored)
output/                  # Báo cáo Markdown + knowledge base
src/quisirella/
  retrieval/             # Phase B: embeddings, intent_index, knowledge_index
  tools/                 # finance_fetch, meta_mcp, sheets
```

---

## An toàn

- Chỉ đọc dữ liệu Meta Ads và Google Sheet (không ghi campaign, không sửa Sheet)
- Quyết định thay đổi quảng cáo luôn trong Ads Manager

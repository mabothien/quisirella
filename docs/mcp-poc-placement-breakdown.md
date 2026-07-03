# PoC — placement breakdown IG (fabrica vs pipeboard vs Graph API)

**Date:** 2026-07-03 (cập nhật: chuyển MCP chính sang Pipeboard remote)  
**Account:** `act_400356462876861`  
**Campaign tested:** `120252990977040110` (Bán retarget)  
**Window:** `last_7d`

## Kết luận nhanh

| Nguồn | Placement breakdown | DM funnel actions | Trạng thái Quisirella |
|---|---|---|---|
| **Graph API trực tiếp** | **PASS** | PASS | Fallback / verify |
| **@0xfabrica** (backup) | Không có param | Raw actions (aggregate) | `.cursor/mcp.json.fabrica` |
| **Pipeboard remote `get_insights`** | **PASS** (runtime PoC) | **PASS** (`messaging_user_depth_2`, `messaging_conversation_replied_7d`, …) | **MCP chính** |

## Pipeboard remote — runtime PoC (2026-07-03)

**Endpoint:** `https://meta-ads.mcp.pipeboard.co/?token=pk_...`  
**Server:** `meta-ads` v1.23.0

```json
tools/call get_insights {
  "object_id": "120252990977040110",
  "level": "campaign",
  "time_range": "last_7d",
  "breakdown": "publisher_platform,platform_position"
}
```

**Kết quả:** HTTP 200 — trả `actions` gồm DM funnel (`onsite_conversion.messaging_user_depth_2_message_send`, `messaging_conversation_replied_7d`, `total_messaging_connection`, …) và metrics per placement row.

→ Pipeboard **gộp** breakdown placement + DM actions trong một tool — thay fabrica + Graph API thủ công cho `meta-fetcher`.

**Lưu ý trust:** request đi qua hạ tầng Pipeboard; allowlist read-only trong `.cursor/permissions.json`.

## Graph API — ground truth (runtime evidence)

```http
GET /v21.0/120252990977040110/insights
  ?fields=spend,impressions,clicks,ctr
  &breakdowns=publisher_platform,platform_position
  &date_preset=last_7d
```

| publisher_platform | platform_position | spend (VND) | CTR |
|---|---|---:|---:|
| facebook | feed | 155.166 | 4,24% |
| instagram | feed | 150.186 | 4,59% |
| instagram | instagram_reels | 61.318 | 4,68% |
| instagram | instagram_stories | 40.692 | 2,80% |
| instagram | instagram_explore_grid_home | 22 | 0% |

## Fabrica — backup only

Tools: `get_account_insights`, `list_active_campaigns`, `get_entity_insights`, `get_campaign_performance` — không có breakdown. Khôi phục từ `.cursor/mcp.json.fabrica` nếu cần.

## Vận hành hiện tại

1. **MCP chính:** Pipeboard remote (`meta-ads` trong `.cursor/mcp.json`).
2. **Read-only:** ~45 tool trong `permissions.json` mcpAllowlist; block write qua `autoRun.block_instructions`.
3. **Fallback:** Graph API hoặc fabrica backup nếu Pipeboard lỗi.

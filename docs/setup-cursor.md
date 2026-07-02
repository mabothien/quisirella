# Thiết lập Meta Ads MCP qua Cursor

Làm theo các bước dưới đây. File này chứa nội dung cần tạo thủ công nếu chưa có trong project.

## 1. Tạo `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://mcp.facebook.com/ads",
      "transport": "http"
    }
  }
}
```

## 2. Authenticate trong Cursor

1. **Cursor Settings → MCP**
2. Server **`meta-ads`** → **Authenticate**
3. Login Meta Business → chọn ad account Quisirella

## 3. Tạo `.cursor/rules/quisirella-analysis.mdc`

```markdown
---
description: Workflow phân tích Quisirella — Meta Ads MCP, xuất Markdown
alwaysApply: true
---

# Quisirella — Phân tích Meta Ads

Đọc trước: config/store_profile.yaml, config/relevance_rules.yaml

- Dùng Meta MCP (meta-ads), chỉ tool read-only
- Thu thập: accounts, insights, audience breakdown, diagnostics, benchmarks
- Lọc nhận định Meta theo relevance_rules.yaml
- Ghi output/01-05*.md tiếng Việt, có frontmatter
- File 03 ghi "chưa có Google Sheets" nếu chưa tích hợp

Prompt mẫu: "Lấy insights Meta Ads 30 ngày, phân tích Quisirella, ghi output/"
```

## 4. File `.env` (tối giản — workflow Cursor không cần điền gì)

```env
# Workflow Cursor: để trống. Chỉ cần khi chạy python -m quisirella run sau này.
# ANTHROPIC_API_KEY=
# META_ACCESS_TOKEN=
```

## 5. Kiểm tra kết nối

Sau khi Authenticate xong, trong chat Cursor hỏi:

> Liệt kê ad accounts Meta Ads MCP có thể truy cập

Nếu trả về danh sách account = kết nối thành công.

## 6. Chạy phân tích lần đầu

> Lấy insights Meta Ads 30 ngày gần nhất cho Quisirella. Phân tích theo store profile, lọc relevance, ghi file 01-05 vào output/

Upload `output/*.md` lên Claude Projects.

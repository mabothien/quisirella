"""Google Sheets tools (service account auth).

The store owner shares the finance spreadsheet with the service account
email once; after that every run is non-interactive.
"""

from __future__ import annotations

import json
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain.tools import tool

from quisirella.settings import (
    GOOGLE_SERVICE_ACCOUNT_FILE,
    GOOGLE_SHEET_ID,
    GOOGLE_SHEET_RANGES,
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _sheets_service():
    key_file = Path(GOOGLE_SERVICE_ACCOUNT_FILE)
    if not key_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy service account key: {key_file}. "
            "Tạo service account trong Google Cloud, tải JSON key về đường dẫn này "
            "và share Google Sheet cho email của service account."
        )
    creds = service_account.Credentials.from_service_account_file(
        str(key_file), scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


@tool
def list_sheet_tabs() -> str:
    """Liệt kê tên các tab (sheet) trong Google Sheet tài chính của Quisirella."""
    service = _sheets_service()
    meta = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    return json.dumps({"spreadsheet": meta.get("properties", {}).get("title"), "tabs": tabs}, ensure_ascii=False)


@tool
def read_sheet_range(range_a1: str) -> str:
    """Đọc dữ liệu từ Google Sheet tài chính theo range A1 notation.

    Args:
        range_a1: Range cần đọc, ví dụ 'DoanhThu!A1:H100' hoặc 'ChiPhi!A:Z'.
    """
    service = _sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=GOOGLE_SHEET_ID, range=range_a1)
        .execute()
    )
    values = result.get("values", [])
    return json.dumps({"range": range_a1, "rows": values}, ensure_ascii=False)


@tool
def read_configured_finance_ranges() -> str:
    """Đọc toàn bộ các range tài chính đã cấu hình sẵn trong .env (GOOGLE_SHEET_RANGES)."""
    if not GOOGLE_SHEET_RANGES:
        return json.dumps(
            {"error": "GOOGLE_SHEET_RANGES chưa được cấu hình trong .env"},
            ensure_ascii=False,
        )
    service = _sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=GOOGLE_SHEET_ID, ranges=GOOGLE_SHEET_RANGES)
        .execute()
    )
    payload = [
        {"range": vr.get("range"), "rows": vr.get("values", [])}
        for vr in result.get("valueRanges", [])
    ]
    return json.dumps(payload, ensure_ascii=False)


SHEETS_TOOLS = [list_sheet_tabs, read_sheet_range, read_configured_finance_ranges]

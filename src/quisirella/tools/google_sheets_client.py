"""Shared Google Sheets API client (service account)."""

from __future__ import annotations

from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from quisirella.settings import GOOGLE_SERVICE_ACCOUNT_FILE

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def sheets_service():
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

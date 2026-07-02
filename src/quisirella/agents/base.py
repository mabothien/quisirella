"""Shared helpers for building subagents and inter-agent data exchange.

Agents communicate through two channels:
1. The supervisor passes tasks/results between them (tool-calling pattern).
2. Structured data is exchanged via SQLite snapshots (storage.db), so a later
   agent (audience, relevance, writer) can read exactly what an earlier agent
   (meta_ads, finance) collected.
"""

from __future__ import annotations

import json

from langchain_anthropic import ChatAnthropic
from langchain.tools import tool

from quisirella.settings import ANTHROPIC_API_KEY, MODEL
from quisirella.storage import db


def build_model() -> ChatAnthropic:
    return ChatAnthropic(model=MODEL, api_key=ANTHROPIC_API_KEY, max_tokens=8096)


def make_snapshot_tools(run_id: int, source: str) -> list:
    """Tools that let an agent persist and read run-scoped data snapshots."""

    @tool
    def save_data_snapshot(name: str, payload_json: str) -> str:
        """Lưu một snapshot dữ liệu (JSON string) vào kho lưu trữ của lần chạy hiện tại.

        Args:
            name: Tên snapshot, ví dụ 'campaign_insights', 'revenue_rows'.
            payload_json: Dữ liệu JSON (string) cần lưu.
        """
        try:
            payload = json.loads(payload_json)
        except json.JSONDecodeError:
            payload = {"raw_text": payload_json}
        db.save_snapshot(run_id, source, name, payload)
        return f"Đã lưu snapshot '{source}/{name}' cho run {run_id}."

    @tool
    def read_data_snapshot(snapshot_source: str, name: str) -> str:
        """Đọc snapshot dữ liệu do một agent khác đã lưu trong lần chạy hiện tại.

        Args:
            snapshot_source: Nguồn snapshot: 'meta_ads', 'finance', 'audience' hoặc 'relevance'.
            name: Tên snapshot cần đọc. Dùng list_available_snapshots để xem danh sách.
        """
        import sqlite3

        with sqlite3.connect(db.DB_PATH) as conn:
            row = conn.execute(
                "SELECT payload FROM snapshots WHERE run_id = ? AND source = ? AND name = ? "
                "ORDER BY id DESC LIMIT 1",
                (run_id, snapshot_source, name),
            ).fetchone()
        if not row:
            return f"Không tìm thấy snapshot '{snapshot_source}/{name}' trong run {run_id}."
        return row[0]

    @tool
    def read_previous_run_snapshot(snapshot_source: str, name: str) -> str:
        """Đọc snapshot cùng loại từ lần chạy TRƯỚC để so sánh xu hướng kỳ này với kỳ trước.

        Args:
            snapshot_source: Nguồn snapshot, ví dụ 'meta_ads' hoặc 'finance'.
            name: Tên snapshot cần đọc.
        """
        prev = db.get_previous_snapshot(run_id, snapshot_source, name)
        if prev is None:
            return "Chưa có dữ liệu từ lần chạy trước (đây có thể là lần chạy đầu tiên)."
        return json.dumps(prev, ensure_ascii=False)

    @tool
    def list_available_snapshots() -> str:
        """Liệt kê tất cả snapshot đã được các agent lưu trong lần chạy hiện tại."""
        return json.dumps(db.list_snapshots(run_id), ensure_ascii=False)

    return [
        save_data_snapshot,
        read_data_snapshot,
        read_previous_run_snapshot,
        list_available_snapshots,
    ]

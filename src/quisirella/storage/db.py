"""SQLite storage: one row per pipeline run, JSON snapshots per data source.

Keeping history lets agents compare the current period against previous runs
(week-over-week / month-over-month trends) instead of a single point in time.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from quisirella.settings import DATA_DIR

DB_PATH = DATA_DIR / "quisirella.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    since TEXT,
    until TEXT
);
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL REFERENCES runs(id),
    source TEXT NOT NULL,          -- e.g. 'meta_ads', 'finance', 'audience'
    name TEXT NOT NULL,            -- e.g. 'campaign_insights', 'revenue_rows'
    created_at TEXT NOT NULL,
    payload TEXT NOT NULL          -- JSON
);
"""


def _connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(_SCHEMA)
    return conn


def start_run(since: str | None, until: str | None) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO runs (started_at, since, until) VALUES (?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), since, until),
        )
        return cur.lastrowid


def save_snapshot(run_id: int, source: str, name: str, payload: object) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO snapshots (run_id, source, name, created_at, payload) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                run_id,
                source,
                name,
                datetime.now(timezone.utc).isoformat(),
                json.dumps(payload, ensure_ascii=False, default=str),
            ),
        )
    # Also drop a raw JSON file for easy manual inspection.
    raw_dir = DATA_DIR / f"run_{run_id}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_file: Path = raw_dir / f"{source}__{name}.json"
    raw_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def get_previous_snapshot(
    current_run_id: int, source: str, name: str
) -> dict | list | None:
    """Return the most recent snapshot of (source, name) from any earlier run."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT payload FROM snapshots "
            "WHERE run_id < ? AND source = ? AND name = ? "
            "ORDER BY run_id DESC, id DESC LIMIT 1",
            (current_run_id, source, name),
        ).fetchone()
    return json.loads(row[0]) if row else None


def list_snapshots(run_id: int) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT source, name, created_at FROM snapshots WHERE run_id = ?",
            (run_id,),
        ).fetchall()
    return [{"source": s, "name": n, "created_at": c} for s, n, c in rows]

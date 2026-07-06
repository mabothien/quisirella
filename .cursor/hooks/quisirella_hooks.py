#!/usr/bin/env python3
"""Quisirella Cursor hooks — session memory + Meta MCP safety.

Usage (from hooks.json):
  python .cursor/hooks/quisirella_hooks.py session-start
  python .cursor/hooks/quisirella_hooks.py log-file-edit
  python .cursor/hooks/quisirella_hooks.py log-session-end
  python .cursor/hooks/quisirella_hooks.py log-stop
  python .cursor/hooks/quisirella_hooks.py block-meta-writes
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT / "output" / "07-session-log.md"
CHECKPOINT_PATH = ROOT / "output" / "09-session-checkpoints.md"
INDEX_PATH = ROOT / "output" / "00-index-claude-knowledge.md"
INTENT_ROUTER_PATH = ROOT / "config" / "intent_router.yaml"
INTENT_INDEX_DIR = ROOT / "data" / "intent_index"
REFRESH_MARKER = ROOT / "data" / "meta_fetch" / ".last_refresh"

# Auto-refresh khi mo chat moi: chi ep refresh neu lan ghi bao cao gan nhat
# da qua nguong nay (tranh fetch trung khi mo nhieu chat trong ngay).
REFRESH_INTERVAL_HOURS = 12

# File bao cao dinh ky (ghi xong => danh dau refresh that su).
REPORT_FILE_PREFIXES = tuple(f"0{n}-" for n in range(1, 7))  # 01- .. 06-

WRITE_TOOL_PREFIXES = (
    "ads_create_",
    "ads_update_",
    "ads_activate_",
    "ads_delete_",
    "ads_manage_",
)


def _read_stdin_json() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def _ensure_log_header() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOG_PATH.exists():
        return
    LOG_PATH.write_text(
        """---
title: Quisirella — Nhat ky phien trao doi Meta Ads
generated_at: 2026-07-02
purpose: session_memory
language: vi
---

# 07 — Session log

Nhat ky tu dong tu Cursor hooks (sessionStart, afterFileEdit output/, sessionEnd, stop).
Doc truoc khi tiep tuc phan tich — ghi nho quyet dinh va file da cap nhat.

""",
        encoding="utf-8",
    )


def _append_log(section: str) -> None:
    _ensure_log_header()
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts}\n\n{section}\n")


def _emit_json(payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def _hours_since_last_refresh() -> float | None:
    """Gio troi qua ke tu lan ghi bao cao 01-06 gan nhat.

    None = chua tung refresh (marker khong ton tai / khong doc duoc) => coi nhu due.
    """
    if not REFRESH_MARKER.exists():
        return None
    try:
        raw = REFRESH_MARKER.read_text(encoding="utf-8").strip()
        ts = datetime.fromisoformat(raw)
    except (ValueError, OSError):
        return None
    if ts.tzinfo is None:
        ts = ts.astimezone()
    delta = datetime.now(timezone.utc).astimezone() - ts
    return delta.total_seconds() / 3600


def _mark_refresh_now() -> None:
    REFRESH_MARKER.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).astimezone().isoformat()
    REFRESH_MARKER.write_text(ts, encoding="utf-8")


def _read_latest_checkpoint(max_lines: int = 40) -> str:
    """Return the most recent ## Checkpoint block from 09-session-checkpoints.md."""
    if not CHECKPOINT_PATH.exists():
        return ""
    text = CHECKPOINT_PATH.read_text(encoding="utf-8")
    marker = "<!-- Checkpoints appended below"
    if marker in text:
        body = text.split(marker, 1)[-1]
    else:
        body = text
    blocks = [b.strip() for b in body.split("## Checkpoint") if b.strip()]
    if not blocks:
        return ""
    latest = "## Checkpoint" + blocks[-1]
    lines = latest.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["... (truncated)"]
    return "\n".join(lines)


def session_start() -> None:
    _ensure_log_header()
    index_note = "output/00-index-claude-knowledge.md"
    log_note = "output/07-session-log.md"
    checkpoint_note = "output/09-session-checkpoints.md"
    router_note = "config/intent_router.yaml"
    recent = ""
    if LOG_PATH.exists():
        lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
        recent = "\n".join(lines[-15:]) if len(lines) > 15 else "\n".join(lines[-8:])

    checkpoint = _read_latest_checkpoint()

    context = (
        "Quisirella Meta Ads session. "
        f"INTENT ROUTER (bat buoc truoc fetch): doc {router_note}; "
        "Phase B: python -m quisirella route-intent \"<user message>\" neu co data/intent_index/. "
        "chay pipeline YAML — xem quisirella-analysis.mdc. "
        f"Session checkpoint (uu tien): {checkpoint_note}. "
        f"Index: {index_note}. Session log: {log_note}. "
        "KPI primary: chi phi/tin nhan (DM-first). Sheet = doanh thu; Meta = ads only."
    )

    hours = _hours_since_last_refresh()
    if hours is None or hours >= REFRESH_INTERVAL_HOURS:
        age = "chua co bao cao truoc" if hours is None else f"{hours:.0f} gio truoc"
        context += (
            "\n\nAUTO-REFRESH NOTE (bao cao 01-06 cap nhat " + age + ", nguong "
            f"{REFRESH_INTERVAL_HOURS}h): SAU KHI classify intent — chi refresh neu intent la "
            "full_business hoac ads_analysis VA user khong noi skip refresh. "
            "finance_lookup, save_session, ig_organic_copy, cached_read, skip_refresh "
            "-> KHONG auto-refresh, KHONG fetch Meta dau chat. "
            "Pipeline: meta-fetcher -> meta-analyst -> report-writer (read-only). "
            "MCP loi -> data_status partial/unavailable, KHONG bia so."
        )
    else:
        context += (
            f"\n\nData con moi (refresh {hours:.0f} gio truoc, < {REFRESH_INTERVAL_HOURS}h) "
            "-> KHONG auto-refresh. Doc output/06 co san; chi refresh khi user yeu cau "
            "hoac intent full_business/ads_analysis."
        )

    if checkpoint.strip():
        context += f"\n\nLatest session checkpoint (09 — doc truoc khi tiep tuc):\n{checkpoint}"

    if recent.strip():
        context += f"\n\nRecent log tail (07):\n{recent}"

    _emit_json({"additional_context": context})


def log_file_edit() -> None:
    data = _read_stdin_json()
    file_path = data.get("file_path", "")
    if not file_path:
        sys.exit(0)

    normalized = file_path.replace("\\", "/")
    if "/output/" not in normalized and not normalized.endswith("/output"):
        sys.exit(0)

    name = Path(file_path).name
    edit_count = len(data.get("edits") or [])
    _append_log(f"- **File updated:** `{name}` ({edit_count} edit(s))")

    # Bao cao 01-06 vua duoc ghi => danh dau moc refresh that su (guard 12h).
    if name.startswith(REPORT_FILE_PREFIXES):
        _mark_refresh_now()

    sys.exit(0)


def log_session_end() -> None:
    data = _read_stdin_json()
    reason = data.get("reason", "unknown")
    duration_ms = data.get("duration_ms")
    session_id = data.get("session_id", "")[:8]
    dur = f"{duration_ms // 1000}s" if duration_ms else "n/a"
    _append_log(
        f"- **Session ended** `{session_id}` — reason: `{reason}`, duration: {dur}"
    )
    sys.exit(0)


def log_stop() -> None:
    data = _read_stdin_json()
    status = data.get("status", "unknown")
    loop_count = data.get("loop_count", 0)
    _append_log(f"- **Agent stop** — status: `{status}`, loop_count: {loop_count}")
    sys.exit(0)


def block_meta_writes() -> None:
    data = _read_stdin_json()
    tool_name = (data.get("tool_name") or "").lower()
    for prefix in WRITE_TOOL_PREFIXES:
        if prefix in tool_name:
            _emit_json(
                {
                    "permission": "deny",
                    "user_message": "Quisirella: chan thao tac ghi Meta Ads (read-only).",
                    "agent_message": (
                        f"Tool `{data.get('tool_name')}` blocked by project policy. "
                        "Use read-only insights tools only."
                    ),
                }
            )
            sys.exit(0)

    _emit_json({"permission": "allow"})
    sys.exit(0)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    handlers = {
        "session-start": session_start,
        "log-file-edit": log_file_edit,
        "log-session-end": log_session_end,
        "log-stop": log_stop,
        "block-meta-writes": block_meta_writes,
    }
    handler = handlers.get(mode)
    if not handler:
        sys.exit(0)
    handler()


if __name__ == "__main__":
    main()

"""CLI entry point.

Usage:
    python -m quisirella auth                       # one-time Meta Business OAuth
    python -m quisirella run                        # last 30 days
    python -m quisirella run --since 2026-06-01 --until 2026-06-30
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import date, timedelta

from quisirella.settings import ANTHROPIC_API_KEY, OUTPUT_DIR, ensure_dirs


def main() -> None:
    # Windows consoles default to cp1252 which cannot print Vietnamese.
    for stream in (sys.stdout, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="quisirella",
        description="Hệ thống agent quản lý Quisirella: thu thập Meta Ads + Google Sheets, "
        "xuất Markdown cho Claude Projects.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="OAuth với Meta Business (chạy 1 lần đầu tiên)")

    run_p = sub.add_parser("run", help="Chạy pipeline phân tích đầy đủ")
    run_p.add_argument("--since", help="Ngày bắt đầu (YYYY-MM-DD), mặc định 30 ngày trước")
    run_p.add_argument("--until", help="Ngày kết thúc (YYYY-MM-DD), mặc định hôm nay")

    args = parser.parse_args()
    ensure_dirs()

    if args.command == "auth":
        from quisirella.tools.meta_mcp import run_auth

        asyncio.run(run_auth())
        return

    if args.command == "run":
        if not ANTHROPIC_API_KEY:
            sys.exit("Thiếu ANTHROPIC_API_KEY trong .env (xem .env.example).")
        until = args.until or date.today().isoformat()
        since = args.since or (date.today() - timedelta(days=30)).isoformat()

        from quisirella.graph import run_pipeline

        summary = asyncio.run(run_pipeline(since, until))
        print("\n" + "=" * 70)
        print(summary)
        print("=" * 70)
        print(f"\nCác file Markdown nằm trong: {OUTPUT_DIR}")
        print("Upload các file này vào Claude Projects làm knowledge base.")


if __name__ == "__main__":
    main()

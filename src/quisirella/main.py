"""CLI entry point.

Usage:
    python -m quisirella auth                       # one-time Meta Business OAuth
    python -m quisirella run                        # last 30 days
    python -m quisirella run --since 2026-06-01 --until 2026-06-30
    python -m quisirella fetch-finance              # full finance fetch
    python -m quisirella fetch-finance --month 2026-06
    python -m quisirella index-intents            # rebuild intent vector index (Phase B)
    python -m quisirella route-intent "câu hỏi"   # semantic intent shortlist
    python -m quisirella index-knowledge          # rebuild knowledge RAG index
    python -m quisirella search-knowledge "..."   # search policy/report chunks
    python -m quisirella eval-rag                 # golden query evaluation (Phase C)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import date, timedelta

from quisirella.settings import ANTHROPIC_API_KEY, FINANCE_FETCH_DIR, OUTPUT_DIR, ensure_dirs


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

    ff_p = sub.add_parser("fetch-finance", help="Thu thập doanh thu từ Google Sheet")
    ff_p.add_argument(
        "--month",
        help="Tháng phân tích (YYYY-MM), ghi vào manifest date_range",
    )

    sub.add_parser("index-intents", help="Rebuild semantic intent index (Phase B)")

    ri_p = sub.add_parser("route-intent", help="Semantic intent shortlist cho câu hỏi")
    ri_p.add_argument("query", help="Câu hỏi free text")
    ri_p.add_argument("--top", type=int, default=5, help="Số intent candidates (default 5)")

    ik_p = sub.add_parser("index-knowledge", help="Rebuild knowledge RAG index (Phase B/C)")
    ik_p.add_argument(
        "--incremental",
        action="store_true",
        help="Chỉ re-embed file thay đổi (cần manifest)",
    )

    sk_p = sub.add_parser("search-knowledge", help="Tìm chunks policy/report/skill")
    sk_p.add_argument("query", help="Câu truy vấn")
    sk_p.add_argument("--top", type=int, default=10, help="Số chunks (default 10)")
    sk_p.add_argument("--type", dest="doc_type", help="Lọc doc_type: policy|report|rule|skill")
    sk_p.add_argument(
        "--retry",
        action="store_true",
        help="CRAG loop: retry với rewrite khi grade=low (optional LLM nếu .env)",
    )

    ev_p = sub.add_parser("eval-rag", help="Đánh giá golden queries (intent + knowledge)")
    ev_p.add_argument("--top", type=int, default=3, help="hit@k threshold (default 3)")

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
        return

    if args.command == "fetch-finance":
        from quisirella.tools.finance_fetch import fetch_finance

        try:
            manifest = fetch_finance(period=args.month)
        except Exception as exc:
            sys.exit(f"fetch-finance thất bại: {exc}")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        print(f"\nĐã ghi vào: {FINANCE_FETCH_DIR}")
        return

    if args.command == "index-intents":
        from quisirella.retrieval.intent_index import build_intent_index

        try:
            manifest = build_intent_index()
        except Exception as exc:
            sys.exit(f"index-intents thất bại: {exc}")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return

    if args.command == "route-intent":
        from quisirella.retrieval.intent_index import route_intent

        try:
            result = route_intent(args.query, top_k=args.top)
        except Exception as exc:
            sys.exit(f"route-intent thất bại: {exc}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.command == "index-knowledge":
        from quisirella.retrieval.knowledge_index import build_knowledge_index

        try:
            manifest = build_knowledge_index(
                reset=not args.incremental,
                incremental=args.incremental,
            )
        except Exception as exc:
            sys.exit(f"index-knowledge thất bại: {exc}")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return

    if args.command == "search-knowledge":
        try:
            if args.retry:
                from quisirella.retrieval.crag import run_retrieval_with_retry

                result = run_retrieval_with_retry(
                    args.query,
                    top_k=args.top,
                    doc_type=args.doc_type,
                )
            else:
                from quisirella.retrieval.knowledge_index import search_knowledge

                result = search_knowledge(
                    args.query,
                    top_k=args.top,
                    doc_type=args.doc_type,
                )
        except Exception as exc:
            sys.exit(f"search-knowledge thất bại: {exc}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.command == "eval-rag":
        from quisirella.retrieval.eval_rag import run_eval_rag

        try:
            result = run_eval_rag(top_k=args.top)
        except Exception as exc:
            sys.exit(f"eval-rag thất bại: {exc}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result.get("overall_pass"):
            sys.exit(1)
        return


if __name__ == "__main__":
    main()

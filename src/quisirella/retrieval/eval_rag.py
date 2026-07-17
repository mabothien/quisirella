"""Evaluate intent routing and knowledge retrieval against golden queries."""

from __future__ import annotations

import time
from typing import Any

import yaml

from quisirella.retrieval.faithfulness import check_claim_faithfulness
from quisirella.retrieval.intent_index import route_intent
from quisirella.retrieval.knowledge_index import search_knowledge
from quisirella.retrieval.session import RetrievalSession, get_retrieval_session
from quisirella.settings import RAG_EVAL_PATH


def _load_eval_config() -> dict[str, Any]:
    with open(RAG_EVAL_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _hit_at_k(candidates: list[str], expected: str, k: int = 3) -> bool:
    return expected in candidates[:k]


def _source_hit(chunks: list[dict[str, Any]], expect_any: list[str]) -> bool:
    sources = [c.get("source_file", "") for c in chunks]
    joined = " ".join(sources).lower()
    for needle in expect_any:
        if needle.lower() in joined:
            return True
    return False


def eval_intents(*, top_k: int = 3, session: RetrievalSession | None = None) -> dict[str, Any]:
    cfg = _load_eval_config()
    cases = cfg.get("intent_queries") or []
    results: list[dict[str, Any]] = []
    hits = 0
    intent_store = session.intent_store if session else None

    for case in cases:
        query = case["query"]
        expected = case["expect_intent"]
        accept = case.get("accept_intents") or [expected]
        routed = route_intent(query, top_k=5, store=intent_store)
        got = routed.get("top_intent")
        candidates = [c.get("intent_id") for c in routed.get("candidates") or []]
        hit = got in accept or _hit_at_k(candidates, expected, top_k) or any(
            a in candidates[:top_k] for a in accept
        )
        if hit:
            hits += 1
        results.append(
            {
                "query": query,
                "expected": expected,
                "got": got,
                "candidates": candidates[:top_k],
                "hit": hit,
                "source": routed.get("source"),
            }
        )

    total = len(cases)
    return {
        "metric": f"intent_hit@{top_k}",
        "hits": hits,
        "total": total,
        "rate": round(hits / total, 4) if total else 0.0,
        "pass": total > 0 and (hits / total) >= 0.9,
        "results": results,
    }


def eval_knowledge(*, top_k: int = 3, session: RetrievalSession | None = None) -> dict[str, Any]:
    cfg = _load_eval_config()
    cases = cfg.get("knowledge_queries") or []
    results: list[dict[str, Any]] = []
    hits = 0
    knowledge_store = session.knowledge_store if session else None

    for case in cases:
        query = case["query"]
        expect_any = case.get("expect_sources_any") or []
        searched = search_knowledge(
            query,
            top_k=10,
            expand=True,
            store=knowledge_store,
        )
        chunks = searched.get("chunks") or []
        hit = _source_hit(chunks[:top_k], expect_any)
        if hit:
            hits += 1
        results.append(
            {
                "query": query,
                "expect_sources_any": expect_any,
                "got_sources": [c.get("source_file") for c in chunks[:top_k]],
                "grade": searched.get("grade"),
                "retrieval_confidence": searched.get("retrieval_confidence"),
                "hit": hit,
            }
        )

    total = len(cases)
    return {
        "metric": f"knowledge_hit@{top_k}",
        "hits": hits,
        "total": total,
        "rate": round(hits / total, 4) if total else 0.0,
        "pass": total > 0 and (hits / total) >= 0.7,
        "results": results,
    }


def eval_faithfulness(*, session: RetrievalSession | None = None) -> dict[str, Any]:
    cfg = _load_eval_config()
    cases = cfg.get("faithfulness_samples") or []
    results: list[dict[str, Any]] = []
    passes = 0
    knowledge_store = session.knowledge_store if session else None

    for case in cases:
        claim = case["claim"]
        expect = bool(case.get("expect_faithful", True))
        searched = search_knowledge(claim, top_k=5, store=knowledge_store)
        chunks = searched.get("chunks") or []
        check = check_claim_faithfulness(claim, chunks)
        ok = check["faithful"] == expect
        if ok:
            passes += 1
        results.append(
            {
                "claim": claim,
                "expect_faithful": expect,
                "faithful": check["faithful"],
                "overlap_ratio": check["overlap_ratio"],
                "pass": ok,
            }
        )

    total = len(cases)
    return {
        "metric": "faithfulness_smoke",
        "passes": passes,
        "total": total,
        "pass": passes == total if total else True,
        "results": results,
    }


def run_eval_rag(*, top_k: int = 3) -> dict[str, Any]:
    t0 = time.perf_counter()
    session = get_retrieval_session()
    warmup_ms = round((time.perf_counter() - t0) * 1000)

    t1 = time.perf_counter()
    intent = eval_intents(top_k=top_k, session=session)
    knowledge = eval_knowledge(top_k=top_k, session=session)
    faith = eval_faithfulness(session=session)
    eval_ms = round((time.perf_counter() - t1) * 1000)

    overall = intent["pass"] and knowledge["pass"] and faith["pass"]
    return {
        "status": "ok" if overall else "fail",
        "overall_pass": overall,
        "warmup": {**session.as_manifest(), "warmup_ms": warmup_ms},
        "eval_ms": eval_ms,
        "intent": intent,
        "knowledge": knowledge,
        "faithfulness": faith,
    }

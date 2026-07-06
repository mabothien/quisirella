"""Corrective RAG loop — local retrieval with optional LLM rewrite."""

from __future__ import annotations

from typing import Any

from quisirella.retrieval.knowledge_index import search_knowledge
from quisirella.retrieval.llm_optional import rewrite_query_llm


def run_retrieval_with_retry(
    query: str,
    *,
    top_k: int = 10,
    doc_type: str | None = None,
    max_retries: int = 2,
    use_llm_rewrite: bool = True,
) -> dict[str, Any]:
    """Retrieve → grade → optional rewrite retry (LLM only when RAG_LLM_PROVIDER set)."""
    attempts: list[dict[str, Any]] = []
    current_query = query

    for attempt in range(max_retries + 1):
        result = search_knowledge(
            current_query,
            top_k=top_k,
            doc_type=doc_type,
            expand=True,
        )
        result["attempt"] = attempt + 1
        attempts.append(
            {
                "attempt": attempt + 1,
                "query": current_query,
                "grade": result.get("grade"),
                "retrieval_confidence": result.get("retrieval_confidence"),
                "chunk_count": result.get("chunk_count", 0),
            }
        )

        if result.get("grade") == "ok" or result.get("status") != "ok":
            result["attempts"] = attempts
            result["final_query"] = current_query
            return result

        if attempt >= max_retries:
            break

        rewritten: str | None = None
        if use_llm_rewrite:
            rewritten = rewrite_query_llm(
                current_query,
                reason=f"grade={result.get('grade')} confidence={result.get('retrieval_confidence')}",
            )

        if rewritten and rewritten.lower() != current_query.lower():
            current_query = rewritten
        else:
            # Heuristic fallback: append domain hint
            current_query = f"{query} chi phí tin nhắn campaign KPI Quisirella"

    result["attempts"] = attempts
    result["final_query"] = current_query
    result["grade"] = result.get("grade", "low")
    return result

"""Retrieval confidence grading (heuristic, no LLM)."""

from __future__ import annotations

from typing import Any

from quisirella.retrieval.scoring import (
    RAG_HIGH_CONFIDENCE,
    RAG_SCORE_FLOOR,
    is_ambiguous_top2,
)


def grade_retrieval(chunks: list[dict[str, Any]]) -> tuple[str, float]:
    """Return (grade, retrieval_confidence) where grade is ok|low|missing."""
    if not chunks:
        return "missing", 0.0

    top = float(chunks[0].get("score", 0.0))
    second = float(chunks[1].get("score", 0.0)) if len(chunks) >= 2 else None

    if is_ambiguous_top2(
        top,
        second,
        score_floor=RAG_SCORE_FLOOR,
        high_confidence=RAG_HIGH_CONFIDENCE,
    ):
        return "low", top

    return "ok", top

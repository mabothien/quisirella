"""Shared retrieval confidence thresholds (intent + knowledge RAG)."""

from __future__ import annotations

from quisirella.settings import (
    INTENT_SCORE_FLOOR,
    RAG_AMBIGUOUS_MARGIN,
    RAG_HIGH_CONFIDENCE,
    RAG_SCORE_FLOOR,
)


def is_ambiguous_top2(
    top: float,
    second: float | None,
    *,
    score_floor: float,
    margin: float = RAG_AMBIGUOUS_MARGIN,
    high_confidence: float | None = None,
) -> bool:
    """True when top score is below floor or too close to second (optional high-confidence bypass)."""
    if top < score_floor:
        return True
    if second is None:
        return False
    if high_confidence is not None and top >= high_confidence:
        return False
    return (top - second) < margin


__all__ = [
    "INTENT_SCORE_FLOOR",
    "RAG_SCORE_FLOOR",
    "RAG_AMBIGUOUS_MARGIN",
    "RAG_HIGH_CONFIDENCE",
    "is_ambiguous_top2",
]

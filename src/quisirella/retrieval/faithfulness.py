"""Heuristic faithfulness check — policy claims vs retrieved chunks."""

from __future__ import annotations

import re
from typing import Any

_TOKEN_RE = re.compile(r"[\w]{4,}", re.UNICODE)
_STOP = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "from",
    "when",
    "meta",
    "campaign",
    "quisirella",
    "nên",
    "cần",
    "theo",
    "trong",
    "hoặc",
}


def _keywords(text: str) -> set[str]:
    tokens = {t.lower() for t in _TOKEN_RE.findall(text)}
    return {t for t in tokens if t not in _STOP and not t.isdigit()}


def check_claim_faithfulness(
    claim: str,
    chunks: list[dict[str, Any]],
    *,
    min_overlap_ratio: float = 0.25,
) -> dict[str, Any]:
    """Check if claim keywords appear in union of chunk contents (heuristic)."""
    claim_kw = _keywords(claim)
    if not claim_kw:
        return {"faithful": True, "overlap_ratio": 1.0, "matched_keywords": []}

    corpus = " ".join(c.get("content", "") for c in chunks)
    corpus_kw = _keywords(corpus)
    matched = claim_kw & corpus_kw
    ratio = len(matched) / len(claim_kw) if claim_kw else 0.0

    return {
        "faithful": ratio >= min_overlap_ratio,
        "overlap_ratio": round(ratio, 4),
        "matched_keywords": sorted(matched),
        "claim_keyword_count": len(claim_kw),
    }


def check_recommendations(
    recommendations: list[str],
    chunks: list[dict[str, Any]],
) -> dict[str, Any]:
    results = []
    for rec in recommendations:
        results.append({"recommendation": rec, **check_claim_faithfulness(rec, chunks)})

    faithful_count = sum(1 for r in results if r["faithful"])
    return {
        "total": len(results),
        "faithful_count": faithful_count,
        "all_faithful": faithful_count == len(results) if results else True,
        "details": results,
    }

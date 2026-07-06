"""Cross-encoder reranking for knowledge retrieval."""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

from quisirella.retrieval.hf_hub import configure_hf_hub
from quisirella.settings import HF_TOKEN, RERANKER_MODEL

# ~512 tokens — truncate chars to avoid silent CrossEncoder clipping on long chunks
RERANK_MAX_CONTENT_CHARS = 1500


@lru_cache(maxsize=1)
def _get_cross_encoder():
    configure_hf_hub(HF_TOKEN)
    from sentence_transformers import CrossEncoder

    return CrossEncoder(RERANKER_MODEL, max_length=512, device="cpu")


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _rerank_passage(content: str) -> str:
    text = (content or "").strip()
    if len(text) <= RERANK_MAX_CONTENT_CHARS:
        return text
    return text[:RERANK_MAX_CONTENT_CHARS]


def apply_freshness_boost(chunks: list[dict[str, Any]], *, boost_weight: float = 0.08) -> list[dict[str, Any]]:
    """Boost scores by doc_priority and relative mtime within result set."""
    if not chunks:
        return chunks

    mtimes = [float(c.get("mtime") or 0) for c in chunks]
    max_mtime = max(mtimes) if mtimes else 0.0
    min_mtime = min(mtimes) if mtimes else 0.0
    span = max_mtime - min_mtime

    boosted: list[dict[str, Any]] = []
    for chunk, mtime in zip(chunks, mtimes):
        priority = int(chunk.get("doc_priority") or 1)
        recency = (mtime - min_mtime) / span if span > 0 else 0.0
        base = float(chunk.get("score", 0.0))
        adjusted = base * (1.0 + boost_weight * priority) + boost_weight * recency
        item = dict(chunk)
        item["score"] = round(min(1.0, adjusted), 4)
        item["score_before_boost"] = round(base, 4)
        boosted.append(item)

    return sorted(boosted, key=lambda c: c["score"], reverse=True)


def rerank_chunks(
    query: str,
    chunks: list[dict[str, Any]],
    *,
    top_k: int = 10,
) -> list[dict[str, Any]]:
    """Rerank candidate chunks with cross-encoder; normalize scores to 0-1."""
    if not chunks:
        return []

    if len(chunks) == 1:
        only = dict(chunks[0])
        only["score"] = only.get("score", 0.5)
        only["rerank_raw"] = 0.0
        return [only]

    pairs = [(query, _rerank_passage(c.get("content", ""))) for c in chunks]
    encoder = _get_cross_encoder()
    raw_scores = encoder.predict(pairs)

    scored: list[dict[str, Any]] = []
    for chunk, raw in zip(chunks, raw_scores):
        item = dict(chunk)
        item["rerank_raw"] = float(raw)
        item["score"] = round(_sigmoid(float(raw)), 4)
        scored.append(item)

    scored.sort(key=lambda c: c["score"], reverse=True)
    return apply_freshness_boost(scored[:top_k])

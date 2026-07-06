"""Lightweight context compression — only when retrieved context is very large."""

from __future__ import annotations

from typing import Any

# Rough chars threshold before trimming (~6000 tokens ≈ 24000 chars)
COMPRESS_CHAR_THRESHOLD = 24_000
MIN_CHUNK_CHARS = 800


def _chunk_chars(chunks: list[dict[str, Any]]) -> int:
    return sum(len(c.get("content", "")) for c in chunks)


def compress_chunks(query: str, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep full chunks when small; trim low-score tail when over threshold."""
    if not chunks:
        return chunks

    total = _chunk_chars(chunks)
    if total <= COMPRESS_CHAR_THRESHOLD:
        return chunks

    # Effectiveness > token: keep top chunks by score until under threshold
    sorted_chunks = sorted(chunks, key=lambda c: c.get("score", 0), reverse=True)
    kept: list[dict[str, Any]] = []
    running = 0
    for chunk in sorted_chunks:
        content = chunk.get("content", "")
        if len(content) < MIN_CHUNK_CHARS or running + len(content) <= COMPRESS_CHAR_THRESHOLD:
            kept.append(chunk)
            running += len(content)
        if running >= COMPRESS_CHAR_THRESHOLD:
            break

    kept_ids = {id(c) for c in kept}
    return [c for c in chunks if id(c) in kept_ids] or sorted_chunks[:5]

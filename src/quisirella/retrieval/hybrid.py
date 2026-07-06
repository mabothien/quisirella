"""Hybrid BM25 + dense retrieval with reciprocal rank fusion."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi

from quisirella.retrieval.embeddings import prefix_for_query
from quisirella.settings import KNOWLEDGE_INDEX_DIR

BM25_CORPUS_FILE = "bm25_corpus.json"
RRF_K = 60


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[\w]+", text, re.UNICODE) if t.strip()]


def corpus_path() -> Path:
    return KNOWLEDGE_INDEX_DIR / BM25_CORPUS_FILE


def _corpus_mtime() -> float:
    path = corpus_path()
    return path.stat().st_mtime if path.exists() else 0.0


def save_bm25_corpus(records: list[dict[str, Any]]) -> None:
    KNOWLEDGE_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with open(corpus_path(), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    _cached_bm25_bundle.cache_clear()


def load_bm25_corpus() -> list[dict[str, Any]]:
    path = corpus_path()
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _build_bm25(records: list[dict[str, Any]]) -> BM25Okapi | None:
    if not records:
        return None
    tokenized = [_tokenize(r.get("search_text", "")) for r in records]
    return BM25Okapi(tokenized)


@lru_cache(maxsize=2)
def _cached_bm25_bundle(corpus_mtime: float) -> tuple[Any, tuple[dict[str, Any], ...]]:
    """Cache BM25Okapi + records; invalidate when corpus file mtime changes."""
    records = tuple(load_bm25_corpus())
    if not records:
        return None, ()
    return _build_bm25(list(records)), records


def _get_bm25_index() -> tuple[BM25Okapi | None, list[dict[str, Any]]]:
    mtime = _corpus_mtime()
    bm25, records_tuple = _cached_bm25_bundle(mtime)
    return bm25, list(records_tuple)


def _rrf_merge(ranked_lists: list[list[str]], *, limit: int) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, chunk_id in enumerate(ranked, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ordered[:limit]


def hybrid_search(
    store: Chroma,
    query: str,
    *,
    top_k: int = 10,
    fetch_k: int = 30,
    doc_type: str | None = None,
    query_variants: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Merge BM25 and dense Chroma results via RRF; return chunk dicts with rrf_score."""
    bm25, records = _get_bm25_index()
    if not records:
        return _dense_only(store, query, top_k=top_k, doc_type=doc_type)

    by_id = {r["chunk_id"]: r for r in records}
    variants = query_variants or [query]

    dense_ids: list[str] = []
    for variant in variants:
        prefixed = prefix_for_query(variant)
        if doc_type:
            results = store.similarity_search_with_score(
                prefixed, k=fetch_k, filter={"doc_type": doc_type}
            )
        else:
            results = store.similarity_search_with_score(prefixed, k=fetch_k)
        for doc, _distance in results:
            chunk_id = doc.metadata.get("chunk_id")
            if chunk_id and chunk_id not in dense_ids:
                dense_ids.append(chunk_id)
        if len(dense_ids) >= fetch_k:
            break
    dense_ids = dense_ids[:fetch_k]

    bm25_ids: list[str] = []
    if bm25 is not None:
        combined_tokens: list[str] = []
        for variant in variants:
            combined_tokens.extend(_tokenize(variant))
        scores = bm25.get_scores(list(dict.fromkeys(combined_tokens)))
        ranked_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        for idx in ranked_idx[:fetch_k]:
            rec = records[idx]
            cid = rec["chunk_id"]
            if doc_type and rec.get("doc_type") != doc_type:
                continue
            if cid not in bm25_ids:
                bm25_ids.append(cid)

    merged = _rrf_merge([dense_ids, bm25_ids], limit=fetch_k)
    out: list[dict[str, Any]] = []
    for chunk_id, rrf_score in merged:
        rec = by_id.get(chunk_id)
        if not rec:
            continue
        out.append(
            {
                "chunk_id": chunk_id,
                "rrf_score": round(rrf_score, 6),
                "source_file": rec.get("source_file", ""),
                "section_title": rec.get("section_title", ""),
                "doc_type": rec.get("doc_type", ""),
                "doc_priority": rec.get("doc_priority", 1),
                "mtime": rec.get("mtime", 0),
                "content": rec.get("content", ""),
            }
        )
    return out[:fetch_k]


def _dense_only(
    store: Chroma,
    query: str,
    *,
    top_k: int,
    doc_type: str | None,
) -> list[dict[str, Any]]:
    prefixed = prefix_for_query(query)
    if doc_type:
        results = store.similarity_search_with_score(
            prefixed, k=top_k, filter={"doc_type": doc_type}
        )
    else:
        results = store.similarity_search_with_score(prefixed, k=top_k)

    out: list[dict[str, Any]] = []
    for doc, distance in results:
        score = max(0.0, 1.0 - (float(distance) / 2.0))
        meta = doc.metadata or {}
        out.append(
            {
                "chunk_id": meta.get("chunk_id", ""),
                "rrf_score": round(score, 6),
                "source_file": meta.get("source_file", ""),
                "section_title": meta.get("section_title", ""),
                "doc_type": meta.get("doc_type", ""),
                "doc_priority": meta.get("doc_priority", 1),
                "mtime": meta.get("mtime", 0),
                "content": doc.page_content.removeprefix("passage: ").strip(),
            }
        )
    return out

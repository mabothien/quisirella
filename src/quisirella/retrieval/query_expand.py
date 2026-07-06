"""Heuristic query expansion for Vietnamese Meta Ads domain terms."""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache
from typing import Any

import yaml

from quisirella.settings import RAG_SYNONYMS_PATH

_TOKEN_RE = re.compile(r"[\w]+", re.UNICODE)


def strip_diacritics(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text) if t.strip()]


@lru_cache(maxsize=1)
def _load_synonym_entries() -> tuple[tuple[str, tuple[str, ...]], ...]:
    if not RAG_SYNONYMS_PATH.exists():
        return ()
    with open(RAG_SYNONYMS_PATH, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    entries: list[tuple[str, tuple[str, ...]]] = []
    seen_keys: set[str] = set()
    for key, values in (raw.get("synonyms") or {}).items():
        canonical = str(key).strip().lower()
        if not canonical or canonical in seen_keys:
            continue
        seen_keys.add(canonical)
        aliases = tuple(str(v).strip() for v in (values or []) if str(v).strip())
        entries.append((canonical, aliases))
    return tuple(entries)


def _match_synonym_terms(query: str, entries: tuple[tuple[str, tuple[str, ...]], ...]) -> list[str]:
    """Match multi-word phrases and single tokens against synonym map."""
    lower = query.lower()
    nodiac = strip_diacritics(lower)
    extra: list[str] = []
    seen_extra: set[str] = set()

    def _add(term: str) -> None:
        t = term.strip()
        if t and t.lower() not in seen_extra:
            seen_extra.add(t.lower())
            extra.append(t)

    for canonical, aliases in entries:
        key_nodiac = strip_diacritics(canonical)
        if canonical in lower or key_nodiac in nodiac:
            _add(canonical)
            for alias in aliases:
                _add(alias)

    tokens = _tokenize(lower)
    token_nodiac = {strip_diacritics(t) for t in tokens}
    for canonical, aliases in entries:
        parts = canonical.split()
        if len(parts) == 1:
            key_n = strip_diacritics(canonical)
            if canonical in tokens or key_n in token_nodiac:
                _add(canonical)
                for alias in aliases:
                    _add(alias)

    return extra


def expand_query(query: str, *, max_variants: int = 3) -> list[str]:
    """Return original query plus heuristic variants for hybrid retrieval."""
    variants: list[str] = [query.strip()]
    seen = {query.strip().lower()}

    entries = _load_synonym_entries()
    extra_terms = _match_synonym_terms(query, entries)

    if extra_terms:
        augmented = f"{query} {' '.join(extra_terms)}"
        if augmented.lower() not in seen:
            variants.append(augmented)
            seen.add(augmented.lower())

    return variants[:max_variants]


def expand_query_metadata(query: str) -> dict[str, Any]:
    variants = expand_query(query)
    return {
        "original": query,
        "variants": variants,
        "variant_count": len(variants),
        "extra_terms": _match_synonym_terms(query, _load_synonym_entries()),
    }

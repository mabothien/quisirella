"""Semantic intent shortlist from config/intent_router.yaml."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import yaml
from langchain_chroma import Chroma
from langchain_core.documents import Document

from quisirella.retrieval.embeddings import get_embeddings, prefix_for_passage, prefix_for_query
from quisirella.retrieval.scoring import INTENT_SCORE_FLOOR, RAG_AMBIGUOUS_MARGIN, is_ambiguous_top2
from quisirella.settings import INTENT_INDEX_DIR, INTENT_ROUTER_PATH

COLLECTION_NAME = "quisirella_intents"
DEFAULT_TOP_K = 5


def load_intent_router() -> dict[str, Any]:
    with open(INTENT_ROUTER_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _intent_documents(router: dict[str, Any]) -> list[Document]:
    docs: list[Document] = []
    intents = router.get("intents") or {}
    for intent_id, cfg in intents.items():
        if intent_id == "ambiguous":
            continue
        description = (cfg.get("description") or "").strip()
        examples = cfg.get("examples") or []
        pipeline = cfg.get("pipeline") or []
        meta = {
            "intent_id": intent_id,
            "pipeline": json.dumps(pipeline, ensure_ascii=False),
            "skip_auto_refresh": str(cfg.get("skip_auto_refresh", False)).lower(),
            "description": description,
        }
        if description:
            docs.append(
                Document(
                    page_content=prefix_for_passage(f"{intent_id}: {description}"),
                    metadata={**meta, "kind": "description"},
                )
            )
        for i, example in enumerate(examples):
            text = str(example).strip()
            if not text:
                continue
            docs.append(
                Document(
                    page_content=prefix_for_passage(f"{intent_id}: {text}"),
                    metadata={**meta, "kind": "example", "example_index": i},
                )
            )
    return docs


def build_intent_index(*, reset: bool = True) -> dict[str, Any]:
    router = load_intent_router()
    docs = _intent_documents(router)
    if not docs:
        raise ValueError("intent_router.yaml has no embeddable intents")

    if reset and INTENT_INDEX_DIR.exists():
        shutil.rmtree(INTENT_INDEX_DIR)
    INTENT_INDEX_DIR.mkdir(parents=True, exist_ok=True)

    Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=str(INTENT_INDEX_DIR),
    )
    return {
        "status": "ok",
        "documents": len(docs),
        "intents": len(router.get("intents") or {}),
        "index_dir": str(INTENT_INDEX_DIR),
        "embedding_model": get_embeddings().model_name,
    }


def _load_store() -> Chroma | None:
    if not INTENT_INDEX_DIR.exists():
        return None
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(INTENT_INDEX_DIR),
    )


def _distance_to_score(distance: float) -> float:
    # Chroma cosine distance: 0 = identical, 2 = opposite (with normalized embeddings ~ [0,2])
    return max(0.0, 1.0 - (distance / 2.0))


def search_intents(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    *,
    store: Chroma | None = None,
) -> dict[str, Any]:
    store = store if store is not None else _load_store()
    if store is None:
        return {
            "status": "index_missing",
            "query": query,
            "candidates": [],
            "ambiguous": True,
            "message": "Run: python -m quisirella index-intents",
        }

    prefixed = prefix_for_query(query)
    results = store.similarity_search_with_score(prefixed, k=top_k)

    # Aggregate best score per intent_id
    by_intent: dict[str, dict[str, Any]] = {}
    for doc, distance in results:
        intent_id = doc.metadata.get("intent_id", "")
        if not intent_id:
            continue
        score = _distance_to_score(float(distance))
        prev = by_intent.get(intent_id)
        if prev is None or score > prev["score"]:
            by_intent[intent_id] = {
                "intent_id": intent_id,
                "score": round(score, 4),
                "description": doc.metadata.get("description", ""),
                "pipeline": json.loads(doc.metadata.get("pipeline", "[]")),
                "skip_auto_refresh": doc.metadata.get("skip_auto_refresh") == "true",
                "matched_text": doc.page_content.removeprefix("passage: ").strip(),
            }

    candidates = sorted(by_intent.values(), key=lambda x: x["score"], reverse=True)[:top_k]
    ambiguous = False
    if not candidates:
        ambiguous = True
    else:
        second_score = candidates[1]["score"] if len(candidates) >= 2 else None
        ambiguous = is_ambiguous_top2(
            float(candidates[0]["score"]),
            float(second_score) if second_score is not None else None,
            score_floor=INTENT_SCORE_FLOOR,
            margin=RAG_AMBIGUOUS_MARGIN,
            high_confidence=None,
        )

    return {
        "status": "ok",
        "query": query,
        "candidates": candidates,
        "ambiguous": ambiguous,
        "top_intent": candidates[0]["intent_id"] if candidates else None,
        "index_dir": str(INTENT_INDEX_DIR),
    }


def check_guards(query: str, router: dict[str, Any] | None = None) -> dict[str, Any]:
    router = router or load_intent_router()
    lower = query.lower()
    guards = router.get("guards") or {}

    for phrase in guards.get("always_block_if_contains") or []:
        if phrase.lower() in lower:
            return {"blocked": True, "reason": f"blocked_phrase:{phrase}"}

    forced: str | None = None
    for intent_id, phrases in (guards.get("force_intent_if_contains") or {}).items():
        for phrase in phrases:
            if phrase.lower() in lower:
                forced = intent_id
                break
        if forced:
            break

    skip_refresh = forced == "skip_refresh" or any(
        p.lower() in lower for p in (guards.get("force_intent_if_contains") or {}).get("skip_refresh", [])
    )

    return {"blocked": False, "forced_intent": forced, "skip_refresh": skip_refresh}


def route_intent(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    *,
    store: Chroma | None = None,
) -> dict[str, Any]:
    router = load_intent_router()
    guard = check_guards(query, router)
    if guard["blocked"]:
        return {"status": "blocked", "query": query, **guard}

    if guard.get("forced_intent") and guard["forced_intent"] != "skip_refresh":
        intent_id = guard["forced_intent"]
        cfg = (router.get("intents") or {}).get(intent_id, {})
        return {
            "status": "ok",
            "query": query,
            "source": "guard",
            "top_intent": intent_id,
            "ambiguous": False,
            "skip_refresh": guard.get("skip_refresh", False),
            "pipeline": cfg.get("pipeline", []),
            "candidates": [{"intent_id": intent_id, "score": 1.0, "source": "guard"}],
        }

    search = search_intents(query, top_k=top_k, store=store)
    if search["status"] != "ok":
        return {**search, "source": "index_missing", "skip_refresh": guard.get("skip_refresh", False)}

    result = {
        **search,
        "source": "semantic",
        "skip_refresh": guard.get("skip_refresh", False),
    }
    if guard.get("skip_refresh"):
        result["modifiers"] = ["skip_refresh"]
    return result

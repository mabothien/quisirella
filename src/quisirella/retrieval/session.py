"""Single-process retrieval session — preload models and reuse Chroma stores."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_chroma import Chroma

from quisirella.retrieval.embeddings import get_embeddings
from quisirella.retrieval.hybrid import _get_bm25_index
from quisirella.retrieval.rerank import _get_cross_encoder
from quisirella.settings import RERANKER_MODEL


@dataclass
class RetrievalSession:
    """Cached models + vector stores for batch eval (one load per process)."""

    embedding_model: str
    reranker_model: str
    knowledge_store: Chroma | None
    intent_store: Chroma | None
    bm25_chunks: int

    @classmethod
    def warmup(cls) -> RetrievalSession:
        from quisirella.retrieval.intent_index import _load_store as load_intent_store
        from quisirella.retrieval.knowledge_index import _load_store as load_knowledge_store

        emb = get_embeddings()
        _get_cross_encoder()
        bm25, records = _get_bm25_index()

        knowledge_store = load_knowledge_store()
        intent_store = load_intent_store()

        return cls(
            embedding_model=emb.model_name,
            reranker_model=RERANKER_MODEL,
            knowledge_store=knowledge_store,
            intent_store=intent_store,
            bm25_chunks=len(records),
        )

    def as_manifest(self) -> dict[str, Any]:
        return {
            "embedding_model": self.embedding_model,
            "reranker_model": self.reranker_model,
            "knowledge_index_loaded": self.knowledge_store is not None,
            "intent_index_loaded": self.intent_store is not None,
            "bm25_chunks": self.bm25_chunks,
        }


_session: RetrievalSession | None = None


def get_retrieval_session(*, refresh: bool = False) -> RetrievalSession:
    global _session
    if _session is None or refresh:
        _session = RetrievalSession.warmup()
    return _session


def warmup_retrieval_models() -> dict[str, Any]:
    """Preload embedding + reranker + Chroma stores; return manifest for eval-rag."""
    return get_retrieval_session().as_manifest()

"""Local sentence-transformers embeddings (no OpenAI API)."""

from __future__ import annotations

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from quisirella.retrieval.hf_hub import configure_hf_hub
from quisirella.settings import EMBEDDING_MODEL, HF_TOKEN

E5_MODELS = ("intfloat/multilingual-e5-small", "intfloat/multilingual-e5-base", "intfloat/e5-small")


def uses_e5_prefix(model_name: str) -> bool:
    lower = model_name.lower()
    return "e5" in lower or lower.startswith("intfloat/")


def prefix_for_query(text: str, model_name: str | None = None) -> str:
    name = model_name or EMBEDDING_MODEL
    if uses_e5_prefix(name):
        return f"query: {text}"
    return text


def prefix_for_passage(text: str, model_name: str | None = None) -> str:
    name = model_name or EMBEDDING_MODEL
    if uses_e5_prefix(name):
        return f"passage: {text}"
    return text


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    configure_hf_hub(HF_TOKEN)
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

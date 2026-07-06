"""Configure Hugging Face Hub authentication from .env."""

from __future__ import annotations

import os


def configure_hf_hub(token: str | None) -> bool:
    """Set HF hub env vars so embeddings/reranker use authenticated downloads."""
    if not token or not token.strip():
        return False
    value = token.strip()
    os.environ.setdefault("HF_TOKEN", value)
    os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", value)
    return True

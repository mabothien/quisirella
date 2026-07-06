"""Pytest fixtures — shared retrieval session for golden eval tests."""

from __future__ import annotations

import pytest

from quisirella.retrieval.session import RetrievalSession


@pytest.fixture(scope="session")
def retrieval_session() -> RetrievalSession:
    """Load embedding + reranker + Chroma stores once per pytest process."""
    return RetrievalSession.warmup()

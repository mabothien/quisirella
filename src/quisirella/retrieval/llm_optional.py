"""Optional LLM for headless query rewrite (none | ollama | anthropic)."""

from __future__ import annotations

from typing import Any

from quisirella.settings import (
    ANTHROPIC_API_KEY,
    MODEL,
    OLLAMA_BASE_URL,
    RAG_LLM_MODEL,
    RAG_LLM_PROVIDER,
)


def get_optional_llm():
    """Return a LangChain chat model or None when provider is 'none'."""
    provider = RAG_LLM_PROVIDER
    if provider in ("", "none"):
        return None

    if provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("RAG_LLM_PROVIDER=anthropic requires ANTHROPIC_API_KEY")
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=RAG_LLM_MODEL or MODEL,
            api_key=ANTHROPIC_API_KEY,
            temperature=0,
        )

    if provider == "ollama":
        try:
            from langchain_community.chat_models import ChatOllama
        except ImportError as exc:
            raise ImportError(
                "Install langchain-community for Ollama: pip install langchain-community"
            ) from exc

        return ChatOllama(
            model=RAG_LLM_MODEL or "llama3.2",
            base_url=OLLAMA_BASE_URL,
            temperature=0,
        )

    raise ValueError(f"Unknown RAG_LLM_PROVIDER: {provider}")


def rewrite_query_llm(query: str, *, reason: str = "low retrieval confidence") -> str | None:
    """Rewrite query via optional LLM; returns None if provider is none or on failure."""
    llm = get_optional_llm()
    if llm is None:
        return None

    prompt = (
        "Rewrite this Vietnamese Meta Ads / luxury jewelry store query for knowledge search. "
        "Keep intent; add domain terms if helpful (chi phí/tin nhắn, phễu, Breakdown Effect, ROAS Sheet). "
        "Return ONLY the rewritten query, no explanation.\n\n"
        f"Reason: {reason}\n"
        f"Query: {query}"
    )
    try:
        response = llm.invoke(prompt)
        text = getattr(response, "content", str(response)).strip()
        return text or None
    except Exception:
        return None


def llm_status() -> dict[str, Any]:
    return {
        "provider": RAG_LLM_PROVIDER,
        "model": RAG_LLM_MODEL or "(default)",
        "available": RAG_LLM_PROVIDER not in ("", "none"),
    }

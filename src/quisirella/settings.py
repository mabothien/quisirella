"""Central configuration loaded from .env and config/ YAML files."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
FINANCE_FETCH_DIR = DATA_DIR / "finance_fetch"
INTENT_INDEX_DIR = DATA_DIR / "intent_index"
KNOWLEDGE_INDEX_DIR = DATA_DIR / "knowledge_index"
OUTPUT_DIR = PROJECT_ROOT / "output"
CREDENTIALS_DIR = PROJECT_ROOT / "credentials"
CURSOR_RULES_DIR = PROJECT_ROOT / ".cursor" / "rules"
SKILL_DIR = PROJECT_ROOT / "src" / "quisirella" / "skill"
INTENT_ROUTER_PATH = CONFIG_DIR / "intent_router.yaml"
RAG_SYNONYMS_PATH = CONFIG_DIR / "rag_synonyms.yaml"
RAG_EVAL_PATH = CONFIG_DIR / "rag_eval.yaml"
RAG_PROMPT_TESTS_PATH = CONFIG_DIR / "rag_prompt_tests.yaml"

load_dotenv(PROJECT_ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("QUISIRELLA_MODEL", "claude-sonnet-4-6")

# Local embeddings (Phase B/C) — no OpenAI required
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
RAG_SCORE_FLOOR = float(os.getenv("RAG_SCORE_FLOOR", "0.35"))
RAG_AMBIGUOUS_MARGIN = float(os.getenv("RAG_AMBIGUOUS_MARGIN", "0.05"))
INTENT_SCORE_FLOOR = float(os.getenv("INTENT_SCORE_FLOOR", "0.3"))
RAG_HYBRID_FETCH_K = int(os.getenv("RAG_HYBRID_FETCH_K", "30"))
RAG_LLM_PROVIDER = os.getenv("RAG_LLM_PROVIDER", "none").strip().lower()
RAG_LLM_MODEL = os.getenv("RAG_LLM_MODEL", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# Hugging Face Hub — faster downloads, higher rate limits (embeddings + reranker)
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN", "")
RAG_HIGH_CONFIDENCE = float(os.getenv("RAG_HIGH_CONFIDENCE", "0.82"))

META_MCP_URL = os.getenv("META_MCP_URL", "https://mcp.facebook.com/ads")
META_APP_ID = os.getenv("META_APP_ID", "")
META_APP_SECRET = os.getenv("META_APP_SECRET", "")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE", str(CREDENTIALS_DIR / "service_account.json")
)
# Deprecated: ranges live in config/finance_sheet.yaml (kept for legacy sheets.py callers)
GOOGLE_SHEET_RANGES = [
    r.strip() for r in os.getenv("GOOGLE_SHEET_RANGES", "").split(",") if r.strip()
]


def load_store_profile() -> dict:
    with open(CONFIG_DIR / "store_profile.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_relevance_rules() -> dict:
    with open(CONFIG_DIR / "relevance_rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_campaign_strategy() -> dict:
    with open(CONFIG_DIR / "campaign_strategy.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_finance_sheet() -> dict:
    with open(CONFIG_DIR / "finance_sheet.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def configure_utf8_stdio() -> str | None:
    """Reconfigure stdout/stderr to UTF-8 (Windows defaults to cp1252).

    Returns the stdout encoding after configuration (for diagnostics).
    """
    import sys

    for stream in (sys.stdout, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    return getattr(sys.stdout, "encoding", None)


def ensure_dirs() -> None:
    from quisirella.retrieval.hf_hub import configure_hf_hub

    configure_hf_hub(HF_TOKEN)
    for d in (
        DATA_DIR,
        FINANCE_FETCH_DIR,
        INTENT_INDEX_DIR,
        KNOWLEDGE_INDEX_DIR,
        OUTPUT_DIR,
        CREDENTIALS_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)

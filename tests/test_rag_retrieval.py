"""Tests for Phase C RAG retrieval (requires built indexes)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_EVAL = PROJECT_ROOT / "config" / "rag_eval.yaml"
KNOWLEDGE_INDEX = PROJECT_ROOT / "data" / "knowledge_index"
INTENT_INDEX = PROJECT_ROOT / "data" / "intent_index"


def _indexes_built() -> bool:
    return KNOWLEDGE_INDEX.exists() and INTENT_INDEX.exists()


requires_indexes = pytest.mark.skipif(
    not _indexes_built(),
    reason="Run: python -m quisirella index-intents && python -m quisirella index-knowledge",
)


@requires_indexes
def test_route_intent_guard_save_session(retrieval_session):
    from quisirella.retrieval.intent_index import route_intent

    result = route_intent("luu phien", store=retrieval_session.intent_store)
    assert result["top_intent"] == "save_session"
    assert result.get("source") == "guard"


@requires_indexes
def test_route_intent_finance_lookup(retrieval_session):
    from quisirella.retrieval.intent_index import route_intent

    result = route_intent("loi nhuan thang 7", store=retrieval_session.intent_store)
    candidates = [c["intent_id"] for c in result.get("candidates") or []]
    assert "finance_lookup" in candidates[:3]


@requires_indexes
def test_search_knowledge_has_grade(retrieval_session):
    from quisirella.retrieval.knowledge_index import search_knowledge

    result = search_knowledge(
        "chi phi tin nhan pheu nguong",
        top_k=5,
        store=retrieval_session.knowledge_store,
    )
    assert result["status"] == "ok"
    assert result["grade"] in ("ok", "low", "missing")
    assert "retrieval_confidence" in result
    assert isinstance(result.get("chunks"), list)


@requires_indexes
def test_golden_intent_hit_rate(retrieval_session):
    from quisirella.retrieval.eval_rag import eval_intents

    report = eval_intents(top_k=3, session=retrieval_session)
    assert report["total"] > 0
    assert report["rate"] >= 0.9, json.dumps(report["results"], ensure_ascii=False, indent=2)


@requires_indexes
def test_golden_knowledge_hit_rate(retrieval_session):
    from quisirella.retrieval.eval_rag import eval_knowledge

    report = eval_knowledge(top_k=3, session=retrieval_session)
    assert report["total"] > 0
    assert report["rate"] >= 0.7, json.dumps(report["results"], ensure_ascii=False, indent=2)


def test_query_expand_synonyms():
    from quisirella.retrieval.query_expand import expand_query

    variants = expand_query("loi nhuan thang 7")
    assert len(variants) >= 2
    joined = " ".join(variants).lower()
    assert "lợi nhuận" in joined


def test_query_expand_pheu():
    from quisirella.retrieval.query_expand import expand_query

    variants = expand_query("campaign pheu")
    joined = " ".join(variants)
    assert "phễu" in joined or "funnel" in joined


def test_faithfulness_heuristic():
    from quisirella.retrieval.faithfulness import check_claim_faithfulness

    chunks = [{"content": "Chi phí tin nhắn là KPI chính cho campaign phễu DM-first"}]
    result = check_claim_faithfulness("Chi phí tin nhắn KPI phễu", chunks)
    assert result["faithful"] is True


def test_eval_config_loads():
    assert CONFIG_EVAL.exists()
    with open(CONFIG_EVAL, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert len(data.get("intent_queries") or []) >= 5
    assert len(data.get("knowledge_queries") or []) >= 3

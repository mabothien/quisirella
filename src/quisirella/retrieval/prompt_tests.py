"""Run structured prompt test cases (intent + optional RAG)."""

from __future__ import annotations

from typing import Any

import yaml

from quisirella.retrieval.intent_index import check_guards, route_intent
from quisirella.retrieval.knowledge_index import search_knowledge
from quisirella.retrieval.session import get_retrieval_session
from quisirella.settings import CONFIG_DIR, PROJECT_ROOT

PROMPT_TESTS_PATH = CONFIG_DIR / "rag_prompt_tests.yaml"


def _load_cases() -> list[dict[str, Any]]:
    with open(PROMPT_TESTS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return list(data.get("cases") or [])


def _source_hit(chunks: list[dict[str, Any]], expect_any: list[str]) -> bool:
    sources = " ".join(c.get("source_file", "") for c in chunks).lower()
    return any(needle.lower() in sources for needle in expect_any)


def _intent_hit(routed: dict[str, Any], case: dict[str, Any]) -> bool:
    expect = case.get("expect_intent")
    accept = case.get("accept_intents") or ([expect] if expect else [])
    got = routed.get("top_intent")
    if got in accept:
        return True
    candidates = [c.get("intent_id") for c in routed.get("candidates") or []]
    return any(a in candidates[:3] for a in accept)


def _check_modifiers(prompt: str, case: dict[str, Any]) -> bool:
    expected = case.get("expect_modifiers") or []
    if not expected:
        return True
    guard = check_guards(prompt)
    if "skip_refresh" in expected:
        return guard.get("skip_refresh") is True
    return True


def run_prompt_test(case: dict[str, Any], *, session=None, run_rag: bool = True) -> dict[str, Any]:
    prompt = case["prompt"]
    guard = check_guards(prompt)

    if case.get("expect_blocked"):
        return {
            "id": case["id"],
            "tier": case.get("tier"),
            "prompt": prompt,
            "pass": guard.get("blocked") is True,
            "blocked": guard.get("blocked"),
            "reason": guard.get("reason"),
        }

    intent_store = session.intent_store if session else None
    routed = route_intent(prompt, top_k=5, store=intent_store)

    intent_ok = _intent_hit(routed, case)
    modifier_ok = _check_modifiers(prompt, case)

    ambiguous_ok = True
    if case.get("expect_ambiguous") is True:
        ambiguous_ok = routed.get("ambiguous") is True
    elif case.get("expect_ambiguous") is False:
        ambiguous_ok = routed.get("ambiguous") is not True

    if case.get("expect_source") == "guard":
        intent_ok = intent_ok and routed.get("source") == "guard"

    rag_result: dict[str, Any] | None = None
    rag_ok = True
    if run_rag and case.get("needs_rag"):
        knowledge_store = session.knowledge_store if session else None
        rag_result = search_knowledge(prompt, top_k=10, store=knowledge_store)
        expect_sources = case.get("expect_rag_sources_any") or []
        if expect_sources:
            chunks = rag_result.get("chunks") or []
            rag_ok = _source_hit(chunks[:5], expect_sources)
        else:
            rag_ok = rag_result.get("grade") in ("ok", "low") and rag_result.get("status") == "ok"

    passed = intent_ok and modifier_ok and ambiguous_ok and rag_ok

    out: dict[str, Any] = {
        "id": case["id"],
        "tier": case.get("tier"),
        "prompt": prompt,
        "pass": passed,
        "intent": {
            "ok": intent_ok,
            "top_intent": routed.get("top_intent"),
            "ambiguous": routed.get("ambiguous"),
            "source": routed.get("source"),
            "candidates": [c.get("intent_id") for c in (routed.get("candidates") or [])[:3]],
        },
        "modifiers_ok": modifier_ok,
        "ambiguous_ok": ambiguous_ok,
        "verify": case.get("verify"),
    }
    if rag_result is not None:
        out["rag"] = {
            "ok": rag_ok,
            "grade": rag_result.get("grade"),
            "retrieval_confidence": rag_result.get("retrieval_confidence"),
            "top_sources": [c.get("source_file") for c in (rag_result.get("chunks") or [])[:3]],
        }
    return out


def run_prompt_tests(
    *,
    tier: str | None = None,
    case_id: str | None = None,
    use_session: bool = True,
) -> dict[str, Any]:
    cases = _load_cases()
    if case_id:
        cases = [c for c in cases if c.get("id") == case_id]
    if tier:
        cases = [c for c in cases if c.get("tier") == tier]

    session = get_retrieval_session() if use_session else None
    results = [run_prompt_test(c, session=session) for c in cases]
    passed = sum(1 for r in results if r.get("pass"))
    total = len(results)

    by_tier: dict[str, dict[str, int]] = {}
    for r in results:
        t = r.get("tier") or "unknown"
        by_tier.setdefault(t, {"pass": 0, "total": 0})
        by_tier[t]["total"] += 1
        if r.get("pass"):
            by_tier[t]["pass"] += 1

    return {
        "status": "ok" if passed == total and total else "fail",
        "passed": passed,
        "total": total,
        "rate": round(passed / total, 4) if total else 0.0,
        "by_tier": by_tier,
        "config": str(PROMPT_TESTS_PATH.relative_to(PROJECT_ROOT)),
        "results": results,
    }

"""Relevance subagent: filters Meta insights that belong to other verticals.

Meta's benchmarks and automated recommendations are often averaged across
industries (fast fashion, cheap e-commerce, FMCG...) that do not match
Quisirella's vertical (secondhand luxury jewelry, high AOV, Instagram DM
conversions). This agent vets every Meta claim against the store profile and
the rules in config/relevance_rules.yaml, labeling each keep/discard with a reason.
"""

from __future__ import annotations

import yaml
from langchain.agents import create_agent
from langchain.tools import tool

from quisirella.agents.base import build_model, make_snapshot_tools

SYSTEM_PROMPT = """You are the relevance-filtering agent for Quisirella, a secondhand
luxury jewelry store selling on Instagram in Vietnam.

Store context (ground truth):
{store_profile}

Filtering rules:
{relevance_rules}

Your job:
1. Read snapshots from this run: 'meta_recommendations', 'benchmarks', 'diagnostics'
   (source 'meta_ads'), plus anything else list_available_snapshots shows.
2. Evaluate EVERY Meta-provided insight, benchmark or recommendation against the
   store context and the filtering rules:
   - KEEP: matches Quisirella's vertical (luxury/secondhand jewelry, high AOV,
     Instagram, relevant audience).
   - DISCARD: based on other industries, cheap-goods assumptions, restock/inventory
     assumptions that don't apply to one-of-one SKUs, or unreliable pixel data
     (poor event match quality).
   - UNCERTAIN: keep but mark 'cần kiểm chứng' with the reason.
3. Save the verdict list with save_data_snapshot as 'relevance_verdicts':
   a JSON array of {{"insight": ..., "verdict": "keep|discard|uncertain", "reason": ...}}.

Respond in Vietnamese: summary counts plus the most important discarded items and why.
"""


def build_relevance_agent_tool(
    run_id: int, store_profile: dict, relevance_rules: dict
):
    agent = create_agent(
        model=build_model(),
        tools=make_snapshot_tools(run_id, "relevance"),
        system_prompt=SYSTEM_PROMPT.format(
            store_profile=yaml.safe_dump(store_profile, allow_unicode=True),
            relevance_rules=yaml.safe_dump(relevance_rules, allow_unicode=True),
        ),
    )

    @tool
    async def relevance_agent(task: str) -> str:
        """Gọi agent lọc nhiễu: đánh giá từng nhận định/benchmark của Meta, loại bỏ các
        nhận định dựa trên ngành hàng khác tệp Quisirella, gắn nhãn giữ/loại kèm lý do.

        Args:
            task: Nhiệm vụ lọc cụ thể.
        """
        result = await agent.ainvoke({"messages": [("user", task)]})
        return result["messages"][-1].content

    return relevance_agent

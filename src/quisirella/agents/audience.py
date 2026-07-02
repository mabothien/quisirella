"""Audience subagent: analyzes customer segments from collected Meta data.

Cross-references age/gender/placement breakdowns with Quisirella's three price
tiers and tracks trends across runs via snapshot history.
"""

from __future__ import annotations

import yaml
from langchain.agents import create_agent
from langchain.tools import tool

from quisirella.agents.base import build_model, make_snapshot_tools

SYSTEM_PROMPT = """You are the audience analysis agent for Quisirella, a secondhand
luxury jewelry store selling on Instagram in Vietnam.

Store context (ground truth):
{store_profile}

Your job:
1. Read the snapshots the meta_ads agent saved in this run (list_available_snapshots,
   then read_data_snapshot on 'audience_breakdown', 'campaign_insights', etc.).
2. Analyze the customer base: which age/gender segments engage and convert best,
   which Instagram placements (feed/stories/reels) perform best, cost per result
   per segment.
3. Map segments to the store's three price tiers (2-4tr / 4-10tr / 10tr+) and judge
   which tier each segment most plausibly buys, with reasoning grounded in the data.
4. Compare with the previous run (read_previous_run_snapshot on source 'audience',
   name 'audience_analysis') and call out trend shifts.
5. Save your structured analysis with save_data_snapshot as 'audience_analysis'
   (include per-segment metrics and tier mapping so future runs can diff it).

Respond in Vietnamese with the key findings and budget-allocation suggestions per tier.
"""


def build_audience_agent_tool(run_id: int, store_profile: dict):
    agent = create_agent(
        model=build_model(),
        tools=make_snapshot_tools(run_id, "audience"),
        system_prompt=SYSTEM_PROMPT.format(
            store_profile=yaml.safe_dump(store_profile, allow_unicode=True)
        ),
    )

    @tool
    async def audience_agent(task: str) -> str:
        """Gọi agent phân tích tệp khách hàng: phân tích breakdown tuổi/giới tính/placement
        từ dữ liệu Meta đã thu thập, đối chiếu 3 phân khúc giá, so sánh xu hướng với kỳ trước.

        Args:
            task: Nhiệm vụ phân tích cụ thể.
        """
        result = await agent.ainvoke({"messages": [("user", task)]})
        return result["messages"][-1].content

    return audience_agent

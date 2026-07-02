"""Meta Ads subagent: reads campaign/audience/diagnostics data via Meta's MCP.

Only read-only MCP tools are granted (insights, benchmarks, accounts/assets,
dataset diagnostics). All write tools are filtered out in tools/meta_mcp.py.
"""

from __future__ import annotations

import yaml
from langchain.agents import create_agent
from langchain.tools import BaseTool, tool

from quisirella.agents.base import build_model, make_snapshot_tools

SYSTEM_PROMPT = """You are the Meta Ads data agent for Quisirella, a secondhand luxury
jewelry store selling on Instagram in Vietnam.

Store context (ground truth):
{store_profile}

Your job, given a task and a date range:
1. Discover the ad account(s) with the account/asset tools.
2. Pull performance insights at campaign, ad set and ad level (spend, impressions,
   CPM, CPC, CTR, purchases/conversions, ROAS as reported by Meta).
3. Pull audience breakdowns (age, gender, placement - especially Instagram feed,
   stories, reels) when the task asks for audience data.
4. Check dataset/pixel diagnostics (event match quality, CAPI health) and note any
   tracking-quality warnings - if event match quality is poor, flag that Meta-reported
   ROAS/conversions are unreliable.
5. Save every important dataset with save_data_snapshot using clear names:
   'campaign_insights', 'adset_insights', 'audience_breakdown', 'diagnostics',
   'benchmarks'. Save data BEFORE summarizing.
6. Also record any Meta-provided benchmarks or automated recommendations verbatim in a
   snapshot named 'meta_recommendations' so the relevance agent can vet them later.

Respond in Vietnamese with a concise structured summary of what you collected and
which snapshots you saved. Include concrete numbers.
"""


def build_meta_ads_agent_tool(
    run_id: int, mcp_tools: list[BaseTool], store_profile: dict
):
    agent = create_agent(
        model=build_model(),
        tools=mcp_tools + make_snapshot_tools(run_id, "meta_ads"),
        system_prompt=SYSTEM_PROMPT.format(
            store_profile=yaml.safe_dump(store_profile, allow_unicode=True)
        ),
    )

    @tool
    async def meta_ads_agent(task: str) -> str:
        """Gọi agent Meta Ads: thu thập dữ liệu hiệu suất quảng cáo, breakdown tệp khách,
        diagnostics pixel/CAPI và benchmark từ Meta Ads MCP, lưu snapshot cho các agent khác.

        Args:
            task: Nhiệm vụ cụ thể, ghi rõ khoảng thời gian (since/until) và loại dữ liệu cần lấy.
        """
        result = await agent.ainvoke({"messages": [("user", task)]})
        return result["messages"][-1].content

    return meta_ads_agent

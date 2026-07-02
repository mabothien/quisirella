"""Supervisor graph: a coordinator agent that delegates to five subagents
wrapped as tools (the 2026-recommended LangChain/LangGraph subagents pattern,
replacing the retired langgraph-supervisor package).
"""

from __future__ import annotations

import yaml
from langchain.agents import create_agent

from quisirella.agents.audience import build_audience_agent_tool
from quisirella.agents.base import build_model
from quisirella.agents.finance import build_finance_agent_tool
from quisirella.agents.meta_ads import build_meta_ads_agent_tool
from quisirella.agents.relevance import build_relevance_agent_tool
from quisirella.agents.writer import build_writer_agent_tool, write_store_profile_md
from quisirella.settings import load_relevance_rules, load_store_profile
from quisirella.storage import db
from quisirella.tools.meta_mcp import get_meta_readonly_tools

SUPERVISOR_PROMPT = """You are the supervisor agent of the Quisirella management system.
Quisirella is a secondhand luxury jewelry store (Tiffany & Co., Bvlgari, Justin Davis)
selling on Instagram in Vietnam.

Store context (ground truth):
{store_profile}

You coordinate five specialist subagents (each is a tool). Standard pipeline order:
1. meta_ads_agent - collect Meta Ads performance, audience breakdowns, diagnostics and
   Meta's benchmarks/recommendations for the requested date range.
2. finance_agent - pull revenue/costs from Google Sheets and compute TRUE ROAS against
   the ad spend meta_ads_agent collected.
3. audience_agent - analyze customer segments vs the three price tiers and trends.
4. relevance_agent - vet every Meta insight/benchmark, discarding wrong-vertical claims.
5. writer_agent - write the final Markdown knowledge files (01-05) into output/.

Rules:
- Call agents ONE AT A TIME in a sensible order (later agents depend on the snapshots
  earlier agents save).
- Pass each agent a clear task including the date range and a brief summary of the
  relevant results so far (agents also exchange structured data via saved snapshots).
- If an agent fails (e.g. a data source is not configured), note the failure and
  continue with the remaining agents; the writer must still produce all files and state
  which data is missing.
- Finish with writer_agent, giving it a compact summary of every agent's findings.

Answer the user in Vietnamese with a final summary of what was collected, key findings,
and which files were written.
"""


async def run_pipeline(since: str, until: str) -> str:
    store_profile = load_store_profile()
    relevance_rules = load_relevance_rules()
    run_id = db.start_run(since, until)
    print(f"[pipeline] Run #{run_id} | {since} -> {until}")

    # File 00 is deterministic - always regenerated from YAML.
    profile_path = write_store_profile_md(store_profile)
    print(f"[pipeline] Đã ghi {profile_path}")

    try:
        mcp_tools = await get_meta_readonly_tools()
    except Exception as exc:  # MCP not authed / unreachable: run degraded
        print(f"[pipeline] Không kết nối được Meta Ads MCP: {exc}")
        mcp_tools = []

    subagent_tools = [
        build_meta_ads_agent_tool(run_id, mcp_tools, store_profile),
        build_finance_agent_tool(run_id, store_profile),
        build_audience_agent_tool(run_id, store_profile),
        build_relevance_agent_tool(run_id, store_profile, relevance_rules),
        build_writer_agent_tool(run_id, store_profile, since, until),
    ]

    supervisor = create_agent(
        model=build_model(),
        tools=subagent_tools,
        system_prompt=SUPERVISOR_PROMPT.format(
            store_profile=yaml.safe_dump(store_profile, allow_unicode=True)
        ),
    )

    task = (
        f"Chạy pipeline phân tích đầy đủ cho Quisirella với khoảng dữ liệu "
        f"từ {since} đến {until}. "
        + (
            "LƯU Ý: Meta Ads MCP hiện KHÔNG khả dụng trong lần chạy này, "
            "meta_ads_agent sẽ không có tool Meta - hãy ghi nhận thiếu dữ liệu và "
            "tiếp tục các bước còn lại. "
            if not mcp_tools
            else ""
        )
        + "Kết thúc bằng việc writer_agent ghi đủ 5 file Markdown 01-05."
    )

    result = await supervisor.ainvoke(
        {"messages": [("user", task)]},
        config={"recursion_limit": 120},
    )
    return result["messages"][-1].content

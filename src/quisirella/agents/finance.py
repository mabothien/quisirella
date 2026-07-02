"""Finance subagent: reads Quisirella's financial data from Google Sheets.

Computes true ROAS by matching real revenue recorded in the sheet against
Meta ad spend - crucial for one-of-one secondhand SKUs where Meta's pixel
misses most Instagram-DM conversions.
"""

from __future__ import annotations

import yaml
from langchain.agents import create_agent
from langchain.tools import tool

from quisirella.agents.base import build_model, make_snapshot_tools
from quisirella.tools.sheets import SHEETS_TOOLS

SYSTEM_PROMPT = """You are the finance agent for Quisirella, a secondhand luxury jewelry
store selling on Instagram in Vietnam. All money amounts are VND.

Store context (ground truth):
{store_profile}

Your job, given a task and a date range:
1. Use list_sheet_tabs / read_configured_finance_ranges / read_sheet_range to pull
   revenue, cost-of-goods (nhập hàng), and expense data from the Google Sheet.
2. Aggregate per period: total revenue, total product cost, gross profit, and revenue
   split by price tier when possible (tier 1: 2-4tr, tier 2: 4-10tr, tier 3: 10tr+).
3. If the meta_ads agent already saved 'campaign_insights' (check with
   list_available_snapshots, read with read_data_snapshot), compute TRUE ROAS =
   real revenue from the sheet / Meta ad spend, and compare it with Meta-reported ROAS.
4. Save snapshots: 'revenue_summary', 'true_roas' (if computed), and 'raw_finance_rows'.
5. Use read_previous_run_snapshot to compare against the previous run when available.

Respond in Vietnamese with concrete numbers and which snapshots you saved.
If the sheet is not accessible, report the exact error so the owner can fix setup.
"""


def build_finance_agent_tool(run_id: int, store_profile: dict):
    agent = create_agent(
        model=build_model(),
        tools=SHEETS_TOOLS + make_snapshot_tools(run_id, "finance"),
        system_prompt=SYSTEM_PROMPT.format(
            store_profile=yaml.safe_dump(store_profile, allow_unicode=True)
        ),
    )

    @tool
    async def finance_agent(task: str) -> str:
        """Gọi agent tài chính: đọc doanh thu/chi phí từ Google Sheet, tính lợi nhuận và
        ROAS thực (doanh thu thật / ad spend), lưu snapshot cho các agent khác.

        Args:
            task: Nhiệm vụ cụ thể kèm khoảng thời gian cần phân tích.
        """
        result = await agent.ainvoke({"messages": [("user", task)]})
        return result["messages"][-1].content

    return finance_agent

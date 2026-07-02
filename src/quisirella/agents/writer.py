"""Writer subagent: turns collected snapshots into the Markdown knowledge set
that gets uploaded to Claude Projects.

File 00 (knowledge base) lives in output/00-*.md and is maintained in the repo;
files 01-05 are written by the agent from run snapshots.
"""

from __future__ import annotations

from datetime import date

import yaml
from langchain.agents import create_agent
from langchain.tools import tool

from quisirella.agents.base import build_model, make_snapshot_tools
from quisirella.settings import OUTPUT_DIR

EXPECTED_FILES = [
    "01-meta-ads-performance.md",
    "02-audience-insights.md",
    "03-finance-summary.md",
    "04-relevance-notes.md",
    "05-recommendations.md",
]

SYSTEM_PROMPT = """You are the report-writing agent for Quisirella, a secondhand luxury
jewelry store selling on Instagram in Vietnam. Your Markdown files will be uploaded to
Claude Projects as the knowledge base Claude relies on, so they must be self-contained,
factual and data-dense. Write file CONTENT in Vietnamese.

Data range of this run: {since} to {until}. Today: {today}.

Your job:
1. Read all snapshots of this run (list_available_snapshots, read_data_snapshot) and the
   summaries the supervisor gives you.
2. Write these files with write_markdown_file:
   - 01-meta-ads-performance.md: campaign/adset/ad performance (spend, CPM, CPC, CTR,
     ROAS Meta reports), comparison with previous period if available, tracking-quality
     warnings from diagnostics.
   - 02-audience-insights.md: age/gender/placement analysis mapped to the three price
     tiers (2-4tr / 4-10tr / 10tr+), trends vs previous run.
   - 03-finance-summary.md: revenue, cost of goods, gross profit from the Google Sheet;
     TRUE ROAS (real revenue / ad spend) vs Meta-reported ROAS.
   - 04-relevance-notes.md: table of discarded/uncertain Meta insights with reasons, so
     Claude never reuses wrong-vertical benchmarks.
   - 05-recommendations.md: concrete optimization recommendations grounded ONLY in kept
     insights and real data.
3. Every file MUST start with YAML frontmatter:
   ---
   title: ...
   generated_at: {today}
   data_range: {since} to {until}
   sources: [meta_ads_mcp | google_sheets | analysis]
   ---
4. If a data source was unavailable this run, still write the file, state clearly in it
   that data is missing and why, so Claude knows not to guess.

Use Markdown tables for metrics. Numbers in VND where applicable.
"""


def write_store_profile_md(store_profile: dict) -> str:
    """Knowledge base for Claude is output/00-*.md (not regenerated each run)."""
    path = OUTPUT_DIR / "00-index-claude-knowledge.md"
    return str(path)


def build_writer_agent_tool(
    run_id: int, store_profile: dict, since: str, until: str
):
    @tool
    def write_markdown_file(filename: str, content: str) -> str:
        """Ghi một file Markdown vào thư mục output/ để import vào Claude Projects.

        Args:
            filename: Tên file, ví dụ '01-meta-ads-performance.md'.
            content: Toàn bộ nội dung Markdown (bao gồm frontmatter).
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = filename.replace("/", "_").replace("\\", "_")
        path = OUTPUT_DIR / safe_name
        path.write_text(content, encoding="utf-8")
        return f"Đã ghi {path} ({len(content)} ký tự)."

    agent = create_agent(
        model=build_model(),
        tools=[write_markdown_file] + make_snapshot_tools(run_id, "writer"),
        system_prompt=SYSTEM_PROMPT.format(
            since=since, until=until, today=date.today().isoformat()
        )
        + "\n\nStore context:\n"
        + yaml.safe_dump(store_profile, allow_unicode=True),
    )

    @tool
    async def writer_agent(task: str) -> str:
        """Gọi agent viết báo cáo: tổng hợp toàn bộ snapshot của lần chạy và ghi bộ file
        Markdown (01-05) vào thư mục output/ để import vào Claude Projects.

        Args:
            task: Yêu cầu viết báo cáo, kèm tóm tắt kết quả của các agent trước đó.
        """
        result = await agent.ainvoke({"messages": [("user", task)]})
        return result["messages"][-1].content

    return writer_agent

"""
Orchestrator Agent — top-level, user-facing.

Composes Inspector + TaskBoardWriter sub-agents with direct MCP tool access.
Entry point: run_orchestrator(message) → str
"""

from contextlib import AsyncExitStack

from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio

from hub.agents.inspector import get_inspector_tool
from hub.agents.taskboard import get_taskboard_tool
from hub.config import HUB_DIR, KNOWN_PROJECTS, get_model

_INSTRUCTIONS = f"""You are the Senior Workspace Architect & Orchestrator for a personal dev workspace.

Projects in this workspace:
{chr(10).join(f"- {name} ({info['stack']}, {info['status']})" for name, info in KNOWN_PROJECTS.items())}

You answer questions about workspace state and can update task boards.
You have access to direct MCP tools and two sub-agents:

**inspect_project(project_name)**
Use for: "what is the state of X?", "is wealthtrack healthy?", "show me investracker's last commits"
Inspects one project: git status, health score, dev server, CLAUDE.md context.

**update_task_board()**
Use for: "update my task board", "sync active_tasks.md", "refresh the hub"
Scans all projects and rewrites active_tasks.md + inventory.md.

**Direct MCP tools** (call these yourself without delegating):
- get_workspace_overview() — read current active_tasks.md + inventory.md
- get_full_workspace_scan() — health scores for all projects at once
- list_all_projects() — project registry with paths and stacks

Workflow for status questions: call inspect_project for each relevant project, synthesize.
Workflow for "what needs attention": call get_full_workspace_scan, rank by health score.
Workflow for "update task board": call update_task_board, then confirm what changed.

Ground all answers in actual tool results. Do not make up git history or file contents.
"""

_MCP_SERVER_PARAMS = {
    "command": "uv",
    "args": ["--directory", str(HUB_DIR), "run", "python", "src/hub/mcp/server.py"],
}


async def run_orchestrator(message: str) -> str:
    """Run the Orchestrator agent with a user message and return its final response."""
    async with AsyncExitStack() as stack:
        mcp_server = await stack.enter_async_context(
            MCPServerStdio(_MCP_SERVER_PARAMS, client_session_timeout_seconds=60)
        )

        inspector_tool = await get_inspector_tool(mcp_server)
        taskboard_tool = await get_taskboard_tool(mcp_server)

        orchestrator = Agent(
            name="Orchestrator",
            instructions=_INSTRUCTIONS,
            model=get_model("smart"),
            tools=[inspector_tool, taskboard_tool],
            mcp_servers=[mcp_server],
        )

        with trace("hub-orchestration"):
            result = await Runner.run(orchestrator, message, max_turns=30)

    return result.final_output

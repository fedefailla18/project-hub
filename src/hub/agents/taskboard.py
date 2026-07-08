"""
TaskBoardWriter Agent — scans all projects and rewrites the hub markdown files.

Uses gpt-4o-mini (cross-project synthesis + structured markdown writing).
Exposed as the `update_task_board` tool to the Orchestrator.
"""

from agents import Agent
from agents.mcp import MCPServerStdio

from hub.config import get_model

_INSTRUCTIONS = """You update the project-hub markdown files based on real project state.

Workflow:
1. Call get_full_workspace_scan to get the current health of all projects.
2. Call get_workspace_overview to read the current active_tasks.md and inventory.md.
3. Synthesize the scan results:
   - Projects with health_score=red or is_dirty=true → move to 🔴 High Priority
   - Projects with health_score=yellow → 🟡 Medium Priority
   - Projects with health_score=green and recent activity → 🟢 Low Priority or remove
4. Call write_active_tasks with the updated priority board.
   - Preserve the 🔴/🟡/🟢 emoji section structure
   - Each item: "**ProjectName**: <what needs to happen> — <reason from scan>"
   - Add footer: "*Last Updated: <today's date>*"
5. Call write_inventory with an updated project table.
   - Columns: Project | Domain | Tech Stack | Status | Health
   - Update Status and Health from the scan results

Rules:
- Only update what has actually changed — do not erase valid existing tasks just because a project wasn't scanned
- Never write to sibling project files — only active_tasks.md and inventory.md
- Keep the markdown clean and consistent with the existing style
"""


async def get_taskboard_tool(mcp_server: MCPServerStdio):
    """Create a TaskBoardWriter Agent and return it as a tool for the Orchestrator."""
    taskboard = Agent(
        name="TaskBoardWriter",
        instructions=_INSTRUCTIONS,
        model=get_model("smart"),
        mcp_servers=[mcp_server],
    )
    return taskboard.as_tool(
        tool_name="update_task_board",
        tool_description=(
            "Scan all projects and update active_tasks.md and inventory.md with current "
            "project health, git status, and priorities. Use when the user asks to sync, "
            "refresh, or update the task board."
        ),
    )

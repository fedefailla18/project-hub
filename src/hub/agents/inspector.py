"""
Inspector Agent — scoped to one project at a time.

Uses ai/gemma3 (local Docker Model Runner) for zero-cost factual extraction.
Exposed as the `inspect_project` tool to the Orchestrator.
"""

from agents import Agent
from agents.mcp import MCPServerStdio

from hub.config import KNOWN_PROJECTS, get_model

_INSTRUCTIONS = f"""You inspect a single software project and report its current state.

Available projects: {", ".join(KNOWN_PROJECTS.keys())}

Workflow for each inspection request:
1. Call get_project_git_status to get branch, last commit, and uncommitted changes.
2. Call read_project_context to read the project's CLAUDE.md or GEMINI.md.
3. Call get_project_health to get a health score (green/yellow/red).
4. Call check_local_service to see if the dev server is running (if applicable).

Return a concise markdown summary with these sections:
- **Project**: name and stack
- **Health**: score + one-line reason
- **Last commit**: hash, message, how many days ago
- **Dev server**: running/not running/N/A
- **Uncommitted changes**: list or "none"
- **Key context**: 2-3 bullet points from CLAUDE.md/GEMINI.md (architecture, current focus)

Be factual and brief. Do not invent information — only report what the tools return.
"""


async def get_inspector_tool(mcp_server: MCPServerStdio):
    """Create an Inspector Agent and return it as a tool for the Orchestrator."""
    inspector = Agent(
        name="Inspector",
        instructions=_INSTRUCTIONS,
        model=get_model("fast"),
        mcp_servers=[mcp_server],
    )
    return inspector.as_tool(
        tool_name="inspect_project",
        tool_description=(
            "Inspect a specific project and return its current state: git status, "
            "health score, dev server status, and key context from its CLAUDE.md. "
            "Input: the project name (e.g. 'wealthtrack', 'investracker')."
        ),
    )

"""
FastMCP server — project_hub_server

Exposes 10 tools and 3 resources for inspecting the /devs/projects workspace.
Write tools only touch files inside project-hub/ — never sibling projects.

Run directly for debugging:
    uv run python src/hub/mcp/server.py
"""

import asyncio
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

from hub.config import HUB_DIR, KNOWN_PROJECTS, WORKSPACE_ROOT

mcp = FastMCP("project_hub_server")


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _project_path(project: str) -> Path:
    if project not in KNOWN_PROJECTS:
        raise ValueError(f"Unknown project '{project}'. Known: {list(KNOWN_PROJECTS)}")
    return WORKSPACE_ROOT / project


async def _run_git(project_path: Path, *args: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "git", "-C", str(project_path), *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()


def _compute_health(
    last_commit_age_days: int,
    is_dirty: bool,
    has_doc: bool,
) -> tuple[str, str]:
    """Returns (health_score, summary)."""
    if last_commit_age_days > 90 or (is_dirty and last_commit_age_days > 30):
        score = "red"
        summary = f"Stale ({last_commit_age_days}d since last commit)"
    elif last_commit_age_days > 30 or is_dirty or not has_doc:
        score = "yellow"
        reasons = []
        if last_commit_age_days > 30:
            reasons.append(f"{last_commit_age_days}d since last commit")
        if is_dirty:
            reasons.append("uncommitted changes")
        if not has_doc:
            reasons.append("no CLAUDE.md or GEMINI.md")
        summary = "; ".join(reasons)
    else:
        score = "green"
        summary = f"Healthy ({last_commit_age_days}d since last commit)"
    return score, summary


# ─── Read tools ──────────────────────────────────────────────────────────────


@mcp.tool()
async def list_all_projects() -> list[dict]:
    """List all known projects in the workspace with stack, status, and directory path."""
    return [
        {
            "name": name,
            "path": str(WORKSPACE_ROOT / name),
            **info,
        }
        for name, info in KNOWN_PROJECTS.items()
    ]


@mcp.tool()
async def get_workspace_overview() -> str:
    """Read current active_tasks.md and inventory.md from project-hub.
    Call this first to understand global state before any analysis."""
    tasks_path = HUB_DIR / "active_tasks.md"
    inventory_path = HUB_DIR / "inventory.md"

    parts = []
    if tasks_path.exists():
        parts.append(f"## active_tasks.md\n\n{tasks_path.read_text()}")
    if inventory_path.exists():
        parts.append(f"## inventory.md\n\n{inventory_path.read_text()}")

    return "\n\n---\n\n".join(parts) if parts else "No hub files found."


@mcp.tool()
async def get_project_git_status(project: str) -> dict:
    """Get git status, recent commits, and branch info for a specific project.

    Args:
        project: Project name (e.g. 'wealthtrack', 'investracker')

    Returns dict with branch, last commit info, uncommitted files, and dirty flag.
    """
    path = _project_path(project)

    if not (path / ".git").exists():
        return {
            "project": project,
            "error": "Not a git repository",
            "branch": None,
            "last_commit_hash": None,
            "last_commit_message": None,
            "last_commit_date": None,
            "last_commit_age_days": None,
            "uncommitted_files": [],
            "is_dirty": False,
        }

    branch, log_line, status_out = await asyncio.gather(
        _run_git(path, "rev-parse", "--abbrev-ref", "HEAD"),
        _run_git(path, "log", "--oneline", "--format=%H|%s|%ci", "-1"),
        _run_git(path, "status", "--short"),
    )

    commit_hash = commit_msg = commit_date = ""
    age_days = 0
    if log_line:
        parts = log_line.split("|", 2)
        commit_hash = parts[0] if len(parts) > 0 else ""
        commit_msg = parts[1] if len(parts) > 1 else ""
        commit_date = parts[2].strip() if len(parts) > 2 else ""
        if commit_date:
            try:
                dt = datetime.fromisoformat(commit_date)
                age_days = (datetime.now(tz=timezone.utc) - dt.astimezone(timezone.utc)).days
            except ValueError:
                age_days = 0

    uncommitted = [line.strip() for line in status_out.splitlines() if line.strip()]

    return {
        "project": project,
        "branch": branch,
        "last_commit_hash": commit_hash[:8] if commit_hash else "",
        "last_commit_message": commit_msg,
        "last_commit_date": commit_date,
        "last_commit_age_days": age_days,
        "uncommitted_files": uncommitted,
        "is_dirty": bool(uncommitted),
    }


@mcp.tool()
async def read_project_context(project: str) -> str:
    """Read CLAUDE.md (preferred) or GEMINI.md from a project directory.

    Args:
        project: Project name

    Returns file content, truncated to 3000 characters.
    """
    path = _project_path(project)
    for filename in ("CLAUDE.md", "GEMINI.md"):
        doc = path / filename
        if doc.exists():
            content = doc.read_text()
            if len(content) > 3000:
                content = content[:3000] + "\n\n[...truncated]"
            return f"# {filename} — {project}\n\n{content}"
    return f"No CLAUDE.md or GEMINI.md found in {project}/"


@mcp.tool()
async def read_project_doc(project: str, filename: str) -> str:
    """Read a specific markdown file from a project directory.

    Args:
        project: Project name
        filename: Markdown filename (e.g. 'ROADMAP.md', 'NEXT_STEPS.md')

    Only .md files are readable. Path traversal is blocked.
    """
    if not filename.endswith(".md") or "/" in filename or "\\" in filename:
        raise ValueError("Only .md files in the project root are readable.")
    path = _project_path(project) / filename
    if not path.exists():
        return f"{filename} not found in {project}/"
    content = path.read_text()
    if len(content) > 5000:
        content = content[:5000] + "\n\n[...truncated]"
    return content


@mcp.tool()
async def get_project_health(project: str) -> dict:
    """Compute a health summary for a project.

    Returns health_score (green/yellow/red), last commit age, doc presence, and a summary string.
    """
    path = _project_path(project)
    info = KNOWN_PROJECTS[project]

    git_data = await get_project_git_status(project)
    age_days = git_data.get("last_commit_age_days") or 0
    is_dirty = git_data.get("is_dirty", False)
    has_claude = (path / "CLAUDE.md").exists()
    has_gemini = (path / "GEMINI.md").exists()
    has_roadmap = (path / "ROADMAP.md").exists()
    has_doc = has_claude or has_gemini

    score, summary = _compute_health(age_days, is_dirty, has_doc)

    return {
        "project": project,
        "stack": info["stack"],
        "status": info["status"],
        "health_score": score,
        "health_summary": summary,
        "last_commit_age_days": age_days,
        "last_commit_message": git_data.get("last_commit_message", ""),
        "branch": git_data.get("branch", ""),
        "is_dirty": is_dirty,
        "uncommitted_files": git_data.get("uncommitted_files", []),
        "has_claude_md": has_claude,
        "has_gemini_md": has_gemini,
        "has_roadmap": has_roadmap,
    }


@mcp.tool()
async def check_local_service(project: str) -> dict:
    """Check if a project's local dev server is running by probing its port.

    Args:
        project: Project name

    Returns is_running, port, and HTTP status code (or None if no port defined).
    """
    info = KNOWN_PROJECTS.get(project, {})
    port = info.get("port")

    if port is None:
        return {"project": project, "port": None, "is_running": None, "note": "No dev port defined"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://localhost:{port}/", timeout=2.0)
            return {"project": project, "port": port, "is_running": True, "http_status": resp.status_code}
    except Exception:
        return {"project": project, "port": port, "is_running": False, "http_status": None}


@mcp.tool()
async def get_full_workspace_scan() -> list[dict]:
    """Scan ALL projects and return a health summary for each.

    Use this for 'what needs attention today?' queries.
    Equivalent to calling get_project_health for every known project.
    """
    results = await asyncio.gather(
        *[get_project_health(name) for name in KNOWN_PROJECTS],
        return_exceptions=True,
    )
    return [
        r if not isinstance(r, Exception) else {"project": "unknown", "error": str(r)}
        for r in results
    ]


# ─── Write tools (hub only) ───────────────────────────────────────────────────


@mcp.tool()
async def write_active_tasks(content: str) -> str:
    """Overwrite active_tasks.md with new content.

    Args:
        content: Full markdown content. Must be non-empty and contain priority sections.

    CONSTRAINT: Only writes to project-hub/active_tasks.md — never to sibling projects.
    """
    if not content.strip():
        raise ValueError("Content must be non-empty.")
    if "Priority" not in content:
        raise ValueError("Content must contain at least one Priority section.")

    target = HUB_DIR / "active_tasks.md"
    target.write_text(content)
    return f"Written: {len(content.encode())} bytes to active_tasks.md"


@mcp.tool()
async def write_inventory(content: str) -> str:
    """Overwrite inventory.md with an updated project table.

    Args:
        content: Full markdown content. Must contain the header row.

    CONSTRAINT: Only writes to project-hub/inventory.md — never to sibling projects.
    """
    if not content.strip():
        raise ValueError("Content must be non-empty.")
    if "Project" not in content:
        raise ValueError("Content must contain an inventory table with a 'Project' column header.")

    target = HUB_DIR / "inventory.md"
    target.write_text(content)
    return f"Written: {len(content.encode())} bytes to inventory.md"


# ─── Resources ────────────────────────────────────────────────────────────────


@mcp.resource("hub://active_tasks")
async def active_tasks_resource() -> str:
    """Current active_tasks.md content."""
    path = HUB_DIR / "active_tasks.md"
    return path.read_text() if path.exists() else "active_tasks.md not found."


@mcp.resource("hub://inventory")
async def inventory_resource() -> str:
    """Current inventory.md content."""
    path = HUB_DIR / "inventory.md"
    return path.read_text() if path.exists() else "inventory.md not found."


@mcp.resource("hub://project/{name}")
async def project_context_resource(name: str) -> str:
    """CLAUDE.md or GEMINI.md for the named project."""
    return await read_project_context(name)


if __name__ == "__main__":
    mcp.run(transport="stdio")

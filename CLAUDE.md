# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`project-hub` is the active AI orchestration service for the `/devs/projects/` workspace. It exposes a FastMCP server with tools to inspect sibling projects, and runs a 3-agent Orchestrator (Inspector + TaskBoardWriter + Orchestrator) that answers questions about workspace state and auto-updates `active_tasks.md` and `inventory.md`.

**Read `STATUS.md` before doing any work** — it tells you what is implemented, what is in progress, and what comes next. Read `ROADMAP.md` for the strategic context.

## Commands

```bash
# Install dependencies (first time or after pyproject.toml changes)
uv sync

# Run the CLI
uv run hub scan                        # Full workspace health report
uv run hub ask "state of wealthtrack?" # Free-form question
uv run hub update                      # Auto-rewrite active_tasks.md + inventory.md
uv run hub ui                          # Launch Gradio UI at http://localhost:7860

# Start the MCP server directly (for debugging or external MCP clients)
uv run python src/hub/mcp/server.py

# Run tests
uv run python -m pytest

# Linting
uv run ruff check src/
uv run ruff format src/
```

## Architecture

```
src/hub/
  config.py        WORKSPACE_ROOT, KNOWN_PROJECTS, Docker Model Runner detection, get_model()
  models.py        ProjectStatus, WorkspaceState Pydantic models
  mcp/
    server.py      FastMCP "project_hub_server" — 10 tools + 3 resources
  agents/
    inspector.py   Inspector Agent (ai/gemma3 local) → exposed as_tool
    taskboard.py   TaskBoardWriter Agent (gpt-4o-mini) → exposed as_tool
    orchestrator.py Top-level Orchestrator + run_orchestrator(message) entry fn
  cli.py           click CLI: ask / scan / update / ui
  ui/
    app.py         Gradio ChatInterface
```

**Data flow**: user invokes CLI or UI → `run_orchestrator()` → Orchestrator Agent calls MCP tools or delegates to Inspector/TaskBoardWriter sub-agents → FastMCP server runs git/file inspection tools → response returned.

**LLM tiers**:
- `get_model("fast")` → `ai/gemma3` via Docker Model Runner (local, zero cost). Falls back to `gpt-4o-mini` if Docker Model Runner is unreachable.
- `get_model("smart")` → `gpt-4o-mini` (always, for cross-project synthesis and markdown writing).

**Hub & Spoke constraint**: The MCP server's write tools (`write_active_tasks`, `write_inventory`) only write to files inside `project-hub/`. Agents never modify sibling project directories.

## Mandatory Documentation Rule

**After any significant change — code, configuration, or architecture — update `STATUS.md`.**

- Move items from `📋 Not Started` → `🔄 In Progress` → `✅ Done`
- Add an entry to the Architecture Decisions Log if a design choice was made
- Update the "Last updated" line with today's date and your name/agent

This rule exists so any future contributor (human or AI) can read `STATUS.md` and know exactly where the project stands without having to read all the code. Skipping this update is the same as leaving the project in an undocumented state.

## Git Convention

Commit messages in this repo use the `meta:` prefix:
```
meta: add MCP server with project inspection tools
meta: implement Inspector and TaskBoardWriter agents
meta: update STATUS.md — Phase 1 complete
```

## Environment Variables

Copy `.env.example` to `.env` (never commit `.env`):

```bash
OPENAI_API_KEY=sk-...          # Required for gpt-4o-mini (smart tier)
HUB_SMART_MODEL=gpt-4o-mini   # Optional override for the smart-tier model
```

Docker Model Runner requires no API key — it uses `api_key="docker"` internally.

# Implementation Status

_Last updated: 2026-07-08 by Claude Code_

---

## Phase 1 — Core Service

### ✅ Done

- `CLAUDE.md` — Claude Code guidance, commands, architecture overview, mandatory STATUS.md rule
- `ROADMAP.md` — Strategic phases (Phase 1 → 2 → 3) and non-goals
- `STATUS.md` — This file; living implementation tracker
- `CONTRIBUTING.md` — Updated with §5 Documentation Contract
- `pyproject.toml` — uv package manifest, `hub` CLI script entry point, dev dependencies
- `.python-version` — Python 3.12
- `.env.example` — Template for OPENAI_API_KEY and HUB_SMART_MODEL
- `.gitignore` — Rewrote malformed single-line file; whitelist now correctly tracks `src/`, `pyproject.toml`, `uv.lock`, documentation files, and blocks `.env`, `.venv/`, `__pycache__/`
- `src/hub/config.py` — `WORKSPACE_ROOT`, `KNOWN_PROJECTS` (7 projects), `init_model_clients()`, `get_model("fast"|"smart")` with Docker Model Runner auto-detection and graceful fallback
- `src/hub/models.py` — `ProjectStatus`, `WorkspaceState` Pydantic models
- `src/hub/mcp/server.py` — `FastMCP("project_hub_server")` with 10 tools + 3 resources:
  - Read tools: `list_all_projects`, `get_workspace_overview`, `get_project_git_status`, `read_project_context`, `read_project_doc`, `get_project_health`, `check_local_service`, `get_full_workspace_scan`
  - Write tools (hub-only): `write_active_tasks`, `write_inventory`
  - Resources: `hub://active_tasks`, `hub://inventory`, `hub://project/{name}`
- `src/hub/agents/inspector.py` — Inspector Agent (`ai/gemma3` local), exposed as `inspect_project` tool
- `src/hub/agents/taskboard.py` — TaskBoardWriter Agent (`gpt-4o-mini`), exposed as `update_task_board` tool
- `src/hub/agents/orchestrator.py` — Orchestrator Agent + `run_orchestrator(message)` entry function
- `src/hub/cli.py` — `hub ask`, `hub scan`, `hub update`, `hub ui` commands (click + rich)
- `src/hub/ui/app.py` — Gradio `ChatInterface` with example prompts
- **End-to-end verified**: `uv sync` installs cleanly; `hub --help` resolves; full workspace scan returns correct health scores for all 7 projects

### 🔄 In Progress

_Nothing currently in progress._

### 📋 Not Started

- Create a `.env` file from `.env.example` and add `OPENAI_API_KEY` (user action required)
- Run a live end-to-end test with the full agent stack: `uv run hub scan` (requires OPENAI_API_KEY)
- Commit Phase 1 to git with `meta:` prefix

---

## Phase 2 — Persistence & Scheduling

### 📋 Planned

- `src/hub/database.py` — SQLite scan history + run logs (pattern from `agents/6_mcp/database.py`)
- `src/hub/tracers.py` — `LogTracer` writing agent traces to SQLite (pattern from `agents/6_mcp/tracers.py`)
- `src/hub/scheduler.py` — Background auto-scan loop (`hub start`)
- Per-agent libSQL memory via `mcp-memory-libsql`
- Gradio auto-refresh panel (`gr.Timer`)
- `hub history` CLI command

---

## Phase 3 — Intelligence & Alerts

### 📋 Planned

- Push notifications on health-score drop to red
- Cross-project reuse suggestions
- Health trend charts
- External webhook integration (Vercel deploys)
- `hub doctor` command

---

## Architecture Decisions Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-07-08 | Python over TypeScript/Kotlin | Direct reuse of `agents/6_mcp/` patterns (FastMCP, OpenAI Agents SDK); same uv toolchain |
| 2026-07-08 | OpenAI Agents SDK over LangGraph | Orchestration-with-delegation pattern (not a cyclic eval loop); `agent.as_tool()` is the right primitive |
| 2026-07-08 | `ai/gemma3` for Inspector tier | Local Docker Model Runner = zero API cost for factual git/file extraction; 3.88B is sufficient |
| 2026-07-08 | `gpt-4o-mini` for Orchestrator + TaskBoardWriter | Cross-project synthesis and structured markdown writing need stronger reasoning |
| 2026-07-08 | Single shared MCP server (not per-agent) | All three agents share one `FastMCP` instance via `AsyncExitStack`; FastMCP handles concurrent tool calls |
| 2026-07-08 | Documentation files created before code | Any contributor entering the project must see current state immediately; code without docs is a liability |
| 2026-07-08 | `asyncio.create_subprocess_exec` for git calls | Async-safe inside FastMCP's async context; avoids blocking the event loop during workspace scans |
| 2026-07-08 | Write tools validate content before writing | Prevents agents from accidentally overwriting files with empty or malformed content |

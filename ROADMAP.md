# Roadmap

Strategic direction for `project-hub` as the active AI orchestration layer of the `/devs/projects/` workspace.

## Vision

Any agent or human entering the workspace should be able to ask one service: *"What is the state of the ecosystem?"* and get a grounded, real-time answer based on actual git history, file presence, and running services — not stale markdown.

The hub evolves from a passive documentation store into a lightweight always-available orchestrator that:
1. Knows the real state of every project (not just what was last written in `active_tasks.md`)
2. Can delegate inspection tasks to a local LLM (zero cost, no API call)
3. Can rewrite its own task board based on what it actually finds
4. Eventually runs on a schedule and pushes alerts when something needs attention

---

## Phase 1 — Core Service (current)

**Goal**: Installable Python service. Run `hub scan` and get a real workspace health report.

| Component | Description |
|-----------|-------------|
| FastMCP server | 10 tools (git status, health, doc reading, port probe) + 3 resources |
| Inspector Agent | `ai/gemma3` local LLM — inspects one project at a time, zero API cost |
| TaskBoardWriter Agent | `gpt-4o-mini` — synthesizes findings into updated markdown |
| Orchestrator Agent | `gpt-4o-mini` — user-facing, routes between sub-agents |
| CLI | `hub scan`, `hub ask`, `hub update`, `hub ui` |
| Gradio UI | Chat interface at `localhost:7860` |
| Docker Model Runner | Local LLM via `http://localhost:12434` — falls back to `gpt-4o-mini` gracefully |

**Status**: See `STATUS.md`.

---

## Phase 2 — Persistence & Scheduling (next)

**Goal**: The hub remembers what it has seen and can run without being invoked.

| Component | Description |
|-----------|-------------|
| `src/hub/database.py` | SQLite: scan history table, run logs (pattern from `agents/6_mcp/database.py`) |
| `src/hub/tracers.py` | `LogTracer` writing agent traces to SQLite (pattern from `agents/6_mcp/tracers.py`) |
| `src/hub/scheduler.py` | Background loop: auto-scan all projects every N hours (`hub start`) |
| Per-agent libSQL memory | `mcp-memory-libsql` MCP server for persistent knowledge graph per agent |
| Gradio auto-refresh | `gr.Timer` status panel that refreshes every 5 minutes |
| `hub history` CLI command | Show last N scan results from SQLite |

---

## Phase 3 — Intelligence & Alerts (aspirational)

**Goal**: The hub proactively identifies cross-project opportunities and problems.

| Component | Description |
|-----------|-------------|
| Push notifications | Pushover/webhook alert when a project's health drops to red |
| Cross-project suggestions | "wealthtrack and healthVault both need Google Sheets auth — share the lib?" |
| Health trend charts | Gradio `gr.Plot` — commit frequency, health score over time |
| External webhooks | Vercel deploy hook → auto-update wealthtrack status on deploy |
| `hub doctor` command | Runs all health checks and produces a prioritized fix list |

---

## Non-Goals

- The hub **does not modify code in sibling projects**. It reads, reports, and updates its own markdown files only.
- The hub is **not a CI system**. It does not run tests or builds — it reads their results.
- The hub is **not a secret manager**. `.env` stays local and untracked.

# Contributing to the Project Hub

Welcome to the command center. This hub is designed to be maintained by both humans and AI agents to ensure total visibility across the workspace.

## Architectures & Rules

### 1. The Hub & Spoke Model
- **The Hub:** Contains metadata, global state, and orchestration.
- **The Spokes:** Individual project directories (e.g., `wealthtrack/`, `healthVault/`). Each project MUST remain independent and functional without the hub.

### 2. Updating the Inventory
Whenever you create a new project or change a project's core tech stack:
1. Update `project-hub/inventory.md`.
2. Ensure the project has its own local `GEMINI.md` defining its specialized agents.

### 3. Agent Personas
- **The Orchestrator (Hub Agent):** Always operates from the `project-hub/` directory. It has the authority to read all sibling directories but only writes to the hub.
- **Project Agents:** Local to their folders. They follow the hub's strategic direction but handle implementation details.

### 4. Git Hygiene
- Never track sibling project files in the Hub repository.
- Ensure the `.gitignore` in this directory remains protective.
- Commit messages in the Hub should reflect "Orchestration" changes (e.g., `meta: update healthVault roadmap`).

## Onboarding a New Project
To add a project to the hub:
1. Create the project folder at the workspace root.
2. Initialize its local Git repo.
3. Add a `GEMINI.md` to the project folder.
4. Add an entry to `project-hub/inventory.md`.
5. Add the project to `KNOWN_PROJECTS` in `src/hub/config.py` (name, port, stack).
6. (Optional) Create a symbolic link in the Hub if frequent context switching is needed.

## §5 Documentation Contract

**Every change to code, configuration, or architecture must include a corresponding update to `STATUS.md`.**

Specifically:
- Move items from `📋 Not Started` → `🔄 In Progress` → `✅ Done` as work progresses
- Add an entry to the **Architecture Decisions Log** when a design choice is made — record the decision and the reason so it is never relitigated
- Update the "Last updated" line with today's date and your name or agent identifier

**This applies to both humans and AI agents.** AI agents (Claude Code, Gemini, etc.) operating in this repo have this rule in their `CLAUDE.md` / `GEMINI.md` and are expected to follow it automatically.

A commit that changes code but not `STATUS.md` is incomplete. Self-correct before merging.

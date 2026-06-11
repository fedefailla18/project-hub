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
4. Add a entry to `project-hub/inventory.md`.
5. (Optional) Create a symbolic link in the Hub if frequent context switching is needed.

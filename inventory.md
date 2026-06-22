# Global Project Inventory

This document is the source of truth for all projects in the `/devs/projects/` workspace.

| Project | Domain | Tech Stack | Status | Repository | Primary Agents |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wealthtrack/` | Finance | Next.js 16, pnpm, Docker, Prisma, Google Sheets | **Active** | `https://github.com/fedefailla18/wealthtrack.git` | Architect |
| `healthVault/` | Health | Markdown, CSV, Python (Planned) | **In Dev** | - | Librarian, Architect |
| `cv-generator/` | Career | Vite, React, TS, Tailwind | **Stable** | - | - |
| `file-importer/` | Finance | Java 11, Spring Boot, PostgreSQL, Docker | **Stable** | `git@github.com:fedefailla18/file-importer.git` | - |
| `importer-porfolio/` | Finance | React, Redux, MUI, pnpm, Docker | **Stable** | `git@github.com:fedefailla18/importer-porfolio.git` | - |
| `agents/` | AI Education | Python, CrewAI, AutoGen, LangGraph | **Research** | - | - |
| `java-servlets/` | Education | Java | **Legacy** | - | - |
| `project-hub/` | Orchestration | Bash, Docker Compose | **Active** | `git@github.com:fedefailla18/project-hub.git` | Orchestrator |

## Project Deep Dives

### WealthTrack (`wealthtrack/`)
- **Focus:** Consolidated net worth & AI wealth advisor.
- **Recent Change:** Migrated to **pnpm**, implemented production-ready **Docker** multi-stage build.

### File Importer (`file-importer/`)
- **Focus:** Crypto transaction history ingestion and P&L calculation.
- **Recent Change:** Optimized **Docker** build with Gradle-in-container strategy.

### Importer Portfolio (`importer-porfolio/`)
- **Focus:** Frontend for the crypto tracking system.
- **Recent Change:** Migrated to **pnpm** and added **Docker** Nginx runner.

---
*Last Updated: June 9, 2026*

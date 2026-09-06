# Global Project Inventory

This document is the source of truth for all projects in the `/devs/projects/` workspace.

| Project | Domain | Tech Stack | Status | Health | Repository |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `project-hub` | AI / Tooling | Python 3.12, FastMCP, Gradio, Docker | **Active** | 🟢 Green | `git@github.com:fedefailla18/project-hub.git` |
| `wealthtrack` | Finance | Next.js 16, React 19, Tailwind 4, Prisma, pnpm, Docker | **Active** | 🟢 Green | `https://github.com/fedefailla18/wealthtrack.git` |
| `importer-porfolio` | Finance | React 18, Redux Toolkit, MUI 5, pnpm, Docker | **Active** | 🟢 Green | `git@github.com:fedefailla18/importer-porfolio.git` |
| `cv-generator` | Career / Calibration | React 18, Vite, TS, Tailwind CSS, pnpm | **Active** | 🟢 Green | `git@github.com:fedefailla18/cv-gen.git` |
| `healthVault` | Health | Markdown, CSV, Python (planned) | **Active** | 🟢 Green | - |
| `investracker` | Finance | Java 11, Spring Boot 2.7, PostgreSQL, Docker | **Stable** | 🟡 Yellow | `git@github.com:fedefailla18/file-importer.git` |
| `agents` | AI Education | Python 3.12, CrewAI, AutoGen, LangGraph | **Research** | 🟡 Stale (Behind Remote) | - |
| `java-servlets` | Legacy | Java (legacy) | **Legacy** | 🟢 Green | - |

## Project Notes

### WealthTrack (`wealthtrack/`)
- Consolidated net worth & AI wealth advisor. Deployed on Vercel (Node 22).
- Migrated to **pnpm** + production-ready **Docker** multi-stage build.

### File Importer / Investracker (`investracker/`)
- Crypto transaction history ingestion and P&L calculation.
- Optimized **Docker** build with Gradle-in-container strategy.
- Merge conflict pending on `integration/new-portfolio-syncing-app`.

### Importer Portfolio (`importer-porfolio/`)
- Frontend for the crypto tracking system.
- Migrated to **pnpm** + **Docker** Nginx runner.

### CV Generator (`cv-generator/`)
- Dual-purpose: interactive CV builder + interview management/calibration hub.
- Migrated to **pnpm**. Now has `CLAUDE.md` at parity with `GEMINI.md`; both AI skills (`senior-interviewer`, `master-fe-requirement-cv-template-translator`) mirrored under `.claude/skills/` and `.gemini/skills/`.
- New **Engineering (Senior)** CV theme (reference implementation for future theme refactors); legacy themes (Modern/Minimal/Compact/Two-Column) still pending migration onto shared components.

---
*Last Updated: 2026-09-06*

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

## Last Update (per project)

One row per project, showing only the **most recent** iteration — overwrite the row (don't append) each time you finish work on a project, so returning after a gap tells you where things stand without re-reading the whole project. For full history, see the `✅ Completed` log in `active_tasks.md` instead.

| Project | Date | What was done |
| :--- | :--- | :--- |
| `cv-generator` | 2026-09-06 | Migrated to pnpm; added `CLAUDE.md` + mirrored the `senior-interviewer` and new `master-fe-requirement-cv-template-translator` skills under `.claude/skills/`; added the **Engineering (Senior)** CV theme. Fixed a critical bug where 26 stale compiled `.js` files under `src/` were silently shadowing their `.tsx`/`.ts` sources (set `tsconfig.json` `noEmit: true` to prevent recurrence). Fixed a render crash on flat-array `technologies` and added a `domains` field. Brought README/GEMINI/CLAUDE/NEXT_STEPS docs to parity. Deleted stale local branch `fix/error-handling`. |
| `wealthtrack` | 2026-09-06 | Fixed "Sync Data" only refreshing the Dashboard — added `revalidatePath()` for every sheet-data route (kept the 24h passive cache TTL, per user's call). Fixed dates from the Apps Script snapshot automation rendering as raw serial numbers on `/balance` and Registro_Saldos-derived screens — added `formatDateDisplay()`. Mirrored the Google Apps Script locally (`apps-script/`). All 102 tests + build passing. |
| `importer-porfolio` | 2026-08-25 | Fixed `App.test.tsx` assertion; merged exchange sync UI branch into `main`; migrated to pnpm + Docker Nginx runner. |
| `project-hub` | 2026-08-25 | Model tier logic updated to zero-cost local runner (`ai/gemma3`); `feature/create-agents` merged into `main`; Docker orchestration (`docker-compose.yml`) added. |
| `healthVault` | 2026-08-25 | Committed Phase 2 Google Sheets integration plan (`PHASE2_PLAN.md`) on `main`. |
| `investracker` | — | Not yet tracked here. Known open item: merge conflict on `integration/new-portfolio-syncing-app` against `main` (see `active_tasks.md`). |
| `agents` | — | Not yet tracked here. Known open item: `main` is 33 commits behind origin. |
| `java-servlets` | — | Not yet tracked here. |

## Project Notes

### WealthTrack (`wealthtrack/`)
- Consolidated net worth & AI wealth advisor. Deployed on Vercel (Node 22).
- Migrated to **pnpm** + production-ready **Docker** multi-stage build.
- Google Sheets automation (`Registro_Saldos`/`Balance` rollforward) lives in a Google Apps Script, mirrored locally at `apps-script/wealthtrack-core.gs.js`.
- "Sync Data" button forces a full refresh across every sheet-reading route (`SHEET_DATA_ROUTES` in `lib/actions.ts`); passive cache TTL stays 24h otherwise.

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

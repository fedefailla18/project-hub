# Global Project Inventory

This document is the source of truth for all projects in the `/devs/projects/` workspace.

| Project | Domain | Tech Stack | Status | Health | Repository |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `project-hub` | AI / Tooling | Python 3.12, FastMCP, Gradio, Docker | **Active** | 🟢 Green | `git@github.com:fedefailla18/project-hub.git` |
| `wealthtrack` | Finance | Next.js 16, React 19, Tailwind 4, Prisma, pnpm, Docker | **Active** | 🟢 Green | `https://github.com/fedefailla18/wealthtrack.git` |
| `importer-porfolio` | Finance | React 18, Redux Toolkit, MUI 5, pnpm, Docker | **Active** | 🟢 Green | `git@github.com:fedefailla18/importer-porfolio.git` |
| `cv-generator` | Career / Calibration | React 18, Vite, TS, Tailwind CSS, pnpm | **Active** | 🟢 Green | `git@github.com:fedefailla18/cv-gen.git` |
| `healthVault` | Health | Markdown, CSV, Python (planned) | **Active** | 🟢 Green | - |
| `investracker` | Finance | Java 11, Spring Boot 2.7, PostgreSQL, Redis, Docker | **Stable** | 🟡 Yellow | `git@github.com:fedefailla18/investracker.git` (renamed from `file-importer` 2026-09-12) |
| `agents` | AI Education | Python 3.12, CrewAI, AutoGen, LangGraph | **Research** | 🟡 Stale (Behind Remote) | - |
| `java-servlets` | Legacy | Java (legacy) | **Legacy** | 🟢 Green | - |

## Last Update (per project)

One row per project, showing only the **most recent** iteration — overwrite the row (don't append) each time you finish work on a project, so returning after a gap tells you where things stand without re-reading the whole project. For full history, see the `✅ Completed` log in `active_tasks.md` instead.

| Project | Date | What was done |
| :--- | :--- | :--- |
| `cv-generator` | 2026-09-06 | Migrated to pnpm; added `CLAUDE.md` + mirrored the `senior-interviewer` and new `master-fe-requirement-cv-template-translator` skills under `.claude/skills/`; added the **Engineering (Senior)** CV theme. Fixed a critical bug where 26 stale compiled `.js` files under `src/` were silently shadowing their `.tsx`/`.ts` sources (set `tsconfig.json` `noEmit: true` to prevent recurrence). Fixed a render crash on flat-array `technologies` and added a `domains` field. Brought README/GEMINI/CLAUDE/NEXT_STEPS docs to parity. Deleted stale local branch `fix/error-handling`. |
| `wealthtrack` | 2026-09-06 | Fixed "Sync Data" only refreshing the Dashboard — added `revalidatePath()` for every sheet-data route (kept the 24h passive cache TTL, per user's call). Fixed dates from the Apps Script snapshot automation rendering as raw serial numbers on `/balance` and Registro_Saldos-derived screens — added `formatDateDisplay()`. Mirrored the Google Apps Script locally (`apps-script/`). All 102 tests + build passing. |
| `importer-porfolio` | 2026-09-12 | [PR #10](https://github.com/fedefailla18/importer-porfolio/pull/10) (Dockerfile for `crypto-ui`) still open, awaiting review. Closed stale [PR #9](https://github.com/fedefailla18/importer-porfolio/pull/9) (pnpm migration, 14 commits behind, superseded by `main`'s own) and deleted 2 fully-merged-elsewhere branches (`chore/migrate-to-pnpm-and-security-updates`, `docs-ui-audit-and-stats-polish`). |
| `project-hub` | 2026-09-08 | `wp` no longer streams raw service logs to the terminal — status line per service + log-on-failure only, `.wp-logs/` — [PR #1](https://github.com/fedefailla18/project-hub/pull/1), still open. Also fixed Ctrl+C leaving gradlew's JVM running, and `run_all()` missing `crypto-ui`. (`wp`/`docker-compose.yml` path/port/schema fixes from the same day already merged to `main`.) |
| `healthVault` | 2026-08-25 | Committed Phase 2 Google Sheets integration plan (`PHASE2_PLAN.md`) on `main`. |
| `investracker` | 2026-09-12 | Repo renamed `file-importer` → `investracker` on GitHub (jar/gradle/docs updated to match; Java package `com.importer.fileimporter` and DB schema `file_importer_schema` deliberately left as-is). PR #61/#62 merged (upload 415, CORS, Binance/MexC/IOL bugs). Opened [PR #63](https://github.com/fedefailla18/investracker/pull/63) (docs reorg: 20 md files → 8, by feature) and [PR #64](https://github.com/fedefailla18/investracker/pull/64) (fixed `/my-trades`+`/orders` 400ing on their own default 2020→now range — Binance rejects >24h windows on those two endpoints), both awaiting review. Earlier the same day: deleted 3 branches confirmed via `git patch-id` already squash-merged into `main`. |
| `agents` | — | Not yet tracked here. Known open item: `main` is 33 commits behind origin. |
| `java-servlets` | — | Not yet tracked here. |

## Project Notes

### WealthTrack (`wealthtrack/`)
- Consolidated net worth & AI wealth advisor. Deployed on Vercel (Node 22).
- Migrated to **pnpm** + production-ready **Docker** multi-stage build.
- Google Sheets automation (`Registro_Saldos`/`Balance` rollforward) lives in a Google Apps Script, mirrored locally at `apps-script/wealthtrack-core.gs.js`.
- "Sync Data" button forces a full refresh across every sheet-reading route (`SHEET_DATA_ROUTES` in `lib/actions.ts`); passive cache TTL stays 24h otherwise.

### InvestTracker (`investracker/`)
- Crypto transaction history ingestion and P&L calculation. Renamed from `file-importer` 2026-09-12 (started as a single-purpose upload-a-file tool, grew into a full multi-exchange portfolio tracker — repo, local dir, gradle, jar, docs all say `investracker` now; Java package `com.importer.fileimporter` and DB schema `file_importer_schema` deliberately not renamed).
- Multi-stage `Dockerfile` (gradle build stage → JRE runtime stage); builds natively on arm64 and amd64. `project-hub/docker-compose.yml`'s `crypto-*` services build this same file, targeting the same Postgres data as `investracker/docker/docker-compose.yml` — don't run both postgres services at once.
- Docs reorganized 2026-09-12: 20 markdown files → 8, in `investracker/docs/`, organized by feature (architecture, accounting-scenarios, exchange-integrations, authentication, testing, roadmap, deploy-guide, api-documentation-guide) instead of by author/date.
- `BinanceSyncServiceSpec` (all 7 tests) fails on an unrelated pre-existing NPE — `Mock(TransactionProcessor)`, a class that no longer exists in `src/main` (accounting logic moved to `CoinInformationService` + `CalculateAmountSpent` when PR #60 removed it in favor of lazy evaluation — not simply renamed to a single class). Fallout from the old `integration/new-portfolio-syncing-app` refactor (already merged); nobody's fixed the test file since.

### Importer Portfolio (`importer-porfolio/`)
- Frontend for the crypto tracking system.
- Migrated to **pnpm**. `Dockerfile` added 2026-09-09 (multi-stage: pnpm build → nginx) — [PR #10](https://github.com/fedefailla18/importer-porfolio/pull/10), pending merge.

### CV Generator (`cv-generator/`)
- Dual-purpose: interactive CV builder + interview management/calibration hub.
- Migrated to **pnpm**. Now has `CLAUDE.md` at parity with `GEMINI.md`; both AI skills (`senior-interviewer`, `master-fe-requirement-cv-template-translator`) mirrored under `.claude/skills/` and `.gemini/skills/`.
- New **Engineering (Senior)** CV theme (reference implementation for future theme refactors); legacy themes (Modern/Minimal/Compact/Two-Column) still pending migration onto shared components.

---
*Last Updated: 2026-09-12*

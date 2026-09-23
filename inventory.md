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
| `importer-porfolio` | 2026-09-23 | [PR #11](https://github.com/fedefailla18/importer-porfolio/pull/11) merged (sync-jobs panel). Its branch kept moving — sync buttons now require an exact `exchangeName` match, new `ConsolidateDialog` + `PortfolioExchangesGuide` banner, Sync CTAs on both activity pages — and picked up a real bug fix today: every Redux thunk's error handling (8 slices) fell back to the raw Spring Boot error body when it had no `.message` field, which then got rendered directly as a React child and crashed `BinanceSpotActivityPage`/`MexcSpotActivityPage` with "Objects are not valid as a React child". Fixed with a shared `extractErrorMessage` helper. `tsc`/lint/build all clean. Opened as new [PR #12](https://github.com/fedefailla18/importer-porfolio/pull/12) (PR #11 had already merged). [PR #10](https://github.com/fedefailla18/importer-porfolio/pull/10) (Dockerfile for `crypto-ui`) still open from before, awaiting review. **`gh` CLI is broken in this environment** (xcrun/libxcrun architecture mismatch) — PR #12 was created via the GitHub REST API directly as a workaround; `gh pr`/`gh issue` commands will fail until Xcode Command Line Tools are repaired. |
| `project-hub` | 2026-09-08 | `wp` no longer streams raw service logs to the terminal — status line per service + log-on-failure only, `.wp-logs/` — [PR #1](https://github.com/fedefailla18/project-hub/pull/1), still open. Also fixed Ctrl+C leaving gradlew's JVM running, and `run_all()` missing `crypto-ui`. (`wp`/`docker-compose.yml` path/port/schema fixes from the same day already merged to `main`.) |
| `healthVault` | 2026-08-25 | Committed Phase 2 Google Sheets integration plan (`PHASE2_PLAN.md`) on `main`. |
| `investracker` | 2026-09-23 | [PR #65](https://github.com/fedefailla18/investracker/pull/65) updated twice more, both confirmed against the user's real DB (not hypothetical): (1) `reconcileOrphanedJobs()` + `SyncJobStartupReconciler` self-heal `sync_job`s left `PENDING`/`RUNNING` by a killed process — any such row found right after boot can only be orphaned, gets marked `FAILED` (retriable) with `RUNNING` chunks reset to `PENDING`, `COMPLETED` chunks/checkpoints untouched. (2) Retrying that reconciled batch then hit `LazyInitializationException` on every `TRADES` chunk — `runJob` reloaded the job via plain `findById`, handing back a lazy `Portfolio` proxy that nothing could initialize once `portfolio.getUser()` was called (no spanning `@Transactional`, by design). Fixed with `SyncJobRepository.findByIdWithPortfolioAndUser`, a `JOIN FETCH` query, without reintroducing any transaction span. 139 tests, same 11 pre-existing failures, 0 new. Also live-blocking `inventory_cost_usdt` column bug (incomplete rename from PR #63) fixed via migration 045, plus an `exchange_name` backfill (046) and Sync CTAs added to the Binance/MexC activity pages. Original PR #65 scope (resumable, chunked job tracking for the Binance full-history sync, `sync_job`/`sync_job_chunk`, spec in `docs/binance-sync-jobs.md`) opened 2026-09-15, still awaiting review. [PR #63](https://github.com/fedefailla18/investracker/pull/63)/[#64](https://github.com/fedefailla18/investracker/pull/64) still open from before, awaiting review. |
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
- Binance full-sync (PR #65, pending review): `sync_job`/`sync_job_chunk` tables track it as 5 independently-retryable jobs (trades/deposits/withdrawals/fiat/convert), each broken into chunks (one symbol, or one 90/30-day window). Deliberately separate from the older `binance_sync_progress`/`BinanceOrderSyncService` tables, which back a different, still-live diagnostic feature (raw per-symbol orders via `BinanceIntegrationController`) — don't conflate the two when reading the schema.
- **Portfolio vs Exchanges** (same PR #65): "Portfolio" (manual entries) and "Exchanges" (API-synced) are meant to be two comparable, separately-owned views — `Portfolio.exchangeName` marks which. Every sync path resolves its target through `PortfolioService.resolveExchangePortfolio(...)`, which refuses to write into a manually-managed or wrong-exchange portfolio (400). `POST /portfolio/consolidate` is the explicit, repeat-safe way to merge an exchange portfolio's transactions into a manual one — sync itself never does this.

### Importer Portfolio (`importer-porfolio/`)
- Frontend for the crypto tracking system.
- Migrated to **pnpm**. `Dockerfile` added 2026-09-09 (multi-stage: pnpm build → nginx) — [PR #10](https://github.com/fedefailla18/importer-porfolio/pull/10), pending merge.
- `SyncJobsPanel` (PR #11, pending review) shows live status for investracker's new Binance sync-job model — 5 rows (trades/deposits/withdrawals/fiat/convert), chunk progress, retry on FAILED. Polls `GET /transaction/sync/binance/jobs` every 4s while any job is active; the WebSocket `JOB_FINISHED`/`JOB_CRASHED` messages just nudge an earlier refresh, they aren't the source of truth.
- `ConsolidateDialog` (same PR) lets the user merge an exchange portfolio's data into a manually-managed one they're viewing (`POST /portfolio/consolidate`); `PortfolioExchangesGuide` is a dismissible banner on `PortfolioHubPage`/`ExchangesLandingPage` explaining why the two sections stay separate.

### CV Generator (`cv-generator/`)
- Dual-purpose: interactive CV builder + interview management/calibration hub.
- Migrated to **pnpm**. Now has `CLAUDE.md` at parity with `GEMINI.md`; both AI skills (`senior-interviewer`, `master-fe-requirement-cv-template-translator`) mirrored under `.claude/skills/` and `.gemini/skills/`.
- New **Engineering (Senior)** CV theme (reference implementation for future theme refactors); legacy themes (Modern/Minimal/Compact/Two-Column) still pending migration onto shared components.

---
*Last Updated: 2026-09-16*

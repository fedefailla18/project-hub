# Unified Task Board

Global priorities across the workspace.

## 🔴 High Priority
- **`investracker`**: Resolve merge conflicts on `integration/new-portfolio-syncing-app` against `main` (which adopted the lazy `InventoryState` refactoring in PR #60).
- **`agents`**: Sync `main` branch with remote origin (33 commits behind).
- **Workspace**: Deploy and monitor the new unified Docker orchestration (`docker-compose.yml`).
- **`investracker`/`wp` [IN PROGRESS]**: **Bug — `./wp run crypto-tracker` (and `./wp run docker`) can't reach the backend ("Network Error" in the UI).** Root cause chain, fully traced:
  - `project-hub/wp`'s `CRYPTO_BACKEND_DIR` points at `../file-importer` — a stub directory (only a stray `docker/data` volume in it, no source, no `gradlew`). The real project was renamed to `investracker/` locally (GitHub repo is still named `file-importer`, hence the confusion) but `wp` was never updated. So `run_crypto()`/`run_all()` `cd` into a dead directory and `./gradlew bootRun` silently fails in the background — the frontend (`importer-porfolio`, correctly hardcoded to `http://localhost:9080`) starts fine and just can't connect.
  - `project-hub/docker-compose.yml`'s `crypto-db`/`crypto-api` services *also* point at `../file-importer` (build context + volumes) — same issue for the `./wp run docker` path. Its `crypto-api` additionally maps port `8080:8080`, but the app listens on **9080** (per `investracker/application.yml` — confirmed correct via `investracker/CLAUDE.md`, which is accurate) — wrong port mapping, and its `SPRING_DATASOURCE_URL` is missing `?currentSchema=file_importer_schema,public`, which investracker's own `docker/docker-compose.yml` includes.
  - Root workspace `CLAUDE.md`'s investracker Quick-Start section documents port **8080** — this is stale/wrong; investracker's own `CLAUDE.md` (accurate) says 9080 for both the app and Swagger UI.
  - There are now **two separate Postgres instances** for the same app: `crypto-db` (project-hub compose, port 5433, backed by `file-importer/docker/data`) and `postgres_importer` (investracker's own compose, port 5435, backed by `investracker/docker/data`). Verified via `\dt` + `pg_stat_user_tables`: `crypto-db` is **completely empty** (0 tables — Liquibase never ran against it, nothing has ever really used it) while `postgres_importer` has all 18 real tables (`databasechangelog` present) and is the one `application.yml` actually points at. `crypto-db` is dead weight, safe to retire.
  - `investracker`'s `Dockerfile` is single-stage: it `COPY build/libs/file-importer-0.0.1-SNAPSHOT.jar app.jar` — it does **not** build from source, it expects a pre-built jar on the host. The jar currently there is from **2026-05-03**, well before the last commit (2026-08-26) — so even once the compose path is repointed correctly, `docker compose up --build` for `crypto-api` would ship stale code unless `./gradlew build` is re-run first, or the Dockerfile is converted to a proper multi-stage build (gradle build happens inside the image).
  - Separately (found while reading `wp`, unrelated to crypto): `run_cv_gen()` has a copy-paste bug — it `cd`s into `$HEALTH_VAULT_DIR` and logs "Starting HealthVault dev server", so `./wp run cv-gen` actually launches healthVault instead of cv-generator.
  - **Open questions asked of the user 2026-09-08** (see below) before touching anything: (1) what to do with the orphaned empty `crypto-db` container + `file-importer/` directory, (2) whether to fix the Dockerfile properly (multi-stage, self-building) or just document "run `./gradlew build` before `docker compose up --build`" as a cheaper stopgap.

## 🟡 Medium Priority
- **`wealthtrack`**: Monitor Vercel deployment of the `feature/optimize-data-and-trends` branch.
- **`healthVault`**: Begin Phase 2 (Google Sheets Integration) research.
- **`project-hub`**: Create symbolic links to project `GEMINI.md` files for faster context switching.
- **`cv-generator`**: Refactor legacy themes (Modern/Minimal/Compact/Two-Column) onto the shared components the Engineering theme introduced (`src/themes/shared/`, `cvRenderHelpers.ts`).

## 🟢 Low Priority
- **Security**: Run periodic scans for new vulnerabilities in the pnpm ecosystem.

## ✅ Completed
- **`project-hub`**: Model tier logic updated to zero-cost local runner (`ai/gemma3`), pycache ignored, branch `feature/create-agents` merged into `main`. Docker orchestration added (`docker-compose.yml`).
- **`wealthtrack`**: Merged debt support & account panel branch (`cr/feat/debt-support-and-account-settings`) into `main`. Cleaned up stale SSO branch. All 102 unit tests passing. Migrated to pnpm + Docker multi-stage build.
- **`cv-generator`**: Extracted sticky `Navbar` component, added candidate/job profiles, resolved TS2322 in `InterviewsDashboard`, build verified, and merged `feature/data-persistence` into `main`.
- **`cv-generator`**: Migrated to pnpm; added `CLAUDE.md` and mirrored the `senior-interviewer` + new `master-fe-requirement-cv-template-translator` skills under `.claude/skills/` (parity with existing `.gemini/skills/`). Added an **Engineering (Senior)** CV theme (paired with content spec `upgrade.md`). Fixed a critical bug where 26 stale compiled `.js` files committed under `src/` were silently shadowing their `.tsx`/`.ts` sources in both dev and prod builds (Vite resolves `.js` before `.tsx` for extensionless imports) — deleted them and set `tsconfig.json` `noEmit: true` to prevent recurrence. Fixed a render crash when `WorkItem.technologies` is a flat array instead of a grouped record, and added support for a `domains` field. Clarified `interviews/README.md` wording (`interviews/jobs/` = roles you're hiring for, not your own job search). Deleted stale local branch `fix/error-handling` (fully superseded by `main`, would have reintroduced the `.js` files and deleted newer candidate data).
- **`healthVault`**: Committed Phase 2 Google Sheets integration plan (`PHASE2_PLAN.md`) on `main`.
- **`importer-porfolio`**: Fixed `App.test.tsx` assertion, built successfully, and merged exchange sync UI branch `docs-ui-audit-and-stats-polish` into `main`. Migrated to pnpm + Docker Nginx runner.
- **`wealthtrack`**: Fixed "Sync Data" only refreshing the Dashboard (added `revalidatePath()` for every sheet-data route in `lib/actions.ts`, keeping the 24h passive cache TTL — user's call). Fixed dates from the Apps Script snapshot automation rendering as raw serial numbers (`46258` etc.) instead of text on `/balance` and Registro_Saldos-derived screens — added `formatDateDisplay()` (`lib/utils/date-utils.ts`) and wired it into `balance-transformers.ts` + `registro-saldos-transformers.ts`. Mirrored the Google Apps Script locally (`apps-script/wealthtrack-core.gs.js`). All 102 tests + build passing.

---
*Last Updated: 2026-09-06*

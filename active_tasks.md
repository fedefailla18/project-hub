# Unified Task Board

Global priorities across the workspace.

## 🔴 High Priority
- **`investracker`**: Resolve merge conflicts on `integration/new-portfolio-syncing-app` against `main` (which adopted the lazy `InventoryState` refactoring in PR #60).
- **`agents`**: Sync `main` branch with remote origin (33 commits behind).
- **Workspace**: Deploy and monitor the new unified Docker orchestration (`docker-compose.yml`).
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

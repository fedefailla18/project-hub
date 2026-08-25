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
- **`cv-generator`**: Review `NEXT_STEPS.md` for potential integration with the Hub.

## 🟢 Low Priority
- **Security**: Run periodic scans for new vulnerabilities in the pnpm ecosystem.

## ✅ Completed
- **`project-hub`**: Model tier logic updated to zero-cost local runner (`ai/gemma3`), pycache ignored, branch `feature/create-agents` merged into `main`. Docker orchestration added (`docker-compose.yml`).
- **`wealthtrack`**: Merged debt support & account panel branch (`cr/feat/debt-support-and-account-settings`) into `main`. Cleaned up stale SSO branch. All 102 unit tests passing. Migrated to pnpm + Docker multi-stage build.
- **`cv-generator`**: Extracted sticky `Navbar` component, added candidate/job profiles, resolved TS2322 in `InterviewsDashboard`, build verified, and merged `feature/data-persistence` into `main`.
- **`healthVault`**: Committed Phase 2 Google Sheets integration plan (`PHASE2_PLAN.md`) on `main`.
- **`importer-porfolio`**: Fixed `App.test.tsx` assertion, built successfully, and merged exchange sync UI branch `docs-ui-audit-and-stats-polish` into `main`. Migrated to pnpm + Docker Nginx runner.

---
*Last Updated: 2026-08-25*

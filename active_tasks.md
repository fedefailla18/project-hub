# Unified Task Board

Global priorities across the workspace.

## 🔴 High Priority
- **WealthTrack:** Deploy Vercel fixes for production errors on new-user login:
  - `ERR_OSSL_UNSUPPORTED` — private key PEM normalization bug fixed in `lib/google-sheets.ts`
  - Navbar disappearing on crash — root `app/error.tsx` error boundary added
  - `/accounts` crashing for new users — missing onboarding redirect guard fixed
  - **Action needed:** Set `GOOGLE_CREDENTIALS_BASE64` in Vercel (base64-encoded service-account JSON) as the recommended long-term fix for the OpenSSL key issue. See `lib/google-sheets.ts` comments for the encode command.
- **HealthVault:** Begin Phase 2 (Google Sheets Integration) research.

## 🟡 Medium Priority
- **Project Hub:** Create symbolic links to project `GEMINI.md` files for faster context switching.
- **CV Generator:** Review `NEXT_STEPS.md` for potential integration with the Hub.

## 🟢 Low Priority
- **Agents:** Summarize latest learning from the `deep_research/` folder.

---
*Last Updated: June 24, 2026*

# Delivery Plan — article-fetcher

## 1) Scope recap
- In scope: Fetch a URL, extract + convert to Markdown, headless-browser fallback for JS-heavy pages, preview-edit-confirm UX, catalog-compatible front-matter output. Same as Phase 0/1 — no changes.
- Out of scope: Automated summarization, direct writes into the Article Catalog System's storage, image downloading, batch/multi-URL processing.

## 2) Milestones
| Milestone | Deliverable | Owner | Target date |
|---|---|---|---|
| M1: Extraction pipeline | `fetcher.py`, `render.py`, `extract.py`, `pipeline.py` — fetch, extract, threshold-based Playwright fallback | You (sole developer) | Done |
| M2: Front-matter & editor UX | `frontmatter.py`, `editor.py` — catalog-compatible front-matter build/parse/validate, `$EDITOR` + confirm flow | You (sole developer) | Done |
| M3: CLI | `cli.py` (`article-fetch` entry point) wiring the full flow together | You (sole developer) | Done |
| M4: Test suite | 25 automated tests (no live network) + manual real-URL smoke test | You (sole developer) | Done |
| M5: SDLC documentation | This documentation set (Phases 0–6 + ADR) | You (sole developer) | In progress |

## 3) Work Breakdown (Epics → Stories)
- **Epic 1: Fetch & Extract** (FR-001, FR-002, FR-003)
  - Story 1.1: HTTP fetch with normalized error handling (FR-001)
  - Story 1.2: trafilatura-based extraction + Markdown conversion (FR-002)
  - Story 1.3: Word-count threshold + Playwright headless-render fallback (FR-003)
- **Epic 2: Front-matter & Review UX** (FR-004, FR-005, FR-006, FR-007)
  - Story 2.1: Build catalog-compatible front-matter from extracted metadata + CLI flags (FR-004)
  - Story 2.2: `$EDITOR` preview/edit flow before any write (FR-005)
  - Story 2.3: Final y/N confirmation, skippable via `--yes` (FR-006)
  - Story 2.4: Re-validate edited front-matter before writing (FR-007)
- **Epic 3: CLI surface** (FR-008, FR-009)
  - Story 3.1: `article-fetch` argument parsing (media-type, tag, output-dir, timeout, fallback toggle) (FR-008)
  - Story 3.2: Default output directory kept separate from the root project's `articles/` (FR-009)
- **Epic 4: Test suite** (NFR-004)
  - Story 4.1: Local HTTP server fixture + HTML fixtures (good/metadata/thin-JS-shell)
  - Story 4.2: Unit tests for extraction, fetch errors, front-matter, pipeline threshold logic
  - Story 4.3: Real-Playwright fallback test, skipped cleanly if chromium isn't installed
  - Story 4.4: CLI end-to-end test using `EDITOR=true` + `--yes`

## 4) Dependencies
- External teams: None (personal project)
- Vendors: None
- Environments: Local development machine only; separate `.venv` from the root project (see Constraints Register C-003)
- Approvals: N/A (sole developer)

## 5) Risks & Mitigations
- **Risk:** `trafilatura` may choose the wrong "main content" region on unusual page layouts.
  **Mitigation:** The preview-edit-confirm flow (FR-005/FR-006) exists specifically so a bad extraction can be caught and fixed before anything is saved.
- **Risk:** The Playwright fallback's Chromium binary is a manual, non-pip-scriptable install step that could be forgotten (C-006).
  **Mitigation:** Documented explicitly in `README.md`; `render.py` surfaces a clear `RenderError` naming the missing step rather than a raw stack trace.
- **Risk:** The 150-word fallback threshold is a heuristic that may not generalize to all sites.
  **Mitigation:** Exposed as a parameter (`min_word_count`) on `pipeline.fetch_and_extract`, not a hardcoded constant — easy to tune later without a redesign.

## 6) Rollout strategy
- Feature flags: None needed (personal project mode — direct use default)
- Phased rollout: N/A — single user, direct use once built
- Rollback plan: The tool only ever writes new files under `--output-dir`; nothing to roll back beyond deleting those files. Uninstalling is just removing `article-fetcher/.venv`.

## 7) Definition of Done (DoD)
- [x] Code implements FR-001 through FR-009
- [x] Automated + manual checks confirm AC-001 through AC-004
- [x] Tool runs locally end-to-end (verified against a real Wikipedia URL)
- [ ] Phase 6 documentation (System Overview, Onboarding) written

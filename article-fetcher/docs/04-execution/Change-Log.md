# Change Log — article-fetcher

## Unreleased
- Added: `article-fetch` CLI — fetch a URL, extract + convert to Markdown, with a threshold-based Playwright fallback for JS-rendered pages (FR-001–FR-003).
- Added: Catalog-compatible front-matter generation, decoupled from `article_catalog`'s code (FR-004–FR-009, ADR-001).
- Added: `$EDITOR` preview/edit + confirm-before-write flow (FR-005–FR-007).
- Added: Test suite (`tests/`) — 25 tests covering extraction, fetch error handling, front-matter round-trip, pipeline threshold/fallback logic, CLI end-to-end flow, and a real headless-Chromium fallback test.
- Changed: N/A (first implementation)
- Fixed: N/A (first implementation)
- Security: N/A — no auth/secrets in scope; outbound fetches are limited to user-supplied public URLs (NFR-003)

# ADR-002: trafilatura + threshold-based Playwright fallback for content extraction

- **Status:** Accepted
- **Date:** 2026-07-04
- **Owners:** Ignacio (sole developer)

## Context

The tool needs to turn an arbitrary article URL into clean Markdown, covering both ordinary static/blog pages and modern JS-rendered pages where the meaningful content doesn't exist in the initial HTML response at all. A library/approach had to be chosen for extraction + Markdown conversion, and a strategy decided for the JS-rendered case, without making every single run pay the cost of a full headless-browser launch.

## Decision

Use `trafilatura` for both steps: `trafilatura.bare_extraction()` (no `output_format`) for structured metadata (title/date/author/sitename via attribute access), and `trafilatura.extract(..., output_format="markdown")` for the Markdown body — these had to be split into two separate calls after confirming trafilatura's actual behavior during implementation (`bare_extraction`'s `.text`/`.raw_text` fields do not reflect the requested `output_format`; only `extract()`'s return value does). If the extracted body's word count is below a threshold (default 150, exposed as a parameter, not hardcoded), fall back to rendering the page with headless Chromium via Playwright and re-run the same extraction on the rendered HTML, using whichever pass yields more words.

## Consequences

### Positive
- One library (`trafilatura`) covers metadata extraction and Markdown conversion, avoiding a `readability-lxml` + `markdownify` combination and its extra surface area.
- The threshold-based fallback means the common case (static, server-rendered articles) never launches a browser — Playwright is imported lazily inside `render.py` and only touched when actually needed.
- Making the threshold a function parameter rather than a constant made the pipeline's decision logic fully unit-testable (force or skip the fallback deterministically) without needing a real thin page or a live browser for most tests.

### Negative
- `playwright install chromium` is a manual, non-pip-scriptable step (~150-300MB Chromium binary) that must be run once and can be forgotten — mitigated by a clear `RenderError` message and explicit `README.md` documentation (C-006).
- The 150-word threshold is a heuristic; a legitimately short article (e.g. a brief news item) could incorrectly trigger the fallback, adding latency without adding real content. Accepted as a reasonable default, with `min_word_count` exposed for tuning if it proves wrong in practice (Requirements Open Question Q-001).
- `trafilatura`'s extraction quality varies by site layout; a wrong "main content" pick isn't detected automatically — this is exactly why the preview-edit-confirm UX (FR-005/FR-006) exists as a safety net rather than relying on extraction being perfect.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| `readability-lxml` + `markdownify` | Well-known, widely used combination | Two libraries instead of one; no built-in metadata (date/author) extraction comparable to trafilatura's; would need a third library (e.g. `htmldate`) for that, which trafilatura already bundles | More moving parts for no clear quality gain |
| Always render every page with Playwright, no static-fetch-first step | Simpler control flow, handles JS pages uniformly | Every single run pays a ~1-2s Chromium launch cost, even though most articles are plain server-rendered HTML | Unnecessarily heavy for the common case; rejected in favor of a fast path with a fallback |
| A hosted "reader" API (e.g. a URL-prefix service that fetches and converts server-side) | Zero local dependencies, no Chromium to install | Sends every fetched URL through a third-party service outside the user's control; a form of external integration the Problem Statement/Constraints explicitly avoid for this personal tool | Rejected — keeps all fetching local, no third-party dependency on content the user is reading |

## Links
- Related requirements: FR-001, FR-002, FR-003, FR-004, NFR-003; Constraints C-006
- Related design docs: `docs/02-planning/High-Level-Design.md` (Options A, B, C), `docs/03-architecture-data/Data-Contracts.md`
- PRs/issues: N/A

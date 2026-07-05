# High-Level Design (HLD) — article-fetcher

## 1) Overview
- What are we building: A standalone CLI that fetches a URL, extracts and converts the main article content to Markdown, and stages it as a catalog-compatible front-matter file for manual review before saving.
- Why: No automated fetch/convert path exists today; adding a web article to any Markdown-based catalog means manual transcription (see `docs/00-scoping/Problem-Statement.md`).

## 2) System Context
- Actors: Sole user (Ignacio) — runs the CLI against a URL of interest.
- External systems: The public web page at the given URL (fetched over plain HTTP(s), or rendered via headless Chromium when needed). No API contracts, no authentication.
- Trust boundaries: Local machine only for execution; the only network calls are outbound fetches of user-supplied URLs. No inbound exposure, no server process.

## 3) Proposed Solution (Big picture)
- Components:
  - **`fetcher.py`** — plain HTTP GET via `requests`, normalizes network failures into `FetchError`.
  - **`extract.py`** — pure function over an HTML string; uses `trafilatura` for both metadata (title/date/author/sitename via `bare_extraction`) and body Markdown (via `extract(..., output_format="markdown")`); returns an `ExtractedArticle` with a `word_count`.
  - **`render.py`** — lazily-imported Playwright headless-Chromium render, used only when the fallback triggers; wraps failures as `RenderError`.
  - **`pipeline.py`** — orchestrates fetch → extract → word-count threshold check → Playwright fallback if needed → picks whichever pass yielded more content.
  - **`frontmatter.py`** — local (not imported from `article_catalog`) id generation, `MEDIA_TYPES`, and YAML front-matter build/render/parse/validate, using the same field names/order as the Article Catalog System's schema.
  - **`editor.py`** — tempfile + `$EDITOR` invocation (mirrors `git commit`'s UX) plus a y/N confirmation helper.
  - **`cli.py`** — `article-fetch` entry point wiring the above into one flow.
- Responsibilities:
  - `fetcher`/`render` own getting HTML by any means (static fetch or JS-rendered).
  - `extract` owns turning HTML into structured Markdown + metadata, independent of how the HTML was obtained.
  - `pipeline` owns the fetch-vs-fallback decision.
  - `frontmatter` owns the on-disk file shape.
  - `editor` owns the human-in-the-loop review step.
  - `cli` owns argument parsing and sequencing; it contains no extraction/rendering logic itself.
- Data flow (steps):
  1. User runs `article-fetch <url> [flags]`.
  2. `pipeline.fetch_and_extract` calls `fetcher.fetch_html`, then `extract.extract_from_html`.
  3. If the result's word count is below the threshold (and the fallback isn't disabled), `render.render_with_playwright` re-fetches via headless Chromium and `extract.extract_from_html` runs again on the rendered HTML; whichever pass has more words wins.
  4. `cli.py` builds front-matter via `frontmatter.build_front_matter` (title/date from extraction, `references=[url]`, `summary=""`, media type/tags from flags) and renders the draft Markdown.
  5. `editor.edit_in_editor` opens the draft in `$EDITOR` for the user to review/fix.
  6. The edited text is re-parsed and validated (`frontmatter.validate_front_matter`); invalid input is rejected with a clear error, not written.
  7. Unless `--yes`, `editor.confirm` asks for a final y/N before `cli.py` writes the file under `--output-dir`.

## 4) Alternatives considered
- **Option A (chosen): `trafilatura` for extraction + Markdown conversion, with a word-count-threshold-based Playwright fallback.** One library covers metadata extraction and Markdown conversion together; Playwright is only invoked when actually needed, keeping the common case fast and dependency-light at runtime.
- **Option B: `readability-lxml` + `markdownify` combo, always static (no browser fallback).** Would miss JS-rendered/SPA pages entirely — rejected because that's a real, expected case (many modern sites render content client-side).
- **Option C: Always render every page with Playwright (no static-fetch-first step).** Simpler control flow, but pays the ~1-2s Chromium launch cost on every single run, even for the large majority of pages that are perfectly readable via a plain HTTP fetch — rejected as unnecessarily heavy for the common case.
- **Option D: Share the root project's `pyproject.toml`/venv instead of a separate one.** Rejected — see Constraints Register C-003 and the standalone-architecture ADR (Phase 3): a separate venv makes the "no calls into `article_catalog`'s IO" constraint structurally true rather than just a convention to remember.

## 5) Key Decisions
- Link to ADRs (draft/accepted):
  - Candidate new ADR (Phase 3): "Standalone architecture — separate venv, no shared code with article_catalog, schema-compatible output only."
  - Candidate new ADR (Phase 3): "trafilatura + threshold-based Playwright fallback for content extraction."

## 6) Non-functional impacts
- Security: N/A — local tool, no authentication, no secrets. The only external interaction is outbound HTTP(S) fetches of user-supplied URLs (NFR-003 covers failure handling for this).
- Performance: The static-fetch-first design (Option A) means most runs never pay the Chromium launch cost; only genuinely thin extractions trigger the heavier fallback path.
- Operability: Direct local use, no ops/on-call needed (personal project mode). The one operational gotcha is the manual `playwright install chromium` step (C-006) — documented in `README.md` and surfaced as a clear error if skipped.

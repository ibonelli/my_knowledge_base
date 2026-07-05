# Implementation Notes — article-fetcher

## Scope implemented
- All of v1 — FR-001 through FR-009: fetch a URL, extract + convert to Markdown, threshold-based Playwright fallback for JS-rendered pages, catalog-compatible front-matter generation, `$EDITOR` preview/edit flow, confirm-before-write (skippable via `--yes`), re-validation of the edited content, and CLI flags for media type/tags/output directory/timeout/fallback toggle.

## Files touched
- `article-fetcher/pyproject.toml` — package metadata; `requests`, `trafilatura`, `playwright`, `PyYAML` dependencies; `article-fetch` console script
- `article-fetcher/README.md`, `.gitignore`
- `article_fetcher/fetcher.py` — HTTP fetch via `requests`, `FetchError`
- `article_fetcher/render.py` — lazily-imported Playwright headless-Chromium render, `RenderError`
- `article_fetcher/extract.py` — `trafilatura`-based extraction (metadata via `bare_extraction`, body via `extract(output_format="markdown")`), `ExtractionError`
- `article_fetcher/pipeline.py` — fetch → extract → word-count threshold → Playwright fallback orchestration
- `article_fetcher/frontmatter.py` — local id-gen, local `MEDIA_TYPES`, front-matter build/render/parse/validate
- `article_fetcher/editor.py` — tempfile + `$EDITOR` + confirm helpers
- `article_fetcher/cli.py` — `article-fetch` entry point
- `tests/conftest.py`, `tests/fixtures/{good_article,metadata_article,thin_js_shell}.html`
- `tests/test_extract.py`, `test_fetcher.py`, `test_frontmatter.py`, `test_pipeline.py`, `test_cli_flow.py`, `test_playwright_fallback.py`

## Key decisions (links to ADRs)
- ADR-001: Standalone architecture — separate venv, no shared code with `article_catalog`, schema-compatible output only.
- ADR-002: `trafilatura` + threshold-based Playwright fallback for content extraction.
- Language/tooling: Python 3.10+, `requests` for HTTP, `trafilatura` for extraction/Markdown conversion, `playwright` for the JS-rendering fallback, stdlib `argparse`/`subprocess`/`tempfile` for the CLI and editor flow.

## Edge cases handled
- Zero-content extraction (even after the Playwright fallback) raises `ExtractionError` rather than silently writing an empty article.
- `fetcher.fetch_html` validates the URL scheme/netloc upfront, giving a clean `FetchError` for garbage input instead of an opaque `requests` traceback; timeout/HTTP-status/other-network failures are each normalized into the same `FetchError` type with an actionable message.
- Playwright is imported lazily inside `render.py` so the common (no-fallback-needed) path never pays for loading it.
- The article id is generated once, before the editor opens, so editing the title in `$EDITOR` never changes the output filename.
- The edited text is re-parsed and re-validated after `$EDITOR` closes — a user-introduced error (blank title, invalid media type) is rejected with a clear message instead of being written.
- `--yes` skips only the final confirmation prompt, not the editor step — it exists both for scripting and as the key testability hook for the CLI's automated tests (avoids needing to fake stdin).

## Known limitations
- No automated summarization — the `summary` field is always blank at write time (deliberate scope decision, not a gap).
- No image extraction/downloading — `images` is always an empty list in v1.
- The 150-word fallback threshold is a fixed default; it's exposed as a function parameter (`pipeline.fetch_and_extract(min_word_count=...)`) but not yet as a CLI flag (Requirements Open Question Q-001).
- No batch/multi-URL support — one URL per invocation (Q-002).
- The Playwright Chromium binary requires a manual, non-pip-scriptable install step (`playwright install chromium`); skipping it surfaces as a `RenderError` only when the fallback is actually triggered, not at install time.
- Test coverage gap (see `docs/05-testing/Traceability.md` for the full list): the CLI's `--no-playwright-fallback` and `--timeout` flags aren't exercised by a dedicated CLI-level test — the underlying `pipeline`-level behavior they toggle is tested directly instead.

## Migration steps
- None — this is a new system with no prior data to migrate.

## How to test locally
- Step 1: `cd article-fetcher && python3 -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -e '.[test]' && .venv/bin/playwright install chromium`
- Step 2: `.venv/bin/pytest -q` (25 tests — verified passing, no live network access required)
- Step 3 (manual): `.venv/bin/article-fetch <a real article URL> --output-dir imported --yes`, then inspect the resulting file under `imported/`

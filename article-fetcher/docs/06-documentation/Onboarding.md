# Onboarding — article-fetcher

## Repository map
- `article_fetcher/` — the Python package
  - `fetcher.py` — HTTP fetch (`requests`), `FetchError`
  - `render.py` — Playwright headless-Chromium fallback (lazily imported), `RenderError`
  - `extract.py` — `trafilatura`-based extraction + Markdown conversion, `ExtractionError`
  - `pipeline.py` — fetch → extract → threshold → fallback orchestration
  - `frontmatter.py` — local id-gen, `MEDIA_TYPES`, front-matter build/render/parse/validate
  - `editor.py` — tempfile + `$EDITOR` + confirm helpers
  - `cli.py` — the `article-fetch` entry point
- `imported/` — default output directory for fetched articles (git-ignores `*.md` inside it — working data, not source)
- `tests/` — `conftest.py` (local loopback HTTP server fixture), `fixtures/` (sample HTML), and the test modules (25 tests total)
- `docs/` — this project's own SDLC artifacts, separate from the root Article Catalog System's `docs/`
- `pyproject.toml` — package metadata, dependencies (`requests`, `trafilatura`, `playwright`, `PyYAML`), and the `article-fetch` console script

Note: like the root project, this package has no tracked `__init__.py` files (works as a PEP 420 implicit namespace package) — intentional, not an oversight.

## How to install / run locally
```bash
cd article-fetcher
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e '.[test]'
.venv/bin/playwright install chromium
```
Requires Python 3.10+. The `playwright install chromium` step downloads the actual browser binary (~150-300MB) and cannot be done via `pip` alone — it's a one-time step; skipping it only matters once the Playwright fallback is actually triggered.

Run the test suite:
```bash
.venv/bin/pytest -q
```

## Usage
```bash
.venv/bin/article-fetch <url> \
  [--media-type {written,graphic,video}] [--tag TAG ...] \
  [--output-dir DIR] [--no-playwright-fallback] [--timeout SECONDS] [--yes]
```

Example:
```bash
.venv/bin/article-fetch https://example.com/some-article --tag ai --output-dir imported
```

This fetches the page, extracts and converts it to Markdown (falling back to a headless-browser render if the content looks too thin), opens the derived front-matter + body in `$EDITOR` for you to review or fix, asks `Save to <path>? [y/N]`, and writes the file under `imported/` (or wherever `--output-dir` points) once confirmed.

If you want the result in the Article Catalog System's catalog, copy the output file into the root project's `articles/` directory and run `article reindex` there yourself — article-fetcher never does this automatically (ADR-001, C-005).

## How to deploy
Not applicable — this runs as a local CLI on the developer's own machine. No server, hosting, or deploy pipeline (personal project mode).

## Key decisions
- [ADR-001 — Standalone architecture](../adr/ADR-001-standalone-architecture.md)
- [ADR-002 — trafilatura + Playwright-fallback extraction](../adr/ADR-002-trafilatura-with-playwright-fallback.md)

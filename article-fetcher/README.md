# article-fetcher

Standalone CLI: give it a URL, it fetches the page, converts the main content to Markdown, and stages
it as a front-matter Markdown file for you to review and edit before saving.

It does **not** import or call into `article_catalog` (the sibling Article Catalog System in this repo) —
it's a fully separate tool with its own virtualenv and dependencies. Its output *is* schema-compatible
with `article_catalog`'s front-matter shape, so if you want an imported article in the catalog, copy the
resulting `.md` file into the root `articles/` directory and run `article reindex` yourself. This tool
never writes there directly.

It does not summarize articles — it only fetches and converts. Summarizing (by hand, or by pasting the
Markdown to an LLM) is a separate, manual step.

## Install

```bash
cd article-fetcher
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e '.[test]'
.venv/bin/playwright install chromium
```

The `playwright install chromium` step downloads the actual headless-browser binary and has no pip
equivalent — it's a one-time step. Skipping it doesn't break the common case (most static articles never
need the Playwright fallback), but the fallback will fail with a `RenderError` if you hit a JS-heavy page
before running it.

Run the test suite:
```bash
.venv/bin/pytest -q
```

## Usage

```bash
.venv/bin/article-fetch <url> [--media-type {written,graphic,video}] [--tag TAG ...] \
  [--output-dir DIR] [--no-playwright-fallback] [--timeout SECONDS] [--yes]
```

Flow:
1. Fetches the URL and extracts the main article content as Markdown (via `trafilatura`). If the content
   looks too thin (likely a JS-rendered page), automatically retries by rendering the page with headless
   Chromium (Playwright) and re-extracting — unless `--no-playwright-fallback` is passed.
2. Opens the derived front-matter + Markdown body in `$EDITOR` (falls back to `vi`) so you can fix the
   title, media type, tags, summary, or body before anything is saved.
3. Prompts `Save to <path>? [y/N]` (skip with `--yes`) and writes the file under `--output-dir`
   (default: `imported/`, relative to this directory — not the root project's `articles/`).

## Key decisions

- [ADR-001 — Standalone architecture](docs/adr/ADR-001-standalone-architecture.md)
- [ADR-002 — trafilatura + Playwright-fallback extraction](docs/adr/ADR-002-trafilatura-with-playwright-fallback.md)

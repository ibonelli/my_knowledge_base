# article-fetcher

## TLDR

```bash
cd article-fetcher
.venv/bin/article-fetch https://www.enriquedans.com/2025/05/cerabyte-el-futuro-del-almacenamiento-de-datos-a-largo-plazo-en-ceramica.html
```

## Intro

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

## Behavior

What happens:
1. It fetches the page and converts the main content to Markdown (falls back to a headless-browser render automatically if the page looks JS-rendered/too thin).
2. It opens a draft front-matter + Markdown file in $EDITOR (falls back to vi if $EDITOR isn't set) so you can fix the title, tags, summary, or body before anything is saved.
3. After you close the editor, it asks Save to <path>? [y/N].
4. If you confirm, it writes the file under imported/ (default output directory, relative to article-fetcher/).

It never touches the root project's articles/ or catalog.db — if you want a fetched article in the actual catalog, copy the resulting .md file into articles/ yourself and run article reindex there.

## Useful flags

```
.venv/bin/article-fetch <url> \
  --media-type {written,graphic,video}   # default: written
  --tag ai --tag productivity            # repeatable, optional
  --output-dir some/other/dir            # default: imported/
  --no-playwright-fallback               # disable the headless-browser fallback
  --timeout 30                           # fetch timeout in seconds, default 15
  --yes                                  # skip the final y/N confirmation (editor still opens)
```
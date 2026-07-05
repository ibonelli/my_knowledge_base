# System Overview — article-fetcher

## What this system does
article-fetcher is a personal, local-only CLI tool that takes a URL, fetches the page, extracts the main article content, converts it to Markdown, and stages it as a front-matter Markdown file for manual review and editing before anything is saved. It is deliberately standalone: it never calls into the sibling Article Catalog System's code, though its output uses the same front-matter field names so a file can optionally be copied into that project's `articles/` and reindexed by hand. It does not summarize articles — summarizing is left to the user, as a separate manual step.

## Architecture summary
- **Components:**
  - `fetcher.py` — plain HTTP GET via `requests`, normalized `FetchError`.
  - `extract.py` — `trafilatura`-based extraction: metadata (title/date/author/sitename) via `bare_extraction()`, body Markdown via `extract(output_format="markdown")`.
  - `render.py` — lazily-imported Playwright headless-Chromium render, used only when the fallback triggers.
  - `pipeline.py` — orchestrates fetch → extract → word-count threshold check → Playwright fallback if the content looks too thin.
  - `frontmatter.py` — local id generation and YAML front-matter build/render/parse/validate, schema-compatible with the Article Catalog System but implemented independently (no import).
  - `editor.py` — tempfile + `$EDITOR` invocation and a y/N confirmation helper.
  - `cli.py` (`article-fetch` command) — wires the above into one flow.
- **Data flow:** `article-fetch <url>` fetches and extracts; if the result is too thin, it re-fetches via headless Chromium and extracts again, keeping whichever pass yielded more content. It then builds a draft front-matter file, opens it in `$EDITOR` for review, re-validates the edited result, asks for a final confirmation (unless `--yes`), and writes the file under `--output-dir` (default: `imported/`).

## Known failure modes
- **Fetch failure** (bad URL, timeout, HTTP error) → `FetchError`, printed to stderr, exit code 1 — occurs before any temp file or editor is touched.
- **Extraction yields zero content**, even after the Playwright fallback → `ExtractionError`, exit code 1.
- **Playwright/Chromium not installed** → `RenderError` naming the missing `playwright install chromium` step, rather than a raw traceback.
- **Edited front-matter is invalid** (empty title, unknown media type) → rejected with a clear error; nothing written.
- **User declines the final confirmation** → aborts cleanly, nothing written, exit code 0.

## Ownership
Sole developer (Ignacio) — owner, user, and on-call for this personal project. No formal SLOs; best-effort availability.

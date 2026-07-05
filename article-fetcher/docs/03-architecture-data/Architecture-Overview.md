# Architecture Overview — article-fetcher

## 1) Boundaries & Ownership
- `article_fetcher/` package (`fetcher.py`, `render.py`, `extract.py`, `pipeline.py`, `frontmatter.py`, `editor.py`, `cli.py`) — owned by sole developer (you). Fully standalone: no shared ownership, code, or runtime dependency with `article_catalog` (C-001, C-003).
- Explicitly NOT owned by this tool: the root project's `articles/` directory and `catalog.db` — this tool never writes there (C-005).

## 2) Interfaces
- **API endpoints:** None — no network-exposed API. Interaction happens via a single CLI command: `article-fetch <url> [--media-type ...] [--tag ...] [--output-dir ...] [--no-playwright-fallback] [--timeout ...] [--yes]`.
- **Events/topics:** None — single-process, synchronous, one URL per invocation.
- **Data stores:** None persistent besides the output `.md` files under `--output-dir` (default: `imported/`, relative to `article-fetcher/`). No database.

## 3) Security Model
- AuthN: None — single local user, no login.
- AuthZ: None — filesystem permissions on the local machine are the only access control.
- Secrets management: N/A — no credentials or tokens. The only network activity is outbound HTTP(S) GET requests to user-supplied URLs, sent with a custom `User-Agent` string (`article-fetcher/0.1 (+personal knowledge base tool)`).

## 4) Operational Model
- Deployment: Runs as a local CLI script inside its own virtualenv (`article-fetcher/.venv`) on the developer's machine — no server process, no hosting (personal project mode: direct use, no deploy pipeline).
- Scaling: N/A — single user, one URL processed per invocation; no concurrency requirements (C-007).
- Failure modes:
  - **Fetch failure** (bad URL, timeout, HTTP error status) → `FetchError`, printed to stderr, exit code 1 — occurs *before* any temp file or editor is touched.
  - **Extraction yields zero content**, even after the Playwright fallback → `ExtractionError`, exit code 1.
  - **Playwright not installed, or Chromium binary missing** → `RenderError` with a message naming the missing `playwright install chromium` step, rather than a raw traceback (C-006).
  - **Edited front-matter is invalid** (empty title, unknown media type) → rejected with a clear error; nothing is written (FR-007).
  - **User declines the final confirmation prompt** → aborts cleanly, nothing written, exit code 0.

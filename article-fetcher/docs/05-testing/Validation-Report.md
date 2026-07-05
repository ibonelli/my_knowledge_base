# Validation Report — article-fetcher

## Execution Summary
- Command: `.venv/bin/pytest -q` (from `article-fetcher/`)
- Result: **25 passed, 0 failed, 0 skipped** (run with `playwright install chromium` already completed, so the two real-Playwright tests executed rather than skipping)
- Static check: `grep -rn "article_catalog" article_fetcher/ tests/ pyproject.toml` — only hits are a code comment and the `pyproject.toml` description string; **zero import statements** (confirms NFR-001/C-001/F-001).

## Manual Verification
- Ran `article-fetch` against a real, live URL (`https://en.wikipedia.org/wiki/Local-first_software`) with `EDITOR=cat` (non-interactive stand-in) and `--yes`:
  - Fetched and extracted successfully; produced a valid front-matter file with correct `title`, `references` (containing the source URL), `tags` (from `--tag`), `media_type` (default `written`), `published_date` (pulled from the page's own metadata), and `created_at` (today).
  - Confirmed the root project's `articles/` directory and `catalog.db` were **not modified** by this run (AC-004, FR-009, C-005).

## Defects Found and Resolved During Implementation
- `extract.py`'s original design assumed `trafilatura.bare_extraction(..., output_format="markdown")` would populate a markdown-formatted `.text` field — verified against the actually-installed `trafilatura==2.1.0` and found this to be incorrect (`.text`/`.raw_text` don't reflect `output_format`). Fixed by splitting into two calls: `bare_extraction()` (no `output_format`) for metadata, `trafilatura.extract(..., output_format="markdown")` for the body. This is now the implemented and tested behavior (see `docs/adr/ADR-002...`).
- `tests/test_pipeline.py`'s original `test_fallback_skipped_when_disabled` incorrectly expected an `ExtractionError` for thin-but-nonzero content with the fallback disabled; corrected to match the intended design (only genuinely zero-content extraction raises — thin content is returned as-is when the fallback is off). A new `test_fallback_triggered_for_zero_content_page` was added to cover the actual zero-content-raises case.

## Risk Acceptance
- The gaps listed in `Traceability.md` (FR-005, FR-008, FR-009, NFR-002 partial coverage) are accepted for v1 — each has either a manual verification already performed, or a lower-risk profile (e.g. `argparse`'s own `choices` validation backstops `--media-type` even without a dedicated test).
- Extraction-quality risk on unusual page layouts is accepted by design — the preview-edit-confirm UX (FR-005/FR-006) is the mitigation, not a test.

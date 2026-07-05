# Test Plan — article-fetcher

## 1) Scope
- In scope: `article_fetcher` package — HTTP fetch, content extraction/Markdown conversion, pipeline threshold/fallback decision logic, front-matter build/parse/validate, the `$EDITOR`+confirm CLI flow, and the real Playwright fallback path.
- Out of scope: Performance/load testing (single-user, one-URL-at-a-time tool by design — C-007); security penetration testing (no attack surface beyond fetching URLs the user themselves chooses to fetch).

## 2) Test Types
- **Unit** — `extract.extract_from_html`, `frontmatter.*` (pure functions, HTML/text fixtures only).
- **Integration** — `fetcher.fetch_html` and `pipeline.fetch_and_extract` against a local loopback HTTP server; CLI end-to-end via `cli.main()`.
- **Real-dependency** — one pair of tests that launch actual headless Chromium via Playwright, skipped cleanly (not failed) when the browser binary isn't installed.
- **Manual smoke test** — a real public URL, run by hand after any pipeline change (not automated, since it depends on live third-party content).

## 3) Test Environments
- Local only — no formal DEV/QA/PROD matrix (personal project mode). "Deployed" doesn't apply; this is a local CLI tool.

## 4) Entry Criteria
- Code implemented per the Phase 2 Delivery Plan work breakdown.
- Dependencies installed: `pip install -e '.[test]'` and `playwright install chromium`.

## 5) Exit Criteria
- All automated tests pass, OR the Playwright-dependent tests cleanly skip with a clear reason (chromium not installed) rather than failing.
- The manual real-URL smoke test succeeds at least once per significant pipeline change.
- No test requires live, non-loopback network access (NFR-004) — verified by inspection: every test either feeds HTML strings directly, uses the local `http.server` fixture, or (for the one manual step) is explicitly documented as the exception.

## 6) Test Cases

| ID | Test | Requirement(s) |
|---|---|---|
| TC-001 | `test_fetch_html_success` | FR-001 |
| TC-002 | `test_fetch_html_404` | FR-001, NFR-003 |
| TC-003 | `test_fetch_html_timeout` | FR-001, NFR-003 |
| TC-004 | `test_fetch_html_rejects_non_http_scheme` / `rejects_malformed_url` | FR-001, NFR-003 |
| TC-005 | `test_extract_from_good_article` | FR-002 |
| TC-006 | `test_extract_metadata_title_and_date` | FR-002, FR-004 |
| TC-007 | `test_extract_from_empty_html_returns_zero_word_count` | FR-002 |
| TC-008 | `test_extract_from_thin_shell_is_thin_without_js` | FR-002 (fallback-trigger baseline) |
| TC-009 | `test_primary_extraction_used_when_above_threshold` | FR-003 |
| TC-010 | `test_fallback_skipped_when_disabled` | FR-003, FR-008 |
| TC-011 | `test_fallback_triggered_and_used_when_it_yields_more_content` | FR-003 |
| TC-012 | `test_forcing_fallback_via_high_threshold_even_on_good_content` | FR-003 |
| TC-013 | `test_fallback_triggered_for_zero_content_page` | FR-003, NFR-003 |
| TC-014 | `test_generate_id_shape` | FR-004 |
| TC-015 | `test_render_and_parse_round_trip` | FR-004, NFR-002 |
| TC-016 | `test_parse_markdown_requires_front_matter` | FR-007 |
| TC-017 | `test_validate_front_matter_requires_title` / `_requires_known_media_type` / `_accepts_valid_input` | FR-007 |
| TC-018 | `test_cli_end_to_end_saves_article` | FR-001–FR-009, AC-001 |
| TC-019 | `test_cli_aborts_without_yes_when_not_confirmed` | FR-006 |
| TC-020 | `test_cli_fetch_error_exits_before_editor` | NFR-003, F-002 (negative test) |
| TC-021 | `test_playwright_renders_client_side_content` | FR-003 (real render) |
| TC-022 | `test_pipeline_uses_real_playwright_fallback_for_thin_js_page` | FR-003, AC-002 (real) |
| TC-023 | Static grep check: no `article_catalog` import anywhere in `article_fetcher/`/`tests/` | NFR-001, C-001, F-001 (negative test) |

## 7) Known Risky Areas
- Extraction quality on unusual page layouts (mitigated by the preview-edit-confirm UX, not by tests — this is inherently a judgment call trafilatura can get wrong).
- The 150-word fallback threshold generalizing across real-world sites beyond the synthetic test fixtures.
- The CLI's `--no-playwright-fallback` and `--timeout` flags are not exercised end-to-end through `cli.main()` — only the underlying `pipeline` parameters they map to are tested directly (see Traceability for the full gap list).

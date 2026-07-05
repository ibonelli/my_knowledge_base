# Traceability Matrix — article-fetcher

## Requirements → Test Cases

| Requirement | Test Case(s) | Status |
|---|---|---|
| FR-001 (fetch URL) | TC-001, TC-002, TC-003, TC-004 | Passed |
| FR-002 (extract + convert to Markdown) | TC-005, TC-006, TC-007, TC-008 | Passed |
| FR-003 (Playwright fallback) | TC-009, TC-010, TC-011, TC-012, TC-013, TC-021, TC-022 | Passed |
| FR-004 (derive metadata + front-matter) | TC-006, TC-014, TC-015 | Passed |
| FR-005 (`$EDITOR` review) | TC-018 (via `EDITOR=true` stand-in) | Partial — the actual interactive editing experience is not automatable; only the flow *around* it (temp file written, editor invoked, result re-read) is tested |
| FR-006 (confirm before write) | TC-018, TC-019 | Passed |
| FR-007 (re-validate edited content) | TC-016, TC-017 | Passed |
| FR-008 (CLI flags) | TC-010 (fallback toggle, at the `pipeline` level), TC-018 (`--tag`, `--output-dir`, `--yes`) | Partial — `--no-playwright-fallback` and `--timeout` are not exercised through `cli.main()` itself, only via the underlying `pipeline` parameters; `--media-type`'s restriction relies on `argparse`'s own `choices` validation rather than a dedicated test |
| FR-009 (never writes to root `articles/`/`catalog.db`) | Manual verification only (AC-004) | Passed (manually) — no dedicated automated test asserts this negative property directly; all automated tests write only under `tmp_path`/explicit `--output-dir`, which never touches the root project by construction |
| NFR-001 (isolation from `article_catalog`) | TC-023 (static grep) | Passed |
| NFR-002 (output schema compatibility) | TC-015 | Partial — round-trip is tested, but there is no automated cross-check against `article_catalog.storage`'s actual field list; compatibility was confirmed by code review at design time |
| NFR-003 (clear errors, no raw tracebacks) | TC-002, TC-003, TC-004, TC-013, TC-020 | Passed |
| NFR-004 (testable without live network) | All of TC-001–TC-020 use loopback/direct HTML only; TC-021/TC-022 use loopback + local Chromium | Passed |

## Constraints → Negative Tests

| Constraint | Test Case | Status |
|---|---|---|
| C-001 / F-001 (no `article_catalog` imports) | TC-023 | Passed |
| C-004 (no auto-summarization) | Implicit — `frontmatter.build_front_matter` always receives `summary=""` from `cli.py`; covered by TC-018's assertion that `meta["summary"] == ""` | Passed |
| C-005 (no writes to root `articles/`/`catalog.db`) | Manual verification (see FR-009 above) | Passed (manually) |
| F-002 (no write without preview/confirm, unless `--yes`) | TC-019 | Passed |
| F-003 (no silent error swallowing) | TC-020 | Passed |

## Gaps Carried Forward
- FR-005, FR-008, FR-009, NFR-002 are marked "Partial" above — these are genuine, acknowledged gaps, not oversights. They're accepted for a personal-project v1 given the manual smoke-testing already performed, but are candidates for follow-up if the tool sees heavier use.

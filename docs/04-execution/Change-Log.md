# Change Log — Article Catalog System

## Unreleased
- Added: `article-gui` PyQt6 desktop GUI — full CLI feature parity (add/edit/delete/list/search/reindex), split-pane Markdown editor with live preview, inline image thumbnails, single-window master-detail layout (FR-008–FR-011, ADR-003).
- Added: `article_catalog/core.py` shared core module — validation and storage/index orchestration used by both the CLI and the GUI (NFR-004, C-007).
- Added: `tests/test_core.py` — 5 tests covering the shared core module (add/list/search/edit/delete/reindex, validation errors, not-found errors, backfill).
- Changed: `article_catalog/cli.py` refactored to delegate to `core.py` instead of implementing validation/orchestration inline; CLI command behavior and output are unchanged.
- Changed: `pyproject.toml` — added `PyQt6>=6.4` as a required dependency and the `article-gui` console script.
- Fixed: N/A
- Security: N/A — no auth/secrets in scope (NFR-003)

## Previous
- Added: `article` CLI (v1) — `add`, `list`, `search`, `edit`, `delete`, `reindex` subcommands.
- Added: Markdown + YAML front-matter storage for article content (`articles/*.md`), per ADR-001.
- Added: SQLite search index (`catalog.db`) over title/tags/media type, rebuildable from Markdown files per ADR-002.
- Added: Test suite (`tests/`) — 12 tests covering storage, index, and CLI behavior.
- Changed: N/A (first implementation)
- Fixed: N/A (first implementation)
- Security: N/A — no auth/secrets in scope (NFR-003)

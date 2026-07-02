# Change Log — Article Catalog System

## Unreleased
- Added: `article` CLI (v1) — `add`, `list`, `search`, `edit`, `delete`, `reindex` subcommands.
- Added: Markdown + YAML front-matter storage for article content (`articles/*.md`), per ADR-001.
- Added: SQLite search index (`catalog.db`) over title/tags/media type, rebuildable from Markdown files per ADR-002.
- Added: Test suite (`tests/`) — 12 tests covering storage, index, and CLI behavior.
- Changed: N/A (first implementation)
- Fixed: N/A (first implementation)
- Security: N/A — no auth/secrets in scope (NFR-003)

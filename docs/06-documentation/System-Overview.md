# System Overview — Article Catalog System

## What this system does
The Article Catalog System is a personal, local-only tool for cataloging articles of any media type (written, graphic, video) sourced from any outlet or time period into one searchable collection. It lets the sole user add articles with structured metadata (title, summary, tags, references, Markdown body, optional images), browse/list them, search by tag and/or title, edit or delete entries, and backfill historical articles with a distinct published date — solving the "organic growth, hard to navigate" problem already observed in the freeform knowledge-base notes. It ships with two interfaces: the original CLI, and a PyQt6 desktop GUI with full feature parity (ADR-003).

## Architecture summary
- **Components:**
  - Storage layer (`articles/*.md`) — one Markdown file per article with YAML front-matter; the source of truth (ADR-001).
  - Index layer (`catalog.db`, SQLite) — derived, rebuildable search index over title/tags/media type (ADR-002); never the source of truth.
  - Core layer (`article_catalog/core.py`) — shared validation and orchestration (add/edit/delete/search/reindex); the only code path either interface uses to touch storage/index (NFR-004, ADR-003).
  - CLI layer (`article_catalog/cli.py`, installed as the `article` command) — subcommands: `add`, `list`, `search`, `edit`, `delete`, `reindex`.
  - GUI layer (`article_catalog/gui/`, installed as the `article-gui` command) — PyQt6 desktop app; single-window master-detail layout (article list/search pane + detail/edit pane), split-pane Markdown editor with live preview, inline image thumbnails.
- **Data flow:** Both `article` (CLI) and `article-gui` (GUI) call the same core-layer functions. Add/edit/delete write to `articles/*.md` first, then update the matching row(s) in `catalog.db`. List/search reads only from `catalog.db` for speed. Reindex (CLI subcommand or GUI button) rebuilds `catalog.db` from scratch by rescanning all Markdown front-matter — the recovery path if the index and files ever diverge.

## Known failure modes
- **SQLite index out of sync or corrupted** → Detected by search/list results not matching what's on disk. Remediation: run `article reindex` or use the GUI's Reindex button — no data loss, since Markdown files are the source of truth.
- **Markdown file edited manually outside the CLI/GUI** (e.g. hand edit or `git pull`) → Not auto-detected yet. Remediation: reindex to resync.
- **Missing or broken image reference** → Architecture specifies "warn but don't block". In the GUI, a missing/unreadable image renders as `[missing: <path>]` text in the thumbnail row rather than failing to load the article; explicit warn-on-save validation is not yet implemented in either interface — see Implementation Notes known limitations.
- **CLI and GUI run against the same catalog concurrently** → Not a supported scenario (single-user, no-concurrency constraint, C-003); last writer wins.

## Ownership
Sole developer (Ignacio) — owner, user, and on-call for this personal project. No formal SLOs; best-effort availability.

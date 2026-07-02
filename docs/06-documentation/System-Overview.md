# System Overview — Article Catalog System

## What this system does
The Article Catalog System is a personal, local-only CLI tool for cataloging articles of any media type (written, graphic, video) sourced from any outlet or time period into one searchable collection. It lets the sole user add articles with structured metadata (title, summary, tags, references, Markdown body, optional images), browse/list them, search by tag and/or title, edit or delete entries, and backfill historical articles with a distinct published date — solving the "organic growth, hard to navigate" problem already observed in the freeform knowledge-base notes.

## Architecture summary
- **Components:**
  - Storage layer (`articles/*.md`) — one Markdown file per article with YAML front-matter; the source of truth (ADR-001).
  - Index layer (`catalog.db`, SQLite) — derived, rebuildable search index over title/tags/media type (ADR-002); never the source of truth.
  - CLI layer (`article_catalog/cli.py`, installed as the `article` command) — mediates all reads/writes, keeping the Markdown store and SQLite index in sync; subcommands: `add`, `list`, `search`, `edit`, `delete`, `reindex`.
- **Data flow:** `article add/edit/delete` writes to `articles/*.md` first, then updates the matching row(s) in `catalog.db`. `article list/search` reads only from `catalog.db` for speed. `article reindex` rebuilds `catalog.db` from scratch by rescanning all Markdown front-matter — the recovery path if the index and files ever diverge.

## Known failure modes
- **SQLite index out of sync or corrupted** → Detected by search/list results not matching what's on disk. Remediation: run `article reindex` — no data loss, since Markdown files are the source of truth.
- **Markdown file edited manually outside the CLI** (e.g. hand edit or `git pull`) → Not auto-detected yet. Remediation: run `article reindex` to resync.
- **Missing or broken `--image` reference** → Architecture specifies "warn but don't block"; not yet implemented (currently silently accepted either way) — see Implementation Notes known limitations.

## Ownership
Sole developer (Ignacio) — owner, user, and on-call for this personal project. No formal SLOs; best-effort availability.

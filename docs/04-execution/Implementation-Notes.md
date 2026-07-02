# Implementation Notes — Article Catalog System

## Scope implemented
- All of v1 — FR-001 through FR-007: add an article with full metadata, list/browse, search/filter by tag and/or title, edit, delete, support for 3 media types (written/graphic/video), and backfilling old articles via a historical `--published-date`.

## Files touched
- `article_catalog/__init__.py`
- `article_catalog/models.py` — `Article` dataclass, `MEDIA_TYPES`
- `article_catalog/storage.py` — Markdown + YAML front-matter read/write, validation, tag normalization
- `article_catalog/index.py` — SQLite schema + queries (articles, tags, article_tags), `rebuild_index`
- `article_catalog/cli.py` — `article` CLI: `add`, `list`, `search`, `edit`, `delete`, `reindex`
- `pyproject.toml` — package metadata, PyYAML dependency, `article` console script
- `.gitignore` — excludes `catalog.db` (derived/rebuildable per ADR-002) and Python build artifacts
- `articles/.gitkeep` — placeholder for the Markdown article store
- `tests/test_storage.py`, `tests/test_index.py`, `tests/test_cli.py`

## Key decisions (links to ADRs)
- ADR-001: Article bodies stored as Markdown with YAML front-matter for metadata.
- ADR-002: SQLite is a derived, rebuildable search index — Markdown files remain the sole source of truth.
- Language/tooling: Python 3.10+, PyYAML for front-matter parsing, argparse for the CLI, stdlib `sqlite3` for the index — chosen to minimize dependencies for a solo-maintained project (confirmed with the user before implementation started).

## Edge cases handled
- Tags are trimmed, lowercased, and de-duplicated on write (mitigates tag-sprawl risk from the Delivery Plan).
- Editing or deleting a non-existent article ID exits cleanly with an error message instead of crashing.
- An empty catalog prints "no articles found" for `list`/`search` rather than nothing.
- Backfilled articles carry a historical `published_date` distinct from `created_at` (the date added to the catalog).
- Full index rebuild verified: deleting `catalog.db` entirely and running `article reindex` reconstructs the index purely from the Markdown files' front-matter with no data loss — the core guarantee behind ADR-002.

## Known limitations
- No image existence/reachability validation on `--image` references — the Architecture Overview specifies "warn but don't block," which is not yet implemented (currently silently accepted either way).
- No automatic re-indexing when a Markdown file is edited outside the CLI (e.g. by hand or via git pull) — `article reindex` must be run manually to resync.
- Title search (`--title`) is a plain case-insensitive substring match (SQL `LIKE`), not fuzzy or ranked.

## Migration steps
- None — this is a new system with no prior data to migrate.

## How to test locally
- Step 1: `python3 -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -e '.[test]'`
- Step 2: `.venv/bin/pytest -q` (12 tests covering storage, index, and CLI)
- Step 3 (manual): `.venv/bin/article --articles-dir articles --db catalog.db add --title "..." --media-type written --tag foo`, then `article list` / `article search --tag foo`

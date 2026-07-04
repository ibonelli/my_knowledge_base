# Implementation Notes — Article Catalog System

## Scope implemented
- All of v1 — FR-001 through FR-007: add an article with full metadata, list/browse, search/filter by tag and/or title, edit, delete, support for 3 media types (written/graphic/video), and backfilling old articles via a historical `--published-date`.
- GUI increment — FR-008 through FR-011, NFR-004, NFR-005: a PyQt6 desktop GUI with full CLI feature parity (add/edit/delete/list/search/reindex), a split-pane Markdown editor with live preview, inline image thumbnails, and a single-window master-detail layout. Both interfaces now call a shared core module rather than duplicating logic (ADR-003).

## Files touched
- `article_catalog/models.py` — `Article` dataclass, `MEDIA_TYPES`
- `article_catalog/storage.py` — Markdown + YAML front-matter read/write, validation, tag normalization
- `article_catalog/index.py` — SQLite schema + queries (articles, tags, article_tags), `rebuild_index`
- `article_catalog/core.py` — **new**, shared core module (NFR-004, ADR-003): `add_article`, `edit_article`, `delete_article`, `get_article`, `list_articles`, `search_articles`, `reindex`, `NotFoundError`. Wraps `storage`/`index` and is the only code path either interface uses to read/write articles.
- `article_catalog/cli.py` — refactored to delegate all business logic to `core`; `article` CLI commands (`add`, `list`, `search`, `edit`, `delete`, `reindex`) are unchanged from the CLI user's perspective.
- `article_catalog/gui/app.py` — **new**, `article-gui` entry point; builds the `QApplication`, connects to the SQLite index, shows `MainWindow`.
- `article_catalog/gui/main_window.py` — **new**, `MainWindow`: master-detail layout (FR-011), tag/title search, split-pane Markdown editor + `QTextEdit`-style live preview via `setMarkdown()` (FR-009), inline image thumbnails via `QPixmap` (FR-010), and add/save/delete/reindex actions, all delegating to `core`.
- `pyproject.toml` — package metadata; `PyQt6>=6.4` added as a required dependency (NFR-005, supersedes the original minimize-dependencies default); new `article-gui` console script.
- `.gitignore` — excludes `catalog.db` (derived/rebuildable per ADR-002), Python build artifacts, and (pre-existing convention in this repo) `__init__.py` files, which is why `article_catalog/gui/` has no `__init__.py` — it works as a PEP 420 implicit namespace package, consistent with the rest of `article_catalog/`.
- `articles/.gitkeep` — placeholder for the Markdown article store
- `tests/test_storage.py`, `tests/test_index.py`, `tests/test_cli.py`, `tests/test_core.py` (**new**)

## Key decisions (links to ADRs)
- ADR-001: Article bodies stored as Markdown with YAML front-matter for metadata.
- ADR-002: SQLite is a derived, rebuildable search index — Markdown files remain the sole source of truth.
- ADR-003: PyQt6 desktop GUI as a second, peer interface to the CLI, both built on a shared core module.
- Language/tooling: Python 3.10+, PyYAML for front-matter parsing, argparse for the CLI, stdlib `sqlite3` for the index, PyQt6 for the GUI — CLI dependencies were originally minimized for a solo-maintained project; PyQt6 is a deliberate, confirmed exception now that the GUI is a first-class interface (NFR-005, ADR-003).

## Edge cases handled
- Tags are trimmed, lowercased, and de-duplicated on write (mitigates tag-sprawl risk from the Delivery Plan).
- Editing or deleting a non-existent article ID raises `core.NotFoundError`; the CLI turns this into a clean error message + exit code 1, the GUI turns it into a `QMessageBox` warning — neither crashes.
- An empty catalog prints "no articles found" (CLI) / shows an empty list (GUI) for `list`/`search` rather than nothing.
- Backfilled articles carry a historical `published_date` distinct from `created_at` (the date added to the catalog).
- Full index rebuild verified: deleting `catalog.db` entirely and running `article reindex` (or the GUI's Reindex button) reconstructs the index purely from the Markdown files' front-matter with no data loss — the core guarantee behind ADR-002.
- GUI image thumbnails: a missing or unreadable image path renders as `[missing: <path>]` text instead of failing to load the article (consistent with Architecture Overview's "warn but don't block").

## Known limitations
- No image existence/reachability validation on `--image` references at write time — the Architecture Overview specifies "warn but don't block," which is only implemented as a GUI-side display fallback so far, not as an explicit warning on save in either interface.
- No automatic re-indexing when a Markdown file is edited outside the CLI/GUI (e.g. by hand or via git pull) — reindex must be run manually to resync.
- Title search (`--title` / GUI title filter) is a plain case-insensitive substring match (SQL `LIKE`), not fuzzy or ranked.
- GUI has no automated widget-level test suite (e.g. `pytest-qt`) yet — verified via a manual headless smoke script (`QT_QPA_PLATFORM=offscreen`) exercising add/select/edit/search/reindex/delete end-to-end; only `core.py` has automated test coverage for the GUI's underlying logic.
- GUI's metadata fields (tags/references/images) are single-line comma-separated text inputs, not dedicated list-editing widgets (e.g. add/remove chips) — adequate for a solo user, could be revisited if it becomes tedious.

## Migration steps
- None for CLI v1. GUI increment: existing catalogs (Markdown files + `catalog.db`) need no migration — the GUI reads/writes the same schema via the same core module as the CLI.

## How to test locally
- Step 1: `python3 -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -e '.[test]'`
- Step 2: `.venv/bin/pytest -q` (17 tests covering storage, index, CLI, and core)
- Step 3 (manual, CLI): `.venv/bin/article --articles-dir articles --db catalog.db add --title "..." --media-type written --tag foo`, then `article list` / `article search --tag foo`
- Step 4 (manual, GUI): `.venv/bin/article-gui --articles-dir articles --db catalog.db` — opens the desktop window; use New/Save/Delete/Reindex and the tag/title search fields.

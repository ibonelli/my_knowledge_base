# Onboarding — Article Catalog System

## Repository map
- `article_catalog/` — the Python package
  - `models.py` — `Article` dataclass, `MEDIA_TYPES`
  - `storage.py` — Markdown + YAML front-matter read/write, validation, tag normalization
  - `index.py` — SQLite schema + queries, `rebuild_index`
  - `core.py` — shared core module used by both interfaces: `add_article`, `edit_article`, `delete_article`, `get_article`, `list_articles`, `search_articles`, `reindex`, `NotFoundError` (NFR-004, ADR-003)
  - `cli.py` — the `article` CLI entry point (`add`, `list`, `search`, `edit`, `delete`, `reindex`)
  - `gui/` — the `article-gui` PyQt6 desktop app
    - `app.py` — entry point, builds `QApplication` and connects to the index
    - `main_window.py` — `MainWindow`: master-detail layout, search, split-pane Markdown editor + live preview, image thumbnails
- `articles/` — the Markdown article store (one `.md` file per article; source of truth per ADR-001)
- `tests/` — `test_storage.py`, `test_index.py`, `test_cli.py`, `test_core.py` (17 tests total)
- `docs/` — SDLC artifacts for this project (this folder)
- `pyproject.toml` — package metadata, dependencies (including `PyQt6`), and the `article` / `article-gui` console script entry points
- `catalog.db` — the SQLite search index (git-ignored; derived and rebuildable per ADR-002, not committed)

Note: this repo's `.gitignore` excludes all `__init__.py` files. `article_catalog/` and `article_catalog/gui/` therefore have none and work as PEP 420 implicit namespace packages — this is intentional and consistent across the whole package, not an oversight.

## How to install / run locally
```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e '.[test]'
```
Requires Python 3.10+. This installs the package in editable mode (including the required `PyQt6` dependency) plus `pytest` for the test suite, and registers the `article` and `article-gui` commands inside `.venv`.

Run the test suite:
```bash
.venv/bin/pytest -q
```

## Usage

### CLI
All commands operate relative to `--articles-dir` (default: `articles/`) and `--db` (default: `catalog.db`).

Add an article:
```bash
.venv/bin/article add --title "My Article" --media-type written \
  --tag ai --tag productivity \
  --summary "One or two sentence summary." \
  --reference "https://example.com/source"
```

List all articles:
```bash
.venv/bin/article list
```

Search by tag and/or title:
```bash
.venv/bin/article search --tag ai
.venv/bin/article search --title "My Article"
```

Edit or delete an existing article (by id):
```bash
.venv/bin/article edit <id> --summary "Updated summary."
.venv/bin/article delete <id>
```

Backfill an old article with a historical date:
```bash
.venv/bin/article add --title "Old Article" --media-type video \
  --published-date 2024-03-10
```

Rebuild the SQLite index from the Markdown files (recovery path — see Known Failure Modes in System-Overview.md):
```bash
.venv/bin/article reindex
```

### GUI
Launch the desktop app against the same articles directory and index:
```bash
.venv/bin/article-gui --articles-dir articles --db catalog.db
```
- Left pane: tag/title search fields, the article list, and New/Reindex buttons.
- Right pane: the selected (or new) article's metadata form, a split-pane Markdown editor with a live rendered preview, inline image thumbnails, and Save/Delete buttons.
- Click an article in the list to load it into the detail pane; click New to clear the form for a new article; Save calls the same `core.add_article`/`core.edit_article` the CLI uses, so the Markdown files and SQLite index stay in sync exactly as they would from the CLI.

The CLI and GUI are interchangeable — either can be used to manage the same `articles/`/`catalog.db`, just not at the same time (single-user, no-concurrency constraint, C-003).

## How to deploy
Not applicable — both the CLI and GUI run locally on the developer's own machine. No server, hosting, or deploy pipeline (personal project mode).

## Key decisions
- [ADR-001 — Markdown as article format](../adr/ADR-001-markdown-as-article-format.md)
- [ADR-002 — SQLite as rebuildable search index](../adr/ADR-002-sqlite-as-rebuildable-search-index.md)
- [ADR-003 — PyQt6 GUI with a shared core module](../adr/ADR-003-pyqt6-gui-shared-core-module.md)

# Onboarding — Article Catalog System

## Repository map
- `article_catalog/` — the Python package
  - `models.py` — `Article` dataclass, `MEDIA_TYPES`
  - `storage.py` — Markdown + YAML front-matter read/write, validation, tag normalization
  - `index.py` — SQLite schema + queries, `rebuild_index`
  - `cli.py` — the `article` CLI entry point (`add`, `list`, `search`, `edit`, `delete`, `reindex`)
- `articles/` — the Markdown article store (one `.md` file per article; source of truth per ADR-001)
- `tests/` — `test_storage.py`, `test_index.py`, `test_cli.py` (12 tests total)
- `docs/` — SDLC artifacts for this project (this folder)
- `pyproject.toml` — package metadata, dependencies, and the `article` console script entry point
- `catalog.db` — the SQLite search index (git-ignored; derived and rebuildable per ADR-002, not committed)

## How to install / run locally
```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e '.[test]'
```
Requires Python 3.10+. This installs the package in editable mode plus `pytest` for the test suite, and registers the `article` command inside `.venv`.

Run the test suite:
```bash
.venv/bin/pytest -q
```

## Usage
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

## How to deploy
Not applicable — this runs as a local CLI on the developer's own machine. No server, hosting, or deploy pipeline (personal project mode).

## Key decisions
- [ADR-001 — Markdown as article format](../adr/ADR-001-markdown-as-article-format.md)
- [ADR-002 — SQLite as rebuildable search index](../adr/ADR-002-sqlite-as-rebuildable-search-index.md)

# Architecture Overview — Article Catalog System

## 1) Boundaries & Ownership
- Storage layer (`articles/*.md`) — owned by sole developer (you). Source of truth for article content (ADR-001).
- Index layer (`catalog.db`, SQLite) — owned by sole developer (you). Derived, rebuildable search index, not source of truth (ADR-002).
- Core layer (shared module, e.g. `article_catalog/core.py`) — owned by sole developer (you). Owns validation and orchestration (add/edit/delete/search/reindex); the only code path allowed to write to storage and index (C-007, ADR-003).
- Interface layer — owned by sole developer (you). Two peers, both calling the core layer, never storage/index directly:
  - CLI (`article_catalog/cli.py`) — existing.
  - GUI (`article_catalog/gui/`) — new, PyQt6, master-detail desktop app (FR-008–FR-011, ADR-003).

## 2) Interfaces
- **API endpoints:** None — no network-exposed API. Interaction happens via CLI commands (e.g. `article add`, `article list`, `article search --tag=<tag>`, `article edit <id>`, `article delete <id>`) or via the equivalent PyQt6 GUI actions (list/search pane, add/edit form, delete confirmation, reindex action).
- **Events/topics:** None — single-process, synchronous operations only. (The GUI is single-window and single-threaded with respect to catalog operations — no background job queue.)
- **Data stores:**
  - `articles/` — folder of Markdown files, one per article, with YAML front-matter (see Data Contracts).
  - `catalog.db` — single local SQLite file indexing article metadata for search.

## 3) Security Model
- AuthN: None — single local user, no login (NFR-003, C-003).
- AuthZ: None — filesystem permissions on the local machine are the only access control.
- Secrets management: N/A — no external APIs, credentials, or tokens involved in v1.

## 4) Operational Model
- Deployment: Runs as a local CLI script/binary or a local PyQt6 desktop app on the developer's machine — no server process, no hosting (personal project mode: direct use, no deploy pipeline).
- Scaling: N/A — single user, catalog size expected to stay in the hundreds-to-low-thousands range; SQLite comfortably handles this scale.
- Failure modes:
  - **SQLite index out of sync or corrupted** → Rebuild by rescanning all Markdown files' front-matter (per ADR-002); no data loss since Markdown files are the source of truth. Reachable from both the CLI (`article reindex`) and the GUI (reindex action).
  - **Markdown file edited manually outside the CLI/GUI** → Re-index that single file on next run (or via the explicit reindex command/action).
  - **Missing or broken image reference** → Warn the user but do not block saving the article (images are optional per Data Contracts). In the GUI, a missing image falls back to a placeholder in the thumbnail preview rather than failing to render the article.
  - **CLI and GUI both open against the same `articles/`/`catalog.db` at once** → Not a supported scenario under the single-user, no-concurrency constraint (C-003); last writer wins, consistent with SQLite's default locking behavior.

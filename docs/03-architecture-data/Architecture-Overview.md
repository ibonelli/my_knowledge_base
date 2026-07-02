# Architecture Overview — Article Catalog System

## 1) Boundaries & Ownership
- Storage layer (`articles/*.md`) — owned by sole developer (you). Source of truth for article content (ADR-001).
- Index layer (`catalog.db`, SQLite) — owned by sole developer (you). Derived, rebuildable search index, not source of truth (ADR-002).
- CLI interface layer — owned by sole developer (you). Mediates all reads/writes to keep the two stores in sync.

## 2) Interfaces
- **API endpoints:** None — no network-exposed API. Interaction happens via CLI commands (e.g. `article add`, `article list`, `article search --tag=<tag>`, `article edit <id>`, `article delete <id>`).
- **Events/topics:** None — single-process, synchronous operations only.
- **Data stores:**
  - `articles/` — folder of Markdown files, one per article, with YAML front-matter (see Data Contracts).
  - `catalog.db` — single local SQLite file indexing article metadata for search.

## 3) Security Model
- AuthN: None — single local user, no login (NFR-003, C-003).
- AuthZ: None — filesystem permissions on the local machine are the only access control.
- Secrets management: N/A — no external APIs, credentials, or tokens involved in v1.

## 4) Operational Model
- Deployment: Runs as a local CLI script/binary on the developer's machine — no server process, no hosting (personal project mode: direct use, no deploy pipeline).
- Scaling: N/A — single user, catalog size expected to stay in the hundreds-to-low-thousands range; SQLite comfortably handles this scale.
- Failure modes:
  - **SQLite index out of sync or corrupted** → Rebuild by rescanning all Markdown files' front-matter (per ADR-002); no data loss since Markdown files are the source of truth.
  - **Markdown file edited manually outside the CLI** → Re-index that single file on next CLI run (or via an explicit `article reindex` command).
  - **Missing or broken image reference** → Warn the user but do not block saving the article (images are optional per Data Contracts).

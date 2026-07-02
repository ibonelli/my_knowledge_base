# High-Level Design (HLD) — Article Catalog System

## 1) Overview
- What are we building: A local, single-user application for cataloging articles (written, graphic, video) with structured metadata and a Markdown body, indexed for fast tag/title search.
- Why: No system currently exists to store and retrieve these articles reliably; unstructured accumulation risks repeating the "organic growth" navigation problem already seen in `AI_New_Links_ReDesignProposal.md`.

## 2) System Context
- Actors: Sole user (Ignacio) — adds, browses, edits, deletes, and searches articles.
- External systems: None identified yet. Open question (Q-002, Phase 1): whether this should integrate with or replace the existing knowledge-base Markdown notes.
- Trust boundaries: Local machine only — no network exposure, no auth required (per NFR-003, C-003).

## 3) Proposed Solution (Big picture)
- Components:
  - **Storage layer (source of truth):** One Markdown file per article, with YAML front-matter for metadata (title, summary, tags, online references, media type, date) and the article body as Markdown text below the front-matter. Satisfies C-001/ADR-001.
  - **Index layer:** A local SQLite database indexing article metadata (title, tags, media type, file path) to support fast tag/title search (FR-004) without re-parsing every Markdown file on each query.
  - **Interface layer:** A CLI or minimal local UI for add/edit/delete/list/search operations. Exact form (CLI vs. local web UI) deferred to Phase 3/4.
- Responsibilities:
  - Storage layer owns durability and portability of article content.
  - Index layer owns queryability (search/filter) and is treated as a derived/rebuildable cache, not the source of truth.
  - Interface layer owns user interaction and keeps the two in sync.
- Data flow (steps):
  1. User adds an article → metadata + Markdown body written to a new Markdown file (with front-matter) → file path + metadata indexed into SQLite.
  2. User searches by tag/title → query hits the SQLite index → returns matching file paths/metadata → Markdown body loaded from file for display.
  3. Backfill → same add flow, but with a historical publish date rather than the current date (FR-007).
  4. Edit/delete → Markdown file is updated/removed, and the SQLite index entry is updated/removed to stay in sync.

## 4) Alternatives considered
- **Option A (chosen): Markdown files + SQLite index.** Keeps content plain-text/git-friendly (NFR-001) while making search fast.
- **Option B: Flat-file only, no DB.** Search via grep/frontmatter parsing across all files on every query.
  - Why rejected: Would need to re-parse every Markdown file per search, becoming slow and fragile as the catalog grows — effectively reproducing the "organic growth" navigation problem this project exists to avoid.

## 5) Key Decisions
- Link to ADRs (draft/accepted):
  - ADR-001: Markdown as canonical article body format (Accepted)
  - Candidate new ADR: "SQLite as a rebuildable search index, not source of truth" — flagged for the post-phase ADR check.

## 6) Non-functional impacts
- Security: N/A — single user, no authentication/authorization required (NFR-003, C-003).
- Performance: SQLite index keeps tag/title search responsive as the catalog grows, supporting NFR-001 and AC-002.
- Operability: Direct deploy, no ops/on-call needed (personal project mode). Data-loss risk mitigated via git-tracked Markdown files and periodic SQLite backup (see Delivery Plan §5).

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
  - **Core layer:** Shared business logic (validation, tag normalization, orchestrating writes across the storage and index layers) extracted from the original CLI-only implementation, called by both interfaces below (NFR-004, C-007, ADR-003).
  - **Interface layer:** Two peer interfaces, both built on the core layer — the existing CLI (add/edit/delete/list/search/reindex), and a new PyQt6 desktop GUI with full feature parity (FR-008–FR-011, ADR-003). Decision on interface form (deferred in the original HLD) is now resolved: both, not either/or.
- Responsibilities:
  - Storage layer owns durability and portability of article content.
  - Index layer owns queryability (search/filter) and is treated as a derived/rebuildable cache, not the source of truth.
  - Core layer owns validation and keeping storage/index in sync — implemented once, used by every interface.
  - Interface layer (CLI, GUI) owns user interaction only; it delegates all reads/writes to the core layer rather than talking to storage/index directly.
- Data flow (steps):
  1. User adds an article (via CLI or GUI) → interface calls the core layer → metadata + Markdown body written to a new Markdown file (with front-matter) → file path + metadata indexed into SQLite.
  2. User searches by tag/title → core layer queries the SQLite index → returns matching file paths/metadata → Markdown body loaded from file for display (GUI additionally renders it live in a preview pane, per FR-009).
  3. Backfill → same add flow, but with a historical publish date rather than the current date (FR-007).
  4. Edit/delete → core layer updates/removes the Markdown file and the SQLite index entry together, so both interfaces stay in sync automatically.

## 4) Alternatives considered
- **Option A (chosen): Markdown files + SQLite index.** Keeps content plain-text/git-friendly (NFR-001) while making search fast.
- **Option B: Flat-file only, no DB.** Search via grep/frontmatter parsing across all files on every query.
  - Why rejected: Would need to re-parse every Markdown file per search, becoming slow and fragile as the catalog grows — effectively reproducing the "organic growth" navigation problem this project exists to avoid.

## 5) Key Decisions
- Link to ADRs (draft/accepted):
  - ADR-001: Markdown as canonical article body format (Accepted)
  - ADR-002: SQLite as a rebuildable search index, not source of truth (Accepted)
  - ADR-003: PyQt6 desktop GUI as a second interface, with a shared core module (Accepted)

## 6) Non-functional impacts
- Security: N/A — single user, no authentication/authorization required (NFR-003, C-003).
- Performance: SQLite index keeps tag/title search responsive as the catalog grows, supporting NFR-001 and AC-002.
- Operability: Direct deploy, no ops/on-call needed (personal project mode). Data-loss risk mitigated via git-tracked Markdown files and periodic SQLite backup (see Delivery Plan §5).
- Consistency: Core-layer extraction (NFR-004) means both CLI and GUI enforce the same validation and stay in sync with the index by construction, rather than by convention.
- Dependencies: PyQt6 becomes a required dependency (NFR-005, C-006) — an intentional exception to the CLI's original "minimize dependencies" default, since the GUI is now a first-class interface.

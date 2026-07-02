# ADR-002: SQLite as a rebuildable search index, not source of truth

- **Status:** Accepted
- **Date:** 2026-07-02
- **Owners:** Ignacio (sole developer)

## Context

The Article Catalog System stores article content as Markdown files with YAML front-matter (per ADR-001), which keeps content plain-text, portable, and git-friendly. However, FR-004 requires searching/filtering articles by tag and/or title, and re-parsing every Markdown file on each search would become slow and fragile as the catalog grows — repeating the same "organic growth" navigation problem this project exists to avoid (see Problem Statement, Risks & Unknowns).

## Decision

A local SQLite database will index article metadata (title, tags, media type, file path) to support fast search/filter. The Markdown files remain the sole source of truth for article content; the SQLite index is treated as a derived, disposable cache that can always be rebuilt by re-scanning the Markdown files' front-matter.

## Consequences

### Positive
- Search/filter (FR-004) stays fast even as the catalog grows, without sacrificing the plain-text/git-friendly storage model from ADR-001.
- Because the index is rebuildable, corruption or loss of the SQLite file is not a data-loss event — the Markdown files are all that need to be backed up/versioned (see Delivery Plan §5 risk mitigation).
- Keeps a clean separation of concerns: storage layer (durability, portability) vs. index layer (queryability).

### Negative
- Introduces a second component (SQLite) that must be kept in sync with the Markdown files on every add/edit/delete (Phase 2 HLD data flow steps 1 and 4) — a sync bug could cause the index to drift from the files.
- Adds a rebuild step as an operational necessity (e.g., after manually editing Markdown files outside the app, or after git-pulling changes from another machine).

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| Flat-file only, no DB (grep/frontmatter parsing per query) | No second component to keep in sync; fully stateless | Re-parses every file on every search; slow and fragile as the catalog grows | Reproduces the exact "organic growth" navigation problem this project exists to avoid |
| SQLite as source of truth (store article body in DB, not files) | Single component, no sync problem | Loses plain-text/git-friendly/diffable properties required by ADR-001 and NFR-001 | Directly conflicts with the already-accepted ADR-001 |

## Links
- Related requirements: FR-002, FR-003, FR-004, FR-007, NFR-001
- Related design docs: `docs/02-planning/High-Level-Design.md`, `docs/01-requirements/Requirements.md`
- PRs/issues: N/A

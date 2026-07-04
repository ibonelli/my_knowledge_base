# Requirements — Article Catalog System

## 1) Goal
- The system shall let a single user add, catalog, and retrieve articles of three media types (written, graphic, video), each with structured metadata and a Markdown body, so previously added content can be found again by tag or title.

## 2) Personas / Users
- Sole user (Ignacio): adds, browses, and searches articles. Also the business owner and technical owner (personal project).

## 3) Functional Requirements
> Use MUST/SHOULD language and stable IDs.

- **FR-001:** The system MUST allow adding a new article with title, summary, tags, online references, Markdown body, and optional images.
- **FR-002:** The system MUST support at least 3 media types: written, graphic, video.
- **FR-003:** The system MUST allow listing/browsing all articles in the catalog.
- **FR-004:** The system MUST allow searching/filtering articles by tag and/or title.
- **FR-005:** The system SHOULD allow editing an existing article's metadata or body.
- **FR-006:** The system SHOULD allow deleting an article from the catalog.
- **FR-007:** The system MUST allow backfilling old articles, not just newly published ones.
- **FR-008:** The system MUST provide a PyQt6 desktop GUI with feature parity to the CLI: add, edit, delete, list, search/filter, and reindex.
- **FR-009:** The GUI MUST let the user edit an article's Markdown body via a split-pane editor with a live rendered preview.
- **FR-010:** The GUI MUST display inline thumbnail previews of images referenced by an article (cover image / embedded images).
- **FR-011:** The GUI MUST use a single-window, master-detail layout (article list/search on one side, selected article's detail/edit view on the other).

## 4) Non-Functional Requirements (NFRs)
- **NFR-001 (Portability):** Article data SHOULD remain plain-text/git-friendly and portable, consistent with ADR-001.
- **NFR-002 (Availability):** Best-effort — no formal SLA (personal project, single user).
- **NFR-003 (Security):** No formal authentication/authorization requirements — single user, no concurrent access.
- **NFR-004 (Consistency):** The CLI and GUI MUST share a single core module for validation and storage/index orchestration, so business logic (tag normalization, media-type validation, keeping the Markdown store and SQLite index in sync) is implemented once, not duplicated per interface.
- **NFR-005 (Dependency footprint):** PyQt6 MUST be a required dependency of the package. This explicitly supersedes the "minimize dependencies" default noted in Implementation Notes — the GUI is a first-class interface, not an optional add-on.

## 5) Data Requirements
- Data elements: title, summary, tags (list), online references/links (list), Markdown body, optional embedded images, media type (written/graphic/video)
- Retention: indefinite; manual delete only (see FR-006)
- PII classification: Not applicable — no personal data expected

## 6) Integration Requirements
- Skipped (personal project mode) — no external system integration identified in Phase 0. Revisit if a future need arises.

## 7) Acceptance Criteria
- **AC-001:** An article of any of the 3 supported media types can be added with full metadata (title, summary, tags, references, Markdown body, optional images). Traces to FR-001, FR-002; Phase 0 Success Metric 1.
- **AC-002:** A previously added article can be found again via tag and/or title lookup. Traces to FR-004; Phase 0 Success Metric 2.
- **AC-003:** An old article can be backfilled (with a past publication date) without breaking retrieval. Traces to FR-007.
- **AC-004:** Every operation available in the CLI (add, edit, delete, list, search, reindex) is achievable via the GUI and produces identical results in the Markdown files and SQLite index. Traces to FR-008, NFR-004.
- **AC-005:** Editing an article's Markdown body in the GUI updates a live rendered preview pane as the text changes. Traces to FR-009.
- **AC-006:** An article with an image reference (cover image or embedded image) shows a thumbnail preview in the GUI detail view. Traces to FR-010.

## 8) Open Questions
- **Q-001:** Do "graphic" and "video" articles need different storage/rendering handling than written ones, or just different metadata?
- **Q-002:** Should this system integrate with or replace the existing knowledge-base Markdown notes, or remain a separate, parallel system?
- **Q-003:** What tagging/organization model will avoid repeating the "organic growth" navigation problem seen in `AI_New_Links_ReDesignProposal.md`?

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

## 4) Non-Functional Requirements (NFRs)
- **NFR-001 (Portability):** Article data SHOULD remain plain-text/git-friendly and portable, consistent with ADR-001.
- **NFR-002 (Availability):** Best-effort — no formal SLA (personal project, single user).
- **NFR-003 (Security):** No formal authentication/authorization requirements — single user, no concurrent access.

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

## 8) Open Questions
- **Q-001:** Do "graphic" and "video" articles need different storage/rendering handling than written ones, or just different metadata?
- **Q-002:** Should this system integrate with or replace the existing knowledge-base Markdown notes, or remain a separate, parallel system?
- **Q-003:** What tagging/organization model will avoid repeating the "organic growth" navigation problem seen in `AI_New_Links_ReDesignProposal.md`?

# Delivery Plan — Article Catalog System

## 1) Scope recap
- In scope: Add, browse, search, edit, delete articles across 3 media types (written, graphic, video); backfill old articles. Same as Phase 0/1 — no changes.
- Out of scope: None defined yet — intentionally left open for v1 (per Phase 0).

## 2) Milestones
| Milestone | Deliverable | Owner | Target date |
|---|---|---|---|
| M1: Data model & storage | SQLite schema + Markdown file storage wired up | You (sole developer) | TBD |
| M2: Article CRUD | Epic 1 complete (add/edit/delete) | You (sole developer) | TBD |
| M3: Browse & Search | Epic 2 complete (list, tag/title search) | You (sole developer) | TBD |
| M4: Multi-media & backfill | Epic 3 complete (3 media types, backfill) | You (sole developer) | TBD |
| M5: v1 done | Definition of Done met, Phase 6 docs written | You (sole developer) | TBD |

## 3) Work Breakdown (Epics → Stories)
- **Epic 1: Article CRUD** (FR-001, FR-005, FR-006)
  - Story 1.1: Add article with full metadata (FR-001)
  - Story 1.2: Edit an existing article (FR-005)
  - Story 1.3: Delete an article (FR-006)
- **Epic 2: Catalog Browsing & Search** (FR-003, FR-004)
  - Story 2.1: List/browse all articles (FR-003)
  - Story 2.2: Search/filter articles by tag and/or title (FR-004)
- **Epic 3: Multi-media & Backfill support** (FR-002, FR-007)
  - Story 3.1: Support written, graphic, and video media types (FR-002)
  - Story 3.2: Backfill old articles with historical metadata (FR-007)

## 4) Dependencies
- External teams: None (personal project)
- Vendors: None
- Environments: Local development machine only — no external hosting/deployment target identified
- Approvals: N/A (sole developer)

## 5) Risks & Mitigations
- **Risk:** Data loss — no backup strategy for the SQLite index or Markdown files.
  **Mitigation:** Git-track all Markdown article files (diffable, versioned); periodically export/back up the SQLite database (e.g., `.sql` dump committed to repo or scheduled file copy).
- **Risk:** Tag/organization sprawl — repeats the "organic growth" navigation problem already seen in `AI_New_Links_ReDesignProposal.md`.
  **Mitigation:** Define a lightweight, controlled tag vocabulary/taxonomy before bulk-backfilling old articles, rather than letting tags emerge ad hoc.

## 6) Rollout strategy
- Feature flags: None needed (personal project mode — direct deploy default)
- Phased rollout: N/A — single user, direct use once built
- Rollback plan: Revert via git (Markdown files) and restore from the most recent SQLite backup if the index becomes corrupted

## 7) Definition of Done (DoD)
- [ ] Code implements FR-001 through FR-007
- [ ] Manual or automated checks confirm AC-001, AC-002, AC-003
- [ ] App runs locally end-to-end
- [ ] Phase 6 documentation (System Overview, Onboarding) written

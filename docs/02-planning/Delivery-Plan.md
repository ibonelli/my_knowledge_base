# Delivery Plan — Article Catalog System

## 1) Scope recap
- In scope: Add, browse, search, edit, delete articles across 3 media types (written, graphic, video); backfill old articles; a PyQt6 desktop GUI with full feature parity to the CLI.
- Out of scope: None defined yet — intentionally left open for v1 (per Phase 0).

## 2) Milestones
| Milestone | Deliverable | Owner | Target date |
|---|---|---|---|
| M1: Data model & storage | SQLite schema + Markdown file storage wired up | You (sole developer) | TBD |
| M2: Article CRUD | Epic 1 complete (add/edit/delete) | You (sole developer) | TBD |
| M3: Browse & Search | Epic 2 complete (list, tag/title search) | You (sole developer) | TBD |
| M4: Multi-media & backfill | Epic 3 complete (3 media types, backfill) | You (sole developer) | TBD |
| M5: v1 done (CLI) | Definition of Done met, Phase 6 docs written | You (sole developer) | Done |
| M6: Desktop GUI | Epic 4 complete (PyQt6 GUI, full CLI parity) | You (sole developer) | TBD |

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
- **Epic 4: Desktop GUI** (FR-008, FR-009, FR-010, FR-011, NFR-004, NFR-005)
  - Story 4.1: Extract a shared core module from `cli.py` (validation, storage/index orchestration) so CLI and GUI both call it (NFR-004, prerequisite for the rest of this epic)
  - Story 4.2: Master-detail main window — article list/search pane + detail pane (FR-008, FR-011)
  - Story 4.3: Add/edit article view with split-pane Markdown editor + live preview (FR-008, FR-009)
  - Story 4.4: Inline image thumbnail preview in the detail view (FR-010)
  - Story 4.5: Delete confirmation and reindex action in the GUI (FR-008)

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
- **Risk:** CLI and GUI drift apart — a validation rule or sync fix applied to one interface but not the other, causing inconsistent behavior between them.
  **Mitigation:** Shared core module (Story 4.1, C-007, NFR-004) — both interfaces call the same functions, so there is only one place to fix.

## 6) Rollout strategy
- Feature flags: None needed (personal project mode — direct deploy default)
- Phased rollout: N/A — single user, direct use once built
- Rollback plan: Revert via git (Markdown files) and restore from the most recent SQLite backup if the index becomes corrupted

## 7) Definition of Done (DoD)
- [x] Code implements FR-001 through FR-007 (CLI v1)
- [x] Manual or automated checks confirm AC-001, AC-002, AC-003
- [x] CLI runs locally end-to-end
- [x] Phase 6 documentation (System Overview, Onboarding) written for CLI v1
- [ ] Code implements FR-008 through FR-011 (GUI)
- [ ] Manual or automated checks confirm AC-004, AC-005, AC-006
- [ ] GUI runs locally end-to-end, sharing the core module with the CLI (NFR-004)
- [ ] Phase 6 documentation (System Overview, Onboarding) updated to cover the GUI

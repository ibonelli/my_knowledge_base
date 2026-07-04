# Constraints Register — Article Catalog System

## Purpose
List constraints that are non-negotiable. This is a primary AI context document.

## Constraints
- **C-001 (Format):** Article body content MUST be stored as Markdown text (per ADR-001), with images embedded via standard Markdown image syntax or references to locally/externally stored files.
- **C-002 (Media types):** The system MUST support at least 3 media types: written, graphic, video.
- **C-003 (Scale):** The system MUST support single-user, no-concurrency access only.
- **C-004 (Compliance):** No compliance requirements apply (personal project).
- **C-005 (Budget):** The system MUST fit within personal time only — no financial budget or fixed deadline.
- **C-006 (GUI framework):** The desktop GUI MUST be built with PyQt6 (per ADR-003). PyQt6 is a required dependency, not optional.
- **C-007 (Shared core):** The CLI and GUI MUST both call a shared core module for validation and storage/index orchestration rather than each implementing that logic independently (per NFR-004, ADR-003).

## Forbidden Solutions (Explicit)
- **F-001:** Do NOT store article bodies as HTML, rich-text binary format (e.g. Word, Notion export), or a database blob (per ADR-001).
- **F-002:** Do NOT introduce multi-user authentication/authorization complexity — not needed under the single-user constraint (C-003).
- **F-003:** Do NOT duplicate article validation/orchestration logic (tag normalization, media-type checks, Markdown/SQLite sync) separately inside the GUI layer — it MUST reuse the shared core module (C-007).

## Notes / Rationale
- C-001 and F-001 derive directly from ADR-001 (Markdown as canonical article format).
- C-002 through C-005 derive from the Problem Statement's "Constraints (Known)" section (`docs/00-scoping/Problem-Statement.md`).
- F-002 is a YAGNI guardrail: the Problem Statement explicitly assumes single user, no concurrent access, no external integrations at this stage.
- C-006 and C-007 derive from ADR-003 (PyQt6 GUI with a shared core module) and directly informed FR-008–FR-011, NFR-004, NFR-005 in Requirements.
- C-006 is a deliberate exception to the "minimize dependencies" default used when the CLI was first built (see Implementation Notes) — accepted because the GUI is now a first-class interface, not optional tooling.

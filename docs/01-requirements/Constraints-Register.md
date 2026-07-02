# Constraints Register — Article Catalog System

## Purpose
List constraints that are non-negotiable. This is a primary AI context document.

## Constraints
- **C-001 (Format):** Article body content MUST be stored as Markdown text (per ADR-001), with images embedded via standard Markdown image syntax or references to locally/externally stored files.
- **C-002 (Media types):** The system MUST support at least 3 media types: written, graphic, video.
- **C-003 (Scale):** The system MUST support single-user, no-concurrency access only.
- **C-004 (Compliance):** No compliance requirements apply (personal project).
- **C-005 (Budget):** The system MUST fit within personal time only — no financial budget or fixed deadline.

## Forbidden Solutions (Explicit)
- **F-001:** Do NOT store article bodies as HTML, rich-text binary format (e.g. Word, Notion export), or a database blob (per ADR-001).
- **F-002:** Do NOT introduce multi-user authentication/authorization complexity — not needed under the single-user constraint (C-003).

## Notes / Rationale
- C-001 and F-001 derive directly from ADR-001 (Markdown as canonical article format).
- C-002 through C-005 derive from the Problem Statement's "Constraints (Known)" section (`docs/00-scoping/Problem-Statement.md`).
- F-002 is a YAGNI guardrail: the Problem Statement explicitly assumes single user, no concurrent access, no external integrations at this stage.

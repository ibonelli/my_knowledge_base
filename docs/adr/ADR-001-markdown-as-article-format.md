# ADR-001: Markdown as the canonical article body format

- **Status:** Accepted
- **Date:** 2026-07-02
- **Owners:** Ignacio (sole developer)

## Context

The Article Catalog System needs to store the body of articles sourced from different media (written, graphic, video) and different outlets, old and new. The storage format for the article body needs to be simple, portable, diffable, and consistent with how the rest of this knowledge base is already maintained (existing notes such as `AI_New_Links_ReDesignProposal.md` are already Markdown).

## Decision

Article bodies will be stored as Markdown text, with images embedded via standard Markdown image syntax (or references to locally/externally stored image files) rather than as HTML, a rich-text binary format, or a database blob.

## Consequences

### Positive
- Plain-text, diffable, git-friendly — fits the existing knowledge-base workflow
- Portable across tools/editors, no vendor lock-in
- Easy to render to HTML later if a viewer/UI is built
- Consistent with existing content in this repository

### Negative
- Markdown has limited native support for complex layouts or rich embedded video — video articles will likely need to store a reference/link/embed rather than the video content itself
- Some semantic structure (e.g., distinguishing a "graphic article" from a "written article" precisely) has to be carried in metadata rather than the format itself

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| HTML | Rich formatting, native embeds | Harder to hand-edit, less diff-friendly, inconsistent with existing notes | Adds complexity not needed for a personal catalog |
| Rich-text / binary (e.g. Word, Notion export) | WYSIWYG editing | Not git-friendly, not portable, hard to diff or script against | Breaks the plain-text philosophy of this knowledge base |
| Database blob / structured fields only (no free text) | Fully queryable | Loses the free-form long-form writing that articles need | Doesn't fit "article" as a concept — need full body text |

## Links
- Related requirements: TBD in Phase 1 (Requirements)
- Related design docs: `docs/00-scoping/Problem-Statement.md`
- PRs/issues: N/A

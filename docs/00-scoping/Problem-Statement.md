# Problem Statement — Article Catalog System

## 1) Summary (TL;DR)
- **Problem:** There is no system to store, catalog, and integrate published articles of different media types (written, graphic, video), sourced from different outlets and time periods, into one browsable collection.
- **Impact:** The sole developer/user (Ignacio) currently has no reliable way to accumulate and later retrieve articles of interest — content risks being scattered or lost, similar to the "organic growth" navigation problem already observed in the AI knowledge-base notes (see `AI_New_Links_ReDesignProposal.md`).
- **Proposed outcome:** A working system where articles (new or old, from any medium) can be added with structured metadata (title, summary, tags, online references, Markdown body, optional images) and reliably retrieved later.

## 2) Background / Context
- **Current state:** No cataloging system exists yet. Article-like content today lives informally in notes (e.g. `AI_New_Links_ReDesignProposal.md`) that has already been flagged as hard to navigate once it grows organically.
- **Why now:** The pain of unstructured, un-tagged accumulation of links/content has already been felt once (see the AI-notes redesign discussion) and is being addressed proactively before it repeats for articles.
- **Stakeholders:**
  - Business owner: Sole developer (you) — personal project mode
  - Technical owner: Sole developer (you)
  - Users: Sole developer (you)

## 3) Scope

### In Scope
- Cataloging articles of different types/media: written, graphic (image-based), and video
- Integrating new articles as well as backfilling old articles from various sources/outlets
- Storing per article: title, summary, tags, online references (links), the article body itself in Markdown, and optionally embedded images

### Out of Scope
- None defined yet — scope is intentionally left open for v1; exclusions will be decided as the project progresses rather than pre-emptively restricted.

## 4) Success Criteria (Measurable)
- [ ] Metric 1: An article of any of the 3 supported media types can be added to the catalog with full metadata (title, summary, tags, references, Markdown body, optional images)
- [ ] Metric 2: A previously added article can be found again via tag and/or title lookup

## 5) Constraints (Known)
- Compliance: None (personal project)
- Security: None specified — single user, no auth requirements identified yet
- Availability: Best-effort — no formal SLA (personal project)
- Budget / timeline: Personal time only, no financial budget or fixed deadline
- Tech constraints: Content must support Markdown as the article body format, with optional embedded images; must accommodate at least 3 media types (written, graphic, video)

## 6) Risks & Unknowns
- **Risk:** Without a clear tagging/organization model from the start, this could repeat the "organic growth" navigation problem already seen in `AI_New_Links_ReDesignProposal.md` (unbounded lists, lost context on why an item was saved).
- **Unknown:** Whether "graphic" and "video" articles need different storage/rendering handling than written ones, or just different metadata (e.g. embed vs. link).
- **Unknown:** Whether this system needs to integrate with or replace the existing knowledge-base Markdown notes, or is a separate, parallel system.
- **Assumption:** Single user, no concurrent access, no external integrations required at this stage.

## 7) Decision Needed
- Approve / reject / revise scope
- Target date for decision: N/A (personal project, no formal gate)

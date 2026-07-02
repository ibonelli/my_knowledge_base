# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is Ignacio's personal knowledge base — currently **markdown/documentation only, no application source code**. There are no build, lint, or test commands because nothing here compiles or runs. Two things live side by side here:

1. **Freeform notes** (e.g. `AI_New_Links_ReDesignProposal.md`) — organically-grown reference material on AI/LLM topics.
2. **An SDLC-managed project**, currently "Article Catalog System" (seeded by `KickOff.txt`), being scoped/planned/built using the custom `sdlc` skill below.

## The `sdlc` skill (`.claude/skills/sdlc/`)

This repo is also the home of a custom Claude Code skill that drives a 7-phase, AI-assisted SDLC. Understanding its architecture matters because it governs how `docs/` gets populated:

- **Entry point:** `.claude/skills/sdlc/SKILL.md` — scans `docs/` to detect progress across phases, then routes to a phase sub-skill. It never does the phase work itself.
- **Phase sub-skills:** `.claude/skills/sdlc/phase-{0-6}-*/SKILL.md` — each is self-contained (scoping → requirements → planning → architecture → execution → testing → documentation), and each ends by returning to the entry SKILL.md for an ADR check + next-phase offer.
- **`references/`** — shared, phase-agnostic resources loaded by sub-skills on demand:
  - `templates.md` — the markdown template for every artifact in every phase
  - `artifact-chain.md` — cross-phase validation rules (e.g. every FR-xxx must trace to a test case); surfaced as warnings, never blocking
  - `personal-project-preset.md` — solo-developer defaults (no stakeholders/compliance/SLA questions) applied when "personal project mode" is active
  - `adr-template.md` — template + trigger conditions for Architecture Decision Records
- **Two composable modes** exist and can be combined: *auto-fill* (propose answers from repo evidence, user confirms/corrects) and *personal project* (skip team/compliance questions, pre-fill solo defaults). Every phase sub-skill must respect whichever mode(s) are active.
- **Mandatory stopping points**: progress detection, end of each phase (before writing files), and the post-phase ADR check. Don't skip these — the design intentionally treats the AI as producing drafts a human approves, not autonomous output.

## `docs/` folder convention

Fixed structure, one folder per phase, created by Phase 0 if absent:
```
docs/00-scoping/  01-requirements/  02-planning/  03-architecture-data/
docs/04-execution/  05-testing/  06-documentation/  docs/adr/
```
ADRs are numbered sequentially: `docs/adr/ADR-NNN-<short-title>.md`, regardless of which phase triggered them.

## Current project state

"Article Catalog System" has completed **Phase 0 (Scoping)** only:
- `docs/00-scoping/Problem-Statement.md`, `docs/00-scoping/Stakeholder-Map.md`
- `docs/adr/ADR-001-markdown-as-article-format.md` — articles are stored as Markdown, not HTML/rich-text/DB blobs

No code has been generated for this project yet (Phase 4 is where implementation would happen). Note: `.claude/plans/code_creation.md` and other files under `.claude/plans/` describe a *different*, unrelated past project ("pelis-feed" / RSS movie feed) — that code does not exist in this repository and should not be treated as current state.

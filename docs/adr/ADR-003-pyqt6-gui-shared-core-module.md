# ADR-003: PyQt6 desktop GUI as a second interface, with a shared core module

- **Status:** Accepted
- **Date:** 2026-07-03
- **Owners:** Ignacio (sole developer)

## Context

The Article Catalog System shipped as a CLI-only tool (v1: FR-001–FR-007), with `article_catalog/cli.py` mixing argparse wiring together with the actual validation and storage/index orchestration logic. The original High-Level Design explicitly deferred the choice of interface form ("CLI or minimal local UI... exact form deferred to Phase 3/4"). A desktop GUI is now wanted, with full feature parity to the CLI, so that the catalog can be operated visually rather than only from the command line.

Adding a second interface raises two decisions: which GUI framework to use, and how to avoid re-implementing (and potentially diverging from) the CLI's validation and sync logic in a second place.

## Decision

Build the GUI with PyQt6, targeting full feature parity with the CLI (add/edit/delete/list/search/reindex), using a single-window master-detail layout with a split-pane Markdown editor (live preview via `QTextEdit.setMarkdown()`) and inline image thumbnails. Extract the validation and storage/index orchestration logic currently embedded in `cli.py` into a shared core module; both the CLI and the GUI call this core module exclusively and never talk to `storage.py`/`index.py` directly. PyQt6 becomes a required (not optional) dependency of the package.

## Consequences

### Positive
- Single implementation of validation and Markdown/SQLite sync (NFR-004, C-007) — a fix or rule change made once applies to both interfaces, removing the risk of CLI/GUI behavioral drift.
- PyQt6 targets current Qt6, is actively maintained, and its `QTextEdit.setMarkdown()` gives live Markdown preview without pulling in a heavier dependency like `PyQtWebEngine`.
- Master-detail single-window layout is a standard, low-complexity desktop pattern appropriate for a solo-user tool.

### Negative
- Requires an upfront refactor of `cli.py` (Story 4.1) before any GUI feature work can start — short-term velocity cost.
- PyQt6 as a required dependency increases install footprint for anyone (including future-you, on a fresh machine) who only ever wants the CLI — a deliberate exception to the "minimize dependencies" principle the CLI was originally built under (see Implementation Notes).
- Introduces a GUI event loop and threading model consideration later if any operation becomes slow enough to need to move off the UI thread (not expected at current/expected catalog scale, per Architecture Overview §4 Scaling).

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| PyQt5 | Mature, widely documented | Targets an older Qt version; no reason to start a new component on the older binding | No compatibility constraint forces Qt5; PyQt6 is the current default |
| Tkinter (stdlib) | No extra dependency at all | Dated widget set, weaker Markdown/rich-text support, no built-in Markdown rendering | Would need extra libraries anyway for live Markdown preview, undermining the "no extra dependency" advantage |
| Web UI (local Flask/FastAPI + browser) | Familiar web stack, easy styling | Introduces a local server process, a new trust boundary, and a framework family unrelated to "desktop GUI" as requested | Explicitly out of scope — user asked for a PyQt desktop GUI |
| GUI duplicates CLI logic independently (no shared core module) | No upfront refactor needed | Two places implementing tag normalization, media-type validation, and Markdown/SQLite sync — drift risk on every future change | Directly conflicts with NFR-004/C-007; rejected in favor of the shared core module |

## Links
- Related requirements: FR-008, FR-009, FR-010, FR-011, NFR-004, NFR-005
- Related design docs: `docs/02-planning/High-Level-Design.md`, `docs/03-architecture-data/Architecture-Overview.md`, `docs/02-planning/Delivery-Plan.md` (Epic 4)
- PRs/issues: N/A

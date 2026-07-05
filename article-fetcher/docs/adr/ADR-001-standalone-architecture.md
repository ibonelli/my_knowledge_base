# ADR-001: Standalone architecture — separate venv, no shared code with article_catalog

- **Status:** Accepted
- **Date:** 2026-07-04
- **Owners:** Ignacio (sole developer)

## Context

article-fetcher's output (a front-matter Markdown file) is schema-compatible with the sibling Article Catalog System project in the same repository, and it would be technically easy to import `article_catalog.core`/`storage`/`index` directly and write straight into `articles/`/`catalog.db`. The user explicitly decided against that during planning: this tool must stay standalone, decoupled from `article_catalog`'s code, kept as a sibling project rather than a new subcommand of the existing `article` CLI.

## Decision

`article-fetcher` lives in its own top-level directory with its own `pyproject.toml` and its own virtualenv, entirely separate from the root project's. It does not import `article_catalog.core`, `storage`, or `index` — the small amount of shared vocabulary (`MEDIA_TYPES`) is duplicated locally in `frontmatter.py` rather than imported. Output front-matter uses the same field names as `article_catalog`'s schema so a file can optionally be copied into `articles/` and reindexed by hand, but the tool itself never performs that write.

## Consequences

### Positive
- The "no calls into article_catalog's IO" rule becomes structurally true, not just a convention to remember: `article_catalog.core` isn't even installed in article-fetcher's venv, so nothing can accidentally import it.
- Keeps dependency footprints separate — `article_catalog` needs PyQt6; article-fetcher needs `trafilatura`/`playwright`. Neither install is bloated by the other's unrelated dependencies.
- The user retains full manual control over whether/when a fetched article actually enters the catalog (via `article reindex` after copying the file) — no silent, automatic catalog mutation from a tool whose extraction quality can vary.

### Negative
- Two separate `.venv` directories to create and maintain on a fresh machine, rather than one.
- The `MEDIA_TYPES` constant is duplicated in two places; if the Article Catalog System's valid media types ever change, this file needs a matching manual update (mitigated by it being a 3-value literal that rarely changes).

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| New `article import <url>` subcommand of the existing CLI, calling `core.add_article` directly | Single install, single venv, immediate catalog integration | Couples an extraction tool of variable quality directly to the catalog's source of truth; violates the explicit "standalone" decision | User explicitly wants this decoupled and reviewed before anything touches the catalog |
| Import `article_catalog.models` via a `sys.path` shim to avoid duplicating `MEDIA_TYPES` | Avoids duplicating a constant | Fragile path arithmetic tied to directory depth; blurs the "fully standalone" boundary for a one-line saving | Simplicity and honesty of the standalone boundary won out over avoiding a 3-value duplication |
| Share the root project's `pyproject.toml`/venv, just as additional dependencies | Only one venv to maintain | Bloats the root project's install with `trafilatura`/`playwright`/Chromium for anyone who only wants the CLI or GUI; weakens the standalone guarantee to "please don't import it" rather than "can't import it" | Rejected in favor of structural isolation |

## Links
- Related requirements: NFR-001, NFR-002; Constraints C-001, C-002, C-003, C-005
- Related design docs: `docs/00-scoping/Problem-Statement.md`, `docs/02-planning/High-Level-Design.md` (Option D)
- PRs/issues: N/A

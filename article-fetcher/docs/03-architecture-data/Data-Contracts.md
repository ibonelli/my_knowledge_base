# Data Contracts — article-fetcher

## 1) Entities / Events

- **ExtractedArticle**
  - Definition: In-memory result of the extraction pipeline (`title`, `body_markdown`, `published_date`, `author`, `sitename`, `word_count`, `used_fallback`). Never persisted directly — consumed by `cli.py` to build the on-disk front-matter file.
  - Owner: Sole developer (you)
  - Versioning: v1 — internal data shape only, not a stored schema.

- **Front-matter Markdown file** (the persisted artifact)
  - Definition: A single `.md` file with YAML front-matter + Markdown body, written under `--output-dir`. Field names and order intentionally match the Article Catalog System's schema (C-002), even though the code that writes it is fully decoupled.
  - Owner: Sole developer (you)
  - Versioning: v1 — no schema versioning process yet; matches the root project's own "handled ad hoc" stance given the same single-developer, single-environment scope.

## 2) Schema (JSON examples)

### Front-matter file — v1
```json
{
  "id": "0b7ade0f",
  "title": "Local-first software - Wikipedia",
  "summary": "",
  "media_type": "written",
  "tags": ["test"],
  "references": ["https://en.wikipedia.org/wiki/Local-first_software"],
  "images": [],
  "published_date": "2026-02-16",
  "created_at": "2026-07-04"
}
```
(Followed by the Markdown body below the closing `---`.)

### ExtractedArticle — v1 (in-memory only)
```json
{
  "title": "Local-first software - Wikipedia",
  "body_markdown": "# Local-first software\n\n...",
  "published_date": "2026-02-16",
  "author": null,
  "sitename": "en.wikipedia.org",
  "word_count": 988,
  "used_fallback": false
}
```

## 3) Validation Rules
- `title` MUST be present and non-empty after stripping whitespace (falls back to the source URL itself if extraction found no title, before the user gets a chance to edit it).
- `media_type` MUST be one of `written`, `graphic`, `video` (same set as the Article Catalog System's `MEDIA_TYPES`, duplicated locally per C-001).
- `summary` is ALWAYS an empty string at write time (C-004) — never computed by this tool.
- `references` always contains the source URL as its one entry at draft time; the user MAY add more via manual edit in `$EDITOR`.
- `images` is ALWAYS an empty list in v1 — no image extraction/downloading is implemented.
- `published_date` prefers the date extracted from the page's own metadata (normalized to `YYYY-MM-DD`); falls back to today's date if extraction found none or it failed to parse.
- `created_at` is always today's date at run time.
- Validation runs a second time on the user's *edited* text (after `$EDITOR` closes), not just on the initial draft — an edit that breaks the title or media type is rejected before anything is written (FR-007).

## 4) Compatibility rules
- Backward compatibility: No formal policy — personal project, single developer, single environment (personal project mode).
- Field-name compatibility with the Article Catalog System's schema (C-002) is the one compatibility rule that IS enforced deliberately, so output files can be copied into `articles/` and reindexed there without transformation, if the user chooses to.
- Deprecation policy: N/A for v1.

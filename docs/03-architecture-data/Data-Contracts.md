# Data Contracts — Article Catalog System

## 1) Entities / Events

- **Article**
  - Definition: A single cataloged article — Markdown file (source of truth) plus a matching row in the SQLite index (per ADR-002).
  - Owner: Sole developer (you)
  - Versioning: v1 — no schema versioning process yet; changes will be handled ad hoc given single-developer, single-environment scope.

- **Tag**
  - Definition: A normalized label attached to one or more articles, used for filtering (FR-004).
  - Owner: Sole developer (you)
  - Versioning: v1

- **ArticleTag** (join)
  - Definition: Many-to-many association between Article and Tag.
  - Owner: Sole developer (you)
  - Versioning: v1

## 2) Schema (JSON examples)

### Article — Markdown front-matter (v1)
```yaml
---
id: "a1b2c3"
title: "Example Article Title"
summary: "One or two sentence summary."
media_type: "written"   # one of: written | graphic | video
tags: ["ai", "productivity"]
references:
  - "https://example.com/source-article"
images:
  - "images/a1b2c3-cover.png"
published_date: "2024-03-10"   # historical date for backfilled articles
created_at: "2026-07-02"       # date added to the catalog
---

Article body in Markdown goes here...
```

### Article — SQLite index row (v1)
```json
{
  "id": "a1b2c3",
  "title": "Example Article Title",
  "summary": "One or two sentence summary.",
  "media_type": "written",
  "file_path": "articles/a1b2c3.md",
  "published_date": "2024-03-10",
  "created_at": "2026-07-02"
}
```

### Tag (v1)
```json
{
  "id": 1,
  "name": "ai"
}
```

### ArticleTag (v1)
```json
{
  "article_id": "a1b2c3",
  "tag_id": 1
}
```

## 3) Validation Rules
- Title MUST be present and non-empty.
- Media type MUST be one of: `written`, `graphic`, `video` (FR-002).
- Summary and references MAY be left blank (e.g. quick backfills where they aren't available yet).
- Tags MAY be empty, but when present MUST be normalized (trimmed, lowercased) before being written to the Tag table, to avoid duplicate tags differing only by casing/whitespace (mitigates the tag-sprawl risk noted in the Delivery Plan).
- `references`, when present, SHOULD be well-formed URLs.
- `published_date` is optional; if absent, defaults to `created_at` (the date the article was added).
- `file_path` in the SQLite index MUST point to an existing Markdown file under `articles/`; the CLI is responsible for keeping this in sync on add/edit/delete (ADR-002).

## 4) Compatibility rules
- Backward compatibility: No formal policy — personal project, single developer, single environment (per personal project mode).
- Deprecation policy: N/A for v1.

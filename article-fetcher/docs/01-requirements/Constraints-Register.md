# Constraints Register — article-fetcher

## Purpose
List constraints that are non-negotiable. This is a primary AI context document.

## Constraints
- **C-001 (Isolation):** The tool MUST NOT import or call into `article_catalog`'s `core`, `storage`, or `index` modules.
- **C-002 (Schema compatibility):** Output front-matter field names MUST match the Article Catalog System's schema (`id, title, summary, media_type, tags, references, images, published_date, created_at`).
- **C-003 (Separate environment):** The tool MUST use its own virtualenv and `pyproject.toml`, separate from the root project's — no shared install.
- **C-004 (No auto-summarization):** The tool MUST NOT compute or write an automated summary; the `summary` field is always left blank at write time.
- **C-005 (No auto-catalog-write):** The tool MUST NOT write into the root project's `articles/` directory or `catalog.db` under any circumstance.
- **C-006 (Manual install step):** Users MUST run `playwright install chromium` once after installing dependencies — this cannot be automated via `pip` alone.
- **C-007 (Scale):** The tool MUST support single-user, single-URL-at-a-time operation only; no concurrency requirements.

## Forbidden Solutions (Explicit)
- **F-001:** Do NOT import `article_catalog.core`, `article_catalog.storage`, or `article_catalog.index` — duplicate the small amount of shared logic (id generation, front-matter shape) locally instead.
- **F-002:** Do NOT write the output file without going through the preview-edit-confirm flow, unless the user explicitly passed `--yes`.
- **F-003:** Do NOT swallow fetch/render/extraction errors silently — always surface a clear error message and a non-zero exit code.

## Notes / Rationale
- C-001, C-002, C-003, C-005 derive directly from the decision (made during planning) to keep this tool fully standalone from the Article Catalog System, while staying output-compatible with it — see `docs/00-scoping/Problem-Statement.md` §5 and §3 Out of Scope.
- C-004 derives from the explicit decision to drop automated summarization from this tool's scope entirely.
- C-006 is a real operational gotcha: skipping it doesn't break the common case (most static articles never need the fallback), but the Playwright fallback fails with a confusing runtime error the first time it's needed if this step was skipped.
- F-002 exists because the whole point of the preview-edit-confirm UX is to protect against auto-derived metadata (especially title/media type) being wrong.

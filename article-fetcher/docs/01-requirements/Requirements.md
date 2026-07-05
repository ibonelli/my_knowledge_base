# Requirements — article-fetcher

## 1) Goal
- The system shall let a single user fetch a URL, extract and convert its main article content to Markdown, and stage the result as a front-matter file for manual review and editing before it is saved anywhere.

## 2) Personas / Users
- Sole user (Ignacio): runs the tool against URLs of interest to produce Markdown drafts, optionally for later inclusion in the separate Article Catalog System.

## 3) Functional Requirements
> Use MUST/SHOULD language and stable IDs.

- **FR-001:** The system MUST fetch a given URL over HTTP(s) and retrieve its HTML content.
- **FR-002:** The system MUST extract the main article content from the fetched HTML and convert it to Markdown.
- **FR-003:** The system MUST fall back to rendering the page with a headless browser (Playwright) when the initial extraction yields content below a minimum word-count threshold, unless the fallback is explicitly disabled.
- **FR-004:** The system MUST derive article metadata (title, published date if available, source URL as a reference) and build front-matter compatible with the Article Catalog System's schema.
- **FR-005:** The system MUST let the user review and edit the derived front-matter and body in their configured `$EDITOR` before anything is written to disk.
- **FR-006:** The system MUST prompt for a final confirmation before writing the file, unless explicitly skipped via a flag.
- **FR-007:** The system MUST validate the edited front-matter (title present, media type valid) before writing, and reject invalid input with a clear error instead of writing it.
- **FR-008:** The system MUST let the user specify media type, tags, output directory, fetch timeout, and whether to allow the Playwright fallback, via CLI flags.
- **FR-009:** The system MUST NOT write into the Article Catalog System's `articles/` directory or `catalog.db` automatically — output always goes to a separate, tool-owned directory.

## 4) Non-Functional Requirements (NFRs)
- **NFR-001 (Isolation):** The system MUST NOT import or call into `article_catalog`'s `core`, `storage`, or `index` modules — it is architecturally standalone.
- **NFR-002 (Output portability):** Output front-matter MUST use the same field names as the Article Catalog System's schema, so a file can optionally be copied there later, even though the code itself is decoupled.
- **NFR-003 (Resilience):** Network, rendering, and extraction failures MUST produce a clear, actionable error message and a non-zero exit code, not a raw stack trace.
- **NFR-004 (Testability):** Core logic MUST be testable without live network access — the automated test suite uses only a local loopback HTTP server, never a real external site.

## 5) Data Requirements
- Data elements: `id`, `title`, `summary` (always blank at write time), `media_type`, `tags`, `references` (the source URL), `images` (always empty in v1), `published_date`, `created_at`, and the Markdown `body`.
- Retention: files persist under `--output-dir` until the user manually moves, edits, or deletes them; the tool never cleans them up automatically.
- PII classification: Not applicable — the tool fetches public web pages, not personal data.

## 6) Integration Requirements
- The only "integration" is ad-hoc HTTP(S) fetching of arbitrary public URLs the user provides — there is no fixed upstream/downstream contract, no authentication, and no API the tool depends on beyond the target page being publicly reachable.

## 7) Acceptance Criteria
- **AC-001:** Given a real static article URL, running the tool (with confirmation skipped) produces a valid front-matter Markdown file with non-empty body content and the source URL present in `references`. Traces to FR-001, FR-002, FR-004, FR-006; Phase 0 Success Metric 1.
- **AC-002:** Given a URL whose primary fetch yields fewer than the word-count threshold, the tool automatically retries via the Playwright fallback, and the fallback's content is used when it yields more words than the primary fetch. Traces to FR-003; Phase 0 Success Metric 2.
- **AC-003:** Editing the front-matter to have an empty title or an invalid media type causes the tool to reject the save with a clear error rather than writing invalid data. Traces to FR-007.
- **AC-004:** The tool never creates or modifies any file under the root project's `articles/` directory or `catalog.db`, under any CLI flag combination. Traces to FR-009, NFR-001.

## 8) Open Questions
- **Q-001:** Should the word-count fallback threshold (currently a fixed default) be exposed as a CLI flag?
- **Q-002:** Should a future version support batch-processing multiple URLs from a file?
- **Q-003:** Should extracted images ever be downloaded locally in a future version, or is a reference-only approach sufficient long-term?

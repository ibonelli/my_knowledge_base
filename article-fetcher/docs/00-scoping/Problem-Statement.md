# Problem Statement — article-fetcher

## 1) Summary (TL;DR)
- **Problem:** Adding an article to a Markdown-based catalog today means manually copying and reformatting the page content — no automated fetch/convert path exists.
- **Impact:** The sole developer/user (Ignacio) spends manual effort transcribing web articles into Markdown; this friction discourages backfilling content from URLs.
- **Proposed outcome:** A standalone CLI tool that, given a URL, fetches the page, extracts the main article content, converts it to Markdown, and stages it as a front-matter Markdown file for manual review/edit before saving.

## 2) Background / Context
- **Current state:** No such tool exists. `ToDo.md` item 1 explicitly requested it: "I need a CLI tool that I provide a link, it fetches the article, converts it to MarkDown and summarize it." The sibling Article Catalog System project already established a Markdown + YAML front-matter schema (`ADR-001` in the root project) that this tool's output deliberately mirrors, without depending on that project's code.
- **Why now:** Same "organic growth / hard to retrieve" motivation that drove the Article Catalog System, but specifically targeting the friction of manually transcribing web articles.
- **Stakeholders:**
  - Business owner: Sole developer (you) — personal project mode
  - Technical owner: Sole developer (you)
  - Users: Sole developer (you)

## 3) Scope

### In Scope
- Fetching a single URL over HTTP(s)
- Extracting the main article content and converting it to Markdown
- Falling back to a headless-browser render for JS-rendered/SPA pages that yield too little content on a plain fetch
- Staging the result as a front-matter Markdown file (schema-compatible with the Article Catalog System) for manual review/edit/confirm before anything is written

### Out of Scope
- Automated summarization — deliberately deferred; summarizing is a manual step outside this tool
- Direct integration with the Article Catalog System's storage or SQLite index — this tool never writes to `articles/` or `catalog.db` directly
- Image extraction/downloading
- Batch or multi-URL processing (v1 is single-URL-at-a-time)

## 4) Success Criteria (Measurable)
- [ ] Metric 1: Given a real article URL, the tool produces a valid front-matter Markdown file with accurate title and body content, with no manual transcription required
- [ ] Metric 2: A JS-rendered page that yields too little content on a plain HTTP fetch is still recovered via the headless-browser fallback

## 5) Constraints (Known)
- Compliance: None (personal project)
- Security: None specified — single user, local tool, no auth
- Availability: Best-effort — no formal SLA (personal project)
- Budget / timeline: Personal time only, no financial budget or fixed deadline
- Tech constraints:
  - Must not import or call into `article_catalog`'s `core`/`storage`/`index` modules — this tool is architecturally standalone
  - Output front-matter field names must match the Article Catalog System's schema (`id, title, summary, media_type, tags, references, images, published_date, created_at`) for compatibility, even though the code is decoupled
  - The Playwright fallback's Chromium binary requires a manual one-time `playwright install chromium` step — this cannot be scripted via `pip` alone

## 6) Risks & Unknowns
- **Risk:** `trafilatura`'s extraction may occasionally choose the wrong "main content" region on unusual page layouts.
- **Risk:** The Playwright fallback adds a heavy dependency (~300MB Chromium binary) and a manual post-install step that could be forgotten, surfacing later as a confusing runtime error.
- **Unknown:** How well the 150-word fallback threshold heuristic generalizes across different sites; may need tuning after real-world use.
- **Assumption:** Single user, single machine, no concurrent runs, no external service integration beyond fetching public URLs.

## 7) Decision Needed
- Approve / reject / revise scope
- Target date for decision: N/A (personal project, no formal gate)

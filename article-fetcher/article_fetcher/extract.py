from dataclasses import dataclass
from datetime import date


class ExtractionError(Exception):
    """Raised when trafilatura itself errors on malformed input (not simply 'no content found')."""


@dataclass
class ExtractedArticle:
    title: str | None
    body_markdown: str
    published_date: str | None  # normalized to YYYY-MM-DD, or None
    author: str | None
    sitename: str | None
    word_count: int
    used_fallback: bool = False


def _normalize_date(raw) -> str | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(str(raw)[:10]).isoformat()
    except ValueError:
        return None


def extract_from_html(html: str, url: str) -> ExtractedArticle:
    import trafilatura

    try:
        # bare_extraction (no output_format) gives structured metadata fields
        # (title/date/author/sitename) via attribute access on the returned Document.
        metadata = trafilatura.bare_extraction(html, url=url, with_metadata=True, favor_recall=True)
        # extract() with output_format="markdown" is the call that actually returns
        # the body as a markdown string — bare_extraction's .text/.raw_text do not
        # reflect the requested output format.
        body_markdown = trafilatura.extract(
            html, url=url, output_format="markdown", with_metadata=False, favor_recall=True
        )
    except Exception as exc:  # trafilatura doesn't expose a single documented exception type
        raise ExtractionError(f"trafilatura failed to process {url}: {exc}") from exc

    body_markdown = (body_markdown or "").strip()

    if metadata is None:
        return ExtractedArticle(
            title=None,
            body_markdown=body_markdown,
            published_date=None,
            author=None,
            sitename=None,
            word_count=len(body_markdown.split()),
        )

    return ExtractedArticle(
        title=metadata.title,
        body_markdown=body_markdown,
        published_date=_normalize_date(metadata.date),
        author=metadata.author,
        sitename=metadata.sitename,
        word_count=len(body_markdown.split()),
    )

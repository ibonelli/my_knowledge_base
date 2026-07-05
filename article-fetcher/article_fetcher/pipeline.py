from . import extract, fetcher, render

MIN_WORD_COUNT = 150


def fetch_and_extract(
    url: str,
    *,
    allow_playwright_fallback: bool = True,
    min_word_count: int = MIN_WORD_COUNT,
    timeout: float = 15.0,
) -> extract.ExtractedArticle:
    html = fetcher.fetch_html(url, timeout=timeout)
    primary = extract.extract_from_html(html, url)

    if primary.word_count >= min_word_count or not allow_playwright_fallback:
        if primary.word_count == 0:
            raise extract.ExtractionError(f"no readable content found at {url}")
        return primary

    rendered_html = render.render_with_playwright(url, timeout=timeout)
    fallback = extract.extract_from_html(rendered_html, url)
    fallback.used_fallback = True

    best = fallback if fallback.word_count > primary.word_count else primary
    if best.word_count == 0:
        raise extract.ExtractionError(f"no readable content found at {url}, even after JS rendering")
    return best

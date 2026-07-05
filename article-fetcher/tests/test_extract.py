from pathlib import Path

from article_fetcher import extract

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_extract_from_good_article():
    result = extract.extract_from_html(_read("good_article.html"), "https://example.com/good")
    assert "local-first" in result.body_markdown.lower()
    assert result.word_count > 150
    assert result.used_fallback is False


def test_extract_metadata_title_and_date():
    result = extract.extract_from_html(_read("metadata_article.html"), "https://example.com/meta")
    assert result.title
    assert "tidal" in result.title.lower()
    assert result.published_date == "2022-04-11"


def test_extract_from_empty_html_returns_zero_word_count():
    result = extract.extract_from_html("<html><body></body></html>", "https://example.com/empty")
    assert result.word_count == 0
    assert result.body_markdown == ""


def test_extract_from_thin_shell_is_thin_without_js():
    # Without a real browser executing the <script>, the static HTML alone should
    # extract to little or no content — this is exactly the case the Playwright
    # fallback exists for.
    result = extract.extract_from_html(_read("thin_js_shell.html"), "https://example.com/thin")
    assert result.word_count < 20

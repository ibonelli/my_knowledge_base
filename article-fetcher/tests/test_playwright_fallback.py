import pytest

from article_fetcher import pipeline, render


def _chromium_available() -> bool:
    try:
        render.render_with_playwright("about:blank", timeout=5.0)
    except render.RenderError:
        return False
    return True


requires_chromium = pytest.mark.skipif(
    not _chromium_available(),
    reason="Playwright chromium is not installed — run `playwright install chromium`",
)


@requires_chromium
def test_playwright_renders_client_side_content(local_server):
    html = render.render_with_playwright(f"{local_server}/thin_js_shell.html")
    assert "undersea cables" in html.lower()


@requires_chromium
def test_pipeline_uses_real_playwright_fallback_for_thin_js_page(local_server):
    result = pipeline.fetch_and_extract(f"{local_server}/thin_js_shell.html", min_word_count=150)
    assert result.used_fallback is True
    assert result.word_count > 150
    assert "undersea cables" in result.body_markdown.lower()

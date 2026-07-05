from pathlib import Path

import pytest

from article_fetcher import extract, pipeline, render

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_primary_extraction_used_when_above_threshold(local_server):
    result = pipeline.fetch_and_extract(f"{local_server}/good_article.html", min_word_count=150)
    assert result.used_fallback is False
    assert result.word_count > 150


def test_fallback_skipped_when_disabled(local_server):
    # thin_js_shell.html extracts to very little without JS, but the fallback is
    # explicitly disabled here — the thin (non-empty) primary result should still
    # be returned rather than triggering Playwright. Only genuinely empty
    # extraction raises (see test_fallback_triggered_for_zero_content_page below).
    result = pipeline.fetch_and_extract(
        f"{local_server}/thin_js_shell.html",
        allow_playwright_fallback=False,
        min_word_count=150,
    )
    assert result.used_fallback is False
    assert result.word_count < 20


def test_fallback_triggered_for_zero_content_page(tmp_path, monkeypatch):
    empty_html_path = tmp_path / "empty.html"
    empty_html_path.write_text("<html><body></body></html>", encoding="utf-8")

    monkeypatch.setattr(
        "article_fetcher.fetcher.fetch_html",
        lambda url, timeout=15.0: empty_html_path.read_text(encoding="utf-8"),
    )

    with pytest.raises(extract.ExtractionError):
        pipeline.fetch_and_extract(
            "https://example.com/empty",
            allow_playwright_fallback=False,
            min_word_count=150,
        )


def test_fallback_triggered_and_used_when_it_yields_more_content(local_server, monkeypatch):
    rendered_html = (FIXTURES_DIR / "good_article.html").read_text(encoding="utf-8")
    monkeypatch.setattr(render, "render_with_playwright", lambda url, timeout=30.0: rendered_html)

    result = pipeline.fetch_and_extract(
        f"{local_server}/thin_js_shell.html",
        min_word_count=150,
    )
    assert result.used_fallback is True
    assert result.word_count > 150


def test_forcing_fallback_via_high_threshold_even_on_good_content(local_server, monkeypatch):
    calls = []

    def fake_render(url, timeout=30.0):
        calls.append(url)
        return (FIXTURES_DIR / "good_article.html").read_text(encoding="utf-8")

    monkeypatch.setattr(render, "render_with_playwright", fake_render)

    result = pipeline.fetch_and_extract(
        f"{local_server}/good_article.html",
        min_word_count=1_000_000,
    )
    assert calls, "expected the Playwright fallback to have been invoked"
    assert result.word_count > 0

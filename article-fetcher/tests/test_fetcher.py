import pytest

from article_fetcher import fetcher


def test_fetch_html_success(local_server):
    html = fetcher.fetch_html(f"{local_server}/good_article.html")
    assert "local-first" in html.lower()


def test_fetch_html_404(local_server):
    with pytest.raises(fetcher.FetchError):
        fetcher.fetch_html(f"{local_server}/does-not-exist.html")


def test_fetch_html_timeout(local_server):
    with pytest.raises(fetcher.FetchError):
        fetcher.fetch_html(f"{local_server}/slow", timeout=0.2)


def test_fetch_html_rejects_non_http_scheme():
    with pytest.raises(fetcher.FetchError):
        fetcher.fetch_html("ftp://example.com/file")


def test_fetch_html_rejects_malformed_url():
    with pytest.raises(fetcher.FetchError):
        fetcher.fetch_html("not a url")

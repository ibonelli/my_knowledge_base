import urllib.parse

import requests

USER_AGENT = "article-fetcher/0.1 (+personal knowledge base tool)"


class FetchError(Exception):
    pass


def fetch_html(url: str, *, timeout: float = 15.0) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise FetchError(f"not a valid http(s) URL: {url!r}")

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise FetchError(f"timed out fetching {url}") from exc
    except requests.exceptions.HTTPError as exc:
        raise FetchError(f"HTTP error fetching {url}: {exc}") from exc
    except requests.exceptions.RequestException as exc:
        raise FetchError(f"failed to fetch {url}: {exc}") from exc

    return response.text

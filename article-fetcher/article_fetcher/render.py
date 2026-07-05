from . import fetcher


class RenderError(Exception):
    pass


def render_with_playwright(url: str, *, timeout: float = 30.0) -> str:
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RenderError(
            "playwright is not installed — run `pip install -e '.[test]'` "
            "and `playwright install chromium`"
        ) from exc

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page(user_agent=fetcher.USER_AGENT)
                page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
                html = page.content()
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise RenderError(f"headless rendering failed for {url}: {exc}") from exc

    return html

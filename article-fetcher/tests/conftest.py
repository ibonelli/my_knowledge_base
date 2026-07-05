import functools
import http.server
import threading
import time
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class _SlowHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/slow":
            time.sleep(2)
        super().do_GET()

    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="session")
def local_server():
    handler = functools.partial(_SlowHandler, directory=str(FIXTURES_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    try:
        yield base_url
    finally:
        server.shutdown()
        thread.join(timeout=5)

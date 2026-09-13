#!/usr/bin/env python3
"""Launchpad dashboard server — http://localhost:8787

- Serves index.html and /api/data (data/latest.json)
- POST /api/refresh runs a full collection synchronously
- A background thread refreshes every 15 minutes
"""
import json, os, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
LATEST = os.path.join(HERE, "data", "latest.json")
PORT = 8787
REFRESH_EVERY = 15 * 60

import sys
sys.path.insert(0, HERE)
import collect

_lock = threading.Lock()


def refresh():
    with _lock:
        try:
            collect.run()
        except Exception as e:
            print(f"refresh failed: {e}", flush=True)


def _background():
    while True:
        time.sleep(REFRESH_EVERY)
        refresh()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, open(os.path.join(HERE, "index.html"), "rb").read(),
                       "text/html; charset=utf-8")
        elif self.path.startswith("/api/data"):
            if os.path.exists(LATEST):
                self._send(200, open(LATEST, "rb").read(), "application/json")
            else:
                self._send(200, b"{}", "application/json")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path == "/api/refresh":
            refresh()
            self._send(200, b'{"ok": true}', "application/json")
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not os.path.exists(LATEST):
        refresh()
    threading.Thread(target=_background, daemon=True).start()
    print(f"Launchpad running at http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

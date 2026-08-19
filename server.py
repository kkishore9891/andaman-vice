#!/usr/bin/env python3
"""Zero-dependency local server: static frontend + JSON API over trip.db.

Run:  python3 server.py [port]     (default 8765)
API:  /api/trip        -> full baked trip JSON (places, routes, events, facts, meta)
      /api/minute?t=N  -> the leaf event covering minute N since trip epoch
Static: everything else served from this directory (index.html, assets/...).
"""
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import db

ROOT = __file__.rsplit("/", 1)[0]


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/trip":
            return self._json(db.export())
        if u.path == "/api/minute":
            t = int(parse_qs(u.query).get("t", ["0"])[0])
            c = db.conn()
            parents = {r["parent_id"] for r in c.execute(
                "SELECT DISTINCT parent_id FROM events WHERE parent_id IS NOT NULL")}
            for r in c.execute(
                    "SELECT * FROM events WHERE start_min<=? AND end_min>? ORDER BY start_min",
                    (t, t)):
                if r["id"] not in parents:
                    return self._json(dict(r))
            return self._json({"error": "minute not mapped", "t": t}, 404)
        return super().do_GET()

    def log_message(self, fmt, *args):
        pass  # quiet


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"serving on http://localhost:{port}")
    HTTPServer(("127.0.0.1", port), H).serve_forever()

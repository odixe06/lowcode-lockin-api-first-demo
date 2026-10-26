"""Local teaching API. Python 3.10+, standard library only."""
import argparse
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)")
    db.commit()
    return db

def make_handler(db_path):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, value, content_type="application/json; charset=utf-8"):
            body = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def do_GET(self):
            route = self.path.split("?", 1)[0]
            if route == "/health":
                return self.send(200, {"status": "ok"})
            if route == "/":
                return self.send(200, (ROOT / "ui/index.html").read_bytes(), "text/html; charset=utf-8")
            if route in ("/tickets", "/export"):
                with connect(db_path) as db:
                    rows = [dict(r) for r in db.execute("SELECT * FROM tickets ORDER BY created_at, id")]
                return self.send(200, rows)
            if route == "/openapi.json":
                return self.send(200, (ROOT / "openapi.json").read_bytes())
            return self.send(404, {"error": "not found"})
        def do_POST(self):
            if self.path != "/tickets":
                return self.send(404, {"error": "not found"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 1 or length > 8192:
                    raise ValueError("request body must contain 1..8192 bytes")
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError("body must be an object")
                title = data.get("title")
                if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
                    raise ValueError("title must contain 1..120 characters")
            except (ValueError, UnicodeError) as error:
                return self.send(400, {"error": str(error)})
            row = dict(id=str(uuid.uuid4()), title=title.strip(), status="open", created_at=datetime.now(timezone.utc).isoformat())
            with connect(db_path) as db:
                db.execute("INSERT INTO tickets VALUES (:id,:title,:status,:created_at)", row)
                db.commit()
            return self.send(201, row)
    return Handler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--db", default=str(ROOT / "data/tickets.db"))
    args = parser.parse_args()
    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    print(f"API and replacement UI: http://{args.host}:{args.port}", flush=True)
    ThreadingHTTPServer((args.host, args.port), make_handler(args.db)).serve_forever()

#!/usr/bin/env python3
"""Cutroom — Milanote-style board server for creative briefs, cloud-backed.

File-based: every board is a JSON file in boards/, every image lives in assets/,
projects live in projects.json. Claude (or anyone) can write board JSON directly
and the app renders it. Every write syncs through to Supabase Storage
(supabase_store.py) so the whole workspace is restorable from the cloud.

Run:  python3 server.py          → http://localhost:8765
"""
import json
import mimetypes
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
BOARDS = os.path.join(ROOT, "boards")
ASSETS = os.path.join(ROOT, "assets")
STATIC = os.path.join(ROOT, "static")
PORT = int(os.environ.get("CUTROOM_PORT", os.environ.get("BRIEFBOARD_PORT", "8765")))
ENV_FILE = os.path.join(os.path.dirname(ROOT), ".env")
PROJECTS_FILE = os.path.join(ROOT, "projects.json")

try:
    import supabase_store as cloud
except Exception:
    cloud = None


def cloud_push(fn_name, *args):
    if cloud:
        cloud.fire_and_forget(getattr(cloud, fn_name), *args)


def load_projects():
    projects = {}
    if os.path.isfile(PROJECTS_FILE):
        try:
            with open(PROJECTS_FILE) as f:
                projects = json.load(f)
        except Exception:
            projects = {}
    if "general" not in projects:
        projects["general"] = {"name": "General", "created": time.strftime("%Y-%m-%d")}
        save_projects(projects)
    return projects


def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=1)
    cloud_push("push_projects")

_anthropic_client = None


def anthropic_client():
    """Lazy Anthropic client, key loaded from marketing brain/.env."""
    global _anthropic_client
    if _anthropic_client is None:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key and os.path.isfile(ENV_FILE):
            for line in open(ENV_FILE):
                if line.startswith("ANTHROPIC_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=key)
    return _anthropic_client


AI_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {"type": "string"},
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["note", "label", "lane"]},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "w": {"type": "integer"},
                    "h": {"type": "integer"},
                    "title": {"type": "string"},
                    "text": {"type": "string"},
                    "color": {"type": "string"},
                    "size": {"type": "integer"},
                },
                "required": ["type", "x", "y", "w", "h", "title", "text", "color", "size"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["reply", "cards"],
    "additionalProperties": False,
}

AI_SYSTEM = """You are the AI layer of Cutroom, an internal Milanote-style whiteboard a direct-response marketing team uses for creative briefs and reference-ad storyboards.

You receive the full JSON of the current board plus an instruction from a team member. Respond with `reply` (one or two sentences to the user) and `cards` (new cards to add — empty if the instruction is a pure question).

Card types you may create:
- note: sticky card. title = short bold header (may be ""), text = body, color = background hex. Palette: "#f7f5ee" neutral, "#fdf3c9" script/idea yellow, "#f3dcE8" emotion pink, "#dff2e1" DO green, "#f9d9d4" DON'T red. Typical w 260-320, h ≈ 26 + 19 per ~34-char line of text (+24 if titled).
- label: floating headline. text = the words, size = font px (22 section, 34 title). h ≈ size + 14. color "" for default, or a hex.
- lane: dashed container rectangle behind a group. title = uppercase tab text. Draw it AROUND cards it should visually group (place it first in your list; it renders behind).

Coordinates are absolute pixels on an infinite canvas; y grows downward. Never overlap existing cards: the board summary includes the current bounding box — place new content below it (bounds.bottom + 80) unless the instruction says otherwise, laying cards out left-to-right in columns ~300px apart. For fields that don't apply, use "" for strings and 0 for size.

Ground everything in what is actually on the board; never invent studies, statistics, or citations. Write in plain direct-response language, no em dashes."""


def board_bounds(cards):
    if not cards:
        return {"left": 0, "top": 0, "right": 0, "bottom": 0}
    return {
        "left": min(c["x"] for c in cards),
        "top": min(c["y"] for c in cards),
        "right": max(c["x"] + c["w"] for c in cards),
        "bottom": max(c["y"] + c["h"] for c in cards),
    }

os.makedirs(BOARDS, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-_]*$")


def slugify(s):
    s = re.sub(r"[^a-z0-9\-_ ]", "", s.lower().strip())
    return re.sub(r"[\s_]+", "-", s)[:60] or "board"


def board_path(slug):
    if not SLUG_RE.match(slug):
        raise ValueError("bad slug")
    return os.path.join(BOARDS, slug + ".json")


def list_boards():
    out = []
    for f in sorted(os.listdir(BOARDS)):
        if not f.endswith(".json"):
            continue
        p = os.path.join(BOARDS, f)
        try:
            with open(p) as fh:
                b = json.load(fh)
        except Exception:
            continue
        out.append({
            "id": f[:-5],
            "title": b.get("title", f[:-5]),
            "project": b.get("project", "general"),
            "cards": len(b.get("cards", [])),
            "updated": os.path.getmtime(p),
        })
    out.sort(key=lambda x: -x["updated"])
    return out


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    # ---- helpers -------------------------------------------------------
    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, ctype=None):
        if not os.path.isfile(path):
            return self.send_json({"error": "not found"}, 404)
        ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n) if n else b""

    # ---- routes --------------------------------------------------------
    def do_GET(self):
        u = urlparse(self.path)
        path = unquote(u.path)
        if path == "/":
            return self.send_file(os.path.join(STATIC, "home.html"), "text/html")
        if path.startswith("/b/"):
            return self.send_file(os.path.join(STATIC, "board.html"), "text/html")
        if path == "/api/boards":
            return self.send_json(list_boards())
        if path == "/api/projects":
            projects = load_projects()
            counts = {}
            for b in list_boards():
                counts[b["project"]] = counts.get(b["project"], 0) + 1
            return self.send_json([
                {"id": slug, "name": p.get("name", slug),
                 "created": p.get("created", ""), "boards": counts.get(slug, 0)}
                for slug, p in projects.items()
            ])
        m = re.match(r"^/api/boards/([a-z0-9\-_]+)$", path)
        if m:
            p = board_path(m.group(1))
            if not os.path.isfile(p):
                return self.send_json({"error": "not found"}, 404)
            return self.send_file(p, "application/json")
        if path.startswith("/assets/"):
            rel = os.path.normpath(path[len("/assets/"):])
            if rel.startswith(".."):
                return self.send_json({"error": "bad path"}, 400)
            return self.send_file(os.path.join(ASSETS, rel))
        if path.startswith("/static/"):
            rel = os.path.normpath(path[len("/static/"):])
            if rel.startswith(".."):
                return self.send_json({"error": "bad path"}, 400)
            return self.send_file(os.path.join(STATIC, rel))
        return self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/api/boards":
            try:
                data = json.loads(self.read_body() or b"{}")
            except Exception:
                return self.send_json({"error": "bad json"}, 400)
            title = data.get("title") or "Untitled board"
            project = data.get("project") or "general"
            if project not in load_projects():
                project = "general"
            slug = slugify(title)
            base, i = slug, 2
            while os.path.exists(board_path(slug)):
                slug = f"{base}-{i}"
                i += 1
            board = {"id": slug, "title": title, "project": project,
                     "created": time.strftime("%Y-%m-%d"),
                     "cards": data.get("cards", []), "edges": data.get("edges", [])}
            with open(board_path(slug), "w") as f:
                json.dump(board, f, indent=1)
            cloud_push("push_board", slug)
            return self.send_json({"id": slug})
        if u.path == "/api/projects":
            try:
                data = json.loads(self.read_body() or b"{}")
            except Exception:
                return self.send_json({"error": "bad json"}, 400)
            name = (data.get("name") or "").strip()
            if not name:
                return self.send_json({"error": "need name"}, 400)
            slug = slugify(name)
            projects = load_projects()
            if slug in projects:
                return self.send_json({"error": "project exists", "id": slug}, 409)
            projects[slug] = {"name": name, "created": time.strftime("%Y-%m-%d")}
            save_projects(projects)
            return self.send_json({"id": slug})
        if u.path == "/api/sync":
            if not cloud:
                return self.send_json({"error": "cloud sync unavailable"}, 500)
            try:
                return self.send_json(cloud.sync())
            except Exception as e:
                return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        if u.path == "/api/ai":
            try:
                data = json.loads(self.read_body() or b"{}")
                slug = data.get("board", "")
                prompt = (data.get("prompt") or "").strip()
                if not prompt or not SLUG_RE.match(slug):
                    return self.send_json({"error": "need board and prompt"}, 400)
                bp = board_path(slug)
                if not os.path.isfile(bp):
                    return self.send_json({"error": "board not found"}, 404)
                with open(bp) as f:
                    board = json.load(f)
                context = json.dumps({
                    "title": board.get("title"),
                    "bounds": board_bounds(board.get("cards", [])),
                    "cards": board.get("cards", []),
                })
                client = anthropic_client()
                response = client.messages.create(
                    model="claude-opus-5",
                    max_tokens=16000,
                    system=AI_SYSTEM,
                    output_config={"format": {"type": "json_schema", "schema": AI_SCHEMA}},
                    messages=[{
                        "role": "user",
                        "content": f"BOARD JSON:\n{context}\n\nINSTRUCTION:\n{prompt}",
                    }],
                )
                if response.stop_reason == "refusal":
                    return self.send_json({"error": "The AI declined this request."}, 400)
                text = next(b.text for b in response.content if b.type == "text")
                result = json.loads(text)
                added = 0
                for c in result.get("cards", []):
                    card = {k: v for k, v in c.items() if v not in ("", 0) or k in ("x", "y")}
                    card["id"] = "ai" + os.urandom(4).hex()
                    board.setdefault("cards", []).append(card)
                    added += 1
                if added:
                    with open(bp, "w") as f:
                        json.dump(board, f, indent=1)
                    cloud_push("push_board", slug)
                return self.send_json({"reply": result.get("reply", ""), "added": added})
            except Exception as e:
                return self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)
        if u.path == "/api/assets":
            board = q.get("board", ["misc"])[0]
            name = q.get("name", ["file.png"])[0]
            name = re.sub(r"[^A-Za-z0-9._\-]", "_", os.path.basename(name))
            d = os.path.join(ASSETS, slugify(board))
            os.makedirs(d, exist_ok=True)
            dest = os.path.join(d, name)
            base, ext = os.path.splitext(name)
            i = 2
            while os.path.exists(dest):
                dest = os.path.join(d, f"{base}-{i}{ext}")
                i += 1
            with open(dest, "wb") as f:
                f.write(self.read_body())
            rel = os.path.relpath(dest, ASSETS).replace(os.sep, "/")
            cloud_push("push_asset", rel)
            return self.send_json({"src": "/assets/" + rel})
        return self.send_json({"error": "not found"}, 404)

    def do_PUT(self):
        m = re.match(r"^/api/boards/([a-z0-9\-_]+)$", urlparse(self.path).path)
        if not m:
            return self.send_json({"error": "not found"}, 404)
        try:
            data = json.loads(self.read_body())
        except Exception:
            return self.send_json({"error": "bad json"}, 400)
        data["id"] = m.group(1)
        with open(board_path(m.group(1)), "w") as f:
            json.dump(data, f, indent=1)
        cloud_push("push_board", m.group(1))
        return self.send_json({"ok": True})

    def do_DELETE(self):
        path = urlparse(self.path).path
        m = re.match(r"^/api/boards/([a-z0-9\-_]+)$", path)
        if m:
            p = board_path(m.group(1))
            if os.path.isfile(p):
                os.remove(p)
            cloud_push("delete_board", m.group(1))
            return self.send_json({"ok": True})
        m = re.match(r"^/api/projects/([a-z0-9\-_]+)$", path)
        if m:
            slug = m.group(1)
            if slug == "general":
                return self.send_json({"error": "cannot delete General"}, 400)
            projects = load_projects()
            projects.pop(slug, None)
            save_projects(projects)
            # boards fall back to General
            for b in list_boards():
                if b["project"] == slug:
                    bp = board_path(b["id"])
                    with open(bp) as f:
                        data = json.load(f)
                    data["project"] = "general"
                    with open(bp, "w") as f:
                        json.dump(data, f, indent=1)
                    cloud_push("push_board", b["id"])
            return self.send_json({"ok": True})
        return self.send_json({"error": "not found"}, 404)


if __name__ == "__main__":
    load_projects()
    if cloud:
        cloud.fire_and_forget(cloud.sync)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Cutroom running → http://localhost:{PORT}")
    srv.serve_forever()

"""Cutroom bridge — push a storyboard spec, get a board URL for the editor.

(Cutroom is the renamed BriefBoard — the internal Milanote-style whiteboard.)
Shells out to cutroom/board_builder.py with the system python3, the same way
the cutroom skill runs it, so this server never drifts from the board layout
logic. Ensures the Cutroom server is up before returning a URL.
"""

import json
import os
import re
import socket
import subprocess
import tempfile
import time

from paths import BRIEFBOARD

PORT = int(os.environ.get("BRIEFBOARD_PORT", "8765"))


def _server_up() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=1):
            return True
    except OSError:
        return False


def ensure_server() -> bool:
    if _server_up():
        return True
    subprocess.Popen(
        ["python3", str(BRIEFBOARD / "server.py")],
        cwd=str(BRIEFBOARD),
        stdout=open("/tmp/cutroom.log", "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(10):
        time.sleep(0.5)
        if _server_up():
            return True
    return False


def push_board(spec: dict, slug: str | None = None,
               project: str | None = None) -> dict:
    """spec is the board_builder semantic spec: {title, summary, project,
    timelines[{label, source, beats[{t, script, frame, visual, emotion, note}]}],
    notes, moodboard}. Frame paths must be absolute local paths; the builder
    copies them into the board's assets."""
    if project:
        spec = {**spec, "project": project}
    up = ensure_server()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(spec, f)
        spec_path = f.name
    cmd = ["python3", str(BRIEFBOARD / "board_builder.py"), spec_path]
    if slug:
        cmd += ["--slug", slug]
    proc = subprocess.run(cmd, cwd=str(BRIEFBOARD), capture_output=True, text=True, timeout=120)
    os.unlink(spec_path)
    if proc.returncode != 0:
        return {"error": "board_builder failed", "stderr": proc.stderr[-2000:], "stdout": proc.stdout[-2000:]}
    m = re.search(r"/b/([a-z0-9\-_]+)", proc.stdout)
    built_slug = m.group(1) if m else slug
    return {"slug": built_slug,
            "url": f"http://localhost:{PORT}/b/{built_slug}",
            "server_up": up,
            "output": proc.stdout.strip()}


def list_boards() -> list[dict]:
    boards_dir = BRIEFBOARD / "boards"
    out = []
    for p in sorted(boards_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(p.read_text())
            title, project = data.get("title", p.stem), data.get("project", "general")
        except (json.JSONDecodeError, OSError):
            title, project = p.stem, "general"
        out.append({"slug": p.stem, "title": title, "project": project,
                    "url": f"http://localhost:{PORT}/b/{p.stem}",
                    "updated": time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime))})
    return out


def export_board(slug: str) -> dict:
    proc = subprocess.run(["python3", str(BRIEFBOARD / "export_board.py"), slug],
                          cwd=str(BRIEFBOARD), capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return {"error": "export failed", "stderr": proc.stderr[-2000:]}
    exports = BRIEFBOARD / "exports"
    candidates = sorted(exports.glob(f"{slug}*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    return {"slug": slug,
            "html": str(candidates[0]) if candidates else None,
            "output": proc.stdout.strip()}

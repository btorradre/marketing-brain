#!/usr/bin/env python3
"""ugc-forge UI — a zero-dependency local web app (Python stdlib only).

Run:  python3 ui/server.py   (then open http://127.0.0.1:8765)

It wraps the CLI: uploads land in ui/runs/<job>/, the pipeline runs as a
subprocess, its log lines stream to the browser over SSE, and finished MP4s /
the manifest are served back for playback and download. The "Preview segments
(free)" button runs --plan-only, which makes NO API calls.
"""
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent      # skill root
SCRIPTS = ROOT / "scripts"
UI = ROOT / "ui"
RUNS = UI / "runs"
RUNS.mkdir(parents=True, exist_ok=True)

JOBS = {}          # job_id -> {dir, proc, lines, status, result}
JOBS_LOCK = threading.Lock()
PORT = int(os.environ.get("UGC_FORGE_PORT", "8765"))


# --------------------------------------------------------------------------- #
# Minimal multipart/form-data parser (no cgi dependency)
# --------------------------------------------------------------------------- #
def parse_multipart(body: bytes, content_type: str):
    """Return (fields: dict[str,str], files: list[(name, filename, bytes)])."""
    m = re.search(r"boundary=([^;]+)", content_type)
    if not m:
        return {}, []
    boundary = m.group(1).strip().strip('"').encode()
    sep = b"--" + boundary
    fields, files = {}, []
    for part in body.split(sep):
        part = part.strip(b"\r\n")
        if not part or part == b"--":
            continue
        if b"\r\n\r\n" not in part:
            continue
        head, data = part.split(b"\r\n\r\n", 1)
        headers = head.decode("utf-8", "replace")
        disp = re.search(r'name="([^"]*)"', headers)
        if not disp:
            continue
        name = disp.group(1)
        fn = re.search(r'filename="([^"]*)"', headers)
        if fn and fn.group(1):
            files.append((name, fn.group(1), data))
        else:
            fields[name] = data.decode("utf-8", "replace").strip()
    return fields, files


# --------------------------------------------------------------------------- #
# Build the CLI argv from submitted form
# --------------------------------------------------------------------------- #
def build_job(fields, files):
    job_id = uuid.uuid4().hex[:10]
    jdir = RUNS / job_id
    jdir.mkdir(parents=True, exist_ok=True)
    out = jdir / "ad.mp4"
    argv = ["--out", str(out), "--run-manifest", str(jdir / "ad.manifest.json")]

    plan = fields.get("mode") == "plan"
    if plan:
        argv.append("--plan-only")

    # Script vs pre-segmented manifest
    if fields.get("input_kind") == "manifest" and fields.get("manifest_json", "").strip():
        mpath = jdir / "segments.json"
        mpath.write_text(fields["manifest_json"])
        argv += ["--manifest", str(mpath)]
    else:
        spath = jdir / "ad.txt"
        spath.write_text(fields.get("script_text", ""))
        argv += ["--script", str(spath)]

    # Avatars
    for i, (name, filename, data) in enumerate(f for f in files if f[0] == "avatar"):
        ext = pathlib.Path(filename).suffix or ".png"
        ap = jdir / f"avatar_{i:02d}{ext}"
        ap.write_bytes(data)
        argv += ["--avatar", str(ap)]

    # Audio source: synth | upload_segments | upload_single
    audio_mode = fields.get("audio_mode", "synth")
    vo_files = [f for f in files if f[0] == "vo_segment"]
    vo_single = [f for f in files if f[0] == "vo_single"]
    if audio_mode == "upload_segments" and vo_files and not plan:
        vodir = jdir / "vo"
        vodir.mkdir(exist_ok=True)
        for i, (_, filename, data) in enumerate(vo_files):
            ext = pathlib.Path(filename).suffix or ".mp3"
            (vodir / f"seg_{i:03d}{ext}").write_bytes(data)
        argv += ["--audio-dir", str(vodir)]
    elif audio_mode == "upload_single" and vo_single and not plan:
        _, filename, data = vo_single[0]
        ext = pathlib.Path(filename).suffix or ".mp3"
        vp = jdir / f"voiceover{ext}"
        vp.write_bytes(data)
        argv += ["--voiceover", str(vp)]
        if fields.get("vo_noise_db", "").strip():
            argv += ["--vo-noise-db", str(int(fields["vo_noise_db"]))]
        if fields.get("vo_min_gap", "").strip():
            argv += ["--vo-min-gap", str(float(fields["vo_min_gap"]))]
    else:
        # Synthesis (or plan preview): voice_id needed only to actually generate.
        voice = fields.get("voice", "").strip() or ("x" if plan else "")
        if not voice and not plan:
            raise ValueError("Provide a voice_id, or upload a voiceover.")
        argv += ["--voice", voice]

    # Lexicon (inline JSON)
    if fields.get("lexicon_json", "").strip():
        lp = jdir / "pron.json"
        lp.write_text(fields["lexicon_json"])
        argv += ["--lexicon", str(lp)]

    # Style anchor -> settings.json
    style = {k[6:]: fields[k].strip() for k in fields
             if k.startswith("style_") and fields[k].strip()}
    if style:
        sp = jdir / "settings.json"
        sp.write_text(json.dumps({"style": style}))
        argv += ["--settings", str(sp)]

    # Options
    if fields.get("aspect"):
        argv += ["--aspect", fields["aspect"]]
    for asp in (fields.get("also_aspect", "") or "").split(","):
        asp = asp.strip()
        if asp:
            argv += ["--also-aspect", asp]
    if fields.get("reanchor_every", "").strip():
        argv += ["--reanchor-every", str(int(fields["reanchor_every"]))]
    if fields.get("reanchor_on_segment", "").strip():
        argv += ["--reanchor-on-segment", fields["reanchor_on_segment"].strip()]
    if fields.get("auto_drift") in ("1", "true", "on"):
        argv.append("--auto-drift")
    if fields.get("lipsync_backend"):
        argv += ["--lipsync-backend", fields["lipsync_backend"]]
    if fields.get("variations") in ("1", "true", "on"):
        argv.append("--variations")
    if fields.get("veo_model", "").strip():
        argv += ["--veo-model", fields["veo_model"].strip()]
    if fields.get("tts_model", "").strip():
        argv += ["--tts-model", fields["tts_model"].strip()]

    return job_id, jdir, argv, plan


def start_job(job_id, jdir, argv, plan):
    cmd = [sys.executable, str(SCRIPTS / "ugc_forge.py"), *argv]
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    job = {"dir": jdir, "proc": proc, "lines": [], "status": "running",
           "result": None, "plan": plan}
    with JOBS_LOCK:
        JOBS[job_id] = job

    def reader():
        for line in proc.stdout:
            job["lines"].append(line.rstrip("\n"))
        rc = proc.wait()
        job["status"] = "done" if rc == 0 else "error"
        job["result"] = collect_result(job_id, jdir, plan, rc)

    threading.Thread(target=reader, daemon=True).start()
    return job


def collect_result(job_id, jdir, plan, rc):
    res = {"job": job_id, "rc": rc, "mode": "plan" if plan else "forge", "outputs": []}
    manifest = jdir / "ad.manifest.json"
    if manifest.exists():
        res["manifest"] = "ad.manifest.json"
        try:
            data = json.loads(manifest.read_text())
            if plan:
                res["plan"] = data.get("segments", [])
            else:
                res["segments"] = data.get("segments", [])
                res["watermark"] = data.get("watermark_note")
        except Exception:
            pass
    if not plan:
        for mp4 in sorted(jdir.glob("*.mp4")):
            res["outputs"].append({"name": mp4.name, "path": mp4.name})
    return res


# --------------------------------------------------------------------------- #
# HTTP handler
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self._send(200, (UI / "index.html").read_text())
        if u.path == "/stream":
            return self.stream(parse_qs(u.query))
        if u.path == "/file":
            return self.serve_file(parse_qs(u.query))
        return self._send(404, "not found")

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/run":
            return self._send(404, "not found")
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        fields, fileparts = parse_multipart(body, self.headers.get("Content-Type", ""))
        try:
            job_id, jdir, argv, plan = build_job(fields, fileparts)
            start_job(job_id, jdir, argv, plan)
        except Exception as e:
            return self._send(400, json.dumps({"error": str(e)}),
                              ctype="application/json")
        return self._send(200, json.dumps({"job": job_id}), ctype="application/json")

    def stream(self, q):
        job_id = (q.get("job") or [""])[0]
        job = JOBS.get(job_id)
        if not job:
            return self._send(404, "no such job")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        idx = 0
        try:
            while True:
                while idx < len(job["lines"]):
                    self._sse("log", job["lines"][idx])
                    idx += 1
                if job["status"] != "running" and idx >= len(job["lines"]):
                    self._sse("done", json.dumps(job["result"] or {"rc": -1}))
                    break
                time.sleep(0.25)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _sse(self, event, data):
        payload = f"event: {event}\n"
        for line in str(data).splitlines() or [""]:
            payload += f"data: {line}\n"
        payload += "\n"
        self.wfile.write(payload.encode("utf-8"))
        self.wfile.flush()

    def serve_file(self, q):
        job_id = (q.get("job") or [""])[0]
        rel = (q.get("path") or [""])[0]
        job = JOBS.get(job_id)
        if not job:
            return self._send(404, "no such job")
        target = (job["dir"] / rel).resolve()
        if not str(target).startswith(str(job["dir"].resolve())) or not target.exists():
            return self._send(404, "not found")
        ctype = "video/mp4" if target.suffix == ".mp4" else "application/json" \
            if target.suffix == ".json" else "application/octet-stream"
        data = target.read_bytes()
        dl = "download" in q
        extra = {"Content-Disposition": f'attachment; filename="{target.name}"'} if dl else None
        return self._send(200, data, ctype=ctype, extra=extra)


def main():
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"[ugc-forge ui] serving {url}  (Ctrl-C to stop)")
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[ugc-forge ui] bye")


if __name__ == "__main__":
    main()

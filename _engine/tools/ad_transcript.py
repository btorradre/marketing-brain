#!/usr/bin/env python3
"""
ad_transcript.py — pull a timestamped transcript from any ad video URL.

Handles Meta Ad Library links (which are JS-walled and can't be curl'd), TikTok, YouTube,
Instagram, or a direct .mp4. Downloads with yt-dlp, strips the audio with ffmpeg, and
transcribes via ElevenLabs Scribe.

    python3 _engine/tools/ad_transcript.py "<url>" [--out <dir>] [--slug <name>]

Writes <slug>.mp4, <slug>.mp3 and <slug>-transcript.md into --out (default: alongside
this script under ./output). Prints the plain transcript to stdout.
"""
import argparse
import json
import os
import pathlib
import re
import ssl
import subprocess
import sys
import urllib.request

ENV_PATH = pathlib.Path(__file__).resolve().parents[2] / ".env"
SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"


def load_key(name: str) -> str:
    """Read one key out of the project .env without disturbing the process env."""
    if os.environ.get(name):
        return os.environ[name]
    if not ENV_PATH.exists():
        sys.exit(f"no .env at {ENV_PATH} and {name} not in environment")
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"{name} not found in {ENV_PATH}")


def ssl_ctx() -> ssl.SSLContext:
    """This machine's Python has no usable system trust store, so lean on certifi."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        bundle = os.environ.get("SSL_CERT_FILE")
        return ssl.create_default_context(cafile=bundle) if bundle else ssl.create_default_context()


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if proc.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:3])}...\n{proc.stderr[-2000:]}")
    return proc


def slugify(url: str) -> str:
    m = re.search(r"[?&]id=(\d+)", url)
    if m:
        return f"ad-{m.group(1)}"
    m = re.search(r"/(\d{6,})", url)
    return f"ad-{m.group(1)}" if m else "ad"


def download(url: str, dest: pathlib.Path) -> pathlib.Path:
    """yt-dlp handles the Ad Library's JS wall; a plain curl of that page returns a stub."""
    mp4 = dest.with_suffix(".mp4")
    if mp4.exists() and mp4.stat().st_size > 0:
        print(f"[skip] already downloaded: {mp4.name}", file=sys.stderr)
        return mp4
    print("[1/3] downloading...", file=sys.stderr)
    run(["yt-dlp", "--no-warnings", "-f", "mp4/best", "-o", str(mp4), url])
    return mp4


def extract_audio(mp4: pathlib.Path) -> pathlib.Path:
    mp3 = mp4.with_suffix(".mp3")
    if mp3.exists() and mp3.stat().st_size > 0:
        print(f"[skip] audio already extracted: {mp3.name}", file=sys.stderr)
        return mp3
    print("[2/3] extracting audio...", file=sys.stderr)
    run(["ffmpeg", "-y", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "16000",
         "-b:a", "64k", str(mp3)])
    return mp3


def transcribe(mp3: pathlib.Path, api_key: str) -> dict:
    print("[3/3] transcribing (ElevenLabs Scribe)...", file=sys.stderr)
    boundary = "----adtranscript"
    fields = {"model_id": "scribe_v1", "timestamps_granularity": "word", "diarize": "true"}
    body = bytearray()
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{mp3.name}\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode()
    body += mp3.read_bytes() + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        SCRIBE_URL, data=bytes(body),
        headers={"xi-api-key": api_key,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=600, context=ssl_ctx()) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs error {e.code}: {e.read().decode()[:900]}")


def build_lines(payload: dict) -> list[tuple[float, str]]:
    """Group words into sentence-ish lines so the transcript reads like a script."""
    words = [w for w in payload.get("words", []) if w.get("type") == "word"]
    if not words:
        return [(0.0, payload.get("text", "").strip())]
    lines, cur, start = [], [], words[0].get("start", 0.0)
    for w in words:
        cur.append(w["text"])
        # break on terminal punctuation, or when a line gets long enough to read as a beat
        if re.search(r"[.!?]$", w["text"]) or len(" ".join(cur)) > 170:
            lines.append((start, " ".join(cur).strip()))
            cur = []
            start = w.get("end", start)
    if cur:
        lines.append((start, " ".join(cur).strip()))
    return lines


def ts(sec: float) -> str:
    return f"{int(sec // 60):02d}:{int(sec % 60):02d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parent / "output"))
    ap.add_argument("--slug", default=None)
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    base = out / (args.slug or slugify(args.url))

    mp4 = download(args.url, base)
    mp3 = extract_audio(mp4)
    payload = transcribe(mp3, load_key("ELEVENLABS_API_KEY"))

    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(mp4)],
                         capture_output=True, text=True).stdout.strip()
    lines = build_lines(payload)
    md = [f"# Transcript: {base.name}", "",
          f"**Source:** {args.url}", f"**Duration:** {float(dur):.1f}s" if dur else "", "",
          "## Timestamped", ""]
    md += [f"**[{ts(t)}]** {txt}" for t, txt in lines]
    md += ["", "## Plain", "", payload.get("text", "").strip(), ""]

    md_path = base.parent / f"{base.name}-transcript.md"
    md_path.write_text("\n".join(md))
    print(f"\n[done] {md_path}", file=sys.stderr)
    print(payload.get("text", "").strip())


if __name__ == "__main__":
    main()

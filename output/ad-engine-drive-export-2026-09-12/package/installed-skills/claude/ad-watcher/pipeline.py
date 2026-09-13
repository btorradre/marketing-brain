#!/usr/bin/env python3
"""ad-watcher pipeline — universal video ad ingestion + Gemini descriptive pass.

Stages
------
1. Resolve source (URL → yt-dlp download, or local path).
2. Scene-change detection via ffmpeg → keyframes + short clips per beat.
3. Transcript (native captions first, then Whisper as fallback).
4. Gemini full-video pass — uploads the whole video + every keyframe and
   returns a structured per-beat breakdown (composition, on-screen text,
   action, motion, audio cues, etc.).
5. Emits a JSON manifest + frame paths Claude can Read and a final layout
   markdown for psychological analysis.

This script does the MECHANICAL work. Claude (the model) does the
psychological / direct-response layer on top of the manifest.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY", "[REDACTED_SECRET]"
)
GEMINI_MODEL = os.environ.get("AD_WATCHER_GEMINI_MODEL", "gemini-2.5-flash")
SCENE_THRESHOLD = float(os.environ.get("AD_WATCHER_SCENE_THRESHOLD", "0.28"))
MIN_BEAT_GAP = float(os.environ.get("AD_WATCHER_MIN_BEAT_GAP", "0.5"))
FALLBACK_INTERVAL = float(os.environ.get("AD_WATCHER_FALLBACK_INTERVAL", "2.5"))
MAX_BEATS = int(os.environ.get("AD_WATCHER_MAX_BEATS", "120"))


def log(stage: str, msg: str) -> None:
    print(f"[{stage}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

def check_deps() -> None:
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            sys.exit(f"[deps] missing {binary} — install via `brew install ffmpeg`")
    try:
        import google.genai  # noqa: F401
    except ImportError:
        sys.exit(
            "[deps] missing google-genai — install via "
            "`pip install google-genai` (used for Gemini video upload)."
        )


# ---------------------------------------------------------------------------
# Stage 1 — resolve source
# ---------------------------------------------------------------------------

def is_url(src: str) -> bool:
    p = urlparse(src)
    return p.scheme in {"http", "https"} and bool(p.netloc)


def download(src: str, work_dir: Path) -> Path:
    if not is_url(src):
        p = Path(src).expanduser().resolve()
        if not p.exists():
            sys.exit(f"[download] local file not found: {src}")
        return p

    if not shutil.which("yt-dlp"):
        sys.exit("[download] missing yt-dlp — install via `brew install yt-dlp`")

    out_template = str(work_dir / "source.%(ext)s")
    log("download", f"yt-dlp → {out_template}")
    subprocess.run(
        [
            "yt-dlp",
            "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "--write-auto-subs", "--write-subs",
            "--sub-lang", "en.*",
            "--convert-subs", "srt",
            "-o", out_template,
            src,
        ],
        check=True,
    )

    for ext in ("mp4", "mkv", "webm", "mov"):
        candidate = work_dir / f"source.{ext}"
        if candidate.exists():
            return candidate
    sys.exit("[download] yt-dlp finished but no source.* file found")


# ---------------------------------------------------------------------------
# Stage 2 — scene-change beat extraction
# ---------------------------------------------------------------------------

def probe_duration(video: Path) -> float:
    res = subprocess.run(
        [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", video.as_posix(),
        ],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(res.stdout)["format"]["duration"])


def detect_scenes(video: Path, threshold: float = SCENE_THRESHOLD) -> list[float]:
    cmd = [
        "ffmpeg", "-i", video.as_posix(),
        "-filter:v", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr", "-f", "null", "-",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    ts: list[float] = [0.0]
    for line in res.stderr.splitlines():
        m = re.search(r"pts_time:(\d+\.?\d*)", line)
        if m:
            t = float(m.group(1))
            if t - ts[-1] > MIN_BEAT_GAP:
                ts.append(t)
    return ts


def extract_beats(video: Path, work_dir: Path, threshold: float = SCENE_THRESHOLD) -> list[dict]:
    duration = probe_duration(video)
    log("beats", f"duration {duration:.1f}s")

    timestamps = detect_scenes(video, threshold)
    if len(timestamps) <= 2 and duration > 8:
        log("beats", f"scene-detect found only {len(timestamps)} cuts; "
                     f"falling back to fixed interval {FALLBACK_INTERVAL}s")
        timestamps = []
        t = 0.0
        while t < duration:
            timestamps.append(round(t, 2))
            t += FALLBACK_INTERVAL

    if len(timestamps) > MAX_BEATS:
        log("beats", f"capping beats {len(timestamps)} → {MAX_BEATS} (uniform decimation)")
        step = len(timestamps) / MAX_BEATS
        timestamps = [timestamps[int(i * step)] for i in range(MAX_BEATS)]

    log("beats", f"{len(timestamps)} beats")

    frames_dir = work_dir / "frames"
    clips_dir = work_dir / "clips"
    frames_dir.mkdir(exist_ok=True)
    clips_dir.mkdir(exist_ok=True)

    beats: list[dict] = []
    for i, ts in enumerate(timestamps):
        num = f"{i+1:03d}"
        frame = frames_dir / f"beat_{num}.jpg"
        clip = clips_dir / f"beat_{num}.mp4"
        next_ts = timestamps[i + 1] if i + 1 < len(timestamps) else min(ts + 2.0, duration)
        clip_dur = max(0.6, min(next_ts - ts, 4.0))

        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{ts}", "-i", video.as_posix(),
             "-frames:v", "1", "-q:v", "3", "-vf", "scale=640:-2", frame.as_posix()],
            capture_output=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{ts}", "-i", video.as_posix(),
             "-t", f"{clip_dur}", "-c:v", "libx264", "-preset", "veryfast",
             "-an", clip.as_posix()],
            capture_output=True,
        )
        beats.append({
            "index": i + 1,
            "t": round(ts, 2),
            "t_end": round(ts + clip_dur, 2),
            "duration": round(clip_dur, 2),
            "frame": frame.as_posix(),
            "clip": clip.as_posix(),
        })

    return beats


# ---------------------------------------------------------------------------
# Stage 3 — transcript
# ---------------------------------------------------------------------------

def find_subtitle(work_dir: Path) -> Path | None:
    for p in work_dir.glob("source.*.srt"):
        return p
    for p in work_dir.glob("source.*.vtt"):
        return p
    return None


def parse_srt(p: Path) -> list[dict]:
    text = p.read_text(errors="ignore")
    blocks = re.split(r"\n\s*\n", text.strip())
    entries: list[dict] = []
    for b in blocks:
        m = re.search(
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
            b,
        )
        if not m:
            continue
        start = (int(m.group(1)) * 3600 + int(m.group(2)) * 60
                 + int(m.group(3)) + int(m.group(4)) / 1000)
        end = (int(m.group(5)) * 3600 + int(m.group(6)) * 60
               + int(m.group(7)) + int(m.group(8)) / 1000)
        lines = b.splitlines()
        idx = next((i for i, ln in enumerate(lines) if "-->" in ln), -1)
        body = " ".join(ln.strip() for ln in lines[idx + 1:] if ln.strip())
        body = re.sub(r"<[^>]+>", "", body)
        if body:
            entries.append({"start": round(start, 2), "end": round(end, 2), "text": body})
    return entries


def whisper_transcript(audio: Path) -> list[dict]:
    """Use Groq Whisper if available; else OpenAI."""
    import requests
    groq = os.environ.get("GROQ_API_KEY")
    openai = os.environ.get("OPENAI_API_KEY")
    if groq:
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        model = "whisper-large-v3"
        key = groq
    elif openai:
        url = "https://api.openai.com/v1/audio/transcriptions"
        model = "whisper-1"
        key = openai
    else:
        log("transcript", "no whisper key (set GROQ_API_KEY or OPENAI_API_KEY); skipping")
        return []

    with audio.open("rb") as fh:
        res = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
            data={"model": model, "response_format": "verbose_json",
                  "timestamp_granularities[]": "segment"},
            files={"file": (audio.name, fh, "audio/mpeg")},
            timeout=120,
        )
    if res.status_code != 200:
        log("transcript", f"whisper error {res.status_code}: {res.text[:200]}")
        return []
    data = res.json()
    return [
        {"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
        for s in data.get("segments", [])
    ]


def get_transcript(video: Path, work_dir: Path) -> tuple[list[dict], str]:
    sub = find_subtitle(work_dir)
    if sub:
        entries = parse_srt(sub)
        if entries:
            return entries, f"captions ({sub.name})"

    audio = work_dir / "audio.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", video.as_posix(), "-vn", "-ac", "1",
         "-ar", "16000", "-b:a", "64k", audio.as_posix()],
        capture_output=True,
    )
    if not audio.exists() or audio.stat().st_size < 1024:
        return [], "none"
    entries = whisper_transcript(audio)
    backend = "groq" if os.environ.get("GROQ_API_KEY") else "openai"
    return entries, f"whisper ({backend})" if entries else "none"


def transcript_for_beat(transcript: list[dict], t: float, t_end: float) -> str:
    chunks = []
    for seg in transcript:
        if seg["end"] < t or seg["start"] > t_end:
            continue
        chunks.append(seg["text"])
    return " ".join(chunks).strip()


# ---------------------------------------------------------------------------
# Stage 4 — Gemini descriptive pass
# ---------------------------------------------------------------------------

GEMINI_SYSTEM_PROMPT = """You are a video-ad analyst. You will receive a full ad video plus N keyframes that represent the start of every visual beat.

For EACH beat (in order), return a JSON object with these keys:
  - "index": beat number (1-indexed, matching what the user provides)
  - "t": start timestamp in seconds (matching the user input)
  - "shot_type": camera framing (e.g. CU, MS, WS, OTS, POV, insert, graphic_overlay, screen_recording, B-roll, talking_head)
  - "composition": one sentence describing framing, subject placement, depth, lighting
  - "subject": who/what is on screen (e.g. "creator, mid-30s woman, kitchen", "product bottle on counter", "graph overlay")
  - "action": what physically happens during the beat
  - "motion": camera + subject motion (e.g. "static handheld", "fast push-in", "whip pan right", "static graphic with kinetic text")
  - "on_screen_text": exact text visible on the frame, or "" if none. Capture caption overlays, headlines, hooks, lower-thirds, statistics. Preserve emojis and casing.
  - "audio_cues": SFX, music shifts, voiceover delivery quality if audible (e.g. "music drop", "whoosh on cut", "VO intimate"); "" if nothing notable
  - "color_palette": dominant tones (e.g. "warm kitchen, soft daylight")
  - "ad_role": label this beat's job in the funnel. ONE of: hook, pattern_interrupt, problem_agitation, mechanism_reveal, social_proof, product_introduction, demonstration, before_after, objection_handling, urgency, cta, transition, b_roll_cutaway, statistic_card, end_card, other
  - "notes": anything noteworthy about craft that doesn't fit above (1 sentence max)

Return STRICT JSON of the form:
{
  "overall": {
    "format": "AIUGC talking head | VSL with B-roll | Animated 3D | Stop-motion | Founder UGC | Doctor talking head | Listicle promo | other",
    "duration_s": <float>,
    "primary_emotion_arc": "<2-4 emotion labels in order, e.g. 'curiosity → recognition → vindication → urgency'>",
    "core_promise": "<the headline benefit promised>",
    "production_notes": "<one paragraph on production craft, pacing, sound design>"
  },
  "beats": [ { ... } ]
}

Do NOT include any prose outside the JSON. Do not wrap in ```json fences."""


def gemini_pass(video: Path, beats: list[dict], transcript_label: str) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)

    log("gemini", f"uploading video to Gemini ({video.stat().st_size/1e6:.1f} MB)")
    video_file = client.files.upload(file=video.as_posix())

    # Wait for ACTIVE
    for _ in range(60):
        info = client.files.get(name=video_file.name)
        if getattr(info, "state", None) and str(info.state).endswith("ACTIVE"):
            break
        time.sleep(1)

    beat_table = "\n".join(
        f"- index={b['index']} t={b['t']:.2f}s duration={b['duration']:.2f}s"
        for b in beats
    )
    user_prompt = (
        f"Here is the full ad video. There are {len(beats)} beats with these start "
        f"timestamps:\n{beat_table}\n\n"
        f"Transcript source: {transcript_label}.\n\n"
        f"Return the JSON described in the system prompt. Cover every beat."
    )

    try:
        parts = [
            types.Part.from_uri(file_uri=video_file.uri, mime_type="video/mp4"),
            types.Part(text=user_prompt),
        ]
        config = types.GenerateContentConfig(
            system_instruction=GEMINI_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        )
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[types.Content(role="user", parts=parts)],
            config=config,
        )
    finally:
        try:
            client.files.delete(name=video_file.name)
        except Exception:
            pass

    raw = response.text or ""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        log("gemini", f"JSON parse failed: {exc}; saving raw text")
        return {"overall": {}, "beats": [], "_raw_gemini": raw}


# ---------------------------------------------------------------------------
# Stage 5 — manifest + claude-facing markdown stub
# ---------------------------------------------------------------------------

def write_manifest(work_dir: Path, source: str, video: Path, beats: list[dict],
                   transcript: list[dict], transcript_label: str,
                   gemini: dict) -> Path:
    # Merge per-beat: ours + gemini + transcript snippet
    gemini_by_index = {b.get("index"): b for b in gemini.get("beats", []) if isinstance(b, dict)}

    enriched = []
    for b in beats:
        g = gemini_by_index.get(b["index"], {})
        enriched.append({
            **b,
            "vo": transcript_for_beat(transcript, b["t"], b["t_end"]),
            "gemini": g,
        })

    manifest = {
        "source": source,
        "video_path": video.as_posix(),
        "work_dir": work_dir.as_posix(),
        "transcript_source": transcript_label,
        "overall": gemini.get("overall", {}),
        "beats": enriched,
    }
    if "_raw_gemini" in gemini:
        manifest["_raw_gemini"] = gemini["_raw_gemini"]

    out = work_dir / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2))
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="video URL or local path")
    ap.add_argument("--out-dir", help="working directory (default: tmp)")
    ap.add_argument("--skip-gemini", action="store_true",
                    help="skip the Gemini pass — frames + transcript only")
    ap.add_argument("--scene-threshold", type=float, default=SCENE_THRESHOLD)
    args = ap.parse_args()

    check_deps()

    if args.out_dir:
        work_dir = Path(args.out_dir).expanduser().resolve()
        work_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Place output next to the local file when possible so the markdown
        # lives beside the video. For URLs, fall back to tmp.
        if is_url(args.source):
            work_dir = Path(tempfile.mkdtemp(prefix="ad-watcher-"))
        else:
            src_path = Path(args.source).expanduser().resolve()
            slug = re.sub(r"\W+", "-", src_path.stem).strip("-").lower()
            work_dir = src_path.parent / f".ad-watcher-{slug}"
            work_dir.mkdir(parents=True, exist_ok=True)
    log("init", f"work_dir = {work_dir}")

    video = download(args.source, work_dir)
    log("video", video.as_posix())

    beats = extract_beats(video, work_dir, threshold=args.scene_threshold)

    transcript, label = get_transcript(video, work_dir)
    log("transcript", f"{label} — {len(transcript)} segments")

    if args.skip_gemini:
        gemini = {"overall": {}, "beats": []}
    else:
        try:
            gemini = gemini_pass(video, beats, label)
        except Exception as exc:
            log("gemini", f"FAILED: {exc}")
            gemini = {"overall": {}, "beats": [], "_error": str(exc)}

    manifest_path = write_manifest(
        work_dir, args.source, video, beats, transcript, label, gemini
    )
    log("done", f"manifest: {manifest_path}")
    print(f"\nMANIFEST_PATH={manifest_path}")
    print(f"WORK_DIR={work_dir}")
    print(f"VIDEO_PATH={video}")
    print(f"FRAME_COUNT={len(beats)}")


if __name__ == "__main__":
    main()

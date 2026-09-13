"""Reference watcher — the MANDATORY head of every adaptation pipeline.

A faithful port of the ad-watcher pipeline, stage for stage:

1. Source: the worker has already put the video in a blob (yt-dlp / GetHookd /
   fetched URL); this module works on that local blob path.
2. Scene-change detection via ffmpeg -> one keyframe + short clip per beat.
3. Transcript: native captions (yt-dlp srt) first; else audio demux + Whisper —
   OpenAI whisper-1 via the workspace's openai credential, or Groq
   whisper-large-v3 when a groq credential exists. NEVER silent: the returned
   transcript label always names the backend that ran (or why none did).
4. Gemini full-video pass — uploads the whole video via the Files API so the
   model actually watches it, passes the beat list + transcript label exactly
   as the original, and returns the structured per-beat breakdown (shot type,
   composition, subject, action, motion, on-screen text, audio cues, color
   palette, ad role).
5. build_manifest merges ours + Gemini + per-beat transcript snippet.

STANDING LAW: all video analysis and video QA runs on Gemini 3.8 Flash
(`gemini-3.8-flash`). Environment and per-call model settings must match this
policy. Conflicting settings fail explicitly; no older-model fallback.
analyze_video() is the generic path (any asset + caller prompt -> JSON) for
frame QA, clip-drift checks and keyframe scoring.

This module does the MECHANICAL work. The calling model does the
psychological / direct-response layer on top of the manifest.
"""
from __future__ import annotations

import json
import os
import re
import time

import requests

from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.engines import shell

# Config (environment only; never a .env file)
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_MODEL = os.environ.get("ADENGINE_GEMINI_WATCH_MODEL") or DEFAULT_GEMINI_MODEL
SCENE_THRESHOLD = 0.28
MIN_BEAT_GAP = 0.0  # Retain rapid cuts; candidates are not verified edit points.
FALLBACK_INTERVAL = 2.5
MAX_BEATS = 120

WHISPER_BACKENDS = {
    "openai": ("https://api.openai.com/v1/audio/transcriptions", "whisper-1"),
    "groq": ("https://api.groq.com/openai/v1/audio/transcriptions", "whisper-large-v3"),
}


def gemini_model(override: str | None = None) -> str:
    for configured in (GEMINI_MODEL, override):
        if configured and configured != DEFAULT_GEMINI_MODEL:
            raise ProviderError(
                f"Visual analysis requires {DEFAULT_GEMINI_MODEL}; conflicting model {configured!r}. "
                "Update ADENGINE_GEMINI_WATCH_MODEL or the job's model setting; no fallback is allowed.")
    return DEFAULT_GEMINI_MODEL


# ---------------------------------------------------------------------------
# Stage 2 — scene-change beat extraction
# ---------------------------------------------------------------------------

def probe_duration(video: str) -> float:
    res = shell.run([settings.ffprobe, "-v", "quiet", "-print_format", "json",
                     "-show_format", video], check=True)
    return float(json.loads(res.stdout)["format"]["duration"])


def detect_scenes(video: str, threshold: float = SCENE_THRESHOLD,
                  min_gap: float = MIN_BEAT_GAP) -> list[float]:
    res = shell.run([settings.ffmpeg, "-i", video,
                     "-filter:v", f"select='gt(scene,{threshold})',showinfo",
                     "-vsync", "vfr", "-f", "null", "-"], timeout=900, check=True)
    ts: list[float] = [0.0]
    for line in res.stderr.splitlines():
        m = re.search(r"pts_time:(\d+\.?\d*)", line)
        if m:
            t = float(m.group(1))
            if t - ts[-1] > min_gap:
                ts.append(t)
    return ts


def extract_beats(video: str, work_dir: str, threshold: float = SCENE_THRESHOLD,
                  fallback_interval: float = FALLBACK_INTERVAL,
                  max_beats: int = MAX_BEATS) -> list[dict]:
    """One keyframe (jpg, 640w) + one short mute clip per beat, written under
    <work_dir>/frames and <work_dir>/clips. Returns beats with local paths the
    worker turns into blobs/assets."""
    duration = probe_duration(video)
    if duration <= 0 or fallback_interval <= 0 or max_beats < 1:
        raise ProviderError("Source duration, review interval and window limit must be positive")
    detected = detect_scenes(video, threshold)
    timestamps = sorted({t for t in detected if 0 <= t < duration})
    if len(timestamps) <= 2 and duration > 8:
        # Sampling adds review windows without erasing the detected boundaries.
        t = 0.0
        while t < duration:
            timestamps.append(round(t, 2))
            t += fallback_interval
        timestamps = sorted(set(timestamps))
    if len(timestamps) > max_beats:
        raise ProviderError(f"{len(timestamps)} review windows exceed limit {max_beats}; "
                            "analyze in smaller sections; no cut candidates were discarded")

    frames_dir = os.path.join(work_dir, "frames")
    clips_dir = os.path.join(work_dir, "clips")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)

    beats: list[dict] = []
    for i, ts in enumerate(timestamps):
        num = f"{i + 1:03d}"
        frame = os.path.join(frames_dir, f"beat_{num}.jpg")
        clip = os.path.join(clips_dir, f"beat_{num}.mp4")
        next_ts = timestamps[i + 1] if i + 1 < len(timestamps) else duration
        clip_dur = min(next_ts - ts, 4.0)
        shell.run([settings.ffmpeg, "-y", "-ss", f"{ts}", "-i", video,
                   "-frames:v", "1", "-q:v", "3", "-vf", "scale=640:-2", frame])
        shell.run([settings.ffmpeg, "-y", "-ss", f"{ts}", "-i", video,
                   "-t", f"{clip_dur}", "-c:v", "libx264", "-preset", "veryfast",
                   "-an", clip])
        beats.append({
            "index": i + 1,
            "t": ts,
            "t_end": next_ts,
            "duration": next_ts - ts,
            "boundary_origin": "source_start" if ts == 0 else (
                "scene_change_candidate" if ts in detected else "sampling_window"),
            "preview_t_end": ts + clip_dur,
            "preview_duration": clip_dur,
            "frame": frame if os.path.exists(frame) else None,
            "clip": clip if os.path.exists(clip) else None,
        })
    return beats


# ---------------------------------------------------------------------------
# Stage 3 — transcript
# ---------------------------------------------------------------------------

def find_subtitle(work_dir: str) -> str | None:
    if not os.path.isdir(work_dir):
        return None
    names = sorted(os.listdir(work_dir))
    for ext in (".srt", ".vtt"):
        for n in names:
            if n.startswith("source.") and n.endswith(ext):
                return os.path.join(work_dir, n)
    return None


def parse_srt(path: str) -> list[dict]:
    with open(path, errors="ignore") as f:
        text = f.read()
    blocks = re.split(r"\n\s*\n", text.strip())
    entries: list[dict] = []
    for b in blocks:
        m = re.search(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
                      r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})", b)
        if not m:
            continue
        start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000
        end = int(m.group(5)) * 3600 + int(m.group(6)) * 60 + int(m.group(7)) + int(m.group(8)) / 1000
        lines = b.splitlines()
        idx = next((i for i, ln in enumerate(lines) if "-->" in ln), -1)
        body = " ".join(ln.strip() for ln in lines[idx + 1:] if ln.strip())
        body = re.sub(r"<[^>]+>", "", body)
        if body:
            entries.append({"start": round(start, 2), "end": round(end, 2), "text": body})
    return entries


def demux_audio(video: str, work_dir: str) -> str | None:
    audio = os.path.join(work_dir, "audio.mp3")
    shell.run([settings.ffmpeg, "-y", "-i", video, "-vn", "-ac", "1",
               "-ar", "16000", "-b:a", "64k", audio])
    if not os.path.exists(audio) or os.path.getsize(audio) < 1024:
        return None
    return audio


def whisper_transcript(audio: str, key: str, backend: str = "openai") -> list[dict]:
    """Whisper via the OpenAI-compatible transcription endpoint (openai whisper-1
    or groq whisper-large-v3), verbose_json with segment timestamps."""
    if backend not in WHISPER_BACKENDS:
        raise ProviderError(f"unknown whisper backend {backend}")
    url, model = WHISPER_BACKENDS[backend]
    with open(audio, "rb") as fh:
        res = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
            data={"model": model, "response_format": "verbose_json",
                  "timestamp_granularities[]": "segment"},
            files={"file": (os.path.basename(audio), fh, "audio/mpeg")},
            timeout=300,
        )
    if res.status_code != 200:
        raise ProviderError(f"whisper ({backend}) HTTP {res.status_code}: {res.text[:200]}")
    data = res.json()
    return [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
            for s in data.get("segments", [])]


def get_transcript(video: str, work_dir: str, openai_key: str | None = None,
                   groq_key: str | None = None, prefer: str = "openai") -> tuple[list[dict], str]:
    """Captions first, then Whisper. The label ALWAYS says what ran:
    'captions (<file>)', 'whisper (openai)', 'whisper (groq)',
    'none (no audio track)', 'none (no whisper credential)', or
    'none (whisper failed: ...)'."""
    sub = find_subtitle(work_dir)
    if sub:
        entries = parse_srt(sub)
        if entries:
            return entries, f"captions ({os.path.basename(sub)})"

    audio = demux_audio(video, work_dir)
    if audio is None:
        return [], "none (no audio track)"

    order = ["openai", "groq"] if prefer != "groq" else ["groq", "openai"]
    keys = {"openai": openai_key, "groq": groq_key}
    available = [b for b in order if keys.get(b)]
    if not available:
        return [], "none (no whisper credential: add an openai or groq credential)"

    errors = []
    for backend in available:
        try:
            entries = whisper_transcript(audio, keys[backend], backend)
            return entries, f"whisper ({backend})" if entries else f"none (whisper ({backend}) returned no segments)"
        except ProviderError as exc:
            errors.append(str(exc))
    return [], f"none (whisper failed: {'; '.join(errors)[:200]})"


def transcript_for_beat(transcript: list[dict], t: float, t_end: float) -> str:
    chunks = [seg["text"] for seg in transcript if seg["end"] > t and seg["start"] < t_end]
    return " ".join(chunks).strip()


# ---------------------------------------------------------------------------
# Stage 4 — Gemini descriptive pass
# ---------------------------------------------------------------------------

GEMINI_SYSTEM_PROMPT = """You are a video-ad and rushes analyst handing evidence to an editing agent.
You receive the full video and a table of candidate review windows, not separate keyframes.
Scene detection is a heuristic: verify hard cuts, jump cuts, match cuts, dissolves,
wipes and fades visually. Sampling windows are NOT cuts. A full-video model pass
does NOT prove that every source frame was inspected. Mark uncertain timing and
request frame-window review; do not invent exact frames, easing, beats or measurements.

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
  "beats": [ { ... } ],
  "editorial": {
    "rushes": {"status": "reviewed|not_present|unknown", "summary": "...", "observations": []},
    "cuts": {"status": "reviewed|not_present|unknown", "summary": "...", "observations": []},
    "transitions": {"status": "reviewed|not_present|unknown", "summary": "...", "observations": []},
    "pacing": {"status": "reviewed|not_present|unknown", "summary": "...", "observations": []},
    "animations": {"status": "reviewed|not_present|unknown", "summary": "...", "observations": []}
  }
}

Every observation needs: id (unique across categories), start_s, end_s (source
seconds, end exclusive; equal only for an instantaneous cut), description,
confidence (0..1), and details (an object).
Rushes: log usable takes, select/reject/alternate, best action in/out points,
head/tail handles, continuity, focus/exposure/shake, occlusion, performance,
speech and audio defects. For a finished reference, describe available shot
segments only; never infer unseen raw takes.
Cuts: verified type, outgoing/incoming shot and action, continuity, exactness
or uncertainty of boundary, edit motivation, J/L audio offsets if audible.
Transitions: start/end, type, direction, overlap/handles, visual and sound cue.
Pacing: shot duration pattern, hook rhythm, acceleration, holds, pauses,
energy by section, speech/music synchronization and purpose. Distinguish visual
rhythm from music tempo; do not report BPM without audio evidence.
Animations: distinguish camera movement, subject motion, baked-in graphics and
editable overlay motion; record target/layer, entry/hold/exit, start/end states,
position/scale/rotation/opacity, direction, text, easing if observable, audio sync.
Use unknown for unresolved categories and not_present only after inspection.
Rushes and pacing must be reviewed even for a continuous shot: log its usable
source segment and hold duration. not_present applies to absent cuts/effects.
No fabricated metrics. Observations describe the source; suggested edit choices
must be explicitly identified as proposals in details, never as observed facts.

Do NOT include any prose outside the JSON. Do not wrap in ```json fences."""

ANALYZE_SYSTEM_PROMPT = """You are a meticulous video and image QA analyst for direct-response ads. Watch the supplied media in full, then answer the user's request. Return STRICT JSON only — an object, no prose outside it, no ```json fences. If the user names fields, use exactly those field names."""


def _make_client(key: str):
    from google import genai
    return genai.Client(api_key=key)


def _gemini_generate(media_path: str, mime_type: str, key: str, model: str,
                     system_instruction: str, user_prompt: str,
                     temperature: float = 0.2, client=None, sleep=time.sleep) -> str:
    """Upload the whole media file via the Files API, wait for ACTIVE, generate,
    and always delete the upload afterwards. Returns the raw text response."""
    from google.genai import types

    client = client or _make_client(key)
    uploaded = client.files.upload(file=media_path)
    try:
        for _ in range(60):
            info = client.files.get(name=uploaded.name)
            state = str(getattr(info, "state", ""))
            if state.endswith("ACTIVE"):
                break
            if state.endswith("FAILED"):
                raise ProviderError("Gemini media processing failed")
            sleep(1)
        else:
            raise ProviderError("Gemini media processing timed out")
        parts = [types.Part.from_uri(file_uri=uploaded.uri, mime_type=mime_type),
                 types.Part(text=user_prompt)]
        config = types.GenerateContentConfig(system_instruction=system_instruction,
                                             response_mime_type="application/json",
                                             temperature=temperature)
        response = client.models.generate_content(
            model=model, contents=[types.Content(role="user", parts=parts)], config=config)
    finally:
        try:
            client.files.delete(name=uploaded.name)
        except Exception:  # noqa: BLE001
            pass
    return response.text or ""


def parse_json_response(raw: str) -> dict:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw_gemini": raw, "_parse_error": True}
    return parsed if isinstance(parsed, dict) else {"result": parsed}


def gemini_pass(video: str, beats: list[dict], transcript_label: str, key: str,
                model: str | None = None, client=None, media_role: str = "reference") -> dict:
    """Full-video descriptive pass. Returns {"overall": {...}, "beats": [...]} and,
    on a parse failure, {"overall": {}, "beats": [], "_raw_gemini": text}."""
    beat_table = "\n".join(
        f"- index={b['index']} t={b['t']:.2f}s duration={b['duration']:.2f}s "
        f"boundary_origin={b.get('boundary_origin', 'unspecified')}" for b in beats)
    user_prompt = (
        f"Here is the full ad video. There are {len(beats)} beats with these start "
        f"timestamps:\n{beat_table}\n\n"
        f"Transcript source: {transcript_label}.\n\n"
        f"Source role: {media_role}. For rushes log takes, selects, rejects, handles and defects.\n"
        f"Return the JSON described in the system prompt. Cover every beat."
    )
    raw = _gemini_generate(video, "video/mp4", key, gemini_model(model),
                           GEMINI_SYSTEM_PROMPT, user_prompt, client=client)
    parsed = parse_json_response(raw)
    if parsed.get("_parse_error"):
        return {"overall": {}, "beats": [], "_raw_gemini": parsed.get("_raw_gemini", "")}
    parsed.setdefault("overall", {})
    parsed.setdefault("beats", [])
    return parsed


def analyze_video(media_path: str, prompt: str, key: str, model: str | None = None,
                  mime_type: str = "video/mp4", system_instruction: str | None = None,
                  client=None) -> dict:
    """Generic Gemini pass: any video/image asset + a caller prompt -> structured JSON.
    Used for frame QA, clip-drift checks, keyframe scoring."""
    raw = _gemini_generate(media_path, mime_type, key, gemini_model(model),
                           system_instruction or ANALYZE_SYSTEM_PROMPT, prompt, client=client)
    return parse_json_response(raw)


# ---------------------------------------------------------------------------
# Stage 5 — manifest
# ---------------------------------------------------------------------------

def build_manifest(source: str, beats: list[dict], transcript: list[dict],
                   transcript_label: str, gemini: dict, model: str | None = None) -> dict:
    """Merge per beat: ours + gemini + transcript snippet. Paths are stripped;
    the worker attaches frame asset ids / urls."""
    gemini_by_index = {b.get("index"): b for b in gemini.get("beats", []) if isinstance(b, dict)}
    enriched = []
    for b in beats:
        entry = {k: v for k, v in b.items() if k not in ("frame", "clip")}
        entry["vo"] = transcript_for_beat(transcript, b["t"], b["t_end"])
        entry["gemini"] = gemini_by_index.get(b["index"], {})
        enriched.append(entry)
    manifest = {
        "schema_version": 2,
        "source": source,
        "transcript_source": transcript_label,
        "transcript": transcript,
        "gemini_model": gemini_model(model) if gemini.get("beats") or gemini.get("overall") else None,
        "overall": gemini.get("overall", {}),
        "beats": enriched,
    }
    from adengine.gen.edit_plan import assess_analysis
    manifest["editorial"] = gemini.get("editorial", {})
    manifest["analysis"] = assess_analysis(beats, gemini)
    for k in ("_raw_gemini", "_error", "_skipped"):
        if k in gemini:
            manifest[k] = gemini[k]
    return manifest


# Detailed review is explicitly bounded. Every decoded frame in the requested
# window is supplied as an image; full-video provider sampling cannot do this.
MAX_REVIEW_FRAMES = 120


def extract_frame_window(video: str, work_dir: str, start_s: float, end_s: float) -> list[dict]:
    import math
    if not all(math.isfinite(v) for v in (start_s, end_s)) or start_s < 0 or end_s <= start_s:
        raise ProviderError("Frame window needs finite 0 <= start_s < end_s")
    if end_s > probe_duration(video) + 0.000001:
        raise ProviderError("Frame window extends beyond source duration")
    probe = shell.run([settings.ffprobe, "-v", "error", "-select_streams", "v:0",
                       "-show_frames", "-show_entries", "frame=best_effort_timestamp_time",
                       "-of", "json", video], timeout=900, check=True)
    decoded = json.loads(probe.stdout).get("frames", [])
    if not decoded or any("best_effort_timestamp_time" not in f for f in decoded):
        raise ProviderError("Source frame timestamps unavailable; cannot verify frame coverage")
    origin = float(decoded[0]["best_effort_timestamp_time"])
    selected = [{"frame_index": i, "t": float(frame["best_effort_timestamp_time"]) - origin}
                for i, frame in enumerate(decoded)
                if start_s <= float(frame["best_effort_timestamp_time"]) - origin < end_s]
    if not selected or len(selected) > MAX_REVIEW_FRAMES:
        raise ProviderError(f"Window has {len(selected)} frames; use smaller windows of 1..{MAX_REVIEW_FRAMES} "
                            "frames. No frames are silently subsampled.")
    first, last = selected[0]["frame_index"], selected[-1]["frame_index"]
    dest = os.path.join(work_dir, "detail_%04d.jpg")
    shell.run([settings.ffmpeg, "-y", "-i", video, "-vf",
               f"select='between(n,{first},{last})',scale=960:-2", "-vsync", "0",
               "-q:v", "2", dest], timeout=900, check=True)
    actual = sorted(n for n in os.listdir(work_dir) if re.fullmatch(r"detail_\d+\.jpg", n))
    if len(actual) != len(selected):
        raise ProviderError("Decoded frame count does not match timestamp ledger")
    for frame, name in zip(selected, actual):
        frame["path"] = os.path.join(work_dir, name)
    return selected


def review_frame_window(frames: list[dict], prompt: str, key: str,
                        model: str | None = None, client=None) -> dict:
    from google.genai import types
    client = client or _make_client(key)
    parts = [types.Part(text=(
        "Inspect every supplied frame in order. Frame times are source seconds, end exclusive. "
        "These are silent images: do not infer audio. Return JSON with covered_frame_indices "
        "(list every inspected index), observations (timed visual findings with confidence), "
        "and unresolved (list). Distinguish cuts, transitions, camera/subject movement and "
        "overlay animation. Do not treat a list of indices as proof of perceptual accuracy. " + prompt))]
    for frame in frames:
        parts.append(types.Part(text=f"frame_index={frame['frame_index']} source_t={frame['t']:.9f}s"))
        with open(frame["path"], "rb") as fh:
            parts.append(types.Part.from_bytes(data=fh.read(), mime_type="image/jpeg"))
    response = client.models.generate_content(
        model=gemini_model(model), contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1))
    result = parse_json_response(response.text or "")
    expected = [f["frame_index"] for f in frames]
    complete = (result.get("covered_frame_indices") == expected
                and isinstance(result.get("observations"), list)
                and bool(result["observations"])
                and result.get("unresolved") == [])
    return {"status": "complete" if complete else "incomplete", "method": "every_frame_as_image",
            "model": gemini_model(model),
            "every_frame_supplied": True, "audio_reviewed": False,
            "frame_count": len(frames), "result": result}

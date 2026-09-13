#!/usr/bin/env python3
"""
Rapid VSL Pipeline
==================
Takes a script + avatar image, segments the script into ~5-second clauses,
generates lip-synced clips via kie.ai Kling 3.0 image-to-video, and stitches
them with FFmpeg into a single VSL mp4.

Usage:
    python3 pipeline.py \\
        --script /path/to/script.txt \\
        --avatar /path/to/avatar.jpg \\
        --setting "Woman sitting in the car" \\
        --brand lunessa \\
        --concept-code RVSL_001
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

KIE_API_KEY = os.environ.get("KIE_API_KEY", "ea55b909fc9fefcb6b964e468062f2c2")
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")
BROLL_ROOT = os.path.join(VAULT_ROOT, "b-roll")

KLING_MODEL = "kling-3.0/video"
KLING_POLL_INTERVAL = 15  # seconds
KLING_MAX_WAIT = 600      # seconds per task
MAX_KLING_RETRIES = 3
RETRY_BACKOFF = 10        # seconds between retries

DEFAULT_SETTING = "Woman sitting in the car"
DEFAULT_MIN_DURATION = 4
DEFAULT_MAX_DURATION = 8
DEFAULT_DURATION = 5  # legacy fallback for --duration CLI arg
DEFAULT_MAX_WORDS = 14
HARD_WORD_CAP = 16
DEFAULT_WORKERS = 4

# Words-per-second baseline for spoken yapper-pace conversational TTS.
# 2.5 wps is the floor; with the +1.5s padding it gives natural lead-in/tail-out.
WORDS_PER_SECOND = 2.5
DURATION_PADDING_SEC = 1.5


def duration_for_words(word_count, min_dur=DEFAULT_MIN_DURATION, max_dur=DEFAULT_MAX_DURATION):
    """Map a segment's word count to a Kling clip duration in [min_dur, max_dur]."""
    raw = (word_count / WORDS_PER_SECOND) + DURATION_PADDING_SEC
    return max(min_dur, min(max_dur, int(round(raw))))


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(stage, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{stage}] {msg}", flush=True)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Stage 1: Script segmentation
# ---------------------------------------------------------------------------

# Conjunction words used as fallback split points (only matched at word boundaries)
SOFT_BREAKS = {"and", "but", "so", "or", "because"}


def segment_script(script_text, max_words=DEFAULT_MAX_WORDS, hard_cap=HARD_WORD_CAP,
                   min_dur=DEFAULT_MIN_DURATION, max_dur=DEFAULT_MAX_DURATION):
    """Split script into ~5s chunks at natural clause breaks.

    Strategy (in priority order):
      1. Sentence terminators: . ! ?
      2. Comma
      3. Conjunctions (and, but, so, or, because)
      4. Hard wrap at hard_cap words
    """
    # Strip "..." (Kling delivery breaks on triple dots — per the Loom)
    text = re.sub(r"\.{2,}", " ", script_text)
    # Em-dashes and en-dashes function as spoken pause/break points — convert to commas
    # so the segmenter can split on them.
    text = re.sub(r"\s*[—–]\s*", ", ", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    # Tokenize into words, keeping trailing punctuation attached
    words = text.split(" ")
    segments = []
    buf = []

    def flush():
        if buf:
            seg_text = " ".join(buf).strip()
            seg_text = re.sub(r"\s+", " ", seg_text)
            if seg_text:
                segments.append(seg_text)
            buf.clear()

    i = 0
    while i < len(words):
        buf.append(words[i])
        i += 1
        wc = len(buf)

        if wc < 4:
            # Don't split too early — segments need to feel like clauses
            continue

        last = buf[-1]
        last_clean = re.sub(r"[^\w]", "", last).lower()

        # Priority 1: hit a sentence terminator
        if re.search(r"[.!?]$", last):
            if wc >= 4:
                flush()
                continue

        # Priority 2: at target length and last char is a comma
        if wc >= max_words - 2 and last.endswith(","):
            flush()
            continue

        # Priority 3: at target length and we're on a conjunction (look back one)
        if wc >= max_words - 1 and last_clean in SOFT_BREAKS:
            # Pop the conjunction back so it starts the next segment
            popped = buf.pop()
            flush()
            buf.append(popped)
            continue

        # Priority 4: hard cap
        if wc >= hard_cap:
            flush()
            continue

    flush()

    # Build segment dicts
    out = []
    for idx, seg in enumerate(segments, start=1):
        # Clean trailing commas/conjunctions that look ugly mid-clip
        clean = seg.strip().rstrip(",")
        # Ensure a terminator so Kling's TTS reads it as a complete phrase
        if not re.search(r"[.!?]$", clean):
            clean += "."
        wc = len(clean.split())
        out.append({
            "index": idx,
            "text": clean,
            "word_count": wc,
            "duration": duration_for_words(wc, min_dur, max_dur),
        })

    return out


# ---------------------------------------------------------------------------
# Stage 2: Avatar upload (one-time)
# ---------------------------------------------------------------------------

def ensure_kling_compatible_format(image_path):
    """kie.ai's Kling endpoint only accepts jpg/jpeg/png. Auto-convert anything
    else (webp, heic, gif, etc.) to PNG using ffmpeg. Returns a path to the
    converted file (or the original path if it's already a supported format)."""
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    if ext in ("jpg", "jpeg", "png"):
        return image_path

    log("upload", f"Converting {ext} → png for Kling compatibility...")
    base = os.path.splitext(os.path.basename(image_path))[0]
    converted_path = os.path.join("/tmp", f"rapid_vsl_{base}_{int(time.time())}.png")
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", image_path, "-frames:v", "1", converted_path],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not os.path.exists(converted_path):
        log("upload", f"  ffmpeg conversion failed: {result.stderr[-300:]}")
        return None
    log("upload", f"  Converted to: {converted_path}")
    return converted_path


def upload_image(image_path):
    """Upload image to a temp host so kie.ai can fetch it via URL.
    Order: litterbox (catbox infra, no auth) → tmpfiles.org → 0x0.st.
    Auto-converts webp/heic/etc → png before upload (Kling only accepts jpg/png)."""
    if not os.path.exists(image_path):
        log("upload", f"Avatar not found: {image_path}")
        return None

    # Convert to a Kling-supported format if needed
    image_path = ensure_kling_compatible_format(image_path)
    if image_path is None:
        return None

    fname = os.path.basename(image_path).replace(" ", "_")

    # Primary: litterbox.catbox.moe (no auth, direct HTTPS, 1h expiry)
    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://litterbox.catbox.moe/resources/internals/api.php",
                data={"reqtype": "fileupload", "time": "1h"},
                files={"fileToUpload": (fname, f)},
                timeout=120,
            )
        body = resp.text.strip()
        if resp.status_code == 200 and body.startswith("http"):
            log("upload", f"Avatar uploaded (litterbox): {body}")
            return body
        log("upload", f"litterbox returned {resp.status_code}: {body[:100]}, trying tmpfiles...")
    except Exception as e:
        log("upload", f"litterbox error: {e}, trying tmpfiles...")

    # Fallback 1: tmpfiles.org (returns viewer URL — convert to /dl/ for direct)
    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://tmpfiles.org/api/v1/upload",
                files={"file": (fname, f)},
                timeout=120,
            )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                viewer_url = data["data"]["url"]
                # Convert tmpfiles.org/<id>/file → tmpfiles.org/dl/<id>/file
                direct_url = viewer_url.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1)
                # Force https
                if direct_url.startswith("http://"):
                    direct_url = "https://" + direct_url[7:]
                log("upload", f"Avatar uploaded (tmpfiles): {direct_url}")
                return direct_url
        log("upload", f"tmpfiles returned {resp.status_code}, trying 0x0.st...")
    except Exception as e:
        log("upload", f"tmpfiles error: {e}, trying 0x0.st...")

    # Fallback 2: 0x0.st
    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://0x0.st",
                files={"file": (fname, f)},
                data={"expires": "24"},
                headers={"User-Agent": "rapid-vsl/1.0"},
                timeout=120,
            )
        body = resp.text.strip()
        if resp.status_code == 200 and body.startswith("http"):
            log("upload", f"Avatar uploaded (0x0.st): {body}")
            return body
        log("upload", f"0x0.st returned {resp.status_code}: {body[:100]}")
    except Exception as e:
        log("upload", f"0x0.st error: {e}")

    return None


# ---------------------------------------------------------------------------
# Stage 3: kie.ai Kling dispatch
# ---------------------------------------------------------------------------

def submit_kling_task(prompt, image_url, duration, sound):
    """Submit a Kling 3.0 task to kie.ai. Returns task_id or None."""
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": KLING_MODEL,
        "input": {
            "prompt": prompt,
            "image_urls": [image_url],
            "sound": sound,
            "duration": str(duration),
            "aspect_ratio": "9:16",
            "mode": "pro",
            "multi_shots": False,
        },
    }
    try:
        resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
        data = resp.json()
        if data.get("code") != 200:
            log("kling", f"  Submit failed: {data.get('msg', 'unknown error')}")
            return None
        return data["data"]["taskId"]
    except Exception as e:
        log("kling", f"  Submit exception: {e}")
        return None


def poll_kling_task(task_id, max_wait=KLING_MAX_WAIT):
    """Poll a Kling task until complete or timeout. Returns video URL or None."""
    headers = {"Authorization": f"Bearer {KIE_API_KEY}"}
    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(
                KIE_STATUS_URL,
                headers=headers,
                params={"taskId": task_id},
                timeout=30,
            )
            data = resp.json()
            if data.get("code") != 200:
                time.sleep(KLING_POLL_INTERVAL)
                continue

            state = data["data"].get("state", "")
            if state == "success":
                result_json = json.loads(data["data"].get("resultJson", "{}"))
                urls = result_json.get("resultUrls", [])
                if urls:
                    return urls[0]
                return None
            elif state == "fail":
                fail_msg = data["data"].get("failMsg", "unknown")
                log("kling", f"    Task {task_id[:8]} failed: {fail_msg}")
                return None
        except Exception as e:
            log("kling", f"    Poll error for {task_id[:8]}: {e}")

        time.sleep(KLING_POLL_INTERVAL)

    log("kling", f"    Timeout waiting for {task_id[:8]}")
    return None


def generate_clip(segment, avatar_url, setting, sound, clips_dir):
    """End-to-end: submit → poll → download for one segment.
    Reads per-segment `duration` from segment dict (set by segment_script).
    Returns dict with status + path + metadata."""
    idx = segment["index"]
    duration = segment.get("duration", DEFAULT_DURATION)
    out_path = os.path.join(clips_dir, f"clip_{idx:03d}.mp4")

    # Resume support
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        log("kling", f"  Segment {idx:03d}: cached")
        return {
            "index": idx,
            "text": segment["text"],
            "video_path": out_path,
            "task_id": "cached",
            "status": "cached",
        }

    prompt = f'{setting} says: "{segment["text"]}"'
    log("kling", f"  Segment {idx:03d} ({duration}s): {prompt[:70]}...")

    last_task_id = None
    for attempt in range(1, MAX_KLING_RETRIES + 1):
        task_id = submit_kling_task(prompt, avatar_url, duration, sound)
        if not task_id:
            log("kling", f"  Segment {idx:03d}: submit attempt {attempt} failed")
            time.sleep(RETRY_BACKOFF)
            continue
        last_task_id = task_id
        log("kling", f"  Segment {idx:03d}: task {task_id[:8]} submitted (attempt {attempt})")

        video_url = poll_kling_task(task_id)
        if not video_url:
            log("kling", f"  Segment {idx:03d}: attempt {attempt} did not return a video")
            time.sleep(RETRY_BACKOFF)
            continue

        # Download
        try:
            vid_resp = requests.get(video_url, timeout=180)
            with open(out_path, "wb") as f:
                f.write(vid_resp.content)
            size_kb = os.path.getsize(out_path) // 1024
            log("kling", f"  Segment {idx:03d}: saved ({size_kb} KB)")
            return {
                "index": idx,
                "text": segment["text"],
                "prompt": prompt,
                "video_path": out_path,
                "task_id": task_id,
                "status": "success",
            }
        except Exception as e:
            log("kling", f"  Segment {idx:03d}: download failed: {e}")
            time.sleep(RETRY_BACKOFF)

    return {
        "index": idx,
        "text": segment["text"],
        "prompt": prompt,
        "video_path": None,
        "task_id": last_task_id,
        "status": "failed",
    }


def generate_all_clips(segments, avatar_urls, setting, sound, clips_dir, workers):
    """Run generate_clip in parallel, in segment order on completion.
    avatar_urls: list of length == len(segments), one URL per segment (allows mid-video swap)."""
    results = [None] * len(segments)
    assert len(avatar_urls) == len(segments), "avatar_urls must match segments length"

    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_idx = {
            pool.submit(generate_clip, seg, avatar_urls[i], setting, sound, clips_dir): i
            for i, seg in enumerate(segments)
        }
        for fut in as_completed(future_to_idx):
            i = future_to_idx[fut]
            try:
                results[i] = fut.result()
            except Exception as e:
                log("kling", f"  Worker exception on segment {i+1}: {e}")
                results[i] = {
                    "index": segments[i]["index"],
                    "text": segments[i]["text"],
                    "video_path": None,
                    "status": "exception",
                }

    return results


# ---------------------------------------------------------------------------
# Stage 4: FFmpeg stitch
# ---------------------------------------------------------------------------

def get_clip_duration(clip_path):
    """Return clip duration in seconds, or None on failure."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", clip_path],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return None


# Silence detection params for trimming Kling clip dead air at start/end.
# -25 dB sits between the typical mean (-23 dB) and noise floor — catches the
# 0.5–1.5s of dead air Kling adds before/after each spoken line, while
# preserving natural mid-speech breathing pauses.
SILENCE_THRESHOLD_DB = -25
MIN_SILENCE_SEC = 0.3
TRIM_SAFETY_MARGIN_SEC = 0.05  # tiny pad so we don't cut off the first/last consonant


def detect_speech_range(clip_path):
    """Run silencedetect on the clip and return (speech_start, speech_end).
    Trims leading/trailing silence only — internal silences are preserved.
    Returns (0.0, duration) if no leading/trailing silence is found."""
    duration = get_clip_duration(clip_path)
    if duration is None:
        return (0.0, None)

    cmd = [
        "ffmpeg", "-i", clip_path,
        "-af", f"silencedetect=noise={SILENCE_THRESHOLD_DB}dB:d={MIN_SILENCE_SEC}",
        "-f", "null", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    # Parse silence_start / silence_end pairs in order
    silences = []
    current_start = None
    for line in stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            current_start = float(m.group(1))
            continue
        m = re.search(r"silence_end:\s*(-?[\d.]+)", line)
        if m and current_start is not None:
            silences.append((max(0.0, current_start), float(m.group(1))))
            current_start = None
    # Handle a trailing silence that runs to EOF (silence_start with no silence_end)
    if current_start is not None:
        silences.append((max(0.0, current_start), duration))

    speech_start = 0.0
    speech_end = duration

    # If first silence starts at (or near) 0, trim it
    if silences and silences[0][0] <= 0.05:
        speech_start = silences[0][1] - TRIM_SAFETY_MARGIN_SEC
        speech_start = max(0.0, speech_start)

    # If last silence ends at (or near) end-of-clip, trim it
    if silences and silences[-1][1] >= duration - 0.05:
        speech_end = silences[-1][0] + TRIM_SAFETY_MARGIN_SEC
        speech_end = min(duration, speech_end)

    # Sanity: don't trim away the entire clip (fallback to full duration)
    if speech_end - speech_start < 0.3:
        return (0.0, duration)

    return (speech_start, speech_end)


def normalize_clip(src_path, dst_path, trim_silence=True):
    """Normalize a single clip to 1080x1920/30fps/h264/aac, preserving audio.
    When trim_silence is True, also trims leading/trailing silence from the clip
    so concatenated output has no dead air between segments."""
    ss, to = (None, None)
    if trim_silence:
        speech_start, speech_end = detect_speech_range(src_path)
        if speech_end is not None and (speech_start > 0 or speech_end < (get_clip_duration(src_path) or 0) - 0.05):
            ss, to = speech_start, speech_end
            log("stitch", f"  Trim {os.path.basename(src_path)}: {speech_start:.2f}s → {speech_end:.2f}s")

    cmd = ["ffmpeg", "-y"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.3f}"]
    cmd += ["-i", src_path]
    if to is not None and ss is not None:
        cmd += ["-t", f"{(to - ss):.3f}"]
    cmd += [
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,"
               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-r", "30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-avoid_negative_ts", "make_zero",
        dst_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(dst_path):
        log("stitch", f"  Normalize failed for {os.path.basename(src_path)}: {result.stderr[-300:]}")
        return False
    return True


def stitch_clips(clip_results, output_dir):
    """Normalize → concat all successful clips into final/final_output.mp4."""
    final_dir = ensure_dir(os.path.join(output_dir, "final"))
    norm_dir = ensure_dir(os.path.join(output_dir, "normalized"))

    successful = [r for r in clip_results if r and r.get("video_path") and os.path.exists(r["video_path"])]
    if not successful:
        log("stitch", "No successful clips to stitch")
        return None

    successful.sort(key=lambda r: r["index"])
    log("stitch", f"Normalizing {len(successful)} clips...")

    normalized_paths = []
    for r in successful:
        norm_path = os.path.join(norm_dir, f"norm_{r['index']:03d}.mp4")
        if os.path.exists(norm_path) and os.path.getsize(norm_path) > 0:
            normalized_paths.append(norm_path)
            continue
        ok = normalize_clip(r["video_path"], norm_path)
        if ok:
            normalized_paths.append(norm_path)
        else:
            log("stitch", f"  Skipping clip {r['index']:03d} due to normalize failure")

    if not normalized_paths:
        log("stitch", "All clips failed to normalize")
        return None

    # Write concat list
    concat_list_path = os.path.join(final_dir, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for p in normalized_paths:
            # FFmpeg concat demuxer requires escaping single quotes in paths
            esc = p.replace("'", r"'\''")
            f.write(f"file '{esc}'\n")

    final_path = os.path.join(final_dir, "final_output.mp4")
    log("stitch", f"Concatenating {len(normalized_paths)} normalized clips...")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        final_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(final_path):
        log("stitch", f"Concat failed: {result.stderr[-500:]}")
        return None

    size_mb = os.path.getsize(final_path) / (1024 * 1024)
    log("stitch", f"Final video: {final_path} ({size_mb:.1f} MB)")
    return final_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Rapid VSL — script → talking-head clips → stitched mp4"
    )
    parser.add_argument("--script", required=True, help="Path to VSL script text file")
    parser.add_argument("--avatar", required=True, help="Path to primary avatar image (vertical jpg/png)")
    parser.add_argument("--secondary-avatar", default=None,
                        help="Optional second avatar image. Used from --secondary-trigger segment onwards "
                             "(e.g. swap to a 'holding product' shot when the brand is first mentioned).")
    parser.add_argument("--secondary-trigger", default=None,
                        help="Keyword (case-insensitive). The first segment whose text contains this keyword "
                             "is where the secondary avatar takes over for the rest of the video.")
    parser.add_argument("--setting", default=DEFAULT_SETTING,
                        help=f'Prompt prefix. Default: "{DEFAULT_SETTING}"')
    parser.add_argument("--brand", default="test", help="Brand slug for output dir (default: test)")
    parser.add_argument("--concept-code", default=None,
                        help="Output subfolder name (default: RVSL_<timestamp>)")
    parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS,
                        help=f"Target words per segment (default: {DEFAULT_MAX_WORDS})")
    parser.add_argument("--min-duration", type=int, default=DEFAULT_MIN_DURATION,
                        help=f"Min seconds per Kling clip (default: {DEFAULT_MIN_DURATION})")
    parser.add_argument("--max-duration", type=int, default=DEFAULT_MAX_DURATION,
                        help=f"Max seconds per Kling clip (default: {DEFAULT_MAX_DURATION})")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                        help=f"Parallel kie.ai workers (default: {DEFAULT_WORKERS})")
    parser.add_argument("--no-audio", action="store_true",
                        help="Pass sound:false to Kling (default sound:true)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Just segment the script and print — don't call kie.ai or ffmpeg")
    args = parser.parse_args()

    # ---- Validate inputs ----
    if not os.path.exists(args.script):
        log("init", f"Script not found: {args.script}")
        sys.exit(1)
    if not os.path.exists(args.avatar):
        log("init", f"Avatar not found: {args.avatar}")
        sys.exit(1)
    if args.secondary_avatar and not os.path.exists(args.secondary_avatar):
        log("init", f"Secondary avatar not found: {args.secondary_avatar}")
        sys.exit(1)
    if args.secondary_avatar and not args.secondary_trigger:
        log("init", "--secondary-avatar requires --secondary-trigger")
        sys.exit(1)
    if not args.dry_run and not shutil.which("ffmpeg"):
        log("init", "ffmpeg not found on PATH")
        sys.exit(1)

    min_dur = max(3, min(args.min_duration, 10))
    max_dur = max(min_dur, min(args.max_duration, 10))

    concept_code = args.concept_code or f"RVSL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    brand = args.brand.lower()
    output_dir = ensure_dir(os.path.join(BROLL_ROOT, brand, concept_code))
    clips_dir = ensure_dir(os.path.join(output_dir, "clips"))

    log("init", f"Brand: {brand}")
    log("init", f"Concept: {concept_code}")
    log("init", f"Output: {output_dir}")
    log("init", f"Duration range: {min_dur}–{max_dur}s")

    # ---- Stage 1: Segment ----
    with open(args.script, "r") as f:
        script_text = f.read()

    segments = segment_script(script_text, max_words=args.max_words,
                              min_dur=min_dur, max_dur=max_dur)
    log("segment", f"Parsed script into {len(segments)} segments")
    for s in segments:
        log("segment", f"  [{s['index']:03d}] ({s['word_count']}w → {s['duration']}s) {s['text']}")

    # ---- Determine secondary avatar trigger point ----
    secondary_start_idx = None
    if args.secondary_avatar and args.secondary_trigger:
        trigger = args.secondary_trigger.lower()
        for s in segments:
            if trigger in s["text"].lower():
                secondary_start_idx = s["index"]
                break
        if secondary_start_idx is None:
            log("init", f"WARNING: secondary trigger '{args.secondary_trigger}' not found "
                        f"in any segment — secondary avatar will NOT be used")
        else:
            count = len(segments) - secondary_start_idx + 1
            log("init", f"Secondary avatar starts at segment {secondary_start_idx:03d} "
                        f"(matched '{args.secondary_trigger}') — {count} segments use it")

    segments_path = os.path.join(output_dir, "segments.json")
    with open(segments_path, "w") as f:
        json.dump({
            "setting": args.setting,
            "min_duration": min_dur,
            "max_duration": max_dur,
            "secondary_start_idx": secondary_start_idx,
            "segments": segments,
        }, f, indent=2)

    if args.dry_run:
        log("done", "Dry run — exiting after segmentation")
        return

    # ---- Stage 2: Upload avatar(s) ----
    log("upload", f"Uploading primary avatar: {args.avatar}")
    primary_url = upload_image(args.avatar)
    if not primary_url:
        log("upload", "Primary avatar upload failed — aborting")
        sys.exit(1)

    secondary_url = None
    if args.secondary_avatar and secondary_start_idx is not None:
        log("upload", f"Uploading secondary avatar: {args.secondary_avatar}")
        secondary_url = upload_image(args.secondary_avatar)
        if not secondary_url:
            log("upload", "Secondary avatar upload failed — falling back to primary only")

    # Build per-segment avatar URL list
    avatar_urls = []
    for s in segments:
        if secondary_url and secondary_start_idx and s["index"] >= secondary_start_idx:
            avatar_urls.append(secondary_url)
        else:
            avatar_urls.append(primary_url)

    # ---- Stage 3: Generate clips ----
    log("kling", f"Dispatching {len(segments)} segments to Kling 3.0 (workers={args.workers})...")
    sound = not args.no_audio
    clip_results = generate_all_clips(
        segments, avatar_urls, args.setting, sound, clips_dir, args.workers
    )

    # Write manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump({
            "concept_code": concept_code,
            "brand": brand,
            "setting": args.setting,
            "min_duration": min_dur,
            "max_duration": max_dur,
            "sound": sound,
            "primary_avatar_url": primary_url,
            "secondary_avatar_url": secondary_url,
            "secondary_start_idx": secondary_start_idx,
            "clips": clip_results,
        }, f, indent=2, default=str)

    succeeded = sum(1 for r in clip_results if r and r["status"] in ("success", "cached"))
    log("kling", f"Generation complete: {succeeded}/{len(segments)} segments succeeded")

    if succeeded == 0:
        log("kling", "No clips succeeded — cannot stitch")
        sys.exit(2)

    # ---- Stage 4: Stitch ----
    final_path = stitch_clips(clip_results, output_dir)
    if not final_path:
        log("stitch", "Stitch failed")
        sys.exit(3)

    log("done", f"✅ Final VSL: {final_path}")


if __name__ == "__main__":
    main()

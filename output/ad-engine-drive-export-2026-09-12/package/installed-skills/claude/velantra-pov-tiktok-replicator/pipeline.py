#!/usr/bin/env python3
"""
velantra-pov-tiktok-replicator pipeline.

Stages:
  1. Download TikTok + extract audio + transcript        (yt-dlp + ffmpeg)
  2. Scene-detected frame extraction + per-scene audio   (ffmpeg)
  3. Gemini scene analysis                               (google-genai, gemini-2.5-pro)
  4. Opus 4.7 creative direction                         (anthropic, claude-opus-4-7)
  5. GPT Image 2 keyframes (POV hook text baked in)      (higgsfield CLI, gpt_image_2)
  6. Seedance 2.0 animation (music baked in via --audio) (higgsfield CLI, seedance_2_0)
  7. ffmpeg concat-only finalize

Each stage checkpoints to disk. Re-running with the same --output-dir resumes.
"""

import argparse
import base64
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

VELANTRA_ROOT = Path(
    os.path.expanduser(
        "~/Documents/marketing brain/statics/product references/velantra"
    )
)

PRODUCT_REGISTRY = {
    "velantra-meridian": {
        "dir": VELANTRA_ROOT / "meridian",
        "context": (
            "Velantra Meridian — Birkin-inspired structured handbag in full premium "
            "pebbled leather (single color, no canvas, no two-tone). Silver/palladium "
            "turn-lock clasp, silver buckle accents, silver feet. Two rigid top handles "
            "in matching leather. Front belt strap through flap. Wider than tall, clean "
            "geometric lines."
        ),
        "available_colorways": [
            "black", "brown", "coffee brown", "gray", "white",
            "green", "burgundy", "light blue", "ultra light blue",
        ],
    },
    "velantra-boat-tote": {
        "dir": VELANTRA_ROOT / "boat tote",
        "context": (
            "Velantra Boat Tote — canvas-and-leather two-tone tote with gold hardware, "
            "Birkin-inspired silhouette. Canvas body with leather trim, handles, and "
            "base. Also available in fully solid-color leather variants."
        ),
        "available_colorways": [
            "navy", "red", "pink", "dark green", "olive green", "orange",
            "sunny yellow", "yellow", "emerald green", "lady pink", "light grey",
            "lineman", "solid green", "solid navy", "solid olive green",
            "solid orange", "solid pink", "solid red", "solid yellow",
        ],
    },
    "velantra-weekender": {
        "dir": VELANTRA_ROOT / "weekender",
        "context": (
            "Velantra Weekender — canvas-and-leather travel weekender bag. Two colorways: "
            "olive canvas with cognac leather trim, and light chocolate canvas with cream "
            "leather trim. Gold hardware, top zip closure, dual top handles + detachable "
            "long strap."
        ),
        "available_colorways": [
            "olive cognac", "light chocolate cream",
        ],
    },
}

DEFAULT_PRODUCT = "velantra-meridian"
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-pro-preview")

# Auto-load API keys from ~/.config/velantra-pov-tiktok-replicator/.env (key=value, one per line)
_CONFIG_ENV = Path.home() / ".config" / "velantra-pov-tiktok-replicator" / ".env"
if _CONFIG_ENV.exists():
    for _line in _CONFIG_ENV.read_text().splitlines():
        _line = _line.strip()
        if not _line or _line.startswith("#") or "=" not in _line:
            continue
        _k, _v = _line.split("=", 1)
        _k, _v = _k.strip(), _v.strip().strip('"').strip("'")
        os.environ.setdefault(_k, _v)


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def run(cmd, **kw):
    print(f"  $ {' '.join(shlex.quote(c) for c in cmd)}", flush=True)
    return subprocess.run(cmd, check=True, **kw)


def run_capture(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def ensure_tools():
    missing = []
    for tool in ("yt-dlp", "ffmpeg", "ffprobe", "higgsfield"):
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=False)
        except FileNotFoundError:
            missing.append(tool)
    if missing:
        sys.exit(
            f"[fatal] Missing tools: {', '.join(missing)}. "
            f"Install: brew install yt-dlp ffmpeg ; higgsfield CLI: see docs.higgsfield.ai"
        )
    r = subprocess.run(["higgsfield", "account", "status"], capture_output=True, text=True)
    if r.returncode != 0 or "expired" in (r.stdout + r.stderr).lower():
        sys.exit("[fatal] higgsfield not authenticated. Run: higgsfield auth login")


def ffprobe_duration(path):
    r = run_capture([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(r.stdout.strip())


def strip_json_fence(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t


# -----------------------------------------------------------------------------
# Stage 1 — Download + audio + transcript
# -----------------------------------------------------------------------------

def stage1_download(url: str, outdir: Path) -> dict:
    ref_video = outdir / "reference.mp4"
    audio = outdir / "original_audio.m4a"
    transcript_path = outdir / "transcript.txt"

    if ref_video.exists() and audio.exists():
        print(f"[stage1] cached → {ref_video.name}, {audio.name}")
    else:
        print("[stage1] downloading TikTok via yt-dlp…")
        tmp_template = str(outdir / "reference.%(ext)s")
        run([
            "yt-dlp",
            "-f", "mp4/bestvideo*+bestaudio/best",
            "--merge-output-format", "mp4",
            "--write-auto-subs", "--write-subs",
            "--sub-langs", "en.*,en",
            "--convert-subs", "srt",
            "-o", tmp_template,
            url,
        ])
        candidates = list(outdir.glob("reference.*"))
        mp4s = [c for c in candidates if c.suffix.lower() == ".mp4"]
        if not mp4s:
            sys.exit("[stage1] yt-dlp did not produce an mp4")
        if mp4s[0] != ref_video:
            mp4s[0].rename(ref_video)

        run([
            "ffmpeg", "-y", "-i", str(ref_video),
            "-vn", "-c:a", "aac", "-b:a", "192k", str(audio),
        ])

    if not transcript_path.exists():
        srt_files = list(outdir.glob("reference*.srt"))
        if srt_files:
            txt = srt_to_text(srt_files[0].read_text(encoding="utf-8", errors="ignore"))
            transcript_path.write_text(txt, encoding="utf-8")
            print(f"[stage1] transcript from native captions ({len(txt)} chars)")
        else:
            txt = whisper_transcribe(audio) or ""
            transcript_path.write_text(txt, encoding="utf-8")
            print(f"[stage1] transcript from Whisper ({len(txt)} chars)" if txt
                  else "[stage1] no transcript available")

    return {
        "video": ref_video,
        "audio": audio,
        "transcript": transcript_path,
        "duration": ffprobe_duration(ref_video),
    }


def srt_to_text(srt: str) -> str:
    lines = []
    for block in re.split(r"\n\s*\n", srt.strip()):
        rows = block.splitlines()
        if len(rows) >= 3:
            text = " ".join(rows[2:]).strip()
            if text:
                lines.append(text)
    return "\n".join(lines)


def whisper_transcribe(audio: Path) -> str:
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    try:
        import requests
    except ImportError:
        return ""
    if groq_key:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {groq_key}"},
                files={"file": (audio.name, audio.open("rb"), "audio/m4a")},
                data={"model": "whisper-large-v3", "response_format": "text"},
                timeout=120,
            )
            if r.ok:
                return r.text
        except Exception as e:
            print(f"[stage1] groq whisper failed: {e}")
    if openai_key:
        try:
            r = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {openai_key}"},
                files={"file": (audio.name, audio.open("rb"), "audio/m4a")},
                data={"model": "whisper-1", "response_format": "text"},
                timeout=120,
            )
            if r.ok:
                return r.text
        except Exception as e:
            print(f"[stage1] openai whisper failed: {e}")
    return ""


# -----------------------------------------------------------------------------
# Stage 2 — Frame extraction + per-scene audio slicing
# -----------------------------------------------------------------------------

def stage2_frames(ref_video: Path, full_audio: Path, duration: float, outdir: Path) -> list[dict]:
    scenes_dir = outdir / "scenes"
    scenes_dir.mkdir(exist_ok=True)
    scenes_json = scenes_dir / "scenes.json"

    if scenes_json.exists():
        scenes = json.loads(scenes_json.read_text())
        print(f"[stage2] cached → {len(scenes)} scenes")
        return scenes

    print(f"[stage2] detecting scenes in {ref_video.name} (duration {duration:.1f}s)…")
    r = subprocess.run([
        "ffmpeg", "-i", str(ref_video),
        "-vf", "select='gt(scene,0.25)',showinfo",
        "-vsync", "vfr",
        "-f", "null", "-",
    ], capture_output=True, text=True)
    scene_times = []
    for line in r.stderr.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            scene_times.append(float(m.group(1)))
    scene_times = sorted(set([0.0] + scene_times))

    # Densify short videos to ensure on-screen text moments aren't missed
    if duration <= 30:
        t = 0.0
        while t < duration:
            if not any(abs(t - s) < 2.0 for s in scene_times):
                scene_times.append(t)
            t += 3.0
        scene_times = sorted(set(scene_times))

    scene_times = scene_times[:60]

    scenes = []
    for i, start in enumerate(scene_times, start=1):
        end = scene_times[i] if i < len(scene_times) else duration
        scene_duration = max(0.5, end - start)
        frame_path = scenes_dir / f"scene_{i:03d}.jpg"
        clip_path = scenes_dir / f"scene_{i:03d}_clip.mp4"
        audio_slice = scenes_dir / f"scene_{i:03d}_audio.m4a"

        keyframe_t = start + min(0.25, scene_duration * 0.25)
        run([
            "ffmpeg", "-y", "-ss", f"{keyframe_t}", "-i", str(ref_video),
            "-frames:v", "1", "-q:v", "2", str(frame_path),
        ])
        run([
            "ffmpeg", "-y", "-ss", f"{start}", "-i", str(ref_video),
            "-t", f"{scene_duration}",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            str(clip_path),
        ])
        # Per-scene audio slice — Seedance gets the music slice that matches this scene's source time
        run([
            "ffmpeg", "-y", "-ss", f"{start}", "-i", str(full_audio),
            "-t", f"{scene_duration}",
            "-c:a", "aac", "-b:a", "192k",
            str(audio_slice),
        ])

        scenes.append({
            "index": i,
            "start_time": start,
            "end_time": end,
            "duration": scene_duration,
            "frame": str(frame_path),
            "clip": str(clip_path),
            "audio_slice": str(audio_slice),
        })

    scenes_json.write_text(json.dumps(scenes, indent=2))
    print(f"[stage2] extracted {len(scenes)} scenes (with per-scene audio slices)")
    return scenes


# -----------------------------------------------------------------------------
# Stage 3 — Gemini scene analysis
# -----------------------------------------------------------------------------

def stage3_gemini_analysis(scenes: list[dict], transcript: str, outdir: Path) -> dict:
    analysis_path = outdir / "analysis" / "gemini_analysis.json"
    analysis_path.parent.mkdir(exist_ok=True)
    if analysis_path.exists():
        print(f"[stage3] cached → {analysis_path}")
        return json.loads(analysis_path.read_text())

    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        sys.exit("[stage3] pip install google-genai")

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("[stage3] GEMINI_API_KEY env var required")

    client = genai.Client()

    parts = []
    parts.append(genai_types.Part.from_text(text=
        f"You are analyzing a TikTok POV video frame by frame to produce structured scene data "
        f"for a downstream creative pipeline.\n\n"
        f"TRANSCRIPT (may be empty for music-only TikToks):\n{transcript or '(none)'}\n\n"
        f"There are {len(scenes)} scenes below. Each frame is labeled with its index and timing.\n"
    ))

    for s in scenes:
        with open(s["frame"], "rb") as f:
            img_bytes = f.read()
        parts.append(genai_types.Part.from_text(text=
            f"--- Scene {s['index']} | start={s['start_time']:.2f}s end={s['end_time']:.2f}s "
            f"duration={s['duration']:.2f}s ---"
        ))
        parts.append(genai_types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))

    parts.append(genai_types.Part.from_text(text=
        "Now produce structured JSON describing the video. Output ONLY JSON, no commentary, "
        "no markdown fences. Schema:\n"
        "{\n"
        '  "global": {\n'
        '    "dominant_palette": [<3-5 color descriptors>],\n'
        '    "lighting_mood": "<one sentence>",\n'
        '    "estimated_pov_subject": "<bag|shoes|jewelry|food|etc>",\n'
        '    "overall_vibe": "<one sentence>",\n'
        '    "pov_overlay_text": [\n'
        '      {"text": "<exact on-screen text>", "start": <float seconds>, "end": <float seconds>, '
        '"position": "top|middle|bottom", "font_style": "tiktok_white_drop_shadow|other"}\n'
        '    ]\n'
        '  },\n'
        '  "scenes": [\n'
        '    {\n'
        '      "index": 1,\n'
        '      "composition": "<framing, angle, depth>",\n'
        '      "key_elements": [<objects/people/text visible>],\n'
        '      "motion": "<camera motion + subject motion>",\n'
        '      "lighting": "<direction, quality, color>",\n'
        '      "background": "<environment>",\n'
        '      "contains_bag": <true|false>\n'
        '    }\n'
        '  ]\n'
        "}\n\n"
        "Be precise about pov_overlay_text — extract the EXACT text visible on screen, its "
        "real start/end timestamps in seconds, and its position. Empty array if no overlay text."
    ))

    print(f"[stage3] sending {len(scenes)} frames to {GEMINI_MODEL}…")
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[genai_types.Content(role="user", parts=parts)],
        config=genai_types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )
    raw = strip_json_fence(resp.text)
    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError as e:
        (analysis_path.parent / "gemini_raw.txt").write_text(raw)
        sys.exit(f"[stage3] Gemini did not return valid JSON: {e}")

    analysis_path.write_text(json.dumps(analysis, indent=2))
    overlay_count = len(analysis.get("global", {}).get("pov_overlay_text", []))
    print(f"[stage3] ✓ {len(analysis.get('scenes', []))} scenes analyzed, "
          f"{overlay_count} overlay text entries detected")
    return analysis


# -----------------------------------------------------------------------------
# Stage 4 — Opus 4.7 creative direction (CHECKPOINT — Claude writes this file
# directly between runs; no API call, no anthropic SDK)
# -----------------------------------------------------------------------------

def stage4_opus_direction(product_key: str, forced_colorway: str | None, outdir: Path) -> dict:
    """
    This stage is performed by Claude (the assistant running this skill), not by an
    API call. The pipeline halts here on the first pass; Claude then reads
    `analysis/gemini_analysis.json`, applies brand judgment, and writes
    `analysis/opus_directions.json`. Re-running the pipeline resumes from Stage 5.
    """
    directions_path = outdir / "analysis" / "opus_directions.json"
    if directions_path.exists():
        directions = json.loads(directions_path.read_text())
        pov_scenes = sum(1 for s in directions.get("scenes", []) if s.get("include_pov_hook"))
        print(f"[stage4] ✓ directions loaded — colorway: {directions.get('selected_colorway')}, "
              f"{len(directions.get('scenes', []))} scenes, {pov_scenes} carry POV hook text")
        return directions

    gemini_path = outdir / "analysis" / "gemini_analysis.json"
    product = PRODUCT_REGISTRY[product_key]
    colorway_directive = (
        f"FORCED colorway: \"{forced_colorway}\""
        if forced_colorway else
        f"AUTO-PICK from: {product['available_colorways']}"
    )

    print("\n" + "=" * 72)
    print("[stage4] HALT — Claude (Opus 4.7) must produce creative direction now.")
    print("=" * 72)
    print(f"  Read:    {gemini_path}")
    print(f"  Write:   {directions_path}")
    print(f"  Product: {product_key}")
    print(f"           {product['context']}")
    print(f"  Colorway: {colorway_directive}")
    print()
    print("  Schema for opus_directions.json (see SKILL.md 'Stage 4' for full prompt rules):")
    print("    {")
    print('      "selected_colorway": "<one of the available colorways>",')
    print('      "colorway_justification": "<one sentence>",')
    print('      "scenes": [{')
    print('        "index": 1, "duration_seconds": 1.8,')
    print('        "image_prompt": "<dense paragraph for gpt_image_2; if this scene overlaps a')
    print('                         pov_overlay_text entry from Gemini, BAKE the exact text into')
    print('                         the prompt with TikTok-style typography direction>",')
    print('        "include_product_reference": true,')
    print('        "include_pov_hook": true,')
    print('        "pov_hook_text": "<exact text or empty>",')
    print('        "motion_prompt": "<short camera/subject motion for seedance_2_0>",')
    print('        "transition_to_next": "hard_cut" or "smooth_morph"')
    print('      }, ...]')
    print("    }")
    print()
    print("  After writing the file, re-run this pipeline with the same --output-dir.")
    print("=" * 72)
    sys.exit(0)


# -----------------------------------------------------------------------------
# Stage 5 — GPT Image 2 keyframes (POV hook text baked in)
# -----------------------------------------------------------------------------

def resolve_product_images(product_key: str, colorway: str) -> list[Path]:
    """Find 2-3 reference images for the requested colorway.
    Looks first in `<product_dir>/colors/<Colorway>/` (case-insensitive match), then
    falls back to top-level filename-prefix matching, then to the first 3 images in the dir.
    """
    product = PRODUCT_REGISTRY[product_key]
    pdir = product["dir"]
    if not pdir.exists():
        sys.exit(f"[stage5] product dir missing: {pdir}")
    cw = colorway.lower().strip()
    exts = ("*.webp", "*.png", "*.jpg", "*.jpeg")

    # 1. Subdirectory match: colors/<Colorway>/
    colors_dir = pdir / "colors"
    if colors_dir.is_dir():
        for sub in colors_dir.iterdir():
            if sub.is_dir() and sub.name.lower() == cw:
                imgs = sorted(sum((list(sub.glob(e)) for e in exts), []))
                if imgs:
                    print(f"[stage5] colorway '{colorway}' → {len(imgs)} images from {sub}")
                    return imgs[:3]

    # 2. Top-level filename-prefix match
    candidates = []
    for ext in exts:
        for p in pdir.glob(ext):
            name = p.name.lower()
            if name.startswith(cw) or cw in name.split(".")[0]:
                candidates.append(p)
    candidates.sort()
    if candidates:
        return candidates[:3]

    # 3. Fallback: first 3 in dir
    all_imgs = sum((sorted(pdir.glob(ext)) for ext in exts), [])
    if not all_imgs:
        sys.exit(f"[stage5] no images found in {pdir}")
    print(f"[stage5] WARNING: no images matched colorway '{colorway}', using first 3 in dir")
    return all_imgs[:3]


def hf_generate(args: list[str]) -> dict:
    cmd = ["higgsfield"] + args + ["--wait", "--json"]
    print(f"  $ {' '.join(shlex.quote(c) for c in cmd)}", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"higgsfield failed: {r.stderr.strip()[:500]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"higgsfield returned non-json: {r.stdout[:500]}")


def hf_extract_result_url(payload) -> str | None:
    if isinstance(payload, list):
        payload = payload[0] if payload else {}
    for key in ("result_url", "url", "output_url"):
        if isinstance(payload.get(key), str):
            return payload[key]
    results = payload.get("results") or payload.get("outputs") or []
    if isinstance(results, list) and results:
        r0 = results[0]
        if isinstance(r0, dict):
            for key in ("url", "result_url", "output_url"):
                if isinstance(r0.get(key), str):
                    return r0[key]
        elif isinstance(r0, str) and r0.startswith("http"):
            return r0
    return None


def download_url(url: str, dest: Path):
    import requests
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)


def stage5_keyframes(
    scenes: list[dict],
    directions: dict,
    product_key: str,
    outdir: Path,
) -> dict[int, Path]:
    gen_dir = outdir / "generated"
    gen_dir.mkdir(exist_ok=True)
    colorway = directions.get("selected_colorway", "black")
    product_images = resolve_product_images(product_key, colorway)

    out_by_index: dict[int, Path] = {}
    for d in directions.get("scenes", []):
        idx = d["index"]
        target = gen_dir / f"scene_{idx:03d}_velantra.png"
        if target.exists():
            out_by_index[idx] = target
            continue

        scene = next((s for s in scenes if s["index"] == idx), None)
        if scene is None:
            continue

        prompt = d["image_prompt"]
        include_product = d.get("include_product_reference", True)

        args = [
            "generate", "create", "gpt_image_2",
            "--prompt", prompt,
            "--image", scene["frame"],
            "--aspect_ratio", "9:16",
            "--resolution", "2k",
        ]
        if include_product:
            for pimg in product_images[:2]:
                args.extend(["--image", str(pimg)])

        success = False
        for attempt in range(2):
            try:
                payload = hf_generate(args)
                url = hf_extract_result_url(payload)
                if not url:
                    raise RuntimeError("no result url in payload")
                download_url(url, target)
                out_by_index[idx] = target
                success = True
                pov_note = " (POV hook text in prompt)" if d.get("include_pov_hook") else ""
                print(f"[stage5] scene {idx} ✓{pov_note}")
                break
            except Exception as e:
                print(f"[stage5] scene {idx} attempt {attempt+1} failed: {e}")
        if not success:
            fallback = gen_dir / f"scene_{idx:03d}_velantra.jpg"
            shutil.copy(scene["frame"], fallback)
            out_by_index[idx] = fallback
            print(f"[stage5] scene {idx} ✗ — using ref frame as keyframe")

    return out_by_index


# -----------------------------------------------------------------------------
# Stage 6 — Seedance 2.0 animation (with original music via --audio)
# -----------------------------------------------------------------------------

def stage6_animate(
    scenes: list[dict],
    directions: dict,
    keyframes: dict[int, Path],
    outdir: Path,
) -> dict[int, Path]:
    anim_dir = outdir / "animated"
    anim_dir.mkdir(exist_ok=True)
    direction_by_index = {d["index"]: d for d in directions.get("scenes", [])}
    out_by_index: dict[int, Path] = {}

    for scene in scenes:
        idx = scene["index"]
        target = anim_dir / f"scene_{idx:03d}_animated.mp4"
        if target.exists():
            out_by_index[idx] = target
            continue

        d = direction_by_index.get(idx, {})
        if idx not in keyframes:
            continue

        motion_prompt = d.get("motion_prompt") or "subtle handheld camera motion"
        seedance_duration = 4 if scene["duration"] <= 5 else 8

        args = [
            "generate", "create", "seedance_2_0",
            "--prompt", motion_prompt,
            "--start-image", str(keyframes[idx]),
            "--audio", scene["audio_slice"],
            "--duration", str(seedance_duration),
            "--aspect_ratio", "9:16",
        ]
        if d.get("transition_to_next") == "smooth_morph" and (idx + 1) in keyframes:
            args.extend(["--end-image", str(keyframes[idx + 1])])

        success = False
        for attempt in range(2):
            try:
                payload = hf_generate(args)
                url = hf_extract_result_url(payload)
                if not url:
                    raise RuntimeError("no result url in payload")
                download_url(url, target)
                out_by_index[idx] = target
                success = True
                print(f"[stage6] scene {idx} ✓ ({seedance_duration}s, audio embedded)")
                break
            except Exception as e:
                print(f"[stage6] scene {idx} attempt {attempt+1} failed: {e}")

        if not success:
            print(f"[stage6] scene {idx} ✗ — Ken Burns fallback with audio mux")
            ken_burns_with_audio(keyframes[idx], Path(scene["audio_slice"]),
                                 scene["duration"], target)
            out_by_index[idx] = target

    return out_by_index


def ken_burns_with_audio(image: Path, audio: Path, duration: float, out_path: Path):
    duration = max(1.0, duration)
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(image), "-i", str(audio),
        "-vf",
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0015,1.2)':d={int(duration*25)}:s=1080x1920:fps=25",
        "-t", f"{duration}",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_path),
    ])


# -----------------------------------------------------------------------------
# Stage 7 — ffmpeg concat-only finalize
# -----------------------------------------------------------------------------

def stage7_finalize(scenes: list[dict], clips: dict[int, Path], outdir: Path) -> Path:
    final = outdir / "final_velantra_pov.mp4"
    trimmed_dir = outdir / "_trimmed"
    trimmed_dir.mkdir(exist_ok=True)

    trimmed_paths = []
    for scene in scenes:
        idx = scene["index"]
        if idx not in clips:
            continue
        src = clips[idx]
        trimmed = trimmed_dir / f"scene_{idx:03d}.mp4"
        run([
            "ffmpeg", "-y", "-i", str(src),
            "-t", f"{scene['duration']}",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            str(trimmed),
        ])
        trimmed_paths.append(trimmed)

    if not trimmed_paths:
        sys.exit("[stage7] no clips to stitch")

    concat_list = outdir / "_concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in trimmed_paths))
    # Re-encode on concat so streams definitely line up (different Seedance jobs may have
    # slightly different audio/video params)
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(final),
    ])
    print(f"[stage7] ✓ {final}")
    return final


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--product", default=DEFAULT_PRODUCT, choices=list(PRODUCT_REGISTRY.keys()))
    ap.add_argument("--colorway", default=None)
    ap.add_argument("--output-dir", default="./velantra-pov-output")
    args = ap.parse_args()

    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    ensure_tools()

    print(f"\n=== Velantra POV TikTok Replicator ===")
    print(f"URL:      {args.url}")
    print(f"Product:  {args.product}")
    print(f"Colorway: {args.colorway or '(auto by Opus from Gemini analysis)'}")
    print(f"Output:   {outdir}\n")

    s1 = stage1_download(args.url, outdir)
    scenes = stage2_frames(s1["video"], s1["audio"], s1["duration"], outdir)
    transcript = s1["transcript"].read_text(encoding="utf-8") if s1["transcript"].exists() else ""
    stage3_gemini_analysis(scenes, transcript, outdir)
    directions = stage4_opus_direction(args.product, args.colorway, outdir)
    keyframes = stage5_keyframes(scenes, directions, args.product, outdir)
    clips = stage6_animate(scenes, directions, keyframes, outdir)
    final = stage7_finalize(scenes, clips, outdir)

    print(f"\n✓ DONE: {final}")


if __name__ == "__main__":
    main()

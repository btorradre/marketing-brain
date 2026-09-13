#!/usr/bin/env python3
"""
generate_video.py — Animate still images into video with Veo 3 (Gemini API).

Image-to-video: you give it a starting frame (and optionally an end frame) plus
a motion prompt, and Veo 3 returns an MP4. Built for the frame-by-frame workflow
where you generate stills first, then animate each one into a short clip.

Two modes:

  1. Single clip
     python generate_video.py \
       --image scene1.jpg \
       --prompt "slow rack focus from the leather edge to the soft woven straw" \
       --output scene1.mp4

  2. Batch from a manifest (the usual case — animate a whole sequence at once)
     python generate_video.py --manifest scenes.json

The API key is NEVER stored in this skill. The script reads it from the
GEMINI_API_KEY environment variable (GOOGLE_API_KEY also works). Export it before
running:  export GEMINI_API_KEY="your-key"

Veo image-to-video is a paid Gemini API feature. Each clip costs real money and
takes ~30s-3min to render, so the script polls and prints progress.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

POLL_INTERVAL_SECONDS = 10
POLL_TIMEOUT_SECONDS = 600  # 10 minutes per clip

# Default model. Veo 3.1 has the best image-to-video adherence in the Veo 3 line.
# Override per run with --model. Common options:
#   veo-3.1-generate-preview        (highest quality, default)
#   veo-3.1-fast-generate-preview   (cheaper/faster — good for high-volume B-roll)
#   veo-3.0-generate-preview        (previous generation)
DEFAULT_MODEL = "veo-3.1-generate-preview"
DEFAULT_ASPECT_RATIO = "9:16"   # vertical, for Reels/TikTok/Meta. Use 16:9 for landscape.
DEFAULT_RESOLUTION = "720p"     # "720p" or "1080p"

MIME_BY_EXT = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def ensure_sdk():
    """Import google-genai, installing it on first use if missing."""
    try:
        from google import genai  # noqa: F401
        return
    except ImportError:
        print("[video-gen] Installing google-genai SDK (first run only)...", flush=True)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages", "google-genai"],
            check=True,
        )


def get_client():
    """Build a Gemini client. Key comes from the environment, never from the skill."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit(
            "[video-gen] ERROR: no API key found.\n"
            "  Set it first:  export GEMINI_API_KEY=\"your-key\"\n"
            "  (Get a key at https://aistudio.google.com/apikey — Veo needs a paid/billing-enabled key.)"
        )
    from google import genai
    return genai.Client(api_key=api_key)


def load_image(path):
    """Read a local image into a Veo Image object."""
    from google.genai import types

    p = Path(path)
    if not p.exists():
        sys.exit(f"[video-gen] ERROR: image not found: {p}")
    mime = MIME_BY_EXT.get(p.suffix.lower())
    if not mime:
        sys.exit(f"[video-gen] ERROR: unsupported image type '{p.suffix}'. Use jpg, png, or webp.")
    return types.Image(image_bytes=p.read_bytes(), mime_type=mime)


def build_config(scene):
    """Assemble GenerateVideosConfig from a scene dict, applying defaults."""
    from google.genai import types

    kwargs = {
        "aspect_ratio": scene.get("aspect_ratio", DEFAULT_ASPECT_RATIO),
        "resolution": scene.get("resolution", DEFAULT_RESOLUTION),
        "number_of_videos": 1,
    }
    if scene.get("negative_prompt"):
        kwargs["negative_prompt"] = scene["negative_prompt"]
    if scene.get("last_frame"):
        kwargs["last_frame"] = load_image(scene["last_frame"])
    # duration_seconds is honored by some Veo configs (typically 4/6/8s). Pass only
    # if asked; otherwise let the model use its default (usually 8s).
    if scene.get("duration_seconds"):
        kwargs["duration_seconds"] = int(scene["duration_seconds"])
    return types.GenerateVideosConfig(**kwargs)


def default_output_path(image_path):
    return str(Path(image_path).with_suffix("").name) + ".mp4"


def generate_one(client, scene, index=None, total=None):
    """Generate a single clip from one scene dict. Returns the output path."""
    label = ""
    if index is not None and total is not None:
        label = f"[{index}/{total}] "

    image_path = scene["image"]
    prompt = scene.get("prompt", "").strip()
    if not prompt:
        sys.exit(f"[video-gen] ERROR: scene for '{image_path}' has no prompt.")
    model = scene.get("model", DEFAULT_MODEL)
    out_path = scene.get("output") or default_output_path(image_path)

    print(f"\n[video-gen] {label}Animating: {image_path}")
    print(f"[video-gen]   model={model}  ar={scene.get('aspect_ratio', DEFAULT_ASPECT_RATIO)}  prompt=\"{prompt[:70]}{'...' if len(prompt) > 70 else ''}\"")

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        image=load_image(image_path),
        config=build_config(scene),
    )

    waited = 0
    while not operation.done:
        if waited >= POLL_TIMEOUT_SECONDS:
            sys.exit(f"[video-gen] ERROR: timed out after {POLL_TIMEOUT_SECONDS}s waiting for {image_path}.")
        time.sleep(POLL_INTERVAL_SECONDS)
        waited += POLL_INTERVAL_SECONDS
        print(f"[video-gen]   ...rendering ({waited}s)", flush=True)
        operation = client.operations.get(operation)

    # Surface RAI / safety filtering or empty results clearly.
    response = getattr(operation, "response", None)
    videos = getattr(response, "generated_videos", None) if response else None
    if not videos:
        err = getattr(operation, "error", None)
        sys.exit(
            f"[video-gen] ERROR: no video returned for {image_path}. "
            f"{('Detail: ' + str(err)) if err else 'It may have been blocked by safety filters — try rewording the prompt.'}"
        )

    video = videos[0]
    client.files.download(file=video.video)
    video.video.save(out_path)
    print(f"[video-gen]   ✓ saved → {out_path}")
    return out_path


def run_manifest(client, manifest_path):
    data = json.loads(Path(manifest_path).read_text())
    defaults = data.get("defaults", {})
    scenes = data.get("scenes", [])
    if not scenes:
        sys.exit("[video-gen] ERROR: manifest has no 'scenes'.")
    # Resolve paths relative to the manifest's own directory for portability.
    base = Path(manifest_path).resolve().parent
    outputs = []
    for i, scene in enumerate(scenes, 1):
        merged = {**defaults, **scene}
        for key in ("image", "last_frame", "output"):
            if merged.get(key) and not os.path.isabs(merged[key]):
                merged[key] = str(base / merged[key])
        outputs.append(generate_one(client, merged, index=i, total=len(scenes)))
    print(f"\n[video-gen] Done. {len(outputs)} clip(s) generated:")
    for o in outputs:
        print(f"  - {o}")
    return outputs


def main():
    ap = argparse.ArgumentParser(description="Animate still images into video with Veo 3 (Gemini API).")
    ap.add_argument("--image", help="Path to the starting-frame image (single-clip mode).")
    ap.add_argument("--prompt", help="Motion/camera-move prompt describing how the still should animate.")
    ap.add_argument("--output", help="Output .mp4 path (default: <image-name>.mp4).")
    ap.add_argument("--last-frame", help="Optional end-frame image for first→last interpolation.")
    ap.add_argument("--negative-prompt", help="Things to avoid (e.g. 'people talking, text, camera shake').")
    ap.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help="9:16 (default) or 16:9.")
    ap.add_argument("--resolution", default=DEFAULT_RESOLUTION, help="720p (default) or 1080p.")
    ap.add_argument("--duration-seconds", type=int, help="Clip length if the model supports it (e.g. 4, 6, 8).")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Veo model id (default: {DEFAULT_MODEL}).")
    ap.add_argument("--manifest", help="Path to a JSON manifest for batch mode (overrides single-clip args).")
    args = ap.parse_args()

    ensure_sdk()
    client = get_client()

    if args.manifest:
        run_manifest(client, args.manifest)
        return

    if not args.image or not args.prompt:
        sys.exit("[video-gen] ERROR: provide --image and --prompt (or use --manifest for batch mode).")

    scene = {
        "image": args.image,
        "prompt": args.prompt,
        "output": args.output,
        "last_frame": args.last_frame,
        "negative_prompt": args.negative_prompt,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "model": args.model,
    }
    if args.duration_seconds:
        scene["duration_seconds"] = args.duration_seconds
    generate_one(client, scene)


if __name__ == "__main__":
    main()

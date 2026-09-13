#!/usr/bin/env python3
"""Animate the approved Fall ad keyframes with Google Gemini Omni."""

import argparse
import base64
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
ENV_PATH = WORKSPACE / ".env"
API = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "models/gemini-omni-flash-preview"
STILLS = ROOT / "generated-assets" / "stills"
CLIPS = ROOT / "generated-assets" / "clips"
STATE_PATH = ROOT / "generated-assets" / "omni-state.json"

JOBS = {
    "sofia_raw": {
        "still": ROOT / "raw-rebuild" / "sofia-fall-regeneration" / "animate-source.png",
        "output": ROOT / "raw-rebuild" / "sofia-fall-regeneration" / "VEL-SOFIA-FALL-RAW-OMNI-02.mp4",
        "prompt": (
            "A single continuous raw handheld iPhone shot from behind on this dock. "
            "The woman takes two slow natural steps forward while the caramel woven "
            "tote swings gently from her right hand and settles with each step. A "
            "small breeze moves a few strands of hair and the sweater hem. The person "
            "filming follows at walking speed with subtle human hand drift and ordinary "
            "phone auto-exposure. Preserve the exact woman, oatmeal cable-knit sweater, "
            "dark jeans, brown boots, bag construction, handles, crossed straps, dock, "
            "boats, cloudy daylight, deep focus, modest dynamic range, and source-frame "
            "texture. Ambient harbor sound. Raw iPhone footage. Vertical 9:16. One "
            "continuous shot."
        ),
    },
    "sofia": {
        "still": STILLS / "VEL-SOFIA-FALL-OUTFIT-GPTIMAGE2-01.png",
        "output": CLIPS / "VEL-SOFIA-FALL-OUTFIT-OMNI-01.mp4",
        "prompt": (
            "A single continuous casual handheld iPhone take in this home entryway. "
            "The woman shifts her weight naturally, lightly adjusts the hem of her "
            "chunky knit sweater with her free hand, then takes one small step so the "
            "caramel woven tote swings gently and settles. Preserve the exact bag "
            "construction, crossed straps, woven texture, outfit, setting, lighting, "
            "framing, and realistic phone-camera look from the opening image. Use "
            "subtle human-scale motion and slight natural handheld drift. Keep the bag "
            "clearly visible throughout. Ambient room sound. Raw iPhone footage. "
            "Vertical 9:16. One continuous shot."
        ),
    },
    "eleanor": {
        "still": STILLS / "VEL-ELEANOR-FALL-COLORWAYS-GPTIMAGE2-01.png",
        "output": CLIPS / "VEL-ELEANOR-FALL-COLORWAYS-OMNI-01.mp4",
        "prompt": (
            "A single continuous casual handheld iPhone take in this home entryway. "
            "The camera drifts forward very slightly while soft window light moves "
            "naturally across the brass hardware. The edge of the folded knit scarf "
            "settles subtly, while both structured weekender bags remain stationary "
            "and fully visible. Preserve the exact light chocolate bag on the left, "
            "the exact army green bag on the right, all handles, straps, hardware, "
            "materials, proportions, boots, setting, lighting, and realistic "
            "phone-camera look from the opening image. Ambient room sound. Raw iPhone "
            "footage. Vertical 9:16. One continuous shot."
        ),
    },
}


def load_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.strip().startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not key:
        raise SystemExit("GEMINI_API_KEY not found in environment or workspace .env")
    return key


def request_json(method, url, key, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}key={key}", data=data, method=method
    )
    if data:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=SSL_CONTEXT
        ) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP {error.code}: {detail}") from error


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


def submit(job, key):
    image_data = base64.b64encode(job["still"].read_bytes()).decode()
    payload = {
        "model": MODEL,
        "input": [
            {"type": "image", "data": image_data, "mime_type": "image/png"},
            {"type": "text", "text": job["prompt"]},
        ],
        "background": True,
        "generation_config": {"video_config": {}},
    }
    response = request_json("POST", API, key, payload)
    interaction_id = response.get("id")
    if not interaction_id:
        raise RuntimeError(f"No interaction id: {json.dumps(response)[:300]}")
    return interaction_id


def poll(interaction_id, key, timeout_seconds=900):
    started = time.time()
    while time.time() - started < timeout_seconds:
        response = request_json("GET", f"{API}/{interaction_id}", key)
        status = response.get("status")
        if status == "completed":
            for step in response.get("steps", []):
                for content in step.get("content", []):
                    if content.get("type") == "video" and content.get("data"):
                        return base64.b64decode(content["data"])
            raise RuntimeError("Interaction completed without video output")
        if status in {"failed", "cancelled", "error"}:
            raise RuntimeError(
                f"Interaction {status}: {json.dumps(response)[:500]}"
            )
        print(f"  {status or 'queued'}; checking again in 12s", flush=True)
        time.sleep(12)
    raise TimeoutError(interaction_id)


def run_one(name, key, state):
    job = JOBS[name]
    if not job["still"].exists():
        raise FileNotFoundError(job["still"])
    if job["output"].exists() and job["output"].stat().st_size > 100_000:
        print(f"{name}: cached at {job['output']}")
        return

    entry = state.setdefault(name, {})
    interaction_id = entry.get("interaction_id")
    if not interaction_id:
        interaction_id = submit(job, key)
        entry["interaction_id"] = interaction_id
        save_state(state)
        print(f"{name}: submitted {interaction_id}", flush=True)

    video = poll(interaction_id, key)
    job["output"].parent.mkdir(parents=True, exist_ok=True)
    job["output"].write_bytes(video)
    entry["completed"] = True
    entry["output"] = str(job["output"])
    save_state(state)
    print(f"{name}: wrote {job['output']} ({len(video)} bytes)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", choices=[*JOBS, "all", "status"])
    args = parser.parse_args()

    state = load_state()
    if args.asset == "status":
        print(json.dumps(state, indent=2))
        return

    key = load_key()
    names = list(JOBS) if args.asset == "all" else [args.asset]
    for name in names:
        run_one(name, key, state)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
3 hook variations: woman injecting Ozempic into her own stomach, iPhone selfie aesthetic.
Output to generated_v3/hook_variations/
"""
import json, os, shlex, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path("/Users/brooksorradre2/Documents/marketing brain/higgsfield-runs/motilli_92888910")
OUT = ROOT / "generated_v3" / "hook_variations"
(OUT / "images").mkdir(parents=True, exist_ok=True)
(OUT / "videos").mkdir(parents=True, exist_ok=True)

SUBJECT = (
    "55yo woman, salt-and-pepper bob to her shoulders, fine crow's feet, soft jawline, "
    "tired but warm eyes, no makeup retouching"
)

ANTI_POLISH = (
    "iPhone 15 Pro front cam, native wide ~26mm, slight barrel distortion, "
    "visible pores, light skin shine, fine lines, hair flyaways, "
    "ungraded, no LUT, no color grade, no studio lighting, no beauty smoothing"
)

ORGANIC_CUES = (
    "(handheld one-hand wobble, rolling-shutter wobble, autofocus micro-pulse, "
    "ambient hair drift, raw phone audio with room tone, no LUT)"
)

# Hard negation chain — kills the fountain-pen interpretation, locks Ozempic visual
DEVICE = (
    "a real OZEMPIC pen (Novo Nordisk's iconic GLP-1 weight-loss injector) — an "
    "elongated thicker pre-filled disposable medication pen with a light pastel-"
    "blue plastic body and a darker matching blue protective cap (the cap is now "
    "off, exposing the short clear needle tip at the bottom), the 'Ozempic' "
    "wordmark printed on the body in clean white sans-serif, a clear medication "
    "viewing window mid-body, dose-dial wheel at the back. NOT a fountain pen, "
    "NOT a writing pen, NOT a generic injector — this is the iconic blue Ozempic "
    "weight-loss injection device"
)

VARIATIONS = [
    {
        "n": 1, "label": "pov_stomach_jab",
        "image_prompt": (
            f"Vertical 9:16 iPhone POV looking down at her own bare stomach, "
            f"ungraded raw phone photo. {SUBJECT} (only chin, neck, chest, hands, "
            "and bare midsection visible — her own POV looking down). Worn olive "
            "sweatshirt pulled up to mid-chest with her left hand, exposing slightly "
            "bloated belly and navel. Her right hand brings the iconic blue Ozempic "
            "pen toward the soft fold of skin she's pinching, the needle tip about "
            f"to make contact. {DEVICE}. Single north-facing bathroom window light "
            f"from the left, slight underexposure on shadow side. {ANTI_POLISH}. 9:16."
        ),
        "kling_prompt": (
            "Her right hand pushes the blue Ozempic pen straight down into the "
            "pinched fold of belly skin — needle goes in, thumb presses the dose-"
            "dial button, small visible body flinch, then the pen is pulled back "
            "out and she rubs the injection spot with her free thumb. Handheld POV "
            "camera bobs gently with her breath, slight downward tilt to follow "
            "the action."
        ),
    },
    {
        "n": 2, "label": "mirror_inject_jab",
        "image_prompt": (
            f"Vertical 9:16 iPhone bathroom-mirror selfie, ungraded raw phone "
            f"photo. {SUBJECT} mid-action in her own bathroom mirror — left hand "
            "pulls her worn olive sweatshirt up to mid-chest, fully exposing her "
            "bare slightly-bloated stomach and navel. Right hand brings the iconic "
            "blue Ozempic pen toward the side of her lower belly, just below the "
            f"navel. {DEVICE}. She watches her own reflection with a tight "
            "humorless half-smile, jaw set. Bathroom vanity light overhead + "
            "window light reflected in the mirror, mixed color temperature, hard "
            f"contact shadow under chin. {ANTI_POLISH}. 9:16."
        ),
        "kling_prompt": (
            "She presses the blue Ozempic pen firmly into the side of her bare "
            "belly, thumb clicks the dose-dial button, holds for a beat, gives a "
            "small wince at her own reflection, then pulls the pen back out and "
            "lets her shirt drop. Handheld iPhone wobble, slight upward pan from "
            "belly to her face in the mirror."
        ),
    },
    {
        "n": 3, "label": "couch_inject_jab",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie from a low waist-height side angle "
            f"(like a friend is filming from across the room), ungraded. {SUBJECT} "
            "sits on her own beige couch leaning back slightly, worn olive "
            "sweatshirt lifted with her left hand to mid-chest exposing her bare "
            "stomach. Her right hand brings the iconic blue Ozempic pen toward "
            "the soft fold of her lower belly. The needle tip is about to make "
            f"contact with the skin. {DEVICE}. She glances down at her stomach "
            "with a tight resigned half-smile. Mixed light: north window camera-"
            "left + warm table lamp camera-right (color-temp mismatch). "
            f"{ANTI_POLISH}. 9:16."
        ),
        "kling_prompt": (
            "She pushes the blue Ozempic pen straight into the soft fold of her "
            "belly, presses the dose-dial with her thumb — the device clicks "
            "audibly, her body flinches subtly, she holds for a beat, then pulls "
            "the pen back out and rubs the injection spot. Handheld camera "
            "wobble, slight tilt upward to her face at the very end."
        ),
    },
]


def parse_result(out):
    out = out.strip()
    for start_char in ('[', '{'):
        idx = out.find(start_char)
        while idx != -1:
            try:
                data = json.loads(out[idx:])
                item = data[0] if isinstance(data, list) and data else data
                return item.get('id'), (item.get('result_url') or item.get('url'))
            except json.JSONDecodeError:
                idx = out.find(start_char, idx + 1)
    return None, None


def run(cmd):
    print(f"\n$ {cmd[:180]}{'...' if len(cmd) > 180 else ''}", flush=True)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.stdout:
        print(p.stdout[-800:])
    return p.returncode, p.stdout


def download(url, path):
    try:
        urllib.request.urlretrieve(url, path)
        return True
    except Exception as e:
        print(f"download failed: {e}")
        return False


for v in VARIATIONS:
    n = v["n"]; label = v["label"]
    print(f"\n========== HOOK VAR {n}: {label} — image ==========")
    rc, out = run(
        f"higgsfield generate create nano_banana_2 "
        f"--prompt {shlex.quote(v['image_prompt'])} "
        f"--aspect_ratio 9:16 --resolution 2k --wait --wait-timeout 5m --json"
    )
    img_job, img_url = parse_result(out)
    if not img_job:
        print(f"VAR {n} image FAIL"); continue
    img_path = OUT / "images" / f"hook_var{n}_{label}.png"
    download(img_url, img_path)
    print(f"saved: {img_path}")

    print(f"\n========== HOOK VAR {n}: {label} — video (5s) ==========")
    rc, out = run(
        f"higgsfield generate create kling3_0 "
        f"--prompt {shlex.quote(v['kling_prompt'] + ' ' + ORGANIC_CUES)} "
        f"--start-image {img_job} --aspect_ratio 9:16 --duration 5 --mode std --sound on "
        f"--wait --wait-timeout 15m --json"
    )
    vid_job, vid_url = parse_result(out)
    if not vid_job:
        print(f"VAR {n} video FAIL"); continue
    vid_path = OUT / "videos" / f"hook_var{n}_{label}.mp4"
    download(vid_url, vid_path)
    print(f"saved: {vid_path}")

print("\n==== DONE ====")

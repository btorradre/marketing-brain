#!/usr/bin/env python3
"""
Motilli replication of GLP-1 SOS reference (gethookd 92888910)
Pipeline: Higgsfield CLI nano_banana_2 (i2i image) -> kling3_0 (i2v video, 5s, sound on)

Honors Kling rules from memory:
- prompts <= 2 sentences
- 5s max clips
- 4 organic imperfection cues appended (handheld jitter, rolling shutter, eye focus drift, background motion)
- pure i2i for product-focused shots
"""

import json
import os
import shlex
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path("/Users/brooksorradre2/Documents/marketing brain/higgsfield-runs/motilli_92888910")
GEN_DIR = ROOT / "generated"
GEN_DIR.mkdir(parents=True, exist_ok=True)
(GEN_DIR / "images").mkdir(exist_ok=True)
(GEN_DIR / "videos").mkdir(exist_ok=True)
MANIFEST_PATH = ROOT / "manifest.json"

MOTILLI_PRODUCT_UPLOAD = "aa6b892d-2a4b-459a-b4e9-7841215ac579"
MOTILLI_PRODUCT_URL = "https://d2ol7oe51mr4n9.cloudfront.net/user_30et6qnNTnNcomVUJnn0bLxTH81/aa6b892d-2a4b-459a-b4e9-7841215ac579.png"

ORGANIC_CUES = "handheld camera jitter, rolling shutter, eye focus drift, subtle background motion"

# 9-beat shot list. Each beat: image prompt (i2i adapt of reference scene) + Kling motion prompt.
BEATS = [
    {
        "n": 1, "label": "hook_pen_sweep",
        "image_prompt": "Selfie 9:16 portrait of a 55 year old woman with grey hair in a green shirt, holding an Ozempic-style injection pen in front of her midsection, soft daylight bathroom, subtle bottles of laxatives blurred behind her on the counter, candid medical-aware mood, photorealistic UGC.",
        "image_refs": [],  # no product anchor needed, character-driven
        "kling_prompt": "Woman lowers the pen and casually sweeps a row of laxative bottles aside with her free hand, looking directly at camera with raised eyebrow.",
    },
    {
        "n": 2, "label": "anim_gut_slowdown",
        "image_prompt": "Animated medical 3D rendering, cross-section of a human torso with stomach and intestines visible in soft anatomical pinks and reds, brown lumpy food paused mid-transit, dark blue background, clinical educational illustration style, no text.",
        "image_refs": [],
        "kling_prompt": "Camera slowly pushes in on the digestive tract, food particles barely creep forward in slow motion, organs gently pulse with reduced motility.",
    },
    {
        "n": 3, "label": "competitor_cabinet",
        "image_prompt": "Same 55 year old grey-haired woman from scene 1 in a soft beige bathrobe, standing at an open medicine cabinet packed with generic blue and purple laxative bottles and pink fiber tubs, holding one bottle up at eye level with a frustrated expression, soft daylight, photorealistic UGC.",
        "image_refs": [],
        "kling_prompt": "Woman picks up a generic laxative bottle, glances at the label, shakes her head and returns it to the cabinet shelf.",
    },
    {
        "n": 4, "label": "couch_concrete_confession",
        "image_prompt": "Same 55 year old grey-haired woman, now in a maroon sweater, sitting on a soft beige couch in warm afternoon home lighting, leaning slightly toward the camera in an intimate selfie framing, hand pressed lightly to her stomach, sincere worried expression, photorealistic UGC.",
        "image_refs": [],
        "kling_prompt": "Woman presses her hand to her stomach, eyes flick down briefly, then back to camera as she shakes her head with a tight humorless smile.",
    },
    {
        "n": 5, "label": "bed_edge_terrified",
        "image_prompt": "Same 55 year old grey-haired woman in soft cream pajamas, sitting on the edge of an unmade bed in soft morning light, looking directly at the camera with a vulnerable concerned expression, hand resting on her thigh, photorealistic intimate UGC selfie 9:16.",
        "image_refs": [],
        "kling_prompt": "Woman sighs and looks down briefly, then back up to camera with a small reluctant smile, head tilting slightly.",
    },
    {
        "n": 6, "label": "motilli_reveal",
        "image_prompt": "Same 55 year old grey-haired woman in a soft blue sweater on a couch, holding the Motilli clear-bodied white-capped jar with green wrap-around label reading 'motilli — CELERY JUICE FIBER GUMMIES — GREEN APPLE' in front of her chest, two heart-shaped dark forest green Motilli gummies (Green Apple flavor, deep matte green color) visible on her open palm, warm afternoon home lighting, hopeful relieved expression, photorealistic UGC selfie 9:16. The jar and gummy color must match the reference image exactly — the gummies are DARK GREEN, not orange or pink.",
        "image_refs": [MOTILLI_PRODUCT_UPLOAD],  # i2i anchor: product fidelity required
        "kling_prompt": "Woman lifts the Motilli jar slightly toward camera, smiles softly, then tilts her open palm so the dark green heart-shaped gummies catch the light.",
    },
    {
        "n": 7, "label": "anim_apigenin_wake",
        "image_prompt": "Animated medical 3D rendering, human stomach and upper intestines glowing with gentle green energy, small green particles labeled with leaf icons drifting into the stomach lining, soft pulse of warm light spreading through the digestive tract, dark blue background, clinical educational style, no text.",
        "image_refs": [],
        "kling_prompt": "Green particles drift into the stomach wall, the organs gently pulse and brighten as motility resumes, food begins flowing normally through the intestines.",
    },
    {
        "n": 8, "label": "kitchen_clockwork",
        "image_prompt": "Same 55 year old grey-haired woman in a light blue sweater and jeans, walking confidently from a sunlit kitchen toward the camera, holding a coffee mug, relaxed flat midsection, genuine happy smile, bright airy home, photorealistic 9:16 lifestyle UGC.",
        "image_refs": [],
        "kling_prompt": "Woman walks toward camera with the coffee mug, smiles wider, then turns to glance out a sunlit window in a relaxed easy moment.",
    },
    {
        "n": 9, "label": "cta_60_day_guarantee",
        "image_prompt": "The Motilli clear-bodied white-capped jar with green wrap-around label reading 'motilli — CELERY JUICE FIBER GUMMIES — GREEN APPLE' sitting on a clean white marble counter, two heart-shaped dark forest green Motilli gummies (Green Apple flavor, deep matte green color) in front of the jar, soft daylight, a small green badge that reads '60-DAY GUARANTEE' overlaid in the upper right, the same 55 year old grey-haired woman partially in frame on the right edge in a green shirt, photorealistic 9:16. The jar and gummy color must match the reference image exactly — the gummies are DARK GREEN, not orange or pink.",
        "image_refs": [MOTILLI_PRODUCT_UPLOAD],  # i2i anchor: product fidelity required
        "kling_prompt": "Camera does a slow gentle push-in toward the Motilli jar on the counter, the woman's hand enters frame and lightly touches the jar.",
    },
]


def parse_result(out, beat_n, kind):
    """Parse higgsfield CLI JSON output. Output is a list of result objects."""
    out = out.strip()
    # Find first '[' or '{' that begins valid JSON
    for start_char in ('[', '{'):
        idx = out.find(start_char)
        while idx != -1:
            try:
                data = json.loads(out[idx:])
                break
            except json.JSONDecodeError:
                idx = out.find(start_char, idx + 1)
                continue
            except Exception:
                idx = -1
                break
        else:
            continue
        if 'data' in dir() and data is not None:
            break
    else:
        print(f"[BEAT {beat_n}] {kind} no parseable JSON in output")
        return None, None
    # Normalize: data is either a list of jobs or a single object
    if isinstance(data, list):
        if not data:
            return None, None
        item = data[0]
    else:
        item = data
    job_id = item.get('id')
    result_url = item.get('result_url') or item.get('url')
    if not result_url:
        # Some payloads have a results[] array
        for r in (item.get('results') or []):
            if r.get('result_url') or r.get('url'):
                result_url = r.get('result_url') or r.get('url')
                break
    return job_id, result_url


def run(cmd, capture=True):
    """Run a shell command, return (returncode, stdout, stderr)."""
    print(f"\n$ {cmd}", flush=True)
    proc = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if proc.stdout:
        print(proc.stdout[:2000])
    if proc.returncode != 0 and proc.stderr:
        print(f"STDERR: {proc.stderr[:2000]}")
    return proc.returncode, proc.stdout, proc.stderr


def gen_image(beat):
    """Run nano_banana_2 i2i image generation for a beat. Returns (job_id, result_url)."""
    prompt = beat["image_prompt"]
    img_args = []
    for ref in beat["image_refs"]:
        img_args.append(f'--image {ref}')
    img_str = " ".join(img_args)
    # Quote prompt safely
    prompt_q = shlex.quote(prompt)
    cmd = (
        f"higgsfield generate create nano_banana_2 "
        f"--prompt {prompt_q} "
        f"{img_str} "
        f"--aspect_ratio 9:16 --resolution 2k "
        f"--wait --wait-timeout 5m --json"
    )
    rc, out, err = run(cmd)
    if rc != 0:
        print(f"[BEAT {beat['n']}] image gen FAILED")
        return None, None
    return parse_result(out, beat['n'], "image")


def gen_video(beat, image_job_id_or_url):
    """Run kling3_0 i2v from the generated image. Returns (job_id, result_url)."""
    full_prompt = f"{beat['kling_prompt']} ({ORGANIC_CUES})"
    prompt_q = shlex.quote(full_prompt)
    # Use the image job_id directly as start-image (CLI accepts UUID)
    start_arg = image_job_id_or_url
    cmd = (
        f"higgsfield generate create kling3_0 "
        f"--prompt {prompt_q} "
        f"--start-image {start_arg} "
        f"--aspect_ratio 9:16 --duration 5 --mode std --sound on "
        f"--wait --wait-timeout 15m --json"
    )
    rc, out, err = run(cmd)
    if rc != 0:
        print(f"[BEAT {beat['n']}] video gen FAILED")
        return None, None
    return parse_result(out, beat['n'], "video")


def download(url, path):
    if not url:
        return False
    try:
        urllib.request.urlretrieve(url, path)
        return True
    except Exception as e:
        print(f"download failed: {e}")
        return False


def load_manifest():
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {"beats": {}}


def save_manifest(m):
    MANIFEST_PATH.write_text(json.dumps(m, indent=2))


def main():
    only = None
    if len(sys.argv) > 1:
        only = [int(x) for x in sys.argv[1].split(',')]
    manifest = load_manifest()
    for beat in BEATS:
        n = beat['n']
        if only and n not in only:
            continue
        bkey = str(n)
        prev = manifest['beats'].get(bkey, {})
        # Resume: skip image gen if already done
        if prev.get('image_url') and prev.get('image_path'):
            print(f"[BEAT {n}] image already generated, skipping")
            img_job = prev.get('image_job_id')
            img_url = prev.get('image_url')
        else:
            print(f"\n========== BEAT {n}: {beat['label']} — image ==========")
            img_job, img_url = gen_image(beat)
            if not img_job:
                print(f"[BEAT {n}] image fail, abort beat")
                continue
            img_path = GEN_DIR / 'images' / f"beat_{n:02d}_{beat['label']}.png"
            if download(img_url, img_path):
                print(f"saved: {img_path}")
            manifest['beats'][bkey] = {
                **prev,
                'beat': beat['label'],
                'image_job_id': img_job,
                'image_url': img_url,
                'image_path': str(img_path),
                'image_prompt': beat['image_prompt'],
            }
            save_manifest(manifest)
        if prev.get('video_url') and prev.get('video_path') and Path(prev['video_path']).exists():
            print(f"[BEAT {n}] video already generated, skipping")
            continue
        print(f"\n========== BEAT {n}: {beat['label']} — video ==========")
        # Use the image job id as the kling start-image input (CLI auto-resolves)
        vid_job, vid_url = gen_video(beat, img_job)
        if not vid_job:
            print(f"[BEAT {n}] video fail")
            continue
        vid_path = GEN_DIR / 'videos' / f"beat_{n:02d}_{beat['label']}.mp4"
        if download(vid_url, vid_path):
            print(f"saved: {vid_path}")
        manifest['beats'][bkey].update({
            'video_job_id': vid_job,
            'video_url': vid_url,
            'video_path': str(vid_path),
            'kling_prompt': beat['kling_prompt'],
        })
        save_manifest(manifest)
    print("\n==== DONE ====")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ('beat', 'image_path', 'video_path')} for k, v in manifest['beats'].items()}, indent=2))


if __name__ == "__main__":
    main()

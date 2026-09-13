#!/usr/bin/env python3
"""
v3: Organic-UGC-tuned, 20-beat segmentation @ ~4s each (~80s total).

Applies PROMPTING_NOTES.md research:
- Lead with format string (vertical 9:16 iPhone selfie, ungraded, raw phone photo)
- Repeat SUBJECT constant verbatim across selfie beats (identity lock)
- Specific window/lighting deficiency, not "soft daylight"
- Anti-polish phrases (no LUT, no studio lighting, no smoothing, visible pores)
- Kling: ONE camera move + ONE subject action per beat, 6 organic cues
- Output dir: generated_v3/ (parallel to existing generated/)
"""

import json
import os
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path("/Users/brooksorradre2/Documents/marketing brain/higgsfield-runs/motilli_92888910")
GEN_DIR = ROOT / "generated_v3"
GEN_DIR.mkdir(exist_ok=True)
(GEN_DIR / "images").mkdir(exist_ok=True)
(GEN_DIR / "videos").mkdir(exist_ok=True)
MANIFEST_PATH = ROOT / "manifest_v3.json"

MOTILLI_PRODUCT_UPLOAD = "aa6b892d-2a4b-459a-b4e9-7841215ac579"

# Subject constant — paste verbatim into every selfie beat for identity lock.
SUBJECT = (
    "55yo woman, salt-and-pepper bob to her shoulders, fine crow's feet, soft jawline, "
    "tired but warm eyes, no makeup retouching"
)

# Organic UGC anti-polish chain — append to every selfie image prompt.
ANTI_POLISH = (
    "iPhone 15 Pro front cam, native wide ~26mm, slight barrel distortion, "
    "visible pores, light skin shine on forehead, hair flyaways, "
    "ungraded, no LUT, no color grade, no studio lighting, no beauty smoothing"
)

# Kling organic motion cues — append as one parenthetical to every motion prompt.
ORGANIC_CUES = (
    "(handheld one-hand wobble, rolling-shutter wobble, autofocus micro-pulse, "
    "ambient hair drift, raw phone audio with room tone, no LUT)"
)

# Animated 3D anti-realism flag — for 3D anatomical cutaway beats.
ANIM_3D = (
    "clinical educational illustration style, anatomical-textbook color palette, "
    "no live-action, no photorealism, dark navy background"
)

# 20-beat shot list. Total runtime: 19 beats * 4s + 1 closer * 6s = 82s.
# Each beat: image_prompt (i2i if image_refs set), kling_prompt (motion only), duration.
BEATS = [
    {
        "n": 1, "label": "hook_pen_hand",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie still, ungraded, raw phone photo. {SUBJECT} "
            "in a worn olive sweatshirt, holding a real OZEMPIC pen (Novo Nordisk's "
            "iconic GLP-1 weight-loss injection device) across her midsection — the "
            "Ozempic pen is an elongated thicker pre-filled disposable medication "
            "pen with a light pastel-blue plastic body and a darker matching blue "
            "protective cap, the 'Ozempic' wordmark visible on the body, a clear "
            "medication viewing window mid-body, and a dose-dial wheel at the back "
            "end. This is a real branded GLP-1 auto-injector exactly as it appears "
            "in pharmacies. NOT a fountain pen, NOT a writing pen, NOT a ballpoint, "
            "NOT a generic unbranded injector. Setting: her own bathroom. Lit only "
            "by a single north-facing window, slight underexposure on shadow side. "
            f"{ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She lowers the Ozempic pen an inch toward camera and glances down at "
            "the blue device once with a tight humorless half-smile. Camera locked, "
            "hand drift only."
        ),
        "duration": 4,
    },
    {
        "n": 2, "label": "laxative_counter_sweep",
        "image_prompt": (
            f"Vertical 9:16 iPhone overhead phone shot, ungraded. Close on a worn white "
            f"bathroom counter cluttered with mismatched generic laxative bottles "
            f"(blue, purple, pink), a few labels facing wrong way, real-life clutter. A "
            f"woman's hand reaches in. Mixed bathroom vanity light overhead. {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Her hand sweeps the laxative bottles to the right, two of them topple "
            "into a small trash can just off frame. Camera locked overhead."
        ),
        "duration": 4,
    },
    {
        "n": 3, "label": "glp1_pen_hero",
        "image_prompt": (
            "Vertical 9:16 product still, ungraded raw phone photo. Three real, "
            "iconic, instantly recognizable GLP-1 medication pens stand upright in a "
            "row on a worn butcher-block counter — branded products as they appear "
            "in the real world, NOT generic. From left to right:\n"
            "1. OZEMPIC pen (Novo Nordisk): elongated thicker pre-filled pen with a "
            "light pastel-blue body and a darker matching blue protective cap, the "
            "'Ozempic' wordmark printed on the body in clean sans-serif lettering, a "
            "small clear medication viewing window mid-body, a dose-dial wheel at "
            "the back end of the pen.\n"
            "2. MOUNJARO KwikPen (Eli Lilly): chunkier rectangular auto-injector "
            "with a white body and a turquoise/teal push-button cap at the top, the "
            "'Mounjaro' wordmark printed on the body, dose dial visible through a "
            "small window.\n"
            "3. ZEPBOUND auto-injector (Eli Lilly): white KwikPen-style auto-"
            "injector with a vivid red and blue accent stripe near the cap, the "
            "'Zepbound' wordmark printed on the body, push-button at the top.\n"
            "These are pre-filled disposable subcutaneous medication pens / GLP-1 "
            "weight-loss injectors as they actually appear in pharmacies. NOT "
            "fountain pens, NOT writing pens, NOT generic unbranded injectors. "
            "Single hard window light from camera-left, dust motes in the beam. "
            "iPhone 15 Pro wide, no LUT, no studio lighting. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Camera does a small handheld drift forward toward the row of pens "
            "(~6cm of motion total), autofocus re-locks once on the middle Mounjaro "
            "KwikPen."
        ),
        "duration": 4,
    },
    {
        "n": 4, "label": "anim_gut_slowdown",
        "image_prompt": (
            "Animated medical 3D rendering, cross-section of a human torso with stomach "
            "and intestines visible in soft anatomical pinks and reds, brown lumpy food "
            f"paused mid-transit, {ANIM_3D}, no text overlays. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Camera slowly pushes in on the digestive tract; food particles barely "
            "creep forward in slow motion."
        ),
        "duration": 4,
    },
    {
        "n": 5, "label": "bathroom_medicine_cabinet",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in a faded beige terry "
            "bathrobe, standing at her own open medicine cabinet packed with mismatched "
            "generic laxative bottles and pink fiber tubs. Bathroom vanity light "
            f"overhead, hard contact shadow under chin. {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She picks up a generic blue laxative bottle, glances at the label with a "
            "mid-sigh half-frustrated expression, returns it to the shelf."
        ),
        "duration": 4,
    },
    {
        "n": 6, "label": "competitor_miralax_handheld",
        "image_prompt": (
            "Vertical 9:16 iPhone close-up, ungraded raw phone photo. A 55yo woman's "
            "hand (light skin, neutral nails) holds a large purple generic stool-softener "
            "bottle at eye level, blurred bathroom counter behind. Bathroom vanity light "
            "overhead. iPhone front cam, no LUT, no smoothing. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "The hand turns the bottle a quarter-rotation; autofocus pulses once on the "
            "label."
        ),
        "duration": 4,
    },
    {
        "n": 7, "label": "competitor_fiber_probiotic",
        "image_prompt": (
            "Vertical 9:16 iPhone close-up, ungraded. Same 55yo woman's hand holds a "
            "pink fiber-gummy tub on a worn bathroom counter, then a generic women's "
            "probiotic bottle visible on the counter beside it, all unbranded. Bathroom "
            "vanity light overhead. iPhone front cam. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Hand swaps the fiber tub for the probiotic bottle and shakes it once with "
            "a small mid-sigh."
        ),
        "duration": 4,
    },
    {
        "n": 8, "label": "mirror_hourglass_despair",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in faded grey cotton "
            "sweats, standing at her own bathroom mirror with both hands pressed to her "
            "lower belly, caught mid-thought. Mirror reflection visible. Mixed light: "
            f"bathroom vanity overhead + window in mirror. {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She presses her palms flat to her stomach, exhales slowly, and looks down "
            "at the reflection of her midsection."
        ),
        "duration": 4,
    },
    {
        "n": 9, "label": "anim_intestine_slow_food",
        "image_prompt": (
            "Animated medical 3D rendering inside human intestines, thick green-brown "
            "viscous food substance moving extremely slowly, gas bubbles forming at the "
            f"bend, {ANIM_3D}, no text. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Camera drifts forward through the intestinal tract; food sludge moves "
            "millimeters, gas bubbles slowly expand."
        ),
        "duration": 4,
    },
    {
        "n": 10, "label": "couch_concrete_confession",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in a worn maroon "
            "cardigan with slight pilling at the elbow, sitting on her own beige couch "
            "with a throw pillow askew behind her. Hand pressed flat to her lower "
            "stomach, caught mid-sigh. Off-center framing pushed to right third, head "
            "slightly clipped at the top. Mixed light: north window camera-left + warm "
            f"table lamp camera-right (color-temp mismatch). {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She presses her palm flat to her stomach, eyes flick down once, then back "
            "to camera with a tight breathy half-laugh. Camera locked, hand drift only."
        ),
        "duration": 4,
    },
    {
        "n": 11, "label": "anim_concrete_torso",
        "image_prompt": (
            "Animated medical 3D rendering of a human torso, the abdomen covered in "
            "cracked grey concrete-like skin texture emphasizing hardness and "
            f"immovability, {ANIM_3D}, no text. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Camera slowly orbits the torso 10°; the cracked concrete pattern shifts "
            "subtly with the angle."
        ),
        "duration": 4,
    },
    {
        "n": 12, "label": "armchair_terrified",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in a dark blue blouse "
            "sitting in her own worn armchair, knees together, hands folded in lap. "
            "Single window camera-left, slight underexposure. Caught mid-thought, eyes "
            f"slightly tired, small reluctant smile. {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She tilts her head a few degrees, gives a small reluctant exhale-laugh "
            "as if admitting something. Camera locked."
        ),
        "duration": 4,
    },
    {
        "n": 13, "label": "motilli_reveal_couch",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie still, ungraded, raw phone photo. {SUBJECT} "
            "in a worn soft-blue cardigan on her own beige couch (same room as the "
            "couch confession beat). She holds the Motilli jar from the reference "
            "image at chest level — label and dark forest-green heart-shaped gummies "
            "must match the reference exactly, do NOT invent color (the gummies are "
            "DARK GREEN, Green Apple flavor). Two dark green heart gummies in her "
            "open palm. Mixed light: north window + warm side lamp. Quiet half-smile, "
            f"mid-exhale (not a posed smile). {ANTI_POLISH}. 9:16."
        ),
        "image_refs": [MOTILLI_PRODUCT_UPLOAD],
        "kling_prompt": (
            "She lifts the Motilli jar an inch toward camera, mid-exhale half-smile "
            "(not posed), then tilts her open palm so the dark green heart gummies "
            "catch the light. Camera locked, hand drift only."
        ),
        "duration": 4,
    },
    {
        "n": 14, "label": "red_x_aisle",
        "image_prompt": (
            "Vertical 9:16 iPhone phone-shot, ungraded. Wide shot down a real grocery "
            "aisle filled with mismatched colorful cleaning and laxative bottles, "
            "fluorescent ceiling lights, slight motion blur as a shopper walks past. "
            "A bold red painted X overlaid across the center of the aisle. Real-store "
            "feel, no rendered look. iPhone front cam. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Camera drifts slightly down the aisle handheld; the red X stays anchored "
            "center-frame."
        ),
        "duration": 4,
    },
    {
        "n": 15, "label": "anim_apigenin_wake",
        "image_prompt": (
            "Animated medical 3D rendering, human stomach and upper intestines glowing "
            "with gentle green energy, small green leaf-shaped particles drifting into "
            "the stomach lining, soft pulse of warm light spreading through digestive "
            f"tract as motility resumes, {ANIM_3D}, no text. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Green particles drift into the stomach wall, the organs gently brighten "
            "and pulse, food begins flowing normally."
        ),
        "duration": 4,
    },
    {
        "n": 16, "label": "motilli_dining_table",
        "image_prompt": (
            "Vertical 9:16 iPhone phone-shot, ungraded. The Motilli jar from the "
            "reference image sitting on a worn dining table next to a half-eaten plate "
            "of dinner — label and dark forest-green heart-shaped gummies must match "
            "the reference exactly (dark GREEN, Green Apple flavor). Two dark green "
            "heart gummies on a white napkin beside the jar. Warm overhead pendant "
            "light + slight window glow. iPhone front cam, no LUT. 9:16."
        ),
        "image_refs": [MOTILLI_PRODUCT_UPLOAD],
        "kling_prompt": (
            "Camera drifts forward 6cm toward the jar, autofocus pulses once on the "
            "gummies on the napkin."
        ),
        "duration": 4,
    },
    {
        "n": 17, "label": "bed_stretch_relief",
        "image_prompt": (
            f"Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in faded cream cotton "
            "pajamas, sitting up in her own unmade bed (visible duvet wrinkles, phone "
            "charger cable on nightstand), arms raised in a happy morning stretch with "
            "a relieved easy smile. Pale morning window light from camera-left. "
            f"{ANTI_POLISH}. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She finishes her stretch, lowers her arms, lets out a small contented "
            "exhale-laugh and turns toward the window."
        ),
        "duration": 4,
    },
    {
        "n": 18, "label": "kitchen_clockwork_walk",
        "image_prompt": (
            f"Vertical 9:16 iPhone phone-shot, ungraded. {SUBJECT} in a faded "
            "light-blue sweatshirt and well-worn jeans, walking from her own sunlit "
            "kitchen toward the phone (handheld POV from waist height, like a friend "
            "is filming). Coffee mug in one hand, easy mid-stride smile. Kitchen "
            "background: dishes drying on rack, magnets on fridge, mail stack on "
            "counter (lived-in, not staged). Harsh midday window light from the right, "
            "hard contact shadow on the floor. iPhone 15 Pro wide. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "She walks toward the camera, smiles wider mid-stride, then glances out "
            "the sunlit window to her left."
        ),
        "duration": 4,
    },
    {
        "n": 19, "label": "anim_brain_nutrient",
        "image_prompt": (
            "Animated medical 3D rendering, a human brain glowing with gentle warm "
            "purple-gold energy, small colorful nutrient particles drifting up from "
            "the digestive system to the brain via translucent spinal pathway, "
            f"{ANIM_3D}, no text. 9:16."
        ),
        "image_refs": [],
        "kling_prompt": (
            "Nutrient particles drift upward toward the brain, the brain gently "
            "brightens as energy flows in."
        ),
        "duration": 4,
    },
    {
        "n": 20, "label": "cta_60_day_guarantee",
        "image_prompt": (
            "Vertical 9:16 product hero, slightly elevated camera. The Motilli jar "
            "from the reference image (label and dark forest-green heart-shaped "
            "gummies must match the reference exactly — gummies are DARK GREEN, Green "
            "Apple flavor) sits on a worn butcher-block counter (NOT pristine marble) "
            "in a real kitchen. Two dark green heart gummies in front of the jar. "
            "Hard slanted window light from camera-left, dust motes in the beam. "
            f"Small green '60-DAY GUARANTEE' badge overlaid upper-right. {SUBJECT} "
            "partially in frame on the right edge in a worn olive shirt, hand "
            "mid-reach toward the jar. iPhone 15 Pro wide. 9:16."
        ),
        "image_refs": [MOTILLI_PRODUCT_UPLOAD],
        "kling_prompt": (
            "Hand-held drift forward toward the jar, ~6cm of motion total. The "
            "woman's hand enters frame and lightly touches the jar. Autofocus "
            "re-locks once on the jar."
        ),
        "duration": 6,  # closer gets extra second
    },
]


def parse_result(out, beat_n, kind):
    out = out.strip()
    for start_char in ('[', '{'):
        idx = out.find(start_char)
        while idx != -1:
            try:
                data = json.loads(out[idx:])
                if isinstance(data, list):
                    if not data:
                        return None, None
                    item = data[0]
                else:
                    item = data
                job_id = item.get('id')
                result_url = item.get('result_url') or item.get('url')
                if not result_url:
                    for r in (item.get('results') or []):
                        if r.get('result_url') or r.get('url'):
                            result_url = r.get('result_url') or r.get('url')
                            break
                return job_id, result_url
            except json.JSONDecodeError:
                idx = out.find(start_char, idx + 1)
                continue
    print(f"[BEAT {beat_n}] {kind} no parseable JSON in output")
    return None, None


def run(cmd):
    print(f"\n$ {cmd[:200]}{'...' if len(cmd) > 200 else ''}", flush=True)
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout[-1500:])
    if proc.returncode != 0 and proc.stderr:
        print(f"STDERR: {proc.stderr[:1500]}")
    return proc.returncode, proc.stdout, proc.stderr


def gen_image(beat):
    img_args = " ".join(f'--image {r}' for r in beat['image_refs'])
    cmd = (
        f"higgsfield generate create nano_banana_2 "
        f"--prompt {shlex.quote(beat['image_prompt'])} {img_args} "
        f"--aspect_ratio 9:16 --resolution 2k "
        f"--wait --wait-timeout 5m --json"
    )
    rc, out, _ = run(cmd)
    if rc != 0:
        return None, None
    return parse_result(out, beat['n'], "image")


def gen_video(beat, image_job_id):
    full_prompt = f"{beat['kling_prompt']} {ORGANIC_CUES}"
    cmd = (
        f"higgsfield generate create kling3_0 "
        f"--prompt {shlex.quote(full_prompt)} "
        f"--start-image {image_job_id} "
        f"--aspect_ratio 9:16 --duration {beat['duration']} --mode std --sound on "
        f"--wait --wait-timeout 15m --json"
    )
    rc, out, _ = run(cmd)
    if rc != 0:
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
        if prev.get('image_url') and prev.get('image_path') and Path(prev['image_path']).exists():
            print(f"[BEAT {n}] image already generated, skipping")
            img_job = prev.get('image_job_id')
        else:
            print(f"\n========== BEAT {n}: {beat['label']} — image ==========")
            img_job, img_url = gen_image(beat)
            if not img_job:
                print(f"[BEAT {n}] image fail, abort beat")
                continue
            img_path = GEN_DIR / 'images' / f"v3_beat_{n:02d}_{beat['label']}.png"
            if download(img_url, img_path):
                print(f"saved: {img_path}")
            manifest['beats'][bkey] = {
                **prev,
                'beat': beat['label'],
                'image_job_id': img_job,
                'image_url': img_url,
                'image_path': str(img_path),
                'image_prompt': beat['image_prompt'],
                'duration': beat['duration'],
            }
            save_manifest(manifest)
        if prev.get('video_url') and prev.get('video_path') and Path(prev['video_path']).exists():
            print(f"[BEAT {n}] video already generated, skipping")
            continue
        print(f"\n========== BEAT {n}: {beat['label']} — video ({beat['duration']}s) ==========")
        vid_job, vid_url = gen_video(beat, img_job)
        if not vid_job:
            print(f"[BEAT {n}] video fail")
            continue
        vid_path = GEN_DIR / 'videos' / f"v3_beat_{n:02d}_{beat['label']}.mp4"
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


if __name__ == "__main__":
    main()

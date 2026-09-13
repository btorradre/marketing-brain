#!/usr/bin/env python3
"""Animate all 34 generated images using Kling 3.0 via kie.ai API."""

import json
import os
import time
import requests

KIE_API_KEY = "[REDACTED_SECRET]"
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
MAX_RETRIES = 3
POLL_INTERVAL = 15
MAX_WAIT = 600  # 10 min per scene

OUTPUT_DIR = "/Users/brooksorradre2/Documents/marketing brain/video ad briefs/replicator-output"
CREATIVE_DIR_JSON = os.path.join(OUTPUT_DIR, "creative_direction/creative_direction.json")
GEN_DIR = os.path.join(OUTPUT_DIR, "generated")
ANIM_DIR = os.path.join(OUTPUT_DIR, "animated")

PRODUCT_IMG = None
for p in [
    os.path.expanduser("~/.claude/skills/vault/motilli/website assets/motilli product reference.png"),
    "/Users/brooksorradre2/Documents/marketing brain/statics/product references/motilli/motilli product reference.png",
]:
    if os.path.exists(p):
        PRODUCT_IMG = p
        break


def upload_image(image_path):
    """Upload image to temp host so Kling can access via URL."""
    try:
        with open(image_path, "rb") as f:
            resp = requests.post("https://0x0.st", files={"file": (os.path.basename(image_path), f)}, timeout=30)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception as e:
        print(f"  0x0.st failed: {e}")

    # Fallback: catbox.moe
    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": (os.path.basename(image_path), f)},
                timeout=30,
            )
        if resp.status_code == 200 and resp.text.startswith("http"):
            return resp.text.strip()
    except Exception as e:
        print(f"  catbox failed: {e}")

    return None


def poll_task(task_id, headers):
    """Poll Kling task until complete or timeout."""
    start = time.time()
    while time.time() - start < MAX_WAIT:
        try:
            resp = requests.get(KIE_STATUS_URL, headers=headers, params={"taskId": task_id}, timeout=30)
            data = resp.json()
            if data.get("code") != 200:
                time.sleep(POLL_INTERVAL)
                continue

            state = data["data"].get("state", "")
            if state == "success":
                result_json = json.loads(data["data"].get("resultJson", "{}"))
                urls = result_json.get("resultUrls", [])
                return urls[0] if urls else None
            elif state == "fail":
                print(f"    Task failed: {data['data'].get('failMsg', 'unknown')}")
                return None
            else:
                elapsed = int(time.time() - start)
                print(f"    Status: {state} ({elapsed}s)")
        except Exception as e:
            print(f"    Poll error: {e}")
        time.sleep(POLL_INTERVAL)

    print(f"    Timeout")
    return None


def build_motion_prompt(scene):
    """Build a Kling-compatible motion prompt from creative direction."""
    desc = scene["adaptation_description"]
    mood = scene.get("mood", "")
    role = scene.get("narrative_role", "")

    # Map narrative roles to motion types
    motion_map = {
        "villain_introduction": "Slow zoom in, character breathes and shifts weight slightly",
        "villain_personality_display": "Character laughs, body jiggles, subtle camera shake",
        "failed_solution_1": "Character stirs glass, grimaces, subtle hand tremor",
        "failed_solution_2": "Character pops item in mouth, hand moves to stomach",
        "villain_confidence": "Slow push in, character smirks, slight head tilt",
        "villain_confidence_escalation": "Character flexes arms slowly, slight camera drift",
        "villain_mocks_solutions": "Character leans forward, gas wisps float from mouth",
        "villain_demonstrates_ineffectiveness": "Arm gesture, sluggish wave pushes through, gas clouds rise",
        "villain_origin_reveal": "Slow zoom into dark passage, character recedes",
        "internal_journey_transition": "Smooth camera track downward through fleshy tunnel, pulsing walls",
        "villain_in_habitat": "Slow ambient drift, bacteria float, character settles",
        "villain_comfort": "Close-up, character sighs and stretches, contented motion",
        "villain_resilience_explanation": "Arms spread wide, gas burst, triumphant gesture",
        "avatar_discovery_villain_reaction": "Split: woman reads label intently / monster's eyes widen in alarm",
        "villain_panic_escalation": "Glowing capsule descends from above, monster shrinks back",
        "villain_deep_panic": "Monster trembles, capsule glows brighter approaching",
        "avatar_holds_product": "Woman holds up product pouch, examines it thoughtfully",
        "villain_mockery_of_product": "Monster recoils in disgust, tongue out",
        "villain_desperate_plea": "Monster flails arms desperately, screaming",
        "avatar_takes_product": "Woman pops gummy in mouth confidently, calm swallow",
        "villain_frantic_alarm": "Monster's eyes bulge, arms thrown out, frantic motion",
        "villain_begging": "Monster shakes and pleads, losing composure",
        "villain_realization_of_doom": "Monster points downward with shaking finger, horror on face",
        "villain_outrage": "Arms thrown up in outrage, dramatic gesture",
        "hero_introduction_1": "Bright droplet bounces into frame, energetic entrance, glowing trail",
        "hero_introduction_2": "Second droplet floats in alongside first, refreshing aura radiates",
        "heroes_in_action_initial": "Pulsing waves flow through walls, gas wisps get absorbed",
        "villain_suffering_1": "Monster screams, chunks dissolve, body shrinks",
        "villain_suffering_2_defeat": "Monster dissolves into puddle, heroes hover triumphantly",
        "transformation_avatar_reflection": "Woman touches stomach, exhales sparkling mist, smiles",
        "call_to_action_solution": "Woman pats stomach, holds product, confident posture",
        "product_details_1": "Product pouch with animated face smiles, tiny monster clings miserably",
        "product_details_2_offer": "Product pouch winks at viewer, highlight shimmer",
        "cta_final_defeat": "Monster floats off screen, product stands confidently",
    }

    motion = motion_map.get(role, "Subtle ambient motion, gentle camera drift")

    prompt = f"{desc} Motion: {motion}. Mood: {mood}."
    # Kling limit is 2500 chars
    if len(prompt) > 2500:
        prompt = prompt[:2497] + "..."
    return prompt


def main():
    os.makedirs(ANIM_DIR, exist_ok=True)

    with open(CREATIVE_DIR_JSON) as f:
        cd = json.load(f)

    scenes = cd["scenes"]
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Upload product image once
    product_url = None
    if PRODUCT_IMG:
        product_url = upload_image(PRODUCT_IMG)
        if product_url:
            print(f"[INFO] Product image uploaded: {product_url}")

    total = len(scenes)
    succeeded = 0
    failed = 0
    skipped = 0

    for scene in scenes:
        sn = scene["scene_number"]
        scene_num = f"{sn:03d}"
        out_path = os.path.join(ANIM_DIR, f"scene_{scene_num}_animated.mp4")
        img_path = os.path.join(GEN_DIR, f"scene_{scene_num}_brand.png")

        if os.path.exists(out_path):
            print(f"[SKIP] Scene {sn}/{total} already animated")
            succeeded += 1
            continue

        if not os.path.exists(img_path):
            print(f"[SKIP] Scene {sn}/{total} — no image")
            skipped += 1
            continue

        print(f"[ANIM] Scene {sn}/{total} ({scene.get('narrative_role', '')})...")

        # Upload image
        image_url = upload_image(img_path)
        if not image_url:
            print(f"  [ERROR] Could not upload image")
            failed += 1
            continue

        # Build motion prompt
        kling_prompt = build_motion_prompt(scene)

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": "5",
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        # Add product as kling_element for product scenes
        if scene.get("include_product") and product_url:
            payload["input"]["kling_elements"] = [{
                "name": "motilli_product",
                "description": "Motilli gummies pouch - match exactly",
                "element_input_urls": [product_url]
            }]

        # Submit with retries
        success = False
        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    print(f"  Attempt {attempt+1} failed: {resp_data.get('msg', 'unknown')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                print(f"  Task: {task_id}")

                video_url = poll_task(task_id, headers)
                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    print(f"  [OK] Saved {out_path}")
                    succeeded += 1
                    success = True
                    break
                else:
                    print(f"  Attempt {attempt+1}: generation failed/timed out")

            except Exception as e:
                print(f"  Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            print(f"  [FAILED] Scene {sn}")
            failed += 1

        time.sleep(5)  # Rate limit

    print(f"\n{'='*60}")
    print(f"ANIMATION COMPLETE")
    print(f"  Succeeded: {succeeded}/{total}")
    print(f"  Failed: {failed}/{total}")
    print(f"  Skipped: {skipped}/{total}")
    print(f"  Output: {ANIM_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

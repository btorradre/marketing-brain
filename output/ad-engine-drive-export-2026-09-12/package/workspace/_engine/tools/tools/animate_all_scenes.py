#!/usr/bin/env python3
"""
Animate all 34 generated scenes using Kling 3.0 via kie.ai.
Reads creative_direction.json for motion/mood per scene.
"""

import json
import os
import re
import sys
import time
import requests
import base64

KIE_API_KEY = "[REDACTED_SECRET]"
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
MAX_RETRIES = 3

OUTPUT_DIR = "/Users/brooksorradre2/Documents/marketing brain/video ad briefs/replicator-output"
GEN_DIR = os.path.join(OUTPUT_DIR, "generated")
ANIM_DIR = os.path.join(OUTPUT_DIR, "animated")
CD_JSON = os.path.join(OUTPUT_DIR, "creative_direction/creative_direction.json")

# Product reference for product scenes
PRODUCT_IMG = None
for p in [
    os.path.expanduser("~/.claude/skills/vault/motilli/website assets/motilli product reference.png"),
    "/Users/brooksorradre2/Documents/marketing brain/statics/product references/motilli/motilli product reference.png",
]:
    if os.path.exists(p):
        PRODUCT_IMG = p
        break


def upload_image_for_kling(image_path):
    """Upload image to kie.ai's file hosting so Kling can access it via URL."""
    KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                KIE_UPLOAD_URL,
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                files={"file": (os.path.basename(image_path), f, "image/png")},
                data={"uploadPath": "images"},
                timeout=60,
            )
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("downloadUrl"):
            url = data["data"]["downloadUrl"]
            return url
        else:
            print(f"  [UPLOAD ERROR] {data}")
    except Exception as e:
        print(f"  [UPLOAD ERROR] {e}")

    return None


def poll_kling_task(task_id, headers, max_wait=900):
    """Poll until Kling task completes."""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(
                f"{KIE_STATUS_URL}?taskId={task_id}",
                headers=headers,
                timeout=30
            )
            data = resp.json()
            if data.get("code") == 200:
                state = data["data"].get("state", "")
                if state == "success":
                    result_json = json.loads(data["data"].get("resultJson", "{}"))
                    urls = result_json.get("resultUrls", [])
                    if urls:
                        return urls[0]
                elif state == "failed":
                    fail_msg = data["data"].get("failMsg", "unknown")
                    print(f"  [FAILED] Task {task_id}: {fail_msg}")
                    return None
                # Still processing — keep polling
        except Exception as e:
            print(f"  [POLL ERROR] {e}")
        time.sleep(20)
    print(f"  [TIMEOUT] Task {task_id}")
    return None


def build_motion_prompt(scene):
    """Build a Kling motion prompt from creative direction."""
    role = scene.get("narrative_role", "")
    desc = scene.get("adaptation_description", "")
    mood = scene.get("mood", "")

    # Motion mapping based on narrative role
    motion_map = {
        "villain_introduction": "Slow zoom in on the monster. Subtle pulsing of its body. Faint wisps of gas float upward. Camera holds steady, dramatic reveal.",
        "villain_personality_display": "The monster jiggles and laughs. Slight camera shake from its rumbling. Gas wisps drift lazily.",
        "failed_solution_1": "Woman stirs powder in glass with frustrated motion. Camera at eye level, slight handheld feel.",
        "failed_solution_2": "Woman pops chew into mouth, hand moves to stomach. Subtle camera push-in on her discomfort.",
        "villain_confidence": "Monster stands firm, unmoving. Slow dolly forward. Atmosphere feels heavy and oppressive.",
        "villain_confidence_escalation": "Monster flexes thick limbs. Slight camera tilt up to emphasize its size.",
        "villain_mocks_solutions": "Monster leans forward conspiratorially. Gas cloud puffs from mouth. Camera slightly wobbles.",
        "villain_demonstrates_ineffectiveness": "Heavy arm gesture, sluggish wave pushes through gut. Camera follows the wave motion.",
        "villain_origin_reveal": "Monster recedes into dark passage. Camera slowly follows it deeper. Lighting dims.",
        "internal_journey_transition": "Dramatic camera dive downward through fleshy tube. Fast dolly forward. Green light grows at end.",
        "villain_in_habitat": "Monster settled in stomach chamber. Slow pan across the stagnant environment. Subtle ambient movement of bacteria.",
        "villain_comfort": "Close-up, monster sighs and stretches. Slow breathing motion. Camera gently drifts.",
        "villain_resilience_explanation": "Monster spreads arms wide, burst of gas. Camera pulls back slightly to show full gesture.",
        "avatar_discovery_villain_reaction": "Split focus — woman reading label, monster jolting in alarm. Quick cut energy.",
        "villain_panic_escalation": "Glowing gummy descends from above. Monster shrinks back. Camera tilts down following the gummy.",
        "villain_deep_panic": "Monster trembles visibly. Gummy glows closer. Camera slow push-in on terrified face.",
        "avatar_holds_product": "Woman holds up product pouch. Soft zoom on the packaging. Warm lighting.",
        "villain_mockery_of_product": "Monster recoils in disgust, tongue out. Quick camera shake.",
        "villain_desperate_plea": "Split scene — woman holding gummy, monster screaming and flailing arms. Dynamic energy.",
        "avatar_takes_product": "Woman pops gummy into mouth confidently. Smooth camera, warm lighting. Calm resolve.",
        "villain_frantic_alarm": "Monster eyes bulging, arms thrown out. Gummy descending fast. Shaky, frantic camera.",
        "villain_begging": "Monster trembling, pleading posture. Camera circles slightly. Losing control energy.",
        "villain_realization_of_doom": "Monster points downward in horror. Camera follows its gaze down into the gut.",
        "villain_outrage": "Arms thrown up in outrage. Camera shake. Dramatic zoom on face.",
        "hero_introduction_1": "Bright green droplet bounces in. Energetic entrance. Camera tracks its bouncy movement. Sparkle effects.",
        "hero_introduction_2": "Second droplet floats in alongside first. Camera widens to show both. Refreshing aura radiates.",
        "heroes_in_action_initial": "Pulsing waves from Apigenin. Chlorophyll absorbs gas wisps. Dynamic dual action. Camera pans between them.",
        "villain_suffering_1": "Monster screaming, body dissolving. Chunks breaking off. Camera close on agonized face.",
        "villain_suffering_2_defeat": "Monster almost gone, faint wisps remain. Gut becomes pink and healthy. Camera pulls back triumphantly.",
        "transformation_avatar_reflection": "Woman smiles in mirror, touches stomach. Sparkling mist on exhale. Warm golden lighting. Slow zoom.",
        "call_to_action_solution": "Woman holds product, pats stomach. Confident pose. Camera at hero angle, slightly low.",
        "product_details_1": "Close-up product with animated face. Tiny defeated monster on corner. Gentle bounce animation.",
        "product_details_2_offer": "Product winks at viewer. Highlight text pops. Friendly promotional energy.",
        "cta_final_defeat": "Product stands tall. Tiny monster floats away. Firm reassuring smile. Camera holds steady on product.",
    }

    motion = motion_map.get(role, "Gentle camera movement. Subtle ambient motion. Smooth cinematic feel.")

    prompt = f"{desc} {motion} Mood: {mood}. Animated 3D style, Pixar/claymation aesthetic, soft lighting, cinematic."

    # Trim to Kling's limit
    if len(prompt) > 2500:
        prompt = prompt[:2497] + "..."

    return prompt


def main():
    os.makedirs(ANIM_DIR, exist_ok=True)

    with open(CD_JSON) as f:
        cd = json.load(f)

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Upload product image once
    product_url = None
    if PRODUCT_IMG and os.path.exists(PRODUCT_IMG):
        print(f"[INFO] Uploading product reference: {PRODUCT_IMG}")
        product_url = upload_image_for_kling(PRODUCT_IMG)
        if product_url:
            print(f"[INFO] Product URL: {product_url}")

    total = len(cd["scenes"])
    succeeded = 0
    failed = 0
    skipped = 0

    for scene in cd["scenes"]:
        sn = scene["scene_number"]
        scene_num = f"{sn:03d}"
        image_path = os.path.join(GEN_DIR, f"scene_{scene_num}_brand.png")
        out_path = os.path.join(ANIM_DIR, f"scene_{scene_num}_animated.mp4")

        # Skip if already animated
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            print(f"[SKIP] Scene {sn} already animated")
            skipped += 1
            succeeded += 1
            continue

        if not os.path.exists(image_path):
            print(f"[SKIP] Scene {sn} — no image found at {image_path}")
            failed += 1
            continue

        print(f"\n[ANIM] Scene {sn}/{total} ({scene.get('narrative_role', '')})")

        # Upload image
        image_url = upload_image_for_kling(image_path)
        if not image_url:
            print(f"  [ERROR] Could not upload image for scene {sn}")
            failed += 1
            continue

        # Build motion prompt
        motion_prompt = build_motion_prompt(scene)
        print(f"  [PROMPT] {motion_prompt[:120]}...")

        # Determine duration based on narrative role
        role = scene.get("narrative_role", "")
        if role in ("internal_journey_transition", "heroes_in_action_initial", "villain_suffering_1", "villain_suffering_2_defeat"):
            duration = "10"
        elif role in ("villain_introduction", "transformation_avatar_reflection", "call_to_action_solution"):
            duration = "10"
        elif role in ("villain_frantic_alarm", "villain_begging", "villain_outrage"):
            duration = "5"
        else:
            duration = "5"

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": motion_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": duration,
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        # Add product as kling_element only for product scenes
        include_product = scene.get("include_product", False)
        if include_product and product_url:
            payload["input"]["kling_elements"] = [{
                "name": "motilli_product",
                "description": "Motilli gummies product pouch — maintain exact appearance",
                "element_input_urls": [product_url]
            }]

        # Submit with retries
        success = False
        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    print(f"  [RETRY {attempt+1}] {resp_data.get('msg', 'unknown')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                print(f"  [TASK] {task_id}")

                video_url = poll_kling_task(task_id, headers)

                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as vf:
                        vf.write(vid_resp.content)
                    print(f"  [OK] Saved {out_path} ({os.path.getsize(out_path)} bytes)")
                    succeeded += 1
                    success = True
                    break
                else:
                    print(f"  [RETRY {attempt+1}] Generation failed or timed out")

            except Exception as e:
                print(f"  [ERROR] Attempt {attempt+1}: {e}")
                time.sleep(10)

        if not success:
            print(f"  [FAILED] Scene {sn} could not be animated")
            failed += 1

        time.sleep(5)  # Rate limiting

    print(f"\n{'='*60}")
    print(f"ANIMATION COMPLETE")
    print(f"  Succeeded: {succeeded}/{total}")
    print(f"  Failed:    {failed}/{total}")
    print(f"  Skipped (cached): {skipped}")
    print(f"  Output:    {ANIM_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

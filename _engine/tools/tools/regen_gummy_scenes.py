#!/usr/bin/env python3
"""Regenerate scenes 19 and 20 with image-to-image using product reference for accurate gummy."""

import json
import os
import time

from google import genai
from google.genai import types

GEMINI_API_KEY = "[REDACTED_SECRET]"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"

OUTPUT_DIR = "/Users/brooksorradre2/Documents/marketing brain/video ad briefs/replicator-output"
CREATIVE_DIR_JSON = os.path.join(OUTPUT_DIR, "creative_direction/creative_direction.json")
GEN_DIR = os.path.join(OUTPUT_DIR, "generated")

PRODUCT_IMG = None
for p in [
    os.path.expanduser("~/.claude/skills/vault/motilli/website assets/motilli product reference.png"),
    "/Users/brooksorradre2/Documents/marketing brain/statics/product references/motilli/motilli product reference.png",
]:
    if os.path.exists(p):
        PRODUCT_IMG = p
        break

SCENES_TO_REGEN = [19, 20]


def main():
    with open(CREATIVE_DIR_JSON) as f:
        cd = json.load(f)

    client = genai.Client(api_key=GEMINI_API_KEY)

    if not PRODUCT_IMG or not os.path.exists(PRODUCT_IMG):
        print("[ERROR] No product reference image found!")
        return

    with open(PRODUCT_IMG, "rb") as f:
        product_part = types.Part(inline_data=types.Blob(data=f.read(), mime_type="image/png"))
    print(f"[INFO] Product reference: {PRODUCT_IMG}")

    scenes_map = {s["scene_number"]: s for s in cd["scenes"]}

    for sn in SCENES_TO_REGEN:
        scene = scenes_map.get(sn)
        if not scene:
            print(f"[ERROR] Scene {sn} not found")
            continue

        scene_num = f"{sn:03d}"
        out_path = os.path.join(GEN_DIR, f"scene_{scene_num}_brand.png")

        # Delete existing to force regeneration
        if os.path.exists(out_path):
            os.remove(out_path)

        desc = scene["adaptation_description"]
        mood = scene.get("mood", "")

        print(f"[GEN] Scene {sn} ({scene.get('narrative_role', '')}) — IMAGE-TO-IMAGE with product ref...")

        edit_prompt = (
            f"I'm providing a product reference image showing Motilli gummies. "
            f"Use this reference to understand EXACTLY what the gummy looks like — its color, shape, texture, and size. "
            f"Generate the following scene, making sure any gummy shown matches the Motilli gummy from the reference EXACTLY:\n\n"
            f"{desc}\n\n"
            f"MOOD: {mood}\n\n"
            f"STYLE: Animated 3D character illustration, Pixar/claymation aesthetic, soft lighting, "
            f"vibrant yet slightly muted colors, cinematic 16:9 composition.\n\n"
            f"CRITICAL: The gummy must look EXACTLY like the one on the Motilli product packaging — same color, shape, and texture. "
            f"Do NOT invent a different gummy design.\n\n"
            f"IMPORTANT: Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays."
        )

        parts = [product_part, types.Part(text=edit_prompt)]

        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                )
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(out_path, "wb") as f:
                        f.write(part.inline_data.data)
                    saved = True
                    print(f"  [OK] Saved {out_path}")
                    break

            if not saved:
                for part in response.candidates[0].content.parts:
                    if part.text:
                        print(f"  [WARN] Text response: {part.text[:200]}")

            time.sleep(3)

        except Exception as e:
            print(f"  [ERROR] {e}")
            time.sleep(10)

    print("\n[DONE] Scenes 19 & 20 regenerated with correct Motilli gummy.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate product scenes (17, 31-34) using IMAGE-TO-IMAGE with product reference."""

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

# Product reference image
PRODUCT_IMG = None
for p in [
    os.path.expanduser("~/.claude/skills/vault/motilli/website assets/motilli product reference.png"),
    "/Users/brooksorradre2/Documents/marketing brain/statics/product references/motilli/motilli product reference.png",
]:
    if os.path.exists(p):
        PRODUCT_IMG = p
        break

PRODUCT_SCENES = [17, 31, 32, 33, 34]


def main():
    with open(CREATIVE_DIR_JSON) as f:
        cd = json.load(f)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Load product reference as image part
    if not PRODUCT_IMG or not os.path.exists(PRODUCT_IMG):
        print("[ERROR] No product reference image found!")
        return

    with open(PRODUCT_IMG, "rb") as f:
        product_part = types.Part(inline_data=types.Blob(data=f.read(), mime_type="image/png"))
    print(f"[INFO] Product reference: {PRODUCT_IMG}")

    scenes_map = {s["scene_number"]: s for s in cd["scenes"]}

    for sn in PRODUCT_SCENES:
        scene = scenes_map.get(sn)
        if not scene:
            print(f"[ERROR] Scene {sn} not found in creative direction")
            continue

        scene_num = f"{sn:03d}"
        out_path = os.path.join(GEN_DIR, f"scene_{scene_num}_brand.png")

        if os.path.exists(out_path):
            print(f"[SKIP] Scene {sn} already exists")
            continue

        desc = scene["adaptation_description"]
        mood = scene.get("mood", "")

        print(f"[GEN] Scene {sn} ({scene.get('narrative_role', '')}) — IMAGE-TO-IMAGE with product ref...")

        # IMAGE-TO-IMAGE: Send product reference image + editing prompt
        edit_prompt = (
            f"Edit this product image to place it in the following scene context. "
            f"Keep the product (Motilli gummies pouch) EXACTLY as shown — same shape, label, colors, branding. "
            f"Do NOT modify the product packaging in any way. "
            f"Build the scene AROUND the product based on this description:\n\n"
            f"{desc}\n\n"
            f"MOOD: {mood}\n\n"
            f"STYLE: Animated 3D character illustration, Pixar/claymation aesthetic, soft lighting, "
            f"vibrant yet slightly muted colors, cinematic 16:9 composition.\n\n"
            f"IMPORTANT: Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays. "
            f"The image must be completely text-free."
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

    print("\n[DONE] Product scenes regenerated with image-to-image.")


if __name__ == "__main__":
    main()

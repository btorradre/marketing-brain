#!/usr/bin/env python3
"""Generate text-to-image frames from creative direction JSON using Nano Banana 2."""

import json
import os
import sys
import time

from google import genai
from google.genai import types

GEMINI_API_KEY = "[REDACTED_SECRET]"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"

OUTPUT_DIR = "/Users/brooksorradre2/Documents/marketing brain/video ad briefs/replicator-output"
CREATIVE_DIR_JSON = os.path.join(OUTPUT_DIR, "creative_direction/creative_direction.json")
GEN_DIR = os.path.join(OUTPUT_DIR, "generated")

# Product reference image (only used when include_product=True)
PRODUCT_IMG = None
for p in [
    os.path.expanduser("~/.claude/skills/vault/motilli/website assets/motilli product reference.png"),
    "/Users/brooksorradre2/Documents/marketing brain/statics/product references/motilli/motilli product reference.png",
]:
    if os.path.exists(p):
        PRODUCT_IMG = p
        break

def main():
    os.makedirs(GEN_DIR, exist_ok=True)
    
    with open(CREATIVE_DIR_JSON) as f:
        cd = json.load(f)
    
    scenes = cd["scenes"]
    villain = cd["villain"]
    heroes = cd["heroes"]
    avatar = cd["avatar"]
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Pre-load product image
    product_part = None
    if PRODUCT_IMG and os.path.exists(PRODUCT_IMG):
        with open(PRODUCT_IMG, "rb") as f:
            product_part = types.Part(inline_data=types.Blob(data=f.read(), mime_type="image/png"))
        print(f"[INFO] Loaded product reference: {PRODUCT_IMG}")
    
    # Build prompts JSON for record-keeping
    prompts_dir = os.path.join(OUTPUT_DIR, "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    all_prompts = []
    
    total = len(scenes)
    succeeded = 0
    failed = 0
    
    for scene in scenes:
        sn = scene["scene_number"]
        scene_num = f"{sn:03d}"
        out_path = os.path.join(GEN_DIR, f"scene_{scene_num}_brand.png")
        
        # Skip if already generated
        if os.path.exists(out_path):
            print(f"[SKIP] Scene {sn}/{total} already generated")
            succeeded += 1
            continue
        
        include_product = scene.get("include_product", False)
        desc = scene["adaptation_description"]
        mood = scene.get("mood", "")
        narrative_role = scene.get("narrative_role", "")
        
        # Build rich text-to-image prompt
        style_prefix = (
            "Animated 3D character illustration style, similar to Pixar/claymation aesthetic. "
            "Soft lighting, vibrant yet slightly muted color palette. "
            "Cinematic composition, 16:9 aspect ratio. "
        )
        
        prompt_text = (
            f"{style_prefix}\n\n"
            f"SCENE DESCRIPTION: {desc}\n\n"
            f"MOOD: {mood}\n\n"
            f"IMPORTANT RULES:\n"
            f"- Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays of any kind\n"
            f"- The image must be completely text-free\n"
            f"- Match the described mood and visual direction precisely\n"
        )
        
        if not include_product:
            prompt_text += "- Do NOT include any product packaging, bottles, pouches, or branded items\n"
        
        # Save prompt for records
        all_prompts.append({
            "scene_number": sn,
            "narrative_role": narrative_role,
            "generation_mode": "text_to_image",
            "include_product": include_product,
            "image_prompt": prompt_text,
        })
        
        print(f"[GEN] Scene {sn}/{total} ({narrative_role}, product={'YES' if include_product else 'NO'})...")
        
        try:
            parts = []
            if include_product and product_part:
                parts.append(product_part)
                prompt_text += (
                    "\n- I've included a product reference image. Include this Motilli gummies pouch "
                    "in the scene as described. Match the product appearance exactly.\n"
                )
            
            parts.append(types.Part(text=prompt_text))
            
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
                # Check for text response (might be refusal)
                for part in response.candidates[0].content.parts:
                    if part.text:
                        print(f"  [WARN] Text response instead of image: {part.text[:200]}")
                failed += 1
                continue
            
            succeeded += 1
            
            # Rate limiting — small delay between calls
            time.sleep(2)
            
        except Exception as e:
            print(f"  [ERROR] Scene {sn}: {e}")
            failed += 1
            # Back off on errors
            if "429" in str(e) or "quota" in str(e).lower() or "rate" in str(e).lower():
                print("  [WAIT] Rate limited — waiting 30s...")
                time.sleep(30)
            else:
                time.sleep(5)
    
    # Save prompts JSON
    with open(os.path.join(prompts_dir, "image_prompts.json"), "w") as f:
        json.dump(all_prompts, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"  Succeeded: {succeeded}/{total}")
    print(f"  Failed: {failed}/{total}")
    print(f"  Output: {GEN_DIR}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

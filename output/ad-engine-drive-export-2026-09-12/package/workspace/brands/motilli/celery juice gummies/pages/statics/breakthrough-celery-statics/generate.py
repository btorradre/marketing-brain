#!/usr/bin/env python3
"""Batch-generate 15 Motilli Breakthrough Celery Juice statics via Nano Banana Pro."""
import os, sys, concurrent.futures, traceback
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = "[REDACTED_SECRET]"
MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro — best for text rendering
ASPECT = "4:5"
OUT = Path(__file__).parent

client = genai.Client(api_key=API_KEY)

# ---------- CONCEPT 1 — HealthInsider editorial chyron ----------
C1_SCENE = (
    "Top 60% of composition: painterly watercolor editorial illustration, 1970s-80s vintage editorial style. "
    "Rolling Italian countryside celery field at golden hour. A large hand-carved wooden archway stands in the "
    "center of the field with the words 'GUT HEALTH' carved into a wooden banner across the top of the archway. "
    "A small group of women ages 45-65 in casual modern clothing (sweaters, jeans, simple tops) walks from the "
    "foreground toward the archway with their backs to the viewer. Warm pink-orange-gold sunset sky behind the "
    "archway. Distant mountains. Celery stalks and leaves growing on both sides of the path. Muted warm palette. "
    "Bottom 40% of composition is clean solid white background reserved for text."
)
C1_LAYOUT = (
    "Layout for the bottom 40% white area: "
    "Top-left: a small red rectangular chyron tag (editorial red #D9261C) containing the white uppercase text "
    "'GLP-HEALTH.NEWS' in a bold sans-serif. "
    "Below the tag, a large black Playfair Display serif headline, left-aligned, headline case, 4 lines: "
    "{HEADLINE}. "
    "Below the headline, an italic dark-gray serif subhead: {SUBHEAD}. "
    "Below the subhead, a bold red (#D9261C) sans-serif CTA reading 'READ MORE →'. "
    "At the very bottom, a tiny 10pt gray disclaimer reading 'Results may vary. Intended for GLP-1 medication users.' "
    "All text spelled exactly as written, no added or omitted words."
)

# ---------- CONCEPT 2 — Clinical mechanism reveal ----------
C2_SCENE = (
    "Top 75% of composition: dramatic photorealistic 3D medical cross-section of a human stomach interior. "
    "Dark moody atmosphere, deep reds and browns. The stomach is partially full of stagnant, partially digested "
    "food with visible bacterial overgrowth and fermentation bubbles. Subtle yellow-tinted hydrogen sulfide gas "
    "bubbles rise from the food mass. Flowing down from the top of the frame into the stomach are glowing bright "
    "Motilli-green (#94C218) molecular particles representing apigenin — they break apart the stagnant food and "
    "the smooth muscle walls of the stomach glow bright green where the particles touch. High-end medical textbook "
    "visualization, photorealistic, moody dramatic lighting. "
    "Bottom 25% of composition is solid pure black, reserved for text overlay."
)
C2_LAYOUT = (
    "Layout for the bottom 25% black area: "
    "Main headline in bold sans-serif, center-aligned, 3 lines: {HEADLINE}. "
    "In the headline, render '{HL_YELLOW}' in bright yellow-green (#D4FF00), render '{HL_RED}' in signal red "
    "(#EF4A65), and render all other headline words in pure white. "
    "Below the headline, a smaller italic light-gray subhead, center-aligned: {SUBHEAD}. "
    "All text spelled exactly as written, no added or omitted words."
)

# ---------- CONCEPT 3 — Soft editorial question ----------
C3_SCENE = (
    "Minimalist premium editorial composition on warm cream off-white background (#F9F5EC). "
    "Centered hero: a translucent, glassy 3D rendering of an anatomically realistic human stomach, "
    "semi-transparent with iridescent pale green and subtle pink tints, catching soft light. Dreamy glass-like "
    "material finish, floating as if suspended. Museum digital-exhibit aesthetic. Soft even ambient lighting. "
    "Top 20% and bottom 25% of the composition are clean empty cream negative space, reserved for text."
)
C3_LAYOUT = (
    "Layout: "
    "Top 20% cream area — a dark charcoal (#1A1A1A) Playfair Display serif headline, center-aligned, 3 lines: "
    "{HEADLINE}. Below the headline, a smaller lighter-gray sans-serif subhead, center-aligned: {SUBHEAD}. "
    "Bottom 25% cream area — a prominent pill-shaped button with solid signal-red fill (#EF4A65), centered, "
    "containing white bold uppercase sans-serif text: {CTA}. Generous whitespace around the button. "
    "All text spelled exactly as written."
)

# ---------- CONCEPT 4 — Before/after clinical proof ----------
C4_SCENE = (
    "Solid black (#000000) background. Middle 65% of composition is a side-by-side medical cross-section "
    "comparison separated by a thin white vertical dividing line. "
    "LEFT PANEL: 3D rendered anatomical cross-section of a bloated, food-stagnant human stomach — distended, "
    "dark red-brown congested tissue, visible partially digested food sitting stagnant, small hydrogen sulfide "
    "fermentation bubbles rising, unhealthy appearance. "
    "RIGHT PANEL: the same anatomical cross-section but healthy and in motion — smaller, smooth muscle tone, "
    "food in proper transit, healthy pink-red tissue, a subtle Motilli-green (#94C218) glow around the muscle walls. "
    "At the very top of the left panel, small white uppercase sans-serif text 'BEFORE'. "
    "At the very top of the right panel, small white uppercase sans-serif text 'AFTER'. "
    "Top 20% and bottom 15% of the composition are empty pure black, reserved for text overlay. "
    "Realistic medical rendering, dramatic lighting."
)
C4_LAYOUT = (
    "Layout: "
    "Top 20% black area — a bold uppercase sans-serif headline, center-aligned, 3 lines: {HEADLINE}. "
    "Render '{HL_YELLOW}' in bright yellow-green (#D4FF00). Render all other headline words in pure white. "
    "Bottom 15% black area — a white sans-serif caption line, center-aligned: {CAPTION}. "
    "Below the caption, a tiny gray italic credit line, center-aligned: {CREDIT}. "
    "All text spelled exactly as written."
)

# ---------- CONCEPT 5 — Provocative metaphor hero ----------
C5_SCENE = (
    "Premium editorial food-meets-wellness photography. Close-up hero shot: a human hand with warm natural skin "
    "tone, clean short unpolished nails, no jewelry, gently holding a single fresh celery stalk cut lengthwise "
    "to reveal its inner fibrous pale-green interior. Small water dewdrops catch the light on the celery's surface. "
    "Background is soft muted cream / pale celery-green, slightly out of focus. Soft natural window lighting. "
    "The hand holds the celery vertically, almost presented. High-end magazine editorial aesthetic. "
    "Top 75% of composition is the hero shot. Bottom 25% is clean cream negative space reserved for text."
)
C5_LAYOUT = (
    "Layout: "
    "Bottom 25% cream area — a bold dark-charcoal (#1A1A1A) sans-serif headline, left-aligned, 2 lines: "
    "{HEADLINE}. "
    "Below the headline, a smaller dark-charcoal underlined sans-serif link reading 'Read More'. "
    "All text spelled exactly as written."
)

# ---------- ASSEMBLE ALL 15 ADS ----------
ADS = [
    # Concept 1
    {
        "file": "motilli_celery_concept1_varA.png",
        "scene": C1_SCENE,
        "layout": C1_LAYOUT.format(
            HEADLINE="'MD in Gastroenterology Reveals TOP Celery Juice Compound to Reset GLP-1 Bloating Without Prescriptions or Laxatives'",
            SUBHEAD="'And why she no longer recommends Miralax to her Ozempic® patients.'",
        ),
    },
    {
        "file": "motilli_celery_concept1_varB.png",
        "scene": C1_SCENE,
        "layout": C1_LAYOUT.format(
            HEADLINE="'Gastroenterologist Warns: 99% of Ozempic® Women Are Treating GLP-1 Bloating in the Wrong Organ — Here\\'s Why'",
            SUBHEAD="'The compound she now recommends — available without a prescription for under $1 a day.'",
        ),
    },
    {
        "file": "motilli_celery_concept1_varC.png",
        "scene": C1_SCENE,
        "layout": C1_LAYOUT.format(
            HEADLINE="'Why 46% of Women on GLP-1s Quit Within a Year — And the Breakthrough Celery Juice Compound That\\'s Changing It'",
            SUBHEAD="'A gastroenterologist explains what she now gives her Mounjaro® patients instead of Miralax.'",
        ),
    },
    # Concept 2
    {
        "file": "motilli_celery_concept2_varA.png",
        "scene": C2_SCENE,
        "layout": C2_LAYOUT.format(
            HEADLINE="'This is what Celery Juice actually does to GLP-1 bloat.'",
            HL_YELLOW="Celery Juice",
            HL_RED="GLP-1 bloat",
            SUBHEAD="'Uncover the real mechanism behind apigenin — and how it wakes up the Ozempic® stomach your laxatives can\\'t reach.'",
        ),
    },
    {
        "file": "motilli_celery_concept2_varB.png",
        "scene": C2_SCENE,
        "layout": C2_LAYOUT.format(
            HEADLINE="'This is what your GLP-1 is doing to the food in your stomach.'",
            HL_YELLOW="food in your stomach",
            HL_RED="GLP-1",
            SUBHEAD="'Why Miralax can\\'t reach it — and the breakthrough celery juice compound that can.'",
        ),
    },
    {
        "file": "motilli_celery_concept2_varC.png",
        "scene": C2_SCENE,
        "layout": C2_LAYOUT.format(
            HEADLINE="'The real cause of GLP-1 sulfur burps — and how to stop them at the source.'",
            HL_YELLOW="stop them at the source",
            HL_RED="GLP-1",
            SUBHEAD="'The celery juice compound changing how Ozempic® bloating is treated in 2026.'",
        ),
    },
    # Concept 3
    {
        "file": "motilli_celery_concept3_varA.png",
        "scene": C3_SCENE,
        "layout": C3_LAYOUT.format(
            HEADLINE="'You Might Have GLP-1 Stomach Slowdown and Not Realise It.'",
            SUBHEAD="'Cement stomach you\\'ve blamed on diet. Sulfur burps you\\'ve blamed on nausea. Bloating you\\'ve accepted as part of the shot. These may all be the same thing.'",
            CTA="'IS IT YOUR STOMACH?'",
        ),
    },
    {
        "file": "motilli_celery_concept3_varB.png",
        "scene": C3_SCENE,
        "layout": C3_LAYOUT.format(
            HEADLINE="'The Part of Your GLP-1 That No One Warned You About.'",
            SUBHEAD="'Half of women on Ozempic®, Wegovy®, Mounjaro® and Zepbound® experience what doctors call delayed gastric emptying. Most never find out it has a name — or a breakthrough natural fix.'",
            CTA="'LEARN THE FIX →'",
        ),
    },
    {
        "file": "motilli_celery_concept3_varC.png",
        "scene": C3_SCENE,
        "layout": C3_LAYOUT.format(
            HEADLINE="'The Real Reason Every Laxative Failed Your GLP-1 Stomach.'",
            SUBHEAD="'It\\'s not your dose. It\\'s not your fiber intake. It\\'s not you. It\\'s six feet of anatomy between where they work and where your medication actually slowed things down.'",
            CTA="'READ THE RESEARCH →'",
        ),
    },
    # Concept 4
    {
        "file": "motilli_celery_concept4_varA.png",
        "scene": C4_SCENE,
        "layout": C4_LAYOUT.format(
            HEADLINE="'CELERY JUICE = CEMENT STOMACH GONE IN 5 DAYS'",
            HL_YELLOW="CELERY JUICE",
            CAPTION="'The natural prokinetic now replacing Miralax for GLP-1 women.'",
            CREDIT="'Based on 412-user consumer trial · 2024'",
        ),
    },
    {
        "file": "motilli_celery_concept4_varB.png",
        "scene": C4_SCENE,
        "layout": C4_LAYOUT.format(
            HEADLINE="'APIGENIN = SULFUR BURPS GONE IN 48 HOURS'",
            HL_YELLOW="APIGENIN",
            CAPTION="'The celery juice compound that reaches where Gas-X, Tums, and Pepto never could.'",
            CREDIT="'Based on 412-user consumer trial · 2024'",
        ),
    },
    {
        "file": "motilli_celery_concept4_varC.png",
        "scene": C4_SCENE,
        "layout": C4_LAYOUT.format(
            HEADLINE="'WHAT OZEMPIC® SLOWS, APIGENIN WAKES BACK UP'",
            HL_YELLOW="APIGENIN",
            CAPTION="'The breakthrough celery juice compound changing how GLP-1 bloating is treated in 2026.'",
            CREDIT="'Consumer trial · 412 GLP-1 users · 2024'",
        ),
    },
    # Concept 5
    {
        "file": "motilli_celery_concept5_varA.png",
        "scene": C5_SCENE,
        "layout": C5_LAYOUT.format(
            HEADLINE="'Why this one compound in celery juice is changing GLP-1 bloating in 2026.'",
        ),
    },
    {
        "file": "motilli_celery_concept5_varB.png",
        "scene": C5_SCENE,
        "layout": C5_LAYOUT.format(
            HEADLINE="'Why women on Ozempic® are throwing out their Miralax for this.'",
        ),
    },
    {
        "file": "motilli_celery_concept5_varC.png",
        "scene": C5_SCENE,
        "layout": C5_LAYOUT.format(
            HEADLINE="'The compound hidden in every celery stalk that your GI never told you about.'",
        ),
    },
]

PREAMBLE = (
    "Direct-response Facebook ad creative, 4:5 portrait, 1080x1350 feel. "
    "Render all specified text exactly as written, legibly, correctly spelled, with the specified typography, "
    "colors, and placement. Do NOT add, omit, or paraphrase any words. Do NOT invent logos. "
    "The ® symbol must be rendered correctly on Ozempic®, Wegovy®, Mounjaro®, Zepbound®."
)

def generate_one(ad):
    name = ad["file"]
    out_path = OUT / name
    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"[skip] {name} already exists")
        return name, "skipped"
    prompt = f"{PREAMBLE}\n\nSCENE:\n{ad['scene']}\n\nTEXT OVERLAY:\n{ad['layout']}"
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=ASPECT),
            ),
        )
        data = None
        for part in resp.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                data = part.inline_data.data
                break
        if not data:
            raise RuntimeError("no image data in response")
        out_path.write_bytes(data)
        print(f"[ok]   {name} ({len(data)//1024} KB)")
        return name, "ok"
    except Exception as e:
        print(f"[err]  {name}: {e}")
        traceback.print_exc()
        return name, f"err: {e}"

def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    targets = [a for a in ADS if not only or a["file"] in only]
    print(f"Generating {len(targets)} ads via {MODEL} at aspect {ASPECT}")
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(generate_one, ad): ad["file"] for ad in targets}
        for fut in concurrent.futures.as_completed(futures):
            name, status = fut.result()
            results[name] = status
    print("\n=== SUMMARY ===")
    for n, s in sorted(results.items()):
        print(f"{s:10s} {n}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Batch generate all 36 Motilli static ads with copy baked in — V3.
Uses the IMAGE GENERATION PROMPTS from the copy deck as composition guidance.
No Grüns/Ozempic references in any prompt.
3 Angles × 4 Templates × 3 Variations = 36 images
"""

import subprocess
import os
import sys
import time

REPLICATOR = os.path.expanduser("~/.claude/skills/ad-replicator/ad_replicator.py")
BASE_DIR = "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/statics"
REFS_DIR = os.path.join(BASE_DIR, "gruns-refs")

REFS = {
    "A": os.path.join(REFS_DIR, "template_a_ozempic_bestie.png"),
    "B": os.path.join(REFS_DIR, "template_b_adderall_mushrooms.png"),
    "C": os.path.join(REFS_DIR, "template_c_poop_more.png"),
    "D": os.path.join(REFS_DIR, "template_d_glp1.png"),
}

# =====================================================================
# COMPOSITION TEMPLATES — from the deck's IMAGE GENERATION PROMPTS
# These describe Motilli-native compositions, NOT Grüns copies.
# =====================================================================

COMP_A = """COMPOSITION & STYLE:
Product advertisement, square format (1080x1080), warm cream/ivory background (#FFF8E7).
Center composition: one large translucent dark green gummy bear (photorealistic, glossy, 3D rendered, celery-green color with subtle speckling) positioned slightly left of center. Behind and to the right of the gummy bear, the Motilli product JAR — a clear/translucent supplement jar with white screw cap, green label reading "motilli" in lowercase white text at top, "CELERY JUICE FIBER GUMMIES" below, filled with dark green gummies visible through the clear jar. The jar is tilted at a slight angle. Both elements cast soft natural shadows.
Top third of frame has the headline text. Below the headline is the subhead. Bottom 15% has the bottom line text.
Lighting: soft, warm, diffused — like morning light through a kitchen window. No harsh shadows. The gummy bear should look appetizing and tactile.
Style: clean commercial product photography, premium supplement brand aesthetic, minimal props, aspirational wellness.
Color palette: Fresh celery green (#6B8E23 / #7CB342), warm cream/ivory background (#FFF8E7), gold/amber accent (#DAA520).
Typography: Bold serif for headline (dark green #1B5E20), clean sans-serif for subhead and bottom line.
IMPORTANT: This is a MOTILLI brand ad. The Motilli product is a CLEAR JAR with white cap and green label — NOT a bag, pouch, or sachet. Match the product reference image EXACTLY. Do NOT include any other brand's name, logo, or visual identity. Do NOT reference Ozempic, GLP-1, or weight loss drugs anywhere."""

COMP_B = """COMPOSITION & STYLE:
Product advertisement, square format (1080x1080), gradient background transitioning from soft sage green at top to warm cream at bottom, with subtle sparkle/star decorative elements scattered lightly.
Center composition: the Motilli product JAR — a clear/translucent supplement jar with white screw cap, green label reading "motilli" in lowercase white text at top, "CELERY JUICE FIBER GUMMIES" below, dark green gummies visible through the clear jar, "5g FIBER" badge on label, "GREEN APPLE" flavor text at bottom of label. The jar is photographed straight-on, slightly angled, with a few loose dark green gummy bears scattered at the base.
Top 25% of frame has the bold headline text. Bottom right corner has a circular credibility badge. Very bottom has small disclaimer text.
Lighting: even, studio-style with gentle gradient lighting. Clean and bright. The packaging should look premium and photographic.
Style: playful, colorful, confident. Premium supplement with personality. Not clinical.
Typography: Heavy bold sans-serif for headline (white or dark green), smaller sans for badge and disclaimer.
IMPORTANT: This is a MOTILLI brand ad. The Motilli product is a CLEAR JAR with white cap and green label — NOT a bag, pouch, or sachet. Match the product reference image EXACTLY. Do NOT include any other brand's name, logo, or visual identity. Do NOT reference Ozempic, GLP-1, or weight loss drugs anywhere."""

COMP_C = """COMPOSITION & STYLE:
Product advertisement, square format (1080x1080), clean white/very light sage background.
Center composition: the Motilli product JAR — a clear/translucent supplement jar with white screw cap, green label reading "motilli" in lowercase white text, "CELERY JUICE FIBER GUMMIES" below, dark green gummies visible through the clear jar — positioned dead center of the frame. Two or three loose dark green gummy bears scattered casually near the jar. The product is the focal point but sized to leave generous space on all sides.
Left and right sides: benefit text callouts with small icons flanking the product on both sides, roughly 3 callouts per side.
Top 20% has a bold headline. Bottom 10% has a social proof bar (star rating + "Reviews").
Lighting: bright, flat, clean — almost editorial. Minimal shadows. The look is informational but still premium.
Style: bold, direct, clean layout with product center stage and benefits radiating outward. Playful but credible.
Typography: Bold playful font for headline (dark green or black), clean sans for callouts, gold stars for review bar.
IMPORTANT: This is a MOTILLI brand ad. The Motilli product is a CLEAR JAR with white cap and green label — NOT a bag, pouch, or sachet. Match the product reference image EXACTLY. Do NOT include any other brand's name, logo, or visual identity. Do NOT reference Ozempic, GLP-1, or weight loss drugs anywhere."""

COMP_D = """COMPOSITION & STYLE:
Product advertisement, square format (1080x1080), soft gradient background from light sage/mint green at top to pale cream at bottom.
Right side: the Motilli product JAR — a clear/translucent supplement jar with white screw cap, green label reading "motilli" in lowercase white text, "CELERY JUICE FIBER GUMMIES" below, dark green gummies visible through the clear jar — positioned in the right 40% of the frame, taking up roughly 60% of the vertical height. The jar is the visual anchor.
Left side (roughly 55-60%): headline text at top, then a vertical stack of 6 benefit bullet bars (green rounded rectangle bars with white text and small icons) running down the left side next to the jar.
Bottom 10% has a social proof bar (star rating + "Reviews") spanning the full width.
Lighting: soft, diffused, premium. The jar should look appetizing with the dark green gummies visible inside.
Style: informational but visually striking. The jar is the hero element while the bullet structure provides scanning value. Premium supplement feel.
Typography: Bold sans-serif for headline (dark green #1B5E20), white text on green (#4CAF50) rounded rectangle bullet bars, gold stars for review bar.
IMPORTANT: This is a MOTILLI brand ad. The Motilli product is a CLEAR JAR with white cap and green label — NOT a bag, pouch, or sachet. Match the product reference image EXACTLY. Do NOT include any other brand's name, logo, or visual identity. Do NOT reference Ozempic, GLP-1, or weight loss drugs anywhere."""

COMPS = {"A": COMP_A, "B": COMP_B, "C": COMP_C, "D": COMP_D}

# =====================================================================
# ALL 36 COPY SETS
# (angle_key, template_key, variation_num, copy_text)
# copy_text contains ONLY the text elements — composition comes from COMPS
# =====================================================================

COPY_SETS = [
    # ============================================================
    # ANGLE 1: CONVENIENCE
    # ============================================================

    # Template A — Provocative Headline Hero
    ("convenience", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Your Juicer's
Replacement

SUBHEAD (below headline, smaller serif or sans, dark green):
Same celery benefits.
Zero cleanup.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → No mess. No stress. Just results."""),

    ("convenience", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Your Morning
Back

SUBHEAD (below headline, smaller serif or sans, dark green):
Celery juice benefits
without the 20-minute ritual.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Ditch the juicer. Keep the glow. ✨"""),

    ("convenience", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
The $200 Juicer
Killer

SUBHEAD (below headline, smaller serif or sans, dark green):
Every benefit of celery juice.
None of the hassle.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Same results. Way less cleanup. 🙌"""),

    # Template B — Provocative Comparison
    ("convenience", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
JUICER?
NAH, GUMMIES.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + celery juice in every serving

DISCLAIMER (very bottom, small text):
*This is not a replacement for whole vegetables. But it is a replacement for scrubbing green pulp off your countertop at 6am."""),

    ("convenience", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
20 MINUTES OF PREP?
NAH, 10 SECONDS.

BADGE (bottom right, circular credibility badge):
Celery juice benefits — no juicer required

DISCLAIMER (very bottom, small text):
*Your morning routine called. It wants those 20 minutes back."""),

    ("convenience", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
WILTING CELERY?
NAH, SHELF-STABLE GUMMIES.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + celery juice nutrients in every serving

DISCLAIMER (very bottom, small text):
*No more $5 bunches of celery that go bad before Wednesday."""),

    # Template C — Short Bold Headline + Benefit Callouts
    ("convenience", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Ditch the juicer 🥤

LEFT CALLOUTS (left side of product, with small icons):
• Prebiotics
• Celery Juice Nutrients
• Less Bloating

RIGHT CALLOUTS (right side of product, with small icons):
• 6g Fiber
• Clean Ingredients
• No Prep

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("convenience", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Skip the mess 🧹

LEFT CALLOUTS (left side of product, with small icons):
• Prebiotic Fiber
• Better Digestion
• Clearer Skin

RIGHT CALLOUTS (right side of product, with small icons):
• No Juicer Needed
• Tastes Amazing
• 10 Seconds

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("convenience", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Same glow. No grind. ✨

LEFT CALLOUTS (left side of product, with small icons):
• Celery Juice Benefits
• Gut Support
• More Energy

RIGHT CALLOUTS (right side of product, with small icons):
• Zero Cleanup
• Shelf Stable
• Just 2 Gummies

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    # Template D — Audience-Qualified Headline + Stacked Bullets
    ("convenience", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
Celery Juice Benefits
Without The Juicer

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Prebiotic Fiber for Gut Health
• Celery Juice Nutrients in Every Serving
• No Washing, Chopping, or Cleanup
• Tastes Better Than Celery Juice
• Shelf Stable — No Wilting, No Waste
• Ready in 10 Seconds

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    ("convenience", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
Still Scrubbing
Your Juicer?

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• All the Celery Juice Goodness
• Packed with Prebiotic Fiber
• No $5 Celery Bunches
• No 20-Minute Morning Routine
• Take Anywhere — Just 2 Gummies
• 0 Mess

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    ("convenience", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
She Ditched the Juicer.
Kept the Results.

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Same Celery Juice Benefits
• More Fiber Than Fresh Juice
• Zero Prep, Zero Cleanup
• Delicious Daily Gummies
• Clean, Vegan Ingredients
• Shelf Stable for Months

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    # ============================================================
    # ANGLE 2: FIBER PARADOX
    # ============================================================

    # Template A
    ("fiber", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Your Juicer's
Dirty Secret

SUBHEAD (below headline, smaller serif or sans, dark green):
It removes 95% of celery's fiber.
We put it back.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → More fiber. Better gut. No juicer required."""),

    ("fiber", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Juicing
Removes The
Best Part

SUBHEAD (below headline, smaller serif or sans, dark green):
95% of celery's fiber goes in the trash.
Not anymore.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → The fiber your juice was missing. 🌿"""),

    ("fiber", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Better Than
Your Juice

SUBHEAD (below headline, smaller serif or sans, dark green):
Celery juice without the fiber
is celery water.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Fiber + nutrients. The way celery was meant to work."""),

    # Template B
    ("fiber", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
CELERY JUICE?
YOU'RE THROWING AWAY THE BEST PART.

BADGE (bottom right, circular credibility badge):
6g prebiotic fiber per serving

DISCLAIMER (very bottom, small text):
*95% of celery's fiber gets discarded during juicing. We kept it."""),

    ("fiber", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
YOUR JUICER REMOVES FIBER.
WE DON'T.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + full celery nutrition

DISCLAIMER (very bottom, small text):
*Juicing strips the gut-health fiber your body actually needs. These gummies deliver it."""),

    ("fiber", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
JUICE THE CELERY.
TRASH THE FIBER.
WONDER WHY YOUR GUT HURTS.

BADGE (bottom right, circular credibility badge):
6g fiber — more than your morning juice

DISCLAIMER (very bottom, small text):
*Or just eat the gummy."""),

    # Template C
    ("fiber", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Your juice is missing this 👇

LEFT CALLOUTS (left side of product, with small icons):
• 6g Prebiotic Fiber
• Full Celery Nutrition
• Better Digestion

RIGHT CALLOUTS (right side of product, with small icons):
• Gut Health
• Less Bloating
• No Waste

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("fiber", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Fiber > juice 🌿

LEFT CALLOUTS (left side of product, with small icons):
• Prebiotic Fiber
• Gut Support
• Celery Nutrients

RIGHT CALLOUTS (right side of product, with small icons):
• What Juicing Strips Out
• Clearer Skin
• More Regular

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("fiber", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
The part your juicer trashes 🗑️

LEFT CALLOUTS (left side of product, with small icons):
• 95% of Fiber Lost in Juicing
• We Kept It All
• Prebiotics

RIGHT CALLOUTS (right side of product, with small icons):
• 6g Fiber
• Gut Health
• Clean Ingredients

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    # Template D
    ("fiber", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
More Fiber Than
Your Morning Juice

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• 6g Prebiotic Fiber Per Serving
• Juicing Removes 95% of Celery's Fiber
• Supports Gut Health & Regularity
• Full Celery Juice Nutrients
• Reduces Bloating
• No Juicer Required

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    ("fiber", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
What Your Juicer
Throws Away

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• The Prebiotic Fiber Your Gut Needs
• 6g Per Serving — More Than Juice
• Supports Digestion & Regularity
• Celery Juice Nutrients Preserved
• Clean, Vegan Ingredients
• Better Than Juice. Seriously.

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    ("fiber", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
Celery Juice
Minus The Flaw

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Juicing Strips Fiber — We Restore It
• 6g Prebiotic Fiber Every Serving
• Full Spectrum Celery Nutrition
• Better Gut Support Than Juice Alone
• Tastes Better Too
• 0 Sugar

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    # ============================================================
    # ANGLE 3: PERMISSION
    # ============================================================

    # Template A
    ("permission", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
You Didn't
Quit Juicing.
You Upgraded.

SUBHEAD (below headline, smaller serif or sans, dark green):
Same commitment.
Smarter delivery.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Consistency without the punishment."""),

    ("permission", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Still Committed.
Done Suffering.

SUBHEAD (below headline, smaller serif or sans, dark green):
You believe in celery juice.
You just hated the process.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Same you. Easier routine. Better results."""),

    ("permission", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top third, large bold serif, dark green #1B5E20):
Consistency
Shouldn't Hurt

SUBHEAD (below headline, smaller serif or sans, dark green):
Celery juice benefits you love.
Without the ritual you dread.

BOTTOM LINE (bottom of image, clean sans-serif):
2 gummies a day → Your gut doesn't care how the fiber gets there."""),

    # Template B
    ("permission", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
QUITTING JUICING ISN'T GIVING UP.
IT'S GROWING UP.

BADGE (bottom right, circular credibility badge):
Same celery benefits — smarter format

DISCLAIMER (very bottom, small text):
*You didn't fail at juicing. The process failed you. We fixed the process."""),

    ("permission", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
DISCIPLINE ISN'T
SCRUBBING A JUICER AT 6AM.

BADGE (bottom right, circular credibility badge):
Daily celery nutrition — no ritual required

DISCLAIMER (very bottom, small text):
*Being consistent with your health doesn't mean being miserable about it."""),

    ("permission", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 25%, heavy bold sans-serif, white or dark green):
YOUR HEALTH COMMITMENT
DESERVES A BETTER FORMAT.

BADGE (bottom right, circular credibility badge):
Celery juice benefits in a daily gummy

DISCLAIMER (very bottom, small text):
*You already did the hard part: deciding celery juice works. Let us handle the rest."""),

    # Template C
    ("permission", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Permission to stop juicing 🙌

LEFT CALLOUTS (left side of product, with small icons):
• Prebiotic Fiber
• Celery Nutrients
• Better Digestion

RIGHT CALLOUTS (right side of product, with small icons):
• No Guilt
• Stay Consistent
• Tastes Good

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("permission", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
You're not lazy. Juicing is broken. 💚

LEFT CALLOUTS (left side of product, with small icons):
• Same Benefits
• Daily Consistency
• Less Bloating

RIGHT CALLOUTS (right side of product, with small icons):
• Zero Dread
• Clean Ingredients
• 10 Seconds

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    ("permission", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top 20%, bold playful font, dark green):
Upgrade, don't quit ⬆️

LEFT CALLOUTS (left side of product, with small icons):
• Celery Juice Benefits
• Prebiotic Fiber
• Gut Support

RIGHT CALLOUTS (right side of product, with small icons):
• No Compromise
• Better Consistency
• Every Day

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews"""),

    # Template D
    ("permission", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
For Women Who
Love Celery Juice
But Hate Juicing

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Every Celery Juice Benefit
• Plus the Fiber Juicing Strips Out
• No Morning Prep Dread
• No Wilting Celery in Your Fridge
• No Guilt When You Miss a Day
• Just Daily Consistency, Simplified

SOCIAL PROOF BAR (bottom, full width):
55,000+ ⭐⭐⭐⭐⭐ reviews"""),

    ("permission", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
Stopped Juicing?
You're Not Lazy.
The Process Was.

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Celery Juice Benefits — Easier Format
• 6g Prebiotic Fiber Per Serving
• No $150/Month Celery Habit
• No Juicer Cleanup Ever Again
• Travel Without Skipping Days
• Consistency You Can Actually Keep

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),

    ("permission", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green #1B5E20):
Your Commitment
Was Never The
Problem

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Full Celery Juice Nutrition
• Prebiotic Fiber Your Gut Needs
• Designed for the Woman Who Believes
• But Was Drowning in Prep
• 2 Gummies — Grab and Go
• Consistency Without Sacrifice

SOCIAL PROOF BAR (bottom, full width):
⭐⭐⭐⭐⭐ Reviews"""),
]


def run_batch():
    output_base = os.path.join(BASE_DIR, "gruns-adapted-v6")
    total = len(COPY_SETS)
    print(f"[BATCH V6] Starting generation of {total} statics")
    print(f"[BATCH V6] Output: {output_base}/")
    print()

    success = 0
    failed = 0
    skipped = 0

    for i, (angle, template, var_num, copy_text) in enumerate(COPY_SETS):
        final_name = f"{angle}_{template.lower()}{var_num}.png"
        final_dir = os.path.join(output_base, f"angle_{angle}")
        final_path = os.path.join(final_dir, final_name)

        # Skip if already generated
        if os.path.exists(final_path):
            print(f"[{i+1}/{total}] SKIP (exists): {final_name}")
            skipped += 1
            continue

        print(f"[{i+1}/{total}] Generating: {final_name} (Angle: {angle}, Template: {template}, Var: {var_num})")

        ref_path = REFS[template]
        comp = COMPS[template]

        # Combine composition guide + copy text into adaptation notes
        adaptation_notes = f"""{copy_text}

{comp}

CRITICAL INSTRUCTIONS:
- Render ALL text listed above clearly and legibly on the image in the specified positions.
- Use the reference image ONLY for layout/composition structure — do NOT copy its text, branding, product name, or visual identity.
- This is a MOTILLI CELERY JUICE FIBER GUMMIES ad. The product is a CLEAR SUPPLEMENT JAR with white screw cap, green label, dark green gummies visible inside. NOT a bag, NOT a pouch, NOT a sachet. It is a JAR — match the product reference image exactly.
- Do NOT include any text from the reference image. Only render the EXACT TEXT specified above.
- Do NOT mention Ozempic, GLP-1, weight loss, or any pharmaceutical drug.
- Do NOT include any brand name other than Motilli."""

        # Temp output dir for this generation
        temp_output = os.path.join(output_base, f"_temp_{angle}_{template.lower()}{var_num}")
        output_file = os.path.join(temp_output, "generated", "ref_001_adapted_v001.png")

        cmd = [
            sys.executable, REPLICATOR,
            "--reference", ref_path,
            "--brand", "motilli",
            "--variations", "1",
            "--adaptation-notes", adaptation_notes,
            "--output-dir", temp_output,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0 and os.path.exists(output_file):
                os.makedirs(final_dir, exist_ok=True)
                os.rename(output_file, final_path)
                print(f"  ✓ Saved: {final_name}")
                success += 1
                # Cleanup temp dir
                import shutil
                shutil.rmtree(temp_output, ignore_errors=True)
            else:
                print(f"  ✗ FAILED: {result.stderr[-300:] if result.stderr else 'No output file'}")
                failed += 1
        except subprocess.TimeoutExpired:
            print(f"  ✗ TIMEOUT")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1

        time.sleep(1)

    print()
    print(f"[BATCH V6] Complete: {success} generated, {skipped} skipped, {failed} failed")
    print(f"[BATCH V6] Output: {output_base}/")


if __name__ == "__main__":
    run_batch()

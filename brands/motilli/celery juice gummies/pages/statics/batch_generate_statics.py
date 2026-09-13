#!/usr/bin/env python3
"""
Batch generate all 36 Motilli static ads with copy baked in.
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

# All 36 copy sets organized as:
# (angle_key, template_key, variation_num, adaptation_notes)

COPY_SETS = [
    # ============================================================
    # ANGLE 1: CONVENIENCE
    # ============================================================

    # Template A — Provocative Headline Hero
    ("convenience", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Your Juicer's
Replacement

SUBHEAD (below headline, smaller, dark green):
Same celery benefits.
Zero cleanup.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → No mess. No stress. Just results.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Your Morning
Back

SUBHEAD (below headline, smaller, dark green):
Celery juice benefits
without the 20-minute ritual.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Ditch the juicer. Keep the glow. ✨

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
The $200 Juicer
Killer

SUBHEAD (below headline, smaller, dark green):
Every benefit of celery juice.
None of the hassle.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Same results. Way less cleanup.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    # Template B — Provocative Comparison
    ("convenience", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
JUICER?
NAH, GUMMIES.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + celery juice in every pack

DISCLAIMER (very bottom, small text):
*This is not a replacement for whole vegetables. But it is a replacement for scrubbing green pulp off your countertop at 6am.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag with bear mascot logo. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
20 MINUTES OF PREP?
NAH, 10 SECONDS.

BADGE (bottom right, circular credibility badge):
Celery juice benefits — no juicer required

DISCLAIMER (very bottom, small text):
*Your morning routine called. It wants those 20 minutes back.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag with bear mascot logo. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
WILTING CELERY?
NAH, SHELF-STABLE GUMMIES.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + celery juice nutrients in every pack

DISCLAIMER (very bottom, small text):
*No more $5 bunches of celery that go bad before Wednesday.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag with bear mascot logo. The text must be rendered clearly and legibly on the image."""),

    # Template C — Short Bold Headline + Benefit Callouts
    ("convenience", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. A few loose green gummy bears near the packet. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. A few loose green gummy bears near the packet. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
Same glow. No grind. ✨

LEFT CALLOUTS (left side of product, with small icons):
• Celery Juice Benefits
• Gut Support
• More Energy

RIGHT CALLOUTS (right side of product, with small icons):
• Zero Cleanup
• Shelf Stable
• Daily Pack

SOCIAL PROOF BAR (bottom):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. A few loose green gummy bears near the packet. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    # Template D — Audience-Qualified Headline + Stacked Bullets
    ("convenience", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
Celery Juice Benefits
Without The Juicer

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Prebiotic Fiber for Gut Health
• Celery Juice Nutrients in Every Pack
• No Washing, Chopping, or Cleanup
• Tastes Better Than Celery Juice
• Shelf Stable — No Wilting, No Waste
• Ready in 10 Seconds

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear in right 40% of frame, stacked green bullet bars down the left side, headline top, social proof bar bottom. Soft gradient sage/mint to cream background. Swap product to Motilli celery juice fiber gummy bear. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
Still Scrubbing
Your Juicer?

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• All the Celery Juice Goodness
• Packed with Prebiotic Fiber
• No $5 Celery Bunches
• No 20-Minute Morning Routine
• Travel-Friendly Daily Packs
• 0 Mess

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear in right 40% of frame, stacked green bullet bars down the left side, headline top, social proof bar bottom. Soft gradient sage/mint to cream background. Swap product to Motilli celery juice fiber gummy bear. The text must be rendered clearly and legibly on the image."""),

    ("convenience", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
She Ditched the Juicer.
Kept the Results.

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Same Celery Juice Benefits
• More Fiber Than Fresh Juice
• Zero Prep, Zero Cleanup
• Delicious Daily Gummies
• Clean, Vegan Ingredients
• Shelf Stable for Months

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear in right 40% of frame, stacked green bullet bars down the left side, headline top, social proof bar bottom. Soft gradient sage/mint to cream background. Swap product to Motilli celery juice fiber gummy bear. The text must be rendered clearly and legibly on the image."""),

    # ============================================================
    # ANGLE 2: FIBER PARADOX
    # ============================================================

    # Template A
    ("fiber", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Your Juicer's
Dirty Secret

SUBHEAD (below headline, smaller, dark green):
It removes 95% of celery's fiber.
We put it back.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → More fiber. Better gut. No juicer required.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Juicing
Removes The
Best Part

SUBHEAD (below headline, smaller, dark green):
95% of celery's fiber goes in the trash.
Not anymore.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → The fiber your juice was missing. 🌿

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Better Than
Your Juice

SUBHEAD (below headline, smaller, dark green):
Celery juice without the fiber
is celery water.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Fiber + nutrients. The way celery was meant to work.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    # Template B
    ("fiber", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
CELERY JUICE?
YOU'RE THROWING AWAY THE BEST PART.

BADGE (bottom right, circular credibility badge):
6g prebiotic fiber per serving

DISCLAIMER (very bottom, small text):
*95% of celery's fiber gets discarded during juicing. We kept it.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
YOUR JUICER REMOVES FIBER.
WE DON'T.

BADGE (bottom right, circular credibility badge):
Prebiotic fiber + full celery nutrition

DISCLAIMER (very bottom, small text):
*Juicing strips the gut-health fiber your body actually needs. These gummies deliver it.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
JUICE THE CELERY.
TRASH THE FIBER.
WONDER WHY YOUR GUT HURTS.

BADGE (bottom right, circular credibility badge):
6g fiber — more than your morning juice

DISCLAIMER (very bottom, small text):
*Or just eat the gummy.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    # Template C
    ("fiber", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    # Template D
    ("fiber", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
More Fiber Than
Your Morning Juice

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• 6g Prebiotic Fiber Per Serving
• Juicing Removes 95% of Celery's Fiber
• Supports Gut Health & Regularity
• Full Celery Juice Nutrients
• Reduces Bloating
• No Juicer Required

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
What Your Juicer
Throws Away

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• The Prebiotic Fiber Your Gut Needs
• 6g Per Serving — More Than Juice
• Supports Digestion & Regularity
• Celery Juice Nutrients Preserved
• Clean, Vegan Ingredients
• Better Than Juice. Seriously.

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),

    ("fiber", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
Celery Juice
Minus The Flaw

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Juicing Strips Fiber — We Restore It
• 6g Prebiotic Fiber Every Serving
• Full Spectrum Celery Nutrition
• Better Gut Support Than Juice Alone
• Tastes Better Too
• 0 Sugar

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),

    # ============================================================
    # ANGLE 3: PERMISSION
    # ============================================================

    # Template A
    ("permission", "A", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
You Didn't
Quit Juicing.
You Upgraded.

SUBHEAD (below headline, smaller, dark green):
Same commitment.
Smarter delivery.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Consistency without the punishment.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("permission", "A", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Still Committed.
Done Suffering.

SUBHEAD (below headline, smaller, dark green):
You believe in celery juice.
You just hated the process.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Same you. Easier routine. Better results.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    ("permission", "A", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, large bold serif, dark green):
Consistency
Shouldn't Hurt

SUBHEAD (below headline, smaller, dark green):
Celery juice benefits you love.
Without the ritual you dread.

BOTTOM LINE (bottom of image, clean sans-serif):
1 pack a day → Your gut doesn't care how the fiber gets there.

COMPOSITION: Keep the exact Grüns 'Ozempic's New Bestie' layout — large gummy bear left of center, Motilli single-serve pack behind it at angle, warm cream/ivory background. Swap product to Motilli celery juice gummies. The text must be rendered clearly and legibly on the image."""),

    # Template B
    ("permission", "B", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
QUITTING JUICING ISN'T GIVING UP.
IT'S GROWING UP.

BADGE (bottom right, circular credibility badge):
Same celery benefits — smarter format

DISCLAIMER (very bottom, small text):
*You didn't fail at juicing. The process failed you. We fixed the process.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    ("permission", "B", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
DISCIPLINE ISN'T
SCRUBBING A JUICER AT 6AM.

BADGE (bottom right, circular credibility badge):
Daily celery nutrition — no ritual required

DISCLAIMER (very bottom, small text):
*Being consistent with your health doesn't mean being miserable about it.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    ("permission", "B", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, heavy bold sans-serif, white or dark green):
YOUR HEALTH COMMITMENT
DESERVES A BETTER FORMAT.

BADGE (bottom right, circular credibility badge):
Celery juice benefits in a daily gummy

DISCLAIMER (very bottom, small text):
*You already did the hard part: deciding celery juice works. Let us handle the rest.

COMPOSITION: Keep the exact Grüns 'Adderall? Nah, Mushrooms' layout — bold headline top, Motilli product bag hero center, gradient sage-to-cream background with sparkle/star elements, credibility badge bottom right. Swap product to Motilli celery juice gummies bag. The text must be rendered clearly and legibly on the image."""),

    # Template C
    ("permission", "C", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    ("permission", "C", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    ("permission", "C", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold playful font, dark green):
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
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop more' layout — clean white/light background, Motilli single-serve packet dead center, benefit callouts radiating on left and right with small icons, headline top, review bar bottom. Swap product to Motilli. The text must be rendered clearly and legibly on the image."""),

    # Template D
    ("permission", "D", 1, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
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

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),

    ("permission", "D", 2, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
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

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),

    ("permission", "D", 3, """EXACT TEXT TO RENDER ON THE IMAGE:

HEADLINE (top, bold sans-serif, dark green):
Your Commitment
Was Never The
Problem

STACKED BULLETS (left side, green rounded rectangle bars with white text and small icons):
• Full Celery Juice Nutrition
• Prebiotic Fiber Your Gut Needs
• Designed for the Woman Who Believes
• But Was Drowning in Prep
• Daily Packs — Grab and Go
• Consistency Without Sacrifice

SOCIAL PROOF BAR (bottom, gold/yellow):
⭐⭐⭐⭐⭐ Reviews

COMPOSITION: Keep the exact Grüns 'Poop More While On a GLP-1' layout — large photorealistic Motilli gummy bear right side, stacked green bullet bars left side, headline top, review bar bottom. Soft gradient background. The text must be rendered clearly and legibly on the image."""),
]


def run_batch():
    total = len(COPY_SETS)
    print(f"[BATCH] Starting generation of {total} statics")
    print(f"[BATCH] Output: {BASE_DIR}/gruns-adapted-v2/")
    print()

    success = 0
    failed = 0
    skipped = 0

    for i, (angle, template, var_num, notes) in enumerate(COPY_SETS):
        output_dir = os.path.join(BASE_DIR, "gruns-adapted-v2", f"angle_{angle}", f"template_{template.lower()}")
        output_file = os.path.join(output_dir, "generated", f"ref_001_adapted_v001.png")
        final_name = f"{angle}_{template.lower()}{var_num}.png"
        final_path = os.path.join(BASE_DIR, "gruns-adapted-v2", f"angle_{angle}", final_name)

        # Skip if already generated
        if os.path.exists(final_path):
            print(f"[{i+1}/{total}] SKIP (exists): {final_name}")
            skipped += 1
            continue

        print(f"[{i+1}/{total}] Generating: {final_name} (Angle: {angle}, Template: {template}, Var: {var_num})")

        ref_path = REFS[template]

        cmd = [
            sys.executable, REPLICATOR,
            "--reference", ref_path,
            "--brand", "motilli",
            "--variations", "1",
            "--adaptation-notes", notes,
            "--output-dir", output_dir,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0 and os.path.exists(output_file):
                # Rename to final name
                os.makedirs(os.path.dirname(final_path), exist_ok=True)
                os.rename(output_file, final_path)
                print(f"  ✓ Saved: {final_name}")
                success += 1
            else:
                print(f"  ✗ FAILED: {result.stderr[-200:] if result.stderr else 'No output file'}")
                failed += 1
        except subprocess.TimeoutExpired:
            print(f"  ✗ TIMEOUT")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1

        # Small delay between generations
        time.sleep(1)

    print()
    print(f"[BATCH] Complete: {success} generated, {skipped} skipped, {failed} failed")
    print(f"[BATCH] Output: {BASE_DIR}/gruns-adapted-v2/")


if __name__ == "__main__":
    run_batch()

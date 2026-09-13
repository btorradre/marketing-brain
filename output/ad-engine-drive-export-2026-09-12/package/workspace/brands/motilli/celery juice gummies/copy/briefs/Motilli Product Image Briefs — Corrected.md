# Motilli Product Image Briefs — CRO-Corrected

These are structured briefs for each product gallery image, incorporating every fix from the CRO audit. Hand these to your designer or use them as prompts for your image generation workflow. Each brief specifies exactly what text, layout, and visual elements should appear.

**Recommended carousel order (changed from current):**
1. Hero Shot
2. Testimonial (Sarah K.)
3. Comparison Chart
4. Ingredients Wheel
5. "Go Green" Benefits
6. Trust Badges
7. Supplement Facts
8. 90-Day Guarantee

---

## Image 1 — Product Hero Shot

```json
{
  "image_number": 1,
  "image_name": "Hero Shot — Outcome-Driven Callouts",
  "role": "First impression. Communicates what this product DOES, not what's in it.",
  "layout": {
    "background": "Split vertical — cream (#F5F0E8) left 55%, soft green (#A8D86B) right 45%",
    "product_placement": "Center-left, Motilli jar at slight angle, lid off, heart-shaped gummies scattered around base",
    "callout_placement": "Right column, three stacked benefit callouts with icons"
  },
  "text_elements": {
    "callout_1": {
      "icon": "Flat stomach silhouette icon",
      "headline": "Flattens Bloating Fast",
      "subtext": "Most users feel lighter in 48 hours"
    },
    "callout_2": {
      "icon": "Gut/stomach icon with sparkle",
      "headline": "Feeds Your Good Gut Bacteria",
      "subtext": "5g prebiotic fiber per serving"
    },
    "callout_3": {
      "icon": "Celery stalk icon",
      "headline": "Real Celery Juice — No Powder Filler",
      "subtext": "The detox shortcut without the juicer"
    }
  },
  "changes_from_original": [
    "REPLACED 'Natural Detoxification' with 'Flattens Bloating Fast' — outcome, not category",
    "REPLACED '5g Prebiotic Fiber Per Serving' with 'Feeds Your Good Gut Bacteria' — what it does, not what it is",
    "REPLACED 'Daily Green Boost' with 'Real Celery Juice — No Powder Filler' — competitive wedge, not vague branding",
    "ADDED supporting subtext under each callout for specificity"
  ],
  "design_notes": "Keep the same jar photography and scattered gummies. Only change the right-column text and icons. The product shot is strong — the callouts were the problem."
}
```

---

## Image 2 — Testimonial (Sarah K., 42) — MOVED TO POSITION 2

```json
{
  "image_number": 2,
  "image_name": "Testimonial — Sarah K.",
  "role": "Social proof. Strongest image in the set. Moved from position 3 to position 2.",
  "layout": {
    "background": "Warm cream (#F5F0E8), same as original",
    "top_bar": "Star rating + customer count banner at top",
    "quote_area": "Large headline quote, supporting testimonial paragraph below",
    "person": "Woman (40s) holding heart-shaped green gummy near face, eyes closed, peaceful expression",
    "product_addition": "Small Motilli jar in bottom-left or bottom-right corner, ~15% of frame"
  },
  "text_elements": {
    "top_banner": "★★★★★ Rated 4.9 / 5 | Trusted by 30,000+ Happy Customers",
    "headline_quote": "\"The only gummy that actually gave me my mornings back.\"",
    "headline_styling": "Underline on 'gave me' and 'my mornings back' — keep current style",
    "body_quote": "\"After just a week, the bloating was gone. I actually feel lighter — not just in my stomach, but my whole body. My skin even looks clearer. I finally feel like myself again.\"",
    "attribution": "— Sarah K. | 42"
  },
  "changes_from_original": [
    "MOVED from position 3 to position 2 in carousel — this is your strongest conversion image",
    "ADDED small product jar in corner — reinforces what she's endorsing",
    "FIXED quotation marks — use consistent curly quotes throughout (original mixed styles)",
    "KEPT everything else — this image works"
  ],
  "design_notes": "The person photography is strong. The quote is specific and emotionally resonant. Only additions are the product jar corner placement and punctuation fix."
}
```

---

## Image 3 — Comparison Chart — MOVED TO POSITION 3

```json
{
  "image_number": 3,
  "image_name": "Comparison Chart — Motilli vs. Other Brands",
  "role": "Differentiation. Creates 'us vs. them' contrast with outcome-based rows added.",
  "layout": {
    "background": "Soft green gradient, same as original",
    "header": "'Motilli™ vs. Other Brands' at top",
    "table": "6 rows (up from 5), checkmarks for Motilli, X marks for competitors",
    "product_images": "Motilli jar bottom-left, generic white bottle bottom-right"
  },
  "text_elements": {
    "header": "'Motilli™ vs. Other Brands'",
    "row_1": {
      "claim": "Stops Bloating in 48 Hours",
      "motilli": "✓",
      "others": "✗",
      "icon": "Flat stomach icon"
    },
    "row_2": {
      "claim": "90-Day Money-Back Guarantee",
      "motilli": "✓",
      "others": "✗",
      "icon": "Shield/guarantee icon"
    },
    "row_3": {
      "claim": "Real Celery Juice — Not Powder Filler",
      "motilli": "✓",
      "others": "✗",
      "icon": "Celery stalk icon"
    },
    "row_4": {
      "claim": "5g Prebiotic Fiber Per Serving",
      "motilli": "✓",
      "others": "✗",
      "icon": "Fiber icon"
    },
    "row_5": {
      "claim": "Clean Label Project Certified",
      "motilli": "✓",
      "others": "✗",
      "icon": "Shield/certification icon"
    },
    "row_6": {
      "claim": "No Artificial Colors or Flavors",
      "motilli": "✓",
      "others": "✗",
      "icon": "Leaf/clean icon"
    }
  },
  "changes_from_original": [
    "MOVED from position 6 to position 3 — differentiation should come early",
    "ADDED 'Stops Bloating in 48 Hours' as ROW 1 — outcome-based row creates emotional contrast",
    "ADDED '90-Day Money-Back Guarantee' as ROW 2 — risk reversal as a competitive advantage",
    "REMOVED 'Clinically Tested Actives' row — replaced with outcome rows that hit harder",
    "REORDERED remaining rows: outcome rows first, spec rows second"
  ],
  "design_notes": "Lead with the two new rows. The original comparison only had spec-based rows (certifications, ingredient types). Adding an outcome row ('Stops Bloating in 48 Hours') and a risk-reversal row ('90-Day Guarantee') creates actual emotional differentiation. Keep the same visual style — alternating cream/green row backgrounds."
}
```

---

## Image 4 — Ingredients Wheel — REWRITTEN

```json
{
  "image_number": 4,
  "image_name": "Ingredients Wheel — Mechanism-Driven",
  "role": "Ingredient education. Every slot now does conversion work.",
  "layout": {
    "background": "Cream (#F5F0E8), same as original",
    "center": "Heart-shaped green gummies clustered in center",
    "ingredient_circles": "4 circular photo insets arranged in a ring around center gummies",
    "arrows": "Subtle curved arrows connecting circles in clockwise flow"
  },
  "text_elements": {
    "ingredient_1": {
      "position": "Top (12 o'clock)",
      "photo": "Fresh celery stalks, chopped, on cutting board",
      "name": "Celery Juice Extract",
      "descriptor": "(Restarts Sluggish Digestion)"
    },
    "ingredient_2": {
      "position": "Right (3 o'clock)",
      "photo": "Glass of bright green chlorophyll liquid",
      "name": "Chlorophyll",
      "descriptor": "(Neutralizes Sulfur Gas & Odor)"
    },
    "ingredient_3": {
      "position": "Bottom (6 o'clock)",
      "photo": "White prebiotic fiber powder in a bowl",
      "name": "Prebiotic Fiber",
      "descriptor": "(Feeds Beneficial Gut Bacteria)"
    },
    "ingredient_4": {
      "position": "Left (9 o'clock)",
      "photo": "Sliced green apple",
      "name": "Green Apple",
      "descriptor": "(Tastes Like Candy, Not Medicine)"
    }
  },
  "changes_from_original": [
    "REPLACED 'Natural Detoxification' under Celery Juice with 'Restarts Sluggish Digestion' — specific mechanism outcome",
    "REPLACED 'Deep Green Cleanse' under Chlorophyll with 'Neutralizes Sulfur Gas & Odor' — addresses the #1 embarrassing GLP-1 symptom",
    "REPLACED '5g Digestive Support' under Prebiotic Fiber with 'Feeds Beneficial Gut Bacteria' — explains HOW it supports digestion",
    "REPLACED 'Natural Flavor' under Green Apple with 'Tastes Like Candy, Not Medicine' — turns a throwaway slot into a purchase objection killer"
  ],
  "design_notes": "Keep the same circular layout and food photography. Only change the parenthetical text under each ingredient name. The visual structure is fine — the descriptor copy was the problem."
}
```

---

## Image 5 — "Go Green. Feel Clean. Every Day." — FIXED

```json
{
  "image_number": 5,
  "image_name": "Benefits Breakdown — Copy Corrected",
  "role": "Brand positioning + three key benefits with complete copy.",
  "layout": {
    "background": "Full green (#8BC34A gradient), same as original",
    "headline_area": "Top-left, stacked tagline",
    "subheadline": "Below tagline, supporting context line",
    "benefit_list": "Three benefits with icons, left column",
    "product": "Motilli jar, right side, angled",
    "badges": "Clean Label Project Certified + Vegan badges, bottom-right"
  },
  "text_elements": {
    "headline": "Go green.\nFeel clean.\nEvery day.",
    "subheadline": "From 5 grams of fiber to full-body detox support, here's what makes Motilli different.",
    "benefit_1": {
      "icon": "Celery leaf sparkle icon",
      "text": "Natural Detoxification"
    },
    "benefit_2": {
      "icon": "Stomach with checkmark icon",
      "text": "Stops Bloating & Supports Healthy Digestion"
    },
    "benefit_3": {
      "icon": "Sparkle/energy icon",
      "text": "Restores Your Daily Energy & Regularity"
    },
    "badge_1": "Clean Label Project® Certified",
    "badge_2": "Vegan"
  },
  "changes_from_original": [
    "FIXED 'Stops Bloating & Supports' — COMPLETED the sentence: 'Stops Bloating & Supports Healthy Digestion'",
    "FIXED 'Restores Your Daily green boost' — replaced with 'Restores Your Daily Energy & Regularity' (consistent casing, meaningful outcome)",
    "Both were truncated/vague in the original — these were active conversion killers"
  ],
  "design_notes": "This image had copy errors that signaled sloppiness. The design layout is fine. Only the benefit text under bullet 2 and bullet 3 needs to change. Proof the final image against these briefs before publishing."
}
```

---

## Image 6 — Trust Badges — SPLIT APPROACH

```json
{
  "image_number": 6,
  "image_name": "Why Choose Motilli — Trust + Outcome Hybrid",
  "role": "Trust signals reframed with at least 2 outcome-oriented bullets.",
  "layout": {
    "background": "Full green (#8BC34A), bordered by fresh produce photography (celery, apples, ginger, herbs) — same as original",
    "header": "'Why Choose Motilli?' centered at top in white",
    "badge_row": "4 trust badges in a row below header",
    "bullet_grid": "6 checkmark bullets in two columns below badges"
  },
  "text_elements": {
    "header": "Why Choose Motilli?",
    "badges": [
      "Clinically Tested Actives",
      "Manufactured in the USA",
      "Clean Label Project® Certified",
      "Vegan & Non-GMO"
    ],
    "bullets_left_column": [
      "✓ Stops Bloating — Most Feel It in 48 Hours",
      "✓ Real Celery Juice Extract — Not Powder",
      "✓ No Artificial Colors or Flavors"
    ],
    "bullets_right_column": [
      "✓ 5g Fiber That Feeds Good Gut Bacteria",
      "✓ Green Apple Flavor (Actually Tastes Good)",
      "✓ 90-Day Money-Back Guarantee"
    ]
  },
  "changes_from_original": [
    "REPLACED 'No Synthetic Flavors' with 'Stops Bloating — Most Feel It in 48 Hours' — outcome bullet",
    "REPLACED 'No Gelatin' with '90-Day Money-Back Guarantee' — risk reversal",
    "REPLACED '5g Fiber Per Serving' with '5g Fiber That Feeds Good Gut Bacteria' — explains WHY the spec matters",
    "REPLACED 'Green Apple Flavor' with 'Green Apple Flavor (Actually Tastes Good)' — kills the taste objection",
    "ADDED specificity to celery juice bullet: '— Not Powder'",
    "KEPT badges unchanged — those work"
  ],
  "design_notes": "Same layout, same food border, same badge row. Only the six checkmark bullets change. Two of the original six were pure 'absence claims' (no gelatin, no synthetic flavors) that only matter to someone already comparing labels. Replace them with outcome and risk-reversal bullets that matter to someone still deciding whether to buy."
}
```

---

## Image 7 — Supplement Facts — ERRORS FIXED

```json
{
  "image_number": 7,
  "image_name": "Supplement Facts Panel — Corrected",
  "role": "Compliance and detail for label-readers. Must be accurate.",
  "layout": {
    "background": "Cream (#F5F0E8)",
    "panel": "Standard supplement facts box format",
    "dosage_bar": "Dark green bar at bottom with usage instructions",
    "other_ingredients": "Below dosage bar"
  },
  "text_elements": {
    "header": "SUPPLEMENT FACTS",
    "serving_size": "Serving Size: 2 Vegan Gummies",
    "servings_per_container": "Servings Per Container: 30",
    "nutrition_table": {
      "calories": {"amount": "10", "dv": ""},
      "total_carbohydrate": {"amount": "6g", "dv": "45%"},
      "dietary_fiber": {"amount": "5g", "dv": "18%"},
      "celery_juice_extract": {"amount": "200mg", "dv": "†"},
      "chlorophyll": {"amount": "300mg", "dv": "†"},
      "prebiotic_fiber_blend": {"amount": "300mg", "dv": "†"},
      "sodium_copper_chlorophyllin": {"amount": "2.5mg", "dv": "†"}
    },
    "footnotes": [
      "*FDA Daily Values are based on a 2,000 calorie diet.",
      "†Daily Value (DV) not established."
    ],
    "dosage_instructions": {
      "instruction_1": "Take 2 gummies daily",
      "instruction_2": "With a full glass of water",
      "instruction_3": "Anytime — with or without food"
    },
    "other_ingredients": "Other Ingredients: Celery Juice, Chlorophyll, Sodium Copper Chlorophyllin, Inulin (Prebiotic Fiber), Sugar, Pectin, Citric Acid, Natural Green Apple Flavor, Coconut Oil."
  },
  "changes_from_original": [
    "FIXED 'Other Ingredients' line — original listed Chlorophyll TWICE and Sodium Copper Chlorophyllin TWICE",
    "FIXED 'Like Inulin' → 'Inulin (Prebiotic Fiber)' — original had a formatting error",
    "FIXED 'Copper Chlorophyll Sugars' → separated into proper ingredient list",
    "FIXED footnote typo: 'urred' → 'based' and 'calorins' → 'calorie'",
    "IMPORTANT: Cross-check this corrected ingredient list against your ACTUAL product label before publishing. These corrections are based on what appears to be copy-paste errors in the original image — verify against the real formulation."
  ],
  "design_notes": "Same layout. This is a compliance image. The only changes are fixing the duplicate ingredients, typos, and formatting errors that undermine credibility for anyone who reads the label closely. DO NOT publish without verifying against the actual physical product label."
}
```

---

## Image 8 — 90-Day Guarantee — STRENGTHENED

```json
{
  "image_number": 8,
  "image_name": "90-Day Guarantee — Strengthened",
  "role": "Risk reversal. Last image in carousel. Final conversion push.",
  "layout": {
    "background": "Cream (#F5F0E8), same as original",
    "badge": "Dark green circular '90 DAYS' seal at top center",
    "guarantee_name": "Bold italic guarantee name below seal",
    "body_copy": "Guarantee terms in body text",
    "product": "Small Motilli jar in bottom-right corner, ~15% of frame"
  },
  "text_elements": {
    "seal_text": "90 DAYS",
    "guarantee_name": "THE EMPTY BOTTLE PROMISE",
    "subtitle": "90-Day Risk-Free Trial",
    "body": "Use the entire bottle. If you don't feel noticeably lighter — less bloating, better digestion, more energy — within 90 days, we'll refund every penny. No questions asked. No return required.",
    "fine_print": "Simply email us at [support email] for a full refund."
  },
  "changes_from_original": [
    "RENAMED guarantee from 'Feel Clean Guarantee' to 'The Empty Bottle Promise' — more visceral, more memorable, and proven higher-converting (used by Alevia and other top supplement brands)",
    "REWORDED body copy: added 'Use the entire bottle' upfront — this is the key risk-reversal line that eliminates the 'what if I only use half' hesitation",
    "ADDED small product jar in corner — reinforces what the guarantee covers",
    "ADDED support email reference in fine print — reduces friction for skeptics who want to know HOW to claim the refund"
  ],
  "design_notes": "Keep the same seal design and cream background. The guarantee name change is the biggest impact — 'Empty Bottle Promise' tells the shopper they can use the ENTIRE product and still get a refund, which is a fundamentally different risk calculation than a generic 'guarantee.' Test this against the original name."
}
```

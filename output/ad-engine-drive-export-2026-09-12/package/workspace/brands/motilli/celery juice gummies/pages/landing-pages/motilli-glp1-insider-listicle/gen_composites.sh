#!/bin/bash
# Two NoraLife-style composites: item1 hero-with-callout-bubbles, item7 check-vs-X collage (failed cabinet).
# Output to *-new.png for QA before swapping over the live names.
export PATH="$HOME/.local/bin:$PATH"
set -u
BRAND="/Users/brooksorradre2/Documents/marketing brain/brands/motilli"
OUT="$BRAND/landing-pages/motilli-glp1-insider-listicle/images"
REF="$BRAND/brand/website-assets/motilli product reference.png"

gen () {
  local name="$1"; local prompt="$2"
  local json; json="$(higgsfield generate create gpt_image_2 --prompt "$prompt" --aspect_ratio 1:1 --resolution 2k --quality high --image "$REF" --wait --wait-timeout 9m --json 2>/dev/null)"
  local url; url="$(printf '%s' "$json" | python3 -c "import sys,json
try:
 d=json.load(sys.stdin); j=d[0] if isinstance(d,list) else d; print(j.get('result_url',''))
except: print('')" 2>/dev/null)"
  if [ -n "$url" ]; then curl -sL "$url" -o "$OUT/$name.png"; echo "OK $name"; else echo "FAIL $name"; printf '%s\n' "$json" | tail -3; fi
}

# ITEM 1 — product hero with two circular ingredient callout bubbles + trust-badge row (NoraLife img #1)
gen item01-hero-new "A premium 1:1 square supplement hero composition on a soft cream-and-sage background with softly blurred green leaves. A single Motilli celery juice fiber gummies jar (clear jar, white cap, bright green label) stands prominently on the RIGHT side. On the LEFT are two stacked circular photo callout bubbles, each with a thin soft-green ring: the TOP circle shows fresh crisp green celery stalks, the BOTTOM circle shows a small clear glass bowl of deep-green chlorophyll liquid; a small neat curved caption sits beneath each circle reading 'Real Celery Juice' and 'Organic Chlorophyll'. Across the BOTTOM is a row of three simple thin-line trust-badge icons with short labels: 'NATURAL INGREDIENTS', 'CLEAN & PURE', 'THIRD-PARTY TESTED'. Two dark-green heart-shaped gummies rest in front of the jar. Bright clean commercial product photography, gentle soft shadows, cohesive fresh green palette, crisp legible lettering. Keep the exact Motilli jar shape, white cap, and bright green label from the reference image." &

# ITEM 7 — green-check vs red-X collage of the failed cabinet (NoraLife img #2 styling)
gen item07-stack-new "A 1:1 square comparison collage, clean modern direct-response style. LEFT HALF (full height, rounded): a single Motilli celery juice fiber gummies jar centered on a soft pale-green panel, a bright GREEN CIRCLE CHECKMARK badge in the TOP-LEFT corner, and three small round trust-seal stamps along the bottom reading 'ALL NATURAL', 'GMO FREE', and 'LAB TESTED'. RIGHT HALF split into two stacked photo tiles: the TOP tile shows a cluttered group of generic over-the-counter constipation remedies — a white osmotic laxative powder jug beside a tub of fiber powder — with a RED CIRCLE X badge in its top-left corner; the BOTTOM tile shows more failed remedies — a bottle of magnesium citrate, a box of stool softeners, and a white probiotic bottle — with a RED CIRCLE X badge in its top-left corner. Bright realistic product photography, cohesive clean look, crisp legible lettering. Keep the exact Motilli jar shape, white cap, and bright green label from the reference image. Only ordinary over-the-counter supplements and laxatives, no prescription drugs." &

wait
echo "=== COMPOSITES DONE ==="
ls -la "$OUT"/item01-hero-new.png "$OUT"/item07-stack-new.png 2>/dev/null

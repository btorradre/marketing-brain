#!/bin/bash
# Generate all 9 inline advertorial images via nano-banana (Gemini 3.1 Flash).
# Image specs derive from the 9 IMAGE markers in the Gut Health Blog advertorial copy.

set -e
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/pages/advertorials/gut-health-blog/images"
PROD_REF="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/updated/product img 1.webp"
LOGDIR="$OUT/.logs"
mkdir -p "$OUT" "$LOGDIR"

gen() {
  local slug="$1"; local aspect="$2"; local prompt="$3"; local ref="$4"
  local log="$LOGDIR/${slug}.log"
  local args=(--output "$slug" --dir "$OUT" --aspect "$aspect" --size 2K)
  if [ -n "$ref" ]; then
    args+=(--ref "$ref")
  fi
  echo "[$slug] starting..." | tee "$log"
  nano-banana "$prompt" "${args[@]}" >>"$log" 2>&1
  echo "[$slug] done" | tee -a "$log"
}

# IMAGE 1 - HERO: Dr. Marsh, board-certified gastroenterologist, editorial portrait
gen "01_hero" "3:2" \
"Editorial medical portrait. Dr. Rebecca Marsh: a 45-year-old board-certified female gastroenterologist with shoulder-length dark brown hair, warm intelligent eyes, light navy blouse and a soft cream cardigan, no stethoscope around her neck, sitting at a clean wood desk in a modern clinic exam room with a softly out-of-focus female patient (woman in her 50s) listening across the desk. Natural window light from the side, neutral confident expression, slight smile. Clean editorial color palette, no text overlays, no logos, no on-screen graphics." \
"" &

# IMAGE 2 - MIRALAX FAILURE TRIPTYCH
gen "02_miralax_failure" "16:9" \
"Three-panel editorial photo triptych of a woman in her early 50s on a GLP-1 medication, white kitchen background. Panel 1: close-up of her hand mixing Miralax powder into a Gatorade bottle on a kitchen counter. Panel 2: same woman seated on a sofa, both hands pressed against her visibly bloated lower abdomen, slight wince. Panel 3: same woman standing in her bathroom doorway looking defeated, soft morning light. Connected by faint red arrows between panels. Editorial direct-response lifestyle photography. No text overlays, no captions." \
"" &

# IMAGE 3 - HIGHWAY DIGESTIVE DIAGRAM
gen "03_highway_diagram" "16:9" \
"Clean editorial medical infographic comparing the human digestive system to a highway. Anatomically accurate cross-section: stomach labeled 'ON-RAMP', small intestine labeled 'MIDDLE STRETCH', colon labeled 'OFF-RAMP'. Show food piling up and fermenting in the stomach (the on-ramp) with small gas bubbles rising, while the colon (off-ramp) is shown empty. Subtle red distension arrows at the stomach. Soft beige/cream background, muted teal and green accents, editorial flat-illustration style with thin clean lines. Light, minimal labels only." \
"" &

# IMAGE 4 - THREE BOTANICAL SOURCES OVERHEAD
gen "04_three_botanicals" "16:9" \
"Overhead editorial flat-lay photo on a soft warm-white surface, three distinct ingredient groupings arranged in a clean horizontal row: LEFT — a bunch of fresh celery stalks freshly cut with a small clear glass of bright green celery juice (apigenin). CENTER — a small amber glass dropper bottle of dark green chlorophyllin liquid beside fresh leafy spinach and parsley leaves. RIGHT — a small white ceramic bowl of pale tan soluble prebiotic fiber powder beside a wooden scoop. Natural top-down lighting, magazine food editorial style, no text overlays, no labels." \
"" &

# IMAGE 5 - LAXATIVE BATHROOM vs MOTILLI KITCHEN CONTRAST
gen "05_contrast_laxative_motilli" "16:9" \
"Editorial diptych. LEFT half: a cluttered bathroom counter, harsh fluorescent light, a half-empty bottle of Miralax powder, a tipped bottle of magnesium pills, a strip of laxative tablets, crumpled tissues, a glass of water — desaturated and slightly chaotic mood. RIGHT half: a calm sunlit kitchen counter beside a bright window, a single clear-glass jar of Motilli celery juice fiber gummies with a bright kelly-green label, fresh celery stalks and a glass of water beside it, light morning steam from a coffee cup. Two distinct moods: chaos versus calm. No text overlays, no logos." \
"$PROD_REF" &

# IMAGE 6 - MOTILLI PRODUCT HERO
gen "06_motilli_product" "1:1" \
"Studio product hero photo of the Motilli bottle on a clean soft pastel celery-green background. Use the reference bottle EXACTLY: clear glass jar, bright kelly-green wraparound label reading 'motilli — CELERY JUICE FIBER GUMMIES — supports natural detoxification' in clean white sans-serif type, white screw cap. Three small dark-green heart-shaped gummies arranged at the base of the bottle. Soft top-down lighting, subtle shadow underneath, premium DTC supplement photography, ultra clean. No text overlays beyond the bottle's printed label." \
"$PROD_REF" &

# IMAGE 7 - THREE WOMEN EDITORIAL COLLAGE
gen "07_three_women_collage" "3:2" \
"Editorial collage of three separate portraits of women on GLP-1 medications, each lit naturally in their own home environment. LEFT portrait: Caroline, 51, warm short blonde hair, soft blue button-up shirt, smiling in her kitchen by a window. CENTER portrait: Diane, 58, silver bob haircut, knit cream sweater, laughing at a dinner table with a wine glass blurred in foreground. RIGHT portrait: Marlene, 62, salt-and-pepper hair, casual olive cardigan, peaceful expression looking off-camera, plants behind her. Soft natural lighting, magazine editorial portrait style. No text overlays, no clinical settings." \
"" &

# IMAGE 8 - CLUTTER vs CLEAN OVERHEAD COMPARISON
gen "08_clutter_vs_clean" "16:9" \
"Top-down editorial photo comparison on a white surface. LEFT half: a cluttered messy spread of laxative products — a box of Miralax, a bottle of magnesium citrate, a Senna pill bottle, a half-empty Linzess prescription bottle, scattered loose pills, all desaturated. RIGHT half: a clean minimal arrangement with a single Motilli bottle (bright kelly-green label, white cap), a small glass of water, a sprig of fresh celery, and a soft folded white cloth. Clear visual contrast between chaos and simplicity. No text overlays." \
"$PROD_REF" &

# IMAGE 9 - MORNING ROUTINE LIFESTYLE
gen "09_morning_routine" "3:2" \
"Editorial lifestyle photo. A woman in her mid-50s in a soft cream robe stands at her bright kitchen island in soft morning sunlight. She is holding a Motilli bottle in one hand and a glass of water in the other, smiling gently and looking down at the bottle. Fresh fruit and a vase of flowers on the counter, white cabinetry, large window with sheer linen curtains behind her. Warm, calm, hopeful tone. Magazine wellness photography style. No text overlays, no logos beyond the Motilli bottle label." \
"$PROD_REF" &

wait
echo ""
echo "ALL JOBS COMPLETE. Output dir:"
ls -la "$OUT/"

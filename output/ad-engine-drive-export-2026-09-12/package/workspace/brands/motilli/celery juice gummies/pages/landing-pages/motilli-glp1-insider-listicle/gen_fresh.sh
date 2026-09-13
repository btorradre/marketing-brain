#!/bin/bash
# Motilli GLP-1 Insider listicle — 4 FRESH images via Higgsfield gpt_image_2
# Matches the existing gen_images.sh pattern (proven). Image-to-image off the real jar for product shots.
export PATH="$HOME/.local/bin:$PATH"
set -u
BRAND="/Users/brooksorradre2/Documents/marketing brain/brands/motilli"
OUT="$BRAND/landing-pages/motilli-glp1-insider-listicle/images"
REF="$BRAND/brand/website-assets/motilli product reference.png"
mkdir -p "$OUT"
MANIFEST="$OUT/manifest.tsv"
: > "$MANIFEST"

gen () {
  local name="$1"; local aspect="$2"; local useref="$3"; local prompt="$4"
  local args=(generate create gpt_image_2 --prompt "$prompt" --aspect_ratio "$aspect" --resolution 2k --quality high --wait --wait-timeout 9m --json)
  if [ "$useref" = "ref" ]; then args+=(--image "$REF"); fi
  local json; json="$(higgsfield "${args[@]}" 2>/dev/null)"
  local url; url="$(printf '%s' "$json" | python3 -c "import sys,json
try:
 d=json.load(sys.stdin); j=d[0] if isinstance(d,list) else d; print(j.get('result_url',''))
except: print('')" 2>/dev/null)"
  if [ -n "$url" ]; then curl -sL "$url" -o "$OUT/$name.png"; printf '%s\t%s\t%s\n' "$name" "$url" "$OUT/$name.png" >> "$MANIFEST"; echo "OK $name"; else printf '%s\tFAILED\t\n' "$name" >> "$MANIFEST"; echo "FAIL $name"; printf '%s\n' "$json" | tail -3; fi
}

# ITEM 4 — bathroom routine comes back: a relaxed, relieved woman, physical ease
gen item04-relief 4:3 noref "Candid documentary photograph of a relaxed, relieved woman around 58 at home in comfortable casual clothes, sitting by a bright window with a warm mug of tea, soft genuine look of physical comfort and ease on her face, calm and unhurried. Soft natural morning light, cozy realistic living room, natural greys in her hair, health-editorial style, not staged, no text." &

# ITEM 7 — one gummy replaces the medicine cabinet: cluttered stack vs single Motilli jar
gen item07-one-vs-stack 4:3 ref "Editorial product photograph on a clean light surface showing a clear visual contrast: on the LEFT a cluttered crowded lineup of five generic supplement products (a tub of fiber powder, a jar of magnesium powder, an electrolyte drink-mix packet, a white probiotic bottle, and a box of stool softeners); on the RIGHT, standing alone with empty clean space around it, a single Motilli celery juice fiber gummies jar with two green heart-shaped gummies beside it. Bright clean studio light, realistic, simplicity versus clutter. Keep the exact Motilli label and jar shape from the reference image, no extra text." &

# ITEM 8 — formulated for GLP-1, standardized apigenin + chlorophyll + low-bulk fiber: science/lab feel
gen item08-formulation 4:3 ref "Clean science-forward product photograph: the Motilli celery juice fiber gummies jar on a bright white laboratory-style surface, surrounded by fresh crisp celery stalks, a small glass beaker of deep-green chlorophyll liquid, and a neat row of green heart-shaped gummies, soft clinical lighting, shallow depth of field, precise and standardized formulated feel. Realistic editorial product photography. Keep the exact Motilli label and jar shape from the reference image, no extra text." &

# BYLINE — Sarah Mitchell, RN, GI health writer: credible approachable author headshot
gen byline-sarah 1:1 noref "Professional friendly headshot portrait of a woman around 47 named Sarah, a registered nurse and health writer, warm approachable confident smile, shoulder-length brown hair, simple professional neutral top, soft neutral blurred indoor background, realistic available-light photography, looks like a credible verified author profile photo, no text." &

wait
echo "=== FRESH BATCH DONE ==="; cat "$MANIFEST"

#!/bin/bash
# Motilli GLP-1 Insider — regenerate the photo set at 1:1, NoraLife-inspired cohesive
# cream+sage palette. Mirrors gen_fresh.sh (proven). Product shots use image-to-image off the jar.
export PATH="$HOME/.local/bin:$PATH"
set -u
BRAND="/Users/brooksorradre2/Documents/marketing brain/brands/motilli"
OUT="$BRAND/landing-pages/motilli-glp1-insider-listicle/images"
REF="$BRAND/brand/website-assets/motilli product reference.png"
mkdir -p "$OUT"
MANIFEST="$OUT/manifest_1x1.tsv"; : > "$MANIFEST"

# shared style suffix for cohesion across the set (NoraLife = one warm world; ours = one green world)
STYLE="Bright clean premium editorial photography, soft natural daylight, cohesive cream-and-sage-green palette, gentle soft shadows, realistic, 1:1 perfectly square composition, no text, no logos other than the product."

gen () {
  local name="$1"; local useref="$2"; local prompt="$3"
  local args=(generate create gpt_image_2 --prompt "$prompt $STYLE" --aspect_ratio 1:1 --resolution 2k --quality high --wait --wait-timeout 9m --json)
  if [ "$useref" = "ref" ]; then args+=(--image "$REF"); fi
  local json; json="$(higgsfield "${args[@]}" 2>/dev/null)"
  local url; url="$(printf '%s' "$json" | python3 -c "import sys,json
try:
 d=json.load(sys.stdin); j=d[0] if isinstance(d,list) else d; print(j.get('result_url',''))
except: print('')" 2>/dev/null)"
  if [ -n "$url" ]; then curl -sL "$url" -o "$OUT/$name.png"; printf '%s\t%s\n' "$name" "$url" >> "$MANIFEST"; echo "OK $name"; else echo "FAIL $name"; printf '%s\n' "$json" | tail -3; fi
}

# ITEM 1 — product hero in an ingredient ring (NoraLife #1 signature)
gen item01-hero ref "A single Motilli celery juice fiber gummies jar standing in the exact center, encircled by a clean ring of fresh celery stalks, leafy celery tops, and a scatter of dark-green heart-shaped gummies arranged in a circle around it like an ingredient halo. Keep the exact Motilli jar shape, white cap, and bright green label from the reference image." &

# ITEM 4 — relief / bathroom routine returns (NoraLife #7 lifestyle vibe)
gen item04-relief noref "A relaxed, relieved woman around 58 sitting comfortably by a sunny window at home holding a warm mug, soft genuine expression of physical ease and calm, light airy room, natural greys in her hair." &

# ITEM 6 — sulfur burps stop / social confidence and closeness
gen item06-social noref "A confident happy woman around 58 laughing warmly and leaning in close with a friend over coffee at a bright table, relaxed and unselfconscious, airy bright home-cafe setting." &

# ITEM 7 — one gummy replaces the cabinet (single jar vs cluttered five)
gen item07-stack ref "On the LEFT a cluttered crowded cluster of five generic supplement products (a tub of fiber powder, a jar of magnesium powder, an electrolyte drink-mix packet, a white probiotic bottle, a box of stool softeners); on the RIGHT, standing alone with clean empty space around it, a single Motilli celery juice fiber gummies jar with two dark-green heart gummies beside it. Clear simplicity-versus-clutter contrast. Keep the exact Motilli jar shape, white cap, and green label from the reference image." &

# ITEM 8 — formulated / lab-tested authority (NoraLife #8: gloved hand holding the product)
gen item08-lab ref "A close-up of a gloved hand in a light blue nitrile glove holding up a single dark-green Motilli heart-shaped gummy between thumb and finger toward the camera, with a soft-focus laboratory and a smiling lab-coated researcher blurred in the background, and a Motilli jar softly visible on the clean bench. Science-forward and clinical. Keep the Motilli jar label from the reference image." &

wait
echo "=== 1:1 BATCH DONE ==="; cat "$MANIFEST"

#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
set -u
BRAND="/Users/brooksorradre2/Documents/marketing brain/brands/motilli"
OUT="$BRAND/landing-pages/motilli-celery-listicle-pagefly/images"
REF="$BRAND/brand/website-assets/motilli product reference.png"
mkdir -p "$OUT"

gen () {
  local name="$1"; local aspect="$2"; local useref="$3"; local prompt="$4"
  local args=(generate create gpt_image_2 --prompt "$prompt" --aspect_ratio "$aspect" --resolution 2k --quality high --wait --wait-timeout 9m --json)
  if [ "$useref" = "ref" ]; then args+=(--image "$REF"); fi
  local json; json="$(higgsfield "${args[@]}" 2>/dev/null)"
  local url; url="$(printf '%s' "$json" | python3 -c "import sys,json
try:
 d=json.load(sys.stdin); j=d[0] if isinstance(d,list) else d; print(j.get('result_url',''))
except: print('')" 2>/dev/null)"
  if [ -n "$url" ]; then curl -sL "$url" -o "$OUT/$name.png"; echo "OK $name"; else echo "FAIL $name"; fi
}

# ingredient + collage (need product ref) + 6 avatars (portraits) — all in parallel
gen ingredient-flatlay 4:3 ref "Overhead ingredient flat-lay on a light marble surface: the Motilli celery juice fiber gummies jar at center, fresh celery stalks, a small dish of green chlorophyll, and a scatter of green gummies arranged neatly around it. Bright clean studio light, fresh natural palette, realistic editorial product photography. Keep the exact Motilli label from the reference." &
gen customer-collage 1:1 ref "A 3x3 grid collage of nine different real-looking women aged 50 to 70, each smiling and holding up a Motilli celery juice fiber gummies jar (bright green label, white cap) in a casual home setting. Varied faces, hair colors, and rooms. Authentic user-generated-content style, warm natural lighting, realistic. Keep the Motilli jar label consistent with the reference." &
gen av-carol 1:1 noref "Friendly natural headshot portrait of a warm, trustworthy woman around 58 named Carol, soft smile, shoulder-length greying hair, simple top, neutral softly blurred background, realistic available-light photography, looks like a real verified customer profile photo." &
gen av-margaret 1:1 noref "Natural headshot portrait of a kind woman around 62, short silver hair, gentle smile, glasses, neutral background, realistic candid profile photo, soft daylight." &
gen av-susan 1:1 noref "Natural headshot portrait of a friendly woman around 55, shoulder-length brown hair with grey, warm smile, casual blouse, neutral blurred background, realistic profile photo." &
gen av-barbara 1:1 noref "Natural headshot portrait of a woman around 66, soft white-grey bob, calm warm expression, simple cardigan, neutral background, realistic candid profile photo, soft light." &
gen av-patricia 1:1 noref "Natural headshot portrait of a woman around 60, auburn-grey hair, bright friendly smile, light scarf, neutral softly blurred background, realistic profile photo." &
gen av-joanne 1:1 noref "Natural headshot portrait of a woman around 64, curly grey hair, gentle confident smile, neutral top, blurred warm background, realistic candid profile photo." &
wait
echo "=== ALL REMAINING DONE ==="

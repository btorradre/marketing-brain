#!/bin/bash
# Regenerate the 4 review testimonial avatars as customers HOLDING the Motilli jar (UGC selfie style,
# like the item10 customer collage). 1:1, image-to-image off the real jar so the label is accurate.
# Output to *-new.png for QA before swapping over the live names.
export PATH="$HOME/.local/bin:$PATH"
set -u
BRAND="/Users/brooksorradre2/Documents/marketing brain/brands/motilli"
OUT="$BRAND/landing-pages/motilli-glp1-insider-listicle/images"
REF="$BRAND/brand/website-assets/motilli product reference.png"
STYLE="Authentic user-generated-content selfie-style photograph, warm natural indoor lighting, realistic skin, casual home setting, 1:1 square, head and shoulders, holding the jar up near her shoulder so the label is clearly visible. Keep the exact Motilli jar shape, white cap, and bright green label from the reference image. No text overlay."

gen () {
  local name="$1"; local prompt="$2"
  local json; json="$(higgsfield generate create gpt_image_2 --prompt "$prompt $STYLE" --aspect_ratio 1:1 --resolution 2k --quality high --image "$REF" --wait --wait-timeout 9m --json 2>/dev/null)"
  local url; url="$(printf '%s' "$json" | python3 -c "import sys,json
try:
 d=json.load(sys.stdin); j=d[0] if isinstance(d,list) else d; print(j.get('result_url',''))
except: print('')" 2>/dev/null)"
  if [ -n "$url" ]; then curl -sL "$url" -o "$OUT/$name.png"; echo "OK $name"; else echo "FAIL $name"; printf '%s\n' "$json" | tail -3; fi
}

gen rev-linda-new   "A warm, genuine woman around 58 with shoulder-length silver-blonde hair, soft smile, simple casual top, holding up a Motilli celery juice fiber gummies jar." &
gen rev-diane-new   "A friendly woman around 62 with glasses and brown-and-grey hair, warm smile, casual blouse, holding up a Motilli celery juice fiber gummies jar." &
gen rev-barbara-new "A kind woman around 66 with a soft white-grey bob, gentle smile, simple cardigan, holding up a Motilli celery juice fiber gummies jar." &
gen rev-carol-new   "A cheerful woman around 55 with auburn-brown hair, bright smile, casual top, holding up a Motilli celery juice fiber gummies jar." &
wait
echo "=== REVIEW AVATARS DONE ==="
ls -la "$OUT"/rev-*-new.png 2>/dev/null

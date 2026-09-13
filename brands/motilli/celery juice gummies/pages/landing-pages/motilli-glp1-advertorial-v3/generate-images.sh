#!/bin/bash
# Generate all advertorial images via higgsfield gpt_image_2 in parallel
set -u
cd "$(dirname "$0")"
mkdir -p images logs

PRODUCT_REF="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/v6/1.png"

# Function: run a higgsfield job, extract result URL, download to images/
gen() {
  local name="$1"
  local aspect="$2"
  local prompt="$3"
  local media_flag="${4:-}"
  local log="logs/${name}.log"

  echo "[$(date +%H:%M:%S)] START $name ($aspect)" | tee -a "$log"

  # shellcheck disable=SC2086
  higgsfield generate create gpt_image_2 \
    --prompt "$prompt" \
    --aspect_ratio "$aspect" \
    --quality high \
    --resolution 2k \
    $media_flag \
    --wait \
    --wait-timeout 8m \
    > "$log" 2>&1

  # Extract first http(s) URL from log
  local url
  url=$(grep -oE 'https?://[^[:space:]]+' "$log" | head -1)
  if [ -z "$url" ]; then
    echo "[$(date +%H:%M:%S)] FAIL $name — no URL in log" | tee -a "$log"
    return 1
  fi

  curl -sSL "$url" -o "images/${name}.jpg"
  if [ -s "images/${name}.jpg" ]; then
    echo "[$(date +%H:%M:%S)] DONE $name — images/${name}.jpg ($(stat -f%z "images/${name}.jpg") bytes)" | tee -a "$log"
  else
    echo "[$(date +%H:%M:%S)] FAIL $name — download empty" | tee -a "$log"
    return 1
  fi
}
export -f gen

# ============= EDITORIAL / LIFESTYLE =============

gen hero "16:9" \
"Editorial magazine photograph of a woman around 55 in a sunlit cream-toned kitchen at morning, seated at a wooden table with a mug of tea, hand resting lightly on her stomach, soft contemplative expression looking out a window. Warm natural daylight, shallow depth of field, neutral palette of cream, sage, and warm beige. Lifestyle health-magazine editorial style. No text, no logos, no medications visible." &

gen secondary-1 "16:9" \
"Open bathroom medicine cabinet packed with constipation and gut products: a Miralax-style white bottle with blue cap, generic fiber gummy jars, a bottle of prunes, an amber magnesium pill bottle, a senna-style laxative box, all visibly used and a little disorganized. Warm overhead bathroom lighting, editorial wide-angle still life, muted cream and beige tones. No real brand names or readable text on labels — generic packaging." &

gen secondary-2 "16:9" \
"Fresh whole celery stalks, a bunch of flat-leaf parsley, and a tall clear glass of vivid green cold-pressed celery juice on a light oak countertop. Soft morning sunlight from the left, water droplets on the celery, clean editorial food-photography style. Cream and sage palette. No text, no labels." &

gen secondary-3 "16:9" \
"Candid editorial photograph of a woman in her late 50s laughing genuinely at a warm restaurant dinner table with two friends, glasses of water and plates between them. Soft amber restaurant lighting, intimate atmosphere, magazine-style lifestyle shot, slight bokeh background. No visible brand logos." &

gen phase-1 "3:2" \
"Editorial lifestyle photograph of a woman in her mid-50s sitting on the edge of a bed in soft morning sunlight streaming through linen curtains, cream-colored bedding, peaceful relieved expression, one hand resting on her stomach. Warm cream and beige palette, magazine quality, soft natural light. No text." &

gen phase-2 "3:2" \
"Editorial photograph of a woman in her mid-50s sleeping peacefully on her side in a softly-lit bedroom at night, cream linen pillow, dim blue moonlight from a window, calm restful expression. Cinematic warm-cool contrast, intimate quiet mood. No text, no devices visible." &

gen phase-3 "3:2" \
"Editorial lifestyle photograph of a woman in her late 50s walking outdoors on a tree-lined path at golden hour, comfortable cream sweater and dark leggings, energized natural stride, soft warm autumn light filtering through leaves. Magazine quality. No text, no logos." &

# ============= PORTRAITS =============

gen testi-robert "1:1" \
"Warm professional editorial portrait of a man around 61 years old, salt-and-pepper hair neatly trimmed, kind genuine smile, gentle eyes, wearing a soft blue casual button-down shirt, soft natural window light from the left, slightly blurred neutral cream studio background. Magazine quality headshot, friendly approachable. No text." &

gen testi-donna "1:1" \
"Warm professional editorial portrait of a woman around 58 years old, shoulder-length brunette hair with light highlights, friendly genuine smile, soft makeup, wearing a cream blouse, natural window light, slightly blurred neutral warm background. Editorial magazine headshot style, approachable and real. No text." &

gen testi-susan "1:1" \
"Warm professional editorial portrait of a woman around 67 years old, silver-grey shoulder-length hair, warm intelligent eyes, kind smile with light laugh lines, wearing a soft sage cardigan over a white top, natural studio window lighting, slightly blurred cream background. Editorial magazine headshot, dignified and approachable. No text." &

gen dr-marsh "1:1" \
"Professional editorial portrait of a female physician around 50 years old, brunette shoulder-length hair, warm intelligent confident expression with subtle smile, wearing a crisp white lab coat over a soft cream blouse, stethoscope around her neck, soft natural studio lighting, slightly blurred warm neutral medical office background with subtle bookshelves. Magazine-quality medical professional headshot. No text, no readable name badges." &

# ============= PRODUCT (image-to-image with reference) =============

gen product-hero "1:1" \
"Clean editorial product photograph of the motilli celery juice fiber gummies bottle (white screw cap, bright green label reading 'motilli'), single bottle centered on a soft cream backdrop with subtle natural shadow. Studio softbox lighting from upper left, sharp focus on label, warm magazine-quality product still. Match the bottle in the reference image exactly. No additional props, no text overlays." \
"--medias $PRODUCT_REF" &

gen callout-1 "16:9" \
"Soft editorial medical illustration of the human digestive system viewed from the front, with the stomach gently highlighted in warm sage green and the colon shown in muted neutral. Anatomically accurate but elegant magazine-infographic style, cream background, subtle linework, no labels, no text, no arrows. Health-magazine aesthetic." &

gen callout-2 "16:9" \
"Editorial top-down photograph of two soft dark-green chewable gummies resting on an open female palm with a fair complexion, warm natural daylight, soft shadow, cream background, clean minimal product lifestyle shot. The gummies should match the dark green motilli gummies in the reference image. No text, no logos visible." \
"--medias $PRODUCT_REF" &

wait
echo ""
echo "[$(date +%H:%M:%S)] ALL JOBS FINISHED"
ls -la images/

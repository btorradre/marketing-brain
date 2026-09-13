#!/bin/bash
# adv-1 image batch 1 — the four slots that do not depend on the product-truth decision.
set -u
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/celery juice gummies/pages/advertorials/glp1-adv-1/images"
LOGDIR="$OUT/.logs"
mkdir -p "$OUT" "$LOGDIR"

gen() {
  local slug="$1"; local aspect="$2"; local prompt="$3"; local ref="${4:-}"
  local log="$LOGDIR/${slug}.log"
  local args=(--prompt "$prompt" --aspect_ratio "$aspect" --quality high --resolution 2k --wait --wait-timeout 14m)
  [ -n "$ref" ] && args+=(--image "$ref")
  echo "[$slug] start $aspect" | tee "$log"
  higgsfield generate create gpt_image_2 "${args[@]}" >>"$log" 2>&1
  local url
  url=$(grep -Eo 'https://[^ ]+\.(png|jpg|jpeg|webp)' "$log" | head -1)
  if [ -n "$url" ] && curl -fsSL "$url" -o "$OUT/${slug}.png"; then
    echo "[$slug] OK" | tee -a "$log"
  else
    echo "[$slug] FAIL" | tee -a "$log"
  fi
}

# 1) LINDA — candid kitchen, narrator
gen "linda-kitchen" "4:3" \
"Candid amateur snapshot of a real 63-year-old white American woman standing in her own ordinary suburban kitchen in Arizona, morning. She has shoulder-length grey-blonde hair, light crow's feet and smile lines, no makeup beyond a little lipstick, a soft heather cardigan over a plain top. She has recently lost a lot of weight so the cardigan hangs slightly loose on her. She is caught mid-moment holding a glass of water, looking slightly off-camera with a tired, relieved, genuine half-smile. The kitchen is lived-in and imperfect: beige laminate counter, a coffee maker, a paper towel roll, a few mugs, a stack of mail, a wall calendar. Flat natural window daylight, slight phone-camera softness, mild digital noise, handheld framing, one shoulder slightly cropped. Photorealistic documentary snapshot, NOT a stock photo, NOT a studio portrait, NOT retouched, no glamour lighting, no shallow-depth-of-field bokeh look. Exactly five fingers on the visible hand. No text anywhere in the image." \
"" &

# 2) FOUNDER — functional nutritionist, Portland
gen "founder-portrait" "4:3" \
"Candid documentary photograph of a real woman in her early 40s who is a functional nutritionist, photographed in her small practice office in Portland Oregon. Brown hair loosely pulled back, minimal makeup, plain olive knit sweater, reading glasses pushed up on her head. She is seated at a cluttered wooden desk turned toward the camera with a calm, unpolished, slightly serious expression, mid-conversation rather than posing. Behind her: a shelf of clinical nutrition and gastroenterology textbooks, a few printed research papers with highlighter marks on the desk, a potted plant, grey Portland daylight through a window. Warm muted tones. Photorealistic, flat natural light, slight grain, imperfect framing, looks like a real person photographed by a colleague, NOT a stock photo, NOT a corporate headshot, no studio lighting. Exactly five fingers on any visible hand. No text anywhere in the image." \
"" &

# 3) THREE INGREDIENTS panel
gen "ingredients-panel" "16:9" \
"Clean editorial three-panel product-ingredient graphic on a pure white background, divided by two thin light-grey vertical rules into three equal panels. LEFT panel: a small bundle of fresh crisp green celery stalks with leafy tops, photographed top-down on white with a soft natural shadow. CENTER panel: a shallow clear glass dish of deep emerald-green liquid chlorophyll, rich and translucent, on white with a soft shadow. RIGHT panel: a small neat mound of fine off-white soluble fiber powder with a delicate silky texture on white with a soft shadow. Under each panel, one line of small clean dark-green (#1B4332) sans-serif capital text, centered: under the left panel 'APIGENIN', under the center panel 'CHLOROPHYLLIN', under the right panel 'SOLUBLE FIBER'. Bright even studio daylight, crisp focus, premium supplement editorial style. Render ONLY the three words specified above, spelled exactly. Do not invent any other words, badges, prices, star ratings, percentages, numbers or logos." \
"" &

# 4) GUARANTEE SEAL — page palette (deep green + gold), not navy
gen "guarantee-seal" "1:1" \
"A flat vector circular guarantee badge, centered on a plain cream (#FFF8F0) background. The badge is a solid deep forest-green (#1B4332) circle with a clean gold (#F4D03F) double-ring border and a subtle gold laurel sprig curving up each side. Inside the circle, stacked and centered in crisp gold and white sans-serif type: the large numeral '90' at the top in gold, the word 'DAY' directly beneath it in gold smaller capitals, then a thin gold horizontal divider line, then 'MONEY-BACK' in white capitals, then 'GUARANTEE' in white capitals. Sharp flat vector, no gradients, no photographic texture, no 3D bevel, no drop shadow, no gloss. Perfectly legible type. Render ONLY the words and numerals specified above, spelled exactly: 90, DAY, MONEY-BACK, GUARANTEE. Do not invent any other words, badges, prices, star ratings, percentages or logos." \
"" &

wait
echo "BATCH 1 COMPLETE"
ls -la "$OUT"/*.png 2>/dev/null

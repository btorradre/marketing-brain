#!/bin/bash
# adv-1 image batch 2 — gummy product shots (i2i from the live PDP bottle) + label-true ingredient panel.
set -u
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/celery juice gummies/pages/advertorials/glp1-adv-1/images"
REF="/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/067977b9-807f-4b1a-8d53-11d305023caf/scratchpad/gummy_ref.png"
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

# 5) PRODUCT CARD — clean packshot, i2i from the real bottle
gen "product-bottle" "4:3" \
"Edit this image. Keep the Motilli bottle EXACTLY as it appears in the reference: the same clear square jar with rounded corners, the same white screw cap, the same bright green wraparound label with identical wording, identical typography, identical layout and identical proportions, and the same dark olive-green gummies visible through the glass above and below the label. Do NOT redesign the label, do NOT reword it, do NOT change the jar silhouette. Only change the surroundings: place the jar upright, slightly left of center, on a clean bone-white surface against a seamless bone-white (#FFF8F0) background, lit by soft even daylight from the upper left with one gentle natural shadow falling to the lower right. To the right of the jar lay two fresh celery stalks with leafy tops, casually placed, not styled into a fan. Nothing else in frame. Photorealistic supplement product photography, crisp focus on the label, no gloss blowouts, no studio spotlights, no reflections on the background, no added text, no badges, no logos, no price, no star ratings." \
"$REF" &

# 6) FINAL CTA — bottle on the page's deep green
gen "product-cta" "16:9" \
"Edit this image. Keep the Motilli bottle EXACTLY as it appears in the reference: the same clear square jar with rounded corners, the same white screw cap, the same bright green wraparound label with identical wording, identical typography, identical layout and identical proportions, and the same dark olive-green gummies visible through the glass. Do NOT redesign the label, do NOT reword it, do NOT change the jar silhouette. Only change the surroundings: place the jar upright and centered on a seamless deep forest-green (#1B4332) background, lit by a soft overhead glow that falls off gently toward the corners, with a subtle natural shadow beneath the jar. Wide horizontal composition with generous empty deep-green space on both sides of the jar. A few fresh celery leaves rest on the surface near the base, dark and understated. Photorealistic, premium, editorial. No added text, no badges, no logos, no price, no star ratings, no seals." \
"$REF" &

# 7) INGREDIENTS PANEL v2 — label-true names
gen "ingredients-panel-v2" "16:9" \
"Clean editorial three-panel product-ingredient graphic on a pure white background, divided by two thin light-grey vertical rules into three equal panels. LEFT panel: a small bundle of fresh crisp green celery stalks with leafy tops, photographed top-down on white with a soft natural shadow. CENTER panel: a shallow clear glass dish of deep emerald-green liquid chlorophyll, rich and translucent, on white with a soft shadow. RIGHT panel: a small neat mound of fine off-white soluble prebiotic fiber powder with a delicate silky texture on white with a soft shadow. Under each panel, one line of small clean dark-green (#1B4332) sans-serif capital text, centered: under the left panel 'CELERY JUICE', under the center panel 'CHLOROPHYLL', under the right panel 'PREBIOTIC FIBER'. Bright even studio daylight, crisp focus, premium supplement editorial style. Render ONLY the words specified above, spelled exactly. Do not invent any other words, badges, prices, star ratings, percentages, numbers or logos." \
"" &

wait
echo "BATCH 2 COMPLETE"
ls -la "$OUT"/*.png

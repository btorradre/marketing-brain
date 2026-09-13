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
gen "product-bottle-v2" "4:3" \
"Edit this image. Keep the Motilli bottle EXACTLY as it appears in the reference: the same clear square jar with rounded corners, the same white screw cap, the same bright green wraparound label with identical wording, identical typography, identical layout and identical proportions, and the same dark olive-green gummies visible through the glass above and below the label. Do NOT redesign the label, do NOT reword it, do NOT change the jar silhouette. Two spelling corrections to the label, and ONLY these two: render the small line at the lower left of the label as '60 VEGAN GUMMIES / DIETARY SUPPLEMENT' (GUMMIES, not GUMMIER), and render the white pill badge as 'Clinically Tested Actives' (Clinically, with an L). Every other word, size and position on the label stays identical to the reference. Only change the surroundings: place the jar upright, slightly left of center, on a clean bone-white surface against a seamless bone-white (#FFF8F0) background, lit by soft even daylight from the upper left with one gentle natural shadow falling to the lower right. To the right of the jar lay two fresh celery stalks with leafy tops, casually placed, not styled into a fan. Nothing else in frame. Photorealistic supplement product photography, crisp focus on the label, no gloss blowouts, no studio spotlights, no reflections on the background, no added text, no badges, no logos, no price, no star ratings." \
"$REF" &

# 6) FINAL CTA — bottle on the page's deep green
gen "product-cta-v2" "16:9" \
"Edit this image. Keep the Motilli bottle EXACTLY as it appears in the reference: the same clear square jar with rounded corners, the same white screw cap, the same bright green wraparound label with identical wording, identical typography, identical layout and identical proportions, and the same dark olive-green gummies visible through the glass. Do NOT redesign the label, do NOT reword it, do NOT change the jar silhouette. Two spelling corrections to the label, and ONLY these two: render the small line at the lower left of the label as '60 VEGAN GUMMIES / DIETARY SUPPLEMENT' (GUMMIES, not GUMMIER), and render the white pill badge as 'Clinically Tested Actives' (Clinically, with an L). Every other word, size and position on the label stays identical to the reference. Only change the surroundings: place the jar upright and centered on a seamless deep forest-green (#1B4332) background, lit by a soft overhead glow that falls off gently toward the corners, with a subtle natural shadow beneath the jar. Wide horizontal composition with generous empty deep-green space on both sides of the jar. A few fresh celery leaves rest on the surface near the base, dark and understated. Photorealistic, premium, editorial. No added text, no badges, no logos, no price, no star ratings, no seals." \
"$REF" &

# 7) INGREDIENTS PANEL v2 — label-true names
wait
echo "BATCH 2 COMPLETE"
ls -la "$OUT"/*.png

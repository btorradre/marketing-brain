#!/bin/bash
# Generate the two missing advertorial images via higgsfield gpt_image_2
set -u
cd "$(dirname "$0")"
mkdir -p images logs

gen() {
  local name="$1"; local aspect="$2"; local prompt="$3"
  local log="logs/${name}.log"
  echo "[$(date +%H:%M:%S)] START $name ($aspect)" | tee -a "$log"
  higgsfield generate create gpt_image_2 \
    --prompt "$prompt" \
    --aspect_ratio "$aspect" \
    --quality high \
    --resolution 2k \
    --wait \
    --wait-timeout 8m \
    > "$log" 2>&1
  local url
  url=$(grep -oE 'https?://[^[:space:]]+' "$log" | head -1)
  if [ -z "$url" ]; then
    echo "[$(date +%H:%M:%S)] FAIL $name — no URL in log" | tee -a "$log"; return 1
  fi
  curl -sSL "$url" -o "images/${name}.jpg"
  if [ -s "images/${name}.jpg" ]; then
    echo "[$(date +%H:%M:%S)] DONE $name — $(stat -f%z "images/${name}.jpg") bytes" | tee -a "$log"
  else
    echo "[$(date +%H:%M:%S)] FAIL $name — download empty" | tee -a "$log"; return 1
  fi
}

# Two-panel mechanism diagram — clean clinical infographic, brand green #94C218
gen mechanism_split "16:9" \
"Clean clinical medical infographic, two panels side by side on a white background, bright lime-green (#94C218) accents and dark slate-blue line art. LEFT PANEL titled 'EVERY LAXATIVE' shows a simple human digestive silhouette with several red arrows all pointing low at the colon and exit, with a small red X — labeled 'wrong spot'. RIGHT PANEL titled 'MOTILLI' shows the same silhouette with three green labeled actions pointing at the stomach high up: 'MOTILITY', 'SULFUR', 'SOFTEN'. Minimal flat vector diagram style, generous white space, crisp legible sans-serif labels, health-magazine clinical aesthetic. No photographic elements." &

# Lifestyle — late-50s woman mid-laugh at outdoor family table, Sunday with grandkids
gen relief_family "16:9" \
"Candid editorial lifestyle photograph of a relaxed happy woman in her late 50s genuinely mid-laugh at a sunlit outdoor family table, soft afternoon golden-hour light through garden trees, family members slightly out of focus around the table, plates and glasses of water, warm natural 'Sunday with the grandkids' atmosphere. She is fully present and at ease, not performing. Shallow depth of field, magazine-quality lifestyle photography, warm cream and sage palette. No text, no logos, no medications visible." &

wait
echo ""
echo "[$(date +%H:%M:%S)] ALL JOBS FINISHED"
ls -la images/

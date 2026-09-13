#!/bin/bash
# Generate the 4 reference-style branded graphics for Motilli via higgsfield gpt_image_2.
# Brand: deep dark-green background, bright lime #94C218 accents, cream text.
# Mechanism: apigenin (motility) + sodium copper chlorophyllin (sulfur) + low-bulk soluble fiber (flow).
set -u
cd "$(dirname "$0")"
mkdir -p images logs

PRODUCT_REF="images/motilli_jar.png"

gen() {
  local name="$1"; local aspect="$2"; local prompt="$3"; local media_flag="${4:-}"
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

# 1) GUT HERO — dark panel, big headline + gut line-art
gen gut_hero "3:2" \
"Bold modern health-brand hero graphic on a deep dark-green (#16330f) background. Large heavy cream-white uppercase sans-serif headline filling the upper portion reading 'YOUR STOMACH BASICALLY STOPS MOVING.'. Behind and around the headline, a large elegant single-line-art illustration of a human stomach and intestines drawn in semi-transparent bright lime-green (#94C218) strokes. Below the headline, two lines of smaller cream-white subtext: 'Your GLP-1 slows your stomach by 50% or more. That is how it quiets appetite — but it also means food sits, ferments, and hardens.' A small bright lime-green chewable gummy icon in the bottom-right corner. Flat vector, generous spacing, crisp legible typography, premium supplement-brand aesthetic. No logos, no extra text." &

# 2) WHAT DOESN'T WORK / WHAT DOES — two-column comparison
gen what_works "3:2" \
"Clean comparison infographic on a warm cream (#f6f8f1) background, two equal columns separated by a thin vertical divider. LEFT column headed 'WHAT DOESN'T WORK' with a large bright red X icon under the heading, then four rows each beginning with a small red cross mark: 'Fiber supplements — bulk a jammed stomach', 'Stimulant laxatives — force the colon, cramps', 'Miralax — aimed at the wrong organ', 'Stool softeners — work at the exit only'. RIGHT column headed 'WHAT DOES' with a large bright lime-green (#94C218) checkmark icon under the heading, then four rows each beginning with a small green check: 'Apigenin from celery juice — restores motility', 'Copper chlorophyllin — neutralizes sulfur burps', 'Low-bulk soluble fiber — softens, no bloat', 'Folate (5-MTHF) + B6 — refills GLP-1 depletion'. A centered footer line in dark slate-green bold text: 'Built for a slowed GLP-1 stomach. Not a normal one.' Flat vector, dark slate-green body text, crisp legible sans-serif, generous spacing, modern supplement-brand style. No logos." &

# 3) THREE-BENEFIT DARK CARD
gen benefit_card "1:1" \
"Premium dark-green (#16330f) rounded-rectangle card graphic, three stacked benefit rows separated by thin lime-green dividers. Each row has a minimal bright lime-green (#94C218) single-line-art icon on the left and two lines of text on the right. Row 1: line-art intestines icon, bold cream-white title 'Gentle Daily Regularity', lime-green subtitle 'Apigenin restarts your stomach's natural motility'. Row 2: line-art stomach icon, bold cream-white title 'Ends the Sulfur Burps', lime-green subtitle 'Chlorophyll neutralizes the gas at the source'. Row 3: line-art brain icon, bold cream-white title 'Restores Energy and Clarity', lime-green subtitle 'Methylated folate + B6 for GLP-1 nutrient depletion'. Flat vector, crisp legible sans-serif, premium supplement-brand aesthetic. No logos, no extra text." &

# 4) DON'T QUIT panel — dark, product bottle (image-to-image from real jar)
gen dont_quit "1:1" \
"Bold dark-green (#16330f) vertical poster graphic. Heavy cream-white uppercase sans-serif headline at top reading 'DON'T QUIT YOUR GLP-1 OVER ONE SIDE EFFECT'. Below it, large friendly bright lime-green (#94C218) text reading 'Fix it.'. Centered beneath, the Motilli celery juice fiber gummies bottle from the reference image (white screw cap, bright green 'motilli' label, dark green gummies) standing with a soft shadow. At the very bottom, a small cream-white line: '90-Day Money-Back Guarantee'. Keep the bottle matching the reference exactly. Flat clean composition, generous spacing, premium supplement-brand aesthetic. No other text, no other logos." \
"--medias $PRODUCT_REF" &

wait
echo ""
echo "[$(date +%H:%M:%S)] ALL JOBS FINISHED"
ls -la images/

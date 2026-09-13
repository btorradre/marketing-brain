#!/bin/bash
# Generates all 11 advertorial images via higgsfield gpt_image_2.
# 6 graphic slots + Carol (byline/founder) + 4 testimonial portraits.
# Each job waits, then the result URL is curl'd down to images/<slug>.png
set -u
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/pages/advertorials/glp1-once-a-week/images"
PROD_REF="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/updated/product img 1.webp"
LOGDIR="$OUT/.logs"
mkdir -p "$OUT" "$LOGDIR"

gen() {
  local slug="$1"; local aspect="$2"; local prompt="$3"; local ref="${4:-}"
  local log="$LOGDIR/${slug}.log"
  local args=(--prompt "$prompt" --aspect_ratio "$aspect" --quality high --resolution 2k --wait --wait-timeout 12m)
  if [ -n "$ref" ]; then
    args+=(--image "$ref")
  fi
  echo "[$slug] starting ($aspect)..." | tee "$log"
  higgsfield generate create gpt_image_2 "${args[@]}" >>"$log" 2>&1
  local url
  url=$(grep -Eo 'https://[^ ]+\.(png|jpg|jpeg|webp)' "$log" | head -1)
  if [ -n "$url" ]; then
    if curl -fsSL "$url" -o "$OUT/${slug}.png"; then
      echo "[$slug] OK -> ${slug}.png" | tee -a "$log"
    else
      echo "[$slug] ERROR: download failed" | tee -a "$log"
    fi
  else
    echo "[$slug] ERROR: no result URL in log" | tee -a "$log"
  fi
}

# ============ 1. RECEIPT (portrait) ============
gen "receipt" "3:4" \
"Top-down photo of a slightly crumpled white paper receipt on a soft cream background with a faint shadow. Bold printed header at the top: 'The \$133 Problem'. Below it, monospace itemized lines, each with a hand-drawn red X mark to the right of the price: 'MIRALAX   \$25', 'SENNA   \$12', 'MAGNESIUM GLYCINATE   \$22', 'PROBIOTICS   \$35', 'DIGESTIVE ENZYMES   \$21', 'SLIPPERY ELM   \$18'. A dashed divider line, then 'TOTAL WASTED: \$133' in bold red. Below the receipt, a bright lime-green (#94C218) check mark next to bold text 'Motilli  \$23.99'. Editorial, high-contrast, realistic receipt paper texture. Every line of text crisp, sharp, perfectly legible and correctly spelled." \
"" &

# ============ 2. MECHANISM (4:3) ============
gen "mechanism" "4:3" \
"Flat vector health-blog illustration on a deep forest-green (#233611) background. A simplified, friendly diagram of a human stomach and colon shown as two clearly SEPARATE organs, each labeled in clean white sans-serif text: 'STOMACH' and 'COLON'. The stomach is highlighted bright lime-green (#94C218) with small stalled, static motion marks around it; the colon below sits muted and empty, waiting. Bold white headline across the top reading: 'YOUR STOMACH STOPS MOVING.' Rounded shapes, minimal, modern editorial, not clinical, no gore. All text large, legible, and correctly spelled." \
"" &

# ============ 3. WITHOUT / WITH (16:9) ============
gen "without-with" "16:9" \
"Two side-by-side flat vector stomach illustrations in a health-blog style on a light cream background, split down the middle by a thin divider. LEFT side, header label 'WITHOUT MOTILLI' in muted red: a stomach congested with backed-up brown food dots piling up and downward stalled red arrows. RIGHT side, header label 'WITH MOTILLI' in green (#94C218): the same stomach with smooth green directional arrows and food moving out on schedule, calm and clear. Strong visual contrast between stuck and flowing. Rounded, friendly, modern, not clinical, no gore. Labels large, legible, correctly spelled." \
"" &

# ============ 4. PRODUCT JAR (1:1, image-to-image) ============
gen "product-jar" "1:1" \
"Clean premium product photograph of the Motilli supplement jar from the reference image: a clear cylindrical glass jar with a white screw-on cap and a bright lime-green (#94C218) wraparound label reading 'motilli' in white lowercase and 'CELERY JUICE FIBER GUMMIES' in white block capitals. Maintain the exact label design, proportions, and colors from the reference. The jar sits on a clean white surface in soft natural daylight with a few fresh celery stalks with green leaves and a single green apple beside it. Dark forest-green heart-shaped gummies visible through the glass. Premium, trustworthy supplement look, soft natural shadow. Label text sharp and legible. No extra text, badges, or graphics." \
"$PROD_REF" &

# ============ 5. RESULT HERO (16:9) ============
gen "result-hero" "16:9" \
"Warm candid lifestyle photograph with soft morning light coming through a kitchen window. A relaxed, content woman in her early 60s wearing a cozy cardigan stands at the kitchen counter holding a coffee mug with both hands (exactly five fingers on each hand), calm and relieved, a gentle natural smile, caught mid-moment, not posed. On the counter beside her sits a clear glass jar of Motilli celery gummies with a bright lime-green label. Neutral cream and warm wood tones, shallow depth of field, authentic documentary style, photorealistic, not stocky. No text overlays." \
"" &

# ============ 6. CTA BOTTLE (1:1, image-to-image) ============
gen "cta-bottle" "1:1" \
"The Motilli jar from the reference image (clear glass jar, white cap, bright lime-green #94C218 label reading 'motilli' lowercase and 'CELERY JUICE FIBER GUMMIES', dark forest-green heart-shaped gummies visible inside) centered on a deep forest-green (#1c2c0e) background with a soft spotlight glow from above. Maintain the exact label design, proportions, and colors from the reference. In the lower corner, a small clean white circular badge reading '90-DAY MONEY-BACK GUARANTEE'. High-contrast, premium, photorealistic. Label and badge text sharp and legible." \
"$PROD_REF" &

# ============ 7. CAROL (byline + founder) ============
gen "carol" "1:1" \
"Authentic headshot portrait of a warm, friendly retired schoolteacher named Carol, about 60 years old, soft grey-blonde hair, gentle genuine smile, simple cardigan, neutral home background, natural daylight. She looks like a real person in an online health community, not a model or stock photo. Photorealistic, candid, relatable. Exactly five fingers if any hand is visible." \
"" &

# ============ 8. PATRICIA (testimonial) ============
gen "testi-patricia" "1:1" \
"Authentic candid headshot of Patricia, a warm friendly white woman about 64 years old, relaxed genuine expression, soft natural home lighting. Looks like a real verified customer review selfie, not a stock model. Photorealistic. Exactly five fingers if any hand is visible." \
"" &

# ============ 9. MARGARET (testimonial) ============
gen "testi-margaret" "1:1" \
"Authentic candid headshot of Margaret, a warm friendly Latina woman about 61 years old, relaxed genuine smile, soft natural home lighting. Looks like a real verified customer review selfie, not a stock model. Photorealistic. Exactly five fingers if any hand is visible." \
"" &

# ============ 10. ROBERT (testimonial) ============
gen "testi-robert" "1:1" \
"Authentic candid headshot of Robert, a friendly man about 64 years old, an engineer, wearing glasses, salt-and-pepper hair, calm genuine expression, soft natural home lighting. Looks like a real verified customer review selfie, not a stock model. Photorealistic. Exactly five fingers if any hand is visible." \
"" &

# ============ 11. LINDA (testimonial) ============
gen "testi-linda" "1:1" \
"Authentic candid headshot of Linda, a warm friendly Black African-American woman about 58 years old, relaxed genuine smile, soft natural home lighting. Looks like a real verified customer review selfie, not a stock model. Photorealistic. Exactly five fingers if any hand is visible." \
"" &

wait
echo ""
echo "ALL JOBS COMPLETE."
echo "Images in $OUT:"
ls -la "$OUT"/*.png 2>/dev/null || echo "(no images — check $LOGDIR)"

#!/bin/bash
# Generates all 7 advertorial images via higgsfield gpt_image_2

set -e
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/pages/advertorials/health-insider-glp1/images"
PROD_REF="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/updated/product img 1.webp"
LOGDIR="$OUT/.logs"
mkdir -p "$OUT" "$LOGDIR"

# Job function: gen <slug> <aspect> <prompt> [image_ref]
gen() {
  local slug="$1"; local aspect="$2"; local prompt="$3"; local ref="$4"
  local log="$LOGDIR/${slug}.log"
  local args=(--prompt "$prompt" --aspect_ratio "$aspect" --quality high --resolution 2k --wait --wait-timeout 10m)
  if [ -n "$ref" ]; then
    args+=(--image "$ref")
  fi
  echo "[$slug] starting..." | tee "$log"
  higgsfield generate create gpt_image_2 "${args[@]}" >>"$log" 2>&1
  echo "[$slug] done" | tee -a "$log"
}

# ============ IMAGE 1: HERO ============
gen "01_hero" "3:2" \
"Warm editorial lifestyle photograph composited with a clean medical infographic overlay. Right two-thirds of frame: a 45-year-old woman who has visibly lost weight on a GLP-1 medication, sitting at a softly lit restaurant dinner table with two friends in the background out of focus. She wears a fitted cream sweater and smiles politely at the camera, but one hand rests discreetly on her lower belly which is noticeably distended and bloated under the fabric. Subtle micro-expression of discomfort behind the smile. Wine glasses, plates, candle light. Warm golden ambient lighting. Left third of frame: a large circular cutout overlay (clean white border, soft drop shadow) containing a stylized medical illustration of the upper human digestive tract — esophagus connecting to a clearly drawn STOMACH which is highlighted in glowing red with visible gas bubbles and fermentation icons inside it. A thick handdrawn-style bright red arrow points directly at the stomach with bold black sans-serif text label reading 'ROOT CAUSE'. The infographic style is clean, modern, editorial — like a Health Magazine illustration. The overall image feels like a Health-Insider article hero. High detail, photorealistic woman, crisp infographic overlay." \
"" &

# ============ IMAGE 3: LAXATIVE TRAP ============
gen "03_laxative_trap" "3:2" \
"High contrast black and white documentary-style still life photograph, top-down overhead view of a cluttered bathroom counter. On the counter: a large white-and-blue powder laxative bottle with a generic label reading 'POLYETHYLENE GLYCOL POWDER', a pink rectangular box of stimulant laxative tablets, a brown amber bottle of senna pills tipped over with a few pills spilling out, a green box of 'SMOOTH MOVE' style herbal laxative tea, and a clear bottle of generic orange fiber gummies. A woman's pale hand reaches in from the right edge of the frame, fingers hovering uncertainly above the products. Harsh top lighting, dramatic shadows, completely desaturated black and white tones. Composited over the entire image is a bold bright RED painterly X, like a hand-painted slash, opaque, dominant, taking up most of the frame. The X is the only color in the image. Editorial photo-essay style. The image conveys frustration and futility." \
"" &

# ============ IMAGE 4: MECHANISM DIAGRAM ============
gen "04_mechanism_diagram" "4:3" \
"Clean modern educational medical infographic on a soft cream-colored background. Title across the top in bold dark serif text: 'Where Your Laxatives Actually Work'. Below the title: a vertical anatomical illustration of the human digestive tract drawn in a clean modern editorial style — esophagus at top, then a prominent STOMACH organ, then small intestine coiling in the middle, then large intestine and COLON at the bottom. The STOMACH at the top is highlighted with a glowing soft-red circle around it and labeled in red sans-serif text reading 'ROOT CAUSE — Where your GLP-1 slows everything down'. A vertical red downward arrow runs from the stomach all the way to the colon, with a small label reading '6 feet' along its length. The COLON at the bottom is highlighted with a muted gray circle and labeled in gray text reading 'Where every laxative works — 6 feet too late'. Bottom caption in serif italic text: 'The problem starts upstream.' Style: modern medical illustration with soft line work, warm earth-tone palette, editorial magazine quality, like an infographic in The New York Times health section." \
"" &

# ============ IMAGE 5: FORMULA HERO (uses bottle ref) ============
gen "05_formula_hero" "4:3" \
"Premium product hero composition on a soft warm gradient background blending sage green to cream. In the exact center of the frame: the Motilli supplement bottle from the reference image — clear glass jar with a bright kelly-green wraparound label reading 'motilli — Celery Juice Fiber Gummies' in clean white sans-serif, white screw cap. Maintain the bottle's exact label design and proportions. Surrounding the bottle in a balanced circular arrangement: 3 round white-bordered photo medallions, each with a soft drop shadow:
- Top-left medallion: vibrant fresh celery stalks with green leaves, with a subtle molecular structure icon overlay, with a small label below reading 'Apigenin (Celery Extract)'.
- Top-right medallion: lush bright green chlorophyll-rich leaves, slightly dewy, with a small label below reading 'Sodium Copper Chlorophyllin'.
- Bottom-center medallion: golden-toned close-up of soft soluble fiber strands / oat fiber texture, with a small label below reading 'Low-Bulk Soluble Fiber'.
Scattered around the base of the bottle: 5-6 dark green heart-shaped gummies (matching the reference). Fresh celery stalks and leaves at the bottom corners. Premium supplement brand photography, soft natural studio lighting, clean editorial composition like a Ritual or Olly product hero. Photorealistic, high detail." \
"$PROD_REF" &

# ============ IMAGE 6: DAILY LIFE COLLAGE (uses bottle ref) ============
gen "06_daily_life_collage" "3:2" \
"Warm lifestyle photo collage composition on a softly-lit warm wooden table surface, viewed slightly from above. The collage consists of 4 overlapping rectangular photographs arranged like scattered polaroids with white borders and soft drop shadows. All 4 photos feature the SAME 45-year-old woman with shoulder-length brown hair, warm features, who has visibly lost weight on a GLP-1:
- Top-left photo: she is mid-laugh during a long dinner with friends, plate cleared in front of her, leaning back relaxed, no hand on belly, candlelit restaurant.
- Top-right photo: she leans across a small cafe table chatting with a girlfriend over coffee, totally present and engaged, soft window light.
- Bottom-left photo: she lifts a 3-year-old grandchild up in the air, arms strong and free, sunlit backyard.
- Bottom-right photo: she walks confidently outdoors on a sunlit park path, hands swinging freely, warm afternoon light.
Centered at the bottom-front of the collage, sitting on a small slice of natural wood: the Motilli supplement bottle from the reference image — clear glass jar, bright kelly-green label reading 'motilli — Celery Juice Fiber Gummies', white cap. Maintain the bottle's exact label. A few dark green heart-shaped gummies scattered next to it. Warm editorial lifestyle photography, golden afternoon light, candid moments, photorealistic, high detail." \
"$PROD_REF" &

# ============ IMAGE 7: WEEKLY TIMELINE ============
gen "07_weekly_timeline" "16:9" \
"Horizontal three-panel side-by-side editorial photograph showing the SAME 45-year-old woman (shoulder-length brown hair, warm features, GLP-1 weight-loss avatar) across three progressive moments. Identical facial features, same person, across all three panels. Each panel has a soft semi-transparent orange banner across the bottom third with crisp white sans-serif text:
- LEFT PANEL: the woman stands at a kitchen counter in the morning holding a coffee mug with both hands, wearing a soft cream cardigan, neutral expression, soft window light coming from the right, kitchen tones muted. Banner text: 'Week 1-2: The Quiet Start'.
- CENTER PANEL: the same woman outdoors at a brunch table with a girlfriend, mid-laugh, wearing a light denim shirt, brighter cheerful clothing, sunny patio setting. Banner text: 'Week 2-3: The First Real Sign'.
- RIGHT PANEL: the same woman walking confidently along a sunlit park path in golden afternoon light, wearing a vibrant warm-coral blouse, energized expression, full of life, arms moving freely. Banner text: 'Week 4+: The Turn'.
Three panels separated by thin white vertical lines. Warm editorial portrait photography, consistent face and identity across all three panels, photorealistic, magazine quality." \
"" &

# ============ IMAGE 2: SIDEBAR PRODUCT CARD (uses bottle ref) ============
gen "02_product_sidebar" "1:1" \
"Clean e-commerce product photograph: the Motilli supplement bottle from the reference image, centered on a pure white seamless background, lit from the front-left with soft diffused natural studio lighting creating a gentle natural shadow underneath. Slight 3/4 angle so the label is fully readable. Maintain the bottle's exact design — clear glass jar, bright kelly-green wraparound label reading 'motilli — Celery Juice Fiber Gummies', white screw cap. To the right of the bottle: 2-3 dark green heart-shaped gummies arranged casually. No additional text overlays, badges, or graphics. Premium clean supplement product card photography." \
"$PROD_REF" &

wait
echo ""
echo "ALL JOBS COMPLETE. Checking logs:"
ls -la "$LOGDIR/"

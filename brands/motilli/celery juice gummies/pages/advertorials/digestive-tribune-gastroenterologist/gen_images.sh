#!/bin/bash
# Generates all 6 inline advertorial images via higgsfield gpt_image_2
# Prompts from the JSON specs embedded in the Dr. Adrian Holt advertorial copy

set -e
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/pages/advertorials/digestive-tribune-gastroenterologist/images"
PROD_REF="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/updated/product img 1.webp"
LOGDIR="$OUT/.logs"
mkdir -p "$OUT" "$LOGDIR"

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

# IMAGE 1: HERO - Doctor + stomach split panel
gen "01_hero" "3:2" \
"Split-panel medical editorial photo. Left panel: 50-year-old female board-certified gastroenterologist with shoulder-length dark hair, navy blouse, no white coat, no stethoscope, sitting at a wood desk in a modern clinic, neutral confident expression, soft window light. Right panel: clean medical illustration of a human stomach in cross-section, shown distended with food pellets backing up at the pyloric exit, color-coded to show slowed motility at the top of the digestive tract. Clean white background. Editorial style. No text overlays." \
"" &

# IMAGE 2: 3-PANEL WOMAN LIFESTYLE - Miralax/bloating/bathroom (16:9 - wide panel)
gen "02_miralax_failure" "16:9" \
"Three-panel medical lifestyle photo of a woman in her early 50s. Panel 1: hand pouring Miralax powder into a Gatorade bottle, kitchen counter, soft morning light. Panel 2: same woman seated on couch, both hands on visibly bloated lower abdomen, wincing slightly. Panel 3: same woman standing next to a toilet, expression of frustration, roll of toilet paper visible. Connected by red arrows. Clean editorial color palette. No text overlays." \
"" &

# IMAGE 3: STOMACH MECHANISM DIAGRAM
gen "03_stomach_diagram" "4:3" \
"Clean medical illustration of the human stomach in cross-section, anatomically accurate. Visible slowing at the pyloric sphincter (lower stomach exit). Food shown as small particles in upper stomach, fermenting and producing gas bubbles. Red distension arrows on stomach walls showing stretching. Labels for 'slowed gastric emptying' and 'fermentation' visible. Neutral medical illustration style, white background. Subtle red and yellow accent colors only." \
"" &

# IMAGE 4: CELERY / APIGENIN
gen "04_celery_apigenin" "4:3" \
"Macro photo of fresh celery stalks freshly cut on a wood cutting board, with a small clear glass of bright green celery juice beside them. Sunlight streaming in. A small mortar with crushed dried herb visible to the side. Editorial natural-food photography style. Clean and clinical, not crunchy or rustic. No text overlays." \
"" &

# IMAGE 5: MOTILLI PRODUCT REVEAL
gen "05_motilli_product" "1:1" \
"Studio product photo of a single Motilli supplement bottle on a clean soft-pastel background (pale celery green). The bottle from the reference image — clear glass jar, bright kelly-green wraparound label reading 'motilli — Celery Juice Fiber Gummies' in clean white sans-serif, white screw cap. Maintain the bottle's exact label design and proportions. Two pale-green heart-shaped gummies resting at the base of the bottle. Soft top lighting, slight shadow. Clean DTC supplement photography style. No props, no text overlays beyond bottle label." \
"$PROD_REF" &

# IMAGE 6: PATIENT TESTIMONIAL COLLAGE
gen "06_patient_collage" "3:2" \
"Editorial collage layout of 6 portrait photos of women between ages 45 and 65, varied ethnicities, all holding or near a small Motilli bottle. Natural everyday lifestyle photography, not studio. Each woman shows a soft, relieved, content expression. Grid of 6 thumbnail-style shots. No text overlays, no captions, no clinical setting. Warm, hopeful tone." \
"$PROD_REF" &

wait
echo ""
echo "ALL JOBS COMPLETE. Checking logs:"
ls -la "$LOGDIR/"

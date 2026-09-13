#!/bin/bash
# Generates all 5 advertorial images via higgsfield gpt_image_2
set -e
OUT="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/pages/advertorials/glp1-motility-suppression/images"
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

# ============ 01 HERO ============
gen "01_hero" "3:2" \
"Warm editorial portrait photograph in a soft naturally-lit gastroenterology consultation room. PRIMARY SUBJECT: a 52-year-old female gastroenterologist (Dr. Rebecca Marsh), warm features, shoulder-length salt-and-pepper hair tucked behind her ears, wearing a soft cream cashmere sweater under an open lightweight unbuttoned white doctor's coat with a stethoscope around her neck. She stands at the right-center of the frame with her arms gently crossed, looking directly at the camera with a serious, compassionate, focused expression — not smiling, but warm and authoritative. Behind her on the wall: framed medical diplomas softly out of focus, a partial anatomical diagram of the digestive system pinned to a corkboard. To her left in the frame, partially cropped at the edge: the shoulder and side of a 60-year-old female patient (visible from shoulder to lower torso only, face cropped out of frame), wearing a soft beige cardigan, one hand resting protectively on her own bloated lower abdomen. Soft warm overhead clinical lighting blended with natural window light from the left, creating gentle shadows. Color palette: warm cream, soft beige, sage green, muted clinical neutrals. Shallow depth of field, photorealistic editorial portrait quality. The composition feels like a Health Magazine cover feature on a respected physician. No on-image text." \
"" &

# ============ 02 SPREADSHEET BEFORE/AFTER ============
gen "02_spreadsheet" "3:2" \
"Top-down editorial product photograph on a softly lit warm cream-colored linen tablecloth surface. Two iPhones placed side by side at slight angles, each displaying a Notes app or simple spreadsheet app on its screen. LEFT PHONE (labeled subtly with small white sticky note above reading 'DAY 6'): the screen shows a tracking spreadsheet with columns 'DATE | TIME | ATTEMPT | RESULT'. Rows visible: 11 consecutive rows with dates like 'Mar 14', 'Mar 15', 'Mar 16', 'Mar 17', 'Mar 18', 'Mar 19', 'Mar 20', 'Mar 21', 'Mar 22', 'Mar 23', 'Mar 24', each with 'YES' attempted but 'NO' in the RESULT column displayed in dark red text. The repetition of red 'NO' down the column is visually striking. RIGHT PHONE (labeled subtly with small white sticky note above reading 'DAY 23'): same app, same spreadsheet structure, columns 'DATE | TIME | ATTEMPT | RESULT'. Rows visible: dates like 'Apr 5', 'Apr 6', 'Apr 7', 'Apr 8', 'Apr 9', 'Apr 10', 'Apr 11', 'Apr 12' — most with 'YES' in the RESULT column in dark green text, a normal pattern of daily or every-other-day results. Both phone screens are crisp and clearly readable. Soft natural window light from upper left, gentle shadows under the phones. A small notepad and pen sit casually in the upper corner. Style: editorial documentary photograph, like a New York Times health feature illustration. Photorealistic, high detail. No additional text overlays beyond the phone screens and small sticky notes." \
"" &

# ============ 03 DIAGRAM ============
gen "03_diagram" "5:4" \
"Clean modern editorial medical infographic on a soft warm cream background. Title across the top in bold dark Georgia serif: 'Where Your Laxatives Actually Work'. Below the title: a vertical anatomical illustration of the upper-to-lower human digestive tract drawn in clean modern editorial line-illustration style with warm muted earth-tone colors. Top of the tract: esophagus. Then a prominent labeled STOMACH organ highlighted with a soft glowing red circular outline around it, with a clean sans-serif label arrow pointing to it reading in red: 'MOTILITY SUPPRESSION HERE — where your GLP-1 mutes the vagal signal'. A long thin red vertical arrow drops from the stomach through the small intestine (coiled in the middle) down to the COLON at the bottom. A small label near the middle of this arrow reads in gray: '~4 feet'. The COLON at the bottom is circled in muted gray with a sans-serif label reading in gray: 'WHERE EVERY LAXATIVE YOU HAVE TRIED WORKS — 4 feet too late'. Bottom of the image: a small italic serif caption reading 'The blockage is upstream of every solution you have tried.' Color palette: warm cream background, muted sage green organs, soft red highlight, muted charcoal-gray labels. Style: modern editorial medical infographic in the style of a New York Times or The Atlantic health feature. Clean, sophisticated, not childish. Photorealistic illustration quality." \
"" &

# ============ 04 PRODUCT ============
gen "04_product" "1:1" \
"Premium e-commerce product photograph on a soft warm cream background with subtle natural gradient. Centered in the frame: a woman's hand (mature, 50s, soft natural skin, no jewelry beyond a simple wedding band) gently holding the Motilli supplement bottle from the reference image — clear glass jar with a bright kelly-green wraparound label reading 'motilli — Celery Juice Fiber Gummies' in clean white sans-serif, white screw cap. Maintain the bottle's exact label design, proportions, and color exactly as in the reference. The bottle is shown at a slight 3/4 angle so the label is fully readable. Around the base of the bottle: 4-5 dark forest-green heart-shaped gummies scattered casually. Two fresh celery stalks with green leaves placed naturally to the lower left, framing the bottom of the composition. Soft natural studio lighting from the front-left, gentle natural shadow underneath. Color palette: warm cream, kelly green, forest green, soft natural skin tones. Style: premium supplement brand product photography like Ritual or Olly. No additional text overlays, badges, or graphics. Photorealistic, high detail." \
"$PROD_REF" &

# ============ 05 WEEK 10 ============
gen "05_week10" "3:2" \
"Warm candid editorial lifestyle photograph at a family dinner table. PRIMARY SUBJECT: a 63-year-old woman with shoulder-length silver-and-brown hair, soft natural makeup, wearing a comfortable but flattering deep teal knit top. She sits at a dinner table mid-laugh, head tilted slightly back, one hand resting gently on the table near a half-eaten plate of food, the other gesturing as she talks. Her expression is genuinely comfortable and present — not posed, not performing — the look of someone who has spent two hours at dinner without thinking about her stomach once. Out of focus in the background: a warmly lit dining room with two other family members visible (an adult daughter and a husband across the table), wine glasses, soft candle light, a serving platter, the remains of a long unhurried meal. Warm golden ambient lighting from candles and a soft overhead pendant. Color palette: deep teal, warm gold candlelight, soft cream tablecloth, muted background. Shallow depth of field with focus on the woman. Style: editorial lifestyle photography like a Real Simple magazine feature, candid moment quality. Photorealistic, high detail. No on-image text." \
"" &

wait
echo ""
echo "ALL JOBS COMPLETE. Checking logs:"
ls -la "$LOGDIR/"
echo ""
echo "Images in $OUT:"
ls -la "$OUT"/*.{jpg,png,webp} 2>/dev/null || echo "(no images yet — check logs)"

#!/bin/bash
# Submit all 28 image jobs to higgsfield in parallel.
cd "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/landing-pages/assets/new-gen"
mkdir -p jobs
rm -f jobs/*.json jobs/*.err jobs/_errors.log

PRODUCT_REF="5a7b6f07-d090-4bec-86ef-2eaeabe48192"

# submit_img <name> <model> <prompt>   (no product ref)
submit_img() {
  local name="$1"; local model="$2"; local prompt="$3"
  (
    higgsfield generate create "$model" --prompt "$prompt" --json > "jobs/${name}.json" 2> "jobs/${name}.err"
  ) &
}

# submit_img_ref <name> <model> <prompt>  (uses product ref)
submit_img_ref() {
  local name="$1"; local model="$2"; local prompt="$3"
  (
    higgsfield generate create "$model" --prompt "$prompt" --image "$PRODUCT_REF" --json > "jobs/${name}.json" 2> "jobs/${name}.err"
  ) &
}

# ============ HERO ============
submit_img_ref "hero" "gpt_image_2" \
"Hero banner image for a wellness supplement landing page. The Motilli bottle (clear plastic jar with lime-green wraparound label, white cap, dark green heart-shaped gummies inside) prominently centered. Around the bottle: exploded scattering of dark green heart-shaped gummies on a pale lime-green tray surface, fresh celery stalks with leafy tops, halved green apple slices. Soft natural diffused daylight. Clean white-to-pale-lime gradient background. Composition leaves negative space on the right third. Crisp DTC supplement product photography, magazine quality, sharp focus on the bottle label. Square 1:1 framing."

# ============ SECTION ILLUSTRATIONS ============
submit_img "s1-apigenin" "gpt_image_2" \
"Modern editorial scientific illustration on pure white background. Two side-by-side stylized human stomach silhouettes. LEFT stomach: drowsy and slow, muted dusty red and grey tones, small food particles sitting still inside, droopy posture. RIGHT stomach: awake and active, vibrant lime green color, food particles flowing through with curved green motion-arrow swooshes around it. Below the stomachs: three fresh celery stalks laid horizontally and a tiny hexagonal apigenin molecular diagram floating beside the right stomach. Friendly, flat-vector editorial style, clean line work, no text labels. Square 1:1."

submit_img_ref "s2-chlorophyllin" "gpt_image_2" \
"A woman's hand (early 40s, soft natural skin, simple wedding band only) gently holding the Motilli bottle upright in a clean modern kitchen. Soft diffused window light from the left. White marble countertop, blurred small potted herb in background. Bottle label fully sharp and readable. Warm relaxed lifestyle DTC photography. Square 1:1."

submit_img "s3-morning" "nano_banana_2" \
"Lifestyle photograph: woman age 45, casual cream linen top, shoulder-length hair, holding a white ceramic coffee mug at a kitchen island. Soft morning sunlight from a window on the left. Relaxed peaceful expression looking off-camera. On the counter slightly behind her, soft-focused: a small white GLP-1 injection pen with blue accent, not focal. White, cream, natural wood tones. Hint of lime green accent (a single celery stalk in a clear glass vase). Bright airy calm DTC lifestyle photography. Square 1:1."

submit_img "s4-dinner-relaxed" "nano_banana_2" \
"Lifestyle photograph: woman age 48, mid-conversation at a warmly-lit restaurant table, fork in hand mid-gesture, plate of healthy colorful food (grilled salmon, greens, roasted vegetables) in front. Warm restaurant lighting, soft bokeh in background. She looks comfortable, engaged, at ease, slight smile. Casual smart outfit. Genuine candid feel. Square 1:1."

submit_img "s5-family-dinner" "nano_banana_2" \
"Lifestyle photograph: four friends (mix of women in their 40s and 50s, one man in his 50s) around a warmly-lit outdoor dinner table at golden hour. Candid laughter, hands gesturing, sharing pasta, salads, bread, wine. String lights overhead. Genuine joyful expressions, no posing. Warm orange and amber tones. Filmic candid lifestyle photography. Square 1:1."

# ============ PRODUCT GALLERY ============
submit_img_ref "p1" "gpt_image_2" \
"Front-facing studio product photograph of the Motilli bottle on pure seamless white background. Bottle perfectly centered, head-on. Crisp soft lighting with subtle contact shadow beneath. Label fully readable. White cap. Clear jar showing dark green heart-shaped gummies inside. Clean ecommerce hero shot. Square 1:1."

submit_img_ref "p2" "gpt_image_2" \
"Studio product photograph of the Motilli bottle at a 3/4 angle on pure white background. Slight realistic contact shadow beneath. Side and front of the label both visible — wordmark prominent. Clean even studio lighting. Dark green heart-shaped gummies visible inside. White screw cap. Square 1:1."

submit_img_ref "p3" "gpt_image_2" \
"Studio product photograph: Motilli bottle standing upright slightly tilted, with about 12 dark-green heart-shaped gummies poured out and scattered on a clean white surface around the base of the bottle. One fresh celery stalk laid diagonally beside the gummies. Soft diffused studio lighting. Editorial supplement product photography. Square 1:1."

submit_img_ref "p4" "gpt_image_2" \
"Extreme macro close-up product photograph: the Motilli bottle label fills most of the frame, focused tightly on the wordmark and CELERY JUICE FIBER GUMMIES tagline. Crisp, sharp, every printed detail legible. Lime green label color saturated. Subtle gradient blur on the edges of the bottle curve. White background visible at edges. Square 1:1."

submit_img_ref "p5" "gpt_image_2" \
"Product photograph: a woman's hand (40s, natural skin, neat neutral manicure) holding the Motilli bottle upright at chest level. Only the hand and bottle visible — no face or body. Plain bright white seamless background. Soft even studio light. Bottle label clearly readable. Square 1:1."

submit_img_ref "p6" "gpt_image_2" \
"Lifestyle product photograph: the Motilli bottle on a clean modern kitchen counter (white marble), with two fresh celery stalks lying flat beside it and two green apple slices showing fresh white flesh. Soft natural morning light from a window on the left. Bright, airy, fresh, healthy mood. Bottle label sharp and readable. Square 1:1."

# ============ CUSTOMER PORTRAITS ============
P_STYLE="Natural candid headshot, friendly genuine smile, warm soft lighting, neutral softly-blurred background. Mid-close framing from shoulders up. Looks like a real verified buyer review photo — not stock, not glamorous, slightly imperfect, authentic. Direct gentle eye contact with camera. Square 1:1."

submit_img "r1-sarah" "nano_banana_2" "Portrait of Sarah, a 42-year-old white American woman with shoulder-length brunette hair softly waved, light makeup, wearing a simple navy blouse. Friendly genuine warm smile showing teeth. ${P_STYLE}"
submit_img "r2-michelle" "nano_banana_2" "Portrait of Michelle, a 45-year-old Asian-American woman with short straight dark hair to her chin, dark-framed glasses, wearing a soft grey sweater. Slight closed-mouth smile, warm and intelligent. ${P_STYLE}"
submit_img "r3-lisa" "nano_banana_2" "Portrait of Lisa, a 51-year-old white American woman with a chin-length blonde bob, light freckles, wearing a coral pink top. Mid-laugh expression, joyful warm crinkled eyes. ${P_STYLE}"
submit_img "r4-christina" "nano_banana_2" "Portrait of Christina, a 38-year-old Latina woman with shoulder-length dark curly hair, warm olive skin, gold hoop earrings, casual cream knit top. Soft friendly smile. ${P_STYLE}"
submit_img "r5-jessica" "nano_banana_2" "Portrait of Jessica, a 46-year-old Black woman with natural shoulder-length curls, warm brown skin, gold stud earrings, wearing a mustard yellow blouse. Gentle soft smile, calm confident expression. ${P_STYLE}"
submit_img "r6-amanda" "nano_banana_2" "Portrait of Amanda, a 41-year-old white American woman with auburn-red hair past her shoulders, visible light freckles, wearing a denim jacket over a white tee. Candid open-mouth laugh, head slightly tilted. ${P_STYLE}"
submit_img "r7-heather" "nano_banana_2" "Portrait of Heather, a 49-year-old white American woman with medium brown hair tied back in a low ponytail, fair skin with light age lines around her eyes, wearing a soft olive green cardigan. Warm closed-mouth smile, kind expression. ${P_STYLE}"
submit_img "r8-rachel" "nano_banana_2" "Portrait of Rachel, a 50-year-old mixed-race woman (Black and white heritage), wavy dark brown hair past her shoulders, light brown skin, small silver hoop earrings, wearing a soft burgundy sweater. Gentle closed-mouth smile. ${P_STYLE}"
submit_img "r9-nicole" "nano_banana_2" "Portrait of Nicole, a 44-year-old white American woman with straight blonde hair past her shoulders, fair skin, light makeup, wearing a simple charcoal grey top. Soft warm closed-mouth smile. ${P_STYLE}"
submit_img "r10-theresa" "nano_banana_2" "Portrait of Theresa, a 52-year-old Latina woman with shoulder-length salt-and-pepper hair (more salt than pepper), warm olive-tan skin with natural age lines, wearing a navy blazer over a white shirt. Confident closed-mouth smile, strong eye contact. ${P_STYLE}"
submit_img "r11-jennifer" "nano_banana_2" "Portrait of Jennifer, a 47-year-old Asian-American woman with straight dark brown hair just past her shoulders, warm tan skin, simple gold necklace, wearing a soft blush pink blouse. Friendly warm smile showing teeth. ${P_STYLE}"

# ============ DOCTORS ============
submit_img "dr-marsh" "nano_banana_2" \
"Professional medical portrait: Dr. Rebecca Marsh, a 50-year-old white American woman gastroenterologist. Shoulder-length light-brown hair, slight natural age lines, wearing a crisp clean white lab coat with a stethoscope draped around her neck. Softly-blurred modern medical clinic background, light beige wall. Warm professional slight closed-mouth confident smile, direct eye contact. Bright clean medical-office lighting. Square 1:1."

submit_img "dr-chen" "nano_banana_2" \
"Professional medical portrait: Dr. Sarah Chen, a 45-year-old Asian-American woman internal medicine physician. Shoulder-length straight dark hair, fair skin, subtle dark-framed glasses, wearing a crisp clean white lab coat over a soft blue shirt. Softly-blurred modern medical office background. Warm professional calm closed-mouth smile, gentle direct eye contact. Bright clean medical-office lighting. Square 1:1."

# ============ BEFORE/AFTER ============
submit_img_ref "ba1-cabinet" "gpt_image_2" \
"Split-screen composition divided by a thin vertical line down the middle. LEFT half labeled BEFORE: a cluttered bathroom shelf overflowing with many generic laxative boxes (white/blue boxes), fiber powder canisters, magnesium bottles, stool softener packs — chaotic, too many products, generic plain labels with no real brand logos. RIGHT half labeled AFTER: a clean minimalist white bathroom shelf with just ONE bottle — the Motilli bottle (clear jar, lime-green wraparound label, white cap, dark green heart-shaped gummies). Bold black-rectangle banner across the top of each half with sharp white sans-serif text — 'BEFORE' on the left half and 'AFTER' on the right half. Clean photographic style, even lighting both sides. Square 1:1."

submit_img_ref "ba2-gas-relief" "gpt_image_2" \
"Split-screen composition divided by a thin vertical line down the middle. LEFT half labeled BEFORE: a cluttered shelf with many generic gas-relief and antacid products (white and pink boxes, chalky tablet bottles, generic antacid packs, anti-gas softgels) — overwhelming clutter, generic plain labels with no real brand logos. RIGHT half labeled AFTER: a clean simple shelf with just ONE Motilli bottle (clear jar, lime-green label, white cap, dark green heart-shaped gummies). Bold black-rectangle banners across the top with white sans-serif 'BEFORE' on left and 'AFTER' on right. Even photographic lighting. Square 1:1."

submit_img "ba3-belly" "gpt_image_2" \
"Split-screen composition divided by a thin vertical line down the middle. Photograph of a woman's torso only — no face, no head visible (cropped from collarbone down to hips). She wears a grey sports bra and dark navy leggings with waistband visible. Soft neutral cream bedroom background. LEFT half labeled BEFORE: the abdomen is distended and bloated, her hands resting on her belly showing the puffiness. RIGHT half labeled AFTER: same exact framing and outfit but the abdomen appears flatter and more relaxed, hands resting comfortably. Bold black-rectangle banners across the top with white sans-serif 'BEFORE' on left and 'AFTER' on right. Realistic photographic style, even soft lighting both sides. Square 1:1."

# ============ MECHANISM DIAGRAM ============
submit_img "diagram-highway" "gpt_image_2" \
"Clean modern editorial flat-vector illustration on a pale lime-tinted off-white background. Centered composition: a stylized human digestive tract simplified into a vertical highway diagram. At the TOP: a stylized stomach shape in lime green, with a bold red-orange arrow pointing into it and a clear label in dark grey sans-serif reading exactly: UPSTREAM - Problem starts HERE. Below the stomach: a connecting vertical lime-green highway road with dashed lane markings flowing downward. At the BOTTOM: a stylized colon/intestine loop in muted grey, with a red strikethrough X drawn across it, labeled in dark grey sans-serif reading exactly: DOWNSTREAM - Laxatives target HERE. Limited palette of lime green, charcoal grey, red-orange accent, and white. Modern infographic style. ALL TEXT MUST BE PERFECTLY LEGIBLE WITH CORRECT SPELLING. Square 1:1."

wait
echo "All jobs submitted."
ls jobs/*.json | wc -l

# Organic B-Roll Research: Colette Wool Tote (Velantra)

Built 2026-09-02 for the 100-clip organic B-roll library. Source of truth for the product was the supplied product images only (canonical 3/4 hero, front, side, interior top-down, Espresso hero, one on-model still). No PDP or spec sheet was used for generation.

## 1. Product analysis (from the images)

See `product_visual_reference_model.md` in this folder for the full breakdown. The short version that every prompt carried:

- East-west brushed wool felt tote, oatmeal-greige, about twice as wide as tall, softly structured, flat base, stands on its own.
- Two wide vertical felt straps on each face that run up into two rolled top handles; the handle grip is leather-wrapped, the lower part of the loop is felt. Short drop: hand or forearm carry only.
- One slim leather belt crossing each face through a felt loop on each strap, both ends curving outward and downward, each tipped with a round aged-gold disc cap.
- Open top, no flap, no zipper; a single small felt tab with a gold snap stud at the top centre of the inner rim, front and back.
- Clean felt side gussets with one vertical centre seam, nothing attached.
- Two colourways that differ only in the trim: Caramel (cognac tan) and Espresso (dark brown). Body identical.
- No logo, embossing, plaque or lettering anywhere.

## 2. Product uncertainties (kept out of every shot)

- Interior pockets, sleeves or dividers: not visible, so no organised-interior shots; contents sit directly on felt.
- Whether the belt is functional: it has no buckle, so it is never adjusted, unbuckled or tied.
- The base underside and the fully empty slouched bag: never shown.
- Shoulder carry: the drop is short and no reference shows it, so it was never staged.
- The back face: assumed identical to the front (symmetric construction); one back-view shot uses that assumption.

## 3. Apify research methodology

- Actor: `clockworks/free-tiktok-scraper` via the Apify REST API, async runs, 5 queries per run, 40 results per query.
- 40 search queries derived from the product's visual class (soft wool/felt carry-all, leather trim, quiet-luxury register, fall): handbag, leather handbag, everyday handbag, quiet luxury bag, tote bag, work tote bag, tote bag outfit, what's in my bag, whats in my bag tote, bag review, handbag unboxing, purse collection, grwm handbag, handbag styling, bag close up, bag details, handbag recommendation, fall bag, fall handbag, wool tote, felt tote bag, suede tote bag, big tote bag, everything bag, carry all tote, old money bag, loro piana tote, bag haul, new bag, bag that fits laptop, mom bag tote, airport tote bag, packing my bag, bag in car, mirror outfit check bag, cafe tote bag, shoulder tote outfit, designer inspired bag, purse, handbag outfit.
- Dataset: 1,600 raw results, 1,481 unique videos, saved with URL, creator, caption, hashtags, views, likes, comments, shares, duration, publish date and thumbnail in `tiktok_reference_dataset.csv`.
- Download selection: 180 videos, 4 to 120 seconds, no ads, no slideshows, round-robin across queries with a light shuffle so the sample was not only the viral tail. All 180 downloaded with yt-dlp into `videos/`, six-frame contact sheets in `frames/`.
- Gemini watched every one of the 180 videos in full (the video file, not the caption) and returned a structured per-shot breakdown: camera height, angle, distance, movement, product orientation, interaction, environment, lighting, face visibility, mirror use, phone-realism cues, transitions and the first-two-second hook. Per-video JSON in `gemini_analysis.jsonl`, aggregate in `pattern_stats.json`.
- Relevant videos (a bag physically on screen for a meaningful stretch): 166 of 180. Shots tagged: 1,168. 165 of 166 read as creator-shot rather than brand production.

## 4. Organic B-roll patterns (the visual grammar)

The category is filmed at home, at chest height, front-on, handheld, in window light, with the bag shown to camera, opened or packed. Street, car and café footage is rare. Nobody films the bag like a product shot; they film what they were already doing with it.

Shot frequency across 1,168 shots (166 videos):

| Dimension | Distribution |
|---|---|
| Camera height | chest 37%, eye 27%, waist 21%, top-down 9%, overhead 4%, high angle 2%, floor 1%, low angle under 1% |
| Camera angle | front 67%, top-down 14%, POV 12%, three-quarter 4%, side profile 2%, behind subject 1% |
| Distance | medium 42%, close-up 33%, full product 13%, full body 7%, environmental wide 2%, macro plus extreme close-up 2% |
| Movement | handheld 52%, natural hand movement 24%, static 19%, mirror filming 2%, walking camera 1%, tracking 1%, pan 1% |
| Product orientation | front 48%, interior 13%, not visible 12%, three-quarter 9%, open 8%, top 5%, back 2%, side 1% |
| Interaction | showing to camera 22%, none 17%, packing items 10%, opening 7%, carrying on shoulder 6%, holding handles 6%, removing items 4%, touching material 4%, carrying in hand 3%, picking up 3% |
| Environment | bedroom 27%, living room 18%, other apartment rooms 17%, store 6%, office 4%, closet 4%, kitchen 4%, hallway 3%, hotel 2%, café 2%, car 2%, sidewalk 1% |
| Lighting | window light 49%, warm indoor 28%, cool indoor 11%, overcast daylight 4%, studio 3%, ring light 2%, mixed 2%, direct sun 1% |
| Face | none 48%, full 43%, partial 6%, cropped 2%, hidden by phone 1% |

Video-level flags (share of the 166 relevant videos):

- Interior or open bag shown: 57%
- Burned-in text overlays: 54%
- Mirror footage: 9%
- Walking footage: 9%
- Car footage: 4%
- Human present: 96%

Content formats: review to camera 22%, what's in my bag 18%, unboxing 12%, packing 10%, collection tour 6%, outfit check 5%, haul 4%, styling several outfits 3%, comparison 3%.

First-two-second hooks that recur: the creator already holding the bag up at chest height in a bedroom or living room; a hand picking the bag up off a bed or sofa; a top-down look into an open bag full of essentials; a bag placed on a chair or bed with the creator entering; the bag on a passenger seat.

Transitions: 88% hard cuts. Zoom cuts 5%. Whip pans, hand-over-lens, walk-in and walk-out are each around 1%.

## 5. Camera behaviour that reads as phone-shot

Cues Gemini actually saw, share of relevant videos: hand shake 81%, off-centre framing 46%, reframing mid-shot 44%, exposure shift 43%, motion blur 30%, autofocus hunting 25%, subject leaving frame 7%, awkward composition 5%, imperfect move start or end 5%, blown window 5%.

The practical translation used in every prompt and motion prompt: one available light source, slightly blown highlights near a window, sensor noise in the shadows, phone sharpening, focus that is not tack sharp, a trace of motion blur, a crooked and off-centre frame, and a small handheld sway with a soft refocus in the animation. Faces stay out of frame or behind the phone, which is also the single most common convention in the category (48% of shots show no face).

## 6. Environments

Home dominates: bedroom, living room and other apartment rooms together are 62% of shots. Closet, kitchen and hallway add 11%. Store footage (6%) is almost all try-on and unboxing content. Office, café, car and sidewalk are each 4% or less, which makes them the shots that stand out in a feed.

Placement follows what a real owner does: bed, sofa cushion, chair seat or chair back, kitchen counter, entry bench, closet shelf, passenger seat, lap. Never a public floor.

## 7. Product interactions

The dominant interaction is simply showing the bag to camera (22%), then packing (10%), opening (7%), holding the handles (6%), removing items (4%) and touching the material (4%). Combined, open-bag behaviour (opening, packing, removing, reaching in) is over a fifth of all shots and appears in 57% of videos, which is why 20 of the 100 clips involve the open bag even though the interior of this product is plain felt.

## 8. Creative opportunities (uncommon shots worth testing)

- Low-angle and floor-level framing: under 1% of the category. COL-006 tests it.
- True side profile and back view: 3% combined. COL-002, COL-003, COL-015, COL-032, COL-096.
- Car footage: 4% of videos. Six clips (COL-074 to COL-079).
- Sidewalk and café: 1% and 2%. Ten clips across 04_Carrying, 06_Outfits and 10_Work_Cafe.
- Set-down and hand-enters-frame transitions: about 1% each. COL-098 to COL-100.
- Texture macros: 2% of shots. Ten Details clips, all locked-off push-ins so hardware cannot drift.

## 9. Avoid (what makes footage read as an AI ad)

- Perfectly centred product, clean backdrop, even studio light, gimbal-smooth moves: none of the 166 organic videos look like this.
- A face that is fully visible and synthetic. The category hides the face half the time anyway; every clip here keeps the face out of frame, behind a phone, or turned away, and the three Omni clips that revealed a face were replaced.
- Belts that tie themselves into bows, extra discs, extra handles, engraved lettering on props: the drift signatures found in Omni output and the reason product-only beats are locked-off push-ins from the approved keyframe.
- A boxy or square bag: the most common GPT Image 2 error on this product, fixed by stating the dimensions in every prompt and re-rolling the four frames that came out upright.
- Any on-screen text, caption, UI or watermark: zero in the library by construction.
- Groceries or implausible loads: contents are limited to what the avatar carries (laptop, knit, water bottle, wallet, keys, notebook, AirPods, sunglasses, lip balm).

## 10. Pipeline used

Product images → Apify TikTok crawl (1,481 videos) → Gemini video analysis (180 watched) → pattern stats → 100-shot manifest (`scripts/manifest.py`) → GPT Image 2 image-to-image keyframes on Higgsfield with the six product references attached (one variant, re-rolled on structural failure; 14 re-rolls in total) → Gemini structural keyframe gate plus full-resolution human review → Omni image-to-video for human-interaction shots (Omni 1.1 Flash from clip 70 onward per Brooks's 2026-09-02 rule) with one re-roll budget, locked-off handheld push-ins from the approved keyframe for product-only beats and for any interaction clip that drifted twice or revealed a face → four-point drift strips reviewed by hand with a usable in/out window per clip → trim to the window → Gemini 3.7 Flash clip QA on the delivered file → `BROLL_LIBRARY/` plus `broll_manifest.csv`.

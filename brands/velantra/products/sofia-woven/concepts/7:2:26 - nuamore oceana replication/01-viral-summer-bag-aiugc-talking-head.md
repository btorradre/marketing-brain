# EDITOR BRIEF 01 — "The Viral Summer Bag" (AIUGC Talking Head)

**Brand:** Velantra · **Product:** Straw Tote ($119.99, hand-woven seagrass, limited quantities)
**Reference:** Nuamore Oceana Ad #1 (FB 1286034803011009) — `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/references/nuamore-ad1-viral-celebrity-1286034803011009.mp4`
**Format:** 9:16, 720x1280+, ~31s · **Angle:** Viral social proof ("this bag is everywhere")
**Date:** 2026-07-02

## Production routing
- **Talking head:** HeyGen AIUGC avatar — **Caroline Nutt** (our actual trained avatar; source footage at `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/_shared/ugc-creators/Caroline Nutt/`) — greenscreen, keyed and pinned bottom-left corner (~35% frame width), running IN FRONT of full-screen B-roll for the entire ad. Casual summer outfit, direct-to-camera, natural energy.
- **Voice:** use the **"Women over 40" voice** in HeyGen for Caroline's read — do NOT use a younger-sounding default; delivery should read as a woman 40+, warm and conversational.
- **All B-roll:** Google Omni — single hybrid image+video prompts (scene + motion + camera + audio in one generation; no separate keyframe→animate step).
- **Product grounding:** every product-visible shot MUST attach a canonical reference image (i2i) — never generate the bag from text alone.
  - Hero ref: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png`
  - Secondary: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw tote 1.webp`, `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/blue 1.png`, `black-colorway/`
- **Captions:** bold white sans-serif, center-frame, 2 lines max, word-grouped (match Nuamore reference).
- **Compliance:** NO celebrity names/faces (Nuamore uses Hailey/Beckham paparazzi shots — we swap to anonymous street-style/"spotted" shots). No origin claims (never "made in USA/Italy/EU").

## Avatar image generation (HeyGen source image)
Generate the greenscreen still HeyGen animates. i2i, identity locked to `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/_shared/ugc-creators/Caroline Nutt/caroline-ref-still.jpg`.
**Image prompt** *(Nano Banana 2 / GPT Image, attach the reference still)*
> IMAGE-TO-IMAGE — attach reference: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/_shared/ugc-creators/Caroline Nutt/caroline-ref-still.jpg. Keep her identity EXACTLY as the reference: same face, warm eyes, long honey-blonde hair with lighter face-framing highlights worn down, gold huggie earrings, layered gold necklaces with a multicolor beaded necklace, natural glossy makeup, light pink manicure. Generate: waist-up UGC-style portrait, direct eye contact with camera, warm mid-speech expression with a slight smile, wearing a white sleeveless summer dress (matches her real footage). Standing against a SOLID CHROMA-KEY GREEN background — flat #00B140, evenly lit, zero shadows, nothing else in frame. Soft natural front light on her face, iPhone front-camera realism, slight skin texture, 9:16 vertical, photoreal. No text, no captions, no logos, no props.

## Script (HeyGen avatar VO — ~31s)
1. "Okay, so I kept seeing this bag all over my feed."
2. "First on TikTok, then every street-style page I follow posted it too,"
3. "and I thought — alright, what's the hype?"
4. "It's called the Velantra Straw Tote, and honestly, I get it now."
5. "It's structured, it's hand-woven, it looks like a two-thousand-dollar bag — but it's not."
6. "Real leather trim, fits your whole day, made for actual summer."
7. "And right now it's on sale, which is wild — because this thing keeps selling out."
8. "It's been sold out multiple times. This is the first time I've seen it actually in stock."
9. "So if you're thinking about it — don't. Just grab it."

## Timeline + B-roll asset prompts

### SHOT 1 — Street-style "spotted" candid #1 (0:00–0:05 · lines 1–2)
Full-screen behind avatar. The "I keep seeing this" evidence layer.
**Google Omni hybrid prompt** *(attach ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png)*
> IMAGE: Candid paparazzi-style photo brought to life — a stylish woman in her late 20s, oversized black sunglasses, gold hoops, black sleeveless top and white wide-leg trousers, sitting at a sidewalk café table, iced coffee in hand. The exact handbag from the reference image — a structured Birkin-style tote in hand-woven natural seagrass with visible whipstitch cross-lacing on the edges, smooth taupe leather top flap with white contrast stitching, two rolled taupe leather handles, crossed leather belt straps at the front, no visible logo — sits on the table beside her, clearly the focal point. Long-lens paparazzi compression, slight foreground obstruction (blurred railing edge), harsh midday sunlight, authentic street-photography color. MOTION: subtle live-photo movement — she lifts the coffee for a sip, hair moves in light breeze, pedestrians pass blurred in background. CAMERA: long telephoto, slow 4% push-in, faint handheld jitter and rolling-shutter wobble like a zoomed phone video. AUDIO: distant street ambience, traffic, café chatter. 5 seconds, 9:16 vertical, photoreal, keep the bag EXACTLY as in the reference — weave texture, taupe leather flap, crossed straps unchanged.

### SHOT 2 — Street-style "spotted" candid #2 (0:05–0:09 · line 3)
**Google Omni hybrid prompt** *(attach ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw tote 1.webp)*
> IMAGE: A second candid street-style photo come to life — different woman, 30s, slicked-back bun, flowy cream linen midi dress, crossing a city crosswalk at golden hour, carrying the exact handbag from the reference image in the crook of her elbow: structured hand-woven natural seagrass tote, taupe leather top flap with white stitching, rolled taupe leather handles, crossed front belt straps, no logo. Shot from across the street, long-lens, other pedestrians softly blurred, warm golden-hour glare. MOTION: she walks three steps mid-crossing, dress flows, bag swings gently at her elbow, cars pass blurred behind. CAMERA: telephoto, slight pan tracking her walk, organic handheld drift, mild focus hunt at the start like a phone zoom clip. AUDIO: city ambience, footsteps, distant horns. 4 seconds, 9:16, photoreal street photography, bag identical to reference.

### SHOT 3 — Coastal editorial (0:09–0:15 · lines 4–5)
The "I get it now" glow-up beat — mirror Nuamore's beach model shots.
**Google Omni hybrid prompt** *(attach ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png)*
> IMAGE: Polished summer editorial — a sun-kissed model in a black off-shoulder swimsuit and gold jewelry stands on a bright beach, turquoise ocean and white surf behind her, holding the exact handbag from the reference image by both rolled taupe leather handles at hip height: structured hand-woven natural seagrass tote with whipstitch edge lacing, taupe leather flap with white contrast stitching, crossed leather belt straps, no logo. Skin glistening, vivid blue sky, high-end resort-campaign lighting. MOTION: she slowly turns her torso toward the sun, chin lifting, breeze moves loose hair strands, waves roll behind, the bag stays crisp and steady in frame. CAMERA: slow vertical tilt-up from bag to face, shallow depth of field, gentle organic sway. AUDIO: waves, seagulls, soft breeze. 6 seconds, 9:16, photoreal luxury campaign grade, bag EXACTLY as reference.

### SHOT 4 — Product macro (0:15–0:19 · line 6)
Pure product credibility beat. STRICT i2i — texture fidelity is the whole shot.
**Google Omni hybrid prompt** *(attach refs: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png + /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw birkin opened.png)*
> IMAGE: Extreme macro close-up of the exact handbag from the reference images — fill the frame with the hand-woven natural seagrass weave, the whipstitch cross-lacing along the edge, and the smooth taupe leather flap with its white contrast stitching. A woman's hand with a neutral manicure slowly brushes across the weave and grips the rolled leather handle. Soft window light, warm neutral backdrop, ultra-sharp fiber-level texture detail. MOTION: fingertips glide over the weave, then lift the leather strap slightly to show its thickness; light shifts subtly across the texture. CAMERA: macro lens, slow 6% pull-back revealing the flap and crossed straps, micro handheld tremble. AUDIO: soft fabric/straw brushing sounds, quiet room tone. 4 seconds, 9:16, photoreal, weave pattern and hardware IDENTICAL to reference — do not invent extra buckles, logos, or zippers.

### SHOT 5 — "Fits your whole day" lifestyle utility (0:19–0:24 · line 7)
**Google Omni hybrid prompt** *(attach ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw birkin opened.png)*
> IMAGE: Overhead-angled poolside scene — the exact handbag from the reference image sits open on a sun lounger: structured hand-woven seagrass tote, taupe leather flap folded open showing the interior. A woman's hands place summer essentials inside one by one: rolled white towel, sunscreen bottle, paperback book, sunglasses case. Bright poolside light, water sparkling out of focus behind. MOTION: hands drop items in naturally, bag flexes slightly but holds its structure, water shimmers in the background. CAMERA: high three-quarter angle, slight slow orbit, casual handheld feel like a friend filming. AUDIO: pool ambience, item rustle, distant splash. 5 seconds, 9:16, photoreal, bag structure and interior consistent with reference.

### SHOT 6 — PDP screen-scroll close (0:24–0:31 · lines 8–9)
**NOT generated.** Editor: capture a real screen recording of the velantrafashion.com Straw Tote PDP — gallery swipe → feature callouts (hand-woven seagrass / leather trim / 2-year warranty) → reviews → price + LOW STOCK/sale badge. Match Nuamore's phone-frame scroll pacing: 2 scroll moves + 1 gallery swipe. Overlay caption follows script lines 8–9.

## Assembly notes
- HeyGen avatar layer runs full duration; B-roll swaps behind it on the beat boundaries above.
- Hard cuts only, no transitions (per house style).
- Captions on every line; keep them clear of the avatar's head.
- End card optional: Velantra wordmark + "Selling out — velantrafashion.com."
- Offer line: script says "on sale" — editor confirms live offer/discount before adding any % claim.

## Asset manifest
| # | Asset | Source | Duration |
|---|---|---|---|
| 1 | Street candid café | Omni (ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png) | 5s |
| 2 | Street candid crosswalk | Omni (ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw tote 1.webp) | 4s |
| 3 | Beach editorial | Omni (ref: /Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png) | 6s |
| 4 | Product macro | Omni (refs: caramel 1 + opened) | 4s |
| 5 | Poolside packing | Omni (ref: opened) | 5s |
| 6 | PDP screen recording | Editor capture | 7s |
| 7 | Talking head | HeyGen greenscreen, full 31s | 31s |

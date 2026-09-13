# ORE-PILL-SWALLOW-UGC-01 — Brief

**Status:** APPROVED + PRODUCED (2026-07-18 → 07-21). See §9 Run log.

## 1. Header

- **Concept:** Pre-launch survey-flow UGC. One script, five creators (women 30–40, cast from Brooks's 5 Pinterest references). Educates the prospect on what Orelli is — Tylenol-in-a-gummy for adults who hate swallowing pills — and drives to the willingness-to-pay survey.
- **Angle:** literally just "Tylenol in a gummy." No mechanism chains, no science. Her mechanism is one line: "I used to struggle swallowing pills until this."
- **Reference:** no reference ad (original concept from Brooks's directive, 2026-07-18). The 5 attached Pinterest images are CASTING references only — beat map is built from the directive, ad-watcher step waived.
- **Pipeline:** Seedance 2.0 via kie.ai, `std` mode, 9:16, 720p. Chained segments, seg-1 native audio = voice anchor.
- **Runtime:** ~25s per ad = 2 segments (15s + 10s) — Brooks's "segment and a half."
- **Output:** 5 finished ads → `products/orelli/concepts/7:18:26 - pill-swallow-survey/` on completion.
- **Cost estimate (no silent spend):** ~41 cr/sec at 720p. 5 ads × 25s = 5,125 cr. Seg-1 casting call (3 takes, creator 1 only) ≈ 1,230 cr. Retake buffer ≈ 2,000 cr. **Total ≈ 8,000–8,500 kie credits.**
- **Congruence flag:** RESOLVED 2026-07-18 — WTP survey LIVE at **https://orelli-survey.vercel.app** (5-question yes-ladder, Brooks-approved). Per-creator attribution via `?c=<name>` (e.g. `?c=dana`). Responses → Notion DB "Orelli — WTP Survey Responses" (Velantra workspace). Source: `brands/Orelli/survey/`.

## 2. Beat map (directive → ad)

| Beat | Execution |
|---|---|
| Hook (callout) | "If you struggle to swallow pills, watch this." — no product visible |
| Agitation | Headache moment, pill sticks, gag, gives up and takes the pain |
| Mechanism (one line) | "I used to struggle swallowing pills until this." — bottle enters frame HERE, first product moment |
| Educate / position | "It's called Orelli, it's basically chewable Tylenol. You just chew it." |
| CTA | Tap link → quick survey → first access. Survey gauges willingness to pay |

## 3. Final script — passed ai-copy-blacklist audit 2026-07-18

> If you struggle to swallow pills, watch this. Every single time I get a headache, the worst part is the actual pill. It gets stuck in my throat, I start gagging, and half the time I just give up and take the pain. I used to struggle swallowing pills until this. It's called Orelli, it's basically chewable Tylenol. You just chew it. Tap the link and take the quick survey, it gets you first access.

**75 words ≈ 24s at 3.2 wps. APPROVED BY BROOKS 2026-07-18 (with "chewable" wording).** Audit notes: no false-contrast stacks, no triple short-sentence stacks, no rhetorical transitions, no hedging, no parallel openers across consecutive sentences ("I gag, I chug" pattern rewritten out). Mechanism line delivered clean, no filler on the product name.

**Compliance option (Brooks's call):** primary line is "it's basically Tylenol in a gummy" — comparative brand name-drop as lived experience. Safer alternate if wanted: "it's the same ingredient as Tylenol, in a gummy."

## 4. Avatar keyframe spec

Route: GPT Image 2. If the 5 Pinterest originals get dropped into `reference/casting/`, avatars are built i2i from them; otherwise t2i from the casting sheet below. All 9:16, phone-selfie framing, arm's-length lens, imperfect crop.

**Product-hold keyframe (seg 2, per creator):** pure i2i composite via GPT Image 2, seeded from canonical bottle ref `brands/Orelli/Lustre Documents/Orelli x Lustre/Lustre Deliverables/Bottle Mockups/02-LargerLogo.png` (frosted bottle, indigo ribbed cap, red heart-shaped chews, white label "Orelli / Adult Chewable Acetaminophen / Pain Reliever ⊘ Fever Reducer"). Bottle at chest height, label facing camera. Never generated from scratch.

### Casting sheet (from the 5 Pinterest refs — women 30–40)

1. **Dana — bedroom flannel.** Mid 30s, dark blonde hair with highlights in a low messy bun, loose face-framing strands, blue-green eyes, gold hoop earrings, brown and navy plaid flannel shacket. Cozy bedroom behind her, unmade bed, white blinds, warm table lamps. Evening wind-down vibe.
2. **Mel — gym ponytail.** Early 30s, brunette high messy ponytail with a pink scrunchie, post-workout glow, no makeup, black v-neck tank, thin gold necklace. Commercial ceiling tile and door behind her, slightly low selfie angle. On-the-go vibe.
3. **Carly — slow morning.** Late 30s, long wavy brunette hair, bare-faced, small silver initial necklace, orange and pink printed satin shirt. Blue upholstered chair, soft morning window light. Seg 1 she cradles a white coffee mug, mug set down out of frame before seg 2 so hands are free for the bottle.
4. **Nina — car glam.** Mid 30s, dark brunette shoulder-length blowout with face-framing layers, full glam, glossy berry lips, cream knit cardigan, layered gold necklaces. Parked car interior, daylight through the sunroof. Errand-run story-time vibe.
5. **Erin — cabin kitchen.** Early 30s, light brunette hair pulled back in a braided updo, soft pink eye makeup, small nose stud, crystal heart necklace, grey knit cardigan over a black top. Warm cabin kitchen behind her, globe pendant light. Homey chat vibe.

Note: SOP's "never clone the reference creator" applies to reference ADS — these are supplied casting refs per Brooks's explicit direction, so 1:1 likeness is intended.

## 5. Segment map — SIMPLE format

Base register (restated verbatim in every prompt): **warm american mid 30s ugc tone, venting to a friend but animated.** Energy holds through the final word. Image input: creator avatar keyframe on seg 1, product-hold keyframe on seg 2. Seg 2 anchors to seg 1's audio.

### Segment 1 — 15s — no product — 45 words (3.0 wps)

```
natural and realistic arm movements, talks with her hands, touches her throat on the gagging line, subtle lean toward the lens, looks directly at the lens the whole time
she says in a warm american mid 30s ugc tone, venting to a friend but animated:
"If you struggle to swallow pills, watch this. Okay so every single time I get a headache, the worst part is the actual pill. It gets stuck in my throat, I start gagging, and half the time I just give up and take the pain."
Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage, expressive ugc movements, UGC aesthetic. Vertical 9:16. NO PRODUCT IN HAND. ONE CONTINUOUS SHOT
```

### Segment 2 — 10s — product in hand — 32 words (3.2 wps)

```
raises the Orelli bottle to chest height with the label facing the camera, gives it one small shake, warm smile building through the last line, looks directly at the lens the whole time
she says in a warm american mid 30s ugc tone, bright with relief:
"I used to struggle swallowing pills until this. It's called Orelli, it's basically chewable Tylenol. You just chew it. Tap the link and take the quick survey, it gets you first access."
Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage, expressive ugc movements, UGC aesthetic. Vertical 9:16. PRODUCT IN HAND, LABEL FACING CAMERA, LABEL TEXT UNCHANGED. ONE CONTINUOUS SHOT
```

Per-creator variation: ONLY the setting/wardrobe context implied by the seed image changes. Movement, voice line, dialogue, and footer stay identical across all 5. Carly's seg-1 movement line swaps hand cues for the mug ("cradles her coffee mug, sets it down out of frame on the last line").

## 6. Post / captions

- Word-by-word captions, heavy white sans, center-low. Single accent color: Orelli cobalt blue (fallback A/B: tangerine). Emphasis words: **swallow pills**, **chewable**, **survey**.
- Hook overlay seg 1 first 2s: "if you struggle to swallow pills 🫠" — overlay in post, not baked in (Seedance text spelling risk).
- No music — ambient room tone only, native audio.
- End card (last 1.5s, post): bottle shot + "Take the 30 second survey" + link sticker area.

## 7. QA gates before spend

1. Seg-1 casting call: 3 takes on creator 1 (Dana), pick the most alive; if all flat → ElevenLabs `--audio` fallback.
2. Voice consistency seg 1 → seg 2 per creator; seg 2 always anchors to seg 1 audio.
3. Identity side-by-side: avatar keyframe vs seg-2 last frame.
4. Product accuracy vs `02-LargerLogo.png` — label text unchanged, red heart chews, indigo cap (broll-auditor pass on seg 2s).
5. End-of-segment energy check on every clip.
6. Runtime bounds: 24–26s per finished ad.

## 8. Compliance

- Risky claim ("basically chewable Tylenol") lives in lived-experience quoted speech only.
- Acetaminophen 500mg = FDA OTC monograph drug — "pain reliever" is on-label language. No efficacy claims beyond the label, no speed/strength comparisons vs Tylenol.
- Never: "FDA approved" (it's monograph, not approved), dosage claims, kids' use. Adults only.
- This is a pre-launch research ad driving to a survey, not a point-of-sale claim — but write as if it will be screenshotted.

## 9. Run log (production actuals)

- **Pipeline actually used:** velantra-ugc kie runner (`kie_seedance.py`, brand-agnostic) in `ref` mode — the seedance-brief-runner skill's script still shells to the retired Higgsfield CLI. Seg 1: refs=[avatar]. Seg 2: refs=[seg-1 last frame, bottle crop] + `reference_audio_urls`=seg-1 anchor.
- **Casting:** 3 Dana takes, all word-perfect; take 1 won (hottest audio: mean −20.0dB, peak −1.3dB; engaged final frame). Other creators ran single takes — every seg 1 came back word-perfect 8/8 energy (Gemini ear).
- **PRONUNCIATION (Brooks 2026-07-19):** Seedance misreads "Orelli" → spoken dialogue spells it **"Orelly"** (label/visual text keeps real spelling). Validated: all finals say or-RELL-ee.
- **Label micro-text:** full packshot ref garbles label text ~50% of rolls; **tight-crop the bottle (keyframes/bottle_crop.png) — materially better.** Mirrored-label rolls happen (Mel 2×, Nina 1×) even with anti-mirror prompt language; fix = GPT Image 2 composite start frame + chain mode.
- **Voice seam at 15s:** reference-audio anchoring is approximate. Gemini flags a shift on most stitches; Dana/Erin blended clean. Acceptable at a hard cut; regen lottery only helps sometimes.
- **Version picks (SHIPPED 7/21):** dana=v3, mel=v4 (composite chain — chain mode cannot take a voice anchor, API mutual-exclusivity confirmed), carly=v4, nina=v2, erin=v2. Delivered to `brands/Orelli/products/chewable-acetaminophen/concepts/7:21:26 - pill-swallow-survey/` with README (per-creator ?c= survey links). Actual spend ≈ 10,900 kie credits (≈$44) vs 8–8.5k estimate — overage = Brooks-requested pronunciation regen wave + label/mirror re-rolls.
- **kie credit mechanics observed:** pre-auth ≈ face cost (615cr/15s, 410cr/10s must fit current balance); auto top-up trickles ~1,500cr per trigger — sequential retry loops (90s) clear rejections. Failed/rejected tasks never charged.

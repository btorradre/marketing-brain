# AIUGC Infinite — Two-Cut Creator Ad Factory

This document describes a process for producing batches of finished, stitched, vertical (9:16) two-cut UGC-style video ads at scale, from a single brand brief. Each ad has two cuts: Cut 1 is a talking-head creator delivering the hook/script with native voiceover; Cut 2 is a hard-cut to the same creator using or demonstrating the product (an image-to-video action scene seeded from Cut 1's last frame). Use this whenever the goal is "build infinite AIUGC," "AIUGC factory," "two-cut UGC ads at scale," or batch UGC production with a cut to a product-action scene. The pipeline described here uses Higgsfield's Marketing Studio (for the talking-head cut, with native voice generation) and a physically-literal image-to-video model such as Seedance 2.0 (for the product-action cut), stitched together with a video-editing tool (e.g. ffmpeg).

**When NOT to use this approach:** if only a single-cut talking head is needed (no cut to product action), a simpler talking-head pipeline is more appropriate. If replicating one specific reference ad exactly, use an ad-replication process instead of generating N original variations. If the ad is 3D animated / claymation rather than live-action UGC, use an animated-video pipeline instead.

## Core pipeline

```
Brand brief + count N
  |
  v
[1] Generate N two-cut scripts
       Each script = { hook_line, cut1_vo, cut2_visual_prompt }
  |
  v
[2] Resolve assets
       - A product entity registered with the image/video generation service (one-time per brand)
       - An identity-locked "character" reference (optional, for consistency across both cuts)
       - Hook + setting choices (rotated per ad, or fixed/random)
  |
  v
[3] For each script (loop):
       a. Cost preflight — check generation cost before committing credits
       b. CUT 1 — generate a UGC-mode talking-head video with the chosen hook,
          setting, and product, with native audio generation on
          → 5-8s of a creator talking with native voiceover
       c. Download Cut 1, extract its last frame as a still image
       d. CUT 2 — generate an image-to-video clip seeded from that last frame,
          describing the product-action motion (5s duration)
          → 5s image-to-video action scene (creator using the product)
       e. Download Cut 2
       f. Concatenate Cut 1 + Cut 2 into a single final video (hard cut)
  |
  v
[4] Save a manifest recording every asset, prompt, and cost for the batch
```

## How to use this

### Required inputs

Before starting, collect:

1. **Brand** — the brand this batch is for, plus access to that brand's research/voice documents and a hero product image.
2. **Count N** — number of ads to produce in this batch (default 5 if unspecified).
3. **Concept seed (optional)** — an angle, hook style, or copywriting brief. If omitted, pull from the brand's research documents and invent N variations.
4. **Aspect ratio** — 9:16 (default), 1:1, or 16:9.
5. **Cut durations** — Cut 1 defaults to 8s, Cut 2 defaults to 5s.
6. **Identity lock (optional)** — a pinned character/avatar reference for consistency. If omitted, Cut 2 inherits identity from Cut 1's last frame (since it's generated image-to-video from that frame); Cut 1's avatar is whatever the talking-head generator produces for the chosen hook.
7. **Hook/setting strategy** — rotate through a catalog of brand-appropriate hook and setting combinations (default), use one fixed combination for the whole batch, or randomize.

### Step 1 — Generate N two-cut scripts

For each of the N ads, produce a script object:
```json
{
  "id": "ad_001",
  "hook_type_hint": "subtle",
  "setting_hint": "kitchen",
  "cut1_vo": "I tried this celery gummy for 14 days and… (≤8s spoken)",
  "cut2_visual_prompt": "Same woman pops open the green jar at her kitchen counter, takes one heart-shaped gummy, smiles. Soft morning light. Handheld. Subtle eye-focus drift. Background blur, plants, clean kitchen.",
  "rationale": "one-line why this angle works"
}
```

Rules for script generation:
- Cut 1 VO is ≤22 words (roughly 8 seconds of natural speech).
- Cut 1 ends mid-thought, to set up the Cut 2 cut and create pull-through (the viewer keeps watching to see the payoff).
- Cut 2's visual matches Cut 1's avatar and setting for continuity.
- Cut 2 always shows the product physically on screen (drink/hold/open/spread/wear it — a concrete action, not an abstract one).
- Every Cut 2 prompt gets 4 organic imperfection cues bolted on: handheld jitter, rolling shutter wobble, eye-focus drift, ambient background motion (see the "looks real" stack below).

### Step 2 — Resolve assets

- If the brand doesn't yet have a product entity registered with the image/video generation service, set one up first (upload the hero product image, create the product entity) — this only needs to happen once per brand.
- Load a brand-appropriate catalog of hook and setting options to rotate through.
- If an identity-lock reference is supplied or already saved for this brand, use it to keep the avatar consistent.

### Step 3 — Per-ad generation loop

For each script:

1. **Cost preflight.** Before generating, check the estimated cost of the run against the account balance. If the total exceeds a reasonable threshold (e.g. 500 credits) or the balance is less than 1.2× the total estimated cost, stop and confirm with the user before continuing.
2. **Generate Cut 1** — a UGC-mode talking-head video using the hook and setting choices, the product reference, native audio generation enabled, 9:16 aspect ratio, ~8s duration, 720p resolution.
3. **Extract the last frame** of Cut 1 as a still image (a fraction of a second before the very end, to avoid grabbing a motion-blurred final frame) — this becomes the seed image for Cut 2.
4. **Generate Cut 2** — an image-to-video clip seeded from that last frame, using the Cut 2 visual prompt, 9:16, 5s duration, 720p.
5. **Stitch Cut 1 and Cut 2 together** into one final video with a hard cut (concatenate the two clips; normalize their video/audio streams first so the concatenation doesn't glitch).

### Step 4 — Manifest

After every ad, record an entry with: ad id, brand, which hook/setting were used, the product entity id, both generation job ids and their credit costs, file paths for both raw cuts and the final stitched video, the exact prompts used, and a timestamp. Keep this manifest so a batch can be audited, reused, or resumed if interrupted.

## Rules & standards

### Cost discipline

Observed 2026 pricing at 9:16, 720p (may drift over time — always check current pricing before a large batch):
- Cut 1 (talking-head, 8s, UGC mode, native audio on): ~40 credits
- Cut 2 (image-to-video action, 5s, standard mode): ~22 credits
- Per finished two-cut ad: ~62 credits
- Batch of N=10: ~620 credits + a 100-credit buffer = ~720 credits

Ways to reduce cost: shorten Cut 1 to 6s (~25% cheaper); use a faster/cheaper generation mode for Cut 2 (slightly lower visual quality); render at 480p for first-pass iteration and only bump to 720p/1080p on confirmed winners.

### Failure modes and fixes

- **Cut 1 has the wrong avatar / a random face:** train and pin a consistent character/identity reference rather than relying on the default talking-head generator output for each hook.
- **Cut 2's face drifts from Cut 1:** make sure the last-frame extraction grabbed a clean frame, not a motion-blur tail — pull the frame slightly earlier than the very last instant if Cut 1 ends mid-gesture.
- **The hard cut between Cut 1 and Cut 2 feels jarring:** this is intentional for UGC pacing; if softer is wanted, crossfade a short amount of video (~150ms) while leaving the audio hard-cut.
- **Audio cuts off mid-word at the end of Cut 1:** increase Cut 1's duration by ~1s, or trim Cut 1 at its last natural pause using silence detection before stitching.
- **The video generator rejects hook/setting parameters:** those parameters are only valid in UGC talking-head mode — make sure Cut 1 stays in that mode.

## Model-specific prompting reference

The three models used across this kind of production work (an image-generation model for hero/native-image stills, a general-purpose image-to-video model for vibe/lifestyle/talking-head work, and a literal/physical image-to-video model for product-action cuts) each respond to different prompting styles. This reference applies whenever generating images or video for this pipeline or similar UGC ad production.

### Universal cheat-sheet across all three model types

| Lever | Image-gen model (e.g. GPT Image 2) | General i2v model (e.g. Kling 3.0) | Literal/physical i2v model (e.g. Seedance 2.0) |
|---|---|---|---|
| Prompt length | 250–400 words | ≤2 sentences (i2v) | 60–120 words |
| Prompt focus when seeded from an image | Describe CHANGES only | Describe MOTION only | Describe MOTION + identity lock |
| Negative prompts | None — phrase as positive constraints | None — phrase positive | None — append explicit lock + negate phrases |
| Sound | n/a | on/off (native audio, dialogue + SFX) | Native audio always; tag voiceover/ambient |
| Sweet-spot duration | n/a | 5s | 5–6s |
| Sweet-spot resolution | 1024×1536 (9:16) | 720p | 720p |
| Mode tier | low / medium / high | std / pro | fast / std |
| Identity tactic | Re-state PRESERVE every turn | Bind subject + same wording across clips | "maintain exact appearance from reference image, no drift, no morphing" |
| #1 failure | AI sheen / waxy skin | Face morphs at 10s | Face drifts when camera moves |
| #1 fix | Stack 3-5 "looks real" cues | Cap to 5s + higher-fidelity mode | Lock to handheld minimal motion |

### The "looks real" stack (use across all model types)

For images and image-to-video alike, stack 3-5 of these to break the AI-generated look:
- handheld jitter / slight handheld tilt
- rolling shutter wobble
- eye-focus drift
- background motion blur
- 35mm grain / sensor noise
- visible skin pores / faint freckles
- imperfect framing / cropped at the elbow
- unedited RAW look / shot on iPhone
- mid-blink / mid-word expression
- ordinary background detail (half-empty mug, dishtowel)

### The 4-cue rule (for talking-head and UGC product-action clips)

Always append to the motion prompt: *"subtle handheld jitter, rolling shutter wobble, eye-focus drift, ambient background motion"* — this is the documented difference between an AI-rendered look and real phone-camera capture.

### Banned vocabulary (all model types)

These don't help and often hurt: `cinematic`, `epic`, `dramatic`, `stunning`, `beautiful`, `masterpiece`; `8k`, `4k`, `ultra-detailed`, `hyperrealistic` (use specific resolution parameters instead); `trending on artstation`, `award-winning`, `professional`; generic verbs like `moves`, `interacts`, `uses`, `experiences`, `enjoys`; competitor brand names (often rejected by the model as IP); vague mood words — replace with concrete visual facts.

### Order of operations when prompting

1. **Start-frame quality matters more than the prompt.** A garbage seed image produces a garbage output. Spend most of the effort on the seed image.
2. **One concrete physical verb beats five abstract ones.** "She unscrews the cap" beats "She uses the product."
3. **Stop redescribing what's already in the frame.** Describe deltas/motion only when working from a seed image.
4. **Generate cheap/fast first, regenerate winners at higher fidelity.** Don't pay for a quality tier you don't need until a creative concept has proven itself.
5. **Pin every parameter explicitly:** duration, resolution, aspect ratio, mode, sound, genre. Default settings will not match a UGC ad's needs.

### Image-generation model prompting (e.g. GPT Image 2 — for hero/native-image stills)

**Prompt structure (canonical order):** Scene/Setting → Subject → Important details → Use case → Constraints.
- Scene anchors lighting, time of day, surface, background.
- Subject is the literal hero (product, person, pack-shot).
- Important details = material, label copy, pose, hands, expression.
- Use case sets the "mode" — explicitly say "Facebook ad image," "Amazon main image," "9:16 native ad," "editorial pin." The model calibrates polish to it.
- Constraints = a preserve list plus exclusions (the substitute for negative prompts).

**Text rendering (the standout feature of this class of model):**
1. Quote the literal copy: `"DROP 12 LBS BY FRIDAY"`.
2. Mark it `EXACT TEXT:` before the string, and add `verbatim, no extra characters, no duplicate text`.
3. Specify typography separately: font style, weight, case, color, alignment, placement.
4. 1–5 words renders best — headlines crisper than paragraphs.
5. Spell hard brand names letter-by-letter in parentheses on first mention (e.g. "Motilli (M-O-T-I-L-L-I)").
6. Use a higher quality setting for dense or small text.
7. If text drifts wrong, change wording slightly and retry — small tweaks fix legibility faster than re-prompting from scratch.

**Editing / image-to-image mode:**
```
CHANGE: <only what is allowed to move>
PRESERVE: <every locked element — list aggressively>
CONSTRAINTS: no extra objects, no redesign, no relighting
```
- Don't redescribe the subject in detail — label each reference image by index and role ("Image 1 = product; Image 2 = avatar; Image 3 = scene reference") and describe only the delta.
- Repeat the preserve list on every iteration — drift compounds otherwise.
- One change per turn — bundled edits degrade faster than serial single edits.
- Downscale reference images before upload; oversized references cost the same and don't help quality.

**Aspect ratios/resolutions:** 1:1 square → 1024×1024; 9:16 vertical → 1024×1536 (or 1152×2048 for extra detail); 16:9 landscape → 1536×1024; 4:5 Meta feed → 1024×1280. Above ~2560×1440 is experimental — render lower and upscale separately if needed.

**Common failure modes and fixes:**

| Failure | Fix |
|---|---|
| Hand/finger artifacts | Specify the exact hand action explicitly; crop tighter; use higher quality setting |
| Skin "AI sheen" / waxy | Add "realistic non-dewy skin, visible pores, faint freckles, slight under-eye texture, ambient sensor noise, no retouching" |
| Body part distortion | Tighten framing; state pose explicitly; avoid full-body vertical shots with a small product |
| Repeated/duplicate product | "single [item] only, no other [items] in frame, no reflections of the [item]" |
| Watermark hallucination | "no watermark, no stock photo overlay, no signature" |
| Brand/IP refusal | Use generic descriptors instead of a real competitor product name |
| Long prompt degradation | Cap at 250–400 words; move secondary detail to a separate style line |
| Vague mood words produce nothing useful | Replace mood words with concrete visual facts (lighting angle, contrast ratio, shadow direction) |
| Edit drifts the face/logo | Re-state the preserve list verbatim every turn |
| AI-glossy product render | Pass a real product reference photo and write "photographic, not CGI, not render, not 3D — taken on a real camera" |

**Copy-paste templates:**

*Hero product on white:*
```
Scene: pure white seamless studio backdrop, soft top-front key light, faint contact shadow under base.
Subject: [Product] photographed dead-center, label facing camera, perfectly upright.
Details: [material], [color], [label copy verbatim in quotes], no condensation, no props.
Use case: Amazon main image, 1:1.
Constraints: single product only, no extra bottles, no text overlay, no watermark, no reflections, white background pure #FFFFFF.
```

*Lifestyle product-in-hand:*
```
Scene: soft north-window light in a real kitchen, late morning, faint bokeh of a wooden countertop and a coffee mug.
Subject: a 54-year-old woman with shoulder-length grey-blonde hair, smile lines, no makeup, wearing a cream linen top, holding [Product] at chest level, looking down at the bottle.
Details: realistic non-dewy skin with visible pores and faint sun freckles, slight imperfection in framing, shallow depth of field (~f/2.8 feel), 35mm.
Use case: Facebook native ad image, 4:5.
Constraints: shot on iPhone, unedited RAW look, no studio lighting, no AI sheen, no extra fingers, single product only.
```

*Before/after split:*
```
Scene: vertical 9:16 frame split horizontally into two equal panels with a thin black divider.
Top panel: same woman [describe], slumped on couch, dim ambient light, dull skin, EXACT TEXT lower-left: "BEFORE" in bold uppercase sans-serif white.
Bottom panel: same woman, upright, kitchen window light, bright skin, holding [Product]. EXACT TEXT lower-left: "AFTER 14 DAYS" same font.
Constraints: identical face in both panels, same hairstyle, only lighting/posture/expression differ. No extra text. No watermark.
```

*Gummy/pill close-up:*
```
Scene: macro shot, marble countertop, morning side-light from a window.
Subject: three [color] [shape] gummies clustered next to an open [Product] bottle, one gummy resting on the cap.
Details: visible texture on gummy surface, faint sugar dust, shallow depth of field, label copy verbatim "[label text]".
Use case: 1:1 ad image.
Constraints: single bottle, no spilled gummies, no extra props, photographic not CGI.
```

*9:16 native ad with on-image headline:*
```
Scene: candid kitchen, morning, woman 50+ holding [Product], shot from chest height, slight handheld tilt.
Subject as above.
EXACT TEXT, upper-third, centered: "I CANCELLED MY OZEMPIC" — bold uppercase condensed sans-serif, off-white with thin black drop shadow, ~8% frame height. Verbatim. No duplicate text. No subtitle.
Use case: 9:16 Meta Reels static.
Constraints: shot on iPhone look, no studio polish, no watermark, single product, hands intact.
```

**Camera/lens vocabulary that works well:** focal length (35mm, 50mm, 85mm portrait, 24mm wide, 100mm macro); aperture feel (shallow depth of field, f/2.8 bokeh, deep focus); body cues (shot on iPhone/unedited RAW, or named camera bodies); film stock (Portra 400 grain, Kodak Gold 200, 35mm film grain, slight film halation); framing (close-up, medium close-up, eye-level, low angle, over-the-shoulder, flat-lay top-down).

**Lighting vocabulary:** quality (soft diffuse, hard direct, overcast daylight, golden hour, blue hour); direction (key from camera-left, rim from behind, top-front 45°); practicals (kitchen window light north-facing, single ring light reflected in eyes, mixed practical); contrast (3:1 ratio, low-key moody, high-key clean); color temp (warm 3200K tungsten, cool 5600K daylight, mixed warm/cool).

### General image-to-video prompting (e.g. Kling 3.0 — for vibe/lifestyle/fashion/talking-head)

**When a start frame is supplied, the still IS the subject** — the prompt describes motion, not subject. Optimal stack, in order: camera move → primary subject motion → secondary/ambient motion → texture/imperfection cues → end-state (only if the clip stalls).

**Motion vocabulary:** camera verbs that work reliably: dolly in slow, dolly push, pull back, whip-pan, tilt up/down, orbit left, crane up, crash zoom, snap focus, rack focus, shoulder-cam drift, static tripod, handheld follow. Subject motion verbs that work: accelerates, weight transfers to left foot, exhales, tilts head 15° right, lifts product to chest height, rotates jar 90° clockwise, unscrews cap — specific over generic. Words the model ignores or muddles: moves, goes, does something, interacts, looks nice, cinematic.

**Prompt length:** ≤2 sentences is the sweet spot for image-to-video. The model can work great with minimal prompting — add small details only when exact camera or action control is needed.

**Quality tiers:** a faster/cheaper tier is good for concept exploration, A/B testing hooks, scrappy UGC; a higher-fidelity tier is worth it for hero ads, product close-ups, character-heavy shots. Explore cheap, finalize expensive.

**Native audio:** generates dialogue (lip-synced if a face is in frame), SFX synced to motion events, and ambient bed (room tone, wind, traffic) in one pass. Quote dialogue lines exactly. Name action sounds explicitly ("the cap clicks open with a soft pop"). Name the room/ambient sound. Turn sound off only when dubbing a separately-generated voiceover over the top.

**Duration tradeoffs:** 5s gives the highest frame-to-frame consistency, cheapest, best for product shots and hard cuts (default); 6–8s works for medium complexity (one subject + environment interaction); 10s only for simple scenes with one subject and a single clean motion arc — multi-subject 10s clips drift. Rule: 2+ subjects or rapid action → hard-cap at 5–6s and chain clips together in post.

**Aspect ratios:** 9:16, 16:9, 1:1 all supported — feed the model the start frame in the aspect ratio wanted out.

**Start-frame + end-frame mode:** pass both a start and end image for controlled interpolation. Use the same aspect ratio on both frames (mismatch causes stretch/crop); keep style/lighting/color close between them; use a minimal prompt (the two frames already define the arc). For multi-clip sequences, export the last frame of clip N as the start frame of clip N+1 — the cleanest way to fake a longer continuous shot. This breaks when faces rotate more than ~45°, products change orientation, or one frame has motion blur and the other doesn't.

**Identity consistency:** helps to use an explicit "bind subject"/element-reference feature if the platform offers one; use the same start-frame-derived character description (exact wording, not paraphrased) on every clip in a sequence; add negative prompts like "no morphing, no warping, no extra limbs, no face shift"; use 5s clips, not 10s. Breaks with multiple faces in frame, 360° head turns at 10s duration, or re-describing the face differently from clip to clip.

**Failure → fix table:**

| Failure | Fix |
|---|---|
| Face morphs mid-clip | 5s only; use identity-binding feature if available; remove face descriptors; higher-fidelity mode |
| Plastic-skin slow-mo | Add "realistic skin texture, visible pores, natural micro-expression"; avoid "cinematic, dreamy, smooth" |
| AI face wobble on a talking head | Use native audio (sound on) instead of dubbing; keep mouth motion implied, not described |
| Hands warp | Keep hands out of close-up; if in frame, prompt "hands stay still, fingers steady, no gesturing" |
| Product label gibberish | Composite the logo in post instead of fighting it; add "preserve product shape, maintain proportions" |
| Stuck with no motion | Add an end-state, e.g. "…then settles back into original frame" |
| Over-eager floaty motion | Strip the prompt down; rely on the start frame; lower any numerical camera-control values |
| Glossy AI-render feel | Add the 4 organic imperfection cues (below) |

**The 4 organic imperfection cues** (handheld jitter + rolling shutter + eye-focus drift + background motion) map to what every credible guide for this model class recommends under different labels — this is the documented difference between AI render and phone capture. Use it on every UGC clip.

**Talking-head pattern template:**
```
Handheld iPhone selfie video, slight natural sway, rolling shutter wobble,
shallow depth of field, eye-focus drift. The woman speaks: "[line]". Subtle
breathing, micro-blinks, soft daylight from window behind camera. Background
slightly out of focus, faint refrigerator hum.
```

**Product-focused pattern template:**
```
Static tripod with subtle handheld micro-jitter. Steam rises and curls slowly
from the rim. Condensation forms a single drip on the glass. Soft window
light. Background blurred. 35mm grain.
```

### Literal/physical image-to-video prompting (e.g. Seedance 2.0 — for product-action Cut 2)

When a start frame is supplied, stop describing what the image looks like — describe what moves. The canonical structure: subject action → environment motion → camera → lighting cue → style/genre → constraints. For a UGC product-action cut, collapse this to a leaner 4-block: [UGC anchor] + [creator action on product] + [single camera move] + [identity lock + negatives]. Target length: 60–120 words.

UGC anchor (always lead with this to bias toward phone footage rather than cinematic gloss): *"UGC creator, iPhone handheld, harsh midday window light, slightly imperfect framing,"*

**Multi-shot in one generation is usually a bad idea here** — for a UGC action cut, animate one continuous beat off the seed frame and stitch multiple clips together in post instead. Multi-shot generation eats fidelity and undermines the model's identity-lock strength.

**Genre/style parameter:** if the platform exposes a genre bias (auto/action/horror/comedy/noir/drama/epic), use "auto" or "comedy" for UGC work — "action"/"epic" introduce speed-ramps and dramatic push-ins that destroy believability; "drama" adds an unnatural color cast.

**Quality tiers:** a faster/cheaper mode is good enough for ~80% of UGC product-action work — what's lost is mainly some text-on-product fidelity and fine hand articulation. Generate the faster/cheaper tier first, regenerate only the winners at higher fidelity.

**Resolution:** 480p is prototyping-only (faces drift faster); 720p is the production sweet spot for social feed (default); 1080p has diminishing returns — reserve for top-of-funnel polish only.

**Duration:** 5s = one beat (lift bottle to mouth, drink, set down) — best identity retention. 8–10s = two beats — drift starts. 12–15s = multi-shot territory, don't use for a single product-action cut. For a UGC product-action cut: 5–6s, hard rule.

**Audio:** this class of model can generate native synchronized audio — phoneme-level lip-sync, ambient SFX reactive to visuals, optional music bed. Default for a product-action Cut 2: no dialogue, just ambient SFX ("no music, only raw room tone and product SFX, no narration") — this keeps the talking-head cut's voiceover dominant in the final stitched ad.

**Identity consistency from the seed frame:** don't re-describe the creator (don't restate hair/clothing already visible in the seed frame). Append an explicit lock phrase: "maintain exact appearance from reference image, consistent character throughout, no deformation, no drift, no face morphing." Keep camera motion small — aggressive orbit/dolly moves cause the face to re-render; "slow handheld, minimal camera motion" preserves identity. Center the subject — faces near frame edges warp first.

**Motion vocabulary:** verbs the model executes literally: picks up, lifts, tilts, unscrews, twists, pours, scoops, dispenses, snaps, pumps, dabs, rubs, sips, drinks, sets down, spreads, shakes, smiles, glances, nods. Verbs it ignores or fudges: "uses," "interacts with," "enjoys," "experiences," "showcases" — too abstract; replace every abstract verb with one concrete physical verb.

**Camera vocabulary:** pick only ONE camera primitive per generation (multiple = jitter): slow dolly in/out, pan right/left, tracking shot following hands, slow orbit, aerial/overhead, handheld, locked-off/fixed camera. For a UGC product-action cut, the only two that should ever be used are "handheld, minimal motion" and "locked-off, fixed camera" — anything else reads as agency-produced.

**Failure → fix table:**

| Failure | Cause | Fix |
|---|---|---|
| Face morphs/drifts | Camera moving too much; clip too long | "handheld, minimal motion"; cap at 5–6s |
| Hands warp / extra fingers | Complex hand-product interaction + fast motion | Slow the verb ("slowly lifts"); keep hands fully in frame |
| Product label gibberish | Logo near edge; reflections; rotation | Center logo with margin; clean reflections in source; avoid orbit/rotate; add "keep label perfectly readable, no garbled text, no logo morphing" |
| Product re-rendered as wrong shape | Product was re-described in the prompt | Stop describing the product; let the seed frame define it; only describe the action |
| Video stays static | No concrete verb; abstract motion | Replace abstract verbs with physical ones ("unscrews cap" not "opens product") |
| Plasticky AI gloss / slow-mo | Default cinematic bias | Lead with the UGC anchor phrase; use "auto" genre; add "no slow motion, real-time pacing, natural imperfect motion" |
| Background hijacks attention | Scene re-rendered each frame | "static background, only [subject/hands] move" |
| Two camera moves blend into jitter | Multiple camera verbs used | Pick one; negate the rest ("no zoom, no pan, only slight handheld jitter") |

**Copy-paste templates:**

*Drink/sip a supplement:*
```
UGC creator, iPhone handheld, harsh window light, kitchen background.
She unscrews the cap, lifts the bottle, takes a small sip, lowers it,
half-smiles at camera. Locked-off camera, minimal handheld jitter.
Ambient room tone, soft cap-click and liquid sip SFX, no music.
Maintain exact appearance from reference image, no face morphing,
no logo morphing, keep label readable. 5s, 720p, 9:16.
```

*Pour into hand / scoop:*
```
UGC creator, handheld iPhone POV, bathroom counter daylight.
She tilts the jar, taps two gummies into her open palm, looks down at them.
Camera locked, only hands and jar move, static background.
Soft tap and rattle SFX, no music, no narration.
Lock identity to reference image, no drift, no warping hands,
keep label perfectly readable, no garbled text. 5s, 720p, 9:16.
```

*Unbox / open:*
```
UGC creator, handheld phone, bedroom soft daylight.
She slides the lid off the box, peels back tissue paper, lifts the bag
out by the handle, holds it up beside her face, raises eyebrows.
Slow handheld, subtle natural shake, no zoom, no pan.
Soft paper rustle and box-thunk SFX, no music.
Maintain exact appearance and product from reference image,
no deformation, no extra props invented. 6s, 720p, 9:16.
```

*Wear / try on (fashion):*
```
UGC creator, mirror selfie iPhone handheld, bedroom natural light.
She lifts the strap onto her shoulder, adjusts it, turns slightly side
to side, glances down at the bag, back up to mirror.
Locked-off, only subject moves, no orbit, no zoom.
Fabric rustle and strap-creak SFX, no music.
Lock face and outfit to reference image, no morphing,
keep hardware and stitching detail consistent. 6s, 720p, 9:16.
```

**Product fidelity anchoring:** source images should be 2000+px on the long edge, sharp, flat lighting, logo centered with margin, reflections cleaned up — a garbage seed produces a garbage output. Negate explicitly on every generation: "no logo morphing, no garbled text, no warped label, no color shift, no extra products invented." Avoid rotational moves on the product (orbit, 360°, dolly arc) — the #1 cause of label scramble; linear lifts/tilts/pours are safe. If the label still scrambles at the production quality tier, too much motion is being asked for — cut duration to 4s or freeze the product and only animate the creator.

**The "natural/organic" look — required cues:** "UGC creator · iPhone handheld · harsh window light / harsh midday sun · slightly imperfect framing · real-time pacing, no slow motion · subtle natural handheld jitter · no music, only ambient room tone · no color grading, no cinematic look." Combined with an "auto" genre setting and 720p (not 1080p), output reads as phone footage most of the time.

**When to pick which model class:**

| Use case | Pick |
|---|---|
| UGC product-action cut with literal action seeded from a last frame | The literal/physical model class (e.g. Seedance 2.0) — best motion literalism, best identity from a single seed, native audio |
| Multi-shot mini-story with a consistent character, no post-production stitching | The general/interpretive model class (e.g. Kling 3.0) with multiple reference elements + storyboarded beats |
| Cinema-grade hero shot with native dialogue and broadcast-quality color | A premium cinematic model (e.g. Veo 3.1) — cleanest motion + audio, but expensive and often over-polished for UGC |
| Fast batch of UGC variants for A/B testing | The literal/physical model class in its cheapest/fastest mode — cheapest serviceable motion + native audio in one pass |
| Creator talking while using the product, lip-synced to an existing voiceover track | The literal/physical model class with the audio role set to "voiceover" |

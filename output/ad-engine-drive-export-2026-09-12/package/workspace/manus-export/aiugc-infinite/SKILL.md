---
name: aiugc-infinite
description: Produce batches of finished, stitched, vertical (9:16) two-cut UGC-style creator ad videos at scale from a single brand brief. Each ad has two cuts — Cut 1 is a talking-head creator delivering a hook/script with native voiceover, Cut 2 is a hard cut to the same creator using or demonstrating the product (an image-to-video action scene seeded from Cut 1's last frame). Use whenever the goal is "build infinite AIUGC", an "AIUGC factory", "two-cut UGC ads at scale", or any batch UGC production that cuts from a talking head to a product-action scene. Not for single-cut talking heads with no product cut, for exact replication of one specific reference ad, or for 3D/claymation animated ads.
---

# AIUGC Infinite — Two-Cut Creator Ad Factory

Produces batches of finished, stitched, vertical (9:16) two-cut UGC-style video ads from a single brand brief. Each ad has two cuts:

- **Cut 1** — a talking-head creator delivering the hook/script with native voiceover (a UGC-preset talking-head video generator with built-in voice generation).
- **Cut 2** — a hard cut to the same creator using or demonstrating the product: a literal, physically-grounded image-to-video clip seeded from Cut 1's last frame.

The two cuts are concatenated into one finished ad with a hard cut. This is a batch pipeline — it runs the same loop N times to produce N finished ads from one brief.

**When NOT to use this:** a single-cut talking head with no product-action cut needs a simpler talking-head pipeline instead. Replicating one specific reference ad exactly calls for an ad-replication process, not N original variations. 3D-animated or claymation ads need an animated-video pipeline, not this one.

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
       a. Cost preflight — check generation cost against account balance before committing credits
       b. CUT 1 — generate a UGC-mode talking-head video with the chosen hook, setting,
          and product, native audio generation on → 5-8s of a creator talking with VO
       c. Download Cut 1, extract its last frame as a still image (the seed for Cut 2)
       d. CUT 2 — generate an image-to-video clip seeded from that last frame, describing
          the product-action motion (5s) → creator using the product
       e. Download Cut 2
       f. Concatenate Cut 1 + Cut 2 into one final video with a hard cut
  |
  v
[4] Save a manifest recording every asset, prompt, and cost for the batch
```

## Required inputs

Collect before starting:

1. **Brand** — access to the brand's research/voice documents and a hero product image.
2. **Count N** — number of ads to produce (default 5 if unspecified).
3. **Concept seed (optional)** — an angle, hook style, or copywriting brief. If omitted, pull from the brand's research documents and invent N variations.
4. **Aspect ratio** — 9:16 (default), 1:1, or 16:9.
5. **Cut durations** — Cut 1 defaults to 8s, Cut 2 defaults to 5s.
6. **Identity lock (optional)** — a pinned character/avatar reference for consistency across the whole batch. If omitted, Cut 2 inherits identity from Cut 1's last frame; Cut 1's avatar is whatever the talking-head generator produces for the chosen hook.
7. **Hook/setting strategy** — rotate through a catalog of brand-appropriate hook and setting combinations (default), use one fixed combination for the whole batch, or randomize.

## Golden nugget doctrine (apply before writing any script)

Before generating hooks or scripts, name the **golden nugget** — the single most emotionally loaded deep frame in the brand's research, the real motive that makes buyers act, never the surface theme.

- Topic ≠ motive. "Memory loss" is a topic; "I thought I was becoming my mother, until I found this" is the motive. Surface angles buy mild curiosity — deep frames trigger identification so strong the reader feels caught.
- The test for every candidate angle: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper.
- The golden nugget leads — it IS the hook, at the very top. It is never buried in the body.
- State the golden nugget in one explicit sentence before drafting scripts. If the brand's research hasn't surfaced one yet, mine reviews/VoC before defaulting to a surface angle.

## Step 1 — Generate N two-cut scripts

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

Rules:
- Cut 1 VO is ≤22 words (roughly 8 seconds of natural speech).
- Cut 1 ends **mid-thought** — this sets up the Cut 2 hard cut and creates pull-through (the viewer keeps watching to see the payoff).
- Cut 2's visual matches Cut 1's avatar and setting for continuity.
- Cut 2 always shows the product physically on screen — a concrete action (drink/hold/open/spread/wear it), never an abstract one.
- Every Cut 2 prompt gets the 4-cue organic-imperfection stack bolted on (see below).

## Step 2 — Resolve assets

- If the brand doesn't yet have a product entity registered with the generation service, set one up first (upload the hero product image, register the product) — one-time per brand.
- Load a brand-appropriate catalog of hook and setting options to rotate through.
- If an identity-lock reference is supplied or already saved for this brand, use it to keep the avatar consistent across the whole batch.

## Step 3 — Per-ad generation loop

For each script:

1. **Cost preflight.** Check the estimated cost of the run against the account balance before generating anything. If the total exceeds a reasonable threshold (roughly 500 credits) or the balance is under 1.2× the estimated total, stop and confirm with the user before continuing.
2. **Generate Cut 1** — a UGC-mode talking-head video using the hook and setting choices, the product reference, native audio generation enabled, 9:16, ~8s, 720p.
3. **Extract the last frame** of Cut 1 as a still image — pull it a fraction of a second before the very end, not the literal last frame, to avoid a motion-blurred grab. This becomes the seed image for Cut 2.
4. **Generate Cut 2** — an image-to-video clip seeded from that last frame, using the Cut 2 visual prompt, 9:16, 5s, 720p.
5. **Stitch** Cut 1 and Cut 2 into one final video with a hard cut. Normalize both clips' video/audio streams to the same resolution/framerate/codec before concatenating so the join doesn't glitch. If Cut 2 has no audio track (common — see the Seedance notes below), synthesize a silent stereo track for it first so the concatenation doesn't desync.

## Step 4 — Manifest

After every ad, record: ad id, brand, which hook/setting were used, the product reference id, both generation job ids and their credit costs, file paths for both raw cuts and the final stitched video, the exact prompts used, and a timestamp. Keep this manifest so a batch can be audited, reused, or resumed if interrupted.

## Cost discipline

Observed pricing at 9:16, 720p (drifts over time — always check current pricing before a large batch):
- Cut 1 (talking-head, 8s, UGC mode, native audio on): ~40 credits
- Cut 2 (image-to-video action, 5s, standard mode): ~22 credits
- Per finished two-cut ad: ~62 credits
- Batch of N=10: ~620 credits + a 100-credit buffer ≈ 720 credits

Reduce cost by: shortening Cut 1 to 6s (~25% cheaper); using a faster/cheaper mode for Cut 2 (slightly lower visual quality); rendering at 480p for first-pass iteration and only bumping to 720p/1080p on confirmed winners.

## Failure modes and fixes

- **Cut 1 has the wrong avatar / a random face** — train and pin a consistent character/identity reference rather than relying on the default talking-head output for each hook.
- **Cut 2's face drifts from Cut 1** — make sure the last-frame extraction grabbed a clean frame, not a motion-blur tail. If Cut 1 ends mid-gesture, pull the frame slightly earlier (e.g. 0.2s before the end instead of 0.1s).
- **The hard cut feels jarring** — this is intentional for UGC pacing. If softer is wanted, crossfade a short amount of video (~150ms) while leaving the audio hard-cut.
- **Audio cuts off mid-word at the end of Cut 1** — increase Cut 1's duration by ~1s, or trim Cut 1 at its last natural pause using silence detection before stitching.
- **The generator rejects hook/setting parameters** — those parameters are only valid in UGC talking-head mode; make sure Cut 1 stays in that mode.

## Model-specific prompting (essentials — full guides in references/)

Three model classes are in play across this pipeline: an image-generation model for hero/native-image stills, a general-purpose image-to-video model for vibe/lifestyle/talking-head work, and a literal/physical image-to-video model for the Cut 2 product-action scene. Each responds to a different prompting style.

**Universal cheat-sheet:**

| Lever | Image-gen model | General i2v model | Literal/physical i2v model |
|---|---|---|---|
| Prompt length | 250–400 words | ≤2 sentences | 60–120 words |
| Prompt focus (when seeded) | Describe CHANGES only | Describe MOTION only | Describe MOTION + identity lock |
| Negative prompts | None — phrase as positive constraints | None — phrase positive | None — append explicit lock + negate phrases |
| Sweet-spot duration | n/a | 5s | 5–6s |
| Sweet-spot resolution | 1024×1536 (9:16) | 720p | 720p |
| Identity tactic | Re-state PRESERVE every turn | Bind subject + same wording across clips | "maintain exact appearance from reference image, no drift, no morphing" |
| #1 failure | AI sheen / waxy skin | Face morphs at 10s | Face drifts when camera moves |

**The "looks real" stack** — stack 3-5 of these on every image or i2v prompt to break the AI-generated look: handheld jitter, rolling shutter wobble, eye-focus drift, background motion blur, 35mm grain/sensor noise, visible skin pores/faint freckles, imperfect framing, unedited RAW/shot-on-iPhone look, mid-blink/mid-word expression, ordinary background detail (half-empty mug, dishtowel).

**The 4-cue rule** for every talking-head or UGC product-action clip — always append to the motion prompt: *"subtle handheld jitter, rolling shutter wobble, eye-focus drift, ambient background motion."* This is the documented difference between an AI-rendered look and real phone-camera capture.

**Banned vocabulary** (all model types): `cinematic`, `epic`, `dramatic`, `stunning`, `beautiful`, `masterpiece`; `8k`, `4k`, `ultra-detailed`, `hyperrealistic`; `trending on artstation`, `award-winning`, `professional`; generic verbs (`moves`, `interacts`, `uses`, `experiences`, `enjoys`); competitor brand names; vague mood words — replace with concrete visual facts.

**Order of operations when prompting:**
1. Start-frame quality matters more than the prompt — spend most of the effort on the seed image.
2. One concrete physical verb beats five abstract ones ("she unscrews the cap" beats "she uses the product").
3. Stop redescribing what's already in the frame — describe deltas/motion only when working from a seed image.
4. Generate cheap/fast first, regenerate winners at higher fidelity.
5. Pin every parameter explicitly: duration, resolution, aspect ratio, mode, sound, genre.

For the full prompting playbooks — text rendering, edit mode, camera/lighting vocabulary, copy-paste templates, and failure→fix tables for each model — see:
- `references/prompting-overview.md` — index + universal cheat-sheet
- `references/gpt-image-2-prompting.md` — hero/native-image stills, on-image typography, editing mode
- `references/kling-3-prompting.md` — general/interpretive image-to-video for vibe/lifestyle/talking-head work
- `references/seedance-2-prompting.md` — literal/physical image-to-video for the Cut 2 product-action scene, including the exact 4-block prompt formula and copy-paste templates

The Cut 2 prompting rules (UGC anchor + concrete-verb action + single camera move + identity lock) should be baked into whatever generates the Cut 2 visual prompts in Step 1 — every Cut 2 prompt the script generator produces should already follow that 4-block structure.

## Which model to pick for which role

| Use case | Pick |
|---|---|
| Cut 2 product-action seeded from a last frame | Literal/physical i2v model (e.g. Seedance 2.0) — best motion literalism, best identity from a single seed, native audio |
| Multi-shot mini-story with a consistent character, no post-production stitching | General/interpretive i2v model (e.g. Kling 3.0) with multiple reference elements + storyboarded beats |
| Cinema-grade hero shot with native dialogue and broadcast-quality color | A premium cinematic model (e.g. Veo 3.1) — cleanest motion + audio, but expensive and often over-polished for UGC |
| Fast batch of UGC variants for A/B testing | The literal/physical model in its cheapest/fastest mode |
| Creator talking while lip-synced to an existing voiceover track | The literal/physical model with the audio role set to "voiceover" |

## Output structure

```
output/run_<timestamp>/
├── scripts.json                # Step 1 output (all N scripts)
├── manifest.json                # one entry per finished ad
├── ad_001.mp4                   # final stitched ad
├── ad_001/
│   ├── cut1.mp4
│   ├── cut1_lastframe.png       # seed for Cut 2
│   ├── cut2.mp4
│   └── prompts.json             # exact prompts used
├── ad_002.mp4
├── ad_002/...
└── ...
```

## Memory hooks

After a successful run, persist: the product/hero-image reference id if setup ran for the first time, the trained identity-lock reference if one was generated, and the winning final ad ids so future batches can reuse what worked.

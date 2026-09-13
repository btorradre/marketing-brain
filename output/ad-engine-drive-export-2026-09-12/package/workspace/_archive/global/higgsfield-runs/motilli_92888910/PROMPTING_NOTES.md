# Higgsfield Prompting Notes — Motilli 92888910 (Organic UGC DR Replication)

Source-grounded synthesis from: Higgsfield Sora 2 Prompt Guide, Marketing Studio Intro,
Seedance 2.0 Prompting Guide, UGC Factory blog, "Selling Content" blog, Soul 2.0 article,
Marketing Studio Video 1, and the local `~/.agents/skills/higgsfield-{generate,product-photoshoot,soul-id}` SKILL.md + `references/` bundle.

Goal: rewrite `run.py` prompts so the output looks like a 55-year-old woman recorded a
testimonial on her iPhone in her actual house — not a softbox-lit AI woman in a render.

---

## 1. Top-level prompting principles (organic-UGC-focused)

1. **Lead with format, not subject.** Higgsfield's own Sora 2 guide opens prompts with the
   format ("UGC reaction video — handheld, shot on front iPhone camera, unfiltered
   realism"). The format string sets the model's entire aesthetic prior. Putting "UGC
   reaction video" in the first 8 tokens is more powerful than 60 tokens of subject
   description further down.

2. **One camera move + one subject action per beat.** Both Sora 2 and Seedance guides
   say this verbatim. Two actions or two camera moves per beat = canned cinematic move
   or motion smearing. Native UGC has *one* thing happening.

3. **Kill the words "cinematic / professional / 8K / flawless."** Higgsfield's UGC
   Factory and Marketing Studio docs explicitly position UGC as the *opposite* of
   cinematic. Soul 2.0's strength is "shot, not generated" — those polish words drag
   it back into stock-photo territory. Replace with "ungraded," "unfiltered," "no LUT,"
   "raw phone video."

4. **Negative phrasing is positive phrasing.** Higgsfield models do not expose a
   `negative_prompt` (per `prompt-engineering.md`). Don't write "no smooth skin" — write
   "visible pores, fine lines, light skin shine, no smoothing." Don't write "not
   cinematic" — write "ungraded iPhone video, flat colors."

5. **In i2i, describe the *change*, not the input.** From the local skill: "Bad: 'a man
   with brown hair…made into anime'. Good: 'transform into anime style, vibrant
   colors.'" For Motilli, when an `--image` is attached, stop redescribing the jar —
   describe what you want changed about the scene around it.

6. **In i2v (Kling/Seedance), describe motion only — never the static frame.** Same
   skill bundle: "Don't redescribe the static frame — model already has it." Most of
   the current `kling_prompt` lines are clean. The image_prompts are where the bloat
   lives.

7. **Lock identity with repeated noun phrases, not descriptions.** Sora 2 + Seedance
   guides: "Reuse exact descriptor phrases across shots." Pick one tight phrase like
   "55yo grey-bobbed woman, fine crow's feet, soft jawline" and paste it identically
   across every selfie beat. Variation = drift.

8. **Aspect ratio + duration go at the END as a stamp, not buried mid-sentence.**
   Seedance pattern: `Total: 5s / 1 shot / 9:16`. Models attend to terminal tokens
   strongly — putting the format stamp at the end re-anchors it.

9. **For organic look: name the device, the lens, and the lighting deficiency.** Not
   "iPhone footage" but "iPhone 15 Pro front cam, native wide ~26mm, slight barrel
   distortion." Not "natural light" but "single north-facing window, unbalanced
   exposure, slight blue auto-white-balance cast." Specificity → realism.

10. **When the brief says "ad," your default should still be UGC.** Higgsfield's
    Marketing Studio docs: "Default when the user doesn't specify: `ugc`." TV Spot is
    explicitly *broadcast-style*, which is the opposite of native-feed DR.

---

## 2. Per-model prompt template

### `nano_banana_2` — image (i2i with product anchor)

The local skill says Nano Banana 2 is for "character / cartoon / animated-style." For
realistic UGC selfies, **Soul 2.0 is the correct model** — Nano Banana 2 has a slight
illustrated bias that fights organic realism. Use Nano Banana 2 only for the **anatomical
3D animated cutaway beats** (2 and 7) and the **product-anchored beats** (6, 9).
Switch the selfie beats (1, 3, 4, 5, 8) to `text2image_soul_v2` (or its UGC presets).

**Template (i2i, product-anchored):**
```
[Format] Vertical 9:16 iPhone selfie still, ungraded, raw phone photo.
[Subject phrase — repeat verbatim every beat] 55yo woman, salt-and-pepper bob, fine
crow's feet, soft jawline, no makeup retouching.
[What changed] holding the [product] from the reference at chest level, casual home
[room].
[Lighting deficiency] single window from camera-left, mixed practical bulb, slight
underexposure on the shadow side.
[Texture cues] visible pores on cheeks and forehead, light skin shine, hair flyaways,
soft lens compression on nose from front-cam proximity.
[Anti-polish] no LUT, no color grade, no studio lighting, no beauty smoothing.
9:16, iPhone front cam.
```

**Annotated example for Beat 6 (Motilli reveal):**
```
Vertical 9:16 iPhone selfie still, ungraded, raw phone photo. 55yo woman,
salt-and-pepper bob, fine crow's feet, soft jawline, no makeup retouching, in a worn
soft-blue cardigan on her own beige couch. She holds the Motilli jar from the
reference at chest level (label and dark-green heart-shaped gummies must match the
attached reference exactly). Two dark forest-green heart gummies rest in her open
palm. Lit by one north-facing window camera-left + a warm lamp on the side table
(mixed color temp). Slight underexposure, visible pores, fine lines around eyes, hair
flyaways, micro front-cam barrel distortion. No LUT, no studio lighting, no
smoothing. 9:16, iPhone front cam.
```

### `kling3_0` — image-to-video (5s, sound on)

The local skill: "`--start-image` anchors first frame. Prompt describes motion." Sora 2
guide: "one camera move + one subject action per beat." Atlabs/Glif Kling guides
confirm Kling responds strongest to **opening the prompt with how the shot is
captured.**

**Template:**
```
[How shot is captured] Handheld iPhone front cam selfie, slight one-hand wobble.
[ONE subject action] [Subject] [verb in present tense] [object] and [tiny secondary
beat: glance / blink / sigh / half-smile].
[ONE camera micro-move OR none] (camera locked, just hand jitter) — OR — (camera
drifts 5° right with autofocus pulse).
[Organic cues — append as one parenthetical] (handheld jitter, rolling-shutter wobble,
autofocus micro-pulse, fabric/hair drift in ambient air).
```

**Annotated Beat 4 (couch confession) example:**
```
Handheld iPhone front cam selfie, one-hand wobble. She presses her palm flat to her
stomach, eyes flick down once, then back to camera with a tight breathy laugh.
Camera locked, just micro hand drift. (handheld jitter, rolling-shutter wobble,
autofocus micro-pulse, hair flyaways drift in still air).
```

Why this works: ONE action ("press palm + brief glance"), ONE non-move ("camera
locked"), organic cues at the end. The current run.py is already close; the fix is
killing the redundant frame redescription.

### `marketing_studio_video --mode ugc` (preset wrapper)

From the local `marketing-modes.md` and Marketing Studio Intro:

- The wrapper *prepends* hook text and *injects* avatar + product RAG before submission
- Your `--prompt` is **creative direction**, not the full storyboard
- Higgsfield explicitly: "Keep language casual and conversational… mention framing
  context ('bed', 'home', 'real rooms')"
- TV Spot mode is *the wrong tool* for this Motilli replication — it's broadcast-style.
  Don't reach for it just because the ref ad has 3D cutaways. Stay in `ugc`.

**Template (`--mode ugc`):**
```
--prompt "[hook line in avatar's first-person voice, ≤14 words]. She [one action] in
[real room]. [Sensory detail tied to product]. iPhone selfie, raw."
--avatars @<json>  --product_ids @<json>  --aspect_ratio 9:16
--duration 8  --resolution 720p  --generate-audio true
```

**Example:**
```
"I tried fiber, laxatives, even Ozempic — nothing moved. She sits on her own couch,
hand on her belly, holds a jar of Motilli green-apple gummies. Visible pores, no
makeup. iPhone front cam, real room, no LUT."
```

**Template (`--mode tv_spot`)** — only use for the closing hero/CTA card if you want
broadcast polish, not for any selfie beat:
```
--prompt "Cinematic 6-sec product spot. Slow push-in on the Motilli jar on a sunlit
kitchen counter, dust motes in the window beam, hand of a 55yo woman enters frame
and lifts the jar toward camera. Warm-cool palette anchor: cream counter, deep green
label."
--mode tv_spot --aspect_ratio 9:16 --duration 6 --resolution 720p
```

### `soul_2` / `soul_cast` / `soul_cinematic` (identity)

From the local `model-catalog.md` + Soul 2.0 article:

- **`text2image_soul_v2` (Soul 2.0)** — *aesthetic UGC, fashion editorial, lifestyle
  character.* This is your default for all Motilli selfie stills. Pair with
  `--soul-id` after training a Soul Character on 5–20 photos of a synthetic 55yo
  woman archetype to lock identity across all 9 beats.
- **`soul_cinematic` (Soul Cinema)** — cinematic stills, film-grade. Use for the
  CTA/hero shot (Beat 9) only if you want it to feel like a film still rather than a
  selfie. For organic-feel DR, **don't.**
- **`soul_cast`** — text-only, "distinctive characterful persona." Use this when you
  want a *very specific* archetype (e.g., a no-nonsense Midwestern grandmother) and
  you don't have or want a trained Soul ID. Cannot accept `--image`.

**Avoiding "generic stock-photo woman":** Soul 2.0 guide is explicit — it understands
"online slang" and "subcultural cues" and rewards "fashion context, niche aesthetics."
Translate that to DR: instead of "55-year-old woman" write "55, salt-and-pepper bob,
slightly tired eyes, the kind of woman who shops at Target and watches Yellowstone."
That subcultural anchor stops the generic-stock-woman mode-collapse.

**Template:**
```
text2image_soul_v2 --soul-id <ref_id>
--prompt "[avatar archetype with a subcultural anchor], [room with personal clutter
detail], [lighting deficiency], [skin texture cues], iPhone selfie, ungraded."
--aspect_ratio 9:16 --quality 2k
```

### `seedance_2_0` (reference-driven video)

When to pick over Kling 3.0 for this run:

- Kling is "single-plane scene without strong dynamics, cheaper" (local catalog)
- Seedance is SOTA when you need **multi-shot identity persistence + lipsync + native
  audio in one pass**. Marketing Studio Intro says Marketing Studio is *powered by*
  Seedance 2.0.
- For the Motilli beats where the woman speaks (1, 3, 4, 5, 8) and lipsync matters,
  **Seedance 2.0 with `--audio <vo_clip>` reference is the better choice.** Kling
  3.0 i2v doesn't lipsync, so any current dialogue audio is being added in
  post-stitch.

**Template:**
```
seedance_2_0
--prompt "Shot 1 of 1 / 5s / 9:16. Handheld iPhone front-cam selfie. [Subject phrase
verbatim] sits on her own couch, hand on belly, says: '[exact line]'. Camera locked,
hand-drift only. (handheld jitter, rolling shutter, autofocus pulse, ambient hair
drift)."
--start-image <still>  --audio <voiceover.mp3>  --duration 5  --aspect_ratio 9:16
```

Differences vs Kling for native lip-sync UGC:
- Seedance uses `--audio` role; Kling 3.0 has no audio reference
- Seedance enforces stronger identity persistence across multiple beats — better for
  this 9-beat run where the same woman appears 6 times
- Cost is higher; budget option is to keep Kling for the 3D cutaways (2, 7) and
  product hero (9) where lipsync doesn't matter, run Seedance only on dialogue beats

---

## 3. Organic UGC cookbook

### Skin
**Use:** "visible pores," "fine lines around the eyes," "light skin shine on the
forehead," "soft jawline, slight under-eye shadow," "no beauty smoothing," "natural
texture, fine imperfections," "sebum highlight on the nose."
**Avoid:** "flawless skin," "dewy glow," "smooth complexion," "perfect makeup,"
"radiant," "porcelain," "youthful glow," "airbrushed."

### Lighting
**Use:** "single north-facing window," "mixed practicals (tungsten lamp + window
daylight)," "slight underexposure on shadow side," "harsh midday window light, hard
contact shadow," "auto-white-balance drift, slight blue cast," "ungraded," "no LUT,"
"unbalanced exposure," "lit only by what's already in the room."
**Avoid:** "softbox," "ring light," "cinematic lighting," "key + fill + rim,"
"professional three-point lighting," "studio lighting," "golden hour cinematic,"
"film-grade," "ARRI ALEXA aesthetic" (this phrase is used in *Seedance for cinematic
fight scenes* — it's the wrong register for UGC).

### Framing
**Use:** "9:16 iPhone selfie," "head-cut, chin-to-eye crop," "off-center, head pushed
to the right third," "low angle from a couch (camera below eye-line)," "front-cam
barrel distortion, nose enlarged subtly," "elbow-extended one-hand selfie distance
(~50cm)," "messy framing, top of head clipped."
**Avoid:** "rule of thirds," "perfectly centered," "balanced composition,"
"professional framing," "wide cinematic shot," "establishing shot."

### Camera
**Use:** "handheld one-hand wobble," "autofocus micro-pulse," "rolling-shutter
wobble," "camera locked except hand drift," "phone-cam compression," "occasional
focus hunt," "native wide ~26mm," "iPhone 15 Pro front cam," "no stabilization, no
post edits."
**Avoid:** "smooth dolly," "Steadicam," "gimbal-stabilized," "tracking shot,"
"crane," "slow push-in" (unless explicitly the broadcast CTA beat), "cinematic motion,"
"sweeping pan."

### Wardrobe
**Use:** "worn cardigan," "faded grey sweatshirt," "lived-in," "old Target hoodie,"
"slightly pilling fabric," "simple cotton tee with a small stain at the collar,"
"unstyled, what she'd actually wear at home."
**Avoid:** "designer," "tailored," "couture," "fashion editorial," "chic," "stylish,"
"polished outfit," "wardrobe by [anything]."

### Environment
**Use:** "her actual kitchen with a half-empty coffee mug on the counter," "couch
with a throw pillow askew," "magnets and a kid's drawing on the fridge," "lived-in
clutter," "stack of mail visible behind her," "phone charger cable on the table."
**Avoid:** "minimalist," "designer interior," "rendered home," "pristine kitchen,"
"perfectly staged," "magazine-ready," "interior design quality."

---

## 4. The 10 worst anti-patterns + 10 best phrases

### REMOVE (drives output toward sterile / AI-clean)
1. "photorealistic UGC" — paradox; Higgsfield's UGC mode is the opposite of
   photorealistic. Use "raw iPhone video" or "ungraded selfie."
2. "cinematic" — anywhere in a UGC prompt. Saves it for the closing TV-spot CTA only.
3. "professional photography" / "professional lighting"
4. "8K" / "ultra HD" / "high resolution"
5. "perfect" / "flawless" / "pristine" / "smooth"
6. "soft daylight" — too generic; replace with the specific window direction
7. "warm afternoon home lighting" — too curated; replace with mixed practicals
8. "candid" alone (it's noise) — replace with the specific gesture that makes it
   candid: "mid-laugh," "looking past the camera," "caught mid-sigh"
9. "selfie 9:16 portrait" said as a description — Higgsfield wants the format up
   front as a *format declaration*, not embedded as adjectives
10. "intimate UGC selfie" — "intimate" reads as editorial; "UGC selfie" alone is
    cleaner

### ADD (drives output toward organic / native)
1. "ungraded iPhone video, no LUT, no color curve"
2. "iPhone 15 Pro front cam, native wide ~26mm"
3. "single north-facing window, unbalanced exposure"
4. "visible pores, fine lines around the eyes, light skin shine"
5. "handheld one-hand wobble, autofocus micro-pulse"
6. "rolling-shutter wobble"
7. "mid-laugh / mid-sigh / caught mid-thought" (replaces "candid")
8. "her actual kitchen, lived-in clutter, mail stack on the counter"
9. "no beauty smoothing, no retouching, no studio lighting"
10. "raw phone audio: room tone, slight HVAC hum, no music" (for video beats with
    sound on)

---

## 5. Diff plan — surgical edits to `run.py`

`run.py` is at `/Users/brooksorradre2/Documents/marketing brain/higgsfield-runs/motilli_92888910/run.py`.
Below: per-beat edits, exact replacements. The macro changes also include:

**Macro change A (model swap for selfie beats):** beats 1, 3, 4, 5, 8 should use
`text2image_soul_v2` (Soul 2.0), not `nano_banana_2`. Soul 2.0 is Higgsfield's
designated UGC/lifestyle model; Nano Banana 2 has a slight illustrated bias.
**Caveat:** this requires a trained Soul ID for identity persistence — if you don't
want to train one right now, keep Nano Banana 2 but lift the prompt rewrites below.

**Macro change B (organic-cue chain upgrade):** the current `ORGANIC_CUES` constant
is `"handheld camera jitter, rolling shutter, eye focus drift, subtle background
motion"`. Per Sora 2 + Marketing Studio docs, add **two more**:
```python
ORGANIC_CUES = (
    "handheld one-hand wobble, rolling-shutter wobble, autofocus micro-pulse, "
    "ambient hair drift, raw phone audio with room tone, no LUT"
)
```

**Macro change C (subject phrase lock):** define a single constant and use it verbatim
in every selfie beat — stop varying the phrasing per beat:
```python
SUBJECT = (
    "55yo woman, salt-and-pepper bob, fine crow's feet, soft jawline, "
    "no makeup retouching"
)
```

### Per-beat edits

**Beat 1 — `hook_pen_sweep`**
Replace:
> "Selfie 9:16 portrait of a 55 year old woman with grey hair in a green shirt,
> holding an Ozempic-style injection pen in front of her midsection, soft daylight
> bathroom, subtle bottles of laxatives blurred behind her on the counter, candid
> medical-aware mood, photorealistic UGC."

With:
> "Vertical 9:16 iPhone selfie, ungraded, raw phone photo. {SUBJECT} in a worn
> olive sweatshirt, holding an injection pen across her midsection in her own
> bathroom. Generic laxative bottles cluttered on the counter behind her, slightly
> out of focus. Lit only by a single north-facing window, slight underexposure on
> shadow side. Visible pores, light skin shine, hair flyaways. No LUT, no studio
> lighting, no smoothing. iPhone 15 Pro front cam, ~26mm. 9:16."

**Beat 2 — `anim_gut_slowdown`** (3D cutaway, keep Nano Banana)
Current is fine; just add explicit *non-realism* flag so Kling doesn't try to
photorealize it:
> Append: "...clinical educational illustration style, no live-action, no
> photorealism, anatomical-textbook color palette."

**Beat 3 — `competitor_cabinet`**
Replace:
> "Same 55 year old grey-haired woman from scene 1 in a soft beige bathrobe,
> standing at an open medicine cabinet packed with generic blue and purple laxative
> bottles and pink fiber tubs, holding one bottle up at eye level with a frustrated
> expression, soft daylight, photorealistic UGC."

With:
> "Vertical 9:16 iPhone selfie, ungraded. {SUBJECT}, same woman as Beat 1, in a
> faded beige terry bathrobe, standing at her own open medicine cabinet packed
> with mismatched generic laxative bottles and pink fiber tubs (real-life clutter,
> a few labels facing the wrong way). She holds one bottle up at eye level with a
> mid-sigh, half-frustrated expression. Bathroom vanity light overhead, hard
> contact shadow under chin. Visible pores, no smoothing. iPhone front cam. 9:16."

Kling motion: keep current — already lean.

**Beat 4 — `couch_concrete_confession`** (this is the one that's reading the most
AI-clean)
Replace:
> "Same 55 year old grey-haired woman, now in a maroon sweater, sitting on a soft
> beige couch in warm afternoon home lighting, leaning slightly toward the camera
> in an intimate selfie framing, hand pressed lightly to her stomach, sincere
> worried expression, photorealistic UGC."

With:
> "Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in a worn maroon cardigan with
> slight pilling at the elbow, sitting on her own beige couch with a throw pillow
> askew behind her. Hand pressed flat to her lower stomach, caught mid-sigh,
> off-center framing pushed to the right third, head slightly clipped at the top.
> Mixed light: north window camera-left + warm table lamp camera-right (color-temp
> mismatch). Visible pores, fine lines under the eyes, hair flyaways. No LUT, no
> beauty smoothing. iPhone 15 Pro front cam, slight barrel distortion. 9:16."

Kling motion: keep current. It already obeys one-action rule.

**Beat 5 — `bed_edge_terrified`**
Replace:
> "Same 55 year old grey-haired woman in soft cream pajamas, sitting on the edge
> of an unmade bed in soft morning light, looking directly at the camera with a
> vulnerable concerned expression, hand resting on her thigh, photorealistic
> intimate UGC selfie 9:16."

With:
> "Vertical 9:16 iPhone selfie, ungraded. {SUBJECT} in faded cream cotton pajamas
> with a small wash-fade on the chest, on the edge of her own unmade bed
> (visible duvet wrinkles, a phone charger cable on the nightstand). Caught mid-
> thought, eyes slightly tired. Single window camera-left, pale morning light,
> shadow side underexposed. Visible pores, light under-eye shadow. iPhone front
> cam. 9:16."

Strip the word "vulnerable" — that's a vibe word that pushes the model toward
melodramatic stock-photo posing. Let the room and lighting carry the emotion.

**Beat 6 — `motilli_reveal`** (product anchor — keep Nano Banana 2 for product
fidelity)
Replace:
> "Same 55 year old grey-haired woman in a soft blue sweater on a couch, holding
> the Motilli clear-bodied white-capped jar with green wrap-around label … warm
> afternoon home lighting, hopeful relieved expression, photorealistic UGC selfie
> 9:16."

With:
> "Vertical 9:16 iPhone selfie, ungraded, raw phone photo. {SUBJECT} in a worn
> soft-blue cardigan on her own beige couch (same room as Beat 4). She holds the
> Motilli jar from the reference image at chest level — label and dark forest-
> green heart-shaped gummies must match the reference exactly, do not invent
> color. Two dark green heart gummies in her open palm. Mixed light: north window
> + warm side lamp. Quiet half-smile, mid-exhale (not a posed smile). Visible
> pores, fine lines, hair flyaways. No LUT, no studio lighting, no beauty
> smoothing. iPhone 15 Pro front cam, ~26mm. 9:16."

Key change: "hopeful relieved expression" → "quiet half-smile, mid-exhale (not a
posed smile)." That single edit is the difference between stock-photo grandma and
real woman.

**Beat 7 — `anim_apigenin_wake`** (3D cutaway)
Append same non-realism flag as Beat 2: "...clinical educational illustration
style, anatomical-textbook palette, no photorealism, no live-action."

**Beat 8 — `kitchen_clockwork`**
Replace:
> "Same 55 year old grey-haired woman in a light blue sweater and jeans, walking
> confidently from a sunlit kitchen toward the camera, holding a coffee mug,
> relaxed flat midsection, genuine happy smile, bright airy home, photorealistic
> 9:16 lifestyle UGC."

With:
> "Vertical 9:16 iPhone video still, ungraded. {SUBJECT} in a faded light-blue
> sweatshirt and well-worn jeans, walking from her own sunlit kitchen toward the
> phone (handheld POV, low angle from waist height as if a friend is holding the
> phone). Coffee mug in one hand, relaxed easy smile mid-stride, not posed.
> Kitchen background: dishes drying on a rack, magnets and a kid's drawing on
> the fridge, mail stack on the counter (lived-in, not staged). Harsh midday
> window light from the right, hard contact shadow on the floor. iPhone 15 Pro,
> wide. 9:16."

Strip "confidently" and "bright airy home" — both are stock-photo language.

**Beat 9 — `cta_60_day_guarantee`** (product hero — keep Nano Banana)
This one is intentionally polished (it's the CTA). But still strip the AI-clean
words:

Replace:
> "...sitting on a clean white marble counter, two heart-shaped dark forest green
> Motilli gummies … in front of the jar, soft daylight, a small green badge that
> reads '60-DAY GUARANTEE' overlaid in the upper right…"

With:
> "Vertical 9:16 product hero, slightly elevated camera. The Motilli jar from the
> reference image (label and dark forest-green heart gummies must match the
> reference exactly) sits on a worn butcher-block counter (not pristine marble) in
> a real kitchen. Two dark green heart gummies in front of the jar. Hard slanted
> window light from camera-left, dust motes in the beam. Small green '60-DAY
> GUARANTEE' badge overlaid upper-right. {SUBJECT} partially in frame on the
> right edge in a worn olive shirt, hand mid-reach toward the jar. iPhone 15 Pro,
> wide. 9:16."

Swapped marble (stock) → butcher block (lived-in). This single change kills the
"render" feel.

### Kling motion-prompt edits (small)

Append two specific cues to every Kling prompt that are missing:

- Replace `"Woman lifts the Motilli jar slightly toward camera, smiles softly"`
  → `"She lifts the Motilli jar an inch toward camera, mid-exhale half-smile (not posed), camera locked, hand drift only."`
- Replace `"Camera does a slow gentle push-in toward the Motilli jar"` (Beat 9)
  → `"Hand-held drift forward toward the jar, ~6cm of motion total, autofocus
  re-locks once on the jar."` — kill "slow gentle push-in" (cinematic).

---

## Sources

- [Higgsfield Sora 2 Prompt Guide](https://higgsfield.ai/sora-2-prompt-guide) — most useful single page; the UGC iPhone selfie phrasings are lifted from here
- [Higgsfield Marketing Studio Intro](https://higgsfield.ai/marketing-studio-intro)
- [Seedance 2.0 Prompting Guide](https://higgsfield.ai/blog/seedance-prompting-guide)
- [Higgsfield UGC Factory Explained](https://higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained)
- [Most Realistic AI Model for UGC](https://higgsfield.ai/blog/3QU3e0LGo6VHDMEQGwdGv1)
- [Soul 2.0 Realistic AI Image Generator for Creative Direction](https://higgsfield.ai/blog/SOUL-2.0-Realistic-AI-Image-Generator-for-Creative-Direction)
- [Marketing Studio Video — $1M Brand](https://higgsfield.ai/blog/marketing-studio-video-1)
- [Create Selling Content with Higgsfield](https://higgsfield.ai/blog/Create-Selling-Content-Using-Higgsfield)
- Local skills: `~/.agents/skills/higgsfield-generate/{SKILL.md, references/prompt-engineering.md, references/model-catalog.md, references/marketing-modes.md}`
- Local skills: `~/.agents/skills/higgsfield-{product-photoshoot,soul-id}/SKILL.md`
- Atlabs Kling 3.0 Prompting Guide (corroboration on opening prompts with shot
  capture method)

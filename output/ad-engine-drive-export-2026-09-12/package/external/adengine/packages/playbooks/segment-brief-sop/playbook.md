---
name: segment-brief-sop
description: "Segment Brief SOP \u2014 Standard Output for Concept Runs (All Brands Except Velantra)"
source_kind: vault-doctrine
---

# Segment Brief SOP — Standard Output for Concept Runs (All Brands Except Velantra)

> **SUPERSEDED FOR BRIEF STRUCTURE (2026-08-21).** The outer brief format for every new video concept is now `Video-Brief-Format-SOP.md`. This document still governs the *segment map* mechanics for chained Seedance runs (base prompt + per-segment table) — drop that table into the Visual Schedule section of the house format rather than shipping this layout on its own.


**Status:** Canonical. Applies to EVERY video concept run for Motilli, Lunessa, Orelli, Avelle, Solorna, Renavita, Foliara, and any future brand — **except Velantra** (Velantra uses its own per-product concept skills with external editor-brief conventions: no local paths, live PDP links, self-contained prompts).

**Reference implementation:** `brands/motilli/creative/MOT-ELLEN-RUPTURE-UGC-01/MOT-ELLEN-RUPTURE-UGC-01-brief.md` (2026-07-06, Ellen rupture car-confession).

**Execution:** the `seedance-brief-runner` skill (`.claude/skills/seedance-brief-runner/`) executes finished briefs — compiles the segment map to `segments.json`, runs the segment-1 casting call, locks the voice anchor, generates all segments with last-frame chaining, and stitches `final.mp4`. This SOP defines the brief; that skill produces the video.

## Why this format

One **base prompt** defined once + a **per-segment table** the editor/pipeline walks down. The base prompt carries every consistency-critical instruction (camera, identity lock, no-morphing, setting lock); each segment row only varies dialogue + performance. This is what produces consistent outputs across a chained generation — never write 19 free-standing prompts.

## Required file

`brands/<brand>/creative/<CONCEPT-ID>/<CONCEPT-ID>-brief.md`

Concept ID convention: `<BRAND>-<CONCEPT>-<FORMAT>-<NN>` (e.g. `MOT-ELLEN-RUPTURE-UGC-01`). Reference video + teardown live in `<CONCEPT-ID>/reference/`.

## Required sections, in order

### 1. Header block
Concept one-liner, reference (source URL + local path + teardown path), pipeline named (e.g. `aiugc-longform` / Seedance 2.0 chaining), estimated segment count + runtime + credit cost, and any mechanism-congruence flags (does the funnel page teach the same mechanism by the same name?).

**GENERATION MODE (2026-07-06): always normal Seedance 2.0 (`std`), 9:16, 720p. `fast` mode is banned — visible distortion (warped hands, face melt under motion). If credits can't cover std, ask for a top-up; never downgrade.**

### 2. Beat map (reference → adaptation)
Two-column table mapping every narrative beat of the reference ad to its adapted equivalent. Forces structural fidelity and surfaces which beats got swapped and why. Prereq: run `ad-watcher` on the reference first — the beat map is derived from its breakdown.

### 3. Final script
Full spoken script in blockquote, with word count + estimated runtime (≈3.2–3.4 words/sec for conversational UGC). Written under `long-form-copy` laws (protected miracle, quoted-authority claims, calibrated proof, loop close). Sentences must break cleanly at segment boundaries (5–10s chunks).

**MANDATORY: run the script through the ai-copy-blacklist** (`_engine/copywriting/updated skills/ai-copy-blacklist.md`) before segmentation — full recursive self-audit: no parallel repetition stacks (two consecutive sentences opening with the same word, including across segment boundaries), no false-contrast stacks, no triple short-sentence stacks, no rhetorical transitions, no hedging. Mark the script header "passed ai-copy-blacklist audit <date>".

### 4. Avatar keyframe spec
- Creator described head-to-toe + setting + camera angle + light, 9:16.
- **Never clone the reference creator** — replicate the format, not the person (change hair, wardrobe, vehicle/room, background).
- State generation route (GPT Image 2 t2i, or Soul if the identity will be reused across a concept family). **ALL i2i uses GPT Image 2 (`gpt_image_2`), never Nano Banana (Brooks 2026-07-06).**
- **Product-hold keyframe:** always a pure i2i composite via GPT Image 2, seeded from the brand's canonical product reference (per `feedback_product_shots_i2i`) — never generated from scratch. Prompt the product out of frame by segment end so the chain continues clean.

### 5. Segment map

- **FORMAT SUPERSESSION (2026-07-08, Google Omni era): the SIMPLE prompt format is canonical. The dense JSON format below is RETIRED** — Brooks: "way too complicated, takes forever." Segments are **10 seconds max** (8-10s, sentence boundaries, ≤34 words each). Each segment is one copy-paste block, exactly this shape:
  1. Movement line: short comma-separated performance cues, e.g. `natural and realistic arm movements, hand to chest, subtle lean forward, looks directly at the lens the whole time`
  2. Voice line: `she says in a warm american early 50s ugc tone, a little worn but animated:` (adjust persona; tiny per-segment color allowed: "quiet but fully present", "bright with relief")
  3. The dialogue in quotes (clean, commas/periods only)
  4. Fixed footer: `Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage, expressive ugc movements, UGC aesthetic. Vertical 9:16. NO PRODUCT IN HAND. ONE CONTINUOUS SHOT` — product segments swap the flag to `PRODUCT IN HAND, LABEL FACING CAMERA, LABEL TEXT UNCHANGED.`
  Reference pack: `brands/motilli/creative/MOT-ELLEN-RUPTURE-UGC-01/MOT-ELLEN-RUPTURE-UGC-01-omni-prompts.md`. Image input per segment: avatar on seg 1, previous segment's last frame for chaining, product keyframe on product segments. Everything below this line is historical context for the retired dense format.
- **PROMPT AUTHORITY (2026-07-06): the UGC Director skill** (`_engine/standalone-skills/UGC DIRECTOR.md`, invocable as `seedanceugcdirector`) **defines the segment prompt format.** Dense timestamped prompts, one per segment — the earlier "short prompt" law is SUPERSEDED: density is survival; Seedance invents visual garbage for anything left undescribed.
- **DELIVERABLE + WORKFLOW (2026-07-07): copy-paste JSON prompt pack, manual generation.** The segment map ships as `<CONCEPT-ID>-seedance-prompts.md` — one complete JSON prompt per segment (keys: format / identity / creator / timeline[3 blocks with camera, right_hand, left_hand, face, in_frame, not_in_frame, light, background] / audio{voice, room_tone, delivery, dialogue} / never), copy-paste ready for the Seedance web UI. **NO @Image tags anywhere in prompts (2026-07-07)** — generation is image to video; the creator is wired in through the image input directly. Identity lines read "the creator stays the exact same person the whole time", never "@Image1 is...". Brooks generates manually in the UI (image input: avatar on segment 1, previous segment's last frame for chaining, product keyframe on the product segment; chosen casting take audio as voice reference). **Do NOT auto-generate the chain via the runner unless explicitly asked** — automated bulk generation burns credits on unreviewed segments. Reference pack: `brands/motilli/creative/MOT-ELLEN-RUPTURE-UGC-01/MOT-ELLEN-RUPTURE-UGC-01-seedance-prompts.md`.
- Per UGC Director, every 15s segment prompt = 3 × 5s blocks, each specifying: Camera / Creator (verbatim locked block, identical in every block of every segment — this is the identity mechanism) / Right hand / Left hand / Face / In frame / **Not in frame** (name the empty space so nothing spawns) / Light (one source, locked per segment) / Background. Header references @Image1 (creator) and product image; one action arc per segment. Audio line carries: voice character + room tone from the skill's library + "natural rhythm with real pauses and filler" + the full Dialogue.
- **@Image mapping via CLI:** attachment order defines the numbers — renumber the skill's @Image refs to match the actual `--image` flag order in the manifest (`reference_images` + per-segment `images`).
- **House style (from the skill):** no hyphens, no em dashes anywhere, numbers as numerals. Dialogue is filler-heavy ("okay so", "honestly", "like"), 30-45 words per 15s, contractions and fragments.
- **SCENE GEOGRAPHY LAW (2026-07-07 — prevents mirrored/flipped segments):** all spatial language is FRAME-relative from the viewer's side ("window on the LEFT of frame"), NEVER person-relative ("on her right") — person-relative is ambiguous and when it contradicts the seed image the model resolves it by mirroring the scene. Before writing prompts, LOOK at the actual seed keyframe and describe its real layout (window side, headrest side, seatbelt diagonal, distinctive background objects). Every prompt carries a `scene_lock` key ("copy the exact left right layout of the start frame into every frame... do not mirror or flip the scene") and the `never` list includes "no mirroring, no flipped seat or window sides".
- Still in force from the acting-beat findings (they complement the skill):
  - **BANNED CLAUSE: "only natural mouth and minor head movement"** — freezes the body into teleprompter delivery. Identity comes from the verbatim creator block + reference image, never stillness.
  - Acting beats tied to specific words go in the per-block Face/hand slots ("Left hand: presses flat on her stomach as she says felt heavy").
  - Never "composed/steady/even/calm" as register words (monotone cues); never backward-looking words ("remembering", "wistful") — drift-off cues. Quiet beats = intense and leaning-in.
  - **The word "cinematic" and the skill's banned camera/film vocabulary never appear.**
  - Segment 1 only, append a compact voice line (`Voice: <age, register, accent — ≤8 words>`) — it establishes the anchor; later segments inherit voice from the anchor audio.
  - Product-hold segment only, append: `no warping hands, keep label perfectly readable.`
- Then a table: `# | ~s | Dialogue (spoken-delivery version) | Performance + vocal cue`. **Seedance supports 15s segments — use them fully: target 12–15s per chunk**, split at sentence boundaries. Fewer segments = fewer seams = less identity/voice drift. Flag special-seed segments (product hold) inline. Drift mitigation: if a segment's face drifts, split that chunk in two and regenerate — don't shorten the whole map preemptively.
- **Dialogue naturalness rules (mandatory — clean written English produces teleprompter cadence):**
  1. The script (section 3) is the clean copy of record; the dialogue cells are the **spoken-delivery version** — same meaning, textured for speech. Never feed the clean written script to the video model.
  2. **Dialogue punctuation: commas and periods ONLY — no ellipses, no em-dashes.** The model renders them as literal dead-air pauses in the video. Rhythm comes from word choice and sentence length; intentional beats are directed in the performance cue ("breath before X"), never written into the dialogue text.
  3. Contractions everywhere; one casual form ("gonna") near the top at most.
  4. Disfluency budget: ~1 per 2 segments, comma-framed verbal texture only ("Mild, right?", "And honestly, it worked") — no trailing-off constructions. NEVER on mechanism terms, numbers, product name, or dosage — those deliver clean.
  5. Every performance cell carries a vocal cue (voice drops / pace picks up / half-laugh / beat before X), not just a physical one.
- **Tonal consistency rules (anti-monotone + anti-drift — the known AI failure mode is up-tempo open → back half decays to monotone, compounding across chained segments):**
  1. ONE named base register, restated verbatim in every segment prompt — the model never invents a segment's tone.
  2. A tonal-deviation table (segments → small shades off the base: "warmth lifts", "a touch quieter") — deviations are shades, never gear changes, and she returns to base by segment end so the next segment seeds from the same place.
  3. Held-energy rule: intensity is constant, color varies. Quiet = quiet-with-presence, not low-energy. "Energy holds through the final word" appears in every prompt.
  4. Anchor discipline: segments 2..N ALL anchor to segment 1's audio, never the previous segment's — drift cannot compound.
  5. Regeneration rule: any segment whose back half fades to flat gets regenerated from the same seed + anchor. Never accept a faded segment — the next one seeds from it.
- Chaining notes: segment-1 native audio = voice anchor — **gate: SEGMENT-1 CASTING CALL — generate 3 takes of segment 1, pick the most alive delivery as the anchor. If all 3 read flat, switch to the ElevenLabs `--audio` fallback (render expressive VO, chunk at segment boundaries, Seedance lip-syncs — deterministic performance) instead of burning more native takes.** Never fix delivery downstream. Last-frame seeding; drift mitigation (split the offending chunk in two if identity drifts).
- QA additions: end-of-segment energy check on every clip (listen to the LAST sentence); tonal drift A/B (seg 1 vs mid vs final back-to-back — same register, same intensity).

### 6. Post / captions
Caption style (word-by-word vs phrase), font weight, placement, single accent color (brand-appropriate + an A/B fallback), the specific emphasis words, hook-overlay decision, audio/music decision, stitch notes.

### 7. QA gates before spend
Minimum: voice consistency first→last segment, identity side-by-side check, product accuracy vs canonical reference (run `broll-auditor` on product segments), lip-sync spot checks, runtime bounds.

### 8. Compliance notes
Where risky claims live (quoted authority / lived experience only), what's protected (e.g., the medication in GLP-1 concepts), what's never named (drug brands).

## Hard rules carried into every brief

1. Base-prompt-once + per-segment-variation-only. No per-segment freehand prompts.
2. Reference teardown (`ad-watcher`) before the beat map. No brief without a beat map.
3. Product shots: pure i2i from the brand's canonical reference image, always.
4. Script before segmentation — never segment a draft, and never segment a script that hasn't passed the ai-copy-blacklist audit.
5. Cost estimate in the header — no silent spend.
6. Velantra excluded — its concept skills own their own brief format.
7. **The 3D-model look is banned (Brooks, 2026-07-29 — standing law, every concept, every brand).** "Whenever we're making a concept, we want to ban the 3D model look. If it looks like a 3D model, it needs to be regenerated." Two things stop it, and both must be in every generation prompt: a hard anti-CGI footer (name what to refuse — 3D render, CGI, product visualisation, ray tracing, catalogue photography, retouching — and what photographic evidence to require: sensor noise, blown highlights, chromatic aberration, JPEG artefacts, imperfect focus, handheld motion blur, crooked framing, worn/creased surfaces, dust and fingerprints, a lived-in setting), and an explicit refusal of the i2i reference's own look, since brand product refs are clean catalogue cutouts whose rendering aesthetic i2i inherits wholesale. Verbatim block: `~/.claude/skills/velantra-weekender/SKILL.md` → "VERBATIM PHOTOREAL BLOCK".
8. **Three variants of every scene, then pick the one that is not artifacted.** Never ship the first roll. Judge photoreal first, then product truth, then composition — a frame that nails the product but reads as CGI is a reject. Keep rejects on disk beside the pick.

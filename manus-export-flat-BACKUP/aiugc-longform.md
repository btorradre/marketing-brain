# AIUGC Longform — Single-Shot Continuous Talking-Head VSL Factory

This document describes how to produce 60–180 second single-shot, continuous-take, creator-talking-head VSL (video sales letter) ads — one creator, one continuous setting, one continuous voiceover, no B-roll, no scene cuts, with a hook overlay burned into the first 8 seconds. Use this whenever the request is for "long-form UGC," "VSL-style talking head," a "60-180s continuous yapper," or to replicate ads in the style of a single continuous-shot creator rant (the reference pattern studied for this format is a joint-pain/menopause supplement ad style referred to below as "HurAgain"). This is distinct from a two-cut format (creator talking, then a hard cut to product-action b-roll) — this format never cuts away from the creator at all.

**When NOT to use this:** for a two-cut format (talking + product-action cut), use a two-cut UGC pipeline instead. For short 15-30s UGC, a simpler short-form pipeline is more appropriate. For replicating one specific existing reference video exactly, use a video-replication process instead of generating original scripts.

## Why long-form needs a different approach than short clips

Every current video-generation model caps individual clips at roughly 15 seconds. A 60-180s single continuous-feeling ad has to be assembled from many short clips — but assembling video from short clips is easy; the hard part is making the AUDIO sound like one unbroken take.

## THE ONE-TAKE AUDIO LAW (read before choosing an approach — this is the load-bearing rule of the whole skill)

**The finished audio must be one unbroken take. The video is assembled from segments; the audio never is.**

This is the single thing that separates a long-form ad that sounds like one person talking from one that sounds like a stitched-together robot, and it is not fixable downstream.

If audio is generated per-clip (i.e. each short video segment gets its own freshly generated voice performance), every segment is an independent performance with its own pitch contour, pace, energy, and room tone. At two or three beats nobody notices. At twenty-plus beats across three or four minutes, every join is audible as a reset — the listener hears the speaker "restart" even when no word is damaged and no gap exists. This was measured on a real 24-segment build: word accuracy 0.998, seam gaps 57ms (against 40ms for a natural pause) — and it still sounded broken, because the defect is in prosody (the rhythm/pitch/stress pattern), which no simple audio metric detects.

**Chunking audio into sentence-safe pieces does not fix this.** Sentence-safe boundaries stop words being severed mid-phrase (important — see below), but a second take of a sentence is still not literally the continuation of a first take, because it never was performed as one.

**The fix:** render the entire script as ONE continuous voiceover in a single text-to-speech pass, with word-level timestamps. Then, for the visual side, split that single audio file into ~8-15 second chunks at sentence boundaries and generate a lip-synced video segment for each chunk (an image-to-video model that can accept a supplied audio track and lip-sync to it, rather than a model that only generates its own dialogue audio). After all segments are generated, discard every segment's own generated audio and lay the ORIGINAL single continuous voiceover back over the whole assembled video. The video is many pieces; the audio is one piece.

**This constrains which video-generation engine can be used.** The engine MUST accept a supplied audio track to lip-sync against — an engine that can only generate its own native dialogue audio per-clip is not eligible for long-form work, no matter how good it looks per-clip, because it guarantees the seam-audio failure described above. An engine that can only receive a full video (not a standalone audio file) as its audio reference, and does so unreliably, is fine for short 2-3 beat ads (where per-clip audio seams are inaudible) but cannot produce a seamless four-minute single-shot piece.

## Core pipeline

```
Brand brief + count N
  |
  v
[1] Generate N VSL scripts (90-180s each)
       Strict arc: hook -> agitation -> authority subversion -> mechanism -> solution -> CTA
  |
  v
[2] Resolve an avatar keyframe (one still portrait image that anchors the creator's
    identity, wardrobe, and setting for the whole ad)
  |
  v
[3] For each VSL script (loop):
       a. Render the WHOLE script as ONE continuous voiceover with word-level timestamps
             This single take is the finished ad's audio. Nothing downstream re-generates it.
       b. Split that audio at SENTENCE boundaries into N chunks of ~8-15s
             Never split a sentence. An over-long sentence splits at a comma instead.
             An under-filled chunk is fine (trailing silence trims cleanly);
             a severed sentence is not.
       c. For each chunk, generate a lip-synced video segment seeded from the SAME
             avatar keyframe image every time (never from the previous segment's last
             frame — see "why not chain" below), using that chunk's audio as the
             lip-sync reference and a motion-only prompt (no dialogue text in the prompt).
       d. Concatenate all video segments together, then replace the entire audio track
             with the one continuous voiceover from step (a), discarding every
             segment's own generated audio. This is what makes it read as one take.
       e. Burn in the hook overlay text on top of the first ~8 seconds (a red rounded
             badge with bold white text is the reference style), fading in over the
             first 0.2s and fading out around 7.6-8.0s.
       -> final video for this script
  |
  v
[4] Save a manifest recording every asset, prompt, and cost for the batch
```

### Why every segment seeds from the SAME avatar keyframe, never from the previous segment

Chaining (where segment 2 is seeded from segment 1's last frame, segment 3 from segment 2's last frame, and so on) is a random walk: each clip inherits the prior clip's accumulated visual error with nothing pulling it back toward the original, and identity/background visibly drift by around segment 10. This was measured directly: background similarity to the original scene was 0.53 when chained versus 0.86 when every segment re-seeded from the same original avatar image, and the chained version's fidelity declined steadily across the run while the unchained version stayed flat. Always keep one single reference avatar image and generate every segment from that same image.

## How to use this

### Required inputs

1. **Brand** — plus access to that brand's research/voice documents.
2. **Count N** — number of VSLs to produce in this batch (default 3 — per-VSL cost is high, so keep batches small unless told otherwise).
3. **Concept seed (optional)** — an angle/desire/hook style. If omitted, invent from the brand's research documents.
4. **Target duration (optional)** — 90/120/150/180 seconds. Default 120.
5. **Voice** — a specific voice to use for the TTS pass (an existing voice ID, or a voice cloned from a reference audio sample). If omitted, use a brand-default voice.
6. **Avatar** — a 9:16 portrait image of the creator, or a process for generating one (from a reference photo via image-to-image, or from a text description). If omitted, generate one from a brand-default description.
7. **Hook overlay style** — default to a red-badge style; other options are no overlay, or a plain caption style.
8. **Aspect ratio** — 9:16 default.
9. **Resolution** — 720p default; 1080p for a hero/final asset.

### Step 1 — Generate VSL scripts

For each script, produce:
```json
{
  "id": "vsl_001",
  "hook_overlay_text": "After trying 14 supplements for my joint pain",
  "hook_overlay_style": "red_badge",
  "vsl_script": "<full continuous spoken script, 90-180s, no scene markers, no SFX>",
  "estimated_duration_seconds": 118,
  "narrative_arc_check": {
    "hook_words_1_to_15": "...",
    "agitation_section": "...",
    "mechanism_section": "...",
    "solution_section": "...",
    "cta_section": "..."
  }
}
```

The script must be pure continuous spoken text — no scene markers, no sound-effect notation — and must follow the seven-beat arc described in the reference pattern below.

### Step 2 — Resolve the avatar keyframe

Get one still 9:16 portrait image that will anchor the creator's identity for the whole ad. In order of preference: use a supplied photo directly; use a cached/previously-approved avatar for this brand; generate one from a saved identity reference; or generate one from a brand-default description via image-to-image or text-to-image. This single image defines who the creator is, what they're wearing, and the setting/background — every segment in the ad inherits its visual identity from this one image.

### Step 3 — Per-VSL production loop

For each script:

**3a. Render the full continuous voiceover.** Send the entire script to a text-to-speech engine in a single call, with word-level timestamp alignment requested. Save the resulting audio file — this is the final ad's audio track, in its entirety, and nothing later in the pipeline re-generates or replaces it.

**3b. Segment the voiceover.** Split the rendered audio at sentence boundaries (periods, question marks, exclamation points) into chunks, targeting roughly 14 seconds each, with a floor of ~8s and a ceiling of ~15s (the practical maximum segment length most video models support well). Prefer chunks that land in the 13-15s sweet spot. Never split mid-sentence — if a single sentence exceeds the maximum, split it at a comma instead. Save each chunk as its own audio file plus a small manifest of chunk durations.

**3c. Render each visual segment.** For each audio chunk, in order, generate a lip-synced video segment: feed the SAME avatar keyframe image as the visual seed every time (not the previous segment's last frame), feed that chunk's audio as the lip-sync reference, and give a short motion-only prompt with no dialogue text in it (since the audio track already carries the actual words). Keep this prompt short — video models produce more visual artifacts as prompt length grows; budget roughly 80 words total.

A workable motion prompt template:
> "UGC iPhone selfie video, locked-off, real-time pacing. Same woman as the reference image, no face morphing, no setting change, no music. Subject lip-syncs to provided audio — natural pauses, expressive intonation, energy held to the final word, never monotone. [duration]s, 720p, 9:16."

If the chosen engine instead takes dialogue text directly in the prompt (rather than a separate audio track) for at least the first segment (to establish a voice anchor before switching to audio-driven lip-sync for later segments), use direction like: "She's animated and expressive, like FaceTiming her best friend about something huge that happened to her — voice rising and falling, stressing key words, speeding up and slowing down. Never monotone, never reading. She says: '[textured dialogue]'. [ONE cue, ≤10 words]." Use positive character framing in delivery direction — negations alone barely steer voice models. Never use backward-looking words ("remembering," "wistful") or flat-register words ("composed," "steady," "even," "calm") — the former cues drift-off, the latter cues monotone delivery. For the first segment specifically, generate a few takes and pick the most alive-sounding one as the voice anchor; if none sound alive, switch to the pre-rendered-audio approach instead (a deterministic performance that the video model just lip-syncs to, rather than letting the model invent its own delivery).

**Dialogue naturalness (mandatory whenever dialogue text is fed directly into a video-generation prompt instead of a separate audio track):** never pass clean, grammatically perfect written English — it produces a flat teleprompter cadence. Texture it for speech first: contractions everywhere; occasional comma-framed verbal texture (roughly one small disfluency per two chunks, e.g. "Mild, right?" — never placed on a mechanism term, a number, the product name, or a dosage); add one short vocal cue per chunk (voice drops / pace picks up / a beat before a key word). Use commas and periods only for dialogue punctuation — no ellipses, no em-dashes, since some models render those as dead-air pauses in the actual video. Intentional pauses belong in the cue direction, not embedded as punctuation in the text. The first segment locks the voice anchor for the rest of the ad — if it sounds like it's being read aloud from a script, regenerate it before generating anything downstream of it.

**Tonal consistency (anti-monotone, anti-drift):** the known failure pattern for AI voice delivery is an energetic opening that gradually decays into monotone by the back half, and this compounds across a long chain of segments. Counter it with: (1) one named base vocal register, restated verbatim in every chunk's prompt, with only small shading deviations between chunks ("warmth lifts slightly") — never a full gear change; (2) explicit instruction in every prompt that energy holds through the final word of the clip, with no trailing off or fading to flat; (3) every segment from the second onward should anchor its voice reference to segment 1's audio specifically, never to the immediately preceding segment's audio (to avoid compounding drift); (4) listen to every clip's last sentence specifically for energy fade, and regenerate any faded segment before letting a later segment build on it; (5) spot-check the first, a middle, and the final segment against each other for register drift.

**3d. Stitch, replace audio, burn overlay.** Concatenate all video segments into one continuous video with no audio. Mux in the single continuous voiceover from step 3a as the entire audio track, discarding every segment's own generated audio. Burn in the hook overlay text over the first ~8 seconds using a text-overlay filter: for the reference style, a solid red rounded rectangle badge behind bold white sans-serif text, centered horizontally, pinned to the upper third of the frame, wrapped to 2-3 lines, fading in over 0-0.2s and fading out over roughly 7.8-8.0s.

### Step 4 — Manifest

Record for each finished VSL: an id, the brand, total duration, number of segments, which voice and avatar were used, the hook overlay text, the generation cost incurred, and the final file path. Keeping this manifest lets a batch be audited or extended later.

## Reference pattern — the "HurAgain" single continuous-shot style

Distilled from two reference ads for the same joint-pain supplement, delivered by two different creators in two different settings but sharing the same narrative spine. This is a single-narrator, continuous-shot format.

**Structural skeleton (percent of total runtime → beat → approximate word count):**

| % through | Beat | Words spoken (approx) |
|---|---|---|
| 0-5% | Hook — promise + curiosity | 15-25 |
| 5-25% | Problem agitation — concrete sensory pain (3am wake-ups, can't sleep on side, hips burning, stiffness on standing, "have to think about every chair") | 80-150 |
| 25-40% | Authority subversion — "doctors said wear and tear," "anti-inflammatories like that was an answer" | 60-100 |
| 40-60% | Mechanism — plain-English root-cause explanation (e.g. estrogen → joint lubrication → estrogen drops in menopause → joints dry out → the ingredient class fixes it) | 100-180 |
| 60-75% | Solution — product name, dosage, what makes this specific product different (e.g. potency) | 80-130 |
| 75-95% | Personal proof — "felt lubricated within weeks," "rusted hinge to well-oiled machine" | 60-100 |
| 95-100% | CTA + guarantee — "link below," "60-day guarantee," "don't wait as long as I did" | 20-40 |

Total roughly 400-700 spoken words for a 90-180s VSL at conversational pace (4-5 words/second).

**Voice & cadence:**
- Conversational "rant" energy: "I'm gonna tell you...", "And here's what nobody told me...", "I had a suspicion..."
- Specific sensory details, never generic: not "I had pain" but "the ache that wakes you up at 3am," "the way you have to think about every chair before you sit in it."
- Authority subversion built in — always positions doctors/experts as having missed the obvious; the viewer agrees because they've experienced the same brush-off.
- Mechanism explained in plain English, no jargon stack: "Estrogen is what keeps your tendons supple."
- Metaphors carry the proof more than data does: "Like someone had sprayed WD-40 on my hips." "Rusted hinge to well-oiled machine."
- No hard sell — the CTA is soft: "link below, don't wait as long as I did."

**Visual pattern:**
- 9:16 vertical phone selfie, low chin-up angle (phone propped or held below eye level).
- One creator, one setting, no cuts, no B-roll, no zoom, no pan.
- Eye-level to upper-third framing — eyes visible across the frame, chest/shoulders typically visible, often with hand gestures rising into the lower frame.
- Practical/ambient lighting only — a kitchen's recessed ceiling light, a car's diffused daylight interior. No softboxes, no visible ring lights.
- Imperfect framing — subject slightly off-center, head sometimes near the top edge, deliberately not "professional."
- Background recognizable but soft — shallow depth of field from a phone camera; the setting reads as "kitchen" or "car" but details aren't sharp enough to scrutinize.

**Hook overlay style:**
- Red rounded badge, fully opaque, slightly rounded corners (~14px radius).
- Bold white sans-serif (system bold), roughly 50-60px at 1080×1920.
- Centered horizontally, pinned upper-third (~18% from top).
- 2-3 lines max, wrapped at natural phrase breaks.
- Pinned roughly 0-8s, fading out as the speaker hits the first transition into agitation.
- Example text: "After trying 14 supplement for my hip pain", "My hip pain journey (tried everything)".

**Why this format converts** (the direct-response mechanics behind it):
- Avatar mirroring — a 50+ candid creator in a plain setting reads as a peer, not an actor, which builds trust.
- Granular specificity — 3am wake-ups, a WD-40 metaphor — feels too specific to be fabricated, which reads as authentic.
- Mechanism education — the viewer learns WHY nothing else worked, which vindicates their past frustration.
- Soft sell — low-pressure CTA plus a guarantee reduces first-purchase friction.

Replicate this faithfully — don't compress the agitation, don't skip the mechanism, don't crank the urgency. The format earns trust through length, not pressure.

**Defaults that reproduce this style faithfully:** 120 seconds (the sweet spot); 9:16, 720p; red-badge upper-third hook overlay; a 50+ female voice by default; a 50+ female avatar in a kitchen or parked-car setting; and a script generator that enforces the seven-beat arc above with word-count guardrails per beat.

## Rules & standards

- **The one-take audio law is non-negotiable** — see above. Never generate per-segment dialogue audio and expect it to sound continuous; always render one continuous voiceover and replace every segment's audio with it.
- **Never chain segments from each other's last frame.** Always re-seed every segment from the same single avatar keyframe image.
- **Never split a sentence across a segment boundary.** Split at sentence punctuation; if a sentence is too long, split at a comma instead — never at an arbitrary word.
- **Keep motion prompts short** (roughly 80 words) — longer prompts increase visual artifacts on this kind of literal, physically-grounded video model.
- **QA every segment's final few words for energy fade** before letting the next segment build on it (when using the direct-dialogue-in-prompt approach) — a faded segment compounds if it's used as an anchor for the next one.
- **Trim leading silence from every audio chunk** before generating its video segment — long silence at the start of a chunk can cause a video model to drop lip-sync entirely for that segment.

## Failure modes and fixes

- **Avatar drifts mid-VSL** (late segments don't look like early ones) → shorten segments (e.g. 6s instead of 8s), always include an explicit "maintain exact appearance, no morphing" instruction in every segment's prompt, and confirm every segment is seeded from the same original avatar image, not a chained previous frame.
- **Lip-sync misses on a segment** → the audio chunk may have long silence at its start; trim leading silence from each chunk before generating.
- **Audio seams / "the segments don't flow into each other"** → this is the single most common long-form failure and the entire reason the One-Take Audio Law exists. It's caused by generating audio per-clip, so every segment is a separate performance. Symptom: each join sounds like the speaker restarting, even with clean words and no measurable gap. This is NOT fixable by chunking, trimming, crossfading, or re-encoding — it was verified on a 24-segment build that scored 0.998 word accuracy and still sounded wrong. The only fix: render one continuous voiceover and replace every segment's own audio with it at the final stitch. If the chosen video-generation engine cannot lip-sync to a supplied audio track, it is the wrong engine for long-form work.
- **Beats that split a sentence** → each segment is its own performance, and the model is implicitly told to come to a stop and hold silence after its final spoken word — so wherever a sentence gets cut, the model delivers terminal falling intonation there. Splitting "needs more push every / time" reads as a dropped word no matter how clean the audio otherwise is. Always chunk at sentence boundaries; break an over-long sentence at a comma, never at an arbitrary word. An under-filled chunk (trailing silence, easily trimmed) is an acceptable outcome; a severed sentence is not.
- **Hook overlay clips into the creator's face** → the badge should sit in the upper third of the frame; adjust its vertical position for taller/different framing.
- **A sentence runs long (past ~12s)** → split at the next-best comma boundary instead.

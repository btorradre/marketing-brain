# Animated Video — 3D/Motion-Graphics Ad Pipeline (Native Audio)

This document describes a production pipeline for animated-style direct-response video ads (3D animated, anthropomorphic characters, motion graphics, "inside the body" mechanism diagrams) built using an image-to-video model that supports native audio generation (dialogue, SFX, and ambient sound baked directly into each clip, with no separate voiceover recording needed). Use this whenever the goal is to build an animated (3D animated, motion graphics, anthropomorphic-character) video ad and want the video model to handle audio generation natively rather than dubbing a separately recorded voiceover over it. This is a sibling process to a claymation/stop-motion pipeline — same architecture, different visual style.

**When NOT to use this:** for stop-motion/claymation style, use a claymation-specific process instead (same architecture, but voiceover comes from a separate TTS engine and clips are silent until stitched). For live-action replication, use a live-action video-replication process. For talking-head/UGC formats, use a UGC-specific pipeline instead.

## Hard-won rules (non-negotiable)

These come from real production experience and are NOT optional — skipping any of them reliably produces visible artifacts.

1. **Video-generation prompts must be ≤2 sentences** — one for visual/camera, one for dialogue. Long, over-specified prompts cause the model to hallucinate (spawning extra elements mid-clip, stretching character proportions, extra fingers, deformed limbs). Resist the urge to over-specify.
2. **Lock the start frame = end frame on every generation call.** Pass the same keyframe image as both the start and end reference. This forces the model to return the camera/composition to the starting frame by clip-end, killing zoom drift and push-in/pull-back twitches, and background-element drift.
3. **Use a separately cloned voice for multi-segment dialogue from the same character.** A video model's own native dialogue generation tends to drift the voice/accent between segments — the same character sounds slightly different in clip 1 vs. clip 2 vs. clip 3. Fix: clone the voice once from a single reference clip using a voice-cloning service, then regenerate all of that character's dialogue with the cloned voice, and swap that audio onto the generated clips. Accept that lip-sync will be approximate in this case, since automated lip-sync tools perform poorly on stylized/non-realistic characters.
4. **Use hard cuts between segments, not crossfades.** Animated characters keep moving through a crossfade, producing ghosting/double-exposure at the boundary. Concatenate clips directly; match character poses at segment boundaries if the cut needs to feel continuous.
5. **Product reveals must be pure image-to-image from the real product photo.** Pass the canonical product photo as a reference image with an explicit "DO NOT invent fine print, labels, or decorative copy" directive. Otherwise the label will be AI-hallucinated gibberish — a credibility killer.
6. **Use one canonical character keyframe.** Generate the first shot once. Regenerate all subsequent keyframes using that first shot as the PRIMARY reference at a low creative-variance setting, with an explicit character-lock description (hair style, distinguishing accessory, correct number of fingers, etc.). Don't let generation variance rebuild the character from scratch shot to shot.
7. **Phonetically spell out difficult words for text-to-speech.** Some words get consistently mispronounced by both video-native audio and separate TTS engines (e.g. "constipation"). Spell them out phonetically in the spoken text (e.g. "con-stuh-pay-shun"). Leave ellipses in for natural pauses.
8. **Use real video stabilization, not a basic deshake filter.** A basic deshake filter cannot fully counter the camera drift these models introduce. Use a stabilization tool with two-pass motion detection and transform (e.g. ffmpeg's vidstab plugin), or fall back to feature-matching stabilization (e.g. via OpenCV) if that's unavailable.
9. **No open-ended mid-clip background elements in prompts.** Specify backgrounds as static. Don't say "flashing warning lights" — say "two warning lights, one left one right, steady not flashing." Open-ended language ("alarms flash") invites the model to multiply the elements — a two-alarm keyframe has been observed spawning roughly 28 alarms once animated.
10. **Captions come from the strategist's written script; timing comes from re-transcribing the final audio.** The written script is the authoritative text (it has correct brand spelling, unlike an automatic transcription of generated audio). Timing comes from re-transcribing the FINAL rendered audio with a word-level speech-to-text tool. Minimum caption duration should be 0.5s for readability.
11. **Max 5-second segments, not 10s.** These video models are trained heaviest on ~5s clips and produce significantly less drift, stretch, and hallucination at that length. Break any 10-second story beat into two 5-second sub-segments that share the same keyframe. A 30-second ad should be six 5-second segments, not three 10-second ones.
12. **Share the keyframe across continuation segments within the same scene.** If segment B continues the same scene as segment A (same character, same set, same camera position — only the dialogue moves forward), pass segment A's keyframe as segment B's reference image too. This forces the model to reproduce the exact same character/background at segment B's start as existed at segment A's start, making the hard-cut between them invisible. Combined with the start=end frame lock within each segment, this gives full visual continuity across the whole scene.

## Pipeline overview

```
INPUT: script + brief + brand
    v
[Stage 1] Strategist pass
          breaks the script into scene beats, produces a shot plan
          Per shot: image_prompt, motion_prompt, dialogue_or_sfx (what the video
          model should vocalize)
    v
[Stage 2] Keyframe generation (image-to-image)
          N animated-style still keyframes. Product shots use pure image-to-image
          from the real product photo.
    v
[APPROVAL GATE] — review the stills before spending video-generation budget
    v
[Stage 3] Video generation with native audio enabled
          Each clip includes:
            - Visual motion (animated style)
            - Character dialogue / narration (generated natively by the video model)
            - Ambient SFX / music if specified in the prompt
          ~5s per clip default, vertical (9:16), highest available quality tier.
          Organic-realism cues still apply even for an animated style.
    v
[Stage 4] (skipped — audio is already baked into the generated clips)
    v
[Stage 5] Stitch
          Clips already have synced audio baked in.
          Simple concatenation (no separate voiceover mix needed) — optionally a
          very light crossfade between clips if the segments truly don't need a
          hard cut.
    v
[OPTIONAL Stage 6] Caption/FX polish pass
          Extract audio from the finished video, transcribe it for word-level
          timing, overlay word-synced captions and any scene FX. Re-render the
          final polished version.
    v
OUTPUT: finished animated ad
```

## How to use this

### Required inputs

1. **Script/brief** — or explicit scene beats.
2. **Brand** — access that brand's voice/product context.
3. **Concept identifier** — a short code for this concept + version (e.g. an angle abbreviation + "ANIM" + a version number, like "GG-ANIM-01" for a "Gut Gridlock" angle, animated format, version 1) — useful for organizing multiple concepts and revisions.
4. **Reference ad (optional)** — if replicating a specific existing animated ad's look, use it to extract style and character cues.

### Optional parameters

- Skip approval gates (for a fully automated run).
- Stop after the keyframe stage (image-only preview).
- A voice-style hint per shot (e.g. "warm female narrator, 40s, conversational," "kid-friendly energetic," "clinical doctor") — the video model doesn't expose named voices, but style-cue language shapes the generated audio's character.
- A short crossfade (e.g. 0.25s) between clip boundaries instead of the default hard cut.

### The animated style block

Prepend this kind of style block to every keyframe-generation prompt that isn't a pure product-reveal image-to-image shot (adjust wording to match the specific reference look being targeted):

```
ANIMATED STYLE (enforce in every frame):
- 3D animated aesthetic, clean polished render (NOT clay, NOT live-action, NOT UGC)
- Soft rim lighting, stylized shading, hand-painted textures
- Anthropomorphic characters with exaggerated expressive features
- Warm palette with selective brand color accents
- 9:16 vertical composition
- Shallow depth of field, cinematic camera composition
- Stylized — NOT photorealistic, NOT technical diagram, NOT flat 2D
```

### Shot-plan fields (per shot)

```json
{
  "shot_number": 1,
  "purpose": "Hook",
  "duration_seconds": 5,
  "image_prompt": "visual description for the keyframe generator",
  "motion_prompt": "how the scene moves",
  "dialogue_line": "exact words the model should speak this shot (narrator VO or character dialogue)",
  "voice_style_hint": "warm female narrator, 40s, conversational",
  "sfx_direction": "ambient kitchen sounds, subtle stomach rumble",
  "has_product": false,
  "pure_i2i": false
}
```

These fields merge into a single generation prompt roughly like:
```
{animated_style_block}. {motion_prompt}. {organic_cues}.
Narration: {voice_style_hint} says "{dialogue_line}". Ambient: {sfx_direction}.
```

### Generation call shape (conceptual — adapt to whichever video-generation API is in use)

```
{
  "prompt": full_prompt_with_dialogue_and_sfx,
  "reference_images": [keyframe_image],
  "sound": true,                       # <- the key setting: native audio ON
  "duration_seconds": 5,
  "aspect_ratio": "9:16",
  "quality_tier": "highest available",
}
```

## Rules & standards

- Product shots must use pure image-to-image from the real canonical product photo — never generate a product's packaging or label from a blank prompt.
- Keep every video-generation prompt to two sentences or fewer.
- Cap every individual video segment at 5 seconds; break longer beats into multiple same-keyframe segments instead of asking for a longer clip.
- Always lock the start and end reference frame to the same image on every generation call.
- Use hard cuts, not crossfades, between animated segments.
- Regenerate every subsequent keyframe from the single canonical first-shot keyframe as the primary reference, not from the previous shot in sequence, to avoid character drift.

## Reference formats to study

The animated format for a mechanism-driven health/wellness ad typically follows one of:
1. **Inside-the-body mechanism** — anthropomorphic organ/cell characters interacting with ingredients.
2. **Product-as-character** — the product itself is personified and has dialogue.
3. **Avatar journey** — a stylized character going through a problem → discovery → relief arc.

## Approximate cost/time per finished ad (order-of-magnitude reference only — check current pricing before committing to a batch)

- Keyframe generation: roughly $0.08 per shot
- Video generation with native audio: roughly $0.70 per shot (audio-enabled clips cost more than silent ones)
- Caption/FX polish pass: effectively free if done locally
- Total for a 9-shot ad: roughly $6.50, 8–15 minutes of processing time

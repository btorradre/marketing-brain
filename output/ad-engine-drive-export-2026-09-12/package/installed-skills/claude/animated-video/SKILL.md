---
name: animated-video
description: End-to-end animated video ad pipeline using Kling 3.0 with NATIVE audio generation (no ElevenLabs needed). Takes a script + brief + brand, breaks it into a scene-beat breakdown, generates still keyframes via Nano Banana 2 image-to-image with product references, animates each still via Kling 3.0 WITH audio enabled (sound=True) so each clip includes dialogue/SFX/ambient directly from Kling, stitches clips with transcript-aligned timing, and optionally post-processes through HyperFrames for word-synced captions. Use when the user wants to build an animated (3D animated, motion graphics, anthropomorphic-character) video ad and wants Kling to handle all audio, or says "run the animated video skill", "build the animated ad with Kling audio", "make an animated video ad".
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Animated Video

Production pipeline for animated-style direct response video ads (3D animated, anthropomorphic characters, motion graphics, inside-the-body diagrams). Sibling to the `claymation` skill — same architecture, different visual style.

## ⚠️ HARD-WON RULES (from CONF-ANIM-01 production, 2026-04-21)

These rules are NOT optional. Skipping any of them produces the artifacts the user has called out before and will reject again.

1. **Kling prompts MUST be ≤2 sentences** — one for visual/camera, one for dialogue. Long strict prompts cause Kling to hallucinate (spawning alarms mid-clip, stretching character proportions, extra fingers, deformed limbs). Resist the urge to over-specify.
2. **Lock start = end frame on every Kling call**. Pass `image_urls: [keyframe_url, keyframe_url]` (same URL twice) in the `input` payload. This forces Kling to return the camera/composition to the starting frame by clip-end, killing zoom drift, push-in/pull-back twitches, and background-element drift. Variant `tail_image_url` is the fallback.
3. **ElevenLabs cloned voice for multi-segment villain dialogue**. Kling's native TTS drifts voice/accent between segments — the same character sounds slightly different in clip 1 vs clip 2 vs clip 3. Fix: clone the voice once from a single Kling reference clip, then regenerate all villain dialogue with the cloned voice, and audio-swap onto the Kling clips. Accept that lip-sync is approximate (Kling's mouth motion ≈ new audio) since sync-lipsync performs poorly on stylized 2D characters.
4. **Hard cuts between segments, NOT crossfades**. Characters animate THROUGH a crossfade, producing ghosting/double-exposure at every boundary. Use `concat` without xfade. Match poses at segment boundaries if the cut needs to feel continuous.
5. **Pure-i2i product reveals**. Pass the canonical product image as the SECOND image reference to Nano Banana, with an explicit `DO NOT invent fine print, labels, or decorative copy` directive. Otherwise the label will be AI-hallucinated gibberish. Credibility killer.
6. **Canonical character keyframe**. Generate shot 1 once. Regenerate all subsequent keyframes from shot 1 as the PRIMARY reference with `temperature=0.28-0.35` and an explicit character lock (hair style, lapel pin, five fingers). Don't let temperature drift rebuild the character.
7. **Phonetic spelling for difficult TTS words**. "Constipation" gets mispronounced by both Kling and ElevenLabs. Spell it `con-stuh-pay-shun` in the TTS text. Leave punctuation like `...` for natural pauses.
8. **Real stabilization, not just deshake**. `ffmpeg` without vidstab cannot fully counter Kling's camera drift. Use the vidstab-enabled Homebrew ffmpeg (`/opt/homebrew/bin/ffmpeg`) with `vidstabdetect` + `vidstabtransform`, or fall back to OpenCV feature-matching stabilization. The `deshake` filter alone is insufficient.
9. **No mid-clip background elements**. In prompts, specify background as static. Do NOT say "flashing warning lights" — say "two warning lights, one left one right, steady not flashing." Open-ended language ("alarms flash") invites Kling to multiply the elements (CONF-ANIM-01 had ~28 alarms spawn from a 2-alarm keyframe).
10. **Captions from strategist script, timings from Whisper**. Text is the authoritative script (fixes brand spelling — "Motilli" not "Motily"). Timings come from re-transcribing the final audio with Whisper word-level output. Minimum caption duration 0.5s for readability.
11. **Max 5-second Kling segments** — not 10s. Kling is trained heaviest on 5s clips and produces significantly less drift, stretch, and hallucination at that length. Break any 10s beat into 2×5s sub-segments that share the same keyframe. A 30s ad = 6×5s segments, not 3×10s.
12. **Shared keyframe across continuation segments within the same scene**. If segment B continues the same scene as segment A (same character, same set, same camera position — only the dialogue moves forward), pass segment A's keyframe as segment B's `image_urls` too. This forces Kling to reproduce the exact same character/background at segment B's t=0 as was at segment A's t=0, making the hard-cut between them invisible. Combined with start=end frame lock within each segment, this gives 100% continuity across the full scene.

## Key Difference vs `claymation`

| | claymation | animated-video |
|---|---|---|
| Visual style | Stop-motion clay | 3D / 2D animated |
| Audio source | ElevenLabs | **ElevenLabs (Kling native audio drifts voice — do NOT use for >1 segment)** |
| Kling prompt | Stop-motion + clay texture | **≤2 sentences, relaxed** |
| Stitch | Silent + separate VO | Hard cuts (no crossfades) |
| Start/end frame | Start only | **Start = end (same image twice)** |

## Key Difference vs `claymation`

| | claymation | animated-video |
|---|---|---|
| Visual style | Stop-motion clay | 3D animated / motion graphics |
| Audio | ElevenLabs TTS separate track | Kling native audio (`sound=True`) per clip |
| Kling prompt | Stop-motion + clay texture enforcement | Smooth animated motion + dialogue-bearing scenes |
| Stitch input | Silent Kling clips + separate VO | Kling clips already include audio |
| Stage 4 | ElevenLabs call | SKIPPED (audio is in the clips) |

Everything else — strategist, shot plan, Nano Banana i2i, sub-shots, whisper sync, HyperFrames polish — works the same way.

## When to Use

- User wants an animated video ad (Serene Herbs "inside the gut" style, or any 3D-animated anthropomorphic format)
- User says "run the animated video skill", "build this as an animated ad", "use Kling audio"
- Reference ad the user provides is in an animated style (not live-action, not UGC, not claymation)

Do NOT use for:
- Claymation / stop-motion → `claymation`
- Live-action replication → `video-scene-replicator`
- Veo 3.1-based animated pipeline (older) → `animated-video-replicator`
- Talking head / UGC → `aiugc-replicator`

## Pipeline Overview

```
INPUT: script + brief + brand
    ↓
[Stage 1] Strategist (Claude Opus 4.7, fallback Gemini 2.5 Flash)
          breaks script into scene beats, outputs shot_plan.json
          Per-shot adds: image_prompt, motion_prompt, dialogue_or_sfx (what Kling should vocalize)
    ↓
[Stage 2] Nano Banana 2 i2i (gemini-3.1-flash-image-preview)
          N animated-style keyframes. pure_i2i: true on product shots.
          from_bytes reference attachment (NOT from_image).
    ↓
[APPROVAL GATE 1] — review stills before Kling credits
    ↓
[Stage 3] Kling 3.0 via kie.ai with sound=True
          Each clip includes:
            - Visual motion (animated style)
            - Character dialogue / narration (Kling native audio gen)
            - Ambient SFX / music if specified in prompt
          5s per clip default, 9:16, pro mode.
          Prompt template includes native audio directives:
            "Character narrates: '{shot.dialogue_line}'."
            "Ambient sound: {shot.sfx_direction}"
          Organic cues still apply for realism.
    ↓
[Stage 4] SKIPPED — audio is baked into Kling clips
    ↓
[Stage 5] FFmpeg stitch
          Kling clips already have synced audio.
          Simple concat (no separate VO mix) — optionally light crossfade between clips.
    ↓
[OPTIONAL Stage 6] HyperFrames polish
          Extract audio from final.mp4, whisper-transcribe for captions,
          overlay word-synced captions + scene FX. Re-render final_polished.mp4.
    ↓
OUTPUT: b-roll/{brand}/{CONCEPT_CODE}/final.mp4
```

## Required Inputs

1. **Script / brief** — or explicit scene beats (same format as claymation)
2. **Brand** — Motilli, Lunessa, Velantra-*, etc.
3. **Concept code** — `ANGLE-ANIM-##` (e.g. `GG-ANIM-01` for Gut Gridlock animated v1)
4. **Reference ad URL** — optional, to extract style + character cues if you want to replicate a specific look

## Optional Flags

- `--no-gates` — skip approval gates
- `--images-only` — stop after Stage 2
- `--voice-style` — pass a voice style hint for Kling audio (e.g. "warm female narrator, 40s, conversational", "kid-friendly energetic", "clinical doctor"). Kling doesn't expose named voices, but style cues shape the generated audio.
- `--crossfade` — add a 0.25s crossfade between clip boundaries (default: hard cut)

## Concept Code Convention

**`ANGLE-ANIM-##`** — 2-3 letter angle + `ANIM` + sequential version.

Examples: `GG-ANIM-01` (Gut Gridlock animated v1), `HH-ANIM-01` (Heart Health animated v1).

## Shot Plan Schema (extends claymation)

New fields specific to this skill:

```json
{
  "shot_number": 1,
  "purpose": "Hook",
  "duration_seconds": 5,
  "image_prompt": "visual description for Nano Banana",
  "motion_prompt": "how the scene moves",
  "dialogue_line": "exact words Kling should speak this shot (narrator VO or character dialogue)",
  "voice_style_hint": "warm female narrator, 40s, conversational",
  "sfx_direction": "ambient kitchen sounds, subtle stomach rumble",
  "has_product": false,
  "pure_i2i": false
}
```

The Kling payload merges these into a single prompt:
```
{animated_style_block}. {motion_prompt}. {organic_cues}.
Narration: {voice_style_hint} says "{dialogue_line}". Ambient: {sfx_direction}.
```

## Animated Style Block

Prepended to every non-i2i image prompt:

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

(User will refine this block based on the reference ad once it's accessible via swipe file.)

## Kling Payload (native audio)

```python
payload = {
    "model": "kling-3.0/video",
    "input": {
        "prompt": full_prompt_with_dialogue_and_sfx,
        "image_urls": [image_url],
        "sound": True,                       # ← KEY DIFFERENCE
        "duration": "5",
        "aspect_ratio": "9:16",
        "mode": "pro",
        "multi_shots": False,
    }
}
```

## Critical SDK Notes

Same as `claymation`:
- Use `types.Part.from_bytes(data=bytes, mime_type='image/png')`, NOT `from_image` (doesn't exist)
- Convert webp references to PNG before passing
- Product shots use `pure_i2i: true` with canonical reference injected

## Dependencies

- `ffmpeg` + `ffprobe` on PATH
- API keys in `~/Documents/marketing brain/.env`: `GEMINI_API_KEY`, `KIE_API_KEY`, `ANTHROPIC_API_KEY` (no ELEVENLABS_API_KEY required)
- `pip install`: `google-genai`, `pillow`, `requests`, `anthropic`

## Costs per finished ad

- Nano Banana 2: ~$0.08 per shot
- Kling 3.0 with audio: ~$0.70 per shot (audio-enabled clips cost more than silent)
- HyperFrames render: free (local)
- **Total: ~$6.50 for 9 shots, ~8–15 min wall clock**

## Output Directory

Same layout as claymation:
```
~/Documents/marketing brain/b-roll/{brand_lowercase}/{CONCEPT_CODE}/
├── script/shot_plan.json
├── images/shot_NN.png
├── clips/shot_NN.mp4          # already has native Kling audio
├── final/final.mp4            # simple concat, no separate VO mix
└── hyperframes/ (optional)
```

No `audio/voiceover.mp3` directory — audio lives in the clips.

## Reference Ads to Study

User will supply GetHookd URLs. The animated format typically follows one of:

1. **Inside-the-body mechanism** (Serene Herbs "inside the gut" style) — anthropomorphic organ characters interacting with ingredients
2. **Product-as-character** — the product itself is personified, has dialogue
3. **Avatar journey** — stylized 3D avatar going through problem → discovery → relief arc

Pending user reference: GetHookd ad `79289275` (not in swipe file yet — add it for style extraction).

## Execution

```bash
python3 ~/.claude/skills/animated-video/pipeline.py \
    --brand Motilli --concept GG-ANIM-01 \
    --script "brands/motilli/scripts/gut_gridlock.md" \
    --brief "inside-the-gut mechanism ad with anthropomorphic bacteria characters" \
    --no-gates
```

## Status

Skill scaffolded — `pipeline.py` forthcoming once the reference ad `79289275` is accessible. The scaffold inherits everything from the `claymation` skill's `pipeline.py` except:
1. Strategist prompt instructs 3D-animated style (not clay)
2. Shot plan schema adds `dialogue_line`, `voice_style_hint`, `sfx_direction`
3. Kling payload uses `sound: True`
4. Stage 4 (ElevenLabs) is skipped
5. Stage 5 stitch is simple concat (+ optional crossfade), no VO mix

---
name: aiugc-longform
description: Long-form continuous-shot AIUGC factory. Produces 60-180s single-shot creator-talking-head VSL ads in the GetHookd "HurAgain" style — one creator, one continuous setting, one continuous voiceover, hook overlay text burned in for the first 8s. Solves the 15s clip cap of Seedance/Kling by cutting ONE continuous pre-rendered voiceover into N×~8s chunks at sentence boundaries, lip-syncing a clip to each chunk, then laying the original unbroken VO back over the assembled video so the finished ad is one take. Every clip seeds from the same avatar keyframe, never from the previous clip, because chaining drifts identity and background. Use when the user says "long-form UGC", "VSL-style talking head", "60-180s continuous yapper", or wants to replicate ads like the joint-pain / menopause / supplement single-shot creator pieces from GetHookd. Distinct from aiugc-infinite (that one is two-cut creator-talking + product-action; this one is single-shot continuous).
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# AIUGC Longform

Single-shot continuous talking-head VSL ad factory. Produces 60-180s creator-style yapper ads as one continuous audio + visually-stitched chain of N short clips. Designed against the HurAgain (Joint Pain Experts 2025) reference pattern: one creator, one continuous setting, one continuous voiceover, no B-roll, no scene cuts, hook text overlay pinned to the first 8s.

## Why a separate skill from `aiugc-infinite`

- `aiugc-infinite` = two-cut (creator-talking → product-action). Each ad ~13s.
- `aiugc-longform` = single-shot continuous talking head. Each ad 60-180s.

Different format, different bottleneck. Long-form has to defeat the **15s clip cap** of every video model in the catalog. We do that by:
1. **Rendering ONE continuous voiceover** for the entire script in a single TTS call, with word timestamps.
2. **Chunking that audio** at sentence boundaries into N clips of ~15s (fewer segments = fewer seams = less identity drift).
3. **Generating each video segment** lip-synced to its own audio chunk, seeded from the avatar keyframe.
4. **Stitching** the video and laying the ORIGINAL continuous VO over the whole thing, discarding every clip's own audio.
5. **Burning** the hook overlay (red badge, white bold text) on the first 8s via FFmpeg `drawtext`.

## THE ONE-TAKE AUDIO LAW (long-form only — read before choosing an engine)

**The finished audio must be one unbroken take. The video is assembled; the audio never is.**

This is THE thing that separates a long-form ad that sounds like one person talking from one that
sounds like a stitched-together robot, and it is not fixable downstream. Per-clip generated audio
means every segment is an independent performance with its own pitch contour, pace, energy and room
tone. At two or three beats nobody notices. At twenty-plus beats across three or four minutes, every
join is audible as a reset — the listener hears the speaker "restart" even when no word is damaged
and no gap exists. Measured on a real 24-segment build: word accuracy 0.998, seam gaps 57ms against
40ms for natural pauses, and it still sounded broken, because the defect is prosody and no audio
metric detects it.

Chunking cannot rescue this. Sentence-safe boundaries stop words being severed mid-phrase (do that
too, see below) but take 2 still is not the continuation of take 1, because it never was.

**Engine eligibility follows directly.** A long-form engine MUST accept a supplied audio track to
lip-sync against:

| Engine | Audio reference | Long-form eligible |
|---|---|---|
| Seedance 2.0 (kie.ai) | `reference_audio_urls` | **yes** |
| Google Omni | standalone audio input is gated by the API; the video-input workaround intermittently 400s | **no — short ads only** |

Omni is excellent for 2-3 beat ads where per-clip audio is inaudible as seams. It structurally cannot
produce a seamless four-minute single-shot piece, and picking it for one guarantees the failure above
no matter how good the chunking, trimming or stitching is.

**The per-clip native-audio rule in `omni-ugc` applies to SHORT multi-beat ads and does not override
this.** Where the two conflict, long-form wins for long-form.

Marketing Studio Video is **not** in this pipeline — its hook+setting features are redundant when the hook is a burned-in overlay and the setting comes from the avatar keyframe.

## Core Pipeline

```
Brand brief + count N
  |
  v
[1] Opus generates N VSL scripts (90-180s each)
       Strict arc: hook → 3am-wakeup agitation → authority subversion → mechanism → solution → CTA
  |
  v
[2] Resolve avatar keyframe (1 PNG anchor)
       Source: --avatar <path>  |  cached --soul-id  |  Nano Banana 2 i2i fallback
  |
  v
[3] For each VSL script (loop):
       a. Render the WHOLE script as ONE continuous VO with word timestamps → vo_full.wav
             This single take is the finished ad's audio. Nothing downstream re-generates it.
       b. Split vo_full.wav at SENTENCE boundaries into N chunks of ~8-15s → chunk_i.wav
             Never split a sentence. Over-long sentence → split at a comma. An under-filled
             chunk is fine (trailing silence trims); a severed sentence is not.
       c. For each chunk i = 1..N:
            seedance_2_0 --start-image <avatar.png> --audio <chunk_i.wav>
                  --duration <D> --prompt='<motion + identity, NO dialogue text>'
                  → seg_i.mp4, lip-synced to chunk_i
            Seed every segment from avatar.png, NOT from the previous last frame. Chaining is
            a random walk: each clip inherits the prior clip's accumulated error with nothing
            pulling it back, and identity/background visibly drift by ~segment 10. Measured:
            background similarity 0.53 chained vs 0.86 unchained, and the chained figure
            declines steadily across the run while the unchained one stays flat.
       d. FFmpeg concat seg_1..N (video), then lay vo_full.wav over the whole thing,
             DISCARDING every clip's own audio. This is what makes it one take.
       e. FFmpeg drawtext: burn red-badge hook overlay text on top half, fade in 0-0.2s, fade out 7.6-8s
       → final_vsl_<n>.mp4
  |
  v
[4] Manifest + output dir
```

## Reference Pattern (HurAgain / Joint Pain Experts 2025)

See [references/huragain-pattern.md](references/huragain-pattern.md) for the full distilled analysis. TL;DR:
- Single continuous selfie phone shot, low-angle, eye-level → low chest framing
- Two settings work: kitchen with wooden cabinets (waist-up) OR parked car driver-seat (chest-up)
- Hook overlay: red rounded badge, bold white sans-serif, ~3 lines, pinned 0-8s
- Voice cadence: conversational, "rant" energy, slight breathlessness, hand gestures implied
- Script arc enforced word-by-word in the script generator's system prompt

## When to Use

- "Build me 5 long-form UGC ads for <brand>"
- "VSL-style talking head, 90-180s, single shot"
- "Replicate the HurAgain ad style"
- "Continuous yapper ads, one creator, no cuts"
- "Native iPhone selfie 2-3 minute ad"

Defer to other skills when:
- Two-cut creator + product-action → `aiugc-infinite`
- 15-30s short-form UGC → `rapid-vsl` (Kling-based) or `aiugc-orchestrator`
- Replicating a specific reference video → `aiugc-replicator`

## Required Inputs

When invoked, collect:

1. **Brand** — `huragain`, `lunessa`, `motilli`, `velantra-*`, `avelle`, `solorna`
2. **Count N** — number of VSLs to produce (default 3 for long-form; per-VSL cost is high)
3. **Concept seed** (optional) — angle/desire/hook style. If omitted, Opus invents from brand vault.
4. **Target duration** (optional) — `--duration 90|120|150|180` seconds. Default 120.
5. **Voice** — `--voice-id <elevenlabs_id>` OR `--clone-voice <audio_file>`. If omitted, picks brand-default from `registry.json`.
6. **Avatar** — `--avatar <path>` to a 9:16 portrait PNG of the creator OR `--soul-id <uuid>`. If omitted, generated from brand-default Nano Banana 2 i2i prompt.
7. **Hook overlay style** — auto-uses `red_badge` style by default; override with `--overlay-style none|red_badge|caption`.
8. **Aspect ratio** — `9:16` (default).
9. **Resolution** — `720p` (default), `1080p` for hero.
10. **Seedance mode** — `std` (default) or `fast` (cheaper, slight fidelity loss).

## Setup (one-time per fresh session)

```bash
higgsfield auth token              # check
higgsfield workspace status        # should be retail_guinea_pig_2000
higgsfield account status          # need ~350-450 credits per VSL
echo $ELEVENLABS_API_KEY           # required
```

## Step-by-Step Execution

### Step 1 — Generate VSL scripts

```bash
python3 scripts/generate_vsl_script.py \
  --brand <brand> \
  --count <N> \
  --duration <seconds> \
  --concept "<seed>" \
  --output output/run_<ts>/scripts.json
```

Returns array of strict-JSON scripts:
```json
[
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
]
```

### Step 2 — Resolve avatar keyframe

`scripts/resolve_avatar.sh <brand> [<override_path>]` returns a local PNG path.

Resolution order:
1. `--avatar <path>` flag → use as-is
2. `brands.<brand>.avatar_keyframe` cached path in registry → use
3. `brands.<brand>.soul_id` → generate keyframe via `higgsfield generate create soul_2 --soul-id <id>` and cache the PNG
4. Fallback: Nano Banana 2 i2i from a brand-default prompt template

The avatar PNG defines: who the creator is, what they're wearing, the setting/background. **All N segments inherit visual identity from this single PNG via last-frame chaining.**

### Step 3 — Per-VSL loop

For each script:

#### 3a. Render full continuous VO

```bash
python3 scripts/render_vo.py \
  --script "$VSL_SCRIPT" \
  --voice-id "$VOICE_ID" \
  --output "$VSL_DIR/vo_full.wav"
```

Calls `POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>/with-timestamps` to get word-level alignment.

#### 3b. Segment the VO

```bash
python3 scripts/segment_vo.py \
  --vo "$VSL_DIR/vo_full.wav" \
  --timestamps "$VSL_DIR/vo_timestamps.json" \
  --target-chunk-seconds 14 \
  --max-chunk-seconds 15 \
  --min-chunk-seconds 8 \
  --output-dir "$VSL_DIR/chunks/"
```

Splits at sentence boundaries (`.`, `?`, `!`) preferring chunks that fall in the 13-15s sweet spot (full Seedance segment length). Won't split mid-sentence unless a sentence exceeds max. Writes `chunk_001.wav` .. `chunk_NNN.wav` and `chunks_manifest.json`.

#### 3c. Render visual segments (Seedance i2v + audio role)

```bash
SEED="$AVATAR_PNG"
for chunk in $VSL_DIR/chunks/chunk_*.wav; do
  i=$(basename "$chunk" | grep -oE '[0-9]+')
  DUR=$(jq -r ".chunks[$((i-1))].duration_seconds | floor" "$VSL_DIR/chunks/chunks_manifest.json")
  bash scripts/render_segment.sh "$VSL_DIR/seg_$i" "$SEED" "$chunk" "$DUR" "$ASPECT" "$RES" "$MODE"
  SEED="$VSL_DIR/seg_$i/segment_lastframe.png"
done
```

Per-segment call:
```bash
higgsfield generate create seedance_2_0 \
  --prompt "$STILL_PROMPT" \
  --start-image "$SEED" \
  --audio "$CHUNK_WAV" \
  --aspect_ratio 9:16 \
  --duration "$DUR" \
  --resolution 720p \
  --mode std \
  --wait --json
```

`STILL_PROMPT` uses the Seedance UGC-anchor pattern (see `references/seedance-2-prompting.md`). **Keep it SHORT — Seedance artifacts more as prompt length grows; budget ≤ ~80 words total including any dialogue:**
> `UGC iPhone selfie video, locked-off, real-time pacing. Same woman as the reference image, no face morphing, no setting change, no music. Subject lip-syncs to provided audio — natural pauses, expressive intonation, energy held to the final word, never monotone. <duration>s, 720p, 9:16.`

When dialogue rides in the prompt (voice-anchor path), replace the lip-sync clause with: `She's animated and expressive, like FaceTiming her best friend about something huge that happened to her — voice rising and falling, stressing key words, speeding up and slowing down. Never monotone, never reading. She says: "<textured dialogue>". <ONE cue, ≤10 words>.` — plus a compact voice line (≤8 words) on segment 1 only; later segments inherit the voice from the anchor audio. Delivery direction is POSITIVE character framing — negations alone barely steer audio models. Never use backward-looking words ("remembering", "wistful") or flat register words ("composed", "steady", "even", "calm") — the former cue drift-off, the latter cue monotone. **Segment-1 casting call: generate 3 takes, pick the most alive as the anchor; if all 3 read flat, switch to the `--audio` ElevenLabs path (Step 3a) — deterministic performance, Seedance just lip-syncs.**

**Dialogue naturalness (mandatory when dialogue is in the prompt instead of `--audio`):** never pass clean written-English script text — it produces teleprompter cadence. Texture the chunk for speech first: contractions everywhere; comma-framed verbal texture only (~1 disfluency per 2 chunks, e.g. "Mild, right?" — never on mechanism terms, numbers, product name, or dosage); add a per-chunk vocal cue (voice drops / pace picks up / beat before X). **Dialogue punctuation: commas and periods ONLY — no ellipses, no em-dashes; the model renders them as dead-air pauses in the video.** Intentional beats go in the cue, not the text. Segment 1 locks the voice anchor, so gate it: if segment 1 sounds read, regenerate before chaining. Full spec: `_engine/sops/Segment-Brief-SOP.md` §5.

**Tonal consistency (anti-monotone/anti-drift):** the known AI voice failure is up-tempo open → back half decays to monotone, compounding across the chain. Counters, all mandatory: (1) one named base register restated verbatim in every chunk prompt, with per-chunk deviations as small shades ("warmth lifts"), never gear changes; (2) "Expressive natural intonation... no monotone" + "Energy holds through the final word of the clip — no trailing off, no fading to flat" in every prompt; (3) all segments 2..N anchor to SEGMENT 1's audio, never the previous segment's; (4) QA every clip's LAST sentence for energy fade and regenerate faded segments before chaining — never let the next segment seed from a faded one; (5) A/B first vs mid vs final segment for register drift.

#### 3d. Stitch + audio replace + overlay burn

```bash
bash scripts/stitch_vsl.sh \
  "$VSL_DIR" \
  "$VSL_DIR/vo_full.wav" \
  "$HOOK_OVERLAY_TEXT" \
  "$HOOK_OVERLAY_STYLE" \
  "$VSL_DIR/final.mp4"
```

What it does:
1. `concat` all `seg_*/seg.mp4` into one continuous video (no audio).
2. Mux in `vo_full.wav` as the audio track (drops every segment's individual audio — replaced wholesale).
3. Apply `drawtext` filter: red rounded box, white bold sans-serif, centered upper-third, fade in 0→0.2s, hold to 7.8s, fade out 7.8→8.0s.

### Step 4 — Manifest

Each finished VSL gets an entry in `manifest.json`:
```json
{
  "vsl_id": "vsl_001",
  "brand": "huragain",
  "duration_seconds": 118,
  "segments_count": 14,
  "voice_id": "...",
  "avatar_path": "avatars/huragain_kitchen.png",
  "hook_overlay_text": "...",
  "credits_used_seedance": 308,
  "elevenlabs_chars_used": 1840,
  "final_path": "vsl_001.mp4",
  "timestamp": "2026-05-08T..."
}
```

## Cost Discipline

Per finished 120s VSL:
- ElevenLabs TTS (1800 chars): ~$0.10-0.30
- Seedance 2.0 (15 segments × 8s × ~22cr): **~330 Higgsfield credits**
- Avatar keyframe (one-time per brand or per run): ~5 credits

For a batch of N=3 VSLs at 120s each: **~990 credits + 100 buffer ≈ 1100 credits**. Confirm with user if `balance < N × 330 × 1.2`.

Reduce cost:
- `--seedance-mode fast` (~25% off)
- `--duration 90` instead of 120 (~25% fewer segments)
- `--resolution 480p` for first iteration

## Output Structure

```
output/run_<brand>_<ts>/
├── scripts.json
├── manifest.json
├── vsl_001/
│   ├── script.json
│   ├── vo_full.wav
│   ├── vo_timestamps.json
│   ├── chunks/
│   │   ├── chunk_001.wav
│   │   ├── chunk_002.wav
│   │   ├── ...
│   │   └── chunks_manifest.json
│   ├── seg_1/
│   │   ├── seg.mp4
│   │   ├── seg_job.json
│   │   └── segment_lastframe.png
│   ├── seg_2/...
│   └── final.mp4    (← THIS is the deliverable)
├── vsl_001.mp4 (symlink/copy of vsl_001/final.mp4 for convenience)
├── vsl_002/...
└── vsl_003/...
```

## Failure Modes & Guardrails

- **Avatar drifts mid-VSL** → late segments don't look like early ones. Fix: shorter segments (6s instead of 8s), prepend `maintain exact appearance, no morphing` to every segment prompt, or burn-in a Soul ID. Audit drift via `scripts/audit_identity.sh` (planned).
- **Lip-sync misses on a segment** → Seedance occasionally drops lip-sync if the audio chunk has long silence at the start. Fix: trim leading silence from each chunk (`segment_vo.py` does this).
- **Audio seams between segments / "the segments don't flow into each other"** → the single most common long-form failure, and the reason the One-Take Audio Law exists. Caused by generating audio per clip, so every segment is a separate performance. Symptom: each join sounds like the speaker restarting, even with clean words and no measurable gap. NOT fixable by chunking, trimming, crossfading or re-encoding — verified on a 24-segment build that scored 0.998 word accuracy and still sounded wrong. Fix: render one continuous VO and replace every clip's audio with it at stitch. If the engine cannot lip-sync to supplied audio, the engine is wrong for long-form.
- **Beats that split a sentence** → each clip is its own performance and the model is told to stop and hold silence after its final word, so it delivers terminal falling intonation wherever the beat ends. Split "needs more push every / time." and it reads as a dropped word however clean the audio is. Chunk at sentence boundaries only; break an over-long sentence at a comma, never at an arbitrary word. An under-filled beat is the acceptable failure (trailing silence is trimmable); a severed sentence is not.
- **Hook overlay clips into the creator's face** → `red_badge` placement is upper-third (y=h*0.18); for tall framing, override with `--overlay-y <pixels>`.
- **Sentence overruns 12s** → segmenter splits at next-best comma boundary, with logging.
- **ElevenLabs rate limit (429)** → 3-attempt backoff at 5s/15s/30s.

## CLI Surface Used (Reference)

| Step | Command |
|---|---|
| Avatar keyframe (Nano Banana 2 i2i) | `higgsfield generate create nano_banana_2 --prompt ... --image <ref> --aspect_ratio 9:16 --resolution 2k --wait --json` |
| Avatar keyframe (Soul 2.0) | `higgsfield generate create soul_2 --prompt ... --soul-id <uuid> --aspect_ratio 9:16 --wait --json` |
| ElevenLabs TTS w/ timestamps | `POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>/with-timestamps` |
| Seedance per segment | `higgsfield generate create seedance_2_0 --start-image <seed> --audio <chunk> --duration <D> --aspect_ratio 9:16 --resolution 720p --mode std --wait --json` |
| Frame extract | `ffmpeg -sseof -0.25 -i seg.mp4 -vframes 1 lastframe.png` |
| Stitch + replace audio + overlay | `ffmpeg -i concat:... -i vo_full.wav -filter_complex "drawtext=...:fade=..."` |

## Quickstart

```bash
# 3 VSLs for Lunessa, 120s each, brand-default voice + auto-generated avatar
bash scripts/run.sh --brand lunessa --count 3 --duration 120

# 1 VSL for HurAgain in 9:16 with explicit avatar + voice + concept
bash scripts/run.sh \
  --brand huragain \
  --count 1 \
  --duration 150 \
  --avatar avatars/huragain_kitchen.png \
  --voice-id 21m00Tcm4TlvDq8ikWAM \
  --concept "I tried 14 supplements before this one finally worked"

# Dry-run (script + cost preflight, no jobs)
bash scripts/run.sh --brand lunessa --count 2 --duration 90 --dry-run
```

## Memory Hooks

After a successful run, persist to `registry.json`:
- `brands.<brand>.avatar_keyframe` → cache the working PNG path
- `brands.<brand>.voice_id` → if user provided a winning voice
- `brands.<brand>.winning_vsl_ids` → for future remixes

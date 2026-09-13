---
name: ugc-forge
description: Consistent, correctly-voiced UGC video ads from one script. Auto-segments an ad script into <=8s beats, voices every beat with ONE ElevenLabs voice (with a pronunciation lexicon so brand terms are never mispronounced), then generates the video with Veo 3 image-to-video SEQUENTIALLY using FRAME CHAINING — each segment starts from the previous segment's final frame, so the creator, wardrobe, lighting, and setting carry forward and cuts are seamless (no drift, no re-rolls). Veo native audio is disabled; ElevenLabs is the only speech source and the video is conformed to the audio. Talking-head segments get a pluggable lip-sync conform pass; b-roll segments just mux the VO. Outputs a single 9:16 MP4 (optional 4:5/16:9), all intermediate clips, per-segment audio stems, and a run manifest for reproducible, selective re-runs. Supports --reanchor-every N for drift control and --variations to run the identical script + identical audio across multiple creator faces. Use when the user says "make a UGC ad from this script", "stitch these clips consistently", "my segments keep drifting", "the AI keeps mispronouncing the brand name", or "run ugc-forge".
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# ugc-forge

One tool: script in → one consistent, correctly-voiced UGC MP4 out. It fixes the two
things that break a clip-by-clip workflow.

**Problem 1 — visual drift.** Generating each ~8s clip independently lets the person,
wardrobe, lighting, and setting wander between clips, forcing endless re-rolls.
**Fix — frame chaining.** Segments are generated *sequentially*: segment 1 is
image-to-video from your reference still; we extract its **final frame** and use it as
the **start frame** of segment 2; repeat down the whole script. Every segment begins
exactly where the last one ended, so identity/wardrobe/lighting/setting carry forward and
the cuts are seamless. Reinforced by a fixed **style anchor** appended to every prompt, a
fixed **negative prompt**, and a fixed **seed** on every call.

**Problem 2 — mispronunciation.** Generated speech mangles brand terms.
**Fix — ElevenLabs + lexicon.** All speech comes from one ElevenLabs `voice_id` (identical
across every segment and every creator variation). A pronunciation lexicon (JSON) rewrites
tricky words to phonetic respellings or SSML `<phoneme>` tags **before** synthesis, so the
fix is deterministic. Veo's native audio is **disabled and never used**. Each segment's
ElevenLabs audio duration (via ffprobe) is the **target** length; the video is conformed to
the audio — the audio is never stretched, trimmed, pitch-shifted, or re-encoded.

## Pipeline

```
parse inputs (script/JSON, reference still, voice_id, lexicon, aspect, settings)
  -> segment script into <=8s beats (sentence/breath boundaries only)
  -> ElevenLabs: synth each beat (apply lexicon), measure duration with ffprobe
  -> Veo 3 image-to-video, SEQUENTIAL + frame-chained:
        seg1 from reference still; extract last frame; seg2 from that frame; ...
        native audio OFF; fixed seed + fixed negative prompt + style anchor
        conform each clip to its audio duration
  -> lip-sync conform (talking_head:true) OR mux VO over visuals (b-roll)
  -> concat all segments -> one continuous MP4
  -> outputs: final MP4 (9:16 + optional 4:5/16:9), segment clips, audio stems, manifest
```

## CLI

```bash
python3 scripts/ugc_forge.py \
  --script ad.txt --avatar creator.png --voice <eleven_voice_id> \
  --lexicon examples/pron.example.json --aspect 9:16 \
  --reanchor-every 4 --out ad.mp4
```

Pre-segmented input, alt aspects, and multi-creator variations:

```bash
python3 scripts/ugc_forge.py \
  --manifest examples/segments.example.json \
  --avatar creatorA.png --avatar creatorB.png --variations \
  --voice <eleven_voice_id> --aspect 9:16 --also-aspect 4:5 --also-aspect 16:9 \
  --out ad.mp4
```

`--variations` runs the **identical** script + **identical** ElevenLabs audio across each
`--avatar`, writing one labeled MP4 per creator (`ad__creatorA.mp4`, `ad__creatorB.mp4`).

### Key flags

| flag | purpose |
|------|---------|
| `--script` / `--manifest` | raw `.txt` to auto-segment, or pre-segmented `{segments:[{line,visual,talking_head}]}` |
| `--avatar` | creator reference still (repeatable → variations) |
| `--voice` | ElevenLabs `voice_id` (identical everywhere) |
| `--lexicon` | pronunciation JSON (respelling or `<phoneme>` spec) |
| `--settings` | style-anchor overrides (see `examples/settings.example.json`) |
| `--aspect` / `--also-aspect` | master aspect (default 9:16) + extra exports (4:5 center-crop, 16:9) |
| `--reanchor-every N` | every N segments, re-seed from the ORIGINAL reference (pulls identity back to true) |
| `--reanchor-on-segment` | force a clean re-anchor at specific indices (hard scene change) |
| `--auto-drift` | also re-anchor when luma drift from the original ref is detected |
| `--lipsync-backend` | `omni` \| `wav2lip` \| `none` (see lip-sync below) |
| `--regen "2,5"` | force re-render of those segments; frame-chain dependents auto-included |
| `--face-index` | which face to lock if the reference has multiple |

## Bring your own ElevenLabs voiceover

You don't have to synthesize — if you've already rendered VO in ElevenLabs, feed
it in and ugc-forge builds a consistent video **synced to your audio**:

```bash
# one audio file per beat (sorted order; count must equal the script's beats)
python3 scripts/ugc_forge.py --script ad.txt --avatar creator.png \
  --audio-dir ./vo_stems --out ad.mp4

# OR one full-ad VO file, auto-split on silence at sentence gaps
python3 scripts/ugc_forge.py --script ad.txt --avatar creator.png \
  --voiceover full_vo.mp3 --vo-noise-db -30 --vo-min-gap 0.35 --out ad.mp4
```

Uploaded audio is the authoritative stem — copied in, never re-encoded; the video
is conformed to it and (talking heads) lip-synced to it. No `--voice` /
`ELEVENLABS_API_KEY` needed in this mode. If the audio count (or silence-split
count) doesn't match the script's beats, ugc-forge **stops and reports**. In the
UI this is the **Voiceover → Upload per beat / Upload full VO** toggle.

## Drift control

Chained frames can slowly accumulate color/exposure drift over many segments.
`--reanchor-every N` re-seeds from the **original** reference still every N segments
(and `--auto-drift` does so when measured luma drift crosses a threshold), pulling identity
back to true. `--reanchor-on-segment 6,12` forces clean re-anchors at hard scene changes.

## Lip-sync (pluggable)

Talking-head segments need the mouth to match the **ElevenLabs** waveform, not Veo's
discarded native speech. The lip-sync pass is a registry of backends
(`scripts/lipsync.py`):

- **`fal` (default, works out of the box)** — Sync.so's lip-sync model hosted on fal.ai,
  via `scripts/lipsync_fal.py`. Uses the `FAL_API_KEY` already in your vault `.env` — no
  local ML, no SDK, no GPU. It uploads the (audio-conformed) clip + the ElevenLabs stem to
  fal storage, runs the job, downloads the result, and **re-muxes your exact stem** so the
  delivered audio is pristine. Model overridable via `UGC_FAL_LIPSYNC_MODEL`. *(Verified
  live: upload → submit → poll → result round-trip against `fal-ai/sync-lipsync`.)*
- `omni` — Google Omni audio-conditioned avatar, wired via `UGC_OMNI_CMD` (shell template
  with `{video} {audio} {out}`).
- `wav2lip` — wav2lip-style model, wired via `UGC_WAV2LIP_CMD`.
- `none` — mux only.

If a backend is unavailable or a call errors mid-run, ugc-forge **falls back to a plain
mux** so the correct, duration-synced audio is always present, and **logs** that mouths
weren't driven (it never silently pretends). B-roll segments (`talking_head:false`) skip
lip-sync and just mux the VO.

## Re-run economy

A run writes `<out>.manifest.json` (segments, prompts, seeds, durations, start-frame
sources, SynthID note). On re-run:

- **Changed lines are auto-detected** (text + lexicon hash) and only those audio stems are
  re-synthesized; unchanged stems are reused.
- **`--regen "i,j"`** forces a video re-roll of those segments. Because of frame chaining,
  regenerating segment *i* invalidates *i+1, i+2, …* **up to the next re-anchor** — those
  dependents are auto-included so the chain stays seamless. Everything before *i* and after
  the next anchor is reused untouched. Fixing one line never re-renders the whole ad.

If re-segmentation changes the segment count vs the prior manifest, ugc-forge **stops and
reports** (pass `--resegment` to accept the new segmentation) rather than guessing.

## Guardrails

- ElevenLabs is the **only** speech source; Veo/native TTS is never used.
- No on-screen text/captions are baked into generation (add in post).
- Audio-vs-script segment-count mismatch → **stop and report**, never guess.
- A safety-filtered or empty Veo call → retry once reworded, then **log and skip** that
  segment (excluded from the final cut) rather than crashing the batch.
- Gemini + ElevenLabs rate limits are handled with exponential backoff.
- A reference image with >1 face → **stop** and ask for `--face-index` before starting
  (requires `opencv-python`; without it, detection is skipped with a warning).
- Veo outputs carry an invisible **SynthID** watermark — noted in the manifest.

## UI (easiest way to run it)

A zero-dependency local web app wraps the CLI — no pip install, stdlib only.

```bash
./ui/run.sh          # or: python3 ui/server.py   -> opens http://127.0.0.1:8765
```

In the browser: paste the script (or pre-segmented JSON), drop in one or more
creator stills (2+ auto-enables variations), set the ElevenLabs `voice_id`, add
lexicon words, and tune drift/output/engine options. Two buttons:

- **Preview segments · free** — runs `--plan-only`: shows every beat, its
  estimated length, talking-head vs b-roll, the lexicon-applied VO text, and the
  exact Veo prompt. **Makes no API calls** — iterate on segmentation for free.
- **Forge video** — runs the full pipeline; logs stream live into the console and
  the finished MP4 (plus alt aspects + downloadable manifest) plays inline.

Each run is isolated under `ui/runs/<job_id>/` (gitignored). Internet is only
needed for **Forge** (Veo + ElevenLabs); the UI itself and **Preview** are local.

## Setup

```bash
pip3 install -r requirements.txt        # google-genai, requests (+ optional opencv-python)
# ffmpeg/ffprobe on PATH; keys in the vault .env: GEMINI_API_KEY, ELEVENLABS_API_KEY
```

Keys are read from the environment / vault `.env` only — never passed as flags, never
logged. See `references/USAGE.md` for a full walkthrough and the manifest schema.

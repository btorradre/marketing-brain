---
name: seedance-brief-runner
description: Executes a Segment-Brief-SOP production brief through Seedance 2.0 — compiles the brief's segment map into segments.json, runs the segment-1 casting call, locks the voice anchor, generates all segments with last-frame chaining (product keyframe overrides included), and stitches final.mp4. Use when the user says "generate the segments", "run the brief", "fire the pipeline", "run the Ellen brief", "seedance run", "build the video from the brief", or wants any MOT/LUN/other-brand segment brief actually produced instead of doing the Higgsfield CLI calls manually. Companion to the Segment-Brief-SOP (_engine/sops/Segment-Brief-SOP.md): the SOP defines the brief, this skill executes it.
disable-model-invocation: false
---

# Seedance Brief Runner

Turns a finished segment brief (Segment-Brief-SOP format) into a finished video. You (Claude) compile the brief into a machine manifest — the judgment work — then `scripts/run_brief.py` executes it deterministically: casting, anchoring, chaining, stitching, resuming.

## Preflight (once per session)

All generation goes through the **official higgsfield CLI** — never the Higgsfield MCP tools (the MCP is for interactive one-offs; the CLI is scriptable, resumable, and what the runner shells out to).

```bash
export SSL_CERT_FILE=$(python3 -m certifi 2>/dev/null)   # known requirement — CLI dies on SSL verify without it
higgsfield auth token                                     # if expired: higgsfield auth login (CLI dies mid-run on expired sessions — check FIRST)
higgsfield workspace status                               # should be retail_guinea_pig_2000
higgsfield account status                                 # enough credits (~2.75cr/sec of video)
command -v ffmpeg && command -v ffprobe && command -v jq && command -v curl
```

**Known CLI failure modes:** (1) expired session → every generate call 401s; re-auth (`higgsfield auth login`) then resume with `run` (done segments skip automatically). (2) missing SSL_CERT_FILE → TLS errors on upload/download; export it before the runner. The runner surfaces the CLI's stderr on failure — read it before retrying.

Budget math: total video seconds × ~2.75cr + casting takes (takes × seg1_duration × 2.75). A 10×~14s brief with a 3-take cast ≈ 400 + 125 ≈ **~525 credits**. Confirm with the user if balance is close.

**MODE RULE (Brooks 2026-07-06): ALWAYS normal Seedance 2.0 (`--mode std`), 9:16, 720p. `fast` mode is BANNED — it produces visible distortion (warped hands, melted faces under motion). If the balance can't cover a std run, STOP and ask for a top-up; never silently downgrade to fast to fit budget.**

## Step 1 — Ensure keyframes exist

The brief names an avatar keyframe spec and (usually) a product keyframe spec:

- **Avatar keyframe**: if no PNG exists yet, generate per the brief's spec (`higgsfield generate create gpt_image_2 --prompt "<spec>" --aspect_ratio 9:16 --wait --json`, or `soul_2` with a cached soul-id). Save into the concept folder (`<CONCEPT>/keyframes/avatar.png`).
- **Product keyframe**: ALWAYS pure i2i composite from the brand's canonical product reference (per `feedback_product_shots_i2i`) — **`gpt_image_2` (NEVER Nano Banana — Brooks 2026-07-06: all i2i uses GPT Image 2)** with `--image <avatar/context ref> --image <canonical product ref>`. Never let Seedance invent the product.

Show both keyframes to the user before spending on video segments.

## Step 2 — Compile the brief → segments.json

Read the brief and write `<CONCEPT>/output/segments.json`. This is the judgment step.

**CANONICAL FORMAT (2026-07-06): UGC-Director mode.** Compile each segment's prompt per `_engine/standalone-skills/UGC DIRECTOR.md` (skill: `seedanceugcdirector`) — dense timestamped 3×5s blocks (Camera / verbatim Creator block / Right hand / Left hand / Face / In frame / Not in frame / Light / Background) + Audio line (voice character, room tone from the skill's library, filler-heavy dialogue). Set the full text as the segment's `"prompt"` field — the runner uses it verbatim. Rules:

1. Every segment still carries `index`, `duration`, `dialogue` (the spoken line only, for validation + captions) alongside `prompt`.
2. **House style hard-fails:** no ellipses or em dashes anywhere in `prompt` or `dialogue` (runner enforces). No hyphens (rephrase), numbers as numerals, the word "cinematic" never.
3. `reference_images` (manifest-level) and per-segment `images` become `--image` flags in order — **@Image numbering in prompts must match that attachment order.** Typical: @Image1 = creator/avatar, @Image2 = product.
4. The verbatim Creator block is IDENTICAL across all blocks of all segments — that plus @Image1 is the identity mechanism (on top of last-frame chaining).
5. Product/special segments: `start_image` (composite keyframe) + product acting beats in the hand/In-frame slots.
6. Optional ElevenLabs mode: `audio_chunk` per segment — runner passes it as `--audio` instead of the seg-1 anchor.

(Legacy mode: manifests with `prompt_template` + `deviation`/`cue` tokens still run, for old briefs.)

Manifest skeleton:

```json
{
  "concept_id": "MOT-ELLEN-RUPTURE-UGC-01",
  "output_dir": "/abs/path/<CONCEPT>/output",
  "avatar_keyframe": "/abs/path/<CONCEPT>/keyframes/avatar.png",
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "mode": "std",
  "voice_line": "Voice: woman early 50s, warm, low, casual American accent.",
  "prompt_template": "UGC iPhone selfie video, locked-off, real-time pacing. Same woman as the reference image, no face morphing, no setting change, no music. She's animated and expressive, like FaceTiming her best friend about something huge — talking with her hands, eyebrows and face acting out her words, big natural mouth movement, voice rising and falling in quick bursts with crisp beats. Never monotone, never reading, never still. <DEVIATION>. She says: \"<DIALOGUE>\". <CUE>.<EXTRA> <DURATION>s, 720p, 9:16.",
  "segments": [
    {"index": 1, "duration": 15, "dialogue": "...", "deviation": "urgent hush, building", "cue": "leans in, breath before the final line"},
    {"index": 8, "duration": 15, "dialogue": "...", "deviation": "plain, direct, no ad-voice", "cue": "raises jar label to lens, lowers it at the end", "start_image": "/abs/path/keyframes/product.png", "extra_prompt": "no warping hands, keep label perfectly readable."}
  ]
}
```

## Step 3 — Casting call (MANDATORY, never skip)

```bash
python3 "<skill_dir>/scripts/run_brief.py" cast --manifest <segments.json> --takes 3
```

Present the 3 take paths to the user — THEY pick by ear (most alive delivery, energy held to the final word, no teleprompter). Then:

```bash
python3 "<skill_dir>/scripts/run_brief.py" set-anchor --manifest <segments.json> --take <n>
```

If the user says all 3 are flat: do NOT keep rolling takes past ~2 rounds — switch to the ElevenLabs fallback (brief's fallback section; `elevenlabs-agent` skill renders the VO, chunk at segment boundaries, recompile manifest with `audio_chunk` per segment).

## Step 4 — Run + stitch

```bash
python3 "<skill_dir>/scripts/run_brief.py" run    --manifest <segments.json> --from 2
python3 "<skill_dir>/scripts/run_brief.py" stitch --manifest <segments.json>
```

Runner behavior you can rely on:
- Chains seg i from seg i-1's `segment_lastframe.png`; `start_image` overrides for product segments.
- Segments 2..N all `--audio` the SEG-1 anchor (never the previous segment) — drift can't compound.
- Existing segments are skipped → re-running `run` resumes after a crash.
- `--only N` regenerates one segment (warns that N+1.. were seeded from the old last frame).
- Hard-fails on ellipses/em-dashes in dialogue and warns on prompts >110 words.

## Step 5 — QA before delivering

Walk the brief's QA gates: identity seg1 vs final, END-of-segment energy on every clip (fade = regenerate that segment), tonal A/B (first/mid/last), broll-auditor on the product segment, lip-sync spot checks, runtime bounds. Report the final.mp4 path + a manifest of what was generated and credits spent (`higgsfield account status` delta).

## Notes

- This skill EXECUTES briefs; it does not write them. If no brief exists, run the concept through the Segment-Brief-SOP flow first (ad-watcher teardown → script → blacklist audit → segment map).
- Non-Velantra brands only by default (Velantra concepts have their own skills).
- Reference implementation brief: `brands/motilli/creative/MOT-ELLEN-RUPTURE-UGC-01/MOT-ELLEN-RUPTURE-UGC-01-brief.md`.

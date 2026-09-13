---
name: seedance-prompt-architect
description: Turn any reference video into a copy-paste PROMPT PACK for manual asset generation — it does NOT generate anything. Watches a reference ad via the /watch skill, detects every hard cut, slices it into cut-aware segments (each ≤15s, ending at the cut), then for each segment writes the image prompts (UGC avatar, product keyframe / start-frame) AND an in-depth Seedance 2.0 image-to-video animation prompt. Product appears in prompts as a Higgsfield product tag like @straw tote. Brand/product agnostic. Use when the user says "build seedance prompts from this reference", "break this ad into segments and write prompts", "make me a prompt pack", "seedance prompting", or hands over a reference video + a product to replicate manually.
disable-model-invocation: false
allowed-tools: [Bash, Read, Write, Skill, AskUserQuestion]
---

# Seedance Prompt Architect

**This skill writes prompts. It does not generate images or video.** The output is a
`prompt-pack.md` the user takes into Higgsfield (or any tool) and generates from **by
hand**. There are zero API calls, no `higgsfield` CLI, no credits. If the user wants
automated end-to-end generation, route to `seedance-directors-cut` or `aiugc-infinite`
instead — this skill is deliberately the manual-workflow companion.

## What it produces

From one reference video it emits, per cut-aware segment:
1. **Image prompts** — the stills to generate first and feed as start frames:
   - **Avatar / creator image** (the UGC person's likeness) — generate once, reuse.
   - **Product keyframe** — the segment's start frame, with the product tagged as `@<product>`.
2. **A Seedance 2.0 video prompt** — the image-to-video animation prompt for that shot
   (concrete action verbs, one camera move, duration = the segment length, identity-lock
   negatives, ambient/audio cue), also tagging `@<product>` where the product appears.

Everything is copy-paste ready. The product token `@straw tote` = a product you've
registered in Higgsfield (Marketing Studio product / reference element); tagging it in the
prompt is how manual Higgsfield generation pulls in the real product. Swap the token for
any brand/product — the skill is generic.

## Core pipeline

```
reference video (URL or local) + product name + @token  [+ optional brand vault, avatar desc]
  |
  v
[1] /watch the reference   → frames (t=MM:SS) + timestamped transcript
  |
  v
[2] detect_cuts.py         → segments.json  (cut-aware, each ≤15s, ends at the cut)
  |
  v
[3] Per segment, read the frames in that time range and analyze the BEAT:
      shot type · subject · concrete action · camera move · on-screen text · audio
  |
  v
[4] Write prompt-pack.md:
      · ASSET PROMPTS (one-time): avatar image, product keyframe(s)
      · PER SEGMENT: start-frame image prompt + Seedance video prompt + continuity note
  |
  v
prompt-pack.md  (+ segments.json)   →  user generates everything manually
```

## Inputs to collect

When invoked, confirm:
1. **Reference video** — URL or local path (required).
2. **Product** — display name + the Higgsfield tag to use in prompts (e.g. name `Straw Birkin`, tag `@straw tote`). If the user only gives a name, propose a tag and confirm.
3. **Avatar / creator** (optional) — a description or an existing image path. If omitted, infer the creator from the reference frames and write an avatar prompt to recreate that likeness.
4. **Brand** (optional) — a `marketing brain/brands/<brand>/` folder. If given, load product references + voice/avatar docs for accuracy. The skill still works with no brand.
5. **Aspect ratio** — default `9:16`.

If any required input is missing, ask once with `AskUserQuestion`, then proceed.

## Step-by-step

### Step 1 — Watch the reference
Invoke the `watch` skill on the reference so you get frames + transcript. Run watch with a
**fixed working dir** so the downloaded video survives for cut detection:

```bash
python3 "${HOME}/.claude/skills/watch/scripts/watch.py" "<source>" \
  --out-dir "${CLAUDE_SKILL_DIR}/output/run_<ts>/watch"
```

(For a local file you can point cut detection straight at that path and still run watch for
the frames+transcript.) Read every frame path watch prints — you need the visuals, not just
the transcript. Note the video file watch saved in the working dir (`*.mp4`/`*.webm`).

### Step 2 — Detect cuts → segments
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/detect_cuts.py" \
  --video "<downloaded_or_local_video>" \
  --max 15 --output "${CLAUDE_SKILL_DIR}/output/run_<ts>/segments.json"
```
This finds hard cuts (ffmpeg scene detection) and slices into segments that each end at a
cut and never exceed 15s (a continuous shot longer than 15s is split at 15s). Tune
`--threshold` (lower = more sensitive to cuts) if the segment table under/over-splits vs
what you see in the frames. **You are the arbiter** — if the frames show a cut the detector
missed (or a "cut" that's really a whip-pan within one shot), correct the segment table by
hand before writing prompts, and say so in the pack.

### Step 3 — Analyze each segment's beat
For every segment, look at the frames whose `t=MM:SS` falls in `[start, end]` and record:
- **Shot type / framing** (selfie, medium, close-up product, POV hands, wide)
- **Subject** (creator, product, hands, environment)
- **Concrete action** — the physical thing happening (holds up bag, unzips, walks, points)
- **Camera move** — pick ONE primitive (handheld, locked-off, slow dolly in, pan, tracking hands)
- **On-screen text** (verbatim if legible) and its role
- **Audio** — what's said (from transcript) or ambient/SFX
- **Cut type** into this segment (hard cut, match cut, etc.)

### Step 4 — Write the prompt pack
Produce `prompt-pack.md` (see `references/prompt-pack.example.md` for the exact shape). Two
parts:

**A. Asset prompts (generate these first, reuse across segments)**
- **Avatar image prompt** — one image of the creator's likeness for identity lock. Follow
  `references/image-avatar-prompting.md`. If the user gave an avatar image, skip and note it.
- **Product keyframe prompt(s)** — hero/context stills that seed the animations, product
  tagged `@<product>`. Prefer transforming an existing product reference (image-to-image)
  over from-scratch generation when a brand folder is present.

**B. Per-segment prompts**
For each segment output a block with:
- **Start-frame IMAGE prompt** — the still to generate/transform that Seedance animates from.
  Name where it comes from: the avatar image, a product keyframe, or the previous segment's
  **last frame** (for a continuous-identity chain). Tag `@<product>` if the product is on screen.
- **Seedance VIDEO prompt** — the image-to-video animation. Follow
  `references/seedance-prompting.md` strictly:
  - `[UGC/context anchor] + [one concrete action verb on subject/@product] + [one camera move] + [identity-lock + negatives]`
  - **Duration = the segment's real length** from segments.json, clamped 4–15s. Flag any
    identity-critical (face-forward talking) shot longer than ~8s: recommend splitting or a
    tighter camera, since Seedance identity drifts past ~6–8s.
  - Include the audio/ambient line and the explicit "no morphing / keep label readable" negatives.
- **Continuity note** — does this segment start a fresh keyframe or chain off the prior
  segment's last frame? State it so the manual operator knows the order to generate in.

Write the pack to `${CLAUDE_SKILL_DIR}/output/run_<ts>/prompt-pack.md` and also drop a copy
next to the reference / in the brand's product folder if one was given. Summarize the segment
table back to the user and point them at the file.

## Rules that keep the pack good

- **Prompts only.** Never call a generation API or the `higgsfield` CLI. If asked to
  "just make it," hand off to `seedance-directors-cut` / `aiugc-infinite` and say so.
- **Cut-aware, never arbitrary.** Segment boundaries come from real cuts; 15s is only a cap.
- **One camera move per Seedance prompt.** Multiple = jitter. (See references.)
- **Concrete verbs only** — `unzips, lifts, tilts, slides strap onto shoulder`, never
  "uses/showcases/experiences."
- **Don't re-describe what's in the start frame.** For i2v, describe motion, not appearance.
- **Tag `@<product>` wherever the product appears** so manual Higgsfield generation binds the
  real product. Keep the token consistent across the whole pack.
- **Product-focused shots = image-to-image** off the canonical product reference, never
  from-scratch (matches house rule for product fidelity).
- **Brand/product agnostic.** Nothing here is Velantra-specific; the same pipeline runs for
  any product by swapping the name + `@token` + reference.

## References (read before writing prompts)
- [`references/seedance-prompting.md`](references/seedance-prompting.md) — Seedance 2.0 i2v prompt structure, camera/verb vocab, duration/identity rules, failure→fix, copy-paste templates.
- [`references/image-avatar-prompting.md`](references/image-avatar-prompting.md) — how to write the avatar likeness image prompt and the product keyframe (start-frame) image prompt.
- [`references/prompt-pack.example.md`](references/prompt-pack.example.md) — the exact output shape to mirror.

## Output layout
```
output/run_<ts>/
├── watch/                 # frames + transcript + downloaded video (from /watch)
├── segments.json          # cut-aware segment table (detect_cuts.py)
└── prompt-pack.md         # THE DELIVERABLE — image + Seedance prompts, per segment
```

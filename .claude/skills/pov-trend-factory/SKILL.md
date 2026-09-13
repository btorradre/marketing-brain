---
name: pov-trend-factory
description: >
  Trend link → finished POV-style product video, raw shot-on-iPhone aesthetic,
  SCENE-AWARE. Pipeline: resolve the link (TrendTrack ad link or direct
  TikTok/IG URL) → fetch + WATCH the video frame by frame → SCAN it for its
  real cut boundaries (a POV ad is rarely one shot) → hook autopsy → 10 new POV
  hooks → user picks → GPT Image 2 generates ONE STILL PER SCENE, every still
  authored independently from the same canonical product reference → QA every
  still → Seedance 2.0 animates each still independently → trim each to its
  scene length, concat, mux. All generation runs on kie.ai (GPT Image 2 i2i +
  bytedance/seedance-2 — Higgsfield is retired). Works for any brand: Motilli,
  Velantra products, Lunessa, etc. Trigger when the user sends a
  trend/TrendTrack/TikTok link and wants a POV video, says "pov factory", "make
  a POV from this trend", "build a POV video from this link", "replicate this
  trend as a POV for <product>", or any POV-style trend-jacking video request.
argument-hint: "<trend-or-video-url> [--brand <brand>] [--product <product>] [--hook-only]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill, ToolSearch
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic. The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper.
- **Where it goes.** The golden nugget LEADS — it is the hook. Never buried.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting the 10 hooks. When analyzing the reference hook, state the nugget IT rides on.

# pov-trend-factory — trend link → raw-iPhone POV product video

## THE ENGINE IS SHARED — this skill is only a POV profile

All scene detection, per-scene keyframe generation, animation and assembly
lives in **`_engine/pipelines/scene_replicator.py`**, which is format-agnostic
and takes ANY reference ad. `scripts/pov_factory.py` is a thin wrapper that
injects the POV doctrine defaults (`footer_preset` ugc/ugc_text,
`max_seconds` 8, `upload_path`, `image_aspect_ratio` 2:3) and forwards the
subcommand. Both entry points work and take identical arguments.

**Anything not POV-specific belongs in the shared runner, not here.** Four
drifting copies of the kie.ai plumbing across skills was the problem this
consolidation fixed. If you need a capability for a non-POV format, add it to
the shared runner.

## KEYFRAME-FIRST DOCTRINE (LOCKED 2026-08-03 — this is the architecture)

**A reference POV ad is almost never one continuous shot.** A 9-second TikTok
routinely carries 6-9 cuts: a pan across the bag, a jump to a close-up, a jump
to the hands. The old single-keyframe build collapsed all of that into one
drifting clip that did not match the reference.

**Every scene gets its own still, and every still is authored independently.**

- `scan` finds the reference's real cut boundaries and cuts a reference frame
  plus a reference clip per scene.
- `image` generates one keyframe PER SCENE, each i2i from THAT scene's own
  reference frame plus the SAME canonical product images.
- `animate` animates each still independently.
- `finish` trims each clip to its scene length and concats.

**NEVER CHAIN.** No clip is ever seeded from another clip's last frame. Chaining
makes every generation inherit the previous one's errors, which is exactly how
a bag's belts multiplied into a lattice and its caramel drifted to grey over
successive segments. Independent stills from a shared reference cannot compound.

**Two free wins fall out of this.** Every still is auditable BEFORE a single
video credit is spent, so frame QA moves to the cheap stage. And each generated
clip is still ONE CONTINUOUS SHOT (the cuts live in the edit), which is why the
Seedance footers still say "no cuts".

## DURATION RULES

- **Generate long, cut short.** Seedance rejects anything under 4s, and POV
  cadence is 3-4s per beat with beats often under 2s. So each scene declares
  `target_seconds` (what it occupies in the final edit) and `gen_seconds` (what
  we ask Seedance for, floor 4). `finish` trims down. Never generate at exactly
  the cut length.
- **The 8-second cap is now the TOTAL assembled duration**, not a per-clip
  limit. It still defaults to 8s and the runner still hard-errors above it.
  Raising it requires setting `"max_seconds"` explicitly in job.json, which
  logs a NOTE. Do not raise it casually — POV doctrine is short.

**THE AESTHETIC IS LOCKED.** Every generated frame must read as raw iPhone
footage a real person grabbed in one take — never studio, never cinematic,
never DSLR. The verbatim IPHONE RAW block (below) goes into every GPT Image 2
prompt; the runner's Seedance footer enforces it in motion.

## Pipeline

```
trend link (TrendTrack / TikTok / IG / local file)
    |
[0] Resolve link ────── TrendTrack MCP (scan_ad / lookup) → raw video URL
    |
[1] Fetch + Watch ───── pov_factory.py fetch  → reference.mp4, first_frame.jpg,
    |                                            original_audio.m4a, music.json
    |                   /watch skill on reference.mp4 → frame-by-frame viewing
    |                   Claude writes analysis/reference-breakdown.md
    |
[2] Scan ────────────── pov_factory.py scan → per-scene reference frame + clip
    |                   + scenes.json (the scene map). VIEW every frame.
    |
[3] Hook autopsy ────── why the reference hook works, what angle it rides,
    |                   golden nugget it sits on → analysis/hook-autopsy.md
    |
[4] 10 POV hooks ────── 3 formula transplants / 4 angle variants / 3 wildcards
    |                   → user picks one (AskUserQuestion)
    |
[5] GPT Image 2 ─────── ONE STILL PER SCENE from each scene's own reference
    |                   frame + shared product refs → QA EVERY still
    |                   → 9:16 crops = scenes/NNN/animate-source.png
    |
[6] Seedance 2.0 ────── each still animated INDEPENDENTLY, gen_seconds each
    |                   → scenes/NNN/raw-clip.mp4
    |
[7] Finish ──────────── trim each to target_seconds, concat, overlay, mux
                        → final.mp4, final-refsound.mp4, trend-sound report
```

Runner: `scripts/pov_factory.py` (stdlib + certifi + ffmpeg + yt-dlp;
Pillow only for the overlay fallback). All stages resumable — state lives in
`kie_upload_cache.json` + `kie_tasks.json`, in-flight taskIds resume polling
instead of paying for fresh tasks. Delete an output file to regenerate it.
Per-scene stages are individually resumable: a failed scene is retried alone.

## Conventions

- Concept ID: `<BRAND>-POV-<slug>-NN` (e.g. `MOT-POV-FRIDGE-01`).
- Output dir: `brands/<brand>/videos/<CONCEPT-ID>/`; scenes in `scenes/NNN/`.
- API key: `KIE_API_KEY` in `marketing brain/.env` (runner auto-loads it).
- Do NOT ask clarifying questions before the hook pick — resolve the
  brand/product from what the user said, pick sane defaults, and run. The ONLY
  built-in stop is the hook pick.

## Stage 0 — Resolve the link

- **TrendTrack ad link** → load the TrendTrack MCP tools via ToolSearch
  (`mcp__claude_ai_TrendTrack__scan_ad`, `lookup`) and pull the creative's
  raw video URL from the scan result.
- **TikTok / IG / YT URL** → pass straight to `fetch` (yt-dlp handles it).
- **Local file path** → `fetch` copies it in.

## Stage 1 — Fetch + Watch (frame by frame)

```bash
python3 "…/.claude/skills/pov-trend-factory/scripts/pov_factory.py" fetch "<url>" "<output_dir>"
```

Then **invoke the `watch` skill** on the local `reference.mp4` and view it
frame by frame. Write `analysis/reference-breakdown.md` with three sections:

1. **Motion ledger** — per-second timestamps with concrete camera verbs:
   `0.0-1.2s slow push-in on the bag, handheld micro-shake · 1.2-2.8s tilt
   down to hands · …`. This ledger feeds the per-scene motion prompts.
2. **Hook capture** — the exact on-screen POV text (verbatim), its position,
   font style, and when it appears/disappears.
3. **Music read** — the sound from `music.json` (name it explicitly). You
   cannot hear audio, so characterize the vibe from metadata + visual pacing:
   cut rhythm, whether motion syncs to an implied beat, energy class. If
   `music.json` is empty, say so.

## Stage 2 — Scan for the real scene structure

```bash
python3 …/pov_factory.py scan "<output_dir>"
```

Flags: `--threshold` (default 0.25, tuned for TikTok's soft cuts),
`--min-gap` (0.35s, drops flash frames), `--max-scene` (4.0s, splits any
over-long span), `--interval` (2.0s fallback when no hard cuts exist).

Writes `scenes.json` and prints the scene table. Then **VIEW every
`scenes/NNN/reference.jpg`.** The detector is good, not perfect:

- It **under-scores low-contrast cuts and cross-dissolves.** `--max-scene`
  catches most misses by splitting long spans, but confirm by eye.
- A reference with no hard cuts (one long take, smooth-morph edit) falls back
  to interval beats. That is correct — a long take still wants authoring as
  separate beats rather than one drifting clip.
- If the split is wrong, edit the scene list in job.json by hand. `scenes.json`
  is a starting point, not a verdict.

`target_seconds` is seeded from the reference's own cut length. Change it when
the edit wants a different rhythm; the sum must fit `max_seconds`.

## Stage 3 — Hook autopsy

Write `analysis/hook-autopsy.md`:

- **Exact hook** (verbatim) and its POV format family ("POV: you…", "When
  you finally…", "Me after…", object-POV, etc.).
- **Golden nugget it rides on** — one sentence, the deep frame, not the topic.
- **Psychological driver** — identification / status signal / in-group wink /
  curiosity gap / tension-release. Why a scroller physically stops.
- **Text–motion congruence** — why THIS hook works over THIS motion (the
  reveal timing, what the camera move pays off).
- **Bridge to our product** — which of the product's proven angles this
  format can carry, calibrated 2 stages LESS aware than Reddit-research
  instinct (the 2 AM doom-scroller rule).

## Stage 4 — 10 POV hooks, then the pick

State OUR golden nugget first (one explicit sentence). Then write exactly 10
hooks in a numbered table with a one-line rationale each, in this locked
spread:

- **1-3 Formula transplants** — the reference hook's exact psychological
  formula, swapped to our product/avatar.
- **4-7 Angle variants** — same POV format family, four different proven
  angles/awareness entries for the product.
- **8-10 Wildcards** — a different POV subformat (object-POV, third-person
  flip, "POV: you're the [product]") still riding the golden nugget.

Hook rules: ≤12 words (overlay legibility at phone size), the avatar's own
voice, granular-specific (never generic), commas and periods only. Velantra:
no competitor mentions, no origin claims, founder is Brooks. Self-audit
all 10 against these rules BEFORE presenting — don't make the user catch
flaws one at a time.

Present the table, then AskUserQuestion with your top 3 (recommended first,
with why) — the user can pick any of the 10 via Other. If the user already
said "you pick", pick and justify in one line, no question.

## Stage 5 — Per-scene keyframes (GPT Image 2)

Write `job.json` (shape documented at the top of `pov_factory.py`) with one
entry in `scenes[]` per detected scene, then:

```bash
python3 …/pov_factory.py image job.json
```

**Each scene's `image_prompt` is a single dense paragraph** describing THAT
scene, in this order:

- Recreates THAT SCENE's composition, camera angle, subject distance, setting,
  and lighting (from its own reference frame, not the ad's opening frame).
- Swaps the original subject/product for OUR product, described exactly from
  its canonical reference images ("the first input image is the composition
  reference; the following images are the exact product — match its shape,
  color, materials, hardware and label precisely, changing nothing").
- **Only the scene with `"carries_hook": true`** gets the HOOK TYPOGRAPHY
  block (normally scene 1). The runner hard-errors if `carries_hook` is set
  and `hook_text` is not inside that scene's `image_prompt` verbatim:

> The image includes a text overlay that reads, verbatim, with exactly this
> spelling and punctuation: "<HOOK TEXT>". Render it in clean bold white
> sans-serif TikTok-caption typography with a thin black outline and a soft
> drop shadow, centered horizontally in the upper portion of the frame,
> fully inside the central 80% width safe area, fully legible at phone size.

- Ends with the verbatim IPHONE RAW block:

> Shot on an iPhone, casual amateur snapshot aesthetic. Slightly imperfect
> framing with a subtle tilt, natural ambient lighting only, mild sensor
> grain, true-to-life muted colors, soft focus falloff. No studio lighting,
> no professional retouching, no DSLR depth of field, no cinematic color
> grade. It must look like a real person grabbed this on their phone in one
> take. Vertical composition with all key elements inside the central 80%
> safe area.

**Continuity is your job, not the model's.** Because every still is generated
independently, wardrobe, setting, lighting and time of day must be restated in
EVERY scene's prompt. Write them once and paste them into all of them. This is
the trade for not compounding drift, and it is a good trade.

**Product truth is non-negotiable:** product renders are always i2i from the
canonical reference — never from imagination. Known canonicals: Motilli →
`brands/motilli/creative/product-images/updated/product img 1.webp` (square
jar, white cap, DARK FOREST GREEN heart gummies — never orange/peach).

**MANDATORY (locked 2026-07-18, no exceptions):** if a product-truth skill
exists for the product (`velantra-straw-tote`, `velantra-weekender`, any
`velantra-<product>` with locked blocks), load it BEFORE writing any
`image_prompt` and paste its verbatim identity + mechanism blocks into EVERY
scene, color-resolved, never paraphrased — and carry its video mechanism line
into every `motion_prompt`. There is NO format exception: a packing/open-bag
POV still shows a flap bag's flap as ONE seamless piece folded all the way
over, flat on the front, with the mouth opening BEHIND it — items go in behind
the flap. A frame with a lifted, split, partial or duplicated flap fails QA no
matter how good the rest looks. Brooks has corrected this three times in one
day; there is no fourth.

**QA GATE — the whole board, before any video spend.** View EVERY
`scenes/NNN/keyframe.png` and check (1) product fidelity against the canonical
ref, (2) on the hook scene, the text read character by character — GPT Image 2
is strong at typography but ONE misspelled word kills the ad, (3) it reads
phone-raw, not studio, and never like a 3D render, (4) continuity across
scenes: same wardrobe, same setting, same light. Any miss → delete that
scene's `keyframe.png`, tweak its `image_prompt`, re-run `image` (it
regenerates only the missing ones). Stills are cheap, clips are not.

## Stage 6 — Per-scene animation (Seedance 2.0)

Write each scene's `motion_prompt` as 1-2 sentences distilled from that
scene's slice of the motion ledger — camera verbs only, no scene
re-description (the still already IS the scene):

> Slow handheld push-in toward the bag, subtle natural hand shake, micro
> parallax in the background.

```bash
python3 …/pov_factory.py animate job.json
```

**LOGO GUARD (LOCKED, learned 2026-07-18):** for any fashion/product subject,
EVERY `motion_prompt` MUST end with an anti-logo line — Seedance's luxury-prior
invents competitor trademarks mid-motion (it morphed a plain black flap into
a Celine Triomphe emblem on the first Straw Tote run; the keyframe was
clean, the logo appeared during animation). Verbatim: "The product stays
exactly as it appears in the first frame, with no logo, no emblem, no
monogram and no brand hardware appearing anywhere at any point." Then QA
every clip's mid and end beats for invented marks before shipping.

- **Default = first_frame mode**: the scene's `animate-source.png` is literally
  frame 1, so a baked hook stays put. The runner appends the locked footer.
- **`"motion_transfer": true`** per scene, only when that scene's motion is too
  complex to describe (whip pans, specific hand choreography): sends the still
  as `@Image1` + that scene's own reference clip as `@Video1`. Stronger motion
  copy, but reference mode can drift a baked hook — QA hard after.
- Engine facts: `bytedance/seedance-2` ONLY (`-fast` is BANNED — distortion).
  ~41 credits/sec at 720p, but createTask pre-authorizes ~130cr/sec. The
  pre-auth hold is per task, so the wall is the LARGEST single scene, not the
  sum — the runner checks against that and refuses before wasting a call.
  Failed tasks are not charged. This machine's TLS resets to kie's result CDN —
  the runner auto-relays downloads through the VPS.
- A failed scene does not kill the batch. Re-run `animate` to retry only the
  scenes still missing a `raw-clip.mp4`.

**QA gate:** watch every `scenes/NNN/raw-clip.mp4`. Text warped or crawling?
→ switch `"text_mode": "overlay"`, strip the typography block out of the hook
scene's `image_prompt`, delete that scene's `keyframe.png` +
`animate-source.png` + `raw-clip.mp4`, re-run `image` then `animate` — the
hook gets burned in post by Pillow instead (the established
no-drawtext-ffmpeg → Pillow path). Never ship warped text.

## Stage 7 — Finish + deliverables

```bash
python3 …/pov_factory.py finish job.json
```

Trims each scene to `target_seconds`, concats via the ffmpeg concat FILTER
(never the concat demuxer — it silently desyncs when clips differ in encode
params, which independently generated scenes always do), applies the Pillow
hook overlay when `text_mode` is `overlay`, and muxes the trend sound.

Produces and you report:

- **final.mp4** — 9:16, native ambient audio. The organic-post master:
  attach the trending sound natively in TikTok/IG when posting (that's where
  the reach is — say the sound's name from music.json in your summary).
- **final-refsound.mp4** — original trend audio muxed in, for Meta placements
  where in-app sound attach doesn't exist. Rights caveat: trending commercial
  sounds are NOT licensed for paid ads — flag this whenever music.json shows
  a commercial track.
- One-line recap: concept ID, hook used, scene count, total duration, credits.

## When NOT to use this skill

- Talking-head / dialogue UGC → `velantra-ugc` (Velantra roster) or
  `omni-ugc` (reference-image reaction ads).
- Multi-scene 1:1 replication of a whole video → `video-scene-replicator` /
  `fashion-replicator`.
- Static ad from a reference image → `ad-replicator`.
- Long-form (>15s) with dialogue → `seedance-brief-runner` with a segment brief.

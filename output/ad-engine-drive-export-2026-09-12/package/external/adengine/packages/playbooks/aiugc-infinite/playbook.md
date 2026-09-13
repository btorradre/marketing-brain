---
name: aiugc-infinite
description: Infinite AIUGC video factory built on Higgsfield Marketing Studio (UGC preset) + Seedance 2.0. Produces two-cut creator ads at scale — Cut 1 is a talking-head (creator delivering the hook/script with native VO from Marketing Studio's UGC engine), Cut 2 is a hard-cut to the same creator using the product or an action scene (image-to-video off Cut 1's last frame via Seedance 2.0). FFmpeg stitches them. Loops N times to produce batches with rotating hooks/settings and avatar-locked identity via Soul Characters. Use when the user says "build infinite AIUGC", "AIUGC factory", "two-cut UGC ads", "scale UGC with Higgsfield + Seedance", or wants batch UGC production with cut-to-action scenes.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# AIUGC Infinite

Two-cut creator-style ad factory powered by **Higgsfield Marketing Studio** (Cut 1: talking head) + **Seedance 2.0** (Cut 2: action / product use). Produces batches of finished, stitched, vertical 9:16 UGC ads from a single brand brief.

## Core Pipeline

```
Brand brief + count N
  |
  v
[1] Generate N two-cut scripts (Anthropic Opus)
       Each script = { hook_line, cut1_vo, cut2_visual_prompt }
  |
  v
[2] Resolve assets (cached in products.json)
       - Higgsfield product_id  (one-time per brand)
       - Soul Character id       (optional, for identity lock across both cuts)
       - Hook + Setting ids      (rotated per ad)
  |
  v
[3] For each script (loop):
       a. Cost preflight  (`higgsfield generate cost ...`)
       b. CUT 1 — `higgsfield generate create marketing_studio_video --mode ugc`
                  with hook_id + setting_id + product + generate_audio=true
                  → 5-8s creator talking with native VO
       c. Download Cut 1 mp4 → ffmpeg extract last frame to PNG
       d. CUT 2 — `higgsfield generate create seedance_2_0`
                  with --medias <last_frame_png> + --duration 5
                  → 5s image-to-video action scene (creator using product)
       e. Download Cut 2 mp4
       f. ffmpeg concat Cut1 + Cut2 → final_ad_<n>.mp4 (hard cut)
  |
  v
[4] Manifest + output dir
       output/run_<ts>/
         ├── ad_001.mp4
         ├── ad_001/cut1.mp4, cut2.mp4, last_frame.png, prompts.json
         ├── ...
         └── manifest.json
```

## When to Use

- "Build me infinite AIUGC" / "AIUGC factory" / "scale UGC creative"
- "Make me 10 UGC ads for <brand> with a cut to product action"
- Any two-cut UGC where Cut 1 is creator talking and Cut 2 is the same creator using/holding/demonstrating the product

Defer to other skills when:
- Single-cut talking head only → `rapid-vsl` (Kling) or `aiugc-orchestrator` (Fabric)
- Replicating a specific reference ad → `aiugc-replicator` or `higgsfield-replicator`
- 3D animated / claymation → `animated-video` or `claymation`

## Required Inputs

When invoked, collect:

1. **Brand** — `motilli`, `lunessa`, `velantra-boat-tote`, `velantra-meridian`, `velantra-weekender`, `avelle`, `solorna`, or path to a brand vault folder
2. **Count N** — number of ads to produce in this batch (default 5)
3. **Concept seed** (optional) — angle, hook style, or copywriting brief. If omitted, the skill loads the brand's vault docs and lets Opus invent N variations
4. **Aspect ratio** — `9:16` (default), `1:1`, `16:9`
5. **Cut durations** — Cut1 default 8s, Cut2 default 5s (Seedance max is workflow-dependent; 5s is the safe-fast default)
6. **Soul Character** (optional) — pinned `soul_id` for identity lock. If omitted, Cut 2 inherits identity from Cut 1's last frame (Seedance i2v); avatar in Cut 1 is the Marketing Studio default for that hook.
7. **Hook/Setting strategy** — `rotate` (default; cycles brand-appropriate combos), `fixed:<hook_id>:<setting_id>`, or `random`

## Setup (one-time, mirrors higgsfield-replicator)

CLI is already installed. Verify each session:
```bash
higgsfield auth token
higgsfield workspace status        # should be retail_guinea_pig_2000
higgsfield account status          # credit balance
```

If a brand has no `higgsfield_product_id` in `products.json`, the orchestrator will set it up on first use — uploading the brand's hero image and creating the Marketing Studio product entity. See `higgsfield-replicator/SKILL.md` Step C.

## Step-by-Step Execution

### Step 1 — Generate N Two-Cut Scripts

Run `scripts/generate_scripts.py`:

```bash
python3 scripts/generate_scripts.py \
  --brand <brand_key> \
  --count <N> \
  --concept "<optional concept seed>" \
  --output output/run_<ts>/scripts.json
```

This loads brand vault docs (research, avatar VoC, copywriting briefs from `marketing brain/brands/<brand>/`) and prompts Opus to produce a JSON array:
```json
[
  {
    "id": "ad_001",
    "hook_type_hint": "subtle",          // routes to hook catalog
    "setting_hint": "kitchen",           // routes to setting catalog
    "cut1_vo": "I tried this celery gummy for 14 days and… (≤8s spoken)",
    "cut2_visual_prompt": "Same woman pops open the green Motilli jar at her kitchen counter, takes one heart-shaped gummy, smiles. Soft morning light. Handheld. Subtle eye-focus drift. Background blur, plants, clean kitchen.",
    "rationale": "<one-line why this angle works>"
  }
]
```

The system prompt enforces:
- Cut 1 ≤ 22 words (≈ 8s of natural speech)
- Cut 1 ends mid-thought to set up Cut 2 cut (creates pull-through)
- Cut 2 visual matches Cut 1's avatar/setting for continuity
- Cut 2 always shows the product physically on screen (drink/hold/open/spread/wear)
- 4 organic imperfection cues bolted onto every Cut 2 prompt (handheld jitter, rolling shutter, eye focus drift, background motion) — see `feedback_kling_prompting.md`

### Step 2 — Resolve Assets

`scripts/resolve_assets.sh` reads `products.json`:
- If `brands.<brand>.higgsfield_product_id` is null, runs setup (uploads hero image, creates MS product).
- Loads brand-default hook + setting catalog from `HOOKS_SETTINGS.md` (snapshot in skill).
- If `--soul-id` provided or cached, locks avatar.

### Step 3 — Per-Ad Loop

`scripts/run_one_ad.sh <script_json> <output_dir>` executes Cut 1 → frame extract → Cut 2 → stitch.

**Cut 1 — Marketing Studio Video (UGC):**
```bash
higgsfield generate create marketing_studio_video \
  --prompt "$CUT1_VO" \
  --start-image "$PRODUCT_ID" \
  --mode ugc \
  --hook_id "$HOOK_ID" \
  --setting_id "$SETTING_ID" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --generate_audio true \
  --resolution 720p \
  --wait --wait-timeout 20m \
  --json > "$OUT/cut1_job.json"

CUT1_URL=$(jq -r '.results[0].result_url // .[0].results[0].result_url' "$OUT/cut1_job.json")
curl -sL -o "$OUT/cut1.mp4" "$CUT1_URL"
```

**Frame extract (last frame as seed for Cut 2):**
```bash
ffmpeg -y -sseof -0.1 -i "$OUT/cut1.mp4" -vframes 1 -q:v 2 "$OUT/cut1_lastframe.png"
```

**Cut 2 — Seedance 2.0 image-to-video:**
```bash
higgsfield generate create seedance_2_0 \
  --prompt "$CUT2_VISUAL_PROMPT" \
  --medias "$OUT/cut1_lastframe.png" \
  --aspect_ratio 9:16 \
  --duration 5 \
  --resolution 720p \
  --mode std \
  --wait --wait-timeout 15m \
  --json > "$OUT/cut2_job.json"

CUT2_URL=$(jq -r '.results[0].result_url // .[0].results[0].result_url' "$OUT/cut2_job.json")
curl -sL -o "$OUT/cut2.mp4" "$CUT2_URL"
```

**Stitch (hard cut, normalize streams):**
```bash
bash scripts/stitch.sh "$OUT/cut1.mp4" "$OUT/cut2.mp4" "$OUT/final.mp4"
```

### Step 4 — Manifest

After every ad, append to `output/run_<ts>/manifest.json`:
```json
{
  "ad_id": "ad_001",
  "brand": "motilli",
  "hook_id": "...", "hook_name": "Interview",
  "setting_id": "...", "setting_name": "Kitchen",
  "product_id": "...",
  "cut1_job_id": "...", "cut1_credits": 12.4,
  "cut2_job_id": "...", "cut2_credits": 4.0,
  "cut1_path": "ad_001/cut1.mp4",
  "cut2_path": "ad_001/cut2.mp4",
  "final_path": "ad_001.mp4",
  "scripts": { "cut1_vo": "...", "cut2_visual_prompt": "..." },
  "timestamp": "2026-05-08T12:00:00Z"
}
```

## CLI Surface Used (Reference)

| Step | Command |
|---|---|
| Cost preflight | `higgsfield generate cost marketing_studio_video --prompt ... --json` |
| Cut 1 | `higgsfield generate create marketing_studio_video --mode ugc --hook_id --setting_id --start-image --generate_audio true --duration 8 --wait --json` |
| Cut 2 | `higgsfield generate create seedance_2_0 --medias <last_frame> --duration 5 --aspect_ratio 9:16 --wait --json` |
| Frame extract | `ffmpeg -sseof -0.1 -i cut1.mp4 -vframes 1 lastframe.png` |
| Stitch | `ffmpeg -i cut1.mp4 -i cut2.mp4 -filter_complex concat=n=2:v=1:a=1 final.mp4` |

## Seedance 2.0 Notes (from `higgsfield model get seedance_2_0`)

Required: `prompt`. Optional: `aspect_ratio` (auto/16:9/9:16/4:3/3:4/1:1/21:9, default 16:9 — set `9:16`), `duration` (default 5), `mode` (std/fast, default std), `resolution` (480p/720p/1080p, default 720p), `genre` (auto/action/comedy/drama/etc.), `medias` (image array — pass last frame here for i2v).

**No `generate_audio` flag.** Cut 2 ships silent / ambient. The stitched ad's audio is Cut 1's VO followed by ambient — design Cut 2 prompts so the visual self-narrates (creator using product, no need for spoken VO). To layer SFX or music, post-process with FFmpeg in `stitch.sh`.

## Marketing Studio Video Notes

Required: `prompt`. Mode enum: `ugc | ugc_how_to | ugc_unboxing | product_showcase | product_review | tv_spot | wild_card | ugc_virtual_try_on | virtual_try_on`. For this skill we lock `mode=ugc` (talking head). `hook_id` + `setting_id` are valid only for UGC-family modes.

`generate_audio: true` produces native dialogue in the avatar's voice — no ElevenLabs needed for Cut 1.

`product_ids` (array) is the formal way to pass MS product entities; `start-image` (single) accepts an upload_id, product_id, or local path. We use `--start-image $PRODUCT_ID` for a single product.

## Cost Discipline

Observed pricing (May 2026, 9:16, 720p):
- Cut 1 (`marketing_studio_video`, 8s, mode=ugc, generate_audio=true): **~40 credits**
- Cut 2 (`seedance_2_0`, 5s, mode=std): **~22 credits**
- Per finished two-cut ad: **~62 credits**
- Batch of N=10: **~620 credits + 100 buffer = ~720 credits**

The orchestrator runs preflight automatically (Step 3 in `run.sh`). Confirm with user before continuing if `total > 500 credits` or `balance < total × 1.2`. Reduce cost by:
- `--cut1-duration 6` (drops MS cost ~25%)
- `--seedance-mode fast` (faster + cheaper, slightly lower visual quality)
- `--resolution 480p` for first-pass iteration; bump to 720p/1080p only on winners

`higgsfield account status` shows live balance.

## Output

```
output/run_<unix_ts>/
├── scripts.json                # Step 1 output (all N scripts)
├── manifest.json               # one entry per finished ad
├── ad_001.mp4                  # final stitched
├── ad_001/
│   ├── cut1.mp4                # raw Marketing Studio output
│   ├── cut1_job.json
│   ├── cut1_lastframe.png      # seed for Cut 2
│   ├── cut2.mp4                # raw Seedance output
│   ├── cut2_job.json
│   └── prompts.json            # exact prompts used
├── ad_002.mp4
├── ad_002/...
└── ...
```

## Failure Modes

- **Cut 1 has wrong avatar / random face** → Train + pin a Soul Character; alternatively, Marketing Studio doesn't expose Soul IDs natively for `marketing_studio_video` — instead we pre-generate a Soul portrait, then use it as `--start-image` in place of the product. For pure identity lock, see `higgsfield-soul-id` skill.
- **Cut 2 face drifts from Cut 1** → Make sure last frame extraction grabbed a clean frame (not a motion-blur tail). If Cut 1 ends mid-gesture, switch frame extract to `-ss 0.2` from end (`-sseof -0.2`).
- **Hard cut feels jarring** → That's intentional for UGC pacing. To soften, see `stitch.sh --crossfade 0.15` (crossfades 150ms of video; audio still hard-cuts).
- **Audio cuts off mid-word at end of Cut 1** → Increase Cut 1 duration to 9s or trim Cut 1 in `stitch.sh` at last natural pause (use `silencedetect` filter).
- **Server rejects hook/setting on non-UGC mode** → This skill always uses `mode=ugc` for Cut 1, so hooks/settings are always valid. Don't change `mode` in `cut1_talking_head.sh` without removing those flags.

## Quickstart

```bash
# Single-command batch run (5 ads for Lunessa)
bash scripts/run.sh \
  --brand lunessa \
  --count 5 \
  --concept "I tried this for 14 days, my cholesterol numbers shifted"

# With explicit hook/setting fixed across the batch
bash scripts/run.sh \
  --brand motilli \
  --count 10 \
  --hook 26cac2dd-99cb-4818-a678-509b0dab2c32 \
  --setting a0eb0be9-f0ff-4aee-9dee-69d9fd20110a

# Dry-run (script generation + cost preflight only, no jobs created)
bash scripts/run.sh --brand lunessa --count 3 --dry-run
```

## Prompting References

This skill ships with model-specific prompting docs in `references/`:
- [`references/PROMPTING.md`](references/PROMPTING.md) — index + universal cheat-sheet across all three models
- [`references/gpt-image-2-prompting.md`](references/gpt-image-2-prompting.md) — for upstream image work (hero/native-image/static)
- [`references/kling-3-prompting.md`](references/kling-3-prompting.md) — substitute when Marketing Studio doesn't fit Cut 1
- [`references/seedance-2-prompting.md`](references/seedance-2-prompting.md) — Cut 2 production reference (UGC anchor, identity-lock, banned camera moves)

The Seedance best practices are baked into `scripts/generate_scripts.py`'s SYSTEM prompt — every Cut 2 prompt produced by the orchestrator follows the 4-block structure (UGC anchor + concrete-verb action + single camera move + identity lock).

## Memory Hooks

After a successful run, persist:
- New `higgsfield_product_id` in `products.json` if setup ran
- Trained `soul_id` if generated
- Winning final ad job IDs in `products.json` `winning_refs[brand].aiugc_two_cut`

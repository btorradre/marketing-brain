---
name: higgsfield-replicator
description: Canonical Higgsfield Marketing Studio replication pipeline using the official higgsfield CLI. Takes a reference ad (image or video) plus a brand and replicates it via `higgsfield generate create marketing_studio_video` (or `marketing_studio_image`) — chooses the right preset (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC/Pro Virtual Try On), loads brand voice from the vault, resolves a brand product entity + Soul Character (cached in products.json), and emits/runs the exact CLI invocation. Use when the user wants to replicate an ad with Higgsfield, says "use Higgsfield" / "Higgsfield mode" / "run this through Marketing Studio", or asks for one-click product ads from a reference. Replaces the manual Nano Banana 2 → Kling pipeline for ad replication.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Higgsfield Replicator (CLI-based)

Strategic orchestrator on top of the official `higgsfield` CLI. This skill does the brand-specific upstream work — reference analysis, preset routing, vault-driven script adaptation, brand product/avatar registry — then runs the canonical CLI commands. The actual generation is handled by the `higgsfield` binary; raw ad-hoc generation requests can also be served by the official `higgsfield-generate` skill (installed at `~/.agents/skills/higgsfield-generate`).

## When to Use This Skill

Use when:
- User says "replicate this ad with Higgsfield" / "use Higgsfield" / "run through Marketing Studio" / "Higgsfield mode"
- User wants a one-click branded ad from a reference image or video
- The reference fits a Higgsfield preset (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On)
- The existing replicators (`ad-replicator`, `video-scene-replicator`, `aiugc-replicator`, `animated-video-replicator`) are invoked with `--use-higgsfield` or the user asks for the Higgsfield variant

Defer to the **existing skills** (Nano Banana 2 + Kling 3.0 path) when:
- The user wants frame-by-frame 1:1 visual replication of a non-standard creative (claymation, custom 3D animation outside Higgsfield's preset library)
- The reference style doesn't fit any Higgsfield preset
- The user explicitly says "don't use Higgsfield"

For raw, no-routing image/video gen ("just generate me a Soul portrait"), point the user at the official `higgsfield-generate` skill — don't run this skill.

## Setup (one-time, already done as of 2026-05-07)

- CLI installed: `npm install -g @higgsfield/cli` → `which higgsfield` returns `/Users/brooksorradre2/.local/bin/higgsfield` (symlink into `~/.npm-global/bin/`)
- Auth: `higgsfield auth login` (device flow). Token stored locally; check via `higgsfield auth token`.
- Workspace selected: `retail_guinea_pig_2000` (`7185c910-9954-4029-9d11-0fde8ed1a767`).
- Official skills bundle: `npx skills add higgsfield-ai/skills --yes --global` installed `higgsfield-generate`, `higgsfield-product-photoshoot`, `higgsfield-marketplace-cards`, `higgsfield-soul-id` to `~/.agents/skills/` (symlinked into Claude Code).

If a fresh session shows "Not authenticated" or workspace not set, re-run:
```bash
higgsfield auth token              # check
higgsfield auth login              # if not authed (interactive, browser device flow)
higgsfield workspace status        # check
higgsfield workspace set 7185c910-9954-4029-9d11-0fde8ed1a767
```

## Required Inputs

When invoked, collect:

1. **Reference ad** — local file path (image or video), GetHookd URL/ID, or product URL
2. **Brand** — `motilli`, `lunessa`, `velantra-boat-tote`, `velantra-meridian`, `velantra-weekender`, `avelle`, `solorna`, or other
3. **Preset** (optional) — one of (CLI `--mode` slug): `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_showcase`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`. If omitted, the skill picks one from the reference. See [PRESETS.md](PRESETS.md).
4. **Soul Character** (optional) — pinned `soul_id` for identity-locked avatar
5. **Hook / Setting** (optional, UGC-family only) — IDs from [HOOKS_SETTINGS.md](HOOKS_SETTINGS.md)
6. **Aspect ratio** (optional) — `9:16` (default), `1:1`, `16:9`, `auto`
7. **Duration** (optional) — 4-15s for video
8. **Variations** (optional) — `count` 1-4, default 1

## Pipeline

```
Reference Ad
  |
  v
[A] Analyze Reference (Opus/Gemini)  → why-it-works + format classification
  |
  v
[B] Route to Preset (rules in PRESETS.md)
  |
  v
[C] Resolve Brand Product (cache in products.json → setup if missing)
  |
  v
[D] Resolve Avatar (Soul Character ID → fallback to Marketing Studio default)
  |
  v
[E] Adapt Script (Opus + brand vault docs → ad copy in brand voice)
  |
  v
[F] Pre-flight: `higgsfield generate cost` → confirm credits before spending
  |
  v
[G] Generate via CLI:
       Image refs:  higgsfield generate create marketing_studio_image ...
       Video refs:  higgsfield generate create marketing_studio_video ...
  |
  v
[H] Save outputs locally + log to ./higgsfield-output/manifest.json
  |
  v
[I] On user approval: pin generation `id` to products.json `winning_refs[brand][preset]`
       for future remixes via `--ad_reference_id <id>`
```

## Step-by-Step Execution

### Step A — Analyze the Reference

Same logic as the existing replicators:
- **Image refs:** Opus → `why_it_works`, `composition`, `style`, `angle`, `audience`, `product_presence`
- **Video refs:** Gemini → full transcript + per-scene visual breakdown + format flag (`talking_head_ugc`, `unboxing`, `tv_spot`, `product_showcase`, `product_review`, `ugc_how_to`, `virtual_try_on`)

Save to `./higgsfield-output/analysis/reference_analysis.json`.

### Step B — Route to Preset

See [PRESETS.md](PRESETS.md) for the decision tree. The preset slug becomes `--mode` on the CLI call (NOT `--preset_type`; the slug enum is `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_showcase`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`).

### Step C — Resolve Brand Product

Read [products.json](products.json). If the brand has no `higgsfield_product_id`, run setup ONCE per brand:

**Path 1 — from a product URL** (best for Avelle / Shopify brands with a clean PDP):
```bash
higgsfield marketing-studio products fetch \
  --url "https://getavelle.com/products/<slug>" \
  --wait \
  --json | jq -r '.id'
```
Save the returned `id` to `products.json` under `brands.<brand>.higgsfield_product_id`.

**Path 2 — from a local hero image** (use for Motilli, Lunessa, Velantra):
```bash
UPLOAD_ID=$(higgsfield upload create "/path/to/hero.png" --json | jq -r '.id')
higgsfield marketing-studio products create \
  --title "Lunessa Red Yeast Rice + CoQ10" \
  --description "Heart health supplement for women 50+" \
  --image "$UPLOAD_ID" \
  --json | jq -r '.id'
```
Save returned ID to `products.json`.

To list existing products and find one by name:
```bash
higgsfield marketing-studio products list --limit 50 --json | jq '.items[] | {id, title}'
```

### Step D — Resolve Avatar

Three modes, in order of preference:

1. **Pinned Soul Character** — pass to CLI as `--soul-2 --soul-id <id>` on a `soul_2` model call. For `marketing_studio_video`, avatars come from the Marketing Studio avatar library (created via `marketing-studio avatars create`). Look up:
```bash
higgsfield soul-id list --json | jq '.items[] | {id, name, status}'
higgsfield marketing-studio avatars list --size 50 --json | jq '.items[] | {id, name}'
```

2. **One-off avatar** — generate quickly with Soul 2:
```bash
higgsfield generate create soul_2 \
  --prompt "<avatar description from brand vault>" \
  --aspect_ratio 9:16 \
  --wait --json
```
Use the returned `result_url` or `id` as a reference image for the next step.

3. **Marketing Studio default** — omit avatar entirely; Higgsfield picks from its 40+ library. Identity drifts run-to-run.

To train a reusable Soul Character (one-time, ~10 min, 5-20 photos):
```bash
# upload photos
for f in photo*.jpg; do higgsfield upload create "$f" --json | jq -r '.id'; done
# train
higgsfield soul-id create \
  --name "Lunessa Linda" \
  --soul-2 \
  --image <id1> --image <id2> --image <id3> --image <id4> --image <id5>
# wait
higgsfield soul-id wait <returned_soul_id>
```
Save the `soul_id` to `products.json` under `brands.<brand>.soul_characters.<character_name>`.

### Step E — Adapt the Script

Same logic as `aiugc-replicator` / `animated-video-replicator` Stage 3:
- Load brand vault docs (research, avatar VoC, copywriting brief) — up to 30k chars
- Send original transcript + brand context to Opus
- Preserve narrative structure, swap product/mechanism/competitors, adapt voice
- Output: a single `--prompt` string for the CLI, plus per-scene narration if the preset is multi-scene (TV Spot / Tutorial)

For static image references this step produces just the `--prompt` value.

### Step F — Pre-flight Cost Check

Always run BEFORE creating a job. This is free and catches expensive runs early:
```bash
higgsfield generate cost marketing_studio_video \
  --prompt "<adapted prompt>" \
  --start-image <product_image_path_or_id> \
  --mode ugc \
  --aspect_ratio 9:16 \
  --duration 8 \
  --json
```
If estimated credits > 50, or if balance < estimated × variations + 100 buffer, stop and confirm with the user.

Live balance check:
```bash
higgsfield account status
```

### Step G — Generate via CLI

**Image references (static product ads):**
```bash
higgsfield generate create marketing_studio_image \
  --prompt "<adapted prompt>" \
  --image <product_id_or_local_path> \
  --aspect_ratio "<from input or auto>" \
  --resolution 2k \
  --wait \
  --json > "./higgsfield-output/jobs/$(date +%s)_image.json"
```

**Video references (the main path):**
```bash
higgsfield generate create marketing_studio_video \
  --prompt "<adapted prompt>" \
  --start-image <product_id_or_local_path> \
  --mode ugc \
  --hook_id "<from HOOKS_SETTINGS.md, UGC-family only>" \
  --setting_id "<from HOOKS_SETTINGS.md, UGC-family only>" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --generate_audio true \
  --resolution 720p \
  --wait \
  --wait-timeout 20m \
  --json > "./higgsfield-output/jobs/$(date +%s)_video.json"
```

**Critical preset rules:**
- `--hook_id` and `--setting_id` are valid ONLY for: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`. Strip them for `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on` — server validation rejects.
- Media flags accept either a UUID (upload_id, job_id, product_id) OR a local file path — paths are auto-uploaded, no manual `upload create` step required.

**Iterating on a winner (remix):**
```bash
# Re-use a prior winning job's style
WINNER_ID=$(jq -r ".brands.lunessa.winning_refs.ugc[0]" products.json)
higgsfield generate create marketing_studio_video \
  --prompt "<new variation prompt>" \
  --start-image <product_id> \
  --mode ugc \
  --ad_reference_id "$WINNER_ID" \
  --count 4 \
  --wait --json
```

**For multiple variations:**
- Either pass `--count 4` (Marketing Studio Video accepts 1-4)
- Or loop: `for i in {1..4}; do higgsfield generate create ... --json; done` for fully independent prompts

### Step H — Save Outputs Locally

The CLI returns the result URL(s) in JSON. Download:
```bash
RESULT_URL=$(jq -r '.results[0].result_url' "./higgsfield-output/jobs/<file>.json")
curl -L -o "./higgsfield-output/generated/<preset>_$(date +%Y%m%d_%H%M)_v1.mp4" "$RESULT_URL"
```

Append to manifest:
```json
{
  "job_id": "...",
  "preset": "ugc",
  "brand": "lunessa",
  "timestamp": "2026-05-07T14:32:00Z",
  "prompt": "...",
  "product_id": "...",
  "soul_id": null,
  "hook_id": "...",
  "setting_id": "...",
  "ad_reference_id": null,
  "output_path": "generated/ugc_20260507_1432_v1.mp4",
  "credits_used": 12.4
}
```

### Step I — Pin Winners (on user approval)

When the user approves a generation, append its `id` to `products.json`:
```json
{
  "brands": {
    "lunessa": {
      "winning_refs": {
        "ugc": ["<job_id_1>", "<job_id_2>"],
        "product_review": ["<job_id_3>"]
      }
    }
  }
}
```
Future runs at the same brand+preset can pass `--ad_reference_id <id>` to seed off the winner.

## Brand Registry

Same brand keys as the other replicators. The skill auto-loads from `marketing brain/brands/<brand>/`:

| Brand Key | Hero Image (relative to vault) | Default Product Context |
|---|---|---|
| `motilli` | `brands/motilli/brand/website-assets/motilli product reference.png` | Celery juice fiber gummies for GLP-1 users |
| `lunessa` | `brands/lunessa/brand/website assets/lunessa spelling corrected .jpg` | Heart health supplement for women 50+ (Red Yeast Rice + CoQ10) |
| `velantra-boat-tote` | (find in brands/velantra/...) | Canvas + leather boat tote, gold hardware |
| `velantra-meridian` | (find in brands/velantra/...) | Leather handbag, silver hardware |
| `velantra-weekender` | (find in brands/velantra/...) | Canvas + leather travel bag |
| `avelle` | (load from brands/avelle/...) | (load from Avelle PDP product images) |
| `solorna` | (load from brands/solorna/...) | (load from Solorna brand docs) |

The Higgsfield product_id for each brand is cached in [products.json](products.json) after first setup.

## CLI Reference (Quick Lookups)

| Purpose | Command |
|---|---|
| Top-level help | `higgsfield --help` |
| Auth status / login / logout | `higgsfield auth token` / `auth login` / `auth logout` |
| Active workspace | `higgsfield workspace status` (set with `workspace set <id>`) |
| Account balance | `higgsfield account status` |
| List models | `higgsfield model list` (`--image` / `--video`) |
| Inspect model params | `higgsfield model get <model_id> --json` |
| Upload local file | `higgsfield upload create ./file.png --json` |
| List uploads | `higgsfield upload list --image --size 50 --json` |
| List MS products | `higgsfield marketing-studio products list --json` |
| Create MS product | `higgsfield marketing-studio products create --title ... --image <upload_id>` |
| Fetch MS product from URL | `higgsfield marketing-studio products fetch --url ... --wait --json` |
| List MS avatars | `higgsfield marketing-studio avatars list --json` |
| List hooks (UGC-family) | `higgsfield marketing-studio hooks list --size 100 --json` |
| List settings (UGC-family) | `higgsfield marketing-studio settings list --size 100 --json` |
| Train Soul Character | `higgsfield soul-id create --name X --soul-2 --image id1 --image id2 ...` |
| List Soul Characters | `higgsfield soul-id list --json` |
| Generate (image/video) | `higgsfield generate create <model_id> --prompt ... [--image ...] [--start-image ...] [...] --wait --json` |
| Cost preview | `higgsfield generate cost <model_id> --prompt ... [...] --json` |
| List recent jobs | `higgsfield generate list --json --size 50` |
| Wait for a job | `higgsfield generate wait <job_id> --timeout 20m --interval 5s` |

## Cost & Credit Discipline

- **ALWAYS** run `higgsfield generate cost` before any `generate create` (it's free)
- Before any `--count > 1`, confirm balance > estimated × count + 100
- `marketing_studio_video` at `--resolution 1080p` and `cinematic_studio_video_v3_0` are the most expensive — flag explicitly to the user
- Use `--resolution 720p` for first-pass iteration; bump to 1080p only on winners

## Workflow Examples

**Replicate a viral GetHookd UGC ad for Lunessa:**
```bash
# Step C: setup product (one-time)
LUNESSA_PRODUCT=$(higgsfield marketing-studio products create \
  --title "Lunessa Heart Health Supplement" \
  --description "Red Yeast Rice + CoQ10 for women 50+" \
  --image "/Users/brooksorradre2/Documents/marketing brain/brands/lunessa/brand/website assets/lunessa spelling corrected .jpg" \
  --json | jq -r '.id')

# Step F: cost check
higgsfield generate cost marketing_studio_video \
  --prompt "<adapted Lunessa script>" \
  --start-image "$LUNESSA_PRODUCT" \
  --mode ugc \
  --hook_id "26cac2dd-99cb-4818-a678-509b0dab2c32" \
  --setting_id "a0eb0be9-f0ff-4aee-9dee-69d9fd20110a" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --json

# Step G: generate
higgsfield generate create marketing_studio_video \
  --prompt "<adapted Lunessa script>" \
  --start-image "$LUNESSA_UPLOAD_ID" \
  --mode ugc \
  --hook_id "26cac2dd-99cb-4818-a678-509b0dab2c32" \
  --setting_id "a0eb0be9-f0ff-4aee-9dee-69d9fd20110a" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --generate_audio true \
  --wait --json > job.json
```

**Replicate a Hyper Motion CGI showcase for Motilli (no avatar/hook):**
```bash
higgsfield generate create marketing_studio_video \
  --prompt "Slow-motion CGI of celery fibers swirling around the Motilli jar, golden honey droplets, soft daylight, 5s pure product hero shot" \
  --start-image "$MOTILLI_UPLOAD_ID" \
  --mode product_showcase \
  --aspect_ratio 9:16 \
  --duration 5 \
  --wait --json
```

**Image-then-Kling pipeline (preferred for tight scene control + product fidelity):**
```bash
# Step 1: nano_banana_2 image-to-image keyframe
IMG_JOB=$(higgsfield generate create nano_banana_2 \
  --prompt "<scene description>" \
  --image "$MOTILLI_UPLOAD_ID" \
  --aspect_ratio 9:16 --resolution 2k \
  --wait --json | jq -r '.[0].id')
# Step 2: Kling 3.0 image-to-video animation (5s, sound on)
higgsfield generate create kling3_0 \
  --prompt "<motion + 4 organic imperfection cues>" \
  --start-image "$IMG_JOB" \
  --aspect_ratio 9:16 --duration 5 --mode std --sound on \
  --wait --json
```

**Iterate on a winner:**
```bash
WINNER=$(jq -r '.brands.lunessa.winning_refs.ugc[0]' products.json)
higgsfield generate create marketing_studio_video \
  --prompt "<variation prompt>" \
  --start-image "$LUNESSA_UPLOAD_ID" \
  --mode ugc \
  --ad_reference_id "$WINNER" \
  --count 4 \
  --wait --json
```

## Output Structure

```
higgsfield-output/
├── analysis/
│   └── reference_analysis.json      # Step A
├── jobs/
│   └── <unix_ts>_<image|video>.json # Raw CLI JSON per job
├── generated/
│   ├── ugc_20260507_1432_v1.mp4
│   └── ...
└── manifest.json                    # Source of truth for every job
```

## Failure Modes & Guardrails

- **"Not authenticated"** → `higgsfield auth login` (interactive, browser device flow)
- **Workspace not set** → `higgsfield workspace set 7185c910-9954-4029-9d11-0fde8ed1a767`
- **Hook/setting passed to non-UGC-family preset** → Server returns 400. Strip those fields for `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on`.
- **Avatar drift across multi-clip runs** → Use a trained Soul Character, not a one-off
- **Brand voice off** → Ensure ≥ 5k chars of vault context made it into the script-adaptation prompt
- **Credit burn on bad runs** → ALWAYS run `generate cost` first; default `--count 1` for first iteration

## Memory Hooks

After each successful run, persist:
- `higgsfield_product_id` → `products.json` (one-time per brand)
- Trained `soul_id`s → `products.json`
- Winning `job_id`s → `products.json` `winning_refs[brand][preset]`

After feedback sessions, update [PRESETS.md](PRESETS.md) routing rules if the user disagrees with a routing decision.

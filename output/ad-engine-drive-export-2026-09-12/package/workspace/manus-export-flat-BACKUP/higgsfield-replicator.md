# Higgsfield Marketing Studio Ad Replicator

This document is a strategic orchestration layer on top of Higgsfield's Marketing Studio generation feature (see the companion Higgsfield generation reference for the underlying model/API mechanics). It does the brand-specific upstream work — analyzing a reference ad, routing it to the right Marketing Studio preset, adapting the script into brand voice, and resolving a brand's product/avatar entities — then fires the actual generation call. Use it whenever the goal is to replicate, adapt, or one-click-produce a branded ad video or image from a reference ad (an image or video) for a specific brand, using Higgsfield's Marketing Studio presets (UGC, Tutorial, Unboxing, Hyper Motion / Product Showcase, Product Review, TV Spot, Wild Card, UGC Virtual Try On, Pro Virtual Try On).

Defer to a manual, frame-by-frame replication approach (generate a keyframe image with an image model, then animate it with a video model, stitching results together) instead of this Marketing Studio pipeline when:
- The reference is a non-standard creative style that doesn't fit any Marketing Studio preset (e.g. claymation, custom 3D animation).
- The user explicitly declines Marketing Studio / Higgsfield for this job.

For a raw, no-routing generation request with no brand/reference-replication logic involved (e.g. "just generate me a portrait"), use the companion Higgsfield generation reference directly instead of this pipeline.

## GOLDEN NUGGET DOCTRINE (mandatory, applies to any hook/angle/script/concept/audit produced here)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: is this the topic, or is this the motive? If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget leads — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting. When analyzing a reference ad/funnel instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/customer-voice/forum data until it does — never default to a surface angle.

## How to use this

### Setup (one-time per environment)

1. Install the Higgsfield CLI and complete the interactive login flow (see the companion Higgsfield generation reference, Step 0).
2. Set an active workspace: check status, then select the workspace ID for the account being used (`higgsfield workspace set <workspace_id>`).
3. If a fresh session shows "Not authenticated" or the workspace isn't set, re-run auth login and workspace set before continuing.

### Required inputs to collect before starting

1. **Reference ad** — a local file (image or video) or a URL to a reference ad or product page.
2. **Brand** — the brand this ad is being produced for, along with its voice/positioning notes and a hero product image.
3. **Preset** (optional) — one of: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_showcase`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`. If omitted, pick one using the Preset Routing decision tree below.
4. **Soul Character** (optional) — a pinned, trained identity/character ID for identity-locked avatar work.
5. **Hook / Setting** (optional, UGC-family presets only) — IDs from the Hooks & Settings catalog below.
6. **Aspect ratio** (optional) — `9:16` (default), `1:1`, `16:9`, `auto`.
7. **Duration** (optional) — 4–15s for video.
8. **Variations** (optional) — count 1–4, default 1.

### Pipeline

```
Reference Ad
  |
  v
[A] Analyze the reference → why it works + format classification
  |
  v
[B] Route to a preset (see Preset Routing below)
  |
  v
[C] Resolve the brand's product entity in Marketing Studio (create it if this brand hasn't been set up yet)
  |
  v
[D] Resolve an avatar (trained Soul Character, one-off avatar, or Marketing Studio default)
  |
  v
[E] Adapt the script into brand voice
  |
  v
[F] Pre-flight cost check before spending credits
  |
  v
[G] Generate via the marketing image or marketing video model
  |
  v
[H] Save outputs and log every job to a manifest
  |
  v
[I] On approval, pin the generation ID as a reusable "winning reference" for future remixes
```

### Step A — Analyze the reference

- **Image references:** work out why it works — composition, style, angle, target audience, how the product is presented.
- **Video references:** produce a full transcript plus a per-scene visual breakdown, and classify the format (`talking_head_ugc`, `unboxing`, `tv_spot`, `product_showcase`, `product_review`, `ugc_how_to`, `virtual_try_on`).

Save this analysis somewhere retrievable for the rest of the run (e.g. a local `analysis` file).

### Step B — Route to a preset

Use the Preset Routing decision tree below. The resulting preset slug becomes the `--mode` value on the generation call — note the mode enum uses slugs like `ugc_how_to` and `product_showcase`, not the human-readable UI labels ("Tutorial", "Hyper Motion").

### Step C — Resolve the brand's product entity

Check whether this brand already has a registered Marketing Studio product ID (see the Product/Brand Cache section below for what to track). If not, set it up once, using one of two paths:

**Path 1 — from a product URL** (best when there's a clean product page):
```bash
higgsfield marketing-studio products fetch \
  --url "https://example.com/products/<slug>" \
  --wait \
  --json | jq -r '.id'
```
Save the returned `id` against this brand for future runs.

**Path 2 — from a local hero image** (use when there's no clean product URL):
```bash
UPLOAD_ID=$(higgsfield upload create "/path/to/hero.png" --json | jq -r '.id')
higgsfield marketing-studio products create \
  --title "<Product name>" \
  --description "<one-line product description>" \
  --image "$UPLOAD_ID" \
  --json | jq -r '.id'
```
Save the returned ID against this brand.

To find an existing product by name instead of re-creating it:
```bash
higgsfield marketing-studio products list --limit 50 --json | jq '.items[] | {id, title}'
```

### Step D — Resolve an avatar

Three modes, in order of preference:

1. **Pinned Soul Character** — a trained, reusable identity/character reference. Look it up in the Soul Character list, or in the Marketing Studio avatar library (avatars created via `marketing-studio avatars create`):
```bash
higgsfield soul-id list --json | jq '.items[] | {id, name, status}'
higgsfield marketing-studio avatars list --size 50 --json | jq '.items[] | {id, name}'
```

2. **One-off avatar** — generate quickly with a Soul image model:
```bash
higgsfield generate create soul_2 \
  --prompt "<avatar description from brand voice notes>" \
  --aspect_ratio 9:16 \
  --wait --json
```
Use the returned result URL or ID as a reference image for the next step.

3. **Marketing Studio default** — omit the avatar entirely and let Marketing Studio pick from its library. Note: identity will drift from run to run under this option.

To train a reusable Soul Character (one-time, roughly 10 minutes, needs 5–20 reference photos of the same person):
```bash
# upload photos
for f in photo*.jpg; do higgsfield upload create "$f" --json | jq -r '.id'; done
# train
higgsfield soul-id create \
  --name "<character name>" \
  --soul-2 \
  --image <id1> --image <id2> --image <id3> --image <id4> --image <id5>
# wait for training to complete
higgsfield soul-id wait <returned_soul_id>
```
Save the resulting `soul_id` against this brand and character name for reuse.

### Step E — Adapt the script

- Load brand voice/positioning/research notes (as much relevant context as is available).
- Combine the original reference transcript with that brand context to produce a new script: preserve the narrative structure, swap in the new product/mechanism/competitive framing, and adapt the voice to the brand.
- Output: a single prompt string for the generation call, plus per-scene narration if the preset is multi-scene (TV Spot / Tutorial).
- For static image references, this step only needs to produce the `--prompt` value.

### Step F — Pre-flight cost check

Always run a cost estimate before creating a job — it's free and catches expensive runs early:
```bash
higgsfield generate cost marketing_studio_video \
  --prompt "<adapted prompt>" \
  --start-image <product_image_path_or_id> \
  --mode ugc \
  --aspect_ratio 9:16 \
  --duration 8 \
  --json
```
If the estimated credits are high (well above typical single-run cost), or the account balance is less than the estimate times the number of variations plus a safety buffer, stop and confirm before proceeding.

Check the live balance with `higgsfield account status`.

### Step G — Generate

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
  --hook_id "<from Hooks & Settings catalog, UGC-family only>" \
  --setting_id "<from Hooks & Settings catalog, UGC-family only>" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --generate_audio true \
  --resolution 720p \
  --wait \
  --wait-timeout 20m \
  --json > "./higgsfield-output/jobs/$(date +%s)_video.json"
```

**Critical preset rules:**
- `--hook_id` and `--setting_id` are only valid for the presets `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`. Strip them for `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on` — the server rejects them otherwise.
- Media flags accept either a UUID (upload ID, job ID, product ID) or a local file path — paths are auto-uploaded, no separate upload step required.

**Iterating on a winner (remix):**
```bash
# Re-use a prior winning job's style
WINNER_ID=$(jq -r ".brands.<brand>.winning_refs.<preset>[0]" products.json)
higgsfield generate create marketing_studio_video \
  --prompt "<new variation prompt>" \
  --start-image <product_id> \
  --mode ugc \
  --ad_reference_id "$WINNER_ID" \
  --count 4 \
  --wait --json
```

**For multiple variations:** either pass `--count 4` (Marketing Studio Video accepts 1–4), or loop the generate command once per fully independent prompt.

### Step H — Save outputs

The call returns the result URL(s) in its JSON response. Download the asset:
```bash
RESULT_URL=$(jq -r '.results[0].result_url' "./higgsfield-output/jobs/<file>.json")
curl -L -o "./higgsfield-output/generated/<preset>_$(date +%Y%m%d_%H%M)_v1.mp4" "$RESULT_URL"
```

Append each run to a manifest record, e.g.:
```json
{
  "job_id": "...",
  "preset": "ugc",
  "brand": "...",
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

### Step I — Pin winners on approval

Once a generation is approved, record its `id` against the brand and preset as a "winning ref," e.g.:
```json
{
  "brands": {
    "<brand>": {
      "winning_refs": {
        "ugc": ["<job_id_1>", "<job_id_2>"],
        "product_review": ["<job_id_3>"]
      }
    }
  }
}
```
Future runs at the same brand + preset can pass `--ad_reference_id <id>` to seed off the winner.

## CLI reference (quick lookups)

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
| List Marketing Studio products | `higgsfield marketing-studio products list --json` |
| Create Marketing Studio product | `higgsfield marketing-studio products create --title ... --image <upload_id>` |
| Fetch Marketing Studio product from URL | `higgsfield marketing-studio products fetch --url ... --wait --json` |
| List Marketing Studio avatars | `higgsfield marketing-studio avatars list --json` |
| List hooks (UGC-family) | `higgsfield marketing-studio hooks list --size 100 --json` |
| List settings (UGC-family) | `higgsfield marketing-studio settings list --size 100 --json` |
| Train a Soul Character | `higgsfield soul-id create --name X --soul-2 --image id1 --image id2 ...` |
| List Soul Characters | `higgsfield soul-id list --json` |
| Generate (image/video) | `higgsfield generate create <model_id> --prompt ... [--image ...] [--start-image ...] [...] --wait --json` |
| Cost preview | `higgsfield generate cost <model_id> --prompt ... [...] --json` |
| List recent jobs | `higgsfield generate list --json --size 50` |
| Wait for a job | `higgsfield generate wait <job_id> --timeout 20m --interval 5s` |

## Rules & standards

### Cost & credit discipline

- **Always** run a cost estimate before any generate call — it's free.
- Before any run with `--count > 1`, confirm the account balance exceeds the estimate times count plus a 100-credit buffer.
- The marketing video model at 1080p resolution, and the top-tier cinema studio video model, are the most expensive options — flag this explicitly before using them.
- Use 720p for first-pass iteration; only bump to 1080p on confirmed winners.

### Failure modes & guardrails

- **"Not authenticated"** → re-run the login flow.
- **Workspace not set** → set the workspace explicitly before continuing.
- **Hook/setting passed to a non-UGC-family preset** → the server returns an error. Strip those fields for `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on`.
- **Avatar drift across multi-clip runs** → use a trained Soul Character, not a one-off avatar.
- **Brand voice sounding off** → make sure a substantial amount of real brand voice/research context (not just a one-line description) made it into the script-adaptation step.
- **Credit burn on bad runs** → always run the cost estimate first; default to a single variation (`--count 1`) for the first iteration of anything new.

### Memory / record-keeping

After each successful run, persist:
- The brand's Marketing Studio product ID (one-time per brand).
- Any trained Soul Character IDs.
- Winning job IDs, keyed by brand and preset.

After a feedback session, update the preset-routing rules below if a routing decision was overruled — that's a signal the decision tree needs adjusting for that brand/reference type.

## Preset Routing

The 9 Marketing Studio presets are the entire creative surface of the video model. Pick exactly one, based on the reference ad's format. Hooks/settings only apply to the UGC family of presets.

### Decision tree

Run through these tests in order — first match wins.

1. **Is the reference a CGI / hyperlapse / object-flying-through-effects clip with no person speaking?** → `product_showcase` (UI label: "Hyper Motion")
2. **Is it a multi-scene narrative ad with story beats (problem → solution → reveal), 20–60s, polished cinematography?** → `tv_spot`
3. **Is the entire ad someone unwrapping/opening a box and revealing the product?** → `ugc_unboxing`
4. **Is it a step-by-step "how to use / do this with the product" demo?** → `ugc_how_to` (UI label: "Tutorial")
5. **Is it a sit-down "I tried this for X days" / star-rating / pros-and-cons review?** → `product_review`
6. **Is the person trying on clothes/accessories — selfie, casual?** → `ugc_virtual_try_on`
7. **Is the try-on cinematic / editorial / fashion-runway style?** → `virtual_try_on`
8. **Is the reference surreal, weird, stunt-driven, viral-bait, or doesn't fit any preset above?** → `wild_card`
9. **Default fallback: selfie-style talking head, casual delivery, single take.** → `ugc`

### Preset compatibility matrix

The slug is what's passed as `--mode` on the marketing video generation call. (The web UI surfaces labels like "Tutorial" and "Hyper Motion" — always use the CLI slug when generating.)

| UI label | `--mode` slug | Hook/Setting? | Avatar? | Product required? | Best use |
|---|---|---|---|---|---|
| UGC | `ugc` | YES | YES | YES | Talking-head selfie ads |
| Tutorial | `ugc_how_to` | YES | YES | YES | "How to use" demos, step-by-step |
| Unboxing | `ugc_unboxing` | YES | YES | YES | Box reveals, ASMR unwraps |
| Product Review | `product_review` | YES | YES | YES | Sit-down reviews, rating cards |
| UGC Virtual Try On | `ugc_virtual_try_on` | YES | YES | YES (apparel) | Casual selfie try-ons |
| Hyper Motion | `product_showcase` | NO | NO | YES | CGI, slow-mo, product hero shots |
| TV Spot | `tv_spot` | NO | YES | YES | 30s narrative commercials |
| Pro Virtual Try On | `virtual_try_on` | NO | YES | YES (apparel) | Cinematic editorial try-ons |
| Wild Card | `wild_card` | NO | optional | YES | Surreal, viral-bait, custom ideas |

The live mode enum can always be pulled directly from the model's schema if this table goes stale.

### Reference-type → preset examples

| Reference description | Preset |
|---|---|
| UGC car-yapper talking-head ad | `ugc` |
| Animated "inside the body" 3D mechanism ad | `wild_card` (custom prompt) — Marketing Studio has no native animated-3D preset |
| Talking-head expert explaining a mechanism | `ugc` (with an authority-styled avatar) or `product_review` |
| 30s broadcast spot with dramatic music | `tv_spot` |
| Slow-mo product splash into water with ingredients flying around | `product_showcase` |
| "I tried it for 14 days, here's what happened" before/after | `product_review` |
| Outfit-of-the-day featuring an apparel/accessory product | `ugc_virtual_try_on` |
| Editorial fashion-magazine-style shoot featuring a premium product | `virtual_try_on` |
| Recipe video using a kitchen product | `ugc_how_to` |
| Box reveal + unwrapping + product discovery | `ugc_unboxing` |
| Surreal "person casually reviewing the product in an extreme location" | `wild_card` (or `ugc` + an extreme setting) |

### Multi-scene reference strategy

If the reference is a multi-scene 30–60s narrative video, don't try to recreate every scene in one Marketing Studio call. Two options:

- **Option A — `tv_spot` preset, single call:** adapt the entire script into one prompt and let the TV Spot template handle multi-scene production. Best for cinematic references.
- **Option B — chained UGC clips:** split the reference into ~5-second beats, generate each as a separate `ugc` clip, then stitch them together externally. Use this when avatar consistency across all clips matters more than cinematic flow. Pin the same Soul Character and setting ID across all clips.

For animated/3D references that don't match any preset, fall back to a manual video-generation approach (an image-to-video model, not Marketing Studio) — there's no native 3D-animation preset here.

## Hooks & Settings (UGC-family presets only)

Hooks and settings are Marketing Studio's reusable openers and locations. They apply ONLY to `--mode` values: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`. For `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on` — do not pass `--hook_id` or `--setting_id` (server validation rejects them).

### How to use

1. Pick a hook (the opener) and/or a setting (the location).
2. Pass the IDs to the video generation call (`--hook_id <uuid> --setting_id <uuid>`).
3. Both are optional — Marketing Studio auto-picks defaults if omitted.

To get the live full list (this catalog is a snapshot and Higgsfield adds new items regularly — re-fetch before any production run):
```bash
higgsfield marketing-studio hooks list --size 100 --json | jq '.items[] | {id, name, type}'
higgsfield marketing-studio settings list --size 100 --json | jq '.items[] | {id, name, type}'
```

### Hook catalog (snapshot)

Hooks are openers that solve the "stop the scroll in the first 1.5s" problem. Two types: `subtle` (natural, narrative) and `stunt` (chaotic, attention-grabbing).

| Name | Type | ID | Use for |
|---|---|---|---|
| Product Hit | stunt | `3d45fb46-254f-4c83-9685-8e3d28945a67` | High-energy ads, sports, snacks, tech |
| Spicy | subtle | `75b6d501-be0e-4416-a7ed-52f04f180574` | Beauty, makeup, fashion (close-up to selfie reveal) |
| Interview | subtle | `26cac2dd-99cb-4818-a678-509b0dab2c32` | Lifestyle/aspirational (food, wellness) |
| Random Object Mic | stunt | `d50eb41c-fcfa-4f4d-93aa-473cdc6bc3b2` | Comedy, viral-bait, casual products |
| Product Crash | subtle | `8101cd3e-3cc9-4607-a171-3582daa2f6ee` | Durability proof, drama-pivot reviews |
| Blizzard | stunt | `31976cc7-e597-4be2-9753-4a80153b0cc7` | Outdoor/durability, electronics, drinks |
| Camera Bump | subtle | `2db84ed8-7082-4981-9c9c-9d61b3c28668` | Fashion, accessories, casual reveal |
| Product Dodge | stunt | `5443eff1-d940-4ad3-9413-957bb048a6b0` | Fast-paced reviews, snacks, tech |
| Epic Fail | subtle | `ec9fdf99-314d-480d-a656-10d9861341e7` | Comedy, casual UGC, fitness products |

### Setting catalog (snapshot)

Settings are the location/environment. Two types: `realistic` (everyday) and `unrealistic` (surreal/cinematic).

| Name | Type | ID | Use for |
|---|---|---|---|
| Bedroom | realistic | `b8368076-35eb-4045-b33b-74b2646d9863` | Wellness, sleep, beauty, supplements (evening routine) |
| Bathroom | realistic | `189fa1ac-1fdc-44f4-bdea-8804a76f0659` | Beauty, skincare, hygiene, supplements (mirror selfie) |
| Kitchen | realistic | `a0eb0be9-f0ff-4aee-9dee-69d9fd20110a` | Food, supplements, gummies, drinks (daily-routine) |
| Gym | realistic | `6bfbe372-e50a-4900-adee-d4cbd0db8a2f` | Fitness, recovery, energy, supplements |
| Office | realistic | `d39dda10-643c-44e2-bfc8-2451dddde7d9` | Productivity, focus supplements, work-from-home |
| In Car | realistic | `fdfa032c-801f-4602-8dfd-1162b0f8c9c9` | Talking-head errands-day energy |
| Street | realistic | `8c95f9ba-5849-44b1-82d0-9f6b33240758` | Fashion, accessories, urban discovery |
| Nature | realistic | `10f47b85-abd7-4899-b6b6-91ff2969d3bf` | Outdoor gear, wellness, mindfulness, fashion |
| Airplane Wing | unrealistic | `b03705e5-bbed-4d83-8d29-3bc2101cd14f` | Surreal viral-bait, durability claims |
| Roofing | unrealistic | `3cf2164e-ffac-4867-9c43-1d673a5cb28a` | High-energy lifestyle, "unbothered" attitude |
| Volcano Rim | unrealistic | `e99c2ee8-3c4a-4697-9a58-908e73c9ad38` | Extreme durability, viral comedy |
| Tiny Reviewer | unrealistic | `f495493f-0251-4bd7-afc0-90bc6a862e04` | Scale-play, hero product showcase |
| Car Roof | unrealistic | `d6992aea-4521-4606-9e4f-8c766e12622c` | Action/lifestyle, never-flinch energy |
| Train Surf | unrealistic | `71f61bb0-dfd9-459b-a220-0dd468b977d5` | Wind/durability proof, viral stunt |

### Stunt hooks: when to use

Stunt hooks (Product Hit, Random Object Mic, Blizzard, Product Dodge, Volcano Rim, etc.) are for top-of-funnel scroll-stoppers — they trade trust for attention.

- **Use for:** new audience cold traffic, pattern-interrupt creative tests, "viral angle" experiments.
- **Avoid for:** high-trust niches (medical, financial, premium luxury) where the absurdity undermines authority — prefer subtle hooks in those categories, and avoid stunt hooks entirely for premium/luxury positioning.

### Combining with brand voice

The hook + setting + adapted-script chain works best when the script LEANS INTO the chosen scene rather than ignoring it. Examples:
- A surreal/extreme setting (e.g. Volcano Rim) paired with a trust-driven health brand: bad fit, kills trust.
- The same surreal setting paired with a brand whose angle is genuinely "extreme durability": great fit — reference the setting directly in the script.
- Kitchen setting paired with a food/supplement/gummy brand: natural fit — have the avatar reach for the product mid food-prep.

When in doubt, the realistic settings (Bedroom, Kitchen, Bathroom, Gym, Office, In Car, Street, Nature) are safer for direct-response performance. Surreal settings reward the right brand fit but burn engagement when forced.

## Product/brand cache structure

Behind this pipeline sits a small cache (a JSON file, keyed by brand) that avoids re-creating Marketing Studio entities on every run. Its fields per brand:

- `higgsfield_product_id` — the Marketing Studio product entity ID once created (null until Step C has run once for that brand).
- `hero_image` — a reference to the brand's locked product hero image, used to create the product entity.
- `default_product_context` — a one-line product description used as a fallback when adapting scripts.
- `soul_characters` — a map of trained, reusable avatar identities for that brand.
- `winning_refs` — a map of preset → list of approved job IDs, used to seed remixes via `--ad_reference_id`.
- `higgsfield_upload_id` — occasionally cached separately when a raw upload ID (pre-product-entity) is reused across runs.

If a brand has no `higgsfield_product_id` yet, run the Step C setup once and save the result back into this structure before generating anything for that brand.

## Templates & examples

**Replicate a viral UGC ad for a supplement brand:**
```bash
# Step C: setup product (one-time)
PRODUCT_ID=$(higgsfield marketing-studio products create \
  --title "Heart Health Supplement" \
  --description "Red Yeast Rice + CoQ10 for women 50+" \
  --image "/path/to/hero-image.jpg" \
  --json | jq -r '.id')

# Step F: cost check
higgsfield generate cost marketing_studio_video \
  --prompt "<adapted script>" \
  --start-image "$PRODUCT_ID" \
  --mode ugc \
  --hook_id "26cac2dd-99cb-4818-a678-509b0dab2c32" \
  --setting_id "a0eb0be9-f0ff-4aee-9dee-69d9fd20110a" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --json

# Step G: generate
higgsfield generate create marketing_studio_video \
  --prompt "<adapted script>" \
  --start-image "$UPLOAD_ID" \
  --mode ugc \
  --hook_id "26cac2dd-99cb-4818-a678-509b0dab2c32" \
  --setting_id "a0eb0be9-f0ff-4aee-9dee-69d9fd20110a" \
  --aspect_ratio 9:16 \
  --duration 8 \
  --generate_audio true \
  --wait --json > job.json
```

**Hyper Motion CGI showcase, no avatar/hook needed:**
```bash
higgsfield generate create marketing_studio_video \
  --prompt "Slow-motion CGI of ingredients swirling around the product jar, golden droplets, soft daylight, 5s pure product hero shot" \
  --start-image "$UPLOAD_ID" \
  --mode product_showcase \
  --aspect_ratio 9:16 \
  --duration 5 \
  --wait --json
```

**Image-then-video pipeline (for tight scene control + product fidelity):**
```bash
# Step 1: image-to-image keyframe with a character/cartoon-capable model
IMG_JOB=$(higgsfield generate create nano_banana_2 \
  --prompt "<scene description>" \
  --image "$UPLOAD_ID" \
  --aspect_ratio 9:16 --resolution 2k \
  --wait --json | jq -r '.[0].id')
# Step 2: animate with a cheaper single-plane video model, sound on
higgsfield generate create kling3_0 \
  --prompt "<motion + a few natural imperfection cues>" \
  --start-image "$IMG_JOB" \
  --aspect_ratio 9:16 --duration 5 --mode std --sound on \
  --wait --json
```

**Iterate on a winner:**
```bash
WINNER=$(jq -r '.brands.<brand>.winning_refs.ugc[0]' products.json)
higgsfield generate create marketing_studio_video \
  --prompt "<variation prompt>" \
  --start-image "$UPLOAD_ID" \
  --mode ugc \
  --ad_reference_id "$WINNER" \
  --count 4 \
  --wait --json
```

## Output structure

```
higgsfield-output/
├── analysis/
│   └── reference_analysis.json      # Step A
├── jobs/
│   └── <unix_ts>_<image|video>.json # Raw job JSON per run
├── generated/
│   ├── ugc_20260507_1432_v1.mp4
│   └── ...
└── manifest.json                    # Source of truth for every job
```

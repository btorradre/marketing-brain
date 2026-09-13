# Higgsfield AI Generation

This document explains how to generate images and videos through Higgsfield AI, and how to use Higgsfield's "Marketing Studio" feature to produce branded ad content (UGC-style videos/images built from an avatar, a product, and optional hooks/settings). Use this whenever a task calls for generating an image, generating a video, animating a still photo (image-to-video), editing/stylizing/remixing an existing image, or producing a branded ad, UGC video, product demo, unboxing video, TV-spot-style commercial, or presenter video. It covers text-to-image, image-to-image, image-to-video, reference-based generation, and the Marketing Studio ad pipeline.

This document does not cover: training a persistent, reusable character/identity reference ("Soul Character") beyond the basic commands noted below; a dedicated product-photoshoot workflow (a specialized pipeline layered on top of one of the image models with extra prompt templates for Pinterest pins, lifestyle shots, hero banners, ad packs, and virtual try-on); generating marketplace/listing card images; or text/chat/TTS tasks.

Access is via the `higgsfield` command-line tool, which wraps Higgsfield's generation API. Any agent with the ability to run shell commands can drive it directly.

## How to use this

### Step 0 — Get set up

1. Check whether the `higgsfield` CLI is installed and on the system path. If not, install it:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
   ```
2. Check authentication with `higgsfield account status`. If it fails with "Session expired" or "Not authenticated", run `higgsfield auth login` (this opens an interactive browser-based device-flow login) and wait for it to complete before continuing.
3. If `higgsfield account status` already prints account info, skip both steps.

### General rules for how to behave while doing this

1. Be concise. Don't print raw IDs or JSON dumps in chat — print the result URL when the job is ready.
2. No internal jargon. Don't narrate mechanical steps like "calling higgsfield cost" or "polling job."
3. Detect the requester's language from their first message and reply in it. Technical arguments (e.g. `--aspect_ratio 16:9`) stay in English regardless.
4. Don't batch-ask for every parameter up front. Pick a sane default model and ask only about what's genuinely missing, one thing at a time.
5. Don't pre-estimate cost unless asked. Just submit the job.
6. Always pass `--wait` to `generate create` so the command blocks until the job finishes and prints the result URL itself, instead of using a separate create-then-poll pattern.

### Workflow — generic generation

1. **Pick a model.** See the Models section below for the full decision guide. Quick summary:
   - **Images:** default to GPT Image 2 for general/high-fidelity work (graphic design, UI, banners, typography). Use Nano Banana 2 for character/cartoon work (step up to Nano Banana Pro on hard cases). Use Soul 2.0 for aesthetic UGC/fashion editorial. Soul Cinema for cinematic stills. Soul Cast for a highly characterful, text-only persona. Soul Location for environments with no people (best in class). Seedream 4.5 for vector illustration or complex face-anchored scene edits. Z Image for fast, cheap iteration.
   - **Video:** default to Seedance 2.0 for serious, multi-shot, motion-heavy production work (SOTA). Use Kling 3.0 as a cheaper substitute for single-plane scenes without heavy motion. Seedance 1.5 Pro for a cheap clean single-take shot. Cinema Studio Video 3.0 for cinema-grade highest fidelity. Minimax Hailuo for cheap footage with strong physics and no audio need. Veo 3.1 Lite for fast batch/volume work. Any advertising/commercial/branded ad video should go through Marketing Studio instead (see below).
   - To find the exact model identifier to submit, list all models and match by display name (`higgsfield model list --json`). See the Models section for the full table.
2. **Pass media inputs straight to the relevant flags.** Media flags (`--image`, `--start-image`, `--end-image`, `--video`, `--audio`) accept either a local file path or a UUID (an upload ID or a previous job ID) — paths are auto-uploaded, no separate upload step is required. Each model only accepts certain roles; see the Media Inputs section.
3. **Validate quickly if unsure of parameters.** Run `higgsfield model get <model_id> --json` once and pass only what's needed; otherwise rely on schema defaults. The server returns non-fatal "adjustments" for values it coerces (e.g. an invalid aspect ratio snapped to the closest match) and a structured error for genuinely invalid parameter values.
4. **Submit and wait in one shot:**
   ```bash
   higgsfield generate create <model_id> --prompt "..." [media flags] [param flags] --wait
   ```
   This blocks until the job reaches a terminal state and prints the result URL. Tunables: `--wait-timeout 20m` (default 10m), `--wait-interval 5s` (default 3s).
5. **Deliver.** Return the result URL plus a one-line summary (model used, duration if video).

To inspect or rerun a past job: `higgsfield generate list --json` and `higgsfield generate get <id> --json`. If a job was started without `--wait`, rejoin it with `higgsfield generate wait <id>`.

### Common parameter examples

```bash
higgsfield generate create gpt_image_2 --prompt "neon city at dusk" --aspect_ratio 16:9 --resolution 2k --wait
higgsfield generate create nano_banana_2 --prompt "anime character concept, expressive pose" --image ./ref.png --wait
higgsfield generate create seedance_2_0 --prompt "camera dollies in" --start-image ./first.png --duration 8 --wait
higgsfield generate create text2image_soul_v2 --prompt "..." --soul-id <soul_ref_id> --quality 2k --wait
```

For machine-readable output (e.g. when chaining into further automated steps), add `--json`. With `--wait --json` the final job object array is returned; without `--wait`, just the job IDs.

Prompt can also be piped via stdin: `echo "..." | higgsfield generate create z_image --wait`.

**Soul image quality:** for `text2image_soul_v2` and `soul_cinematic`, pass `--quality 1.5k` or `--quality 2k`. These are UI-facing tiers; the backend maps them to `720p`/`1080p` and model-specific dimensions based on the selected `--aspect_ratio`. `soul_location` has no quality selector — its dimensions are fixed per aspect ratio.

## Rules & standards — errors

- `Missing required params: prompt` → no prompt was given; ask for one.
- `Invalid values: aspect_ratio=99:99 (allowed: ...)` → a bad enum value; pick from the allowed list.
- `Unknown params: foo` → the model's schema doesn't accept that flag; check `higgsfield model get <model_id>`. If this happens for `hook_id` or `setting_id`, the selected model does not support Marketing Studio setup items.
- `Session expired` → run `higgsfield auth login` again.

See the Troubleshooting section for the full error/fix list.

---

## Models

Preferred defaults for quick-start guidance:
- **Images:** GPT Image 2 (general/high-fidelity) and Nano Banana 2 (character/cartoon).
- **Video:** Seedance 2.0 (all-purpose serious video).

### Image models

| Model | Provider | What it's for |
|---|---|---|
| Nano Banana 2 | Google | **Fast everyday default for character work.** Edits, general generation, character/cartoon/animated-style outputs. Reach for this when the brief calls for character or cartoon-style image generation. |
| Nano Banana Pro | Google | **Top-tier Nano Banana.** Same canvas as Nano Banana 2 with extra fidelity and accuracy on harder briefs. Pick when 2 isn't getting there. |
| Nano Banana | Google | Reliable, budget-friendly entry in the Nano Banana family — same realistic look at a lighter price point. |
| Higgsfield Soul 2.0 | Higgsfield | **Aesthetic UGC, fashion editorial, character generation.** Editorial/lifestyle/"magazine cover" briefs. Soul-aware (accepts a Soul Character reference). |
| Soul Cinema | Higgsfield | **Cinematic stills, film-grade lighting.** Pick for "cinematic" requests or concept-art mood. |
| Soul Cast | Higgsfield | **Distinctive, characterful personas.** For a creative, expressive character rather than photoreal default. Text-only (no reference image). |
| Soul Location | Higgsfield | **Best-in-class environments and locations.** Unmatched for pure scene/place generation without a person in frame. |
| Seedream 4.5 | Bytedance | **Vector illustrations and complex scene edits with faces.** For a face-anchored photo edit into a complex new scene (more than an outfit change), without heavy filters. |
| Seedream 5.0 Lite | Bytedance | Same Seedream lineage as 4.5, faster turnaround for visual-reasoning and instruction-based edits. |
| Z Image | Tongyi-MAI | **Fastest in the catalog.** Built for speed, drafts, and LoRA-driven stylization. Pick when the brief is "fast and cheap, let me iterate." |
| Flux 2.0 | Black Forest Labs | Precise prompt adherence with multiple variants (pro, flex, max). A strong creative alternative for a different look from the Banana family. |
| Flux Kontext Max | Black Forest Labs | **Context-aware editing and style transfer.** Strong for anime, stylized looks, typography remix — when defaults feel too generic. |
| Kling O1 Image | Kling | Versatile photorealistic image generation with broad aspect-ratio support. |
| GPT Image 1.5 | OpenAI | Earlier-generation OpenAI image model with editing and text-rendering capabilities. |
| GPT Image 2 | OpenAI | **Default high-fidelity image generation.** Graphic design, UI, banners, typography, and any brief with on-image text. |
| Grok Imagine | xAI | Expressive, high-contrast, bold creative outputs. Worth trying for anime and stylized looks. |
| Cinema Studio Image 2.5 | Higgsfield | Cinematic still frames up to 4K, dramatic film look. |
| Marketing Studio Image | Higgsfield | **Branded image ads.** Retrieval-augmented over the user's avatars and products — runs inside the Marketing Studio flow. |
| Auto | Higgsfield | **Smart routing layer.** Picks the best image model from the prompt automatically. Use when intent is open and you don't want to commit to a specific model. |

### Video models

| Model | Provider | What it's for |
|---|---|---|
| Seedance 2.0 | Bytedance | **SOTA all-purpose video.** Crisp, consistent identity, multi-shot capable. Default for any serious motion/cinematic/production brief. |
| Kling 3.0 | Kling | **Cheaper Seedance 2.0 substitute** for single-plane scenes that don't need heavy motion. Multi-shot, audio sync, motion transfer. |
| Seedance 1.5 Pro | Bytedance | A budget-friendly Seedance for clean single-take shots. |
| Marketing Studio | Higgsfield | **All advertising and commercial video** — UGC, unboxing, TV spot, product showcase. Default whenever the brief is "make an ad." |
| Cinema Studio Video 3.0 | Higgsfield | **Top-tier cinema-grade execution.** For film-look briefs at highest fidelity. |
| Veo 3.1 Lite | Google | **Fast and cost-effective Veo.** Built for batch and volume work. |
| Google Veo 3.1 | Google | Ultra-realistic, top-tier cinematic quality. Quality tiers basic/high/ultra. Format set constrained — verify accepted aspect ratio and duration before submitting. |
| Google Veo 3 | Google | Reliable cinematic with broad creative range and audio support. |
| Minimax Hailuo | Hailuo | **Cheap with strong physics.** Solid budget pick when natural-physics motion matters; no audio in current variants. |
| Wan 2.7 | Wan | Synchronized audio with character-consistent video. Newer Wan release. |
| Wan 2.6 | Wan | Open-weight, stylized, experimental creative. Cheap option when the brief is intentionally artistic. |
| Kling 2.6 | Kling | Cinematic motion with advanced physics — earlier Kling release alongside 3.0. |
| Grok Imagine (video) | xAI | Text and image-to-video with audio support. Worth trying for stylized creative briefs. |
| Cinema Studio Video | Higgsfield | Cinematic compositions with dramatic mood. Use Cinema Studio Video 3.0 as the modern default. |
| Cinema Studio Video v2 | Higgsfield | Refined cinematic camera and color with genre control. Use Cinema Studio Video 3.0 as the modern default. |

### Picking flow — image (in order, higher entry wins when two could apply)

1. Brand product visual work (Pinterest pin, lifestyle shot, hero banner, ad pack, virtual try-on) is generally best served by a dedicated product-photoshoot-style workflow layered on top of GPT Image 2 with mode-specific prompt templates, rather than a bare model call — keep that distinction in mind, but a direct model call still works if no such specialized workflow is available.
2. Branded ad image with presenter avatar + product (Marketing Studio shape, retrieval-augmented over the user's assets) → Marketing Studio Image.
3. Aesthetic UGC / fashion editorial / lifestyle character → Soul 2.0.
4. Cinematic still frame → Soul Cinema.
5. Highly characterful, creative character (text-only, distinctive persona, no reference photo) → Soul Cast.
6. Locations / environments / no-people scenes → Soul Location. Best in class — nothing else matches.
7. Vector illustrations OR face edit + complex scene swap (more than an outfit change, no heavy filters) → Seedream 4.5. Seedream 5.0 Lite for the same niche but faster.
8. A trained, reusable character/identity reference ("Soul Character") → Soul 2.0 for stills, Soul Cinema for cinematic vibe.
9. Anime / stylized / non-default look where defaults feel flat → Flux Kontext Max or Grok Imagine. Worth trying.
10. Character or cartoon-style work → Nano Banana 2; step up to Nano Banana Pro on hard cases.
11. Fast and cheap iteration / drafts / LoRA work → Z Image.
12. Default for everything else → GPT Image 2. High-fidelity general generation, graphic design, UI, banners, anything with on-image text.
13. Intent-only request, no preference, want auto-routing → Auto.

### Picking flow — video (in order)

1. All advertising / commercial video (UGC, unboxing, TV spot, product showcase, branded ad) → Marketing Studio. See Marketing Modes below.
2. Default all-purpose serious video (multi-shot, consistent identity, motion-heavy, production work) → Seedance 2.0. SOTA.
3. Single-plane scene without strong dynamics, cheaper → Kling 3.0. Substitute for Seedance 2.0 when motion isn't critical.
4. Cheap clean shot without cuts → Seedance 1.5 Pro.
5. Image-to-video with an explicit first frame → Kling 3.0 with a start frame, or Seedance 2.0 with a start frame for higher motion.
6. Cinema-grade execution (highest fidelity, film look) → Cinema Studio Video 3.0.
7. Cheap with strong physics, audio not needed → Minimax Hailuo.
8. Fast batch / volume → Veo 3.1 Lite.
9. Veo-format-bound work (specific aspect ratio/duration set Veo accepts) → Veo 3.1; Veo 3 is slightly behind.
10. Stylized / animation-style edit-driven work → Wan 2.7.
11. Stylized cheap experimental → Wan 2.6.
12. Anime / bold-style outputs where defaults feel flat → Grok Imagine (video). Worth trying.

### Things to keep in mind

- **Don't invent model names.** List all models if unsure — submitting an unknown model returns `unknown model "..."`.
- **Audio reference for Seedance 2.0** comes through media inputs with role `audio`, not via a separate `generate_audio` flag.
- **Text-only models reject reference images.** Z Image, Soul Cast, Soul Location, and some Wan configurations are text-only; pass no media flags to them.
- For cinema video, prefer Cinema Studio Video 3.0 as the modern default; reach for earlier Cinema Studio Video variants only when specifically named.
- When a specific model is named, use it — the defaults above cover common intents; the rest of the catalog exists for users who know what they want.

### Media role conventions (quick reference)

| Model | Accepted media roles |
|---|---|
| Seedance 2.0 | `image`, `start_image`, `end_image`, `video`, `audio` |
| Kling 3.0 | `start_image`, `end_image` |
| Kling 2.6 | `start_image` |
| Veo 3.1 | `start_image` (max 1) |
| Veo 3 | `image` (max 1) |
| Marketing Studio (video) | `image`, `start_image`, `end_image` |
| Most image models | `image` (1+) |
| Z Image, Soul Cast, Soul Location | none — text-only |

For simple image-to-video, `start_image` is the role you want. For pure video models that only declare `image`, the `image` flag is auto-remapped to `start_image`.

### Aspect ratios and durations

These are model-specific; unsupported values are clamped to the nearest allowed one with an "adjustments applied" note when the model declares a closed set. Check per-model if in doubt. Common patterns:

- **Seedance 2.0** image: `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`. Duration 4–15s.
- **Kling 3.0**: `16:9`, `9:16`, `1:1`. Duration 3–15s. Modes `pro`/`std`. Sound `on`/`off`.
- **Soul 2.0**: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`. Quality `1.5k` or `2k` maps to backend `720p`/`1080p`.
- **Soul Cinema**: same as Soul 2.0 plus `21:9`. Quality `1.5k` or `2k`.
- **Soul Location**: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`, `9:21`. No quality/resolution selector; dimensions are fixed by aspect ratio.
- **Veo 3.1**: `16:9` or `9:16`. Duration `4`, `6`, or `8` only. Quality `basic`/`high`/`ultra`.
- **Marketing Studio (video)**: `auto`/`21:9`/`16:9`/`4:3`/`1:1`/`3:4`/`9:16`. Resolution `480p` or `720p`.

### Response feedback types

- **Adjustments** — a non-fatal coercion (e.g. an unsupported aspect ratio snapped to the closest allowed value). Included in the response, job still proceeds.
- **Validation error** — a fatal mismatch (unknown declared parameter, or an unsupported media role). Returns an error and does not submit.

---

## Media Inputs

How to pass reference images, videos, and audio.

### Path or UUID — both work

Each media flag accepts either a local file path or a UUID. Paths are auto-uploaded before submission; a UUID is auto-detected as either an upload ID or a previous job ID.

```bash
# Local path — auto-uploaded
higgsfield generate create nano_banana_2 --prompt "stylize in watercolor" --image ./photo.png --wait

# Upload id (from a prior upload)
higgsfield generate create nano_banana_2 --prompt "..." --image <upload_id> --wait

# Job id from a previous generation
higgsfield generate create seedance_2_0 --prompt "anim" --start-image <previous_job_id> --wait
```

Type is auto-detected from the file extension:
- Image: `png`, `jpg`/`jpeg`, `webp`, `gif`
- Video: `mp4`, `mov`, `webm`
- Audio: `mp3`, `wav`, `m4a`, `ogg`

### Roles by model family

Each model declares a closed set of accepted roles. Passing the wrong role is rejected locally before submission.

| Model | Accepted roles | Notes |
|---|---|---|
| Most image models (Nano Banana 2, Flux 2, Seedream 4.5, GPT Image 2, …) | `image` | 1+ references, often up to 8. |
| Seedance 2.0 | `image`, `start_image`, `end_image`, `video`, `audio` | Audio is via the `audio` role, NOT via a `generate-audio` flag. |
| Kling 3.0 | `start_image`, `end_image` | Image-to-video with optional last-frame transition. |
| Kling 2.6 | `start_image` | Single frame anchor. |
| Veo 3.1 | `start_image` | Max 1 reference. |
| Veo 3 | `image` | Single image-to-video. |
| Marketing Studio Video | `image`, `start_image`, `end_image` | Plus `avatars`, `product_ids`, `assets` as separate fields. |
| Z Image, Soul Cast, Soul Location | (none) | Text-only. Reject media inputs. |

For simple image-to-video on a model that only declares `image`, that flag is auto-remapped to `start_image` when unambiguous. When in doubt, fetch the model's schema to see its accepted media roles.

### Multiple images

Most image models accept multiple references — repeat the image flag:

```bash
higgsfield generate create nano_banana_2 --prompt "..." \
  --image ./a.png --image ./b.png --image <upload_id> \
  --wait
```

Single-reference video models (Veo 3, Veo 3.1, Kling 2.6) reject extra images with an error before submission.

### Audio reference (Seedance)

Seedance 2.0 is the one model that takes an audio reference for lipsync/soundtrack matching, passed via the `audio` role:

```bash
higgsfield generate create seedance_2_0 \
  --prompt "person speaking" \
  --start-image ./headshot.png \
  --audio ./voice.mp3 \
  --duration 8 \
  --wait
```

**Do not pass a separate "generate audio" flag to Seedance 2.0** — its schema doesn't declare one. Use the audio media role instead.

### Schema mismatch errors

- "Model accepts only image (no roles)" — the model uses a legacy single-image-list shape, not role-tagged media. Drop role-prefixed flags and use the plain image flag.
- "Model does not accept media inputs" — the model is text-only (Z Image, Soul Location, Soul Cast, and some Wan configurations). Drop all media flags.
- "Unknown media role" — the role isn't valid for this model. Check the model's schema and its declared media roles.

---

## Prompt Engineering

### Basics

Higgsfield models reward concrete, sensory prompts.

- **Subject + setting + style**: "a red fox curled in a snowy pine forest, golden hour, cinematic"
- **Camera**: lens (35mm, 85mm), angle (low, overhead), motion (dolly in, tracking shot)
- **Lighting**: rim light, neon glow, moody backlight
- **Style/medium**: oil painting, watercolor, photograph, anime, 3D render

Keep it under ~200 tokens. Models distort with very long prompts.

### Image-to-image

When passing a reference image, the prompt should describe what changes, not redescribe the input.

- Bad: "a man with brown hair in a leather jacket holding coffee, made into anime"
- Good: "transform into anime style, vibrant colors, soft cel shading"

### Image-to-video

A start-frame image anchors the first frame. The prompt describes motion, not the static scene.

- Verbs: zooms in, dollies left, sweeping pan, slow push, fast whip
- Subject motion: "the dancer spins", "smoke rises slowly"
- Don't redescribe the static frame — the model already has it.

### Negative phrasing

Most models don't expose a negative-prompt field. Phrase everything positively:
- Instead of "no blur" → "tack sharp"
- Instead of "no people" → "uninhabited landscape"

### Aspect ratio guidance

- `16:9` — landscape, cinematic
- `9:16` — vertical, social
- `1:1` — square, profile/icon
- `4:3`, `3:4`, `21:9` — model-dependent, check the model's schema

### Safety

Models reject prompts flagged `nsfw` or `ip_detected`. Avoid:
- Real public figures
- Sexual content
- Trademarks / branded characters

---

## Troubleshooting

### Authentication
- "Session expired." → re-run the login flow.
- "Stored credentials are for ... but current environment ..." → re-run login for the current API URL.
- "Not authenticated." → run login first.

### Validation
- "Missing required params: prompt" — no prompt was given. Ask for one.
- "Invalid values: `<param>=<v>` (allowed: ...)" — pick from the allowed enum.
- "Unknown params: `<name>`" — schema doesn't accept this flag. Check the model's schema.

### Job lifecycle
- "Job ended with status 'failed'" — server-side failure, often prompt content/safety related. Try rephrasing.
- "nsfw" / "ip_detected" — content policy hit. Rephrase.
- "Timeout after 10m" — model is slow; bump the wait timeout to 30m or retry.

### Rate limits
- HTTP 429 — too many requests. Back off and retry later.

### CloudFlare / anti-bot
- A captcha-delivery response body means the server's anti-bot system fired. Wait 30s and retry. If persistent, this needs escalation to the platform provider.

### Cost
- A cost/estimate command returns a credit estimate without submitting the job — useful whenever asked "how much will this cost?"

---

## Marketing Studio

Branded image/video generation: avatars + products + optional setup hooks/settings + ad-style modes. This is the path for any advertising, commercial, or branded ad video/image.

### Concepts

- **Avatar** — the presenter's face. Either a curated preset (browsable) or a custom one built from uploaded photos. For UGC modes, an avatar is optional if the brief clearly mentions a person — the backend can synthesize a Soul Character automatically. Supply a specific avatar when a specific presenter is wanted.
- **Product** — the brand item, with a title and reference images. Either imported from a URL or created from uploaded images.
- **Webproduct** — the App Store/web-page version. Auto-routes when fetching App Store URLs.
- **Hook** — a reusable opening angle/ad hook. Hook text is prepended to the prompt; it does not replace the prompt.
- **Setting** — a reusable environment/scene context.

### Discovery

List existing avatars, products, hooks, and settings before assuming none exist.

`--hook_id` and `--setting_id` apply to the video model only — never pass them to the image model.

### Workflow — quick ad video

1. **Get the product.**
   - Existing product → list products and pick by name.
   - URL → fetch the product from the URL and wait for the import to finish.
   - Local images → upload each image, then create the product with a title and the uploaded image IDs.
   Capture the product ID. When using a hook, strongly prefer also passing product context — hooks are designed to pivot into a product and work poorly without it.
2. **Pick an avatar if needed.**
   - Default: list avatar presets and pick one matching the brand voice.
   - Custom: create one from an uploaded photo.
   - For UGC modes, the avatar can be omitted when no specific presenter is required and the brief mentions a person — the backend can synthesize one.
3. **Optionally pick setup items** (hook and/or setting) from the discovery lists. Pass the selected IDs to the video model only. Don't copy a hook's own prompt text into the main prompt unless the wording should be explicitly reinforced.
4. **Pick a mode if needed.** Default is `ugc`; a mode is not required just because a hook is present. Other current slugs: `ugc_how_to`, `ugc_unboxing`, `product_showcase`, `product_review`, `tv_spot`, `wild_card`, `ugc_virtual_try_on`, `virtual_try_on`. See Marketing Modes below.
5. **Generate in one shot**, e.g.:
   ```bash
   PRODUCT_IDS_JSON=$(mktemp)
   AVATARS_JSON=$(mktemp)
   printf '["<product_id>"]' > "$PRODUCT_IDS_JSON"
   printf '[{"id":"<avatar_id>","type":"preset"}]' > "$AVATARS_JSON"

   higgsfield generate create marketing_studio_video \
     --prompt "..." \
     --avatars @"$AVATARS_JSON" \
     --product_ids @"$PRODUCT_IDS_JSON" \
     --mode ugc \
     --duration 15 \
     --resolution 720p \
     --aspect_ratio 9:16 \
     --wait
   ```
   Add `--hook_id <hook_id>` and/or `--setting_id <setting_id>` when a setup hook/setting was selected. `product_ids` and `avatars` are JSON arrays passed via a file reference (`@/path/to/file.json`) — never pass a bare ID directly for these two fields. Resolution is `480p` or `720p`. Aspect ratio is one of `auto`/`21:9`/`16:9`/`4:3`/`1:1`/`3:4`/`9:16`. Audio generation is supported for Marketing Studio video (unlike Seedance 2.0's separate audio-flag restriction). `--wait` blocks until done; increase the timeout for longer ad runs.
6. **Deliver.** Return the URL plus a one-line summary (mode, duration).

### Click-to-Ad shortcut (URL-driven)

When given a product URL and asked for a marketing video in one go:

```bash
# 1. Trigger fetch (returns the product id and starts a background scrape)
higgsfield marketing-studio products fetch --url https://shop.example.com/sneakers --wait

# 2. Generate the marketing video against the same URL — backend reuses the entity
higgsfield generate create marketing_studio_video \
  --url https://shop.example.com/sneakers \
  --mode ugc \
  --duration 15 \
  --aspect_ratio 9:16 \
  --wait
```

Repeated fetches for the same URL dedupe — the backend reuses the existing entity instead of re-scraping.

### Workflow — marketing image

Same idea, using the marketing image model:

```bash
higgsfield generate create marketing_studio_image \
  --prompt "..." \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait
```

---

## Marketing Avatars

### Preset vs custom

| | Preset | Custom |
|---|---|---|
| Source | Curated by Higgsfield | User-uploaded |
| Cost | None for selection | Cost of upload |
| Diversity | Limited but professional | Unlimited |
| Use when | Generic ad, fast turnaround | Brand-specific face, founder, employee |

### Listing presets

```bash
higgsfield marketing-studio avatars list
higgsfield marketing-studio avatars list --json | jq '.[] | select(.gender=="female")'
```

Filter by `name`, `gender`, etc. on the JSON output.

### Creating a custom avatar

```bash
ID=$(higgsfield upload create founder.png)
URL=$(higgsfield upload create founder.png --json | jq -r .url)   # cloudfront URL if needed
higgsfield marketing-studio avatars create --name "Founder" --image $ID --image-url $URL
```

`--image-url` is the cloudfront URL from the upload — required by the API.

### Passing to video

```bash
AVATARS_JSON=$(mktemp)
printf '[{"id":"<avatar_id>","type":"preset"}]' > "$AVATARS_JSON"

higgsfield generate create marketing_studio_video \
  --avatars @"$AVATARS_JSON" \
  ... \
  --wait
```

`type` is `preset` for curated avatars, `custom` for user-created ones. The avatars flag expects a JSON array, passed via a file reference.

For UGC modes, an avatar is optional if the brief clearly mentions a person and no specific presenter was requested — the backend can synthesize a Soul Character automatically.

---

## Marketing Modes

Current mode values for the marketing video model. The live schema is the source of truth if validation ever fails — re-check it.

| Mode slug | Human-readable label | Best for |
|---|---|---|
| `ugc` | UGC | Default. Casual, organic-feel content from a presenter. |
| `ugc_how_to` | Tutorial | "Here's how to use this." Tutorial/explainer. |
| `ugc_unboxing` | Unboxing | "Just got this in the mail." Unboxing reveal. |
| `product_showcase` | Product Showcase | Clean product highlight, polished. |
| `product_review` | Product Review | Presenter giving an opinion on the product. |
| `tv_spot` | TV Spot | Broadcast-style commercial. Higher production. |
| `wild_card` | Wild Card | Experimental, model picks the vibe. |
| `ugc_virtual_try_on` | UGC Virtual Try On | Person trying on clothing/accessories — UGC vibe. |
| `virtual_try_on` | Pro Virtual Try On | Same, but more polished, model-driven. |

**Default when unspecified:** `ugc`.

### Picking flow

- "Looks like a real person filmed on phone" → `ugc` family (`ugc`, `ugc_unboxing`, `ugc_virtual_try_on`, `ugc_how_to`)
- "Polished broadcast commercial" → `tv_spot`
- "Show the product itself, less presenter" → `product_showcase`
- "Presenter giving an opinion" → `product_review`
- "Try clothing on someone" → `virtual_try_on` (polished) or `ugc_virtual_try_on` (organic feel)
- "Surprise me / something different" → `wild_card`

### Other parameters (marketing video model)

- `aspect_ratio`: `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` (default `16:9`).
- `duration`: integer ≥ 4 seconds. No fixed cap noted; check the model schema for the current upper bound.
- `resolution`: `480p` or `720p` (default `720p`).
- `generate_audio`: boolean (default `false`).
- `avatars`: array of `{id, type}` where `type` is `preset` or `custom`.
- `product_ids`: array of product UUIDs.
- `hook_id`: optional Marketing Studio setup hook UUID.
- `setting_id`: optional Marketing Studio setup setting UUID.
- `medias`: optional reference images with role `image`, `start_image`, or `end_image`.
- `feature: "click_to_ad"`: when generating from a single landing-page URL (Click-to-Ad flow).
- `product: { id?, url? }`: alternative single-product reference; the URL flow auto-fetches.

### URL-driven Click-to-Ad shortcut

1. Fetch/create the product from the URL and wait for completion.
2. Generate the marketing video against the same URL — the backend looks up/reuses the entity and submits.

Repeated fetches for the same URL dedupe — the backend reuses any existing non-failed entity.

---

## Marketing Products

Two ways to register a product: URL fetch (auto-imports title, description, images) or manual (supply your own).

### URL fetch (default)

```bash
ID=$(higgsfield marketing-studio products fetch --url https://shop.example.com/sneakers --wait --json | jq -r .id)
```

Waiting polls until status is `completed` or `failed` (default timeout 90s). If `failed`, check the failure reason — usually an invalid URL or a blocked scrape.

App Store URLs auto-route to the "webproducts" endpoint instead:

```bash
higgsfield marketing-studio webproducts fetch --url https://apps.apple.com/... --wait
```

### Manual

When product photos and details are available directly:

```bash
A=$(higgsfield upload create shoe1.png)
B=$(higgsfield upload create shoe2.png)
higgsfield marketing-studio products create \
  --title "AeroRun Pro" \
  --description "Lightweight running shoe" \
  --image $A --image $B
```

Returns the product entity directly — no polling needed.

### Manual webproduct

For App Store/web pages without URL fetch:

```bash
higgsfield marketing-studio webproducts create \
  --url "https://example.com" \
  --title "MyApp" \
  --subtitle "Productivity for teams" \
  --description "..." \
  --favicon-url "https://example.com/favicon.png" \
  --desktop "https://cdn/screenshot1.png" \
  --mobile "https://cdn/mobile-screenshot.png"
```

### Listing

```bash
higgsfield marketing-studio products list
higgsfield marketing-studio products list --json
higgsfield marketing-studio webproducts list
```

---

## Setup Items (Hooks & Settings)

Marketing Studio setup items are optional reusable context for the marketing video model.

- **Hook** sets the opening angle/ad hook. The hook prompt is prepended to the main prompt; it does not replace it.
- **Setting** sets the scene/environment context.
- Supported by the marketing video model only — never pass setup items to the marketing image model.

### Discover items

```bash
higgsfield marketing-studio hooks list
higgsfield marketing-studio settings list
```

Add `--json` for IDs, and `--search <term>` to filter large lists.

Response shape: `items` (each with `id`, `name`, `prompt`, `source`, optional `type`, optional media URLs, pin/status metadata), `cursor` (for the next page), `has_more`.

### Generate with setup items

Pass one or both IDs alongside product context:

```bash
PRODUCT_IDS_JSON=$(mktemp)
printf '["<product_id>"]' > "$PRODUCT_IDS_JSON"

higgsfield generate create marketing_studio_video \
  --prompt "..." \
  --mode ugc \
  --product_ids @"$PRODUCT_IDS_JSON" \
  --hook_id <hook_id> \
  --setting_id <setting_id> \
  --duration 15 \
  --aspect_ratio 9:16 \
  --wait
```

When using a hook, pass product context whenever possible — hooks are designed to transition into a product pitch and are weak without it.

Mode is optional and defaults to `ugc`; set it explicitly only for a specific non-default style.

For UGC modes, avatars are optional if the brief clearly mentions a person — the backend can synthesize a Soul Character. Supply avatars when a specific presenter was selected.

If the request is rejected for an unknown `hook_id` or `setting_id` parameter, don't retry with that flag for the selected model — its schema doesn't support setup items.

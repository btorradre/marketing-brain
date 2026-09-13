---
name: claymation
description: End-to-end claymation-style direct response video ad pipeline. Takes a script + brief + brand, breaks it into a villain/hero arc OR accepts structured scene beats, generates clay-textured stills via Nano Banana 2 image-to-image with product references, animates each still via Kling 3.0 with slow stop-motion prompts + organic handheld cues, generates voiceover via ElevenLabs, stitches clips with whisper-aligned shot cut points, and (optionally) post-processes through HyperFrames to add word-synced captions + audio-reactive overlays, outputting a ready-to-upload 9:16 MP4. Use when the user wants to build a claymation ad, replicate an Andrei Lunev claymation style, or says "make a claymation ad", "build the claymation ad", "run the claymation pipeline".
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Claymation

Production pipeline for claymation-style direct response video ads. One command, script + brief → finished 9:16 MP4 with VO and word-synced captions.

## The Format

Two supported arc modes:

**A. 9-shot villain/hero arc** (~42s, Andrei Lunev / HeyOz format):

| Shot | Purpose |
|------|---------|
| 1 | Problem (relatable complaint) |
| 2 | Tease (magical transformation hint) |
| 3 | Villain reveal (clay monster, cold lighting, center frame) |
| 4 | Conflict (villain tormenting avatar) |
| 5 | Failed fixes (3 ineffective solutions) |
| 6 | Internal repair (tiny clay crew fixing body mechanism) |
| 7 | Hero reveal (MIRROR of shot 3 — same composition, warm/lush) |
| 8 | Victory (hero defeats villain) |
| 9 | Resolution (product + guarantee) |

**B. Structured scene beats** (any N shots, user-defined):
When the brief includes explicit scene beats with timestamps (e.g. "SCENE BEATS" section with `00:00 – 00:04 | HOOK` entries), the strategist uses those exactly. One shot per beat. Validated live on the Motilli "Wrong Floor" concept (7-beat mechanism-install ad).

9:16 vertical. Visible clay texture (fingerprints, tool marks, hand-sculpted imperfections). Shots 3 and 7 (mode A) are the highest-impact frames and often become the Meta thumbnail.

## Pipeline Overview

```
INPUT: script + brief + brand
    ↓
[Stage 1] Strategist (Claude Opus 4.7, fallback Gemini 2.5 Flash)
          detects mode A or B from brief, outputs shot_plan.json
    ↓
[Stage 2] Nano Banana 2 i2i (gemini-3.1-flash-image-preview)
          N clay stills. `pure_i2i: true` on product shots bypasses style blocks
          for 1:1 material transformation of the canonical product reference.
          REFERENCES ARE ATTACHED VIA types.Part.from_bytes (NOT from_image —
          that method does not exist in current google-genai SDK).
    ↓
[APPROVAL GATE 1] — review stills before Kling credits
    ↓
[Stage 3] Kling 3.0 via kie.ai (image-to-video)
          Every prompt includes the 4 organic-cue sentences:
            - subtle inconsistent handheld micro jitter
            - slight rolling shutter wobble during motion
            - eyes briefly lose focus, then re-lock onto camera
            - background movement continues even when subject is still
          5s per clip, 9:16, pro mode, sound: False (VO is separate).
    ↓
[Stage 4] ElevenLabs TTS
          Full VO from concatenated shot VO lines.
          Conservative settings: stability 0.55, style 0.2.
    ↓
[Stage 5] FFmpeg stitch
          Each Kling clip stretched via setpts to match its VO duration.
          Clips concatenated, VO mixed in, optional PIL-rendered caption PNG overlays.
    ↓
[OPTIONAL Stage 6] HyperFrames polish (recommended for final delivery)
          Whisper transcribes the VO for word-level timestamps.
          Captions rebuilt from whisper (not segments.json) for true audio sync.
          Video re-stitched with whisper-derived shot cut points.
          HyperFrames composition adds word-synced caption overlays + audio-reactive
          pulse on product/hero moments. Re-render → final_polished.mp4.
    ↓
OUTPUT: b-roll/{brand}/{CONCEPT_CODE}/final.mp4 (+ final_polished.mp4 if HyperFrames'd)
```

## When to Use

- User wants a claymation ad built end-to-end from a script + brief
- User says "run the claymation pipeline", "make this a claymation ad", "build the claymation ad for X"
- Brand is registered (Motilli, Lunessa, Velantra-*) — auto-loads research + product refs

Do NOT use for:
- Live-action video replication → `video-scene-replicator`
- 3D animated Veo-powered format → `animated-video-replicator`
- Kling-audio-native animated format → `animated-video`
- Talking head / UGC → `aiugc-replicator` or `fabric-talking-head`

## Required Inputs

1. **Script** — path to a `.md` file, or raw text. If only a brief is given, strategist writes the script.
2. **Brief** — free text. If the brief contains explicit scene beats (timestamps + VO + visual), mode B kicks in.
3. **Brand** — `Motilli`, `Lunessa`, `Velantra-Boat-Tote`, etc. Auto-loads research + canonical product reference images.
4. **Concept code** — `ANGLE-CLAY-##` (e.g. `WF-CLAY-01` for "Wrong Floor" v1).

## Optional Flags

- `--voice` — ElevenLabs voice name (default `rachel`)
- `--no-gates` — skip approval gates (autonomous batch)
- `--no-captions` — skip pipeline-burned captions (use when post-processing through HyperFrames)
- `--images-only` — stop after Stage 2

## Concept Code Convention

**`ANGLE-CLAY-##`** — 2-3 letter angle + `CLAY` + sequential version.

Examples: `HL-CLAY-01` (Hair Loss v1), `GG-CLAY-02` (Gut Gridlock v2), `WF-CLAY-01` (Wrong Floor v1).

## Output Directory Layout

```
~/Documents/marketing brain/b-roll/{brand_lowercase}/{CONCEPT_CODE}/
├── script/
│   ├── brief.md                    # Raw brief + script as provided
│   └── shot_plan.json              # N-shot breakdown with VO + prompts
├── images/
│   ├── shot_01.png … shot_NN.png   # Nano Banana 2 clay stills
│   └── shot_NNa.png / shot_NNb.png # Sub-shots when a shot is split
├── clips/
│   ├── shot_01.mp4 … shot_NN.mp4   # Kling 3.0 animated clips
│   └── shot_NNa.mp4 / shot_NNb.mp4 # Sub-shot clips
├── audio/
│   ├── voiceover.mp3               # ElevenLabs VO
│   └── segments.json               # Estimated per-shot timing
├── final/
│   ├── final.mp4                   # Pipeline-stitched deliverable
│   ├── final_polished.mp4          # HyperFrames post-processed (captions + FX)
│   ├── captions.srt                # Editable subtitles
│   └── assembly_guide.md           # Shot list + timing
├── hyperframes/my-video/           # (optional) HyperFrames project
│   ├── index.html                  # composition source
│   ├── DESIGN.md                   # visual identity
│   ├── transcript.json             # whisper word-level timings
│   └── caption_groups.json         # derived caption cards
└── .progress.json
```

## Critical SDK Notes (DO NOT SKIP)

### Image attachment via google-genai
```python
# ✓ CORRECT — from_bytes works
with Image.open(ref_path) as im:
    im = im.convert("RGB")
    buf = io.BytesIO()
    im.save(buf, format="PNG")
parts.append(types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png"))

# ✗ WRONG — types.Part.from_image does NOT exist in current google-genai SDK
# This fails silently and Nano Banana generates text-only, ignoring the reference.
parts.append(types.Part.from_image(Image.open(ref_path)))
```

**This was the single most important bug fixed in this skill.** Without `from_bytes`, every "product reference" instruction is silently dropped and the model hallucinates a random product.

### WebP references
PIL + google-genai handles WebP poorly. Convert product refs to PNG once (`Image.open(webp).save(png, 'PNG')`), store at the PNG path, point registry at the PNG. Example: `hero-01.webp` → `hero-01.png` (already done for Motilli).

## Product Shots — Always Pure Image-to-Image

**Rule**: Every product-focused shot (end card, hero product shot, close-up where the product IS the subject) sets `pure_i2i: true` in the shot plan.

**What `pure_i2i` does**:
- Bypasses CLAY_STYLE_BLOCK + avatar description + art direction
- Sends a minimal "Edit this image" directive alongside the product reference
- Nano Banana does a faithful 1:1 material transformation (plastic → clay)
- Jar geometry, label text, proportions stay IDENTICAL to the reference

```json
{
  "shot_number": 7,
  "purpose": "END CARD",
  "pure_i2i": true,
  "image_prompt": "short additional direction only",
  "extra_refs": ["/path/to/canonical/product/reference.png"],
  "extra_products_description": "1:1 clay transformation of reference product photo."
}
```

**Aspect protection for product shots**: include explicit geometric language — e.g. "jar is a SQUARE CUBOID, NOT cylindrical. Add cream negative space above/below to fill the 9:16 canvas. Do NOT stretch the jar vertically."

**Transparency**: For transparent/clear plastic jars, state explicitly: "jar body is CLEAR TRANSPARENT PLASTIC — you can see THROUGH to the gummies INSIDE. Do NOT render jar as opaque white or solid."

**When NOT to use pure i2i**: product is background element, or product is integrated into a larger scene. Use `has_product: true` + `extra_refs` (without `pure_i2i`) so the clay style block still applies.

## Sub-Shot Splits

When a single shot needs to cut between two different visuals (e.g. woman relief → product end card), generate sub-shots:

1. Create `shot_07a.png` + `shot_07b.png` (woman + product)
2. Kling-animate each → `shot_07a.mp4` + `shot_07b.mp4`
3. Re-stitch as 8 segments with whisper boundaries (shot 7 slot splits into 7a + 7b timings)

Reference: the `/tmp/gen_split_shot7.py` pattern used in the WF-CLAY-01 concept dir.

## Clay Style Block

Every non-i2i image prompt prepends this:

```
CLAYMATION STYLE (MANDATORY, enforce in every pixel):
- Stop-motion clay aesthetic, hand-sculpted figures (plasticine/Play-Doh)
- Visible fingerprints, thumb indents, tool marks, seams, subtle asymmetry
- Matte clay texture — NO shine, NO plastic, NO CGI polish, NO 3D-render smoothness
- Shallow depth of field, soft directional key light (slightly warm)
- Tactile surfaces — viewer can see the clay was pressed, rolled, poked
- 9:16 vertical composition, macro framing on character-focused shots
- Frame slightly off-kilter (hand-held stop-motion rig feel)
```

## Kling Motion Rules

Every Kling prompt includes the 4 organic cues (see Pipeline Overview). For clay specifically:
- Slow, deliberate — claymation illusion breaks at high speed
- Stop-motion pop cadence, jittery micro-motion (NOT smooth CGI interpolation)
- Preserve clay texture and hand-made imperfections in every frame
- 5s per clip default

Product end cards: "Hold locked-off product shot. No zoom, no push-in. Tiny handheld breath only."

## Whisper-Aligned Sync (Stage 6)

The pipeline's Stage 5 stretches clips based on VO word-count estimates — real TTS pacing drifts from the estimate. For tight sync:

1. `npx hyperframes transcribe audio/voiceover.mp3 -m small.en` → `transcript.json`
2. Find each shot's first-word timestamp in the transcript (use unique 3-word phrases — e.g. match "Your GLP-1 slows", not just "Your", to avoid matching other occurrences)
3. Build shot boundaries from those word timestamps
4. Re-stitch: for each Kling clip, setpts factor = `target_boundary_duration / source_clip_duration`
5. Concat stretched clips + mix VO

Reference implementation: see the whisper re-stitch inline script in the WF-CLAY-01 concept dir.

## HyperFrames Polish (Stage 6)

For word-synced captions + audio-reactive overlays:

```bash
cd ~/Documents/"marketing brain"/b-roll/{brand}/{CONCEPT}/hyperframes/my-video
npx hyperframes lint
npx hyperframes render -o ../../final/final_polished.mp4 -q high
```

Project structure:
- `index.html` — GSAP timeline with caption GROUPS parsed from whisper transcript
- `DESIGN.md` — visual identity (fonts, colors, motion rules)
- `video.mp4` / `vo.mp3` — symlinks to `../../final/final.mp4` and `../../audio/voiceover.mp3`

Caption style for warm storytelling DR tone: Inter 600, 66px, white fill, 3-layer drop shadow (warm black), bottom third, fade + 12px slide-up entrance, fade + 6px slide-up exit. Brand-weight bump (Inter 700) on product-name caption cards.

## Approval Gates

- **Gate 1** (after images): review N PNGs before spending Kling credits
- **Gate 2** (after stitch): review `final.mp4`

Skip with `--no-gates` for batch runs.

## Costs per finished ad

- Nano Banana 2: ~$0.08 per shot (~$0.70 for 9 shots)
- Kling 3.0: ~$0.50 per shot (~$4.50 for 9 shots)
- ElevenLabs TTS: ~$0.20 for 42s
- HyperFrames render: free (local)
- **Total: ~$5.40, ~8–15 min wall clock**

## Dependencies

- `ffmpeg` + `ffprobe` on PATH
- API keys in `~/Documents/marketing brain/.env`: `GEMINI_API_KEY`, `KIE_API_KEY`, `ELEVENLABS_API_KEY`, `ANTHROPIC_API_KEY`
- `pip install`: `google-genai`, `pillow`, `requests`, `anthropic`
- `npx hyperframes` for Stage 6 polish

## Execution

```bash
# Full pipeline
python3 ~/.claude/skills/claymation/pipeline.py \
    --brand Motilli --concept WF-CLAY-01 \
    --script "brands/motilli/scripts/wrong_floor_brief.md" \
    --brief "short concept hint (villain/hero or theme)" \
    --voice rachel --no-captions --no-gates

# Images only (stop after Stage 2)
python3 ~/.claude/skills/claymation/pipeline.py ... --images-only
```

Kling in this skill uses `sound=False` with a separate ElevenLabs VO. For Kling-generated audio instead (no ElevenLabs), use the `animated-video` skill.

## Known Brand Canonical Product References

| Brand | Canonical ref path |
|-------|-------------------|
| Motilli | `brands/motilli/motilli pdp/images/hero-01.png` — square jar, white cap, HEART-shaped dark-green gummies |
| Lunessa | `brands/lunessa/fh research docs/Lunessa Research Docs 3.0/lunessa spelling corrected.jpg` |
| Velantra-* | `statics/product references/velantra/{boat tote\|meridian\|weekender}/*.{jpg,webp}` |

## Validated Concept: "The Wrong Floor" (Motilli, WF-CLAY-01)

7-beat mechanism-install ad (GLP-1 constipation). Living reference implementation at:
`~/Documents/marketing brain/b-roll/motilli/WF-CLAY-01/`

- 7 shots, whisper-aligned, HyperFrames-polished
- Shot 7 split into 7a (woman relief) + 7b (transparent product jar)
- 25 word-synced caption groups
- Green-glow pulse overlay on the Motilli-mention beat (33.28s – 46.28s)
- Caption split: "Keep the medication." → "Skip the side effects." → "Motilli.com." across three caption cards

Study this concept before building new claymation ads.

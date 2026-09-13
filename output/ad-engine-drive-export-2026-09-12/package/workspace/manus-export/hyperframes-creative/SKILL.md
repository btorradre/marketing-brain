---
name: hyperframes-creative
description: Provides non-animation creative direction for HyperFrames video compositions — design-spec handling (frame.md / design.md), palette selection, typography, narration and story structure, beat/rhythm planning, audio-reactive visuals, composition patterns, and brand/style decisions such as picking or adapting a named frame-preset. Use this whenever a HyperFrames video needs visual/creative direction beyond raw technical assembly — choosing colors, fonts, mood, composition, pacing, or a design system for a video, verifying a built composition against its design spec, or writing narration/beat plans for a multi-scene video. Not for atomic motion patterns, transitions, or scene-blueprint choreography (that is a separate animation-focused part of the pipeline) and not for the underlying technical contract of a HyperFrames project (a separate core/technical layer handles that).
---

# HyperFrames Creative

This skill is the brand, pacing, style, narration, and composition layer for HyperFrames video
projects. It assumes the technical contract for the project (composition structure, timing
primitives, render pipeline) is already in place — that is owned by a separate technical/core
layer of the pipeline, not by this skill. This skill is intentionally **non-animation**: atomic
motion patterns, scene blueprints, transitions, and CSS marker effects belong to a separate
animation-focused part of the pipeline. When a task is purely about motion choreography or
transitions, treat that as out of scope here and hand it off; this skill covers the *decision* of
how much motion energy a scene should carry (see Motion below), not the frame-by-frame mechanics.

> **Read these two references first for any non-trivial composition — they override web
> instincts and are the single biggest lever against generic output:**
>
> - `references/design-system.md` (house-style section) — "interpret the prompt, generate real
>   content," the lazy-default list, and the background/foreground layer recipe. This is what
>   turns a literal restyle into a *concept*.
> - `references/composition-rules.md` (video-composition section) — video-medium scale, depth,
>   and foreground detail. It explains how to avoid empty web-page layouts without imposing a
>   universal element count.
>
> Skipping these is the single biggest cause of generic, web-page-looking output. For anything
> beyond a one-line edit, read both before choosing colors or writing HTML.

## What this skill does

Given a request to build, restyle, or direct a HyperFrames video, this skill supplies:

1. **Design-system resolution** — finding and reading a project's existing design spec
   (`frame.md` / `design.md` / `DESIGN.md`), or building one from scratch via a named style, a
   frame-preset, house-style defaults, or an interactive picker.
2. **Palette selection** — nine ready-made category palettes with exact hex tokens, or guidance
   for deriving a palette from OKLCH.
3. **Typography rules** — which fonts render safely, banned "AI tell" fonts, pairing rules, and
   video-specific sizing.
4. **Composition and video-medium rules** — how to make a frame read as a produced video frame
   rather than a scaled-up web page: density, color presence, scale, frame composition.
5. **Narration and story structure** — pacing, tone, number pronunciation, the value-first story
   spine that governs narrated workflows.
6. **Beat/rhythm planning** — per-scene direction (concept, mood, choreography verbs, transition
   type, depth layers, SFX) and how to plan the rhythm of a multi-scene piece.
7. **Data and audio-reactive guidance** — how to present stats/infographics on video, and how to
   drive visuals from pre-extracted audio data.
8. **Prompt expansion** — the mandatory enrichment step that turns a user's seed prompt into a
   full per-scene production spec before any HTML gets written.
9. **Design adherence** — a post-authoring checklist that verifies a built composition actually
   followed its design spec (or, absent a spec, followed house style).

## The creative decision workflow

### Step 1 — Resolve or establish the design system

If the project already has a design spec, **read it first** and treat its frontmatter tokens
(colors, fonts, spacing, tone, constraints) as brand truth. Precedence for which file to read is
`frame.md` → `design.md` → `DESIGN.md` — read the first that exists, ignore the rest. A spec is
YAML frontmatter (the normative layer — quote hex/font values verbatim, never invent or round
them) plus a markdown body (context and judgment, not values). Full resolution and parsing rules,
including how to seed a spec from a frame-preset, live in `references/design-system.md`.

If no design spec exists and the request calls for visual direction, choose a route:

- **A ready-made frame-preset** (optional) — thirteen fully-specified visual identities in
  `references/frame-presets-1.md` and `references/frame-presets-2.md`, each with exact colors,
  type ramps, component specs, and per-frame-type composition recipes. Adopt one as the project's
  spec when its look fits the brief.
- **A named style or mood** — eight cultural/design-movement-grounded starters (Swiss Pulse,
  Velvet Standard, Deconstructed, Maximalist Type, Data Drift, Soft Signal, Folk Frequency, Shadow
  Cut) in `references/prompt-expansion.md`, matched to mood first, content second.
- **Fast defaults** — no named style, just house-style rules for color, typography, motion, and
  background layering. See `references/design-system.md`.
- **Interactive selection** — build a two-phase visual picker (mood boards, then fine-tuning) for
  a human to choose from. See `references/design-system.md`.

### Step 2 — Pick a palette

Declare one background, one foreground, and one accent color before writing any HTML. Match
light/dark to content (food, wellness, kids → light; tech, cinema, finance → dark), tint neutrals
toward the accent hue, and never invent colors per-element. Nine category palettes with exact hex
values — Bold/Energetic, Warm/Editorial, Dark/Premium, Clean/Corporate, Nature/Earth,
Neon/Electric, Pastel/Soft, Jewel/Rich, Monochrome — are in `references/palettes.md`. Alternatively
derive a palette from OKLCH: pick a hue, build background/foreground/accent at different
lightnesses, tint everything toward that hue.

### Step 3 — Typography

Pick typefaces deliberately, not by category reflex. Eighteen font families render deterministically
with zero setup; a fixed list of "AI tell" fonts (Inter, Playfair Display, Poppins, Syne, etc.) is
banned as a training-data default. Full rules — safe families, pairing guardrails (never two
sans-serifs, weight contrast must be extreme), video sizing, dark-background compensation, and a
font-discovery script — are in `references/typography-and-motion.md`.

### Step 4 — Prompt expansion (mandatory for anything beyond a trivial edit)

Run the expansion step before writing HTML for any non-trivial or multi-scene composition. This
step is never pass-through — even a detailed user brief lacks the atmosphere layers, secondary
motion, micro-details, transition choreography, and exact hex/typography values that make a scene
feel alive rather than merely compliant. The expansion consumes the design spec plus
`references/design-system.md` and `references/narration-and-story.md` (beat-direction) and
`references/composition-rules.md` (video-composition), and produces a full per-scene production
spec written to a working file (not dumped into chat) for review before construction proceeds. See
`references/prompt-expansion.md` for the full procedure and output format.

### Step 5 — Plan beats and rhythm (multi-scene work)

For anything with more than one scene, plan beats and rhythm before writing HTML. Each beat is a
world, not a layout — concept, mood direction, animation choreography verbs, transition type,
depth layers, and SFX cues, all described experientially first and reduced to CSS/motion values
second. Name the scene rhythm (e.g. `hook-PUNCH-breathe-CTA`) before implementing. See
`references/narration-and-story.md` for beat-direction and story-spine doctrine, and — for the
mechanics of scene transitions themselves (CSS patterns, shader transitions, timing) — hand off
to the animation-focused part of the pipeline, which owns that catalog.

### Step 6 — Narration (if the composition has voiceover/TTS)

2.5 words per second is natural pace; write numbers as they should be spoken (TTS reads literally);
structure around hook / story / proof / CTA as the content warrants. See
`references/narration-and-story.md`.

### Step 7 — Composition and video-medium rules

Video frames are not web pages. Apply video-appropriate density, color presence (accent must be
visible, not a 5% ghost), scale (headlines 64–120px not 32–48px), motion intensity, and frame
composition (two focal points minimum, fill the frame, anchor to edges, split frames). Named
composition patterns — picture-in-picture, text-behind-subject, title cards, slideshows — are in
`references/composition-rules.md`.

### Step 8 — Motion (high-level only)

This skill covers only the high-level guardrails: vary eases and speeds, respect the
build/breathe/resolve scene structure, treat easing as emotion not technique, and the load-bearing
GSAP rules that prevent compositions from lint-clean-but-broken renders (overlapping transform
tweens, `immediateRender` traps, ambient pulses that must attach to the seekable timeline). See
`references/typography-and-motion.md`. For atomic motion patterns, scene blueprints, named text
effects, and the full transition catalog (CSS and shader), hand off to the animation-focused part
of the pipeline — that catalog is out of scope here.

### Step 9 — Data and audio-reactive elements (as needed)

For stats/infographics on video: keep successive related stats visually continuous, always pair a
number with a visual-weight element, and avoid web chart patterns (pie charts, multi-axis charts,
dashboards, gridlines). For audio-reactive compositions: pre-extract audio band data (the
`scripts/extract-audio-data.py` script in this skill does this), map audio signals to visual
properties by content logic (not generic equalizer/spectrum clichés), and sample every frame via a
timeline-attached loop, never a single tween. See `references/data-and-audio.md`.

### Step 10 — Design adherence (after authoring, before serving)

Run a post-authoring verification pass. If a design spec exists: check every color, font,
corner-radius, spacing, and depth value against the spec, and confirm none of the spec's declared
avoidance rules appear. If no spec exists: check palette consistency across scenes and confirm none
of the house-style lazy defaults crept in undeliberately. Report violations as a checklist and fix
each before serving. See `references/design-system.md`.

## Reference map

| Topic | File |
| --- | --- |
| Design-spec resolution/parsing, house-style defaults, interactive picker, post-build adherence checks | `references/design-system.md` |
| Category palettes with exact hex tokens | `references/palettes.md` |
| Frame-presets 1 of 2 — cartesian, creative-mode, coral, biennale-yellow, daisy-days, cobalt-grid, capsule | `references/frame-presets-1.md` |
| Frame-presets 2 of 2 — claude, editorial-forest, blockframe, blue-professional, broadside, bold-poster | `references/frame-presets-2.md` |
| Named composition patterns (PiP, text-behind-subject, title card, slideshow) + video-medium density/scale/color/frame rules | `references/composition-rules.md` |
| Font rules, pairing guardrails, video sizing + high-level motion guardrails and load-bearing GSAP rules | `references/typography-and-motion.md` |
| Narration pacing/tone/number-pronunciation, value-first story-spine doctrine, per-beat direction and rhythm planning | `references/narration-and-story.md` |
| Stats/infographic presentation rules + audio-reactive animation mapping | `references/data-and-audio.md` |
| Mandatory prompt-expansion procedure + eight named visual-style starters (mood-to-style routing) | `references/prompt-expansion.md` |

## Scripts

- `scripts/extract-audio-data.py` — decodes an audio or video file via ffmpeg and outputs
  per-frame RMS amplitude and logarithmically-spaced frequency-band data as JSON, ready to embed
  in an audio-reactive composition. Requires Python 3.9+, `ffmpeg` on PATH, and `numpy`. Standalone
  — no project-specific dependencies. Usage:

  ```bash
  python extract-audio-data.py input.mp3 -o audio-data.json
  python extract-audio-data.py input.mp4 --fps 30 --bands 16 -o audio-data.json
  ```

  A companion contrast-checking script exists in the source project but depends on that project's
  internal rendering-engine packages and bootstrap tooling, so it isn't portable outside that
  environment and isn't included here. If contrast auditing is needed, verify color contrast
  manually against WCAG AA (4.5:1 for normal text, 3:1 for large text ≥24px or ≥19px bold) using
  the declared foreground/background token pairs from the design spec.

## Boundaries

- Do not override the project's technical contract (composition structure, timing primitives) —
  that belongs to a separate technical/core layer.
- Do not require a full design system for a minimal, intentionally sparse technical composition.
- Do not add extra scenes, narration, music, captions, or transitions unless the request calls for
  them, or propose the expansion first and get it confirmed.
- Keep reference lookups task-specific — don't read every reference file for a simple edit.
- Do not fabricate figures, dates, or claims when adapting a frame-preset or writing data-driven
  scenes — every numeral must trace to the script/brief or render as a placeholder.

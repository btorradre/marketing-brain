---
name: website-to-hyperframes
description: Capture a website and turn it into a professional short video — a product launch video, a social ad, a feature announcement, a brand reel, or a launch teaser — using HyperFrames, an HTML-based video-rendering framework ("HTML in, video out"). Use whenever someone gives a URL and wants a video made from it, or asks to "capture this site," "turn this into a video," "make a promo from my site," or similar.
---

# Website to Video (HyperFrames)

This document describes a 7-step process for turning an existing website into a professional short video using HyperFrames, an open-source, HTML-based video-rendering framework. It works by treating HTML `<div>` elements as keyframes, HTML data attributes as a timeline, CSS as visual styling, and the GSAP animation library as the animation engine — anything a web browser can render (CSS animations, GSAP, Lottie animations, WebGL shaders, Three.js, embedded video) can become a frame in the final rendered video. The renderer captures every frame deterministically and produces an MP4.

Each of the 7 steps produces a concrete artifact (a file) that gates moving on to the next step — don't skip a step or its artifact.

Users say things like:
- "Capture https://... and make me a 25-second product launch video"
- "Turn this website into a 15-second social ad for Instagram"
- "Create a 30-second product tour from https://..."

## How to use this — the 7-step workflow

### Step 1: Capture the site and understand it

Run the capture command, pointed at the URL and an output folder:

```bash
npx hyperframes capture <URL> -o <project-dir>/capture
```

Example: `npx hyperframes capture https://stripe.com -o videos/stripe-launch/capture`

Keep all capture artifacts (screenshots, downloaded assets, extracted data files) inside a dedicated `capture/` subfolder of your project directory — this keeps them cleanly separated from the build files you'll create in later steps (`SCRIPT.md`, `STORYBOARD.md`, `DESIGN.md`, the finished compositions, the rendered video, etc.), which live at the project root.

No API keys are required for the capture itself. It automatically extracts design tokens (colors, fonts), takes screenshots, and downloads assets with contextual descriptions. Optionally, if a Gemini API key is set in the environment (`GEMINI_API_KEY` / `GOOGLE_API_KEY`), the capture can generate richer AI-written descriptions of each image it downloads (at a small per-image cost).

Once the capture finishes, read through what it produced and build a working understanding of the site. After reading each file below, write a short 1-2 sentence summary — these summaries become working memory even after the raw file content is no longer directly in front of you.

**Must read:**
1. **The scroll screenshots** — a sequence of full-viewport screenshots covering the entire page height. Start with the very first one (the hero section, full resolution) — this is the most important single image; note whether the background is light or dark, what the dominant visual element is, and what colors stand out. Then look through the rest to see the whole page. After viewing them all, write 3-4 sentences describing the site's visual mood, layout patterns, color strategy, and overall feel.
2. **The extracted design-token data** — note the top 5-7 colors (as hex values), every font family and its available weights, the number of distinct sections on the page, and the number of headings/CTAs.
3. **The extracted visible-text data** — each line is tagged with its HTML element type (heading, paragraph, link). Use these tags to understand the page's information hierarchy: headings are the key messages, paragraphs are supporting copy. Strip the tag label when you quote this text later in your script.
4. **The extracted asset descriptions** — a one-line summary per downloaded asset. Note which ones are the most visually striking or most useful for a video (hero images, logos, product screenshots).

**Read if present:** any extracted animation data (scroll-triggered animations, marquees, canvas/WebGL effects, named CSS animations); any Lottie animation manifest (view the preview images); any video manifest (view the preview images for each embedded video); any extracted shader/GLSL data (if the site uses WebGL visual effects, this contains the actual shader source — read it to extract the color values used in gradients and the general algorithmic approach; you can recreate similar effects using Canvas 2D, per `references/techniques.md`).

**Read on-demand, only when needed for a specific scene:** individual images and SVGs in the assets folder — use the asset-description index to find what's needed rather than opening everything.

**For a rich capture with 30+ images:** it's worth doing a dedicated, focused pass whose only job is: "look at every image and every SVG in the captured assets, and for each one write one line: filename, what it shows, dominant colors, approximate size." Use that catalog as the asset reference for the rest of the process.

**Gate — before moving to Step 2, write out a short site summary:**
- Site: [name]
- Colors: [top 3-5 hex values with their roles]
- Fonts: [font families]
- Sections: [count] sections, [count] headings, [count] CTAs
- Key assets: [3-5 most useful assets for the video]
- Vibe: [one sentence describing the visual identity]

### Step 2: Write a brand cheat sheet (DESIGN.md)

Write a `DESIGN.md` file — a concise brand reference for the captured site, roughly 90 lines across 6 fixed sections (Overview, Colors, Typography, Elevation, Components, Do's and Don'ts). This is a cheat sheet you'll consult while writing the storyboard and building compositions later — it is NOT the creative plan itself (that's Step 4). See `references/design-guide.md` for the required structure and two full worked examples (a dark cinematic brand and a light corporate brand).

**Gate:** `DESIGN.md` exists in the project directory before moving on.

### Step 3: Write the narration script (SCRIPT.md)

Before writing, re-read `DESIGN.md`, especially its Overview and Components sections — your script should reference real product features, real stats, and real components the site actually highlights, using exact numbers pulled from the extracted visible-text data.

The script is the backbone of the whole video — every downstream scene duration, animation timing, and beat comes from the narration, so write it before the storyboard, not after.

Save as `SCRIPT.md`. See `references/script-guide.md` for pacing rules, tone guidance, number-pronunciation rules, structure, and a full worked example.

**Gate:** `SCRIPT.md` exists before moving on.

### Step 4: Write the storyboard (STORYBOARD.md)

Before writing anything, fully re-read: `DESIGN.md` (every creative decision must be grounded in the actual brand identity you captured); the extracted asset-description data in full (this is your menu of available visuals); and `references/techniques.md` (pick 2-3 techniques per beat).

The storyboard is the creative north star — it tells whoever builds the actual video compositions exactly what to build for each beat: mood, camera, animations, transitions, assets, sound. Write it as if you're briefing a motion designer who has never seen the website.

Save as `STORYBOARD.md`. See `references/storyboard-guide.md` for the full required structure (global direction block, asset audit table, per-beat direction fields, transition-type decision table, and three full worked example beats).

**Gate:** `STORYBOARD.md` exists with beat-by-beat direction and an asset audit table before moving on.

### Step 5: Generate voiceover and map timing

**Audition voices before committing** — generate the first sentence of `SCRIPT.md` in 2-3 different voices/providers and pick the one that sounds most natural. Generate the full script as `narration.wav`, save the literal spoken text (with pronunciation substitutions applied) as `narration.txt`, then get word-level timestamps (either from the TTS provider directly, or via a separate transcription pass) and map them onto `STORYBOARD.md`'s beats, replacing estimated timecodes with real measured ones. See `references/production-guide.md` for the full process.

**Gate:** `narration.wav` (or `.mp3`) and `transcript.json` exist, and the beat timings in `STORYBOARD.md` have been updated to real measured values.

### Step 6: Build the compositions

Before building anything, fully re-read `DESIGN.md`, `STORYBOARD.md`, the asset descriptions, `references/techniques.md`, and `transcript.json`. Work one beat at a time with a clean/focused context per beat: build the static end-state first, verify the layout, add entrance animations, add continuous mid-scene motion to every element, add the exit/transition, cross-check assets against the storyboard, then self-review. See `references/production-guide.md` for the full per-beat process, the critical technical rules the rendering engine requires (no infinite loops, no `Math.random()`, explicit timeline registration, flexbox centering instead of transform-based centering under GSAP, minimum font sizes, no full-screen dark linear gradients, and more), and the self-review checklist.

**Gate:** every composition has been self-reviewed for layout, asset placement, and animation quality — no overlapping elements, no misplaced assets, no static images without any motion.

### Step 7: Validate and deliver

Run `npx hyperframes lint` then `npx hyperframes validate`, fixing all errors from one before moving to the next. Render still snapshots at each beat's midpoint with `npx hyperframes snapshot <project-dir> --at <timestamps>` and review every one carefully against the checklist in `references/production-guide.md`. Then run `npx hyperframes preview` and let whoever owns the video scrub through it and flag changes. **Rendering to a final MP4 is on-demand only — never automatic**; only render (`npx hyperframes render --output renders/<project-name>.mp4`) when explicitly asked.

**Gate:** `npx hyperframes lint` and `npx hyperframes validate` both pass with zero errors.

## Quick reference

**Common video types and their typical shape:**

| Type | Duration | Beats | Narration |
|---|---|---|---|
| Social ad (IG/TikTok) | 10-15s | 3-4 | Optional hook sentence |
| Product demo | 30-60s | 5-8 | Full narration |
| Feature announcement | 15-30s | 3-5 | Full narration |
| Brand reel | 20-45s | 4-6 | Optional, music focus |
| Launch teaser | 10-20s | 2-4 | Minimal, high energy |

**Common output formats:**
- Landscape: 1920x1080 (default)
- Portrait: 1080x1920 (Instagram Stories, TikTok)
- Square: 1080x1080 (Instagram feed)

## Reference files

- `references/design-guide.md` — Step 2: full DESIGN.md structure + two worked examples.
- `references/script-guide.md` — Step 3: pacing, tone, number-pronunciation table, structure, worked example.
- `references/storyboard-guide.md` — Step 4: global direction block, asset audit rules, per-beat fields, motion-verb table, transition decision table, three worked beats, file layout.
- `references/production-guide.md` — Steps 5-7: voiceover/timing mapping, the per-beat build process, the critical deterministic-rendering technical rules, the composition self-review checklist, and the validate/snapshot/preview/render process.
- `references/techniques.md` — 11 visual-technique code patterns (SVG path drawing, Canvas 2D procedural art, CSS 3D transforms, per-word kinetic typography, Lottie, video compositing, character-by-character typing, variable font animation, motion-path animation, velocity-matched transitions, audio-reactive animation) plus a table matching technique combinations to video energy. Used in Steps 4 and 6.

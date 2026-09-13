# Website to Video (HyperFrames)

This document describes a 7-step process for turning an existing website into a professional short video — a product launch video, a social ad, a feature announcement, a brand reel, or a launch teaser — using HyperFrames, an open-source, HTML-based video-rendering framework ("HTML in, video out"). Use this whenever someone gives you a URL and wants a video made from it, or asks to "capture this site," "turn this into a video," "make a promo from my site," or similar. Each of the 7 steps produces a concrete artifact (a file) that gates moving on to the next step — don't skip a step or its artifact.

HyperFrames is installed and run via its command-line interface (`npx hyperframes ...`). It works by treating HTML `<div>` elements as keyframes, HTML data attributes as a timeline, CSS as visual styling, and the GSAP animation library as the animation engine — anything a web browser can render (CSS animations, GSAP, Lottie animations, WebGL shaders, Three.js, embedded video) can become a frame in the final rendered video. The renderer captures every frame deterministically and produces an MP4.

## How to use this — the 7-step workflow

### Step 1: Capture the site and understand it

Run the capture command, pointed at the URL and an output folder:

```bash
npx hyperframes capture <URL> -o <project-dir>/capture
```

Example: `npx hyperframes capture https://stripe.com -o videos/stripe-launch/capture`

Keep all capture artifacts (screenshots, downloaded assets, extracted data files) inside a dedicated `capture/` subfolder of your project directory — this keeps them cleanly separated from the build files you'll create in later steps (`SCRIPT.md`, `STORYBOARD.md`, `DESIGN.md`, the finished compositions, the rendered video, etc.), which live at the project root.

No API keys are required for the capture itself. It automatically extracts design tokens (colors, fonts), takes screenshots, and downloads assets with contextual descriptions. Optionally, if you set a Gemini API key in your environment, the capture can generate richer AI-written descriptions of each image it downloads (at a small per-image cost).

Once the capture finishes, read through what it produced and build a working understanding of the site. After reading each file below, write yourself a short 1-2 sentence summary — you'll want these summaries as working memory even after the raw file content is no longer directly in front of you.

**Must read:**
1. **The scroll screenshots** — a sequence of full-viewport screenshots covering the entire page height. Start with the very first one (the hero section, full resolution) — this is the most important single image; note whether the background is light or dark, what the dominant visual element is, and what colors stand out. Then look through the rest to see the whole page. After viewing them all, write 3-4 sentences describing the site's visual mood, layout patterns, color strategy, and overall feel.
2. **The extracted design-token data** — note the top 5-7 colors (as hex values), every font family and its available weights, the number of distinct sections on the page, and the number of headings/CTAs.
3. **The extracted visible-text data** — each line is tagged with its HTML element type (heading, paragraph, link). Use these tags to understand the page's information hierarchy: headings are the key messages, paragraphs are supporting copy. Strip the tag label when you quote this text later in your script.
4. **The extracted asset descriptions** — a one-line summary per downloaded asset. Note which ones are the most visually striking or most useful for a video (hero images, logos, product screenshots).

**Read if present:**
5. Any extracted animation data — note if the site uses scroll-triggered animations, marquees, canvas/WebGL effects, or named CSS animations.
6. Any Lottie animation manifest — view the preview images to see what each animation looks like.
7. Any video manifest — view the preview images for each embedded video.
8. Any extracted shader/GLSL data — if the site uses WebGL visual effects (gradient waves, particle systems, noise fields), this contains the actual shader source code. Read it to extract the color values used in gradients and the general algorithmic approach (noise functions, blend modes) — you can recreate similar effects in your own compositions using Canvas 2D or an embedded WebGL canvas (see the Canvas 2D technique in the templates section below).

**Read on-demand, only when you need it for a specific scene:** individual images and SVGs in the assets folder — use the asset-description index to find what you need rather than opening everything.

**For a rich capture with 30+ images:** it's worth doing a dedicated, focused pass — either yourself or by delegating the task to a helper — whose only job is: "look at every image and every SVG in the captured assets, and for each one write one line: filename, what it shows, dominant colors, approximate size." Use that catalog as your asset reference for the rest of the process.

**Gate — before moving to Step 2, write out a short site summary:**
- Site: [name]
- Colors: [top 3-5 hex values with their roles]
- Fonts: [font families]
- Sections: [count] sections, [count] headings, [count] CTAs
- Key assets: [3-5 most useful assets for the video]
- Vibe: [one sentence describing the visual identity]

### Step 2: Write a brand cheat sheet (DESIGN.md)

Write a `DESIGN.md` file — a concise brand reference for the captured site, roughly 90 lines across 6 fixed sections. This is a cheat sheet you'll consult while writing the storyboard and building compositions later — it is NOT the creative plan itself (that's Step 4). See the Templates section below for the required structure and a full worked example.

Gate: `DESIGN.md` exists in the project directory before moving on.

### Step 3: Write the narration script (SCRIPT.md)

Before writing, re-read `DESIGN.md`, especially its Overview and Components sections — your script should reference real product features, real stats, and real components the site actually highlights, using exact numbers pulled from the extracted visible-text data.

The script is the backbone of the whole video — every downstream scene duration, animation timing, and beat comes from the narration, so write it before the storyboard, not after.

Save as `SCRIPT.md`. See the Templates section below for pacing rules, tone guidance, number-pronunciation rules, structure, and a full worked example.

Gate: `SCRIPT.md` exists before moving on.

### Step 4: Write the storyboard (STORYBOARD.md)

Before writing anything, fully re-read: `DESIGN.md` (every creative decision must be grounded in the actual brand identity you captured — if the site is light with a purple accent, plan light scenes, not dark moody ones); the extracted asset-description data in full (this is your menu of available visuals — read every line, and view directly any asset whose description you don't fully understand before assigning it to a beat); and the visual-techniques reference in the Templates section below (pick 2-3 techniques per beat).

The storyboard is the creative north star — it tells whoever builds the actual video compositions exactly what to build for each beat: mood, camera, animations, transitions, assets, sound. Write it as if you're briefing a motion designer who has never seen the website.

Save as `STORYBOARD.md`. See the Templates section below for the full required structure (global direction block, asset audit table, per-beat direction fields, transition-type decision table, and three full worked example beats).

Gate: `STORYBOARD.md` exists with beat-by-beat direction and an asset audit table before moving on.

### Step 5: Generate voiceover and map timing

**Audition voices before committing.** Never just use the first voice you try — generate the first sentence of `SCRIPT.md` in 2-3 different voices/providers and pick the one that sounds most natural and conversational. Listen specifically for pacing: does it breathe between sentences? Does it sound like a person or a robot? Options include a free local TTS engine (HyperFrames ships a `npx hyperframes tts SCRIPT.md --voice <voice-name> --output narration.wav` command that runs locally with no API key, though it requires a reasonably current Python installation), a premium cloud TTS service with a wide voice selection (note: some of these don't return word-level timestamps, so you'll need a separate transcription pass afterward), or a TTS service that returns word timestamps directly as part of generation (which saves you the separate transcription step).

Generate the full script as `narration.wav` (or `.mp3`) in the project directory. Also save the exact text you sent to the TTS engine — with pronunciation substitutions already applied (e.g. "API" → "A P I", "$2T" → "two trillion") — as `narration.txt` in the same directory. This is distinct from `SCRIPT.md` (the human-readable creative document); having the literal spoken-text version saved separately makes it trivial to regenerate the audio later with a different voice without re-deriving all the pronunciation substitutions.

**Transcribe for word-level timestamps** (skip this if your TTS provider already returned them):

```bash
npx hyperframes transcribe narration.wav
```

This produces `transcript.json` — a list of `{ text, start, end }` entries, one per word. These timestamps become the source of truth for every beat's duration.

**Map timestamps to beats.** Go through `STORYBOARD.md` beat by beat. For each beat: find the first word of that beat's narration cue in the transcript, find the last word, set the beat's start time to the first word's start time and its end time to the last word's end time, and add 0.3-0.5 seconds of padding at the end for visual breathing room. Update `STORYBOARD.md` with these real durations, replacing your original estimated timecodes with the actual measured ones. Beat boundaries should land on word onsets — i.e., hard cuts synced to the voice.

Gate: `narration.wav` (or `.mp3`) and `transcript.json` exist, and the beat timings in `STORYBOARD.md` have been updated to real measured values.

### Step 6: Build the compositions

Before building anything, fully re-read: `DESIGN.md` (every composition must use the exact hex colors and font families from this file — if it says white backgrounds, use white, not dark); `STORYBOARD.md` (the beat-by-beat plan you're now executing — each beat specifies its assets, animations, transitions, and techniques); the extracted asset-description data (when the storyboard assigns an asset to a beat, re-read its description to understand what it actually shows and how to position/style it correctly); the visual-techniques reference for the code patterns behind whatever techniques the storyboard calls for; and `transcript.json` for the word-level timestamps driving scene durations.

**Work one beat at a time, with a clean/focused context per beat.** By this point you'll have accumulated a large amount of captured data, plus `DESIGN.md`, `SCRIPT.md`, `STORYBOARD.md`, and the transcript, all competing for attention. Building each composition is much more reliable if you deliberately narrow your focus to one single beat at a time — read that beat's storyboard section fresh, build it, review it, and only then move to the next beat, rather than trying to hold the entire video's worth of detail in mind at once. If you're delegating pieces of this work (e.g. to a sub-task or helper), give each one only what it needs: the specific storyboard section for its one beat, plus asset file *paths* (not inlined file contents — see the critical rule below), plus font file paths.

**Per-composition process, for each beat:**
1. Read that beat's storyboard section fully — mood, visual description, assets, animation choreography, transition, SFX — before writing any HTML.
2. Build the static end-state first. Position every element exactly where it should be at its most visible moment (the point where everything has fully entered and is correctly placed), as plain static HTML+CSS, with no animation yet. The CSS position is the ground truth; animations are just the journey to and from it.
3. Verify the static layout by actually looking at it: are elements where the storyboard says they should be? Are depth layers present (foreground/midground/background)? Any unintended overlaps? Are assets sized sensibly (a hero image should fill 50-70% of the frame, not sit at 100x100px)?
4. Add entrance animations, animating FROM an offscreen/invisible starting state TO the already-correct CSS position.
5. Add mid-scene activity. Every visible element needs continuous, ongoing motion — a still image sitting on a still background is just a JPEG with a progress bar underneath it. Common patterns: a slow zoom or pan on any photo/screenshot; a number counting up from 0 to its target value; a subtle shimmer sweep or gentle pulse on a logo grid; a subtle float (a few pixels of vertical drift, looping) on any persistent element; for a logo or CTA under music or dramatic narration, audio-reactive scale/glow driven by the beat.
6. Add the exit/transition specified by the storyboard for this beat — a CSS-based exit animation, a shader-based transition (a more expensive, "wow moment" style transition — reserve these for a handful of true centerpiece beats, like the opening hero reveal and the closing CTA, since overusing them flattens their impact), or a hard cut with no exit animation at all.
7. Cross-check assets actually used: re-open the storyboard's asset assignments for this beat, confirm every one is actually referenced in your HTML by filename, and add anything missing. Also check for two common failure patterns: (a) an SVG or image having been pasted inline as raw markup/data instead of referenced as a file — replace any inlined asset with a proper file reference; (b) a captured local font file existing but the composition still pulling from a generic web font source instead — replace with a local font reference.
8. Self-review the finished composition against the checklist in the Rules section below.
9. Move to the next beat.

**Asset presentation — never embed a raw flat, static image.** Every image needs some motion treatment: a perspective tilt for a sense of depth, a slow Ken Burns zoom (subtle scale increase over the beat's duration) to make a photo feel cinematic, wrapping it in a simple device frame (laptop/phone shape), extracting one element and animating it at a different depth for a parallax effect, or clipping it to a window and animating its position for a scroll-reveal effect.

**Audio wiring** goes in the root file that orchestrates the whole video: the narration track, an optional music/underscore track (typically at a much lower volume so it sits under everything), optional individual sound-effect elements at specific timestamps, and — only if explicitly requested — burned-in captions as a separate synchronized element.

Gate: every composition has been self-reviewed for layout, asset placement, and animation quality — no overlapping elements, no misplaced assets, no static images without any motion.

### Step 7: Validate and deliver

Run these two checks in sequence, fixing all errors from one before moving to the next:

```bash
npx hyperframes lint
npx hyperframes validate
```

`lint` checks the HTML structure statically (missing required attributes, timeline registration, animation-tween conflicts). `validate` actually loads each composition in a headless browser and catches runtime JavaScript errors, missing assets, and failed network requests.

**Visual verification (snapshot).** After lint and validate both pass, render still snapshots so you can actually see your own output — always use the built-in snapshot command rather than assembling your own frame-capture script, since later tooling expects its specific file-naming convention:

```bash
npx hyperframes snapshot <project-dir> --at <beat-midpoints>
```

Calculate a midpoint timestamp for each beat from your `STORYBOARD.md` timings (aim for roughly 60-70% into each beat — after its entrance animation has finished but before its exit begins) and pass them as a comma-separated list, e.g. `npx hyperframes snapshot <project-dir> --at 2.9,10.4,18.7,23.9`. Output lands as individual PNG files in a `snapshots/` folder.

**View every snapshot carefully — don't just glance and move on.** For each one, check:
- **Visibility:** Is there actually visible content (not an all-white or all-black frame)? Can you read every piece of text (watch for white-on-light or dark-on-dark text)? Are the images/assets actually showing (empty space where an image should be usually means a bad file path)?
- **Positioning and layout:** Do background images fill the entire frame? Are elements positioned where the storyboard says they should be? Is more than about 40% of the frame empty/flat with nothing on it (too sparse)? Is anything overlapping incorrectly, or bleeding off the frame edge?
- **Visual quality:** Are any overlays too heavy (a background barely visible through a dark tint)? Is there one clear dominant element per frame, with everything else clearly secondary? Do the actual rendered colors match `DESIGN.md`?
- **Code vs. rendered cross-check:** for each beat, does the snapshot actually show every asset your HTML references? If an image tag is present but nothing shows up, the file isn't loading, the path is wrong, or it's hidden behind another layer. If a snapshot shows nothing useful at a given timestamp, try a slightly later one — the composition might still be mid-entrance-animation at that exact moment.

If any frame has issues, go back to Step 6 and fix that specific composition before proceeding.

**Preview:**

```bash
npx hyperframes preview
```

This opens an interactive studio view in a browser where you can scrub through every beat.

**Rendering to a final MP4 file is on-demand only — never automatic.** The preview IS the delivery: let whoever you're building this for scrub through it and flag anything they want changed before you spend the time rendering a final file (rendering takes real wall-clock time and is wasted effort if changes are still coming). Only render when explicitly asked — "render it," "make the final," "export the MP4," "I'm happy, produce the file." When you do render, always specify an explicit, human-readable output filename rather than accepting the tool's default timestamped filename:

```bash
npx hyperframes render --output renders/<project-name>.mp4
```

Example: `npx hyperframes render --output renders/stripe-launch.mp4`

For vertical/social formats, check the render command's help output for the relevant viewport/format flags.

Gate: `npx hyperframes lint` and `npx hyperframes validate` both pass with zero errors.

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

## Rules & standards

### Global storyboard guardrails (Step 4)

Every `STORYBOARD.md` should open with a global-settings block:

```markdown
**Format:** 1920×1080
**Audio:** [TTS provider] voiceover + underscore + SFX
**VO direction:** [voice character — e.g., "mid-age male, calm confident delivery,
Apple keynote register — economy of words, silence between sentences is a feature"]
**Style basis:** DESIGN.md (brand colors, fonts, components from the captured site)
```

Followed by guardrails, adapted to the specific brand:
- Push color presence — muted is fine, flat is not. Every beat should have at least one color that pulls the eye.
- Motion should be visible and intentional — err toward more movement than feels safe; subtle motion reads as static at 30fps.
- Use as many captured assets as the creative vision allows, generously — the assets exist, use them.
- Aim for 8-10 visual elements per beat, not 2-3. A strong beat has background texture, midground content, foreground accents, floating decorative elements, animated icons, and typographic detail — it should feel dense and alive.
- Use at least 2-3 different visual techniques per beat, not just across the whole video. Don't default to plain fade/scale/opacity for everything — mix in SVG path drawing, CSS 3D transforms, typing effects, counter animations, procedural canvas art. Each beat should feel like its own visual world.

If there's an underscore/music track, describe its mood, reference artists, and exactly when it swells or drops — e.g. "Minimal electronic. Warm sustained pad already playing when the video starts. Sits underneath everything, never competing with VO. Swells gently during the flex section, drops to near-nothing for the comparison, resolves on a final chord."

### Asset audit rules (Step 4)

Before writing any beats, audit every captured asset in a table (Asset / Type / Assign to Beat / Role), and enforce these minimums:
- At least 50% of product screenshots and hero images must appear somewhere in the video.
- The brand logo must appear in both the first AND the last beat.
- The site's single most signature visual (its gradient wave, hero illustration, or key product UI) must appear — it's the most recognizable brand element and skipping it is a mistake.
- No more than 2 consecutive text-only beats — the 3rd must contain a visual asset.
- The opening beat must contain a visual asset, never text-only.

### Per-beat direction fields (Step 4)

Each beat in the storyboard needs: a **Concept** (2-3 sentences on the visual world, the metaphor, and the feeling — write this first, everything else flows from it); the **VO cue** (which narration line plays over this beat); a **Visual description** written cinematically with camera language (pan, zoom, drift, settle), describing at least 5 distinct visual elements across foreground/midground/background, not just "text + background"; a **Mood direction** using cultural/design references rather than hex codes (e.g. "Geometric, rhythmic, precise — think Josef Albers or Bauhaus color studies"); the specific **Assets** to use, referenced by filename; an **Animation choreography** naming a specific motion verb for every element (see the energy table below — if you can't name the verb, the element isn't yet designed); a **Transition** specification (see the decision table below); **Depth layers** (every beat needs at least 2 — what's in foreground vs. background); and **SFX cues** (what sound plays at what moment).

**Motion verb energy levels:**

| Energy | Verbs | Example |
|---|---|---|
| High impact | SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS | "$1.9T" SLAMS in from left at -5° |
| Medium energy | CASCADE, SLIDES, DROPS, FILLS, DRAWS | Three cards CASCADE in staggered 0.3s |
| Low energy | types on, FLOATS, morphs, COUNTS UP, fades in | Counter COUNTS UP from 0 to 135K |

**Transition type decision table:**

| Choose a shader transition for | Choose a CSS transition for | Choose a hard cut for |
|---|---|---|
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments | Continuous camera-motion beats where the scene feels like one move broken into cuts | Rapid-fire lists, percussive edits on the beat, comedic timing |
| Any moment the music/VO punctuates with a downbeat or SFX hit | Beats that ease from one composition into the next with shared motion vocabulary | Sequences of 3+ quick tempo-matched switches |
| Brand moments where the transition itself IS the visual | Minimal/editorial pacing | Anytime a 0.3-0.8s transition would feel too slow |

Rule of thumb: shader-transition into the true centerpiece beats of the video; CSS-transition or hard-cut the connective-tissue beats in between. A 5-7 beat brand reel usually wants only 1-2 shader transitions (the hero reveal and the CTA) — too many flattens their impact.

Common CSS transition patterns: velocity-matched upward (exit with upward motion + blur + fast ease-in, enter with the mirror motion decelerating); whip pan (fast horizontal motion + blur on both exit and entry); blur-through (pure blur ramp on both sides); zoom-through (scale + blur on both sides); or a hard/smash cut for rapid sequences. How velocity-matching works: exit the outgoing beat with an accelerating ease curve plus a blur ramp, and enter the incoming beat with a decelerating ease curve plus a blur clear — matching the exit velocity to the entry velocity within roughly 5% tolerance makes the viewer perceive one continuous camera move rather than two separate animations glued together.

### Script pacing and tone rules (Step 3)

- 2.5 words per second is a natural speaking pace. 15 seconds ≈ 37 words. 30 seconds ≈ 75 words. 60 seconds ≈ 150 words.
- Leave room for pauses — silence between sentences is a feature, not dead air. The script should feel noticeably shorter than the finished video; visual breathing room matters.
- Write like a person, not a brochure: use contractions ("it's," "you'll," "that's," "we've"), vary sentence length (short punchy phrases mixed with longer flowing ones), read it out loud and rewrite anything that sounds robotic, and avoid jargon unless the audience clearly expects it.
- **Number pronunciation — write what you want the voice to actually say, since TTS reads literally:**

  | On the website | Write in the script as |
  |---|---|
  | 135+ | more than one hundred thirty five |
  | $1.9T | nearly two trillion dollars |
  | 99.999% | ninety nine point nine percent |
  | 200M+ | over two hundred million |
  | 10x | ten times |
  | API | A P I |
  | stripe.com | stripe dot com |

  The visual on screen can still show the exact figure while the voice rounds it for natural speech.

- **Structure:** a hook (something surprising or impressive — a bold claim, a provocative question, a contrast, or a striking number; vary which type you use rather than always defaulting to a stat), a story (what the product does and who uses it, kept concrete), proof (real stats, real customer names, real numbers from the site), and a call to action (what the viewer should do next). Not every video needs all four — a 15-second social ad might be just Hook + Proof + CTA.
- **The opening line is the single most important sentence in the video** — it must create tension, curiosity, or surprise within the first 3 seconds. If your opening is generic ("Welcome to Stripe," "Introducing our product"), start over. Patterns that work: a bold claim ("The financial infrastructure that powers the internet economy"), a provocative question ("What if your database could think?"), a contrast ("Your AI agent already knows how to make videos. It just needs the right format."), or a shocking number (use sparingly — not every video should open with a stat).

### Critical technical rules for building compositions (Step 6)

These exist because the underlying rendering engine is deterministic — violating them produces broken output:
- **No infinite repeat loops** — calculate the exact number of repeats needed from the beat's actual duration instead.
- **No non-deterministic randomness** (e.g. `Math.random()`) — use a seeded pseudo-random number generator instead, so the same frame always renders identically.
- **Register every animation timeline** so the renderer can find and play it (e.g. storing it on a well-known global lookup keyed by a composition id).
- **Build timelines synchronously** — don't wrap timeline-construction code in async/await.
- **Never use a CSS `transform` for centering an element** that also has GSAP-driven animation on it — not `translate(-50%, -50%)`, not `translateX(-50%)` alone. GSAP animates the `transform` property directly, and doing so overwrites ALL existing CSS transforms including any centering offset, which sends the element flying off-screen. Use flexbox centering on a wrapper element instead (`display:flex; align-items:center; justify-content:center`).
- **Minimum font sizes:** 20px for body text, 16px for labels — anything smaller becomes unreadable after video compression.
- **No full-screen dark linear gradients** — they create visible banding artifacts in H.264 video compression. Use a solid fill plus localized radial glows instead.
- Every root-level composition element needs both a start-time attribute and a duration attribute set explicitly — without an explicit duration, a composition with any looping animation inside it can be interpreted as having an infinite duration, which stalls playback.
- If you animate captions or on-screen text out with a fade, follow the fade with an explicit, deterministic "kill" step (forcing opacity to 0 and visibility to hidden) — otherwise a per-word or per-character animation running inside that same text can override the fade-out and leave text stuck on screen.
- Don't reference the exact same image/video file twice with identical start-time and duration values — this can cause the renderer to discover and double-render it. Either use a single element with proper depth-layering, or stagger the start times.

### Self-review checklist for every composition (Step 6)

- Every asset assigned to this beat in the storyboard is actually present and referenced by file path in the HTML (not inlined).
- Elements are positioned where the storyboard specifies — no misplacement.
- No overlapping text (text over text is always a readability failure).
- At least 2 depth layers are present.
- Every visible element has ongoing mid-scene motion, not just an entrance and an exit.
- Font sizes are at or above the minimums (20px body / 16px labels).
- No full-screen dark linear gradients.
- The timeline is properly registered so the renderer can find it.
- Colors match `DESIGN.md` exactly — paste the hex value directly rather than approximating it by eye.
- Every composition's root element has both its start-time and duration attributes explicitly set.
- Any caption/text fade-out has a deterministic hard-kill step following it.
- No duplicate media references with identical timing.

## Templates & examples

### DESIGN.md — required structure (Step 2)

Six fixed sections, kept under ~100 lines total:

**`## Overview`** — 3-4 factual sentences: layout patterns (bento grid, logo wall, hero section), color strategy, typography tone, overall feel. Precise, not poetic.

**`## Colors`** — 5-10 key colors with exact hex values and their roles, e.g.:
```
- **Primary Surface**: `#020204` — deep black background
- **Primary Content**: `#FFFFFF` — high-purity white for text and borders
- **Accent Warm**: `#FB923C` — orange for CTAs and highlights
```

**`## Typography`** — font families with weights, roles, and any distinctive usage, e.g.:
```
- **Serif**: Cormorant Garamond (Italic). Major headings, brand identity.
- **Monospace**: Geist Mono. Subheaders, labels, terminal readouts. High tracking (0.1-0.3em), all-caps.
- **Sans-Serif**: Inter. Body copy, interface elements. Small sizes (9-14px).
```

**`## Elevation`** — one paragraph on the site's depth strategy: borders, shadows, glassmorphism, or flat color shifts, with specific patterns named (e.g. "1px borders at white/10 opacity" or "layered backdrop-blur with thin borders").

**`## Components`** — name every notable UI component specifically ("Cinematic Accordion," not "Cards"; "Logo Marquee," not "Scrolling section"), noting its distinctive visual treatment.

**`## Do's and Don'ts`** — 3-5 rules each, derived from what the site actually does and doesn't do.

Rules: use exact hex values from the extracted design tokens, never approximate them. Name components by what you actually see, not generic terms. Keep the whole document under 100 lines — it's a cheat sheet, not a full design system. No "Style Prompt," "Assets," or "Motion" sections — those belong in the storyboard, not here.

**Full worked example (dark, cinematic brand):**

```markdown
# Design System

## Overview

Soulscape 2026 is a cinematic, "high-signal" digital experience that positions itself as the vanguard of AI filmmaking. The visual personality is dark, technical, and premium, characterized by high-contrast "Flare" on "Void" (white on black) aesthetics. The layout is dense but organized, utilizing heavy horizontal layering and border-defined sections to evoke a wide-screen cinematic feel. Motion is a core tenet, with atmospheric grain overlays, shifting light leaks, and slow-moving marquees creating constant, breathing texture.

## Colors

- **Primary Surface**: `#020204` (Void) - Deep black for the entire background.
- **Primary Content**: `#FFFFFF` (Flare) - High-purity white for typography and primary borders.
- **Accent 1 (Warm)**: `#FB923C` - Orange for industry/executive tiers and primary CTAs.
- **Accent 2 (Cool)**: `#60A5FA` - Blue for creative voices and summit-focused components.
- **Subtle Overlays**: `rgba(255, 255, 255, 0.02)` to `0.08` for glass backgrounds.

## Typography

- **Serif**: Cormorant Garamond (Italic). Major headings and "Soul" brand identity. Classical cinematic contrast.
- **Monospace**: Geist Mono. Subheaders, labels, terminal readouts. High tracking (0.1-0.3em), all-caps.
- **Sans-Serif**: Inter. Body copy and interface elements. Small sizes (9-14px).

## Elevation

- **Glassmorphism**: Components use backdrop-filter blur(10px) with thin borders (1px solid rgba(255, 255, 255, 0.08)).
- **Layering**: Depth via fixed global grain-overlay and localized light-leak gradients rather than box-shadows.
- **Interaction**: Hover triggers subtle translateY(-5px) and increased border opacity.

## Components

- **Cinematic Accordion**: Expanding horizontal/vertical card system where panels expand from compressed state to reveal full-bleed imagery and large serif typography.
- **HUD Explorer**: Floating mobile navigation trigger styled as a "Lens" with pulsing glow and terminal readouts.
- **Slow Marquees**: Continuous horizontal tickers for partner logos and veteran listings.
- **Glass Cards**: Content containers with subtle gradients, rounded corners (2.5rem), and high-contrast iconography.
- **Grain & Flicker**: Global CSS noise filters and holographic flicker animations on UI labels.

## Do's and Don'ts

### Do's

- Use thin subtle borders (white/10) to separate sections rather than solid color changes.
- Maintain high letter-spacing on all Geist Mono labels.
- Use serif italics for emotional or visionary statements.
- Keep imagery desaturated or stylized with dark gradients for readability.

### Don'ts

- Do not use bright solid background colors — the page must remain in "The Void."
- Do not use standard drop shadows — use radial glow or bloom effects instead.
- Do not use sharp high-speed animations — all motion should be fluid and breathing.
```

**Contrasting worked example (light, corporate brand):**

```markdown
# Design System

## Overview

Stripe's visual personality is defined by high-precision, technical sophistication, and a fluid, forward-moving motion language. The layout is dense but expertly balanced, utilizing a "canary" grid system that favors high-density data visualizations and modular bento-style layouts. The tone is authoritative and innovative, characterized by smooth CSS animations, complex SVG graphics that mimic UI dashboards, and the iconic "hero wave" background that uses layered gradients to create depth and movement.

## Colors

- **Brand Primary**: #635bff (The signature Stripe Blurple)
- **Text Solid**: #0a2540 (Deep navy for primary headings)
- **Text Soft**: #424770 (Subdued slate for descriptions and secondary text)
- **Surface Background**: #ffffff (White primary surface)
- **Surface Subdued**: #f6f9fc (Light gray for section contrast)
- **Accent Green**: #212d45 (Used in high-converting success UI graphics)
- **Accent Orange**: #ff6118 (Used for specific product highlights like Connect)
- **Accent Yellow**: #fc5 (Warm highlight used in bento cards)
- **Border Quiet**: #e6ebf1 (Soft borders for cards and dividers)

## Typography

- **Primary Font**: Sohne (sohne-var), a custom neo-grotesque that balances technical precision with approachability. Used across all headers and body copy.
- **Monospace Font**: SourceCodePro-Medium, specifically for code snippets, tabular data, and technical UI identifiers.
- **Heading Scale**: hds-heading--xxl ~3rem, hds-heading--lg ~1.5rem, hds-heading--md ~1.125rem
- **Body Scale**: Standard body text centers around 1rem (16px) with a line-height of 1.5-1.6.

## Elevation

- **Shadows**: Multi-layered shadow system (e.g., 0 30px 60px -12px rgba(50,50,93,0.25)). Shadows are diffused and deep for a floating effect.
- **Borders**: Heavy use of 1px solid borders to define bento grid boundaries instead of shadows in flat sections.
- **Glass/Layering**: Navigation overlays use backdrop-filter blur(5px) with translucent white background.

## Components

- **Navigation Popover**: Animated dropdown spanning page margin with multi-column bento layouts.
- **Bento Cards**: Interactive grid-aligned containers with gradient hover effects that follow the cursor.
- **Customer Marquee**: Seamless horizontal scrolling loop of flat-colored SVG logos.
- **UI Graphics**: Custom HTML/CSS representations of the Stripe Dashboard with tabular numbers and mini-charts.
- **CTA Buttons**: Rounded-pill shapes with subtle scale transforms on hover.

## Do's and Don'ts

- **Do**: Use smooth cubic-bezier(.25, 1, .5, 1) transitions for all hover states and entering animations.
- **Do**: Maintain strict vertical alignment between iconography and text labels.
- **Don't**: Use sharp-cornered cards; always apply a border-radius.
- **Don't**: Over-saturate backgrounds; stick to white or #f6f9fc and let brand assets provide color pop.
```

### SCRIPT.md — worked example (Step 3)

From a real 62-second product launch video (~140 words, 2.3 words/sec — leaving room for pauses and visual breathing):

```
Your AI agent already knows how to make videos.
It just needs the right format.

This is Hyperframes. An open source framework. HTML in, video out.

A div is a keyframe. Data attributes are your timeline.
CSS is your look. G-Sap is your animation engine.

Anything a browser can render can be a frame in your video.

CSS animations. G-Sap. Lottie. Shaders. Three.js.

Drop in music, sound effects, footage — it all composes together.

No new framework for the agent to learn.
Just HTML.

The agent writes it. The renderer captures every frame as MP4.
It's deterministic. Identical outputs, every time.

Give your agent the CLI. Tell it what to make.
Watch it build.

Hyperframes. Go make something.
```

### STORYBOARD.md — three worked example beats (Step 4)

The difference between a mediocre beat description and a great one: mediocre describes pixels ("Dark navy background. '$1.9T' in white, 280px. Logo top-left. Wave image bottom-right."); great describes an experience ("Camera is already mid-flight over a vast dark canvas. The gradient wave sweeps across the frame like aurora borealis — alive, shifting. '$1.9T' SLAMS into existence with such force the wave ripples in response. This isn't a slide — it's a moment."). Write the second, then figure out the pixel-level specifics.

**BEAT 1 — COLD OPEN (0:00–0:05)**

VO: "Your AI agent already knows how to make videos."

Concept: We're already in motion when the video starts. No title card, no fade from black. We're mid-flight over an infinite creative workspace — dozens of living compositions scattered below us like a city seen from a drone. Each one is alive, running a different animation. The message is clear before any words: this tool makes videos. Lots of them.

Visual: Slow smooth diagonal drift over a vast canvas (3600×2200px plane). Scattered across it: 25 composition cards at organic angles (±5-15° rotation), soft shadows, thin borders. Each card contains a DIFFERENT running animation — kinetic type, gradient morph, data viz, particle system, logo assembly, SVG drawing, shader noise, 3D rotating object. Depth-of-field: close cards slightly blurred, focal sweet-spot in mid-distance, far cards smaller and desaturated.

Camera: Diagonal drift top-left to bottom-right, slight 2-3° rotation over 5s. power1.inOut ease. Zoom accelerates in final second as we approach one specific card.

Assets: Product screenshots and logo on cards. Each card is a mini-composition with its own animation.

SFX: Ambient warmth pad already playing. Faint textured hum — overhearing creative activity from a distance.

**BEAT 5 — THE THESIS (0:20–0:24)**

VO: "Anything a browser can render can be a frame in your video."

Mood: Big statement. This sentence gets its own canvas. Clean, spacious, typographic.

Visual: Words appear as staggered kinetic typography. "Anything a browser can render" — distinctive serif, gentle fade + rise (y: 24px → 0, opacity 0 → 1, 0.4s, power2.out). Held beat — one second of stillness. "can be a frame in your video." appears below. As the final word lands, the entire text pulses once — a brief warm flash, subtle scale bump to 101%.

Transition OUT: Whip pan left — x:-400, blur:24px, opacity:0.4, 0.3s power3.in

SFX: Silence under the first line. On the capture pulse — a soft analog shutter click.

**BEAT 7 — THE CONTRAST (0:38–0:44)**

VO: "No new framework for the agent to learn. Just HTML."

Mood: Clean comparison. Light base. Two worlds side by side.

Visual: Left half: dense code, small, compressed, overwhelming. Scrolls slowly upward. Slightly desaturated. Right half: spacious HTML, syntax-highlighted, generous line spacing, inviting. On "Just HTML." — the left side folds inward along its center line, like a book closing. The right side expands to fill the frame. Warm glow rises behind it.

Transition IN: Zoom through — scale 0.75→1, blur 20px→0, 0.5s expo.out
Transition OUT: Velocity-matched upward — y:-150, blur:30px, 0.33s power2.in

Assets: Real framework code on the left (actual content, not lorem ipsum). Real HyperFrames HTML on the right.

SFX: Left side carries a faint low drone. On fold: drone cuts. Silence. Then a single clean chime as the right side expands.

### Suggested production file layout

```
project/
├── index.html                    root — VO + underscore + beat orchestration
├── DESIGN.md                     brand reference (from Step 2)
├── SCRIPT.md                     narration text (from Step 3)
├── STORYBOARD.md                 creative north star (from Step 4)
├── transcript.json               word-level timestamps (from Step 5)
├── narration.wav                 TTS audio (from Step 5)
├── capture/                      captured website data (from Step 1)
│   ├── screenshots/
│   ├── assets/
│   │   ├── svgs/
│   │   ├── fonts/
│   │   ├── lottie/
│   │   └── videos/
│   └── extracted/
│       ├── tokens.json
│       ├── visible-text.txt
│       ├── asset-descriptions.md
│       ├── animations.json
│       └── assets-catalog.json
└── compositions/
    ├── beat-1-hook.html
    ├── beat-2-features.html
    └── ...
```

### Visual technique code patterns (for Steps 4 & 6)

11 proven, standard motion-design patterns — every composition should use at least 2-3 of them per beat.

**1. SVG path drawing** — a path draws itself in real time, like someone tracing with a pen. Use for revealing diagrams, arrows, connector lines, or brand marks. Give the path a `stroke-dasharray` equal to its own total length and a matching `stroke-dashoffset`, then animate `stroke-dashoffset` to 0. Use the path's own `getTotalLength()` method to calculate the exact dasharray value dynamically rather than guessing it.

**2. Canvas 2D procedural art** — animated noise, particle fields, or data visualizations that evolve frame by frame. Draw into a `<canvas>` element using a deterministic hash function (not `Math.random()`) so the same frame always renders identically, and drive the redraw via a GSAP animation on a proxy time value with an `onUpdate` callback.

**3. CSS 3D transforms** — perspective rotations for depth; use for product showcases, card flips, architectural reveals. Always set `perspective` on the parent element and `transform-style: preserve-3d` on the element being rotated, then animate `rotationY`/`rotationX` via GSAP.

**4. Per-word kinetic typography** — words appear one by one, synced to the transcript's word-level timestamps. Wrap each word in its own inline-block span, start each at opacity 0, and animate each one in individually at its actual timestamp from the transcript, sliding in from a horizontal offset that decays across the sequence (e.g. 80px → 60px → 50px → 25px → 12px) to mimic a camera settling.

**5. Lottie animation** — vector animations (logos, character animations, icons) played inside a composition, either via a Lottie web-component player or the `lottie-web` library loading a local JSON animation file.

**6. Video compositing** — embedding real video footage inside a composition. Videos must be muted with `playsinline` set; the rendering framework itself controls playback/seeking, so don't call `.play()` manually.

**7. Character-by-character typing** — a terminal-style typing effect, updating a text element's content one character at a time on a timeline, paired with a blinking cursor using a stepped (non-eased) animation.

**8. Variable font axis animation** — animating `font-variation-settings` in real time to reshape glyphs, for fonts that expose axes like optical size or weight. Load the actual captured local variable font file via `@font-face` (never substitute a generic web font), then animate the relevant axis custom properties.

**9. Motion-path animation** — animating an element along an arbitrary SVG path (a slider following a curve, a particle along a trajectory, a guided reveal), using GSAP's motion-path plugin.

**10. Velocity-matched transitions** — exit one beat and enter the next with matched velocities so the cut reads as one continuous camera move. Exit with an accelerating ease plus a blur ramp; enter the next composition with a decelerating ease plus a matching blur clear, timed so the fastest point of both curves meets exactly at the cut.

**11. Audio-reactive animation** — driving any animatable property directly from the currently-playing audio track: a logo pulsing on bass hits, a CTA glowing on treble, a background subtly breathing during quiet passages. Use for videos with music or dramatic narration (skip for calm/tutorial pacing). How it works: pre-extract the audio's frequency bands into a data file (fps, total frame count, and a list of per-frame band-energy values), then sample it per-frame on the timeline (not as a single tween — a single tween will not react to audio; you need true per-frame sampling) to drive scale/glow/etc. Keep the intensity subtle on small elements (roughly ≤5% scale change, ≤30% glow change) — audio-reactive motion on tiny elements reads as jitter, not rhythm; bigger background elements can push further (10-30%). Avoid literal equalizer bars, spectrum analyzers, waveform displays, strobing, or rainbow color-cycling — the audio should drive timing and intensity, while the actual visual vocabulary still comes from the brand identity.

**Matching technique combinations to video energy:**

| Video energy | Techniques to combine |
|---|---|
| High impact (launches, promos) | Per-word typography + velocity transitions + counter animations |
| Cinematic (tours, stories) | SVG path drawing + video compositing + 3D transforms |
| Technical (dev tools, APIs) | Character typing + Canvas 2D procedural + motion-path animation |
| Premium (luxury, enterprise) | Variable font animation + Lottie + slow velocity transitions |
| Data-driven (stats, metrics) | Canvas 2D procedural + counter animations + SVG path drawing |

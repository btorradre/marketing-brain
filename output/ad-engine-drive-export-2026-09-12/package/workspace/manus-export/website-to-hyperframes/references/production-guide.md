# Steps 5-7: Voiceover, Build, Validate & Deliver

## Step 5: Generate voiceover and map timing

**Audition voices before committing.** Never just use the first voice you try — generate the first sentence of `SCRIPT.md` in 2-3 different voices/providers and pick the one that sounds most natural and conversational. Listen specifically for pacing: does it breathe between sentences? Does it sound like a person or a robot? Options include a free local TTS engine (HyperFrames ships a `npx hyperframes tts SCRIPT.md --voice <voice-name> --output narration.wav` command that runs locally with no API key, though it requires a reasonably current Python installation), a premium cloud TTS service with a wide voice selection (note: some of these don't return word-level timestamps, so you'll need a separate transcription pass afterward), or a TTS service that returns word timestamps directly as part of generation (which saves you the separate transcription step).

Generate the full script as `narration.wav` (or `.mp3`) in the project directory. Also save the exact text you sent to the TTS engine — with pronunciation substitutions already applied (e.g. "API" → "A P I", "$2T" → "two trillion") — as `narration.txt` in the same directory. This is distinct from `SCRIPT.md` (the human-readable creative document); having the literal spoken-text version saved separately makes it trivial to regenerate the audio later with a different voice without re-deriving all the pronunciation substitutions.

**Transcribe for word-level timestamps** (skip this if your TTS provider already returned them):

```bash
npx hyperframes transcribe narration.wav
```

This produces `transcript.json` — a list of `{ text, start, end }` entries, one per word. These timestamps become the source of truth for every beat's duration.

**Map timestamps to beats.** Go through `STORYBOARD.md` beat by beat. For each beat: find the first word of that beat's narration cue in the transcript, find the last word, set the beat's start time to the first word's start time and its end time to the last word's end time, and add 0.3-0.5 seconds of padding at the end for visual breathing room. Update `STORYBOARD.md` with these real durations, replacing your original estimated timecodes with the actual measured ones. Beat boundaries should land on word onsets — i.e., hard cuts synced to the voice.

**Gate:** `narration.wav` (or `.mp3`) and `transcript.json` exist, and the beat timings in `STORYBOARD.md` have been updated to real measured values.

## Step 6: Build the compositions

Before building anything, fully re-read: `DESIGN.md` (every composition must use the exact hex colors and font families from this file — if it says white backgrounds, use white, not dark); `STORYBOARD.md` (the beat-by-beat plan you're now executing — each beat specifies its assets, animations, transitions, and techniques); the extracted asset-description data (when the storyboard assigns an asset to a beat, re-read its description to understand what it actually shows and how to position/style it correctly); `techniques.md` for the code patterns behind whatever techniques the storyboard calls for; and `transcript.json` for the word-level timestamps driving scene durations.

**Work one beat at a time, with a clean/focused context per beat.** By this point you'll have accumulated a large amount of captured data, plus `DESIGN.md`, `SCRIPT.md`, `STORYBOARD.md`, and the transcript, all competing for attention. Building each composition is much more reliable if you deliberately narrow your focus to one single beat at a time — read that beat's storyboard section fresh, build it, review it, and only then move to the next beat, rather than trying to hold the entire video's worth of detail in mind at once. If you're delegating pieces of this work, give each one only what it needs: the specific storyboard section for its one beat, plus asset file *paths* (not inlined file contents), plus font file paths.

**Per-composition process, for each beat:**
1. Read that beat's storyboard section fully — mood, visual description, assets, animation choreography, transition, SFX — before writing any HTML.
2. Build the static end-state first. Position every element exactly where it should be at its most visible moment (the point where everything has fully entered and is correctly placed), as plain static HTML+CSS, with no animation yet. The CSS position is the ground truth; animations are just the journey to and from it.
3. Verify the static layout by actually looking at it: are elements where the storyboard says they should be? Are depth layers present (foreground/midground/background)? Any unintended overlaps? Are assets sized sensibly (a hero image should fill 50-70% of the frame, not sit at 100x100px)?
4. Add entrance animations, animating FROM an offscreen/invisible starting state TO the already-correct CSS position.
5. Add mid-scene activity. Every visible element needs continuous, ongoing motion — a still image sitting on a still background is just a JPEG with a progress bar underneath it. Common patterns: a slow zoom or pan on any photo/screenshot; a number counting up from 0 to its target value; a subtle shimmer sweep or gentle pulse on a logo grid; a subtle float (a few pixels of vertical drift, looping) on any persistent element; for a logo or CTA under music or dramatic narration, audio-reactive scale/glow driven by the beat.
6. Add the exit/transition specified by the storyboard for this beat — a CSS-based exit animation, a shader-based transition (a more expensive, "wow moment" style transition — reserve these for a handful of true centerpiece beats, like the opening hero reveal and the closing CTA, since overusing them flattens their impact), or a hard cut with no exit animation at all.
7. Cross-check assets actually used: re-open the storyboard's asset assignments for this beat, confirm every one is actually referenced in your HTML by filename, and add anything missing. Also check for two common failure patterns: (a) an SVG or image having been pasted inline as raw markup/data instead of referenced as a file — replace any inlined asset with a proper file reference; (b) a captured local font file existing but the composition still pulling from a generic web font source instead — replace with a local font reference.
8. Self-review the finished composition against the checklist below.
9. Move to the next beat.

**Asset presentation — never embed a raw flat, static image.** Every image needs some motion treatment: a perspective tilt for a sense of depth, a slow Ken Burns zoom (subtle scale increase over the beat's duration) to make a photo feel cinematic, wrapping it in a simple device frame (laptop/phone shape), extracting one element and animating it at a different depth for a parallax effect, or clipping it to a window and animating its position for a scroll-reveal effect.

**Audio wiring** goes in the root file that orchestrates the whole video: the narration track, an optional music/underscore track (typically at a much lower volume so it sits under everything), optional individual sound-effect elements at specific timestamps, and — only if explicitly requested — burned-in captions as a separate synchronized element.

**Gate:** every composition has been self-reviewed for layout, asset placement, and animation quality — no overlapping elements, no misplaced assets, no static images without any motion.

### Critical technical rules for building compositions

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

### Self-review checklist for every composition

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

## Step 7: Validate and deliver

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

**Gate:** `npx hyperframes lint` and `npx hyperframes validate` both pass with zero errors.

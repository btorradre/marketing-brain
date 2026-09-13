# Step 4: Write the Storyboard

Before writing anything, fully re-read: `DESIGN.md` (every creative decision must be grounded in the actual brand identity you captured — if the site is light with a purple accent, plan light scenes, not dark moody ones); the extracted asset-description data in full (this is your menu of available visuals — read every line, and view directly any asset whose description you don't fully understand before assigning it to a beat); and `techniques.md` (pick 2-3 techniques per beat).

The storyboard is the creative north star — it tells whoever builds the actual video compositions exactly what to build for each beat: mood, camera, animations, transitions, assets, sound. Write it as if you're briefing a motion designer who has never seen the website.

Save as `STORYBOARD.md` in the project directory.

---

## Global direction

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

---

## Asset audit

Before writing any beats, audit every captured asset in a table (Asset / Type / Assign to Beat / Role):

| Asset | Type | Assign to Beat | Role |
|---|---|---|---|
| wave-fallback-desktop.png | Hero image | Beat 1 | Full-bleed animated background |
| enterprise-accordion-hertz.png | Photo | Beat 3 | Enterprise credibility, Ken Burns pan |
| stripe-logo.svg | SVG | Beat 1, Beat 5 | Brand mark opener + closer |
| datavizstatic3x.png | Data viz | Beat 3 | Supporting visual behind stats |
| icon-3.svg | Icon | SKIP | Decorative, too small |

Enforce these minimums:
- At least 50% of product screenshots and hero images must appear somewhere in the video.
- The brand logo must appear in both the first AND the last beat.
- The site's single most signature visual (its gradient wave, hero illustration, or key product UI) must appear — it's the most recognizable brand element and skipping it is a mistake.
- No more than 2 consecutive text-only beats — the 3rd must contain a visual asset.
- The opening beat must contain a visual asset, never text-only.

---

## Per-beat direction fields

Each beat is a WORLD, not a layout. Before writing CSS specs and animation instructions, describe what the viewer EXPERIENCES. The difference between a great storyboard beat and a mediocre one:

**Mediocre:** "Dark navy background. '$1.9T' in white, 280px. Logo top-left. Wave image bottom-right."
**Great:** "Camera is already mid-flight over a vast dark canvas. The gradient wave sweeps across the frame like aurora borealis — alive, shifting. '$1.9T' SLAMS into existence with such force the wave ripples in response. This isn't a slide — it's a moment."

The first describes pixels. The second describes an experience. Write the second, then figure out the pixel-level specifics.

Each beat needs:

### Concept
2-3 sentences on the visual world, the metaphor, and the feeling — write this first, everything else flows from it.

### VO cue
Which narration line plays over this beat.

### Visual description
Written cinematically with camera language (pan, zoom, drift, settle), describing at least 5 distinct visual elements across foreground/midground/background, not just "text + background."

### Mood direction
Cultural/design references rather than hex codes:
- "Geometric, rhythmic, precise — think Josef Albers or Bauhaus color studies."
- "Warm workspace. Nice notebook energy, not technical blueprint."
- "Cinematic title sequence. The kind of opening where you lean forward."

### Assets
The specific captured files to use, referenced by filename:
- "Background: `wave-fallback-desktop.png` — full-bleed, slow zoom 1→1.04 over beat duration"
- "Logo: `svgs/stripe-logo.svg` — centered, fades in at 0.5s"
- "Enterprise photo: `enterprise-accordion-hertz.png` — Ken Burns pan, 70% opacity overlay"

### Animation choreography
A specific motion verb for every element — if you can't name the verb, the element isn't yet designed.

**Motion verb energy levels:**

| Energy | Verbs | Example |
|---|---|---|
| High impact | SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS | "$1.9T" SLAMS in from left at -5° |
| Medium energy | CASCADE, SLIDES, DROPS, FILLS, DRAWS | Three cards CASCADE in staggered 0.3s |
| Low energy | types on, FLOATS, morphs, COUNTS UP, fades in | Counter COUNTS UP from 0 to 135K |

### Transition
How this beat hands off to the next.

**Transition type decision table:**

| Choose a shader transition for | Choose a CSS transition for | Choose a hard cut for |
|---|---|---|
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments | Continuous camera-motion beats where the scene feels like one move broken into cuts | Rapid-fire lists, percussive edits on the beat, comedic timing |
| Any moment the music/VO punctuates with a downbeat or SFX hit | Beats that ease from one composition into the next with shared motion vocabulary | Sequences of 3+ quick tempo-matched switches |
| Brand moments where the transition itself IS the visual | Minimal/editorial pacing | Anytime a 0.3-0.8s transition would feel too slow |

Rule of thumb: shader-transition into the true centerpiece beats of the video; CSS-transition or hard-cut the connective-tissue beats in between. A 5-7 beat brand reel usually wants only 1-2 shader transitions (the hero reveal and the CTA) — too many flattens their impact. If your rendering framework doesn't ship a shader-transition library, use velocity-matched CSS transitions for centerpiece beats instead — the effect is less dramatic but still reads as intentional.

Common CSS transition patterns:
- **Velocity-matched upward**: exit `y:-150, blur:30px, 0.33s power2.in` → entry `y:150→0, blur:30px→0, 1.0s power2.out`
- **Whip pan**: exit `x:-400, blur:24px, 0.3s power3.in` → entry `x:400→0, blur:24px→0, 0.3s power3.out`
- **Blur through**: exit `blur:20px, 0.3s` → entry `blur:20px→0, 0.25s power3.out`
- **Zoom through**: exit `scale:1→1.2, blur:20px, 0.2s power3.in` → entry `scale:0.75→1, blur:20px→0, 0.5s expo.out`
- **Hard cut / smash cut** for rapid-fire sequences

How velocity-matching works: exit the outgoing beat with an accelerating ease curve (power2.in or power3.in) plus a blur ramp, and enter the incoming beat with a decelerating ease curve (power2.out or power3.out) plus a blur clear — matching the exit velocity to the entry velocity within roughly 5% tolerance makes the viewer perceive one continuous camera move rather than two separate animations glued together.

### Depth layers
What's in foreground, midground, and background. Every beat needs at least 2 layers — e.g. "BG: dark navy fill + subtle radial glow. MG: stat cards with drop shadow. FG: brand logo bottom-right."

### SFX cues
What sound plays at what moment — e.g. "On the capture pulse — a soft, warm analog shutter click." / "Left side carries a faint low drone. On fold: drone cuts. Silence. Then a single clean chime."

---

## Three worked example beats

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

---

## Suggested production file layout

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

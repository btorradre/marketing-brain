# Prompt Expansion and Visual Styles

The mandatory prompt-expansion procedure that turns a user's seed prompt into a full per-scene
production spec, plus eight named visual-style starters for mood-to-style routing. See
`../SKILL.md` for when this step runs in the overall workflow.

## Prompt Expansion

Run on every composition beyond a trivial edit. Expansion is not about lengthening a short prompt
— it's about grounding the request against the design spec (`frame.md` or `design.md`) and house
style, and producing a consistent intermediate that every downstream step reads the same way.

Runs after design direction is established (palette/typography/preset chosen). The expansion
consumes the design spec (if present) and produces output that cites its exact values.

### Prerequisites

Read before generating:

- The design spec — `frame.md` → `design.md` → `DESIGN.md` (read the first that exists) — extract
  brand colors, fonts, mood, and constraints. The expansion cites these exact values (hex codes,
  font names); it does not invent new ones.
- `narration-and-story.md` (beat-direction section) — per-beat planning format (concept, mood,
  choreography verbs, transitions, depth layers, rhythm). The expansion outputs each scene using
  this format.
- `composition-rules.md` (video-composition section) — video-medium rules for density, scale, and
  color presence. The expansion applies these automatically.
- `design-system.md` (house-style section) — its rules for Background Layer (2-5 decoratives),
  Color, Motion, Typography apply to every scene. The expansion writes output that conforms to
  them.

If no design spec exists yet, establish one first (see `../SKILL.md` Step 1). Expansion without a
design context produces generic scene breakdowns that later steps ignore.

### Why always run it

The expansion is never pass-through. Every request — no matter how detailed — is a seed. The
expansion's job is to enrich it into a fully-realized per-scene production spec that can be built
from directly.

Even a detailed 7-scene brief lacks things only the expansion adds:

- **Atmosphere layers per scene** (required 2–5 from house style: radial glows, ghost type,
  hairline rules, grain, thematic decoratives) — a request almost never lists these; expansion
  adds them.
- **Secondary motion for every decorative** — breath, drift, pulse, orbit. A decorative without
  ambient motion feels dead.
- **Micro-details that make a scene feel real** — registration marks, tick indicators, monospace
  coord labels, typographic accents, code snippets in the background, grid patterns. Things a
  request didn't think to include.
- **Transition choreography at the object level** — not "crossfade" but "X expands outward and
  becomes Y." Specific duration, ease, and morph source/target.
- **Pacing beats within each scene** — where tension builds, where a hold lets the viewer breathe,
  where the accent word lands.
- **Exact hex values, typography parameters, ease choices** from the design spec — no vagueness
  left to guess at scene-build time.

Expansion's job on a detailed prompt is not to summarize or pass through — it's to take what was
written and make it richer. The original content stays; the atmosphere, ambient motion, and
micro-details are added on top. That's what makes the difference between a scene that matches the
brief and a scene that feels alive.

The quality gap between a single-pass composition and a properly-planned multi-scene composition
comes from this step. Expansion front-loads the richness so every scene gets built from a rich
brief, not a terse one.

**Do not skip. Do not pass through.** Single-scene compositions and trivial edits are the only
exceptions.

### What to generate

Expand into a full production prompt with these sections:

1. **Title + style block** — cite the design spec's exact hex values, font names, and mood. Do NOT
   invent a palette — quote what the design provides.

2. **Rhythm declaration** — name the scene rhythm before detailing any scene. Example:
   `hook-PUNCH-breathe-CTA` or `slow-build-BUILD-PEAK-breathe-CTA`. Use `narration-and-story.md`
   (rhythm planning) for rhythm templates by video type.

3. **Global rules** — parallax layers, micro-motion requirements, transition style, primary +
   accent transitions. Match energy to mood (calm → slow eases, high → snappy eases).

4. **Per-scene beats** — for each scene, use the beat-direction format from
   `narration-and-story.md`:
   - **Concept** — the big idea in 2-3 sentences. What visual WORLD? What metaphor? What should
     the viewer FEEL?
   - **Mood direction** — cultural/design references, not hex codes ("Bauhaus color studies",
     "cinematic title sequence", "editorial calm").
   - **Depth layers** — BG treatment, MG content, and FG accents or structural details as the
     concept needs. Use `composition-rules.md` to choose density; do not force an element count or
     invent content to fill one.
   - **Animation choreography** — specific verbs per element. High: SLAMS, CRASHES. Medium:
     CASCADE, SLIDES. Low: floats, types on, counts up. Every element gets a verb. If the verb
     can't be named, the element is not yet designed.
   - **Transition out** — the transition type and specific parameters, not just "crossfade" but
     "blur crossfade, 0.4s, power2.inOut."

5. **Recurring motifs** — visual threads across scenes from the brand palette.

6. **Negative prompt** — what to avoid, informed by the design spec's constraints if present.

### Output

Write the expanded prompt to a working file in the project directory (e.g.
`.hyperframes/expanded-prompt.md`) rather than dumping it inline — it will be hundreds of lines.
Summarize it briefly ("expanded into N scenes across [duration] seconds with specific visual
elements, transitions, and pacing — review and edit the file, then confirm when ready to proceed")
and only move to construction after it's approved or confirmed.

## Visual Style Library

Eight named visual identities for HyperFrames videos, each grounded in a real graphic-design
tradition and expressed as a design.md-compatible token block. Use these as starters — copy the
YAML into a project's `design.md` frontmatter, then customize.

**How to pick:** match mood first, content second. Ask: "What should the viewer FEEL?"

**How to use:** copy the style's YAML token block into `design.md` frontmatter. Add `## Overview`,
`## Colors`, `## Typography`, `## Elevation`, `## Components`, `## Do's and Don'ts` prose sections
to complete the file.

### Quick Reference

| Style             | Mood                    | Best for                            | Transition character              |
| ------------------- | ------------------------- | -------------------------------------- | -------------------------------------- |
| Swiss Pulse          | Clinical, precise          | SaaS, data, dev tools, metrics          | Cinematic zoom or iris reveal           |
| Velvet Standard      | Premium, timeless          | Luxury, enterprise, keynotes            | Cross-warp morph                        |
| Deconstructed        | Industrial, raw            | Tech launches, security, punk            | Glitch or whip pan                      |
| Maximalist Type      | Loud, kinetic              | Big announcements, launches             | Ridged burn                             |
| Data Drift           | Futuristic, immersive      | AI, ML, cutting-edge tech               | Gravitational lens or domain warp       |
| Soft Signal          | Intimate, warm             | Wellness, personal stories, brand       | Thermal distortion                      |
| Folk Frequency       | Cultural, vivid            | Consumer apps, food, communities         | Swirl vortex or ripple waves            |
| Shadow Cut           | Dark, cinematic            | Dramatic reveals, security, exposé       | Domain warp                             |

### 1. Swiss Pulse — Josef Müller-Brockmann

**Mood:** Clinical, precise | **Best for:** SaaS dashboards, developer tools, APIs, metrics

```yaml
name: Swiss Pulse
colors:
  primary: "#1a1a1a"
  on-primary: "#ffffff"
  accent: "#0066FF"
typography:
  headline:
    fontFamily: Helvetica Neue
    fontSize: 5rem
    fontWeight: 700
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
  stat:
    fontFamily: Helvetica Neue
    fontSize: 7rem
    fontWeight: 700
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "power4.in"
    ambient: "none"
  duration:
    entrance: 0.4
    hold: 1.5
    transition: 0.6
  atmosphere:
    - grid-lines
    - registration-marks
  transition: cinematic-zoom
```

Grid-locked compositions. Every element snaps to an invisible 12-column grid. Numbers dominate the
frame at 80–120px. Animated counters count up from 0. Hard cuts, no decorative transitions. Nothing
floats.

### 2. Velvet Standard — Massimo Vignelli

**Mood:** Premium, timeless | **Best for:** Luxury products, enterprise software, keynotes,
investor decks

```yaml
name: Velvet Standard
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent: "#1a237e"
typography:
  headline:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 300
    letterSpacing: 0.15em
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.6
rounded:
  sm: 0px
  md: 2px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.in"
    ambient: "sine.inOut"
  duration:
    entrance: 1.2
    hold: 3.0
    transition: 1.5
  atmosphere:
    - subtle-grain
    - hairline-rules
  transition: cross-warp-morph
```

Generous negative space. Symmetrical, centered, architectural precision. Thin sans-serif, ALL CAPS,
wide letter-spacing. Sequential reveals with long holds. Nothing snaps — everything glides with
intention. Luxury takes its time.

### 3. Deconstructed — Neville Brody

**Mood:** Industrial, raw | **Best for:** Tech news, developer launches, security products,
punk-energy reveals

```yaml
name: Deconstructed
colors:
  primary: "#1a1a1a"
  on-primary: "#f0f0f0"
  accent: "#D4501E"
typography:
  headline:
    fontFamily: Space Grotesk
    fontSize: 4rem
    fontWeight: 700
  label:
    fontFamily: Space Mono
    fontSize: 0.75rem
    fontWeight: 700
    textTransform: uppercase
rounded:
  none: 0px
spacing:
  sm: 4px
  md: 12px
  lg: 24px
motion:
  energy: high
  easing:
    entry: "back.out(2.5)"
    exit: "steps(8)"
    ambient: "elastic.out(1.2, 0.4)"
  duration:
    entrance: 0.3
    hold: 1.0
    transition: 0.5
  atmosphere:
    - scan-lines
    - glitch-artifacts
    - grain-overlay
  transition: glitch
```

Type at angles, overlapping edges, escaping frames. Bold industrial weight. Gritty textures:
scan-line effects, glitch artifacts baked into design. Text SLAMS and SHATTERS. Letters scramble
then snap to final position. Intentional irregularity — nothing should feel polished.

### 4. Maximalist Type — Paula Scher

**Mood:** Loud, kinetic | **Best for:** Big product launches, milestone announcements, high-energy
hype videos

```yaml
name: Maximalist Type
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent-red: "#E63946"
  accent-yellow: "#FFD60A"
typography:
  headline:
    fontFamily: Anton
    fontSize: 8rem
    fontWeight: 400
    textTransform: uppercase
  subhead:
    fontFamily: Space Grotesk
    fontSize: 3rem
    fontWeight: 700
rounded:
  none: 0px
spacing:
  sm: 0px
  md: 8px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "back.out(1.8)"
    ambient: "power3.out"
  duration:
    entrance: 0.3
    hold: 0.8
    transition: 0.4
  atmosphere:
    - type-layers
    - color-blocks
  transition: ridged-burn
```

Text IS the visual. Overlapping type layers at different scales and angles, filling 50–80% of
frame. Bold saturated colors — maximum contrast. Everything kinetic: slamming, sliding, scaling.
2–3 second rapid-fire scenes. No static moments. Fast arrivals, hard stops.

### 5. Data Drift — Refik Anadol

**Mood:** Futuristic, immersive | **Best for:** AI products, ML platforms, data companies,
speculative tech

```yaml
name: Data Drift
colors:
  primary: "#0a0a0a"
  on-primary: "#e0e0e0"
  accent-purple: "#7c3aed"
  accent-cyan: "#06b6d4"
typography:
  headline:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 200
    letterSpacing: 0.05em
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 300
rounded:
  sm: 4px
  md: 12px
  full: 9999px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: moderate
  easing:
    entry: "sine.inOut"
    exit: "power2.out"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 2.5
    transition: 1.5
  atmosphere:
    - particle-field
    - light-traces
    - radial-glow
  transition: gravitational-lens
```

Thin futuristic sans-serif — floating, weightless, minimal. Fluid morphing compositions. Extreme
scale shifts (micro → macro). Particles coalesce into numbers. Light traces data paths through the
frame. Smooth, continuous, organic. Nothing hard.

### 6. Soft Signal — Stefan Sagmeister

**Mood:** Intimate, warm | **Best for:** Wellness brands, personal stories, lifestyle products,
human-centered apps

```yaml
name: Soft Signal
colors:
  primary: "#FFF8EC"
  on-primary: "#2a2a2a"
  accent-amber: "#F5A623"
  accent-rose: "#C4A3A3"
  accent-sage: "#8FAF8C"
typography:
  headline:
    fontFamily: Playfair Display
    fontSize: 3rem
    fontWeight: 400
    fontStyle: italic
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.7
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  sm: 12px
  md: 24px
  lg: 48px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.inOut"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 3.0
    transition: 1.5
  atmosphere:
    - soft-gradient
    - warm-grain
  transition: thermal-distortion
```

Handwritten-style or humanist serif fonts. Personal, lowercase, delicate. Close-up framing: single
element fills the frame. Slow drifts and floats, never snaps. Soft organic motion. Nothing should
feel hurried or polished. Intimate, never corporate.

### 7. Folk Frequency — Eduardo Terrazas

**Mood:** Cultural, vivid | **Best for:** Consumer apps, food platforms, community products,
festive launches

```yaml
name: Folk Frequency
colors:
  primary: "#ffffff"
  on-primary: "#1a1a1a"
  accent-pink: "#FF1493"
  accent-blue: "#0047AB"
  accent-yellow: "#FFE000"
  accent-green: "#009B77"
typography:
  headline:
    fontFamily: Fredoka One
    fontSize: 4rem
    fontWeight: 400
  body:
    fontFamily: Nunito
    fontSize: 1rem
    fontWeight: 600
rounded:
  sm: 8px
  md: 16px
  lg: 32px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "back.out(1.6)"
    exit: "elastic.out(1, 0.5)"
    ambient: "sine.inOut"
  duration:
    entrance: 0.5
    hold: 1.5
    transition: 0.8
  atmosphere:
    - pattern-tiles
    - confetti-burst
    - color-blocks
  transition: swirl-vortex
```

Bold warm rounded type. Pattern and repetition — folk art rhythm and density. Layered compositions
with rich visual texture. Every frame feels handcrafted. Colorful motion: elements bounce, pop,
spin into place with joy. Overshoots feel intentional. Celebratory energy.

### 8. Shadow Cut — Hans Hillmann

**Mood:** Dark, cinematic | **Best for:** Security products, dramatic reveals, investigative
content, intense launches

```yaml
name: Shadow Cut
colors:
  primary: "#0a0a0a"
  on-primary: "#f0f0f0"
  surface: "#3a3a3a"
  accent: "#C1121F"
typography:
  headline:
    fontFamily: Oswald
    fontSize: 4rem
    fontWeight: 700
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 48px
motion:
  energy: moderate
  easing:
    entry: "power3.out"
    exit: "power4.in"
    ambient: "sine.inOut"
  duration:
    entrance: 0.8
    hold: 2.5
    transition: 1.2
  atmosphere:
    - deep-shadow
    - vignette
    - grain-overlay
  transition: domain-warp
```

Near-monochrome: deep blacks, cold greys, stark white + one blood accent. Sharp angular text like
film noir title cards. Heavy contrast, no softness. Elements emerge from darkness — reveal is the
narrative. Slow creeping push-ins, dramatic scale reveals. The pause before the hit matters. The
domain-warp transition dissolves reality before the next scene.

### Mood → Style Guide

| If the content feels...              | Use...            |
| ---------------------------------------- | ------------------- |
| Data-driven, analytical, technical         | Swiss Pulse           |
| Premium, enterprise, luxury                 | Velvet Standard       |
| Raw, punk, aggressive, rebellious           | Deconstructed          |
| Hype, loud, high-energy launch              | Maximalist Type        |
| AI, ML, speculative, futuristic             | Data Drift             |
| Human, warm, personal, wellness              | Soft Signal            |
| Cultural, fun, consumer, festive             | Folk Frequency          |
| Dark, dramatic, intense, cinematic           | Shadow Cut               |

### Creating Custom Styles

These 8 styles are starters — not constraints. Create new ones:

1. **Name it** after a designer, art movement, or cultural reference.
2. **Write YAML tokens** — `colors` (2–5 tokens), `typography` (2–3 scales), `rounded`, `spacing`,
   `motion` (energy + easing + duration + atmosphere + transition).
3. **Add prose** — one paragraph describing the feel, what to do, what to avoid.
4. **Token references** — use `{colors.accent}`, `{typography.headline}` in component definitions.

The pattern: YAML tokens (what) → prose rationale (why) → components (how they combine).

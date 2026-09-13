# Frame Presets (1 of 2)

Thirteen ready-made, fully-specified visual identities for HyperFrames video projects, split
across this file and `frame-presets-2.md` for size. Each preset is a video-first "frame.md"
companion design system — the unit is the 1920×1080 frame, not a slide in a deck. Adopting one
means treating its colors, typography, component specs, and per-frame-type composition recipes as
locked brand truth; composition (which recipe to use where) stays free.

This file covers: **cartesian, creative-mode, coral, biennale-yellow, daisy-days, cobalt-grid,
capsule**. See `frame-presets-2.md` for: claude, editorial-forest, blockframe, blue-professional,
broadside, bold-poster.

Every preset shares the same structural contract, described once here instead of per-preset:

- **Frontmatter is normative** — `colors`, `typography`, `spacing`, `components` are the real,
  machine-readable values. Quote them verbatim; never invent or round them.
- **The container law** — every frame ground sets `container-type: size`; all frame-relative units
  are `cqw`/`cqh` (percent of frame width/height) resolved against it, never `vw`/`vh`. This is
  what keeps a preset's proportions correct at any render size.
- **Motion is intentionally out of scope** in every preset below — these are composition-only
  specs. Motion and transition choreography belong to the animation-focused part of the pipeline
  (see `../SKILL.md`).
- **Numerals & Claims hard rule** — never invent figures, dates, or counts when applying a preset;
  render data slots as placeholders (`— figure —`, `{metric}`) until the actual script/brief
  supplies real values.
- **Aspect ratios** — 1920×1080 (16:9) is primary; 1080×1920 (9:16) and 1080×1080 (1:1) are
  documented per preset as guidance, not pixel-locked.

Each preset below is reproduced in full: its YAML frontmatter (colors, typography, spacing,
components), followed by its complete prose spec (overview, frame craft bar, colors, typography,
depth, shapes, components, six frame-type treatments, composition do/don't rules, aspect-ratio
table, approved entities, numerals rule, pre-render self-audit, and known gaps/font-loading notes).

---

## Preset: Cartesian

```yaml
version: alpha
name: Cartesian — Frame (video / frame layer)
description: >
  Video-first companion to Cartesian's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the five-tone warm-stone palette, Playfair Display 400 + Inter, the
  universal 1px taupe hairline as the only structural device, compass-drafted geometric rings,
  and zero shadow / zero fill. Composition, frame scale, and aspect-ratio behavior are rewritten
  for the frame. Restraint is the rule; motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg-primary: "#EDE8E0"
  bg-secondary: "#E2DBD1"
  text-primary: "#1A1A1A"
  text-secondary: "#5A5A5A"
  accent: "#8A8178"
  line: "#B8B0A4"
  white-overlay: "rgba(255,255,255,0.3)"

typography:
  # — reading ramp (Inter) —
  body:        { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.6, color: "text-secondary" }
  body-sm:     { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:    { fontFamily: "Inter", cqw: 1.3,  weight: 400, lineHeight: 1.5 }
  label:       { fontFamily: "Inter", px: 14, weight: 500, tracking: "3px", upper: true, color: "accent" }
  attribution: { fontFamily: "Inter", px: 15, weight: 400, tracking: "2px", upper: true, color: "accent" }
  micro:       { fontFamily: "Inter", px: 12, weight: 400, tracking: "2px", upper: true, color: "accent" }
  # — display / hero ramp (Playfair Display 400, sentence case) —
  h3:          { fontFamily: "Playfair Display", cqw: 1.8, weight: 400, lineHeight: 1.1 }
  timeline-headline:{ fontFamily: "Playfair Display", cqw: 1.9, weight: 400, lineHeight: 1.1 }
  card-headline:{ fontFamily: "Playfair Display", cqw: 2.0, weight: 400, lineHeight: 1.15 }
  stat-figure: { fontFamily: "Playfair Display", cqw: 3.0, weight: 400, lineHeight: 1.0 }
  quote-mark:  { fontFamily: "Playfair Display", cqw: 9.0, weight: 400, lineHeight: 0.5, color: "line" }
  h2:          { fontFamily: "Playfair Display", cqw: 4.0, weight: 400, lineHeight: 1.1 }
  h1:          { fontFamily: "Playfair Display", cqw: 6.2, weight: 400, lineHeight: 1.06 }
  display:     { fontFamily: "Playfair Display", cqw: 8.0, weight: 400, lineHeight: 1.04 }

spacing:
  pad-x: "7cqw"
  pad-y: "5cqw"
  gap-xl: "6cqw"
  gap-lg: "5cqw"

components:
  hairline:
    rule: "0.07cqw solid {colors.line}"
    description: "The universal structural device — every separator (agenda rule, timeline connector, card border, stats top) is this 1px taupe line. No thick borders exist."
  card:
    backgroundColor: "{colors.white-overlay}"
    border: "0.07cqw solid {colors.line}"
    rounded: "0"
    shadow: "none"
    description: "Faint white-overlay fill (canvas bleeds through) is what makes a card distinct from a bare region."
  card-icon:
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    size: "40px circle"
    textColor: "{colors.accent}"
    typography: "Playfair numeral/letter"
    description: "Ringed circle mark."
  agenda-row:
    borderBottom: "0.07cqw solid {colors.line}"
    typography: "{typography.h3} (numeral {colors.accent}, label {colors.text-primary})"
    description: "Numeral left, label right over a taupe rule."
  timeline:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.timeline-headline} + {typography.body-sm}"
    description: "A single taupe top rule across items — no nodes, no dots."
  stats-cluster:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.stat-figure} + uppercase {colors.accent} labels"
    description: "Inline modest stat figures (no hero numeral)."
  geo-ring:
    border: "1px solid {colors.line} (inner dashed ::before ~70–80%)"
    rounded: "50%"
    size: "10–50cqw"
    opacity: "0.2–0.5"
    description: "Compass-construction rings behind content. 1–2 per frame, never more."
  horizontal-accent:
    backgroundColor: "{colors.text-primary}"
    size: "~18cqw × 1px"
    description: "The system's only INK-BLACK rule — a strong terminal accent on cover/closing, sparingly."
  vertical-line:
    backgroundColor: "{colors.line}"
    size: "1px × full height, ~5cqw from edge"
    opacity: "0.3–0.4"
    description: "Drafting-paper alignment guide. Optional."
  image-placeholder:
    backgroundColor: "{colors.bg-secondary}"
    mark: "crossed +30°/−30° 1px taupe diagonals (an X)"
    typography: "small uppercase {typography.micro}"
    description: "The signature image-not-wired mark."
  team-photo:
    backgroundColor: "{colors.bg-secondary}"
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    typography: "Playfair initial in {colors.accent}"
    description: "Circular portrait frame."
```

### Overview

Cartesian at frame scale is a **quiet museum-catalog editorial system** — restraint through 1px
lines. Every structural separator is a single 1px taupe hairline; there are no thick borders, no
fills (save the faint white-overlay card), no shadows, no rounded rectangles. Hierarchy comes from
**type contrast and negative space**, and atmosphere from **compass-drafted geometric rings**
drifting behind content.

The voice is a literary pairing: **Playfair Display** at weight 400 (the thin-stroke didone, never
bold, always sentence case) carries every headline, numeral, and quote mark in ink; **Inter**
carries body in warm gray and labels in uppercase taupe with 2–3px tracking. The palette is five
warm stones plus ink — no populist accent color exists. The correct density is **sparse and
breathing**: one clear idea, well-framed, on stone paper.

**Key characteristics at frame scale:**

- **1px taupe hairline** as the universal structural device — every separator is this one line.
- **Playfair Display 400** (ink, sentence case) for display; **Inter** body (gray) + labels (taupe, tracked).
- **Five warm stones + ink** — no red/blue/green; the only "color" is type contrast.
- **Compass-drafted geometric rings** (solid + dashed, 20–50% opacity) behind content for mood.
- **Flat** — zero shadow, zero rounded rectangle (circles only); the lone ink line is the `horizontal-accent`.
- **Sparse and breathing** — generous negative space; crowding reads as broken.

### The Frame

**Frame Craft Bar** — three eyeball tests gate every frame before any structural check:

- **Squint** — one Playfair element dominates at **3–6× its nearest neighbor**; the serif/sans + size contrast carries hierarchy, not weight.
- **Silence** — declarative frames read **55–60% empty**; Cartesian has **no dense frame** — even the agenda/index breathes (the system breaks when crowded).
- **Restraint** — **at most two geo rings** per frame; the single INK-BLACK `horizontal-accent` rule used sparingly; no populist accent color ever.
- **Reference** — aim at a **Vignelli editorial / Cooper Hewitt catalogue / pencil-and-tracing-paper plan**; failure looks like a **shadowed, rounded-card SaaS deck**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x` (7cqw) generous gutters; geometry may bleed off an edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. The 1px hairlines and geo rings hold
their proportion against the frame at any render size.

### Colors

Tokens identical to the source. `{colors.bg-primary}` is the ground; `{colors.text-primary}` ink is
headlines and the one black accent rule; `{colors.text-secondary}` gray is body; `{colors.accent}`
taupe is labels, numerals, small text; `{colors.line}` taupe is every 1px structural border.
`{colors.bg-secondary}` is the only secondary fill (placeholders, photo frames). **No populist
accent** — when emphasis is needed, grow the type, switch sans→serif, or add a single
`horizontal-accent` ink line. Headlines are never taupe; small text is never ink.

### Typography

Two ramps. The **reading ramp** (Inter body 1.0cqw gray, labels in px taupe) carries copy + chrome;
the **display ramp** (Playfair `h3` 1.8cqw → `display` 8.0cqw, all weight 400) carries every headline.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`/`h1`; 4–6 → `h2`; 7+ → `h3`. Cartesian has no hero-stat numeral — stats stay modest (`stat-figure` 3cqw).
- **Playfair at 400, ink, sentence case** — never bold, never uppercase, never taupe. **Inter labels uppercase, 2–3px tracked, taupe.** Italic via Playfair italic for emphasis only.

### Depth & Surface

The flat plane is the only technique. Hierarchy from:

- **Type contrast** — Playfair serif vs Inter sans; the 8cqw→0.7cqw scale.
- **1px taupe hairlines** — every divider, card outline, timeline rule, photo ring.
- **Tone** — ink vs gray vs taupe.
- **Negative space** — generous padding.
- **Geometric atmosphere** — compass rings that suggest depth without creating it.

**Ceiling:** no box-shadow, no elevated card, no gradient, no rounded rectangle. The single ink line
(`horizontal-accent`) is the only non-taupe rule.

### Shapes

- **50% (circle)** — card-icon, team-photo, nav-dot, every geo ring.
- **0** — everything else; soft-rounded corners do not exist.

### Components

- **hairline** — the universal 1px taupe separator (the identity).
- **card** (1px taupe + white-overlay) / **card-icon** (ringed circle) / **agenda-row** / **timeline** (line, no nodes) / **stats-cluster** — all built on the hairline.
- **geo-ring** — compass decoration (solid + dashed), 1–2 per frame. **horizontal-accent** — the one ink line, sparingly. **vertical-line** — drafting guide.
- **image-placeholder** (crossed-X) / **team-photo** (ringed initial) — the stone-fill placeholders.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Every frame is sparse and breathing; 1–2 geo decorations max.

**1 · Cover** (identity · move: serif + compass ring · left). **Ground** `{colors.bg-primary}`, `pad-x`. **Composes** geo-ring (right, ~34cqw, solid+dashed), vertical-line (left), label, display/h1. **Focal** a 2–3 line Playfair `display`/`h1` headline in ink (italic on the key word), left-anchored, with a taupe `label` above and an Inter subtitle below. **Chrome** optional bottom meta row (Playfair value + taupe label). **Accent** the geo ring; optionally one `horizontal-accent` ink line (if it clears the meta). **Silence** ~55% empty. **Fixed** Playfair 400 ink sentence-case, ≤2 geo elements, 1px lines. **Free** title, ring placement, meta. **Density** sparse.

**2 · Agenda / Index** (index · move: hairline list · left). **Ground** `{colors.bg-primary}`, `pad-x`. **Composes** label, h2, agenda-rows. **Focal** a Playfair `h2` over 4–6 agenda rows (Playfair numeral in taupe + Playfair label in ink), each on a 1px taupe rule. **Chrome** taupe `label` eyebrow. **Accent** none — taupe numerals carry it. **Silence** moderate; rows generously spaced. **Fixed** 1px taupe rules, Playfair 400. **Free** items, count. **Density** standard (sparse rows).

**3 · Pull Quote** (quote · move: centered statement · compass ring). **Ground** `{colors.bg-primary}`, centered. **Composes** geo-ring (centered dashed, ~26cqw), quote-mark, h2/display-quote, attribution. **Focal** a 2-line Playfair quote in ink, centered, under a 50%-taupe Playfair quote-mark; a taupe uppercase attribution beneath. **Accent** the faint centered ring. **Silence** ~60% — deliberately open. **Fixed** Playfair 400, one ring, centered. **Free** quote, attribution. **Density** sparse.

**4 · Closing Plate** (closer · move: centered ring · centered). **Ground** `{colors.bg-primary}`, centered. **Composes** geo-ring (centered, ~40cqw, solid+dashed), label, h1/display, horizontal-accent. **Focal** a 1–2 line Playfair sign-off in ink (italic key word), centered inside the largest compass ring; a short ink `horizontal-accent` beneath. **Accent** the ring + the one ink line. **Silence** ~60%. **Fixed** Playfair 400, centered, ≤2 geo. **Free** sign-off, ring scale. **Density** sparse.

**5 · Two-Column Editorial** (content · move: asymmetric split · left). **Ground** `{colors.bg-primary}`, `pad-x`, two columns with `gap-xl`. **Composes** label, h2, body, image-placeholder (crossed-X) or card. **Focal** a Playfair `h2` + Inter body in the text column; an image-placeholder or card in the other. **Accent** none. **Silence** generous gutter. **Fixed** 1px taupe card/placeholder borders, white-overlay fill. **Free** which side is text, body copy. **Density** standard.

**6 · Stats / Timeline** (data · move: hairline rail · left). **Ground** `{colors.bg-primary}`, `pad-x`. **Composes** label, h3, stats-cluster or timeline. **Focal** a modest Playfair stat row (or a 1px-rule timeline with year + headline + body, no nodes), framed by a 1px taupe top rule. **Accent** none. **Silence** moderate. **Fixed** modest stat scale, hairline rule, no nodes. **Free** figures, phases. **Density** standard.

### Composition Rules

**Do:** use a single 1px taupe line for every separator (the identity); set every Playfair headline at 400, ink, sentence case; render labels taupe, uppercase, 2–3px tracked; layer one or two compass rings (20–50% opacity) behind content for atmosphere; let frames breathe (55–60% empty on declarative frames); lean centered on quote/closer, asymmetric/left on cover/agenda/editorial; use `bg-secondary` for placeholder fills.

**Don't:** introduce a populist accent color (stone and ink only); bold Playfair, render headlines in taupe, or use thick (2px+) borders; add shadows, elevated cards, or rounded rectangles (circles only); crowd the frame; use more than two geo decorations per frame; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment            | 16:9                       | 9:16                                 | 1:1                          |
| --------------------- | --------------------------- | ------------------------------------ | ---------------------------- |
| Cover                 | headline left, ring right   | headline top, ring below             | headline upper, ring behind  |
| Agenda / Index        | h2 + rows                   | h2 + rows (tighter)                  | h2 + rows                    |
| Pull Quote            | centered, ring behind       | centered, taller                     | centered                     |
| Closing Plate         | centered in ring            | centered, ring scaled                | centered                     |
| Two-Column Editorial  | text + visual side-by-side  | stacked (collapse)                   | stacked                      |
| Stats / Timeline      | horizontal rail             | vertical stack (drop timeline rule)  | compact                      |

Generous `pad-x` holds on the short edge; re-step display per ratio above the 1.4cqw floor. On
9:16, the timeline rule loses meaning when stacked — switch to a vertical list.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder (the crossed-X image-placeholder, or a ringed initial for portraits).

### Numerals & Claims (hard rule)

Never invent figures, dates, or counts at frame scale. Render slots as `— figure —`, `{metric}`.
Stats and timeline years carry placeholders until the script supplies them. Agenda ordinals
(01, 02…) are decorative and may be sequential.

### Pre-Render Self-Audit

- **Squint** — one Playfair element dominates; the serif/sans contrast carries hierarchy.
- **Silence** — declarative frames 55–60% empty; nothing is crowded.
- **Palette** — five stones + ink only; no populist accent; headlines ink, labels taupe.
- **Lines** — every separator is a 1px taupe hairline; the only ink line is `horizontal-accent`.
- **Type** — Playfair 400 sentence-case, fit-to-measure; labels uppercase 2–3px; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded rectangle; ≤2 geo rings per frame.
- **Anchor** — centered on quote/closer, left/asymmetric on cover/agenda/editorial; no 3 in a row alike.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope. The 0.6s fade in the source is a deck mechanic.
- Playfair Display + Inter via Google Fonts. CJK pairing (Noto Serif SC 700/400) carries over;
  Playfair has no Hanzi italic — substitute weight/taupe for emphasis.
- 9:16 / 1:1 are guidance; verify the legibility floor and that the timeline collapses to a
  vertical list.
- Geo rings, the crossed-X placeholder, and the dashed inner ring are CSS-only; no external
  imagery is required.

---

## Preset: Creative Mode

```yaml
version: alpha
name: Creative Mode — Frame (video / frame layer)
description: >
  Video-first companion to Creative Mode's design.md. The unit is the frame (1920×1080),
  not the slide-in-a-deck. Atoms are identical and sacred — warm cream canvas, 4px ink
  borders, hard offset shadows (no blur), Archivo Black uppercase at 0.92 line-height,
  JetBrains Mono taxonomy, Space Grotesk body, the four-accent palette. Composition,
  frame scale, and aspect-ratio behavior are rewritten for the frame. Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#EFE9D9"
  cream-2: "#E4DCC4"
  ink: "#0F0F0F"
  ink-2: "#2A2A2A"
  green: "#1F8A4C"
  green-dark: "#136636"
  pink: "#F06CA8"
  pink-dark: "#D14E8B"
  orange: "#E85A1F"
  yellow: "#F5C518"

typography:
  # — reading ramp (px @ 1920, with cqw) —
  body-lg:    { fontFamily: "Space Grotesk", px: 28, cqw: 1.46, weight: 400, lineHeight: 1.4 }
  body-md:    { fontFamily: "Space Grotesk", px: 24, cqw: 1.25, weight: 400, lineHeight: 1.3 }
  mono-label: { fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.06em", upper: true }
  mono-kicker:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.14em", upper: true }
  table-head: { fontFamily: "Archivo Black", px: 28, cqw: 1.46, weight: 400, upper: true }
  # — display / hero ramp (frame-native, cqw-first) —
  step-title: { fontFamily: "Archivo Black", px: 34,  cqw: 1.77, weight: 400, lineHeight: 1.0, upper: true }
  badge-label:{ fontFamily: "Archivo Black", px: 28,  cqw: 1.46, weight: 400, upper: true }
  marker:     { fontFamily: "Archivo Black", cqw: 2.4, weight: 400, lineHeight: 1.0, upper: true }
  stamp-num:  { fontFamily: "Archivo Black", cqw: 2.2, weight: 400, lineHeight: 0.9 }
  stat-num:   { fontFamily: "Archivo Black", cqw: 6.4, weight: 400, lineHeight: 0.88 }
  step-num:   { fontFamily: "Archivo Black", cqw: 7.0, weight: 400, lineHeight: 0.85 }
  display-head: { fontFamily: "Archivo Black", cqw: 4.2, weight: 400, lineHeight: 0.92, tracking: "-0.01em", upper: true }
  display-lg: { fontFamily: "Archivo Black", cqw: 8.0,  weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-xl: { fontFamily: "Archivo Black", cqw: 11.0, weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-hero:{ fontFamily: "Archivo Black", cqw: 15.5,weight: 400, lineHeight: 0.84, tracking: "-0.02em", upper: true }

spacing:
  frame-pad: "3.3cqw"        # 64px chrome gutter @1920
  content-gutter: "5cqw"     # 96px content gutter @1920
  grid-gap: "1.5cqw"         # 28px
  cell-pad: "1.7cqw"         # 32px

components:
  frame-chrome:
    typography: "{typography.mono-label}"
    placement: "topbar 2.5cqw from top, meta 2.5cqw from bottom, both inset {spacing.frame-pad}"
    rounded: "0"
    shadow: "none"
    description: "Mono topbar (section label left + 999px ink-stroked pill right) + meta footer (descriptor left + NN • NN counter right, 0.5cqw ink dot divider). Present on most frames."
  stat-cell:
    backgroundColor: "{colors.green} · {colors.pink} · {colors.orange} · {colors.cream}"
    textColor: "{colors.cream} on accent · {colors.ink} on cream"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.stat-num} + {typography.mono-label}"
    shadow: "none"
    description: "Flat accent/cream stat tile, square corners, no shadow."
  step-card:
    backgroundColor: "{colors.cream} · {colors.pink} · {colors.yellow} · {colors.green}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.step-num} + {typography.step-title} + {typography.body-md}"
    shadow: "none"
    description: "Ink-bordered card; giant step-num top. Sequence alternates cream with accents and ENDS on green."
  marker-block:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.ink}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.marker}"
    shadow: "1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}"
    description: "The one hard-offset featured callout per frame."
  kicker-block:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.mono-kicker}"
    padding: "0.5cqw 1cqw"
    rounded: "0"
    description: "Inverted eyebrow chip."
  badge-rotated:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    typography: "{typography.badge-label}"
    rounded: "0"
    transform: "rotate(-4deg)"
    description: "Deliberate-imperfection annotation."
  pill-badge:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.ink}"
    rounded: "999px"
    typography: "{typography.mono-label}"
    description: "The ONLY rounded element; reads as a chip, not a card."
  stamp:
    backgroundColor: "{colors.pink}"
    border: "0.4cqw solid {colors.cream}"
    size: "~18cqw square"
    rounded: "0"
    transform: "rotate(-6deg)"
    typography: "{typography.stamp-num}"
    description: "Closing seal with a cream circular inner ring."
  comparison-table:
    backgroundColor: "{colors.cream-2}"
    border: "0.4cqw solid {colors.ink}"
    rule: "0.3cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.table-head} + {typography.body-md}"
    shadow: "none"
    description: "Ink head row with cream Archivo labels; pink/green column-fill variants."
  decorative-circle:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "50%"
    description: "Decorative figure; pairs with a green panel for shape contrast."
```

### Overview

Creative Mode at frame scale is a **neo-brutalist editorial poster in motion's clothing** — warm
cream paper, near-black ink, and four accents that collide at full saturation. Every frame is one
flat color-blocked composition: no gradients, no blurred shadows, no rounded cards (save the one
pill chip). Depth is **hard offset shadow** (a solid same-direction duplicate) or **color-block
contrast**, never light.

The display voice is **Archivo Black in strict uppercase at 0.92 line-height** — letters overlap
their own cap height; that tightness is the brand. **JetBrains Mono** carries every label, kicker,
counter, and axis as a "technical artifact" register. **Space Grotesk** carries the few body lines.
The frame is loud by construction and calm by restraint: two or three accents per frame, the green
ground reserved for a single closing plate, the hard shadow spent on one featured element only.

**Key characteristics at frame scale:**

- **Cream ground** (`{colors.cream}`) on nearly every frame; `{colors.green}` reserved for the closing plate.
- **0.4cqw (4px @1920) ink borders** on every structural element; 0.3cqw internal rules.
- **Hard offset shadow** (≈1.25cqw, orange+ink) on one featured block per frame — never blurred.
- **Archivo Black uppercase**, 0.92 line-height, always; sentence-case Archivo Black does not exist.
- **Two or three accents per frame**, never all four; collisions are the design.
- **One pill chip** (999px) per frame as the sole rounded element.

### The Frame

**Frame Craft Bar:**

- **Squint** — exactly one element dominates, at **3–6× its nearest neighbor** (a chasm, not a ramp): the `display-hero`/`display-xl` claim or the `stat-num` figure, never two rival headlines.
- **Silence** — sparse frames (cover, claim, closer) read **45–60% empty**; the **stat grid and comparison ledger are the one dense exception**. Never fill a sparse frame to look complete.
- **Restraint** — the scarce gestures fire **once per frame**: at most one hard-offset shadow, two-to-three accents (never all four), the green ground reserved for the single closing plate.
- **Reference** — aim at a **Risograph editorial poster / punk-zine spread**; failure looks like a **rounded, soft-shadowed SaaS feature grid**.

- **Primary:** 1920×1080 (16:9). All display sizes authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** chrome at `3.3cqw` (64px) inset; content at `5cqw` (96px) gutter. No load-bearing element crosses the `3.3cqw` line.

**The container law (load-bearing).** Every frame ground sets `container-type: size`. ALL
frame-relative units are `cqw`/`cqh` (1cqw = 1% of the frame's width), resolved against that
ground — **never `vw`.** `vw` measures the page viewport, so a frame inflates whenever it isn't
rendered full-screen; `cqw` resolves against the frame at any render size.

### Colors

Tokens identical to the source. At frame scale: `{colors.cream}` is the **ground**, `{colors.ink}`
is borders + type, and the four accents (`green` / `pink` / `orange` / `yellow`) are **flat fills
rationed two-to-three per frame.** `{colors.orange}` is also the hard-shadow color. `{colors.green}`
doubles as the single closing-plate ground — its rarity is the impact. Never introduce a fifth
accent; never use pure white; never gradient.

### Typography

Two ramps. The **reading ramp** (body, mono labels, table heads) holds px+cqw for chrome and copy.
The **display/hero ramp** is frame-native and authored in `cqw` — from `display-head` (4.2cqw) up
to `display-hero` (15.5cqw) for a wordmark cover.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw (≈27px@1920)**. Mono chrome at 1.15cqw is colophon only.
- **Fit-to-measure:** a headline's size tracks its line length. Cap the headline block at **≤ 78cqw** and never touch the safe margin. ≤3 words → `display-hero`/`display-xl`; 4–6 words → `display-lg`; 7+ words → `display-head`. Short lines go big; long lines step down.
- **Uppercase + 0.92 line-height on all Archivo Black**, always. Mono carries 0.06–0.14em tracking. Never letter-space Archivo Black beyond the encoded −0.01em; never set body centered.

### Depth & Surface

Zero blur. Two depth devices only:

- **Hard offset shadow** — a solid duplicate offset ≈1.25cqw in X and Y (`box-shadow: 1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}`). **One featured block per frame** (marker, stamp). Diagram stacks may use a 0.95cqw ink-only offset.
- **Color-block contrast** — cream on cream-2, ink on cream, accent on cream. No shadow needed when contrast carries.

**Ceiling:** no blurred shadow, no gradient, no glow, anywhere.

### Shapes

- **0 radius** on every structural element — stat cells, step cards, table cells, markers, panels.
- **50%** on decorative circles, stamp inner ring, the meta dot.
- **999px** on the topbar pill chip only — the single rounded exception.
- **Rotation** only at the fixed brand angles: badge −4deg, stamp −6deg.

### Components

- **frame-chrome** — the mono topbar + meta footer. Present on most frames; dropped only on a pure full-bleed wordmark beat if it competes.
- **stat-cell / step-card** — ink-bordered flat-fill blocks; step sequences end on green.
- **marker-block** — the one hard-shadow featured callout per frame.
- **kicker-block** — inverted ink eyebrow chip; **badge-rotated** — −4deg yellow annotation; **pill-badge** — the lone rounded chip.
- **stamp** — the −6deg closing seal. **comparison-table** — cream-2 ledger with ink head row.
- **decorative-circle** — yellow disc for shape contrast against a green panel.

### Frame Treatments

> Recipe per plate: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Authored at 1920×1080. Lean centered; vary the anchor; one idea per frame.

**1 · Wordmark Cover** (identity · move: full-frame lockup · centered). **Ground** `{colors.cream}`, `frame-pad`. **Container** grid, chrome top/bottom, focal centered. **Composes** frame-chrome, the wordmark. **Focal** the two-line wordmark at `display-hero` (15.5cqw), centered, second line in an accent (`{colors.pink}`/`orange`). **Chrome** mono topbar (section label + pill) and meta footer (descriptor + 01•NN). **Accent** the second-line color only; optionally one corner decorative-circle bleeding off an edge. **Silence** ~55% empty cream. **Fixed** Archivo Black uppercase 0.84 lh, one accent on the wordmark, square corners. **Free** which accent, line break, whether a circle bleeds a corner. **Density** sparse.

**2 · Big Claim** (oversized statement · move: scale · left). **Ground** one full-bleed accent (`{colors.pink}`/`green`/`orange`), `content-gutter`. **Container** flex, claim left-anchored and vertically centered. **Composes** kicker-block, the claim. **Focal** a 2–3 line claim at `display-xl`/`display-lg`, ink on the accent (ink-on-fire — never white). **Chrome** small ink kicker-block above the claim; mono meta footer. **Accent** the ground IS the accent; no second accent competes. **Silence** ~45% of the colored field empty. **Fixed** ink type on accent, fit-to-measure sizing, no shadow on type. **Free** the claim, which accent ground, which word breaks. **Density** sparse — one idea.

**3 · Stat Grid** (catalog · move: density — the one dense frame · centered). **Ground** `{colors.cream}`, `content-gutter`. **Container** grid: a centered `display-head` over a 3-up row of stat-cells. **Composes** frame-chrome, 3× stat-cell. **Focal** the row of three ink-bordered cells (green / pink / orange), each a `stat-num` + mono label. **Chrome** mono topbar + meta. **Accent** the three cell fills (the named density exception — three accents allowed here). **Silence** ~25% — tight by design. **Fixed** 0.4cqw borders, square corners, no per-cell shadow, mono labels. **Free** the three figures+labels, head copy, which three accents. **Density** dense-exception.

**4 · Closing Plate** (closer · move: ground-swap · centered). **Ground** `{colors.green}` (the single green frame of the run), `frame-pad`. **Focal** a 2-line sign-off at `display-lg` in `{colors.cream}`, centered. **Composes** frame-chrome (cream variant), stamp. **Chrome** cream mono topbar + meta. **Accent** one `{colors.pink}` stamp rotated −6deg in a corner, cream ring + stamp-num. **Silence** ~55% empty green. **Fixed** green ground reserved to this beat, cream-on-green type, one stamp. **Free** sign-off copy, stamp text, stamp corner. **Density** sparse.

**5 · Featured Marker** (callout · move: hard-shadow focal · left/asymmetric). **Ground** `{colors.cream}`. **Composes** frame-chrome, marker-block, optional body-md support line. **Focal** the pink marker-block with the signature orange+ink hard offset shadow, set asymmetrically. **Accent** pink block + orange shadow (two accents). **Silence** ~50%. **Fixed** exactly one hard shadow on the frame, 0.4cqw borders. **Free** marker copy, block position, optional support line. **Density** sparse.

**6 · Comparison Ledger** (data · move: matrix · left). **Ground** `{colors.cream}`, `content-gutter`. **Composes** frame-chrome, comparison-table. **Focal** the cream-2 table with ink head row; one column fill (pink or green) marks the winner. **Accent** the single column fill. **Silence** tight — the second density exception. **Fixed** cream-2 fill, 0.3cqw internal rules, ink head row with cream Archivo labels. **Free** rows, which column fills, copy. **Density** dense-exception.

### Composition Rules

**Do:** compose around one idea per frame, focal element 3–5× its neighbors (squint test); lean centered — cover, claim, stat grid, and closer all center their focal element (reserve left/asymmetric for the marker and ledger); keep sparse frames 45–60% empty (only the stat grid and ledger run dense); use two or three accents per frame (reserve `{colors.green}` ground for the closing plate); spend the hard offset shadow on one featured block per frame; size headlines fit-to-measure; render Archivo Black uppercase at 0.92 lh.

**Don't:** round corners (except the pill chip); gradient, blur, or glow; set Archivo Black in sentence case or letter-space it beyond −0.01em; use all four accents on one frame, a fifth accent, or pure white; center body copy or set labels in anything but JetBrains Mono; blow a headline edge-to-edge (step the ramp down for long lines); put two hard shadows on one frame.

### Aspect-Ratio Behavior

| Treatment          | 16:9                             | 9:16                          | 1:1                       |
| ------------------- | --------------------------------- | ----------------------------- | -------------------------- |
| Wordmark Cover      | two lines centered                | stacked taller, circle top    | centered, tighter          |
| Big Claim           | claim left, full accent           | claim top, accent full        | claim centered             |
| Stat Grid           | head over 3-up row                | head top, 3 stacked           | head top, 2×2 (4th cell)   |
| Closing Plate       | sign-off centered, stamp corner   | stacked, stamp below          | centered, stamp corner     |
| Featured Marker     | marker asymmetric                 | marker centered, shadow down  | marker centered            |
| Comparison Ledger   | full-width table                  | table scrolls to fewer cols   | 2-col table                |

Safe area holds the `3.3cqw` chrome inset on the short edge for every ratio; re-step display per
ratio so no load-bearing line drops below the 1.4cqw floor.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Products/sections are content-agnostic; the system supplies geometry, not brands.

### Numerals & Claims (hard rule)

Never invent figures, percentages, counts, or dates at frame scale. Render data slots as
`— figure —`, `{metric}`, `N×`. Real numerals appear only when the script supplies them — the stat
grid and ledger especially carry placeholders, not fabricated values.

### Pre-Render Self-Audit

- **Squint** — one element dominates at 3–5× its neighbor, else rescale.
- **Silence** — sparse frames 45–60% empty; only stat grid / ledger run dense.
- **Accents** — two or three per frame, never all four; green ground only on the closer.
- **Depth** — 0 blur; at most one hard offset shadow; color-block contrast otherwise.
- **Geometry** — square corners except the pill; rotation only at −4/−6deg.
- **Type** — Archivo Black uppercase 0.92 lh, fit-to-measure, ≥1.4cqw on load-bearing lines.
- **Anchor** — centered default; left/asymmetric only on marker + ledger; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the closing green is described as a plate, not a transition.
- Archivo Black requires Google Fonts; fallback is `sans-serif`. CJK pairing (Noto Serif SC 900 / NSC 400) carries over.
- 9:16 / 1:1 are guidance, not pixel-locked; verify the legibility floor per ratio.
- Decorative geometry (circle, stamp, stacked blocks) is CSS-only; no external imagery is required.

---

## Preset: Coral

```yaml
version: alpha
name: Coral — Frame (video / frame layer)
description: >
  Video-first companion to Coral's design.md. The unit is the frame (1920×1080), not the
  slide-in-a-deck. Atoms are identical and sacred — the three-surface system (coral fire /
  ink black / warm cream), Bebas Neue uppercase tracked + Inter body, the 45° diagonal hatch,
  decorative wallpaper numerals, hard color-region splits, zero shadow, zero radius (save
  circles). Composition, frame scale, and aspect-ratio behavior are rewritten for the frame.
  Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  coral: "#E85D5D"
  coral-dark: "#D44A4A"
  cream: "#F5F0E8"
  cream-dark: "#E8E0D4"
  black: "#1A1A1A"
  gray: "#6B6B6B"
  light-gray: "#B0B0B0"
  white: "#FFFFFF"

typography:
  # — reading ramp (Inter) —
  body:          { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.7 }
  body-light:    { fontFamily: "Inter", cqw: 1.5,  weight: 300, lineHeight: 1.5, note: "pull-quote voice" }
  section-label: { fontFamily: "Inter", px: 12, weight: 700, tracking: "4px", upper: true }
  item-label:    { fontFamily: "Inter", px: 11, weight: 700, tracking: "3px", upper: true }
  quote-attribution: { fontFamily: "Inter", px: 14, weight: 600, tracking: "3px", upper: true }
  quote-role:    { fontFamily: "Inter", px: 12, weight: 400, tracking: "1px" }
  # — display / hero ramp (Bebas Neue, uppercase, tracked) —
  card-title:    { fontFamily: "Bebas Neue", cqw: 1.9, weight: 400, lineHeight: 1.1, tracking: "1px", upper: true }
  sidebar-value: { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, upper: true }
  bar-title:     { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  card-stat:     { fontFamily: "Bebas Neue", cqw: 2.5, weight: 400, lineHeight: 1.0, upper: true }
  column-title:  { fontFamily: "Bebas Neue", cqw: 3.7, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  section-headline:{ fontFamily: "Bebas Neue", cqw: 4.2, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  stat-numeral:  { fontFamily: "Bebas Neue", cqw: 5.0, weight: 400, lineHeight: 1.0, upper: true }
  hero-title:    { fontFamily: "Bebas Neue", cqw: 6.5, weight: 400, lineHeight: 0.9, tracking: "4px", upper: true }
  jumbo-feature: { fontFamily: "Bebas Neue", cqw: 9.0, weight: 400, lineHeight: 1.0, tracking: "12px", upper: true }
  # — decorative —
  background-numeral: { fontFamily: "Bebas Neue", cqw: 10.0, weight: 400, color: "rgba(0,0,0,0.12)", note: "wallpaper numeral inside a coral region" }
  giant-mark:    { fontFamily: "Bebas Neue", cqw: 14.0, weight: 400, color: "rgba(0,0,0,0.35)", note: "decorative quote mark inside a coral region" }

spacing:
  pad-x: "5cqw"       # standard horizontal frame padding
  pad-y: "4cqw"
  pad-col: "3cqw"
  gap-grid: "1.7cqw"
  card-pad: "2cqw"

components:
  diagonal-hatch:
    backgroundImage: "repeating-linear-gradient(45deg, transparent 0 20px, rgba(0,0,0,.06) 20px 40px)"
    placement: "::before overlay on {colors.coral} regions"
    description: "Signature 45° hatch (6% ink). Variants −45° 30/60px, 90° vertical 60/62px 10% ink. Texture, never depth."
  region-split:
    layout: "two/three solid surfaces meeting at a hard edge; ratios 38/62 rows, 40/60 cols, 50/50"
    rounded: "0"
    description: "The primary layout device — no gradient, no rounded junction; the boundary is the layout."
  card:
    backgroundColor: "{colors.white}"
    borderTop: "0.26cqw solid {colors.coral}"
    rounded: "0"
    shadow: "none"
    typography: "{typography.card-title} + {typography.body}"
    description: "5px coral TOP border is the only chrome; holds a card-icon, title, body, coral card-stat."
  sidebar-item:
    backgroundColor: "{colors.white}"
    borderLeft: "0.2cqw solid {colors.coral}"
    rounded: "0"
    typography: "{typography.sidebar-value} + {typography.section-label}"
    description: "4px coral LEFT border is the only chrome."
  card-icon:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.white}"
    size: "2.5cqw square"
    rounded: "0"
    description: "The card mark — one white Bebas glyph centered."
  accent-line:
    backgroundColor: "{colors.coral}"
    size: "4cqw × 0.25cqw (60×4 closing variant)"
    rounded: "0"
    description: "Sub-headline accent rule."
  background-numeral:
    typography: "{typography.background-numeral}"
    color: "rgba(0,0,0,0.12)"
    placement: "behind a {colors.coral} region's title"
    description: "The wallpaper-numeral signature (12% ink)."
  giant-mark:
    typography: "{typography.giant-mark}"
    color: "rgba(0,0,0,0.35)"
    placement: "inside a {colors.coral} region"
    description: "Oversized quote mark / character, half-decorative."
  timeline:
    line: "0.2cqw solid {colors.black} (gradient-dashed ::after)"
    node: "{colors.coral} circle, {colors.cream} halo, 50% radius"
    description: "Ink line with coral nodes + cream halos."
  info-bar:
    backgroundColor: "{colors.cream-dark}"
    typography: "{typography.bar-title} + uppercase {typography.section-label}"
    rounded: "0"
    shadow: "none"
    description: "Footer band beneath a feature region — Bebas title left, Inter meta right."
```

### Overview

Coral at frame scale is a **bold magazine poster** built from three solid surfaces — coral fire,
ink black, warm cream — that meet at **hard color edges.** The region boundary IS the layout: a
frame splits into a coral plane + a cream plane, or a coral panel + an ink panel, each holding a
self-contained composition. No gradient transitions, no rounded junctions, no drop shadows.

The voice is a two-face hierarchy: **Bebas Neue** — tall condensed caps, always uppercase, always
tracked (1–12px) — carries every headline, stat, title, and meta figure; **Inter** carries every
body line, label, and attribution across weights 300–700. Bebas declares; Inter explains. The
signature atmospherics are the **45° diagonal hatch** (6% ink) over coral regions and the
**oversized wallpaper numeral** (12% ink) behind a region's title.

**Key characteristics at frame scale:**

- **Three surfaces, hard edges** — `{colors.coral}` / `{colors.black}` / `{colors.cream}` as solid regions.
- **Bebas uppercase + tracking** on every display element; **Inter** on every body/label.
- **45° hatch** (6% ink) on coral regions; **wallpaper numerals** (12%) and **giant marks** (35%) behind content.
- **Ink-on-fire** — Bebas on coral is always ink, never white. Eyebrows coral on cream/ink, ink on coral.
- **Flat** — no shadow, no elevation; radius only on circles (nav dots, timeline nodes).
- **Coral as accent AND environment** — 4–5px coral borders, 48px coral icon squares, and full coral regions.

### The Frame

**Frame Craft Bar:**

- **Squint** — one element dominates at **3–6× its nearest neighbor**: the `hero-title`/`jumbo-feature` or a wallpaper numeral behind a region's title, never two rival headlines.
- **Silence** — coral/cream/ink regions read **40–55% empty**; the **three-column catalog is the one dense exception**. A coral region underfilled gets a wallpaper numeral, never more content.
- **Restraint** — coral fires as **either accent or one full region per frame** (not both at full strength); one giant-mark per quote; ink-on-fire (never white on coral).
- **Reference** — aim at a **sports-magazine cover / Saul Bass travel poster**; failure looks like a **soft drop-shadowed card deck**.

- **Primary:** 1920×1080 (16:9). Display sizes authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `5cqw` (pad-x) standard frame padding; region edges may bleed full-frame.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` resolved against it — **never `vw`.**

### Colors

Tokens identical to the source. At frame scale the three surfaces are intermixed by composition —
coral/cream, coral/ink, ink/cream, or single-surface. `{colors.coral}` is both accent (borders,
icon squares, timeline nodes, eyebrows on cream/ink) and environment (full regions). Headlines:
ink on cream/coral, cream on ink — **never gray, never white-on-coral.** Eyebrows: coral on
cream/ink, ink on coral — coral-on-coral does not exist. The only sanctioned gradient is the rare
135° coral-dark→coral feature region; everything else is flat.

### Typography

Two ramps. The **reading ramp** (Inter body 1.0cqw, body-light 1.5cqw, labels in px) carries copy
and eyebrows; the **display/hero ramp** (Bebas, `card-title` 1.9cqw → `jumbo-feature` 9.0cqw, plus
the decorative `background-numeral` 10cqw and `giant-mark` 14cqw) carries every headline and stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its line length. Cap the block at **≤ 78cqw**; ≤3 words → `hero-title`/`jumbo-feature`; 4–6 → `section-headline`; 7+ → `column-title`.
- **Every Bebas element is uppercase with ≥1px tracking** (2px standard, 4px hero, 12px jumbo). **Every Inter label is uppercase, 1–4px tracked.** No italic, no underline, no sentence-case Bebas.

### Depth & Surface

Flat, with hard color edges. Depth signals only:

- **Hard region boundaries** — the primary structural device.
- **Accent borders** — 5px coral top (cards), 4px coral left (sidebar tiles), 4px ink (timeline).
- **45° hatch** — 6% ink texture on coral regions (no depth).
- **Wallpaper typography** — numerals at 12%, giant marks at 35%, layered behind content.

**Ceiling:** no box-shadow, no elevated card, no soft gradient (save the one 135° coral feature), no rounded rectangle.

### Shapes

- **0 radius** on every rectangle — regions, cards, sidebar tiles, icon squares, info bars, accent lines.
- **50%** on circles only — nav dots (10px), nav arrows (44px), timeline nodes (20px).

### Components

- **region-split** — the layout device; surfaces meet at a hard edge.
- **card** (5px coral top) / **sidebar-item** (4px coral left) / **card-icon** (48px coral square) — the only chrome on each is its single coral border.
- **diagonal-hatch** / **background-numeral** / **giant-mark** — the atmospheric + wallpaper signatures on coral regions.
- **accent-line** — coral sub-headline rule. **timeline** — ink line, coral nodes, cream halos. **info-bar** — cream-dark footer band.

### Frame Treatments

> Recipe per plate: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Lean centered where the move allows; vary anchor; one idea per region.

**1 · Region-Split Cover** (identity · move: hard region edge · left). **Ground** 38/62 split — `{colors.coral}` top band (hatch + wallpaper numeral) over `{colors.cream}`. **Container** grid rows; brand + meta in the coral band, hero title in the cream field. **Composes** region-split, diagonal-hatch, background-numeral, hero-title. **Focal** a 2-line `hero-title` in ink, second line in `{colors.coral}`, left-anchored in the cream field. **Chrome** Bebas brand left, Bebas meta right in the coral band. **Accent** coral band + coral second line. **Silence** the cream field ~45% empty. **Fixed** ink-on-fire in band, hatch on coral, hard edge. **Free** title copy, which line is coral, meta. **Density** sparse.

**2 · Feature Stat** (anchor · move: scale · coral environment · left). **Ground** full `{colors.coral}` with hatch. **Composes** diagonal-hatch, background-numeral, section-label, stat headline, body-light. **Focal** a `stat-numeral`/`jumbo-feature` figure or 2-line headline in ink, with a `background-numeral` (12% ink) behind it as wallpaper. **Chrome** an ink `section-label` eyebrow; an optional Inter-300 support line ≤44cqw. **Accent** the coral ground IS the environment; ink type, no white. **Silence** ~40% of the coral field empty. **Fixed** ink-on-coral, hatch present, wallpaper numeral behind. **Free** the figure, headline, support copy. **Density** sparse.

**3 · Quote Layout** (quote · move: panel split · giant mark). **Ground** 40/60 split — `{colors.coral}` left panel (hatch + giant-mark) + `{colors.black}` right panel. **Composes** region-split, giant-mark, body-light, accent-line, quote-attribution. **Focal** a 2–3 line pull quote in `{colors.cream}` Inter weight 300 on the ink panel. **Chrome** a `giant-mark` (35% ink) on the coral panel; a `60×4` coral accent-line above the attribution. **Accent** coral panel + coral accent-line. **Silence** the coral panel is mostly the mark. **Fixed** Inter-300 quote, ink panel, ink-on-coral mark. **Free** quote, attribution, mark glyph. **Density** sparse.

**4 · Closing Plate** (closer · move: cream field + coral band · centered). **Ground** `{colors.cream}` field with a bottom `{colors.coral}` band (hatch). **Composes** section-label, section-headline/hero-title, accent-line, info-bar. **Focal** a 2-line sign-off in ink, centered, with a coral `accent-line` beneath. **Chrome** an ink eyebrow above; a coral band footer carrying a Bebas sign-off + year. **Accent** coral band + coral accent-line. **Silence** ~55% empty cream. **Fixed** centered, ink type, one coral band. **Free** sign-off copy, band contents. **Density** sparse.

**5 · Three-Column Catalog** (catalog · move: density — the dense frame · centered head). **Ground** `{colors.cream}` (or `{colors.black}`), `pad-x`. **Composes** section-headline, 3× card. **Focal** a centered `section-headline` over three white `card`s (5px coral top, 48px icon square, Bebas title, Inter body, coral stat). **Accent** the three coral top borders + icon squares. **Silence** tight — the density exception. **Fixed** 5px coral top as sole chrome, no shadow/radius. **Free** the three cards' content. **Density** dense-exception.

**6 · Timeline** (process · move: horizontal rail · left). **Ground** `{colors.cream}`, `pad-x`. **Composes** section-headline, timeline. **Focal** the ink timeline-line with 4–5 coral nodes (cream halos) and Bebas labels. **Accent** coral nodes. **Silence** moderate. **Fixed** ink line, coral nodes, cream halos. **Free** node count, labels. **Density** standard.

### Composition Rules

**Do:** compose as multi-surface region splits — coral / ink / cream meeting at hard edges (the boundary is the layout); set every Bebas element uppercase + tracked (2px standard, 4px hero, 12px jumbo), every Inter label uppercase 1–4px; render eyebrows coral on cream/ink, ink on coral, headlines ink on cream/coral, cream on ink; apply the 45° hatch (6% ink) on coral regions, fill underweight coral regions with a 12% wallpaper numeral; use the 5px coral top (cards) / 4px coral left (tiles) as the only chrome on those elements; lean centered on cover sign-offs and catalog heads, left/panel-split on features and quotes.

**Don't:** render Bebas in sentence case or untracked, or pair it with a non-Inter body sans; add a fourth surface, a drop shadow, an elevation, or a rounded rectangle; put white headlines on coral (always ink) or gray headlines anywhere; soften a region boundary with a gradient (except the rare 135° coral feature); fill a coral region with sparse fragments — fully populate it or add a wallpaper numeral / giant mark; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment             | 16:9                          | 9:16                                   | 1:1                    |
| ---------------------- | ------------------------------ | ---------------------------------------- | ------------------------ |
| Region-Split Cover     | 38/62 rows, title left         | taller coral band, title below           | 40/60, title lower       |
| Feature Stat           | figure left, numeral right     | figure top, numeral behind               | centered figure          |
| Quote Layout           | 40/60 coral+ink                | stacked: coral mark top, quote below     | stacked                  |
| Closing Plate          | cream + bottom coral band      | cream + taller band                      | centered, band below     |
| Three-Column Catalog   | head over 3-up                 | head top, 3 stacked                      | head top, 2+1            |
| Timeline               | horizontal rail                | vertical rail                            | compact horizontal       |

Safe area holds the `5cqw` padding on the short edge; re-step display per ratio so no load-bearing
line drops below the 1.4cqw floor. Bebas runs ~20% wider in CJK — adjust line breaks per ratio.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The system supplies surfaces and geometry, not brands.

### Numerals & Claims (hard rule)

Never invent figures, stats, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `N×`. Real numerals appear only when the script supplies them. Wallpaper numerals
(01, 02…) are decorative and may be ordinal.

### Pre-Render Self-Audit

- **Squint** — one focal element per region dominates at 3–5× its neighbor.
- **Silence** — sparse frames 40–55% empty; only the catalog runs dense.
- **Surfaces** — two or three of coral/ink/cream, meeting at hard edges; no fourth surface.
- **Type** — Bebas uppercase + tracked, fit-to-measure; ink-on-coral; eyebrow color correct for surface; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded rectangle; hatch + wallpaper carry texture.
- **Anchor** — centered on sign-offs/heads, panel/left on features/quotes; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the 0.6s opacity fade in the source is a deck mechanic, not a frame spec.
- Bebas Neue + Inter via Google Fonts. CJK pairing (ZCOOL XiaoWei / Yozai) carries over; Bebas runs ~20% wider in CJK.
- 9:16 / 1:1 are guidance, not pixel-locked; verify the legibility floor per ratio.
- The 45° hatch, wallpaper numerals, giant marks, and timeline dash are CSS-only; no external imagery is required.

---

## Preset: Biennale Yellow

```yaml
version: alpha
name: Biennale Yellow — Frame (video / frame layer)
description: >
  Video-first companion to Biennale Yellow's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — warm parchment grounds, a single deep indigo ink, solar yellow deployed
  as bloom / panel / tile underprint, Instrument Serif display + Archivo sans + JetBrains Mono data,
  1px hairline rules as the only border, atmospheric depth (no shadows), and the bottom-right
  pagenum. Composition + frame scale rewritten. Restraint is the rule; motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#E9E5DB"
  paper-deep: "#DCD6C4"
  sun: "#F1EE2E"
  sun-soft: "#F8F39B"
  haze: "#F0DA7C"
  ink: "#1B2566"
  ember: "#E26B4A"

typography:
  # — reading + data ramp —
  body:    { fontFamily: "Archivo", cqw: 0.85, weight: 400, lineHeight: 1.5, color: "ink" }
  body-lede:{ fontFamily: "Archivo", cqw: 0.95, weight: 400, lineHeight: 1.55 }
  micro-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.18em", upper: true }
  rail-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.32em", upper: true }
  mono-data:{ fontFamily: "JetBrains Mono", cqw: 0.73, weight: 400, tracking: "0.04em" }
  pagenum: { fontFamily: "JetBrains Mono", px: 13, weight: 400, tracking: "0.08em", opacity: 0.75 }
  # — display ramp (Instrument Serif 400, tight, negative tracking) —
  ledger-title:{ fontFamily: "Instrument Serif", cqw: 1.55, weight: 400, lineHeight: 1.15 }
  strand-title:{ fontFamily: "Instrument Serif", cqw: 1.7, weight: 400, lineHeight: 1.1 }
  headline-sm:{ fontFamily: "Instrument Serif", cqw: 2.9, weight: 400, lineHeight: 1.0 }
  headline:{ fontFamily: "Instrument Serif", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.005em" }
  date-rail:{ fontFamily: "Instrument Serif", cqw: 5.0, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-it:{ fontFamily: "Instrument Serif", cqw: 7.0, weight: 400, italic: true, lineHeight: 1.04, tracking: "-0.005em" }
  numeral-md:{ fontFamily: "Instrument Serif", cqw: 7.5, weight: 400, lineHeight: 0.92, tracking: "-0.01em" }
  display:{ fontFamily: "Instrument Serif", cqw: 14.6, weight: 400, lineHeight: 0.86, tracking: "-0.018em" }
  numeral-jumbo:{ fontFamily: "Instrument Serif", cqw: 28.0, weight: 400, lineHeight: 0.84, tracking: "-0.04em" }

spacing:
  pad-edge: "4cqw"
  pad-region: "4.2cqw"
  gap-region: "2.5cqw"

components:
  sun-bloom:
    background: "radial gradient {colors.sun} core → {colors.sun-soft} → {colors.haze} → transparent on {colors.paper}"
    size: "42–70% of the frame, off-center or behind the focal element"
    description: "The primary depth layer. One per frame; a flat parchment frame reads as broken."
  ember-bloom:
    background: "radial {colors.ember} at 15–22% opacity"
    placement: "corner opposite the sun-bloom"
    description: "Subordinate counter-temperature balance; never dominant."
  block-tile:
    backgroundColor: "{colors.sun} at 40–70% opacity"
    layout: "rectangles on an 8×4 grid behind cover/colophon"
    description: "A layered poster underprint."
  yellow-panel:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink}"
    rounded: "0"
    border: "none (meets paper directly)"
    description: "Full-bleed column/third — the strongest color statement, ink on top."
  hairline-rule:
    rule: "1px solid {colors.ink} (soft variant: {colors.ink} at 18–20%)"
    description: "The ONLY border — header underlines, footer tops, ledger separators. No thicker rule exists."
  strand-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.strand-title} + {typography.body}"
    description: "Serif numeral + serif title + sans body. Numbered editorial lists."
  ledger-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.mono-date} · {typography.ledger-title} · {typography.body} · {typography.mono-data}"
    description: "4-col tabular — mono date · serif title · sans venue · mono duration (right)."
  footer-band:
    borderTop: "1px solid {colors.ink} per cell"
    typography: "{typography.micro-label} + {typography.body-sm}"
    description: "4-column metadata strip at the foot of cover/colophon."
  vertical-rail:
    typography: "{typography.rail-label}"
    transform: "rotated up the left edge"
    description: "Section marker on chapter/divider frames."
  pagenum:
    typography: "{typography.pagenum}"
    color: "{colors.ink} at 75%"
    placement: "bottom-right"
    description: "The only persistent chrome."
```

### Overview

Biennale Yellow at frame scale is a **literary-editorial system** in the register of an art
biennale catalogue: warm parchment, a single deep indigo ink, and solar yellow as atmosphere. No
cards, no buttons, no shadows, no rounded corners — the structural vocabulary is just **paper, ink,
and yellow.** Depth is delivered by soft radial **sun blooms**, not elevation.

The voice is three faces in rigid roles: **Instrument Serif** (weight 400, tight line-height,
negative tracking) carries every display, numeral, and quote from 40px to 720px+; **Archivo** carries
body and the wide-tracked uppercase micro-label; **JetBrains Mono** carries every date, figure, and
the pagenum. Text is **always ink** — contrast comes from size and weight, never color. The mood
sits between a folded museum brochure and a slow-reading literary quarterly: confident, atmospheric,
deeply restrained.

**Key characteristics at frame scale:**

- **Warm parchment ground** on every frame; never white, never gray.
- **Single ink** (`{colors.ink}`) for all type and all rules; **solar yellow** as bloom / panel / tile.
- **Instrument Serif 400** display (tight, negative-tracked); **Archivo** body + micro-labels; **JetBrains Mono** data.
- **1px hairline rules** are the only border — no thicker weight exists; **no shadows, no rounded corners**.
- **Sun bloom** is the primary depth layer on every frame; an ember counter-bloom adds warm-cool tension.
- **Editorial-restrained** — sparse reads as elegant; crowding breaks the catalogue feel.

### The Frame

**Frame Craft Bar:**

- **Squint** — one Instrument Serif moment dominates at 3–6× its neighbor; the sun bloom centers the eye.
- **Silence** — frames read **55–60% empty**; the **ledger is the one dense exception** (density via quiet hairline repetition, not richness).
- **Restraint** — **one ink color** for all type and rules; **one sun bloom** per frame (+ optional subordinate ember); never invert (no yellow text on ink).
- **Reference** — aim at an **art-biennale catalogue / slow exhibition poster / literary quarterly**; failure looks like a **flat CMS template** (no bloom) or a **bordered-card deck**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-edge` 4cqw (40–76px equivalent) — the elegance depends on edge negative space; only blooms, tiles, and panels bleed.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Hairlines stay 1px; bloom sizes scale
as `%` of the frame.

### Colors

Tokens identical to the source. `{colors.paper}` is the universal ground; `{colors.ink}` (deep
indigo navy) is **every line of type and every rule** — there is no secondary text color.
`{colors.sun}` deploys three ways: the **bloom** (radial atmosphere), the **yellow-panel**
(full-bleed poster fill, ink on top), and the **block-tile** underprint. `{colors.sun-soft}`/`haze`
are bloom mid/outer stops. `{colors.ember}` appears **only** as a 15–22% counter-bloom — never a
fill, never text. **The system never inverts** — ink on sun is correct; yellow text on ink does not exist.

### Typography

Two ramps. The **reading/data ramp** (Archivo body 0.85cqw ink, micro-labels in px, JetBrains Mono
data) carries copy + chrome; the **display ramp** (Instrument Serif `ledger-title` 1.55cqw →
`numeral-jumbo` 28cqw) carries every headline, numeral, and quote.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono/labels in px are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`; 4–6 → `headline`; 7+ → `headline-sm`. The jumbo numeral is a divider's whole point — don't shrink it.
- **Instrument Serif is weight 400 only** (its contrast is the weight signal), tight line-height (0.84–1.06), negative tracking; **micro-labels uppercase Archivo 600, ≥0.16em**; **mono for all numerals/dates**. No bold serif, no second text color, no mono in body/display.

### Depth & Surface

Atmospheric, not structural. Depth from:

- **Sun bloom** — the primary layer: a layered radial (sun 70–95% core → sun-soft → haze 18–22% → paper 0%), 42–70% of the frame. One per frame.
- **Ember bloom** — a 15–22% peach counter-bloom in the opposite corner; always subordinate.
- **Block-tile underprint** — translucent yellow rectangles on an 8×4 grid (cover/colophon).
- **Yellow panel** — the one "hard" color statement: a flooded column/third, ink on top.
- **Hairline rules** — 1px ink for structural separation (soft 18–20% variant for dense rows).

**Ceiling:** zero box-shadow, zero text-shadow, zero rounded corner, no border thicker than 1px.

### Shapes

- **0 radius on everything** — strict rectangles. Blooms are edgeless (they fade into paper).

### Components

- **sun-bloom / ember-bloom / block-tile** — the atmospheric depth set. **yellow-panel** — the poster-fill statement.
- **hairline-rule** — the only border (1px ink; soft variant for dense rows).
- **strand-row / ledger-row / footer-band** — the editorial list, tabular calendar, and metadata strip.
- **vertical-rail** — rotated chapter marker. **pagenum** — the bottom-right mono chrome.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> A sun bloom + bottom-right pagenum on every frame; sparse is the default.

**1 · Cover** (identity · move: display + sun bloom · left). **Ground** paper + a large sun-bloom (left-of-center) + an ember counter-bloom (opposite corner). **Composes** micro-label, display, date-rail, footer-band, pagenum. **Focal** a 2-line Instrument Serif `display` (italic key word) in ink, left, under a micro-label. **Chrome** a serif date-rail top-right; a 4-column footer-band at the foot. **Accent** the sun bloom + yellow. **Silence** the bloom holds the open space. **Fixed** ink type, one bloom, 1px footer rules, no shadow. **Free** title, date, footer cells. **Density** low.

**2 · Chapter Divider** (section · move: jumbo numeral · vertical rail). **Ground** paper + a corner-anchored sun-bloom. **Composes** vertical-rail, numeral-jumbo, headline-sm. **Focal** a single huge Instrument Serif `numeral-jumbo` (≈28cqw) dominating, with a serif title beneath. **Chrome** a rotated vertical-rail label up the left edge; pagenum. **Accent** the bloom behind the numeral. **Silence** ~60%. **Fixed** serif 400, jumbo numeral, rail label. **Free** the ordinal, title, rail text. **Density** low.

**3 · Ledger** (catalog · move: hairline tabular rows · the dense frame). **Ground** paper (bloom optional, subtle). **Composes** headline-sm + micro-label topbar, ledger-rows. **Focal** a 4-column tabular calendar — mono date · serif title · sans venue · mono duration — separated by hairline-soft rules under a 1px ink header rule. **Chrome** pagenum. **Accent** none — density through quiet repetition, not color. **Silence** tight — the density exception. **Fixed** hairline rules, mono dates, serif titles. **Free** rows, venues. **Density** dense-exception.

**4 · Manifesto / Quote** (quote · move: italic serif · centered bloom). **Ground** paper + a centered sun-bloom. **Composes** numeral-lg quote mark, display-it, attribution. **Focal** a 2-line Instrument Serif italic `display-it` quote in ink, centered, under an oversized serif quote mark. **Chrome** a micro-label attribution. **Accent** the centered bloom. **Silence** ~60% — deliberately open. **Fixed** italic serif, one bloom, ink. **Free** quote, attribution. **Density** low.

**5 · Poster Panel** (statement · move: yellow panel · split). **Ground** paper with a full-bleed `{colors.sun}` `yellow-panel` (column or third). **Composes** yellow-panel, micro-label, headline. **Focal** an Instrument Serif `headline` in ink sitting on the sun panel (ink-on-yellow — a signature). **Chrome** micro-label; pagenum. **Accent** the panel itself. **Silence** the paper side stays open. **Fixed** ink-on-sun, panel meets paper directly (no border), no shadow. **Free** headline, panel side/width. **Density** low.

**6 · Strand List** (programme · move: numbered editorial rows · left). **Ground** paper + a subtle sun-bloom. **Composes** micro-label, headline-sm, strand-rows. **Focal** a numbered list — serif numeral + serif title + sans body, hairline-soft separators. **Chrome** micro-label; pagenum. **Accent** the bloom. **Silence** moderate; rows breathe. **Fixed** serif numerals, hairline-soft rules. **Free** items, copy. **Density** standard.

### Composition Rules

**Do:** start on warm parchment, add one sun bloom (optionally an ember counter-bloom) — atmosphere is the depth; set every line in ink, use Instrument Serif 400 (tight, negative-tracked) for display, Archivo body, JetBrains Mono for all numerals/dates; make every separator a 1px ink hairline (soft variant for dense rows); flood a yellow panel for poster moments (ink on top); keep micro-labels uppercase Archivo 600, 0.16–0.32em; pin the pagenum bottom-right; lean sparse, left/asymmetric on cover/chapter/list, centered on manifesto.

**Don't:** use drop shadows, rounded corners, bordered cards, or a border thicker than 1px; use a second text color; bold Instrument Serif; invert ink grounds; use mono for body/display; substitute fonts; crowd the canvas; omit the bloom (flat parchment reads as a CMS template); blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment        | 16:9                                             | 9:16                          | 1:1                          |
| ------------------ | -------------------------------------------------- | ------------------------------- | ------------------------------- |
| Cover              | display left, date-rail top-right, footer foot     | display top, footer stacks      | display upper, footer foot      |
| Chapter Divider    | jumbo numeral, rail left                           | numeral centered, rail top      | numeral centered                |
| Ledger             | 4-col rows                                         | drop venue col → 3-col          | 3-col                           |
| Manifesto          | centered italic                                    | centered, taller                | centered                        |
| Poster Panel       | side panel + paper                                 | top/bottom panel band           | panel third                     |
| Strand List        | numbered rows                                      | rows (tighter)                  | rows                            |

`pad-edge` holds on the short edge; display clamps use the shorter axis so portrait doesn't blow out
headlines. Keep load-bearing lines ≥ 1.4cqw. Ledger/strand fixed first columns may tighten on 9:16.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Programme titles, venues, and dates are content; the system supplies paper, ink, yellow.

### Numerals & Claims (hard rule)

Never invent figures, dates, durations, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `NN JUN`, `N m`. Chapter ordinals (01, 02…) are decorative.

### Pre-Render Self-Audit

- **Squint** — one serif display moment dominates; the bloom centers the eye.
- **Silence** — sparse frames 55–60% open; only the ledger runs dense (via repetition, not richness).
- **One color** — ink for all text + rules; sun for bloom/panel/tile; ember counter-bloom only; no inversion.
- **Type** — Instrument Serif 400 tight negative-tracked, fit-to-measure; micro-labels uppercase 0.16em+; mono numerals; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 rounded corner, 1px hairlines only; one sun bloom present.
- **Anchor** — left on cover/chapter/list, centered on manifesto; pagenum bottom-right.
- **Fabrication** — every numeral/date traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source's 280ms crossfade is a deck mechanic.
- Instrument Serif + Archivo + JetBrains Mono via Google Fonts. CJK: Smiley Sans (display) / Noto Serif SC (body) / Noto Sans SC (labels); italic serif and mono tabular figures have no exact Hanzi equal — keep ledger dates Latin.
- 9:16 / 1:1 are guidance; the `min(vw,vh)` clamp pattern keeps display from blowing out — verify per ratio.
- Sun/ember blooms, block tiles, yellow panels, and hairline rules are CSS-only; no external imagery is required.

---

## Preset: Daisy Days

```yaml
version: alpha
name: Daisy Days — Frame (video / frame layer)
description: >
  Video-first companion to Daisy Days' design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the sunny-garden pastel palette (cream + turquoise/pink/butter/mint/
  lavender/peach/sky + coral accent), charcoal 3px outlines, hard offset shadows (6/4px, no blur),
  the Fredoka + Quicksand pairing, generous radii, headline text-shadow on color, dot bullets, and
  the hand-drawn SVG ornament layer. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F0E6"
  turquoise: "#7ECDC0"
  soft-pink: "#F7C8D4"
  butter: "#FDE68A"
  mint: "#A8E6CF"
  lavender: "#D4A5E8"
  peach: "#FFCBA4"
  sky: "#A8D8F0"
  coral: "#F8635F"
  text-dark: "#2D2D2D"
  text-muted: "#6B6B6B"
  white: "#FFFFFF"

borders: { primary: "3px solid text-dark", thin: "2px solid text-dark" }
shadows: { default: "6px 6px 0 text-dark", small: "4px 4px 0 text-dark", text-headline: "3px 3px 0 text-dark", text-headline-soft: "3px 3px 0 rgba(0,0,0,0.2)" }

typography:
  # — reading ramp (Quicksand) —
  body:    { fontFamily: "Quicksand", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  body-strong:{ fontFamily: "Quicksand", cqw: 0.95, weight: 600, lineHeight: 1.5 }
  meta:    { fontFamily: "Quicksand", cqw: 0.78, weight: 600, lineHeight: 1.45 }
  # — display ramp (Fredoka One / Fredoka 600 — single weight, never italic) —
  badge:   { fontFamily: "Fredoka One", cqw: 0.9, tracking: "0.02em" }
  label-display:{ fontFamily: "Fredoka One", cqw: 1.3, lineHeight: 1.3, tracking: "0.02em" }
  subtitle:{ fontFamily: "Fredoka One", cqw: 1.8, lineHeight: 1.2, tracking: "0.02em" }
  quote:   { fontFamily: "Fredoka One", cqw: 2.6, lineHeight: 1.35 }
  title:   { fontFamily: "Fredoka One", cqw: 3.0, lineHeight: 1.15, tracking: "0.02em" }
  headline:{ fontFamily: "Fredoka One", cqw: 4.5, lineHeight: 1.1, tracking: "0.02em" }
  display: { fontFamily: "Fredoka One", cqw: 6.5, lineHeight: 1.1, tracking: "0.02em" }

spacing:
  pad-slide: "3cqw"
  radius: "20px"
  radius-lg: "28px"
  radius-pill: "50px"
  radius-round: "50%"

components:
  card:
    backgroundColor: "{colors.white}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius} (28px featured)"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "The universal container; white-on-pastel is standard."
  framed-header:
    backgroundColor: "pastel cap + {colors.white} body"
    border: "3px solid {colors.text-dark} (one continuous)"
    rounded: "{spacing.radius-lg}"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "Pastel header strip flush above a white body — one unit, one shadow."
  badge-pill:
    backgroundColor: "{colors.butter}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius-pill}"
    typography: "{typography.badge}"
    shadow: "4px 4px 0 {colors.text-dark}"
    description: "Section tag. white-space:nowrap."
  circle-marker:
    backgroundColor: "any pastel"
    textColor: "{colors.white} (dark on butter)"
    border: "3px solid {colors.text-dark}"
    rounded: "50%"
    size: "bullet 20 / icon 44 / dot 48 / step 90"
    typography: "Fredoka numeral"
    description: "Steps carry a small shadow."
  bullet-dot:
    backgroundColor: "{colors.butter}"
    border: "2px solid {colors.text-dark}"
    rounded: "50%"
    size: "20px (::before, 4px from line top)"
    description: "Lists never use glyph bullets."
  ornament:
    type: "hand-drawn SVG (daisy, star, sun, cloud, rainbow)"
    stroke: "2.1px {colors.text-dark}"
    placement: "z-index:1 behind content (z-index:2), cropping past the frame edge"
    description: "3–7 per frame, clustered at corners/edges."
  quote-mark:
    typography: "oversized Fredoka quote glyph"
    color: "{colors.soft-pink} (charcoal stroke)"
    description: "Above a quote body."
  text-headline-shadow:
    shadow: "3px 3px 0 {colors.text-dark} (soft 20% variant on pink/mint)"
    appliesTo: "Fredoka headlines on saturated surfaces (cream headlines sit flat)"
    description: "Makes the headline read 'outlined' like the shapes."
```

### Overview

Daisy Days at frame scale is a **cheerful, childlike system** — picture-book illustration meets
sticker-sheet kawaii. Every shape carries a **3px charcoal outline**, every elevated element a
**solid hard offset shadow** (no blur), every surface a sunny-garden pastel. The voice is one
pairing: **Fredoka One** (chunky rounded, single weight) for every headline, **Quicksand** for
every body and meta line. The signature is the **hand-drawn SVG ornament layer** — daisies, stars,
suns, clouds, rainbows clustering at corners and cropping past the edge.

The palette is **multi-pastel with one warm pop**: cream canvas, seven pastel surfaces, and
`{colors.coral}` reserved for small high-attention markers only. Headlines on a saturated surface
get a 3px charcoal text-shadow (so they read "outlined" like the shapes) and switch to white;
headlines on cream sit flat in charcoal. Depth is 2D and graphic — thick outline + hard offset =
sticker-on-paper.

**Key characteristics at frame scale:**

- **Cream default + rotating pastel surfaces**; `{colors.coral}` is a marker accent, never a surface.
- **Fredoka One** headlines + **Quicksand 500/600** body — strict by role, never crossed.
- **3px charcoal outline + hard offset shadow** (6/4px, zero blur) on every elevated shape.
- **Generous radii** — 20px cards, 28px featured, pill badges, full-circle markers; no square corners.
- **Headline text-shadow on saturated surfaces** (white text); flat charcoal on cream.
- **Dot bullets** (outlined butter discs, never glyphs) + a **3–7 ornament wreath** per frame.

### The Frame

**Frame Craft Bar:**

- **Squint** — one Fredoka headline or content card dominates at 3–6× its neighbor.
- **Silence** — **one content container per frame** surrounded by an ornament wreath; the **info-card grid is the one dense exception**. Empty corners read as broken.
- **Restraint** — cream or **one** pastel surface; coral is a small-marker accent (never a surface); charcoal borders + hard offset shadows only; no ninth color.
- **Reference** — aim at a **children's picture-book / sticker-sheet kawaii zine**; failure looks like a **flat, square-cornered, blurred-shadow corporate slide**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-slide` ~3cqw; ornaments deliberately bleed past the edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders stay 3px/2px; radii stay
20/28/50px; shadow offsets scale in `cqw` so the sticker offset holds proportionally.

### Colors

Tokens identical to the source. Default ground `{colors.cream}`; rotate saturated pastels
(turquoise / soft-pink / butter / mint / lavender / peach / sky) for tonal mood. **Cards are white**
on any surface. **Borders + shadows are always `{colors.text-dark}` charcoal** — never colored,
never blurred, never `rgba` (save the soft text-shadow variant). `{colors.coral}` is the lone
high-saturation accent — small markers only, never a surface. Body is charcoal/muted; pastels
carry no semantic meaning. No ninth color.

### Typography

Two ramps. The **reading ramp** (Quicksand 500 body 0.95cqw, 600 emphasis, meta) carries copy; the
**display ramp** (Fredoka One `label-display` 1.3cqw → `display` 6.5cqw, single weight) carries
every headline, title, quote, and marker numeral.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; meta is chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`; 4–6 → `headline`; 7+ → `title`.
- **Fredoka One for all display, Quicksand for all body — never crossed.** Fredoka is single-weight (no italic, no underline, no alt weights); Quicksand stays 500/600/700. Fredoka tracking 0.02em; Quicksand body never uppercase.

### Depth & Surface

2D graphic depth — hard offset shadow, solid charcoal, zero blur, bottom-right:

- **`shadows.default` 6px** cards, frames, badges, chart containers.
- **`shadows.small` 4px** small cards, step circles, avatars.
- **Text-headline shadow** — 3px charcoal on Fredoka headlines over saturated surfaces (20% soft variant on pink/mint); cream headlines flat.
- **Outline + offset** together are the sticker-on-paper signature.

**Ceiling:** no blurred shadow, no `rgba` (except the soft text-shadow), no gradient, no glow; an element either casts a hard charcoal offset or none.

### Shapes

- **20px** cards, **28px** featured, **50px** pill (badges, counter), **50%** all circles, **4px** legend swatch. Zero square corners — every region is rounded.

### Components

- **card / framed-header** — the white-fill bordered containers (one shadow). **badge-pill** — butter section tag.
- **circle-marker** family (bullet 20 / icon 44 / dot 48 / step 90) + **bullet-dot** — outlined pastel discs, Fredoka numerals.
- **ornament** — the hand-drawn SVG sticker layer (3–7 per frame). **quote-mark** — soft-pink Fredoka anchor. **text-headline-shadow** — the on-color headline treatment.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One content container per frame + a 3–7 ornament wreath; empty corners read as broken.

**1 · Cover** (identity · move: ornament wreath · saturated · centered). **Ground** a saturated pastel (e.g. `{colors.turquoise}`). **Composes** badge-pill, display, body sub, 3–7 ornaments, counter. **Focal** a 1–2 line Fredoka `display` in white with the 3px charcoal text-shadow, centered, under a butter badge-pill. **Chrome** counter pill. **Accent** the ornament wreath (daisies + stars at corners, cropping past edges). **Silence** content centered; ornaments fill the edges. **Fixed** text-shadow on color, 3px outlines, charcoal shadows. **Free** surface color, ornament mix/positions, copy. **Density** full-but-not-crowded.

**2 · Info Cards** (catalog · move: 3-up white cards · cream · the dense frame). **Ground** `{colors.cream}`, `pad-slide`. **Composes** headline (flat charcoal), 3× card (circle-icon + Fredoka title + Quicksand body), a couple ornaments. **Focal** three white 3px-bordered cards with 6px shadows. **Chrome** flat headline. **Accent** the pastel circle-icons (rotate turquoise/coral/lavender). **Silence** tight — the density exception (fewer ornaments here). **Fixed** white cards, 3px + 6px, 20px radius. **Free** card content, icon hues. **Density** dense-exception.

**3 · Process Steps** (sequence · move: rotating circle markers · peach · centered). **Ground** `{colors.peach}` (or another pastel). **Composes** headline (white + text-shadow), 3–4 step circles + `→` arrows, ornaments. **Focal** a row of 90px outlined step circles, fills rotating coral → mint → sky → lavender, Fredoka white numerals, linked by Fredoka arrows. **Chrome** white headline with text-shadow. **Accent** the rotating circle fills. **Silence** moderate. **Fixed** 3px circles + small shadow, rotating fills, arrow glyphs. **Free** step count, labels. **Density** standard.

**4 · Quote** (quote · move: quote-mark anchor · soft-pink · centered). **Ground** `{colors.soft-pink}`. **Composes** a white quote card (28px radius, 6px shadow), quote-mark, Fredoka quote, Quicksand attribution, ornaments. **Focal** a Fredoka `quote` in charcoal inside the white card, under an oversized soft-pink quote-mark. **Chrome** Quicksand 700 attribution. **Accent** the quote-mark + a star or two. **Silence** card centered, ornaments at corners. **Fixed** quote-mark anchor, white card. **Free** quote, attribution. **Density** moderate.

**5 · Framed Section** (feature · move: cap+body card · cream). **Ground** `{colors.cream}`. **Composes** framed-header (pastel cap + white body), bullet-dot list, ornaments. **Focal** a framed-header — a pastel cap strip (Fredoka title, optional text-shadow) above a white body with a butter-dot bullet list. **Accent** the cap color + bullet dots. **Silence** moderate. **Fixed** one continuous 3px border + one shadow, butter dot bullets. **Free** cap color, list. **Density** standard.

**6 · Closing** (closer · move: ornament wreath · saturated · centered). **Ground** a saturated pastel (e.g. `{colors.lavender}`). **Composes** badge-pill, display (white + text-shadow), 3–7 ornaments. **Focal** a Fredoka `display` sign-off in white with the charcoal text-shadow, centered. **Accent** the ornament wreath. **Silence** content centered. **Fixed** text-shadow on color, ornaments fill corners. **Free** sign-off, surface, ornaments. **Density** full.

### Composition Rules

**Do:** pair Fredoka One headlines + Quicksand body strictly by role; outline every shape 3px charcoal + a hard offset shadow (6/4px, no blur), white card fills on any surface; give Fredoka headlines on saturated surfaces a 3px charcoal text-shadow + white text (flat charcoal on cream); use outlined butter-disc bullets (never glyphs), cluster 3–7 hand-drawn ornaments per frame (corners, cropping past edges); keep one content container per frame, rotate marker colors (coral → mint → sky → lavender → butter), reserve coral for small markers; center most frames — lean cream for content-dense frames, saturated for cover/closer/quote.

**Don't:** use square corners; use blurred or `rgba` shadows (save the soft text-shadow); use colored borders (charcoal only); use a coral surface or a ninth color; use a third font, a Quicksand headline, or a Fredoka body; use italic/underline Fredoka or uppercase Quicksand body; use glyph bullets or leave empty corners; put two competing content panels on one frame; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment       | 16:9                        | 9:16                              | 1:1          |
| ---------------- | ------------------------------ | ------------------------------------ | -------------- |
| Cover             | centered, corner ornaments     | centered, taller, more ornaments     | centered       |
| Info Cards        | 3 across                       | stacked                              | 2+1            |
| Process Steps     | horizontal + arrows            | vertical, arrows rotate down         | 2×2            |
| Quote             | centered card                  | centered, taller                     | centered       |
| Framed Section    | cap + body                     | cap + body taller                    | cap + body     |
| Closing           | centered, wreath               | centered, wreath                     | centered       |

`pad-slide` holds on the short edge; re-step display above the 1.4cqw floor. On tighter ratios keep
the ornament count toward the upper end (5–7) so corners never read empty.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Ornaments and pastels are content-agnostic; counters/badges carry per-deck text.

### Numerals & Claims (hard rule)

Never invent figures, dates, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N`. Step numbers and any chart values carry placeholders until the script supplies them; the slide
counter is decorative chrome.

### Pre-Render Self-Audit

- **Squint** — one Fredoka headline or content card dominates per frame.
- **Silence** — one container per frame surrounded by an ornament wreath; only the info-card grid runs dense.
- **Color** — cream or one pastel surface; coral markers only; charcoal borders/shadows; no ninth hue.
- **Type** — Fredoka headlines (text-shadow + white on saturated, flat charcoal on cream), Quicksand body; ≥1.4cqw floor.
- **Depth** — 3px outline + hard offset (no blur, no rgba save soft text-shadow); rounded corners only.
- **Ornaments** — 3–7 per frame, cropping past edges; no empty corners. **Bullets** — outlined discs, never glyphs.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source uses scroll-snap nav, no transition spec.
- Fonts: the source names Fredoka One; Google now serves the Fredoka variable family — request
  `Fredoka:wght@500;600;700` and set display weight 600 (visually equal to Fredoka One), keeping
  Fredoka One first in the stack for environments that still serve it. Quicksand loads normally.
  CJK: ZCOOL XiaoWei (display) / Yozai (body).
- 9:16 / 1:1 are guidance; keep ornament count high so corners stay filled per ratio.
- Ornaments (daisy/star/sun/cloud/rainbow), markers, and framed headers are CSS/SVG-only.
- Contrast: keep `{colors.text-muted}` off pastel surfaces (cream/white cards only); small text on saturated grounds should be charcoal or white.

---

## Preset: Cobalt Grid

```yaml
version: alpha
name: Cobalt Grid — Frame (video / frame layer)
description: >
  Video-first companion to Cobalt Grid's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — warm cream paper, electric cobalt ink (the only ink), the permanent
  graph-paper grid, Newsreader serif 400 + Hanken Grotesk + DM Mono, the top/bottom cobalt
  hairlines, and the pixel-glitch + QR-block signatures. Composition, frame scale, and
  aspect-ratio behavior are rewritten for the frame. Motion is out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#F0EBDE"
  paper-2: "#E6E0CE"
  ink: "#1F2BE0"
  ink-soft: "#5560E5"
  grid: "rgba(31,43,224,0.10)"
  ink-faint: "rgba(31,43,224,0.18)"

typography:
  # — reading ramp —
  body:        { fontFamily: "Hanken Grotesk", cqw: 0.83, weight: 400, lineHeight: 1.5 }
  body-lede:   { fontFamily: "Hanken Grotesk", cqw: 0.95, weight: 400, lineHeight: 1.5 }
  micro:       { fontFamily: "Hanken Grotesk", px: 13, weight: 600, tracking: "0.16em", upper: true }
  micro-strong:{ fontFamily: "Hanken Grotesk", px: 16, weight: 600, tracking: "0.18em", upper: true }
  mono-tag:    { fontFamily: "DM Mono", cqw: 0.78, weight: 400, tracking: "0.05em" }
  mono-chrome: { fontFamily: "DM Mono", px: 13, weight: 400, tracking: "0.06em" }
  # — display / hero ramp (Newsreader 400, negative tracking) —
  table-name:  { fontFamily: "Newsreader", cqw: 1.5, weight: 400, lineHeight: 1.15 }
  row-headline:{ fontFamily: "Newsreader", cqw: 2.1, weight: 400, lineHeight: 1.05 }
  ed-callout:  { fontFamily: "Newsreader", cqw: 2.6, weight: 400, lineHeight: 1.1, italic: true }
  headline:    { fontFamily: "Newsreader", cqw: 4.6, weight: 400, lineHeight: 0.95 }
  headline-index:{ fontFamily: "Newsreader", cqw: 5.0, weight: 400, lineHeight: 0.95 }
  display-quote:{ fontFamily: "Newsreader", cqw: 5.7, weight: 400, lineHeight: 1.05, tracking: "-0.005em" }
  display-chapter:{ fontFamily: "Newsreader", cqw: 6.8, weight: 400, lineHeight: 1.0, tracking: "-0.005em" }
  display-closing:{ fontFamily: "Newsreader", cqw: 9.4, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-hero:{ fontFamily: "Newsreader", cqw: 10.4, weight: 400, lineHeight: 0.9, tracking: "-0.008em" }
  vbig-numeral:{ fontFamily: "Newsreader", cqw: 12.5, weight: 400, lineHeight: 0.9, tracking: "-0.015em" }

spacing:
  edge: "4cqw"          # standard frame edge inset (~80px@1920)
  pad-top: "7cqw"
  pad-bottom: "6cqw"
  gap-md: "2cqw"

components:
  graph-grid:
    backgroundImage: "linear-gradient grid, ~2cqw cells, 10% {colors.ink} ({colors.grid})"
    placement: "behind EVERY frame on the ground"
    description: "Permanent graph-paper grid — never disabled; the canvas tone."
  hairlines:
    rule: "0.12cqw solid {colors.ink}"
    placement: "≈3cqw from top + bottom, inset {spacing.edge}"
    description: "Two persistent cobalt rules framing every composition."
  page-chrome:
    typography: "{typography.pagenum}"
    color: "{colors.ink}"
    placement: "page number bottom-right, nav/meta hint bottom-left, above the bottom hairline"
    description: "The only persistent chrome."
  pixel-glitch:
    backgroundColor: "{colors.paper}"
    fill: "repeating-linear-gradient(90deg, {colors.ink} 0 2px, transparent 2px 8px)"
    size: "14–30cqw wide, full height, stair-stepped"
    placement: "right on cover/data, left on chapter/colophon; z above grid, below headline"
    description: "Stair-stepped scanline column. Decorative."
  qr-block:
    backgroundColor: "{colors.paper}"
    cells: "8×8, {colors.ink} on / {colors.grid} off"
    size: "3–9cqw square"
    shadow: "0 0 0 0.12cqw {colors.paper} (anti-shadow for readability, not elevation)"
    description: "QR mosaic patch — corner punctuation."
  topbar-rule:
    typography: "{typography.headline-index} + {typography.mono-tag}"
    borderBottom: "0.12cqw solid {colors.ink}"
    description: "Section header on index/data/table frames."
  ledger-row:
    layout: "grid: mono num · Newsreader name · Hanken desc · mono delta"
    borderBottom: "0.06cqw solid {colors.ink-faint} (header 0.12cqw solid {colors.ink})"
    typography: "{typography.mono-tag} + {typography.table-name} + {typography.body}"
    description: "Dense matrix row with ↑/↓/— delta."
  pixel-stack-bar:
    cells: "column-reverse, {colors.grid} off / {colors.ink} on"
    baseline: "0.12cqw solid {colors.ink} + {typography.mono-tick} ticks"
    description: "Data as grid-unit cells; echoes the glitch."
  vstack-label:
    typography: "{typography.mono-tick}"
    transform: "writing-mode: vertical-rl"
    description: "Catalogue chrome along a frame edge."
```

### Overview

Cobalt Grid at frame scale is a **two-color risograph trend-report** — warm cream paper, electric
cobalt ink, and a **permanent graph-paper grid** behind every frame. Cobalt is the only ink:
headlines, body, rules, the grid, the pixel-glitch decoration, the QR patches. There is no accent
color and no second surface.

The voice is a three-face conversation: **Newsreader** serif at weight 400 (size, not weight,
makes hierarchy) carries every display and headline; **Hanken Grotesk** carries body and
uppercase tracked labels; **DM Mono** carries all chrome — page numbers, tags, ticks, vertical
stacks. Every frame is framed by top + bottom cobalt hairlines; declarative frames carry the
**pixel-glitch column** and a **QR-block** patch.

**Key characteristics at frame scale:**

- **Strictly two-color** — cream paper + cobalt ink; no accent, no second surface.
- **Permanent ~2cqw graph-paper grid** (10% cobalt) behind every frame; cannot be disabled.
- **Top + bottom 1.5px cobalt hairlines** frame every composition, inset by `edge`.
- **Newsreader 400** for all display (negative tracking); **Hanken 600** uppercase 0.16em labels; **DM Mono** chrome.
- **Pixel-glitch column + QR-block** as the signature decorative patches on declarative frames.
- **Pixel-stack bars** render data as grid-unit cells (cobalt on / 10% off).

### The Frame

**Frame Craft Bar:**

- **Squint** — one Newsreader element dominates at **3–6× its nearest neighbor** (`display-hero`/`vbig-numeral`); hierarchy is size, never weight.
- **Silence** — declarative frames (cover, chapter, quote, colophon) read **45–60% empty** with the grid showing; the **index ledger and data frame are the one dense exception** (density via quiet repetition, not richness).
- **Restraint** — **two-color only** (cream + cobalt, never a second hue); one pixel-glitch column and at most one QR-block per declarative frame.
- **Reference** — aim at a **WIRED Japan / Shift two-color risograph monograph**; failure looks like a **colorful dashboard with a second accent hue**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `edge` (4cqw) inset; hairlines + page chrome live on the safe line.

**The container law (load-bearing).** Every frame ground sets `container-type: size` AND carries
the graph-paper `background-image`; ALL frame-relative units are `cqw`/`cqh` against it — never
`vw`. The grid `background-size` is `~2cqw 2cqw` so cell density holds at any render size.

### Colors

Tokens identical to the source. `{colors.paper}` is the ground; `{colors.ink}` cobalt is the only
ink (type, rules, grid lines, glitch, QR). `{colors.ink-soft}` is a secondary cobalt for editorial
subtitles only; `{colors.grid}` (10%) is the permanent grid + chart "off" cells; `{colors.ink-faint}`
(18%) is faint row dividers. **Never a second hue** — emphasis comes from size, from switching
Hanken→Newsreader, from a mono delta arrow, or from opacity, never from color.

### Typography

Two ramps. The **reading ramp** (Hanken body 0.83cqw, mono chrome in px) carries copy + labels;
the **display/hero ramp** (Newsreader `headline` 4.6cqw → `vbig-numeral` 12.5cqw) carries every
statement and figure.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono chrome (px) is colophon only.
- **Fit-to-measure:** size the headline to its line length. Cap the block at **≤ 78cqw**; ≤3 words → `display-hero`/`vbig-numeral`; 4–6 → `display-chapter`; 7+ → `headline`.
- **Newsreader at 400 only**, in cobalt, with negative tracking (hero −0.008em, numeral −0.015em). **Hanken labels uppercase, 0.16–0.18em.** **DM Mono 0.04–0.08em.** No bold serif.

### Depth & Surface

Flat. Depth is structural only:

- **1.5px cobalt rules** — slide hairlines, topbar rule, chart baseline.
- **1px ink-faint dividers** — dense list / ledger rows.
- **The graph-paper grid** — measured-plane tone behind everything.
- **Pixel-glitch + QR** — texture and graphic punctuation, no z-axis.

**Ceiling:** no drop shadow (the QR's 1.5px paper outset is an anti-shadow for readability, not elevation), no gradient, no rounded corner, no second color.

### Shapes

- **0 radius everywhere** — frames, ledger rows, QR cells, glitch blocks, charts. Zero circular elements; this squareness is part of the identity.

### Components

- **graph-grid / hairlines / page-chrome** — the permanent frame furniture, inherited by every composition.
- **pixel-glitch** (edge column) + **qr-block** (corner patch) — the signature decoration on declarative frames.
- **topbar-rule** — the index/data/table section header. **ledger-row** — dense matrix row with delta arrows.
- **pixel-stack-bar** — data as grid-unit cells. **vstack-label** — vertical mono catalogue chrome.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> The grid + hairlines are present on every frame. Choose density by type: declarative = sparse, index/data = dense.

**1 · Hero Cover** (identity · move: serif + glitch · left). **Ground** paper + grid, hairlines. **Composes** pixel-glitch (right, ~26cqw), qr-block (top-right), display-hero, ed-callout. **Focal** a 1–2 line `display-hero` Newsreader headline in cobalt, left-anchored, with an italic `ed-callout` subtitle in `{colors.ink-soft}`. **Chrome** Hanken kicker; mono meta top + page number. **Accent** none (cobalt is the only ink). **Silence** ~45% paper. **Fixed** Newsreader 400, glitch + QR present, grid + hairlines. **Free** title, glitch step pattern, QR placement. **Density** sparse.

**2 · Index Ledger** (catalog · move: dense matrix · left — the dense frame). **Ground** paper + grid, hairlines, `pad-top`/`pad-bottom`. **Composes** topbar-rule, ledger-rows. **Focal** a topbar (`headline-index` + mono lab-tag, 1.5px rule) over 4–6 ledger rows (mono num · Newsreader name · Hanken desc), ink-faint dividers. **Chrome** page number. **Accent** mono delta arrows. **Silence** tight — the density exception (the grid wants filling). **Fixed** 1.5px topbar rule, 1px ink-faint dividers, Newsreader names. **Free** rows, lab-tag, deltas. **Density** dense-exception.

**3 · Chapter Opener** (section · move: scale · sparse · left). **Ground** paper + grid, hairlines. **Composes** pixel-glitch (left, ~14cqw, low opacity), mono index, display-chapter, body-lede. **Focal** a `display-chapter` Newsreader title, with a small mono `CHAPTER NN` index above and an optional Hanken lede ≤42cqw. **Accent** none. **Silence** ~60% — let the grid breathe. **Fixed** Newsreader 400, glitch low-opacity, grid showing. **Free** title, lede, glitch side. **Density** sparse.

**4 · Data Frame** (chart · move: pixel-stack · left). **Ground** paper + grid, hairlines, `pad-top`. **Composes** topbar-rule, pixel-stack-bar row. **Focal** a row of 6–8 pixel-stack bars (cobalt on / 10% off) over a 1.5px cobalt baseline with mono ticks. **Chrome** topbar headline + mono fig-tag; page number. **Accent** none — data is cobalt cells. **Silence** moderate. **Fixed** grid-unit cells, cobalt baseline, mono ticks. **Free** bar values (from script), tick labels. **Density** standard/dense.

**5 · Manifesto / Quote** (quote · move: centered statement · sparse). **Ground** paper + grid, hairlines. **Composes** display-quote (or display-manifesto), attribution rule, optional compact glitch. **Focal** a 2–3 line Newsreader pull in cobalt, with a Hanken kicker above and a 1px cobalt attribution rule + mono byline beneath. **Accent** none. **Silence** ~55% — deliberately open. **Fixed** Newsreader 400, attribution rule, grid showing. **Free** quote, byline. **Density** sparse.

**6 · Colophon** (closer · move: right-aligned close · sparse). **Ground** paper + grid, hairlines. **Composes** pixel-glitch (left edge, mirroring the cover), display-closing, mono credit columns. **Focal** a right-aligned `display-closing` Newsreader title with a Hanken kicker above. **Chrome** 3–4 column mono credit grid at the foot; page number. **Accent** none. **Silence** ~50%. **Fixed** glitch on left, Newsreader 400. **Free** closing line, credits. **Density** sparse.

### Composition Rules

**Do:** keep the graph-paper grid + top/bottom hairlines on every frame (they are the system); set Newsreader at 400 in cobalt, make hierarchy with size not weight, negative-track display; track Hanken labels uppercase 0.16em, DM Mono chrome 0.04–0.08em; render data as pixel-stack cells (cobalt on / 10% off) echoing the glitch language; use the pixel-glitch column + QR patch on declarative frames (cover, chapter, quote, colophon); lean declarative frames sparse and breathing, index/data dense; vary anchor (left for index/chapter, centered for quote/closer).

**Don't:** introduce a second ink color; bold Newsreader, round any corner, or add a drop shadow (QR outset is an anti-shadow only); disable the grid or suppress the hairlines; crowd chapter / quote / colophon (those let the grid show); blow a serif headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment           | 16:9                            | 9:16                                     | 1:1                            |
| --------------------- | ---------------------------------- | ------------------------------------------- | --------------------------------- |
| Hero Cover            | headline left, glitch right        | headline top, glitch full-width band        | headline upper, glitch lower      |
| Index Ledger          | topbar + rows                      | topbar + fewer rows                         | 2-col compresses to 1             |
| Chapter Opener        | title left, glitch left            | title top, glitch side                      | centered title                    |
| Data Frame            | 6–8 bars                           | 4–5 bars taller                             | square chart                      |
| Manifesto / Quote     | centered pull                      | centered, taller                            | centered                          |
| Colophon              | right-aligned, glitch left         | stacked, glitch top                         | centered close                    |

Grid + hairlines hold on the short edge for every ratio; re-step display so no load-bearing line
drops below 1.4cqw. Mono chrome stays Latin/digit-only.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Trend names, signals, and figures are content; the system supplies the grid and chrome.

### Numerals & Claims (hard rule)

Never invent figures, deltas, dates, or signal counts at frame scale. Render slots as `— figure —`,
`{metric}`, `↑ —`. Mono catalogue ordinals (001, 002…) are decorative and may be sequential.

### Pre-Render Self-Audit

- **Squint** — one Newsreader element dominates at 3–5× its neighbor.
- **Silence** — declarative frames 45–60% empty; only index/data run dense.
- **Two-color** — cream + cobalt only; no second hue anywhere.
- **Furniture** — grid present, top/bottom hairlines present, page chrome above the hairline.
- **Type** — Newsreader 400 negative-tracked, fit-to-measure; Hanken labels 0.16em; ≥1.4cqw floor.
- **Depth** — 0 shadow (QR outset excepted), 0 rounded corner.
- **Anchor** — left on index/chapter/cover, centered on quote/closer; no 3 consecutive frames share an anchor.
- **Fabrication** — every numeral/delta traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the 280ms cross-fade in the source is a deck mechanic.
- Pixel-glitch is rendered in CSS here (stacked scanline blocks) rather than the source's inline SVG.
- Three Google Fonts (Newsreader, Hanken Grotesk, DM Mono); CJK pairing (Noto Serif SC 700/400) carries over.
- 9:16 / 1:1 are guidance; verify the legibility floor and grid density per ratio.
- The QR mosaic and glitch step patterns are hand-authored; there is no generative layer.

---

## Preset: Capsule

```yaml
version: alpha
name: Capsule — Frame (video / frame layer)
description: >
  Video-first companion to Capsule's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the pill geometry (9999px small / 2rem cards) with a 2px ink outline on
  everything, the sun-bleached cream canvas, the nine-color candy palette, Bodoni Moda + Space
  Grotesk, soft hard-offset shadows (4/6/8/12px in 8% ink), floating decorative-pill wallpaper,
  radial accent glows, and the grain overlay. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F5F0"
  ink: "#1A1A1A"
  outline: "#1E1E1E"
  white: "#FFFFFF"
  coral: "#E85D4E"
  lime: "#C4D94E"
  lavender: "#C5B5E0"
  sky: "#8BB4F7"
  violet: "#A06CE8"
  yellow: "#F2D160"
  peach: "#F5B895"
  mint: "#A8E6CF"
  shadow: "rgba(26,26,26,0.08)"

typography:
  # — reading ramp (Space Grotesk) —
  body:      { fontFamily: "Space Grotesk", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:  { fontFamily: "Space Grotesk", cqw: 0.95, weight: 400, tracking: "0.18em", upper: true }
  pill-text: { fontFamily: "Space Grotesk", cqw: 0.75, weight: 600, tracking: "0.12em", upper: true }
  label:     { fontFamily: "Space Grotesk", px: 14, weight: 500, tracking: "0.1em", upper: true }
  # — display / hero ramp (Bodoni Moda, ink, sentence case) —
  card-headline:{ fontFamily: "Bodoni Moda", cqw: 1.9, weight: 700, lineHeight: 1.1 }
  orbit-numeral:{ fontFamily: "Bodoni Moda", cqw: 2.6, weight: 700, lineHeight: 1.0 }
  quote-display:{ fontFamily: "Bodoni Moda", cqw: 4.2, weight: 600, lineHeight: 1.3, tracking: "-0.01em" }
  stat-number: { fontFamily: "Bodoni Moda", cqw: 3.6, weight: 800, lineHeight: 1.0, tracking: "-0.03em" }
  section-headline:{ fontFamily: "Bodoni Moda", cqw: 4.0, weight: 700, lineHeight: 1.05, tracking: "-0.01em" }
  headline:    { fontFamily: "Bodoni Moda", cqw: 5.0, weight: 700, lineHeight: 1.05, tracking: "-0.02em" }
  closing-display:{ fontFamily: "Bodoni Moda", cqw: 8.5, weight: 800, lineHeight: 0.95, tracking: "-0.03em" }
  display:     { fontFamily: "Bodoni Moda", cqw: 12.0, weight: 800, lineHeight: 0.88, tracking: "-0.03em" }

spacing:
  pad: "5cqw"
  gap-md: "2cqw"
  card-pad: "2cqw 1.6cqw"

components:
  pill:
    rounded: "9999px (small) / 2rem (cards)"
    border: "0.2cqw solid {colors.outline}"
    backgroundColor: "any candy or {colors.white}"
    description: "The universal container — every chip/button/label/stat tile/node/bar. No unstroked pill exists."
  pill-card:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.4cqw 0.4cqw 0 {colors.shadow}"
    typography: "{typography.card-headline} + {typography.body}"
    description: "Holds a circular card-icon, Bodoni headline, Space Grotesk body."
  stat-pill:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.stat-number} (COLORED) + {typography.pill-text}"
    description: "The one place color touches a numeral; + a 40px accent bar."
  title-pill:
    backgroundColor: "{colors.yellow}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.pill-text}"
    description: "Sits above the display headline on cover/closing."
  card-icon:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "50%"
    size: "60px"
    typography: "Bodoni numeral/letter in {colors.ink}"
    description: "Card mark."
  floating-pill:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px / 50%"
    transform: "rotate(−20°..+25°)"
    shadow: "none"
    typography: "{typography.pill-text}"
    description: "Decorative wallpaper confetti, 5–8 per declarative frame. Flat — no shadow."
  quote-highlight:
    backgroundColor: "{colors.lime} / {colors.sky}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    description: "Inline candy pill wrapping a phrase inside a Bodoni quote — the emphasis mechanism, replacing bold/italic."
  bar-track:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    fill: "child candy pill, value at right edge"
    description: "36px pill chart track."
  accent-line:
    backgroundColor: "{colors.coral}"
    rounded: "9999px"
    size: "60×4 (80×4 closing)"
    description: "Coral pill rule."
  atmosphere:
    background: "1–3 radial candy glows (6–15% opacity) over {colors.cream} + 4% grain overlay"
    description: "Baseline canvas layers on every frame. Never absent."
```

### Overview

Capsule at frame scale is a **playful editorial system where every container is a pill.** The
`border-radius: 9999px` (small) / `2rem` (cards) rule plus a 2px ink outline wraps every chip,
card, icon, bar, and node — inflated, friendly, graphically distinct. The canvas is sun-bleached
cream warmed by soft radial candy glows and a permanent 4% grain overlay.

The voice is a two-face conversation: **Bodoni Moda** (didone serif, weight 700–800, always ink,
always sentence case) carries every headline, stat, and quote; **Space Grotesk** carries body and
all uppercase tracked pill/label text. Nine candy accents fill pills interchangeably with no
semantic meaning. Depth is a **soft hard-offset shadow** (4/6/8/12px in 8% ink) — lifted, not
stamped — reserved for content-bearing containers; decorative floating pills are flat.

**Key characteristics at frame scale:**

- **Pill geometry everywhere** — 9999px small, 2rem cards — each wrapped in a 2px `{colors.outline}` stroke.
- **Bodoni Moda** display (ink, sentence case) + **Space Grotesk** body/pills (uppercase, tracked).
- **Nine candy accents**, interchangeable; color touches stat numerals + pill fills, never headlines.
- **Soft offset shadows** (4/6/8/12px, 8% ink) on content containers only; floating pills are flat.
- **Floating decorative-pill wallpaper** (5–8, tilted) + radial glows + 4% grain on declarative frames.
- **Cream canvas** warmed by atmosphere — bare corners read as broken.

### The Frame

**Frame Craft Bar:**

- **Squint** — one Bodoni headline or stat dominates at **3–6× its nearest neighbor**.
- **Silence** — declarative frames carry **atmosphere, not clutter** (pills as wallpaper, not content); the **pillar-cards and stat grid are the dense exception**.
- **Restraint** — every pill carries the 2px outline; color touches **fills + stat numerals only** (never a headline); soft shadow on content-bearing pills only (floating pills are flat); no tenth accent.
- **Reference** — aim at a **Memphis / ice-cream-parlor editorial spread**; failure looks like a **flat, sticker-less SaaS card grid**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad` (5cqw); floating pills may bleed off edges as wallpaper.

**The container law (load-bearing).** Every frame ground sets `container-type: size` AND carries
the radial-glow + grain atmosphere; ALL frame-relative units are `cqw`/`cqh` against it — never
`vw`. Pill radii stay `9999px`/`2rem` (shape, not scale); shadow offsets scale in `cqw`.

### Colors

Tokens identical to the source. `{colors.cream}` is the ground; `{colors.ink}`/`{colors.outline}`
is type + the universal 2px stroke; the nine candy accents fill pills with **no semantic mapping**
— pair a warm (coral/yellow/peach) with a cool (sky/lavender/violet/mint) with a neutral-bright
(lime); never two same-family adjacent. Color appears on **stat numerals and pill fills only** —
never on a Bodoni headline. Shadow is always `{colors.shadow}` (8% ink). No tenth color.

### Typography

Two ramps. The **reading ramp** (Space Grotesk body 0.85cqw, uppercase tracked pill/label text)
carries copy + chips; the **display ramp** (Bodoni `card-headline` 1.9cqw → `display` 12cqw, all
700–800) carries every headline, stat, and quote.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display`/`closing-display`; 4–6 → `headline`; 7+ → `section-headline`.
- **Bodoni 700+ in ink, sentence case** (italic via `<em>` only, color allowed on the italic key word as a candy hue); **Space Grotesk pills/labels uppercase, 0.08em+ tracked**; negative-track Bodoni display.

### Depth & Surface

Soft hard-offset shadow is the only depth, in `{colors.shadow}` (8% ink), bottom-right:

- **0.2cqw (4px)** small nodes; **0.3cqw (6px)** stat-pills, orbit pills, diagram nodes; **0.4cqw (8px)** pillar-cards; **0.6cqw (12px)** the visual frame.
- The **2px outline** does most of the lift against cream; the shadow adds the float.
- **Decorative floating pills cast no shadow** — this separates content from atmosphere at a glance.

**Ceiling:** no blurred shadow, no re-colored shadow, no gradient depth.

### Shapes

- **9999px** — all small pills (chips, buttons, bars, nodes, floating pills, quote highlights, accent lines).
- **2rem** — larger cards (pillar-card, stat-pill, chart container, visual frame).
- **50%** — circular pills (card-icon 60px, step-node 56px, orbit-center 160px, nav dots).
- **0** — only the grain overlay and the gradient region inside a visual frame. No sharp-cornered text container exists.

### Components

- **pill** — the universal 2px-outlined container. **pill-card / stat-pill / title-pill** — the white/yellow content pills with soft shadows.
- **card-icon** — circular candy mark; **floating-pill** — flat tilted wallpaper confetti; **quote-highlight** — inline candy emphasis pill.
- **bar-track** — pill-shaped chart bar; **accent-line** — coral pill rule; **atmosphere** — the baseline glow + grain on every frame.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Atmosphere (glow + grain) on every frame; declarative frames carry floating-pill wallpaper.

**1 · Cover** (identity · move: title pill + display · centered). **Ground** cream + atmosphere, floating-pill wallpaper. **Composes** title-pill, display, accent-line, floating-pills (5–8). **Focal** a 1–2 line Bodoni `display` headline in ink (italic key word in a candy hue), centered, under a yellow title-pill; a coral accent-line below. **Chrome** uppercase Space Grotesk sub. **Accent** the italic word + candy floating pills. **Silence** content centered; pills fill the edges. **Fixed** pill outlines, Bodoni ink, flat floating pills. **Free** title, which candy hues, pill words/positions. **Density** medium-atmospheric.

**2 · Pillar Cards** (catalog · move: 3-up grid · left — the dense frame). **Ground** cream + atmosphere. **Composes** title-pill (lavender), section-headline, 3× pill-card. **Focal** three white 2rem pill-cards (circular candy card-icon, Bodoni card-headline, Space Grotesk body) with 0.4cqw shadows, under a Bodoni section-headline. **Chrome** a lavender header tag-pill. **Accent** the three card-icon fills (coral/sky/lime sequence). **Silence** tight — the density exception (no floating pills here). **Fixed** 2px outlines, soft shadows, ink headlines. **Free** card content, icon hues. **Density** dense-exception.

**3 · Stat Grid** (data · move: stat pills · centered head). **Ground** cream + atmosphere. **Composes** section-headline, 3–4× stat-pill. **Focal** a row of white stat-pills, each a COLORED Bodoni stat-number + uppercase label + accent bar. **Accent** the colored numerals + bars (the one place color meets type). **Silence** moderate. **Fixed** 2rem pills, colored numerals only, soft shadow. **Free** figures (from script), hues. **Density** standard.

**4 · Pull Quote** (quote · move: highlight pill · left). **Ground** cream + atmosphere, a few floating pills. **Composes** quote-display, quote-highlight, accent-line. **Focal** a Bodoni quote in ink with one phrase wrapped in a lime/sky `quote-highlight` pill (the emphasis mechanism — never bold). **Chrome** uppercase attribution. **Accent** the highlight pill. **Silence** ~50%. **Fixed** Bodoni 600, highlight-pill emphasis. **Free** quote, highlight color/phrase. **Density** sparse.

**5 · Orbit** (concept · move: gravitational pills · centered). **Ground** cream + atmosphere. **Composes** orbit-center (160px lime circle, Bodoni ordinal), 4–6 orbit-pill satellites (candy, tilted, soft shadow). **Focal** the lime center anchored by orbiting candy pills. **Accent** the satellite hues. **Silence** moderate. **Fixed** circular center, outlined satellites with shadow. **Free** ordinal, satellite words/positions. **Density** medium.

**6 · Closing Plate** (closer · move: title pill + display · centered). **Ground** cream + atmosphere, floating-pill wallpaper. **Composes** title-pill (yellow), closing-display, accent-line, floating-pills. **Focal** a Bodoni `closing-display` sign-off in ink (italic word in violet/candy), centered. **Accent** the italic word + pills. **Silence** content centered. **Fixed** Bodoni ink, flat pills. **Free** sign-off, pill words. **Density** medium-atmospheric.

### Composition Rules

**Do:** make every text container a pill (9999px / 2rem) with the 2px ink outline; set Bodoni headlines in ink, sentence case (color lives on stat numerals + pill fills); use soft offset shadows (4/6/8/12px, 8% ink) on content containers, keep floating pills flat; float 5–8 candy pills + radial glows + grain on declarative frames (bare corners read as broken); wrap inline emphasis in a candy quote-highlight pill, never bold/italic-alone; pair warm+cool+neutral-bright accents, lean centered on cover/closer, left on cards/quote.

**Don't:** use a sharp-cornered text container or an unstroked pill; color a Bodoni headline or set it uppercase; use a blurred or re-colored shadow, or a tenth accent color; put a shadow on decorative floating pills; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment      | 16:9                              | 9:16                          | 1:1                     |
| ---------------- | ------------------------------------ | -------------------------------- | -------------------------- |
| Cover            | display centered, pills around       | display top, pills band          | centered, fewer pills      |
| Pillar Cards     | head + 3-up                          | head + 3 stacked                 | head + 2+1                 |
| Stat Grid        | 3–4 across                           | 2×2                               | 2×2                        |
| Pull Quote       | quote left                           | quote top, highlight inline      | centered                   |
| Orbit            | center + 4–6 satellites              | center + 3 satellites            | center + 4                 |
| Closing          | centered + pills                     | centered, pills band             | centered                   |

`pad` holds on the short edge; re-step display above the 1.4cqw floor. Floating-pill count drops
on tighter ratios so they stay wallpaper, not clutter.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Floating-pill words are neutral atmospheres ("VISION", "FUTURE", "NEXT"), never
content-specific.

### Numerals & Claims (hard rule)

Never invent figures, stats, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N%`. Stat-pill numbers and bar-track widths carry placeholders until the script supplies values.

### Pre-Render Self-Audit

- **Squint** — one Bodoni element dominates at 3–5× its neighbor.
- **Silence** — declarative frames carry atmosphere not clutter; only pillar/stat grids run dense.
- **Pills** — every container is a pill with a 2px outline; no sharp text container.
- **Color** — candy on fills + stat numerals only; headlines ink; no tenth hue.
- **Depth** — soft offset shadow on content only; floating pills flat; no blur.
- **Type** — Bodoni ink sentence-case, fit-to-measure; pills uppercase tracked; ≥1.4cqw floor.
- **Anchor** — centered on cover/closer/orbit, left on cards/quote; no 3 consecutive alike.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the 0.6s fade in the source is a deck mechanic.
- Bodoni Moda + Space Grotesk via Google Fonts. CJK pairing (ZCOOL XiaoWei / Yozai) carries over.
- 9:16 / 1:1 are guidance; verify the floor and that floating-pill count scales down.
- The grain overlay, radial glows, floating pills, and bar fills are CSS-only; no external imagery is required.

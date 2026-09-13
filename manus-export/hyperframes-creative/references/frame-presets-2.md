# Frame Presets (2 of 2)

Continuation of `frame-presets-1.md`. See that file's header for the shared structural contract
(container law, motion-out-of-scope, numerals hard rule, aspect-ratio guidance) that applies to
every preset below as well.

This file covers: **claude, editorial-forest, blockframe, blue-professional, broadside,
bold-poster**. See `frame-presets-1.md` for: cartesian, creative-mode, coral, biennale-yellow,
daisy-days, cobalt-grid, capsule.

---

## Preset: Claude

```yaml
version: alpha
name: Claude — Frame (video / frame layer)
description: >
  Video-first companion to Claude's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — warm cream paper (never pure white, never cool), a single terracotta coral
  as scarce "voltage", hairline ink elevation (no heavy shadow), EB Garamond for all
  display + Inter body + JetBrains Mono for the index/code voice on a warm-navy code surface,
  sentence-case display, and the ✱ coral spike mark. Composition + frame scale rewritten. Motion
  out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink: "#141413"
  cream: "#FAF9F5"
  tile: "#EFE9DE"
  tile-strong: "#ECE3D4"
  coral: "#CC785C"
  navy: "#181715"
  navy-soft: "#1F1E1B"
  navy-elev: "#252320"

borders: { hairline: "1px solid ink@12%", hairline-strong: "1px solid ink@20%", dark: "1px solid cream@14% (on navy)" }
shadows: { card: "0 1px 3px ink@8%, 0 4px 16px ink@4%", none: "none" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 1.5, weight: 400, lineHeight: 1.5 }
  lead:    { fontFamily: "Inter", cqw: 2.08, weight: 400, lineHeight: 1.5 }
  card-title:{ fontFamily: "Inter", cqw: 2.3, weight: 500, lineHeight: 1.25, tracking: "-0.005em" }
  button:  { fontFamily: "Inter", cqw: 1.46, weight: 500, lineHeight: 1.0 }
  tag-upper:{ fontFamily: "Inter", cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  kicker:  { fontFamily: "JetBrains Mono", px: 28, cqw: 1.46, weight: 500, tracking: "0.16em", upper: true }
  mono-label:{ fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.02em" }
  code:    { fontFamily: "JetBrains Mono", cqw: 1.67, weight: 400, lineHeight: 1.6 }
  # — display ramp (EB Garamond 400, sentence case, negative tracking. Renderer embeds only 400/700 — author at 400; italic is the synthesized slant) —
  headline:{ fontFamily: "EB Garamond", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.018em" }
  quote-pull:{ fontFamily: "EB Garamond", cqw: 5.0, weight: 400, lineHeight: 1.12, tracking: "-0.012em", italic: true }
  display-italic:{ fontFamily: "EB Garamond", cqw: 6.7, weight: 400, lineHeight: 1.05, tracking: "-0.012em", italic: true }
  display:{ fontFamily: "EB Garamond", cqw: 7.3, weight: 400, lineHeight: 1.02, tracking: "-0.022em" }
  number-hero:{ fontFamily: "EB Garamond", cqw: 9.4, weight: 400, lineHeight: 0.95, tracking: "-0.025em" }
  display-cover:{ fontFamily: "EB Garamond", cqw: 9.9, weight: 400, lineHeight: 0.98, tracking: "-0.028em" }
  number-unit:{ fontFamily: "JetBrains Mono", cqw: 2.08, weight: 500, lineHeight: 1.0 }

spacing:
  slide-pad: "4.2cqw"   # ~80px @1920
  gap-md: "1.7cqw"
  hairline: "1px"
  radius-sm: "6px"
  radius-md: "8px"
  radius-lg: "12px"
  radius-pill: "9999px"

components:
  card-hairline:
    backgroundColor: "{colors.cream} or {colors.tile}"
    border: "1px solid {colors.ink}@12%"
    rounded: "{spacing.radius-lg}"
    shadow: "{shadows.card}"
    typography: "{typography.card-title} + {typography.body}"
    description: "The editorial content card. Elevation is the hairline + ONE soft warm shadow — never a heavy drop, glow, or gradient."
  kicker-spike:
    typography: "{typography.kicker}"
    mark: "✱ coral spike prefix"
    description: "The eyebrow — JetBrains Mono uppercase, indexical (2–5 words), prefixed with the coral ✱. Never plain text, never a sentence."
  coral-callout:
    backgroundColor: "{colors.coral} (full-bleed) or {colors.cream} with a coral edge"
    textColor: "{colors.cream} on coral"
    rounded: "{spacing.radius-md}"
    typography: "{typography.button} / {typography.h2}"
    description: "The ONE voltage moment per frame — the CTA, the single inline link, OR the full-bleed band. Never two corals in one frame."
  number-lockup:
    typography: "{typography.number-hero} figure + {typography.number-unit} unit"
    description: "Hero stat — a EB Garamond figure paired with a JetBrains Mono unit (200K, +1,204, −318, 17 files). Figure is serif; the unit is ALWAYS mono, never the serif."
  pull-quote:
    typography: "{typography.quote-pull} (EB Garamond italic) + {typography.tag-upper} cite"
    description: "A commit message, a reviewer line, or the thesis. EB Garamond italic, small Inter uppercase cite beneath."
  section-rule:
    rule: "1px solid {colors.ink}@12% (or {colors.cream}@14% on navy)"
    description: "The only separator. A coral 1px rule may draw on to introduce a section. Never 2px+, never a heavy divider."
  code-surface:
    backgroundColor: "{colors.navy} body / {colors.navy-elev} title bar + status strip"
    textColor: "{colors.cream} (JetBrains Mono); syntax in coral (keywords) / teal #5DB8A6 (strings) / amber #E8A55A (numbers)"
    border: "1px solid {colors.cream}@14%"
    rounded: "{spacing.radius-md}"
    description: "The warm-navy code / terminal surface. This preset owns the surrounding surface, title bar, status strip, and mono chrome — not the code rendering itself."
  spike-mark:
    glyph: "✱ (U+2731), always {colors.coral}"
    description: "The brand mark. Fades + scales 0.92→1 on a single emphasis beat; never spins."
```

### Overview

Claude at frame scale is a **warm-editorial brand book come to life** — the register of a literary
imprint or a research note. The thesis is three colors: **cream is the ground, ink is the voice,
coral is the voltage** — and a fourth (warm navy) only where code shows itself. Every surface is
**warm cream** (never pure white, never cool gray); content gathers on a **tile** surface half a
step darker — the demarcation is a half-step, never a hard contrast. Elevation is a **1px hairline**
ink border at low alpha plus, rarely, one soft warm shadow. There are no heavy drops, no glows, no
gradients on content.

Three editorial voices, each in its own face: **EB Garamond** carries every display moment — covers,
headlines, pull-quotes, big stat numerals — at large display sizes with gentle negative tracking;
its **italic** is the expressive register. **Inter** carries body, leads, card titles, buttons, and
UI chrome. **JetBrains Mono** carries the indexical layer — kickers, technical labels, the code
window, status strips. Switching a voice's face collapses the register: a sans headline or a serif
label reads as a different brand.

**Key characteristics at frame scale:**

- **Cream / ink / coral trinity** + a warm-navy code surface; cream is the default ground, ink the voice, coral the scarce voltage.
- **EB Garamond** (sentence case, negative-tracked) for all display; **Inter** body/chrome; **JetBrains Mono** index + code.
- **Hairline elevation** — a 1px low-alpha ink border + at most one soft warm shadow. No heavy drop, glow, or gradient.
- **Coral is rationed** — at most ONE coral moment per frame (CTA, inline link, OR full-bleed band); coral never sets a headline or a body run.
- **Density is free** — fill the frame as the content wants; a frame may stand on a single focal or carry a dense, layered composition.
- **The ✱ coral spike** opens kickers; warm navy is reserved for the code/terminal surface.

### The Frame

**Frame Craft Bar:**

- **Squint** — one EB Garamond display moment dominates at 3–6× its neighbor.
- **Trinity** — cream/tile ground, ink text, coral exactly **once**; warm navy only on the code surface; no cool gray / pure white / fourth hue.
- **Type** — EB Garamond sentence-case display (negative-tracked); Inter 400 body; JetBrains Mono kickers (uppercase 0.16em, coral ✱) + code.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` ~4.2cqw; the kicker/mono chrome sit inside it.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Hairlines stay 1px; card radii stay
6/8/12px; the warm-paper reading must survive every ratio.

### Colors

Tokens identical to the source. Default ground `{colors.cream}`; content gathers on
`{colors.tile}` / `{colors.tile-strong}` (half-step warm steps, never a hard contrast).
**Headlines & body:** `{colors.ink}` on cream/tile; `{colors.cream}` on navy. **Coral**
(`{colors.coral}`) is the scarce voltage — one moment per frame (CTA, inline link, or full-bleed
band), never body text, never a card fill. **Warm navy** (`{colors.navy}` / `navy-soft` /
`navy-elev`) is the code / terminal / dark-card surface — a structural anchor, not a fourth brand
hue. **No cool grays, no pure white, no pure black.**

**Fixed syntax colors (decoration, NOT remixable brand hues).** When a code line is hand-set rather
than rendered by a code block, keywords are coral, strings are **teal `#5DB8A6`**, numbers are
**amber `#E8A55A`**; status reads success `#5DB872` / warn `#C64545`. These track the code surface,
not the brand trinity — keep them out of the brand palette.

### Typography

Two ramps. The **reading/chrome ramp** (Inter `body` 1.5cqw / `lead` 2.08cqw weight 400; JetBrains
Mono `kicker`/`mono-label` in px) carries copy + chrome; the **display ramp** (EB Garamond `headline` 4.6cqw
→ `display-cover` 9.9cqw, weight 400, negative-tracked) carries every headline + stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display-cover`; 4–6 → `display`; 7+ → `headline`. Reserve the 7.3–9.9cqw tier for cover / statement / stat.
- **EB Garamond display is sentence case** (NOT title case, NOT uppercase), weight 400, negative-tracked (−0.012..−0.028em); reach for **italic** when the line is a stance or a definition. **Inter body** sentence case weight 400. **JetBrains Mono** kickers UPPERCASE 0.16em with the coral ✱. No uppercase serif, no sans headline, no serif label.

### Depth & Surface

Hairline elevation:

- **1px hairline** ink border at ~12% alpha is the primary lift (cream@14% on navy).
- **One soft warm shadow** (`0 1px 3px ink@8%, 0 4px 16px ink@4%`) — used rarely, never heavy.
- **Half-step surface** — a `{colors.tile}` block on cream reads elevated by the warm step, not by a cast shadow.

**Ceiling:** no heavy drop shadow, no glow, no gradient on content, no tilt. The system has no light
to emit; it reads by warmth and hairline.

### Shapes

- **6px** small chrome, **8px** cards / code surface, **12px** large cards / quote frames, **9999px** true pills only. No square corners, no heavy rounding; the editorial register is gently rounded, never hard.

### Components

- **card-hairline** — the editorial content card (hairline + one soft shadow). **section-rule** — the only separator (1px, coral may draw on).
- **kicker-spike** — the ✱ coral eyebrow. **coral-callout** — the one voltage moment (CTA / inline link / full-bleed band).
- **number-lockup** — EB Garamond figure + mono unit (the PR `+N / −M`, `200K`, file counts). **pull-quote** — EB Garamond italic + cite (a commit message / reviewer line).
- **code-surface** — the warm-navy code / terminal surface; the code content itself is rendered by a dedicated code-block component, this owns the surface + mono chrome.
- **spike-mark** — the ✱ brand glyph, always coral.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · Fixed/Free · density.
> One coral moment per frame; open with a kicker-spike.

**1 · Cover** (identity · move: oversized EB Garamond · cream). **Ground** `{colors.cream}`, `slide-pad`. **Composes** kicker-spike, display-cover, lead, mono-label index. **Focal** a 2–3 line EB Garamond `display-cover` (sentence case, ink) under a coral ✱ kicker. **Chrome** mono index strip (repo · branch). **Accent** the single coral ✱. **Fixed** EB Garamond 400 sentence case, hairline, cream ground. **Free** title, the mono index, layout + how full the frame runs. **Density** free.

**2 · Statement** (statement · move: single EB Garamond line · cream or navy). **Ground** `{colors.cream}` (or `{colors.navy}` for gravity). **Composes** kicker-spike, display, optional lead. **Focal** one 2-line EB Garamond `display` carrying the change in a sentence — reach for italic if it's a stance. **Chrome** mono kicker. **Accent** none — the serif carries it (or one coral word). **Fixed** sentence-case serif. **Free** the line, ground, layout + density. **Density** free.

**3 · Code Surface** (code · move: warm-navy code window · the PR-critical frame). **Ground** `{colors.cream}` framing a `{colors.navy}` code-surface (8px, cream@14% hairline, `navy-elev` title bar + filename in mono). **Composes** mono-label filename, the code block (diff / before→after / typed-on snippet), optional `section-rule`. **Focal** the code panel — the diff / before→after / typed-on snippet. **Chrome** mono filename + status strip. **Accent** syntax coral/teal/amber inside the panel; one coral marker outside (e.g. a `+`/`−` gutter cue). **Fixed** warm-navy surface, mono code, hairline. **Free** which code treatment, the code content (from the diff), how large the panel runs. **Density** dense.

**4 · Number / Impact** (data · move: oversized figure · cream). **Ground** `{colors.cream}`, `slide-pad`. **Composes** kicker-spike, number-lockup, lead/caption, optional `section-rule`. **Focal** a EB Garamond `number-hero` figure with a mono unit over a 1px rule — the PR impact (`+1,204 / −318`, `17 files`, `2.1× faster`). **Chrome** mono tag. **Accent** the figure in ink; at most one coral unit. **Fixed** serif figure + mono unit, hairline rule. **Free** the figures (from the script), tag, layout + density. **Density** free.

**5 · Pull-quote** (quote · move: EB Garamond italic · cream). **Ground** `{colors.cream}`. **Composes** kicker-spike, pull-quote, tag-upper cite. **Focal** a EB Garamond italic `quote-pull` — a commit message, a reviewer line, or the thesis — with a small Inter uppercase cite (author · role) beneath. **Chrome** mono kicker. **Accent** none, or one coral mark. **Fixed** EB Garamond italic quote + uppercase cite. **Free** quote, attribution, layout + density. **Density** free.

**6 · Closing / CTA** (closer · move: coral voltage · cream or navy). **Ground** `{colors.cream}` (or `{colors.navy}`). **Focal** a short EB Garamond sign-off with the one coral-callout (the CTA or full-bleed band) and, for a "shipped-by" close, a row of hairline-ringed avatar chips. **Composes** display sign-off, coral-callout, optional contributor row. **Chrome** mono index. **Accent** the single coral voltage. **Fixed** one coral moment, hairline avatar rings, sentence-case serif. **Free** sign-off, who ships, layout + density. **Density** free.

### Composition Rules

**Do:** stand every frame on the warm cream floor, gather content on a half-step tile surface; set all display in EB Garamond sentence case negative-tracked, Inter 400 body, JetBrains Mono kickers (uppercase 0.16em, coral ✱) + code; ration coral to one moment per frame — CTA, inline link, OR full-bleed band; elevate with a 1px hairline + at most one soft warm shadow, reserve warm navy for the code/terminal surface; lead with one clear focal, open regions with a kicker-spike, fill the frame as the content wants; pair a EB Garamond figure with a mono unit for every stat.

**Don't:** use pure white, cool gray, or pure black; add a fourth brand hue (navy is structural, syntax colors are decoration); use a heavy drop shadow, glow, gradient on content, or tilt; set EB Garamond display uppercase or title-case; use a sans headline, a serif label, or a serif-set numeric unit; use two coral moments in one frame or let coral set a headline/body run; blow a headline past the measure.

### Aspect-Ratio Behavior

| Treatment       | 16:9                       | 9:16                              | 1:1                       |
| ----------------- | ----------------------------- | ------------------------------------ | ---------------------------- |
| Cover             | display left, index top       | display top, index below             | display, index corner        |
| Statement         | line left/centered            | line stacked                         | centered                     |
| Code Surface      | panel framed in cream         | panel taller, fewer lines            | panel centered, square       |
| Number/Impact     | figure left                   | figure centered, taller              | centered                     |
| Pull-quote        | quote left                    | quote stacked                        | centered                     |
| Closing/CTA       | sign-off + avatar row         | sign-off top, avatars below          | centered, avatars wrap       |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. The code surface keeps
its hairline + mono chrome on every ratio; the avatar row wraps rather than shrinks below legibility.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Contributor avatars come from the project's own asset store (staged from the PR's
people graph); the ✱ spike, hairlines, and the code surface are CSS-only and need no external imagery.

### Numerals & Claims (hard rule)

Never invent figures, stats, diffs, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `+N / −M`. Number-lockups, code panels, and impact stats carry placeholders until the
script (from the PR ingest) supplies real values. Branch names, file counts, and `+/−` totals trace
to the diff; commit/issue numbers are chrome.

### Pre-Render Self-Audit

- **Squint** — one EB Garamond display moment dominates.
- **Trinity** — cream floor + tile step + ink voice; coral appears exactly once; warm navy only on the code surface; no cool gray / pure white / fourth hue.
- **Type** — EB Garamond sentence-case display (negative-tracked); Inter 400 body; JetBrains Mono kickers (uppercase 0.16em, coral ✱) + code; ≥1.4cqw floor.
- **Depth** — 1px hairline + at most one soft warm shadow; no heavy drop / glow / gradient / tilt; 6/8/12px radii.
- **Code** — code rendered by a dedicated code-block on the warm-navy surface; syntax coral/teal/amber; figures paired with a mono unit.
- **Fabrication** — every numeral / diff traces to the PR, else placeholder.

### Known Gaps

- Motion intentionally out of scope. Claude's motion register (short cross-dissolves, no
  overshoot/bounce/elastic, coral the only "draw-on", numbers count up, code types on line by
  line) lives in the animation-focused part of the pipeline, not here.
- EB Garamond + Inter + JetBrains Mono ship as licensed local WOFF2 assets bundled with this
  preset (weights 400 + 700, staged into an `assets/fonts/` directory with the matching
  `@font-face` block, so renders resolve offline without a first-run Google Fonts fetch). Author
  display at weight 400 (700 reads as a heavy bold, off-register); treat italic as the
  browser-synthesized slant, acceptable for the pull-quote register. EB Garamond is a warm
  old-style serif (low contrast, humanist); if it ever fails, fall back to Georgia or another
  old-style serif — never to a sans. CJK: Noto Serif SC (display) / Noto Sans SC (body) / Noto
  Sans Mono CJK (code); the sentence-case warmth carries when the serif drops.
- Syntax colors (teal `#5DB8A6` / amber `#E8A55A` / status) are fixed decoration, declared in
  §Colors — they are NOT in the remixable `colors:` block, so a brand remix never repaints them.
- The code content itself is rendered by a dedicated code-block component, not this preset — this
  preset owns only the surrounding warm-navy surface + mono chrome.
- 9:16 / 1:1 are guidance; verify the legibility floor and that the cream/tile warmth +
  one-coral discipline hold per ratio.

---

## Preset: Editorial Forest

```yaml
version: alpha
name: Editorial Forest — Frame (video / frame layer)
description: >
  Video-first companion to Editorial Forest's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — the green/pink/cream editorial triad, Source Serif 4 at weight 500
  (optical-size axis) for all display + JetBrains Mono 500 uppercase chrome, flat paper depth (no
  shadows), 2px hairline rules, 6/8px card radii, and the monogram circle stamp. Composition + frame
  scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  green: "#2e4a2a"
  green-deep: "#243a21"
  green-lite: "#3a5a36"
  pink: "#e89cb1"
  pink-deep: "#d27e96"
  cream: "#efe7d4"
  cream-2: "#e6dcc4"
  ink: "#1a1a17"

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Source Serif 4", cqw: 1.56, weight: 400, lineHeight: 1.38 }
  body-card:{ fontFamily: "Source Serif 4", cqw: 1.35, weight: 400, lineHeight: 1.34 }
  label:   { fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  caption-mono:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 500, tracking: "0.14em", upper: true }
  # — display ramp (Source Serif 4 weight 500, opsz, negative tracking) —
  title-card-sm:{ fontFamily: "Source Serif 4", cqw: 2.9, weight: 500, lineHeight: 0.98, tracking: "-0.01em" }
  title-card:{ fontFamily: "Source Serif 4", cqw: 3.5, weight: 500, lineHeight: 0.96, tracking: "-0.01em" }
  headline:{ fontFamily: "Source Serif 4", cqw: 4.4, weight: 500, lineHeight: 1.0, tracking: "-0.02em" }
  headline-xl:{ fontFamily: "Source Serif 4", cqw: 5.0, weight: 500, lineHeight: 0.96, tracking: "-0.02em" }
  display:{ fontFamily: "Source Serif 4", cqw: 7.3, weight: 500, lineHeight: 1.02, tracking: "-0.02em" }
  display-hero:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.02em" }
  stat-figure:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.03em" }
  stat-figure-unit:{ fontFamily: "Source Serif 4", cqw: 5.7, weight: 500, lineHeight: 0.92 }
  name:    { fontFamily: "Source Serif 4", cqw: 2.3, weight: 600, lineHeight: 1.0 }

spacing:
  slide-pad: "5cqw"
  rule: "2px"
  rule-card: "2.5px"
  radius-card: "6px"
  radius-step: "8px"

components:
  topbar:
    typography: "{typography.label} (JetBrains Mono) + monogram-circle or counter"
    placement: "top edge, label left, mark right"
    description: "On EVERY frame — the system's spine; a frame without it reads untreated."
  footline:
    typography: "{typography.caption-mono} ×2, space-between"
    placement: "absolute bottom edge"
    description: "On cover/data/summary frames."
  monogram-circle:
    border: "2px solid {colors.pink}"
    rounded: "50%"
    size: "130px"
    typography: "mono monogram"
    description: "The identity stamp. Cover/summary only."
  topic-tile:
    backgroundColor: "{colors.green} (pink text) / {colors.pink} (green-deep) / {colors.green-lite} (pink) / {colors.cream-2} + 2px {colors.green} border (green)"
    rounded: "{spacing.radius-card}"
    shadow: "none"
    typography: "{typography.caption-mono} ordinal + {typography.title-card-sm} + mono foot"
    description: "Fills rotate; never repeat one across a grid."
  step-tile:
    backgroundColor: "{colors.cream} + green border / {colors.green} / {colors.pink}"
    border: "2.5px solid"
    rounded: "{spacing.radius-step}"
    typography: "mono ordinal + {typography.title-card} + {typography.body-card} + mono marker over a top rule"
    description: "Framework/process card."
  kpi-block:
    typography: "{typography.caption-mono} tag → {typography.stat-figure} (+{typography.stat-figure-unit}) → {typography.body}"
    rule: "2px accent rule above"
    description: "Oversized serif figure."
  meta-dl:
    borderTop: "2px solid {colors.green}"
    typography: "{typography.caption-mono} dt + {typography.meta-value} dd"
    description: "3-column dt/dd grid."
  bar:
    backgroundColor: "{colors.pink} / {colors.cream} / {colors.green}"
    rounded: "3px 3px 0 0"
    size: "56px wide"
    typography: "mono value above"
    description: "Vertical chart bar."
  rule-thin:
    rule: "2px solid (green on cream / pink on green / green-deep on pink)"
    description: "The only separator. Never 1px, never 3px+."
```

### Overview

Editorial Forest at frame scale is a **serif-led literary-editorial system** — the register of a
Penguin classic or a quiet annual report. One confident voice, **Source Serif 4 at weight 500**
(optical-size axis engaged), carries every headline and stat up to ~12cqw; **JetBrains Mono** at
weight 500 uppercase is the editorial chrome (labels, captions, axis ticks, footlines). Three
surfaces — forest green, dusty rose, oat cream — and nothing else. Depth is **flat and paper-based**:
no shadows, no gradients; elevation is color-block contrast + 2px hairlines + border-vs-fill.

The unmistakable signature is **weight 500** (never 400 display, never 700) and the **mono/serif
role inversion** (mono for chrome, serif for body and display). Body text drops to serif weight
400 — that 500→400 step is the reading rhythm. Every frame carries a mono topbar; the monogram
circle is the identity stamp.

**Key characteristics at frame scale:**

- **Green / pink / cream triad** — two surface tones per frame is typical, three is loud.
- **Source Serif 4 weight 500** (opsz, negative tracking) for all display; **serif 400** body; **JetBrains Mono 500** uppercase chrome.
- **Flat — no shadows, no gradients**; elevation is color-block + 2px hairline + border-vs-fill.
- **2px hairline rules** are the only separator (2.5px on step tiles); 6/8px card radii; the monogram circle is the only full round.
- **Topbar on every frame** (mono label + monogram/counter); footline on data/cover frames.
- **Spacious & committed** — one subject per frame in deep negative space; fewer elements at larger sizes.

### The Frame

**Frame Craft Bar:**

- **Squint** — one Source Serif 4 moment dominates at 3–6× its neighbor; the surface block centers the eye.
- **Silence** — one subject per frame in deep negative space; the **topic-tile and step grids are the one dense exception**.
- **Restraint** — **two surface tones max** per frame (three is loud); serif **weight 500** display / **400** body; green ground reserved for gravity moments.
- **Reference** — aim at a **Penguin classic / quiet annual report / art-book spread**; failure looks like a **shadowed, multi-color web dashboard**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` 5cqw; the topbar/footline sit inside it.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Hairlines stay 2px; card radii stay 6/8px.

### Colors

Tokens identical to the source. Default ground `{colors.cream}` for content; `{colors.green}` for
cover/statement/summary gravity. **Headlines:** green on cream, cream (or pink at hero scale) on
green, green-deep on pink. **Body:** ink on cream, cream on green, green-deep on pink. Labels/rules
take the region's accent (pink on green, green on cream, green-deep on pink). Tile fills rotate
green / pink / green-lite / cream-2-with-green-border. **No fourth color family** — the triad +
near-duplicates is the whole palette; never `rgba` transparency on a surface.

### Typography

Two ramps. The **reading/chrome ramp** (Source Serif 4 **400** body 1.56cqw; JetBrains Mono labels
in px) carries copy + chrome; the **display ramp** (Source Serif 4 **500** `title-card-sm` 2.9cqw →
`display-hero`/`stat-figure` 11.5cqw, opsz, negative-tracked) carries every headline + figure.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `display-hero`; 4–6 → `headline-xl`; 7+ → `headline`. Reserve the 7.3–11.5cqw tier for statement/stat/cover.
- **Serif is weight 500 for display, 400 for body** (the rhythm), 600 only for an attribution name. Negative tracking (−0.01..−0.03em), tight line-height (0.92–1.02). **Mono uppercase, 0.08–0.18em.** No italic, no underline, no third face, no serif body at 500.

### Depth & Surface

Flat, paper-based. Elevation from:

- **Color-block contrast** — a green tile on cream reads elevated by ink-block separation.
- **2px hairline rules** — section separators in the region's accent.
- **Border vs fill** — a cream-2 tile + 2px green border reads a different elevation than a solid tile.

**Ceiling:** zero shadow (adding `box-shadow` shatters the paper feel), no gradient, no glow; surfaces are solid ink-on-paper.

### Shapes

- **6px** topic tiles, **8px** step tiles, **2px** legend swatch, **3px 3px 0 0** bar tops, **50%** monogram circle. No square corners, no heavy rounding.

### Components

- **topbar** (the spine) + **footline** + **monogram-circle** (identity stamp) — the chrome set.
- **topic-tile** (6px, rotating fills) / **step-tile** (8px, 2.5px border) — the catalog + framework patterns.
- **kpi-block** (oversized serif figure) / **meta-dl** (3-col, 2px rule) / **bar** / **rule-thin** — data + structure.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Topbar on every frame; one subject per frame in deep negative space.

**1 · Cover** (identity · move: oversized serif · green · left). **Ground** `{colors.green}`, `slide-pad`. **Composes** topbar (mono label + monogram-circle), display-hero, body lede, footline. **Focal** a 2-line Source Serif 4 `display-hero` in pink (one word in cream), left. **Chrome** mono topbar; mono footline. **Accent** pink display + the monogram circle. **Silence** ~50%. **Fixed** serif 500, flat, monogram 2px pink. **Free** title, which word is cream. **Density** low.

**2 · Topic Tiles** (catalog · move: rotating-fill grid · cream · the dense frame). **Ground** `{colors.cream}`, `slide-pad`. **Composes** topbar, headline-xl, 3–4× topic-tile. **Focal** a row of 6px tiles, fills rotating green / pink / cream-2-with-border, each a mono ordinal + serif title. **Chrome** mono topbar. **Accent** the tile fills (mix 3 of 4, never repeat one). **Silence** tight — the density exception. **Fixed** 6px radius, rotating fills, no shadow. **Free** tile titles, which fills. **Density** dense-exception.

**3 · KPI Stat** (data · move: oversized figure · green). **Ground** `{colors.green}`, `slide-pad`. **Composes** topbar, kpi-block (mono tag + 220px stat-figure + serif description), footline. **Focal** a Source Serif 4 `stat-figure` (~11.5cqw, +unit) in pink over a 2px pink rule. **Chrome** mono topbar + footline. **Accent** the pink figure. **Silence** ~55%. **Fixed** serif 500 figure, 2px accent rule, flat. **Free** the figure (from script), tag, description. **Density** low.

**4 · Statement** (quote · move: display serif · cream · left). **Ground** `{colors.cream}`, generous pad. **Composes** topbar, display, name (600), caption-mono role. **Focal** a 2-line Source Serif 4 `display` (~7.3cqw) in green; a 600-weight attribution name + mono role beneath. **Chrome** mono topbar. **Accent** none — the serif carries it. **Silence** ~55%. **Fixed** serif 500 display + 600 name only, no italic. **Free** quote, name, role. **Density** low.

**5 · Step Framework** (process · move: 8px step tiles · cream/green). **Ground** `{colors.cream}` (or green), `slide-pad`. **Composes** topbar, headline, 3–4× step-tile. **Focal** a row of 8px step tiles (2.5px border) — mono ordinal + serif 68px title + body + mono marker over a top rule; fills rotate cream-with-green-border / green / pink. **Accent** the tile fills. **Silence** moderate. **Fixed** 8px radius, 2.5px border, mono markers. **Free** steps, fills. **Density** standard.

**6 · Chart** (data · move: bars + meta · green). **Ground** `{colors.green}`, `slide-pad`. **Composes** topbar, headline, bars + 2px axis rules, meta-dl. **Focal** 56px pink/cream/green bars on inner-edge 2px rules with mono ticks; an optional 3-col meta-dl beneath. **Chrome** mono topbar. **Accent** the bar fills. **Silence** moderate. **Fixed** 56px bars, 3px tops, 2px axes, mono ticks. **Free** values (from script), labels. **Density** standard.

### Composition Rules

**Do:** run every display in Source Serif 4 weight 500 (opsz, negative-tracked, tight line-height), body at 400; set every label/caption/axis/footline in JetBrains Mono 500 uppercase 0.08–0.18em; give every frame a topbar (mono label + monogram or counter), footline on data/cover; pick one dominant surface per frame (max two tones), rotate tile fills (never repeat one across a grid); separate sections with 2px hairlines in the region's accent, reserve the monogram circle for cover/summary; scale display aggressively (7.3–11.5cqw) for statement/stat/cover, lean left/editorial, one subject per frame.

**Don't:** use box-shadow, gradient, or glow; use a third typeface, italic, underline; use serif body at 500 or mono at headline scale; use a fourth color family or `rgba` surfaces; use 1px or 4px+ rules (2px / 2.5px only); put two competing content blocks on one frame; omit the topbar; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment        | 16:9                                 | 9:16                            | 1:1                          |
| ------------------- | --------------------------------------- | ---------------------------------- | -------------------------------- |
| Cover               | display left, monogram top-right        | display top, monogram below        | display, monogram corner         |
| Topic Tiles         | 3–4 across                              | stacked                            | 2×2                              |
| KPI Stat            | figure left                             | figure centered, taller            | centered                         |
| Statement           | quote left                              | quote stacked                      | centered                         |
| Step Framework      | 3–4 across                              | stacked                            | 2×2                              |
| Chart               | bars + meta                             | bars taller, meta stacks           | square chart                     |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. Topbar spans the top
on every ratio; the monogram may drop to a corner.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The monogram, footline strings, and tile counters carry per-deck identity; figures are content.

### Numerals & Claims (hard rule)

Never invent figures, KPIs, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `— %`. Issue numbers / counters are decorative chrome.

### Pre-Render Self-Audit

- **Squint** — one serif moment dominates; the surface block centers the eye.
- **Silence** — one subject per frame in deep negative space; only the topic-tile/step grids run dense.
- **Triad** — two surface tones max; headlines/body/labels use the correct per-surface color; no fourth family.
- **Type** — Source Serif 4 500 display (opsz, negative-tracked) / 400 body; mono uppercase 0.08–0.18em; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 gradient; 2px hairlines; 6/8px radii; monogram the only full round.
- **Chrome** — topbar present on every frame; footline on data/cover.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source relies on deck-navigation scaling, no transition spec.
- Source Serif 4 (opsz 8..60) + JetBrains Mono via Google Fonts — the optical-size axis is critical;
  a non-opsz fallback flattens the size-aware letterforms. CJK: LXGW WenKai (display) / Noto Serif
  SC (body) / Noto Sans Mono CJK (chrome).
- 9:16 / 1:1 are guidance; verify the floor and that two-tone discipline holds per ratio.
- Bars, hairlines, tiles, and the monogram circle are CSS-only; no external imagery is required.
- Contrast: green-on-pink / pink-on-green only at display scale (84px+); keep small text
  cream-on-green or ink-on-cream.

---

## Preset: BlockFrame

```yaml
version: alpha
name: BlockFrame — Frame (video / frame layer)
description: >
  Video-first companion to BlockFrame's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — 4px black borders + 8px hard offset shadows, the five-pastel candy palette
  (pink/blue/green/yellow/cream) plus black/white/off-white, Inter 800–900 uppercase display +
  Space Grotesk label chrome, square corners, label-pills, tilted decorations, star bursts, stripe
  blocks, dot grids. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  black: "#000000"
  white: "#FFFFFF"
  offwhite: "#FFFDF5"
  pink: "#FE90E8"
  blue: "#C0F7FE"
  green: "#99E885"
  yellow: "#F7CB46"
  cream: "#FFDC8B"

borders: { primary: "4px solid black", thin: "3px solid black" }
shadows: { default: "8px 8px 0 black", small: "4px 4px 0 black", hover: "6px 6px 0 black", close-yellow: "12px 12px 0 yellow", close-white: "6px 6px 0 white" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  card-title:{ fontFamily: "Inter", cqw: 1.15, weight: 700, upper: true, lineHeight: 1.2 }
  label:   { fontFamily: "Space Grotesk", px: 13, weight: 600, tracking: "0.08em", upper: true }
  counter: { fontFamily: "Space Grotesk", px: 14, weight: 700, tracking: "0.1em", upper: true }
  # — display ramp (Inter 800–900, uppercase, negative tracking) —
  heading-md:{ fontFamily: "Inter", cqw: 2.1, weight: 700, lineHeight: 1.1, tracking: "-0.01em", upper: true }
  quote-text:{ fontFamily: "Inter", cqw: 2.7, weight: 900, lineHeight: 1.15, tracking: "-0.02em", upper: true }
  stat-number:{ fontFamily: "Inter", cqw: 3.3, weight: 900, lineHeight: 1.0 }
  heading-lg:{ fontFamily: "Inter", cqw: 3.3, weight: 800, lineHeight: 1.0, tracking: "-0.02em", upper: true }
  close-title:{ fontFamily: "Inter", cqw: 4.2, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }
  heading-xl:{ fontFamily: "Inter", cqw: 5.0, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }

spacing:
  slide-pad: "3.1cqw"   # 60px @1920
  gap-md: "1.7cqw"

components:
  card-elevated:
    backgroundColor: "{colors.white}"
    border: "0.4cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.8cqw 0.8cqw 0 {colors.black}"
    description: "Primary card. Border/shadow coupled: 4px↔8px, 3px↔4px."
  card-small:
    backgroundColor: "{colors.white}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    description: "Stat cards, team cards, timeline steps."
  label-pill:
    border: "0.3cqw solid {colors.black}"
    backgroundColor: "any pastel / {colors.white}"
    rounded: "9999px"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "{typography.label}"
    description: "The universal eyebrow — never plain text."
  button-primary:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.black}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "Inter 700"
    description: "The CTA."
  star-burst:
    backgroundColor: "any pastel"
    border: "0.3cqw solid {colors.black}"
    clip: "10-point clip-path star"
    description: "Corner attention-grabber."
  stripe-block:
    backgroundImage: "45° {colors.black} + pastel diagonal stripes"
    border: "0.3cqw solid {colors.black}"
    description: "Poster decoration."
  bg-dot-grid:
    backgroundImage: "radial-dot ~1.2px dots, 24px grid, {colors.black}"
    description: "Faint corner/ground overlay."
  tilt-deco:
    transform: "rotate(±2°–12°)"
    description: "Rotated rectangle/badge/star. Stat cards alternate −2/+2°. The grid-puncture signature."
  stat-deco-dot:
    backgroundColor: "any pastel"
    border: "2px solid {colors.black}"
    rounded: "50%"
    size: "12px"
    description: "The ONLY round shape, pinned to stat cards."
  close-frame:
    backgroundColor: "{colors.black}"
    textColor: "{colors.white}"
    border: "0.4cqw solid {colors.white}"
    rounded: "0"
    shadow: "1.2cqw 1.2cqw 0 {colors.yellow}"
    description: "Inverted closer — the only colored shadow."
```

### Overview

BlockFrame at frame scale is a **maximalist neobrutalist** system on five laws: every region has a
4px black border, every elevated element an 8px hard offset shadow, every corner square, every
accent a saturated pastel, and every layout allowed to be a little crooked. The joy is the
deliberate collision — bordered cards meeting bordered cards, shadows stacking, tilted decorations
puncturing the grid.

The voice is **Inter** at weight 800–900 in tight uppercase with negative tracking (display) +
weight 500 sentence body, and **Space Grotesk** weight 600 uppercase 0.08em as the label/chrome
voice. Five candy pastels (pink/blue/green/yellow/cream) cycle as full-bleed grounds across frames
— the color cycling is the primary rhythm. Depth is **hard offset shadow** (8px/4px, solid black,
zero blur, bottom-right); the close-frame's 12px yellow shadow is the one colored exception.

**Key characteristics at frame scale:**

- **4px black borders + 8px hard shadows** on primary cards; 3px + 4px on chrome (weights coupled).
- **Five-pastel palette** cycled as full-bleed grounds; black/white/off-white structural.
- **Inter 800–900 uppercase** negative-tracked display; **Space Grotesk** label chrome.
- **Square corners** everywhere (only the stat-deco dot is round); **tilted decorations** puncture the grid.
- **Label-pills** open every region; star bursts, stripe blocks, dot grids are reusable attention units.
- **Comfortably dense** — packed reads as authoritative; empty corners read as broken.

### The Frame

**Frame Craft Bar:**

- **Squint** — one Inter display moment dominates at 3–6× its neighbor; cards read as a system, not rivals.
- **Silence** — cover/quote/close keep air (decorations, not content); the **feature-card and stat grids are the dense exception**.
- **Restraint** — the 4px→8px / 3px→4px coupling holds; black borders only (white on close); pastel ground cycles one per frame; no sixth pastel.
- **Reference** — aim at a **zine / 1990s sticker-book / toy-packaging spread**; failure looks like a **flat, borderless, blurred-shadow web card grid**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `slide-pad` ~3.1cqw; decorations may bleed off edges.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders/shadows scale in `cqw` so the
4px↔8px coupling holds proportionally; corners stay square.

### Colors

Tokens identical to the source. `{colors.offwhite}` is the default ground, but frames **cycle**
through `{colors.cream}`/`blue`/`pink`/`green`/`yellow` grounds — the cycle is the rhythm.
`{colors.black}` is every border + structural text; `{colors.white}` is card fills. The five pastels
are interchangeable with **no semantic meaning** — pair by juxtaposition (pink+blue+green trio,
cream+yellow warm pair). `{colors.yellow}` is the CTA + the one colored (close) shadow;
`{colors.black}` ground is the close surface. **No sixth pastel.**

### Typography

Two ramps. The **reading/chrome ramp** (Inter body 0.95cqw weight 500, Space Grotesk labels in px)
carries copy + chrome; the **display ramp** (Inter `heading-md` 2.1cqw → `heading-xl` 5cqw, weight
800–900 uppercase) carries every headline + stat.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `heading-xl`; 4–6 → `heading-lg`; 7+ → `heading-md`.
- **Inter display is uppercase, weight 800–900, negative-tracked** (−0.01..−0.03em); body weight 500 sentence case; **Space Grotesk labels uppercase 0.08em**. No sentence-case display, no untracked display.

### Depth & Surface

Hard offset shadow, solid black, zero blur, bottom-right:

- **0.8cqw (8px)** primary cards; **0.4cqw (4px)** chrome; **0.6cqw (6px)** hover.
- **Border-based depth** — the 4px/3px borders do much of the lift; shadow makes it "elevated."
- **Tilt** — ±2°–12° rotation breaks the grid for perceived dimension.
- **Inverted close** — 12px YELLOW shadow (and 6px white on close-btn) — the only colored shadows.

**Ceiling:** no blurred shadow, no rounded corner (save the stat-deco dot), no gradient depth.

### Shapes

- **0 radius everywhere** except the 12px stat-deco dot (50%). Square corners are the structural identity.

### Components

- **card-elevated / card-small** — the bordered+shadowed content cards (weight-coupled).
- **label-pill** — the universal eyebrow (border+shadow+pastel). **button-primary** — yellow CTA.
- **star-burst / stripe-block / bg-dot-grid / tilt-deco** — the reusable decoration units (one per frame min).
- **stat-deco-dot** — the lone round shape. **close-frame** — the inverted black+white+yellow-shadow closer.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Cycle the ground color; add ≥1 decoration per frame; open with a label-pill.

**1 · Cover** (identity · move: decorations puncture · left). **Ground** `{colors.cream}` (or offwhite) + faint dot-grid. **Composes** label-pill, heading-xl, tilt-deco rect, star-burst, counter. **Focal** a 2–3 line Inter `heading-xl` uppercase, left, under a label-pill; tilted pastel rects + a star burst puncture the right. **Chrome** counter pill. **Accent** the decorations' pastels. **Silence** right third holds decorations. **Fixed** 4px/8px coupling, uppercase display, square. **Free** title, decoration placement/colors. **Density** comfortable.

**2 · Feature Cards** (catalog · move: 3-up bordered grid · blue ground). **Ground** `{colors.blue}`, `slide-pad`. **Composes** label-pill, heading-lg, 3× card-elevated (icon-square + card-title + body). **Focal** three white bordered+shadowed cards. **Chrome** label-pill eyebrow. **Accent** the pastel icon-squares (pink/green/yellow). **Silence** tight — dense by design. **Fixed** 4px border + 8px shadow, square, uppercase card-titles. **Free** card content, icon hues. **Density** dense-exception.

**3 · Stat Grid** (data · move: tilted stat cards · green ground). **Ground** `{colors.green}`, `slide-pad`. **Composes** label-pill, heading-lg, 3× card-small (tilted −2/+2°, stat-deco dot, stat-number + label). **Focal** three tilted bordered stat cards. **Accent** the deco-dots' pastels + black stat numerals. **Silence** moderate. **Fixed** alternating tilt, 3px+4px, round deco-dot only. **Free** figures (from script), dot hues. **Density** dense-exception.

**4 · Closing Plate** (closer · move: inverted black · centered). **Ground** `{colors.black}`. **Composes** close-frame (4px white border, 12px yellow shadow), label-pill (inverted), close-title, star-burst. **Focal** a white `close-title` inside the white-bordered frame with the yellow offset shadow; a pink star punctures a corner. **Accent** the yellow shadow + pink star. **Silence** ~50%. **Fixed** white-on-black, 12px yellow shadow (only here), square. **Free** sign-off, star placement. **Density** low.

**5 · Quote** (quote · move: bordered quote frame · pink ground). **Ground** `{colors.pink}` (or offwhite). **Composes** label-pill, quote-text in a card-elevated, attribution. **Focal** an Inter `quote-text` (900 uppercase) inside a white bordered+shadowed frame. **Accent** the ground + one decoration. **Silence** moderate. **Fixed** uppercase quote, 4px/8px. **Free** quote, ground. **Density** comfortable.

**6 · Timeline** (process · move: stepped bordered cards · offwhite). **Ground** `{colors.offwhite}`. **Composes** label-pill, heading-lg, 3–4 card-small steps + step-connectors. **Focal** a row of bordered step cards linked by black connector bars, each a pastel + step-num. **Accent** the step pastels. **Silence** moderate. **Fixed** 3px+4px steps, square, connectors. **Free** steps, hues. **Density** standard.

### Composition Rules

**Do:** pair 4px borders with 8px shadows, 3px with 4px (the coupling is non-negotiable); cycle pastel grounds across frames to keep the deck visually rhythmic; set Inter display uppercase, 800–900, negative-tracked; open every region with a label-pill; render shadows solid black, zero blur, bottom-right; add ≥1 decoration (tilt/star/stripe/dots) per frame; use yellow for CTAs; use the inverted black + 12px yellow shadow close-frame for the closer; tilt decorations ±2°–12°; lean left on most frames.

**Don't:** use rounded corners (save the stat-deco dot); use blurred shadows; use colored borders (black only, save the close-frame white); use a sixth pastel; set Inter display sentence-case or untracked; treat a label as plain text; keep everything perfectly aligned (tilt is the signature); leave corners empty; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment       | 16:9                              | 9:16                              | 1:1                          |
| ----------------- | ------------------------------------ | ------------------------------------ | -------------------------------- |
| Cover             | title left, decorations right        | title top, decorations below         | title, fewer decorations         |
| Feature Cards     | 3 across                             | 3 stacked                            | 2+1                              |
| Stat Grid         | 3 tilted across                      | 3 tilted stacked                     | 2×2                              |
| Closing           | centered close-frame                 | centered, taller                     | centered                         |
| Quote             | quote frame                          | quote stacked                        | centered                         |
| Timeline          | horizontal steps                     | vertical (connectors hidden)         | 2×2                              |

`slide-pad` holds on the short edge; re-step display above the 1.4cqw floor. Decoration count drops
on tighter ratios so the frame stays bordered, not cluttered.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Pastel fills, decorations, and tilts are content-agnostic.

### Numerals & Claims (hard rule)

Never invent figures, stats, or counts at frame scale. Render slots as `— figure —`, `{metric}`,
`N×`. Slide counters and list numbers are decorative.

### Pre-Render Self-Audit

- **Squint** — one Inter display moment dominates; cards read as a system.
- **Silence** — only feature/stat grids run dense; cover/quote/close keep air with decorations.
- **Borders/shadows** — 4px↔8px / 3px↔4px coupling holds; solid black, zero blur.
- **Color** — pastel ground cycles; black borders only (white on close); no sixth pastel.
- **Type** — Inter uppercase 800–900 negative-tracked, fit-to-measure; Space Grotesk labels 0.08em; ≥1.4cqw floor.
- **Shape** — square corners (only stat-deco dot round); ≥1 tilt/decoration per frame.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source toggles between states via display, no transition.
- Inter + Space Grotesk via Google Fonts. CJK: Noto Sans SC 900 (sentence case — the uppercase
  signal drops); lean harder on borders/shadows/decoration to carry the brutalist identity.
- 9:16 / 1:1 are guidance; verify the floor and that decoration count scales down.
- Star bursts (clip-path), stripe blocks, dot grids, and tilts are CSS-only; no external imagery is required.

---

## Preset: Blue Professional

```yaml
version: alpha
name: Blue Professional — Frame (video / frame layer)
description: >
  Video-first companion to Blue Professional's design.md. The unit is the frame (1920×1080). Atoms
  are identical and sacred — the warm cream canvas, a single saturated cobalt (#1e2bfa) as the only
  accent, the three-step gray text ladder, Space Grotesk (display/numerals/chrome) + Inter (body),
  soft cobalt-tinted cards (4% fill / 20% border / 10–14px radius) with NO shadows, pill chrome, and
  the cobalt progress bar. Composition + frame scale rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#fdfae7"
  primary: "#1e2bfa"
  text: "#111111"
  text-muted: "#6b6b6b"
  text-light: "#9a9a9a"
  accent-light: "rgba(30,43,250,0.08)"
  accent-medium: "rgba(30,43,250,0.15)"
  border: "rgba(30,43,250,0.2)"
  card-bg: "rgba(30,43,250,0.04)"
  positive: "#059669"
  negative: "#dc2626"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — reading ramp (Inter body + Space Grotesk chrome) —
  body:    { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Space Grotesk", cqw: 0.8, weight: 600, tracking: "0.08em", upper: true, color: "primary" }
  tag:     { fontFamily: "Space Grotesk", px: 12, weight: 500, color: "primary" }
  counter: { fontFamily: "Space Grotesk", px: 13, weight: 500, tracking: "0.05em", color: "text-muted" }
  # — display / numerical ramp (Space Grotesk, near-black headings / cobalt numerals) —
  h3:      { fontFamily: "Space Grotesk", cqw: 1.25, weight: 500, lineHeight: 1.3, tracking: "-0.02em", color: "text" }
  stat-num:{ fontFamily: "Space Grotesk", cqw: 1.9, weight: 700, lineHeight: 1.0, color: "primary" }
  blockquote:{ fontFamily: "Space Grotesk", cqw: 2.4, weight: 500, lineHeight: 1.35, color: "text" }
  h2:      { fontFamily: "Space Grotesk", cqw: 2.6, weight: 600, lineHeight: 1.1, tracking: "-0.02em", color: "text" }
  metric-value:{ fontFamily: "Space Grotesk", cqw: 3.0, weight: 700, lineHeight: 1.0, color: "primary" }
  h1:      { fontFamily: "Space Grotesk", cqw: 4.2, weight: 700, lineHeight: 1.08, tracking: "-0.02em", color: "text" }
  quote-mark:{ fontFamily: "Space Grotesk", cqw: 8.0, weight: 700, lineHeight: 0.5, color: "primary", opacity: 0.15 }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "Universal content card. Never solid-colored, never opaque-bordered, NO shadow."
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.primary}) + {typography.metric-label} + {typography.metric-desc}"
    description: "+ optional inline ↑/↓ change chip ({colors.positive}/{colors.negative} text, no fill)."
  tag-pill:
    backgroundColor: "{colors.accent-light}"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "Top-right of the slide-header."
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "{radii.pill}"
    typography: "Space Grotesk 600"
    shadow: "soft cobalt on hover only — the system's only shadow"
    description: "The one solid element."
  accent-line:
    backgroundColor: "{colors.primary}"
    size: "60×4, 2px radius"
    description: "Above cover titles / eyebrow separators."
  bar-track:
    backgroundColor: "{colors.accent-light}"
    fill: "{colors.primary} (display:block so width resolves)"
    rounded: "{radii.bar}"
    description: "28px track; fill carries the value."
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "50%"
    size: "56px"
    description: "Sequential steps fade opacity 1.0→0.85→0.7→0.55."
  split-highlight:
    backgroundColor: "{colors.accent-light}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radii.card-md}"
    description: "Inline pull-quote callout."
  slide-header:
    typography: "{typography.h4-eyebrow} (cobalt) left, tag-pill right; {typography.h2} below"
    description: "Top band of every content frame."
  atmosphere:
    elements: "clipped diagonal cobalt-tint panel, 3×3 cobalt dot grid, concentric closing rings"
    description: "Cover/closing only. Never on content frames."
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px tall, bottom edge, width grows with index"
    description: "Persistent progress strip."
```

### Overview

Blue Professional at frame scale is a **consulting-grade system: restraint with one strong
commitment.** A warm cream canvas and a single saturated cobalt that carries every accent —
eyebrow, metric, CTA, chart fill, progress bar. No secondary brand color, no pastels, just cream,
cobalt, and a tight ladder of grays. The register is investment-research / consulting-firm
briefing: measured, data-dense without crowding, executive-readable at distance.

The voice is two faces in fixed roles: **Space Grotesk** (display, every numeral, all chrome —
eyebrows uppercase 0.08em) and **Inter** (body, muted gray, line 1.6). Headlines are near-black;
cobalt is reserved for accent moments. Depth is **soft and tinted** — 4% cobalt card fills with 20%
cobalt borders and 10–14px radii — never shadowed. The lack of harsh shadows is the premium signal.

**Key characteristics at frame scale:**

- **Warm cream ground** on every frame; **single cobalt** as the only accent.
- **Space Grotesk** (display/numerals/chrome) + **Inter** (body) — near-black headlines, cobalt numerals.
- **Tinted cards** — cobalt 4% fill, cobalt 20% 1.5px border, 10–14px radius, **no shadow**.
- **Pill chrome** (100px) — tag pills + the one solid cobalt CTA; cobalt **progress bar**.
- **Soft rounded corners everywhere** (no square corners save the progress bar).
- **Atmosphere** (diagonal panel, dot grid, concentric rings) on cover/closing only.

### The Frame

**Frame Craft Bar:**

- **Squint** — one **near-black headline or cobalt numeral** dominates at 3–6× its neighbor.
- **Silence** — content frames read **balanced, not crowded**; the **dashboard is the one dense exception**.
- **Restraint** — a **single cobalt accent** carries everything; headlines stay near-black (never cobalt); no shadows (tinted cards do the lift); positive/negative inline-text only.
- **Reference** — aim at an **investment-research / consulting quarterly briefing**; failure looks like a **heavy-outlined, multi-color dashboard**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x` 5cqw; bottom reserves room for the counter + progress bar.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Card radii stay px (10–14px); the
pill radius stays 100px; borders stay 1–1.5px.

### Colors

Tokens identical to the source. `{colors.bg}` cream is the universal ground; `{colors.primary}`
cobalt is the **only** accent — every eyebrow, numeral, CTA, chart fill, progress bar, and the 4px
highlight left-rule. Headlines are `{colors.text}` near-black (never cobalt); body is
`{colors.text-muted}`; tertiary is `{colors.text-light}`. Cards fill `{colors.card-bg}` (4%) with
`{colors.border}` (20%) borders. `{colors.positive}`/`{colors.negative}` appear **only inline** on
directional change chips — never as fills. **No second accent color.**

### Typography

Two ramps. The **reading ramp** (Inter body 0.85cqw muted; Space Grotesk eyebrow uppercase 0.08em
cobalt) carries copy + chrome; the **display/numerical ramp** (Space Grotesk `h3` 1.25cqw → `h1`
4.2cqw near-black; numerals `stat-num`/`metric-value` in cobalt) carries headings and figures.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; px chrome (tag/counter) is colophon only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤3 words → `h1`; 4–6 → `h2`; 7+ → `h3`. Cobalt numerals scale `metric-value`→`stat-num` by card size.
- **Headlines near-black, −0.02em**; **eyebrows cobalt, uppercase, 0.08em**; **numerals cobalt 600–700**; **body Inter 400 muted, line 1.6**. No italic, no uppercase body, no cobalt headline.

### Depth & Surface

Soft and tinted — never offset. Depth from:

- **Tinted cards** — 4% cobalt fill + 20% cobalt 1.5px border + 10–14px radius reads as lifted without offset.
- **Border-left accent** — the 4px cobalt rule on split-highlight blocks pulls a callout forward.
- **Rounded corners** — the 10–14px radius is part of the softness; square corners break it.

**Ceiling:** zero box-shadow on content (the only shadow is a soft cobalt CTA hover); no opaque cobalt borders; no harsh outlines.

### Shapes

- **100px** — tag pills, CTA, nav buttons (pill chrome).
- **14/12/10px** — cards by size (large metric / standard stat / detail + mini).
- **6px** — bar tracks + fills. **50%** — step circles, nav circles, dots, closing rings.
- **0** — only the progress bar. No square-cornered content.

### Components

- **card-tinted / metric-card** — the universal soft-tint content cards (no shadow).
- **tag-pill / cta-button / accent-line** — the cobalt pill chrome + the one solid CTA + the 60×4 rule.
- **bar-track / step-circle / split-highlight** — cobalt data + sequence + callout patterns.
- **slide-header** (eyebrow + tag pill) — the structural rhythm; **atmosphere** (diagonal/dots/rings) on cover/closing only; **progress-bar** on every frame.

### Frame Treatments

> Recipe: ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density.
> Atmosphere only on cover/closing; content frames carry the slide-header rhythm.

**1 · Cover** (identity · move: diagonal accent · left). **Ground** cream + the clipped diagonal cobalt-tint panel (right ~36%) + a 3×3 cobalt dot grid. **Composes** accent-line, meta, h1, body sub. **Focal** a 2-line Space Grotesk `h1` near-black, left, under a cobalt accent-line + meta. **Chrome** counter + progress bar. **Accent** the cobalt line + diagonal panel. **Silence** the diagonal panel holds the right third. **Fixed** near-black h1, cobalt accents, atmosphere here only. **Free** title, meta. **Density** low.

**2 · Dashboard** (data · move: 3-up metric grid · the dense frame). **Ground** cream, `pad-x`. **Composes** slide-header (eyebrow + tag-pill), h2, 3× metric/tinted card. **Focal** a row of tinted cards — cobalt `metric-value` + Inter label + muted desc + optional green/red change chip. **Chrome** eyebrow left, tag-pill right; progress bar. **Accent** the cobalt numerals. **Silence** tight — the density exception. **Fixed** 4% tint cards, 20% borders, no shadow, cobalt numerals. **Free** figures (from script), labels. **Density** dense-exception.

**3 · Bar Ranking** (data · move: cobalt bars · left). **Ground** cream, `pad-x`. **Composes** eyebrow, h2, bar-track rows. **Focal** 3–5 labeled cobalt-fill bars on cobalt-8% tracks with cobalt percentages. **Chrome** eyebrow; progress bar. **Accent** the cobalt fills + figures. **Silence** moderate. **Fixed** 6px tracks, cobalt fills. **Free** rows, values (from script). **Density** standard.

**4 · Pull Quote** (quote · move: concentric rings · centered). **Ground** cream, centered, with faint concentric closing-rings behind. **Composes** quote-mark, blockquote, cite. **Focal** a Space Grotesk `blockquote` near-black under a 15%-opacity cobalt quote-mark; an uppercase cobalt-muted cite beneath. **Accent** the faint rings + quote-mark. **Silence** ~55%. **Fixed** near-black quote, soft rings. **Free** quote, cite. **Density** low.

**5 · Split + Highlight** (content · move: asymmetric split · left). **Ground** cream, two columns. **Composes** eyebrow, h2, body, split-highlight block. **Focal** an Inter body column beside a cobalt-8% highlight block (4px cobalt left rule) carrying an inline pull quote. **Accent** the highlight's left rule. **Silence** generous gutter. **Fixed** tinted highlight, 4px cobalt rule. **Free** body, callout. **Density** standard.

**6 · Closing / CTA** (closer · move: centered rings + CTA). **Ground** cream + concentric closing-rings. **Composes** accent-line, h1, body, cta-button. **Focal** a Space Grotesk `h1` near-black, centered, with the one solid cobalt `cta-button` pill below. **Accent** the CTA + rings. **Silence** ~60%. **Fixed** one CTA, near-black h1, soft rings. **Free** sign-off, CTA label. **Density** low.

### Composition Rules

**Do:** start every frame on warm cream, let cobalt carry every accent (eyebrow, numeral, CTA, bar, progress); set headlines near-black −0.02em, eyebrows cobalt uppercase 0.08em, numerals cobalt 600–700; use tinted cards (4% fill, 20% border, 10–14px radius, no shadow), body Inter 400 muted line 1.6; keep all chrome pill-shaped (100px), one solid cobalt CTA per closing frame; reserve atmosphere (diagonal panel, dots, rings) for cover/closing, content frames keep the slide-header rhythm; lean left on cover/dashboard/split, centered on quote/closer.

**Don't:** use a second accent color or a cobalt headline; use drop shadows on content (only the soft cobalt CTA hover); use opaque cobalt borders; use square corners (save the progress bar); substitute fonts; use uppercase body; use the green/red change chips as general accents (directional comparisons only); fill space with heavier borders instead of substance; blow a headline edge-to-edge.

### Aspect-Ratio Behavior

| Treatment            | 16:9                          | 9:16                              | 1:1                          |
| ---------------------- | -------------------------------- | ------------------------------------ | -------------------------------- |
| Cover                  | title left, diagonal right       | title top, diagonal band below       | title upper, dots corner         |
| Dashboard              | 3 cards across                   | 3 stacked                            | 2×2                              |
| Bar Ranking            | 3–5 bars                         | 3–5 bars (tighter)                   | 3 bars                           |
| Pull Quote             | centered, rings behind           | centered, taller                     | centered                         |
| Split + Highlight      | side-by-side                     | stacked                              | stacked                          |
| Closing / CTA          | centered + CTA                   | centered + CTA                       | centered + CTA                   |

`pad-x` holds on the short edge; re-step display above the 1.4cqw floor. The diagonal cover panel
becomes a top/bottom band on 9:16. Numerals stay Latin Arabic digits in CJK builds.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. Figures, metrics, and quotes are content; the system supplies cream + cobalt + grays.

### Numerals & Claims (hard rule)

Never invent figures, financials, percentages, or dates at frame scale. Render slots as `— figure —`,
`{metric}`, `+NN%`, `↑ —`. Directional chips require a real comparison from the script.

### Pre-Render Self-Audit

- **Squint** — one near-black headline or cobalt numeral dominates per frame.
- **Silence** — content frames balanced, not crowded; only the dashboard runs dense.
- **Single accent** — cobalt only; headlines near-black; positive/negative inline only.
- **Type** — Space Grotesk headings −0.02em near-black, cobalt eyebrows 0.08em + numerals; Inter body muted line 1.6; ≥1.4cqw floor.
- **Depth** — tinted cards (no shadow), soft rounded corners, 20% cobalt borders; no square content corners.
- **Anchor** — left on cover/dashboard/split, centered on quote/closer; atmosphere on cover/closing only.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source's slide transitions + bar-fill animations are deck mechanics.
- Space Grotesk + Inter via Google Fonts. CJK pairing (Noto Sans SC 700 display / Noto Serif SC 400
  body) carries over; the eyebrow's uppercase+tracking signal weakens in CJK — pair it with the accent-line.
- 9:16 / 1:1 are guidance; verify the floor and that the diagonal panel reflows to a band.
- Diagonal panel (clip-path), dot grid, concentric rings, and bars are CSS-only; no external imagery is required.

---

## Preset: Broadside

```yaml
version: alpha
name: Broadside — Frame (video / frame layer)
description: >
  Video-first companion to Broadside's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the two-register surface system (dark ink-black / fire-orange), massive
  Barlow in lowercase weight 900 treated as graphic primitive, IBM Plex Mono chrome (uppercase,
  0.14em), the single fire-orange accent, the flat plane, and 1px hairline dividers. Composition +
  frame scale rewritten for the frame. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink-black: "#111111"
  ink-black-alt: "#1A1A18"
  fire-orange: "#E85D26"
  cream: "#F0ECE5"
  cream-muted: "#888880"
  cream-hint: "#505048"
  border-dark: "#282826"
  ink-on-orange-muted: "rgba(17,17,17,0.75)"
  ink-on-orange-hint: "rgba(17,17,17,0.55)"
  ink-on-orange-faint: "rgba(17,17,17,0.40)"
  ink-on-orange-border: "rgba(17,17,17,0.20)"

typography:
  # — reading ramp —
  body:    { fontFamily: "Barlow", cqw: 1.2, weight: 400, lineHeight: 1.6 }
  lead:    { fontFamily: "Barlow", cqw: 1.6, weight: 400, lineHeight: 1.5 }
  caption: { fontFamily: "Barlow", cqw: 0.9, weight: 400, lineHeight: 1.5 }
  label:   { fontFamily: "IBM Plex Mono", cqw: 0.72, weight: 500, tracking: "0.14em", upper: true }
  # — display / hero ramp (Barlow, lowercase, negative tracking) —
  h3:      { fontFamily: "Barlow", cqw: 2.8, weight: 600, lineHeight: 1.2, lower: true }
  quote-text:{ fontFamily: "Barlow", cqw: 3.8, weight: 700, lineHeight: 1.15, tracking: "-0.02em", lower: true }
  h2:      { fontFamily: "Barlow", cqw: 4.5, weight: 700, lineHeight: 1.1, tracking: "-0.02em", lower: true }
  stat-value:{ fontFamily: "Barlow", cqw: 5.5, weight: 900, lineHeight: 1.0, tracking: "-0.04em" }
  h1:      { fontFamily: "Barlow", cqw: 7.5, weight: 800, lineHeight: 0.9, tracking: "-0.03em", lower: true }
  fadelist-item:{ fontFamily: "Barlow", cqw: 7.5, weight: 900, lineHeight: 1.0, tracking: "-0.03em", lower: true }
  quote-mark:{ fontFamily: "Barlow", cqw: 10.0, weight: 900, lineHeight: 0.6 }
  fadelist-title:{ fontFamily: "Barlow", cqw: 10.5, weight: 900, lineHeight: 0.9, tracking: "-0.04em", lower: true }
  display: { fontFamily: "Barlow", cqw: 13.0, weight: 900, lineHeight: 0.88, tracking: "-0.04em", lower: true }

spacing:
  pad-x: "5.5cqw"
  pad-y: "5.5cqw"
  gap-lg: "3.5cqw"
  gap-md: "2cqw"
  gap-sm: "1cqw"

components:
  registers:
    dark: "ground {colors.ink-black}, text {colors.cream}, accent {colors.fire-orange}"
    orange: "ground {colors.fire-orange}, text {colors.ink-black}"
    description: "Two surfaces only — no cream/paper register. One register per frame."
  slide-chrome:
    rule: "1px solid {colors.border-dark} (dark) / 20% ink (orange)"
    placement: "top + bottom bars (label left, number right)"
    description: "SUPPRESSED on cover/chapter/statement/quote/end — declarative frames let type fill the field."
  kicker:
    typography: "{typography.label}"
    color: "{colors.fire-orange} (dark) / 55% ink (orange)"
    description: "Uppercase mono eyebrow."
  rule:
    backgroundColor: "{colors.fire-orange} (dark) / {colors.ink-black} (orange)"
    size: "36×2px"
    description: "Stub accent bar — the system's only ornament."
  broadside-num:
    typography: "{typography.label}"
    placement: "top-left of orange cover/chapter, low opacity"
    description: "Mono catalogue numeral."
  stat-card:
    borderTop: "1px solid {colors.border-dark}"
    typography: "{typography.stat-value} (orange on dark / ink on orange) + {typography.body} + {typography.label}"
    description: "Top-border-only block, no other borders."
  bullet:
    marker: "orange `/` mono via ::before"
    typography: "{typography.lead}"
    description: "Capped at THREE items."
  bar-track:
    borderLeft: "1px solid {colors.border-dark}"
    bars: "{colors.cream-hint}, one .accent {colors.fire-orange}"
    typography: "{typography.label} axis"
    description: "Vertical bar chart, left axis only."
  compare-panel:
    layout: "two equal panels split by a 1px vertical rule"
    payoff: "right panel may fill {colors.fire-orange}"
    description: "Before/after."
  fadelist:
    typography: "{typography.fadelist-item} ×3 at opacity 1.0/0.5/0.22 + {typography.fadelist-title}"
    description: "Three stacked words + one oversized title opposite."
```

### Overview

Broadside at frame scale is a **protest-poster system where type is so large it stops reading as
text and becomes graphic primitive.** Barlow `display` at 13cqw puts a single lowercase word
nearly across the frame. The system runs in **two registers**: a dark ink-black ground with cream
text for documentation, and a fire-orange ground with dark ink for declaration. Fire-orange is the
only color — accent on dark, environment on orange. The plane is flat; hierarchy is weight, size,
and 1px hairlines.

**Barlow** carries every text role from display to body — expressive range from weight (400–900)
and size, not face contrast. **IBM Plex Mono** is chrome only (numbers, kickers, tags, axis labels,
the `/` bullet marker), always uppercase and tracked. Display is **lowercase** — the system's most
distinctive single decision, a deliberate inversion of the brutalist norm.

**Key characteristics at frame scale:**

- **Two registers** — dark (cream text) / orange (ink text). No cream/paper register.
- **Massive lowercase Barlow 900**, negative-tracked, as graphic primitive (display 13cqw).
- **Fire-orange is the only color** — accent on dark, full environment on orange.
- **IBM Plex Mono chrome** — uppercase, 0.14em; the `/` bullet marker; mono catalogue numbers.
- **Flat plane** — no shadow, no radius (save nav dots), no gradient; 1px hairlines carry structure.
- **Low density** — one statement per frame, bullets capped at three, chrome suppressed on declarative frames.

### The Frame

**Frame Craft Bar:**

- **Squint** — exactly **one display moment dominates** at 3–6× everything else; nothing competes.
- **Silence** — declarative frames read **45–55% empty**; the **stat grid is the one dense exception**.
- **Restraint** — **one register per frame**; **fire-orange is the only color** (accent on dark, environment on orange); one display moment; bullets capped at three.
- **Reference** — aim at **broadside printing / a report with one loud color / a Wim Crouwel grid with one loud color**; failure looks like a **multi-accent corporate slide deck**.

- **Primary:** 1920×1080 (16:9). Type authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-x`/`pad-y` 5.5cqw — deliberately tight so the massive type crowds the frame edge.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. 1px hairlines stay 1px.

### Colors

Tokens identical to the source, in two registers. **Dark:** `{colors.ink-black}` ground,
`{colors.cream}` text, `{colors.fire-orange}` accent (kickers, accent stat, bullet `/`, lead bar,
quote mark, rule stub). **Orange:** `{colors.fire-orange}` ground, `{colors.ink-black}` headlines +
body, with the dark-ink overlays (75/55/40/20%) as the muted tones. Choose one register per frame
and commit. **No second accent color** — on orange, emphasis is weight/opacity on the ink, never a
new hue. Cream text on orange does not exist (ink-on-fire is absolute).

### Typography

Two ramps. The **reading ramp** (Barlow body 1.2cqw, mono label 0.72cqw) carries copy + chrome; the
**display ramp** (Barlow `h2` 4.5cqw → `display` 13cqw, weight 700–900) carries every statement.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤2 words → `display`; 3–4 → `h1`; 5+ → `h2`. Broadside packs only ONE display moment per frame.
- **Barlow display is lowercase, weight 700–900, negative-tracked** (−0.04em largest, −0.02em h2). **Mono chrome is uppercase, 0.1em+.** No italic, no underline, no uppercase display.

### Depth & Surface

Flat plane, the only technique. Hierarchy from:

- **Weight + size contrast** — the dominant signal (900 lowercase display).
- **1px hairlines** — chrome bars, stat-card top, compare divider, bar-track left, chart baseline.
- **Color shift** — orange on ink, ink on cream, cream-muted on cream.
- **Negative space** — generous, intentional empty regions.

**Ceiling:** no box-shadow, no elevation, no rounded surface (save nav dots), no gradient ground.

### Shapes

- **0 radius everywhere** except nav dots (50%). Cards, panels, tags, stat blocks, bars — sharp rectangles.

### Components

- **registers** — the two-surface system. **slide-chrome** — optional hairline bars, suppressed on declarative frames.
- **kicker** (mono eyebrow) / **rule** (36×2 stub) / **broadside-num** (catalogue mark) — the chrome ornament set.
- **stat-card** (top-border only) / **bullet** (orange `/`, max 3) / **bar-track** (one accent bar) / **compare-panel** (orange payoff) / **fadelist** (1.0/0.5/0.22 stack).

### Frame Treatments

> Recipe: ground · register · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One statement per frame; chrome suppressed on declarative frames.

**1 · Cover** (identity · move: massive type · ORANGE register · left). **Ground** fire-orange. **Composes** broadside-num, rule, kicker, display, lead. **Focal** a 1–2 word Barlow `display` (13cqw) lowercase in ink, left-anchored, over a small ink rule stub + mono kicker; a Barlow lead line beneath in 75% ink. **Chrome** mono catalogue number top-left, mono meta top-right (no chrome bars). **Accent** the ink itself is the pop on orange. **Silence** ~45%. **Fixed** ink-on-fire, lowercase 900, flat. **Free** the word, kicker, lead. **Density** low.

**2 · Statement** (declarative · move: type IS composition · DARK register · left). **Ground** ink-black. **Composes** kicker, display. **Focal** a 2–4 word Barlow `display`/`h1` lowercase in cream, with ONE clause inked `{colors.fire-orange}`. **Chrome** mono kicker; no bars. **Accent** the orange clause. **Silence** ~55%. **Fixed** lowercase 900, one orange clause, flat. **Free** the statement, which clause is orange. **Density** low.

**3 · Stat Grid** (data · move: top-border cards · DARK · the dense frame). **Ground** ink-black, chrome bars present. **Composes** slide-chrome, kicker, 3× stat-card. **Focal** a row of three top-border-only stat-cards — big Barlow-900 numeral in `{colors.fire-orange}`, Barlow label, mono note. **Chrome** top + bottom hairline bars (label + number). **Accent** the orange numerals. **Silence** moderate — the density exception. **Fixed** top-border-only cards, orange numerals, 1px hairlines. **Free** figures (from script), labels. **Density** dense-exception.

**4 · Fadelist** (narrative · move: opacity stack · DARK). **Ground** ink-black. **Composes** fadelist (3 stacked Barlow-900 words at 1.0/0.5/0.22), fadelist-title. **Focal** the three-stage word stack opposite an oversized display title in `{colors.fire-orange}` (before/during/after). **Accent** the orange title. **Silence** moderate. **Fixed** the opacity ladder, lowercase 900. **Free** the three words, the title. **Density** low-moderate.

**5 · Pull Quote** (quote · move: oversized mark · DARK · left). **Ground** ink-black, chrome suppressed. **Composes** quote-mark, quote-text, attribution. **Focal** a Barlow `quote-text` (700, lowercase) at ≤78cqw under an oversized fire-orange `quote-mark` (10cqw, line-height 0.6). **Chrome** mono attribution (name + role). **Accent** the orange quote mark. **Silence** ~50%. **Fixed** orange mark, lowercase quote. **Free** quote, attribution. **Density** low.

**6 · Compare** (argument · move: split + orange payoff · DARK→ORANGE). **Ground** ink-black left panel + fire-orange right (payoff) panel, 1px divider. **Composes** compare-panel pair, kicker, h3. **Focal** two panels — left documents (cream on dark), right declares (ink on orange). **Chrome** mono panel labels. **Accent** the orange payoff panel. **Silence** moderate. **Fixed** ink-on-fire right panel, 1px divider, flat. **Free** the before/after content. **Density** standard.

### Composition Rules

**Do:** set every Barlow display in lowercase weight 900, negative-tracked (the system's signature); use fire-orange as full environment on declarative frames, the lone accent on dark; keep chrome in IBM Plex Mono uppercase 0.14em, use the `/` mono bullet marker; cap bullets at three, one statement per frame, build hierarchy from weight, size, 1px hairlines; suppress chrome bars on cover/chapter/statement/quote/end (let type fill the field); lean left on most frames — the type IS the composition.

**Don't:** uppercase Barlow display; add a second accent color; put cream text on orange (ink-on-fire is absolute); use a cream/paper register; use a drop shadow, a rounded surface (save nav dots), or a gradient ground; pair a serif companion — chrome is never Barlow; pack two display moments into one frame; blow a long line edge-to-edge.

### Aspect-Ratio Behavior

| Treatment   | 16:9                            | 9:16                            | 1:1                 |
| ------------- | ---------------------------------- | ----------------------------------- | ----------------------- |
| Cover         | word left, lead below              | word top, lead below                | centered word            |
| Statement     | display left                       | display stacked taller              | display centered         |
| Stat Grid     | 3 across                           | 3 stacked                           | 2+1                       |
| Fadelist      | stack + title side-by-side         | stack over title                    | stack over title          |
| Pull Quote    | mark + quote left                  | mark top, quote below               | centered                  |
| Compare       | side-by-side panels                | stacked (dark over orange)          | stacked                   |

`pad-x` holds tight on the short edge; re-step display so the one big line stays ≤78cqw and above the
1.4cqw floor. Mono chrome stays Latin/digit-only.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The system supplies type and one color, not brands.

### Numerals & Claims (hard rule)

Never invent figures, percentages, dates, or counts at frame scale. Render slots as `— figure —`,
`{metric}`, `NN%`. Catalogue numbers (No. 01) are decorative chrome and may be sequential.

### Pre-Render Self-Audit

- **Squint** — exactly one display moment dominates; nothing competes.
- **Silence** — declarative frames ~45–55% empty; only the stat grid runs dense.
- **Register** — one register per frame; ink-on-fire on orange, cream on dark; no second hue.
- **Type** — Barlow lowercase 900 negative-tracked, fit-to-measure; mono chrome uppercase 0.14em; ≥1.4cqw floor.
- **Depth** — 0 shadow, 0 radius (save nav dots); 1px hairlines only.
- **Bullets** — capped at three, orange `/` marker.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source's per-element entry animations are deck mechanics.
- Barlow + IBM Plex Mono via Google Fonts; Noto Sans SC is the CJK fallback (the lowercase-display
  signal has no CJK equivalent — the two-register color system carries the identity).
- 9:16 / 1:1 are guidance; verify the one big line stays ≤78cqw and above the floor per ratio.
- Bars, compare panels, and the dashed image placeholder are CSS-only; no external imagery is required.

---

## Preset: Bold Poster

```yaml
version: alpha
name: Bold Poster — Frame (video / frame layer)
description: >
  Video-first companion to Bold Poster's design.md. The unit is the frame (1920×1080). Atoms are
  identical and sacred — the four-color palette (white / brown-black ink / tomato red / off-white),
  the three-face stack (Shrikhand display tilted at poster scale, Libre Baskerville serif body,
  Space Grotesk mono chrome), the stacked text-shadow on red display, the 3px+1.5px double-border
  grid, red leftbar cards, red em-dash bullets, and the red progress bar. Composition + frame scale
  rewritten. Motion out of scope.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#FFFFFF"
  dark: "#1C1410"
  red: "#D8000F"
  light: "#F5F2EF"

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Libre Baskerville", cqw: 0.85, weight: 400, lineHeight: 1.75, color: "dark" }
  body-cell:{ fontFamily: "Libre Baskerville", cqw: 0.7, weight: 400, lineHeight: 1.55 }
  label:   { fontFamily: "Space Grotesk", px: 10, weight: 600, tracking: "2px", upper: true, color: "red" }
  bullet-body:{ fontFamily: "Space Grotesk", cqw: 0.62, weight: 400, lineHeight: 1.45 }
  # — display / hero ramp (Shrikhand 400, tilted) —
  card-title:{ fontFamily: "Shrikhand", cqw: 1.9, weight: 400, lineHeight: 1.1, color: "dark" }
  cell-number:{ fontFamily: "Shrikhand", cqw: 2.7, weight: 400, lineHeight: 1.0, color: "red" }
  section-header:{ fontFamily: "Shrikhand", cqw: 3.3, weight: 400, lineHeight: 1.0, color: "dark" }
  red-quote:{ fontFamily: "Shrikhand", cqw: 4.7, weight: 400, lineHeight: 1.15, color: "bg", shadow: "stacked" }
  hero-title-bottom:{ fontFamily: "Shrikhand", cqw: 10.4, weight: 400, lineHeight: 0.9, color: "dark", rotate: "2deg" }
  hero-title:{ fontFamily: "Shrikhand", cqw: 11.5, weight: 400, lineHeight: 0.88, color: "dark" }
  hero-title-red:{ fontFamily: "Shrikhand", cqw: 13.5, weight: 400, lineHeight: 0.85, color: "red", rotate: "-4deg" }
  close-big:{ fontFamily: "Shrikhand", cqw: 13.5, weight: 400, lineHeight: 0.88, color: "red", rotate: "-5deg" }
  stat-big:{ fontFamily: "Shrikhand", cqw: 22.0, weight: 400, lineHeight: 0.82, color: "red", rotate: "-6deg" }

spacing:
  pad-slide: "3cqw 3.6cqw"
  gap-grid: "1.5cqw 2cqw"

components:
  progress-bar:
    backgroundColor: "{colors.red}"
    size: "0.5cqw tall, bottom edge, width grows with index"
    description: "The most prominent chrome."
  hero-title-stack:
    typography: "{typography.hero-title} + {typography.hero-title-red} + {typography.hero-title-bottom}"
    transform: "≥4 tilt (−4°/+2°), ≥1 line in {colors.red}"
    description: "A 3-line Shrikhand composition — the signature opener."
  stat-big:
    typography: "{typography.stat-big}"
    color: "{colors.red} (or {colors.bg} on red with stacked shadow)"
    transform: "rotate(-6deg)"
    description: "Hero numeral at poster scale."
  fin-grid:
    border: "0.3cqw solid {colors.dark} outer"
    rule: "0.15cqw solid {colors.dark} inner (touching at intersections)"
    rounded: "0"
    typography: "{typography.cell-number} ({colors.red}) + {typography.label} + {typography.body-cell}"
    description: "The double-border tabular signature."
  red-leftbar-card:
    borderLeft: "4px solid {colors.red}"
    padding: "0 0 0 ~1cqw"
    rounded: "0"
    shadow: "none"
    typography: "{typography.card-title} + {typography.body} + red em-dash bullets"
    description: "Editorial card cantilevered off a red left rule — no outline."
  red-panel:
    backgroundColor: "{colors.red}"
    textColor: "{colors.bg}"
    description: "Full-bleed statement surface; display carries the stacked text-shadow."
  dark-panel:
    backgroundColor: "{colors.dark}"
    textColor: "{colors.bg}"
    description: "Full-bleed dark statement surface; red accents."
  stacked-text-shadow:
    shadow: "2px 2px 0 rgba(28,20,16,.25), 4px 4px 0 rgba(28,20,16,.2), 6px 6px 0 rgba(28,20,16,.15)"
    appliesTo: "red display text on red panels only"
    description: "The ONLY shadow in the system — text-shadow, not box-shadow."
  bullet:
    marker: "red em-dash (—) or round (•) glyph at absolute-left"
    color: "{colors.red}"
    description: "No default disc bullets; capped at three."
```

### Overview

Bold Poster at frame scale is a **populist editorial poster** — vintage Italian sports-magazine
display, classical serif body, one saturated tomato red, grids ruled in ink. Every frame should
feel printed: heavy display type at poster scale, locked to one red accent, on a white/off-white
sheet (or a full red/dark statement panel), with decoration kept to a strict minimum.

The voice is a three-face stack: **Shrikhand** (heavy slab-script, weight 400 only, routinely
tilted −6°..+2°) carries every hero title, section header, stat, and card title; **Libre
Baskerville** (literary serif) carries every body paragraph — it's what makes the system feel
printed; **Space Grotesk** (uppercase, 2–3px tracked) is chrome only — labels, eyebrows, counters,
bullet bodies. The plane is flat; the only shadow is the stacked text-shadow on red display.

**Key characteristics at frame scale:**

- **Four colors only** — white / brown-black ink / tomato red / off-white. Red is the lone accent.
- **Shrikhand display, tilted** (−6° stat, −5° close, −4° hero-red, +2° hero-bottom) — the signature movement.
- **Libre Baskerville serif body** (line 1.75); **Space Grotesk** chrome (uppercase tracked).
- **Double-border grids** (3px outer + 1.5px inner ink); **red leftbar cards**; **red em-dash bullets** (max 3).
- **Stacked text-shadow** on red display — the only shadow; flat plane otherwise; square corners.
- **Red progress bar** at the bottom edge of every frame.

### The Frame

**Frame Craft Bar:**

- **Squint** — **one display moment dominates** at 3–6× everything else (the hero stack, `stat-big`, or `close-big`); nothing competes.
- **Silence** — statement frames reserve **~50–60% negative space**; the **financial grid is the one dense exception**.
- **Restraint** — **four colors only**, red the lone accent; one display moment per frame; the stacked text-shadow on red is the only shadow; bullets capped at three.
- **Reference** — aim at a **vintage Italian sports-magazine cover / mid-century European annual report**; failure looks like a **rounded, soft-shadowed multi-accent slide**.

- **Primary:** 1920×1080 (16:9). Display authored in **`cqw`** (`px ÷ 1920 × 100 = cqw`).
- **Vertical:** 1080×1920 (9:16). **Square:** 1080×1080 (1:1).
- **Safe area:** `pad-slide` ~3cqw — deliberately tight so the poster type crowds the frame.

**The container law (load-bearing).** Every frame ground sets `container-type: size`; ALL
frame-relative units are `cqw`/`cqh` against it — never `vw`. Borders stay px; rotation transforms hold.

### Colors

Tokens identical to the source. `{colors.bg}` white is the default ground; `{colors.dark}` is body,
borders, headers; `{colors.red}` is the only accent — every numeral, section rule, eyebrow,
leftbar, bullet, progress bar, and the full statement-panel ground. `{colors.light}` off-white
stripes alternating panels. **No fifth color** (no green/blue/yellow); categorical difference comes
from position, label, and tilt. Red is never body text, never a tint, never an untexted fill.

### Typography

Two ramps. The **reading/chrome ramp** (Baskerville body 0.85cqw, Space Grotesk labels in px)
carries copy + chrome; the **display ramp** (Shrikhand `section-header` 3.3cqw → `stat-big` 22cqw)
carries every statement and numeral.

- **Legibility floor:** any load-bearing line ≥ **1.4cqw**; mono labels are chrome only.
- **Fit-to-measure:** size the headline to its length. Cap the block at **≤ 78cqw**; ≤2 words → `stat-big`/`hero-title-red`; 3–4 → `hero-title`; 5+ → `section-header`. The hero is a stacked 3-line composition.
- **Shrikhand is weight 400, tilted on statement/hero elements, red on numerals**; **Baskerville body at line ≥1.5**; **Space Grotesk chrome uppercase, 2–3px**. Inline `<strong>` switches face to Space Grotesk 600. No italic display, no untilted red hero.

### Depth & Surface

Flat plane. Depth from:

- **Heavy borders** — 3px+1.5px double-border grids, 2px global-card outline, 4px red leftbar rules.
- **Surface inversion** — full-bleed red or dark statement panels.
- **Tilt** — rotated Shrikhand breaks the baseline for perceived dimension.
- **The single shadow** — stacked text-shadow on red display only (text-shadow, three steps).

**Ceiling:** no box-shadow, no rounded surface (square corners; only the hint pill is 4px), no gradient.

### Shapes

- **0 radius everywhere** except the hint pill (4px). Cards, cells, panels, callouts — sharp rectangles.

### Components

- **hero-title-stack** — the 3-line tilted opener. **stat-big** — the poster numeral.
- **fin-grid** — the double-border tabular signature. **red-leftbar-card** — the cantilevered editorial card.
- **red-panel / dark-panel** — statement surfaces. **stacked-text-shadow** — the one shadow.
- **bullet** — red em-dash (max 3). **progress-bar** — the red bottom strip.

### Frame Treatments

> Recipe: ground · register · composes · focal · chrome · accent · silence · Fixed/Free · density.
> One display moment per frame; statement frames reserve massive negative space.

**1 · Hero Stack** (identity · move: 3-line tilted stack · left). **Ground** white. **Composes** hero-title-stack, label, body tagline, progress-bar. **Focal** a 3-line Shrikhand stack (e.g. ink / red-tilted / paper) — one red line, one+ tilted. **Chrome** mono eyebrow + Baskerville tagline; bottom progress bar + counter. **Accent** the red line. **Silence** right half open. **Fixed** Shrikhand 400, ≥1 tilt + ≥1 red, square. **Free** the words, line sizes. **Density** low.

**2 · Hero Stat** (statement · move: poster numeral · red panel · centered). **Ground** full `{colors.red}`. **Composes** stat-big, label, body sub. **Focal** a `stat-big` numeral rotated −6° in white with the stacked shadow, centered, with a mono label above + Baskerville sub below. **Accent** the ink stacked-shadow on white. **Silence** ~60%. **Fixed** white-on-red + stacked shadow, −6° tilt. **Free** the figure (from script), label. **Density** low.

**3 · Financial Grid** (data · move: double-border matrix · the dense frame). **Ground** white, `pad-slide`. **Composes** label, section-header, fin-grid. **Focal** a 3px-outer/1.5px-inner ink grid of cells (red Shrikhand numeral + mono label + Baskerville body). **Chrome** mono eyebrow; progress bar. **Accent** the red numerals. **Silence** tight — the density exception. **Fixed** double-border, red numerals, serif body. **Free** figures (from script), labels. **Density** dense-exception.

**4 · Pull Quote** (quote · move: tilted/stacked display · red panel · left). **Ground** full `{colors.red}`. **Composes** red-quote, Baskerville cite. **Focal** a 2-line Shrikhand quote in white with the stacked shadow; a Baskerville cite beneath. **Accent** the stacked shadow. **Silence** ~50%. **Fixed** white-on-red + stacked shadow. **Free** quote, cite. **Density** low.

**5 · Editorial Cards** (content · move: red leftbar cards · left). **Ground** white (or alternating off-white stripes). **Composes** label, section-header, 2–3× red-leftbar-card. **Focal** cards cantilevered off 4px red rules — Shrikhand title + Baskerville body + red em-dash bullets (max 3). **Accent** the red left rules + bullets. **Silence** moderate. **Fixed** 4px red leftbar, em-dash bullets, no outline. **Free** card content. **Density** standard.

**6 · Closing Statement** (closer · move: tilted close-big · centered/left). **Ground** white or `{colors.dark}`. **Composes** close-big, label, body sub, progress-bar. **Focal** a Shrikhand `close-big` (rotated −5°, red) sign-off; mono eyebrow + Baskerville contact line. **Accent** the red tilted title. **Silence** ~60%. **Fixed** −5° tilt, red close-big. **Free** sign-off, contact. **Density** low.

### Composition Rules

**Do:** stack hero titles in 3 Shrikhand lines — at least one tilted, at least one red; make every numeral red Shrikhand, tilt statement display −5° to −6°; set eyebrows in Space Grotesk 600 uppercase 2–3px red, body in Baskerville line 1.75; build data grids with the 3px outer + 1.5px inner double border, use red leftbar cards elsewhere; use red em-dash bullets capped at three; apply the stacked text-shadow on red display; keep one display moment per frame, reserve negative space on statement frames.

**Don't:** use a second accent color; round corners (square only, save the hint pill); use a drop shadow — the stacked text-shadow on red is the only one; substitute fonts (no Shrikhand body, no Baskerville labels, no Space Grotesk headlines); use default disc bullets or an untilted red statement display; crowd a statement frame; blow a long line edge-to-edge.

### Aspect-Ratio Behavior

| Treatment         | 16:9                        | 9:16                        | 1:1                    |
| -------------------- | ------------------------------ | ------------------------------- | --------------------------- |
| Hero Stack           | stack left, tagline below      | stack centered, taller          | stack, tagline below         |
| Hero Stat            | numeral centered               | numeral centered, taller        | centered                     |
| Financial Grid       | 3 cells across                 | 2 across / stacked              | 2×2                          |
| Pull Quote           | quote left                     | quote stacked                   | centered                     |
| Editorial Cards      | 2–3 across                     | stacked                         | stacked                      |
| Closing              | close-big centered             | close-big stacked               | centered                     |

`pad-slide` stays tight on the short edge; re-step display so the line stays ≤78cqw above the floor.
Tilts hold; the progress bar spans the bottom on every ratio.

### Approved Entities

No real customers, logos, or vendors are defined in the source — render any such mark as a
placeholder. The system supplies type, one red, and ink rules, not brands.

### Numerals & Claims (hard rule)

Never invent figures, financials, percentages, or dates at frame scale. Render slots as `— figure —`,
`{metric}`, `+NN%`. Catalogue numbers / progress are decorative.

### Pre-Render Self-Audit

- **Squint** — one display moment dominates; nothing competes.
- **Silence** — statement frames reserve ~50–60% negative space; only the fin-grid runs dense.
- **Color** — four colors only; red is the lone accent; no red body text.
- **Type** — Shrikhand 400 tilted on statements, red numerals, fit-to-measure; Baskerville body line 1.75; mono chrome uppercase 2–3px; ≥1.4cqw floor.
- **Depth** — flat; the stacked text-shadow on red display is the only shadow; square corners.
- **Bullets** — red em-dash, capped at three.
- **Fabrication** — every numeral traces to the script, else placeholder.

### Known Gaps

- Motion intentionally out of scope; the source's slide transitions are deck mechanics.
- Shrikhand + Libre Baskerville + Space Grotesk via Google Fonts. CJK: Noto Serif SC 900/400 +
  Noto Sans SC; Shrikhand's slab-script has no Hanzi equal — keep tilts + red + double-borders to
  carry the identity.
- 9:16 / 1:1 are guidance; verify the one big line ≤78cqw per ratio and that tilts don't clip.
- Grids, leftbar cards, and the stacked shadow are CSS-only; no external imagery is required.

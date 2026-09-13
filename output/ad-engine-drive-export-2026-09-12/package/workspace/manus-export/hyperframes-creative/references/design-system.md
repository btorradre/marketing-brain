# Design System

Design-spec resolution and parsing, house-style defaults, the interactive design picker workflow,
and post-build design-adherence checks for HyperFrames video projects. See `../SKILL.md` for the
overall workflow this file supports.

## Design Spec — `frame.md` / `design.md`

The single source of truth for what a design spec is, how to find it, and how to read it. Other
sections of this reference defer here for resolution and format; how to *apply* a spec to a video
frame (brand, not layout) is covered in `composition-rules.md`.

### What `frame.md` is

`frame.md` is the frame-scale design system for a video/HyperFrames project — the video-first
companion to `design.md` (which is written for web/static pages). Same file format as `design.md`;
it reframes the brand with the frame as the unit.

A spec is YAML frontmatter + a markdown body, and the two layers are not equal:

- **Frontmatter is the normative layer** — `colors`, `typography`, `spacing`, `components` are the
  real, machine-readable values. Quote them verbatim (exact hex, font family, weight); never
  invent or round them.
- **Prose is context** — the `##` sections (Overview, The Frame, Composition Rules, …) carry
  intent, when-to-use, and constraints the tokens can't hold. Read them for judgment, not for
  values.

### Resolving which spec to read

Precedence — read the first that exists, ignore the rest:

```
frame.md  →  design.md  →  DESIGN.md
```

```bash
SPEC=$(ls frame.md design.md DESIGN.md 2>/dev/null | head -1)
```

- `frame.md` is the preferred spec for video projects and wins when more than one exists.
- `frame.md` is always lowercase — there is no `FRAME.md` variant in a live project. (`design.md`
  and `DESIGN.md` are genuinely different files on Linux; a frame-preset ships an uppercase
  `FRAME.md` *template*, adopted as lowercase `frame.md` — see "Starting from a preset" below.)

Load the spec once at the start of the workflow; every later step (expansion, authoring,
adherence) consumes the already-loaded spec rather than re-resolving it.

### Starting from a preset (optional)

Optionally seed `frame.md` from a ready-made frame-preset in `frame-presets-1.md` /
`frame-presets-2.md` — a fixed set of thirteen, each shipping a `FRAME.md` template whose tokens
get copied in and overlaid with brand-specific values. Referencing a preset is not required; a
bespoke or picker-generated spec is equally valid.

| Preset               | Look                                                                                                                                                                                                                                                                                                     | Pick when                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| biennale-yellow         | Literary-editorial catalogue — warm parchment ground, single deep indigo ink, solar yellow as radial bloom / panel / tile underprint, Instrument Serif 400 display (tight, negative-tracked) + Archivo body + JetBrains Mono data, strict rectangles (0 rounded corners), 1px hairline rules as sole border, no shadows  | confident / atmospheric / restrained; a product that wants museum-catalogue elegance and editorial authority                     |
| blockframe              | Maximalist neobrutalist — 4px black borders, 8px hard offset shadows, five candy pastels, Inter 800–900 uppercase, square corners, tilted decorations                                                                                                                                                    | bold / punchy / playful-loud; a product that wants to feel confident and graphic                                                 |
| blue-professional       | Consulting-grade restraint — warm cream canvas, single saturated cobalt (#1e2bfa) accent only, Space Grotesk + Inter typography, soft tinted cards (4% fill / 20% border / 10–14px radius) with NO shadows, pill chrome (100px), 3-step gray text ladder, cobalt progress bar                           | measured / executive-readable / premium-signal; a product that wants investment-research rigor and refined restraint             |
| bold-poster             | Populist editorial poster — Shrikhand display tilted −6°..+2°, Libre Baskerville serif body, Space Grotesk mono chrome, four colors only (white / brown-black ink / tomato red / off-white), double-border grids (3px+1.5px), red leftbar cards, red em-dash bullets, stacked text-shadow on red display, square corners | powerful / printed / restrained; a product that wants editorial authority and vintage gravitas                                   |
| broadside               | Protest-poster system — two-register flat plane (ink-black / fire-orange), massive lowercase Barlow 900 treated as graphic primitive, IBM Plex Mono chrome (uppercase, 0.14em), fire-orange sole accent, 1px hairlines, sharp corners, no shadow                                                        | bold / typographic / declarative; a product that wants presence and authority                                                    |
| capsule                 | Playful editorial — every container a pill (2px ink outline), cream canvas, nine candy accents, Bodoni Moda + Space Grotesk, soft offset shadows, floating-pill wallpaper                                                                                                                                | friendly / soft / editorial; a product that wants warmth and approachability                                                     |
| cartesian               | Museum-catalog editorial — 1px taupe hairline grid, five warm-stone palette, Playfair Display 400 + Inter, sharp corners, compass-drafted geometric rings, zero shadow / zero fill                                                                                                                       | sparse / literary / restrained; a product that wants quiet authority and editorial rigor                                         |
| claude                  | Warm-editorial brand book — warm cream paper (never pure white), terracotta coral (#CC785C) as scarce voltage, hairline ink elevation (no heavy shadow), EB Garamond serif display + Inter body + JetBrains Mono index / code on a warm-navy code surface, sentence-case display, ✱ coral spike           | considered / literary / developer-facing; a code change, launch, or doc that wants editorial calm and a first-class code surface |
| cobalt-grid             | Modernist two-color risograph — cream paper, electric cobalt ink, permanent graph-paper grid (10% cobalt), top/bottom cobalt hairlines, Newsreader 400 serif + Hanken Grotesk + DM Mono, 0° corners, pixel-glitch column + QR-block patches                                                              | restrained / systemic / editorial; a product that wants clarity and measured authority                                           |
| coral                   | Bold editorial magazine — three solid surfaces (coral fire / ink black / warm cream) meeting at hard edges, 45° diagonal hatch on coral, Bebas Neue + Inter tracked caps, zero shadows/radius (circles 50%), oversized wallpaper numerals and giant marks                                                | bold / structuralist / editorial; a product that wants graphic confidence and hard-edged confidence                              |
| creative-mode           | Neo-brutalist editorial — cream canvas, 4px ink borders, hard offset shadows (no blur), four accents rationed two-to-three, Archivo Black uppercase at 0.92 line-height, JetBrains Mono taxonomy, Space Grotesk body, square corners save one pill chip                                                  | sparse / graphic / punchy-restrained; a product that wants editorial presence and geometric confidence                           |
| daisy-days              | Cheerful picture-book — 3px charcoal outlines, 6/4px hard offset shadows (no blur), nine sunny-garden pastels (cream + turquoise/soft-pink/butter/mint/lavender/peach/sky + coral accent), Fredoka One + Quicksand, generous radii (20–50px), hand-drawn SVG ornament layer (daisies/stars/suns/clouds/rainbows)         | playful / childlike / sticker-sheet kawaii; a product that wants warmth and whimsy                                               |
| editorial-forest        | Serif-led literary-editorial — green / pink / cream editorial triad, Source Serif 4 weight 500 (opsz) for display + JetBrains Mono 500 uppercase chrome, flat paper depth (no shadows), 2px hairline rules, 6/8px card radii, monogram circle stamp                                                      | spacious / restrained / editorial; a product that wants quiet confidence and literary tone                                       |

Each preset folder also ships a `frame-showcase.html` — a preview contact sheet of its frame
treatments; open it to see the look, never include it in a project.

### Consuming it

How to apply the spec to a frame — strict on brand (hex, fonts, weight relationships, Do's/Don'ts),
free on layout — is the consumption contract in `composition-rules.md` ("The Design Spec Is Brand,
Not Layout"). Read it before choosing colors or writing HTML.

## House Style

Creative direction for compositions when no design spec is provided. These are starting points —
override anything that doesn't serve the content. When a design spec exists, its brand values take
precedence; house-style fills gaps.

### Before Writing HTML

1. **Interpret the prompt.** Generate real content. A recipe lists real ingredients. A HUD has real
   readouts.
2. **Pick a palette.** Light or dark? Declare bg, fg, accent before writing code.
3. **Pick typefaces.** Run the font-discovery approach in `typography-and-motion.md` — or pick a
   font already known that fits the theme. The script broadens options; it's not the only source.

### Lazy Defaults to Question

These patterns are AI design tells — the first thing every LLM reaches for. Before using one,
pause and ask: is this a deliberate choice for THIS content, or a default?

- Gradient text (`background-clip: text` + gradient)
- Left-edge accent stripes on cards/callouts
- Cyan-on-dark / purple-to-blue gradients / neon accents
- Pure `#000` or `#fff` (tint toward the accent hue instead)
- Identical card grids (same-size cards repeated)
- Everything centered with equal weight (lead the eye somewhere)
- Banned fonts (see `typography-and-motion.md` for the full list)

If the content genuinely calls for one of these — a centered layout for a solemn closing, cards for
a real product UI mockup, a banned font because it's the perfect thematic match — use it. The goal
is intentionality, not avoidance.

### Color

- Match light/dark to content: food, wellness, kids → light. Tech, cinema, finance → dark.
- One accent hue. Same background across all scenes.
- Tint neutrals toward the accent hue (even subtle warmth/coolness beats dead gray).
- **Contrast:** aim for WCAG AA (4.5:1 normal text, 3:1 large text ≥24px or ≥19px bold). Text must
  be readable with decoratives removed.
- Declare palette up front. Don't invent colors per-element.

### Background Layer

Every scene needs visual depth — persistent decorative elements that stay visible while content
animates in. Without these, scenes feel empty during entrance staggering.

Ideas (mix and match, 2-5 per scene):

- Radial glows (accent-tinted, low opacity, breathing scale)
- Ghost text (theme words at 3-8% opacity, very large, slow drift)
- Accent lines (hairline rules, subtle pulse)
- Grain/noise overlay, geometric shapes, grid patterns
- Thematic decoratives (orbit rings for space, vinyl grooves for music, grid lines for data)

All decoratives should have slow ambient animation — breathing, drift, pulse. Static decoratives
feel dead.

**Decorative count vs motion count.** The "2-5 per scene" count refers to decorative *elements*. If
a project's design spec says "single ambient motion per scene," it means one looping motion applied
to these decoratives (a shared breath/drift/pulse) — not one element total. A scene with 4
decoratives sharing one breathing motion is correct; a scene with 1 decorative is under-dressed.

### Motion

See `typography-and-motion.md` for full rules. Quick reference: 0.3–0.6s, vary eases, combine
transforms on entrances, overlap entries.

### Typography

See `typography-and-motion.md` for full rules. Quick reference: 700-900 headlines / 300-400 body,
serif + sans (not two sans), 60px+ headlines / 20px+ body.

### Palettes

Declare one background, one foreground, one accent before writing any HTML.

| Category            | Use for                                          | File                          |
| --------------------- | -------------------------------------------------- | ------------------------------- |
| Bold / Energetic       | Product launches, social media, announcements       | `palettes.md` § Bold / Energetic  |
| Warm / Editorial       | Storytelling, documentaries, case studies           | `palettes.md` § Warm / Editorial  |
| Dark / Premium         | Tech, finance, luxury, cinematic                    | `palettes.md` § Dark / Premium    |
| Clean / Corporate      | Explainers, tutorials, presentations                | `palettes.md` § Clean / Corporate |
| Nature / Earth         | Sustainability, outdoor, organic                    | `palettes.md` § Nature / Earth    |
| Neon / Electric        | Gaming, tech, nightlife                             | `palettes.md` § Neon / Electric   |
| Pastel / Soft          | Fashion, beauty, lifestyle, wellness                | `palettes.md` § Pastel / Soft     |
| Jewel / Rich           | Luxury, events, sophisticated                       | `palettes.md` § Jewel / Rich      |
| Monochrome             | Dramatic, typography-focused                        | `palettes.md` § Monochrome        |

Or derive from OKLCH — pick a hue, build bg/fg/accent at different lightnesses, tint everything
toward that hue.

## Design Picker

A two-phase visual picker: mood boards first (pick a complete direction), then fine-tune individual
categories. Use this when the request calls for interactive, human-in-the-loop selection rather
than an autonomously chosen palette/preset.

### Prerequisites

Read these before generating options — they define the rules the options must follow: this file's
House Style and Design Spec sections above, `typography-and-motion.md`, `composition-rules.md`
(video-composition rules), and `prompt-expansion.md` (the visual-styles section).

### Building the picker

1. Generate options deeply contextual to the request — every category, not just architectures,
   must reflect the specific product, brand, audience, and mood. Generic options that could appear
   on any picker are a failure.

   **Mood boards** — as many as the creative space warrants (4-8). Every board must tell a
   different STORY about the brand, not just reshuffle the same elements. Ask: "what are the
   genuinely different ways to position this product?" A cat food brand might be: playful chaos,
   premium positioning, comfort/cozy, social-native, flavor showcase, humor-led,
   sensory/appetizing. Each is a different narrative, not a different font on the same layout.

   **Architectures** — one per mood board minimum, each visually distinct. Use `{{prompt_headline}}`
   and `{{prompt_sub}}` tokens. If media assets were provided, use them as background images
   (`url(path)` without quotes — single quotes inside `style='...'` break the attribute).

   **Palettes** (5-6) — named after the brand's world, not generic moods. The palette names and
   colors should feel like they belong to THIS specific product. Always mix dark + light + tinted.
   Every palette must be visually distinct at swatch size — if two palettes share the same
   background lightness AND a similar accent hue, cut one. Test: would a user see the difference in
   a 14px swatch chip? If not, they're duplicates.

   **Type pairings** (5-6) — run the font-discovery approach from `typography-and-motion.md`
   BEFORE generating pairings. This is not optional — skipping it reaches for the same 8 fonts
   every time (Bricolage Grotesque, Instrument Serif, Fraunces, Archivo Black, DM Serif Display,
   Space Grotesk, Fredoka) — a training-data default, not a contextual choice. Match the brand's
   energy and audience. Cross-category per the pairing rules (never two sans-serifs).

2. Copy the design-picker HTML template (see `../SKILL.md` scripts section — the template lives at
   `templates/design-picker.html` in the source project and is not bundled with this skill) into a
   working file for the project, e.g. `.hyperframes/pick-design.html`.

3. Replace these placeholders programmatically (don't hand-escape quotes with text search/replace):
   - `__ARCHITECTURES_JSON__` — array of architecture objects
   - `__PALETTES_JSON__` — array of palette objects
   - `__TYPEPAIRS_JSON__` — array of type pairing objects
   - `__MOODBOARDS_JSON__` — array of mood board objects (see format below)
   - `__PROMPT_JSON__` — object with prompt context (see format below)

### Architecture data format

Each architecture object must include a `preview_html` field — the HTML that renders in the
preview panel. Use token placeholders that the template replaces at runtime: `{{bg}}`, `{{fg}}`,
`{{ac}}`, `{{mt}}`, `{{hf}}`, `{{hw}}`, `{{bf}}`, `{{bw}}`, `{{cr}}` (corner radius), `{{pad}}`,
`{{gap}}`, `{{shadow}}`, `{{g}}` (grid line color), `{{fg3}}`/`{{fg6}}`/`{{fg8}}`/`{{fg15}}` (fg at
opacity), `{{ac3}}`/`{{ac5}}`/`{{ac25}}` (accent at opacity).

Every token must be used. Apply `{{cr}}` to all cards, buttons, and containers. Apply `{{shadow}}`
to elevated elements (cards, buttons, code blocks). Apply `{{pad}}` and `{{gap}}` to control
spacing. If a token isn't used in the preview_html, that option will have no visible effect.

**Density matters.** Each architecture preview must include 15+ distinct elements to give a real
sense of the layout: headline, subhead, body paragraph, label/overline, stat with number, secondary
stat, quote/testimonial, attribution, card with title+body, second card (different treatment),
code/command block, primary button, secondary button, list or tags, accent divider/rule, and a data
element (table row, progress bar, or chart).

Optionally include `components` (component styling rules) and `dos` (do's and don'ts) as strings —
these appear in the generated `design.md`.

**Layout constraint:** all preview HTML must use percentage widths or `max-width: 100%`. Use
`flex-wrap: wrap` on all flex rows. Absolute-positioned decoratives must stay within a parent with
`overflow: hidden`.

**Security:** architecture `preview_html` must not contain `<script>` tags, event handlers
(`onclick`, `onerror`, etc.), or `javascript:` URLs — it is injected via `innerHTML`.

**Image URLs:** when using background images in `preview_html`, use `url(path/to/image.jpg)`
WITHOUT quotes around the path. Single quotes like `url('path.jpg')` break because `preview_html`
is inside a `style='...'` attribute — the inner single quotes terminate the outer attribute.

**Palette variety:** always include a mix of light, dark, and tinted backgrounds across the 6
palettes — even for calm/wellness prompts.

### Example architecture object

```json
{
  "name": "Editorial Stack",
  "description": "Vertical rhythm with large type, pull quotes, and data callouts",
  "tag": "editorial / longform / narrative",
  "mood": "Confident, unhurried, typographically driven",
  "preview_html": "<div style='background:{{bg}};color:{{fg}};padding:{{pad}};min-height:100vh;font-family:\"{{bf}}\",sans-serif;font-weight:{{bw}};'>...</div>"
}
```

### Mood board data format

Each mood board pre-selects one option from each category. A person picks a mood board in Phase 1,
then fine-tunes in Phase 2 with those selections pre-filled.

```json
{
  "name": "Terminal Precision",
  "description": "Code-forward, data-dense, CLI energy. Dark canvas, monospace body, sharp corners.",
  "theme": "dark",
  "arch_index": 0,
  "palette_index": 0,
  "type_index": 0,
  "corners_index": 0,
  "density_index": 0,
  "depth_index": 1,
  "easing_index": 0,
  "corners": "0px",
  "padding": "12px",
  "gap": "8px",
  "shadow": "0 2px 16px rgba(0,230,255,0.15)"
}
```

Indices reference into the ARCHITECTURES, PALETTES, and TYPEPAIRS arrays. The template renders a
mini preview of each mood board using its architecture's `preview_html` with the mood board's
palette/type applied.

### Prompt context data format

```json
{
  "title": "AI Coding Assistant",
  "headline": "Your Code, Understood.",
  "subline": "An AI coding assistant that reads your entire codebase.",
  "section_desc": "Layout options for your product launch"
}
```

`title` appears in the Phase 1 header. `headline` and `subline` replace `{{prompt_headline}}` and
`{{prompt_sub}}` in architecture preview_html so previews show real content.

### Content tokens in preview_html

In addition to the standard design tokens (`{{bg}}`, `{{fg}}`, `{{ac}}`, etc.), architecture
`preview_html` can use `{{prompt_headline}}` (the actual headline text) and `{{prompt_sub}}` (the
actual subline text). This makes previews contextual — a person sees their own content styled, not
generic placeholders.

### Serving and selection

4. Serve the file locally, e.g. `cd <project-dir> && python3 -m http.server 8723 &` (use port 8723
   or any unused port above 8000; try the next port if the check fails). Verify with a curl check
   before sharing the link — only share it if it returns HTTP 200.
5. Once a selection is made, the output is a design.md-spec-compliant file: YAML frontmatter with
   `colors`, `typography`, `rounded`, and `spacing` tokens, followed by `## Overview`, `## Colors`,
   `## Typography`, `## Layout`, `## Elevation`, `## Components`, and `## Do's and Don'ts` prose
   sections. Save it verbatim to `design.md` in the project root, kill the background server, then
   proceed with construction.

## Design Adherence

Post-authoring verification that the composition follows the design spec. Run it after building,
before serving the preview.

If a design spec (`frame.md` / `design.md`) exists, check the built composition against it:

1. **Colors** — every hex value in the composition appears in the spec's palette section (however
   it's labeled: Colors, Palette, Theme, etc.). Flag any invented colors.
2. **Typography** — font families and weights match the spec's type spec. No substitutions.
3. **Corners** — border-radius values match the declared corner style, if specified.
4. **Spacing** — padding and gap values fall within the declared density range, if specified.
5. **Depth** — shadow usage matches the declared depth level, if specified (flat = none, subtle =
   light, layered = glows).
6. **Avoidance rules** — if the spec has a section listing things to avoid (commonly "What NOT to
   Do", "Don'ts", "Anti-patterns", or "Do's and Don'ts"), verify none are present.

Report violations as a checklist. Fix each one before serving.

If no design spec exists (house-style-only path), verify instead:

1. **Palette consistency** — the same bg, fg, and accent colors are used across all scenes. No
   per-scene color invention.
2. **No lazy defaults** — check the composition against the "Lazy Defaults to Question" list above.
   If any appear, they must be a deliberate choice for the content, not a default.

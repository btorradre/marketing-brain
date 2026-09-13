# Data attributes and tracks reference

Every HyperFrames composition uses `data-*` attributes to declare timing and structure to the framework. This is the full attribute table plus the rules behind `data-track-index` and relative timing.

## Composition root

Every renderable composition needs one root element:

| Attribute | Required | Meaning |
|---|---|---|
| `data-composition-id` | Yes | Unique ID. Must match the animation registry key on `window.__timelines`. |
| `data-width` / `data-height` | Yes | Pixel frame size. Common values: `1920x1080`, `1080x1920`, `1080x1080`. |
| `data-duration` | Conditional* | Render duration in seconds (total length / frame count), not the GSAP timeline length. **Read once at compile time**, like `data-width`/`data-height`: a static root `data-duration` is locked before scripts run, so a script or a variables-driven value cannot change the render length. To vary length per render, author the root `data-duration` directly. (A clip's own `data-duration` is different — it's re-read from the live DOM, so scripts/variables can drive it.) Only when the root omits `data-duration` does the renderer derive total length from the live DOM/timeline after scripts run. |
| `data-fps` | No | Optional frame rate hint. Render flags can override output fps. |
| `data-composition-variables` | No | JSON array of variable declarations (on `<html>`). See `variables-and-media.md`. |

\* `data-duration` is optional whenever the runtime can auto-infer duration: a registered GSAP timeline, a finite CSS animation, a finite WAAPI `element.animate()`, or a registered Lottie animation. It is **required** for Three.js (no auto-inference), for infinite/unbounded CSS or WAAPI animations, and for any composition with no GSAP timeline and no animation signal at all. See `determinism-layout-motion.md` → "Duration contract for non-GSAP runtimes" for the per-runtime breakdown.

The root should be `position: relative`, have explicit pixel dimensions, and hide overflow unless intentionally composing outside the frame.

## Clip attributes

Timed child elements are clips. **`class="clip"` is required on visible timed elements** (`<div>`, `<img>`, etc.) — without it the runtime keeps the element visible for the whole composition, ignoring `data-start`/`data-duration`. Omit `class="clip"` on `<video>` (framework manages visibility directly) and `<audio>` (no visual).

**Clips must be direct children of the composition root.** A clip nested inside a wrapper `<div>` is not registered — most visibly, a `<video>` inside a wrapper is never seeked/decoded and renders black. To wrap or transform a clip, put the wrapper *inside* the clip, or animate the clip element itself; do not wrap the clip. (`<video>`/`<audio>` additionally must be at the host root, never in a sub-composition's `<template>` — see `variables-and-media.md`.)

| Attribute | Required | Meaning |
|---|---|---|
| `id` | Yes | Stable DOM ID for linting, timeline targets, and debugging. Must be unique across the *assembled* page — see the note on duplicate ids below. |
| `data-start` | Yes | Start time in seconds, or a supported clip-time reference (see "Relative timing" below). |
| `data-duration` | Required for `div`, `img`, and sub-compositions | Duration in seconds. Video/audio can default to media duration when known. |
| `data-track-index` | Yes | Timeline track. Clips on the same track must not overlap. |
| `data-media-start` | No | Offset into the media source, in seconds. |
| `data-volume` | No | Static audio volume, `0` to `1`, default `1`. For fades, animate `volume` on the timeline instead. |
| `data-has-audio` | No (`<video>` only) | `"true"` to declare the video carries an audio track when auto-detection would miss it. |

**Visibility window is inclusive of both ends.** A clip shows while `start ≤ t ≤ start + duration` — it still renders at exactly `t = start + duration`, so the final frame holds the animation's resolved end state. A reveal/entrance that lands exactly on `data-duration` is therefore visible on the last frame; it does not need to finish *before* `data-duration` to guarantee the end state renders.

## Sub-composition host attributes

When a clip is a sub-composition host (loads another composition file):

| Attribute | Required | Meaning |
|---|---|---|
| `data-composition-id` | Yes | The internal composition ID of the loaded file. |
| `data-composition-src` | Yes | Path to the sub-composition HTML file. |
| `data-width` / `data-height` | Yes | Render dimensions for the sub-composition instance. |
| `data-variable-values` | No | Per-instance variable overrides as JSON. |
| `data-var-src` | No | Binds the element's `src` to a declared variable id (media/image substitution, authored src = fallback). |
| `data-var-text` | No | Binds the element's own text to a scalar variable id; children are preserved. |

See `sub-compositions.md` for the full wiring pattern.

## Authoring hints

- `id="root"` — a common convention so CSS can target the composition root with `#root` instead of `[data-composition-id="main"]`. Not required by the runtime, but consistent with the rest of the ecosystem.
- `class="clip"` — required runtime visibility marker on visible timed elements.
- `data-layout-allow-overflow` — tells the layout auditor that overflow on this element (or its descendants) is intentional. Notes:
  - The layout audit measures the element's bounding box at sampled timestamps, not rendered pixels — CSS `overflow: hidden` clips the visual but does **not** suppress a layout finding. This attribute is the actual escape hatch; CSS overflow alone is not.
  - Can be set on the composition root as well as any child. When the flagged offender is the root reporting its own children's union as overflowing, put the fix on the root, not on individual text descendants — shrinking font sizes will not converge.
  - In a multi-scene composition where every scene-local element stays in the DOM during other scenes' time windows, the layout-box union almost always overflows the canvas during morph seams — mark the root and every scene-local element with this attribute at construction, not after the fact.
  - **This attribute has a wide blast radius.** It's inherited down the subtree, so it also suppresses rendered-perception checks for text clipping, cramped containers, and foreground-over-panel collisions for every descendant. Putting it on a persistent panel that also hosts real foreground content disables collision checks on that content for the panel's whole lifetime. Prefer the narrowest opt-out — scope it to the smallest decorative wrapper, or use a per-element bleed flag for one intentional primary-text crop. Off-canvas and foreground-over-panel checks still run even under this attribute, so it can't hide a wordmark sliced by the frame edge or text bleeding onto a panel edge.
- `data-layout-ignore` — exclude this element from layout audits entirely.

## Legacy / removed attributes

| Legacy name | Use instead |
|---|---|
| `data-layer` | `data-track-index` |
| `data-end` | `data-duration` |

## Tracks and clips

Clips are timed children of the composition root. **Tracks are a temporal-overlap concept, not a visual-stacking concept.**

A clip is any DOM element with `data-start`, `data-duration` (where required), and `data-track-index`. Common kinds: visual `<div>` clips (scenes, cards, overlays — always require `data-duration`); sub-composition hosts (always require `data-duration`); video clips (`<video>` with `muted` and `playsinline`, duration can default to media length); audio clips (`<audio>`, duration can default to media length); image clips (`<img>`, always requires `data-duration`).

`data-track-index` controls temporal overlap, not paint order:

- Two clips on the same `data-track-index` must NOT overlap in time — the lint tooling flags this.
- Visual layering (front/back) is controlled by CSS `z-index`, not by track index. A clip on track `5` is not "above" a clip on track `1` — it's just on a different lane in time.

Common track conventions: track 0 for base video (e.g. an A-roll); track 1+ for visual scenes, overlays, captions; higher tracks (e.g. 10+) for audio, kept separate from visual tracks so overlap linting stays clear. When adding a new clip to an existing composition: find an existing track with no overlap against your new clip's time range, or pick a fresh track index — never overlap two clips on the same track (the render is undefined if you do).

`data-start` is in seconds, measured from the start of the composition. For sub-compositions, the sub-composition's internal timeline runs from `data-start` to `data-start + data-duration` of the host. `data-media-start` (on `<video>`/`<audio>`) is an offset into the *source media* — use it to skip the first few seconds of a media file without trimming the file itself.

### Relative timing

`data-start` accepts a clip ID instead of a number, meaning "start when that clip ends." Add `+ N` / `- N` to offset; a negative offset produces overlap (useful for crossfades).

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main" data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
<video
  id="scene-a"
  data-start="intro + 2"
  data-duration="20"
  data-track-index="0"
  src="..."
></video>
<video
  id="scene-b"
  data-start="intro - 0.5"
  data-duration="20"
  data-track-index="1"
  src="..."
></video>
```

Rules: references resolve **inside the same composition only** — they cannot reach into a parent or sibling sub-composition. The referenced clip must have a known duration (explicit `data-duration`, or inferred from media) or the reference cannot resolve. **No circular references** — `A → B → A` is rejected and cycles are detected. A value that parses as a number is always treated as absolute seconds; otherwise the resolver expects `<id>`, `<id> + <number>`, or `<id> - <number>` (whitespace optional). References can chain (`A → B → C`) — keep chains under 3–4 levels for readability. Negative offsets create overlap; overlapping clips must be on **different tracks** (same-track overlap is rejected).

### Duplicate-id note

Every `id` must be unique across the *assembled* page, not just within one file. Because sub-compositions are authored and often previewed as separate files, it's easy to give two different scenes' hero image or video the same id (e.g. `#hero-video` in both `compositions/act1.html` and `compositions/act2.html`) — each file looks completely valid in isolation, and most lint tooling checks one file at a time and misses the cross-file collision. At render time the frame producer looks elements up by id; a duplicate causes both instances to come back blank. Prefix element ids inside a sub-composition with that composition's own id (`#act1-hero-video`) to make collisions structurally impossible.

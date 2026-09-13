# HyperFrames Core — Composition Contract

HyperFrames renders video from HTML. A composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable (every frame can be reproduced from a time value alone, with no notion of "playback"), and whose media playback (video/audio) is owned by the framework rather than the page's own JavaScript. This document is the technical contract for building one renderable HyperFrames project: how to structure the HTML/CSS/JS, how timing and tracks work, how sub-compositions and variables work, the hard determinism and layout rules the render engine depends on, the plan-layer file formats (`BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md`), and the production/review process for taking a video from an approved plan to a finished render. Use it whenever you are asked to build, edit, inspect, validate, or reason about a HyperFrames HTML video composition, storyboard, or brief — it is the reference to read before writing composition HTML.

## How to use this

1. **Establish intent before building anything.** Before writing HTML, pin down: what the video is for (destination/platform), the target canvas size, the target length, the one message it must communicate, the audience, and the language. Only ask about fields that are genuinely unknown and that would change the output — infer everything the request already answers. See "The brief: capturing and locking intent" below for the full field registry and question discipline.
2. **Write the intent down as `BRIEF.md`** at the project root before any other project file exists. This is the durable record of what was confirmed — later steps (and anyone resuming the work later) read this file instead of re-asking the same questions.
3. **Decide the project's architecture** — one big HTML file ("monolithic") or one file per scene wired together by an orchestrator file ("modular"). See "Two architectures" below. Prefer modular once the video has three or more scene cuts.
4. **Plan the video as a storyboard** — an ordered list of frames/scenes with a one-line description, rough duration, narration guide, and transition, before writing any composition markup. Write this to `STORYBOARD.md`. If a review process is available (a live board, a shared document, or simply presenting the plan to whoever commissioned the video), present the plan as frame cards and get it approved before building.
5. **Optionally sketch layouts first.** For a plan that needs sign-off on layout before full visual treatment, build quick unstyled wireframe versions of each frame (real headline/stat text placed where it will live, plain blocks standing in for charts/media, no animation, minimal styling) and get those approved before doing full visual design and motion.
6. **Build each composition file** following the data-attribute contract, the determinism rules, and the layout rules below. If building many independent scenes, they can be produced independently and in parallel (by different people or different automated workers) as long as each one is self-contained and gets verified before being merged in — see "Building scenes independently" below.
7. **Assemble** the scenes into the final index composition (tracks, sub-composition slots, continuous audio at the root).
8. **Add transitions, captions, and audio** as needed.
9. **Verify determinism and layout** — run the project's lint/check tooling, and eyeball a handful of representative frames (a "contact sheet" / snapshot at scene midpoints) rather than trusting automated checks alone. Several of the rules below are silent bugs that automated gates can miss.
10. **Get sign-off, then render**, and only then treat the video as delivered. Never render before an explicit approval on the final look.

## Two architectures

There are two ways to structure a HyperFrames project. Both use the identical runtime contract (`data-*` attributes plus a `window.__timelines[id]` registry) — the choice is structural, not behavioral.

| | Monolithic (single file) | Modular (sub-compositions) |
|---|---|---|
| Project layout | `index.html` only | `index.html` + `compositions/<scene>.html` per scene |
| Where scenes live | Inline `<section class="clip">` siblings under the root | Each scene is a separate file wrapped in `<template>` |
| Timeline registration | One timeline keyed at the root's `data-composition-id` | Root timeline (often near-empty) + one timeline per sub-composition, each keyed by its own id |

**Pick monolithic when:** the whole video is one continuous scene with no hard cuts; scenes share heavy state (one canvas/WebGL context spanning the whole video, a single SVG that morphs across all beats); total scope is small (roughly 200–400 lines of markup + script); no scene is reused across projects.

**Pick modular when:** the video has clear scene cuts, each its own segment of the timeline; some scenes are large (over ~100 lines of markup or significant scripted animation); a scene is reusable (a kinetic intro, an end-card logo lockup, a transition); the video has continuous audio spanning multiple visual segments (keep audio at the root, visual segments as sub-compositions); you want to author or iterate on scenes in isolation.

**Refactoring between them is mechanical and reversible.** To lift a monolithic scene into a sub-composition: wrap the scene's markup, its scoped CSS, and its slice of the parent timeline into a `<template>`; save it as `compositions/<scene>.html`; replace the inline content in `index.html` with a slot `<div data-composition-src="compositions/<scene>.html">`; have the sub-composition register its own timeline at `window.__timelines["<scene>"]`. The parent timeline shrinks accordingly. If a monolithic project is approaching three or more scene cuts, modularize before adding the next scene — a mixed project where some scenes are inline and siblings live in `compositions/` is the hardest shape to maintain.

### The modular orchestrator pattern

When using sub-compositions, `index.html` should be thin: its job is to declare slots, lay them out in time, mount the root-level audio track, and register a (usually near-empty) root timeline. All scene animation lives inside the sub-compositions.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #000;
      }
      #root {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      /* Sub-comp slots stretch to fill the root. */
      [data-composition-id="root"] > div[data-composition-src] {
        position: absolute;
        inset: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="root"
      data-width="1920"
      data-height="1080"
      data-duration="30"
    >
      <!-- Sequential scenes — each one a sub-composition slot. -->
      <div
        id="el-intro"
        data-composition-id="intro"
        data-composition-src="compositions/intro.html"
        data-start="0"
        data-duration="6"
        data-track-index="1"
      ></div>

      <div
        id="el-body"
        data-composition-id="body"
        data-composition-src="compositions/body.html"
        data-start="6"
        data-duration="18"
        data-track-index="1"
      ></div>

      <div
        id="el-outro"
        data-composition-id="outro"
        data-composition-src="compositions/outro.html"
        data-start="24"
        data-duration="6"
        data-track-index="1"
      ></div>

      <!-- Continuous audio at the root — survives scene cuts. -->
      <audio
        id="el-bgm"
        src="assets/bgm.mp3"
        data-start="0"
        data-duration="30"
        data-track-index="10"
        data-volume="0.6"
      ></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

Key properties of this layout:

- **Visual scenes on the same `data-track-index`** (e.g. `1`) — sequential, cannot overlap on the same track. For a cross-fade between two scenes, put one on a higher track and overlap their times by the fade duration.
- **Audio on a separate, higher track index** (e.g. `10`) — keeps overlap-linting rules clear of any visual collisions.
- **Root timeline is near-empty.** All animation lives in the sub-compositions. A root-level fade-to-black at the very end is fine; don't stage a parallel animation track from the root.
- **Host slot ids** use `el-<name>` or `<scene-id>`. The slot's `data-composition-id` must still equal the sub-composition's internal id.

### Sub-composition archetypes

**A. Content scene (default).** The sub-composition contains the scene's full DOM, scoped CSS, and timeline. Most scenes are this.

**B. Host media + main-timeline driver (required for any `<video>`/`<audio>`).** Media playback only works when the `<video>`/`<audio>` element is a direct child of the host root — never inside a sub-composition's `<template>` (it renders blank/black there). This applies to every clip, including a scene-specific one — not just media that spans scenes. The scene's sub-composition keeps the frame/shell; the media is a host sibling positioned over it. A sub-composition's timeline cannot drive host elements (a selector query does not resolve across that boundary), so author the media's per-scene motion (scale/opacity/morph/tilt/breathing) on the main timeline in `index.html`, at global time = scene-local time + the scene slot's `data-start`.

```html
<!-- index.html (host) -->
<div
  id="el-final"
  data-composition-id="final-anim"
  data-composition-src="compositions/final-anim.html"
  data-start="20"
  data-duration="6"
  data-track-index="1"
></div>

<!-- media is a DIRECT root child; sits over the sub-comp's frame -->
<video
  id="final-video"
  class="clip"
  src="assets/final.mp4"
  data-start="20"
  data-duration="6"
  data-track-index="2"
  muted
  playsinline
  style="position:absolute; left:360px; top:100px; width:1200px; height:680px; object-fit:cover; border-radius:24px;"
></video>

<script>
  // MAIN timeline drives the host video. Global time: scene starts at 20.
  window.__timelines = window.__timelines || {};
  const main = window.__timelines["main"];
  main.fromTo(
    "#final-video",
    { scale: 1.4, filter: "blur(14px)" },
    { scale: 1.0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" },
    20,
  ); // = slot data-start (+ any scene-local offset)
</script>

<!-- compositions/final-anim.html — frame/shell only, no <video>, no host-element animation -->
<template>
  <div
    data-composition-id="final-anim"
    data-width="1920"
    data-height="1080"
    data-duration="6"
    style="position:absolute; inset:0; pointer-events:none;"
  >
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // animate ONLY this sub-comp's own elements here (labels, frame, overlays)
      window.__timelines["final-anim"] = tl;
    </script>
  </div>
</template>
```

Caveats: the host media must be a direct root child and exist statically in `index.html`'s DOM. Clip lifecycle owns the media element's visibility across its `[data-start, data-start+data-duration]` window — main-timeline opacity/scale tweens compose fine with it, but for an opacity reveal/crossfade prefer a host wrapper so you aren't fighting the lifecycle on the media element itself. Two media elements sharing the same `src` + `data-start` trigger a benign duplicate-media warning; both still render.

**C. Multi-scene merge.** When several beat-level scenes share continuous state (a chat thread that grows, a persistent headline word carrying across a cut, one canvas with internal phase changes), collapse them into one sub-composition and use internal phase `<div>`s rather than multiple sub-composition slots:

```html
<!-- compositions/act2-merged.html -->
<template>
  <div data-composition-id="act2-merged" data-width="1920" data-height="1080" data-duration="9">
    <style>
      [data-composition-id="act2-merged"] .phase {
        position: absolute;
        inset: 0;
        opacity: 0;
      }
    </style>
    <div class="phase" id="phase-a">…</div>
    <div class="phase" id="phase-b">…</div>
    <div class="phase" id="phase-c">…</div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.set("#phase-a", { opacity: 1 }, 0);
      tl.to("#phase-a", { opacity: 0, duration: 0.4 }, 3.0);
      tl.set("#phase-b", { opacity: 1 }, 3.0);
      // …
      window.__timelines["act2-merged"] = tl;
    </script>
  </div>
</template>
```

Reach for this over multiple sequential slots when scenes share DOM, share a canvas, or need to cross-fade with persistent elements. Each phase is just a `<div>` inside the same sub-composition — the parent timeline never needs to know about the internal phase boundaries.

**D. Audio at root, reactive visual inside.** Audio always lives at the host (`index.html`) as a root-level `<audio>` element so playback survives scene cuts. A sub-composition that visualizes audio should read a pre-baked frequency curve at init, then sample that baked curve from its own timeline — the visual must still be a deterministic function of the timeline's time, never of the audio element's live playback position.

### Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Sub-comp file | `compositions/<scene-id>.html` | `compositions/act0-intro-bell.html` |
| Sub-comp `<template>` id (optional) | `<scene-id>-template` | `<template id="act0-intro-bell-template">` |
| Sub-comp root `data-composition-id` | `<scene-id>` (must match host slot) | `data-composition-id="act0-intro-bell"` |
| Timeline registry key | matches `data-composition-id` | `window.__timelines["act0-intro-bell"]` |
| Host slot `id` | `el-<short>` or `<scene-id>` | `id="el-intro"`, `id="act0"` |
| Element ids inside a sub-comp | prefix with the scene id | `#act0-bell`, `#b1-tape` |
| Audio at root | `data-track-index` well above visual tracks | `10` while visuals use `1` |

The `-template` suffix on `<template>` is conventional but not required — the runtime extracts contents from whichever `<template>` is in `<body>`, regardless of id. The id prefix inside a sub-composition is the only real safeguard against id collisions when multiple sub-compositions are mounted into the same host page at once.

### Editing an existing project

Before adding or modifying scenes, identify which architecture is in use — a `compositions/` directory present means modular, absent means monolithic. In a monolithic project, add new scenes as inline `<section class="clip">` elements with a non-overlapping `data-start` and a sensible `data-track-index`, extending the existing single timeline. In a modular project, match the existing pattern: add a new file under `compositions/`, add a slot in `index.html`, keep the root timeline thin — don't start inlining new scenes into `index.html` when sibling scenes are sub-compositions. If a monolithic project needs a third or fourth scene cut, lift each scene into a sub-composition first. When picking a new slot's `data-start`/`data-duration`, continue the existing sequencing convention rather than introducing a new track index unless parallel visual layers are actually needed — most sequential-scene projects use exactly one visual track.

Also, when editing: read the existing files first and preserve unrelated timing, tracks, ids, variables, and media paths. Match existing composition ids and timeline keys. `data-hidden` on any composition element hides it in both preview and render, overriding its time window — it is non-destructive and reversible (used for temporarily toggling a layer off without deleting it).

## The two root forms (not interchangeable)

- **Standalone** (top-level `index.html`): the root `<div data-composition-id="…">` sits directly in `<body>` — **no `<template>` wrapper** (wrapping it hides all content and breaks rendering).
- **Sub-composition** (loaded via `data-composition-src`): the root **must** be wrapped in `<template>`.

Transport rule: the runtime only clones `<template>` contents — everything outside it (including the entire `<head>`, its styles and scripts) is discarded, so `<style>`/`<script>` must live **inside** the template.

Host-id rule: the host slot's `data-composition-id` must **exactly equal** the inner template's `data-composition-id`, and both must equal the `window.__timelines["<id>"]` key — no `-mount`/`-slot`/`-host` suffix on either side.

### Root must be sized (a silent layout bug)

The standalone root needs an explicit sized box (`width`/`height` in px), and every ancestor down to a `height: 100%` element must have a resolved height — otherwise a flex or `100%`-height child collapses to roughly 0 and content piles into the top-left corner. Don't rely on automated checks alone to catch this — inspect a rendered snapshot.

### One paused timeline

Each composition registers **exactly one** `gsap.timeline({ paused: true })` at `window.__timelines["<id>"]` (key = root `data-composition-id`), built **synchronously** at page load. Render duration is the root's `data-duration`, not the timeline's own length. Don't manually nest sub-timelines into the host timeline.

## Minimal composition

The smallest renderable HyperFrames composition — a standalone (top-level) root with one clip and one tween:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Minimal HyperFrames Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #0b0f14;
        color: white;
        font-family: Inter, system-ui, sans-serif;
      }
      #root {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      .clip {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
      }
      h1 {
        margin: 0;
        font-size: 96px;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-width="1920"
      data-height="1080"
      data-duration="5"
    >
      <section id="title-card" class="clip" data-start="0" data-duration="5" data-track-index="1">
        <h1 id="title">Hello HyperFrames</h1>
      </section>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.from("#title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

Required elements: a root `<div>` with `data-composition-id`, `data-start="0"`, `data-width`, `data-height`, `data-duration`; at least one clip (any element with `data-start`, `data-duration`, `data-track-index`); a GSAP timeline created paused and registered on `window.__timelines["<composition-id>"]`.

## Data attributes reference

### Composition root

Every renderable composition needs one root element:

| Attribute | Required | Meaning |
|---|---|---|
| `data-composition-id` | Yes | Unique ID. Must match the animation registry key on `window.__timelines`. |
| `data-width` / `data-height` | Yes | Pixel frame size. Common values: `1920x1080`, `1080x1920`, `1080x1080`. |
| `data-duration` | Conditional* | Render duration in seconds (total length / frame count), not the GSAP timeline length. **Read once at compile time**, like `data-width`/`data-height`: a static root `data-duration` is locked before scripts run, so a script or a variables-driven value cannot change the render length. To vary length per render, author the root `data-duration` directly. (A clip's own `data-duration` is different — it's re-read from the live DOM, so scripts/variables can drive it.) Only when the root omits `data-duration` does the renderer derive total length from the live DOM/timeline after scripts run. |
| `data-fps` | No | Optional frame rate hint. Render flags can override output fps. |
| `data-composition-variables` | No | JSON array of variable declarations (on `<html>`). See "Variables" below. |

\* `data-duration` is optional whenever the runtime can auto-infer duration: a registered GSAP timeline, a finite CSS animation, a finite WAAPI `element.animate()`, or a registered Lottie animation. It is **required** for Three.js (no auto-inference), for infinite/unbounded CSS or WAAPI animations, and for any composition with no GSAP timeline and no animation signal at all. See "Duration contract for non-GSAP runtimes" below for the per-runtime breakdown.

The root should be `position: relative`, have explicit pixel dimensions, and hide overflow unless intentionally composing outside the frame.

### Clip attributes

Timed child elements are clips. **`class="clip"` is required on visible timed elements** (`<div>`, `<img>`, etc.) — without it the runtime keeps the element visible for the whole composition, ignoring `data-start`/`data-duration`. Omit `class="clip"` on `<video>` (framework manages visibility directly) and `<audio>` (no visual).

**Clips must be direct children of the composition root.** A clip nested inside a wrapper `<div>` is not registered — most visibly, a `<video>` inside a wrapper is never seeked/decoded and renders black. To wrap or transform a clip, put the wrapper *inside* the clip, or animate the clip element itself; do not wrap the clip. (`<video>`/`<audio>` additionally must be at the host root, never in a sub-composition's `<template>` — see "Media" below.)

| Attribute | Required | Meaning |
|---|---|---|
| `id` | Yes | Stable DOM ID for linting, timeline targets, and debugging. |
| `data-start` | Yes | Start time in seconds, or a supported clip-time reference (see "Relative timing"). |
| `data-duration` | Required for `div`, `img`, and sub-compositions | Duration in seconds. Video/audio can default to media duration when known. |
| `data-track-index` | Yes | Timeline track. Clips on the same track must not overlap. |
| `data-media-start` | No | Offset into the media source, in seconds. |
| `data-volume` | No | Static audio volume, `0` to `1`, default `1`. For fades, animate `volume` on the timeline instead. |
| `data-has-audio` | No (`<video>` only) | `"true"` to declare the video carries an audio track when auto-detection would miss it. |

**Visibility window is inclusive of both ends.** A clip shows while `start ≤ t ≤ start + duration` — it still renders at exactly `t = start + duration`, so the final frame holds the animation's resolved end state. A reveal/entrance that lands exactly on `data-duration` is therefore visible on the last frame; it does not need to finish *before* `data-duration` to guarantee the end state renders.

### Sub-composition host attributes

When a clip is a sub-composition host (loads another composition file):

| Attribute | Required | Meaning |
|---|---|---|
| `data-composition-id` | Yes | The internal composition ID of the loaded file. |
| `data-composition-src` | Yes | Path to the sub-composition HTML file. |
| `data-width` / `data-height` | Yes | Render dimensions for the sub-composition instance. |
| `data-variable-values` | No | Per-instance variable overrides as JSON. |
| `data-var-src` | No | Binds the element's `src` to a declared variable id (media/image substitution, authored src = fallback). |
| `data-var-text` | No | Binds the element's own text to a scalar variable id; children are preserved. |

### Authoring hints

- `id="root"` — a common convention so CSS can target the composition root with `#root` instead of `[data-composition-id="main"]`. Not required by the runtime, but consistent with the rest of the ecosystem.
- `class="clip"` — required runtime visibility marker on visible timed elements.
- `data-layout-allow-overflow` — tells the layout auditor that overflow on this element (or its descendants) is intentional. Notes:
  - The layout audit measures the element's bounding box at sampled timestamps, not rendered pixels — CSS `overflow: hidden` clips the visual but does **not** suppress a layout finding. This attribute is the actual escape hatch; CSS overflow alone is not.
  - Can be set on the composition root as well as any child. When the flagged offender is the root reporting its own children's union as overflowing, put the fix on the root, not on individual text descendants — shrinking font sizes will not converge.
  - In a multi-scene composition where every scene-local element stays in the DOM during other scenes' time windows, the layout-box union almost always overflows the canvas during morph seams — mark the root and every scene-local element with this attribute at construction, not after the fact.
  - **This attribute has a wide blast radius.** It's inherited down the subtree, so it also suppresses rendered-perception checks for text clipping, cramped containers, and foreground-over-panel collisions for every descendant. Putting it on a persistent panel that also hosts real foreground content disables collision checks on that content for the panel's whole lifetime. Prefer the narrowest opt-out — scope it to the smallest decorative wrapper, or use a per-element bleed flag for one intentional primary-text crop. Off-canvas and foreground-over-panel checks still run even under this attribute, so it can't hide a wordmark sliced by the frame edge or text bleeding onto a panel edge.
- `data-layout-ignore` — exclude this element from layout audits entirely.

### Legacy / removed attributes

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

## Sub-compositions

A sub-composition is a separate HTML file embedded in a host composition. HyperFrames loads it, seeks it independently, and composites the result into the host at `data-start`.

### Host wiring

In the host composition, the sub-composition appears as a clip with `data-composition-src`:

```html
<div
  id="chart"
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

`data-composition-id` on the host must match the internal `data-composition-id` of the file at `data-composition-src`. The host clip needs its own `data-start`, `data-duration`, `data-track-index`, `data-width`, `data-height`.

### Mental model — what the runtime actually does

When a host loads a sub-composition via `data-composition-src`, the runtime: (1) fetches the HTML file; (2) parses it as a DOM document; (3) **finds the `<template>` element and clones ONLY its contents into the host slot**; (4) everything **outside** the `<template>` (including the entire `<head>`) is **discarded**.

So `<template>` is not just a wrapper — it is the transport container. If a node needs to exist in the live render, it must be inside `<template>`. Full stop.

### File shape

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- head is metadata for the source file only; the runtime ignores it -->
  </head>
  <body>
    <template>
      <!-- EVERYTHING the runtime needs goes here: styles, markup, scripts -->
      <style>
        /* Root: style by #root, never a class. (At render the CSS is scoped to
           data-composition-id, so a class on the root stops matching — see Pitfall 3.) */
        #root {
          position: absolute;
          inset: 0;
          color: #fff;
        }
        /* .label, #bar, … — descendants, plain selectors */
      </style>

      <div id="root" data-composition-id="data-chart" data-width="1920" data-height="1080">
        <!-- sub-composition markup -->
      </div>

      <script>
        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
        // ... build timeline ...
        window.__timelines["data-chart"] = tl;
      </script>
    </template>
  </body>
</html>
```

Contrast with **standalone** compositions, which put the root directly in `<body>` with no `<template>` wrapper.

### Three pitfalls that pass static checks but break at render

Static file checks cannot prove the cross-file mount contract — these failures only appear when the runtime actually mounts the sub-composition.

**Pitfall 1 — `<style>` in `<head>` instead of inside `<template>`.** Standard HTML convention says put `<style>` in `<head>`; that's correct for a standalone file but **wrong** for a HyperFrames sub-composition, because the runtime only clones `<template>` contents — `<head><style>` is dropped on the floor.

```html
<!-- ❌ WRONG — looks normal, ships catastrophically broken -->
<head>
  <style>
    #root { font-size: 88px; ... }
  </style>
</head>
<body>
  <template>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>

<!-- ✅ RIGHT — styles are inside the template, root styled by #root (see Pitfall 3) -->
<head></head>
<body>
  <template>
    <style>
      #root { font-size: 88px; ... }
    </style>
    <div id="root" data-composition-id="data-chart" ...>...</div>
  </template>
</body>
```

Symptom: isolated checks pass and the render completes, but every text element appears as tiny unstyled default text in the top-left, and SVGs expand to canvas size because no CSS reached the live DOM. The same trap applies to `<script>` blocks, `<link rel="stylesheet">`, and custom-element registrations — anything that must execute or apply in the render belongs inside `<template>`.

**Pitfall 2 — host `data-composition-id` ≠ inner template `data-composition-id`.** It feels natural to give the host slot a different name (e.g. `chart-mount`) than the actual chart id (`data-chart`), but HyperFrames does not work that way — the host's `data-composition-id` is the lookup key the framework uses to find the registered timeline. Static checks pass because each file's ids are individually valid; the cross-file mismatch only blows up at render.

```html
<!-- ❌ WRONG — host renames the slot; runtime can't find the timeline -->
<!-- host file (e.g. index.html) -->
<div data-composition-id="chart-mount" data-composition-src="compositions/chart.html" ...></div>

<!-- chart.html -->
<template>
  <div data-composition-id="data-chart" ...>...</div>
  <script>
    window.__timelines["data-chart"] = tl;
  </script>
</template>

<!-- ✅ RIGHT — both ids match, and the timeline key matches them too -->
<div data-composition-id="data-chart" data-composition-src="compositions/chart.html" ...></div>
<!-- chart.html template root: data-composition-id="data-chart" -->
<!-- timeline: window.__timelines["data-chart"] = tl; -->
```

Symptom: the render waits (often ~45 seconds per scene) for the sub-composition's timeline to register, times out, then captures static initial-state frames — the video is full-length but no animation plays for the mismatched slot.

**Pitfall 3 — styling the root by a class instead of `#root`.** When sub-compositions are inlined into one composited render, each file's CSS gets scoped to its own `data-composition-id` so scenes can't leak styles into each other — every rule `S` becomes `[data-composition-id="<id>"] S`, a *descendant* selector. A rule whose leftmost selector is the root's own class (`.frame`) becomes `[data-composition-id="<id>"] .frame`, which cannot match the root itself (the root *is* the scoped element, not a descendant of it) — so every `.frame…` rule silently drops. `#root` is special-cased and keeps matching the root; plain descendant selectors match normally.

```html
<!-- ❌ WRONG — class on the root, stylesheet keyed off it -->
<template>
  <style>
    .frame {
      position: absolute;
      inset: 0;
      background: #faf9f5;
    }
    .frame .title {
      font-size: 120px;
    }
  </style>
  <div id="root" class="frame" data-composition-id="03-scene" ...>
    <div class="title">…</div>
  </div>
</template>

<!-- ✅ RIGHT — root styled by #root, descendants by plain selectors -->
<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      background: #faf9f5;
    }
    .title {
      font-size: 120px;
    }
  </style>
  <div id="root" data-composition-id="03-scene" ...>
    <div class="title">…</div>
  </div>
</template>
```

Symptom: identical to Pitfall 1 — tiny unstyled text in the top-left, images at natural size, only inline styles surviving. The trap is that isolated checks or single-scene previews can look correct because they don't reproduce the final scoped mount; the defect only appears in the composited render.

### Verification checklist before render

For every sub-composition file:

1. Confirm `<style>`, `<script>`, and the main markup all live *inside* `<template>` (the first occurrence of each should come after the opening `<template>` tag and before its close).
2. Confirm host `data-composition-id` == internal `data-composition-id` == the `window.__timelines[...]` key, for every sub-composition — all three strings must match exactly.
3. Confirm the root element is styled via `#root`, not via a class also declared on the `data-composition-id` element.

For the runtime end-to-end check, do a fast preview/snapshot pass and eyeball each sub-composition's rendered frame — that is the only check that reliably catches these three pitfalls; static inspection alone can miss all three.

### What HyperFrames does with the sub-composition

It loads the file and registers its timeline under its internal `data-composition-id`; seeks the sub-composition's timeline independently from the host's playhead; plays the sub-composition's content from `data-start` of the host clip, for `data-duration` seconds. Do **not** manually nest a sub-composition's timeline into the host timeline (e.g. adding it as a child of the host's GSAP timeline) — HyperFrames already drives them independently, and nesting causes double-seeks.

### The host clip's `data-duration` is the slot's visible window

`data-duration` on the host clip defines how long the slot is visible, and it takes precedence over the sub-composition's own internal timeline length. Two consequences: if the sub-composition's internal timeline finishes *before* `data-duration` elapses, the slot holds on the final frame for the rest of the window (no need to pad the timeline with empty tweens). If `data-duration` is *shorter* than the host composition, the slot ends — and goes blank — when its own `data-duration` elapses; this is intended, the clip is a fixed-length window, not "fill until the composition ends." To keep a sub-composition visible for the whole composition, set its `data-duration` to span the host window, or add another clip to cover the remaining time. Leaving a single full-bleed sub-composition shorter than the composition is almost always a mistake.

### Animations inside sub-compositions

Prefer `gsap.fromTo()` over `gsap.from()` for entrance tweens. The host re-seeks the sub-composition every time its clip becomes visible; `gsap.from()` records the starting state at registration time and can desync on seek-back, while `gsap.fromTo()` declares both endpoints explicitly and replays cleanly regardless of seek order.

### Per-instance variables

If the sub-composition declares variables on its `<html>` element (`data-composition-variables`), the host can override values per instance:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-variable-values='{"title":"Q4 Revenue","accent":"#66d9ef"}'
  data-start="2"
  data-duration="8"
  data-track-index="2"
  data-width="1920"
  data-height="1080"
></div>
```

The host can render the same sub-composition multiple times with different `data-variable-values` to produce per-instance variations.

## Variables and media

Two separate concerns, grouped because both control "what flows into the HTML from outside": runtime parameters (variables) and external media files (video/audio).

### Variables

Declare variables on the `<html>` element with `data-composition-variables`. Each declaration needs `id`, `type`, `label`, and `default`:

```html
<html
  data-composition-variables='[
    {"id":"title","type":"string","label":"Title","default":"Hello"},
    {"id":"accent","type":"color","label":"Accent","default":"#66d9ef"}
  ]'
></html>
```

Prefer declarative bindings — no script needed — for direct substitution:

```html
<img class="clip" data-start="0" data-duration="5" data-var-src="heroImage" src="fallback.jpg" />
<h1 class="clip" data-start="0" data-duration="5" data-var-text="title">Fallback</h1>
<style>
  .card {
    color: var(--accent);
  }
</style>
```

`data-var-src="id"` substitutes the element's `src` (a URL string, or an image reference object); the authored `src` is the fallback. `data-var-text="id"` substitutes the element's own text; element children (nested clips, animated spans) are preserved. Every scalar variable is applied automatically as a `--{id}` CSS custom property on the composition root, so `var(--id)` in CSS responds to overrides with no manual `setProperty` boilerplate. Bindings resolve identically in preview and render, and per-instance for sub-compositions. Caveat: media with audio should keep a real fallback `src`, since render-time audio extraction reads the authored attribute.

For logic beyond direct substitution (loops, conditionals, derived values), read values once during initialization:

```js
const { title, accent } = window.__hyperframes.getVariables();
document.getElementById("title").textContent = title;
```

**Variable rules:**

- Supported types and their extra options (consumed by an editing UI, if one is present): `string` (optional `placeholder`, `maxLength`), `number` (optional `min`, `max`, `step`, `unit`), `color` (none), `boolean` (none), `enum` (**required** `options: [{ "value": "...", "label": "..." }, ...]`).
- Always provide useful `default` values so a preview works without any override supplied.
- Use `data-variable-values='{"title":"Pro"}'` on sub-composition hosts for per-instance overrides.
- The render tooling accepts a `--variables` JSON object (or a `--variables-file`) for render-time overrides, and a strict mode that turns undeclared keys, type mismatches, and invalid enum values into hard errors instead of warnings.
- Read values once during init, not on every animation tick — variables don't change mid-render.
- Media color grading can reference exact variables inside a color-grading configuration; the runtime resolves the reference from the current composition's variables before applying shader adjustments, finishing details, blur/pixelate effects, and custom LUTs.

**Two JSON shapes, easy to confuse:** `data-composition-variables` is an *array of declarations* (the schema): `[{id, type, label, default}, ...]`. Values passed at render time or via `data-variable-values` are *objects keyed by id* (the actual values): `{ title: "Q4", accent: "#fff" }`.

### Media

**Non-negotiable: `<video>`/`<audio>` must be a direct child of the host composition root (`index.html`).** The runtime only registers and drives media that is a direct root child. Media placed inside a sub-composition's `<template>`, or wrapped in any intermediate `<div>`, is never seeked/decoded — it renders blank (paper/white) or black. Don't rely on automated checks alone here; a per-frame snapshot reveals the blank panel.

Consequences: a scene-specific video clip still lives at the host root, not inside that scene's sub-composition — the sub-composition keeps only the frame/shell, and the media is a sibling host element positioned over it. A sub-composition cannot reach or animate host elements — neither a DOM query nor a GSAP selector string resolves across that boundary; a sub-composition's timeline only drives its own subtree. So all per-scene motion on host media (scale/opacity/morph/tilt/breathing) must be authored on the **main timeline** in `index.html`, at **global time** (scene-local time + the scene slot's `data-start`). For 3D tilt without a perspective parent, use GSAP's `transformPerspective` on the element.

Video elements must be muted and inline. Audio must be a separate `<audio>` element, even when it uses the same source file as a video:

```html
<video
  id="a-roll"
  class="clip"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="0"
  muted
  playsinline
></video>

<audio
  id="a-roll-audio"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="10"
  data-volume="1"
></audio>
```

**Media rules:** don't call `video.play()`, `audio.play()`, pause, or seek in composition code — HyperFrames owns playback. Don't place media inside a sub-composition's `<template>` or any wrapper `<div>` — direct host-root child only, else it never decodes. Don't try to drive host media from a sub-composition's timeline — it has no effect; drive it from the main timeline at global time. Don't animate timed media element dimensions directly — animate a non-timed wrapper instead. Don't nest video inside a timed wrapper — put timing on the media element itself, or keep the wrapper untimed. Add `crossorigin="anonymous"` for external media that needs canvas capture or pixel inspection. Audio always lives on a separate `<audio>` element even if its source file is identical to a `<video>`'s — the `<video>` stays muted, the `<audio>` carries sound. For volume fades/ducking, animate `volume` on the timeline (e.g. `tl.to("#bgm", { volume: 0, duration: 1 }, "outro")`) rather than swapping `data-volume` — the runtime probes the timeline's volume keyframes and applies them identically in preview and render; `data-volume` is only the static baseline for elements no tween touches.

For media duration: `<video>` and `<audio>` can omit `data-duration` if the media's intrinsic length is known and the full clip should play; otherwise provide `data-duration` explicitly.

Codec note: rendering decodes video via FFmpeg (frames pre-extracted and injected), so HEVC/H.265 assets (8/10-bit) render correctly everywhere; live preview auto-proxies any browser-hostile asset (transcoding and caching an H.264 copy on first use).

## Determinism, animation runtime, and layout

HyperFrames seeks compositions frame-by-frame. Every frame must be reproducible from its time value alone — same input time, same pixels. Three contracts enforce this: the animation runtime contract, the determinism rules, and the layout contract.

### Animation runtime contract

GSAP is the primary runtime. The core requirement is generic: animation state must be seekable from HyperFrames time.

For GSAP: create the timeline **synchronously** during page initialization. Use `gsap.timeline({ paused: true })`. Register it on `window.__timelines["<composition-id>"]`, where the key must match `data-composition-id` on the composition root. Do **not** call `tl.play()` for render-critical motion. Do **not** build timelines inside `async` functions, Promises, `setTimeout`, or event handlers — the renderer can sample the page before they finish. Do **not** create empty tweens only to set a duration — use `data-duration` on the clip instead. Do **not** `gsap.set()` clip elements from later scenes at page-load time — they are not in the DOM yet; use `tl.set(selector, vars, time)` inside the timeline at or after the clip's `data-start`.

### Duration contract for non-GSAP runtimes

The render engine needs a positive total duration before it will capture a single frame — without one, capture fails outright ("Composition has zero duration"). A GSAP timeline supplies this automatically. CSS, WAAPI, and Lottie compositions have no timeline object, so the runtime infers duration itself:

- **CSS**: longest `animation-delay` + `animation-duration` × finite `animation-iteration-count` across animated elements (offset by each element's `data-start`). `animation-iteration-count: infinite` cannot be inferred.
- **WAAPI**: longest `element.animate()` effect's computed end time. Infinite `iterations` cannot be inferred.
- **Lottie**: the registered animation's native length (total frames ÷ frame rate, or the player's own duration) — always finite regardless of loop setting.
- **Three.js**: not inferable at all — time only flows in via a seek event; there's no animation-clip inspection.

`data-duration` on the root element is therefore optional whenever every non-GSAP animation on the page is finite. It is **required** when: the composition has an infinite/unbounded CSS or WAAPI animation, the composition uses Three.js, or there is no GSAP timeline and no animation signal at all for any adapter to discover.

### Determinism rules

Rendered frames must be reproducible from the requested time. Do **not** use any of the following for visual state:

- `Date.now()`, `performance.now()`, or any render-time clock.
- Unseeded `Math.random()` — use a seeded pseudo-random generator if random-looking placement is needed.
- Render-time network fetches for required assets — inline or pre-bundle them.
- Hover, scroll, pointer, or focus state — the renderer has no input events.
- Infinite loops such as `repeat: -1`. Compute a finite count instead: `repeat: Math.max(0, Math.floor(duration / cycleDuration) - 1)` — use `floor`, not `ceil` (`ceil` overshoots the composition's duration), and `max(0, …)` avoids a negative repeat count, which GSAP treats as infinite.

Also avoid: animating anything outside the visual-property allowlist — `opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, and transforms. Never tween `display` or raw `visibility`. GSAP's `autoAlpha` is allowed on a registered seekable timeline because it interpolates opacity and only changes actual visibility at the fully-hidden endpoint. A zero-duration `tl.set(..., { visibility: "hidden" | "visible" })` is also allowed at an explicit beat boundary for a deterministic hard kill. **Both exceptions apply only to non-clip elements or wrappers inside a clip — never target a `.clip` element itself:** the framework alone controls a clip's visibility lifecycle. Also avoid animating the same property on the same element from multiple timelines at the same time — GSAP's overwrite behavior in that situation is order-dependent and can flip between renders.

### Layout contract

Build the visible end-state in static HTML and CSS first, then animate from/to that state.

- The composition root has fixed pixel frame dimensions.
- **The root composition's total duration (render length/frame count) is fixed at compile time** — read once from the static root `data-duration` before scripts run, exactly like `data-width`/`data-height`. A script or an override value that rewrites the root `data-duration` afterward is ignored. To vary render length per output, author the root `data-duration` directly. (A *clip's* own `data-duration` is re-read from the live DOM, so scripts/variables can still drive clip lengths. Only when the root omits `data-duration` does the renderer probe the live DOM/timeline for total length.)
- Scene containers should fill the scene with `width: 100%; height: 100%; box-sizing: border-box`.
- Use padding, flex, grid, and `max-width` for layout. Avoid positioning main content with hardcoded `top`/`left` offsets when a layout container can do it.
- Use `position: absolute` for layers and decorative elements, not as the default content-layout strategy.
- Prefer transforms and opacity for animation.
- Keep text inside its intended container — use `max-width`, wrapping, or a font-fitting helper such as `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })` if the runtime provides one.
- For text measurement without triggering DOM reflow, use a text-measurement helper if the runtime provides one (e.g. `window.__hyperframes.pretext`: `pretext.prepare(text, font)` then `pretext.layout(prepared, maxWidth, lineHeight)`) — pure arithmetic, safe to call per-frame for text reflow, shrinkwrap containers, and pre-render layout computation.
- **Do not** use `<br>` in body text. Forced breaks ignore the actual rendered font width and can produce an extra break when the line already wraps naturally, causing overlap. Let text wrap via `max-width`. Exception: short display titles where each word is deliberately meant to be on its own line.
- **Transformed elements must be block-level and sized.** `transform`/`scaleX`/`scaleY` is a no-op on an inline `<span>`, and scaling an auto-width (0px) element shows nothing — an invisible bar or fill. Give them `display: block`/`inline-block`/flex-item **and** a real `width`/`height` (e.g. `width: 100%` inside a sized parent). This is a silent bug automated checks may miss.
- **Absolutely-positioned decoratives that pulse or overshoot** (a `yoyo` scale, a `back.out` ease) need clearance at their *peak* size and must not straddle an `overflow: hidden` edge — otherwise they overlap a neighbor or get clipped. Position for the largest frame, not the resting one. Also a silent bug.

### Why this matters

The renderer takes a time value and produces a pixel buffer — there is no notion of "playback," only a fresh seek for every frame. Any state that depends on having reached this frame *through* a prior frame (timers, accumulated state, event-driven animations) will desync when the renderer samples out of order or in parallel. If you find yourself reaching for `setTimeout`, `requestAnimationFrame`, or `addEventListener` to drive a visual, rebuild it as a tween on the timeline instead.

## Full-screen motion pattern

For full-frame motion (continuous backgrounds, color washes, full-bleed visual states that span multiple clips), prefer a **shared background layer + transparent timed content layers** over stacked opaque scene backgrounds.

**Why:** stacking opaque scene divs means every scene change has to repaint the entire frame, every cross-scene visual continuity has to be faked, and every "global" state (a hue shift, a vignette, film grain) has to be duplicated on every scene. A shared background layer driven by the seekable timeline gives one continuous visual surface and makes scenes themselves cheap and transparent.

```html
<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <!-- Shared background — NOT a clip. Always visible. Driven by the timeline. -->
  <div id="bg" class="full-bleed"></div>

  <!-- Timed content layers — transparent backgrounds. -->
  <section
    id="scene1"
    class="clip transparent"
    data-start="0"
    data-duration="6"
    data-track-index="1"
  >
    <!-- content -->
  </section>
  <section
    id="scene2"
    class="clip transparent"
    data-start="6"
    data-duration="14"
    data-track-index="1"
  >
    <!-- content -->
  </section>
</div>

<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Drive the shared background from the seekable timeline.
  tl.to("#bg", { backgroundColor: "#0a1530", duration: 6, ease: "sine.inOut" }, 0);
  tl.to("#bg", { backgroundColor: "#1a0a30", duration: 14, ease: "sine.inOut" }, 6);

  // Scene-local animations stay transparent on top.
  tl.from("#scene1 h1", { y: 48, opacity: 0, duration: 0.6 }, 0.2);

  window.__timelines["main"] = tl;
</script>
```

**Rules:** the background is not a clip — no `data-start`/`data-duration`/`data-track-index`; it exists for the whole composition. Content scenes have transparent backgrounds — whatever's in the shared `#bg` shows through. Drive global state from the shared layer — hue shifts, vignettes, grain, film-look filters get animated once on the shared layer, not per-scene. Do not animate visibility (`display`/`visibility`) on `.clip` elements — HyperFrames already shows/hides clips based on `data-start`/`data-duration`; animate a *child wrapper* inside the clip instead. Verify intentional overflow with a rendered snapshot before silencing an overflow warning.

**When not to use this pattern:** if scenes really are visually disjoint — hard cuts between distinct color worlds with no continuity — the stacked-opaque pattern is fine. The shared-background pattern is for compositions where the background *is part of the motion language*, not just backdrop.

## Tailwind projects

Some projects are scaffolded to use a browser-runtime build of Tailwind CSS (pinned version `@tailwindcss/browser@4.2.4` — treat it as Tailwind v4, not an older v3 setup). Signs a project uses this: `index.html` contains `window.__tailwindReady`; the task asks for Tailwind utility classes, `@theme`, custom utilities, or v3-to-v4 fixes; rendered frames show missing styles or a frame-0 flash of unstyled content.

Do not replace the scaffolded runtime with an unpinned Tailwind CDN script — that defeats reproducibility. Keep the readiness shim deterministic; the renderer waits for `window.__tailwindReady` before capturing frame 0. For offline / locked-down / production-stable renders, compile Tailwind to a CSS file and ship the stylesheet instead of the browser runtime.

### v4 browser runtime rules

Tailwind v4 is CSS-first:

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand: oklch(0.68 0.2 252);
    --font-display: "Inter", sans-serif;
  }

  @utility headline-balance {
    text-wrap: balance;
    letter-spacing: 0;
  }
</style>
```

Avoid v3-only patterns:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Do not add a JS config file only for composition colors, fonts, spacing, or utilities — use `@theme` and `@utility` instead. Migrating from v3? Load an existing JS config explicitly with `@config "./tailwind.config.js";` inside a `text/tailwindcss` block — v4 does not auto-detect v3 config files.

### Composition pattern

Use Tailwind for static layout and style; keep render-critical timing in GSAP or another seekable runtime.

```html
<section
  id="hero"
  class="clip absolute inset-0 grid place-items-center bg-zinc-950 text-white"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="w-[1280px] max-w-[82vw] text-center">
    <h1 class="text-7xl font-black leading-none text-balance">Render-ready Tailwind</h1>
  </div>
</section>
```

For repeated items, parameterize via CSS variables — keep the class list static so the runtime sees every utility:

```html
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 0"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 1"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 2"></span>
```

### Dynamic class safety

The browser runtime scans classes it can see — do not build render-critical class names only at seek time:

```js
// Risky: the runtime may never see every generated class.
element.className = `bg-${color}-500`;
```

Prefer complete class tokens in HTML, data-attribute variants, or explicit CSS:

```html
<div data-tone="blue" class="bg-blue-500 data-[tone=rose]:bg-rose-500"></div>
```

If a generated class is truly unavoidable, make sure the full class token still appears somewhere as a static string in a `text/tailwindcss` block before validation.

### Video-specific guardrails (every bullet is a hard rule)

- **Stable dimensions only** — use `w-[…]` / `h-[…]` / `aspect-video` / grid / flex. No `md:`/`lg:` breakpoints — the renderer is a fixed viewport.
- **Animate via transforms/opacity** — `translate-*`, `scale-*`, `opacity-*` are seek-safe; animating Tailwind sizing utilities is not.
- **No `transition-*` for render-critical motion** — a seekable runtime (GSAP) must own the state.
- **No interaction variants** — `hover:`/`focus:`/`active:`/`group-*:`/`peer-*:`/scroll/pointer variants never fire during a render.
- **Bare `border` is broken in v4** — v4's default is `currentColor` (v3 was `gray-200`). Always write the color explicitly: `border border-white/20`.
- **v4 utility renames** — `shadow-sm` → `shadow-xs`, `rounded-sm` → `rounded-xs`, `outline-none` → `outline-hidden`, `flex-shrink-*` → `shrink-*`, `flex-grow-*` → `grow-*`.
- **Modern CSS is fine** — `color-mix()`, container queries, logical properties all work; the renderer runs current Chrome.

### Quick debug checklist

When Tailwind styles don't apply in a render, check in order: is the project actually scaffolded for Tailwind? Does `index.html`'s `<head>` load the pinned browser-runtime script (not an unpinned CDN)? Is the `window.__tailwindReady` promise present? Are there any leftover v3 `@tailwind` directives? Have config tokens moved into `@theme` (or an explicit `@config` reference for v3 migration)? Does every render-critical class appear as a complete static token (no string-built class names)? Then re-run validation and do a quick draft render to prove frame 0 isn't flashing unstyled content — preview alone can hide that defect.

## The project's four layers: brief, storyboard, script, compositions

A HyperFrames project's files read as four layers: **`BRIEF.md`** (why, for whom, and everything that was asked for) → **`STORYBOARD.md`** (what, frame by frame) → optionally a design/style-spec file (the look — palette, type ramp, components) → **`compositions/`** (the thing itself, the actual HTML). An optional **`SCRIPT.md`** sits alongside the storyboard as the locked narration when the video is voiced.

### The brief: capturing and locking intent

Before building, confirm the run's shape and the video's core facts, and write the confirmed result to `BRIEF.md` at the project root, as the very first file created for the project. Every later step reads this file instead of re-asking the same questions — it is the project's "no-repeat" record of what was already confirmed.

**Run shape.** Three independent concerns describe how a run should behave — don't conflate them:

| Term | Values | Meaning |
|---|---|---|
| `flow` | `automation` or `companion` | Who drives execution — a fully automated pipeline, or an interactive collaborative build. |
| `storyboard` | `yes` or `no` | Whether a live/shared board is used for plan and layout review before building. |
| `mode` | `collaborative` or `autonomous` | Derived from the two above — governs how later preference and checkpoint questions behave. |

Derive `mode` from the confirmed run shape:

| `flow` | `storyboard` | Derived `mode` |
|---|---|---|
| `companion` | either | `collaborative` |
| `automation` | `yes` | `collaborative` |
| `automation` | `no` | `autonomous` |

Default to `collaborative` only when there isn't enough information to derive a mode (e.g. resuming an old project with incomplete state).

An ongoing signal such as "surprise me," "decide for me," "just build it," or "stop asking" sets `flow: automation`, `storyboard: no`, and therefore `mode: autonomous` whenever it appears during intent capture. A bare "go" or "looks good" at a checkpoint accepts only that checkpoint's displayed recommendation — it does not change the overall mode. Once a storyboard file exists, persist the derived mode in its own metadata; on resume, an explicit mode value there overrides the derivation, since it may represent a later user change. A mid-run "stop asking, finish it" changes only checkpoint behavior going forward — set mode to autonomous in the storyboard file if it exists, but don't rewrite the already-confirmed `flow`/`storyboard` fields. Only an explicit signal such as "let's review together" resumes collaborative checkpoints; ordinary feedback does not change mode.

**Gate behavior** — how each kind of question behaves under each mode:

| Gate | Collaborative | Autonomous |
|---|---|---|
| Preference (preset, voice, caption identity) | Ask when required. | Decide and state the choice with a one-line reason. |
| Checkpoint (plan, sketches, pre-render review) | Ask and wait. | Post the same summary, then continue. |
| Quality (completeness of fetched material, lint, structural checks, workflow-specific verification) | Run and stop on errors. | Run and stop on errors — quality gates are never relaxed by mode. |
| Routing ambiguity | Resolve explicitly — a wrong route changes the deliverable. | Same requirement. |
| A needed credential/sign-in is unavailable | Show status and wait for sign-in or an explicit offline choice. | Show status and continue through an available offline option if one exists. |

Autonomous mode never silently drops a required capability — if there's no available way to do something the plan needs, surface the blocker instead of quietly omitting it. A credential problem never relaxes a quality gate.

Rendering stays user-gated in both modes. After checks pass, a collaborative run asks "render now, or what changes?" An autonomous run asks the one kept question, "preview first, or render?" Render only happens after an explicit yes.

Autonomous mode is not silent — it replaces absorbed questions with visible decisions and short reasons, always names the final preview or rendered artifact, reports the actual duration for a time-based deliverable, and includes a contact sheet / snapshot sheet with frame identifiers where available, so the person still gets a review surface even though intermediate checkpoints didn't pause.

**Shared field registry.** Ask only the fields actually used by the current build; values that were inferred or derived by policy get stated in the brief, not asked as questions:

| Field | Meaning | Policy |
|---|---|---|
| `flow` | who drives execution | Ask at the end of intent capture, when both flows are actually supported. An autonomous signal answers it directly. |
| `storyboard` | whether to review on a live board | Ask before `flow`. A direct storyboard request answers it. |
| `destination` | where the video will play | Infer from the request. Ask only when unknown and the answer would change aspect ratio, type scale, or composition. |
| `aspect` | canvas size | Derive from destination: social feed → `1080x1080`; TikTok/Reels/Shorts → `1080x1920`; YouTube/website/desktop → `1920x1080`. State the derivation out loud. |
| `length` | target duration | Recommend a range supported by the material, with the reason. |
| `language` | narration and caption language | Use the requester's own language and state it. |
| `audience` | who will watch | Infer when clear. Ask only when a different answer changes the story or terminology. |
| `message` | the one thing the video must communicate | Derive and echo it in one sentence. Do not move to storyboarding until this is clear. |
| `angle` | route/story shape | Recommend one option with a reason. |
| `narration` | `yes` / `minimal` / `no`, plus any route-specific modes | Follow the selected route's own defaults. |

**Remembered defaults.** If the environment supports it, check previously confirmed preferences (e.g. a personal defaults store keyed by project) before asking a familiar question again — a remembered value becomes the recommended answer and its source gets named ("last time you picked 1080x1920 for TikTok"). A remembered value never overrides the current request and never skips a question that's actually required this time. Only record a value the requester *explicitly confirmed*, never a value that was merely inferred or defaulted — confirmation happens after the brief is written. The first time a project records a preference, say one short line that it will be remembered for future runs; don't re-record a value merely because an autonomous build happened to reuse it — only an explicit confirmation in the current run creates a new memory event.

**Question protocol** — the discipline for asking:

1. Ask only unanswered fields that materially affect the output.
2. Ask one field per message and wait for its answer before asking the next.
3. Put the recommended option first with a short reason. A numbered choice list is fine for factual fields (destination, length, language) where it scaffolds recall — but a creative field the request hasn't already shaped (message, angle, tone) needs an open, anchored question; a list there steers the answer instead of collecting it.
4. Skip a question when the current request already answers it. Inference alone is not the same as an answer — don't silently assume.
5. Ask `storyboard` and then `flow` last, only for routes that support them.
6. Announce any deferred questions before handing off to the build — don't surprise the requester later.
7. When an autonomous signal appears, ask no more preference or checkpoint questions — state the completed brief and the reasons for the decisions made, then build.
8. Send one plain question with, at most, one numbered option list at a time — never place several different fields in the same list.
9. Before the final hand-off summary, run one integration check: look for a consequence the combined answers create together that no single answer showed on its own, and surface it with a proposed adjustment.
10. The hand-off summary separates fields the requester explicitly stated from fields that were inferred or defaulted, with the reasoning shown for both.
11. Revision is not confirmation — after any correction to the summary, present the updated summary again and get confirmation before executing.

At a checkpoint, "go" accepts only that checkpoint's displayed recommendation. If a message explicitly presents a complete brief and states that "go" will accept every displayed default, "go" may then confirm the whole displayed brief — don't assume that broader acceptance without that sentence being present.

### `BRIEF.md` — the intent document

`BRIEF.md` sits at the project root. It has a YAML frontmatter block with one key per confirmed field — run-shape fields first (`workflow`, `flow`, `storyboard`), then the registry fields the build actually used (`message`, `destination`, `aspect`, `language`, `audience`, `length`, `angle`, …). Store canonical, normalized values (e.g. a normalized aspect string, not a loose description), but preserve the requester's own wording in the body text where it matters.

Only a specific preference-backed subset of these fields is appropriate to persist as a cross-project default if a memory system is available: `destination`, `aspect`, `language`, `flow`, `storyboard`, `voice`, `style_preset`. A style preset should be recorded per-workflow (a look confirmed for one genre of video is not automatically a default for a different genre). `message`, `audience`, `length`, and `angle` describe *this* video and belong only in this file's frontmatter, never promoted to a general default.

**Body — four optional sections, write only what was actually learned:**

- `## Intent` — a short paragraph: what the video is, for whom, why now; tone and feel in the requester's own words.
- `## Assets` — the requester's own material, one line each: `path — what it is, where it belongs`. Anything named here should be treated as staged, never re-discovered from elsewhere.
- `## Customizations` — any special capability or bespoke ask ("count-up on the revenue stat," "capture the pricing page too"), each with enough detail to act on directly.
- `## Notes` — anything true that fits no field: constraints, references, things to avoid.

The body prose is project-local — nothing in it should be promoted to cross-project memory (only the frontmatter's preference-backed subset is memory).

**Lifecycle:** created once, as the very first action on a fresh project — never before. A workflow that finds an existing `BRIEF.md` should read it and ask no brief question again. If a project exists (other project files/folders present) but `BRIEF.md` doesn't, treat it as a pre-brief project: resume from whatever the storyboard file and any recorded preferences already say, optionally backfilling `BRIEF.md` from what they already contain — never re-interrogate a half-built project from scratch. `BRIEF.md` stays the run's ongoing truth: a mid-run decision (e.g. "make it 9:16 after all") should rewrite the relevant field directly and re-record any persisted preference — a changed mind is itself a confirmed answer. An accepted capability, adopted material, or bespoke ask lands as one new line in the matching body section. Resume reads this file, so writing back to it is what makes an interrupted project resumable — a decision that only lives in conversation is a decision that resume will never see. `message` and `audience` live here first — a storyboard file may keep its own copies for its own rendering purposes, but when the two disagree, `BRIEF.md` holds what was actually confirmed.

**Example:**

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Compound interest is a snowball, not a ladder"
destination: x-feed
aspect: 1080x1080
language: en
length: 60s
angle: concept
---

## Intent

Teach retail investors why starting early beats contributing more. Confident,
a little playful — closer to a bar-napkin sketch than a lecture.

## Assets

- public/growth-curve.png — the real 30-year S&P chart; the proof beat builds on it.

## Customizations

- Count-up on the final dollar figure.

## Notes

- No stock-photo aesthetics; keep it typographic.
```

### `STORYBOARD.md` — the plan layer

A storyboard is the plan layer for a video — an ordered set of frames (key moments) in one markdown file. A contact-sheet-style board view (if the tooling supports one) renders it visually.

**Frontmatter (global direction):**

| Key | Meaning | Example |
|---|---|---|
| `format` | Canvas size | `1920x1080` |
| `duration` | The brief's rough length expectation (advisory, not a hard limit) | `22s` |
| `message` | One-line thesis | `Ship a launch video in an afternoon` |
| `arc` | Narrative arc | `Hook → Problem → Solution → Proof → CTA` |
| `audience` | Who it's for | `indie devs on X` |
| `mode` | Interaction mode (see above; default collaborative) | `autonomous` |

Set `duration` from the brief's `length` when the storyboard is first written. It's an expectation, not a hard gate — assembly reports where the cut actually lands against it and flags a large gap; judge whether the drift serves the piece, and update the value if the intended length genuinely changes.

**Per-frame sections.** One `## Frame N — Title` heading per frame. Metadata as `- key: value` bullets; everything below the bullets until the next heading is the free-form narrative.

| Key | Meaning |
|---|---|
| `status` | `outline` → `built` → `animated` (defaults to `outline`) |
| `src` | project-relative path to the frame's HTML sub-composition (a tile poster, if rendered, comes from it) |
| `duration` | e.g. `4s` |
| `transition_in` | `crossfade` / `cut` / `wipe` … |
| `scene` | one-line contact-sheet caption |
| `voiceover` | the frame's narration guide |
| `poster` | seconds to seek for a tile poster image (past the intro animation) |
| *any other key* | kept verbatim as workflow-specific per-frame data (effects, assets, …) |

The status ladder means: `outline` — a frame with no built file yet, renders as a placeholder; `built` — the middle rung, the frame's HTML file exists and its layout is confirmed (a wireframe sketch or better), motion not yet added; `animated` — fully built, motion included. Multi-line narration/voiceover values collapse to one line on save.

**Example:**

```markdown
---
format: 1920x1080
message: "Ship a launch video in an afternoon"
arc: Hook → Problem → Solution → Proof → CTA
audience: indie devs on X
---

## Frame 1 — Hook

- scene: Big type punches in on the beat
- duration: 3s
- poster: 2s
- transition_in: cut
- status: animated
- voiceover: "Ship a launch video in an afternoon."
- src: compositions/frames/01-hook.html

Open cold on the promise. This is the thesis — everything after pays it off.

## Frame 2 — The problem

- scene: A 20-minute timer spins on a stack of rejected takes
- duration: 4s
- transition_in: crossfade
- status: built
- voiceover: "The old way? Prompt, wait twenty minutes, get something that misses."
- src: compositions/frames/02-problem.html

The old way: prompt, wait, get something that misses. Establish the pain we remove.
```

**Frame comments — a structured feedback channel.** If a review surface writes structured comments (e.g. to a sidecar JSON file), the shape is:

```json
{
  "version": 1,
  "pass": "sketch",
  "submitted_at": "2026-07-09T12:04:00Z",
  "comments": [
    {
      "frame": 3,
      "src": "compositions/frames/03-mechanism.html",
      "title": "Mechanism",
      "text": "Swap the bar chart for a before/after slider."
    }
  ]
}
```

`pass` names which review round the batch belongs to (`storyboard` for the text-layer review, `sketch` for the static-frame review, `final` for the assembled video). `comments[].frame` is the frame's 1-based index in the storyboard — the key to look up. `comments[].src`/`title` are copied from the frame at submit time, so if frames get reordered after submission, a mismatch shows the drift. `comments[].text` is the feedback, verbatim.

The whole lifecycle: a workflow finding this file at a checkpoint should treat it as the revision feedback — revise exactly the frames it names, delete the file, and re-present the affected frames. It's created only on submit and never lingers across review rounds. If a review submission arrives through an asynchronous channel that doesn't itself notify anyone (e.g. someone filled out comments on a shared board), whoever is running the review should ask the requester to reply directly (even just "done") once they've submitted, so the comments actually get picked up and processed.

### `SCRIPT.md` — locked narration (optional)

The **locked narration** for a project: the final spoken lines plus voice and delivery notes. This is optional — a video with no narration (BGM-only, silent overlay) has none. The storyboard's per-frame `voiceover` field is the lighter, editable *guide*; `SCRIPT.md` is the *commit*.

Free-form markdown, not strictly parsed — a review surface can render it read-only, and a text-to-speech step should extract the indented spoken lines specifically.

**Shape:** a header block, then one section per spoken line.

| Part | Holds |
|---|---|
| Header | Voice (provider + voice name), voice settings (e.g. stability/similarity/style), overall voice direction |
| `## Line N — <label> (Frame N)` | One spoken line, tied to its storyboard frame |
| `**Time:**` | The board's rough window — a guide, not authoritative (real timing comes from actual generated-audio word timestamps) |
| `**Delivery:**` | Per-line delivery note |
| Indented block | The actual spoken text — the only part that should be fed to a text-to-speech engine |

**Example:**

```markdown
# SCRIPT — acme-launch

**Voice:** Rachel (ElevenLabs)
**Voice settings:** stability 0.35 · similarity 0.75 · style 0.20
**Voice direction:** Confident, warm, a little playful.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 3.0s
**Delivery:** Land the promise on the beat.

    Ship a launch video in an afternoon.

## Line 2 — The problem (Frame 2)

**Time:** 3.0 – 7.0s
**Delivery:** Wry, a touch tired.

    The old way? Prompt, wait twenty minutes, get something that misses.
```

Feed each line's spoken text to whatever text-to-speech provider is available. Real per-word timing from that generation step should replace the `**Time:**` guide values once available.

## The review process: plan, sketch, build, final look

This describes how a video earns fidelity one approval pass at a time, when a live review surface (a shared board, a document, or simply presenting drafts to the requester) is part of the workflow. A fully autonomous run posts the same checkpoint summaries and continues without waiting, keeping exactly one question before the final render.

### Pass 1 — The plan

Before presenting the plan, make sure whatever review surface is being used (a live board, a shared doc) is actually up and reachable. Present the plan as a proposal: open by stating **"This video tells [audience] that [message],"** then a frame-by-frame table — one row per frame: frame number, beat type and duration, what's on screen, and *why* (how it serves the message). Note that feedback can land in either the review surface's own comment mechanism or directly in conversation — one revision loop either way — and that a submission on the review surface still needs some kind of direct follow-up ping to guarantee it gets picked up and processed.

In the same message, ask two things: (a) approve the plan or request changes, and (b) do a quick wireframe/sketch pass first (recommended — a fast layout check right after this approval) or skip straight to a full build. Iterate until approved, revising exactly the frames named in feedback each round.

This is a checkpoint — a fully autonomous run (see mode table above) normally skips the live-board loop entirely; if a run switches to autonomous mid-flight after a board already exists, keep updating the board and post the same summary as a heads-up without waiting for a reply, and let the one still-kept question happen at the final-look pass instead.

### Pass 2 — The sketch pass (skippable)

As soon as the plan is approved, build a quick wireframe version of every frame — the frame's layout at its key moment, real headline/stat/label text placed where it will actually live, plain blocks standing in for panels/charts/diagrams/media (define upfront what each block type stands for), the base background/ink colors plus one accent, and nothing else. No decoration, no full visual treatment, no motion — those arrive with the real build.

Each sketch should still be a real, technically valid composition file (so any preview tooling can render a poster image from it) — a template wrapper, correct composition id, root styled via `#root`, one paused *empty* timeline correctly registered. This pass needs no validation tooling run against it — a sketch is only a few dozen lines of HTML, and the whole set of sketches for a video can land in minutes.

Mark each frame as reaching the middle status (`built`) as its sketch lands, so a live board fills in visually on its own. Once every frame is at that status, pause and ask one thing: does the board look right, or which frames need to change? Revise only the sketches actually named in feedback, re-present, and loop until the layout is confirmed. Only then does the real visual design and motion get applied on top of the confirmed layouts.

A confirmed board of sketches is itself a valid stopping point — if what was actually requested was a storyboard to pitch, review, or hand off rather than a finished video, the sketched board *is* the deliverable; confirm it, hand over the board, and go no further unless asked to continue to a full build.

In a fully autonomous run, or when the requester chose to skip sketches at Pass 1, skip this pass entirely — frames go straight from outline to fully built.

### Pass 3 — Building on confirmed layouts

However the build actually happens — one person or process per frame working in parallel, or one build pass working through scenes in order — a confirmed sketch's composition is settled: placement, hierarchy, and copy were already approved on the board. Building from a confirmed sketch means dressing that exact layout (full visual treatment, real assets, motion) — never redrawing it from scratch. Whoever builds a frame that has a confirmed sketch should be told explicitly that the sketch exists and represents an approved layout; the landed frame must still read as the approved wireframe, just fully dressed.

Mark each frame as fully built (`animated`) as it lands. In collaborative mode, this build stage is gated on the sketch board having been confirmed in Pass 2.

### Pass 4 — The final look

After all checks pass, use whatever final composition preview is available. In collaborative mode, ask one thing: render now, or what changes? In a fully autonomous run, this is the one question the mode still keeps: "preview first, or render?" Open the preview on a "preview" answer; render only on an explicit render approval. Never render before this approval.

**After approval, offer to save the whole setup as a reusable template — once.** An approved run is a proven bundle: design spec, storyboard skeleton (structure kept, content blanked), and the confirmed brief values can all be frozen together so a future similar request can start from it instead of from scratch, skipping straight past the questions already answered this time. If this is offered and accepted, confirm the saved name and make clear that name is something the requester can casually reference later ("make another one like X," or "same as last time") without needing to remember any technical details. In a fully autonomous run, don't ask — just name the save option in the delivery note instead.

## The production loop: from an approved plan to a delivered video

The stages between an approved plan and a video in the requester's hands, described as **dependencies rather than a strict numbered sequence** — order between independent stages is free (audio can render in the background while frames are being built; overlapping wait time with work is the standard trick), but order *inside* a dependency chain is not. A stage whose need is absent simply doesn't run — no narration means no audio stage; a single scene means no transitions. An edit request re-enters at whichever stage/artifact it actually touches and re-runs verification from there.

| Stage | Needs | Produces |
|---|---|---|
| **Blocks & assets** | the approved plan | any reusable component blocks the plan calls for, installed once before any parallel work starts (installing them concurrently from multiple workers risks a race); requester-supplied assets staged; logos/images/color grades resolved |
| **Audio** | narration text (when narrated); the storyboard's mood/music direction | voice files + word-level timings + background music + sound effects, generated in the background while other stages proceed |
| **Frames** | the design spec + the plan (+ a confirmed sketch when one exists — dress that layout, never redraw it) | each scene as its own composition file, marked as fully built in the storyboard as it lands |
| **Duration sync** | word timings + frames | scene durations trued up to the real generated-voice length — the real duration always wins, a silent scene keeps its estimate, and a synced value is never hand-edited afterward |
| **Assembly** | the built frames | the index composition — scenes wired in as sub-compositions on tracks |
| **Transitions** | the assembled index | scene-to-scene handoffs injected |
| **Captions** | word timings + the assembled index | the caption track (if no script exists to time against, transcribe the generated audio first) |
| **Verify** | the assembled index (+ captions/transitions when present) | all structural/lint/layout checks passing, plus a quick eyeball of a contact sheet at each scene's midpoint |
| **Deliver** | verification passing | a final-look pause, then on approval a full render, then optionally publishing to a stable public link, then the offer to save the setup as a reusable template |

The Frames stage should follow whatever motion/shape citations the plan already made — a scene planned against a named shot template or named motion techniques gets built by actually reading that reference material before its motion is written; names should come from wherever that reference material is indexed, never invented on the spot, and a scene the plan left uncited should get its citation decided at build time rather than improvising untracked motion.

**Two scheduling facts worth knowing:** external generation calls (image plates, text-to-speech, background music, video generation) are independent work — fire every generation whose input is already known concurrently or in the background, and overlap the wait with reading or building something else; three assets generated one after another cost roughly three times the wall-clock time of firing them together. Also, inspecting a generated image or video mid-session (especially at full detail) can be an expensive operation in some environments — batch visual checks into one contact sheet rather than many single-frame looks, and schedule them at natural phase boundaries rather than constantly mid-build.

Two points in this loop carry the requester's actual voice: the plan that starts it was approved in Pass 1 (or posted as a heads-up in autonomous mode), and nothing renders before the Pass 4 final-look approval. Everything between those two points is free to schedule however is most efficient.

## Building scenes independently (parallel work)

When a video has many scenes that can be built independently, the underlying workflow goal is: hand each scene's *entire* self-contained spec to an independent builder (a person, or a separate automated process/agent), let them build purely from that spec without needing to see the rest of the project, then verify each output file actually exists and is correct before merging it into the final assembly. The mechanics of *how* work gets distributed to independent workers differ across tools and platforms — the important, tool-independent rules are:

- **Completion is judged by the artifact existing on disk**, not by any notification that a worker "finished" — some systems report completion unreliably. After a wait, verify the actual output file exists and is valid; a missing file means that unit of work failed and should be retried once with the same instructions plus the failure reason attached.
- **A concurrency limit reduces parallelism, not the amount of work** — every scene still gets built; if only a few workers can run at once, batch the work into waves of that size rather than dropping scenes or merging multiple scenes into one worker's task.
- **Each independent builder needs a fully self-contained packet**, not access to the whole project — see "The frame/scene builder role" below for what that packet should contain and how one scene should be built from it.

### The frame/scene builder role

When one scene/frame of a larger video is being built as an independent, self-contained unit of work (whether by a different person, a different automated process, or simply as a discrete step you're doing yourself), follow this process. It assumes the builder has been handed: a `frame_id` (used verbatim as the composition id, the timeline registry key, and the output filename, e.g. `compositions/frames/03-feature.html`); the design-truth file (palette, type ramp, components — the visual "look" to pull every visual token from); and a self-contained packet of everything needed for this one frame, which should include:

- `scene` — a one-line caption describing the design intent (not visible on-screen text).
- `voiceover` — the narration line for this frame, used only as a **timing reference** (to sync entrances to the voice) — it is never rendered as visible text; captions are a separate track handled elsewhere.
- `duration` — the frame's fixed render length in seconds. Never change it or stretch/compress content to fill a different length.
- `transition_in` — informational only; whoever assembles the final video stamps the actual transition. A frame builder never authors the transition itself.
- A **time-coded shot sequence** — the actual build spec: a sequence of "Scene" lines (e.g. `Scene 1 (0.0–Xs): … → Scene 2: … → Scene N`), each describing what's on screen, what enters/moves/reveals, and the layout — inline. Build this faithfully, beat for beat; every window described is a phase that must be realized, with each reveal timed to land on its narration cue.
- A named shot template/blueprint (or an explicit "compose from scratch" marker) describing the overall shape and signature move of this shot.
- Which element is the visual focal point and what role each other element plays.
- The mechanics (a "recipe") for any named motion technique cited in the shot sequence — reproduce these mechanics rather than guessing at a technique from its name alone; guessing loses the technique's actual signature move.
- The canvas size and whether captions are enabled (and if so, the safe-area cutoff for caption clearance).

**If a confirmed sketch/wireframe for this frame already exists**, read it first and preserve its composition exactly — placement, hierarchy, and copy were already approved; don't move or drop anything from it. What's still yours to add: the full visual treatment, real finished content wherever the sketch used placeholder blocks, and the actual motion — mapping each described scene onto a timeline phase, revealing each piece on its narration cue with proper entrance tweens. The final landed frame must still read as the approved wireframe, just fully dressed.

**What a frame builder does NOT decide** — these belong elsewhere in the process, and touching them breaks the contract with the rest of the project:

- **What is said** — narration text is locked elsewhere (in the script file or the frame's `voiceover` line). A frame builder only shows; it never writes or restates narration as on-screen text.
- **Duration** — fixed from real generated-voice timing elsewhere. Build the shot to land within the given duration; don't stretch or trim it.
- **Transitions between frames** — stamped onto the root timeline by whoever assembles the final video. A frame builder authors the shot itself but never an "exit" tween — the transition between scenes *is* the exit, except for the final frame in the whole video, which can genuinely settle/fade out.
- **Audio** (narration, background music, sound effects) — assembled separately at the project root. No `<audio>` element belongs inside an individual frame's composition file.
- **Design tokens** — palette, fonts, and components come only from the shared design-truth file; a frame builder should never invent them, and never lift a word or label out of the design-truth file as visible copy — that file is a style spec, not content. Visible text comes only from this frame's own scene description/narrative.
- **Which motions or assets exist** — named upstream in the packet. A frame builder implements what's named; it never fetches new assets or invents new motion techniques on its own.
- **The shared storyboard file itself** — a frame builder should only ever read its own packet, never open or write the shared storyboard directly; whoever is coordinating the whole project owns that file's state.

**Constraints every frame must satisfy, in addition to workflow-specific rules:**

- **Caption keep-out — all content in the top ~83% of the frame.** If a caption pill sits at the bottom of the canvas, it owns roughly the bottom 17%. Keep every element (headline, cards, code panel, diagram, stats, brand mark) above roughly 83% of the frame height. This holds even when captions are disabled for this particular render, for consistency across frames.
- **Fill the content area, especially in a portrait/vertical frame.** Compose across the whole usable region rather than floating one small cluster in the middle. Anchor the hero element high (roughly 20–35% down from the top), flow supporting elements downward with rhythm, and scale the hero toward full-bleed. A landscape frame's usable region is shorter, so simple vertical centering near the middle is fine there.
- **Visible text is short motion-graphics copy** — a hero word, a stat, a one-word emphasis (`"$83K"`, `"2× faster"`, `"INSTANT"`) — never a full sentence lifted from the narration. If a caption track already shows the spoken words synced to voice, repeating them as on-screen text double-prints the same words.
- **Build the whole shot — reveal across the full duration, never front-load everything near the start.** Dumping the whole canvas in the first quarter of the shot and then holding it reads as a static slide, not a video. Instead, reveal each piece (a line, a card, a node, a stat) as the narration reaches it, pacing the reveals across the entire duration — especially the back half — with any camera-style move running underneath throughout. Only *exits* are banned on a non-final frame (an exit tween gets truncated by the cut to the next scene and reads as a glitch); mid-shot reveals are always fine. The one exception is a frame deliberately marked as a still/hold moment — there, an entrance followed by a quiet settle is correct; a held read beats forced motion.
- **Implement the shot sequence faithfully — every described "Scene" beat is a real timeline phase.** The time-coded shot sequence *is* the build spec: map each described beat onto a phase of the one timeline, each piece revealing as narration reaches it. For any named motion technique, reproduce the actual mechanics of its recipe rather than guessing from the name. A named shot template gives the overall shape — keep its signature move recognizable while instantiating it with this frame's actual content. If no template is named ("compose from scratch"), sequence the shot directly from the described beats. Never front-load the whole sequence at the very start regardless.

**Process:**

1. **Read** the full packet (the frame's own spec, any inlined shot-template description, any inlined motion-technique recipes), then the design-truth file for the visual look. The most consequential thing to get right structurally is the file-transport rule: every `<style>` and `<script>` block (including any animation-library load) must live *inside* the `<template>` wrapper, since a runtime that only clones template contents will silently produce a blank, unstyled sub-composition otherwise — and a project-wide check run after assembly can miss that a specific sub-composition never got wired in.
2. **Design** — turn the time-coded shot sequence into an actual timeline using the design-truth file's components and type scale: each described beat becomes a phase revealed on its narration cue, each named motion built from its recipe, the chosen template's signature move kept recognizable. Look for a visual idea that reinforces the beat rather than a literal restyling of the words.
3. **Author** the full sub-composition file: a `<template>`-wrapped root carrying the correct composition id, styled via `#root` (never a class on that same element), with exactly one paused timeline registered under the frame's id, built synchronously. Prefix any ids and reusable class names with the frame's own id so that when many frames are assembled together nothing collides (standard selectors like `#root` and `.clip` are the exceptions).
4. **Self-check** against the checklist below and fix anything found before considering the frame finished.

**Self-check checklist** (a frame builder generally cannot run full project-wide validation tooling on a single not-yet-assembled frame — these checks operate on the assembled project and would only report on other files. So the self-check has to happen by careful re-reading before finishing; if a retry happens later with specific findings attached, treat each one as a hard constraint):

- The entire file is exactly one bare `<template>…</template>` fragment — no `<!doctype>`, `<html>`, `<head>`, or `<body>` outside it — and the root inside carries the correct composition id.
- Every `<style>` and `<script>` block, including any animation-library load, lives inside `<template>`.
- The frame's root is styled via `#root`, never via a class also present on that same element — at render time a class on the root gets scoped to a descendant selector that can't actually match it, so the whole scene renders unstyled even though an isolated preview might still look correct.
- A frame's full-bleed background (a color field, gradient, or grid) is authored as its own full-duration `class="clip"` element on the lowest content track — never as a `background` set directly on the root/composition-id element itself. At final assembly the frame root is only visible during its own time window, so a background painted on it isn't a dependable full-frame ground; dark content can end up rendering over a black host background and become invisible.
- Every `class="clip"` element has `data-start`, `data-duration`, and `data-track-index`.
- Exactly one paused timeline, registered under the frame's own id.
- No CSS `transition`, no `repeat`/`yoyo`, and no other non-deterministic animation logic anywhere (the renderer seeks frame-by-frame, not through real playback).
- No CSS `transform` (e.g. a `translateY(-50%)` centering trick) sits on any element that also has a GSAP transform property (`x`/`y`/`scale`/`rotation`) tweened on it — GSAP overwrites the whole `transform` and silently drops the CSS centering, so the element visibly jumps. Center with `margin`/`inset` (or offset `top`/`left`) instead, fold any needed offset into the tween itself via percentage-based transform properties, or use a `fromTo` tween (which is exempt from this issue).
- The main subject is visible by roughly half a second in, using proper entrance tweens (declaring both start and end state) rather than a CSS-hidden starting state.
- No exit tween on a non-final frame.
- The shot's pieces reveal on their narration cues across the full duration rather than all firing at time zero; a non-still frame keeps content arriving rather than holding a fully-populated canvas from early on.
- Every described beat in the shot sequence is actually realized as a phase, any named shot template's signature move is present and recognizable, and the whole shot paces to the narration rather than front-loading.
- Every font actually named in the CSS has a matching font-face declaration inside this same file, pointing at a real font file that ships with the project. Only ever use fonts that actually have a shipped file — never name a system font (especially for non-Latin scripts like Japanese, Chinese, or Devanagari) that the render environment doesn't actually have installed; the render machine is typically a clean, minimal browser environment, so an unavailable font silently falls back to something generic and the typography is simply wrong in the final video. For non-Latin visible text, either use a shipped font that covers the needed script, or transliterate/romanize the text; if neither is possible, that content is out of scope for this frame — never invent a font name that doesn't exist as a real file.
- Nothing sits below the caption safe-area cutoff, and no full narration sentence is rendered as visible on-screen text (a quick visual eyeball, not something to derive from code).

## Validation

Whatever CLI or tooling a HyperFrames project ships with should be run before considering any composition finished:

- A full lint/structural/runtime/layout/contrast check should pass with zero findings.
- For any project using sub-compositions, take a snapshot at several representative timestamps (e.g. each scene's midpoint) and actually look at each frame.
- Use a live preview for human review — anything in the timeline should still be editable there before final approval.
- Only render after explicit approval from whoever commissioned the video.

## Note on the frame-packet builder helper script

The source project includes a script (`scripts/lib/frame-packets-core.mjs`) that is a helper module for building the "frame packet" data structures described above — it parses a storyboard's markdown into individual frame blocks, extracts fields like `src` from each block, and assembles the self-contained packet (with inlined shot-template and motion-recipe content) that gets handed to whoever builds each individual frame. It is implementation code specific to one particular automation environment and is not reproduced here in detail — the packet *contents* it produces are what's documented above, in "The frame/scene builder role."

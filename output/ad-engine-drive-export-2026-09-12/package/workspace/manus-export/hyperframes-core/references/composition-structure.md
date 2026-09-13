# Composition structure — minimal skeleton, architectures, archetypes

How to architect a project — the smallest renderable file, when to inline everything in one HTML file, when to split into sub-compositions, what the `index.html` orchestrator looks like at scale, and the common sub-composition archetypes seen in real projects.

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

## The modular orchestrator pattern

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

## Sub-composition archetypes

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

## Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Sub-comp file | `compositions/<scene-id>.html` | `compositions/act0-intro-bell.html` |
| Sub-comp `<template>` id (optional) | `<scene-id>-template` | `<template id="act0-intro-bell-template">` |
| Sub-comp root `data-composition-id` | `<scene-id>` (must match host slot) | `data-composition-id="act0-intro-bell"` |
| Timeline registry key | matches `data-composition-id` | `window.__timelines["act0-intro-bell"]` |
| Host slot `id` | `el-<short>` or `<scene-id>` | `id="el-intro"`, `id="act0"` |
| Element ids inside a sub-comp | prefix with the scene id | `#act0-bell`, `#b1-tape` |
| Audio at root | `data-track-index` well above visual tracks | `10` while visuals use `1` |

The `-template` suffix on `<template>` is conventional but not required — the runtime extracts contents from whichever `<template>` is in `<body>`, regardless of id. The id prefix inside a sub-composition is the only real safeguard against id collisions when multiple sub-compositions are mounted into the same host page at once — and this matters more than it looks: a duplicate id across two different sub-composition files (each individually valid) causes both instances to render blank once they're assembled into one page, because the frame producer looks elements up by id.

## Editing an existing project

Before adding or modifying scenes, identify which architecture is in use — a `compositions/` directory present means modular, absent means monolithic. In a monolithic project, add new scenes as inline `<section class="clip">` elements with a non-overlapping `data-start` and a sensible `data-track-index`, extending the existing single timeline. In a modular project, match the existing pattern: add a new file under `compositions/`, add a slot in `index.html`, keep the root timeline thin — don't start inlining new scenes into `index.html` when sibling scenes are sub-compositions. If a monolithic project needs a third or fourth scene cut, lift each scene into a sub-composition first. When picking a new slot's `data-start`/`data-duration`, continue the existing sequencing convention rather than introducing a new track index unless parallel visual layers are actually needed — most sequential-scene projects use exactly one visual track.

Also, when editing: read the existing files first and preserve unrelated timing, tracks, ids, variables, and media paths. Match existing composition ids and timeline keys. `data-hidden` on any composition element hides it in both preview and render, overriding its time window — it is non-destructive and reversible (used for temporarily toggling a layer off without deleting it).

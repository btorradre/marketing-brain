# Sub-compositions

A sub-composition is a separate HTML file embedded in a host composition. HyperFrames loads it, seeks it independently, and composites the result into the host at `data-start`.

## Host wiring

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

## Mental model — what the runtime actually does

When a host loads a sub-composition via `data-composition-src`, the runtime: (1) fetches the HTML file; (2) parses it as a DOM document; (3) **finds the `<template>` element and clones ONLY its contents into the host slot**; (4) everything **outside** the `<template>` (including the entire `<head>`) is **discarded**.

So `<template>` is not just a wrapper — it is the transport container. If a node needs to exist in the live render, it must be inside `<template>`. Full stop.

## File shape

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

## Three pitfalls that pass static checks but break at render

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

## Verification checklist before render

For every sub-composition file:

1. Confirm `<style>`, `<script>`, and the main markup all live *inside* `<template>` (the first occurrence of each should come after the opening `<template>` tag and before its close).
2. Confirm host `data-composition-id` == internal `data-composition-id` == the `window.__timelines[...]` key, for every sub-composition — all three strings must match exactly.
3. Confirm the root element is styled via `#root`, not via a class also declared on the `data-composition-id` element.

For the runtime end-to-end check, do a fast preview/snapshot pass and eyeball each sub-composition's rendered frame — that is the only check that reliably catches these three pitfalls; static inspection alone can miss all three.

## What HyperFrames does with the sub-composition

It loads the file and registers its timeline under its internal `data-composition-id`; seeks the sub-composition's timeline independently from the host's playhead; plays the sub-composition's content from `data-start` of the host clip, for `data-duration` seconds. Do **not** manually nest a sub-composition's timeline into the host timeline (e.g. adding it as a child of the host's GSAP timeline) — HyperFrames already drives them independently, and nesting causes double-seeks.

## The host clip's `data-duration` is the slot's visible window

`data-duration` on the host clip defines how long the slot is visible, and it takes precedence over the sub-composition's own internal timeline length. Two consequences: if the sub-composition's internal timeline finishes *before* `data-duration` elapses, the slot holds on the final frame for the rest of the window (no need to pad the timeline with empty tweens). If `data-duration` is *shorter* than the host composition, the slot ends — and goes blank — when its own `data-duration` elapses; this is intended, the clip is a fixed-length window, not "fill until the composition ends." To keep a sub-composition visible for the whole composition, set its `data-duration` to span the host window, or add another clip to cover the remaining time. Leaving a single full-bleed sub-composition shorter than the composition is almost always a mistake.

## Animations inside sub-compositions

Prefer `gsap.fromTo()` over `gsap.from()` for entrance tweens. The host re-seeks the sub-composition every time its clip becomes visible; `gsap.from()` records the starting state at registration time and can desync on seek-back, while `gsap.fromTo()` declares both endpoints explicitly and replays cleanly regardless of seek order.

## Per-instance variables

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

The host can render the same sub-composition multiple times with different `data-variable-values` to produce per-instance variations. Full variable-declaration rules: `variables-and-media.md`.

# Variables and media

Two separate concerns, grouped because both control "what flows into the HTML from outside": runtime parameters (variables) and external media files (video/audio).

## Variables

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
- Render tooling that accepts render-time overrides typically supports a `--variables` JSON object (or a `--variables-file`) plus a strict mode that turns undeclared keys, type mismatches, and invalid enum values into hard errors instead of warnings.
- Read values once during init, not on every animation tick — variables don't change mid-render.
- A color-grading configuration can reference exact variable ids; the runtime resolves the reference from the current composition's variables before applying shader adjustments, finishing details, blur/pixelate effects, and custom LUTs.

**Two JSON shapes, easy to confuse:** `data-composition-variables` is an *array of declarations* (the schema): `[{id, type, label, default}, ...]`. Values passed at render time or via `data-variable-values` are *objects keyed by id* (the actual values): `{ title: "Q4", accent: "#fff" }`.

## Media

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

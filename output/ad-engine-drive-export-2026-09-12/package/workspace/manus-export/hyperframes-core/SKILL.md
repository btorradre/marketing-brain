---
name: hyperframes-core
description: Build, edit, and validate HyperFrames HTML video compositions - seekable DOM timing via data-* attributes, class="clip" visibility, sub-compositions, tracks, variables, and framework-owned media playback. Covers the deterministic-render rules the renderer depends on, the BRIEF.md/STORYBOARD.md/SCRIPT.md plan-layer file formats, and the plan-sketch-build-final review and production process for taking a video from an approved plan to a finished render. Use whenever asked to build, edit, inspect, validate, or reason about a HyperFrames HTML video composition, storyboard, or brief - read this before writing composition HTML.
---

# HyperFrames Core

HyperFrames renders video from HTML. A composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable (every frame can be reproduced from a time value alone — there is no notion of "playback"), and whose media playback (`<video>`/`<audio>`) is owned by the framework rather than by page JavaScript.

This is the technical contract for building one renderable HyperFrames project: how to structure the HTML/CSS/JS, how timing and tracks work, how sub-compositions and variables work, the hard determinism and layout rules the render engine depends on, the plan-layer file formats (`BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md`), and the production/review process for taking a video from an approved plan to a finished render.

Adjacent concerns live outside this contract: the animation runtime library (GSAP/Lottie/Three.js adapters, named motion techniques and shot blueprints) is its own domain; creative/visual design guidance is its own domain; a keyframe extraction/generation capability and a shared component/asset registry are their own domains; command-line tooling for linting, previewing, and rendering is its own domain. This document only covers the structural contract a composition file must satisfy.

## How to use this

1. **Establish intent before building anything.** Before writing HTML, pin down: what the video is for (destination/platform), the target canvas size, the target length, the one message it must communicate, the audience, and the language. Only ask about fields that are genuinely unknown and that would change the output — infer everything the request already answers.
2. **Write the intent down as `BRIEF.md`** at the project root before any other project file exists. This is the durable record of what was confirmed — later steps (and anyone resuming the work later) read this file instead of re-asking the same questions. Format and lifecycle: `references/brief-format.md`.
3. **Decide the project's architecture** — one big HTML file ("monolithic") or one file per scene wired together by an orchestrator file ("modular"). Prefer modular once the video has three or more scene cuts. Full guidance: `references/composition-structure.md`.
4. **Plan the video as a storyboard** — an ordered list of frames/scenes with a one-line description, rough duration, narration guide, and transition, before writing any composition markup. Write this to `STORYBOARD.md`. If a review process is available, present the plan as frame cards and get it approved before building. Format: `references/storyboard-and-script-format.md`.
5. **Optionally sketch layouts first.** For a plan that needs sign-off on layout before full visual treatment, build quick unstyled wireframe versions of each frame (real headline/stat text placed where it will live, plain blocks standing in for charts/media, no animation, minimal styling) and get those approved before doing full visual design and motion.
6. **Build each composition file** following the data-attribute contract, the determinism rules, and the layout rules. If building many independent scenes, they can be produced independently and in parallel as long as each one is self-contained and gets verified before being merged in.
7. **Assemble** the scenes into the final index composition (tracks, sub-composition slots, continuous audio at the root).
8. **Add transitions, captions, and audio** as needed.
9. **Verify determinism and layout** — run whatever lint/check tooling the project ships with, and eyeball a handful of representative frames (a "contact sheet" / snapshot at scene midpoints) rather than trusting automated checks alone. Several of the rules below are silent bugs that automated gates can miss.
10. **Get sign-off, then render**, and only then treat the video as delivered. Never render before an explicit approval on the final look.

## The two root forms (not interchangeable)

- **Standalone** (top-level `index.html`): the root `<div data-composition-id="…">` sits directly in `<body>` — **no `<template>` wrapper** (wrapping it hides all content and breaks rendering).
- **Sub-composition** (loaded via `data-composition-src`): the root **must** be wrapped in `<template>`.

Transport rule: the runtime only clones `<template>` contents — everything outside it (including the entire `<head>`, its styles and scripts) is discarded, so `<style>`/`<script>` must live **inside** the template.

Host-id rule: the host slot's `data-composition-id` must **exactly equal** the inner template's `data-composition-id`, and both must equal the `window.__timelines["<id>"]` key — no `-mount`/`-slot`/`-host` suffix on either side.

Full wiring pattern, file shape, and the three pitfalls that pass static checks but break at render: `references/sub-compositions.md`.

### Root must be sized (a silent layout bug)

The standalone root needs an explicit sized box (`width`/`height` in px), and every ancestor down to a `height: 100%` element must have a resolved height — otherwise a flex or `100%`-height child collapses to roughly 0 and content piles into the top-left corner. Don't rely on automated checks alone to catch this — inspect a rendered snapshot. Minimal skeleton: `references/composition-structure.md`.

### One paused timeline

Each composition registers **exactly one** `gsap.timeline({ paused: true })` at `window.__timelines["<id>"]` (key = root `data-composition-id`), built **synchronously** at page load. Render duration is the root's `data-duration`, not the timeline's own length. Don't manually nest sub-timelines into the host timeline. Full contract, including non-GSAP runtimes: `references/determinism-layout-motion.md`.

## Non-negotiable rules (silent bugs automated gates may miss)

- No render-time clocks (`Date.now()`, `performance.now()`), no unseeded `Math.random()`, no render-time network fetches, no hover/scroll/pointer/focus state, no `repeat: -1` (use a finite count instead). See `references/determinism-layout-motion.md`.
- Animate only the visual-property allowlist (`opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transforms). Never tween `display` or raw `visibility` on a `.clip` element — the framework alone controls a clip's visibility lifecycle. GSAP `autoAlpha` and a zero-duration `tl.set(..., {visibility:...})` boundary set are the only visibility exceptions, and only on non-clip elements or wrappers inside a clip.
- No `<br>` in body text — let text wrap via `max-width`. Transformed elements must be block-level and sized (a `transform` on an auto-width inline `<span>` is a no-op). Pulsing absolute decoratives need clearance at their peak size, not their resting size.
- `<video>`/`<audio>` must be a **direct child of the host root** (`index.html`) — never inside a sub-composition's `<template>` or any wrapper `<div>`. Media placed anywhere else is never seeked/decoded and renders blank or black. Details: `references/variables-and-media.md`.
- Every `id` must be unique across the **assembled** page. A duplicate `<video>`/`<img>` id (even across two different sub-composition files that both get inlined into one render) causes both instances to render blank, because the frame producer looks elements up by id — and this kind of cross-file duplicate slips past most lint tooling since each file looks valid on its own. Inside a sub-composition, prefix element ids with the composition id (e.g. `#03-scene-hero`).
- A full-screen scene fill (a background color field, gradient, or grid) belongs on a full-bleed **child** clip (`position: absolute; inset: 0`, its own `data-start`/`data-duration`/`data-track-index`), never painted as a `background` directly on the composition root / `data-composition-id` element itself. A composition root is only visible during its own clip time window, so a background painted on it is not a dependable full-frame ground — dark content can end up rendering over a black host background and become invisible, even though it looks correct in an isolated preview.

## Building a composition — quick reference

| Topic | Reference |
|---|---|
| Minimal renderable skeleton; monolithic vs. modular; orchestrator `index.html`; sub-composition archetypes (content scene, host media + main-timeline driver, multi-scene merge, audio-at-root); naming conventions; editing an existing project | `references/composition-structure.md` |
| Every `data-*` attribute (root, clip, sub-composition host, legacy aliases); `class="clip"`; tracks and same-track overlap; relative timing (`data-start="otherClip + 2"`) | `references/data-attributes-and-tracks.md` |
| Wiring a sub-composition; the `<template>` transport contract; the three pitfalls that pass static checks but break at render; the pre-render verification checklist | `references/sub-compositions.md` |
| Declaring and binding variables (`data-composition-variables`, `data-var-src`, `data-var-text`); placing and driving `<video>`/`<audio>`; volume, trimming, codec notes | `references/variables-and-media.md` |
| The determinism bans; the animatable-property allowlist; the duration-inference contract for GSAP vs. CSS/WAAPI/Lottie/Three.js; the layout contract (sizing, text fit, transform rules); the full-screen shared-background motion pattern | `references/determinism-layout-motion.md` |
| Working in a project scaffolded for the Tailwind v4 browser runtime — CSS-first `@theme`/`@utility`, dynamic-class safety, video-specific guardrails | `references/tailwind.md` |
| `BRIEF.md` — capturing and locking intent, the run-shape/mode model, the shared field registry, the question-asking protocol | `references/brief-format.md` |
| `STORYBOARD.md` (frontmatter, per-frame fields, the frame-comments feedback channel) and `SCRIPT.md` (locked narration for text-to-speech) | `references/storyboard-and-script-format.md` |
| The plan → sketch → build → final-look review passes; the production loop's stage dependencies (blocks/assets, audio, frames, duration sync, assembly, transitions, captions, verify, deliver); building scenes independently in parallel; the frame/scene-builder role and its self-check | `references/production-and-review-process.md` |

## Editing an existing project

Before adding or modifying scenes, identify which architecture is in use — a `compositions/` directory present means modular, absent means monolithic. In a monolithic project, add new scenes as inline `<section class="clip">` elements with a non-overlapping `data-start` and a sensible `data-track-index`, extending the existing single timeline. In a modular project, match the existing pattern: add a new file under `compositions/`, add a slot in `index.html`, keep the root timeline thin — don't start inlining new scenes into `index.html` when sibling scenes are sub-compositions. If a monolithic project needs a third or fourth scene cut, lift each scene into a sub-composition first.

When editing: read the existing files first and preserve unrelated timing, tracks, ids, variables, and media paths. Match existing composition ids and timeline keys. `data-hidden` on any composition element hides it in both preview and render, overriding its time window — it is non-destructive and reversible (useful for temporarily toggling a layer off without deleting it).

## Validation

Whatever CLI or tooling a HyperFrames project ships with should be run before considering any composition finished:

- A full lint/structural/runtime/layout/contrast check should pass with zero findings.
- For any project using sub-compositions, take a snapshot at several representative timestamps (e.g. each scene's midpoint) and actually look at each frame — several of the rules above are silent bugs that only a rendered snapshot reveals.
- Use a live preview for human review before final approval.
- Only render after explicit approval from whoever commissioned the video.

If the project's tooling exposes a CLI (commonly invoked as `npx hyperframes <command>` — e.g. `check`, `snapshot --at <timestamps>`, `preview`, `render`), those commands are ordinary standalone tooling and can be run directly; see the project's own CLI documentation for the exact command set available.

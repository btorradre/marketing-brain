---
name: hyperframes-keyframes
description: >
  Author and verify seek-safe 2D/3D keyframes for a HyperFrames video/motion-graphics
  composition — GSAP timelines, CSS keyframes, Anime.js, WAAPI, FLIP, paths, masks,
  SVG morph/draw, text motion, and 3D depth — then confirm them with the `hyperframes`
  CLI diagnostics. Use when a composition needs an element to move, transform, reveal,
  or change state in a way that must remain scrubbable/seekable at any point in time,
  not just play forward once. This is a mechanism reference for implementing motion you
  already intend, not a guide for broad scene strategy, brand design, media sourcing,
  captions strategy, or general video planning.
---

# HyperFrames Keyframes

Keyframes, in this system, are a "pose contract": a keyframe defines the visible states an animated subject passes through, preserves that subject's continuous identity across the animation, must run in a "seek-safe" runtime (the animation must be able to jump to any timestamp and render correctly, not just play linearly), and every claimed pose must be verified against actual rendered pixels, not just code that looks right.

This document is a mechanism reference, not a visual-style guide: use it when you already know what should happen and need to choose and correctly implement the underlying animation mechanism. It is not the place for broad scene strategy, brand design, media sourcing, captions strategy, or general video planning — those belong to the wider composition-planning and scene-recipe side of the HyperFrames system. Use `references/keyframe-patterns.md` only when choosing an implementation mechanism, not visual style.

## Procedure

1. **Identify the animated subject, its visible states, its final state, and the total runtime.** Name the actual DOM/SVG/canvas element that moves — not a wrapper or helper element — and enumerate the poses (positions/states) it must visibly pass through, including what it looks like at the very end.
2. **Choose the smallest mechanism that proves the intended motion.** Match the need (e.g., "subject travels a visible route" → path travel) to a technique using the Mechanism Choice table below. Only consult `references/keyframe-patterns.md` if the right mechanism isn't obvious from the table.
3. **Author the keyframes in the declared runtime** (GSAP, CSS, Anime.js, or WAAPI), building them synchronously and registering the resulting timeline/instance in the runtime's expected global registry (see Runtime Rules). Do not build timelines asynchronously or leave them unregistered — the composition player needs to be able to find and seek them.
4. **Verify the result using the CLI diagnostics**: run `lint`, `check`, `keyframes`, one focused `--shot` on the actual animated selector, and snapshots at the specific proof times (first frame, proof poses, final-minus-hold, and the exact final frame).
5. **If verification fails, fix the source keyframes and rerun the smallest failing diagnostic** before attempting a full render. Don't just re-render and hope; isolate the failure with the narrowest possible tool first.

Before declaring the work done, run the full verification pass again (`lint`, `check`, `keyframes`, one focused `--shot`, and snapshots) and confirm: the first frame is correct, proof poses are visible, there is a final-minus-hold frame and an exact final frame, the motion is owned by the actual subject (not a decoy/helper element), and there are no leftover debug overlays in the output.

## Contract (non-negotiable properties of any keyframe animation)

- Name the moving subject explicitly.
- Name the poses needed to prove the intended motion, including the final state.
- Keyframe visible channels only — never hidden/helper state that doesn't render.
- Preserve object identity when continuity matters (the same element should persist through the motion rather than being swapped for a look-alike).
- Crossfade only when the intended motion is genuinely a replacement or dissolve of one thing for another.
- Hold readable or semantic states long enough for a viewer to actually see them.
- The final frame is part of the animation itself, not an afterthought/cleanup step.
- Do not reset the subject back to its rest/starting state unless that was explicitly requested.
- Do not end the animation on a black frame unless that was explicitly requested.
- If editing a pre-existing starter scene, preserve its layout, copy, assets, colors, and final state — do not redesign it — unless explicitly asked to redesign.

## Runtime rules by technology

**GSAP**
- Build the timeline synchronously at page load (not inside an async callback or event handler).
- Use `gsap.timeline({ paused: true })` — never an auto-playing timeline for render-critical motion.
- Register the timeline as `window.__timelines[compositionId]`.
- The registry key must match the element's `data-composition-id` attribute exactly.
- Do not call `tl.play()` for render-critical motion — the player drives the timeline via seeking, not playback.
- Keep all repeats finite (no infinite loops).

**CSS keyframes**
- Use a finite duration and a finite iteration count.
- Use a deterministic delay (not one derived from runtime/random state).
- Set `animation-fill-mode: both` so the element holds its start/end states outside the active animation range.
- Use the `data-start` attribute when the timing belongs to a clip.

**Anime.js**
- Create the animation instance synchronously.
- Set `autoplay: false`.
- Use finite duration and finite loop counts.
- Push every created instance into `window.__hfAnime` (initialize as an array if needed: `window.__hfAnime = window.__hfAnime || []`).

**WAAPI (Web Animations API)**
- Use a finite `duration`.
- Set `fill: "both"`.
- Construct the animation deterministically.
- Verify any WAAPI-driven animation with `--shot` (which seeks WAAPI animations) plus snapshots rather than assuming it behaves like GSAP/CSS.

**Never use for render-critical motion, in any runtime:**
`Date.now()`, `performance.now()`, unseeded `Math.random()`, hover or scroll triggers, timers (`setTimeout`/`setInterval`), timelines created asynchronously, unregistered `requestAnimationFrame` calls, infinite loops. All of these break "seek-safety" — the ability to jump the composition to any timestamp and get a correct, deterministic render.

## GSAP skeleton (canonical starting structure)

```js
const root = document.querySelector("[data-composition-id]");
const compositionId = root.dataset.compositionId;
const tl = gsap.timeline({ paused: true });

tl.addLabel("state-a", 0);
tl.to(".subject", {
  keyframes: [
    { x: 0, opacity: 1, duration: 0.2 },
    { x: 120, opacity: 1, duration: 0.4, ease: "power2.out" },
    { x: 100, opacity: 1, duration: 0.2, ease: "power2.inOut" },
  ],
  ease: "none",
});

window.__timelines = window.__timelines || {};
window.__timelines[compositionId] = tl;
```

Use labels for semantic states. Use position parameters instead of chained delays. Use `immediateRender: false` for later `from()`/`fromTo()` tweens that touch the same property as an earlier tween.

## Keyframe forms

- **Array keyframes** — a pose ladder with a per-step duration and easing.
- **Percentage keyframes** — exact timing placement inside one tween.
- **Property arrays** — compact multi-stop changes to a single property.
- Set `ease: "none"` on the parent tween when each individual stop already carries its own per-step easing.
- Use `easeEach` when every segment in the ladder should share the same overall feel/easing.
- Do not copy numeric distances or timing values from examples verbatim — derive them from the actual composition's real geometry and duration.
- For one subject moving between two boxes/positions, prefer a single continuous transform tween or FLIP (see Mechanism table) over multiple separately-eased keyframes. Splitting `x/y/scale` into several distinct eased keyframes should only be done when the viewer is meant to feel distinct beats — every additional segment changes velocity and risks reading as an unwanted hitch.

## Channels — what to animate

Prefer compositor/visual channels, which animate cheaply and predictably:
`x/y/z`, `xPercent/yPercent`, `scale`, `rotationX/Y/Z`, `skew`, `transformOrigin`, `svgOrigin`, `opacity`, `autoAlpha`, `clip-path`, masks, CSS custom properties (vars), SVG path/dash values, camera transforms, shader uniforms.

Avoid layout/lifecycle channels, which are expensive, unpredictable, or not reliably seekable:
`top/left/right/bottom`, `width/height`, `margin/padding`, `display`, `visibility` (as a tweened property), late DOM element creation, or helper/overlay elements that are secretly doing the subject's motion instead of the subject itself.

For visibility changes specifically: use `autoAlpha` on the registered, seekable GSAP timeline, or a zero-duration `tl.set()` placed at an explicit time boundary. Target only a non-clip element, or a wrapper element inside the clip — never target the `.clip` element itself directly. Never duration-tween the raw CSS `visibility` property, and never tween `display`.

## Mechanism choice table

Choose the smallest mechanism that proves the prompt — mechanisms can be combined, but every added mechanism must clarify the idea; decoration for its own sake is not proof of the intended motion.

| Need | Mechanism |
|---|---|
| Same subject changes box or hierarchy | shared element / FLIP |
| Subject travels a visible route | path travel |
| Stroke grows or traces | stroke draw |
| Shape becomes another shape | shape interpolation |
| Reveal boundary is visible | clip, mask, or shader uniform |
| Many items move with order | stagger / indexed delay |
| Text itself moves | line, word, character, or band subdivision |
| Surface bends, stretches, or crops | parent/child counter-transform |
| UI has states | explicit state machine |
| Scene has depth | DOM 3D, Three.js, or WebGL camera/object keyframes |

For the full parts-shelf breakdown of each mechanism (what it solves, what to keyframe, which runtime, how to verify), see `references/keyframe-patterns.md`.

## Timing principles

- Anticipation (a small counter-motion before the main move) should only be used when it clarifies cause or direction.
- Acceleration should leave the rest state smoothly.
- The "peak proof" moment must show the mechanism unmistakably — it's the frame that proves the animation is doing what it claims.
- Follow-through sells energy and direction after the main motion.
- Overshoot should only be used when the subject should feel elastic or tactile.
- Constant-speed path travel usually needs `ease: "none"`.
- Discrete UI state changes usually need a sharp ease-out.
- Repeated elements need ordered/staggered offsets, not identical timing for every item.
- Final lockups (the resting end state) need longer holds than intermediate transition poses.
- Smoothness means continuous velocity on the same subject — avoid sudden velocity discontinuities.
- Do not let two tweens overlap while writing the same transform property unless that overlap is deliberate and has been verified to produce the intended combined result.
- Avoid animating a large `clip-path`/mask change on the same hero surface at the same time it's also scaling or traveling; instead, sequence nested reveals to happen after the main move has settled.

## Text

- Preserve line boxes, word spacing, readability, and final fit throughout the animation.
- If text moves internally (letters/words shifting), move the actual glyphs or masked text bands — not just decorative elements around the text while the text itself sits static.
- Always snapshot the readable frames as part of verification.

## SVG

- For stroke growth, prefer a dedicated draw-SVG plugin/mechanism (e.g. GSAP's DrawSVGPlugin); fall back to manipulating `stroke-dasharray`/`stroke-dashoffset` directly if unavailable.
- For shape interpolation (one shape becoming another), prefer a dedicated shape-morph plugin/mechanism (e.g. GSAP's MorphSVGPlugin); convert primitive shapes (circles, rects) to paths first if needed, and split complex silhouettes into simpler component parts before morphing.

## 3D

- Scale alone is fake depth and should not be relied on to sell a 3D effect.
- Use actual perspective on a stable parent element, `transform-style: preserve-3d`, real z-axis travel, rotation, camera/world motion, correct occlusion, and correct layer ordering when objects visually cross in depth.
- Use one or two diagnostic viewing angles that specifically expose the depth relationship being claimed. If the angled proof shows no actual depth crossing, improve the z-travel, camera setup, or occlusion until it does.

## Canvas / WebGL

- Keyframe camera position, camera target, object transform, material opacity, shader uniforms, and postprocess intensity — all driven through deterministic state, not live/random input.
- Render strictly from the composition's own time value (not wall-clock time).
- Use the ghost-rendering diagnostic (`--ghost`) for canvas/WebGL work, because ordinary marker/bounding boxes cannot see motion happening inside a canvas element.

## CLI verification commands

Run these as CLI commands (via `npx`) to lint, check, and inspect the composition:

```bash
npx hyperframes lint
npx hyperframes check
npx hyperframes keyframes .
npx hyperframes keyframes . --json
npx hyperframes keyframes . --runtime all
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --samples <n>
npx hyperframes keyframes . --selector "<selector>" --shot "<file>" --layout strip --from <t0> --to <t1>
npx hyperframes keyframes . --shot "<file>" --ghost --angle <angle>
npx hyperframes snapshot . --at <times>
```

Choose `<selector>` for the real animated subject (not a wrapper). Choose `<times>` for the first frame, proof poses, final-minus-hold, and the exact final frame. Choose `<angle>` only when depth specifically needs to be proven.

| Tool | Proves |
|---|---|
| `keyframes` | targets, explicit stops, paths, traces, composed parent/child motion, CSS stops, Anime registration |
| `--shot` | ghosts, route shape, time spacing, DOM 3D projection, focused selector proof |
| `--layout strip` | in-place motion, overlaps, contact, subtle scale/opacity, text waves |
| `--ghost` | canvas, WebGL, shader motion, rendered 3D |
| `snapshot --at` | masks, text readability, full state, final lockup, black/reset tails |

**If selector proof looks wrong, in order:**
1. Rerun with `--json` to get machine-readable detail.
2. Find the actual animated target (it may not be the selector you assumed).
3. Shoot that actual target.
4. Snapshot full frames.
5. Trust painted pixels over log output — the log can claim success while the render is wrong.

## Diagnostic reading guide

- `flat` means no explicit middle poses exist.
- `keyframes` means explicit stops exist.
- `motionPath` means a route exists.
- `trace` means multi-stroke drawing is happening.
- `composed with` means child motion inherits parent motion.
- Even ghost spacing in a `--shot`/`--ghost` output means constant speed.
- Clustered ghosts mean slow-in or a settle.
- Large gaps between ghosts mean fast travel.
- A helper-selector shot is not proof of the real subject's motion. An onion-skin shot layered over an otherwise broken full frame is not proof either — always confirm the full frame is correct too.

## Error handling reference

| Failure | Fix |
|---|---|
| endpoint-only (no visible middle poses) | add middle poses, hold the peak proof moment, rerun `--shot` |
| identity break (subject seems to be swapped mid-animation) | keep one element alive throughout, use shared source/final boxes, remove any substitute crossfade |
| fake 3D | add real z/camera travel, occlusion, and angled proof |
| wrong final frame | add a final hold, snapshot both final-minus-hold and the exact final frame |
| unseekable runtime | pause autoplay, register the instance in the correct global, remove timers, build the timeline synchronously |
| unreadable text | preserve line boxes, reduce displacement, add a final hold, snapshot the text frames specifically |

## Definition of done

Run `lint`, `check`, `keyframes`, one focused `--shot`, and snapshots. Confirm: the first frame is correct, proof poses are visible, there's a final-minus-hold frame and an exact final frame, motion is owned by the actual subject (not a helper/decoy element), and there are no debug overlays left in the output.

For the full parts-shelf mechanism table with source links (GSAP, Anime.js, MDN, Three.js docs) and additional runtime skeletons, see `references/keyframe-patterns.md`.

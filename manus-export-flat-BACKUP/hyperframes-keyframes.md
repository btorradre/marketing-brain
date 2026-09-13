# HyperFrames Keyframes

This document describes how to author seek-safe 2D/3D keyframes for a HyperFrames video/motion-graphics composition — GSAP timelines, CSS keyframes, Anime.js, WAAPI, paths, masks, SVG morph/draw, text motion, and 3D depth — and how to verify them with the `hyperframes` CLI. Use it whenever a composition needs an element (a subject) to move, transform, reveal, or change state in a way that must remain scrubbable/seekable at any point in time, not just play forward once. It is a mechanism reference, not a visual-style guide: consult it when you already know what should happen and need to choose and correctly implement the underlying animation mechanism. It is not the place for broad scene strategy, brand design, media sourcing, captions strategy, or general video planning — those live in separate HyperFrames reference documents (`hyperframes-animation.md` for broad scene recipes, `hyperframes-core.md`/`hyperframes-creative.md` for the wider composition system).

Keyframes, in this system, are a "pose contract": a keyframe defines the visible states an animated subject passes through, preserves that subject's continuous identity across the animation, must run in a "seek-safe" runtime (the animation must be able to jump to any timestamp and render correctly, not just play linearly), and every claimed pose must be verified against actual rendered pixels, not just code that looks right.

## How to use this

1. **Identify the animated subject, its visible states, its final state, and the total runtime.** Name the actual DOM/SVG/canvas element that moves — not a wrapper or helper element — and enumerate the poses (positions/states) it must visibly pass through, including what it looks like at the very end.
2. **Choose the smallest mechanism that proves the intended motion.** Look at the Mechanism Choice table below to match the need (e.g., "subject travels a visible route" → path travel) to a technique. Only consult the deeper mechanism reference/parts-shelf material if the right mechanism isn't obvious from the table.
3. **Author the keyframes in the declared runtime (GSAP, CSS, Anime.js, or WAAPI), building them synchronously and registering the resulting timeline/instance in the runtime's expected global registry** (see Runtime Rules below). Do not build timelines asynchronously or leave them unregistered — the composition player needs to be able to find and seek them.
4. **Verify the result using the CLI diagnostics**: run `lint`, `check`, `keyframes`, one focused `--shot` on the actual animated selector, and snapshots at the specific proof times (first frame, proof poses, final-minus-hold, and the exact final frame).
5. **If verification fails, fix the source keyframes and rerun the smallest failing diagnostic** before attempting a full render. Don't just re-render and hope; isolate the failure with the narrowest possible tool first.

Before declaring the work done, run the full verification pass again (`lint`, `check`, `keyframes`, one focused `--shot`, and snapshots) and confirm: the first frame is correct, proof poses are visible, there is a final-minus-hold frame and an exact final frame, the motion is owned by the actual subject (not a decoy/helper element), and there are no leftover debug overlays in the output.

## Rules & standards

### Contract (non-negotiable properties of any keyframe animation)

- Name the moving subject explicitly.
- Name the poses needed to prove the intended motion, including the final state.
- Keyframe visible channels only — never hidden/helper state that doesn't render.
- Preserve object identity when continuity matters (the same element should persist through the motion rather than being swapped for a look-alike).
- Crossfade only when the intended motion is genuinely a replacement or dissolve of one thing for another.
- Hold readable or semantic states long enough for a viewer to actually see them.
- The final frame is part of the animation itself, not an afterthought/cleanup step.
- Do not reset the subject back to its rest/starting state unless that was explicitly requested.
- Do not end the animation on a black frame unless that was explicitly requested.
- If editing a pre-existing starter scene, preserve its layout, copy, assets, colors, and final state — do not redesign it — unless the user explicitly asked for a redesign.

### Runtime rules by technology

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
- Note: the text/documentation surface for this runtime does not list WAAPI explicitly as supported for text; verify any WAAPI-driven animation with `--shot` (which seeks WAAPI animations) plus snapshots rather than assuming it behaves like GSAP/CSS.

**Never use for render-critical motion, in any runtime:**
- `Date.now()`
- `performance.now()`
- unseeded `Math.random()`
- hover or scroll triggers
- timers (`setTimeout`/`setInterval`)
- timelines created asynchronously
- unregistered `requestAnimationFrame` calls
- infinite loops

All of these break "seek-safety" — the ability to jump the composition to any timestamp and get a correct, deterministic render.

### Keyframe forms

- **Array keyframes** — a pose ladder with a per-step duration and easing.
- **Percentage keyframes** — exact timing placement inside one tween.
- **Property arrays** — compact multi-stop changes to a single property.
- Set `ease: "none"` on the parent tween when each individual stop already carries its own per-step easing.
- Use `easeEach` when every segment in the ladder should share the same overall feel/easing.
- Do not copy numeric distances or timing values from examples verbatim — derive them from the actual composition's real geometry and duration.
- For one subject moving between two boxes/positions, prefer a single continuous transform tween or FLIP (see Mechanism table) over multiple separately-eased keyframes. Splitting `x/y/scale` into several distinct eased keyframes should only be done when the viewer is meant to feel distinct beats — every additional segment changes velocity and risks reading as an unwanted hitch.

### Channels — what to animate

Prefer compositor/visual channels, which animate cheaply and predictably:
`x/y/z`, `xPercent/yPercent`, `scale`, `rotationX/Y/Z`, `skew`, `transformOrigin`, `svgOrigin`, `opacity`, `autoAlpha`, `clip-path`, masks, CSS custom properties (vars), SVG path/dash values, camera transforms, shader uniforms.

Avoid layout/lifecycle channels, which are expensive, unpredictable, or not reliably seekable:
`top/left/right/bottom`, `width/height`, `margin/padding`, `display`, `visibility` (as a tweened property), late DOM element creation, or helper/overlay elements that are secretly doing the subject's motion instead of the subject itself.

For visibility changes specifically: use `autoAlpha` on the registered, seekable GSAP timeline, or a zero-duration `tl.set()` placed at an explicit time boundary. Target only a non-clip element, or a wrapper element inside the clip — never target the `.clip` element itself directly. Never duration-tween the raw CSS `visibility` property, and never tween `display`.

### Mechanism choice table

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

### Timing principles

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

### Text

- Preserve line boxes, word spacing, readability, and final fit throughout the animation.
- If text moves internally (letters/words shifting), move the actual glyphs or masked text bands — not just decorative elements around the text while the text itself sits static.
- Always snapshot the readable frames as part of verification.

### SVG

- For stroke growth, prefer a dedicated draw-SVG plugin/mechanism; fall back to manipulating `stroke-dasharray`/`stroke-dashoffset` directly if unavailable.
- For shape interpolation (one shape becoming another), prefer a dedicated shape-morph plugin/mechanism; convert primitive shapes (circles, rects) to paths first if needed, and split complex silhouettes into simpler component parts before morphing.

### 3D

- Scale alone is fake depth and should not be relied on to sell a 3D effect.
- Use actual perspective on a stable parent element, `transform-style: preserve-3d`, real z-axis travel, rotation, camera/world motion, correct occlusion, and correct layer ordering when objects visually cross in depth.
- Use one or two diagnostic viewing angles that specifically expose the depth relationship being claimed. If the angled proof shows no actual depth crossing, improve the z-travel, camera setup, or occlusion until it does.

### Canvas / WebGL

- Keyframe camera position, camera target, object transform, material opacity, shader uniforms, and postprocess intensity — all driven through deterministic state, not live/random input.
- Render strictly from the composition's own time value (not wall-clock time).
- Use the ghost-rendering diagnostic (`--ghost`) for canvas/WebGL work, because ordinary marker/bounding boxes cannot see motion happening inside a canvas element.

## Templates & examples

### Recommended agent configuration for keyframe generation

Keyframe generation work in this system is expected to be handled through an image-capable configuration built on an OpenAI image model, presented with:

- Display name: "HyperFrames Keyframes"
- Short description: "Author seek-safe video keyframes"
- Default framing/prompt for the task: "Use hyperframes-keyframes to author seek-safe 2D/3D keyframes and verify them with the CLI."

In practice this just means: when a request calls for producing or checking seek-safe keyframes for a HyperFrames composition, this document's procedure and rules are the operating spec to follow, and the diagnostic CLI commands below are the way to confirm success — there is no separate exotic image-generation step beyond what's described here.

### GSAP skeleton (canonical starting structure)

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

### CSS skeleton

```css
.<subject> {
  animation: <name> <duration> <ease> both;
  animation-iteration-count: 1;
}
@keyframes <name> {
  0% {
    transform: <pose-a>;
    opacity: <a>;
  }
  100% {
    transform: <pose-b>;
    opacity: <b>;
  }
}
```

### Anime.js skeleton

```js
const animation = anime.timeline({ autoplay: false });
animation.add({ targets: "<selector>" /* derived channels */ });
window.__hfAnime = window.__hfAnime || [];
window.__hfAnime.push(animation);
```

### Three.js / WebGL skeleton

```js
const state = { progress: 0 };
tl.to(state, {
  progress: 1,
  duration: <duration>,
  onUpdate: () => {
    // derive camera/object/material values from state.progress
    renderer.render(scene, camera);
  },
});
```

### Mechanism parts shelf (detailed reference)

Start with one primary mechanism; add supporting motion only when it clarifies the idea. This is a parts shelf, not a style guide.

| Mechanism | Solves | Keyframe | Runtime | Verify |
|---|---|---|---|---|
| Path travel | Subject must visibly follow a route | path progress, tangent rotation, follower offset, trail opacity | GSAP MotionPath or sampled x/y/z | strip shot at bends; final snapshot |
| Stroke draw | A line, ring, or outline appears over time | dash/draw range, stroke opacity, endpoint state | DrawSVG or SVG dash fallback | partial mid snapshot; complete final |
| Shape interpolation | One silhouette becomes another | source path, middle path, target path, fill/stroke | MorphSVG or path tween | first/mid/final snapshots |
| Shared element | Same subject changes box or hierarchy | source box, target box, x/y, scale, radius, context opacity | GSAP Flip or manual FLIP | one identity moves; no substitute crossfade |
| Clip/mask reveal | Animated boundary exposes content | clip path, mask position/size, edge softness, inner counter-motion | CSS, SVG, GSAP, or shader | snapshot edge frames and final unclipped state |
| Ordered repetition | Many items enter, leave, or transform in order | indexed delay, x/y, scale, opacity, final alignment | GSAP stagger, Anime stagger, CSS vars | check first/middle/last item timing |
| Text subdivision | Text motion needs readable internal timing | line/word/char/band wrappers, y/x, opacity, final fit | SplitText, authored spans, Anime splitText | strip shot plus final readability snapshot |
| Surface transform | Image/card stretches, crops, or changes shape | parent scale/skew/clip, child counter-scale, transform origin | GSAP/CSS keyframes | no accidental warped final |
| UI state machine | Interface passes through semantic states | closed, active, loading, success/error, final | GSAP/CSS/Anime | snapshots hit states in order |
| DOM depth | HTML elements need 3D separation | perspective, z, rotationX/Y, opacity, crossing layer order | CSS 3D + GSAP/CSS/Anime | angled `--shot`; overlap snapshot |
| Camera/object 3D | Canvas/WebGL scene moves in depth | camera, target, object transform, material opacity | Three.js/WebGL + GSAP proxy | `--ghost`; snapshots at proof poses |
| Shader uniform | Pixel effect is driven by scalar progress | progress, edge width, noise, color mix, opacity | ShaderMaterial/WebGL uniforms | `--ghost`; snapshot 0/edge/mid/final |
| Instanced system | Many 3D objects move as one system | instance transforms, scale, color/opacity, camera | Three InstancedMesh | snapshots, because DOM boxes miss internals |
| Imported model | Model animation must scrub deterministically | `AnimationMixer.setTime`, camera, material, lights | Three AnimationMixer | drive from composition time; `--ghost` |

### CLI verification commands

Run these as shell/CLI commands (via `npx`) to lint, check, and inspect the composition:

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

### Diagnostic reading guide

- `flat` means no explicit middle poses exist.
- `keyframes` means explicit stops exist.
- `motionPath` means a route exists.
- `trace` means multi-stroke drawing is happening.
- `composed with` means child motion inherits parent motion.
- Even ghost spacing in a `--shot`/`--ghost` output means constant speed.
- Clustered ghosts mean slow-in or a settle.
- Large gaps between ghosts mean fast travel.
- A helper-selector shot is not proof of the real subject's motion. An onion-skin shot layered over an otherwise broken full frame is not proof either — always confirm the full frame is correct too.

### Error handling reference

| Failure | Fix |
|---|---|
| endpoint-only (no visible middle poses) | add middle poses, hold the peak proof moment, rerun `--shot` |
| identity break (subject seems to be swapped mid-animation) | keep one element alive throughout, use shared source/final boxes, remove any substitute crossfade |
| fake 3D | add real z/camera travel, occlusion, and angled proof |
| wrong final frame | add a final hold, snapshot both final-minus-hold and the exact final frame |
| unseekable runtime | pause autoplay, register the instance in the correct global, remove timers, build the timeline synchronously |
| unreadable text | preserve line boxes, reduce displacement, add a final hold, snapshot the text frames specifically |

### Definition of done

Run `lint`, `check`, `keyframes`, one focused `--shot`, and snapshots. Confirm: the first frame is correct, proof poses are visible, there's a final-minus-hold frame and an exact final frame, motion is owned by the actual subject (not a helper/decoy element), and there are no debug overlays left in the output.

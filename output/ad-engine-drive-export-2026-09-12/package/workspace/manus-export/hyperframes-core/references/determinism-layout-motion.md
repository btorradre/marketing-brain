# Determinism, animation runtime, layout, and full-screen motion

HyperFrames seeks compositions frame-by-frame. Every frame must be reproducible from its time value alone — same input time, same pixels. Three contracts enforce this: the animation runtime contract, the determinism rules, and the layout contract. A fourth section covers the full-screen shared-background motion pattern, which depends on the determinism and layout rules to work correctly.

## Animation runtime contract

GSAP is the primary runtime. The core requirement is generic: animation state must be seekable from HyperFrames time.

For GSAP: create the timeline **synchronously** during page initialization. Use `gsap.timeline({ paused: true })`. Register it on `window.__timelines["<composition-id>"]`, where the key must match `data-composition-id` on the composition root. Do **not** call `tl.play()` for render-critical motion. Do **not** build timelines inside `async` functions, Promises, `setTimeout`, or event handlers — the renderer can sample the page before they finish. Do **not** create empty tweens only to set a duration — use `data-duration` on the clip instead. Do **not** `gsap.set()` clip elements from later scenes at page-load time — they are not in the DOM yet; use `tl.set(selector, vars, time)` inside the timeline at or after the clip's `data-start`.

## Duration contract for non-GSAP runtimes

The render engine needs a positive total duration before it will capture a single frame — without one, capture fails outright ("Composition has zero duration"). A GSAP timeline supplies this automatically. CSS, WAAPI, and Lottie compositions have no timeline object, so the runtime infers duration itself:

- **CSS**: longest `animation-delay` + `animation-duration` × finite `animation-iteration-count` across animated elements (offset by each element's `data-start`). `animation-iteration-count: infinite` cannot be inferred.
- **WAAPI**: longest `element.animate()` effect's computed end time. Infinite `iterations` cannot be inferred.
- **Lottie**: the registered animation's native length (total frames ÷ frame rate, or the player's own duration) — always finite regardless of loop setting.
- **Three.js**: not inferable at all — time only flows in via a seek event; there's no animation-clip inspection.

`data-duration` on the root element is therefore optional whenever every non-GSAP animation on the page is finite. It is **required** when: the composition has an infinite/unbounded CSS or WAAPI animation, the composition uses Three.js, or there is no GSAP timeline and no animation signal at all for any adapter to discover.

For runtime-specific API details beyond this duration contract (GSAP plugin usage, Lottie player setup, Three.js render-loop wiring), consult the animation runtime library's own documentation for that runtime.

## Determinism rules

Rendered frames must be reproducible from the requested time. Do **not** use any of the following for visual state:

- `Date.now()`, `performance.now()`, or any render-time clock.
- Unseeded `Math.random()` — use a seeded pseudo-random generator if random-looking placement is needed.
- Render-time network fetches for required assets — inline or pre-bundle them.
- Hover, scroll, pointer, or focus state — the renderer has no input events.
- Infinite loops such as `repeat: -1`. Compute a finite count instead: `repeat: Math.max(0, Math.floor(duration / cycleDuration) - 1)` — use `floor`, not `ceil` (`ceil` overshoots the composition's duration), and `max(0, …)` avoids a negative repeat count, which GSAP treats as infinite.

Also avoid: animating anything outside the visual-property allowlist — `opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, and transforms. Never tween `display` or raw `visibility`. GSAP's `autoAlpha` is allowed on a registered seekable timeline because it interpolates opacity and only changes actual visibility at the fully-hidden endpoint. A zero-duration `tl.set(..., { visibility: "hidden" | "visible" })` is also allowed at an explicit beat boundary for a deterministic hard kill. **Both exceptions apply only to non-clip elements or wrappers inside a clip — never target a `.clip` element itself:** the framework alone controls a clip's visibility lifecycle. Also avoid animating the same property on the same element from multiple timelines at the same time — GSAP's overwrite behavior in that situation is order-dependent and can flip between renders.

## Layout contract

Build the visible end-state in static HTML and CSS first, then animate from/to that state.

- The composition root has fixed pixel frame dimensions.
- **The root composition's total duration (render length/frame count) is fixed at compile time** — read once from the static root `data-duration` before scripts run, exactly like `data-width`/`data-height`. A script or an override value that rewrites the root `data-duration` afterward is ignored. To vary render length per output, author the root `data-duration` directly. (A *clip's* own `data-duration` is re-read from the live DOM, so scripts/variables can still drive clip lengths. Only when the root omits `data-duration` does the renderer probe the live DOM/timeline for total length.)
- Scene containers should fill the scene with `width: 100%; height: 100%; box-sizing: border-box`.
- Use padding, flex, grid, and `max-width` for layout. Avoid positioning main content with hardcoded `top`/`left` offsets when a layout container can do it.
- Use `position: absolute` for layers and decorative elements, not as the default content-layout strategy.
- Prefer transforms and opacity for animation.
- Keep text inside its intended container — use `max-width`, wrapping, or a font-fitting helper if the runtime provides one (e.g. `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })`).
- For text measurement without triggering DOM reflow, use a text-measurement helper if the runtime provides one (e.g. `window.__hyperframes.pretext`: `pretext.prepare(text, font)` then `pretext.layout(prepared, maxWidth, lineHeight)`) — pure arithmetic, safe to call per-frame for text reflow, shrinkwrap containers, and pre-render layout computation.
- **Do not** use `<br>` in body text. Forced breaks ignore the actual rendered font width and can produce an extra break when the line already wraps naturally, causing overlap. Let text wrap via `max-width`. Exception: short display titles where each word is deliberately meant to be on its own line.
- **Transformed elements must be block-level and sized.** `transform`/`scaleX`/`scaleY` is a no-op on an inline `<span>`, and scaling an auto-width (0px) element shows nothing — an invisible bar or fill. Give them `display: block`/`inline-block`/flex-item **and** a real `width`/`height` (e.g. `width: 100%` inside a sized parent). This is a silent bug automated checks may miss.
- **Absolutely-positioned decoratives that pulse or overshoot** (a `yoyo` scale, a `back.out` ease) need clearance at their *peak* size and must not straddle an `overflow: hidden` edge — otherwise they overlap a neighbor or get clipped. Position for the largest frame, not the resting one. Also a silent bug.

## Why this matters

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

Note: this pattern is about a shared **background**, not a shared full-bleed content fill. A full-bleed scene *fill* (a solid color panel, gradient, or grid meant to ground one particular scene) should still be authored as its own full-duration `class="clip"` child element on the lowest content track — never painted as a `background` directly on the composition root itself. See `data-attributes-and-tracks.md` for why a root-level background is unreliable once a composition is assembled into a larger render.

# GSAP Animation Reference

A reference for writing animations with the GSAP JavaScript library — core tween methods, easing, staggering, timelines, and performance practices — plus two ready-made effect patterns (typewriter text, audio-reactive visualizers). Use this whenever you're writing a web-based animation, motion graphic, or video composition that uses GSAP (e.g. an HTML/JS-based video composition, an animated web page, or any programmatic motion-graphics deliverable built with JavaScript + CSS/SVG/Canvas).

## How to use this

1. Include GSAP (and any plugins you need, such as TextPlugin) via a script tag or package import.
2. Pick the right tween method for what you're animating: `gsap.to()` to animate toward new values, `gsap.from()` for entrance animations (animate from given values to the current state), `gsap.fromTo()` when you need to specify both start and end explicitly, and `gsap.set()` to apply values instantly with no animation.
3. Always use camelCase property names (e.g. `backgroundColor`, `rotationX`), and prefer GSAP's transform aliases (`x`, `y`, `scale`, `rotation`, etc.) over writing raw CSS `transform` strings.
4. For anything with more than one or two animated elements in sequence, build a `gsap.timeline()` rather than chaining individual tweens with manual delays — use the timeline's position parameter and labels to sequence precisely.
5. For performance, animate only transform and opacity properties where possible, mark actively-animating elements with `will-change: transform`, use `stagger` instead of many separate tweens, and kill or pause tweens that are no longer visible/needed.
6. For responsive or accessibility-aware behavior (e.g. respecting `prefers-reduced-motion`, or different animation on desktop vs. mobile), use `gsap.matchMedia()`.

## Rules & standards

### Core tween methods
- **gsap.to(targets, vars)** — animate from current state to `vars`. Most common.
- **gsap.from(targets, vars)** — animate from `vars` to current state (entrances).
- **gsap.fromTo(targets, fromVars, toVars)** — explicit start and end.
- **gsap.set(targets, vars)** — apply immediately (duration 0).
- Always use camelCase property names.

### Common vars
- **duration** — seconds (default 0.5).
- **delay** — seconds before start.
- **ease** — `"power1.out"` (default), `"power3.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"`.
- **stagger** — a number (e.g. `0.1`) or an object: `{ amount: 0.3, from: "center" }`, `{ each: 0.1, from: "random" }`.
- **overwrite** — `false` (default), `true`, or `"auto"`.
- **repeat** — a number, or `-1` for infinite. **yoyo** — alternates direction with repeat.
- **onComplete**, **onStart**, **onUpdate** — callbacks.
- **immediateRender** — default `true` for `from()`/`fromTo()`. Set `false` on later tweens targeting the same property+element to avoid overwrite conflicts.

### Transforms and CSS
Prefer GSAP's transform aliases over raw `transform` strings:

| GSAP property | Equivalent |
|---|---|
| `x`, `y`, `z` | translateX/Y/Z (px) |
| `xPercent`, `yPercent` | translateX/Y in % |
| `scale`, `scaleX`, `scaleY` | scale |
| `rotation` | rotate (deg) |
| `rotationX`, `rotationY` | 3D rotate |
| `skewX`, `skewY` | skew |
| `transformOrigin` | transform-origin |

- **autoAlpha** — prefer over `opacity`. At 0, also sets `visibility: hidden`.
- **CSS variables** — e.g. `"--hue": 180`.
- **svgOrigin** (SVG only) — global SVG coordinate space origin. Don't combine with `transformOrigin`.
- **Directional rotation** — `"360_cw"`, `"-170_short"`, `"90_ccw"`.
- **clearProps** — `"all"` or a comma-separated list; removes inline styles on complete.
- **Relative values** — `"+=20"`, `"-=10"`, `"*=2"`.

### Function-based values
```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  stagger: 0.1,
});
```

### Easing
Built-in eases: `power1`–`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`. Each has `.in`, `.out`, `.inOut` variants.

### Defaults
```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

### Controlling tweens
```javascript
const tween = gsap.to(".box", { x: 100 });
tween.pause();
tween.play();
tween.reverse();
tween.kill();
tween.progress(0.5);
tween.time(0.2);
```

### gsap.matchMedia() — responsive and accessibility
Runs setup only when a media query matches; auto-reverts when it stops matching.
```javascript
let mm = gsap.matchMedia();
mm.add(
  {
    isDesktop: "(min-width: 800px)",
    reduceMotion: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { isDesktop, reduceMotion } = context.conditions;
    gsap.to(".box", {
      rotation: isDesktop ? 360 : 180,
      duration: reduceMotion ? 0 : 2,
    });
  },
);
```

### Timelines

**Creating a timeline:**
```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

**Position parameter** (third argument controls placement):
- Absolute: `1` — at 1s
- Relative: `"+=0.5"` — after end; `"-=0.2"` — before end
- Label: `"intro"`, `"intro+=0.3"`
- Alignment: `"<"` — same start as previous; `">"` — after previous ends; `"<0.2"` — 0.2s after previous starts

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<"); // same start as .a
tl.to(".c", { opacity: 0 }, "<0.2"); // 0.2s after .b starts
```

**Labels:**
```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.play("outro");
tl.tweenFromTo("intro", "outro");
```

**Timeline options:** `paused: true` (create paused, call `.play()` to start), `repeat`, `yoyo` (apply to whole timeline), `defaults` (vars merged into every child tween).

**Nesting timelines:**
```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
```

**Playback control:** `tl.play()`, `tl.pause()`, `tl.reverse()`, `tl.restart()`, `tl.time(2)`, `tl.progress(0.5)`, `tl.kill()`.

### Performance

- **Prefer transform and opacity.** Animating `x`, `y`, `scale`, `rotation`, `opacity` stays on the compositor. Avoid `width`, `height`, `top`, `left` when transforms achieve the same effect.
- **will-change:** `will-change: transform;` — only on elements that actually animate.
- **gsap.quickTo() for frequent updates** (e.g. mouse-following):
```javascript
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" }),
  yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });
container.addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```
- **Stagger beats many tweens.** Use `stagger` instead of separate tweens with manual delays.
- **Cleanup.** Pause or kill off-screen animations.

### Best practices
- Use camelCase property names; prefer transform aliases and `autoAlpha`.
- Prefer timelines over chaining with delay; use the position parameter.
- Add labels with `addLabel()` for readable sequencing.
- Pass defaults into the timeline constructor.
- Store the tween/timeline return value when you need to control playback later.

### Do not
- Animate layout properties (width/height/top/left) when transforms suffice.
- Use both `svgOrigin` and `transformOrigin` on the same SVG element.
- Chain animations with delay when a timeline can sequence them instead.
- Create tweens before the DOM exists.
- Skip cleanup — always kill tweens when they're no longer needed.

## Templates & examples

### Typewriter text effect

Reveal text character by character using GSAP's TextPlugin.

**Required plugin:**
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

**Basic typewriter:**
```js
const text = "Hello, world!";
const cps = 10; // chars per second: 3-5 dramatic, 8-12 conversational, 15-20 energetic
tl.to(
  "#typed-text",
  { text: { value: text }, duration: text.length / cps, ease: "none" },
  startTime,
);
```

**With blinking cursor.** Three rules: (1) one cursor visible at a time — hide the previous before showing the next; (2) the cursor must blink when idle, including after typing and during pauses; (3) no gap between text and cursor — elements must be flush in the HTML.

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```
```css
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.cursor-blink { animation: blink 0.8s step-end infinite; }
.cursor-solid { animation: none; opacity: 1; }
.cursor-hide { animation: none; opacity: 0; }
```
Pattern: blink → solid (typing starts) → type → solid → blink (typing done).
```js
tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], startTime);
tl.to("#typed-text", { text: { value: text }, duration: dur, ease: "none" }, startTime);
tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], startTime + dur);
```

**Backspacing.** TextPlugin removes from the front — wrong for backspace. Use manual substring removal:
```js
function backspace(tl, selector, word, startTime, cps) {
  const el = document.querySelector(selector);
  const interval = 1 / cps;
  for (let i = word.length - 1; i >= 0; i--) {
    tl.call(
      () => { el.textContent = word.slice(0, i); },
      [],
      startTime + (word.length - i) * interval,
    );
  }
  return word.length * interval;
}
```

**Spacing with static text.** When a typewriter word sits next to static text, use `margin-left` on a wrapper span. Don't use flex gap (spaces the cursor from the text) or a trailing space in static text (collapses when the dynamic text is empty).
```html
<div style="display:flex; align-items:baseline;">
  <span style="font-size:40px; color:#555;">Ship something</span>
  <span style="margin-left:14px;"><span id="word"></span><span id="cursor">|</span></span>
</div>
```

**Word rotation.** Type → hold → backspace → next word. Cursor blinks during every idle moment (holds, after backspace).
```js
words.forEach((word, i) => {
  const typeDur = word.length / 10;
  tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
  tl.to("#typed-text", { text: { value: word }, duration: typeDur, ease: "none" }, offset);
  tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + typeDur);
  offset += typeDur + 1.5; // hold

  if (i < words.length - 1) {
    tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
    const clearDur = backspace(tl, el, word, offset, 20);
    tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + clearDur);
    offset += clearDur + 0.3;
  }
});
```

**Appending words** (build a sentence word-by-word into the same element):
```js
let accumulated = "";
words.forEach((word) => {
  const target = accumulated + (accumulated ? " " : "") + word;
  const newChars = target.length - accumulated.length;
  tl.to("#typed-text", { text: { value: target }, duration: newChars / 10, ease: "none" }, offset);
  accumulated = target;
  offset += newChars / 10 + 0.3;
});
```

**Multi-line cursor handoff.** When handing off between typewriter lines: hide previous → blink new → pause → solid when typing. Never go hidden→solid directly (it skips the idle state).
```js
tl.call(
  () => {
    prevCursor.classList.replace("cursor-blink", "cursor-hide");
    nextCursor.classList.replace("cursor-hide", "cursor-blink");
  },
  [],
  handoffTime,
);
const typeStart = handoffTime + 0.5; // brief blink pause
tl.call(() => nextCursor.classList.replace("cursor-blink", "cursor-solid"), [], typeStart);
tl.to("#next-text", { text: { value: text }, duration: dur, ease: "none" }, typeStart);
tl.call(() => nextCursor.classList.replace("cursor-solid", "cursor-blink"), [], typeStart + dur);
```

**Typing speed guide:**

| CPS | Feel | Good for |
|---|---|---|
| 3-5 | Slow, deliberate | Dramatic reveals, suspense |
| 8-12 | Natural typing | Dialogue, narration |
| 15-20 | Fast, energetic | Tech demos, code |
| 30+ | Near-instant | Filling long blocks |

### Audio-reactive visualizer

Pre-extract audio data, then drive canvas/DOM/WebGL rendering from a GSAP timeline. A helper script (`extract-audio-data.py`, requiring ffmpeg and numpy) analyzes an audio or video file and outputs per-frame loudness and frequency-band data as JSON — if you don't have that exact script, write equivalent code (ffmpeg to extract audio + an FFT/band-energy analysis) to produce the same data shape.

**Data format:**
```json
{
  "fps": 30, "totalFrames": 5415,
  "frames": [{ "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3] }]
}
```
- **rms** (0–1): overall loudness, normalized across the track.
- **bands[]** (0–1): frequency magnitudes. Index 0 = bass, higher = treble. Each band normalized independently.

**Loading the data.** Load it synchronously, not with async `fetch()` — the timeline must be built synchronously so a deterministic rendering/capture pass can read it immediately after page load; building timelines inside a `.then()` callback means the timeline isn't ready in time.
```js
// Option A: inline (small files, under ~500KB)
var AUDIO_DATA = { /* paste audio-data.json contents */ };

// Option B: sync XHR (large files)
var xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false);
xhr.send();
var AUDIO_DATA = JSON.parse(xhr.responseText);
```

**Rendering approaches:**
- **Canvas 2D** (most common — bars, waveforms, circles, gradients):
```js
for (let f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    () => {
      const frame = AUDIO_DATA.frames[f];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // draw using frame.rms and frame.bands
    },
    [],
    f / AUDIO_DATA.fps,
  );
}
```
- **WebGL / Three.js** — patch the clock for deterministic time if doing frame-exact rendering; update shader uniforms from the audio data each frame.
- **DOM elements** — fine for fewer than ~20 animated elements; less performant than Canvas for many.

**Spatial mapping:**
- Horizontal: bass left, treble right (iterate bands left-to-right).
- Vertical: bass bottom, treble top.
- Circular: bass at 12 o'clock, wrap clockwise; mirror for a full circle.

**Smoothing:**
```js
let prev = null;
const smoothing = 0.25; // 0.1-0.2 snappy, 0.3-0.5 flowing
function smooth(f) {
  const raw = AUDIO_DATA.frames[f];
  if (!prev) {
    prev = { rms: raw.rms, bands: [...raw.bands] };
    return prev;
  }
  prev = {
    rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
    bands: raw.bands.map((b, i) => prev.bands[i] * smoothing + b * (1 - smoothing)),
  };
  return prev;
}
```

**Motion principles:**
- Bass drives big moves — scale, glow, position shifts.
- Treble drives detail — shimmer, flicker, edge effects.
- RMS drives globals — background brightness, overall energy.
- Pick 2–3 properties to animate; more looks noisy.
- Keep minimums above zero — quiet sections still need life.

**Band count:**

| Bands | Detail | Good for |
|---|---|---|
| 4 | Low | Background glow, pulsing |
| 8 | Medium | Bar charts, basic spectrum |
| 16 | High | Detailed EQ (default) |
| 32 | Very high | Dense radial layouts |

**Layering.** Layer multiple canvases with CSS z-index for depth — a background layer driven by bass/RMS and a foreground layer driven by individual bands creates depth without added complexity.
```html
<canvas id="bg-layer" style="position:absolute;top:0;left:0;z-index:1;"></canvas>
<canvas id="main-layer" style="position:absolute;top:0;left:0;z-index:2;"></canvas>
```

# HyperFrames Animation Technique Library

## Purpose

This is the complete animation technique library for HyperFrames, an HTML/video-composition rendering framework that builds animated video output from paused, seek-driven GSAP (or other runtime) timelines rendered frame-by-frame. Reach for this document any time you are building an animated HTML/CSS/JS video composition and need to choose or implement a specific motion effect — an atomic technique (a single animated behavior like a spring pop-in or a camera push), a composed multi-phase scene template (a full shot combining several techniques), a scene-to-scene transition, or a runtime-specific implementation detail (GSAP, CSS keyframes, Three.js, Lottie, Anime.js, the Web Animations API, WebGPU/TypeGPU, or HTML-captured-as-canvas-texture). It contains concrete, load-bearing implementation detail — CSS properties, JavaScript/GSAP code patterns, easing functions, timing values, keyframe structures, parameter ranges, and hard constraints — reverse-engineered from production compositions and a large corpus of studied reference video ads.

The core rendering discipline behind every technique in this document: a HyperFrames composition builds ONE paused animation timeline per composition, registers it on a global so the renderer can seek it to an exact point in time, and the renderer then captures the composition frame-by-frame by seeking that timeline — never by playing it in real time. This means every animation technique in this library must be **deterministic** (the same seek time always produces the same visual state) and **seek-safe** (seeking backward or forward, including to time zero, must render the correct frame with no reliance on animations having "already played"). That discipline explains many of the specific rules below: no `Math.random()` or `Date.now()`-based randomness (use index-seeded pseudo-random hashes instead), no infinite loops (`repeat: -1` is forbidden — compute finite repeat counts from the visible duration), no CSS `@keyframes` animations that run on the browser's independent clock for anything render-critical, and a strong preference for `fromTo()` over `from()` so the starting state is always explicit rather than implied by whatever the CSS/DOM state happened to be at load time.

## How to use this

**Default approach: compose atomic rules.** For most motion work, pick 2–4 atomic animation rules from the Animation Rules section below and glue them together on a single paused timeline. This is faster and produces cleaner code than reaching for a full pre-built scene template. Look up a rule by its trigger, tag, or category, read its full recipe, and adapt the HTML/CSS/JS pattern to your content.

**Reach for a composed blueprint when:** the scene you're building matches an existing pre-designed multi-phase template (a brand reveal, a social-proof moment, a UI demo, a data-viz reveal, etc.) and reusing its phase pipeline saves real authoring time, or you want runnable ground-truth code for a complex 4–5 phase choreography. Don't read a blueprint speculatively — load it once you've already decided the shot needs full scene-level orchestration rather than a from-scratch composition of atomic rules. Every blueprint below documents which "role" (Hook, Problem, Product Intro, Key Feature, Benefits, Social Proof, CTA, Brand Outro) it serves, a duration range, a full time-coded shot structure, a motion vocabulary, and a rule-by-rule mapping back to the atomic Animation Rules section — use that mapping to find the exact implementation for each moving part.

**Picking a runtime:** GSAP is the default choice for the large majority of motion work — it covers timeline orchestration, transforms, easing, and stagger, and essentially all of the atomic rules in this library are written against it. Reach for Lottie when an asset already has its own pre-baked animation timeline (typically an After Effects export). Reach for Three.js for 3D scenes, camera motion through 3D space, or shader-driven visuals. Reach for Anime.js for lightweight tweening in cases where a full GSAP timeline would be overkill. Reach for plain CSS keyframes for simple repeated motifs, decorative loops, shimmer, or glow where a JavaScript-driven timeline isn't worth the cost. Reach for the Web Animations API when you want native browser keyframes without a GSAP dependency. Reach for TypeGPU/WebGPU when a canvas needs to be GPU-rendered — particle systems, liquid-glass effects, custom shaders. Multiple runtimes can coexist in a single composition; each one registers its own animation instances on its own runtime-specific global variable so the render engine can seek all of them together in a single pass.

**Composition-level constraints that shape every technique below** (the "why" behind many of the specific rules that follow):

- The composition builds one **paused** timeline per composition and registers it on a shared global registry keyed to the composition's ID — the render engine drives the playhead, the composition code never calls `.play()` for anything render-critical.
- Total render duration comes from an explicit duration value set on the composition root — never try to "pad" a timeline's length with empty filler tweens to extend it.
- No `Math.random()`, `Date.now()`, or `performance.now()` anywhere in render-critical code — use index-seeded deterministic pseudo-random hash functions instead (several concrete implementations appear throughout the rules below).
- No infinite repeats (`repeat: -1`) — compute a finite repeat count from the composition's visible duration.
- Never build a timeline inside `async` code, a `setTimeout`, or a `.then()` Promise callback — the render engine reads the registered timeline synchronously right after the page loads; anything built asynchronously may not exist yet when the first frame is captured, and different parallel render workers may see it in different states, causing visible flicker across frames of the same video.
- Animate **transforms and paint-only properties** (`opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, custom CSS properties) — never animate `width`, `height`, `top`, `left`, `margin`, `padding`, or other properties that trigger browser layout reflow. This is not just a performance nicety: because the renderer captures individual frames rather than a continuous real-time stream, the browser's layout engine snaps reflow-triggering properties to whole device pixels, which is invisible on a fast tween but produces visible stutter on a slow one. Use `scaleX`/`scaleY` (with the correct `transform-origin`) or `x`/`y` offsets instead, or use masking/clip-path techniques.
- Never duration-tween `display` or raw `visibility` — use GSAP's `autoAlpha` (which combines opacity with an endpoint visibility toggle) or a zero-duration timeline `set()` at an explicit boundary instead.
- Group staggers should be capped so an arrival reads as one cohesive beat (roughly: item count × stagger interval ≤ about half a second).
- Put no CSS `transition` property on any animated element — CSS transitions interpolate on the browser's own clock independently of the seek-driven timeline and will flicker or desync under seek. Use `will-change: transform` as a compositor hint on elements carrying many concurrent tweens instead.
- DOM measurements (`getBoundingClientRect()`, `offsetHeight`, etc.) should only be taken at one-time composition setup, and only in a single-scene composition — in a multi-scene montage, later clips may not be laid out yet when an earlier clip's setup code runs, so use hand-authored CSS-matched constants instead of measuring across scene boundaries. Never re-measure inside a per-frame `onUpdate` callback — the renderer may sample frames out of real-time order across parallel workers, and a live DOM measurement can desync from the deterministic value used to build the tween.

## Broader Motion-Design Techniques

These are thirteen proven, more general motion-design patterns — standard techniques that a well-produced composition typically uses two or three of, layered underneath the atomic rules and blueprints described later in this document. Each includes a minimal, adaptable code pattern.

### 1. SVG Path Drawing

A path draws itself in real time, like someone tracing it with a pen — used for revealing diagrams, arrows, connector lines, or brand marks.

```html
<svg viewBox="0 0 400 200">
  <path
    class="draw-path"
    d="M 50 100 L 200 50 L 350 100"
    stroke="#c84f1c"
    stroke-width="4"
    fill="none"
    stroke-linecap="round"
  />
</svg>
<style>
  .draw-path {
    stroke-dasharray: 280;
    stroke-dashoffset: 280;
  }
</style>
<script>
  tl.to(".draw-path", { strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }, 0.5);
</script>
```

Use `path.getTotalLength()` to calculate the real dasharray value dynamically rather than guessing it.

### 2. Canvas 2D Procedural Art

Animated noise, particle fields, data visualizations — anything that evolves frame by frame. Drive it with a GSAP proxy object and a deterministic hash function so the same frame always renders identically:

```html
<canvas id="proc-canvas" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("proc-canvas");
  var ctx = canvas.getContext("2d");

  function hash(x, y) {
    var n = x * 374761393 + y * 668265263;
    n = (n ^ (n >> 13)) * 1274126177;
    return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff;
  }

  function drawFrame(t) {
    ctx.fillStyle = "#0a0a0a";
    ctx.fillRect(0, 0, 1920, 1080);
    for (var i = 0; i < 200; i++) {
      var x = hash(i, 0) * 1920;
      var y = hash(i, 1) * 1080;
      var brightness = hash(i, Math.floor(t * 10)) * 255;
      ctx.fillStyle = "rgba(255, 255, 255, " + brightness / 255 + ")";
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  var proxy = { time: 0 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: 5,
      ease: "none",
      onUpdate: function () {
        drawFrame(proxy.time);
      },
    },
    0,
  );
</script>
```

### 3. CSS 3D Transforms

Perspective rotations create depth — used for product showcases, card flips, architectural reveals.

```html
<div class="stage" style="perspective: 900px;">
  <div class="card-3d" style="transform-style: preserve-3d;">
    <div class="face front">Product</div>
    <div class="face back" style="transform: rotateY(180deg);">Details</div>
  </div>
</div>
<script>
  tl.to(".card-3d", { rotationY: 360, rotationX: 15, duration: 1.2, ease: "sine.inOut" }, 0);
</script>
```

Always set `perspective` on the parent element, and `transform-style: preserve-3d` on the element(s) being animated.

### 4. Per-Word Kinetic Typography

Words appear one by one, synced to word-level transcript timestamps. This is the core technique for narration-driven videos.

```html
<div class="headline">
  <span class="word w-0">Anything</span>
  <span class="word w-1">a</span>
  <span class="word w-2">browser</span>
  <span class="word w-3">can</span>
  <span class="word w-4">render</span>
</div>
<style>
  .word {
    display: inline-block;
    opacity: 0;
    margin: 0 0.12em;
  }
</style>
<script>
  // Word onset times from the transcript (seconds relative to the beat's start)
  var timings = [0.0, 0.23, 0.28, 0.63, 0.78];
  var slides = [80, 60, 50, 25, 12]; // horizontal slide decay (px)

  document.querySelectorAll(".word").forEach(function (word, i) {
    tl.from(
      word,
      { x: slides[i], y: 14, opacity: 0, duration: 0.35, ease: "power2.out" },
      timings[i],
    );
  });
</script>
```

The slide distance DECAYS per word (80px → 12px) — this mimics a camera settling.

### 5. Lottie Animation

Vector animations that play inside a composition — used for logos, character animations, icons.

```html
<div id="logo-anim" class="lottie" style="width:500px;height:500px;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>
  window.__hfLottie = window.__hfLottie || [];

  const anim = lottie.loadAnimation({
    container: document.getElementById("logo-anim"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "../capture/assets/lottie/animation-0.json",
  });
  window.__hfLottie.push(anim); // REQUIRED — the runtime seeks every registered instance

  gsap.set("#logo-anim", { scale: 0.3, opacity: 0 });
  tl.to("#logo-anim", { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }, 0.2);
</script>
```

`autoplay: false` + `loop: false` + pushing the instance into the shared registry are all mandatory — the runtime seeks each registered player to the exact composition time, so anything left on `autoplay`/`loop` runs on the wall clock and renders non-deterministically. The seek is always to an absolute time (no modulo looping, no playback-rate scaling) — bake repeating cycles or non-default speed directly into the Lottie asset or into an explicit timeline, and verify the render. See the Lottie adapter section below for the full contract and the `.lottie`/dotLottie variant.

### 6. Video Compositing

Embedding real video footage inside a composition. Videos must be `muted` with `playsinline`.

```html
<div class="video-frame" style="width:680px;height:840px;border-radius:16px;overflow:hidden;">
  <video
    id="footage"
    src="../capture/assets/videos/clip.mp4"
    muted
    playsinline
    style="width:100%;height:100%;object-fit:cover;"
  ></video>
</div>
<script>
  // Video playback is controlled by the render framework — don't call play() manually
  tl.from(".video-frame", { scale: 0.9, opacity: 0, duration: 0.3, ease: "power2.out" }, 0);
</script>
```

The runtime handles video seeking and playback for you.

### 7. Character-by-Character Typing

Terminal typing effect using a timeline `.call()` to update text content one character at a time.

```html
<div class="terminal-line">
  <span class="prompt">❯</span>
  <span class="typed" id="typed-text"></span>
  <span class="cursor" style="width:11px;height:22px;background:#333;display:inline-block;"></span>
</div>
<script>
  var CMD = "some example command";
  var typed = document.getElementById("typed-text");

  // Cursor blinks
  tl.to(".cursor", { opacity: 0, duration: 0.12, yoyo: true, repeat: 20, ease: "steps(1)" }, 0);

  // Type each character
  for (var i = 0; i < CMD.length; i++) {
    (function (idx) {
      tl.call(
        function () {
          typed.textContent = CMD.substring(0, idx + 1);
        },
        null,
        (idx / CMD.length) * 0.9,
      );
    })(i);
  }
</script>
```

Use `ease: "steps(1)"` for a cursor blink — it creates a discrete on/off toggle rather than a fade.

### 8. Variable Font Axis Animation

Animate `font-variation-settings` to reshape glyphs in real time — works with variable fonts that expose axes like optical size (`opsz`), weight (`wght`), or softness (`SOFT`).

```html
<style>
  /* Load a locally captured variable font — do not use a remote Google Fonts @import.
     Point this at a locally hosted .woff2 asset. */
  @font-face {
    font-family: "Fraunces";
    src: url("../capture/assets/fonts/Fraunces-Variable.woff2") format("woff2");
    font-weight: 100 900;
    font-style: normal;
    font-display: block;
  }
  .wordmark {
    --opsz: 144;
    --wght: 440;
    font-family: "Fraunces", serif;
    font-variation-settings:
      "opsz" var(--opsz),
      "wght" var(--wght);
    font-size: 200px;
  }
</style>
<script>
  tl.to(".wordmark", { "--opsz": 72, "--wght": 300, duration: 0.45, ease: "power2.out" }, 0);
</script>
```

The glyph subtly reshapes as the axes animate — optical size adjusts fine detail, weight changes stroke thickness.

### 9. GSAP MotionPathPlugin

Animate an element along an arbitrary SVG path — used for sliders that follow curves, particles along trajectories, guided reveals.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/MotionPathPlugin.min.js"></script>
<div class="dot" style="width:20px;height:20px;background:#2a8a7c;border-radius:50%;"></div>
<script>
  gsap.registerPlugin(MotionPathPlugin);
  tl.to(
    ".dot",
    {
      motionPath: { path: "M 12 300 C 280 280 520 80 820 50 S 1200 48 1308 38" },
      duration: 1.5,
      ease: "power2.out",
    },
    0,
  );
</script>
```

### 10. Velocity-Matched Transitions

Exit one beat and enter the next with matched velocities — this creates the perception of continuous motion across a cut.

```javascript
// EXIT (in the outgoing composition): accelerating with blur
tl.to(
  ".content",
  { y: -150, filter: "blur(30px)", opacity: 0, duration: 0.33, ease: "power2.in" }, // accelerates
  beatDuration - 0.33,
);

// ENTRY (in the incoming composition): decelerating from blur
gsap.set(".content", { y: 150, filter: "blur(30px)" });
tl.to(
  ".content",
  { y: 0, filter: "blur(0px)", duration: 1.0, ease: "power2.out" }, // decelerates
  0,
);
```

The fastest point of both curves meets exactly at the cut — the viewer perceives smooth camera-like motion across the boundary. Match ease families: `.in` for exits, `.out` for entries.

### 11. Audio-Reactive Animation

Drive any GSAP-tweenable property from the playing audio track. Bass pulses a logo on kick drums, treble glows a CTA on cymbals, amplitude breathes a background during quiet phrases — motion locked to the track in a way pre-authored tweens never can.

**When to use:** any video with music or dramatic narration — brand reels, product launches, hype edits. Skip for calm/tutorial pacing.

**How it works:** pre-extract audio frequency bands into a JSON file, then sample it per frame via `tl.call()`:

```js
// audio-data.json: { fps: 30, totalFrames: 900, frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...] }
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        var bass = frame.bands[0]; // 0–1
        var treble = frame.bands[13];
        gsap.set(".logo", { scale: 1 + bass * 0.04 }); // 3–4% pulse on bass
        gsap.set(".cta", { filter: `drop-shadow(0 0 ${treble * 24}px #00C3FF)` });
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}
```

Per-frame sampling is required — a single tween will not react to the audio. Extract the audio band data ahead of time with an ffmpeg + numpy-based extraction script that outputs the JSON shape above given `--fps` and `--bands` parameters.

Keep text/logo intensity subtle (roughly ≤5% scale, ≤30% glow) — audio-reactive motion on small elements reads as jitter. Bigger backgrounds can push to 10–30%. **Never do:** equalizer bars, spectrum analyzers, waveform displays, strobing, or rainbow color cycling. The audio should provide *timing and intensity*; the visual vocabulary still comes from the brand.

### 12. Clip-Path Reveal Masks

A fixed window that content slides through — text or images enter from one side and are clipped by an invisible boundary. This is different from SVG path drawing: here the mask is static and the content moves.

```html
<div id="reveal-mask">
  <div id="reveal-content">Your headline text here</div>
</div>
<style>
  #reveal-mask {
    position: absolute;
    inset: 0;
    clip-path: inset(0 200px 0 0); /* clips 200px from the right */
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #reveal-content {
    font-size: 108px;
    white-space: nowrap;
  }
</style>
<script>
  // Content starts offscreen right, slides left through the mask window
  gsap.set("#reveal-content", { x: 400, opacity: 0 });
  tl.to("#reveal-content", { x: 0, opacity: 1, duration: 1, ease: "power2.out" }, 0);
</script>
```

Variations: `clip-path: circle(0% at 50% 50%)` → `circle(100%)` for iris reveals. `clip-path: polygon(...)` for custom shapes.

### 13. WebGL Fragment Shader Art

Full GPU generative backgrounds — domain-warped FBM noise, cosine-palette coloring, iridescent organic patterns. Far richer than Canvas 2D.

```html
<canvas id="shader-bg" width="1920" height="1080"></canvas>
<script>
  var canvas = document.getElementById("shader-bg");
  var gl = canvas.getContext("webgl");
  if (!gl) {
    /* fall back to a plain gradient */
  }

  var fsrc = `
    precision mediump float;
    varying vec2 v_uv;
    uniform float u_time;
    uniform vec2 u_res;

    float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float noise(vec2 p) {
      vec2 i = floor(p), f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i), hash(i+vec2(1,0)), f.x),
                 mix(hash(i+vec2(0,1)), hash(i+vec2(1,1)), f.x), f.y);
    }
    float fbm(vec2 p) {
      float v = 0.0, a = 0.5;
      mat2 R = mat2(0.8, 0.6, -0.6, 0.8);
      for (int i = 0; i < 5; i++) { v += a*noise(p); p = R*p*2.02; a *= 0.5; }
      return v;
    }
    vec3 palette(float t) {
      return vec3(0.5)+vec3(0.5)*cos(6.28318*(vec3(1)*t+vec3(0.0,0.33,0.67)));
    }
    void main() {
      vec2 uv = v_uv; uv.x *= u_res.x/u_res.y;
      float t = u_time * 0.4;
      vec2 q = vec2(fbm(uv*3.0+t*0.3), fbm(uv*3.0+vec2(5.2,1.3)+t*0.2));
      vec2 r = vec2(fbm(uv*3.0+q*4.0+vec2(1.7,9.2)+t*0.15), fbm(uv*3.0+q*4.0+vec2(8.3,2.8)+t*0.1));
      float n = fbm(uv*3.0+r*2.0);
      vec3 col = palette(n*2.0+t*0.2);
      col = mix(col, palette(length(q)*3.0+t*0.1), 0.4);
      col *= 0.7+0.3*n;
      float vig = 1.0-0.4*length(v_uv-0.5);
      gl_FragColor = vec4(col*vig, 1.0);
    }
  `;

  // Compile, link, set up a fullscreen quad, then render via a GSAP proxy:
  var proxy = { time: 0.5 };
  tl.to(
    proxy,
    {
      time: 5,
      duration: BEAT_DUR,
      ease: "none",
      onUpdate: function () {
        gl.uniform1f(uTime, proxy.time);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      },
    },
    0,
  );
</script>
```

Always include a Canvas 2D gradient fallback for environments without WebGL.

### When to Use What

| Video energy | Techniques to combine |
| --- | --- |
| High impact (launches, promos) | Per-word typography + velocity transitions + counter animations |
| Cinematic (tours, stories) | SVG path drawing + video compositing + 3D transforms |
| Technical (dev tools, APIs) | Character typing + Canvas 2D procedural + MotionPath |
| Premium (luxury, enterprise) | Variable font animation + Lottie + slow velocity transitions |
| Data-driven (stats, metrics) | Canvas 2D procedural + counter animations + SVG path drawing |

### HTML-Captured-as-GPU-Texture Techniques (advanced, sparing use)

A heavier, separate capability from everything above: capturing ANY live HTML/CSS as a GPU texture, then rendering it through WebGL shaders, Three.js 3D scenes, or post-processing effects at 60fps, pixel-perfect, with every CSS feature supported. Reach for this on 1–3 hero beats per video, not every beat — the contrast between flat standard-GSAP beats and these treated beats is itself part of the visual storytelling.

**Core boilerplate** (shared by every effect in this category):

```html
<!-- 1. Source HTML — content goes inside a canvas that captures its subtree -->
<canvas
  id="hic-source"
  layoutsubtree
  width="1920"
  height="1080"
  style="position:absolute;inset:0;opacity:0;"
>
  <div id="hic-content" style="width:1920px;height:1080px;">
    <!-- YOUR HTML CONTENT HERE — text, images, cards, dashboards, anything -->
  </div>
</canvas>

<!-- 2. Render target — the visible canvas that shows the effect -->
<canvas id="hic-output" width="1920" height="1080" style="position:absolute;inset:0;"></canvas>
```

```js
// 3. Feature detection — always check, always provide a fallback
function isHiCSupported() {
  var tc = document.createElement("canvas");
  if (!("layoutSubtree" in tc)) return false;
  tc.setAttribute("layoutsubtree", "");
  var ctx = tc.getContext("2d");
  return ctx && typeof ctx.drawElementImage === "function";
}
var apiOk = isHiCSupported();

// 4. Capture function — call this every frame in onUpdate
var capCanvas = document.getElementById("hic-source");
var capCtx = capCanvas.getContext("2d");
function captureContent() {
  if (apiOk) {
    capCtx.drawElementImage(document.getElementById("hic-content"), 0, 0, 1920, 1080);
  }
}

// 5. Drive from a GSAP timeline — capture + render every frame
tl.to(
  proxy,
  {
    /* your animation properties */
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      // render your effect here (Three.js or raw WebGL2)
    },
  },
  0,
);
```

**Fallback:** when the capture API is unavailable in a preview browser, draw a solid-color placeholder or use Canvas 2D text — the effect still works at final render time when the render engine's headless browser has the feature enabled.

**Effect catalog:**

**1. 3D Rotation with Bloom (Three.js)** — content floats in 3D space, slowly rotating with cinematic glow around bright edges, like a product screenshot displayed in a dark theater. Use for hero product showcases, feature reveals, premium-feeling CTAs. Key components: `PlaneGeometry` + `CanvasTexture` + `EffectComposer` + `UnrealBloomPass`.

```js
// After the boilerplate above, add:
var scene3d = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(45, 1920 / 1080, 0.1, 100);
camera.position.set(0, 0, 4);

var renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("hic-output"),
  antialias: true,
  alpha: true,
});
renderer.setSize(1920, 1080);

var texture = new THREE.CanvasTexture(capCanvas);
var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(3.6, 2.2),
  new THREE.MeshBasicMaterial({ map: texture }),
);
scene3d.add(mesh);

// Post-processing: bloom for cinematic glow.
// EffectComposer / RenderPass / UnrealBloomPass are ES-module named imports
// (see below) — NOT properties of THREE in modern versions. Three.js r150+
// removed the UMD examples/js/ globals.
var composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene3d, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.3, 0.4, 0.85));

var proxy = { rotY: -0.12, zoom: 4.2 };
tl.to(
  proxy,
  {
    rotY: 0.12,
    zoom: 3.6,
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      texture.needsUpdate = true;
      mesh.rotation.y = proxy.rotY;
      camera.position.z = proxy.zoom;
      composer.render();
    },
  },
  0,
);
```

Load Three.js and post-processing via ES modules:

```html
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
  import { EffectComposer } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/EffectComposer.js";
  import { RenderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/RenderPass.js";
  import { ShaderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/ShaderPass.js";
  import { UnrealBloomPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/UnrealBloomPass.js";
  // ... rest of composition code using these imports
</script>
```

The old `examples/js/` UMD path was removed in Three.js r152 — use `examples/jsm/` (ES modules).

**2. Magnetic Cursor Distortion (raw WebGL2)** — content warps and bends toward a moving point like a magnet pulling on pixels, with chromatic aberration splitting RGB channels at the distortion site. Use for an interactive feel, a product demo with a cursor, or a "look at THIS feature" moment. No Three.js needed — raw WebGL2 with a custom fragment shader combining a Gaussian warp and a chromatic split:

```js
var gl = document.getElementById("hic-output").getContext("webgl2", {
  alpha: false,
  preserveDrawingBuffer: true,
});

var VS = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

var FS = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 fragColor;
uniform sampler2D u_tex;
uniform vec2 u_cursor;   // cursor position (0-1)
uniform float u_strength; // warp strength (0-1)

void main() {
  vec2 uv = v_uv;
  vec2 delta = uv - u_cursor;
  float dist = length(delta);
  float warp = u_strength * exp(-dist * dist * 8.0);
  vec2 warped = uv - delta * warp * 0.3;

  // Chromatic aberration at the distortion site
  float aberration = warp * 0.008;
  float r = texture(u_tex, warped + vec2(aberration, 0.0)).r;
  float g = texture(u_tex, warped).g;
  float b = texture(u_tex, warped - vec2(aberration, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}`;

// Compile, link, set up quad geometry, upload the texture...

// Drive cursor position from GSAP
var proxy = { cx: 0.2, cy: 0.5, strength: 0.0 };
tl.to(
  proxy,
  {
    cx: 0.8,
    cy: 0.4,
    strength: 1.0,
    duration: BEAT_DURATION,
    ease: "power2.inOut",
    onUpdate: function () {
      captureContent();
      gl.uniform2f(cursorLoc, proxy.cx, proxy.cy);
      gl.uniform1f(strengthLoc, proxy.strength);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    },
  },
  0,
);
```

**3. Shatter / Fragment Explosion (Three.js)** — content breaks into geometric fragments that fly apart, revealing what's behind. Use for a dramatic transition, a "breaking free" moment, or tension release. Subdivide the source texture into a triangle mesh via `BufferGeometry`, then animate each fragment's position/rotation with GSAP, driven by a seeded PRNG (never `Math.random()`):

```js
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
var rng = mulberry32(42);

var fragments = [];
for (var i = 0; i < NUM_FRAGMENTS; i++) {
  var geom = new THREE.BufferGeometry();
  var mesh = new THREE.Mesh(geom, new THREE.MeshBasicMaterial({ map: texture }));
  scene3d.add(mesh);
  fragments.push({ mesh: mesh, targetPos: randomExplosionVector(rng), delay: rng() * 0.5 });
}

// Hold still, then EXPLODE
tl.to({}, { duration: holdTime }, 0);
fragments.forEach(function (frag) {
  tl.to(
    frag.mesh.position,
    { x: frag.targetPos.x, y: frag.targetPos.y, z: frag.targetPos.z, duration: 0.8, ease: "power3.in" },
    holdTime + frag.delay,
  );
  tl.to(
    frag.mesh.rotation,
    { x: rng() * 4, y: rng() * 4, duration: 0.8, ease: "power2.in" },
    holdTime + frag.delay,
  );
});
```

**4. Liquid / Fluid Surface (Three.js)** — content floats above (or IS) a rippling liquid surface with real-time wave dynamics. Use for an organic/premium feel, ambient backgrounds, "living" product showcases. Subdivided `PlaneGeometry` with vertex displacement driven by a noise-based vertex shader:

```js
var vertexShader = `
  varying vec2 vUv;
  uniform float u_time;
  void main() {
    vUv = uv;
    vec3 pos = position;
    pos.z += sin(pos.x * 3.0 + u_time * 2.0) * 0.15;
    pos.z += cos(pos.y * 2.5 + u_time * 1.5) * 0.1;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`;

var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(4, 3, 64, 64), // heavily subdivided for smooth waves
  new THREE.ShaderMaterial({
    vertexShader: vertexShader,
    fragmentShader: `varying vec2 vUv; uniform sampler2D u_tex;
      void main() { gl_FragColor = texture2D(u_tex, vUv); }`,
    uniforms: { u_tex: { value: texture }, u_time: { value: 0 } },
  }),
);
```

**5. Portal / Dimensional Reveal (Three.js)** — a glowing circular portal opens and content emerges through it from another dimension. Use for a product reveal, an "entering the app" moment, or a hero feature introduction.

**When to use HTML-in-Canvas vs standard GSAP:**

| Scenario | Use | Why |
| --- | --- | --- |
| Hero product screenshot showcase | HTML-in-Canvas (3D rotation + bloom) | Makes flat UI feel cinematic |
| Feature list / stats | Standard GSAP | Content-focused, doesn't need 3D |
| CTA / brand reveal | HTML-in-Canvas (portal or magnetic) | Makes the moment memorable |
| Social proof / logos | Standard GSAP | Orderly cascade, trust is steady |
| Transition between acts | HTML-in-Canvas (shatter) | Dramatic act break |
| Background atmosphere | HTML-in-Canvas (liquid surface) | Premium ambient feel |
| Quick feature cards | Standard GSAP | Speed matters, 3D would slow it down |

**More effects you can build from the same core boilerplate + a custom fragment shader** — each is a single GLSL function applied to the captured texture; you are not limited to these, any GLSL effect from ShaderToy, The Book of Shaders, or elsewhere can be adapted by copying the fragment shader, replacing built-in resolution/time uniforms with your own `u_res`/`u_time`, and adding a `uniform sampler2D u_tex` for the captured content:

**6. Noise Dissolve** — content dissolves into noise particles, revealing what's behind. Good for transitions.

```glsl
uniform float u_progress; // 0.0 = fully visible, 1.0 = fully dissolved
uniform sampler2D u_tex;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vec2 uv = v_uv;
  float noise = hash(uv * 50.0);
  float threshold = u_progress;
  if (noise < threshold) {
    float edge = smoothstep(threshold - 0.05, threshold, noise);
    fragColor = vec4(1.0, 0.6, 0.2, 1.0) * (1.0 - edge); // orange edge glow
  } else {
    fragColor = texture(u_tex, uv);
  }
}
```

**7. Holographic / Iridescent** — a rainbow-shifting holographic sheen that moves with time; premium, futuristic feel.

```glsl
uniform float u_time;
uniform sampler2D u_tex;

void main() {
  vec4 color = texture(u_tex, v_uv);
  float angle = v_uv.x * 6.28 + v_uv.y * 3.14 + u_time * 0.5;
  vec3 holo = vec3(
    sin(angle) * 0.5 + 0.5,
    sin(angle + 2.094) * 0.5 + 0.5,
    sin(angle + 4.189) * 0.5 + 0.5
  );
  fragColor = vec4(mix(color.rgb, holo, 0.15 + 0.1 * sin(u_time)), color.a);
}
```

**8. Scan Lines + CRT** — retro CRT monitor look, good for "code" or "terminal" beats.

```glsl
uniform sampler2D u_tex;
uniform float u_time;

void main() {
  vec2 uv = v_uv;
  vec2 centered = uv - 0.5;
  float dist = dot(centered, centered);
  uv = uv + centered * dist * 0.15;

  vec4 color = texture(u_tex, uv);
  float scanline = sin(uv.y * 800.0) * 0.04;
  color.rgb -= scanline;
  color.r = texture(u_tex, uv + vec2(0.001, 0.0)).r;
  color.b = texture(u_tex, uv - vec2(0.001, 0.0)).b;
  float vignette = 1.0 - dist * 2.0;
  fragColor = vec4(color.rgb * vignette, 1.0);
}
```

**9. Frosted Glass Blur** — content behind frosted glass, visible but softened. Good for "behind the scenes" or "coming soon."

```glsl
uniform sampler2D u_tex;
uniform float u_blur; // 0.0 = clear, 1.0 = full frost

void main() {
  vec2 uv = v_uv;
  vec4 color = vec4(0.0);
  float radius = u_blur * 0.015;
  for (float x = -2.0; x <= 2.0; x += 1.0) {
    for (float y = -2.0; y <= 2.0; y += 1.0) {
      color += texture(u_tex, uv + vec2(x, y) * radius);
    }
  }
  color /= 25.0;
  float frost = fract(sin(dot(uv * 200.0, vec2(12.9898, 78.233))) * 43758.5453);
  color.rgb += frost * 0.03 * u_blur;
  fragColor = color;
}
```

**10. Pixel Sort / Glitch Art** — pixels rearrange in vertical or horizontal strips, digital art aesthetic.

```glsl
uniform sampler2D u_tex;
uniform float u_intensity; // 0-1

void main() {
  vec2 uv = v_uv;
  float row = floor(uv.y * 80.0);
  float noise = fract(sin(row * 127.1) * 43758.5);
  float displace = step(0.7, noise) * u_intensity * 0.1;
  float r = texture(u_tex, uv + vec2(displace, 0.0)).r;
  float g = texture(u_tex, uv).g;
  float b = texture(u_tex, uv - vec2(displace * 0.5, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}
```

**Geometry ideas beyond flat planes:** `SphereGeometry` (content mapped onto a globe — world map, global reach), `CylinderGeometry` (content on a rotating cylinder — carousel/scroll feel), `TorusGeometry` (content wrapped around a ring — infinity, cycle), `BoxGeometry` (content on a 3D box — product packaging, dice), GLTF models (content mapped as a screen texture on a phone, laptop, or monitor model).

**Post-processing stacking** (via a Three.js `EffectComposer`): bloom + film grain = cinematic; bloom + chromatic aberration = lens effect; depth of field + vignette = focused attention; film grain + scan lines = retro. Multiple passes stack — add as many as you want.

## Library Adapters

Each runtime a composition might use (GSAP, Anime.js, CSS keyframes, Web Animations API, TypeGPU/WebGPU, Three.js, Lottie, and the HTML-in-canvas capture technique above) needs its animation instances registered on a runtime-specific global object so the seek-driven render engine can drive every instance's playhead in lockstep. The sections below document each adapter's contract and idiomatic usage.

### GSAP (the default runtime)

GSAP is the default choice for the large majority of motion work. The composition creates a **paused** timeline synchronously and registers it on a shared global registry keyed by the composition's own ID, and the render engine seeks it frame by frame.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  tl.from(".title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0);
  tl.to(".accent", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.25);

  window.__timelines["main"] = tl; // key must equal the composition root's id
</script>
```

- The registry key must match the composition root's own composition ID.
- Bracket and dot syntax both register (`window.__timelines["main"] = tl` and `window.__timelines.main = tl` are equivalent); bracket form is required when the id isn't a valid JS identifier (e.g. contains a hyphen).
- Do not call `tl.play()` for render-critical motion.
- Do not build timelines inside async code, timers, or event handlers.
- Keep loops finite — the render engine renders a finite video duration.
- **Render duration comes from an explicit duration attribute on the composition root, not from the GSAP timeline's own computed length.** Do not pad the timeline with empty tweens to "extend" it — set the duration attribute instead.

**Core tween methods:**

- `gsap.to(targets, vars)` — animate from the current state to `vars`. Most common.
- `gsap.from(targets, vars)` — animate from `vars` to the current state (entrances).
- `gsap.fromTo(targets, fromVars, toVars)` — explicit start and end states.
- `gsap.set(targets, vars)` — apply immediately (zero duration).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

**Common vars cheatsheet:** `duration` (seconds, default 0.5); `delay` (seconds before start); `ease` (e.g. `"power1.out"` default, `"power3.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"` — see the Easing & Stagger section below); `stagger` (number or object, see below); `repeat` (finite number, never `-1`); `yoyo` (alternates direction with repeat); `overwrite` (`false` default, `true`, or `"auto"`); `immediateRender` (default `true` for `from()`/`fromTo()` — set `false` on later tweens targeting the same property+element that shouldn't re-render immediately); `onComplete`/`onStart`/`onUpdate` callbacks.

**Animated property allowlist** — the render engine is stricter than vanilla GSAP:

- **Compositor-cheap:** `opacity`, `x`, `y`, `scale`, `scaleX`, `scaleY`, `rotation`, `rotationX`, `rotationY`, `skewX`, `skewY`, `transformOrigin`
- **Visual fills:** `color`, `backgroundColor`, `borderColor`, `borderRadius`
- **CSS variables:** e.g. `"--hue": 180`
- **Media `volume`** (on `<audio>`/`<video>`): animate for fades/ducking, e.g. `tl.to("#bgm", { volume: 0, duration: 1 }, "outro")` — the runtime probes these keyframes and drives them identically in preview and final render.
- **DOM text `innerText`** for numeric counters: tween it directly with `tl.to(el, { innerText: 100, snap: { innerText: 1 } })` — `snap` keeps it integer. Prefer a manual `onUpdate` proxy form when you need locale formatting or a suffix.

**Avoid** (use the matching transform alias instead): `width` / `height` / `top` / `left` / `right` / `bottom` / `margin*` / `padding*` — these trigger layout reflows. Use `scaleX`/`scaleY` (with `transformOrigin`) or `x`/`y`.

**Forbidden** (breaks the renderer or the visibility lifecycle): `display`, raw `visibility` — never duration-tween these; use `autoAlpha` (opacity plus an endpoint visibility toggle) or a zero-duration `set()` at an explicit timeline boundary. Anything driven by `Math.random()`, `Date.now()`, `performance.now()`, or a live event handler — animation state must be a deterministic function of time alone.

**Best practices:** use camelCase property names; prefer transform aliases and `autoAlpha`; prefer timelines over chained tweens with `delay` — use the position parameter instead; add labels with `addLabel()` for readable sequencing; pass shared defaults into the timeline constructor; store the tween/timeline return value when controlling playback.

**Do not:** animate layout properties when transforms suffice; use both `svgOrigin` and `transformOrigin` on the same SVG element; chain animations with `delay` when a timeline position parameter would do; create tweens before the DOM exists; use infinite `repeat: -1`.

#### GSAP — Timelines and Labels

Build one paused timeline per composition, attach it to the shared registry, and let the render engine seek it. Never call `.play()` for render-critical motion.

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.5, ease: "power3.out" },
});

tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

Timeline options: `paused: true` is required. `repeat`/`yoyo` apply to the whole timeline — `repeat: -1` is forbidden, use finite counts. `defaults` are vars merged into every child tween — use this instead of repeating `ease`/`duration` on every line.

**Position parameter** — the third argument to `.to()`/`.from()`/`.fromTo()` controls placement on the timeline:

| Form | Meaning |
| --- | --- |
| `0`, `1.5` | Absolute time in seconds |
| `"+=0.5"` | 0.5s after the end of the timeline |
| `"-=0.2"` | 0.2s before the end of the timeline |
| `"intro"` | At the `intro` label |
| `"intro+=0.3"` | 0.3s after the `intro` label |
| `"<"` | Same start as the previous tween |
| `">"` | Right after the previous tween ends |
| `"<0.2"` | 0.2s after the previous tween starts |
| `">-0.1"` | 0.1s before the previous tween ends |

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<"); // same start as .a
tl.to(".c", { opacity: 0 }, "<0.2"); // 0.2s after .b starts
```

Prefer the position parameter over `delay:` — it composes naturally and survives refactors that re-order tweens.

**Labels:**

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");

tl.addLabel("outro", "+=0.5");
tl.to(".a", { opacity: 0 }, "outro");
```

Labels make a long timeline readable and let multiple tweens converge on the same beat without re-typing absolute times.

**Nesting timelines:**

```javascript
const master = gsap.timeline({ paused: true });
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
```

Do not nest a sub-composition's own timeline into a host composition's timeline — sub-compositions with their own independent start time are seeked independently by the render engine. Nesting is only for grouping pieces of the *same* composition's own timeline.

**Inside sub-compositions, prefer `fromTo` over `from`:**

```javascript
// Sub-composition entrance — survives re-seek cleanly
tl.fromTo(".title", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.2);
```

The render engine re-seeks a sub-composition every time its host clip becomes visible. `gsap.from()` snapshots the starting state at registration time (page load); when the playhead jumps back before the sub-composition's start, that snapshot can desync from the actual CSS state and the element renders in the wrong position. `gsap.fromTo()` declares both endpoints explicitly, so the seek-back always produces the same start state. In top-level (standalone) compositions either form works, since there's no re-seek-through-mount cycle.

**Playback control** (debug/preview only): `tl.play()`, `tl.pause()`, `tl.reverse()`, `tl.restart()`, `tl.time(2)`, `tl.progress(0.5)`, `tl.kill()`. In rendered output the render engine calls `seek()` internally — your timeline must produce identical state for the same time value every time it is seeked.

#### GSAP — Transforms and Performance

**Transform aliases** — prefer GSAP's transform aliases over raw `transform` strings:

| GSAP property | Equivalent |
| --- | --- |
| `x`, `y`, `z` | `translateX/Y/Z` (px) |
| `xPercent`, `yPercent` | `translateX/Y` in `%` |
| `scale`, `scaleX`, `scaleY` | `scale` |
| `rotation` | `rotate` (deg) |
| `rotationX`, `rotationY` | 3D rotate |
| `skewX`, `skewY` | `skew` |
| `transformOrigin` | `transform-origin` |

Aliases let GSAP track and interpolate each axis independently, preventing accidental overwrites between separate tweens on the same element.

**`autoAlpha`** — prefer it over `opacity` for show/hide: `gsap.to(".panel", { autoAlpha: 0, duration: 0.4 })`. It sets both `opacity: 0` and `visibility: hidden`, removing the element from hit-testing/accessibility at zero alpha. Use it only on non-clip wrapper elements — the framework owns top-level clip visibility. Never duration-tween raw `visibility` or `display`.

**`clearProps`** — removes inline styles set by GSAP when a tween completes: `gsap.to(".item", { x: 100, rotation: 45, clearProps: "all" })` (or a comma-separated list of specific props). Useful at the end of an animation segment to hand the element back to CSS.

**CSS variables:** `gsap.to(".chart", { "--hue": 180, duration: 1 })` — animate any custom property (color, length, number).

**Relative and directional values:** relative — `"+=20"`, `"-=10"`, `"*=2"`. Directional rotation — `"360_cw"`, `"-170_short"`, `"90_ccw"`.

**SVG specifics:** `svgOrigin` sets the transform origin in the SVG's global coordinate space, not the element's local box — do NOT combine `svgOrigin` with `transformOrigin` on the same element, pick one. Animate SVG transform attributes via the same alias names (`x`, `y`, `rotation`) — GSAP handles the SVG-specific quirks.

**Performance rule — animate transforms, not layout properties.** Animate `x`, `y`, `scale`, `rotation`, `opacity`. Never animate `left`, `right`, `top`, `bottom`, `width`, `height`, `margin*`, or the text-reflow props `letterSpacing`/`wordSpacing`/`fontSize` — and never use `roundProps`.

This is a **render-correctness** rule, not just a GPU-performance nicety. The renderer seeks frame by frame and screenshots each frame, and the browser compositor snaps layout properties to whole device pixels. On a fast tween the per-frame step is several pixels so the snap is invisible; on a slow tween or a long ease-out tail the value moves less than a pixel per frame — it holds the same pixel for several frames, then jumps a whole one. The result: motion that looks smooth when fast but visibly stutters when slow. Transforms interpolate sub-pixel and stay smooth at any speed.

"Layout property" is broader than position — anything that triggers reflow snaps the same way. `letterSpacing`/`fontSize` are a common trap. The faithful smooth fix depends on which property — do not reach for `scale` reflexively:

- **`fontSize`** → animate `scale`. Scaling text up/down is the same visual and stays sub-pixel smooth (no reflow).
- **`letterSpacing`/`wordSpacing`** → uniform `scale` is NOT the same effect (it resizes the glyphs, not the gaps between them). To animate spacing smoothly, split the text into per-character (or per-word) elements and animate each one's `x` — the glyph spread is then a transform, sub-pixel smooth and visually identical to a letter-spacing tween. If the spacing change is a minor flourish, hold the final value statically instead.

**Fixing a flagged animation — preserve the intent.** A fix that merely passes a lint check can silently change the look. Swapping a `letterSpacing` tighten for a uniform `scale` "lints clean" but animates a *different thing*. Two rules: (1) reproduce the same visual — same start/end state, same trajectory, only sub-pixel-smooth, using the faithful equivalent (per-glyph `x` for spacing, `scale` for `fontSize`); (2) verify against the original, not against a linter — render the original and the fixed version and compare motion at key moments; the fix should differ only by the removed stutter, never by where things end up.

**Converting a position animation to a transform:** leave the element at its resting `left`/`top` in CSS and animate the *offset* with `x`/`y`:

```javascript
// CSS: #card { left: 1340px; top: 540px }   ← resting position stays in CSS
tl.to("#card", { left: 1340, top: 540, duration: 1 }); // ✗ stutters
tl.fromTo("#card", { x: 640, y: 0 }, { x: 0, y: 0, duration: 1 }); // ✓ x/y = delta from CSS rest
```

For a parent-relative `left: "100%"` sweep, use `xPercent: 100` only when the element is the full width of its container; otherwise convert to pixels.

**The one exception:** elements drawn through the HTML-in-canvas capture API described earlier — those under a canvas ancestor that captures its subtree. That canvas rasterizes from sub-pixel computed style, so layout props don't snap there. Everything the browser lays out normally follows the rule above.

**`will-change` (sparingly):** `.title { will-change: transform; }` — only on elements that actually animate; applied everywhere it becomes useless and burns memory.

**`gsap.quickTo` for frequent updates (preview-only):** for high-frequency updates driven by real user events (pointer move, scroll), `quickTo` reuses the same tween instead of creating a new one each frame. Render mode has no input events — the renderer seeks frame by frame and events like `mousemove`/`scroll` never fire, so this technique applies to live browser preview only; for audio-reactive motion in final renders, pre-extract audio data and drive the timeline declaratively as shown in the Audio-Reactive Animation technique above.

**Stagger beats N tweens** — one tween with a `stagger` option beats N tweens with manual delays for both readability and runtime cost. **Cleanup:** in live preview, pause or `kill()` off-screen animations; render mode is unaffected since the renderer drives time directly.

#### GSAP — Easing and Stagger

**Easing.** Built-in ease families: `power1`, `power2`, `power3`, `power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`, `none`. Each has `.in`, `.out`, `.inOut` variants.

| Ease | Use for |
| --- | --- |
| `power1.out`, `power2.out` | Gentle motion for secondary elements (a caption fade, a small shift). NOT the entrance default. |
| `power3.out` (house default), `power4.out` | The standard long-tail settle. Entrances, title cards, hero reveals. |
| `sine.inOut` | Long, slow, calm motion. Crossfades, ambient drift. |
| `back.out(1.7)` | Overshoot then settle. RARE — explicitly-playful register only, never a default. |
| `elastic.out(1, 0.3)` | Springy bounce. Same playful-only rule; prefer a baked spring (see below). |
| `expo.inOut` | Snappy, dramatic. Quick transitions between hero scenes. |
| `none` (linear) | Camera moves with timed counterpoint, mechanical motion. |

Pick `.out` for entrances, `.in` for exits, `.inOut` for symmetric moves and continuous motion.

**Smooth beats bouncy** — this is a house doctrine repeated throughout the rules below: entrances default to `power3.out` or a baked critically-damped spring (see below); overshoot eases (`back`/`elastic`/`bounce`) are a rare, explicitly-playful register, never the house style.

**Easing vocabulary (character and mood).** Easings are a tone of voice — a composition that only whispers is boring, one that varies between whisper/normal/punch is engaging. Draw on roughly 3 easing characters across a composition's beats, but vary *within* the smooth families by energy (`sine`/`power1` calm → `power3` standard → `power4`/`expo` punch) rather than reaching for overshoot to add variety. Overshoot is a register (explicitly playful), not a spice — one ease everywhere reads flat, but bounce everywhere reads cheap, and the second failure is worse.

| Family | Character | Typical use |
| --- | --- | --- |
| `power1`–`power4` | Gentle (1) to aggressive (4) acceleration curves | General purpose. `power3` is the house workhorse; `power2` for gentle secondary motion, `power4` for dramatic snaps |
| `back(N)` | Overshoot then settle. N controls how far past the target (1=subtle, 4=wild) | RARE — explicitly-playful register only. Keep N ≤ 2; prefer a baked spring at damping 0.6–0.7 for a physical settle |
| `elastic(amp, freq)` | Spring bounce. amp=magnitude, freq=oscillation speed | RARE — same playful-only rule; the baked spring below is the physical version |
| `bounce` | Ball-drop bouncing | RARE — physical-comedy register only (something literally dropping) |
| `expo` | Extreme acceleration (steeper than power4) | Premium/luxury reveals, dramatic entrances |
| `sine` | Smooth, organic, no hard edges | Ambient float, breathing, Ken-Burns-style drift, anything that loops. `.inOut` for yoyo motion |
| `circ` | Circular acceleration (starts very fast, ends very gentle or vice versa) | Camera moves, scene transitions, orbital motion |
| `steps(N)` | Discrete N-step jumps, no interpolation | Typing effects, cursor blink, counter ticks, retro/digital aesthetics |

**Mood mapping:** match easing character to the beat's emotional content. Smooth/organic easings (`sine`, `power1`) feel contemplative and drifting. Aggressive deceleration (`power4.out`, `expo.out`) feels snappy and confident. Spring overshoot (`back.out`) feels bouncy and physical — but reach for it only on explicitly-playful beats.

**Defaults:**

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.6, ease: "power3.out" }, // the house settle
});
```

Setting defaults at timeline scope documents the motion language of that composition in one place.

**Spring eases (baked physics, seek-safe).** The "iOS feel" is a damped spring's velocity curve, not a bounce — a fast launch into a long asymptotic settle. Well-made system animations are critically damped or close to it; `power3.out`/`expo.out` approximate that curve. When you want the exact curve — or a physical overshoot for the rare playful register — bake the spring's closed-form solution into a function ease:

```javascript
// springEase — a damped spring's exact position curve as a GSAP ease.
// response         ≈ seconds one oscillation would take (0.3–0.6 for entrances)
// dampingFraction  1.0       = critically damped — smooth settle, NO overshoot (house default)
//                  0.80–0.85 ≈ the iOS system register — ~1–1.5% overshoot, felt not seen
//                  0.60–0.70 = explicitly playful — ~5–10% overshoot (rare; replaces back.out)
function springEase({ response = 0.5, dampingFraction = 1 } = {}) {
  const w = (2 * Math.PI) / response; // undamped natural frequency
  const z = dampingFraction;
  let pos; // x(t): 0 → 1, starting at rest (v0 = 0)
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  } else if (z > 1) {
    const wo = w * Math.sqrt(z * z - 1);
    pos = (t) =>
      1 - Math.exp(-z * w * t) * (Math.cosh(wo * t) + ((z * w) / wo) * Math.sinh(wo * t));
  } else {
    pos = (t) => 1 - Math.exp(-w * t) * (1 + w * t);
  }
  // Settle time: last moment the curve sits outside ±0.1% of target.
  // Fixed-step scan, runs once at setup — deterministic (no Math.random / Date.now).
  const EPS = 0.001;
  const rate = z <= 1 ? z * w : (z - Math.sqrt(z * z - 1)) * w; // slowest decay mode
  const SCAN = 12 / rate;
  const N = 4800;
  let T = SCAN;
  for (let i = N; i >= 0; i--) {
    const t = (i / N) * SCAN;
    if (Math.abs(1 - pos(t)) > EPS) {
      T = ((i + 1) / N) * SCAN;
      break;
    }
  }
  const xT = pos(T);
  return {
    duration: T, // use as the tween's duration — the settle time IS the physics
    ease: (p) => pos(p * T) + p * (1 - xT), // normalized so ease(1) === 1 exactly
  };
}
```

Usage — take **both** the ease and the duration from the helper (the settle time is part of the physics; overriding the duration just re-times the same curve, so tune speed via `response` instead):

```javascript
const settle = springEase({ response: 0.4 }); // critically damped → duration ≈ 0.59s
tl.fromTo(
  "#hero",
  { scale: 0, opacity: 0 },
  { scale: 1, opacity: 1, duration: settle.duration, ease: settle.ease },
  0.2,
);
```

| dampingFraction | overshoot | register |
| --- | --- | --- |
| **1.0 (default)** | none (monotone) | The house settle — the exact curve `power3.out` approximates. Product / enterprise / serious tone. |
| 0.80–0.85 | ~1–1.5% | "Alive, not bouncy" — the iOS system default register. Felt, not seen. |
| 0.60–0.70 | ~5–10% | Explicitly-playful ONLY (replaces `back.out` — a spring's second-order settle reads physical where `back` reads cartoon). |
| < 0.55 | > 12% | Don't. Cartoon-wobble territory. |

| response | duration (ζ=1) | feel |
| --- | --- | --- |
| 0.25–0.35 | 0.37–0.51s | tight snap — chips, small UI |
| 0.35–0.50 | 0.51–0.74s | standard entrance |
| 0.50–0.70 | 0.74–1.03s | weighted hero landing — check the visible-by-t≤0.5s rule |

Craft notes: at ζ=1 the true spring front-loads harder than `power3.out` (~67% vs ~58% travelled at quarter-time) and settles on a longer asymptotic tail — that long tail is the "premium" read; use it when the settle IS the shot (a wordmark landing, a final lockup). At ζ<1, overshooting curves go on transforms only — never on `opacity` (it would push past 1) or color; split opacity onto its own `power2.out` tween at the same timeline position. The default of this section is ζ=1 — real spring physics is not a license for bounce.

**Stagger:**

```javascript
gsap.fromTo(".item", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.08 });
```

Object form:

```javascript
gsap.fromTo(
  ".item",
  { y: 24, opacity: 0 },
  {
    y: 0,
    opacity: 1,
    stagger: {
      each: 0.08, // delay between each
      from: "center", // "start" | "end" | "center" | "edges" | "random" | index
      amount: 0.6, // total stagger time (overrides each if both set)
      grid: "auto", // for 2D stagger
      axis: "x" | "y",
    },
  },
);
```

Prefer `stagger` over N separate tweens with manual delays. Use `fromTo()` rather than `from()` so the start state is explicit.

**Function-based values.** Any var can be a function `(index, target, targets) => value`:

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  rotation: (i) => (i % 2 === 0 ? 5 : -5),
  stagger: 0.1,
});
```

Use this for per-element values that depend on index, attributes, or measured size.

**`gsap.matchMedia` (preview only):** runs setup only when a media query matches and auto-reverts when it stops matching. Useful for live browser preview at different viewport sizes and for `prefers-reduced-motion`, but is NOT a substitute for rendering at the composition's actual fixed pixel dimensions — the final render always happens at a fixed viewport size.

### CSS Keyframe Animations

Use plain CSS `@keyframes` for simple repeated motifs, background motion, shimmer, glow, masks, and non-sequenced decoration — this avoids the JavaScript-timeline cost for content that belongs to one element with a fixed duration. For scene choreography, GSAP is usually clearer.

**Contract:** put the animated element in the DOM before runtime initialization finishes; give timed elements a start-offset value so local animation time matches the clip; use a finite `animation-duration` and `animation-iteration-count` because the renderer's negative-delay seek fallback cannot represent unbounded duration; prefer `animation-fill-mode: both` so seeked states hold correctly before and after active motion; avoid wall-clock JavaScript, hover-triggered state, and class toggles that depend on user events. The runtime discovers elements by their computed `animation-name`, seeks their browser Animation handles when available, and falls back to pausing with a negative `animation-delay`.

**Basic pattern:**

```html
<div
  id="pulse-ring"
  class="clip pulse-ring"
  data-start="0"
  data-duration="4"
  data-track-index="2"
></div>

<style>
  .pulse-ring {
    width: 280px;
    height: 280px;
    border: 4px solid rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation-name: pulse-ring;
    animation-duration: 1200ms;
    animation-timing-function: cubic-bezier(0.2, 0, 0, 1);
    animation-iteration-count: 3;
    animation-fill-mode: both;
  }

  @keyframes pulse-ring {
    from {
      opacity: 0;
      transform: scale(0.82);
    }
    35% {
      opacity: 1;
    }
    to {
      opacity: 0;
      transform: scale(1.18);
    }
  }
</style>
```

**Stagger pattern** — use CSS custom properties to avoid duplicating keyframes:

```html
<div class="clip dots" data-start="1" data-duration="3" data-track-index="3">
  <span style="--i: 0"></span>
  <span style="--i: 1"></span>
  <span style="--i: 2"></span>
</div>

<style>
  .dots span {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 10px;
    border-radius: 50%;
    background: currentColor;
    animation: dot-pop 900ms ease-out both;
    animation-delay: calc(var(--i) * 120ms);
  }

  @keyframes dot-pop {
    from {
      opacity: 0;
      transform: translateY(18px) scale(0.75);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
</style>
```

**Good uses:** decorative loops with a known repeat count; mask, glow, shimmer, grain, and subtle parallax layers; simple one-element entrances where a full JS timeline would be excessive.

**Avoid:** infinite CSS animations unless you have verified the browser exposes seekable animation handles for CSS animations (prefer a finite iteration count covering the visible duration — if you do use `infinite`, the composition root needs an explicit duration attribute, since there's nothing else to infer total length from); animating layout properties like `top`/`left`/`width`/`height` when transforms work; relying on hover, focus, scroll, or media queries to trigger render-critical motion; changing animation classes after startup unless another deterministic timeline controls that change.

**Composition duration inference:** the render engine needs to know a composition's total length. A GSAP timeline reports this automatically; a CSS-only composition has no timeline object, so the runtime infers duration from the longest running animation's computed end time (delay + duration × finite iteration-count, offset by any element start-time attribute). An explicit duration attribute on the root is optional whenever every CSS animation on the page is finite. `animation-iteration-count: infinite` has no finite end time and cannot be auto-inferred — if the composition's only animation is infinite, the root element must carry an explicit intended total-length duration attribute.

### Anime.js

The render engine can seek Anime.js instances through its own runtime adapter — the composition owns the animation objects, the render engine owns the clock.

**Contract:** create animations or timelines synchronously during composition initialization; set `autoplay: false` so Anime.js does not advance on its own clock; register every returned animation or timeline on a shared global array; use finite durations and loop counts; avoid callbacks that mutate the DOM based on wall-clock time, network state, or unseeded randomness. The adapter seeks every registered instance via its own `seek(timeMs)` method, where `timeMs` is the render engine's time in milliseconds.

**Basic pattern:**

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4.0.2/lib/anime.iife.min.js"></script>
<script>
  const anim = anime({
    targets: ".mark",
    translateX: 280,
    rotate: "1turn",
    opacity: [0, 1],
    duration: 1200,
    easing: "easeOutExpo",
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

**Timeline pattern:**

```html
<script>
  const tl = anime.timeline({
    autoplay: false,
    easing: "easeOutCubic",
  });

  tl.add({
    targets: ".title",
    translateY: [40, 0],
    opacity: [0, 1],
    duration: 650,
  }).add(
    {
      targets: ".accent",
      scaleX: [0, 1],
      duration: 450,
    },
    250,
  );

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(tl);
</script>
```

**Module builds:** if you use an ES module build, the adapter doesn't care how the instance was created — it only needs the returned object to expose `seek()`, `pause()`, and preferably `play()`:

```html
<script type="module">
  import { animate } from "https://cdn.jsdelivr.net/npm/animejs/+esm";

  const anim = animate(".chip", {
    x: "18rem",
    duration: 900,
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

**Good uses:** small SVG and DOM flourishes where Anime.js syntax is compact; imported Anime.js examples made seek-driven; multiple independent micro-animations pushed into the same registry. Use GSAP for complex scene sequencing unless the syntax specifically favors Anime.js — GSAP remains the primary authoring path.

**Avoid:** leaving `autoplay` at the Anime.js default; depending on a "currently running" auto-discovery instead of explicitly pushing to the registry array; infinite loops (compute a finite repeat count from the composition duration); building animations in timers, promises, event handlers, or after async asset loads.

### Web Animations API (WAAPI)

The render engine can seek native `element.animate()` animations through its WAAPI runtime adapter — useful for native browser keyframes with JavaScript-created timing and no GSAP dependency.

**Contract:** create animations synchronously during composition initialization; use `element.animate(...)` with a finite `duration` and `iterations`; use `fill: "both"` so seeked states persist; pause animations after creation or let the adapter pause them on first seek; avoid callbacks and promises for render-critical state. The adapter enumerates all document animations, sets each one's `currentTime` to the render engine's time in milliseconds, then pauses it.

**Basic pattern:**

```html
<div id="orb" class="clip orb" data-start="2" data-duration="3" data-track-index="2"></div>

<script>
  const orb = document.getElementById("orb");
  const animation = orb.animate(
    [
      { transform: "translate3d(-160px, 0, 0) scale(0.8)", opacity: 0 },
      { transform: "translate3d(0, 0, 0) scale(1)", opacity: 1, offset: 0.35 },
      { transform: "translate3d(120px, 0, 0) scale(1.08)", opacity: 1 },
    ],
    {
      duration: 3000,
      delay: 2000,
      easing: "cubic-bezier(0.2, 0, 0, 1)",
      fill: "both",
      iterations: 1,
    },
  );

  animation.pause();
</script>
```

**Stagger pattern:**

```js
document.querySelectorAll(".token").forEach((token, index) => {
  const animation = token.animate(
    [
      { transform: "translateY(24px)", opacity: 0 },
      { transform: "translateY(0)", opacity: 1 },
    ],
    {
      duration: 620,
      delay: index * 80,
      easing: "cubic-bezier(0.2, 0, 0, 1)",
      fill: "both",
      iterations: 1,
    },
  );
  animation.pause();
});
```

**Good uses:** lightweight DOM motion where CSS keyframes are too rigid and GSAP is unnecessary; generated animations from structured data; simple timelines representable as keyframes, delays, and offsets.

**Composition duration inference:** a WAAPI-only composition has no timeline object, so the runtime infers duration from every animation's computed end time (offset by when the animation was created relative to composition start). An explicit duration attribute is optional as long as every `element.animate()` call uses a finite `duration` and `iterations`.

**Avoid:** infinite `iterations` (has no finite computed end time — add an explicit duration attribute to the root if you must use it); depending on the `animation.finished` promise to mutate render-critical DOM; running separate clocks with `requestAnimationFrame`, timers, or `performance.now()`; animating layout properties when transforms and opacity suffice; assuming clip-local start time is automatic — the WAAPI adapter seeks document-level animation time, so model clip offsets with `delay` or create the animation on an element whose visibility is controlled by the render engine's own timing.

### TypeGPU / raw WebGPU

The render engine supports TypeGPU and raw WebGPU through its own runtime adapter — the adapter doesn't own the pipeline, it publishes the render engine's time and dispatches a seek event so the composition can render the exact GPU frame.

**Render-environment prerequisite:** WebGPU + the HTML-in-canvas capture technique together need the render engine's headless browser launched with unsafe-WebGPU and canvas-draw-element feature flags. Stock headless Chromium does not support that combination out of the box — for compositions combining WebGPU with HTML-in-canvas capture (liquid-glass effects and similar), point the render engine at a browser binary that does support the combination (e.g. Brave or Chrome Canary) via an environment variable pointing to that binary. Plain TypeGPU layers without HTML-in-canvas capture work in the standard headless browser — only the combination needs the override.

**Contract:** initialize WebGPU asynchronously (`await navigator.gpu.requestAdapter()`), but register all GSAP tweens **synchronously** — before any `await` — since the render engine reads the timeline immediately at page load. Render from the render engine's own published time, not `performance.now()`. Listen for the seek event and re-render at exactly that time. Guard against environments where WebGPU is unavailable — the adapter does not check for you. For video renders, call `await device.queue.onSubmittedWorkDone()` after submitting GPU work to ensure the canvas is flushed before the frame is captured.

**Basic pattern:**

```html
<canvas id="gpu-layer"></canvas>
<script>
  (async () => {
    if (!navigator.gpu) return;
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) return;
    const device = await adapter.requestDevice();
    const canvas = document.getElementById("gpu-layer");
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext("webgpu");
    const fmt = navigator.gpu.getPreferredCanvasFormat();
    ctx.configure({ device, format: fmt, alphaMode: "opaque" });

    const timeUniform = new Float32Array([0]);
    const timeBuf = device.createBuffer({
      size: 16,
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
    });

    function render(t) {
      timeUniform[0] = t;
      device.queue.writeBuffer(timeBuf, 0, timeUniform);
      const enc = device.createCommandEncoder();
      const pass = enc.beginRenderPass({
        colorAttachments: [
          {
            view: ctx.getCurrentTexture().createView(),
            loadOp: "clear",
            clearValue: { r: 0, g: 0, b: 0, a: 1 },
            storeOp: "store",
          },
        ],
      });
      pass.setPipeline(pipeline);
      pass.setBindGroup(0, bindGroup);
      pass.draw(3);
      pass.end();
      device.queue.submit([enc.finish()]);
    }

    render(0);
    window.addEventListener("hf-seek", (e) => render(e.detail.time));
  })();
</script>
```

**Timeline registration:** GSAP tweens driving text/HTML must be registered synchronously before any `await`:

```js
const tl = gsap.timeline({ paused: true });

// Caption tweens: synchronous, added before WebGPU init
gsap.set(".cap", { opacity: 0 });
tl.to("#cap-1", { opacity: 1, duration: 0.3 }, 1.0);
tl.to("#cap-1", { opacity: 0, duration: 0.2 }, 3.5);

window.__timelines["my-comp"] = tl;

// GPU-dependent tweens can go inside the async IIFE
(async () => {
  // ... WebGPU init ...
  const proxy = { value: 0 };
  tl.to(proxy, { value: 1, duration: 2, onUpdate: render }, 0.5);
})();
```

**Video-backed effects (liquid glass, distortion):** to use a `<video>` element as the GPU input texture, wait for its metadata before creating the texture, then create it at the video's native resolution:

```js
const videoEl = document.getElementById("aroll");

await new Promise((r) => {
  if (videoEl.readyState >= 1) r();
  else videoEl.addEventListener("loadedmetadata", r, { once: true });
});

const vw = videoEl.videoWidth,
  vh = videoEl.videoHeight;
const bgTex = device.createTexture({
  size: [vw, vh],
  format: "rgba8unorm",
  usage:
    GPUTextureUsage.COPY_DST | GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.RENDER_ATTACHMENT,
});

function render(t) {
  try {
    device.queue.copyExternalImageToTexture({ source: videoEl }, { texture: bgTex }, [vw, vh]);
  } catch (_) {
    /* frame not decoded yet */
  }
  // ... draw ...
}
```

**Render-mode caveat:** the headless browser used for final rendering may fail `copyExternalImageToTexture` for video elements. For production renders, pre-extract key frames via ffmpeg as PNGs and load them as image textures instead.

**Frosted blur via downsample pass:** a single-pass Gaussian kernel is too weak for glass-like frosted blur. Use a two-pass approach — (1) render the full-res texture to a small texture (~1/6 resolution; bilinear filtering during the downsample naturally averages pixels), then (2) sample the small texture for the frosted interior (bilinear upscale = heavy smooth blur) and the full-res texture for sharp areas and chromatic refraction. This approximates a mip-level texture sample without generating actual mipmaps.

**Transparent vs opaque canvas:** `alphaMode: 'opaque'` — the GPU canvas renders the full frame (video + effect); use when the GPU pipeline handles all visual content. `alphaMode: 'premultiplied'` — the GPU canvas is transparent where alpha = 0, letting HTML elements below show through; use for overlays (particles, path animations) on top of a regular `<video>` element.

**WGSL full-screen triangle** — the standard vertex shader for full-screen effects (no vertex buffer needed):

```wgsl
struct Vo { @builtin(position) pos: vec4f, @location(0) uv: vec2f }

@vertex fn vs(@builtin(vertex_index) vi: u32) -> Vo {
  let ps = array<vec2f, 3>(vec2f(-1., -1.), vec2f(3., -1.), vec2f(-1., 3.));
  let ts = array<vec2f, 3>(vec2f(0., 1.), vec2f(2., 1.), vec2f(0., -1.));
  return Vo(vec4f(ps[vi], 0., 1.), ts[vi]);
}
```

Draw with `pass.draw(3)` — one triangle that covers the viewport.

**Rounded-rect SDF** (liquid glass pill):

```wgsl
fn sdf_box(p: vec2f, half_size: vec2f, corner_radius: f32) -> f32 {
  let d = abs(p) - half_size + vec2f(corner_radius);
  return length(max(d, vec2f(0.))) + min(max(d.x, d.y), 0.) - corner_radius;
}
```

Use this to define inside/ring/outside zones for glass effects — negative values are inside the shape.

**Deterministic rendering:** no `Math.random()` — use a seeded PRNG. No `requestAnimationFrame` for the render loop — render only in response to the seek event. No `performance.now()` for animation time — read the render engine's published time value directly from the seek event. After GPU submit, call `await device.queue.onSubmittedWorkDone()` for render-mode frame capture.

### Three.js / WebGL

The render engine supports Three.js through its own runtime adapter. The adapter does not own the scene — it publishes the render engine's time and dispatches a seek event so the composition can render the exact frame.

**Contract:** create the scene, camera, renderer, materials, and assets synchronously when possible. Render from the render engine's own time, not wall-clock time. Listen for the seek event and render exactly that time. Load models, textures, and HDRIs before render-critical seeking — do not fetch them at seek time. Avoid `requestAnimationFrame` or a renderer's own animation loop as the source of truth for render-critical motion. **Always set an explicit duration on the composition root.** Unlike CSS/WAAPI/Lottie, the Three.js adapter has no duration auto-inference — it only forwards time via the seek mechanism, it doesn't inspect the scene for an animation clip's length. Without an explicit duration (and no GSAP timeline), the render engine has no way to know how long to capture and will fail with a "zero duration" error.

The adapter publishes the current time on a shared global variable and dispatches a custom "seek" event with the time in its detail payload on each seek.

**Basic pattern:**

```html
<canvas id="three-layer"></canvas>
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";

  const canvas = document.getElementById("three-layer");
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  // Match these to your composition's frame size.
  renderer.setSize(1920, 1080, false);
  renderer.setPixelRatio(1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1920 / 1080, 0.1, 100);
  camera.position.set(0, 0, 6);

  const mesh = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.4, 4),
    new THREE.MeshStandardMaterial({ color: 0x64d2ff, roughness: 0.38 }),
  );
  scene.add(mesh);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2));

  function renderAt(time) {
    mesh.rotation.y = time * 0.7;
    mesh.rotation.x = Math.sin(time * 0.6) * 0.16;
    renderer.render(scene, camera);
  }

  window.addEventListener("hf-seek", (event) => {
    renderAt(event.detail.time);
  });

  renderAt(window.__hfThreeTime || 0);
</script>
```

```css
#three-layer {
  width: 100%;
  height: 100%;
  display: block;
}
```

**Loading addons** (`GLTFLoader`, `OrbitControls`, etc.): use an import map so bare specifiers resolve. Both the inline `+esm` import and the import-map form work; pick whichever a given composition needs.

```html
<script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/"
    }
  }
</script>
<script type="module">
  import * as THREE from "three";
  import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
  import { OrbitControls } from "three/addons/controls/OrbitControls.js";
  // ...
</script>
```

Pin the `three` version in both entries to the same value — mixing versions across the import map and bare imports causes silent breakage.

**AnimationMixer pattern** for GLTF or authored clip animation — seek the mixer directly: `mixer.setTime(time)` inside the same render-at-time function above. If several mixers exist, seek all of them from the same `time`.

**Good uses:** deterministic 3D objects, product spins, particles with seeded data, and shader plates; camera moves derived purely from `time`; GLTF animation clips when assets are local and loaded before validation completes.

**Avoid:** using `Date.now()`, `performance.now()`, or clock deltas to update scene state; leaving render-critical work inside a free-running animation loop; loading remote models or textures at render time; device-pixel-ratio-dependent output (pin renderer size and pixel ratio for video renders); post-processing passes that depend on previous-frame history unless you can reconstruct state purely from time.

### Lottie / dotLottie

The render engine can seek both `lottie-web` and dotLottie players through its own Lottie runtime adapter. Lottie is a strong fit because the animation timeline is already encoded in the asset — the render engine only needs a player object it can seek.

**Contract:** load assets from local project files. Set `autoplay: false`. Prefer `loop: false` unless a loop is explicitly wanted. Register every returned animation or player on a shared global array. Keep the Lottie container dimensions stable with CSS. The adapter seeks `lottie-web` via `goToAndStop(timeMs, false)` and dotLottie via its own frame/percentage APIs depending on player shape.

**lottie-web pattern:**

```html
<div id="logo-lottie" class="lottie-layer"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<script>
  const anim = lottie.loadAnimation({
    container: document.getElementById("logo-lottie"),
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "assets/logo-reveal.json",
  });

  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(anim);
</script>
```

```css
.lottie-layer {
  width: 100%;
  height: 100%;
}
```

**dotLottie pattern:**

```html
<canvas id="product-lottie" class="lottie-canvas"></canvas>
<script src="https://unpkg.com/@lottiefiles/dotlottie-web"></script>
<script>
  const player = new DotLottie({
    canvas: document.getElementById("product-lottie"),
    src: "assets/product-flow.lottie",
    autoplay: false,
    loop: false,
  });

  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(player);
</script>
```

```css
.lottie-canvas {
  width: 100%;
  height: 100%;
  display: block;
}
```

**Multiple animations:** push each player into the same registry array; the render engine seeks them all to the same composition time.

**Composition duration inference:** a Lottie-only composition has no GSAP timeline object, so the runtime reads the registered animation's native length directly (total frames divided by frame rate for lottie-web, or the player's own duration property for dotLottie). An explicit duration attribute is optional as long as every animation is registered on the shared array — even when `loop: true` is set.

**Good uses:** After Effects exports already known to render correctly in lottie-web; logo reveals, icon loops, decorative accents, product-UI motion; porting Lottie usage from another framework into plain HTML.

**Avoid:** relying on remote path URLs at render time; starting playback with `play()`; assuming unsupported After Effects effects will survive export (test the JSON or `.lottie` file in a browser first); loading a player asynchronously and registering it after the composition has already been validated.

### Animate-Text (named text-animation effects)

A separate catalog of 24 named, deterministic text-animation effects (e.g. `typewriter` at an exact character-timing/stagger/easing spec) is maintained externally and referenced here as a vocabulary — the implementation specs (exact GSAP timings, easing strings, DOM split rules, stagger algorithms) live in that external catalog rather than being duplicated in this document. When a beat needs a deterministic, precisely-specified text animation and you have access to that catalog, load it and use the effect ID's exact spec. When you don't have access to it, or the beat's text animation is simple enough to describe in prose ("headline fades up word by word, 80ms stagger"), implement it inline using the per-word kinetic typography technique described earlier in this document, plus the broader motion-design principles throughout.

**Effect names (vocabulary only — see the per-character/per-word rules elsewhere in this document for implementable equivalents):**

- **Per-character (7):** soft-blur-in, per-character-rise, typewriter, bottom-up-letters, top-down-letters, stagger-from-center, stagger-from-edges
- **Per-word (8):** per-word-crossfade, spring-scale-in, shared-axis-y, blur-out-up, kinetic-center-build, short-slide-right, short-slide-down, depth-parallax-words
- **Per-line (2):** mask-reveal-up, line-by-line-slide
- **Whole element (7):** micro-scale-fade, shimmer-sweep, fade-through, shared-axis-z, scale-down-fade, focus-blur-resolve, shared-axis-x

Use this vocabulary when naming a text-animation choice in a plan or brief, and reach for a specific named effect when you want the SAME named effect reused consistently across multiple beats so they read as one coherent design system rather than one-off treatments, or when choosing between several similar effects (e.g. typewriter vs. per-character-rise vs. bottom-up-letters) and wanting to see all the options in one place.

## Animation Rules

These are atomic motion recipes — the building blocks. Compose 2–4 per scene on a single paused timeline.

**The shared contract every rule below assumes** (stated once here so individual rules don't repeat it):

- Runs on ONE **paused** GSAP timeline registered on the shared timeline registry — never autoplay, never a second competing timeline.
- Is **seek-safe in both directions**: use `fromTo` with explicit from-states (correct at t=0 under any seek; `immediateRender: false` when re-owning a target already touched by an earlier tween), absolute values — never relative `+=` tweens; state should be readable as a pure function of timeline time, never from a mutable tracker variable.
- Is **deterministic**: no `Math.random()`, no `Date.now()` — index-derived pseudo-random hashes and baked schedules only; finite repeats, never `repeat: -1`.
- Animates **transforms and paint-only properties** — `width`/`height`/`top`/`left` tweens are forbidden (use scale/translate proxies, masks, or the Anchored Layout Expand rule below).
- Caps group staggers so an arrival reads as one beat (roughly: item count × stagger ≤ about 0.5s).
- Puts **no CSS `transition`** on animated elements (they'd interpolate independently of seek and flicker) and hints the compositor with `will-change: transform` where many tweens run at once.
- Measures the DOM (`offsetHeight`, `getBoundingClientRect`) at build time only in a **single-scene** composition — in a multi-scene montage, later clips may not be laid out yet, so use authored CSS-matched constants instead.
- Lives inside a standard scene "clip" wrapper per the core composition contract (a class marking it as a timed clip, plus timing data attributes) — the recipes below show mechanism DOM only, not the full scene scaffold.

A rule's own "Critical Constraints" section (included with each rule below) lists only what is SPECIFIC to that rule beyond this shared contract.

### Text & Typography

#### Hacker Flip 3D Reveal

Character-level 3D rotation with deterministic glyph substitution — a "decryption" / airport flap-display reveal. Characters flip down from 90° in 3D while cycling through pseudo-random glyphs, then settle on the target character, so the eye catches the right letter just as the flip settles. Resolves to a short target word (typically a brand or label).

**How it works:** each character gets its own per-char tween from `rotateX: 90deg` (hidden, hinged at the bottom edge) to `0deg` (upright), staggered across the word. Below a reveal-threshold progress the char displays a seeded pseudo-random glyph that reshuffles every few frames; past the threshold, the real target character clicks into place. A hidden ghost copy of the full word reserves layout width so narrow flicker glyphs never shift the line.

```html
<div class="hacker-text-wrap" id="hacker-text" data-target="{phrase}">
  <!-- ghost row + per-char spans injected by the setup script -->
</div>
```

```css
/* the scene root (or nearest 3D ancestor) MUST set perspective: 1500px */
.hacker-text-wrap {
  font-family: {monoFont}; /* monospace so flicker glyphs hold width */
  font-weight: 900;
  font-size: HACKER_FONT_SIZE;
  position: relative; /* ghost stacks absolutely behind the live row */
}
.hacker-char {
  display: inline-block;
  transform-origin: bottom; /* flap-display hinge */
  transform-style: preserve-3d;
}
.hacker-ghost {
  opacity: 0;
  pointer-events: none;
  position: absolute;
  inset: 0 auto auto 0;
}
```

```js
const wrap = document.getElementById("hacker-text");
const targetWord = wrap.dataset.target;
const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";

// Ghost row (reserves width) + live per-char spans
const ghost = document.createElement("div");
ghost.className = "hacker-ghost";
ghost.textContent = targetWord;
wrap.appendChild(ghost);
const charEls = [...targetWord].map((ch) => {
  const span = document.createElement("span");
  span.className = "hacker-char";
  span.textContent = ch === " " ? " " : ch;
  span.dataset.target = ch;
  wrap.appendChild(span);
  return span;
});

// Index-seeded hash — same frame always yields the same glyph
function pseudoGlyph(seed) {
  const h = ((seed * 9301 + 49297) % 233280) / 233280;
  return GLYPHS[Math.floor(h * GLYPHS.length)];
}

charEls.forEach((el, i) => {
  const state = { p: 0 };
  tl.to(
    state,
    {
      p: 1,
      duration: FLIP_DURATION,
      ease: "power3.out",
      onUpdate: () => {
        if (state.p < REVEAL_THRESHOLD) {
          el.textContent = pseudoGlyph(i * 1000 + Math.floor(state.p * 100));
        } else {
          el.textContent = el.dataset.target === " " ? " " : el.dataset.target;
        }
        el.style.transform = `rotateX(${90 - state.p * 90}deg)`;
        el.style.opacity = Math.min(1, state.p * 2);
      },
    },
    i * CHAR_STAGGER,
  );
});
```

**Variations:** top-down hinge (`transform-origin: top` for a falling-flap look); center spin (`transform-origin: center` reads as a barrel roll, not a flap); number-only glyph pool for a price/countdown decode; two-pass decode chaining two flip-duration tweens with different glyph pools (symbols → letters → real) for a longer reveal.

**Values:** HACKER_FONT_SIZE 6–10% of viewport min-dimension (the flip IS the focal beat; ghost must match exactly). FLIP_DURATION 0.4–1.0s (under 0.4s the flicker phase has no time; over 1.0s drags). CHAR_STAGGER 0.03–0.08s (total decode = stagger × (chars−1) + flip duration — fit the phase budget). REVEAL_THRESHOLD 0.5–0.7 (lower reveals too early — no tension; higher reads as a hard end-reveal). FLICKER_RATE 3–6 frames per glyph swap (<3 looks like noise; >6 looks like discrete typing).

**Critical constraints:** `perspective` on the scene root is REQUIRED (without parent perspective, `rotateX` renders as a flat squash, not a 3D flip); `transform-style: preserve-3d` on each character. A ghost placeholder with identical content and font must back the live characters, or narrow glyphs shift the layout mid-flicker (monospace preferred). The flicker seed must be char index plus quantized progress — the same frame must always show the same glyph. Flicker rate should be at least ~3 frames per swap; per-char `onUpdate` work stays O(1). Center the flip dead-center with no decorative chrome (timestamp lines, tiny corner annotations) — the flip is the beat; a necessary secondary label should be big typography in the same stack, never a tiny corner annotation.

**See also:** the Card Morph Anchor rule (a flip reveals a phrase, a card morphs into the next shot); the Counting with Dynamic Scale rule (the numeric counterpart).

#### Vertical Spring Ticker (Slot Machine)

Slot-machine style vertical scrolling using additive spring physics within a masked container — each spring contributes one discrete "step" of scroll, producing a "click-click-click" rhythm with natural settling. Distinct from a continuous marquee, whose semantics are endless linear motion (see the Sine Wave Loop rule below for continuous-motion semantics).

**How it works:** a masked window of fixed height (`overflow: hidden`) holds a vertical stack of items, each exactly the window's height tall. Each spring holds a 0→1 progress; a shared `onUpdate` sums them and applies a `translateY` of `-sum × itemHeight`. Springs fire sequentially with overlap (step spacing ≤ step duration), so each step snaps in while the previous is still settling — that overlap is what makes them additive, and a `back.out` overshoot is what makes each step read as a "click."

```html
<div class="ticker" id="ticker">
  <div class="stack-inner" id="stack-inner">
    <div class="item">{item0}</div>
    <div class="item">{item1}</div>
    <div class="item">{itemN}</div>
  </div>
</div>
```

```css
.ticker {
  width: TICKER_WIDTH;
  height: ITEM_HEIGHT; /* MUST match .item height exactly */
  overflow: hidden; /* the mask is the window */
}
.stack-inner {
  display: flex;
  flex-direction: column; /* mandatory — vertical stacking */
}
.item {
  height: ITEM_HEIGHT; /* MUST equal .ticker height */
  display: flex;
  align-items: center;
  justify-content: center;
  /* font-variant-numeric: tabular-nums; — for numeric tickers */
}
```

```js
const innerEl = document.getElementById("stack-inner");
const springs = Array.from({ length: STEPS }, () => ({ p: 0 }));

function applyTransform() {
  const sumP = springs.reduce((acc, s) => acc + s.p, 0);
  innerEl.style.transform = `translateY(${-sumP * ITEM_HEIGHT}px)`;
}
applyTransform(); // initial state

springs.forEach((spring, i) => {
  tl.to(
    spring,
    {
      p: 1,
      duration: STEP_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
      onUpdate: applyTransform,
    },
    STEP_START + i * STEP_SPACING,
  );
});
```

**Variations:** numeric ticker (price/counter rolling) — items are the digit sequence, same spring-step pattern per decimal position, `tabular-nums` required. Reverse direction (countdown) — flip the translate sign and reverse item order. Pause between groups — several fast steps, a long pause, then one dramatic final step with a bigger bounce factor. Continuous infinite ticker is NOT this rule (this rule is discrete steps) — a looping news ticker is a single linear tween with duplicated items instead.

**Values:** ITEM_HEIGHT ≈ font-size × 1.25 (must hold capital descenders). TICKER_WIDTH 30–60% of viewport width. STEPS 1–4 (number of transitions, not items; STEPS ≤ itemCount − 1). STEP_DUR 0.3–0.7s (under 0.3s the overshoot is invisible; over 0.7s the click reads as a slide). STEP_SPACING 0.3–0.5s, MUST be ≤ STEP_DUR so springs overlap. BOUNCE_FACTOR 1.4–2.5 (1.4 gentle click, 2.0 firm, 2.5+ casino spin-and-land for a climax step).

**Critical constraints:** container height must equal item height pixel-exact, and all items equal height, or partial item edges show above/below the mask and drift accumulates across steps. `overflow: hidden` on the container, not the inner stack; `flex-direction: column` on the stack. Sum the springs in `onUpdate` — never tween the final position directly; each spring contributing its own snap is the slot-machine pacing. Overlap steps and keep `back.out` per step — non-overlapping steps or an out-only ease collapse into a linear scroll. Never update items via `innerHTML` between steps — the ticker moves the SAME items via translate; swapping content shows the previous item AS the new one. Hold the climax at least 1s after the final step. `tabular-nums` for numeric tickers.

**See also:** the Reactive Displacement rule (a ticker pushed by an incoming element); the Scale-Swap Transition rule (a ticker scales out after settling); the Press-Release Spring rule (a button press triggers the spin).

#### Counting with Dynamic Scale

A number counts from A to B while its transform scale grows to its final size — escalating visual weight ("this is impressive") without tweening `font-size` or forcing text layout on every frame. The final font size is static CSS; only the transform changes.

**How it works:** two synchronized tweens at the SAME timeline position with the SAME ease: (1) a proxy value rendered as text via `onUpdate` (rounded and locale-formatted), (2) the counter's transform scale from a start scale to 1, where the start scale equals the start display size divided by the end display size. A suffix (`%`, `×`, `+`) slides in AFTER the count lands — the number gets its own beat — and a label fades in early.

```html
<div class="counter-wrap">
  <span class="counter" id="counter">0</span><span class="counter-suffix">{suffix}</span>
</div>
<div class="counter-label">{label}</div>
```

```css
.counter-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  width: {counterContainerWidth}; /* fixed width — no layout shift as digit count changes */
}
.counter {
  font-variant-numeric: tabular-nums; /* MANDATORY — digits keep equal width */
  display: inline-block;
  font-size: {endSize}; /* final size is static; GSAP animates scale, not font-size */
  transform-origin: center center;
}
.counter-suffix {
  opacity: 0;
  transform: translateY(20px);
}
```

```js
const counter = document.getElementById("counter");
const state = { value: 0 };
const START_SCALE = START_SIZE / END_SIZE;

// Count value — onUpdate changes text only
tl.to(
  state,
  {
    value: TARGET_VALUE,
    duration: COUNT_DUR,
    ease: COUNT_EASE,
    onUpdate: () => {
      counter.textContent = Math.round(state.value).toLocaleString();
    },
  },
  0,
);

// Visual growth — compositor transform sharing the count's timing + ease
tl.fromTo(counter, { scale: START_SCALE }, { scale: 1, duration: COUNT_DUR, ease: COUNT_EASE }, 0);

// Suffix slides in AFTER the count completes
tl.to(
  ".counter-suffix",
  { opacity: 1, y: 0, duration: SUFFIX_DUR, ease: `back.out(${SUFFIX_BOUNCE_FACTOR})` },
  COUNT_DUR,
);

// Label fades in early
tl.from(".counter-label", { opacity: 0, y: 12, duration: LABEL_DUR, ease: "power2.out" }, LABEL_AT);
```

**Variations:** direct `innerText` tween without a proxy (GSAP can tween `innerText` directly for a number-only counter, using `snap: { innerText: 1 }`) — keep the proxy form when you need locale formatting or suffix logic; the scale tween stays separate either way. 3D depth entry adds a small negative-Z push-in, requiring `perspective` on the wrapper and `preserve-3d` on the counter. Multi-stat coordinated reveal — 3 stats counting in parallel share the SAME ease, duration, and start position so they finish together as a chord, not an arpeggio; each stat usually also wants a paired graphic (see the Stat Bars & Fills rule below).

**Values:** TARGET_VALUE ideally 2–3 digits (4+ digits needs a wider container and must fit at end size without clipping). START_SIZE/END_SIZE ratio roughly 40–60% (design inputs used once for the start scale; never tween either directly). COUNT_DUR 1.2–2.5s (below ~0.8s reads as a flash — the eye must read the digits scrolling past). COUNT_EASE `power2.out`/`power3.out` (default)/`expo.out` — shared by both the value and the scale; more `.out` means more dramatic deceleration at the peak. SUFFIX_DUR 0.3–0.6s, fires at the count's end, never during the count. SUFFIX_BOUNCE_FACTOR 1.4–2.0 (overshoot is fine on the suffix since it's punctuation, not data). LABEL_AT before the count's midpoint; LABEL_DUR 0.4–0.7s.

**Critical constraints:** `tabular-nums` is mandatory plus a fixed-width container as belt-and-suspenders — without them digit-count transitions (9 → 10 → 100) jitter as glyph widths change. Never set `fontSize` in `onUpdate` — final type size is static CSS, only the transform changes per frame; keep `onUpdate` O(1) (text only, no style writes or DOM creation). Use `Math.round`, not `Math.floor` — halfway through the final integer should already display the final value. Avoid `back.out`/`elastic.out` on the counter itself — overshoot makes the number look unstable; grow in place, don't bounce. The label should be big text, not a page-style caption — a tiny paragraph under a hero-size number reads as visual noise in video; display-size, uppercase, tracked.

**See also:** the Stat Bars & Fills rule (the paired graphic — give it the same ease/duration so number and fill land as one beat); the SVG Path Draw rule (icons drawing in around the number); the Center-Outward Expansion rule (icons bursting outward at the count peak).

#### Discrete Text Sequence

Instead of character-by-character typewriter, replace entire text states at time thresholds — enabling non-linear effects (typos, backspaces, bulk paste, "thinking" gaps) that smooth per-char typing can't achieve. If the effect is simply "type each character with no edits," this rule is overkill — use the smooth-slice variation below instead.

**How it works:** the typing is authored as a sparse array of `{ t, text }` states; on every `onUpdate` a reverse search finds the latest entry whose `t` has passed and renders its text. Display jumps between states with no animation between them — realism comes from the schedule shape: fast keystroke clusters (0.06–0.20s apart), pauses at word breaks (0.3–0.6s), a typo, backspaces peeling back to the fork, then a bulk paste replacing many characters in one entry. A block cursor blinks via a deterministic sine square wave on the same timeline.

```html
<div class="terminal">
  <div class="prompt">$</div>
  <div class="text-wrap">
    <span class="text" id="text"></span><span class="cursor" id="cursor">_</span>
  </div>
</div>
```

```css
.terminal {
  font-family: {monoFont}; /* monospace required — proportional jitters even in a fixed box */
  display: flex;
  align-items: baseline;
  font-size: TERMINAL_FONT_SIZE;
}
.text-wrap {
  display: inline-flex;
  align-items: baseline;
  min-width: TEXT_WRAP_MIN_WIDTH; /* ≥ widest state — stops right-edge jitter */
  white-space: nowrap;
}
.cursor {
  display: inline-block; /* inline ignores width */
  width: CURSOR_WIDTH;
}
```

```js
// Each entry shows from its t until the NEXT entry's t.
// Shape: keystrokes → typo → backspace to the fork → bulk paste → completion mark.
const SEQUENCE = [
  { t: 0.0, text: "" },
  { t: T_K1, text: "{p1}" }, // first keystrokes (~3-5 chars, 0.1-0.2s apart)
  { t: T_K2, text: "{p1 + ' ' + p2_typo}" }, // continuation containing a typo
  { t: T_BS, text: "{p1 + ' ' + p2_partial}" }, // backspace(s) — peel back to the fork
  { t: T_BULK, text: "{fullCorrectedText}" }, // bulk paste — many chars in one jump
  { t: T_DONE, text: "{fullCorrectedText + ' ✓'}" }, // completion marker
];

// Reverse-search for the latest entry whose t has passed
function textAt(time) {
  for (let i = SEQUENCE.length - 1; i >= 0; i--) {
    if (time >= SEQUENCE[i].t) return SEQUENCE[i].text;
  }
  return "";
}

const textEl = document.getElementById("text");
const cursorEl = document.getElementById("cursor");

const driver = { t: 0 };
tl.to(
  driver,
  {
    t: TOTAL_DURATION,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      textEl.textContent = textAt(driver.t);
    },
  },
  0,
);

// Cursor blink — deterministic sin square wave, never a CSS animation
const blink = { p: 0 };
tl.to(
  blink,
  {
    p: Math.PI * 2 * BLINK_CYCLES,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
    },
  },
  0,
);
```

**Variations — smooth character slice** (continuous typewriter with no pauses or edits — faster to author but uniformly "machine-typed"):

```js
const fullText = "{fullPhrase}";
const len = { v: 0 };
tl.to(
  len,
  {
    v: fullText.length,
    duration: TYPE_DUR,
    ease: "power1.inOut",
    onUpdate: () => {
      textEl.textContent = fullText.substring(0, Math.floor(len.v));
    },
  },
  0,
);
```

Other variations: a thinking pause simply holds one state for 0.8–2.0s (under 0.5s reads as a stutter, not thought) by leaving a gap before the next entry's time. A completion pulse can scale the text 1.03–1.08 with a yoyo when the final state lands. Per-state color shift can branch on the driver's time vs. milestones (success color after the done marker, dim mid-edit).

**Values:** TERMINAL_FONT_SIZE 48–96px for full-bleed comps, smaller for terminal-style detail. TEXT_WRAP_MIN_WIDTH must be ≥ the widest state (measure with a hidden probe after fonts have loaded if unsure). Milestone times: keystrokes 0.06–0.20s apart, pauses 0.3–0.6s, monotonically increasing, the done marker at least ~1s before the composition ends for climax dwell. TYPE_DUR (smooth variant) roughly chars × 0.06–0.12s, fast to relaxed. BLINK_CYCLES one cycle per 0.5–0.8s of total duration. CURSOR_WIDTH about 0.3× font size.

**Critical constraints:** reverse-search the array each frame — O(n) with small n (≤30 typical); never index by frame since the sequence is sparse. A `min-width` on the text wrap is mandatory, or the right edge jitters as state length changes. Discrete jumps must be INSTANT — any transition on the text turns the jump into a smear and kills the "typing" feel. Cursor blink is sine/sequence-driven on the timeline, `display: inline-block`, monospace font, `white-space: nowrap` (wrapping mid-state breaks the illusion; trailing spaces must survive). Use discrete only for non-linear states (typos, pauses, bulk paste) — plain typing should take the smooth-slice variation.

**See also:** the Context-Sensitive Cursor rule (same SEQUENCE pattern plus segment-colored cursor); the 3D Text Depth Layers rule (discrete text with layered depth); the Counting with Dynamic Scale rule (a discrete label beside a smooth counter); the Press-Release Spring rule (a post-completion press beat).

#### ASR Keyword Glow

Words in a phrase visually activate (glow blur plus scale) when "spoken," following an attack-sustain-release envelope over per-word start/end timestamps. In a real audio-transcript pipeline the timings come from a word-level transcript; for a promotional video, hand-author them to control emphasis pacing. The envelope never falls to zero after a word — it decays to a rest level, leaving a breadcrumb of recent emphasis.

**How it works:** a single linear driver tween (`ease: "none"` — any other ease distorts the per-word envelope, so do not change it) sweeps scene time; its `onUpdate` loops over ALL words computing each one's envelope: 0 before start, linear attack to 1 over the attack duration, sustain at 1 until end, decay to a rest level over the release window, then hold at rest. The envelope drives `text-shadow` blur and `scale` — one driver for the whole phrase, never one tween per word (60+ words would bloat the timeline).

```html
<div class="phrase">
  <span class="word" data-word="{w1Key}">{w1}</span>
  <span class="word" data-word="{w2Key}">{w2}</span>
  <!-- … the final word may be the brand, with the .brand modifier -->
  <span class="word brand" data-word="{brandKey}">{brandWord}</span>
</div>
```

```css
.phrase {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  color: {restColor};
}
.word {
  display: inline-block; /* required for transform on <span> */
  transform-origin: 50% 50%;
  text-shadow: 0 0 0 {glowColorTransparent};
}
.word.brand {
  color: {brandAccentColor};
}
```

```js
// Per-word spoken windows — one entry per span; brand word 1.5-2× a normal word's window.
const TIMINGS = {
  // {w1Key}: { start: …, end: … },  — seconds, local to the scene
};

function envelope(time, start, end) {
  if (time < start) return 0;
  if (time < end) return Math.min((time - start) / ATTACK_DUR, 1);
  const releaseEnd = end + RELEASE;
  if (time < releaseEnd) return 1 - ((time - end) / RELEASE) * (1 - REST_LEVEL);
  return REST_LEVEL;
}

const words = document.querySelectorAll(".word");
const driver = { t: 0 };
tl.to(
  driver,
  {
    t: SCENE_DURATION,
    duration: SCENE_DURATION,
    ease: "none", // linear — t maps 1:1 to scene time
    onUpdate: () => {
      words.forEach((el) => {
        const timing = TIMINGS[el.dataset.word];
        if (!timing) return;
        const env = envelope(driver.t, timing.start, timing.end);
        el.style.textShadow = `0 0 ${MAX_BLUR * env}px ${glowColorRgba(env)}`;
        el.style.transform = `scale(${1 + MAX_SCALE_BOOST * env})`;
      });
    },
  },
  0,
);
```

**Variations:** a karaoke style — the default amplitudes read too subtle in video, so render inactive words dim and lerp the active word toward bright + larger, with at most 1–2 words bright at any moment; recommended for short phrases (5–10 words) where one word at a time should pop, keeping the subtle default for long dense text. A multi-octave glow multiplies the sustain by a slow sine to make high-emphasis words breathe at peak. A color shift on the peak lerps from the rest color to a peak color as the envelope rises. A 3D pop-out adds a `translateZ` proportional to the envelope so the spoken word leans toward camera (requires `perspective` on the parent). From real ASR transcripts, convert `{ word, start_ms, end_ms }` entries to seconds and feed them in identically.

**Values:** ATTACK_DUR 0.1–0.25s (must be less than the shortest word's window or it never reaches 1). RELEASE 0.2–0.5s. REST_LEVEL 0.15–0.4 default (0.05–0.2 for karaoke) — must stay above 0 (breadcrumb) and below 1. MAX_BLUR 15–25px default (30–45px karaoke) — bigger reads as "shouting." MAX_SCALE_BOOST 0.03–0.10 additive at peak (karaoke 0.15–0.25). SCENE_DURATION should equal the composition's own duration so the driver ends in sync with the seek window.

**Critical constraints:** timings must be monotonic and non-overlapping — every entry's end must precede the next entry's start, or the envelope becomes ambiguous. The brand word's window should be 1.5–2× a normal word's — let it sustain since it's the headline. The driver ease must stay `"none"` — any other ease warps every word's envelope timing. Use `text-shadow`, not `box-shadow` — the glow must hug the glyph, not the inline-block rectangle. Use one driver looping all words, never one tween per word. Commit to a style — values between the default and karaoke columns yield awkward "half-loud" emphasis. Climax dwell should be at least 1s after the final word's emphasis, since the last word IS the headline beat.

**See also:** the 3D Text Depth Layers rule (depth on the active word at peak); the Sine Wave Loop rule (idle breathe between emphasis moments); the Context-Sensitive Cursor rule (typewriter matching the ASR cadence).

#### 3D Text Depth Layers

The same text rendered N times at increasing offsets — back layers translucent, front layer full opacity and brand color — creates a physical "stacked extrusion" depth illusion on large typography. Distinct from `text-shadow` (which can't have per-layer hue/opacity/animation): each layer is a real DOM element.

**How it works:** a build script appends a fixed layer count of copies back-to-front; each back layer sits at a translate offset of `i × offsetX`, `i × offsetY` with alpha stepping down per layer, while the front copy (index 0) is `position: relative` so it defines the container size (back layers stack absolutely behind it). The default entrance cascades the layers' fades back-to-front while a proxy tween grows the offsets from 0 to full, so the depth "builds forward" and lands as the last layer fades in.

```html
<div class="depth-stack">
  <!-- layers injected by script — LAYER_COUNT copies of {label} -->
</div>
```

```css
.depth-stack {
  position: relative; /* front layer defines size; back layers stack behind */
}
.depth-text {
  font-weight: 900; /* black weight — thin text loses the illusion */
  font-size: HERO_FONT_SIZE;
  letter-spacing: HERO_LETTER_SPACING;
  line-height: 1;
  color: {frontColor};
}
.depth-text.is-back {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none; /* decorative */
}
.depth-text.is-front {
  position: relative;
  z-index: 10;
}
```

```js
const stack = document.querySelector(".depth-stack");

// Build back-to-front so the FRONT (i=0) is appended LAST
for (let i = LAYER_COUNT - 1; i >= 0; i--) {
  const el = document.createElement("div");
  el.className = "depth-text " + (i === 0 ? "is-front" : "is-back");
  el.textContent = "{label}";
  if (i > 0) {
    const alpha = Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
    el.style.color = `rgba({backHueRGB}, ${alpha})`; // rgba in color, NOT element opacity
    el.style.transform = `translate(${i * OFFSET_X}px, ${i * OFFSET_Y}px)`;
  }
  el.dataset.layer = String(i);
  stack.appendChild(el);
}

// Cascade entry — back layers fade in first, building forward
stack.querySelectorAll(".depth-text").forEach((el) => {
  const i = Number(el.dataset.layer);
  const finalAlpha = i === 0 ? 1 : Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
  tl.fromTo(
    el,
    { opacity: 0 },
    { opacity: finalAlpha, duration: LAYER_FADE_DUR, ease: "power2.out" },
    LAYER_CASCADE_START + (LAYER_COUNT - 1 - i) * LAYER_CASCADE_STEP,
  );
});

// Depth grows on entry — offsets interpolate 0 → full
const depthState = { p: 0 };
tl.to(
  depthState,
  {
    p: 1,
    duration: DEPTH_GROW_DUR,
    ease: "power2.out",
    onUpdate: () => {
      stack.querySelectorAll(".depth-text.is-back").forEach((el) => {
        const i = Number(el.dataset.layer);
        el.style.transform = `translate(${i * OFFSET_X * depthState.p}px, ${i * OFFSET_Y * depthState.p}px)`;
      });
    },
  },
  LAYER_CASCADE_START, // align with the cascade so depth lands as the last layer fades in
);
```

**Variations:** a static depth (single hero shot) renders all layers at final positions from t=0, optionally fading the whole stack in with a subtle scale from ~0.94–0.98 to 1 over 0.5–0.8s. A dynamic depth pulse modulates the offsets with a sine multiplier after the grow completes, one beat per 0.7–1.5s reading as a heartbeat. A color-shift on back layers steps hue/lightness per layer instead of fading to translucent, so depth reads as a colored cast shadow.

**Values:** LAYER_COUNT 4–6 (fewer doesn't read as 3D, more clutters on tight kerning). OFFSET_X/OFFSET_Y 1–3px each (beyond ~4px reads as glitch/chromatic aberration, not depth). BACK_ALPHA_MAX 0.6–0.85 for the nearest back layer. BACK_ALPHA_STEP 0.08–0.15. BACK_ALPHA_MIN 0.1–0.2 (below 0.1 the deepest layer vanishes on dark backgrounds). HERO_FONT_SIZE 60px minimum, 200–340px for a hero. HERO_LETTER_SPACING −0.03em to 0 (tighter makes offsets read as depth, not repetition). LAYER_CASCADE_STEP 0.04–0.10s. LAYER_FADE_DUR 0.3–0.6s. DEPTH_GROW_DUR 0.4–0.8s.

**Critical constraints:** offset direction implies light direction — pick one sign convention for the whole composition. Back layers should be translucent or darker, never more saturated than the front (a more-saturated back layer reads as a halo, not depth). Set back-layer color via `rgba()` in `color`, not element `opacity` — opacity fades the whole rendered glyph including any shadow. The front layer's `position: relative` defines the container size; back layers are absolute with `pointer-events: none`, offsets via `transform: translate()`, never `top`/`left`. Do not layer CSS `text-shadow` alongside layered depth — they compound and over-extrude. Do not stack per-letter animation on top of the depth stack — combining, say, hacker-flip character decoding with a 6-layer depth stack is chaos; drop to 2–3 layers or apply depth only to the static post-reveal state.

**See also:** the Counting with Dynamic Scale rule (a counter rendered with depth layers); the Sine Wave Loop rule (idle breathing on the front layer post-reveal); the Center-Outward Expansion rule (a depth-stacked wordmark after the burst lands).

#### Context-Sensitive Cursor

In a typewriter sequence, the cursor's color (and optionally height/blink behavior) matches the active text segment — brand accent while typing the brand name, dim on placeholders, success color on the completion mark. The eye lands on the keyword being typed because the cursor shifts with it. Layers on top of the Discrete Text Sequence rule's `SEQUENCE` pattern above.

**How it works:** the text is authored as a `SEQUENCE` of `{ t, text, segment, color }` entries; a linear driver's `onUpdate` reverse-searches for the current entry and writes both the visible text and the cursor's `background` (the cursor is a colored block, so `background`, NOT `color`). A second linear tween sweeps a phase through `2π × BLINK_CYCLES_PER_SCENE` and gates cursor opacity on `sin(phase) > 0` — a deterministic square-wave blink on the timeline.

```html
<div class="terminal">
  <div class="prompt">$</div>
  <div class="text-wrap">
    <span class="text" id="text"></span><span class="cursor" id="cursor">_</span>
  </div>
</div>
```

```css
.terminal {
  font-family: {monoFont}; /* proportional fonts drift the cursor mid-segment */
  display: flex;
  align-items: baseline;
  white-space: pre; /* preserve trailing spaces — cursor sits at segment end */
}
.text {
  white-space: pre;
}
.cursor {
  display: inline-block; /* inline ignores width/height */
  width: {cursorWidth}px;
  height: {cursorHeight}px;
  background: {textColor}; /* default — overridden per segment in onUpdate */
  vertical-align: {cursorBaselineFix}px; /* small negative — anchor to baseline, not line-height */
}
```

```js
// Adjacent entries usually share a text prefix but may differ in `segment` —
// that's what shifts the cursor color mid-line.
const SEQUENCE = [
  { t: 0, text: "", segment: "main", color: "{mainColor}" },
  { t: T_LEADIN_END, text: "{leadInChunk}", segment: "main", color: "{mainColor}" },
  { t: T_BRAND_IN, text: "{leadInBrandPrefix}", segment: "brand", color: "{brandColor}" },
  { t: T_BRAND_OUT, text: "{leadInBrandFull}", segment: "main", color: "{mainColor}" },
  { t: T_CMD_IN, text: "{leadInCmdPrefix}", segment: "cmd", color: "{cmdColor}" },
  { t: T_SUCCESS, text: "{leadInDone}", segment: "success", color: "{successColor}" },
];

function entryAt(time) {
  for (let i = SEQUENCE.length - 1; i >= 0; i--) {
    if (time >= SEQUENCE[i].t) return SEQUENCE[i];
  }
  return SEQUENCE[0];
}

const textEl = document.getElementById("text");
const cursorEl = document.getElementById("cursor");

const driver = { t: 0 };
tl.to(
  driver,
  {
    t: DURATION,
    duration: DURATION,
    ease: "none",
    onUpdate: () => {
      const entry = entryAt(driver.t);
      textEl.textContent = entry.text;
      cursorEl.style.background = entry.color;
    },
  },
  0,
);

// Deterministic square-wave blink
const blink = { p: 0 };
tl.to(
  blink,
  {
    p: Math.PI * 2 * BLINK_CYCLES_PER_SCENE,
    duration: DURATION,
    ease: "none",
    onUpdate: () => {
      cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
    },
  },
  0,
);
```

**Variations:** non-blinking during active typing (solid cursor while letters are appearing, resuming blink on idle) — this MUST be a pure function of the driver's time; tracking a mutable "last change time" in `onUpdate` is not reverse-seek-safe. Bake the change times from `SEQUENCE` instead — every entry whose text differs from its predecessor is a typing event, computed once at build time as a `CHANGE_TIMES` array, and read in `onUpdate` via `CHANGE_TIMES.some((t) => t <= driver.t && driver.t - t < TYPING_GRACE)`. Cursor height can shift on segment (a larger cursor on a brand segment, 1.1–1.25×). A contrast reversal (dark text on light needing a dark cursor) should keep `entry.color` as the single source of truth.

**Values:** DURATION 4–8s per typed line. Entry `t` spacing 0.2–0.5s for micro-additions, ascending and non-uniform, slowing down on highlights. Segment palette 3–4 colors max. cursorWidth/Height 8–24px / 0.85–1.0× font size (too thin vanishes in render compression, too tall outranks the text). BLINK_CYCLES_PER_SCENE period ≈0.6–1.2s and MUST be a whole number, or the sine sweep ends mid-cycle and the cursor pops on the last frame. TYPING_GRACE 0.15–0.3s, must be less than the shortest dwell between adjacent entries or the cursor never blinks.

**Critical constraints:** cursor color goes on `background` since it's a colored block, not a glyph. Blink is timeline-driven sine, pure of any mutable tracker (see the non-blinking-while-typing variation for the seek-safe form). `white-space: pre` on the text and container — collapsed trailing spaces park the cursor in the wrong column. Monospace font plus `display: inline-block` cursor — proportional faces drift the cursor mid-segment. BLINK_CYCLES_PER_SCENE must be a whole number for the fixed duration.

**See also:** the Discrete Text Sequence rule (the underlying SEQUENCE pattern); the Camera-Cursor Tracking rule (camera follows the cursor); the Press-Release Spring rule (post-typing confirm press).

#### Dynamic Content Sequencing

A utility pattern (not itself a motion rule) for scenes that show a SEQUENCE of items (cards, phrases, stats): each item's duration is computed from its content length plus per-item config, and the sequencer assigns absolute start/end times automatically — no hardcoded offsets per item. Distinct from Discrete Text Sequence (one text element changing states) — this rule swaps between distinct content blocks.

**How it works:** a content array of `{ eyebrow, title, body, speedFactor, hold }` entries is reduced once at build time into a flat `TIMELINE` of `{ …entry, start, end }` — duration per entry is a base duration plus (body length × seconds-per-char) plus hold, so longer text earns more reading time. A single linear driver's `onUpdate` reverse-searches the active entry and swaps the DOM only on transitions (a "last title" guard — per-frame `textContent` writes flicker in render); an optional progress bar fills 0→100% across the whole run.

```html
<div class="display">
  <div class="eyebrow" id="eyebrow"></div>
  <div class="title" id="title"></div>
  <div class="body" id="body"></div>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
</div>
```

```css
.body {
  min-height: 160px; /* reserve space — content height varies; without this, layout jumps */
}
.progress-fill {
  height: 100%;
  width: 0%;
}
```

```js
// N entries, each with its own pacing (optionally a speedFactor multiplier);
// the final entry uses a larger hold (closing beat).
const CONTENT = [
  { eyebrow: "{eyebrow1}", title: "{title1}", body: "{body1}", hold: HOLD_MID },
  // …
  { eyebrow: "{eyebrowN}", title: "{titleN}", body: "{bodyN}", hold: HOLD_FINAL },
];

// Pre-compute absolute start/end ONCE — never in onUpdate.
let cumulative = 0;
const TIMELINE = CONTENT.map((entry) => {
  const dur = BASE_DURATION + entry.body.length * SEC_PER_CHAR + entry.hold;
  const start = cumulative;
  cumulative += dur;
  return { ...entry, start, end: cumulative };
});

function entryAt(time) {
  for (let i = TIMELINE.length - 1; i >= 0; i--) {
    if (time >= TIMELINE[i].start) return TIMELINE[i];
  }
  return TIMELINE[0];
}

const eyebrowEl = document.getElementById("eyebrow");
const titleEl = document.getElementById("title");
const bodyEl = document.getElementById("body");
const progressEl = document.getElementById("progress-fill");

const TOTAL_DURATION = cumulative + TAIL_PAD;
const driver = { t: 0 };
let lastTitle = "";

tl.to(
  driver,
  {
    t: TOTAL_DURATION,
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      const entry = entryAt(driver.t);
      // Swap content only on transitions — no per-frame DOM thrash
      if (entry.title !== lastTitle) {
        eyebrowEl.textContent = entry.eyebrow;
        titleEl.textContent = entry.title;
        bodyEl.textContent = entry.body;
        lastTitle = entry.title;
      }
      progressEl.style.width = `${(driver.t / TOTAL_DURATION) * 100}%`;
    },
  },
  0,
);
```

**Variations:** a crossfade between items returns BOTH adjacent entries during an overlap window (a small overlap constant on each side) and renders them with opacities computed from distance to the boundary. Per-item motion variation maps an `entry.style` key to a different rule per chapter (e.g. 3D Text Depth Layers → Hacker Flip 3D → Counting with Dynamic Scale) — the sequencer only orchestrates timing. Auto-extending composition duration from the computed total is possible in script, but a composition's duration is normally read at load time and setting it after init may not take effect, so author the duration manually from a rough total instead.

**Accelerating cadence (geometric hold decay)** — for rhetorical escalation ("everyone says…", a roll-call, a praise flurry), the beat grid itself accelerates: early entries hold ~1s (read speed), then windows shrink geometrically into a ~0.15–0.3s flurry, braking on an emphasis state before the resolve. The acceleration is pre-computed into the same flat `TIMELINE` — still content-driven, still deterministic, no speed-up tween anywhere:

```js
// Geometric decay on the hold, clamped at a flurry floor; the brake state holds longest.
const HOLDS = CONTENT.map((entry, i) => Math.max(FLURRY_FLOOR, HOLD_START * Math.pow(DECAY, i)));
HOLDS[CONTENT.length - 1] = HOLD_FINAL;

let cumulative = 0;
const TIMELINE = CONTENT.map((entry, i) => {
  // Past ~0.5s states are glanced as motion texture, not read —
  // drop the per-char term or you never reach flurry speed.
  const readable = HOLDS[i] >= READ_THRESHOLD;
  const dur = HOLDS[i] + (readable ? entry.body.length * SEC_PER_CHAR : 0);
  const start = cumulative;
  cumulative += dur;
  return { ...entry, start, end: cumulative };
});
```

Worked example — a "praise-chip flurry": ~16 short quotes hard-cut through a chip beside a pinned wordmark. The first 3 states hold at ~1.0s each (each reads fully); a decay factor of ~0.8 shrinks every following window until a flurry floor of ~0.2s catches it (roughly 12 states over ~2.5s — a churn of acclaim, individually glanced); the longest phrase takes ~1.6s as the brake before the closing lockup. Values: HOLD_START 0.8–1.2s; DECAY 0.75–0.88 (higher = longer runway before the flurry bites); FLURRY_FLOOR 0.15–0.3s (below ~0.15s swaps to strobe); READ_THRESHOLD ~0.5s; brake ≥4× the floor or the stop doesn't register as a beat. The usual 3–6 entry guidance relaxes here — 12–18 states are legal precisely because flurry states aren't individually read.

**Values:** BASE_DURATION 0.6–1.5s minimum per entry regardless of length. SEC_PER_CHAR 0.03–0.06 s/char (≈17–33 chars/sec, uniform across the sequence so the pace reads as one engine). HOLD_MID 0.5–1.0s, less than HOLD_FINAL. HOLD_FINAL 1.0–2.0s (climax dwell, must exceed HOLD_MID by a clear margin). SPEED_FACTOR 0.5–2.0 (default 1.0), per-entry only. TAIL_PAD 0.0–1.0s (a quiet beat after the last entry — prefer 0 when the next composition owns the breath). CONTENT N: 3–6 entries (the accelerating-cadence variation relaxes this).

**Critical constraints:** pre-compute the TIMELINE once at build — never recompute in `onUpdate`, the reverse search over the flat array is the whole per-frame cost. DOM swap only on entry transition (a title/key guard) — per-frame `textContent` assignment flickers in render. A `min-height` on the body element prevents downstream elements (progress bar, brand) from jittering as content height varies. Sequential only — for parallel tracks use a different reduction. Titles must fit one line at the chosen size; bodies must fit inside `min-height` after wrapping.

**See also:** the Discrete Text Sequence rule (per-entry typewriter on the body); the Context-Sensitive Cursor rule (cursor color per chapter); the Vertical Spring Ticker rule (animated word swap instead of hard cut); the Scale-Swap Transition rule (visual morph between entries).

#### Kinetic Beat Slam

Percussive kinetic typography — short phrases slam in one at a time on a steady beat, each with a DIFFERENT entrance, then stack into a locked finale. The recipe for "punchy/rhythmic" text-forward pieces (taglines, manifestos, hype intros). What separates rhythmic from generic: (1) one shared onset array driving every element, (2) distinct entrances per phrase rather than one reused helper, and (3) optional rhythm chrome (metronome ticks, a beat bar) that visibly keeps the beat.

**How it works:** a single tempo grid — a pulse duration in seconds, and a set of beat times on that grid — is the rhythmic spine; every phrase entrance, accent, and chrome tick reads its time from it, so the piece locks to one pulse instead of drifting hand-tuned offsets. Each phrase gets a different transform axis (scale+blur slam / side snap / rise+rotate) with short attacks (0.35–0.6s on the hit), then the stack holds with a finite low-amplitude breath.

```html
<div class="kbs-stage">
  <div class="kbs-line" id="p1"><span class="verb">Notice</span> more.</div>
  <div class="kbs-line" id="p2"><span class="verb">Decide</span> faster.</div>
  <div class="kbs-line" id="p3"><span class="verb">Act</span> now.</div>
</div>
<!-- optional rhythm chrome -->
<div class="kbs-metronome" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
```

```css
.kbs-stage {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 120px 160px; /* title-safe margin */
}
.kbs-line {
  font-family: "Archivo Black", "League Gothic", sans-serif; /* embedded display face */
  font-size: 150px;
  line-height: 0.96;
  letter-spacing: -0.03em;
  color: #f5f5f5;
}
.kbs-line .verb {
  color: #ff5b2e; /* exactly one accent hue */
}
.kbs-metronome {
  position: absolute;
  bottom: 64px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 14px;
}
.kbs-metronome i {
  width: 6px;
  height: 28px;
  background: #ff5b2e;
  opacity: 0.25;
}
```

```js
// ONE tempo grid drives everything — phrases AND the metronome read it.
const PULSE = 0.4; // seconds per sub-beat
const BEATS = [PULSE * 1, PULSE * 5, PULSE * 9]; // phrase onsets, on the grid

// Distinct entrances per phrase (NOT one reused helper).
tl.fromTo(
  "#p1",
  { scale: 1.5, filter: "blur(16px)", opacity: 0 },
  { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "power4.out" },
  BEATS[0],
);
tl.fromTo(
  "#p2",
  { x: -320, opacity: 0 },
  { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" },
  BEATS[1],
);
tl.fromTo(
  "#p3",
  { y: 90, rotation: 6, opacity: 0 },
  { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "circ.out" },
  BEATS[2],
);

// Rhythm chrome: each tick flashes on the SAME grid, not a magic offset.
gsap.utils.toArray(".kbs-metronome i").forEach((tick, i) => {
  tl.to(tick, { opacity: 1, duration: 0.08, yoyo: true, repeat: 1, ease: "none" }, PULSE * (i + 1));
});

// Finale hold: floor (not ceil) so the repeat never overshoots the composition duration;
// max(0,…) so a short hold never yields a negative repeat (GSAP reads negative as -1 = infinite).
const holdStart = BEATS[2] + 0.7,
  cycle = 1.6,
  holdDur = SCENE_DURATION - holdStart;
tl.to(
  ".kbs-stage",
  {
    scale: 1.01,
    duration: cycle / 2,
    ease: "sine.inOut",
    yoyo: true,
    repeat: Math.max(0, Math.floor(holdDur / cycle) - 1),
  },
  holdStart,
);
```

**Variations:** entrance easing by attack character — `power4.out` as the hard-slam default hit, `expo.out` for the hardest snap (side-snaps, whip-ins), `back.out(2)` for an overshoot pop (accents only, never body words), `circ.out` for a heavy rise with momentum; use at least 3 distinct easings across the piece. Rhythm chrome alternatives — a center beat bar or a monospace label tag pulsing on-beat instead of the metronome ticks. Finale dressing — stack an accent underline sweep (see the CSS Marker Patterns rule below); don't just leave the last phrase sitting.

**Values:** BEATS spacing 1.2–1.8s (under 0.8s is frantic, over 2.5s loses the pulse; keep spacing even — it's a beat). Entrance duration 0.35–0.6s (the hit must resolve before the next beat; exits ≤0.25s). Exactly one accent hue for the verbs; the rest mono white/near-black. Display face 150px+, heavy weight.

**Critical constraints:** one beat array, not scattered offsets — every element times off the shared `BEATS`/`PULSE` values; this is the single biggest lever for "rhythmic." A different entrance per phrase — a reused single entrance helper for all lines is the flat-but-competent tell; vary the motion axis, reuse the ease family. Finale repeat math: use `Math.max(0, Math.floor(dur / cycle) - 1)` — `Math.ceil` overshoots the composition duration, and a negative repeat is read by GSAP as infinite. No banned exit animations between scenes in a montage — the transition IS the exit; only a final scene may fade out. The display font must be genuinely embedded/available, or it silently falls back at render.

**See also:** the 3D Text Depth Layers rule (extruded depth on the slammed words); the CSS Marker Patterns rule (finale underline/circle); the Sine Wave Loop rule (the finale breath).

#### Gradient Text Sweep

A gradient tweened THROUGH letterforms — `background-clip: text` plus an oversized-background `backgroundPosition` tween. Continuous sweep across a held headline, a traveling word-to-word highlight (stacked-copy opacity envelopes), or a hue-sweep that settles to a solid via a pixel-identical twin crossfade. Glyphs never move; the effect is finite and seek-safe.

Boundaries: the ASR Keyword Glow rule above is word-timed emphasis railed to audio timestamps — this rule is a design beat with no audio rail. The Ambient Glow Bloom rule's traveling sweep is a sheen riding over a surface; here the gradient is masked into the type itself. The CSS Marker Patterns rule draws accents around text, never fills.

**How it works:** the text carries a gradient background wider than its own box (e.g. `background-size: 300% 100%`) clipped into the glyphs, so tweening `backgroundPosition` slides the gradient through the visible letterforms. Two gotchas own this rule: `background-position` percentages only produce travel when `background-size` exceeds 100% (at 100% the image is pinned and the tween is a silent no-op); and the percent axis runs opposite to the perceived travel (tweening from `"100% 50%"` to `"0% 50%"` moves the highlight left-to-right through the text).

1. **Continuous sweep** (held title card) — one long **linear** `backgroundPosition` tween spanning the hold, with matching first and last color stops so the travel has no visible seam and reads as endless while remaining a single finite tween.
2. **Word-to-word highlight** — each word is two pixel-identical stacked copies: a base copy in the resting color and a gradient-clipped copy at zero opacity. A per-word opacity envelope (rise, then fall as the next word rises) passes the highlight along on an index-derived stagger — an envelope, not a moving mask; no per-word position measurement.
3. **Hue-sweep → solid** — the gradient holds position while a `filter: hue-rotate()` tween sweeps its hues; the settle is a stacked-copy crossfade to a solid twin, never a color-stop tween (gradients with different stops don't interpolate reliably).

```html
<!-- Forms A/C: gradient headline; solid twin behind for the Form C settle -->
<div class="headline-stack">
  <h1 class="headline solid-twin">{headlineText}</h1>
  <h1 class="headline gradient-fill" id="headline">{headlineText}</h1>
</div>

<!-- Form B: per-word stacked copies -->
<p class="line">
  <span class="word"><span class="w-base">{word1}</span><span class="w-hot">{word1}</span></span>
  <span class="word"><span class="w-base">{word2}</span><span class="w-hot">{word2}</span></span>
</p>
```

```css
.headline-stack,
.word {
  display: grid; /* twins share one cell — pixel-identical boxes */
}
.headline,
.w-base,
.w-hot {
  grid-area: 1 / 1;
}
.gradient-fill,
.w-hot {
  background-image: {gradient}; /* {sweepGradient} A/C, {highlightGradient} B */
  background-size: SWEEP_SPAN 100%; /* MUST exceed 100% or the position tween is dead */
  background-position: 100% 50%; /* start; tween toward 0% for left→right travel */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.solid-twin {
  color: {settleColor};
}
.w-base {
  color: {restColor};
}
.w-hot {
  opacity: 0; /* the envelope raises it as the highlight passes */
}
```

```js
// Form A: continuous sweep. 100% → 0% reads left→right (percent axis inverted);
// ease "none" — an eased sweep reads as an object, not light.
tl.fromTo(
  "#headline",
  { backgroundPosition: "100% 50%" },
  { backgroundPosition: "0% 50%", duration: SWEEP_DUR, ease: "none" },
  SWEEP_START,
);

// Form B: traveling highlight — per-word rise/fall envelopes, index stagger.
gsap.utils.toArray(".w-hot").forEach((el, i) => {
  const at = HIGHLIGHT_START + i * WORD_LAG;
  tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: HOT_RISE, ease: "power2.out" }, at);
  tl.to(el, { opacity: 0, duration: HOT_FALL, ease: "power2.in" }, at + WORD_LAG);
});

// Form C: hue-sweep, then crossfade to the solid twin (never tween color stops).
tl.fromTo(
  "#headline",
  { filter: "hue-rotate(0deg)" },
  { filter: `hue-rotate(${HUE_RANGE}deg)`, duration: HUE_DUR, ease: "power1.inOut" },
  HUE_START,
);
tl.to(
  "#headline",
  { opacity: 0, duration: SETTLE_SNAP_DUR, ease: "power2.in" },
  HUE_START + HUE_DUR,
);
```

**Variations:** a title-card crawl stretches Form A across a long terminal hold (3–8s), `ease: "none"`, with the sweep duration equal to the whole hold — one tween, no loop. A one-pass sheen inside type reads as the gradient being the resting fill everywhere except one narrow highlight band (≤~25% of the span); one backgroundPosition pass carries the band through and the text returns to rest with no crossfade. A karaoke settle uses Form B with the fall tweens skipped: the line lights cumulatively left-to-right and holds fully lit, settle color equal to the hot state, base copies starting dimmer. A gradient climax word emphasizes one word (often rotated ~-8°) carrying the gradient while the line stays solid — static gradient plus a short Form C hue shift on landing, settling to the brand accent; pairs with a Kinetic Beat Slam arrival.

**Values:** SWEEP_SPAN 200–400% (must exceed 100%; wider = softer/slower feel, narrower = busier color per glyph). SWEEP_DUR 1.2–3s, matching the card's hold exactly (slower than ~4s stops registering as motion). WORD_LAG 0.25–0.5s (HOT_FALL should start exactly WORD_LAG after the rise so envelopes cross — a gap reads as a blink). HOT_RISE/HOT_FALL 0.15–0.3s/0.25–0.45s (fall slightly longer so the highlight "trails"). HUE_RANGE/HUE_DUR 40–180°/0.8–1.6s (past ~180° the palette dissociates from itself mid-sweep). SETTLE_SNAP_DUR 0.1–0.35s. The settle color should be one of the gradient's own stops (or the brand ink) so the settle reads as resolution.

**Critical constraints:** `background-size` must exceed 100% on any element whose `backgroundPosition` is tweened, or the tween is a silent no-op. The percent axis is inverted — left-to-right perceived travel is `100% → 0%`. Both the `-webkit-background-clip: text` prefix AND unprefixed `background-clip: text`, with `color: transparent`, are required — missing the prefix renders a solid gradient block over the text in some render browsers. `ease: "none"` on position sweeps — this is supposed to read as light, not an accelerating object. Seamless ends for a crawl (first and last color stops equal), or the wrap point flashes a hard edge mid-hold. Stacked copies must be pixel-identical (same box, font, weight, tracking, one grid cell) — any metric drift makes the crossfade a double-exposure. Settle by crossfade, never by tweening stops; and the glyphs never move — if the type must travel, that's a separate wrapper-level rule. No CSS `@keyframes` shimmer — wall-clock animation desyncs from seek; every sweep is a timeline tween.

**See also:** the Kinetic Beat Slam rule (the slam lands the climax word, hue settle finishes it); the Spring-Pop Entrance rule (pop in solid, sweep after); the Discrete Text Sequence rule (swap-slot under a riding crawl); the Ambient Glow Bloom rule (surface-level sibling); the CSS Marker Patterns rule (strokes around text; fills here).

#### Chromatic Glitch

RGB-split/slice glitch that snaps sharp — offset color copies jitter on a deterministic hash of quantized timeline time (never `Math.random`), or horizontal slice bands displace and converge under a stepped ease; a brief vibration, then a clean resolve. Entrance stretch, emphasis burst, and slice-reveal forms.

Boundaries: the Motion-Blur Streak rule below is velocity blur tied to travel — its element is going somewhere fast. A glitching element is in place; the disturbance is temporal, not directional. The Hacker Flip 3D Reveal rule above substitutes glyphs (a decode); here the glyphs are fixed and only displaced copies of them move.

**How it works:** the subject is stacked with a base copy on top (full legibility at every frame) and ghost copies behind. All motion comes from one finite amplitude-envelope tween read by an `onUpdate`: (1) quantized time — `Math.floor(tl.time() / JITTER_STEP)` — the stutter comes from offsets that hold for the step duration and then jump; smoothly interpolated offsets read as wobble, not glitch, so this quantization IS the digital texture; (2) a deterministic hash where offsets are a pure function of `(step, layerIndex)`; (3) an amplitude envelope — a proxy tween carries amplitude `1 → 0` over the glitch duration, and per-frame offset equals `amp × (hash × 2 − 1) × maxSplit`; when the envelope hits zero the copies sit at exactly 0, and a final `tl.set` clamps the rest state so the hold is bit-exact. The slice form swaps color copies for N full copies each clipped to a horizontal band via `clip-path: inset()`, with per-band `x` (and optional `scaleX` stretch) starting at hash-derived offsets and converging to 0 under a stepped ease.

```js
const glitchHash = (n) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x); // 0..1, pure — a scrub to any t recomputes the same frame
};
```

```html
<!-- Form A: RGB-split — ghosts behind, base on top. Copies metric-identical (one grid cell, same font stack); aria-hidden on every non-base copy. -->
<div class="glitch-stack" id="glitch-stack">
  <span class="glitch-copy warm" aria-hidden="true">{glitchText}</span>
  <span class="glitch-copy cool" aria-hidden="true">{glitchText}</span>
  <span class="glitch-base">{glitchText}</span>
</div>
```

```css
.glitch-stack {
  display: grid; /* all copies share one cell — pixel-identical boxes */
}
.glitch-base,
.glitch-copy {
  grid-area: 1 / 1;
}
.glitch-base {
  z-index: 2; /* grid items take z-index without position */
  color: {textColor};
}
.glitch-copy {
  z-index: 1;
  opacity: 0; /* raised only while the envelope is live */
  will-change: transform; /* updates every frame while live */
  mix-blend-mode: screen; /* additive on dark bg; drop to normal (and lower opacity) on light */
}
.glitch-copy.warm {
  color: {warmSplit}; /* classic: red/orange */
}
.glitch-copy.cool {
  color: {coolSplit}; /* classic: cyan/blue */
}
```

```js
// Form A: RGB-split jitter — envelope snaps to full amplitude, decays to zero.
// All per-frame state derives from tl.time() + the envelope: pure, replays on seek.
const copies = gsap.utils.toArray("#glitch-stack .glitch-copy");
const amp = { a: 0 };
tl.set(amp, { a: 1 }, GLITCH_START);
tl.set(copies, { opacity: SPLIT_OPACITY }, GLITCH_START);
tl.to(
  amp,
  {
    a: 0,
    duration: GLITCH_DUR,
    ease: "power3.in", // most of the violence up front, dying fast
    onUpdate: () => {
      const step = Math.floor(tl.time() / JITTER_STEP); // quantized — the stutter
      copies.forEach((el, layer) => {
        const jx = (glitchHash(step * 13 + layer * 7) * 2 - 1) * MAX_SPLIT * amp.a;
        const jy = (glitchHash(step * 29 + layer * 11) * 2 - 1) * MAX_SPLIT * 0.35 * amp.a;
        gsap.set(el, { x: jx, y: jy });
      });
    },
  },
  GLITCH_START,
);
// The clean resolve: clamp ghosts to exact rest — never rely on the decay
// landing on zero. A ghost left 1px off reads as a bug every frame after.
tl.set(copies, { x: 0, y: 0, opacity: 0 }, GLITCH_START + GLITCH_DUR);

// Form B: slice displacement — N band copies of the same content converge.
const slices = gsap.utils.toArray("#slice-stack .slice");
const bandH = 100 / slices.length;
slices.forEach((el, i) => {
  gsap.set(el, { clipPath: `inset(${i * bandH}% 0 ${100 - (i + 1) * bandH}% 0)` });
  const dir = glitchHash(i * 3 + 1) > 0.5 ? 1 : -1;
  tl.fromTo(
    el,
    {
      x: dir * (SLICE_OFFSET_MIN + glitchHash(i * 5 + 2) * (SLICE_OFFSET_MAX - SLICE_OFFSET_MIN)),
      scaleX: 1 + glitchHash(i * 7 + 3) * SLICE_STRETCH,
      opacity: 1,
    },
    { x: 0, scaleX: 1, duration: SLICE_RESOLVE_DUR, ease: "steps(SLICE_STEPS)" },
    SLICE_START + glitchHash(i * 11 + 4) * SLICE_JITTER_LAG,
  );
});
```

**Variations:** a glitch-stretch entrance — the element ENTERS glitching, layering a whole-stack `fromTo` scaleX-from-stretched/opacity-from-0 tween with `power4.out` alongside the envelope so stretch, split, and envelope all die at the same frame. An emphasis burst on a held word — a spasm, not an arrival — 2–3 short envelopes (0.12–0.2s each) separated by clean gaps of 0.2–0.4s, each its own set/to/set triplet; the clean frames between bursts make it read as energy rather than a rendering fault. A slice reveal uses Form B as the arrival itself: bands start opaque but displaced, converge under the stepped ease, and dropping the color copies gives the monochrome, more restrained enterprise version. A card/non-text glitch is content-agnostic (logo lockup, small card) — keep the max split proportional (~1% of element width) or oversized splits read as broken layout, not interference.

**Values:** MAX_SPLIT 4–14px at headline sizes, roughly 0.06–0.1em (vertical component ~35% of horizontal; base must stay legible at peak). JITTER_STEP 1/30–1/12 second (shorter = frantic buzz, longer = VHS stutter; must be at least one render frame or quantization vanishes). GLITCH_DUR 0.25–0.6s for an entrance, 0.12–0.2s for a burst (≥~1s stops reading as an event and starts reading as a broken render). SPLIT_OPACITY 0.5–0.9 with screen blend on dark, 0.35–0.6 unblended on light (screen on white is invisible). SLICE_COUNT 4–10. SLICE_OFFSET_MIN/MAX 12–60px, derived per-band from the hash, never uniform. SLICE_STRETCH 0–0.5 (0 = pure displacement, ~0.3 = stretched-scanline read). SLICE_RESOLVE_DUR/STEPS/JITTER_LAG 0.2–0.4s / 3–6 / ≤0.08s per band.

**Critical constraints:** quantize time — the stutter IS the effect; offsets hold for the jitter step then jump, and if the glitch looks like jelly you interpolated. Per-frame values must be pure functions of quantized time and index — the hash inputs use `tl.time()`, nothing else. Clamp the rest state explicitly at the envelope's end — never rely on the decay landing exactly on zero. Base copy stays on top and always legible — ghosts vibrate behind it, and a glitch that destroys legibility for more than ~2 frames is a tear-down, not an accent. Keep it brief, then clean — the glitch duration should be well under half the element's total screen time, with emphasis bursts as separate finite triplets. No CSS `@keyframes` glitch loops — everything runs through the timeline's `onUpdate`. Match the register — RGB-split is a loud consumer/tech gesture; the monochrome slice variant is the only form that belongs in a restrained enterprise composition.

**See also:** the Kinetic Beat Slam rule (one beat lands with the glitch-stretch entrance); the Spring-Pop Entrance rule (pop clean, burst on the stress beat); the Gradient Text Sweep rule (gradient carries the hold after the resolve); the Discrete Text Sequence rule (state swap masked at max amplitude); the Motion-Blur Streak rule (the traveling sibling — if it's moving fast, blur it there instead).

### Data & Stats

(The Counting with Dynamic Scale rule above is also part of this category — the number half of a stat beat.)

#### Stat Bars & Fills

The graphics that give a stat visual weight beside its number: a small bar chart, a progress bar/ring filling to a percentage, or a star row filling to a fractional rating. Pair these with the Counting with Dynamic Scale rule above (the number) for a complete stat scene.

**Layout blueprint — pick ONE and hold it across all stats:** single-focus (one centered frame, the number is the hero, a ring or bar sits under/around it — cleanest for a sequential reveal of stat 1 → stat 2 → stat 3 in the same frame), or split-frame (big number on the left, paired graphic on the right — better when stats are shown together or each needs a distinct visual). Don't mix blueprints between stats in one piece — that reads as inconsistent.

**1 — Growth bars (CSS `scaleY` stagger).** Bars grow from the baseline with a stagger; the last bar is the accent. Heights are authored in CSS (inline height per bar); GSAP only reveals `scaleY: 0 → 1` — never animate `height`.

```css
.bars {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  height: 280px;
}
.bar {
  width: 48px;
  background: #3a4a64;
  transform: scaleY(0);
  transform-origin: bottom center; /* grow UP from the baseline, not from center */
}
.bar:last-child {
  background: #ffc300; /* accent the final/current bar */
}
```

```js
tl.to(".bar", { scaleY: 1, duration: 0.7, ease: "power3.out", stagger: 0.08 }, 0.3);
```

**2 — Progress fill.** Bar form uses `scaleX` from a left origin:

```css
.track {
  width: 520px;
  height: 16px;
  background: #1b263b;
  border-radius: 8px;
  overflow: hidden;
}
/* width:100% is REQUIRED — an absolutely-positioned fill with no width is 0px, and scaleX of 0 is
   still 0 → the bar renders invisible (automated gates may miss a zero-width scaled element). */
.fill {
  width: 100%;
  height: 100%;
  background: #ffc300;
  transform: scaleX(0);
  transform-origin: left center;
}
```

```js
const PCT = 0.92; // 92%
tl.to(".fill", { scaleX: PCT, duration: 1.0, ease: "power2.out" }, 0.3);
```

Ring form uses a measured stroke draw (mechanics in the SVG Path Draw rule below):

```js
const ring = document.querySelector("#ring");
const LEN = ring.getTotalLength(); // measure, don't hard-code the circumference
ring.style.strokeDasharray = LEN;
ring.style.strokeDashoffset = LEN; // empty
// rotate the <circle> -90deg in CSS so the fill starts at 12 o'clock
tl.to(ring, { strokeDashoffset: LEN * (1 - 0.92), duration: 1.1, ease: "power2.out" }, 0.3);
```

**3 — Star-rating fill (fractional).** A gold star row revealed left-to-right to a fractional value (e.g. 4.6/5) via a clip wipe over a gold layer sitting on a gray layer.

```html
<div class="stars">
  <div class="stars-gray">★★★★★</div>
  <div class="stars-gold" id="goldStars">★★★★★</div>
</div>
```

```css
.stars {
  position: relative;
  font-size: 64px;
  letter-spacing: 8px;
}
.stars-gray {
  color: #2b3548;
}
.stars-gold {
  position: absolute;
  inset: 0;
  color: #ffc300;
  width: 100%;
  clip-path: inset(0 100% 0 0);
}
```

```js
const RATING = 4.6,
  MAX = 5;
tl.to(
  "#goldStars",
  { clipPath: `inset(0 ${100 - (RATING / MAX) * 100}% 0 0)`, duration: 1.0, ease: "power2.out" },
  0.3,
);
```

**Values:** bar count 4–6 (reads as "a trend" without clutter; the last bar is the current/accent value). Fill duration 0.8–1.2s, matched to the paired count-up so number and graphic land together (share the ease). Stagger 0.06–0.1s (larger feels sluggish, 0 loses the build). Exactly one accent hue across bars/fill/stars, the rest muted.

**Critical constraints:** use `scaleY`/`scaleX`/`clipPath`, never `height`/`width` tweens — author each bar's final height in CSS and scale from 0. `transform-origin` must be `bottom` (bars grow up) or `left` (fills grow right) — the default center origin scales from the middle and looks wrong. The fill needs `width: 100%` — a zero-width fill scaled by any factor is still invisible. Measure, don't hard-code — ring length via `getTotalLength()`. Match the paired number's timing — the fill and the count-up should peak together (same start and ease) so the stat resolves as one beat, and a paired counter's `onUpdate` must stay O(1).

**See also:** the Counting with Dynamic Scale rule (the number beside the graphic — same ease/duration); the SVG Path Draw rule (progress-ring draw mechanics).

#### Chart Scrub Readout

The chart is already ON screen — this rule interrogates it. A vertical tracking line rides the scrub position, a marker dot follows the series, and a live tooltip reads out `date: value` per position, values flickering past like an odometer. It's the "this data is real — look closer" beat: the scrub proves the chart is an instrument, not a picture.

Boundary with its neighbors: the Stat Bars & Fills rule owns the chart's ARRIVAL; the Counting with Dynamic Scale rule owns a single number swelling in place. This rule assumes the graphic already exists and adds a read head moving across it. The three chain naturally: the line draws in (via SVG Path Draw or Stat Bars & Fills), this rule scrubs it, and the landing value hands off to a count-up lockup.

**How it works:** (1) data is baked at setup — a literal `DATA` array of `{ d, v }` points (or a pure index formula). The polyline's `points` attribute is computed once from `DATA` by pure mapping functions, so the chart and the readout share one source of truth. (2) One driver tween (`p: 0 → 1`) derives everything in its `onUpdate`: tracking-line x, marker x/y, tooltip position — every output is a pure function of `p`, so any seek lands the identical frame. (3) The marker rides the polyline, its y interpolating between the two neighboring baked points from the same arrays that built the chart — a separately keyframed marker inevitably floats off the line. (4) The readout is threshold-stepped — the nearest data index derives from `p`, and `textContent` is written only when that index changes (a last-index guard). Transforms glide every frame (compositor-cheap); text steps per data point.

```html
<!-- inside a standard scene clip. Size the SVG so viewBox units === CSS pixels:
     one coordinate space serves the polyline, tracking line, marker, AND the HTML tooltip. -->
<div class="chart-wrap">
  <!-- position: relative — the tooltip transforms against this box -->
  <svg class="chart" viewBox="0 0 CHART_W CHART_H" width="CHART_W" height="CHART_H">
    <polyline id="series-a" class="series" fill="none" />
    <line id="track-line" y1="0" y2="CHART_H" stroke-dasharray="6 6" />
    <circle id="marker" r="MARKER_R" />
  </svg>
  <div class="tooltip" id="tooltip">
    <span id="tip-date">{firstDate}</span>
    <span id="tip-value">{firstValue}</span>
  </div>
</div>
```

```css
.tooltip {
  position: absolute;
  top: 0;
  left: 0;
  min-width: TIP_MIN_WIDTH; /* fixed — the box must not resize as values change length */
}
#tip-value {
  font-variant-numeric: tabular-nums; /* MANDATORY — digits flicker past; widths must not */
}
```

```js
// Data baked at setup — literal values.
const DATA = [
  { d: "{date1}", v: V1 },
  // ... N points, chronological ...
];

// Pure mapping functions — geometry derives from DATA once.
const PAD = CHART_PAD;
const PLOT_W = CHART_W - PAD * 2;
const PLOT_H = CHART_H - PAD * 2;
const vals = DATA.map((p) => p.v);
const V_MIN = Math.min(...vals);
const V_MAX = Math.max(...vals);
const X = (i) => PAD + (i / (DATA.length - 1)) * PLOT_W;
const Y = (v) => PAD + PLOT_H * (1 - (v - V_MIN) / (V_MAX - V_MIN));

document
  .getElementById("series-a")
  .setAttribute("points", DATA.map((p, i) => `${X(i)},${Y(p.v)}`).join(" "));

const line = document.getElementById("track-line");
const marker = document.getElementById("marker");
const tooltip = document.getElementById("tooltip");
const tipDate = document.getElementById("tip-date");
const tipValue = document.getElementById("tip-value");

// Tooltip pops in as the scrub begins — a small fromTo scale/opacity spring at SCRUB_AT.

// ONE driver — line, marker, and tooltip are all projections of p.
const scrub = { p: 0 };
let lastIdx = -1;
tl.to(
  scrub,
  {
    p: 1,
    duration: SCRUB_DUR,
    ease: SCRUB_EASE,
    onUpdate: () => {
      const f = scrub.p * (DATA.length - 1); // fractional index
      const i = Math.min(DATA.length - 2, Math.floor(f));
      const t = f - i;
      const x = X(i) + (X(i + 1) - X(i)) * t;
      const y = Y(DATA[i].v) + (Y(DATA[i + 1].v) - Y(DATA[i].v)) * t;

      // Transforms glide every frame (cheap, deterministic)
      line.setAttribute("x1", x);
      line.setAttribute("x2", x);
      marker.setAttribute("cx", x);
      marker.setAttribute("cy", y);
      tooltip.style.transform = `translate(${x + TIP_DX}px, ${y - TIP_DY}px)`;

      // Text steps only when the nearest data point changes
      const idx = Math.round(f);
      if (idx !== lastIdx) {
        tipDate.textContent = DATA[idx].d;
        tipValue.textContent = `${DATA[idx].v.toLocaleString()} {unitLabel}`;
        lastIdx = idx;
      }
    },
  },
  SCRUB_AT,
);
// End hold: the driver finishes before the scene does — the landed value reads.
```

**Variations:** a peak stop — the scrub is the wind-up, the landing is the stat: use `power3.out` easing to decelerate onto the final/peak point, then pop the emphasis at landing (marker scale from 1 to a peak-pop scale) — pair with a pill tooltip that springs to its final label (see the Spring-Pop Entrance rule below) for the classic "line breaks above the band" climax. A second-series activation on cross — series B sits dimmed; partway through the scrub tween its stroke to the lit color (0.25s, `power2.out`), and in the driver's `onUpdate` read from B's array once the crossing threshold is passed (still index-guarded). A two-chart glide sweeps chart A, glides the cursor/tooltip group across the gutter with a plain `x` tween (dead travel, no readout), then chart B activates with its own driver — one driver per chart. A cursor-led scrub form makes an oversized cursor the visible actor, another projection of the SAME driver (positioned from `x` in the same `onUpdate`), never a second tween that merely matches timing. A playhead form drops the cursor entirely; the tracking line IS the actor (timeline scrubbers, audio waves, session replays), with `ease: "none"` for mechanical playback rather than a hand.

**Values:** N (data points) 10–40 (fewer reads as a slideshow, more blurs into texture — the flicker is the point, only first and final values must be legible). SCRUB_DUR 1.5–3s (shorter = confident sweep, longer = inspection; leave at least ~0.8s of scene after the driver ends so the landed value holds). SCRUB_EASE `power1.inOut` default, `"none"` for the playhead form, `power3.out` for a peak stop — never `back.out` (a read head that overshoots and re-reads looks broken). Crossing threshold 0.55–0.75 of the scrub (earlier and A never establishes, later and B's readout has no time to live). TIP_DX/TIP_DY 16–48px up-and-right (flip the sign near the chart's right edge so the tooltip never exits the frame). MARKER_R/stroke width r 6–12/4–8px (the marker must dominate the line it rides). TIP_MIN_WIDTH at least as wide as the longest `date: value` state.

**Critical constraints:** `DATA` is literal at setup; polyline points derive from it via pure functions so the chart and readout share one source of truth. Seed at setup — call the scrub applier once with p=0 right after building, or a seek to t=0 before the driver runs shows the tracking line/marker at their HTML-default positions. Single driver — one `p` tween; all scrub outputs (line, marker, tooltip, any cursor) computed in its `onUpdate`, each a pure function of `p`. Readout writes guarded by index change — `onUpdate` stays O(1). SVG viewBox units must equal CSS pixels so one coordinate space serves both the SVG internals and the HTML tooltip's transform. `tabular-nums` plus a fixed `min-width` on the tooltip value. The chart must pre-exist — draw-in belongs to the SVG Path Draw or Stat Bars & Fills rules, sequenced BEFORE the scrub. Land the read — hold the final value at least 0.8s (or hand off to a count-up lockup).

**See also:** the SVG Path Draw rule (the series draws in first); the Stat Bars & Fills rule (surrounding dashboard chrome); the Spring-Pop Entrance rule (peak dot + pill pop at the landing); the Counting with Dynamic Scale rule (closing stat lockup); the Cursor-Click Ripple and Context-Sensitive Cursor rules (the cursor-led form's actor); the Control-Target Sync rule (the sibling WRITE direction — there a control edits a target; here a scrub reads a dataset).

### Camera & Viewport

#### Coordinate Target Zoom

A simple `scale > 1` on a wrapper pushes off-center content OFF the visible canvas. To zoom into a specific non-centered element, apply scale AND an inverse translation in lockstep so the target lands at viewport center.

**How it works:** two nested wrappers, separated concerns — never scale and translate on the SAME element (`translate × scale` ≠ `scale × translate` in CSS transform composition). The outer wrapper applies `scale` (the zoom) around `transform-origin: 50% 50%`; the inner wrapper applies `translate(x, y)` (the counter-shift). The counter-translate is the negation of the target's offset from viewport center: `T = -offset`. Derivation: the inner translate moves the target to `offset + T` in pre-scale units; the outer scale S (around center) maps that to `S × (offset + T)`; landing at center means `S × (offset + T) = 0` → `T = -offset`. The formula does NOT depend on S — the translate is identical at 1.5×, 2×, or 3×. A common wrong intuition is `T = -offset × (S - 1)`; it coincidentally matches at S=2 and is wrong everywhere else.

⚠️ This is the NESTED-wrapper formula. The single-wrapper camera form described in the Viewport Change rule below puts `translate(x,y) scale(S)` on ONE element, where CSS applies scale first — there the counter-translate is `T = -offset × S`. The two formulas are not interchangeable; match the formula to the wrapper structure.

**Getting the offset.** `T = -offset` is only as good as `offset`. The #1 way this pattern ships broken is hand-computing `offset` from a layout formula, getting the sign or magnitude wrong, and letting the zoom amplify a small error off-screen. Default to measuring the target's real laid-out center; reserve the formula for symmetric rows.

**Default — measure the actual center** (works for any layout, immune to sign errors because it reads the rendered DOM, not a mental model):

```js
await document.fonts.ready; // metrics final; fallback fonts are 10–30px off → tens of px after a 3×+ zoom
const W = 1920,
  H = 1080;
const r = document.getElementById("target-card").getBoundingClientRect();
const TARGET_OFFSET_X = r.left + r.width / 2 - W / 2;
const TARGET_OFFSET_Y = r.top + r.height / 2 - H / 2;
```

Measure once at setup and bake it — never per-frame in `onUpdate`. Because the measurement is async (waiting for fonts), build and register the timeline inside the same async setup so the baked offset is ready before the timeline is published to the shared registry.

**Shortcut — symmetric equal-width row ONLY:**

```js
const index_offset = targetIndex - (N - 1) / 2;
const TARGET_OFFSET_X = index_offset * (CARD_WIDTH + CARD_GAP);
```

⚠️ This assumes every sibling is the same width — the moment the row is asymmetric it gives the wrong answer, often the wrong sign (a heavier side shifts the centered target the OPPOSITE way you'd guess). For anything but equal cards, measure.

**Headroom budget** — cap the scale from the measured size (a zoom multiplies any centering error; keep the target ≤~88% of the canvas at peak):

```js
const maxScale = Math.min((0.88 * W) / r.width, (0.88 * H) / r.height);
const ZOOM_SCALE = Math.min(DESIRED_SCALE, maxScale);
```

A target filling 97%+ of the frame reads as cut off the instant its center is slightly off — and a hand-baked offset always is.

```html
<div class="zoom-outer" id="zoom-outer">
  <div class="zoom-inner" id="zoom-inner">
    <div class="content">
      <div class="card">{other}</div>
      <div class="card target" id="target-card">{target}</div>
      <div class="card">{other}</div>
    </div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — at zoom > 1 the scaled content leaks past the frame */
}
.zoom-outer {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* center scaling is what the counter-translate math assumes */
  will-change: transform;
}
.zoom-inner {
  display: grid;
  place-items: center;
  will-change: transform;
}
```

```js
// TARGET_OFFSET_X/Y and ZOOM_SCALE come from "Getting the offset" — measured
// at setup (after fonts.ready), baked. Counter-translation = -offset.
const counterX = -TARGET_OFFSET_X;
const counterY = -TARGET_OFFSET_Y;

// Scale and counter-translate MUST share position, duration, AND ease —
// otherwise the target visibly wanders mid-zoom.
tl.to("#zoom-outer", { scale: ZOOM_SCALE, duration: ZOOM_DUR, ease: "power3.inOut" }, ZOOM_AT);
tl.to(
  "#zoom-inner",
  { x: counterX, y: counterY, duration: ZOOM_DUR, ease: "power3.inOut" },
  ZOOM_AT,
);
```

**Variations:** a zoom-out (target → wide view) reverses the phases — start zoomed-in, tween to scale 1 and translate 0, with the "reveal" as the panorama. A multi-target zoom sequence chains zooms (target A → pause → target B → pull back); each segment needs its own counter-translation pair.

**Values:** ZOOM_SCALE 1.5× modest → 3× dominant → 5×+ extreme (capped by the headroom budget; raster media needs source resolution ≥ rendered size × ZOOM_SCALE). ZOOM_DUR 1.0–2.0s (under 0.8s feels like a teleport, over 2.5s drags; both tweens share it). ZOOM_AT after the layout lands plus 0.5–1.5s (give the viewer time to scan before the camera commits). DWELL at least 1.0s after the zoom settles (1.5–2s ideal — the viewer must be able to read the target).

**Critical constraints:** the outer wrapper scales, the inner translates — never both transforms on one element; nested wrappers keep the math clean. `transform-origin: 50% 50%` on the outer wrapper is required, or the counter-translate derivation breaks. `overflow: hidden` on the scene root, or zoomed content leaks past the frame. Scale and counter-translate must share duration and ease at the same timeline position, or the target drifts mid-zoom. The offset must be measured once at setup (after fonts load), baked, never recomputed per-frame or hand-derived for a non-symmetric layout. Scale within the headroom budget — target ≤~88% of the canvas at peak, derived from the measured size.

**See also:** the Viewport Change rule (the single-wrapper form, `T = -offset × S`); the Multi-Phase Camera rule (a zoom phase inside a phased camera); the Sine Wave Loop rule (idle breathing after the zoom settles); the Discrete Text Sequence rule (text assembly in the target before the zoom).

#### Two-Phase Camera Cursor Tracking

Keeps a horizontally-growing element (a search bar with typing text, a long URL animating in) visible by switching between two camera modes.

**How it works:** separate "world space" (the full target element with all content) from "screen space" (the viewport). Two phases — Phase 1 (static): the world container sits at a fixed initial offset, the camera doesn't move, anchoring the viewer's eye before tracking begins. Phase 2 (tracking): activates when the focal point (cursor, highlight, last typed glyph) exceeds a target screen position (a fraction of the viewport width from the left); the world translates leftward, keeping the focal point pinned at that screen position.

The offset math is mathematically continuous at the phase boundary — at the instant tracking starts, the world position equals what the static phase had, so the transition is seamless: `finalWorldX = Math.min(INITIAL_OFFSET, trackingOffset)`. While the focal point hasn't grown past the target, the tracking offset is a less-negative number and `Math.min` returns the static value; once the focal point would cross the target, the tracking offset overtakes. Do NOT replace this with a hard `if (typingProgress > threshold)` branch — the camera will visibly jump.

```html
<div class="viewport">
  <div class="world">
    <div class="search-bar">
      <span class="text" id="reveal-text">{phrase}</span><span class="cursor">|</span>
    </div>
  </div>
</div>
```

```css
.viewport {
  position: absolute;
  inset: 0;
  overflow: hidden; /* clip the world's left edge as it pans off-screen */
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: VIEWPORT_PAD_LEFT; /* Phase-1 anchor X — must match the JS constant */
}
.world {
  display: flex;
  align-items: center;
  white-space: nowrap; /* text must stay on one line for the camera math */
}
.search-bar .text {
  display: inline-block;
  overflow: hidden;
  vertical-align: bottom;
}
.search-bar .cursor {
  display: inline-block; /* inline sibling of the text, NOT absolutely positioned —
     absolute positioning misaligns with the camera math */
  width: CURSOR_WIDTH;
  margin-left: CURSOR_GAP;
  background: {accentColor};
  height: CURSOR_HEIGHT_EM;
  vertical-align: bottom;
  /* no CSS blink animation — CSS clocks don't sync to seek; blink is a GSAP tween below */
}
```

```js
// Pre-measure the target text width to compute tracking distance.
// Measure SYNCHRONOUSLY — no fonts.ready gate (see Critical Constraints).
const textEl = document.getElementById("reveal-text");
const targetCursorScreenX = CURSOR_TARGET_FRACTION * VIEWPORT_WIDTH;
const fullWidth = textEl.scrollWidth; // total text width after full reveal
const trackingDelta = Math.max(0, VIEWPORT_PAD_LEFT + fullWidth - targetCursorScreenX);

// Phase 1 — text reveals progressively; camera holds. maxWidth tween
// (width/left/top tweens are forbidden); ease "none" = linear typing rate.
tl.fromTo(
  ".search-bar .text",
  { maxWidth: 0 },
  { maxWidth: fullWidth, duration: REVEAL_DUR, ease: "none" },
  REVEAL_START,
);

// Phase 2 — camera tracks. Start BEFORE full reveal so the handoff feels
// continuous (Math.min form above makes it mathematically continuous).
tl.to(".world", { x: -trackingDelta, duration: TRACK_DUR, ease: "power2.inOut" }, TRACK_START);

// Cursor blink — finite GSAP yoyo (never CSS @keyframes; CSS animation clocks
// aren't synced to HF's seek and flicker non-deterministically).
const blinkRepeats = Math.ceil(SCENE_DURATION / BLINK_HALF_PERIOD) - 1;
tl.to(
  ".search-bar .cursor",
  { opacity: 0, duration: BLINK_HALF_PERIOD, ease: "steps(1)", yoyo: true, repeat: blinkRepeats },
  0,
);
```

**Variations:** centered-to-center-tracked — `justify-content: center; padding: 0`, target fraction 0.5, tracking once the focal point crosses the midline. Left-aligned-to-right-tracked — as written, best when content exceeds viewport width from the start. A continuous typing driver replaces the `maxWidth` tween with an `onUpdate` typing clock plus per-frame width measurement driving the cursor screen X — required when the typed text is consumed elsewhere in the scene (e.g. by a parent strip's camera offset).

**Values:** VIEWPORT_PAD_LEFT 0 to ~10% of viewport width, must match the CSS `padding-left` or the camera math drifts. VIEWPORT_WIDTH equals the composition's own pixel width, never tweened. CURSOR_TARGET_FRACTION 0.5–0.75 (lower = less revealed text in frame; higher delays tracking). CURSOR_WIDTH/GAP 4–10px / a few px (gap should be ≤ cursor width or it visually detaches). CURSOR_HEIGHT_EM 0.85–1.0em (matches the typed glyph height). REVEAL_DUR chars × 0.05–0.15s, `ease: "none"` since any easing distorts the per-keystroke cadence. TRACK_START before reveal completes, overlapping so the handoff feels continuous. TRACK_DUR 0.8–2.0s, `power2.inOut`/`power3.inOut` (`back.out` reads as UI bounce, not camera). BLINK_HALF_PERIOD 0.2–0.4s, `steps(1)` hard on/off.

**Critical constraints:** build the timeline SYNCHRONOUSLY with no wait for font loading. Frames render in parallel workers, each a fresh browser context — a promise-gated timeline means some workers seek frames BEFORE the promise resolves and find no timeline registered, rendering CSS initial state (empty text) while others render correctly, producing visible flicker across the finished video. Register the timeline at script-parse time — the camera math tolerates a few percent width error from fallback-font measurement; worker-race flicker is unacceptable. If precise post-font measurement genuinely matters, re-measure inside the tween's `onUpdate` instead (still deterministic per-frame), or force blocking font loading via `font-display: block`. Measure with `getBoundingClientRect()`/`scrollWidth`/probe nodes, never character count × font size — proportional fonts have variable glyph widths. Use the continuous `Math.min` math at the phase boundary, never a hard threshold branch. `white-space: nowrap` on the world plus pre-allocated width (tween `maxWidth` to the full target width) prevents layout shift mid-tween. The cursor is an inline sibling of the text and blinks via a finite GSAP yoyo, never CSS `@keyframes … infinite`. `overflow: hidden` on the viewport clips the world as it pans.

**See also:** the Context-Sensitive Cursor rule (cursor color per text segment); the Discrete Text Sequence rule (non-linear text reveals under this camera).

#### Multi-Phase Camera

A camera wrapper around the ENTIRE scene that progresses through discrete zoom phases at scripted triggers, with continuous sine-driven micro-drift overlaid so the camera never feels static between phases. Distinct from a single linear zoom — multi-phase creates cinematic pacing (anticipation → reveal → settle).

**How it works:** the camera is one wrapping element whose `transform: scale() translate(x, y)` is composed from two channels inside a single `onUpdate` writer: (1) phase scale — a proxy object stepped through phases at trigger times (phase-1 scale at t=0 → phase-2 scale at its trigger → phase-3 scale at its trigger); (2) drift offset — a continuous sine-based `translateX`/`translateY` (small amplitude, slow frequency) ADDED to the phase transform, where X and Y run at slightly different frequencies (ratio ≈1.3) — equal frequencies produce a perfect diagonal that reads mechanical, while ~1.3 gives an organic Lissajous pattern.

```html
<div class="camera" id="camera">
  <div class="content">
    <div class="hero">{Brand}</div>
    <div class="tagline">{tagline}</div>
    <div class="cta">{ctaText}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — any phase scale < 1 exposes the content's edges */
  background: {sceneBgColor}; /* background on .scene, NOT .camera — a camera-borne
     background warps/translates with the transform and reveals the outer void */
}
.camera {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* off-center origin creates phase-to-phase drift */
  will-change: transform;
}
```

```js
const camera = document.getElementById("camera");

// Three-phase scale plan: pullback → focus → push.
const phase = { scale: PHASE_1_SCALE }; // Phase 1 is the initial value — no tween

// Phase 2 — settle to neutral focus
tl.to(phase, { scale: PHASE_2_SCALE, duration: PHASE_2_DUR, ease: PHASE_2_EASE }, PHASE_2_AT);

// Phase 3 — slow push-in for the climax
tl.to(phase, { scale: PHASE_3_SCALE, duration: PHASE_3_DUR, ease: PHASE_3_EASE }, PHASE_3_AT);

// Drift driver — continuous sine motion overlaid on the phase scale.
// The ONE writer of camera.style.transform.
const drift = { p: 0 };
tl.to(
  drift,
  {
    p: Math.PI * 2 * DRIFT_CYCLES,
    duration: TOTAL_DURATION, // spans the whole composition
    ease: "none",
    onUpdate: () => {
      const dx = Math.sin(drift.p) * DRIFT_AMP_X;
      const dy = Math.sin(drift.p * DRIFT_FREQ_RATIO) * DRIFT_AMP_Y;
      camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
    },
  },
  0,
);

// Content reveals happen INSIDE the camera frame (hero/tagline/cta beats).
```

**Phase patterns:**

| Pattern | Scale sequence (1 → 2 → 3) | Feel | When to use |
| --- | --- | --- | --- |
| Focus-in | back → neutral → slight push | Approach → settle → slight push | Default product reveal |
| Dramatic reveal | push → neutral → pull | Wide → focus → settle back | Hero shot with breathing room |
| Steady push | neutral → slight push → more push | Gradual forward momentum | Continuous narrative push |
| Bookend pull | neutral → strong push → neutral | Settle → push → release | CTA emphasis then release |

**Variations:** phase trigger by content beat — align a camera tween's start with a content tween's end (entry completes → push begins) rather than a fixed clock value. Camera shake (panic/impact) — a brief higher-amplitude, higher-frequency drift tween over a short window, same drift mechanism with its own shake amplitude/cycles/duration/start. A targeted zoom into an off-center element combines scale with counter-translation, dividing the measured offset by the current scale before feeding it into the writer (full counter-translate doctrine in the Coordinate Target Zoom rule above).

**Values:** PHASE_1/2/3_SCALE 0.88–0.96 / 0.98–1.02 / 1.04–1.15 (tighter spread = subtler camera; scale < 1 REQUIRES `overflow: hidden` on the scene). PHASE_2_AT/DUR 0.3–1.0s / 1.0–1.8s (longer duration = slower, more cinematic settle). PHASE_3_AT/DUR 2.0–4.0s / 1.0–2.0s (phase-3's start must be ≥ phase-2's start plus its duration or focus is preempted). PHASE_2/3_EASE `power2.out`/`power3.out`/`power2.inOut` (spring/back easing on a camera feels uncomfortable; each later phase should settle deeper). TOTAL_DURATION equals the composition's own duration (the drift tween must span the whole composition). DRIFT_CYCLES 1–3 (1 = one slow breath; high values read as mechanical wobble). DRIFT_AMP_X/Y 2–8px / 1–4px (imperceptible per-frame, visible over time — if it reads as a shake, it's too much). DRIFT_FREQ_RATIO 1.2–1.5 (1.0 = perfect diagonal, mechanical; ~1.3 = organic Lissajous). A hero reveal should start after the phase-2 settle lands, or a hero fading in mid-pull-back feels like it's flying away.

**Critical constraints:** the camera wraps EVERYTHING in the scene — a per-element camera creates parallax bugs and breaks the "one viewpoint" read. There is one writer: phase scale and drift compose inside the single drift `onUpdate`; nothing else touches the camera's transform. `overflow: hidden` on the scene is required whenever any phase scale is below 1. `transform-origin: 50% 50%` on the camera — off-center origin creates unpredictable phase-to-phase drift. Scene background goes on the scene, not the camera, or scaling/translating reveals the outer void. Hero reveal starts after the initial pull-back ease lands.

**See also:** the Coordinate Target Zoom rule (counter-translate math for the targeted variation); the Orbit 3D Entry rule (orbit inside a drifting camera); the Counting with Dynamic Scale rule (climax push synced to counter peak); the 3D Text Depth Layers rule (depth-stacked hero under camera moves); the Sine Wave Loop rule (element idle inside the camera).

#### Viewport Change (Virtual Camera)

Simulates camera effects (zoom/pan/focus-lock on a moving element) by transforming a wrapper around ALL scene content. The "world" moves opposite to the perceived camera. Distinct from the Multi-Phase Camera rule above (2–3 discrete phases plus drift) — this rule is a single continuous zoom/pan, often used for focus-lock following a moving element.

**How it works:** camera intent maps to world transform — camera pans right → world `translateX(-distance)`; camera zooms in → world `scale(>1)`; camera follows an element's X → world `translateX(viewportCenter - elementWorldX)` per-frame. Get the sign right or everything moves the wrong way. A single `.world` wrapper holds the camera transform; elements inside are positioned in world space, unchanged.

**Single-element composite transform** (this rule's form): both scale and translate live on ONE wrapper as `translate(x, y) scale(S)`. CSS applies scale FIRST, then translate (right-to-left matrix composition), so a point at world offset `(ox, oy)` lands on screen at `(S × ox + x, S × oy + y)`. To map the target to viewport center, solve `S × offset + T = 0`: `T = -offset × S`.

This is DIFFERENT from the Coordinate Target Zoom rule above, which uses two nested wrappers (outer scales, inner translates) and derives `T = -offset` (independent of S). Mixing up the two forms drifts the target off-center as scale changes. Use this single-wrapper form when you want one source of truth for camera state (a scale/x/y object) written via `onUpdate`; use nested wrappers when scale and translate can tween independently with shared ease.

```html
<div class="world" id="world">
  <div class="content">
    <div class="hero">{Brand}</div>
    <div class="tagline">{tagline}</div>
    <div class="cta" id="cta">{ctaUrl}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* REQUIRED — any non-1.0 scale reveals edges or pushes content off-frame */
  background: {bgGradient}; /* on .scene, NOT .world — a world-borne background warps with the camera */
}
.world {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%; /* centered scaling is what the math assumes */
  will-change: transform;
}
```

```js
const world = document.getElementById("world");

// Camera state — single source of truth. The world transform is composed from
// this object in ONE place so the transform string order is stable.
const cam = { scale: 1, x: 0, y: 0 };
function applyCamera() {
  world.style.transform = `translate(${cam.x}px, ${cam.y}px) scale(${cam.scale})`;
}
applyCamera(); // seed frame 0

// Zoom in on the CTA: single-element composite transform → T = -offset × S.
// TARGET_OFFSET_Y is the target's measured offset from viewport center at
// neutral camera (sign matters — positive = below center).
const counterY = -TARGET_OFFSET_Y * TARGET_SCALE;

tl.to(
  cam,
  {
    scale: TARGET_SCALE,
    y: counterY,
    duration: ZOOM_DUR,
    ease: "power3.inOut",
    onUpdate: applyCamera,
  },
  ZOOM_START,
);
```

**Scale value guide:**

| Effect | Scale | Feel |
| --- | --- | --- |
| Subtle | 1.02–1.05 | Barely perceptible — "professional" |
| Medium | 1.05–1.15 | "Ta-da" emphasis |
| Noticeable | 1.15–1.30 | Focus on region |
| Dramatic | 1.5–2.5 | Element fills screen |
| Full-screen | 3.0+ | Element covers viewport |

Perception: less than 5% scale change is imperceptible; 10–15% is comfortable emphasis; over 30% is cinematic/dramatic. For a natural product feel, prefer 1.05–1.15× over 2–3s; save big >1.3× zooms for dramatic narrative moments.

**Extreme range — 4–12× outward (workspace reveal).** The same single-cam math runs far past the table: a zoom-out workspace reveal opens punched-in at 4–12× on one detail (a single cell, message, or button) and pulls out to the full workspace in one continuous move. The mechanics don't change — one camera-state object, `T = -offset × S`, one apply-camera writer — only the authoring direction does: build the workspace at its final (1×) layout and OPEN scaled-in (a large initial scale, counter-translate aiming the opening detail, seeded via the apply function so a seek to t=0 lands punched-in). The wide landing frame is then everything at native design size — text crisp, raster assets at source resolution. Never the inverse — authoring the close-up at 1× and scaling the world down for the wide frame drops every label below legible pixel size and softens raster media. Measure the opening target precisely: at scale 8, a 1px error in the baked offset is 8px on screen at the opening pose. The opening detail must survive being magnified by the scale factor on the first frames — vector/DOM text is safe, raster needs source resolution ≥ rendered × scale.

**Variations:** focus-lock (camera follows a moving cursor/character) — keep the element at a fixed screen X by computing the world offset per-frame inside the driver's `onUpdate`:

```js
const focusEl = document.querySelector(".moving-cursor");
const targetScreenX = VIEWPORT_WIDTH * FOCUS_SCREEN_X_FRAC; // 0.4–0.7; 0.5 = dead center
const focusUpdate = { p: 0 };
tl.to(
  focusUpdate,
  {
    p: 1,
    duration: FOLLOW_DUR, // matches how long the focused element is in motion
    ease: "power2.inOut",
    onUpdate: () => {
      const rect = focusEl.getBoundingClientRect();
      cam.x = targetScreenX - (rect.left + rect.width / 2);
      applyCamera();
    },
  },
  FOLLOW_START,
);
```

Composite scale (multi-phase) — two proxy tweens multiplied through one writer, combining a slow push-in with a brief release for a breath/punch shape. Camera mode transition (centered → follow) — crossfade two camera modes via a 0→1 weight tween; intermediate frames interpolate between the modes' offsets.

**Values:** TARGET_OFFSET_Y should be measured via `getBoundingClientRect`, not a free parameter. TARGET_SCALE 1.3× modest → 1.6–2.0× typical → 3×+ (raster media needs source resolution ≥ rendered × TARGET_SCALE). ZOOM_START after content lands plus ~0.5s scan time. ZOOM_DUR 1.0–2.0s. DWELL at least 1.0s after the zoom settles. VIEWPORT_WIDTH is the composition's real pixel width.

**Critical constraints:** one `.world` wrapper carries the whole camera — every scene element lives inside it; a second transformed wrapper is a second camera. Single source of truth via the camera-state object plus the apply-camera writer — when scale and translate both change, write them in ONE place, never split them across tweens that touch the transform directly. The single-wrapper counter-translate is `T = -offset × S` — don't import the nested-wrapper `T = -offset` formula. `overflow: hidden` on the scene; `transform-origin: 50% 50%` on the world; background on the scene, never on the world.

**See also:** the Coordinate Target Zoom rule (nested-wrapper alternative, `T = -offset`); the Multi-Phase Camera rule (viewport-change inside one phase); the Sine Wave Loop rule (idle micro-drift after the viewport settles).

#### 3D Camera Flight

Every other camera rule described so far is a 2D camera — the Viewport Change, Multi-Phase Camera, and Coordinate Target Zoom rules simulate the camera with scale plus translate on a flat wrapper — the lens never tilts, and there's no depth axis to travel along. The 3D Page Scroll rule below is a static tilt — one angle held all scene while content scrolls inside. This rule is the missing camera that FLIES — dives into an angled grid, pulls back while the world rotates flat, streaks past standing cards, decelerates out of a blur into focus: a perspective camera traveling with `rotateX`/`rotateY`/`translateZ` through a 3D-laid-out world, under the same single-camera discipline as the Viewport Change rule: one perspective wrapper, one camera state object, one transform writer, every leg a sequenced tween on that state.

**How it works — five layers, strictly separated:**

1. **The lens** — `perspective: PERSPECTIVE_PX` on a static `.stage` wrapper, set once, never tweened, never moved. Changing perspective mid-shot reads as the lens itself warping, not the camera moving.
2. **The world** — a `.world` div with `transform-style: preserve-3d`, laid out at final 1× size: the ground surface (grid, form card, canvas) as flat DOM, optional props (a giant date number, a floating label) at static `translateZ` offsets so travel produces parallax, and standing cards counter-tilted to face the camera at their landing pose.
3. **The camera state** — a single object `cam = { x, y, z, rx, ry }` (the world's pose), written to the world's transform by ONE function, `applyCamera()`, in a fixed order: `translate3d(x, y, z) rotateX(rx) rotateY(ry)`. With translate composed OUTSIDE the rotations, x/y/z always move the world along screen axes no matter how it is currently tilted — pan is always sideways, z is always toward/away from the lens. Putting the rotations first would change what every leg's numbers mean as the tilt changes.
4. **The legs** — sequential tweens on `cam`, each one camera move: dive in (`power4.out` — violent arrival, sharp settle), tilt-to-flatten pull-back (`power2.inOut` — a repositioning, no slam), lateral flight, final dive. Camera intent inverts onto the world pose exactly as in the Viewport Change rule: camera flies in → world z increases (comes toward the lens); camera pans right → world x negative; camera tilts down over the surface → world rx positive (far edge tips away).
5. **Depth cues** — depth-of-field via the Depth-of-Field Blur rule below on the non-focal planes (cards, props — leaf elements, never the world itself), and velocity blur on travel legs via the Motion-Blur Streak rule's camera-travel carve-out — applied to the stage, never the world (a `filter` on a `preserve-3d` element flattens it).

Landing poses are authored, not derived: set `cam` to candidate values at design time, call `applyCamera()`, screenshot, adjust, bake the numbers as constants. There is no counter-translate formula to get wrong in 3D — the pose IS the design decision. Never measure per-frame (a live rect measurement in `onUpdate` desyncs under parallel frame sampling), and don't hand-derive 3D projections — your eye at design time beats the math.

```html
<!-- The lens: static perspective, nothing else. -->
<div class="stage">
  <!-- The world: preserve-3d, laid out at final 1× size; the camera flies by
       tweening THIS element's pose. Travel legs push content past the frame
       edges by design — hence a layout-overflow-allowed marker. -->
  <div class="world" id="world" data-layout-allow-overflow>
    <div class="surface">
      <div class="grid">{gridCells}</div>
      <div class="card layer" id="card-a" data-depth="0">{cardA}</div>
      <div class="card layer" id="card-b" data-depth="0">{cardB}</div>
    </div>
    <!-- Foreground props float at PROP_Z for parallax; they blur and fly past,
         never carry a read. -->
    <div class="prop layer" data-depth="2" style="--px: PROP_X; --py: PROP_Y">{propGlyph}</div>
  </div>
</div>
```

```css
.scene {
  overflow: hidden; /* travel legs push world content past the frame on purpose */
  background: {sceneBg}; /* the void the flight exposes at frame edges — must be a
     designed surface (deep brand color / soft gradient), never default white */
}
.stage {
  position: absolute;
  inset: 0;
  perspective: PERSPECTIVE_PX; /* THE LENS — static, never tweened */
  /* travel blur (motion-blur-streak carve-out) attaches HERE, never on .world */
}
.world {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
  transform-origin: 50% 50%;
  will-change: transform;
  /* keep CLEAN: no filter, opacity < 1, overflow, clip-path, or mask — each
     flattens preserve-3d. Background on .scene, blur on .stage or leaf cards. */
}
.surface {
  position: absolute;
  inset: WORLD_INSET; /* world runs larger than the frame so travel has runway */
  transform-style: preserve-3d;
}
.prop {
  position: absolute;
  left: var(--px);
  top: var(--py);
  /* static world-space pose; counter-tilt faces the camera at the dive pose */
  transform: translateZ(PROP_Z) rotateX(PROP_COUNTER_TILT);
}
.layer {
  --dof: 0px; /* DoF channel per depth-of-field-blur — leaf elements only */
  filter: blur(var(--dof));
  will-change: filter;
}
```

```js
const world = document.getElementById("world");

// Camera state — the ONLY source of truth for the world's pose. Every leg
// tweens this object; nothing else touches world.style.transform.
const cam = { x: 0, y: 0, z: WIDE_Z, rx: 0, ry: 0 };

function applyCamera() {
  // Fixed order: translate OUTSIDE the rotations → x/y/z stay screen-aligned
  // at any tilt. Changing this order changes what every baked pose means.
  world.style.transform = `translate3d(${cam.x}px, ${cam.y}px, ${cam.z}px) rotateX(${cam.rx}deg) rotateY(${cam.ry}deg)`;
}
applyCamera(); // seed frame 0 so a seek to t=0 renders the opening pose

// ── LEG 1 — DIVE IN: wide establishing pose → angled close-up on card A.
// fromTo states the opening pose explicitly; power4.out = violent arrival,
// razor-sharp settle. Travel blur: motion-blur-streak carve-out on .stage.
const DIVE_POSE = { x: DIVE_X, y: DIVE_Y, z: DIVE_Z, rx: DIVE_RX, ry: DIVE_RY };
tl.fromTo(
  cam,
  { x: 0, y: 0, z: WIDE_Z, rx: 0, ry: 0 },
  { ...DIVE_POSE, duration: DIVE_DUR, ease: "power4.out", onUpdate: applyCamera },
  DIVE_AT,
);
// Decelerate-INTO-FOCUS: non-focal planes' --dof ramps to BLUR_PER_DEPTH × data-depth
// on the SAME window/ease (depth-of-field-blur focal pull); card A stays at --dof: 0.

// ── LEG 2 — TILT-TO-FLATTEN PULL-BACK: every channel returns to neutral on ONE
// power2.inOut tween — a reposition, not a slam. DoF releases on the same window
// so the flat overview arrives fully crisp.
const FLAT_POSE = { x: 0, y: 0, z: 0, rx: 0, ry: 0 };
tl.to(
  cam,
  { ...FLAT_POSE, duration: FLATTEN_DUR, ease: "power2.inOut", onUpdate: applyCamera },
  FLATTEN_AT,
);
tl.to(".layer", { "--dof": "0px", duration: FLATTEN_DUR, ease: "power2.inOut" }, FLATTEN_AT);

// ── LEG 3 — LATERAL FLIGHT: screen-aligned pan (translate is outside the
// rotations, so x is a pure sideways move even mid-tilt).
tl.to(cam, { x: PAN_X, duration: PAN_DUR, ease: "power2.inOut", onUpdate: applyCamera }, PAN_AT);

// ── LEG 4 — FINAL DIVE onto card B: same grammar as leg 1; card A racks OUT of
// focus as card B racks in (depth-of-field-blur rack, shared window).
const LAND_POSE = { x: LAND_X, y: LAND_Y, z: LAND_Z, rx: LAND_RX, ry: LAND_RY };
tl.to(
  cam,
  { ...LAND_POSE, duration: LAND_DUR, ease: "power4.out", onUpdate: applyCamera },
  LAND_AT,
);
tl.to("#card-a", { "--dof": `${MAX_BLUR}px`, duration: LAND_DUR, ease: "power4.out" }, LAND_AT);
tl.to("#card-b", { "--dof": "0px", duration: LAND_DUR, ease: "power4.out" }, LAND_AT);
// Landing dwell: ≥1 s of stillness on card B — unless ending held mid-dive.
```

**Variations:** continuous flight past standing cards — one long leg instead of dive-land-dive: sustained z + x travel (2–4s, `power2.inOut`/`power1.inOut` near-constant cruise) through a corridor of cards and props at staggered `PROP_Z`. Parallax does the work — near props streak past while far ones crawl; keep ONE plane sharp at a time via staggered depth-of-field tweens. Props crossing the camera plane (as `cam.z + PROP_Z` approaches `PERSPECTIVE_PX`) blow up to fill the frame and vanish — that IS the fly-past; never let a focal card cross it. Ending held mid-dive — give the final leg a window that overruns the composition duration so the last frame holds mid-tween, still traveling, blur not fully resolved; seek-safe by construction (a seek to the last frame lands at a deterministic pose). A whip sweep drives leg 3 with the Nudge Curve rule's three-phase chain (burst-dominant) on `cam.x`, with the Motion-Blur Streak rule's camera-travel carve-out on the same window. A hold drift folds Multi-Phase-Camera-style micro-drift through the SAME writer — a driver tween writes tiny `dx`/`dy`/`drx` into a drift object and `applyCamera()` composes `cam.x + drift.dx` etc; never let drift write the transform itself — two writers on one transform is the classic camera bug.

**Values:** PERSPECTIVE_PX 700–1400px (moving-camera sweet spot 800–1200; smaller = wilder foreshortening, more violent dives; larger = near-orthographic, the flight flattens). WORLD_INSET −50% to −150% per side (world 2–4× the frame so lateral legs have runway). PROP_Z 80–300px (higher = stronger parallax, earlier fly-past). DIVE_RX/LAND_RX 30–55° ("angled grid" starts ~30°; keep |rx| ≤ ~65° and |ry| ≤ ~30° — beyond that flat planes go edge-on, text unreadable). DIVE_Z/LAND_Z 300–700px at a ~1000px perspective (the Z budget: `cam.z + PROP_Z ≤ ~0.6 × PERSPECTIVE_PX` for readable content — near the perspective distance, scale blows toward infinity and elements invert/vanish past the camera plane). WIDE_Z −100 to −400px (negative z = world pushed away = camera wide). DIVE_DUR/LAND_DUR 0.6–1.0s (commitment, not a polite zoom; under 0.5s reads as a cut). FLATTEN_DUR 1.2–2.0s (the repositioning is the breath between dives). PAN_DUR 0.8–1.5s plain, 0.5–0.8s for a whip. Ease law: `power4.out` on dives/landings, `power2.inOut` on repositioning/cruise (spring/back on a camera reads as the world wobbling on a string; four identical pushes read as a slideshow). Holds ≥0.8s between legs, final dwell ≥1s unless ending held mid-dive.

**Critical constraints:** one lens, one state, one writer — perspective on the static stage only (never on the world, never tweened); every leg tweens the single `cam` object; only `applyCamera()` writes the transform. Fixed transform order — translate outside the rotations; reorder it and every authored pose silently means something else. Keep the world CLEAN — `filter`, `opacity < 1`, `overflow` other than visible, `clip-path`, or `mask` on the world (or any intermediate wrapper) forces `transform-style: flat` and collapses every `translateZ` in the scene; travel blur goes on the stage, depth-of-field on leaf cards, fades on children, background on the scene. Camera intent inverts onto the world — same sign law as Viewport Change, two more axes to get right. Poses must be authored and baked, never measured per-frame or hand-derived projections. The first leg is a `fromTo` and `applyCamera()` runs once at setup so a seek to t=0 renders the exact establishing pose. Only sacrificial props may cross the camera plane. Reads happen at landings — angled, blurred, flying text is texture; anything the viewer must read gets a near-flat pose or a sharp held close-up ≥1s. `overflow: hidden` on the scene plus the layout-overflow-allowed marker on the world, since travel legs deliberately push panels past the frame.

**See also:** the Viewport Change rule (2D counterpart, same single-writer law — right when the shot never tilts); the Multi-Phase Camera rule (leg-sequencing grammar plus hold micro-drift); the Coordinate Target Zoom rule (aim math for a flat-hold zoom while rx/ry are 0); the Depth-of-Field Blur rule (non-focal defocus/racks); the Motion-Blur Streak rule (travel blur on the stage); the Nudge Curve rule (whip-sweep burst tuning); the 3D Page Scroll rule (static-tilt cousin — camera should NOT travel); the Orbit 3D Entry and Depth Scatter Assemble rules (elements moving under a still camera — the inverse; don't run both on one beat).

#### Depth-of-Field Blur (Selective Focus / Rack Focus)

Pulls the eye to one focal element by blurring (and slightly dimming) everything around it while the focal layer stays sharp — the camera's depth of field falling off the background, or a rack-focus shifting which plane is in focus. `filter` and `opacity` are paint-only, so both tween seek-safe.

**How it works:** every layer carries a blur custom property (px of blur), read by `filter: blur(var(--dof))`, plus its own opacity. A GSAP tween advances each layer's blur variable from 0 to its target and its opacity from 1 to a dim level over the focus-shift window. The focal layer's blur variable stays 0. Per-layer targets derive from a `data-depth` index, so the falloff is identical on every seek. Three mechanics share this one primitive: (1) focal pull — one window, off-focus layers go sharp→blurred while the focal layer holds at 0; (2) rack focus — two adjacent windows on the same property, plane A's blur ramps 0→max at the same position plane B's ramps max→0, with state continuity mattering exactly as in the Press-Release Spring rule (A's resting blur after the rack must equal what B held before it); (3) blur-the-cluster-while-pushing-in — the depth-of-field tween runs at the SAME timeline position as a camera push-in, so "the world recedes" and "we push in" read as one move.

```html
<div class="world" id="world">
  <!-- Focal layer — stays sharp -->
  <div class="layer focal" id="focal">{FocalLabel}</div>
  <!-- Off-focus layers — blur + dim; data-depth orders near→far -->
  <div class="layer ctx" data-depth="1">{Context A}</div>
  <div class="layer ctx" data-depth="2">{Context B}</div>
  <div class="layer ctx" data-depth="3">{Context C}</div>
</div>
```

```css
.world {
  /* single wrapper so a concurrent camera push-in transforms everything
     together; DoF is independent of the camera */
  position: relative;
  width: 100%;
  height: 100%;
  transform-origin: 50% 50%;
}
.layer {
  --dof: 0px; /* px of blur; filter reads it — starts sharp */
  filter: blur(var(--dof));
  will-change: filter; /* promotes the layer so per-frame re-rasterization is cheap */
}
.focal {
  z-index: 2; /* sharp layer must sit ABOVE the blurred ones, or its crisp
     edges read as bleeding into the haze */
}
.ctx {
  z-index: 1;
}
```

```js
// Mechanic 1 — FOCAL PULL. Blur scales with data-depth so far planes blur
// more than near ones; the focal layer (--dof: 0, opacity: 1) is untouched.
gsap.utils.toArray(".ctx").forEach((el) => {
  const depth = Number(el.dataset.depth) || 1;
  tl.to(
    el,
    {
      "--dof": `${BLUR_PER_DEPTH * depth}px`,
      opacity: DIM_LEVEL, // dim, not gone
      duration: FOCUS_DUR,
      ease: "power2.inOut",
    },
    FOCUS_START,
  );
});
```

**Variations:** rack focus between two depth planes — `gsap.set` plane B pre-blurred BEFORE the rack (no pop), then two tweens sharing the rack's start and duration: A → max blur + dim, B → 0px + full opacity, so they cross at the midpoint. Blur the cluster while pushing in — run the focal-pull tweens at the same position and duration as a camera tween on the world (scale/x/y, `power2.inOut`) — independent property channels, no conflict. Spotlight a hero metric in a card grid — all non-hero cards defocus (grid blur + dim level) on one shared window; heroes are skipped. Refocus/settle — if the beat resolves back to "everything visible," ramp all blur variables back to 0 with opacity back to 1 over the tail. A bounded focus-breathing on the focal layer (optional) is a finite driver writing a small sine-derived blur during a hold, kept ≤~0.6px or it reads as "still focusing" — default to omitting it.

**Values:** BLUR_PER_DEPTH 3–6px per depth step (a 3-plane stack tops out ~9–18px; low = gentle DoF, high = tilt-shift falloff). MAX_BLUR 8px soft → 16px default → 24px heavy (terminal blur for a fully-defocused plane; above ~24px on a big surface, shrink/group the layer instead). GRID_BLUR 6–12px. DIM_LEVEL 0.4 strong → 0.55 default → 0.7 subtle (rarely below 0.35 — fully dark reads as "removed," not "defocused"). FOCUS_DUR 0.5–1.2s (a rack/pull is a deliberate move, not a snap; shorter = snap focus, longer = languid). FOCAL_BREATH_PX ≤0.6px, period 2–3s. Focal vs context sizing: keeping the context layers smaller/grouped lets a modest blur radius still read as "out of focus" and stays cheap.

**Critical constraints:** tween the blur custom property on the timeline — reading `filter: blur(var(--dof))` keeps it on the seek clock. Blur the small/grouped layers, not the giant one — filter cost scales with radius × pixel area, so a large blur on a full-frame background is the worst case; keep per-layer radius ≤~24px on large surfaces and lean on the opacity dim to do the push-back work — dim plus modest blur reads more like real depth of field than blur cranked to the max. `will-change: filter` on every layer whose blur animates. The focal layer must stay genuinely sharp — untouched or breathing ≤0.6px; any visible blur on the focal element kills the "this is the thing" read. State continuity on a rack — the outgoing plane starts at the blur the incoming plane was holding, and vice versa. Depth of field is independent of the camera — blur the layers, transform the world for the push-in, don't fake one with the other. Settle sharp before a hand-off — refocus to 0 blur in the tail if the next beat is a crossfade/push. The sharp focal layer sits above blurred layers in z-index.

**See also:** the Multi-Phase Camera rule (the push-in this rule's falloff accompanies); the Coordinate Target Zoom rule (zoom onto the focal core); the Viewport Change rule (pan and rack across a tilted card plane); the Counting with Dynamic Scale rule (a hero metric counting up sharp); the 3D Page Scroll rule (the parallax stack to rack between); the Sine Wave Loop rule (post-rack idle; keep both amplitudes tiny).

### Layout & Network

#### Avatar Cloud Network

Avatars distributed on an elliptical ring connected by SVG dashed lines to a center hub — social-proof "community" reveal with staggered entry. Distinct from the Orbit 3D Entry rule below (continuous orbit): this settles into a static composed formation.

**How it works:** three layers — SVG lines (behind), avatars (middle), hub (in front — lines terminate AT its edge, never pass through). Avatar positions and lines are built once at setup from ONE shared center; the timeline then runs hub fade → avatar cascade → outward line draw → breathing dwell. Drawing FROM the center is the narrative: "the hub connects to its community."

```html
<svg class="lines" viewBox="0 0 1920 1080"><!-- lines injected --></svg>
<div class="hub-wrap">
  <div class="hub">{counterValue} {counterLabel}</div>
  <!-- avatars injected -->
</div>
```

```css
.lines {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}
.hub-wrap {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.hub {
  position: relative;
  z-index: 5;
}
.avatar {
  position: absolute;
  z-index: 2;
  transform: translate(-50%, -50%); /* centers on the (left, top) the script sets */
  will-change: transform, opacity;
}
```

```js
// CENTER_X/Y must equal the hub's RENDERED center exactly — every avatar
// position and line endpoint derives from it. For a place-items:center hub on
// a 1920×1080 canvas: (W/2, H × CENTER_Y_FACTOR).
const C = { x: CENTER_X, y: CENTER_Y };
const wrap = document.querySelector(".hub-wrap");
const svg = document.querySelector(".lines");

for (let i = 0; i < AVATAR_COUNT; i++) {
  const a = (i / AVATAR_COUNT) * Math.PI * 2 - Math.PI / 2; // start at top
  const x = C.x + Math.cos(a) * RADIUS_X;
  const y = C.y + Math.sin(a) * RADIUS_Y;

  const av = document.createElement("div");
  av.className = "avatar"; // assign image / glyph from authoring data
  av.style.left = `${x}px`;
  av.style.top = `${y}px`;
  wrap.appendChild(av);

  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  const attrs = {
    x1: C.x,
    y1: C.y,
    x2: x,
    y2: y,
    stroke: "{lineColor}",
    "stroke-dasharray": "6 8",
  };
  Object.entries(attrs).forEach(([k, v]) => line.setAttribute(k, String(v)));
  const len = Math.hypot(x - C.x, y - C.y); // straight line — Math.hypot, not getTotalLength()
  line.style.strokeDashoffset = String(len);
  svg.appendChild(line);
}

tl.from(".hub", { opacity: 0, scale: 0.8, duration: HUB_DUR, ease: `back.out(${HUB_BOUNCE})` }, 0);

const avatars = document.querySelectorAll(".avatar");
avatars.forEach((av, i) => {
  tl.from(
    av,
    { opacity: 0, scale: 0, duration: AVATAR_DUR, ease: `back.out(${AVATAR_BOUNCE})` },
    AVATAR_AT + i * AVATAR_STAGGER,
  );
});
svg.querySelectorAll("line").forEach((line, i) => {
  tl.to(
    line,
    { strokeDashoffset: 0, duration: LINE_DUR, ease: "power2.out" },
    LINES_AT + i * LINE_STAGGER,
  );
});

// Climax dwell — out-of-phase breathing holds the eye on the formed network:
// one phase proxy (0 → 2π·BREATH_CYCLES, ease "none"); onUpdate scales avatar i by
// 1 + sin(p + (i/n)·2π) · BREATH_AMP — sine-wave-loop's multiplicative onUpdate form.
// Keep the -50% centering in the same transform write.
```

**Variations:** size variety — vary avatar sizes by a small index-keyed array so the ring doesn't read rigidly repetitive. Solid lines — drop the dash and draw; lines fade in via opacity, more corporate, less networky. Multi-orbit — an inner ring (fewer, larger) connected to the hub; an outer ring is an unconnected "halo." Glyph avatars — flags/emoji/icons instead of faces, reading "global community" or role spread.

**Values:** AVATAR_COUNT 8–12 (fewer feels sparse; more clutters the ellipse). RADIUS_X/Y ~20–30% of width / ~18–25% of height (ratio X/Y 1.5–3.0 reads as perspective, 1 reads flat). Avatar size 80–120px @1920 (ring must fit 10+ without overlap). HUB_DUR 0.4–0.6s, HUB_BOUNCE 1.4–1.8. AVATAR_AT at least 0.6× HUB_DUR (hub established before satellites arrive). AVATAR_DUR 0.4–0.7s, AVATAR_BOUNCE 1.4–1.8 slightly firmer than the hub. AVATAR_STAGGER 0.06–0.10s (cascade reads "joining," simultaneous reads "already there"). LINES_AT overlaps the last avatar's settle, starting ~0.1–0.2s before it. LINE_DUR 0.4–0.7s, LINE_STAGGER 0.02–0.05s = a wave outward. BREATH_CYCLES 1.0–2.0 over the remaining seconds (under 1 = single sigh, over 2 = anxious); BREATH_AMP 0.02–0.06.

**Critical constraints:** CENTER_X/Y must match the hub's actual rendered center — when composed with another scene, bake them from the same source as the hub's final position, or lines visibly miss it. The hub's z-index must sit above the lines, since lines terminate at its edge and never cross it. Lines draw outward (dashoffset length → 0), starting after avatars are mostly settled. RADIUS_X should exceed RADIUS_Y (a horizontal ellipse reads as perspective; a circle reads flat). Climax dwell should be at least 1s after lines complete. For straight lines, use `Math.hypot` for length — `getTotalLength()` isn't needed.

**See also:** the Counting with Dynamic Scale rule (the hub IS a growing counter); the Sine Wave Loop rule (the breathing form); the Orbit 3D Entry rule (the continuously-orbiting cousin).

#### 3D Page Scroll

A webpage (or long content) presented as a tilted 3D card. Spring-eased scroll reveals specific sections while a static 3D perspective adds physical depth. (For a camera that actually travels/tilts, see the 3D Camera Flight rule above — this rule's tilt never moves.)

**How it works:** two independent transforms combine — (1) a static 3D tilt (`rotateY` + `rotateX` with `perspective` on the card; the angle does not change during the scene) and (2) scroll (the content inside the card translates vertically within a clipped container, with spring-like deceleration via `power3.out`/`power4.out`). An optional spotlight overlay is a radial-gradient mask that dims everything except a focal region after the scroll lands — it sits above the scrolling content, fixed relative to the card, never inside the scrolling layer.

```html
<div class="tilt-card">
  <div class="page-content">
    <!-- Full {Brand} webpage recreation, taller than the card so scrolling
         matters. Each section is REAL DOM, not a screenshot — screenshots
         can't be individually highlighted or scrolled-to with precision. -->
    <section class="page-hero">{heroContents}</section>
    <section class="page-features">{featuresContents}</section>
    <section class="page-target" id="target-section">{targetContents}</section>
    <section class="page-cta">{ctaContents}</section>
  </div>
  <div class="spotlight"></div>
</div>
```

```css
.tilt-card {
  position: absolute;
  left: 50%;
  top: 50%;
  /* tilt + perspective in CSS only if no other transform tween touches this
     element — if GSAP also tweens scale on .tilt-card, set the tilt via
     gsap.set() instead to avoid matrix overwrites */
  transform: translate(-50%, -50%) perspective({perspectivePx}) rotateY({tiltYDeg}) rotateX({tiltXDeg});
  transform-style: preserve-3d;
  width: {cardWidth};
  height: {cardHeight};
  border-radius: 24px;
  background: {cardBackgroundColor};
  overflow: hidden; /* clip the scrolling content at the rounded corners */
  /* shadow X-offset sign must match tiltY sign (negative tiltY ⇒ positive X) */
  box-shadow: 40px 30px 80px rgba(0, 0, 0, 0.45);
}
.page-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  /* height intrinsic from sections — taller than the card */
}
.spotlight {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  background: radial-gradient(ellipse 60% 35% at 50% 50%, transparent 50%, {spotlightDimColor} 100%);
}
```

```js
// SCROLL_DISTANCE is measured at design time from the real page layout
// (top of .page-content origin to vertical center of #target-section,
// accounting for card height) — NOT a free tunable.
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT,
);

// Spotlight fades in on the target after the scroll settles.
tl.to(
  ".spotlight",
  { opacity: 1, duration: SPOTLIGHT_FADE_DUR, ease: "power1.inOut" },
  SPOTLIGHT_AT,
);
```

**Variation — multi-step scroll (scroll → pause → scroll):** multiple `y:` tweens at different positions, both distances measured from the page-content origin (not delta from the previous step) — GSAP composes successive tweens on the same property, each starting where the previous one left off:

```js
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_A, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_A,
);
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_B, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_B,
);
// SCROLL_AT_A + SCROLL_DUR ≤ SCROLL_AT_B — the two scrolls must not fight for y
```

**Values:** tiltYDeg −12 to −4 (left-leaning) or 4 to 12 (bigger = more dramatic 3D; near 0 collapses to a flat panel). tiltXDeg 0–6 (positive tilts the top edge away). perspectivePx 800–2000px (smaller = more foreshortening, larger = nearly orthographic). Card width/height less than the total content height (otherwise the scroll has nothing to reveal). Section heights should sum to at least the card height plus scroll distance, so the target section lands within frame. SCROLL_AT at or after the end of any prior tweens on the page content. SCROLL_DUR 0.8–1.8s (shorter feels like a hard cut, longer feels programmatic). SCROLL_DISTANCE must be measured from the real layout — actual cumulative section heights, never estimated, never overshooting content end. SPOTLIGHT_AT at or slightly before scroll end. SPOTLIGHT_FADE_DUR 0.4–0.8s. Ease: `power3.out` default, `power4.out` for momentum, `power2.inOut` for a cinematic pan — pick ONE for all scrolls in a scene.

**Critical constraints:** the tilt is static — the card holds its angle the whole scene. Shadow direction must match the tilt — a left-leaning card casts a shadow to the right; a mismatch breaks the 3D illusion. Page content is real HTML, not a screenshot, and scroll distances come from the real layout geometry. `overflow: hidden` plus `transform-style: preserve-3d` on the card, to clip at the rounded corners and support clean perspective composition. The spotlight is an overlay above the scrolling content, never inside it. Use the same easing across a multi-phase scroll, and non-overlapping scroll windows.

**See also:** the ASR Keyword Glow rule (on-page keyword highlight synced to voiceover); the Multi-Phase Camera rule (camera zoom while the page scrolls); the Cursor-Click Ripple rule (cursor lands in the scrolled-into-view section); the 3D Camera Flight rule (when the camera itself should travel).

#### Center-Outward Expansion

Elements begin at one shared center point and radiate outward to their final positions — the entry beat itself, or motion driven by another animation's progress (a counting number, a beat). Flat 2D cousin of the Depth Scatter Assemble rule below (per-element 3D cloud): here every element shares the SAME origin.

**How it works:** each element carries its final offset as data attributes. Its position lerps between center and target: `x = targetX × progress`. Self-centering is baked as `xPercent`/`yPercent: -50` so the tweened `x`/`y` are pure offsets from the stage center. Standalone burst = per-item staggered `fromTo`; driven burst = one shared proxy (see Variations).

```html
<div class="burst-wrap">
  <div class="burst-item" data-target-x="-360" data-target-y="-180">{itemA}</div>
  <div class="burst-item" data-target-x="360" data-target-y="-180">{itemB}</div>
  <div class="burst-item" data-target-x="0" data-target-y="360">{itemC}</div>
</div>
```

```css
.burst-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}
.burst-item {
  position: absolute;
  top: 50%;
  left: 50%; /* GSAP xPercent/yPercent -50 bakes the centering; x/y tween the offset */
  will-change: transform;
}
```

```js
document.querySelectorAll(".burst-item").forEach((el, i) => {
  tl.fromTo(
    el,
    { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 0.6, opacity: 0 },
    {
      x: Number(el.dataset.targetX),
      y: Number(el.dataset.targetY),
      scale: 1,
      opacity: 1,
      duration: EXPAND_DUR,
      ease: EXPAND_EASE,
    },
    ENTRY_AT + i * STAGGER,
  );
});
```

**Variations:** synced to a driver (chord) — when the burst shadows a counter or a beat, drop the stagger and drive all items from ONE 0→1 proxy tween with the driver's exact duration AND ease; `onUpdate` writes a translate offset of `targetX × p, targetY × p` per item so the two read as one beat. A partially-spread start avoids full pile-up with 6+ items by starting from a fraction of the target offset. Idle micro-float can hand off to the Sine Wave Loop rule below after landing instead of freezing.

**Values:** ITEM_COUNT 3–8 (more than 8 = visual chaos mid-expansion; low counts want a wider spread). EXPAND_DUR 1.0–1.8s, must equal the driver's duration in the synced variant. EXPAND_EASE `power3.out` default, `power2.out` gentler, `expo.out` dramatic stop — NEVER `in` eases. STAGGER 0.04–0.08s (tighter = chord, looser = lazy arpeggio). ENTRY_AT 0–0.5s (a beat of compositional quiet before the burst). START_PROGRESS 0–0.5 (0 = dramatic full cluster, ~0.3 avoids the pile-up).

**Critical constraints:** tween `x`/`y` over the baked `xPercent`/`yPercent: -50` — mutating `left`/`top` fights the centering and causes pixel jitter. Out-easing only — `in` easings read as items being sucked back mid-air. No other absolute-positioned siblings inside the burst wrap, or they'd steal the centered baseline. The burst IS the beat — don't park a "real headline" label below it (the eye snaps to the label and ignores the burst); if a label is needed, reveal it post-burst in the same stack. The synced variant needs identical duration and ease as the driver, or the chord falls apart.

**See also:** the Counting with Dynamic Scale rule (the classic chord driver); the Depth Scatter Assemble rule (3D per-element cloud); the Card Morph Anchor rule (burst out of a morphed card); the Sine Wave Loop rule (post-landing life).

#### Split Tilt Cards

Two cards side-by-side with opposing Y-rotation, creating a symmetric "book-open" 3D split for comparisons, before/after, or feature pairs. Each card slides in from its own side (reinforcing "they came from their own worlds and met here"), then the pair idles in counter-phase.

**How it works:** `perspective` on the scene root (REQUIRED — without it `rotateY` flattens to a 2D layout) and `transform-style: preserve-3d` on the stage and both cards. Entry starts each card off-axis with a tilt plus overshoot, settling to the resting tilt — a pivot-into-place. Idle is a gentle counter-phase Y-bob (the two yoyo tweens run in opposite directions); copy fades up during the cards' settle, not after.

```html
<div class="split-stage">
  <div class="card card-left">
    <div class="card-eyebrow">{leftEyebrow}</div>
    <div class="card-headline">{leftHeadline}</div>
    <div class="card-body">{leftBody}</div>
  </div>
  <div class="card card-right">…</div>
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: SCENE_PERSPECTIVE; /* REQUIRED */
}
.split-stage {
  display: flex;
  gap: STAGE_GAP;
  transform-style: preserve-3d;
}
.card {
  width: CARD_WIDTH;
  transform-style: preserve-3d;
  will-change: transform;
}
/* Shadow falls WITH the facing direction: left card faces right → shadow right. */
.card-left {
  box-shadow: -CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
.card-right {
  box-shadow: CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
```

```js
// Entry — from outside, opposing tilts settle with a small pivot
tl.fromTo(
  ".card-left",
  { x: -ENTRY_SLIDE_DIST, rotateY: TILT + TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  LEFT_AT,
);
tl.fromTo(
  ".card-right",
  { x: ENTRY_SLIDE_DIST, rotateY: -TILT - TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: -TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  RIGHT_AT,
);

// Counter-phase idle bob — opposite signs = alive; synchronized = conveyor belt
tl.to(
  ".card-left",
  { y: -FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);
tl.to(
  ".card-right",
  { y: FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);

// Copy fades up during the settle
tl.from(
  ".card-eyebrow, .card-headline, .card-body",
  { opacity: 0, y: COPY_RISE, stagger: COPY_STAGGER, duration: COPY_DUR, ease: "power2.out" },
  COPY_REVEAL_AT,
);
```

**Variations:** badges/floating labels must be positioned on the PARENT, never inside a card, or they'd inherit its `rotateY` and tilt off-axis. Three-plus cards can keep the center card flat (`rotateY: 0`) with the outer two tilting inward ("old way / nothing / our way"). A zoom-through — a separate camera tween scaling the stage — reads as the viewer crossing the gap between the tilted pair.

**Values:** SCENE_PERSPECTIVE 1000–2400px (lower exaggerates the tilt, higher reads near-isometric). TILT 10–18° (under 10 reads almost flat, over 18 folds shut and copy blurs). TILT_OVERSHOOT 4–12° for the pivot-into-place feel. STAGE_GAP 40–120px, roughly 0.06–0.15× CARD_WIDTH (small = fused pair, large = compared-but-separate). CARD_WIDTH 480–820px @1920 (2× card width plus gap should be ≤ 0.95× the stage at full tilt). ENTRY_SLIDE_DIST 200–500px, roughly 0.3–0.6× CARD_WIDTH. ENTRY_DUR 0.6–1.2s. RIGHT_AT is LEFT_AT plus 0–0.3s (zero feels mechanical, large fragments the pair). FLOAT_AMP 3–8px (subtle is the point). FLOAT_DURATION 1.6–3.2s round trip (breathing cadence; IDLE_START must be ≥ the entry's end). COPY_REVEAL_AT during the entry tail (copy popping in after cards are already idle reads disconnected).

**Critical constraints:** `perspective` on the scene root is REQUIRED; `preserve-3d` on the stage AND each card. Shadow direction must match tilt (left card faces right → shadow falls right, mirrored) — a wrong sign reads as broken 3D. Idle must be counter-phase — the two bobs run with opposite signs at the same position. Badges belong outside the card divs. Body copy should be at most 2 lines per card — tilted long paragraphs collapse into perspective blur. Symmetric weight — same width, same vertical center, similar line counts, or asymmetry breaks the comparison metaphor.

**See also:** the Card Morph Anchor rule (the pair can morph into one unified shape afterward); the Counting with Dynamic Scale rule (numbers as each side's headline); the Sine Wave Loop rule (the idle form).

#### Orbit with 3D Entry

Elements flip in from 3D space (`rotateX` + `rotateY` + negative z) then settle into a continuous elliptical orbit around a center label. Distinct from one-shot reveals — the orbit keeps running, driven by a 0→1 progress tween INSIDE the timeline (never `requestAnimationFrame`).

**How it works:** per element, two phases — (1) a `back.out` flip from a hidden 3D orientation to flat, IN PLACE at its orbital starting position (see Critical Constraints); (2) a continuous orbit where `onUpdate` computes x/y from `cos`/`sin(initialAngle + p·2π)` on the ellipse. The stage needs `perspective` on the scene root and `preserve-3d` on the stage and items, or the flip flattens to a 2D scale.

```html
<div class="orbit-stage">
  <div class="orbit-item" data-angle="0">{glyph1}</div>
  <div class="orbit-item" data-angle="60">{glyph2}</div>
  <!-- … evenly-spaced angles … -->
  <div class="orbit-center">{centerLabel}</div>
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: 1800px; /* REQUIRED */
}
.orbit-stage {
  position: relative;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
}
.orbit-item {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-style: preserve-3d;
  will-change: transform;
}
.orbit-center {
  position: relative;
  transform: translateZ(220px); /* wins paint order inside preserve-3d */
  z-index: 9999;
}
```

```js
const items = document.querySelectorAll(".orbit-item");
const RADIUS_Y = RADIUS_X * Y_TO_X_RATIO; // perspective-flattened ellipse

items.forEach((el, i) => {
  const a0 = (Number(el.dataset.angle) / 360) * Math.PI * 2;
  const startX = Math.cos(a0) * RADIUS_X;
  const startY = Math.sin(a0) * RADIUS_Y;

  // 1) Park at the orbital position, hidden — BEFORE any tween fires
  gsap.set(el, {
    xPercent: -50,
    yPercent: -50,
    x: startX,
    y: startY,
    rotateX: ROTATE_X_FROM,
    rotateY: ROTATE_Y_FROM,
    z: Z_FROM,
    opacity: 0,
    scale: SCALE_FROM,
  });

  // 2) Flip in IN PLACE — rotation/opacity/scale only, never translate
  tl.to(
    el,
    {
      rotateX: 0,
      rotateY: 0,
      z: 0,
      opacity: 1,
      scale: 1,
      duration: ENTRY_DUR,
      ease: `back.out(${FLIP_BACK})`,
    },
    i * STAGGER,
  );

  // 3) Continuous orbit — each item gets its OWN progress tween (own initialAngle)
  const orbit = { p: 0 };
  tl.to(
    orbit,
    {
      p: 1,
      duration: ORBIT_DURATION,
      ease: "none",
      onUpdate: () => {
        const a = a0 + orbit.p * Math.PI * 2;
        const x = Math.cos(a) * RADIUS_X;
        const y = Math.sin(a) * RADIUS_Y;
        // capped z-index band [1, 50] — see center-label clearance below
        el.style.zIndex = String(1 + Math.round(((y + RADIUS_Y) / (2 * RADIUS_Y)) * 49));
        el.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
      },
    },
    i * STAGGER + ENTRY_DUR,
  );
});

tl.from(
  ".orbit-center",
  { opacity: 0, scale: 0.6, duration: ENTRY_DUR, ease: `back.out(${CENTER_BACK})` },
  CENTER_FADE_AT,
);
```

**Variations:** a collapse-to-center variant multiplies both radii (and item scale) from a final 1→0 driver in `onUpdate`, so the ring condenses into the center element — pairs with a CTA "click" igniting the collapse. A tilted orbit plane adds `rotateX(25deg)` to the stage so items visibly arc through the plane.

**Values:** RADIUS_X 300–900px (must also clear the center label horizontally — see below). Y_TO_X_RATIO 0.4–0.7 (keep under 1 — a tilted ring, not a frontal halo). ORBIT_DURATION 4–25s per revolution — must be at least the time on screen, or the tween ends and items freeze. ENTRY_DUR 0.4–0.8s. STAGGER 0.06–0.12s (below reads "popcorn," above reads plodding). FLIP_BACK/CENTER_BACK 1.2–2.0 / 1.2–1.8 (calm the center pop if both fire close together). CENTER_FADE_AT after 2–4 items land (too early competes, too late leaves a hole). ROTATE_X/Y_FROM, Z_FROM ±60–120°, ±45–120°, −200 to −400 (one consistent rotation direction across items — mixed signs read as noise). SCALE_FROM 0.2–0.6. Item count 4–12 (fewer feels empty, more crowds the center).

**Critical constraints:** entry must flip IN PLACE at the orbital position, NOT at center — set each item's transform at its `cos(a0)·RADIUS_X, sin(a0)·RADIUS_Y` position with opacity 0 BEFORE adding tweens, then phase 1 animates only rotation/opacity/scale. A `fromTo` that keeps x/y at 0 would flip at the stage center, collide with the center label, then teleport to the orbit when phase 2 starts. Center-label clearance is critical — z-index alone is unreliable inside `preserve-3d` (paint order follows actual Z), so push the label forward with a `translateZ` offset plus a very high z-index, cap item z-index to a [1, 50] band, and size the ring so items clear the label horizontally at every angle (a heavier wordmark needs a wider ring). Each item must get its OWN orbit tween — a shared selector-based tween can't carry per-item initial angle. The center element is the headline — the orbit is ornament; if it dominates, grow the center or fade the items down.

**See also:** the Center-Outward Expansion rule (burst entry; a reversed driver becomes the collapse finish); the Cursor-Click Ripple rule (the click that triggers a collapse); the Depth Scatter Assemble rule (a 3D entrance that resolves flat instead of orbiting).

#### AI Tracking Box

An animated bounding box of four L-bracket corner markers plus a confidence label that follows a moving target, simulating real-time AI object detection. Rendered in detection yellow on a dark background — the industry convention (autonomous-vehicle HUDs, security computer vision, ML demos) — red reads "warning," green "success," blue "info," none of which read "detection."

**How it works:** ONE `ease: "none"` driver tween advances a phase; its `onUpdate` computes the TARGET's position from trig, then derives the box's position/size FROM the target — every frame, in that order. The box never gets its own position tween: if it trails the target it reads as a broken tracker, not a smart AI. Size jitters a few percent off-tempo (a non-integer frequency multiple) to mimic continuous re-fitting, and the confidence label flickers inside a tight band around 95–99%.

```html
<div class="bg-mascot" id="mascot">{targetGlyph}</div>
<div class="track-box" id="track-box">
  <div class="corner tl"></div>
  <div class="corner tr"></div>
  <div class="corner bl"></div>
  <div class="corner br"></div>
  <div class="label" id="label">{LABEL} · {confidence}%</div>
</div>
```

```css
.track-box {
  position: absolute; /* position + size written by the driver's onUpdate */
  pointer-events: none;
  will-change: transform, width, height;
}
.corner {
  position: absolute;
  width: 48px;
  height: 48px;
}
/* Each corner draws only its two outer borders — .tr/.bl/.br mirror this: */
.corner.tl {
  top: -8px;
  left: -8px;
  border-top: 6px solid {detectionYellow};
  border-left: 6px solid {detectionYellow};
}
.label {
  position: absolute;
  top: -56px;
  left: -8px;
  background: {detectionYellow};
  color: {labelTextColor}; /* near-black on yellow */
  font-family: {monoFont}; /* mono = machine readout */
  white-space: nowrap;
}
```

```js
const box = document.getElementById("track-box");
const mascot = document.getElementById("mascot");
const label = document.getElementById("label");
const C = { x: COMP_WIDTH / 2, y: COMP_HEIGHT / 2 };

// Entry — the AI "locks on"
gsap.set(box, { opacity: 0, scale: ENTRY_SCALE });
tl.to(
  box,
  { opacity: 1, scale: 1, duration: ENTRY_DUR, ease: `back.out(${ENTRY_BOUNCE})` },
  ENTRY_START,
);

// Tracking — target first, box derived from it, every frame
const tracking = { p: 0 };
tl.to(
  tracking,
  {
    p: Math.PI * 2 * CYCLES,
    duration: TRACK_DUR,
    ease: "none",
    onUpdate: () => {
      const mx = C.x + Math.cos(tracking.p) * DRIFT_X;
      const my = C.y + Math.sin(tracking.p) * DRIFT_Y;
      mascot.style.left = `${mx - MASCOT_SIZE / 2}px`;
      mascot.style.top = `${my - MASCOT_SIZE / 2}px`;

      const w = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT) * SIZE_VAR;
      const h = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT + Math.PI / 2) * SIZE_VAR;
      box.style.width = `${w}px`;
      box.style.height = `${h}px`;
      box.style.left = `${mx - w / 2}px`;
      box.style.top = `${my - h / 2}px`;

      const conf = Math.round(
        CONFIDENCE_MEAN + Math.sin(tracking.p * CONFIDENCE_FREQ_MULT) * CONFIDENCE_VAR,
      );
      label.textContent = `${LABEL_TEXT} · ${conf}%`;
    },
  },
  TRACK_START,
);
```

**Variations:** multi-object tracking uses one driver per box/target pair with phases offset by π/N so they don't tick synchronously. A lost-then-reacquired variant fades the box to ~0.2–0.4 opacity, then re-snaps with a harder overshoot and flashes a "REACQUIRED" label via `tl.set`. A tracking-then-zoom hands off to the Viewport Change rule above — "the AI found something, now show it."

**Values:** ENTRY_SCALE 0.5–0.9 (below 1 — the box snaps UP into focus). ENTRY_DUR/BOUNCE 0.3–0.8s / 1.2–2.5, `back.out` only (elastic reads cartoonish, power reads flat). TRACK_START at or after entry end (a gap = pause for emphasis; none = seamless lock and follow). TRACK_DUR 2–8s, at least one full cycle or the drift never reads as oscillation. CYCLES 0.5–3 (keep the effective rate under ~0.6Hz or the motion blurs). DRIFT_X/Y 40–200px (center ± drift must keep the target fully on screen). SIZE_BASE 200–500px (must visibly enclose the target at all jitter sizes). SIZE_VAR 5–10% of SIZE_BASE (more reads broken, none reads like a static screenshot; keep under 0.15×). SIZE_FREQ_MULT 1.5–3, non-integer (integer ratios pulse in lock-step with drift, which reads mechanical). CONFIDENCE_MEAN/VAR 95–99 / 1–3 (mean ± var should stay within 95–99; under 95 reads "uncertain," 100 reads "fake-precise"; 97 is the sweet spot). CONFIDENCE_FREQ_MULT 3–6, greater than SIZE_FREQ_MULT so the label flickers faster than the box breathes. MASCOT_SIZE must equal the rendered target size, or the target drifts out of the box.

**Critical constraints:** the box is recomputed per-frame FROM the target — one driver computes the target position, then the box derives from it in the same `onUpdate`; never tween the box's position separately. Corner L-brackets, not a full border, are the genre signature — a full border reads as a generic UI box. Yellow-on-dark is the convention; substituting another hue loses genre legibility. Confidence should flicker in a tight band inside 95–99, in a mono font. `pointer-events: none` on the box, since it's a decorative overlay.

**See also:** the Viewport Change rule (zoom into the detection); the Multi-Phase Camera rule (wide during tracking, push-in on lock); the Sine Wave Loop rule (the target idle-breathes inside the box).

#### Depth Scatter ↔ Assemble

N elements (glyphs, cards, logo fragments) fly in from a rotating 3D depth-cloud and lock into a flat layout — or the reverse. Each element has its OWN index-derived point in the cloud (translateZ depth plus rotateX/Y tumble plus x/y scatter). Distinct from the Orbit 3D Entry rule (flip-in then continuous orbit) and the Center-Outward Expansion rule (flat burst from one shared center): here the resolve is a flat assembled layout.

**How it works:** each element's flat target lives in data attributes; its scattered state is pure trig on its index — a golden-angle spread, stepped depth — so the cloud is byte-identical every render with no `Math.random`:

```js
const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 rad — even spread, no clumping
const a = i * GOLDEN;
const scatterX = Math.cos(a) * RADIUS;
const scatterY = Math.sin(a) * RADIUS;
const scatterZ = Z_NEAR - (i / (n - 1)) * (Z_NEAR - Z_FAR); // stepped depth
const rotX = Math.sin(a) * TUMBLE;
const rotY = Math.cos(a) * TUMBLE;
```

Elements are PARKED at their scatter points (`gsap.set`, opacity 0) before any tween, then each tweens to its flat target while the whole stage slowly rotates so the scatter has life before it locks. Requires `perspective` on the scene root and `preserve-3d` on the stage AND each element, or depth plus tumble flatten to a 2D scale.

```html
<div class="cloud-stage">
  <div class="frag" data-target-x="-260" data-target-y="0">{glyph1}</div>
  <div class="frag" data-target-x="-130" data-target-y="0">{glyph2}</div>
  <!-- … one .frag per glyph / fragment … -->
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: 1400px; /* REQUIRED */
}
.cloud-stage {
  position: relative;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
  will-change: transform;
}
.frag {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-style: preserve-3d;
  backface-visibility: hidden; /* hides the mirrored face mid-tumble */
  will-change: transform, opacity;
}
```

```js
const frags = Array.from(document.querySelectorAll(".frag"));
const n = frags.length;
const GOLDEN = Math.PI * (3 - Math.sqrt(5));

// 1) Park every fragment in the cloud BEFORE any tween fires
const scatter = frags.map((el, i) => {
  const a = i * GOLDEN;
  const depthT = n > 1 ? i / (n - 1) : 0;
  return {
    x: Math.cos(a) * RADIUS,
    y: Math.sin(a) * RADIUS,
    z: Z_NEAR - depthT * (Z_NEAR - Z_FAR),
    rotationX: Math.sin(a) * TUMBLE,
    rotationY: Math.cos(a) * TUMBLE,
  };
});
frags.forEach((el, i) => gsap.set(el, { xPercent: -50, yPercent: -50, ...scatter[i], opacity: 0 }));

// 2) The cloud rotates so the scatter has life during assembly
tl.to(
  ".cloud-stage",
  { rotationY: CLOUD_SPIN_DEG, duration: CLOUD_SPIN_DUR, ease: "power1.out" },
  0,
);

// 3) ASSEMBLE — cloud point → flat target, index stagger = cloud collapsing inward
frags.forEach((el, i) => {
  tl.to(
    el,
    {
      x: Number(el.dataset.targetX),
      y: Number(el.dataset.targetY),
      z: 0,
      rotationX: 0,
      rotationY: 0,
      opacity: 1,
      duration: ASSEMBLE_DUR,
      ease: ASSEMBLE_EASE,
    },
    i * STAGGER,
  );
});
```

**Variations:** a tumble-swap (the beat-change hand-off) has two glyph sets share the cloud with ONE shared 0→1 progress tween driving both in its `onUpdate` — outgoing lerps layout→cloud with fading opacity, incoming lerps cloud→layout with rising opacity; two separate tweens drift out of phase under seek and the cross stops reading as one hand-off. A radial letter-explode → resolve is a flat-plane special case (Z_NEAR = Z_FAR = 0, small tumble) — reverse the assemble for the explode, pure in-plane. Scatter-OUT reverses the assemble (layout → cloud, opacity 1→0) ONLY as the composition's final beat — mid-shot it reads as the shot ending. A parallax lockup gives back layers deeper Z and longer assemble duration, foreground shallower/shorter, for a depth-speeded slide-in that locks into a logo.

**Values:** n 4–14 (fragments 4–9 is the sweet spot — above ~14 individual paths stop reading). RADIUS 250–700px (keep the farthest scatter in frame or fragments pop in with no travel). Z_NEAR/Z_FAR +150…+450 / −150…−500 (large |z| needs a wider perspective or fragments smear). TUMBLE 40–110° (past 90° glyphs show blank mid-tween by design; cap ~80° for one-faced cards). ASSEMBLE_DUR 0.7–1.4s. ASSEMBLE_EASE `power3.out` default (`expo.out` snaps, `back.out(1.4)` seats with overshoot — never `in`). STAGGER 0.03–0.09s (item count × stagger should be under ASSEMBLE_DUR — one collapsing motion, not a queue). CLOUD_SPIN_DEG/DUR 15–60° over at least the assemble duration (gentle life — too fast competes with the assembly). SWAP_DUR 0.5–1.0s on the beat boundary (shorter = a harder cross).

**Critical constraints:** every scattered value is index-derived — `cos`/`sin(i × GOLDEN)` plus stepped z, spreading points evenly with no clumps and no `Math.random`. `gsap.set` the cloud BEFORE adding tweens, or frame 0 shows the assembled layout followed by a teleport when the first tween starts. `perspective` plus `preserve-3d` are needed on the stage AND each fragment — missing any one flattens the depth. Resolve flat — the settled state is z=0, rotations 0; a still-tilted resolve reads unfinished. A tumble-swap needs one shared progress for both glyph sets. Depth ordering is automatic inside `preserve-3d` (paint order follows actual Z) — no manual z-index needed, unlike the orbit rule's capped band.

**See also:** the Orbit 3D Entry rule (settles into a continuous orbit instead); the Hacker Flip 3D Reveal rule (glyphs decode on arrival); the 3D Text Depth Layers rule (extrude the locked wordmark); the Center-Outward Expansion rule (flat 2D cousin); the Sine Wave Loop rule (idle breathe on the resolved layout).

#### Anchored Layout Expand

> The law: author the layout at its final (expanded) state in CSS, then fake the collapsed state with transforms. The container never changes size — the visible region does — and everything downstream rides a matched translate. The browser computes layout ONCE; every intermediate frame is pure transform.

THE one-axis growth primitive: a container pinned at one edge appears to grow along a single axis, and the in-flow content after it moves in perfect contact with the traveling edge — a dropdown, a sub-task stack, a growing composer card, a pane widening over a neighbor. Growth and push are ONE motion: if the panel's bottom edge and the pushed content ever separate or overlap, the illusion dies.

Distinct from the Card Morph Anchor rule below (a free-floating two-shot morph with no neighbors to push — this rule's container is a live layout participant), the Spring-Pop Entrance rule below (arrival at a point, no edge travel or reflow), and the Reactive Displacement rule below (displacement by a colliding intruder — here content moves because the container's edge reached it, layout causality rather than collision).

**How it works:** (1) mask — a wrapper at the final body height, `overflow: hidden`, never tweened. (2) Sheet — the panel surface plus content inside the mask, starting tucked above the mask window (behind the pinned header). (3) Below — ONE wrapper holding everything after the container, also starting tucked away. (4) Grow — ONE `fromTo` drives sheet AND below from tucked to zero offset. Shared tween ⇒ the descending bottom edge and the pushed content stay in exact contact by construction. Collapse is the same pair tweened back.

When the surface must visibly stretch in place (rows revealed top-first, or a pane growing sideways), use the proxy counter-scale variant below instead.

```html
<div class="stack">
  <div class="expander">
    <div class="expander-head">{headerLabel}</div>
    <div class="expand-mask" id="expand-mask" data-layout-allow-overflow>
      <div class="expand-sheet" id="expand-sheet">
        <div class="expand-row">{rowA}</div>
        <div class="expand-row">{rowB}</div>
      </div>
    </div>
  </div>
  <!-- EVERYTHING that must be pushed lives in this one wrapper -->
  <div class="below" id="below">{followingContent}</div>
</div>
```

```css
/* Layout is the EXPANDED end state — no collapsed geometry exists in CSS. */
.expander-head {
  position: relative;
  z-index: 2; /* the sheet slides out from UNDER the header */
}
.expand-mask {
  height: BODY_H; /* authored final height — NEVER tweened */
  overflow: hidden;
}
.expand-sheet {
  height: BODY_H;
  border-radius: 0 0 SHEET_RADIUS SHEET_RADIUS; /* bottom-only — header + sheet read as one grown card */
  will-change: transform; /* + on .below */
}
```

```js
// BODY_H must equal the mask's CSS height exactly — measure once at build.
// (Montage caveat: per the contract, in a multi-scene master use an authored
// CSS-matched constant instead — later clips may not be laid out yet.)
const BODY_H = document.querySelector("#expand-mask").offsetHeight;

// The grow: ONE tween, BOTH sides of the seam.
tl.fromTo(
  ["#expand-sheet", "#below"],
  { y: -BODY_H },
  { y: 0, duration: GROW_DUR, ease: GROW_EASE },
  GROW_AT,
);

// Garnish: rows already ride the sheet; the fade stagger makes them read as "options arriving".
tl.fromTo(
  ".expand-row",
  { opacity: 0 },
  { opacity: 1, duration: ROW_FADE_DUR, stagger: ROW_STAGGER, ease: "power2.out" },
  GROW_AT + GROW_DUR * 0.25,
);

// Collapse — same machinery back; faster (closing is a snap decision).
tl.fromTo(
  ["#expand-sheet", "#below"],
  { y: 0 },
  { y: -BODY_H, duration: COLLAPSE_DUR, ease: "power3.in", immediateRender: false },
  COLLAPSE_AT,
);
```

**Variations — proxy counter-scale (surface stretches in place)**, for rows revealed top-first holding their screen positions (the "payload card expands from the tool-call line"). Drive the mask `scaleY` and the sheet's exact inverse from ONE proxy — two independent tweens are wrong, since eased midpoints of `s` and `1/s` are not inverses and the content squashes mid-grow. Net content scale is `s × 1/s = 1` every frame; seek-safe because everything derives from the one interpolated proxy.

```js
const grow = { h: COLLAPSED_H }; // 0 for fully collapsed
tl.fromTo(
  grow,
  { h: COLLAPSED_H },
  {
    h: BODY_H,
    duration: GROW_DUR,
    ease: GROW_EASE,
    onUpdate: () => {
      const s = Math.max(grow.h / BODY_H, 0.0001); // clamp: no divide-by-zero
      gsap.set("#expand-mask", { scaleY: s, transformOrigin: "50% 0%" });
      gsap.set("#expand-sheet", { scaleY: 1 / s, transformOrigin: "50% 0%" });
      gsap.set("#below", { y: grow.h - BODY_H });
    },
  },
  GROW_AT,
);
```

Other variations: a one-axis pane expand (X) rotates the same machinery 90° — pin the left edge, sheet offset horizontally (or proxy `scaleX` plus counter-scale, origin `0% 50%`). Decide the neighbor's fate explicitly: overlap (the pane paints over it, no neighbor tween) or push (the neighbor rides the same tween) — never both. A typed-wrap growth variant grows a composer card taller as typed text wraps: quantize to one short step per wrap boundary, each moving the pair by one line height, with wrap times coming from the deterministic typing schedule (never measured at render time). Two battle-tested traps: composer cards have no pinned header (they grow from the TOP edge with the footer staying put, so a plain y-step clips the top out of the mask — combine the proxy counter-scale with wrap quantization and split the surface into a sheet carrying the top radius plus a footer carrying the bottom radius so the growth seam stays invisible), and wrap TIME vs. wrap POSITION are two different authorities (the typing schedule decides when a wrap fires, the browser's line-breaking decides where text actually wraps, and proportional fonts silently disagree — author an explicit newline at the chosen split point with `white-space: pre-wrap` so both derive from the same authored fact). A springy open (rare, explicitly playful) uses `back.out(1.2)` so the edge overshoots a few px and the pushed content bounces with the panel correctly, since they're in contact — default stays `power3.out`. A row that grows a sub-task stack makes the row the pinned header, the stack the sheet, and every later row lives in the below wrapper.

**Values:** BODY_H measured/authored (drift from the CSS height causes a visible gap or overlap at full open). GROW_AT at the trigger beat plus 0–0.1s (growth needs a cause — click, wrap, status beat — or it reads haunted). GROW_DUR 0.35–0.6s (below ~0.3s the pushed content appears to teleport). GROW_EASE `power3.out` default, `back.out(1.1–1.3)` only for the playful register. ROW_STAGGER/FADE_DUR 0.04–0.08s / 0.2–0.3s (start rows ~25% into the grow so none flash inside a closed panel). COLLAPSE_DUR 0.2–0.35s, `power3.in` (faster than open). STEP_DUR/LINE_H (typed-wrap variant) 0.12–0.2s / the CSS line-height.

**Critical constraints:** NEVER tween `width`/`height`/`top`/`left`/`margin`/`padding` — the mask's height is a CSS constant; only its children transform. A layout-overflow-allowed marker on the mask is required, since the collapsed phase parks the sheet outside the mask's box by construction — the marker is the sanctioned waiver for a layout audit that would otherwise flag this as an overflow bug. Sheet and below must share one tween (or one proxy) — matched-but-separate tweens on the two sides of the contact edge are the classic seam bug. Everything downstream must ride the below wrapper, since content outside it is overlapped at t=0 and orphaned during the grow. `overflow: hidden` on the mask, or the tucked sheet is visible above the header at t=0. Counter-scale needs a proxy, clamped so the scale never reaches exactly zero. Sizes must be deterministic build-time constants or one-time measurements, never per-frame layout reads.

**See also:** the Cursor-Click Ripple rule (the igniting click); the Spring-Pop Entrance rule (richer per-row arrivals); the Discrete Text Sequence rule (the typing that drives stepped growth); the Scale-Swap Transition rule (the grown menu's exit).

### SVG & Icons

#### SVG Icon Enrichment

Treats an SVG icon as a composition of animated PARTS, not an opaque image. Each meaningful internal element (a clock hand, a scissor blade, a recording dot, a data line) gets its own micro-animation, targeted by id. Distinct from the SVG Path Draw rule below (which animates the OUTLINE drawing) — enrichment animates INTERNAL PARTS, ideally after the outline has drawn.

**Four signature patterns:**

| Pattern | Use For | Math | Tip |
| --- | --- | --- | --- |
| Rotation | Clock, gear, loader, dial | `rotate(deg cx cy)` attribute, linear | see the transform-center gotcha |
| Oscillation | Scissors, wings, toggle | `rotate(±sin·amp)` on opposing groups | opposite signs on the two parts |
| Pulse | Recording dot, heart, notification | `scale(1 + sin·amp)` + opacity | ring lags dot by π/2 for ripple |
| Dash flow | Cutting line, data stream | `strokeDashoffset` linear via time | negative for L→R, positive for R→L |

**The transform-center gotcha:** for rotation around an explicit point inside an SVG, use the SVG `transform` ATTRIBUTE, not CSS transform — `el.setAttribute("transform", \`rotate(${deg} ${cx} ${cy})\`)`. The CSS combination `transform: rotate(...)` plus `transform-origin: 60px 60px` plus `transform-box: fill-box` interprets the origin in the element's OWN bbox-local coordinates, NOT viewBox coordinates. For a thin `<line>` (whose bbox is the line's narrow envelope), a coordinate like `60 60` bbox-local is a point OUTSIDE the line — the hand flies along an off-center arc instead of rotating in place. The same trap applies to small inner shapes (a dot circle whose bbox is the small circle, not the full viewBox). For scaling around a center point, use the same attribute route: `translate(cx cy) scale(s) translate(-cx -cy)`.

```html
<!-- named children are the animation targets -->
<svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="50" fill="none" stroke="{accentColor}" stroke-width="6" />
  <line
    id="hand-min"
    x1="60"
    y1="60"
    x2="60"
    y2="22"
    stroke="{textColor}"
    stroke-width="6"
    stroke-linecap="round"
  />
  <line
    id="hand-sec"
    x1="60"
    y1="60"
    x2="60"
    y2="30"
    stroke="{recordColor}"
    stroke-width="3"
    stroke-linecap="round"
  />
  <circle cx="60" cy="60" r="6" fill="{textColor}" />
</svg>
<!-- pulse icon: #rec-ring + #rec-dot circles; dash-flow: a <line> with stroke-dasharray="14 12" -->
```

```js
// Pattern 1 — Rotation. Proxy tween → SVG transform attribute (explicit center, see gotcha).
const hand = document.getElementById("hand-min");
const minState = { deg: 0 };
tl.to(
  minState,
  {
    deg: 360 * MIN_REVOLUTIONS,
    duration: TOTAL_DURATION,
    ease: "none", // linear motion is the point
    onUpdate: () => hand.setAttribute("transform", `rotate(${minState.deg} 60 60)`),
  },
  0,
);
// second hand: same shape with SEC_REVOLUTIONS (visibly faster).

// Pattern 3 — Pulse. One phase proxy drives dot + ring, ring offset by π/2.
const dot = document.getElementById("rec-dot");
const ring = document.getElementById("rec-ring");
const pulse = { p: 0 };
tl.to(
  pulse,
  {
    p: Math.PI * 2 * PULSE_CYCLES,
    duration: TOTAL_DURATION,
    ease: "none", // sine handles the curve
    onUpdate: () => {
      const sD = 1 + Math.sin(pulse.p) * PULSE_DOT_AMP;
      const sR = 1 + Math.sin(pulse.p + Math.PI / 2) * PULSE_RING_AMP;
      dot.setAttribute("transform", `translate(60 60) scale(${sD}) translate(-60 -60)`);
      ring.setAttribute("transform", `translate(60 60) scale(${sR}) translate(-60 -60)`);
      ring.style.opacity = String(
        PULSE_RING_OPACITY_BASE + Math.sin(pulse.p) * PULSE_RING_OPACITY_AMP,
      );
    },
  },
  0,
);

// Pattern 4 — Dash flow. Linear offset tween on a dashed stroke.
const flowState = { offset: 0 };
tl.to(
  flowState,
  {
    offset: DASH_FLOW_TOTAL_OFFSET, // negative = L→R
    duration: TOTAL_DURATION,
    ease: "none",
    onUpdate: () => {
      document.getElementById("data-flow").style.strokeDashoffset = String(flowState.offset);
    },
  },
  0,
);
```

**Variations:** a stroke-draw → enrichment chain draws the outline first (via the SVG Path Draw rule below), then starts enrichment right after — the icon "wakes up" after assembly. A per-icon entry stagger, for a row of icons, starts each one's enrichment as it fades in rather than synchronized.

**Values:** MIN_REVOLUTIONS 0.5–2.0 (avoid integer revolutions if the end frame is visible — it lands back at start). SEC_REVOLUTIONS 4–10 (over 3× the minute-hand rate or the speed difference doesn't read). PULSE_CYCLES 2–4 over a 3–5s composition (5+ reads as anxious flicker, 1 or fewer reads as forgotten). PULSE_DOT_AMP 0.05–0.20 (0.05 = breathing, 0.20 = throbbing). PULSE_RING_AMP 0.04–0.12, must be less than PULSE_DOT_AMP or the ring overshadows the dot. PULSE_RING_OPACITY_BASE/AMP 0.4–0.6 / 0.3–0.5 (base minus amp ≥0 and base plus amp ≤1). DASH_FLOW_TOTAL_OFFSET ±100–400, must be an integer multiple of the dash period (dash plus gap) or the end frame shows a phase jump.

**Critical constraints:** the transform-center gotcha above — use the SVG `transform` attribute for any rotation/scale around an explicit interior point, never CSS `transform-origin` plus `transform-box: fill-box` on thin lines or small inner shapes. No `requestAnimationFrame` — like a raw CSS animation, it desyncs from the seek-driven render, so continuous motion lives inside the timeline as linear proxy tweens. Amplitudes should stay subtle — icons are decorative, not headlines; calibrate rotation speed against composition length, not absolute time. Phase-offset the parts (minute vs. second hand at different speeds, ring lagging dot by π/2) — pure sync looks mechanical. `stroke-linecap: round` on flowing/dashed lines for clean dash edges. Climax dwell of at least 1s if the enrichment is the headline beat.

**See also:** the SVG Path Draw rule (outline draws first, enrichment second); the Orbit 3D Entry rule (orbiting items are enriched icons); the Sine Wave Loop rule (the whole icon floats while internal parts animate).

#### SVG Path Draw

Reveals an SVG shape by animating its stroke as if a pen were tracing it. Two stroke properties together: `stroke-dasharray = <pathLength>` makes the entire path one dash; `stroke-dashoffset` starts at the path length (dash shifted fully out of view — invisible) and tweens to 0 (fully drawn). The length comes from the DOM API `path.getTotalLength()` — measured, never guessed. Works on anything with a stroke: `<path>`, `<circle>`, `<rect>`, `<line>`, `<polyline>`, `<polygon>`, `<ellipse>`.

```html
<svg class="logo-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <path id="bar-left" d="M 60 40 L 60 160" />
  <path id="bar-right" d="M 140 40 L 140 160" />
  <path id="bar-mid" d="M 60 100 L 140 100" />
</svg>
```

```css
.logo-mark path {
  fill: none; /* outline-only draw — a fill would appear immediately and ruin the reveal */
  stroke: {accentColor};
  stroke-width: 12;
  stroke-linecap: round; /* softer endpoints */
  stroke-linejoin: round;
}
```

```js
// Setup: measure each path and set its dash pattern. Real measured geometry, not a magic number.
document.querySelectorAll(".logo-mark path").forEach((p) => {
  const len = p.getTotalLength();
  p.style.strokeDasharray = `${len}`;
  p.style.strokeDashoffset = `${len}`;
});

// Stagger draws so the eye reads continuous motion — each segment starts at
// ~70-80% of the previous segment's duration, before it finishes.
tl.to(
  "#bar-left",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#bar-right",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_2_START,
);
tl.to(
  "#bar-mid",
  { strokeDashoffset: 0, duration: FINAL_SEGMENT_DUR, ease: "power2.out" },
  SEG_3_START,
);

// Companion wordmark fades in only after the last stroke settles.
tl.to(
  ".brand-line",
  { opacity: 1, duration: BRAND_FADE_DUR, ease: "power1.out" },
  BRAND_FADE_START,
);
```

**Variations:** a ring starting at 12 o'clock — a `<circle>`/`<rect>` stroke starts at 3 o'clock by default, so rotate the element −90deg so a progress ring draws from the top (`style="transform-origin: 100px 100px; transform: rotate(-90deg)"`). A linear (constant-speed) draw uses `ease: "none"` for a steady-rate "real pen" trace. Draw-then-fill, for filled shapes, tweens `fillOpacity: 0 → 1` AFTER the stroke completes (requires `fill-opacity: 0` initially and a real `fill` in CSS).

**Values:** SEGMENT_DRAW_DUR 0.3–0.8s (fast snap vs. deliberate pen trace; over ~1s feels sluggish for a logo reveal). FINAL_SEGMENT_DUR 60–80% of SEGMENT_DRAW_DUR, proportional to segment length (a short connector at full duration reads slower than its siblings). SEG_N_START at the previous start plus 70–80% of its duration (reads as continuous motion, not N isolated animations). SEG_1_START 0–0.4s (a small ~0.2s lead-in lets the viewer settle). BRAND_FADE_START at or after the last stroke's end plus a ~0.2s beat (earlier and the wordmark competes with the draw). BRAND_FADE_DUR 0.3–0.8s (snap = urgent, glide = premium). Ease families are discrete choices: stroke draws use `power2.out` (a hand lifting at the end of a stroke) or `"none"` for constant speed — never `back.out`/`elastic.out` since pens don't bounce; fades use `power1.out`.

**Critical constraints:** `fill: none` for outline-only draws, or the fill appears immediately. The dasharray/dashoffset must equal the measured `getTotalLength()`, set at setup — requires the SVG to already be in the DOM (an inline SVG is fine, a loaded `<image>` SVG is not). For complex paths, if `getTotalLength()` looks wrong, overestimate slightly (multiply by ~1.05) — too large is invisible at animation start, too small clips the end. Stagger multi-path draws at roughly 70–80% of the previous segment's duration.

**See also:** the SVG Icon Enrichment rule (internal parts animate after the outline draws); the Counting with Dynamic Scale rule (a stroke draws an icon while a number counts up); the Hacker Flip 3D Reveal rule (a logo draws, the wordmark decodes beneath).

### Idle & Ambient

#### Sine Wave Loop (subtle jitter / bounded ambient)

> Reach for this last. Circular breathing — scaling text/cards up and down to look "alive" — is cheap and reads weak. "I'd rather have NO motion than BAD motion." First fill the back of a shot with sequential reveal timed to the voiceover; if a frame has genuinely settled and still needs life, the sanctioned move is subtle jitter — this rule at the LOW end of its amplitude range. A full breathing loop is the rare last resort on a single held hero, never stamped on every element.

Keeps a settled element from feeling dead using `Math.sin` on the timeline clock. Two forms: a yoyo form (one `sine.inOut` tween with `yoyo: true` and a finite `repeat` count, preferred when the idle stands alone on a property nothing else touches), and an `onUpdate` form (one long `ease: "none"` tween drives a phase proxy from 0 to `2π × CYCLES`, and `onUpdate` maps `Math.sin(phase)` into the transform — required when the offset multiplies/adds onto another live value: compound transforms, amplitude envelopes, multi-octave). Either way, idle begins where the entry settled — at phase 0, `sin(0) = 0`, so the offset is zero and there's no jump from the entry's resting state.

```js
// onUpdate form — phase-driven, composable.
const phase = { p: 0 };
tl.to(
  phase,
  {
    p: Math.PI * 2 * CYCLES,
    duration: IDLE_DUR,
    ease: "none", // sine provides the easing; a non-linear phase tween distorts the wave
    onUpdate: () => {
      const s = Math.sin(phase.p);
      hero.style.transform = `translateY(${s * Y_AMP_PX}px) scale(${1 + s * SCALE_AMP})`;
      // secondary elements: offset by Math.PI / 2 — synced motion looks mechanical
      dot.style.transform = `scale(${1 + Math.sin(phase.p + Math.PI / 2) * DOT_SCALE_AMP})`;
    },
  },
  IDLE_START_TIME,
);

// Yoyo form — standalone property, finite repeats.
tl.to(
  "#badge",
  { y: -Y_AMP_PX, duration: PERIOD / 2, ease: "sine.inOut", yoyo: true, repeat: REPEATS },
  IDLE_START_TIME,
);
```

**Variations:** a multi-octave (organic) form stacks a higher-frequency overlay on the primary sine, with the secondary amplitude smaller than the primary and the combined max staying inside the normal amplitude range. A settle-and-fade — strongly recommended when the idle duration exceeds ~6s — ramps amplitude to zero over the last ~20% of the idle so the scene visibly settles before the inter-scene transition, computed as an envelope multiplier that's 1 until the fade fraction begins, then ramps linearly to 0. This is the single biggest fix when a video shows "everything's still moving at the end," and it pairs naturally with break-boundary transitions (the outgoing visual is static when the crossfade/push begins).

**Values:** SCALE_AMP 0.008–0.015 default (push to 0.02–0.04 only when isolated on canvas, scene under 6s, or an explicitly kinetic brief). Y_AMP_PX 2–3px default (4–6px only under the same gating; rotation ±0.3–0.8° is rarely needed at all). Period 1.5–3s (2.5–4s when idle is long); under 1.5s is frantic, over 4s is lifeless in a short window. CYCLES derived from the period, roughly `IDLE_DUR/3` to `IDLE_DUR/1.5`. IDLE_START_TIME at least ~0.1s after the entry settles (sin(0)=0 there means no jump off the entry tail). IDLE_DUR is the remaining time from start to the composition's total duration — one long tween fills the hold, never restarted. DOT_SCALE_AMP 0.04–0.12 (small accents tolerate more than the hero). OCTAVE_RATIO 2.0–4.0 (integer-ish reads musical, non-integer reads organic).

**Critical constraints:** prefer reveal, then jitter, then breath — default to the LOW end of every amplitude range; at the upper end across 5+ consecutive scenes the whole film reads as "shimmering." A long idle window (over 6s, or idle spanning more than 30% of the composition) should halve the amplitude values, slow the period to 3–4s, and add the settle-and-fade tail. Concurrent idle on N elements (columns, a card grid, a stat row) should scale per-element amplitude down by roughly 1/√N and stagger the periods slightly — three columns bobbing at ±6px compound to ±18px of competing motion, while three at ±2–3px read as one collective breath. Compose, don't replace — idle ADDS to the element's resting transform, never overwrites the entry's final translation. The phase tween's ease should be `"none"`, since sine itself is the curve. No CSS `@keyframes` for idle — a CSS animation runs on the browser's independent render clock, so a CSS-driven idle flickers/desyncs; drive idle inside the timeline instead.

**See also:** the Ambient Glow Bloom rule below (the glow-layer counterpart, same bounded-breathe discipline); the Press-Release Spring, Counting with Dynamic Scale, Card Morph Anchor, and Orbit 3D Entry rules (settled elements this can follow); the Spring-Pop Entrance rule (the arrival that precedes any idle).

#### Ambient Glow Bloom

A soft radial glow that blooms in behind a hero element (card, logo, metric) and holds, giving it presence. Unlike the Press-Release Spring rule's click-triggered burst or the ASR Keyword Glow rule's word-timed envelope, this glow is un-triggered — it blooms on the hero's settle and stays lit. Two forms: a hero bloom that swells behind a settling element then breathes, and a traveling sweep that translates a soft highlight across a surface exactly once.

**How it works:** a radial-gradient layer sits behind the hero (glow behind, hero in front — a glow in front occludes it), starting at zero opacity. Over the bloom-in window it ramps opacity from 0 to a peak with a gentle scale swell, timed so the bloom's end lands on the hero's settle frame — glow and hero resolve as ONE beat ("powering on"), never glow-then-card. After bloom-in: (1) hero bloom — a bounded idle breathe during the hold, a finite `ease: "none"` tween advancing a phase proxy whose `onUpdate` nudges opacity and scale a hair around peak (never a `yoyo` loop); `sin(0) = 0` means the breathe starts exactly at the bloom's resting state. (2) Traveling sweep — a narrow highlight band at one edge translates ONCE across to the other, clipped to the surface (`overflow: hidden`); one pass, no return — a repeating sweep reads as a loading shimmer, not a reveal accent (the shimmer-sweep variation below is the sanctioned exception).

Peak opacity should stay restrained — a HARD ceiling around 0.45 — so the glow gives presence without washing the frame; the glow color should be darker and more saturated than the element it backs (a same-hue, same-lightness glow disappears into the surface).

```html
<div class="bloom-stage">
  <div class="bloom-glow" id="bloom-glow"></div>
  <!-- z-index: 1; inset: GLOW_INSET (negative); background: {glowGradient} -->
  <div class="hero-card" id="hero-card">{HeroLabel}</div>
  <!-- z-index: 2 -->
</div>
<!-- sweep form: <div class="sweep" id="sweep"> inside the overflow:hidden surface -->
```

```js
// ── Form A: HERO BLOOM ── bloom in soft, landing on the hero's settle.
tl.fromTo(
  "#bloom-glow",
  { opacity: 0, scale: GLOW_START_SCALE },
  { opacity: GLOW_PEAK_OPACITY, scale: 1, duration: BLOOM_DUR, ease: "power2.out" },
  BLOOM_START,
);
// Bounded breathe during the hold — finite phase tween, NOT a yoyo loop.
const glow = document.getElementById("bloom-glow");
const phase = { p: 0 };
tl.to(
  phase,
  {
    p: Math.PI * 2 * BREATHE_CYCLES,
    duration: BREATHE_DUR,
    ease: "none",
    onUpdate: () => {
      const s = Math.sin(phase.p);
      glow.style.opacity = String(GLOW_PEAK_OPACITY + s * OPACITY_AMP);
      glow.style.transform = `scale(${1 + s * SCALE_AMP})`;
    },
  },
  BLOOM_START + BLOOM_DUR,
);

// ── Form B: TRAVELING SWEEP ── one finite pass, constant glide.
tl.fromTo(
  "#sweep",
  { x: SWEEP_START_X, opacity: 0 },
  { x: SWEEP_END_X, opacity: SWEEP_PEAK_OPACITY, duration: SWEEP_DUR, ease: "none" },
  SWEEP_START,
);
tl.to("#sweep", { opacity: 0, duration: SWEEP_FADE_DUR, ease: "power1.in" }, SWEEP_FADE_START);
```

**Variations:** bloom-and-hold — for scenes under 3s or a hero with its own idle, skip the breathe entirely, the single `fromTo` is the whole recipe. Pulse-on-arrival — bloom slightly past peak with a small overshoot on opacity plus a scale of ~1.06, then a second adjacent tween eases down to a steady hold — one breath punctuating the landing, no ongoing loop. Multi-hero relay — stagger per-glow bloom starts by ~0.15–0.3s across a row, shrinking the amplitude values per the 1/√N rule above. Diagonal raked sweep — angle the gradient at roughly 105° across a wordmark for the classic one-pass logo sheen, with a narrower sweep width and higher peak opacity.

**Shimmer sweep (text-clipped status-phrase working-state)** — the sweep re-aimed inside type: a soft highlight gradient clipped into a status phrase ("Thinking…", "Analyzing dataset…") via `background-clip: text` travels left-to-right through the letterforms — the grey-on-grey shimmer that says "still working." Unlike every other form here it legitimately repeats while the status is live — the repetition is diegetic working-state, not idle wobble (the same defense as a blinking caret). Two things keep it honest: it is bounded (one finite tween whose pass count is computed from the status window, never `repeat: -1`), and it is killed at resolve — the moment the status completes, the shimmer stops dead; a shimmer surviving into the answer beat turns a working indicator into decoration.

```js
// Status shimmer — N passes as ONE bounded tween. Killed at resolve.
const status = document.getElementById("status-phrase");
// CSS on #status-phrase: background: {shimmerGradient}; background-size: 300% 100%;
// -webkit-background-clip: text; background-clip: text; color: transparent;
const shimmer = { p: 0 };
const PASSES = Math.round(STATUS_DUR / PASS_PERIOD); // whole passes, computed up front
tl.to(
  shimmer,
  {
    p: PASSES,
    duration: STATUS_DUR,
    ease: "none",
    onUpdate: () => {
      const t = shimmer.p % 1; // 0→1 within each pass; percent axis inverted → left→right travel
      status.style.backgroundPosition = `${(1 - t) * 100}% 50%`;
    },
  },
  STATUS_START,
);
tl.set(status, { backgroundPosition: "100% 50%" }, STATUS_START + STATUS_DUR); // resolve: dead.
```

Keep it a whisper: the shimmer gradient should be the status text's own grey with one slightly-lighter band (highlight stop a step above the base, nothing near white); the background-size around 300% keeps the band narrow in the glyphs; the pass period at 1.2–1.8s reads slower as a sheen accent, faster as a spinner. A whole-number pass count lands the band at its start position exactly at the kill frame, so the final `tl.set` is visually a no-op. This is the working-state cousin of the Gradient Text Sweep rule above — reach here when the sweep MEANS "in progress," there when the gradient is the typographic treatment itself.

**Values:** GLOW_PEAK_OPACITY 0.15 subtle → 0.30 default → 0.45 hard ceiling (higher washes the frame — a glow you consciously notice is too strong). GLOW_INSET −200 to −450px at 1920×1080 (negative so the halo extends past the hero; too small reads as a tight rim). GLOW_START_SCALE 0.80–1.0 (grow into place, never shrink). BLOOM_DUR/BLOOM_START 0.6–1.4s (the bloom's end should land on the hero's settle frame). OPACITY_AMP/SCALE_AMP 0.02–0.05 / 0.01–0.03 default (peak plus opacity amp must stay ≤0.45; push only when the glow is the sole motion). BREATHE_CYCLES period 2.5–4s per breath (the glow breathes slower than element breathing elsewhere). SWEEP_WIDTH 15–35% of surface for a grid, 8–15% for a wordmark. SWEEP_DUR 0.8–1.6s (one deliberate pass — slow enough to read as light). SWEEP_PEAK_OPACITY 0.10 → 0.25 default → 0.40 (same ≤~0.45 wash limit; tight sweeps tolerate the high end). SWEEP_START_X/END_X fully off-surface at both ends, so there's no visible spawn/despawn mid-surface. PASS_PERIOD (shimmer) 1.2–1.8s with a whole-number pass count.

**Critical constraints:** glow peak opacity must stay at or below 0.45 including breathe amplitude — default to the LOW end (0.15–0.30). Glow behind, hero in front; glow color darker and more saturated than the hero surface. Land the glow and the hero as one beat — before or after reads as two separate events. The breathe is bounded, the sweep is one pass — the only sanctioned repetition is the shimmer sweep, bounded and killed at resolve. Concurrent halos compound — scale per-glow amplitudes down by roughly 1/√N and stagger breathe periods so they don't pulse in lockstep. Don't combine a `boxShadow` glow on the hero with this halo layer — they compete and read muddy; the glow lives on its own dedicated layer.

**See also:** the Sine Wave Loop rule (the hero breathes on scale/y while the glow breathes on opacity, out of phase); the Press-Release Spring rule (the click-triggered sibling — never both behind one element); the Counting with Dynamic Scale and Stat Bars & Fills rules (bloom behind a landing stat); the Center-Outward Expansion rule (sweep across the assembled grid); the Gradient Text Sweep rule (the design-beat gradient counterpart).

### Transition & Motion

#### Reactive Displacement

Exit animation of element A is mathematically DERIVED from the entry spring of element B — a causal link: "A moves because B hit it." Distinct from the Scale-Swap Transition rule below (which overlaps but isn't causal) and the Card Morph Anchor rule below (one container morphing).

A single 0→1 driver tween (the "entry spring") feeds three concurrent derived motions in one `onUpdate`: the intruder (B, entering) has its position interpolated off-stage → settled over the full driver, plus tilt settling to 0° and a sharp early opacity reveal; the victim (A, exiting) has its position interpolated settled → off-stage in the OPPOSITE direction, completing at roughly 0.4–0.5 of the driver — NOT 1.0. The victim finishing BEFORE the intruder's entry creates the "hit then settle" rhythm; sharing one eased driver makes the impact moment mathematically synchronized.

```js
// Both cards absolutely centered; overflow: hidden on the scene (off-stage travel);
// will-change: transform, opacity on both; intruder z-index ABOVE victim.
const INTRUDER_START_X = STAGE_W; // off-stage right
const VICTIM_END_X = -STAGE_W; // off-stage left — SAME axis, opposite direction

gsap.set("#victim", { x: 0, opacity: 1, rotation: 0 });
gsap.set("#intruder", { x: INTRUDER_START_X, opacity: 0, rotation: -INTRUDER_TILT });

const driver = { p: 0 };
tl.to(
  driver,
  {
    p: 1,
    duration: DRIVER_DUR,
    ease: `back.out(${BOUNCE_FACTOR})`, // the intruder spring
    onUpdate: () => {
      // Intruder: full 0→1 progress maps enter (off-stage → center)
      const intruderX = INTRUDER_START_X * (1 - driver.p);
      const intruderOpacity = Math.min(1, driver.p * FADE_IN_SHARPNESS);
      const intruderRot = -INTRUDER_TILT * (1 - driver.p); // settles to 0°
      const intruder = document.getElementById("intruder");
      intruder.style.transform = `translate(-50%, -50%) translateX(${intruderX}px) rotate(${intruderRot}deg)`;
      intruder.style.opacity = String(intruderOpacity);

      // Victim: completes its exit at VICTIM_FRACTION of the driver — by the
      // time the intruder centers, the victim is already off-stage.
      const victimP = Math.min(1, driver.p / VICTIM_FRACTION);
      const victimX = VICTIM_END_X * victimP;
      const victim = document.getElementById("victim");
      victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px)`;
      victim.style.opacity = String(1 - victimP);
    },
  },
  DRIVER_AT,
);
// Climax dwell — intruder holds centered for ≥ DWELL_MIN before the scene ends.
```

**Variations:** an impact rotation on the victim adds rotation proportional to the victim's own progress, tuned to the perceived intruder weight. A vertical collision has the intruder enter from top with the victim displaced downward — reads as "weight dropped on it." A wobble after settle adds a damped sine wobble (rotation, linearly decaying) starting after the intruder centers, before final stillness — "impact aftermath." A multi-victim ripple has the intruder displace multiple aligned cards, each victim's progress on a slightly offset driver phase for a cascade ripple.

**Values:** DRIVER_AT is phase-dependent — after the prior reading beat resolves; must leave at least the minimum dwell before the scene ends. DRIVER_DUR 0.6–1.4s (short = zippy punch, long = heavy landed impact; higher bounce on long durations reads as floaty). BOUNCE_FACTOR 1.2–2.0, typically 1.4–1.6 (stay in the `back.out` family, or `elastic.out` for oscillation — changing family rewrites the feel). VICTIM_FRACTION 0.4–0.5 (under 0.4 the victim disappears before the impact reads; over 0.5 feels parallel, not causal; hard cap ~0.6). STAGE_W at least the composition width, or the off-stage element is partially visible at start. INTRUDER_TILT 5–15°, typically ~10° (low = clean glide, high = "spin-and-plant"; sign consistent with entry direction for momentum transfer). FADE_IN_SHARPNESS 3–8 (the intruder reaches full opacity at 1/FADE_IN_SHARPNESS of progress; must be greater than 1 or it's transparent at center). DWELL_MIN at least 1.0s, typically 1.0–1.5s — post-impact dwell is where the new content gets read.

**Critical constraints:** single driver = single source of truth — both motions computed inside ONE driver's `onUpdate`, never separate independent tweens per element, which would merely be near each other in time. The victim must complete its exit at a fraction of the driver — the "hit" is the overlap moment; after it, the victim is just vacating space the intruder will fill. Directional momentum transfer — same axis, opposite directions; different axes read as passing, not colliding. The intruder's z-index must sit above the victim explicitly, not just by DOM order, or the victim looks like it tunneled through. The intruder enters tilted and settles flat — a small initial tilt going to 0° reads as "spinning in then planting." Climax dwell after impact — the impact is the headline beat, so hold the settled intruder at least the minimum dwell. `overflow: hidden` on the scene, since off-stage motion exceeds the frame.

**See also:** the Control-Target Sync rule below (the live-editing mirror — repeated coupled edits, nothing exits); the Hacker Flip 3D Reveal rule (intruder text reveal during entry); the Sine Wave Loop rule (idle breathing during the dwell); the Vertical Spring Ticker rule (a ticker that "shoves" the previous content out).

#### Press-Release Spring Chain

Separates input (linear compression) from output (spring recovery) to create tactile feel: the overshoot is a natural byproduct of the spring config, not manually coded, with secondary motion (shadow shrink, release burst, background glow) layered on the same trigger frame. This is a reaction on an element already resting on screen — an arrival that springs in from nothing is the Spring-Pop Entrance rule below; add a visible cursor actor and it becomes the Physics Press Reaction rule below.

Two phases split at the release: (1) press — linear ease into compression (scale from 1 down, shadow shrinks); linear, not spring — the dip must read as instant/tactile, not squishy. (2) release — `back.out(BOUNCE_FACTOR)` spring back to 1.0; optional burst glow ring expands behind the button, optional environmental glow fades in.

State continuity is critical: the release tween's start value MUST equal the press tween's end value, or the spring snaps to a different position. GSAP threads this automatically when both tweens target the same property at adjacent timeline positions — the release start time equals the press start time plus the press duration; a gap or overlap breaks it.

```html
<div class="press-stage">
  <div class="bg-glow" id="bg-glow"></div>
  <!-- Burst sits BEHIND the button (z-index 1 vs 2), same footprint, blurred
       radial gradient, opacity 0. bg-glow is a full-stage radial at negative
       inset so it extends past the stage edges. -->
  <div class="burst" id="burst"></div>
  <button class="btn" id="btn">{buttonLabel}</button>
</div>
```

```js
// Phase 1 — press (linear compression)
tl.to(
  "#btn",
  { scale: PRESS_SCALE, boxShadow: "{btnPressedShadow}", duration: PRESS_DUR, ease: "power1.in" },
  PRESS_START,
);

// Phase 2 — release (spring back; start scale == PRESS_SCALE by adjacency)
tl.to(
  "#btn",
  {
    scale: 1,
    boxShadow: "{btnRestShadow}",
    duration: RELEASE_DUR,
    ease: `back.out(${BOUNCE_FACTOR})`,
  },
  RELEASE_START,
);

// Phase 3 — burst glow pops behind the button, then fades
tl.fromTo(
  "#burst",
  { scale: 1, opacity: 0 },
  {
    scale: BURST_PEAK_SCALE,
    opacity: BURST_PEAK_OPACITY,
    duration: BURST_GROW_DUR,
    ease: "power2.out",
  },
  RELEASE_START,
);
tl.to("#burst", { opacity: 0, duration: BURST_FADE_DUR, ease: "power2.in" }, BURST_FADE_START);

// Phase 4 — environmental glow fades in after release
tl.to(
  "#bg-glow",
  { opacity: BG_GLOW_PEAK_OPACITY, duration: BG_GLOW_FADE_DUR, ease: "power2.out" },
  RELEASE_START,
);
```

**Variations:** a subtle press (status save/muted CTA) uses press scale ~0.96, bounce factor ~1.4, and a reduced burst. A dramatic press (hero CTA/"ship it") uses press scale ~0.88, bounce factor ~2.5, and a maxed burst. A color shift during press darkens mid-press and returns on release, interpolating `backgroundColor` at the same timeline positions as the scale tweens (same state-continuity rule). A state change at release (approve/confirm), instead of returning to the rest color, swaps to a success color at release start and pops a checkmark via a separate, firmer `back.out` tween — the button is now terminal, no further presses expected.

**Values:** button footprint should be at least 3–5% of canvas area — a small button at 1080p is closer to 1% and the press reads as visually insignificant. PRESS_SCALE 0.88 dramatic / 0.92 default / 0.96 subtle (never under 0.85 — broken — or over 0.98 — no perceptible dip). PRESS_DUR 0.10–0.30s (shorter = snappier; must be shorter than RELEASE_DUR — input faster than spring recovery). RELEASE_DUR 0.40–0.90s (shorter = tight pop, longer = loose wobbly settle). BOUNCE_FACTOR 1.4 soft / 2.0 firm / 2.8 cartoony, or `elastic.out(amplitude, period)` for a rubbery oscillation instead of one overshoot. RELEASE_START must equal PRESS_START plus PRESS_DUR — adjacency gives automatic state continuity. BURST_PEAK_SCALE 3 subtle / 6 default / 8 max (beyond ~8 the radial gradient pixelates visibly). BURST_PEAK_OPACITY 0.4–1.0 (grow roughly equals fade, 0.4–0.7s each; blur 40–100px, hard ring to ambient haze). BG_GLOW_PEAK_OPACITY 0.1 subtle / 0.25 default / 0.45 max (higher washes the whole composition; fade-in 0.6–1.0s; inset −300 to −500px at 1080p).

**Critical constraints:** state continuity — the release start value must exactly equal the press end value, enforced by same-property adjacency. Linear press, spring release — both spring is squishy, both linear is mechanical with no overshoot punch. Anchor compression on center (`transform-origin: 50% 50%`), or the button collapses asymmetrically. The burst sits behind, not in front — burst z-index below the button, or it occludes the button at peak opacity. Don't tween `boxShadow` and `filter` on the same element — they compete in the layout pipeline; shadow on the button, blur on the separate burst layer. Climax dwell — after the burst peak and reveal, the composition must run at least 1s more (2s for dramatic variants); a reveal near the very end reads as "flashed and gone."

**See also:** the Spring-Pop Entrance rule below (the ENTRANCE counterpart — arrival, not reaction); the Physics Press Reaction rule below (this press with a visible cursor actor); the Cursor-Click Ripple rule below (the cursor click that triggers the press); the Sine Wave Loop rule (idle micro-float BEFORE the press); the Center-Outward Expansion rule (badge burst synced to the release).

#### Physics Press Reaction (Cursor + Element Synced)

Models a real click: a cursor approaches a button, lands, and both compress IN SYNC, then release together. Distinct from the Press-Release Spring rule above (no cursor — just a press happening); this rule is the COMBINED cursor plus element behavior. A single press intensity value drives both — press down compresses both to `1 - PRESS_INTENSITY` via ONE targets array, release springs both back to 1.0 with overshoot. The cursor translates to the button's center BEFORE the press starts; after release it may move on or hold.

```html
<button class="btn" id="btn">{ctaCopy}</button>
<!-- Cursor at scene-root level so it translates freely; arrow TIP is the click
     point, so transform-origin: 0 0 — scaling around the tip keeps it stable. -->
<svg class="cursor" id="cursor" style="pointer-events: none; transform-origin: 0 0">…</svg>
```

```js
gsap.set("#cursor", { x: CURSOR_START_X, y: CURSOR_START_Y }); // off-screen / far corner

// Phase 1 — approach
tl.to(
  "#cursor",
  { x: BUTTON_CENTER_X, y: BUTTON_CENTER_Y, duration: APPROACH_DUR, ease: "power2.inOut" },
  APPROACH_START,
);

// Phase 2 — coordinated press down: ONE targets array, same scale
tl.to(
  ["#btn", "#cursor"],
  { scale: 1 - PRESS_INTENSITY, duration: PRESS_DOWN_DUR, ease: "power1.in" },
  PRESS_DOWN_AT,
);

// Phase 3 — release: both spring back together
tl.to(
  ["#btn", "#cursor"],
  { scale: 1, duration: RELEASE_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  RELEASE_AT,
);

// Phase 4 — inner glow during press, resting shadow on release (contact confirmation)
tl.to(
  "#btn",
  { boxShadow: "{btnPressedShadow}", duration: PRESS_DOWN_DUR, ease: "power1.in" },
  PRESS_DOWN_AT,
);
tl.to(
  "#btn",
  { boxShadow: "{btnRestingShadow}", duration: RELEASE_DUR, ease: "power2.out" },
  RELEASE_AT,
);

// Cursor optionally exits after the press settles
tl.to(
  "#cursor",
  { x: CURSOR_EXIT_X, y: CURSOR_EXIT_Y, duration: CURSOR_EXIT_DUR, ease: "power2.out" },
  CURSOR_EXIT_AT,
);
```

**Variations:** a multiple-element chain press has button A pressed, A triggers a swap, the cursor moves to button B, and it presses again — each press is one full down-release sub-routine. A hold press (continuous pressure) inserts a hold window between press-down and release: both scales stay compressed, inner glow stays on, suggesting "thinking" or "loading." A synchronized inner-glow pulse during the hold uses a sine driver to modulate a `boxShadow` alpha, suggesting "processing."

**Values:** APPROACH_START 0–0.3s (long delays read as a dead frame). APPROACH_DUR 0.7–1.3s (faster = urgent, slower = deliberate). PRESS_DOWN_AT equals APPROACH_START plus APPROACH_DUR, so the cursor arrives exactly as the press begins, avoiding "tapping on air." PRESS_DOWN_DUR 0.1–0.25s. RELEASE_AT greater than PRESS_DOWN_AT plus PRESS_DOWN_DUR, with an optional 0.05–0.4s pause (or a 0.3–0.8s hold window) for "thinking" interactions. RELEASE_DUR 0.4–0.7s, long enough for the overshoot to settle. PRESS_INTENSITY 0.05 subtle / 0.10 standard / 0.15 heavy, applied to both cursor and button via the single targets array. BOUNCE_FACTOR 1.6 soft / 2.0 firm / 2.4 cartoony. CURSOR_START/EXIT off-screen or a far corner (the approach must read as motion-in, not a teleport; exit at or after release end). BUTTON_CENTER should be a measured value. Glow pulse (if used) 1–4 cycles, base alpha 0.15–0.3, amplitude 0.1–0.2 (base minus amplitude ≥0). CURSOR_SIZE 48–96px at 1080p.

**Critical constraints:** the same press scale must apply to cursor AND button (one targets array) — button-only scaling makes the cursor "tap on air," cursor-only scaling makes the button feel disconnected. The cursor must arrive BEFORE the press starts — a clear "cursor over target" moment, or the press is unattributed. `back.out(BOUNCE_FACTOR)` on the release, for both together — a linear release loses the tactile feel, and release must come after press. The cursor's `transform-origin: 0 0` (the arrow's tip is the click point, so scaling around the tip keeps it stable); `pointer-events: none` on the cursor. Inner glow appears DURING press and fades on release — the outer shadow shrinks (pushed in), the inner glow appears (energy concentrated). Climax dwell of at least 1s after release. No real `mouseenter`/`click` events — everything runs through the timeline.

**See also:** the Press-Release Spring rule above (the button-only press; this rule layers the cursor on top); the Cursor-Click Ripple rule below (adds a ripple at the click point); the Scale-Swap Transition rule below (the press TRIGGERS the swap).

#### Cursor Click Ripple

An animated cursor moves to a target element, performs a click with visual depression, and emits expanding ripple rings from the click point. Three sequential phases on one timeline: move (eased translation to the target's center), click (scale depression on cursor and target together, yoyo back), ripple (1–3 staggered rings expand and fade from the click point). This is a point event at one location — a sustained hold across space is the Cursor Drag rule below.

```html
<button class="target-button">{ctaLabel}</button>
<div class="cursor"><!-- arrow SVG, positioned at the entry corner --></div>
<!-- Rings live in DOM from t=0 at the click-target CENTER, scale 0 + opacity 0 -->
<div class="ripple ripple-1"></div>
<div class="ripple ripple-2"></div>
<div class="ripple ripple-3"></div>
```

```css
.ripple {
  position: absolute;
  left: 50%;
  top: 50%; /* click-target center */
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid {rippleColor};
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
}
```

```js
// Phase 1 — Move: eased, not linear
tl.to(".cursor", { x: TARGET_X, y: TARGET_Y, duration: MOVE_DUR, ease: MOVE_EASE }, 0);

// Phase 2 — Click: cursor + target depress together, then return
tl.to(
  ".cursor",
  { scale: CURSOR_PRESS_SCALE, duration: PRESS_DUR, ease: "power2.in", yoyo: true, repeat: 1 },
  CLICK_AT,
);
tl.to(
  ".target-button",
  { scale: TARGET_PRESS_SCALE, duration: PRESS_DUR, ease: "power2.in", yoyo: true, repeat: 1 },
  CLICK_AT,
);

// Phase 3 — Ripple burst, N rings staggered from the click point
tl.set([".ripple-1", ".ripple-2", ".ripple-3"], { opacity: 1 }, RIPPLE_AT);
tl.to(
  [".ripple-1", ".ripple-2", ".ripple-3"],
  {
    scale: RIPPLE_SCALE,
    opacity: 0,
    duration: RIPPLE_DUR,
    ease: RIPPLE_EASE,
    stagger: RIPPLE_STAGGER,
    immediateRender: false, // holds scale 0 / opacity 0 until the click moment
  },
  RIPPLE_AT,
);
```

**Variations:** a single ring, with no stagger, is more elegant when the rest of the scene is busy. A keyframed attack-decay ramps opacity from 0 to peak to 0 across the duration for a clearer "energy radiates and dissipates" envelope. A multi-ring expanding pulse (3 rings at ~0.08s stagger) suits a scene's climactic click.

**Values:** MOVE_DUR 0.4–1.0s (short darts vs. long "considered click"; must end before CLICK_AT or it reads as a misclick). MOVE_EASE is a discrete choice — `power2.inOut` calm, `power3.out` decisive, `back.out(1.2–1.4)` settles onto the button with a tiny recoil (higher values read cartoonish). CLICK_AT equals MOVE_DUR plus 0–0.3s (zero pause reads as autopilot, over 0.3s reads as hesitation). PRESS_DUR 0.06–0.12s (half; yoyo ×2) — short is crisp, long is mushy, and it must finish before the next phase needs normal scale. CURSOR/TARGET_PRESS_SCALE 0.80–0.90 / 0.92–0.97 — the cursor compresses MORE than the target, since the cursor is the actor and the target is the recipient. RIPPLE_AT equals CLICK_AT plus 0–0.08s (simultaneous feels causal, a slight delay feels acoustic). RIPPLE_DUR 0.5–1.0s (sharp ping vs. soft sonar; must complete before anything that needs the ring gone). RIPPLE_SCALE 3–6 (3 stays near the click site; lower it if the ring would exit the frame before fading). RIPPLE_STAGGER 0.06–0.12s or 0 (below ~0.06s reads as one thick ring, above ~0.12s as separate events). RIPPLE_EASE is a discrete choice — `power2.out` standard ping, `power3.out` sharper attack, `expo.out` strong distant pulse. TARGET_X/TARGET_Y must be layout-derived and match the target's visual centroid — a few-pixel miss reads as missing the button.

**Critical constraints:** move before click — the click should only trigger after the move tween settles, since clicking mid-motion reads as unintentional. Rings live in the DOM from t=0 at the click-target center with zero scale and opacity, never conditionally rendered, with `immediateRender: false` on the expand tween so they hold invisible until the trigger. Ripple from the click point — the button's visual center, not any element's bounding-box origin. Synchronized depression — cursor and target depress at the same position with the same duration and both yoyo back. The cursor stays above all content (high z-index) for the whole sequence, with `pointer-events: none` on cursor and ripples.

**See also:** the Orbit 3D Entry rule (click as the pivot that collapses orbiters); the Center-Outward Expansion rule (click triggers an outward burst); the Press-Release Spring rule (stronger physical feel on the target); the Scale-Swap Transition rule below (the button's post-click state change).

#### Cursor Drag

> Cursor look, sizing, off-screen entry, and tip-targeting defer to a shared oversized-cursor house doctrine (not repeated here) — this rule owns the drag MECHANICS only.

THE held-journey verb: the cursor presses down on a payload, carries it, and releases it somewhere else. The load-bearing law is LOCKSTEP: the cursor tip and the payload's grip point move as one rigid object for the entire travel — a one-frame drift reads as the chip slipping out of the hand. Distinct from the Cursor Click Ripple rule above (move → point event at a single location) — a drag is a sustained hold across space, and the payload is the co-star. Reuse the Physics Press Reaction rule above for the grab's press dip (cursor plus payload compress together); for N simultaneous actors see the Multi-Cursor Choreography rule below — this rule is one protagonist performing a workflow beat.

**How it works:** five beats — approach (cursor glides to the source chip, `power2.inOut`) → grab (a press dip on cursor and chip together; on the down-beat a `tl.set` reveals a ghost — a pre-rendered semi-transparent clone at the chip's position — plus a small lift `fromTo` to a slightly larger scale with a soft shadow, `immediateRender: false`) → travel (cursor and ghost move as MATCHED tweens) → drop (ghost off, placed field pops in with selection chrome) → adjust/exit (optional handle resize, then the cursor glides to the next target).

Matched tweens means same timeline position, same duration, same ease, over straight lines — that keeps the pair rigidly locked at every eased midpoint. A shared targets array only works when both need identical deltas; with different start points, use two matched `fromTo`s. Rule-specific corollary of the base seek-safety law: a relative `+=` travel on either partner breaks the lockstep under seek.

Measure chip and slot rects at build time — a few-pixel miss on the drop line reads as a failed drag (in a multi-scene montage, use authored CSS-matched constants instead). A tip-offset value aligns the cursor's TIP (not its bbox) with the grip point.

```html
<!-- Ghost = clone of the chip AT the chip's position, in DOM from t=0, opacity: 0.
     Same silhouette as the chip — or hand and payload read as different objects.
     Placed field sits at the slot's final position, opacity: 0, with a .select-box
     and four corner .handle elements inside. -->
<div class="tray-chip" id="source-chip"><span class="grip-dots">⋮⋮</span> {chipLabel}</div>
<div class="drag-ghost" id="drag-ghost"><span class="grip-dots">⋮⋮</span> {chipLabel}</div>
<div class="placed-field" id="placed-field">
  {placedLabel}
  <!-- + selection chrome -->
</div>
<div class="cursor" id="cursor"><!-- arrow SVG --></div>
```

```js
const chipRect = document.querySelector("#source-chip").getBoundingClientRect();
const slotRect = document.querySelector("#placed-field").getBoundingClientRect();
const TRAVEL_DX = slotRect.left - chipRect.left;
const TRAVEL_DY = slotRect.top - chipRect.top;

// Travel — MATCHED tweens: same position, duration, ease; absolute endpoints.
tl.fromTo(
  "#drag-ghost",
  { x: 0, y: 0 },
  { x: TRAVEL_DX, y: TRAVEL_DY, duration: TRAVEL_DUR, ease: TRAVEL_EASE, immediateRender: false },
  TRAVEL_AT,
);
tl.fromTo(
  "#cursor",
  { x: chipRect.left + TIP_OFFSET_X, y: chipRect.top + TIP_OFFSET_Y },
  {
    x: chipRect.left + TIP_OFFSET_X + TRAVEL_DX,
    y: chipRect.top + TIP_OFFSET_Y + TRAVEL_DY,
    duration: TRAVEL_DUR,
    ease: TRAVEL_EASE,
    immediateRender: false,
  },
  TRAVEL_AT,
);

// Drop is a state commit: ghost off + placed field on at the SAME position.
tl.set("#drag-ghost", { opacity: 0 }, DROP_AT);
tl.fromTo(
  "#placed-field",
  { opacity: 0, scale: 0.92 },
  { opacity: 1, scale: 1, duration: SNAP_DUR, ease: "power3.out" },
  DROP_AT,
);
tl.fromTo(
  [".select-box", ".handle"],
  { opacity: 0, scale: 0.6 },
  { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out", stagger: 0.02 },
  DROP_AT + SNAP_DUR * 0.4,
);
```

**Variations:** a corner-handle proportional resize renders as uniform `scale` with `transform-origin` at the opposite (anchor) corner, since width/height tweens are forbidden — the anchor stays put, the dragged corner travels. The corner's position is linear in scale (`corner = anchor + scale × (corner₀ − anchor)`), so a cursor tween to the corner's end position with the same duration and ease stays glued to the handle exactly. One-axis resizes are `scaleX`/`scaleY` on the same origin logic — stretch-safe boxes only; route to the Anchored Layout Expand rule's counter-scale form when content must stay undistorted. A fill-handle auto-fill (the spreadsheet verb) drags a cell's fill handle straight down on a `"none"` (linear) ease; each row commits via a snapped `tl.set` (never a fade) keyed to the handle's linear progress, so the fill edge and cursor never separate. A grab-lift-reorder lifts the item (small negative y plus a small rotation whose sign comes from index parity) plus a shadow-on; as the carried item crosses the neighbor's midpoint, the neighbor springs into the vacated slot via a `fromTo` translate with `power3.out` — the neighbor's counter-move sells the reorder, without it the list reads as broken. A component grab between surfaces drags a chip mockup-to-mockup, swapping identity on drop (a `tl.set` recolor plus label swap, tiny settle pop) — the drop chrome is just the identity swap, no handles.

**Values:** approach/press timings follow the Cursor Click Ripple rule — approach 0.4–1.0s, press-dip halves 0.06–0.12s, cursor compresses more than the payload. GHOST_OPACITY 0.5–0.75 (below 0.5 vanishes on busy documents, near 1.0 reads as the original moving — then hide the source chip at the grab). GHOST_LIFT_SCALE/LIFT_DUR 1.03–1.08 / 0.12–0.2s (the shadow is the "off the surface" cue, the scale is garnish). TRAVEL_DUR/EASE 0.6–1.2s / `power2.inOut` (a considered drag decelerates into the slot; `power1.inOut` for a calmer carry). TRAVEL_AT must be at least the grab time plus 2× press duration plus the lift duration. DROP_AT/SNAP_DUR equals TRAVEL_AT plus TRAVEL_DUR exactly / 0.2–0.3s (a gap between arrival and snap reads as the drop failing). RESIZE_SCALE/DUR by story, roughly 0.4–0.6 / 0.6–1.0s, `power2.inOut`. LIFT_RISE/LIFT_TILT 6–12px / 2–4° for the reorder pickup, index-derived tilt sign.

**Critical constraints:** lockstep is the law — matched tweens over straight lines (or one shared tween when deltas are identical); verify at the eased midpoint, not just the endpoints, with absolute endpoints on both partners. The ghost is pre-rendered — a DOM clone at the source position from t=0, opacity 0, revealed by `tl.set`; placed field and chrome likewise, never cloned at runtime, never conditionally rendered. Grab has weight — a press dip plus lift shadow before any travel, since a chip departing without a press reads as telekinesis. Drop is a state commit — ghost off and placed field on at the same timeline position. Resizes are uniform `scale`, origin at the anchor corner — never width/height, and one-axis stretch only on stretch-safe boxes. Linear ease on the fill-handle travel, since the evenly-spaced snap reveals depend on it. One verb per beat — drag, then resize, then exit; overlapping a travel with a resize turns choreography into mush. `pointer-events: none` on cursor, ghost, and chrome.

**See also:** the Physics Press Reaction rule (the grab's press dip); the Cursor-Click Ripple rule (a plain click before/after); the Spring-Pop Entrance rule (the placed field's snap-settle); the Waterfall Entry rule below (kinetic fill cascade); the Multi-Phase Camera rule (the zoom-breathing carrier shot golden drag demos ride); the Multi-Cursor Choreography rule (this verb inside an ensemble).

#### Multi-Cursor Choreography

> The camera never chases anyone. No real camera — any "pan" is the canvas group translating inside a static frame. And per the idle-motion doctrine, every cursor must PERFORM: travel to a target, act, then rest still. Scheduled rest is stillness; aimless wander loops are wobble.

THE ensemble primitive: two to four labeled cursor actors — each an arrow plus a name-tag pill in its own color — work one shared canvas at the same time. No single interaction is the subject; the simultaneous liveness is ("a team is in here, working"), usually as ambience under a headline building over the top. Distinct from the Cursor Click Ripple and Cursor Drag rules above: those are one protagonist the viewer follows click-by-click; here the actors are chorus, not lead — each action smaller and quieter than a solo cursor's, the value in the interleaving. Also distinct from the Two-Phase Camera Cursor Tracking rule above — that locks the viewport to one focal cursor; this rule forbids exactly that — the frame is static and the eye roams freely.

**How it works:** (1) the actor table — a literal `ACTORS` array: per actor a name, a color, and a waypoint schedule (`{ x, y, at, dur }` legs plus action beats). All coordinates and times are hand-authored constants — the choreography is data: deterministic, seekable, and auditable for collisions before a single frame renders. (2) Legs as explicit `fromTo`s — each leg tweens the actor wrapper from the previous waypoint to the next at an absolute position; gaps between legs are rests where the cursor sits still exactly where it landed. (3) Actions — a leg can end in a grab (press dip; the payload rides the next leg in lockstep, per the Cursor Drag rule's mechanics at chorus intensity), a drop (a `tl.set` identity swap plus a tiny settle pop), or a hover (a highlight fades in under the tip, once, then holds). (4) The interleaved beat grid — actions land on alternating beats (roughly 1.2/2.6/4.0s): at any moment at most one action lands while the others glide or rest; each actor owns a home zone of the canvas, and only one actor at a time leaves its zone so paths never cross near-simultaneously. Short specimens under ~5s can compress beat spacing to ~0.3–0.9s — zones still prevent collisions. (5) Ambience staging — cursors may already be mid-canvas at t=0 (the team was working before we arrived), or enter off-frame on staggered starts; the canvas group may slowly translate-pan under the ensemble (element translate, not a camera).

```html
<!-- Canvas group (mockups + payload chips) may translate for an ambient pan.
     One wrapper per actor: arrow + name tag move as ONE object. -->
<div class="canvas-group" id="canvas-group">
  <div class="mockup" id="mockup-a">{mockupA}</div>
  <div class="canvas-chip" id="chip-1">{chipLabel}</div>
</div>
<div class="actor" id="actor-1">
  <svg class="actor-arrow"><!-- arrow path, fill: ACTOR_1_COLOR --></svg>
  <span class="actor-tag" style="background: ACTOR_1_COLOR">{actorName1}</span>
</div>
```

```js
// The choreography IS this table — all literals; read the `at` columns to
// verify beats interleave. Each actor owns a zone.
const ACTORS = [
  {
    id: "#actor-1", // zone: left mockup
    legs: [
      { from: { x: 180, y: 420 }, to: { x: 320, y: 300 }, at: 0.2, dur: 0.9 },
      { to: { x: 340, y: 480 }, at: 2.0, dur: 0.8 }, // rest 0.9s between legs
    ],
  },
  {
    id: "#actor-2", // zone: center mockup
    legs: [
      { from: { x: 900, y: 200 }, to: { x: 820, y: 360 }, at: 0.6, dur: 1.0 },
      { to: { x: 980, y: 380 }, at: 3.4, dur: 0.7 },
    ],
  },
  {
    id: "#actor-3", // zone: right panel — enters from off-frame
    legs: [{ from: { x: 1980, y: 520 }, to: { x: 1560, y: 460 }, at: 1.4, dur: 1.1 }],
  },
];

ACTORS.forEach((actor) => {
  let prev = actor.legs[0].from;
  tl.set(actor.id, { x: prev.x, y: prev.y }, 0); // on stage (or off) from t=0
  actor.legs.forEach((leg) => {
    tl.fromTo(
      actor.id,
      { x: prev.x, y: prev.y },
      { x: leg.to.x, y: leg.to.y, duration: leg.dur, ease: "power2.inOut", immediateRender: false },
      leg.at,
    );
    prev = leg.to;
  });
});

// Actions at chorus intensity — actor 1 grabs the chip: press dip, then the
// chip rides leg 2 in lockstep (matched tween: same position, duration, ease).
tl.to("#actor-1", { scale: 0.88, duration: 0.07, ease: "power2.in", yoyo: true, repeat: 1 }, 1.1);
tl.fromTo(
  "#chip-1",
  { x: 0, y: 0 },
  { x: CHIP_DX, y: CHIP_DY, duration: 0.8, ease: "power2.inOut", immediateRender: false },
  2.0, // = actor-1 leg 2 `at` and `dur`, exactly
);
// Drop: identity swap + tiny settle — quieter than a solo cursor's snap
tl.set("#chip-1", { backgroundColor: "{chipSwapColor}" }, 2.8);
tl.fromTo(
  "#chip-1",
  { scale: 1.06 },
  { scale: 1, duration: 0.2, ease: "power3.out", immediateRender: false },
  2.8,
);

// Optional ambient canvas pan (element translate, NOT a camera)
tl.fromTo("#canvas-group", { x: 0 }, { x: PAN_DX, duration: 6.0, ease: "none" }, 0.3);
```

**Variations:** the ambient collaborative canvas (a Hook register) — the default form: actors mid-canvas at t=0, canvas slowly panning, a headline building over the top (see the Waterfall Entry rule below) — the demo is set-dressing for the words, so keep every action small and the beat grid loose. One labeled editor (N=1, still ensemble-styled) — a single labeled teammate cursor performs one visible edit (deletes and retypes a headline word via the Discrete Text Sequence rule, or drops one component) — the name tag is the point, a PERSON did this. A featured beat inside the ensemble — one actor briefly becomes the lead with a full Cursor Drag grab-carry-drop while the others explicitly REST for that window; freeze the chorus, since two things moving with intent at once splits the eye. Staggered entrances — cursors enter from off-frame at a per-actor stagger, each gliding to its zone ("the team assembles"), entry vectors from different edges.

**Values:** ACTOR_COUNT 2–4 (one is a solo rule's job; five or more reads as noise — no viewer tracks five pointers). Leg duration 0.6–1.2s, `power2.inOut` (human, considered mouse movement; sub-0.5s across long distances reads as a teleport). Rest gaps 0.5–1.5s (rests make the ensemble read as people; zero-rest actors read as screensavers). Action beat spacing at least 1.0s (while one acts, others may glide but must not act — audit by sorting all beat times). Zones — one per actor (only the acting actor crosses zones; two cursors within ~80px reads as a glitch — check waypoint pairs at overlapping times). PAN_DX ~40–80px, linear (parallax life, not a camera move; omit for busier ensembles). Tag/arrow size should be smaller than a solo lead's, since the oversized-cursor treatment is for protagonists. Colors: one saturated hue each from the palette's accent range, tag pill and arrow fill sharing the hue.

**Critical constraints:** the table IS the choreography — all waypoints, times, and actions are literal data; if you can't verify non-collision by reading the `at` columns, the schedule is too clever. Every leg is an explicit `fromTo` with the previous waypoint as the from-state, `immediateRender: false` on all but each actor's initial placement — chained `.to()`s on shared properties capture stale starts under seek. Interleave, never chord — at most one action landing at any moment; simultaneous travel is fine (that's the liveness), simultaneous payoffs compete. Chorus intensity — every action is a quieter version of its solo rule: smaller dips, subtler snaps, no ripple bursts. Rest is stillness — between legs a cursor holds exactly where it landed, no idle drift, no yoyo wander on any actor. Payload lockstep — a carried chip's tween must match its actor's leg exactly. The wrapper moves, never the parts — arrow plus name tag are one element; tweening them separately shears the actor apart under seek. Camera locked — no viewport zoom/pan tweens; the only large-scale motion is the linear canvas-group translate. Actors are people — human-speed glides, pauses, one thing at a time; `pointer-events: none` on all actors.

**See also:** the Cursor Drag rule (full-treatment featured beat); the Cursor Click Ripple rule (chorus click — press only, skip the ripple); the Discrete Text Sequence rule (a labeled actor's retype edit); the Viewport Change rule (the canvas-group translate math); the Spring-Pop Entrance rule (components popping in as drop results).

#### Control-Target Sync

THE live-editing move: an inspector/editor control is manipulated — a value scrubbed, a field retyped, a dropdown picked — and a bound second element answers in the same frame. The button rotates WHILE the rotation value scrubs; icons resize PER KEYSTROKE. The persuasion is causality — one gesture, two surfaces changing together — and this rule is the coupling contract that produces it.

Nearest precedent is the Reactive Displacement rule above: that rule also derives two elements' motion from one source, but it is collision physics — an entering intruder displaces an exiting victim, once, as a transition, and the victim leaves. This rule is a live editing mirror: the control is manipulated repeatedly across several beats, the target answers every time, and both sides hold the stage throughout. The numeric readout rides the Counting with Dynamic Scale rule's proxy pattern; discrete steps ride the Discrete Text Sequence rule's threshold pattern — what this rule adds is the law that binds either of them to the target.

**How it works:** an edit beat is a set of concurrent tweens at ONE timeline label — the readout tween (numeric proxy plus `onUpdate` writing `textContent` only) and the target transform tween (`rotation`/`x`/`y`/`scale` to the same endpoint) placed at the label with the same duration and ease. The two motions are two projections of one gesture — value at 40% ⇒ target at 40%, on every frame, under any seek. That mathematical lockstep reads as "the panel is editing the page," not "two animations happen to overlap." For discrete edits (per-keystroke retypes, dropdown picks, unit snaps) the couple steps instead of glides: a single threshold state array carries BOTH sides — each state holds the readout text AND the target's property value — and one driver applies whichever state is active. Both sides read from the same state object, so they cannot desync. Chain 2–4 edit beats with short holds between, and end on a landed edit — the last value applied and holding, never a tooltip with the dropdown unopened.

```html
<!-- Bipartite by construction: target surface + inspector panel share the frame.
     Every scrubbed readout gets `font-variant-numeric: tabular-nums` and a fixed
     min-width (≥ the longest value) or the panel edge jitters as digits change. -->
<div class="target-surface">
  <div class="target-button" id="target-button">{buttonLabel}</div>
  <div class="preview-row">
    <div class="preview-icon">{iconA}</div>
    …
  </div>
</div>
<div class="panel">
  <div class="field-row">
    <span>Rotation</span><span class="field-value" id="rotation-readout">0°</span>
  </div>
  <div class="field-row">
    <span>Class</span><span class="field-value mono" id="class-readout">text-1xl</span>
  </div>
</div>
```

```js
// ---- Continuous couple: ONE label; both tweens share duration AND ease ----
tl.addLabel("edit1", EDIT1_AT);
const rotState = { v: 0 };
const rotReadout = document.getElementById("rotation-readout");
tl.to(
  rotState,
  {
    v: ROT_TARGET,
    duration: SCRUB_DUR,
    ease: SCRUB_EASE,
    onUpdate: () => {
      rotReadout.textContent = `${Math.round(rotState.v)}°`;
    },
  },
  "edit1",
);
tl.to(
  "#target-button",
  { rotation: ROT_TARGET, duration: SCRUB_DUR, ease: SCRUB_EASE },
  "edit1", // same label — the mirror answers in the same frame
);

// ---- Discrete couple: ONE state array carries BOTH sides ----
const STEPS = [
  { t: 0.0, text: "text-1xl", scale: 1.0 }, // must equal the initial state
  { t: 0.4, text: "text-4xl", scale: 1.9 },
  { t: 1.0, text: "text-xl", scale: 0.85 }, // backspace
  { t: 1.35, text: "text-2xl", scale: 1.3 }, // lands
];
const stepAt = (time) => [...STEPS].reverse().find((s) => time >= s.t) ?? STEPS[0];

tl.addLabel("edit3", EDIT3_AT);
const classReadout = document.getElementById("class-readout");
const stepDriver = { t: 0 };
let lastStep = null;
tl.to(
  stepDriver,
  {
    t: STEPS_TOTAL,
    duration: STEPS_TOTAL,
    ease: "none",
    onUpdate: () => {
      const s = stepAt(stepDriver.t);
      if (s !== lastStep) {
        classReadout.textContent = s.text; // control steps
        gsap.set(".preview-icon", { scale: s.scale }); // target steps — same state object
        lastStep = s;
      }
    },
  },
  "edit3",
);
```

**Variations:** a dropdown pick → instant conversion (self-conversion) has the pick convert the panel's own readout in place, collapsing control and target into one element (menu pop via the Spring-Pop Entrance rule, row hover-stepping via the Dynamic Content Sequencing rule) — the conversion must be an INSTANT snap, not tweened, since instantness is the feature being sold. An easing-handle drag → target re-animates (deferred mirror): the edit authors a behavior, so the mirror is a REPLAY, not a concurrent transform — beat 1 drags the handle (handle tween plus coords readout), then at a later label the target performs its motion with the newly-authored curve, often under a zoom-out (Viewport Change rule) — the one sanctioned case where the response isn't in the gesture's own beat, but the replay must still be unmistakably the edited parameter. A read-sync mirror (reverse direction) has the gesture happen ON the target (hovering swatches, selecting an element) with the PANEL readout as the bound side — same discrete contract, one state array of `{ t, hoverTarget, readout }` driving both the highlight and the text. A color couple has the readout count while the target's `backgroundColor` tweens between two palette stops at the same label — keep it two fixed stops (GSAP interpolates), never derive per-frame hex strings by hand.

**Values:** SCRUB_DUR 0.8–1.6s — the viewer must see BOTH sides move; under ~0.6s the mirror registers subconsciously at best. SCRUB_EASE `power1.inOut`/`power2.inOut`, shared verbatim by both tweens — never `back.out`/`elastic.out`, since an overshooting value reads as a broken hinge and the readout is data. Edit endpoints should be visible but plausible (e.g. −10° tilt, 38px shift, 1xl→4xl→2xl — a 2° rotation doesn't demonstrate anything). HOLD_BETWEEN 0.3–0.8s (each landed value gets a breath; below 0.3s the beats smear into one gesture). BEAT_COUNT 2–4 (one edit is a moment, not a demo; past 4 the shot reads as a settings tour). Discrete step gaps 0.15–0.5s per discrete-text-sequence pacing, and the first state must equal the on-load state. VALUE_MIN_WIDTH should be at least as wide as the longest value.

**Critical constraints:** one label, one gesture — the readout tween and target tween share position, duration, AND ease; never sequence readout-then-target, and never stagger the target behind the readout even slightly, since a delayed response reads as an animation following an edit rather than a bound surface; a mismatched ease desyncs the mirror mid-tween even when endpoints agree. Discrete steps must share one state object, so both sides read the same array entry and desync is impossible by construction. The readout is data — no overshoot, no bounce on the settle; the target may carry the gesture's ease but must land exactly on the edited value. Co-visibility is load-bearing — control and target share the frame for every edit beat; a camera move must never crop the mirror out. `tabular-nums` plus a fixed `min-width` on every scrubbed readout; `onUpdate` stays O(1). End on a landed edit — the final beat resolves with the value applied and holding.

**See also:** the Cursor-Click Ripple and Context-Sensitive Cursor rules (the hand performing the gesture); the Counting with Dynamic Scale rule (the readout half alone, when there is no bound target); the Discrete Text Sequence rule (retypes inside the control field); the Spring-Pop Entrance rule (dropdowns/chrome around the couple); the Multi-Phase Camera rule (punch-and-return framing); the Chart Scrub Readout rule (the sibling READ direction — a scrub interrogates a chart instead of editing a target).

#### Scale-Swap Transition

Simulates a "morph" between two DOM elements by overlapping exit and entrance scale animations. Lighter weight than the Card Morph Anchor rule below (which morphs container dimensions — use that for SHAPE changes; this rule is for SAME-shape state swaps) and easier than SVG path interpolation.

At a single trigger, two coordinated tweens fire: (1) outgoing — scale from 1.0 to an exit scale plus opacity from 1 to 0, fast `power2.in` (rushing away); (2) incoming — scale from the exit scale to 1.0 plus opacity from 0 to 1, `back.out(BOUNCE_FACTOR)` (arriving with weight). A small overlap window during which both are mid-tween creates the morph illusion; the incoming sits on top via z-index so the outgoing's fade-tail doesn't bleed through.

```html
<!-- Both cards position: absolute; inset: 0 in one fixed-size wrapper — same
     footprint, same transform-origin: 50% 50%. Incoming starts opacity: 0,
     transform: scale(EXIT_SCALE), z-index above the outgoing. -->
<div class="swap-wrap">
  <div class="card outgoing" id="outgoing">{outgoingIcon} {outgoingLabel}</div>
  <div class="card incoming" id="incoming">
    {incomingIcon} {incomingLabel}
    <div class="sub" id="sub">{incomingSubline}</div>
  </div>
</div>
```

```js
// Outgoing: shrink + fade fast
tl.to(
  "#outgoing",
  { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR, ease: "power2.in" },
  TRIGGER,
);

// Incoming: pops in with overshoot, starting OVERLAP before the exit finishes
tl.to(
  "#incoming",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER + EXIT_DUR - OVERLAP,
);

// Inner content reveals AFTER the incoming settles
tl.fromTo(
  "#sub",
  { opacity: 0, y: SUB_REVEAL_Y_PX },
  { opacity: 1, y: 0, duration: SUB_REVEAL_DUR, ease: "power3.out" },
  TRIGGER + EXIT_DUR + SUB_REVEAL_DELAY,
);
```

**Variations:** a delayed inner content reveal is the classic pattern above — morph the container, then reveal inner text once it settles; the 0.2–0.4s gap lets the eye land on the new shape before reading. A triple swap (3-state cycle) chains A→B→C with two triggers; each transition is its own tween pair, the previous incoming becoming the next outgoing — good for state-evolution narratives (early → mid → final labels). A color-shift transition (no scale), for a flat morph between same-shape states, drops the scale and keeps opacity plus a brief background hue tween — less dramatic, more product-UI tone.

**Values:** TRIGGER at or after the outgoing settled plus a presence-dwell — the outgoing must "land" before transforming. EXIT_DUR 0.3–0.5s. ENTER_DUR 0.45–0.7s, longer than EXIT_DUR so the overshoot can settle. OVERLAP 0.1–0.2s (over 0.3s both are clearly visible together — no morph; under 0.05s leaves a visible empty gap). EXIT_SCALE 0.6–0.8 (smaller exits feel dramatic but risk reading as "vanish" instead of "morph"). BOUNCE_FACTOR 1.4 soft / 1.8 firm / 2.2 cartoony. SUB_REVEAL_DELAY 0.2–0.4s (reveals during the morph compete with the swap for attention).

**Critical constraints:** the incoming's z-index must sit above the outgoing, or the outgoing's fade-tail (opacity 0.3–0.5) bleeds through and double-exposes the frame. Both elements must share `transform-origin: 50% 50%`, or the morph reads as one thing teleporting elsewhere. Bouncy ease ONLY on the incoming — outgoing `power2.in`, incoming `back.out`; reversed, the swap feels mechanical. Both cards must be `position: absolute; inset: 0` in the same fixed-size wrapper (sized to fit both states — the wrap never resizes). Don't `display: none` the outgoing after the fade — leave it at zero opacity so layout doesn't reflow. Inner content reveals after the container settles, and climax dwell of at least 1s after the final state and subline land.

**See also:** the Press-Release Spring rule (a button press TRIGGERS the swap — cause and effect); the Card Morph Anchor rule below (shape-changing alternative); the Reactive Displacement rule (when the replacement should read as a causal collision); the Sine Wave Loop rule (idle breathing on the final state).

#### Card Morph Anchor

A free-floating container morphs apparent size, corner radius, and surface treatment between two shots — the morph itself IS the transition; the viewer's eye tracks the persistent container. Distinct from the Anchored Layout Expand rule above (an edge-pinned live layout participant that grows along one axis and reflows neighbors — here nothing is pushed) and the Theme Crossfade Morph rule below (a whole-theme reskin under a fixed anchor — here a single container changes shape).

**How it works:** since `width`/`height` tweens are forbidden, substitute uniform `scale` for apparent size; the remaining morph channels are paint-only — `borderRadius`, `background`, `boxShadow`. All channels ride ONE tween (one ease, one duration) so the shape morphs in lockstep. Content choreography: old content fades out during the first ~40% of the morph, new content fades in during the last ~40% — the shape-only gap between is the natural "blink." Optionally the morph card itself fades at the very end, revealing the real next-shot element rendered behind it.

```html
<!-- DOM order = stacking: the anchor renders BEFORE the card, so the card is on top -->
<div class="next-shot-anchor"><img src="{nextShotAnchor}" alt="anchor" /></div>
<div class="morph-card">
  <div class="content-old">{shotOneContent}</div>
  <div class="content-new">{shotTwoContent}</div>
</div>
```

```css
.morph-card {
  width: SHOT_ONE_W;
  height: SHOT_ONE_H; /* shot-1 geometry; the morph is scale, never width/height */
  border-radius: SHOT_ONE_RADIUS;
  background: {surfaceShotOne};
  overflow: hidden; /* content must clip during the shape change */
  display: grid;
  place-items: center;
  will-change: transform;
}
.content-old,
.content-new {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.content-new {
  opacity: 0; /* author its inner sizes at apparent-size ÷ END_SCALE — it scales with the card */
}
.next-shot-anchor {
  position: absolute;
  opacity: 0; /* fades in as the morph card fades out */
}
```

```js
const END_SCALE = SHOT_TWO_W / SHOT_ONE_W; // uniform — keep the two shots aspect-matched

// Hold shot 1 for HOLD_BEAT first — an instant morph reads as glitchy.

// One tween, all channels: uniform scale + paint-only properties.
tl.to(
  ".morph-card",
  {
    scale: END_SCALE,
    borderRadius: SHOT_TWO_RADIUS / END_SCALE, // borderRadius is pre-scale — divide to land the APPARENT radius
    background: "{surfaceShotTwo}",
    boxShadow: "{shadowShotTwo}",
    duration: MORPH_DUR,
    ease: "power2.inOut",
  },
  MORPH_START,
);

tl.to(
  ".content-old",
  { opacity: 0, duration: MORPH_DUR * OLD_FADE_FRAC, ease: "power1.in" },
  MORPH_START,
);
tl.to(
  ".content-new",
  { opacity: 1, duration: MORPH_DUR * NEW_FADE_FRAC, ease: "power1.out" },
  MORPH_START + MORPH_DUR * (1 - NEW_FADE_FRAC),
);

// Optional handoff — card fades out over the pixel-identical real anchor.
tl.to(
  ".morph-card",
  { opacity: 0, duration: MORPH_DUR * FINAL_FADE_FRAC, ease: "power1.in", immediateRender: false },
  MORPH_START + MORPH_DUR * (1 - FINAL_FADE_FRAC),
);
tl.to(
  ".next-shot-anchor",
  { opacity: 1, duration: MORPH_DUR * FINAL_FADE_FRAC, ease: "power1.out" },
  MORPH_START + MORPH_DUR * (1 - FINAL_FADE_FRAC),
);
```

**Morph channels:** apparent size — uniform `scale`, the substitution for the forbidden width/height tween, aspect preserved. `borderRadius` — paint-only, in pre-scale units (tween to apparent radius divided by end scale, capped at half the smaller side). `background` — paint-only; gradients interpolate only with equal stop counts (solid→solid uses `backgroundColor` instead). `boxShadow` — paint-only; a base shadow to accent glow shifts emphasis.

**Variations:** landing on a non-centered target (a dock icon, sidebar slot) adds `x`/`y` to the same tween, computed as the FLIP-style delta between the card's and the target's rects — both measured at build time (single-scene only) and tweening the difference; don't hand-compute from CSS values, since paddings, borders, and parent transforms compound. An aspect change between shots is absorbed by morphing to the nearest uniform fit and letting the crossfade/handoff absorb the small delta, or dropping the handoff and holding the card's final state.

**Values:** HOLD_BEAT 0.6–1.5s, at least the shot-1 entry settle time — the viewer must register shot 1 first. MORPH_DUR 0.6–1.2s (under 0.5s can't fit both content fades). END_SCALE equals SHOT_TWO_W divided by SHOT_ONE_W (icon-sized handoffs typically land at 80–400px apparent width). SHOT_TWO_RADIUS ≤ half the smaller apparent side (half = a perfect circle; beyond is clamped). OLD/NEW_FADE_FRAC 0.3–0.5 each, summing to ≤1 (the gap between is the shape-only "blink"). FINAL_FADE_FRAC 0 (no handoff) or 0.1–0.2 (only when a pixel-identical anchor exists). Ease: `power2.inOut` canonical, `power3`/`expo.inOut` OK — never `back`/`elastic`, since overshoot fights the shape change.

**Critical constraints:** the uniform-scale substitution is mandatory — never tween `width`/`height`; scale plus the paint-only channels are the ONLY morph properties. The handoff anchor must be pixel-identical to the card's final state (same apparent size, radius, background, shadow, inner icon dimensions) — any delta is a visible pop during the crossfade; if it can't match exactly, drop the handoff and hold the morph card. Stacking must be by DOM order, never a z-index snap mid-fade — render the anchor before the card, since a `set` during an active opacity tween flips stacking before the fade finishes and flickers. `overflow: hidden` on the card, since content must clip as the radius changes. Hold a beat before morphing, and use the same ease family for shape and crossfade.

**See also:** the Anchored Layout Expand rule (edge-pinned one-axis growth with reflow); the Theme Crossfade Morph rule below (whole-theme reskin under a fixed anchor); the Scale-Swap Transition rule above (content swap without shape change); the Sine Wave Loop rule (a breath on the final state).

#### Theme Crossfade Morph

The whole world re-skins while one thing holds still. A composer box cycles through four IDE themes; a checkout widget flips through brand skins — background, typography, corner radii, toolbar icons, footer logos all change AT ONCE, in place, in ~0.3s, N times — and through every flip one anchor element (the prompt string, the widget layout, the wordmark) NEVER MOVES. The anchor's stillness is the rhetorical claim: everything changes, this doesn't.

Boundary: the Card Morph Anchor rule above morphs one container between two shots — its dimensions, radius, and surface tween continuously. This rule re-skins an ENTIRE scene through N discrete states — nothing tweens property-by-property (fonts, icons, and logos can't interpolate); the "morph" is a fast simultaneous crossfade of complete pre-styled layers. (The Scale-Swap Transition rule swaps an element at center; here the surroundings swap and the element holds.)

**How it works:** (1) one skin = one complete layer — each theme state is a fully pre-styled, full-bleed layer containing everything that changes (background, shell/chrome, toolbar icons, footer logos, typography); all skins exist in the DOM from t=0, stacked, with skin 0 starting visible and the rest at zero opacity. (2) the morph is a crossfade — at each boundary, two opposing opacity tweens run at the same timeline position over ~0.3s: outgoing 1→0, incoming 0→1. Because both layers are complete, every property "blends" simultaneously for free — including the un-tweenable ones (font families, icon glyphs, logos), which read as morphing precisely because everything else is mid-blend around them. (3) the anchor renders once, on top — the element that must not move lives in its own layer above all skins and is EXCLUDED from every skin layer; no transforms, no re-parenting, no per-skin restyle. (4) windows are precomputed — each boundary's time is `cycleStart + k × (skinHold + morphDur)`, steady cadence by default, holding the final skin longest when it's the resolve.

The only animated property is `opacity` — which is why this rule is seek-safe with zero special machinery.

```html
<div class="theme-stage">
  <!-- One complete pre-styled layer per skin; skin-0 visible at t=0 -->
  <div class="skin skin-0"><div class="shell">…terminal chrome, mono type, footer badge…</div></div>
  <div class="skin skin-1">
    <div class="shell">…rounded composer, sans type, toolbar pills, logo…</div>
  </div>
  <div class="skin skin-2"><div class="shell">…dark shell, its own chrome and footer…</div></div>

  <!-- The anchor: rendered ONCE, above every skin. It never moves. -->
  <div class="anchor" id="anchor">{anchorText}</div>
</div>
```

```css
.theme-stage {
  position: absolute;
  inset: 0;
}
.skin {
  position: absolute;
  inset: 0;
  opacity: 0;
  /* Each skin fully self-styled: its own background, fonts, radii,
     icons, chrome, logos. Nothing inherited across skins. */
}
.skin-0 {
  opacity: 1; /* the opening state — matches the timeline's fromTo */
}
.shell {
  /* CRITICAL: shared geometry. The shell box (and any element that
     "persists" across skins — toolbar row, footer row) sits at the SAME
     coordinates in every skin, so mid-blend frames read as one UI
     changing clothes, not two UIs ghosting. */
  position: absolute;
  left: SHELL_LEFT;
  top: SHELL_TOP;
  width: SHELL_WIDTH;
  height: SHELL_HEIGHT;
}
.anchor {
  position: absolute;
  z-index: 10; /* above every skin */
  left: ANCHOR_LEFT;
  top: ANCHOR_TOP;
  /* No transforms, no transitions — the stillness is load-bearing. */
}
```

```js
const skins = gsap.utils.toArray(".skin");

// Boundary k→k+1 at T_k: outgoing fades down as incoming fades up —
// ONE simultaneous crossfade, everything blends at once.
skins.forEach((skin, k) => {
  if (k === 0) return; // skin-0 is the opening state
  const at = CYCLE_START + k * (SKIN_HOLD + MORPH_DUR);
  tl.fromTo(skin, { opacity: 0 }, { opacity: 1, duration: MORPH_DUR, ease: "power2.inOut" }, at);
  tl.to(
    skins[k - 1],
    { opacity: 0, duration: MORPH_DUR, ease: "power2.inOut" },
    at, // same position — the blend is simultaneous, never sequential
  );
});

// The anchor gets NO tweens. Its absence from the timeline is the point.
```

**Variations:** an anchor-typography reskin (per-layer copies) — when the anchor's own type treatment must change with the theme (mono in a terminal skin, sans in an editor skin), each skin carries its own copy of the anchor at PIXEL-IDENTICAL geometry and there is no separate top layer; the invariant shifts from "one element" to "one geometry" — verify by screenshotting two skins at 50% opacity, since a couple-pixel baseline drift reads as the anchor flinching. A skin-cycle tour with logo relay crossfades a large brand logo outside the anchored shell in the SAME windows as the skins (logo k with skin k, same duration) — the paired swap sells "same product, every brand." A washout finale fades in a faint low-key layer (dot-grid, blueprint wash) after the last skin while the last shell drops toward ~0.25 opacity, resolving the cycle into a held diagram of itself. An emphasis brake uses steady cadence for N−1 skins, then holds the final skin 2–3× the normal hold — the cycle demonstrates breadth, the brake lands the resolve.

**Values:** N_SKINS 3–5 (two is a before/after — consider the Card Morph Anchor rule instead; past five the cycle pads). SKIN_HOLD 0.8–1.5s (long enough to register the logo/footer identity, short enough to keep the churn rhetorical). MORPH_DUR 0.25–0.4s, ~0.3s canonical (faster reads as a hard cut; slower reads as a mushy dissolve with lingering double-exposure). CYCLE_START at or after the anchor settle plus a beat. Shell geometry must be identical across skins; contents inside the slots differ freely. Anchor position must be pixel-identical across the scene (or, in the per-layer form, identical in every skin). Washout/brake: shell drops to ~0.2–0.3 opacity, hold 2–3× SKIN_HOLD.

**Critical constraints:** the anchor never moves — no transforms, no opacity dips, no re-parenting, no restyle; the contrast between total churn and total stillness is the entire device, and one flinch turns the shot into a slideshow. Nothing tweens but `opacity` — no `borderRadius`/`background` tweens; radii and colors change by being different in the next layer; visibility toggles only via `opacity`, never `display`/`visibility`. Pixel-align the shared geometry, since mid-blend both skins are partially visible — aligned shells read as one UI changing clothes, misaligned shells ghost into two UIs. Pre-style everything — each skin is complete and static, no class toggling, no runtime restyle mid-tween. Outgoing and incoming tweens must share one timeline position, or a staggered blend flashes the stage background between skins. Adjacent windows only — skin k crossfades with k+1, never k+2; at no frame are three skins partially visible. Camera static, always — a push-in on top of a theme cycle destroys the stillness that makes the anchor read. Hard cuts are the cheaper sibling — if the states should snap rather than blend, that belongs to the Discrete Text Sequence rule instead.

**See also:** the Context-Sensitive Cursor rule (caret color switches at each boundary); the Discrete Text Sequence rule (type the anchor first; or the hard-cut alternative); the Card Morph Anchor rule (the single-container sibling); the Spring-Pop Entrance rule (the lockup that joins the anchor at the resolve); the Sine Wave Loop rule (drifting field under the cycle — never on the anchor).

#### Spring-Pop Entrance

> Smooth beats bouncy. This entrance defaults to a smooth long-tail settle — `power3.out` (or `expo.out` for a faster front) — that decelerates cleanly into the resting size with NO overshoot. Bouncy `back.out` is the #1 instant turn-off in agent-made videos and is almost never executed well; it is a rare, explicitly-playful exception (consumer/fun brand), never the default. When unsure, settle smoothly.

THE entrance primitive: an element (or staggered group) arrives by springing from nothing — `scale: 0 → 1`, optional small `y` rise — and settles without bouncing. This is arrival, not reaction: distinct from the Press-Release Spring rule above (a click/press → release feedback chain on an element that already rests on screen).

**How it works:** one `fromTo` carries the whole arrival — from `{ scale: 0, opacity: 0 }` (explicit, so t=0 is correct under seek) to `{ scale: 1, opacity: 1, ease: "power3.out" }`. For a group, the same `fromTo` runs per element at an index-based stagger, capped so the group reads as one arriving beat. The scale grow is load-bearing; the y rise is garnish — drop everything else and it must still read as a clean entrance. Let the ease produce the settle; never hand-key an intermediate overshoot state, since it double-bounces against the curve.

```html
<div class="pop-hero" id="hero">{heroLabel}</div>

<div class="pop-grid">
  <div class="pop-item">{itemA}</div>
  <div class="pop-item">{itemB}</div>
  <div class="pop-item">{itemC}</div>
</div>
```

```css
.pop-hero,
.pop-item {
  transform-origin: 50% 50%; /* in-place pop; move to the source point for the anchored variation */
  will-change: transform;
}
.pop-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: GRID_GAP;
  place-items: center;
}
```

```js
// Single hero pop — smooth long-tail settle, no overshoot.
tl.fromTo(
  "#hero",
  { scale: 0, opacity: 0 },
  { scale: 1, opacity: 1, duration: POP_DUR, ease: "power3.out" },
  ENTRY_AT,
);

// Staggered group pop — one arriving beat.
gsap.utils.toArray(".pop-item").forEach((el, i) => {
  tl.fromTo(
    el,
    { scale: 0, opacity: 0, y: Y_RISE },
    { scale: 1, opacity: 1, y: 0, duration: POP_DUR, ease: "power3.out" },
    GROUP_ENTRY_AT + i * STAGGER,
  );
});
```

**Variations:** a calm settle (premium/enterprise) uses `power3.out`, no rotation, a small y rise of 0–12px — a weighted, confident landing for a hero wordmark or product shot. A firm settle (everyday default) uses `power3.out` or `expo.out` for a punchier front, with a y rise around 24px — cards, icons, callouts. An exact-physics settle swaps the ease for the baked spring ease function documented in the GSAP Easing and Stagger adapter section above (critically damped), taking the duration from the helper. An origin-anchored pop, for a callout growing out of a specific point (a marker, a pointer tip), sets `transform-origin` to that point so the scale grow reads as "emerging from the source" rather than "inflating in place." Popping into a held slot should land and hold still — no idle loop baked into the entrance; hand off to the Sine Wave Loop rule for subtle jitter if the held frame genuinely needs life, but prefer revealing the next element on its own cue instead. A bouncy pop (RARE — explicitly-playful only) swaps the ease for `back.out(OVERSHOOT)` and optionally settles a small rotation from a starting angle to 0, only for a deliberately playful register — never product/enterprise/serious tone, and even then keep the overshoot at ≤~2, or better, use the baked spring at a damping fraction of 0.6–0.7 (~5–10% overshoot that reads physical where `back.out` reads cartoon).

**Values:** EASE `power3.out` default, `expo.out` punchier — `back.out(OVERSHOOT)` only in the playful variant. POP_DUR 0.4–0.7s (shorter = tight snap; the hero must be visible by t ≤ 0.5s). STAGGER 0.04–0.08s, self-capped by roughly `min(0.06, 0.5 / itemCount)`. ITEM_COUNT 3–9 (over 9, the stagger vanishes — switch to a wipe/sweep reveal instead). Y_RISE 0–32px, small — never large enough to read as a slide-up. ROT_FROM −10° to +10°, playful variant only, alternating sign by index. ENTRY_AT 0–0.4s (a beat of quiet, but keep the subject landing by t ≤ 0.5s).

**Critical constraints:** default ease is `power3.out` (no overshoot); `back.out` only in the explicitly-playful variant, and there keep the overshoot ≤~2. Item count times stagger must be ≤ roughly 0.5s, so the group lands inside one beat. Entrances must state the collapsed from-state in `fromTo` — never rely on a CSS-hidden start, since it would render visible before the tween claims it under seek. `transform-origin: 50% 50%` for an in-place pop; the source point only for the anchored variation. This is a finite arrival — idle motion on a held element is a separate, later Sine Wave Loop tween.

**See also:** the Center-Outward Expansion rule (pop while radiating to slots); the Press-Release Spring rule (the click-feedback counterpart); the Sine Wave Loop rule (post-arrival jitter, sparingly).

#### Motion-Blur Streak

Real motion blur isn't available to a seeked renderer (it integrates over shutter time), so this rule FAKES it for a fast fly-in or hard camera push-through. The whole point is the coupling: the blur envelope rides the SAME ease and window as the position tween, so peak blur lands exactly on peak speed and the element is razor-sharp the instant it stops. Two paths: (A) directional SVG blur — inline `<feGaussianBlur stdDeviation="X 0">` (X on the motion axis, 0 across it), tweened via a proxy, cleanest for a true directional smear; (B) echo/ghost trail — 2–4 duplicates at decreasing opacity, offset backward along the motion vector, collapsing into the lead as it settles, no filter cost, a stylized "speed-line" trail.

Entrances and mid-shot moves only — never a mid-composition exit. A blurred element fleeing off-frame mid-composition reads as a glitch; a hard exit between scenes belongs to the composition's own transition machinery (see the Transitions Catalog below). One sanctioned scope extension: the envelope may ride the camera wrapper during a travel leg — see the camera-travel carve-out below.

**How it works:** a fast `out`-eased move front-loads velocity — fastest off the start, bleeding to zero at the settle. Map the blur/echo envelope onto that same curve: position travels from an off-frame/pushed-back start to rest over the move duration; in lockstep on the same window and ease, the smear goes from peak blur to 0 (path A) or the ghosts collapse onto the lead (path B). By the settle the element is fully crisp and dwells at least 1s — the contrast between violent streak and still, sharp settle IS the effect. GSAP can't tween an SVG attribute directly — tween a plain proxy object and write the `stdDeviation` in `onUpdate`, seeding it once at setup so a seek to t=0 shows the streaked start.

```html
<!-- inside a standard scene clip; overflow: hidden on the scene (the smear extends past rest) -->
<svg width="0" height="0" aria-hidden="true" style="position: absolute">
  <filter id="streak" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur id="streak-blur" in="SourceGraphic" stdDeviation="0 0" />
  </filter>
</svg>
<div class="streak-el" id="streak-el" style="filter: url(#streak)">{phrase}</div>
<!-- Path B instead: N-1 aria-hidden .streak-ghost duplicates BEHIND the lead, no filter -->
```

```js
// Path A — proxy-tweened directional blur.
const blurNode = document.getElementById("streak-blur");
const blurProxy = { v: PEAK_BLUR };
const writeBlur = () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} 0`); // X axis only
writeBlur(); // seed frame 0 — a seek to t=0 must show the streaked start, not a sharp pre-frame

tl.fromTo(
  "#streak-el",
  { x: ENTER_FROM_X, opacity: 0 },
  { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
  MOVE_START,
);
tl.to(blurProxy, { v: 0, duration: MOVE_DUR, ease: MOVE_EASE, onUpdate: writeBlur }, MOVE_START);

// Path B — ghosts on the SAME window/ease; per-ghost variation by index.
gsap.utils.toArray(".streak-ghost").forEach((g) => {
  const i = Number(g.dataset.i); // 1..N-1, set in HTML
  tl.fromTo(
    g,
    { x: ENTER_FROM_X - i * ECHO_STEP_PX, opacity: GHOST_BASE_OPACITY / i },
    { x: 0, opacity: 0, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );
});
```

**Variations:** a vertical streak swaps axes — `y`, `stdDeviation="0 Y"`, vertical echo offsets. A camera push-through uses a symmetric depth-wise blur envelope (`stdDeviation="B B"`) alongside a scale-from tween, so the wordmark punches out of soft focus and snaps crisp at the lock. A staggered grid streak-in has each card streak into its slot at an index-based offset, with its own blur proxy/ghosts, sharp the instant it lands. A hold-the-streak variant runs the blur on a marginally slower curve than the position (e.g. position `expo.out`, blur `power3.out`) so the last wisp resolves just after arrival — sparingly, the default is locked envelopes.

**Camera-travel carve-out:** the envelope is also sanctioned at the wrapper level — on the camera-wrapper of a virtual-camera scene (Viewport Change, Multi-Phase Camera, or 3D Camera Flight rules above) during a travel leg — a dive, a whip sweep, a violent final push. This does NOT violate "never a mid-composition exit": the world never leaves frame, the camera travels through it, and every leg ends with the world at rest, sharp, inside the frame. Each leg is an arrival at the next pose, so the entrance doctrine applies leg by leg. Three deltas from the element-level recipe: (1) the envelope follows the leg's ease — an `out` leg (dive, final push) uses the base recipe unchanged, while an `inOut` repositioning leg peaks mid-leg (split the envelope at the velocity peak, 0→peak on the in-half ease over the first half, peak→0 on the out-half over the second, seeding the proxy at 0 for these since the streaked state lives mid-leg, not at t=0). (2) filter placement — for a 2D camera, `filter: url(#streak)` goes on the world wrapper; for 3D flight, it goes on the perspective stage above the 3D context, since a filter on a `preserve-3d` element flattens it and collapses every `translateZ` (never per-element inside the world — one frame-wide envelope, not N desynced ones). (3) full-frame blur is heavy — cap the peak blur around 18–20 at wrapper level (vs. 30 for one element); a brief whip may touch ~24; the axis rule stays the same (`"X 0"` for a lateral whip/pan, `"B B"` for a dive/push).

A named "whip sweep" composition — the heavily-blurred lateral whip that resolves into the next region — is two rules on one window: position via the Nudge Curve rule's three-phase chain (below), tuned burst-dominant (tail still ≥3× ramp-in in time), and blur ramping 0→peak across the ramp-in, held at peak through the linear burst (constant velocity = constant smear), peak→0 across the tail. Swap or reveal the next region's content DURING the burst — the smear masks the change; the `power4.out` tail lands it sharp.

```js
tl.to(cam, { x: WHIP_X * 0.1, duration: 0.12, ease: "power3.in", onUpdate: applyCamera }, WHIP_AT);
tl.to(
  cam,
  { x: WHIP_X * 0.75, duration: 0.1, ease: "none", onUpdate: applyCamera },
  WHIP_AT + 0.12,
);
tl.to(
  cam,
  { x: WHIP_X, duration: 0.35, ease: "power4.out", onUpdate: applyCamera },
  WHIP_AT + 0.22,
);

tl.to(blurProxy, { v: PEAK_BLUR, duration: 0.12, ease: "power3.in", onUpdate: writeBlur }, WHIP_AT);
// blur holds at PEAK through the linear burst (no tween needed — value rests at PEAK)
tl.to(blurProxy, { v: 0, duration: 0.35, ease: "power4.out", onUpdate: writeBlur }, WHIP_AT + 0.22);
```

**Values:** MOVE_EASE `expo.out`/`power4.out` (default)/`power3.out`, `out`-family ONLY — `in`/`inOut` puts peak speed in the wrong place. MOVE_DUR 0.25–0.6s (over ~0.7s reads as a focus pull, not velocity). ENTER_FROM_X/Y 40–120% of the element's own dimension (enough runway for the streak to read). PEAK_BLUR 8–30, default 18 (over 30 erases the glyph at the start; ~18–20 is the cap at wrapper level). SCALE_FROM 1.3–2.5 for the push-through variation. N (ghosts) 2–4 (over 4 reads as strobe, not streak). ECHO_STEP_PX 12–40px (N times the step should stay roughly inside the entry runway). GHOST_BASE_OPACITY 0.3–0.6 (opaque ghosts read as duplicate elements). CARD_STAGGER 0.05–0.12s (one assembling wave, not separate arrivals).

**Critical constraints:** blur peaks at peak speed and resolves to 0 at the settle — share the ease and window between position and envelope, or a blur that lingers after the stop reads as a focus pull. Entrances/mid-shot arrivals only — never a mid-composition exit; wrapper-level use only per the carve-out. Seed `stdDeviation` at setup — at the peak for the entrance shape, at 0 for a whip/`inOut` leg. Use a generous filter region (extending well past the element's box) or the smear clips at the box edge. Match the directional axis to the motion — `"X 0"` horizontal, `"0 Y"` vertical, `"B B"` only for a depth/scale move (symmetric blur on a sideways move looks like defocus). Dwell at least 1s sharp after the snap — a streak landing at the very last beat reads as "flashed and gone." Use it on a heavy element on a solid field — thin type or a busy backdrop swallows the smear. `overflow: hidden` on the scene, since the smear/furthest ghost extends past the resting position during travel.

**See also:** the Kinetic Beat Slam rule (streak as one beat's entrance); the Center-Outward Expansion rule (grid streak-in); the Scale-Swap Transition rule (same-footprint morph — not an arrival); the Nudge Curve rule below (the whip sweep's position half); the 3D Camera Flight and Viewport Change rules (the carve-out's wrappers).

#### Waterfall Entry

Staggered ARRIVAL cascade: words/elements whip in from below (one consistent direction), each starting before the previous settles — an accelerating wave that resolves into a composed layout. Title cards, segment openers, list/feature intros.

This is an in-scene arrival, not a scene-to-scene seam. Its seam sibling (a different, related technique for cutting BETWEEN scenes, not covered in this rule) follows a different rule set — do not mix the two: for an arrival like this one, opacity is BINARY 0→1 via `tl.set` at entry (never fade), the default axis is Y from below, and there is no outgoing side. The scene-to-scene version instead ignites at partial opacity mid-path (the fade IS the velocity trick there) and runs words out on a mirrored ease — treat these as two distinct techniques even though they share a name.

**Choreography:** overlap, don't queue — the next element starts within roughly ±2 frames of the previous settling, gaps SHRINK across the cascade, and the last element snaps. Velocity varies by weight — heavy/anchor elements travel further and longer, light words/punctuation snap in tight:

| Parameter | Anchor/heavy | Normal word | Light/punctuation |
| --- | --- | --- | --- |
| Y offset | 60–80px | 40–50px | 30–48px |
| Duration | 0.16–0.20s | 0.13–0.16s | 0.10–0.13s |
| Overlap | 0–2f gap | 1f overlap | 1–2f overlap |

Ease `power4.out` (`expo.out` for extra snap); never `.inOut` on an entry. One direction per cascade. Split the FINAL word into fragments to extend the climax; fragments travel further. Post-settle, the group usually slides to make room for the next beat — that's the Nudge Curve rule below.

**JS pattern:** each element gets a `tl.set` (instant reveal plus offset) then a `tl.to` (whip to rest). The next element's start time equals the previous element's start plus its duration, minus an overlap-frames × frame-duration term (positive overlap = cascade, negative = a deliberate gap). CSS: elements start at `opacity: 0; display: inline-block`.

```js
var F = 1 / 60;
var t0 = 0.1;
// anchor (heaviest): biggest travel, longest settle
tl.set("#el-1", { opacity: 1, y: 80 }, t0);
tl.to("#el-1", { y: 0, duration: 0.18, ease: "power4.out" }, t0);
// normal word: 2 frames after the anchor finishes
var t1 = t0 + 0.18 + 2 * F;
tl.set("#el-2", { opacity: 1, y: 45 }, t1);
tl.to("#el-2", { y: 0, duration: 0.15, ease: "power4.out" }, t1);
// light word: 1 frame BEFORE the previous finishes (overlap)
var t2 = t1 + 0.15 - F;
tl.set("#el-3", { opacity: 1, y: 40 }, t2);
tl.to("#el-3", { y: 0, duration: 0.14, ease: "power4.out" }, t2);
// split final-word fragments: tightest overlap, extra travel (lighter)
var t3 = t2 + 0.14 - F;
tl.set("#frag-a", { opacity: 1, y: 70 }, t3);
tl.to("#frag-a", { y: 0, duration: 0.16, ease: "power4.out" }, t3);
var t4 = t3 + 0.14 - F;
tl.set("#frag-b", { opacity: 1, y: 70 }, t4);
tl.to("#frag-b", { y: 0, duration: 0.15, ease: "power4.out" }, t4);
// punctuation: lightest, fastest
var t5 = t4 + 0.13 - 2 * F;
tl.set("#dot", { opacity: 1, y: 48 }, t5);
tl.to("#dot", { y: 0, duration: 0.12, ease: "power4.out" }, t5);
```

**Anti-patterns:** don't queue entries where each waits for the previous to fully settle — overlap by ±1–2 frames so the cascade reads as a wave, not a queue. Don't use the same offset/duration for every cascade element — vary by weight, since anchors travel further and punctuation snaps. Don't apply a gradual opacity fade on an arrival — use a binary 0→1 opacity via `tl.set` instead, since fading fights the snap (a seam cut fades, an arrival doesn't).

#### Particle Burst

Discrete flying particles as a one-shot event: a confetti pop that erupts upward and drifts back down on gravity, a dot burst radiating from behind a landing word, or a glyph dissolve where text breaks into particles that scatter and die. Particles are ephemeral garnish — born from a beat, they fly, then are gone; they never become layout.

Boundaries: the CSS Marker Patterns rule's burst mode is radiating DRAWN LINES — a static accent, no flight. The Press-Release Spring rule's release burst is one blurred radial layer faking an explosion — enough when a single glow pop will do. The Center-Outward Expansion rule moves REAL LAYOUT ELEMENTS to final resting slots; particles have no destination, only physics and a death.

**How it works:** the whole event is one driver tween and one formula. (1) Seeded setup — a fixed pool of particle divs is created once at composition setup (a deterministic loop; setup-time generation is fine, per-frame DOM creation is not). Each particle derives everything from a pure hash function of its index:

```js
// angle, speed, size, spin, color (palette[i % palette.length]) — all from prand(i * k)
const prand = (n) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x); // 0..1, pure function of n
};
```

(2) A ballistic formula — a proxy tween advances a progress value `T: 0 → 1` over the flight duration with `ease: "none"`; `onUpdate` positions every particle as a pure function of `T`:

```
x(T) = vx · T·FLIGHT_DUR
y(T) = vy · T·FLIGHT_DUR + ½ · G · (T·FLIGHT_DUR)²
rot(T) = spin · T·FLIGHT_DUR
```

Gravity supplies the rise-decelerate-fall arc for free. Because position is computed from `T` (never accumulated per frame), a seek to any moment renders the exact mid-flight state — this is what makes DOM particles seek-safe. The driver's `ease: "none"` is load-bearing — the physics lives in the formula, and an eased driver warps gravity so the arc stops reading as thrown objects.

(3) Death — an opacity tail inside the same formula (fading over the last fraction of the flight), or the confetti signature: a separate instant-shrink tween scaling the pool to 0 in a blink at flight end. Either way the particles end invisible and stay invisible.

```html
<div class="burst-stage">
  <div class="particle-field" id="particle-field"></div>
  <div class="burst-hero" id="burst-hero">{heroWord}</div>
</div>
```

```css
/* .burst-stage: position: relative; display: grid; place-items: center.
   .burst-hero: z-index: 2 — particles fly BEHIND the word. */
.particle-field {
  position: absolute;
  z-index: 1;
  left: 50%;
  top: 50%; /* the launch origin — offset to taste (e.g. the word's baseline) */
  width: 0;
  height: 0;
}
.particle {
  position: absolute;
  left: 0;
  top: 0;
  border-radius: 2px; /* confetti chip; 50% for dots */
  opacity: 0; /* invisible until the event fires */
  will-change: transform, opacity;
}
```

```js
// Setup: deterministic pool, generated ONCE.
const field = document.getElementById("particle-field");
const palette = ["{accentA}", "{accentB}", "{accentC}"]; // 3-5 brand tokens
const parts = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const el = document.createElement("div");
  el.className = "particle";
  const size = SIZE_MIN + prand(i * 3 + 1) * (SIZE_MAX - SIZE_MIN);
  el.style.width = `${size}px`;
  el.style.height = `${size * 0.7}px`; // slightly oblong = confetti chip
  el.style.background = palette[i % palette.length];
  field.appendChild(el);
  // Index-seeded launch parameters — the particle's whole life, fixed here.
  const angle = -Math.PI / 2 + (prand(i * 5 + 2) * 2 - 1) * CONE; // upward cone
  const speed = SPEED_MIN + prand(i * 7 + 3) * (SPEED_MAX - SPEED_MIN);
  parts.push({
    el,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed, // negative = up
    spin: (prand(i * 11 + 4) * 2 - 1) * SPIN_MAX,
  });
}

// Confetti pop — one driver, pure ballistic formula.
const drive = { T: 0 };
tl.fromTo(
  drive,
  { T: 0 },
  {
    T: 1,
    duration: FLIGHT_DUR,
    ease: "none", // physics lives in the formula, not the ease
    onUpdate: () => {
      const t = drive.T * FLIGHT_DUR; // seconds of flight — pure function of T
      const fade = Math.min(1, (1 - drive.T) / FADE_FRAC); // opacity tail
      parts.forEach((p) => {
        const x = p.vx * t;
        const y = p.vy * t + 0.5 * G * t * t; // rise, stall, drift down
        p.el.style.transform = `translate(${x}px, ${y}px) rotate(${p.spin * t}deg)`;
        p.el.style.opacity = String(drive.T === 0 ? 0 : fade); // T===0 guard covers seeks before the event
      });
    },
  },
  BURST_AT,
);
```

**Variations:** a confetti pop followed by an instant-shrink is the playful signature — a full burst, a gravity drift, then every chip scales to 0 in a blink (a fade fraction near 0, plus a shrink tween on all particles at flight-end minus the shrink duration); keep the whole event tiny relative to the subject, a garnish measured in a few dozen pixels, not a screen-filling cannon. A dot burst behind a landing word is radial instead of a cone (angle derived directly from the index across a full circle), with gravity near 0, a short flight (0.4–0.7s), round dots, and the pool z-indexed behind the word, firing at the word's settle frame. A glyph dissolve seeds each particle's origin across the glyph block's own box, with a gentle outward drift and low gravity; the text fades out over the first ~30% of flight while particles fade in from its silhouette, colored to match the text so the swarm reads as the text's own material (true per-pixel dissolves are Canvas-2D territory, per the Canvas 2D Procedural Art technique earlier in this document; this DOM version sells it up to roughly 40 particles). A two-stage burst splits the pool — 70% on the main driver, 30% on a second driver ~0.12s later with lower speeds, the split index-derived; same formula, two windows.

**Values:** PARTICLE_COUNT 10–18 for a pop/dots, 24–40 for a dissolve, capped around ~40 (per-frame style writes; past that, seek performance and visual register both degrade). G 900–1600 px/s² for confetti (natural fall), 0–200 px/s² for dots/dissolve (drift). SPEED_MIN/SPEED_MAX 250–700 px/s, per-particle via the hash function, never uniform. CONE 0.35–0.8 radians (~20–45°) — wider reads as a splash, narrower as a fountain. FLIGHT_DUR 0.7–1.4s; the arc should peak roughly 35–45% of the way through flight (check that `|vy| / G ≈ 0.4 × FLIGHT_DUR`). SIZE_MIN/SIZE_MAX 5–14px for chips, 4–8px for dots, on a 1080p frame. SPIN_MAX 180–720 deg/s for confetti, 0 for dots. FADE_FRAC 0.2–0.35 (near 0 when using the instant-shrink form). BURST_AT should be on a cause — the word's settle, a click, a lockup completing — an uncaused burst is noise.

**Critical constraints:** position must be a pure function of time with the driver ease `"none"` — `x(T)`, `y(T)`, `rot(T)` computed from the driver value every frame, never accumulated per tick (accumulation breaks the moment the renderer seeks); gravity IS the formula, so an eased driver bends the parabola. Use a fixed pool with no per-frame DOM creation — all particles exist after setup at zero opacity, and the event only writes `transform`/`opacity`; keep the particle count at or below roughly 40, since per-frame style writes scale linearly with it. Particles must start AND end at zero opacity — the `drive.T === 0` guard covers seeks to before the event, and the tail/shrink covers seeks after; a chip frozen mid-air at driver end is a bug on every subsequent frame. Particles are punctuation — one event per beat, fired on a cause, small relative to the subject, dead before the next beat, z-ordered behind or around the word it celebrates, never over it. A persistent particle system is a background effect, and that's a different technique from this rule.

**See also:** the Spring-Pop Entrance rule (confetti fires on the hero's settle frame); the Kinetic Beat Slam rule (one beat earns the confetti payoff); the Press-Release Spring rule (single-layer glow alternative, or compose both); the CSS Marker Patterns rule (drawn-line burst when the accent should feel hand-annotated); the Scale-Swap Transition rule (glyph dissolve covers the exit).

#### Nudge Curve

Slow-fast-slow three-phase group slide — reposition a composed group (word rows, card stacks, lists) to reveal content or make room. This is an in-scene group slide, not a scene seam. No single built-in ease produces this shape — a symmetric `power4.inOut` smacks to a stop. Chain three tweens on one property instead:

| Phase | Ease | Distance | Time | Feel |
| --- | --- | --- | --- | --- |
| 1 ramp-in | `power3.in` | ~10% | ~20% | barely moves — motion registers, no jolt |
| 2 burst | `none` (linear) | ~65% | ~18% | ~2× average px/frame — purposeful |
| 3 tail | `power4.out` | ~25% | ~62% | decaying creep to rest — kills the smack |

**Rules:** the tail should be at least 3× the ramp-in in TIME — if it still smacks, extend the tail's time (not its distance), or switch to `power5.out`. Phase 2 stays linear — easing it loses the burst contrast. Reveal new content DURING phase 2 — the burst masks its appearance. The same ratios apply on the vertical axis — scale distances proportionally, keep the time ratios. A cascade arrival usually precedes this slide — see the Waterfall Entry rule above.

**JS** — reference values for a 270px leftward slide (0.57s total); scale distances proportionally for other travels while preserving the TIME ratios, keeping the tail at least 3× the ramp-in:

```js
var t = /* start after content settles */;
tl.to(".text-row", { x: -30,  duration: 0.12, ease: "power3.in"  }, t);          // ramp-in: 11% dist / 21% time
tl.to(".text-row", { x: -210, duration: 0.10, ease: "none"       }, t + 0.12);   // burst:   67% dist / 18% time
tl.to(".text-row", { x: -270, duration: 0.35, ease: "power4.out" }, t + 0.22);   // tail:    22% dist / 61% time
// vertical: same ratios on y. 150px variant: -15 / -115 / -150 at the same times.
```

**Anti-patterns:** don't use a single symmetric ease (e.g. `power4.inOut`) for a group slide — use the three-phase chain above instead. Don't let the nudge tail run shorter than 3× the ramp-in — extend the tail's TIME, not its distance.

### Effect Recipes

#### GSAP Effects (Drop-in Patterns)

Drop-in animation patterns, assuming a paused timeline already exists in scope.

**Typewriter.** Requires GSAP's TextPlugin alongside the core GSAP script:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

Basic form:

```js
const text = "Hello, world!";
const cps = 10; // chars per second — see timing table below
tl.to(
  "#typed-text",
  { text: { value: text }, duration: text.length / cps, ease: "none" },
  startTime,
);
```

Blinking cursor — three rules: one cursor visible at a time (hide the previous before showing the next); the cursor must blink when idle (after typing, during holds); no gap between text and cursor (elements flush in HTML).

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```

```css
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
.cursor-blink {
  animation: blink 0.8s step-end infinite;
}
.cursor-solid {
  animation: none;
  opacity: 1;
}
.cursor-hide {
  animation: none;
  opacity: 0;
}
```

Pattern: blink → solid (typing starts) → type → blink (typing done):

```js
tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], startTime);
tl.to("#typed-text", { text: { value: text }, duration: dur, ease: "none" }, startTime);
tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], startTime + dur);
```

Multi-line handoff: hide the previous cursor, blink the new one, a brief pause (~0.5s), then solid when typing starts — never go directly from hidden to solid, since that skips the idle blink.

Backspacing — TextPlugin removes from the front, which is wrong for backspace. Use manual substring removal instead:

```js
function backspace(tl, selector, word, startTime, cps) {
  const el = document.querySelector(selector);
  const interval = 1 / cps;
  for (let i = word.length - 1; i >= 0; i--) {
    tl.call(
      () => (el.textContent = word.slice(0, i)),
      [],
      startTime + (word.length - i) * interval,
    );
  }
  return word.length * interval;
}
```

Spacing with static text — a typewriter word next to static text (in a baseline-aligned flex row): use `margin-left` on the wrapper span. Don't use flex `gap` (it spaces the cursor from the text) and don't put a trailing space in the static text (it collapses when the dynamic span is empty).

Word rotation — type, hold, backspace, next word, with the cursor blinking during every idle moment:

```js
let offset = 0;
words.forEach((word, i) => {
  const typeDur = word.length / 10;
  // cursor: solid while typing, blink during holds (same call pattern as above)
  tl.to("#typed-text", { text: { value: word }, duration: typeDur, ease: "none" }, offset);
  offset += typeDur + 1.5; // hold
  if (i < words.length - 1) offset += backspace(tl, "#typed-text", word, offset, 20) + 0.3;
});
```

Appending words — build a sentence word by word into the same element by keeping an accumulated string, each step tweening the text value to `accumulated + " " + word` with a duration proportional to the new characters, then advancing the offset.

**Typing timing guide:**

| CPS | Feel | Good for |
| --- | --- | --- |
| 3–5 | Slow, deliberate | Dramatic reveals, suspense |
| 8–12 | Natural typing | Dialogue, narration |
| 15–20 | Fast, energetic | Tech demos, code |
| 30+ | Near-instant | Filling long blocks |

**Audio Visualizer.** Pre-extract audio data, drive Canvas/DOM rendering from the timeline. Do NOT use the Web Audio API at render time — there's no live playback during a seek.

Extract audio data ahead of time with an ffmpeg + numpy-based extractor script (accepting `--fps` and `--bands` options) that outputs a JSON shape like `{ "fps": 30, "totalFrames": 5415, "frames": [{ "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3] }] }` — `rms` (0–1) is overall loudness, `bands[]` (0–1) are frequency magnitudes with index 0 as bass, each band normalized independently.

Loading synchronously — inline the JSON for small files (under ~500KB), or a synchronous XHR request for large ones:

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false); // synchronous — deliberate
xhr.send();
const AUDIO_DATA = JSON.parse(xhr.responseText);
```

Do NOT use async `fetch()` — the timeline is read synchronously right after page load; building it inside a `.then()` callback means it isn't ready when capture starts.

Driving the timeline — Canvas 2D is the workhorse (bars, waveforms, circles, gradients) via one `tl.call()` per frame:

```js
const ctx = document.getElementById("viz").getContext("2d");
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

For WebGL/Three.js, the render engine patches `THREE.Clock` for deterministic time — update uniforms from audio data each frame the same way. DOM elements are fine under ~20 elements, slower than Canvas beyond that.

Smoothing:

```js
let prev = null;
const smoothing = 0.25; // 0.1-0.2 snappy, 0.3-0.5 flowing
function smooth(f) {
  const raw = AUDIO_DATA.frames[f];
  if (!prev) prev = { rms: raw.rms, bands: [...raw.bands] };
  else {
    prev = {
      rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
      bands: raw.bands.map((b, i) => prev.bands[i] * smoothing + b * (1 - smoothing)),
    };
  }
  return prev;
}
```

Design guide: spatial mapping — horizontally, bass left/treble right; vertically, bass at the bottom; circularly, bass at 12 o'clock wrapping clockwise (mirror for a full circle). Bass drives big moves (scale, glow, position); treble drives detail (shimmer, flicker, edges); RMS drives globals (background brightness, overall energy). Pick 2–3 animated properties — more looks noisy. Keep minimums above zero so quiet sections still have life. Band count: 4 for a background glow/pulse, 8 for bar charts, 16 for a detailed EQ (default), 32 for dense radial layouts. Layering — stack canvases with z-index, a background layer driven by bass/rms under a foreground layer driven by individual bands gives depth without per-element complexity.

#### CSS Marker Patterns

Pure CSS plus GSAP implementations of five hand-drawn marker/highlight drawing modes — no external library dependency, full timeline control. Shared scaffold for every mode: the wrap is `position: relative; display: inline`; the text copy is `position: relative` and z-indexed above the accent (below it for the sketchout mode, where the lines cross the text).

**1. Highlight mode** — a yellow marker sweep behind text, the most common mode.

```html
<span class="mh-highlight-wrap">
  <span class="mh-highlight-bar" id="hl-1"></span>
  <span class="mh-highlight-text">highlighted text</span>
</span>
```

```css
.mh-highlight-bar {
  position: absolute;
  inset: 0 -6px; /* bleed past the text edges */
  background: #fdd835;
  opacity: 0.35;
  transform: scaleX(0);
  transform-origin: left center;
  border-radius: 3px;
  z-index: 0;
}
```

```js
tl.to("#hl-1", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.6);
// Optional hand-drawn skew: gsap.set("#hl-1", { skewX: -2 });
// Multi-line: tl.to(".mh-highlight-bar", { scaleX: 1, ..., stagger: 0.3 }, 0.6);
```

**2. Circle mode** — a hand-drawn ellipse around text, `border-radius: 50%` plus a slight rotation for an organic feel.

```html
<span class="mh-circle-wrap">
  <span class="mh-circle-text">IMPORTANT</span>
  <span class="mh-circle-ring" id="circle-1"></span>
</span>
```

```css
.mh-circle-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 130%; /* tight (short words): 150%; rounded-rect: 120% + border-radius: 30% */
  height: 160%;
  transform: translate(-50%, -50%) rotate(-3deg) scale(0);
  border: 3px solid #e53935;
  border-radius: 50%;
  z-index: 0;
}
```

```js
tl.to("#circle-1", { scale: 1, rotation: -3, duration: 0.6, ease: "back.out(1.7)" }, 0.7);
```

**3. Burst mode** — radiating lines from the text's center, each line a positioned span rotated to its angle. Use roughly 12 lines at 30° steps and vary the line length (40–80px); equal lengths look mechanical.

```html
<span class="mh-burst-wrap">
  <span class="mh-burst-text">WOW</span>
  <span class="mh-burst-container" id="burst-1">
    <span class="mh-burst-line" style="--angle: 0deg; --len: 70px;"></span>
    <span class="mh-burst-line" style="--angle: 30deg; --len: 55px;"></span>
    <!-- …one line per 30° step through 330deg, --len varied 40-80px -->
  </span>
</span>
```

```css
.mh-burst-container {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  z-index: 1; /* text copy at z-index: 2 */
}
.mh-burst-line {
  position: absolute;
  display: block;
  width: 3px;
  height: var(--len);
  background: #1e88e5;
  left: -1.5px;
  top: calc(-1 * var(--len));
  transform: rotate(var(--angle));
  transform-origin: bottom center;
  opacity: 0;
}
```

```js
tl.fromTo(
  "#burst-1 .mh-burst-line",
  { scaleY: 0, opacity: 0 },
  { scaleY: 1, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.03 },
  0.7,
);
```

**4. Scribble mode** — a wavy SVG underline that draws itself via `stroke-dashoffset`.

```html
<span class="mh-scribble-wrap">
  <span class="mh-scribble-text">underlined text</span>
  <svg class="mh-scribble-svg" viewBox="0 0 500 24" preserveAspectRatio="none">
    <path
      id="scribble-1"
      d="M0,12 Q31,0 62,12 Q93,24 125,12 Q156,0 187,12 Q218,24 250,12 Q281,0 312,12 Q343,24 375,12 Q406,0 437,12 Q468,24 500,12"
      fill="none"
      stroke="#FDD835"
      stroke-width="3"
      stroke-linecap="round"
    />
  </svg>
</span>
```

```css
.mh-scribble-svg {
  position: absolute;
  left: 0;
  bottom: -6px; /* strikethrough variant: top: 50%; transform: translateY(-50%) */
  width: 100%;
  height: 24px;
  z-index: 0;
}
```

```js
const path = document.querySelector("#scribble-1");
const len = path.getTotalLength();
gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });
tl.to("#scribble-1", { strokeDashoffset: 0, duration: 0.8, ease: "power1.inOut" }, 0.7);
```

Path tuning: the `Q` control points alternate y between 0 and 24 for a natural wobble. Tighter waves use smaller x-increments (~25px per half-wave); looser waves use ~50px; a subtler amplitude keeps the y range around 0–16.

**5. Sketchout mode** — a cross-hatch over de-emphasized text, two angled lines creating a "crossed out" effect.

```html
<span class="mh-sketchout-wrap">
  <span class="mh-sketchout-text">old price</span>
  <span class="mh-sketchout-lines" id="sketchout-1">
    <span class="mh-sketchout-line mh-sketchout-fwd"></span>
    <span class="mh-sketchout-line mh-sketchout-bwd"></span>
  </span>
</span>
```

```css
.mh-sketchout-lines {
  position: absolute;
  inset: 0 -4px;
  overflow: hidden;
  z-index: 1; /* text at z-index: 0 — the lines cross OVER it */
}
.mh-sketchout-line {
  position: absolute;
  display: block;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: #e53935;
  transform-origin: left center;
}
.mh-sketchout-fwd {
  transform: scaleX(0) rotate(-12deg);
}
.mh-sketchout-bwd {
  transform: scaleX(0) rotate(12deg);
}
```

```js
// Forward slash first, backward follows
tl.to("#sketchout-1 .mh-sketchout-fwd", { scaleX: 1, duration: 0.3, ease: "power2.out" }, 1.0);
tl.to("#sketchout-1 .mh-sketchout-bwd", { scaleX: 1, duration: 0.3, ease: "power2.out" }, 1.15);
```

**Combining modes in captions:** cycle modes across caption groups for visual variety — every 2–3 groups for high energy, 3–4 for medium, 4–5 for low:

```js
const MODES = ["highlight", "circle", "burst", "scribble"];
GROUPS.forEach((group, gi) => {
  const mode = MODES[gi % MODES.length];
  group.emphasisWords.forEach((word) => applyMode(word.el, mode, tl, word.start));
});
```

## Composed Blueprints

A blueprint is a product-agnostic, time-coded shot template — a full scene structure with named slots and one signature move — reverse-engineered from a large corpus of studied golden video-ad clips. It encodes a whole shot across its full duration, with reveals paced to the spoken line rather than dumped at t=0, so instantiating one keeps content arriving instead of freezing. Each blueprint below documents: the roles it serves (the marketing "beat" a shot plays — Hook, Problem, Product Intro, Key Feature, Benefits, Social Proof, CTA, Brand Outro), a duration range, a scene-by-scene shot structure with bracketed `[slots]` to fill in with your own content, a motion vocabulary (plain-English list of every distinct movement in the shot), a rule mapping (which Animation Rule above implements each motion verb), and a camera modifier (what the virtual camera does, if anything).

**Picking a blueprint:** find the beat's role in the "roles served" list below (or in the summary table implied by each blueprint's roles); pick the blueprint whose shape fits the beat. If two fit, prefer the one whose motions are closer to what you already have planned. Open the blueprint's full recipe, read its time-coded template and slots, and choose a posture — reproduce (slots map cleanly onto your content), adapt (the structure fits but content or surface differs — keep the signature move), or compose (nothing fits — build a new shot from the atomic Animation Rules above instead). If nothing in this menu fits the beat, don't force a wrong blueprint — compose freely from the Animation Rules, still pacing the reveals to any voiceover across the whole shot.

Every recurring move in the golden-clip vocabulary is backed by a rule in the Animation Rules section above. A blueprint's "rule mapping" cites the real rule by name so you can jump straight to its full recipe.

#### Agent Progress Theater

**Intent:** agent work performed as WORKING-STATE theater — a short trigger beat hands the frame to the machine, which then visibly works: loaders spin, status phrases swap, dots pulse, counters tick — before the receipt arrives as a card whose rows cascade in and CHANGE STATE (badges flip to checks, labels strike through, severity pills read out), or as a conversation thread building message by message onto a camera push-in payoff. The subject is the machine performing labor over time. It is NOT a typed prompt awaiting output (no prompt is ever typed — the trigger is a click, a menu choice, or an already-running scan); it is NOT the Cursor-UI-Demo blueprint below (at most one igniting click here, then the cursor exits and the UI performs itself); it is NOT the Grid Card Assemble blueprint below (rows there assemble into a static enumeration and hold — rows here are alive, arriving as agent output and then mutating, checking off one by one while the viewer watches).

**Roles served:** Key Feature — when the feature is the agent doing multi-step work (build a plan, scan a repo, fix a vulnerability, handle infrastructure) and the proof is status theater: a loader lockup with a typed label, status couplets swapping under an accent spinner, then a checklist/findings card that populates and checks off in front of the viewer. Also Key Feature — when the agent's work lives inside a conversation or automation thread: user/agent bubbles and tool-call/reply cards popping in sequence, the working state carried by pulsing loading dots or rapidly ticking diff counters, resolved by ONE camera push-in tight on the confirmation line.

**Duration:** 4.2–11.6s (short members are a single card-and-check-off or thread beat at ~4–5s; long members chain trigger → interstitial → status swaps → receipt card at ~9–12s; thread payoff spans 4.2–9.1s).

**Shot structure:** a warm flat canvas (off-white/warm beige/near-white background, optional faint grid or dot-grid texture), white rounded cards with soft drop shadows, ONE working-accent color reserved for the machine (spinner, status words, active step) and one done-color for completion (checks, "Completed"). The camera is static or makes one slow move — motion is overwhelmingly element-level springs, staggers, and state flips. Two folded sub-shapes: (A) checklist/findings theater and (B) message-thread payoff.

- **Scene 1 (0.0–~1.5s) — the trigger.** Something asks the machine to work, in ONE beat. Pick a variant: an option menu (a centered white pill card poses the question, springs open downward into a rounded menu with 3–4 staggered option rows, a cursor hover-dances between rows and clicks the chosen one, the menu scales down and fades); a modal click (a close-up modal with a dismiss/action button, a hand cursor clicks it with a quick press-down spring, the modal fades away, optionally followed by a serif interstitial line landing staggered then clearing); an already-working state (a "Scan in progress" heading with a thin accent arc spinner and a motionless cursor resting on a "Starting…" pill, then the whole scene rapidly scales up and fades as a push-through exit); a workspace push-through (a rapid camera push-in through a multi-panel workspace that scales past the viewport edges, clearing to bare canvas); or a thread opener (a user bubble spring-pops in, or a stats card pops in with rapidly ticking diff counters as the automation's opening receipt).

- **Scene 2 (~1–4s) — the working state.** The frame belongs to the machine; nothing is clickable. Pick 1–3 working motifs and chain them: a loader lockup (a spinning accent asterisk/arc beside a working label typed on rapidly, a shimmer sweep passing through the letters, the spinner occasionally morphing asterisk↔dot); status couplets (2–3 centered pairs — a dark action line over an accent status word with its own spinner, swapping via quick fades/slides at a steady cadence); a scan/tool label that types/expands rightward then shrinks and docks as a fixed corner header; a status heading that flips tense as rows land beneath it ("Using [Tool]" → "Used [Tool]"), with a gently pulsing "Thinking" and gray meta-lines fading in below. For the thread variant, an agent reply fades/slides up, then a monospace tool-call line appears beneath it with three pulsing loading dots that vanish the instant the result lands.

- **Scene 3 (~2–4s) — the receipt cascades in.** The work materializes as a card that builds. Checklist variant: a white progress/summary pill or card spring-pops in with a bounce, then springs open downward (or glides up as a taller findings panel expands beneath it); rows cascade in one by one, staggered, each with a number badge or severity pill, a label, and an optional gray meta line; then the state mutation runs — badges flip one by one from numbered outline to a solid done-color circle with a white checkmark (a slight scale bounce), the checked label simultaneously strikes through and dims, while pending items keep partially-drawn arc outlines animating; end the run mid-list, some checked, some still numbered, since the work is visibly ongoing. Thread-payload variant: the camera pushes in / pans down centering the tool-call line as a white payload card expands downward from it with 2–4 light monospace key/value lines fading in, then a resolution message expands into place below, OR a dark thread card scales up from a status row to dominate the frame while the background darkens, its reply expanding into place under a "1 reply" divider.

- **Scene 4 (final ~1–2.5s) — resolve.** Hold/scroll variant: the finished (or mid-mutation) card stack holds static to the end, or the viewport scrolls down the final card revealing a second heading plus a numbered list, ending mid-list, optionally under a slow continuous zoom into the card (the header drifting off the top). Payoff push-in variant (sub-shape B's defining move): static through the build, then ONE camera push-in plus pan-down tightening onto the confirmation line — "Sent using [@Bot]" plus a thank-you bubble springing in — then a reaction button springs into an active pill with bouncy overshoot and a count; the push eases into a gentle near-imperceptible drift, and the clip ends on the close-up with no end card.

**Motion vocabulary:** pill springs open downward into a menu; option rows fade/slide in staggered; cursor hover-dance with a pale highlight following it between rows; a single igniting click with a press-down spring; menu scale-down fade exit; modal fade-away; a thin accent arc spinner rotation; a spinning asterisk loader; asterisk↔dot morph; a typed-on loader label with caret; left-to-right text shimmer sweep; a serif interstitial with word-staggered fade in/out; status couplets swapping via quick fades/slides under an accent spinner; a pulsing "Thinking" label; a status heading tense flip; a label that types/expands rightward then shrinks and docks as a corner header; a scene scale-up/fade push-through exit; a rapid camera push-in through a multi-panel workspace; a slow continuous zoom into a card with the header drifting off frame; a summary card spring pop with bounce; a card gliding up as a panel expands beneath it; anchored downward panel/payload expansion; rows staggering in via slide-up and fade; a badge flip from numbered outline to solid circle with a white checkmark and scale bounce; strikethrough plus dim on completion; partially-drawn arc outlines animating on pending items; severity-pill readouts; a viewport scroll down the final card; a chat-bubble spring scale-up pop-in; a reply fade/slide-up; a monospace tool-call line with three pulsing loading dots that die the instant the result lands; a payload card expanding downward from the line; green/red diff counters ticking and settling rapidly; internal window scroll under a static frame; a brand logo pop-in beside a status row; a card scaling up from a row to dominate the frame while the background darkens; a reply message expanding into place; inline code chips/link coloring; a reaction button springing into an active pill with bouncy overshoot and a count; a camera push-in plus pan-down centering the payoff; a slight pull-back plus gentle end drift; a static hold.

**Rule mapping:** the pill/menu/panel/payload-card growth uses the Anchored Layout Expand rule (an edge-anchored, height-masked wrapper with an inner counter-translate, container drawn at final size), with the spring flavor from the Spring-Pop Entrance rule. Option/findings/task rows staggering in use the Spring-Pop Entrance rule (staggered-group form, capped stagger) or a plain fade+translate stagger via the GSAP Effects recipe rule — not the Waterfall Entry rule, since its binary no-fade arrival law would contradict this dialect's soft fade/slide cascade. Cursor movement plus clicks use the Cursor-Click Ripple rule plus the Press-Release Spring rule for the button's press-down spring; a pale hover-highlight fill following the cursor is a plain background-fill tween, no dedicated rule needed. Scale-down fade exits and push-through exits use the Scale-Swap Transition rule. Spinner rotation and asterisk-to-dot morphing use the SVG Icon Enrichment rule (rotating SVG parts) and the Scale-Swap Transition rule respectively. Typed-on labels use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule for the caret. The shimmer sweep through loader letters uses the Ambient Glow Bloom rule's single-pass sheen or the CSS Marker Patterns rule's highlight sweep. Serif interstitials, status couplets, and status-heading tense flips use the Dynamic Content Sequencing rule plus the Discrete Text Sequence rule. Pulsing labels and loading dots use the Sine Wave Loop rule (finite repeats, explicitly killed at the resolve beat — see the doctrine note below). The rapid camera push-in through the workspace uses the Viewport Change and Multi-Phase Camera rules, optionally with the Motion-Blur Streak rule as panels clear the frame. The slow continuous zoom into the receipt card uses the Multi-Phase Camera rule's steady-push pattern. Spring pop-ins (summary card, chat bubble, brand logo) use the Spring-Pop Entrance rule. The badge flip (numbered outline → solid checkmark circle with bounce) combines the Scale-Swap Transition rule, the SVG Path Draw rule for the checkmark, and the Spring-Pop Entrance rule for the bounce, with the Dynamic Content Sequencing rule driving the pending→active→complete state progression. Strikethrough plus dim on the checked label uses the CSS Marker Patterns rule's strike-through draw plus a plain opacity dim. Partially-drawn arc outlines on pending items use the SVG Path Draw rule (partial dashoffset, held mid-draw). Viewport scroll / internal window scroll uses a plain transform-only content translate inside a masked window (Viewport Change only if the whole FRAME moves). Diff counters ticking use the Counting with Dynamic Scale rule (with the scale-growth component suppressed, since these tick at fixed size). The dark thread card scaling up to dominate the frame uses the Card Morph Anchor rule with a plain overlay fade for the background darkening. Reply/resolution message expansion uses the Spring-Pop Entrance rule or the Anchored Layout Expand rule for a true downward growth. The reaction button pop uses the Spring-Pop Entrance rule plus the Press-Release Spring rule's activation flavor plus the Counting with Dynamic Scale rule if the count ticks. The push-in plus pan-down onto the payoff uses the Coordinate Target Zoom rule (for an off-center target) or the Viewport Change rule, with a slight pull-back plus gentle end drift from the Multi-Phase Camera rule's micro-drift.

**Camera modifier:** the default is a STATIC frame — the theater is element-level; at most ONE real camera move per shot. Choose one of: a trigger push-through (a rapid push-in through the opening workspace that clears to bare canvas, via Viewport Change plus Multi-Phase Camera, optionally with Motion-Blur Streak); a receipt zoom (one slow continuous zoom into the checklist card across the whole mutation run, header drifting off the top, via Multi-Phase Camera's steady push); or a payoff push-in (sub-shape B's defining move — static through the build, then one push-in plus pan-down tightening onto the confirmation line, easing to a micro-drift end). Everything else — swaps, cascades, check-offs, scrolls — happens on a locked frame; any "scroll" is content translating inside its own window, not the camera.

**Doctrine note (idle-motion discipline):** the working-state motifs (spinner rotation, pulsing dots, pulsing "Thinking") brush against the general idle-motion caution elsewhere in this document — here they are DIEGETIC: the pulse performs "the machine is working" and is the narrative content of Scene 2, not decorative breathing. Keep every loop finite, timeline-driven, and seek-safe (finite repeats on the Sine Wave Loop rule, timeline-driven rotation on the SVG Icon Enrichment rule), and kill it at the exact frame the state resolves — the loading dots should vanish the instant the payload card expands; the spinner should swap out with the loader lockup.

#### Camera Journey

**Intent:** the real viewport camera is the STORYTELLER — a multi-leg journey (dive in → a mid-journey beat fires → travel to the consequence/reposition → landing push, at rest) across ONE continuous world, where the travel itself carries the narrative. Two folded sub-shapes: (A) action roundtrip — the camera dives into a UI panel, a cursor/typed action fires, and the camera swoops/pans to another region where the consequence renders as element motion; (B) cursorless flight — pure cinematic 3D flight (motion blur, depth of field, tilt-to-flatten rotations) over static or self-animating content, with no cursor anywhere.

**Boundary:** this is NOT the Cursor-UI-Demo blueprint below — there the camera CHASES the cursor (a servo following the actor); here the camera IS the actor, moving on its own narrative motivation, and in sub-shape A the cursor acts only at the leg hinge (in B it never appears). It is NOT the Device-Surface-Showcase blueprint below — there one device/surface is hero and the camera merely presents it; here no single surface is hero, the journey traverses multiple regions/panels/depth planes and the traversal IS the story. It is NOT the Spatial-Pan-Stations blueprint below — there pre-placed stations on a flat canvas are visited by repeated pans of the same type; here the legs are heterogeneous (push-in, swoop, pull-back-rotate, whip, dive) and each leg is motivated by a fired action or by the reveal it lands on.

**Roles served:** Benefits — when the benefit IS a cause-and-effect round trip ("do this small thing here, get this big thing there" — a comment triggers a chart morph, an agent finding produces a verified commit, a chat message produces a receipt and ledger entry); the camera physically connects the action to its payoff so the viewer travels the value chain instead of being told it. Also Key Feature — when the feature should feel cinematic and inevitable, a form or a generated content plan explored by a flying camera (dives, whip sweeps, tilt-to-flatten, a violent final push onto the CTA/hero card), the content acting by itself (a dropdown self-selects, keyword cards simply exist in depth) with no hand on the wheel.

**Duration:** 5.6–11.1s (sub-shape A 5.6–9.0s; sub-shape B 6.3–11.1s).

**Shot structure:** one oversized world — a UI canvas (a design tool, a code-review-plus-agent-panel layout, a phone-and-desktop pairing) for sub-shape A, or a 3D-laid-out space (a floating form card, a calendar grid with standing keyword cards) for sub-shape B — wrapped by a single virtual camera; content animates as elements INSIDE the world while the camera travels; every leg is a sequential tween on the same camera state.

- **Scene 0 (optional, 0.0–~1.8s) — static prologue.** Camera locked on a prologue beat: a static promo card with a floating 3D product card, a typed headline with an accent word, or a wide establishing shot of the app. A typewriter line may finish. The prologue breaks by a hard cut or by the headline shrinking and slipping away as the first dive begins.
- **Scene 1 (~0.5–2.0s) — leg 1: dive in.** The camera pushes in fast and tight onto the focal element. Sub-shape A: a flat whole-viewport push onto an actionable element (a comment box, an agent panel, a chat bubble) where typed text finishes typing or response text streams in — the header/context leaves the frame, since this is commitment, not a polite zoom. Sub-shape B: the push lands at an ANGLE — a tilted 3D close-up of a form region or a calendar grid, foreground elements motion-blurred during the travel, neighbors soft under depth of field.
- **Scene 2 (~1.5–6.0s) — leg 2: the mid-journey beat (the hinge).** The camera holds, drifts, or pulls slowly while the content ACTS. Sub-shape A — the action fires: a cursor clicks Send/Create-PR (or a message sends implicitly) and the acted element clears/vanishes, optionally preceded by theater (a status spinner cycles status words, to-do items strike through, response text streams). Sub-shape B — the content self-acts: a dropdown expands by itself (pushing the field below down), shows a row hover highlight with no cursor, and collapses with the new value selected; or the flight decelerates into focus on one card, its metrics sharp, neighboring cards blurred.
- **Scene 3 (~4.0–8.0s) — leg 3: travel to the consequence/reposition.** Sub-shape A: the camera pulls back/swoops/pans to another region while the consequence builds as element motion — bars shrink into the baseline while a node-dotted line draws left-to-right, or a verified commit row slides into a timeline with a reaction pill popping, or a receipt card expands row by row from a skeleton. An optional second leg extends the trip. Sub-shape B: a repositioning move — a slow pull-back that ROTATES the world flat and centered (3D to straight-on 2D), or a heavily motion-blurred WHIP SWEEP that resolves into a flat lateral pan across a calendar/card; quiet element beats may play on the flat hold (a thin focus outline fading in around one field and sweeping to the next), and the card keeps a near-imperceptible tilt/scale drift so the hold never feels dead.
- **Scene 4 (final ~1–2s) — leg 4: landing.** Sub-shape A: the camera comes to rest, a cursor hovers or drifts toward the payoff (an open Export menu item, a commit link, a View-transaction button), ending still on the changed state. Sub-shape B: a sudden violent push-in/dive (motion-blurred) onto the CTA button scaled huge in frame, or the hero keyword card — ending held tight, or holding MID-DIVE (the last frames still traveling, the flat overview explicitly not the final image).

**Motion vocabulary:** whole-viewport camera push-in (fast/tight and slow/subtle); camera pull-back reframe; camera pan up/right/down; dive/swoop between stacked panels; fast decelerating zoom-out to rest; sudden violent push-in onto a button scaled huge; continuous 3D flight through a card grid; dive into an angled 3D close-up; slow pull-back that rotates/flattens the world to straight-on; heavily motion-blurred whip sweep; motion blur on camera travel; depth of field with blurred neighbors; decelerate-into-focus; hard cut/match cut into extreme close-up; near-imperceptible tilt/scale drift on holds; typed text finishing in an input; typewriter headline; headline shrinks and slips away as the camera dives; streaming AI response text; status-word spinner cycling labels; to-do strikethrough draw; cursor click; clicked element clears/vanishes; dropdown cascades open/self-expands and collapses with a row hover highlight; bar-to-line chart morph; commit row slide-in on a timeline; reaction pill appears; skeleton-to-content card build; receipt/label rows expand row by row; thin focus outline fading in and sweeping between fields; camera drift toward a button; 3D card subtle float; cursor hover at rest.

**Rule mapping:** the multi-leg camera itself uses the Multi-Phase Camera rule for phase sequencing and drift, layered over the Viewport Change rule's base virtual-camera primitive. Diving tight onto an off-center element uses the Coordinate Target Zoom rule. Fast decelerating zoom-outs use the Coordinate Target Zoom rule's zoom-out variation or the Multi-Phase Camera rule's pull phase. Motion blur on camera travel (dive, whip sweep, violent final push) uses the Motion-Blur Streak rule's camera-travel carve-out. Depth of field on neighbors while one card is in focus uses the Depth-of-Field Blur rule, run at the same position as the camera leg. The 3D flight itself (sub-shape B's core) uses the 3D Camera Flight rule. A whip sweep composes the Nudge Curve rule (burst-dominant tuning) with the Motion-Blur Streak rule's camera-travel carve-out on the same window. Typed text, streaming responses, and skeleton-to-content state swaps use the Discrete Text Sequence rule plus the GSAP Effects typewriter recipe and the Context-Sensitive Cursor rule for any caret. Which content appears per leg uses the Dynamic Content Sequencing rule. The cursor click on Send/Create-PR uses the Cursor-Click Ripple rule plus the Press-Release Spring rule (or the Physics Press Reaction rule for a weightier press). To-do strikethrough uses the CSS Marker Patterns rule; row hover highlight uses the ASR Keyword Glow rule's accent glow. The bar-to-line chart morph composes the Stat Bars & Fills rule (bars scaling to the baseline) with the SVG Path Draw rule (the line drawing in) at the same timeline position. Commit-row slide-ins, reaction pills, and receipt rows use the Spring-Pop Entrance rule for single arrivals or the Waterfall Entry rule for a row-by-row cascade. A self-expanding dropdown uses the Anchored Layout Expand rule plus the Reactive Displacement rule for the sibling's displacement. A focus-ring traveling between fields uses a plain-outline restyle of the AI Tracking Box rule. 3D card float and near-imperceptible drift use the Sine Wave Loop rule plus the Multi-Phase Camera rule's drift component (the tilt component belongs to the 3D Camera Flight rule).

**Camera grammar:** this blueprint IS its camera — every leg is a tween on ONE camera state (the Viewport Change rule's single world wrapper), sequenced by the Multi-Phase Camera rule, aimed by the Coordinate Target Zoom rule. Legs must be motivated: sub-shape A moves because an action fired, sub-shape B moves because the next reveal demands it. Vary the leg verbs — a journey of four identical pushes reads as a slideshow. Ease law: hard `out`-family on dives and landings (violent arrival, sharp settle), `power2.inOut` on repositioning legs; spring/back easing on a camera feels wrong. Sub-shape B layers the 3D Camera Flight rule's perspective wrapper under the same single-state discipline.

**Seek-safety:** the entire journey — every leg, every blur envelope, every depth-of-field pull — lives on the ONE paused timeline, so any frame seek reproduces the exact mid-leg camera pose. One camera state object, transform composed in a single writer function, no CSS `transition` anywhere near the wrapper, blur via proxy-tweened attributes/CSS-variable channels (both seek-safe), and ending mid-dive is fine — a seek to the last frame just lands mid-tween. Per-leg targets should be measured once at setup (after fonts load) and baked; never measured live inside `onUpdate`.

**Overflow:** a traveling camera deliberately moves world content past the frame edges on every leg. Keep `overflow: hidden` on the scene root AND mark the moving world wrapper with a layout-overflow-allowed marker — otherwise an automated layout check would flag every panel the journey leaves behind as an overflow bug rather than recognizing it as intentional.

#### Comparison Split-Cards

**Intent:** two paired items of equal weight shown side by side with mirrored 3D "book-open" tilts — the eye reads them as a balanced comparison, then a pill badge lands at each card's inner edge to punctuate. The motion IS the symmetry: two cards arriving from opposite wings into a held spread.

**Roles served:** Key Feature — when two complementary features/capabilities of equal weight should be presented simultaneously, not sequentially (an A/B, an "X + Y together," paired concepts the viewer must weigh side by side). Not for more than 2 items (use the Grid Card Assemble blueprint below) or sequential steps.

**Duration:** 4–6s.

**Shot structure:** a background canvas carrying two faint ambient glow blooms — one accent near the 30% mark, another near the 70% mark — so each side owns a color identity across a 50% symmetry axis; equal-width cards under one shared perspective parent.

- **Scene 1 (0.0–~0.8s) — title sets the concept.** A centered title line with an accent keyword slides DOWN into place from just above, a short smooth settle. The downward arrival is deliberate — it forms a non-conflicting T-shape against the cards, which arrive from the sides next.
- **Scene 2 (~0.4–1.9s) — the split-tilt entry (signature move).** Two equal-width feature cards arrive from opposite wings — the left card from the left, the right card from the right ~0.2s behind — each carrying a mirrored 3D `rotateY` tilt (left faces right, right faces left, opening like a book) and scaling from ~0.85 to 1 as it lands. The entry overlaps the title's tail so the whole thing reads as ONE arrival. Each card holds an image/label/subtitle; box-shadows fall outward from the tilt (left shadow right, right shadow left).
- **Scene 3 (~1.9s–end) — badges punctuate, then hold.** A pill badge lands at each card's inner edge (left then right, ~0.3s apart), overlapping its card by roughly 15% so it reads as attached, not orbiting. This is the lone overshoot in the shot — it earns the punctuation. Settles and holds.

**Motion vocabulary:** title slide-down from above; mirrored opposite-wing card entry; static book-open `rotateY` tilt; tilt-matched outward box-shadow; inner-edge badge spring-pop; gentle phase-opposed idle float (left vs. right, never synchronized) registered as subtle jitter; dual side-glow ambient.

**Rule mapping:** the two cards entering from opposite wings with mirrored tilts and tilt-matched shadow use the Split Tilt Cards rule (keeping the two-layer split so entry x/scale and idle never collide on one alias). The title slide-down settle is a plain translate-plus-opacity tween on a long-tail `power3` ease. The inner-edge pill badge pop (the one overshoot) uses the Spring-Pop Entrance rule's overshoot register, since it earns the punctuation. Phase-opposed idle float on the pair uses the Sine Wave Loop rule at a low-amplitude register — subtle jitter, not lazy breathing; left `sin(t)`, right `sin(t+π)` so they never conveyor-belt. The two faint side glows behind the cards use the Ambient Glow Bloom rule, one per accent.

**Camera modifier:** static by default — the symmetry is the subject and a camera move would break the balance.

#### Constellation / Hub + Satellites

**Intent:** labeled/iconned nodes spring into a ring/cluster around a center, then the shot resolves on the core — either by pushing the camera INTO the center (depth of field collapsing onto it) or by holding a hub mark while the satellites ORBIT it. The "everything connects to / sits around one center" beat.

**Roles served:** Hook — a constellation of tool/app nodes springs into a wide ring, then a sustained camera push-in with depth of field resolves on the inner core ("it connects everything / one hub for all your tools"). Social Proof — the product brand mark lands as the center hub and partner logos spring onto a ring and revolve around it ("plugs into / sits at the center of your stack"). CTA — the ring resolves by COLLAPSE rather than a push-in: category icons drift around an empty central CTA, a cursor click implodes the orbit toward the click point, and the product demo springs OUT of that collapse as the answer (scope → choice → consequence → product). Social Proof — a persistent center logo accrues proofs: its wordmark decodes, a claim ticker swaps, the logo glides to center, then avatars cascade into orbit with drawn connectors while partner logos scroll the bottom strip, four claims reading as one statement. Social Proof — the ecosystem beat as a static end card: a two-line serif headline is the center (no hub mark, no ring), ~20 app icons pop in scattered frame-wide in a quick stagger, then keep drifting very slowly outward to the end — "connects to thousands of apps" said with count and spread, not geometry.

**Duration:** 5–8s (the CTA orbit-collapse variant ~6s; the scatter-drift end card ~2.5s as a closing beat).

**Shot structure:** nodes ring a center, then one of two finishers resolves on the core.

- **Scene 1 (0.0–~1.5s):** a dark/space-field background (optionally with slow-drifting diffused gradient blobs). Primary nodes (circles carrying an icon plus a label) SPRING-POP in (scale 0→1, ~1.15 elastic overshoot, staggered) arranged in a wide ring/cluster around an empty or marked center hub.
- **Scene 2 (~0.7–2.5s, overlapping):** smaller secondary nodes (platform/partner-logo chips) pop in staggered with the same elastic spring, filling the gaps; optional thin connector lines / an orbit ring draw from hub to nodes. Camera holds.
- **Scene 3 (~2.5s–end, the resolve):** see the finisher variant below; it lands and holds on the magnified/orbited center to the end.

**Variants:** the Hook push-in finisher runs a continuous smooth camera push-in toward the center inner cluster — inner nodes scale up and stay sharp while outer nodes push toward the edges and progressively blur (depth of field), background scaling up smoothly, holding magnified on the core. The Social-Proof orbit finisher snaps the center brand mark in via a quick 3D rotate that decelerates and settles; a thin orbit ring draws around it; N partner badges spring onto the ring (staggered overshoot) and revolve CLOCKWISE while staying upright, under a continuous slow camera ZOOM-OUT (ecosystem reveal). An optional Social-Proof type-push-through opener (prepended before Scene 1) has a centered headline type/slide in with a huge transparent-fill outline copy of the same words behind it; the outline text scales up exponentially toward camera (a high-speed dolly/push-through), breaches the frame, then HARD-CUTS to the hub background of Scene 1. The Social-Proof scatter-drift finisher (no ring) has the center be a two-line serif headline building in place, ~20 app icons popping in SCATTERED across the whole frame in a quick stagger with no ring geometry and no connectors, then a very slow outward drift to the end; the camera is fully static, and the "everything around one center" read comes from the drift vectors pointing away from the headline — often chained as the end card of a preceding UI beat.

**Motion vocabulary:** staggered elastic spring-pop node entrances (~1.15 overshoot); slow gradient-blob drift; connector-line/orbit-ring draw-on; 3D snap-rotate-settle on the hub mark; continuous camera push-in (inner sharp, outer depth-of-field blur, background scale-up); clockwise orbital revolve of upright badges; continuous slow camera zoom-out (ecosystem reveal); optional outline-text push-through dolly entry. Scatter-drift finisher: frame-wide scattered icon pop-in (staggered, no ring); sustained slow outward icon drift; in-place two-line serif headline build; static-frame hold to the end.

**Rule mapping:** staggered spring-pop node entrances use the Spring-Pop Entrance rule's elastic overshoot plus a plain stagger recipe; a 3D-flip-in flavor uses the Orbit 3D Entry rule. The ring/cluster layout of nodes around a center uses the Avatar Cloud Network rule (nodes on an elliptical ring plus SVG lines to a center). Icons on the nodes use the SVG Icon Enrichment rule. Connector lines and the orbit-ring draw-on use the SVG Path Draw rule. Slow gradient-blob drift uses the Sine Wave Loop rule's idle looped drift. The 3D snap-rotate-settle on the hub mark uses the Orbit 3D Entry rule's 3D-flip entry. The clockwise orbital revolve of upright badges uses the Orbit 3D Entry rule's continuous elliptical orbit. The camera push-in toward center uses the Multi-Phase Camera rule's push-in phase plus the Coordinate Target Zoom rule. Background scale-up during the push-in and the continuous slow zoom-out both use the Multi-Phase Camera rule. The outline-text push-through dolly opener composes the 3D Text Depth Layers rule (outline copy behind) with the Multi-Phase Camera rule's push-through. Depth-of-field blur on outer nodes during the push-in uses the Depth-of-Field Blur rule. Frame-wide scattered icon pop-in (no ring) uses the Spring-Pop Entrance rule's staggered group plus a plain stagger recipe, with positions pre-baked scattered rather than the elliptical-ring layout of the Avatar Cloud Network rule. Sustained slow outward icon drift uses the Center-Outward Expansion rule (outward vectors, slow sustained register, drift targets sitting slightly past the pop-in positions). The in-place serif headline build uses a plain staggered line/word reveal.

**Camera modifier:** the push-in-with-depth-of-field (Hook) uses the Multi-Phase Camera rule's push-in phase targeted via the Coordinate Target Zoom rule onto the core, with the focus-falloff blur backed by the Depth-of-Field Blur rule. The orbit finisher (Social Proof) uses a slow continuous zoom-out via the Multi-Phase Camera rule's pull-back phase while satellites revolve. The scatter-drift finisher (Social Proof end card) uses no camera move at all — the frame never moves, and the outward drift is entirely element-level.

#### CTA Morph & Press

**Intent:** a resting brand mark condenses at the same screen center into a smaller, brighter CTA, then a cursor arrives from off-stage and lands a human-aimed click on it. The viewer's eye is walked from "this is who we are" to "and this is what you do." The morph and the click are the two headline beats.

**Roles served:** CTA — when the close moves from brand identity to a single user action, two elements share the same center sequentially (a morph, not a cut), and the payoff is a simulated click with physical feedback; reach for it for a focused "click here" sign-off with no spatial set, no multi-step UI. Hook (role-widened) — the same machinery run as an OPENER: a lone widget (a pill/chip lockup) on a flat field transforms in place, performs its payload, then vanishes to a plain frame that a typed title resolves. The click, when present, ignites the morph rather than closing it; there may be no cursor at all. Reach for it when the product hook IS one widget doing one thing.

**Duration:** 4–6s (the Hook widget-morph opener runs 5–7.5s).

**Shot structure:** a background canvas; hero and CTA are flex-centered siblings sharing one transform origin.

- **Scene 1 (0.0–~1.4s) — presence.** The hero mark/brand lockup holds dead-center, alive but resting — only a faint rotational breath on the mark; any title text under it stays rock-stable. Camera static.
- **Scene 2 (~1.4–2.4s) — the morph (signature move).** The hero CONDENSES at the same screen center into a smaller, brighter CTA (button/card): the outgoing mark shrink-fades exactly as the CTA scales up in its place. Because they share one transform origin, the eye reads it as one element transforming, not a swap.
- **Scene 3 (~2.4–3.4s) — approach.** A cursor arrives from off-stage on a decelerating path (it "arrives," it does not pass through) and lands a few pixels off the CTA's geometric center, so the aim reads human, not scripted.
- **Scene 4 (~3.4s–end) — press.** The cursor lands a physical click — cursor and CTA compress together in lockstep, then release with feedback (an optional ripple/glow bloom). Holds on the clicked state.

**Variant — Hook (widget-morph opener):** reorders the beats — press first, morph second, title last. (1) Presence: a lone pill/chip lockup sits centered on a flat field; optionally the cursor glides in, a hover pill-background appears behind the chip, and the click lands with the same lockstep press. (2) The morph: the widget transforms IN PLACE — expands downward anchored at its top edge into a menu, or spring-morphs outward into a prompt card with a small overshoot settle — new content fades/slides into place. (3) Payload: the transformed state performs — a placeholder types with a blinking caret, user text types while a control flips from muted to its vibrant active color, or the menu snap-collapses back to the pill carrying the new value plus a checkmark pop; the background may snap to a new color under the persistent foreground card. (4) Resolve: the widget VANISHES; a plain frame closes the beat — a closing title types on center, or a hold on the flipped solid state.

**Motion vocabulary:** faint rotation-only resting breath (logo scope only); same-center morph-swap (shrink-fade paired with scale-up sharing a transform origin); cursor decel-arrival from off-stage; off-center human aim; lockstep press compression; release feedback ripple/glow. Hook opener additions: anchored downward expand of a pill into a menu and a springy snap-collapse back; chip-to-card spring morph with overshoot settle; a placeholder/user-text typewriter with a blinking caret (may cut mid-word); a control color-state flip from muted to vibrant; a background color snap under a persistent foreground card; a checkmark pop; the widget vanishing to a blank frame; a typed closing title.

**Rule mapping:** the hero-to-CTA condense at one center uses the Scale-Swap Transition rule (a shared `transform-origin: 50% 50%` is what sells the morph; the CTA is `position: absolute` so it doesn't shove the hero during the brief overlap). Resting-hero aliveness (rotation only, scoped to the mark) uses the Sine Wave Loop rule's low-amplitude rotation register. Cursor press plus release in lockstep uses the Physics Press Reaction rule's press-down and release portion. Cursor approach (deceleration from off-stage, off-center landing, hard-cut opacity-in) is a plain translate on `power2.out`. Click ripple/release glow uses the Cursor-Click Ripple rule's attack-decay ring and/or the Ambient Glow Bloom rule's release bloom. In the Hook variant, the chip-to-prompt-card spring morph at one center uses the Scale-Swap Transition rule's base contract (run in the expand direction) plus the Card Morph Anchor rule for the corner-radius/surface ride-along. The anchored-edge expand/snap-collapse (pill ↔ menu, top edge pinned) uses the Anchored Layout Expand rule (edge-anchored directional growth with counter-scaled children — the Card Morph Anchor rule stays reserved for uniform-scale morphs only). Placeholder plus user typing, the blinking caret, and any mid-word cut use the GSAP Effects typewriter recipe plus the Context-Sensitive Cursor rule for the blink plus the Discrete Text Sequence rule for mid-word cut states. The control color flip from muted to vibrant uses the Press-Release Spring rule's color-transition variation. The checkmark pop and card-arrival overshoot use the Spring-Pop Entrance rule. The hover pill-background and igniting click reuse the base variant's Physics Press Reaction and Cursor-Click Ripple mappings unchanged.

**Camera modifier:** static throughout — the morph and click happen in element space; a camera move would compete with the click as the climax. The Hook opener keeps the same contract — even the background color flip is an element-level snap, not a camera event.

#### Cursor-Driven UI Demo

**Intent:** a visible custom cursor drives a real (reconstructed) app UI through clicks/hovers/drags so the screen changes state shot to shot, while the camera chases each interaction — the product surface is the subject and the cursor is the actor.

**Roles served:** Product Intro — first look at the product surface, the cursor sweeps/hovers to introduce the app and reveal what it is, landing on a hovered hero element or freshly popped result, light and exploratory, with a backdrop that steps colors as it goes. Key Feature — one specific multi-step workflow demonstrated end to end (edit/configure/select across 2–4 discrete beats), each beat a real edit the UI responds to live, landing locked on the primary action button or the produced result. Key Feature — an agency/confirmation workflow framed by a cockpit of 3D-tilted flanks, a step list ticking pending → active → complete (a snap state machine), and a flank button taking the PRESS as the payoff (color flip to success, a checkmark stamp) — the click is the climax, not a passing gesture. Key Feature — the static-stage STATE TOUR: the cursor drives a reconstructed app through 2–4 discrete feature states on a LOCKED frame, every scene change a click-triggered element swap/scale (a modal springs from center, a side panel slides in from the right edge, settings hard-swap, a table populates, a node-graph builds), never a real camera move, optionally bookended by a title card and a brand end beat. Key Feature — the DRAG-DROP journey: one continuous zoom-breathing shot of a document workspace where the cursor drags a ghosted field chip from an inputs sidebar onto the page, drop-snaps it into a placed field, a modal/typing beat completes it, and the placed element is adjusted in close-up before the cursor heads to the Finish/CTA. Product Intro — the low-event BROWSE: the cursor roams one clean page state and the filter controls answer with slight hover updates, no typed input, no title beats, and the shot may end mid-roam. Product Intro — the HOVER-INSPECT run: a click spawns a labeled toolbar, the camera zooms out from a tight crop to the full page, then the cursor sweeps page elements while a floating inspector panel TRACKS the cursor, outline-highlighting and content-snapping per hovered element. Hook — the ambient MULTI-CURSOR canvas: several labeled teammate cursors work a design canvas simultaneously while the canvas group translate-pans within a static frame and a headline builds word-group by word-group over the demo; the live workshop itself is the hook. Benefits — the demo|text|demo SANDWICH: two static-stage demo beats bridge through a full-screen kinetic/title interlude and back.

**Duration:** 4.0–12.9s (Key Feature runs longest, 4.0–12.9s, with mined state tours at 10.4–12.9s and drag-drop journeys at 9.8–10.6s; Product Intro 4.5–9.3s; Hook ~6.5s; the Benefits demo|text|demo sandwich totals 11.6–12.8s).

**Shot structure:** a product UI surface (a fixed app window, a dashboard/editor, a parallax content-card stack, or a container object/icon) — centered over a background color/gradient, shown flat or 3D-isometric; a custom brand-colored cursor with an icon is the protagonist and the camera servos to whatever it touches; the UI responds LIVE and in sync with each cursor action. Two role-tuned tempos fold in — Product Intro sweeps to introduce, Key Feature performs a workflow — and the camera spans a spectrum from the full chase, to one continuous zoom-breathe, to a fully LOCKED static stage where the UI itself does all the moving.

- **Scene 1 — surface establishes plus first touch.** The product UI surface arrives centered — either simply present, a 3D-parallax stack of content cards, or a container/icon that flies in with a 3D tumble and settles. The custom cursor enters and performs the FIRST action on its first target, with the UI responding live in the same beat. Camera holds or begins a slow push-in toward the acted-on region. Variants: Product Intro uses a low-commitment first touch (a hover/sweep or a field highlight); Key Feature uses a concrete edit (a drag, a typed field, a resized handle); the static-stage tour hard-cuts or window-scales-up from an optional title card, with the app UI fully present from frame one and the camera LOCKED from the start; the Hook multi-cursor variant has no single protagonist, several labeled cursors already at work while the canvas pans and a headline builds.
- **Scene 2 — camera chases to the next interaction (the engine).** The camera moves to the next target (push-in plus pan, a whip-pan, a pan-down) and the cursor performs the next action as the UI updates live; the surface's inner content swaps per interaction. Product Intro navigation is exploratory — a slow pan plus a depth-of-field focus-pull across a parallax card stack, or a container fanning into option cards that spring to position, with the backdrop stepping its color as content swaps. Key Feature repeats for 2–4 beats total, each a distinct operation (a counter counting up, a pill/swatch selecting, a modal sliding up and typing), connected by whip-pans/progressive zoom. The static-stage tour never moves the camera — every beat is a click-triggered element response (a modal springing from center, a side panel sliding in, a table populating row by row, a node-graph building). The drag-drop variant has the cursor grab a field chip and drag a ghost across the page, dropping it with a snap and bounding-box handles, followed by a completion beat (a modal spring-up, a typed name with a live cursive preview), all riding one continuous zoom-breathing arc. The hover-inspect variant has the click spawn a labeled toolbar, zoom out from a tight crop to the full page, then sweep the cursor across page elements with a tracking inspector panel.
- **Scene 3 — payoff state, camera settles, hold.** The cursor lands on its final target and the screen reaches the payoff state; the camera comes to rest and holds. Product Intro hovers the hero element (a card scaling up, a pill appearing, a result card popping in). Key Feature locks a close-up on the outcome (the cursor lands on the primary action button with a hover-backdrop spring-pop). The static-stage tour may add a detachable end beat, or simply rest the cursor on the next target. The drag-drop variant closes on the placed element adjusted (a corner-handle resize) then the cursor sweeps toward Finish/CTA. The browse/hover-inspect modes end mid-demo, with no payoff lock at all.

**Motion vocabulary:** cursor-driven click/hover/sweep-highlight/drag/type; per-interaction live UI response (scroll, value climb, region resize, content swap); camera push-in plus pan/whip-pan/pan-down servoing to each target; coordinate zoom onto the acted region; press-and-ripple on a clicked control; button press-compress; screen-state swap shot to shot; card fan-out to corners; 3D container fly-in and tumble-settle; perspective-flatten (3D-to-2D snap); paginated/stepped backdrop color advance; depth-of-field focus-pull across a parallax card stack; counter count-up; pill/swatch select; modal slide-up plus typing; UI-keyword highlight glow; hard panel swap; side detail panel slide-in; table populating row by row; formula typed into a cell with an instant range populate; drag-and-drop with a ghost chip and drop-snap; corner-handle resize; continuous zoom-breathing single shot; multiple labeled collaborative cursors moving independently; canvas-group translate-pan within a static frame; a headline building word-group by word-group; a click spawning a labeled toolbar; a floating inspector panel tracking the cursor with per-element content snap.

**Rule mapping:** the viewport following the cursor uses the Two-Phase Camera Cursor Tracking rule as the primary mechanism. The click itself uses the Cursor-Click Ripple rule. Screen-state swaps between beats use the Scale-Swap Transition rule. Camera push-in/pan/whip-pan to the next target uses the Viewport Change rule, sequenced into discrete beats by the Multi-Phase Camera rule, aimed via the Coordinate Target Zoom rule. Cursor icon/state changes with context use the Context-Sensitive Cursor rule. Step-by-step UI state progression uses the Dynamic Content Sequencing rule. Sweep-highlights and UI-keyword accents use the ASR Keyword Glow rule. Clicked-button press/release uses the Press-Release Spring rule (or the Physics Press Reaction rule for a heavier press). Panel/card morphs between two states use the Card Morph Anchor rule. Terminal hover-scale, result-card pop-ins, and the final action button's hover-backdrop use the Spring-Pop Entrance rule. Card fan-out to corners composes the Split Tilt Cards rule (the spread) with the Spring-Pop Entrance rule (the settle). A 3D-parallax content-card stack as the surface uses the 3D Page Scroll rule. A tracked badge/pill appearing on an element uses the AI Tracking Box rule. A counter or value count-up uses the Counting with Dynamic Scale rule; a result bar/number filling uses the Stat Bars & Fills rule. Depth-of-field focus-pull across the parallax stack uses the Depth-of-Field Blur rule alongside the 3D Page Scroll rule and the Viewport Change rule's pan. Paginated backdrop color advance uses the Discrete Text Sequence rule applied to a background-color state rather than text. A 3D container's fly-in and tumble-settle uses the Depth Scatter Assemble rule. Element-scale fake zooms on the static-stage tour use the Coordinate Target Zoom rule applied to the surface wrapper rather than the world. Side-panel slide-ins and hard panel swaps compose the Card Morph Anchor/Scale-Swap Transition rules with the Dynamic Content Sequencing rule for per-beat content. Tables populating row by row and fill-handle cascades use the Waterfall Entry rule. Formula typing and letter-by-letter names use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule. A node-graph build composes the Center-Outward Expansion rule (the cards) with the SVG Path Draw rule (the connecting lines). Modal/toolbar/dropdown/window pop-ins use the Spring-Pop Entrance rule. Ghost-chip drag-and-drop, cursor-carried components, fill-handle drags, and corner-handle resizes use the Cursor Drag rule. A tracking inspector panel composes the AI Tracking Box rule's per-frame follow mechanics with the Dynamic Content Sequencing rule for per-element content. A live cursive preview building per keystroke uses the SVG Path Draw rule's progressive stroke reveal keyed to typing progress. Continuous zoom-breathing (the drag-drop variant) uses the Multi-Phase Camera rule's pull-back/focus/push phases plus drift. Motion-blur window fly-ins and tight-crop-to-full-page zoom-outs use the Motion-Blur Streak rule plus the Viewport Change rule. Multiple collaborative cursors use the Multi-Cursor Choreography rule. The canvas-group translate-pan uses the Viewport Change rule (though the camera stays semantically locked). A headline building word by word uses the Waterfall Entry rule.

**Camera modifier:** the defining motion is the camera CHASE — the viewport follows the cursor from target to target via the Two-Phase Camera Cursor Tracking rule, realized as concrete push-in/pan/whip-pan moves under the Viewport Change rule, sequenced into discrete beats by the Multi-Phase Camera rule, with each beat's destination targeted via the Coordinate Target Zoom rule. Product Intro biases toward a slow, exploratory pan plus focus-pull; Key Feature biases toward snappier whip-pans/progressive zoom that march through the workflow and lock static on the action button. At one pole, the static-stage state tour LOCKS the camera for the entire clip and lets the UI itself do all the moving. The drag-drop variant replaces discrete chase beats with ONE continuous zoom-breathing arc. The hover-inspect variant inverts the push-in: a tight-crop open zooms OUT to the full page before the cursor sweep. Pick the pole per brief — chase for workflow marches, locked stage for dense reconstructed dashboards, a single breathe for one-document journeys. What separates this blueprint from the Device-Surface-Showcase blueprint below is the CURSOR-as-actor, not the camera — a fully static tour still belongs here as long as a visible cursor drives every state change.

#### Data-Viz / Count-Up

**Intent:** make numbers and charts the hero — a count-up ring/number, a trend chart, a tilted stat/card grid — and traverse the data instruments with a camera that pushes THROUGH them (or scrolls across them) to land on one hero metric, so the data itself carries the argument.

**Roles served:** Problem — quantifies the pain with real-looking instruments: a count-up ring, then a trend chart, then a stat grid, the camera pushing THROUGH each object into the next to dramatize a worsening/large-scale problem. Product Intro — a confident "look at the result / the data" open: a hard cut from a hook word into a perspective-tilted grid of data-viz cards, then a hands-off camera scroll lands one glowing hero metric while a kinetic tagline assembles word by word. Hook — a cold-open hook on ONE dramatic statistic: the frame opens dark and empty, 3–5 thematic icons puncture in clustered at center, then the headline number EXPLODES upward in size as the icons fling outward to their marks (the count-up and the spread are one beat), closed by a slow camera lean-in, kinetic from frame 1. Key Feature — prove the feature with its own analytics: on a black canvas, kinetic headline beats alternate with self-drawing charts and a 3D-tilted dark dashboard that a cursor SCRUBS (a tracking line plus live tooltips), stitched by hard cuts and one zoom punch — the one variant where a cursor touches the data. Social Proof — a single count-up instrument (a radial gauge arc-draw plus a rapidly ticking metric plus a caption) embedded as ONE BEAT inside a kinetic-typography relay, entered and exited by element-level scale/blur push-throughs.

**Duration:** ~4–12s (the Hook variant ~4s; Product Intro ~6s; the dark-scrub-montage ~7.3–7.75s; Problem ~11–12s; the gauge-beat ~2.5s inside a ~10.8s relay).

**Shot structure:** a data-viz field on a dark or light background with soft corner glows; a gradient brand stroke on charts/rings; clean sans-serif white/dark text; a continuous camera move runs underneath that traverses 2–3 data instruments and resolves on a hero metric — one instrument per beat, and the camera carries the cut.

- **Scene 1:** the first data instrument establishes centered — a stat reads as the hero. A bold center number COUNTS UP while its transform scale grows to the static final type size, with a label below; its paired graphic (a circular progress ring sweeping with a gradient stroke, or a bar/fill) animates in on the SAME ease so number plus graphic land as one beat. Supporting avatar/object elements pop in with spring overshoot into a scattered glowing orbit; a headline fades up. A very slow continuous camera zoom-in runs throughout.
- **Scene 2:** the camera traverses to the next instrument, and that instrument animates — a gradient trend line/area chart DRAWS left to right on grid lines (Problem), or off-center cards SCROLL away as the layout glides (Product Intro). The arriving second stat counts up / the chart resolves.
- **Scene 3/N:** the camera lands the hero metric card (big number, label, delta, rising chart) dead-center; a soft accent glow blooms behind it; the move reaches its peak then eases to a settled, slightly wider composition with the hero centered and supporting cards flanking. Hold on the final frame.

**Variants:** the Problem push-through (count-up → trend → grid) runs Scene 1 as a centered ring plus count-up with scattered orbiting elements, then a fast camera PUSH-IN straight through the center of the ring into a card holding a header over a gradient line chart that draws left to right with grid lines and a translucent area fill, camera pushes through then settles; Scene 3 pans to a second card whose number counts up, holding a grid of the avatar/object elements where a subset dim/blur while the rest receive accent circular checkmark badges that spring-pop, and the camera settles to the end — the traversal is z-depth push-through between instruments. The Product-Intro scroll-to-hero variant opens with a brief hook orb and hard cut, then a slightly perspective-tilted grid of data-viz cards begins SCROLLING with its tilt held while a one-word-at-a-time kinetic tagline builds, the hero card gliding into dead-center as off-center cards slide away, an accent glow blooming behind it with a slight push-in, then the camera eases BACK OUT to a settled wider tilted composition. The Key-Feature dark-scrub-montage alternates kinetic-word beats with data instruments on a black canvas, hard cuts stitching the beats with the camera locked per beat — one beat has a heading hold while a trend line draws itself and breaks above the band with a pop tooltip; another beat is a fast zoom PUNCH into a close-up, slightly 3D-tilted dark analytics dashboard where a white cursor SCRUBS a chart (a vertical tracking line, live date/value tooltips, a second chart activating with a color flip) while the tilted plane drifts gently sideways, then a quick pull-away/fade to black; a final beat lands the closing stat lockup and holds static. The Social-Proof gauge-beat runs inside a static-camera kinetic-type relay: thin concentric arcs radiate from center, a thick progress arc draws clockwise over them, a large metric rapidly ticks up with a caption below, the group slowly scales up, then hard-cuts out — entry/exit for every beat is a scale-up-from-blur in and a scale-up-and-blur-past-frame out, a fake push-through with no camera anywhere.

**Motion vocabulary:** count-up number with transform-scale growth on the value; circular progress-ring sweep; growth bar/progress fill; gradient trend-line plus area-fill left-to-right draw; spring-overshoot pop-in of scattered glowing avatar/object elements; perspective-tilted card grid; directional grid scroll; hero-card centering; soft accent glow bloom behind the hero; slow continuous zoom-in; fast camera push-in/push-through the center of an instrument; lateral/vertical camera pan between cards; a gentle push-in that peaks then eases back out to a wider settle; selective dim/blur of a subset plus spring-pop checkmark badges; a full-frame hook orb into a hard cut; a kinetic tagline assembled word by word. Dark-scrub-montage additions: a self-drawing chart line that breaks above its band; a peak dot plus a pill tooltip spring-pop; a cursor chart scrub with a vertical tracking line and live tooltip readouts; a chart activation color flip; a 3D-tilted dark dashboard plane with slow lateral drift; a fast zoom punch-in; a pull-away/fade-to-black beat exit; hard-cut beat stitching; a kinetic word push-through (element scaling up past the frame); a typed line with a blinking cursor; an impact slam word plus particle-dissolve punctuation; a glowing wave draw; a green delta arrow pop; a stat lockup hold. Gauge-beat additions: concentric static arcs plus a thick clockwise progress-arc draw; a rapid count-up tick; a scale-up-from-blur entrance and a scale-up-and-blur-past-frame exit.

**Rule mapping:** the count-up number whose transform scale grows with the value uses the Counting with Dynamic Scale rule. The circular progress-ring sweep uses the Stat Bars & Fills rule's ring form, drawn via the SVG Path Draw rule. Growth bars/progress fills paired beside a number use the Stat Bars & Fills rule. The gradient trend-line/area-chart draw uses the SVG Path Draw rule. Spring-overshoot pop-ins of avatar/object elements use the Spring-Pop Entrance rule; their scattered-ring layout uses the Avatar Cloud Network rule, or the Orbit 3D Entry rule if they keep orbiting. Spring-pop checkmark badges use the Spring-Pop Entrance rule. The perspective-tilted card grid uses the 3D Page Scroll rule. Directional scroll across the tilted plane composes the 3D Page Scroll rule's scroll with the Viewport Change rule's lateral/vertical pan form. Hero-card centering uses the Coordinate Target Zoom rule or the Viewport Change rule. The hard-cut from the hook orb into the grid uses the Scale-Swap Transition rule. The kinetic tagline assembled word by word uses the Kinetic Beat Slam rule (one onset grid, distinct per-word entrances). Slow continuous zoom-in, push-throughs, lateral/vertical pans, and the push-in-then-out bookend all use the Multi-Phase Camera rule. The soft accent glow bloom behind the hero card uses the Ambient Glow Bloom rule. Selective dim/blur of a subset uses the Depth-of-Field Blur rule (the same focus-falloff rule used in the Constellation blueprint above). A cursor chart scrub uses the Chart Scrub Readout rule. A chart activation color flip is a plain color/opacity chord at the scrub handoff. A 3D-tilted dashboard plane with slow lateral drift composes the 3D Page Scroll rule's tilt with the Sine Wave Loop rule's drift, kept tiny so the scrub stays legible. A fast zoom punch-in uses the Multi-Phase Camera rule (one short aggressive push phase) aimed via the Coordinate Target Zoom rule, with the Motion-Blur Streak rule added at peak velocity. Kinetic word push-through and blow-past-frame exits use the Kinetic Beat Slam rule's beat grammar plus the Motion-Blur Streak rule. Typed lines with a blinking cursor use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule's square-wave blink. An impact slam word uses the Kinetic Beat Slam rule, with its particle-dissolve punctuation using the Particle Burst rule (a deterministic glyph-to-particle dissolve). A glowing wave draw composes the SVG Path Draw rule with the Ambient Glow Bloom rule's glow envelope. A green delta arrow pop and a peak dot plus pill tooltip use the Spring-Pop Entrance rule.

**Camera modifier:** the camera is the through-line that traverses the data instruments — one camera wrapper sequenced by the Multi-Phase Camera rule, with each stop targeted via the Coordinate Target Zoom rule onto the focal instrument/card. The Problem push-through mode combines a slow continuous zoom-in with a fast push-in straight through the center of one instrument into the next, then a lateral/vertical pan to the final card — the z-depth push-through is the signature move. The Product-Intro scroll-to-hero mode uses a hands-off directional scroll across the tilted card plane that lands the hero card center, then a gentle push-in that PEAKS and eases BACK OUT to a wider settle. The Key-Feature montage-cut mode is NOT a through-line at all — hard cuts stitch the instrument beats, the frame is locked inside each beat, and exactly ONE fast zoom punch lands the dashboard close-up, with exits as pull-away/fade-to-black; between instruments, elements fake the push (kinetic words scaling up past the frame). The gauge-beat form drops even the punch — fully static, all push-through element-level.

#### Device / Surface Showcase

**Intent:** a product surface — a device mockup or a floating browser/app window — is the hero held in frame while its screens cycle through a real flow, showcased by a camera move that ranges from a static hold to a continuous 3D push.

**Roles served:** Key Feature — show a feature being experienced inside its real interface, the surface housing the action and its screens advancing through a flow, rather than enumerating tiles or chasing a cursor across a workflow (three mechanic variants differ by camera treatment, not by role). Key Feature — the floating-window push-scroll variant carried to a spotlight climax: a real webpage rendered as a tilted 3D card coasts in like a phone held up (no spring), header keywords flare on a karaoke glow as the voiceover names them, the page rolls to the demoed section, and one element LIFTS off the surface under a radial spotlight that dims the rest. Product Intro — a compact end-to-end product flow (setup/auth → action → success/confirm) plays out cursorless as successive screen states inside the held surface, capped by a confirming button press, bookended by title-card beats — the surface introduces the product by completing its core loop, not by touring screens. Key Feature — the showcase-carousel: two surfaces in sequence (a widget card cycling brand skins, a phone frame with app screens sliding through it) gated by interstitial claim words — a breadth carousel ("N brands / N apps"), not a flow.

**Duration:** 5–11.3s (the page-scroll-spotlight variant 5–9s; floating-window 7.8s; the 3D-hand variant 7.9s; the in-device approval sub-mode 7.9s; the stepwise-flow variant 8.5–9.4s; the static device-tour 9.6s; the showcase-carousel 11.3s).

**Shot structure:** one product surface — a device mockup or a floating browser/app window — is the persistent hero on a styled backdrop (a gradient, a radial, or a stylized 3D void); its screens/sections cycle through a real product flow while a showcase camera (static-hold, push-in-then-zoom-out, or one continuous push) presents it. Each screen state holds roughly 1.0–1.5s.

- **Scene 1 (0.0–~1.5s):** the surface establishes — it slides in from an edge, drifts in from a tilt, or dissolves from a full-frame title card, and settles, with an accent shape or backdrop resolving behind it; the first screen is visible. The showcase camera begins (see the variants below).
- **Scene 2 (~1.5s–~Xs):** the surface is OPERATED on its own face — a tap/select/scroll triggers the first screen advance: old content pushes out or scrolls up, new content pulls up or pushes in from the side; concurrently a label/header word updates. The camera continues its move.
- **Scene 3+ (~Xs–end, repeat for 2–4 screen beats):** the surface ADVANCES through successive screens, each a discrete swap or scroll synced to the surface's flow, while supporting copy swaps or holds a marked reading position. Holds on the final screen (or, in one variant, blooms out).

**Variants:** the static-tour variant (Key Feature, 9.6s) has a device mockup slide in from off-screen and settle, an accent-color shape scaling up behind it with a spring overshoot; the camera stays STATIC the entire clip — a tap compresses a button, the UI scrolls/transitions to the next view, and a side headline swaps beside the device per screen; no camera move, no cursor. The floating-window variant (Key Feature, 7.8s) opens on a full-frame title card (an icon draws in at center, a feature name below, holding ~2s), which dissolves to a macOS-style browser/app window floating on a vivid gradient (traffic-lights, a URL pill, tabs, left nav, central content, a right sidebar); the camera pushes in on a target region (an active item highlighted, a cursor drifting down the list), then zooms back out to re-frame the whole window while the content scrolls through sections, the highlighted item staying marked. The 3D-hand variant (Key Feature, 7.9s) is FULLY 3D: a 3D device drifts in a stylized void with bloom and particles, opening tilted and self-rotating to face the lens nearly flat as ONE CONTINUOUS forward camera push begins; a glossy 3D hand rises from the bottom-foreground and gesture-drives the surface (swipes to scroll a picker panel, taps an option while a header word letter-flips in place); the selection applies (a new layout grows from center to fill the device face, nav flips, a marquee scrolls horizontally); the hand swipes again to scroll the page upward, then drifts out; the camera never stops pushing until the bright device face BLOOMS into a light wash — a zoom-through portal exit. The stepwise-flow variant (Product Intro, 8.5–9.4s; an in-device Key-Feature sub-mode at 7.9s) is CURSORLESS end to end: the surface completes setup/auth → action → success as a narrative arc, opening on a title card or a typed terminal command; the flow surface arrives and step 1 completes via rapid sequential pops (OTP digits filling boxes left to right capped by a green check, or log steps popping top-down); state advances laterally or via a dark-to-light scene swap into a confirm card whose elements stagger in; COMMIT — the CTA button is pressed (a press dip, a spinner "Processing") and a success state renders with check bullets, with a slight camera push-in firing ONLY at the state transition; EXIT — the surface leaves and closing title cards pop in and ease smaller. The showcase-carousel variant (Key Feature, 11.3s) has two surfaces in sequence on a slowly drifting pastel mesh gradient, static camera, gated by centered interstitial claim words: a widget card scales in, flips into a tilted vertical widget and cycles N brand skins (~0.8s each) while a large brand logo crossfades below per flip, then a phone frame enters oversized and tilted, settles upright at center, and full app screens slide left through it, holding on the last — a breadth carousel, no taps, no cursor, no camera.

**Motion vocabulary:** surface establish (edge slide-in plus settle, tilt drift-in plus self-rotate-to-camera, or a title-card dissolve); accent shape spring behind the surface; element-level screen-cycling (scroll-swap, push-in-from-side, scale-swap); button tap-compress; staggered side-headline reveal plus copy swap; in-place header-word letter-flip; floating browser-window-on-gradient idle float; full-frame title-card opener; camera push-in on a region; camera zoom-out re-frame; content scroll-through; one continuous 3D camera-follow push with no cuts; 3D device drift plus self-rotate; stylized-environment bloom/particles; 3D-hand entrance plus swipe-scroll plus tap; picker-panel slide-in; template-apply grow-from-center; horizontal marquee scroll; zoom-through bloom/portal exit; static-hold (no camera) as the floor of the camera range. Stepwise-flow additions: title-card bookends; a typed terminal command with a prompt chevron; sequential top-down log pops; an animated trailing-dots wait state; sequential digit pops with a green check confirm; a lateral screen slide with persistent chrome; a dark-to-light scene swap; a staggered card build-in; a button press dip plus fill flip; a spinner processing state; a success check-bullet reveal; a notification banner spring-in; a lockscreen fade/blur-away as a card expands to fill the device face; a commit-synced micro push-in; a dim overlay; a squircle spring pop; a circular ring draw; an icon morph to a checkmark; a surface exit before a title coda. Showcase-carousel additions: an interstitial claim-word gate; brand-skin cycling with a per-flip logo crossfade; a card flip/morph into a tilted widget; an oversized-tilted surface entry settling upright; a fast slide-left screen carousel inside a static frame; a drifting mesh-gradient backdrop.

**Rule mapping:** screen-cycling (UI scrolling/sections scrolling inside the surface) uses the 3D Page Scroll rule as the primary mechanic for the surface's screen flow. The floating-window establish plus the tilted/floating UI-card presentation composes the 3D Page Scroll rule's tilt/perspective framing with the CSS 3D Transforms technique described earlier in this document. Screen and side-copy state swaps use the Discrete Text Sequence rule. In-place header-word letter-flips use the Hacker Flip 3D Reveal rule. A screen swap as a coordinated shrink-out/pop-in between two states uses the Scale-Swap Transition rule. The "new layout grows from center to fill the face" template-apply move uses the Center-Outward Expansion rule (clustered-at-center → expand to fill). The surface morphing between states, or a title-card-to-window dissolve, uses the Card Morph Anchor rule. Button tap-compress uses the Press-Release Spring rule (or the Physics Press Reaction rule for a heavier press). A floating-window cursor click on the highlighted list item uses the Cursor-Click Ripple rule. An accent-highlight pop on the active item uses the ASR Keyword Glow rule. A drifting cursor down a sidebar list uses the Two-Phase Camera Cursor Tracking rule, paired with the push-in. Floating browser-window idle float and the 3D device's drift-breathe use the Sine Wave Loop rule. A 3D device's drift, self-rotate, and perspective depth use the CSS 3D Transforms technique (or a true Three.js/WebGL scene for a genuine 3D device — see the camera modifier below). A horizontal marquee scroll uses the Viewport Change rule's pan mode on the marquee strip (a thin fit — a literal CSS marquee loop is closer to a plain CSS/JS recipe than a named motion rule). The 3D-hand entrance and its swipe/tap gesture driving the surface is flagged as a special case needing a heavier capability beyond the standard rule library (a real 3D hand model plus WebGL, per the Three.js adapter and the HTML-in-canvas techniques above) — no motion-shape rule in this document models a 3D gesturing hand as a swipe-to-scroll/tap-to-select protocol; the flat cursor rules only model a pointer or typing caret. The zoom-through bloom/portal exit is similarly flagged — no named transition covers a bloom/portal fly-through; build it from the WebGL fragment-shader techniques described earlier. A typed terminal command or non-linear log text uses the Discrete Text Sequence rule with the Dynamic Content Sequencing rule computing each step's window from content length. Sequential top-down log pops, left-to-right OTP digit pops, and staggered confirm-card build-ins use the Spring-Pop Entrance rule's staggered-group form (low overshoot for log lines). A trailing-dots wait state uses the Sine Wave Loop rule (finite repeats, stepping the opacity of three dots on a shared phase). A lateral screen slide with persistent chrome reuses the screen-cycling mapping above (the 3D Page Scroll rule's translateX form inside the clipped surface, with the chrome sitting outside the sliding layer). A notification banner spring-in or a squircle pop uses the Spring-Pop Entrance rule. A lockscreen fade/blur-away as a card expands to fill the device face composes the Card Morph Anchor rule's uniform-scale container morph with the Depth-of-Field Blur rule's blur-away. A commit-synced micro push-in uses the Multi-Phase Camera rule (a single short push phase placed at the state transition). A button press dip plus fill flip uses the Press-Release Spring rule's color-transition variation. A spinner processing state uses the SVG Icon Enrichment rule's rotating internal element. Success check bullets and a biometric ring draw use the SVG Path Draw rule plus the Spring-Pop Entrance rule for the bullet pops. An icon morph to a checkmark is flagged as a special case (a true SVG path morph, beyond the rule library's scope — build it as a keyframed shape interpolation if your runtime supports it). An interstitial claim-word gate is a plain fade-plus-gentle-scale-up chord, deliberately quieter than the Kinetic Beat Slam rule. Brand-skin cycling with a per-flip logo crossfade uses the Discrete Text Sequence rule's whole-state content replacement plus the Scale-Swap Transition rule for flips that read as shrink-out/pop-in; the card-to-tilted-widget flip/morph uses the Card Morph Anchor rule plus the CSS 3D Transforms technique. A drifting mesh-gradient backdrop uses the Sine Wave Loop rule at a very low amplitude on gradient-blob position/hue.

**Camera modifier:** the showcase camera spans a RANGE keyed by variant, all riding a single content-wrapping virtual camera (the Viewport Change rule). The static-tour variant makes NO camera move at all (the camera held at scale 1, or omitted) — all motion is element-level; this is the floor of the range. The floating-window variant runs a two-phase push-in-then-zoom-out arc via the Multi-Phase Camera rule: push IN on the sidebar/region via the Coordinate Target Zoom rule, then zoom back OUT to re-frame the whole window while content scrolls. The 3D-hand variant runs ONE continuous forward push with no cuts, via the Multi-Phase Camera rule's steady-push mode (plus its sine micro-drift) layered over the CSS 3D Transforms technique so the device self-rotates-to-lens during the push, running unbroken into the flagged bloom/portal exit. Across all three, the Viewport Change rule is the base virtual-camera primitive, the Multi-Phase Camera rule sequences the push/zoom phases (and supplies the always-on micro-drift that keeps even the "static" tour from feeling dead), and the Coordinate Target Zoom rule aims the push at off-center screen detail.

**Overflow:** a panned or scrolled surface deliberately moves content past the edges of its framing card. Clip it at the card (`overflow: hidden` on the card/window) AND mark the moving inner layer with a layout-overflow-allowed marker — otherwise an automated layout check will flag the parts that scroll off as bugs rather than recognizing them as intentional; the card clips them visually, the marker tells the check it's on purpose.

#### Fixed Anchor, Cycling World

**Intent:** one element is PINNED — a wordmark, a composer box, an anchor line that enters once and never moves again — while the adjacent region (or the entire surrounding theme) cycles through many discrete states around it, cadence often manipulated (steady stepping, a fast carousel, or a slow-to-accelerating flurry), resolving on an emphasis beat into a completed lockup or a muted freeze. The stillness of the anchor IS the claim: everything changes, this stays. Distinct from the Kinetic Type Beats blueprint below (sub-shape A), where a word-slot inside a centered line swaps and the sentence itself is the subject — there the anchor is a sentence frame on a bare type field; here the anchor is the PRODUCT identity and what cycles around it can be non-text (whole theme skins, chrome/logo swaps, textured label chips, a carousel list), the cycle asserts breadth ("everyone says / works everywhere / calling all X"), and the resolve completes the anchor into a lockup. Distinct from the Ticker Takeover blueprint below, whose cycle ends in a collision — a hero crashes in and shoves the text aside; here nothing ever collides with the anchor: the cycle stops, and a final element quietly joins it.

**Roles served:** Brand Outro — when the sign-off is the brand name sitting immovable while praise quotes/tagline words cycle beside or beneath it, steady per-word highlight stepping or a hard-cut chip flurry that accelerates, landing on the finished lockup. Benefits — when "works everywhere" is shown literally: one product surface (a prompt composer with one verbatim string) pinned dead-center while its ENTIRE shell morphs in place through N product themes (background, typography, radii, chrome, logos all crossfading at once), ending in a washed-out freeze. Hook — when the opener is a roll-call: a static anchor line holds while an accent-colored line beneath it runs as a fast vertical carousel through an audience/option list, then the block clears into follow-up statement beats that land the brand line.

**Duration:** 6.6–11.1s (the Benefits variant is shortest at ~6.6s with 4 theme beats; the Brand Outro variant runs ~9–9.4s; the Hook variant runs longest at ~11s when the anchor-cycle block hands off to follow-up statement beats). The cycle engine itself occupies ~3–5s regardless of role.

**Shot structure:** a flat static frame — camera locked throughout — on a solid or subtly drifting background; two folded sub-shapes: (A) adjacent-region cycle, where the anchor holds and a neighboring slot swaps through N states, and (B) whole-context morph, where the anchor holds and everything AROUND it re-skins in place.

- **Scene 1 (0.0–~2.0s) — the anchor lands and pins.** The anchor (a wordmark, product name, composer box, or lead line) enters once — a fade/scale-in centered, a word-by-word build, or already present at frame one — at a fixed position it will hold for the entire clip. Zero movement from here on: no drift, no breathe, no re-layout. If the anchor is a UI surface (sub-shape B), it carries a verbatim string with a blinking cursor.
- **Scene 2 (~2.0s to ~70% of runtime) — the cycle engine (signature move).** The world changes around the unmoved anchor. Sub-shape A (adjacent-region cycle): a region beside/beneath the anchor steps through N discrete states via one swap mechanic and one cadence — instant hard-cut label replacement (a chip/tape label slaps over the old one, re-fitting width each time, growing away from the anchor, never over it); sequential per-word highlight stepping (one word of a tagline snaps bright/bold while the rest sits dim grey, the highlight walking the line); or a fast vertical carousel (each list item slides/fades through the accent slot ~0.5s per phrase). Cadence is either steady stepping (~0.5–1s per state) or a slow-to-accelerating flurry (~1s beats compressing to ~0.15–0.3s per swap). The cycling region must never overlap, touch, or displace the anchor. Sub-shape B (whole-context morph): at roughly 1.3s intervals the entire theme — background color, typography, corner radii, toolbar icons, footer brand logos, contextual lines — morphs in place via quick (~0.3s) crossfades through N product skins, every property blending simultaneously; no hard cuts, no wipes; the anchor's content string is identical in every skin.
- **Scene 3 (~70–85%) — the emphasis beat.** The cycle resolves, not just stops. Brand Outro (highlight stepping): the whole tagline snaps solid bright at once. Brand Outro (flurry): the flurry halts and holds on the longest/weightiest phrase. Benefits (theme morph): the final beat mutes — a faint dot-grid fades in across the background while the UI drops to low opacity, a washed-out blueprint freeze. Hook (carousel): the anchor block clears, handing off to 1–3 centered word-by-word statement beats that carry toward the close.
- **Scene 4 (final beat to end) — lockup completion and hold.** A final element joins the still-unmoved anchor and the finished composition holds static to the end: a closing word drops in below aligned to the last cycled state, the chip vanishes on a hard cut and a brand sign-off appears beside the anchor on a shared baseline, or a final brand line builds word by word dead-center and holds. The lockup is the payoff — give it 20–30% of the runtime.

**Motion vocabulary:** anchor fade/scale-in entrance; a permanently pinned anchor with zero movement; instant hard-cut chip replacement with width resize-to-fit; sequential per-word highlight stepping through a line; dim-to-grey line state; a whole-line illumination snap; a fast vertical carousel slide/fade of one line under a static line; cadence acceleration into a flurry; a hold-on-longest-phrase emphasis beat; an in-place theme-morph crossfade blending background/fonts/radii/icons simultaneously; per-beat chrome/logo swap; a blinking text cursor; a dot-grid backdrop fade-in; a global opacity washout; an end freeze; word-by-word phrase build; a block clear between scenes; a drop-in of a final word; a hard cut to the final lockup; a long static hold.

**Rule mapping:** instant hard-cut chip/label/phrase swaps at time thresholds, per-word highlight stepping, dim-line-to-full-line illumination, and per-state chip width sets (set discretely, never tweened) all use the Discrete Text Sequence rule. A fast vertical carousel of the accent line under the static anchor uses the Vertical Spring Ticker rule (its footer-reveal step unused — Scene 4's lockup takes its place). Per-phrase state windows computed from a script of N states use the Dynamic Content Sequencing rule (the accelerating-cadence variation, pre-computing the beat array with shrinking hold values). Word-by-word phrase builds use the Dynamic Content Sequencing rule plus the Waterfall Entry rule (or the Kinetic Beat Slam rule when the statements should land percussively). The anchor's entrance and the drop-in of the final closing word use the Spring-Pop Entrance rule with a restrained, editorial overshoot register. A blinking cursor in a pinned composer uses the Context-Sensitive Cursor rule (color adapting per theme skin at segment boundaries). The whole-context theme morph uses the Theme Crossfade Morph rule (N pre-styled full-scene layers stacked at the same geometry, opacity-crossfaded, the shared anchor string rendered once on top); a composer shell's radius/surface component alone uses the Card Morph Anchor rule. A subtly drifting background field beneath the cycle uses the Sine Wave Loop rule (bounded drift; the anchor itself gets none). The dot-grid fade-in and global opacity washout freeze are plain opacity tweens; the long static hold needs no rule.

**Camera modifier:** none — every member of this blueprint is fully camera-static; the cycle is the only motion, and the pinned anchor's stillness is load-bearing. Do not add a push-in "for energy" — it would break the anchor contract.

#### Grid / Card Assemble

**Intent:** N items (tiles/cards/logos/list-lines) self-assemble in a staggered cascade into a grid or vertical list and hold — a "look how much/who/what it does" beat that enumerates breadth at once; an optional camera zoom-OUT pulls back to reveal the assembled array sitting inside a vaster whole.

**Roles served:** Key Feature — a grid of labeled feature tiles/pills (icon plus label) cascades one by one into a 2-column-brick or 3×3 grid, then holds near-static with a slow push-in — enumerate many capabilities, no live UI, no cursor. Key Feature — open TIGHT on 2–3 glowing icons, then a camera zoom-out unfolds a row of glassmorphism cards that grow from behind the icons (icons shrink to card headers), the center card scales forward, the group floats, then sweeps out — a "pillars revealed at once" variant. Benefits — short value phrases populate a single vertical list at roughly 1 item/sec, co-resident and accumulating; each line enters via a spring marker-pop plus check-draw plus pill mask-wipe, OR the whole stack snaps up one slot per beat (slot-machine) so the newest lands in the bright focal slot. Social Proof — a wall of partner/app logos builds into a center grid (whole-enter, randomized pop-in, or column slide-up), an optional headline plus accent-gradient proof-number filling in above, then a continuous camera zoom-out shrinks the array to reveal a vast ecosystem; optional fixed HUD/viewfinder brackets; optional grid slide-up fly-out exit. Key Feature — the array assembles by POPULATING ITSELF: skeleton pills fill and swap to real data, cards spring in tethered to map markers, and the state keeps flipping live after assembly (status pills stepping through states); no cursor, locked frame — the "look how much" beat becomes "look, it's doing it right now." Benefits — a breadth FIELD: a rapidly streaming list past a fixed focal slot, or a chip array with one highlighted hero, plays its breadth motion, then CLEARS to concise centered payoff text (a claim, price, or URL end card).

**Duration:** 3.0–10.5s (Social Proof 3.0–6s; the live-populate variant 4.2–7.8s; the Key Feature grid 5.8–7.3s; the Benefits stream/field-to-payoff variant 5.9–8.4s; the Key Feature glass-card variant 6.5s; the Benefits list variant 6.5–10.5s, scaling roughly 1 item/sec with count).

**Shot structure:**

- **Scene 1 (0.0–~1.0s) — open plus first arrivals.** On a gradient/radial/dark background (optionally with a dot-grid or drifting-watermark texture), an empty grid or list region is established and items begin to ASSEMBLE in a quick staggered cascade (~0.04–0.08s gap; list pacing ~1 item/sec). Each item (a feature tile, pill, logo tile, or benefit line) fades and slides/scales a short distance directly into its slot — low drama, no scatter, no big bounce (spring overshoot is reserved for accent markers). Camera static. An opening headline/hook may fill in line by line above the array, with any proof number counting up in an accent gradient.
- **Scene 2 (~1.0s to ~Xs) — array resolves and holds.** Remaining items finish arriving; layout resolves into the final grid/mosaic/list shape. The completed array HOLDS, alive but resting: a gentle continuous parallax/sine float on the tiles and/or a slow camera push-in (a faint scale-up). Optional accent-color glow travels across/behind the tiles.
- **Scene 3 (~Xs–end) — settle/reveal/exit.** Everything settles and holds to the end, or the optional camera modifier runs (see below), or a closing line/CTA book-ends the array, or the field CLEARS to payoff copy — the array exits and a concise centered claim/price/URL lands, or the camera PUSHES THROUGH one highlighted hero item and crossfades into a second, vaster receding word-grid depth field that continuously scales down to reveal ever more items before fading to the payoff.

**Variants:** the Key Feature grid variant assembles labeled icon-plus-label tiles into a 2-column-brick or 3×3 grid, holding near-static with a slow push-in plus an optional traveling-glow sweep, book-ended by a headline and CTA, no camera reveal. The Key Feature glass-card-reveal variant is CAMERA-DRIVEN, not element-stagger — open tight on 2–3 glowing icons, camera zoom-out grows N glass cards from behind the icons (icons shrink to become card headers), the center card scales up slightly and moves forward to overlap the sides with a quick spring, cards hold side by side with continuous parallax float, and the exit is a fast motion-blur sweep sliding the cards off-frame. The Benefits vertical-list variant runs a single vertical benefit-line stack at roughly 1 item/sec with three sub-modes — BUILD (each line stays fully lit; entry is a marker spring-pop plus a check/icon draw-in plus a pill mask-wipe of the text), SNAP (the whole stack steps up one slot per beat so the newest line lands in the bright focal slot, lines leaving it dimming by position), or STREAM (the list scrolls rapidly and continuously past the focal slot — center item opaque and slightly enlarged, neighbors faded/shrunk — then decelerates to stop on the chosen item, optionally split-framed against a fixed static label, then clearing to a centered payoff line). The Key Feature live-populate variant is a data-population wave, cursorless, frame-locked (plus or minus one gentle opening zoom-out that makes room for the headline) — two board shapes: ANCHORED (white data cards spring in one by one, each tethered by a thin line to its marker on a map/board surface whose markers pulse with expanding fading rings) or TABULAR (new columns appear as grey skeleton pills, progress fills run left to right staggered top to bottom, each bar swapping to its real value/avatar chip on completion); after assembly the array stays LIVE, with status pills flipping states in quick snappy swaps or a second population wave running on a newly revealed region. The Social Proof logo-wall-zoom-out variant has an intro beat (a trusted-by headline card or a product screenshot) crossfade/cut to a center logo grid that builds, then a continuous camera zoom-out shrinks the whole grid toward center to reveal a vast ecosystem and holds, with optional fixed HUD/viewfinder brackets and an optional exit where the whole grid slides up and flies out through the top.

**Motion vocabulary:** item stagger-assemble (fade plus short slide/scale into slot); brick/grid/list layout resolve; randomized pop-in; column slide-up; a vertical-list step (slot-machine snap-and-hold); a spring-overshoot marker pop; a check/icon draw-in; a pill/label mask-wipe reveal; dim-by-position de-emphasis; line-by-line headline fill; an accent-gradient number count-up; a near-static hold with a gentle parallax/sine float; a slow camera push-in; a camera zoom-out reveal (continuous or phased pull-back); cards-grow-from-behind-icons with icon-shrink-to-header; a center-card scale-up plus forward overlap (spring); a traveling-glow sweep; fixed HUD/viewfinder brackets; a motion-blur slide-out sweep exit; a grid slide-up fly-out exit; a book-end headline fade; a perpetual decorative orbit/loop; a skeleton-pill progress fill (left to right, leading tip, color transition); a fill-completes-swap-to-real-data beat; a staggered top-to-bottom fill cascade; live status-pill state flips; a tethered-card spring-in with pulsing marker rings; a two-wave populate with a headline crossfade; a sticky-column internal horizontal scroll; a rapid vertical stream past a fixed focal slot with deceleration; a split fixed-label layout; a highlighted hero chip; a push-through-the-hero-item exit; a receding word-grid depth field; a clear-to-payoff coda; a price snap-build; a left-to-right URL reveal with a final-beat color flip.

**Rule mapping:** item stagger-assembly into a slot uses the Center-Outward Expansion rule (per-item stagger, short-path slide variant — for a wall too dense for a true center burst, use its "starting partially-spread" or direct-into-slot form). Randomized pop-in stagger and column slide-up use a plain stagger recipe. The vertical-list step or slot-machine snap-and-hold uses the Vertical Spring Ticker rule. A spring-overshoot marker pop uses the Spring-Pop Entrance rule. A check/icon draw-in inside a marker uses the SVG Path Draw rule; a live line-art icon in a tile uses the SVG Icon Enrichment rule. A pill/label mask-wipe text reveal uses the Clip-Path Reveal Masks technique from the broader-techniques section earlier in this document. Dim-by-position de-emphasis is a plain per-line opacity tween by slot position. Line-by-line headline fill uses the Discrete Text Sequence rule. An accent-gradient proof number count-up uses the Counting with Dynamic Scale rule. A gentle parallax/sine float on the hold uses the Sine Wave Loop rule (applying the concurrent-elements amplitude reduction for a held grid). A slow camera push-in uses the Multi-Phase Camera rule's steady-push pattern. Center-card scale-up plus forward overlap uses the Spring-Pop Entrance rule plus the CSS 3D Transforms technique for the z-depth overlap. Cards-grow-from-behind-icons is driven by the camera reveal itself (Multi-Phase Camera rule) — the grow/shrink are scale tweens chorded to the pull-back phase, no separate rule needed. Fixed HUD/viewfinder brackets use a static-bracket variant of the AI Tracking Box rule (an overlay frame, not tracking). A book-end headline fade uses the Discrete Text Sequence rule or a plain fade. A perpetual decorative orbit/disc/loop uses the Sine Wave Loop rule (or the Orbit 3D Entry rule if it's an orbiting badge ring). A traveling-glow sweep across/behind tiles uses the Ambient Glow Bloom rule. A motion-blur slide-out sweep (glass-card exit) uses the Motion-Blur Streak rule. A grid slide-up fly-out exit is a plain staggered off-frame translate. A skeleton-pill progress fill uses the Stat Bars & Fills rule's progress-fill `scaleX` form, with the leading tip as a chorded child element. Fill-completes-swap-to-real-data, live status-pill flips, and headline crossfades between waves use the Discrete Text Sequence rule (whole-state replacement at time thresholds). A staggered top-to-bottom fill cascade is a plain per-row stagger on the fill tweens. A tethered-card spring-in composes the Spring-Pop Entrance rule (the card) with the Avatar Cloud Network rule (the thin connection-line-to-anchor layout, anchor coordinates matching the marker exactly) plus the SVG Path Draw rule if the tether draws in. Pulsing marker rings reuse the Cursor-Click Ripple rule's expanding-ring attack-decay envelope, minus the cursor/click, on a bounded repeat. A sticky-column internal horizontal scroll uses the Viewport Change rule's pan form on the inner column layer (with the sticky column outside the panned layer), marked with a layout-overflow-allowed attribute and clipped at the table card. A rapid vertical stream past a focal slot with deceleration uses the Vertical Spring Ticker rule's continuous form (one long decelerating translate instead of stepped tweens), reusing the dim-by-position mapping for the focal-slot emphasis. A pill-widens-as-label-fills beat uses the Card Morph Anchor rule's uniform-scale/clip-path substitution law (never tween width) plus the Discrete Text Sequence rule for the label fill. A push-through-the-hero-item exit uses the Multi-Phase Camera rule (a single accelerating push phase) aimed via the Coordinate Target Zoom rule at the highlighted chip, crossfading at peak. A receding word-grid depth field uses the Viewport Change rule (one world wrapper, camera scale decreasing continuously — the zoom-out reveal grammar pointed at a word field, with size/opacity tiers faking the depth). A price snap-build uses the Discrete Text Sequence rule's non-linear typing (bulk additions, exactly its typo/partial-state mechanic). A left-to-right URL reveal uses the same Clip-Path Reveal Masks technique as the pill mask-wipe above; the final-beat color flip is a plain `tl.set` at the beat.

**Camera modifier (zoom-out reveal, optional — the role-defining move for the glass-card and logo-wall variants):** a camera wrapper around the whole array scales DOWN over the hold, revealing the assembled grid/cards sitting inside a larger environment. A continuous single-pass zoom-out (Social Proof ecosystem pull-back) uses the Viewport Change rule (one wrapper, camera scale decreasing via a single writer). A phased pull-back → focus → settle with built-in drift (Key Feature tight-icons → cards-unfold) uses the Multi-Phase Camera rule's "Dramatic reveal: push → neutral → pull" pull-back phase pattern, with card grow/shrink chorded to the pull-back phase.

#### Kinetic-Type Beats

**Intent:** a flat, centered, bold-type shot where the motion IS the word/phrase changing — the line either swaps tokens in place by hard cut, or builds a statement across full-screen beats (each with its own move) that lands a spring-pop payoff.

**Roles served:** this is the widest-serving blueprint in the library, spanning six roles across many sub-shapes. Hook — a stationary line landing a punchy rhetorical question or "you keep doing X" callout where the in-place token swap itself is the joke; or one statement escalating across distinct full-screen beats punctuating on a spring-pop payoff element; or rapid centered word beats warming up for a typography-to-brand arc that resolves into a logo reveal; or three center-stage beats on a constant field, each element alone on screen, where a beat's payload may be non-text. Problem — 3–5 short pain statements (or a "what-if?" framing) that each land alone on a bare canvas before the next replaces it, no product visible yet; or an ordered chain of question/hook phrases that scale-pop through center relay-style, landing a specially-styled climax word, or resolving the question on a product surface entering as an element move (never a camera zoom). Product Intro — hard-cutting through "Introducing…"/tagline/value beats to resolve on the brand name or logo; or a fixed headline holding while only one word-slot changes (cursor-deleted-and-retyped once, or rapid-cycled through a role list) before handing off to the product/brand payoff — the purest sub-shape A; or a sentence building word by word on a flat brand-color field where each hero word earns a bespoke one-shot effect payoff before a punch-word finale; or the anchored type itself mutating, an "Introducing"/predecessor beat building or swapping into the wordmark in place, which then transforms into a short payoff beat. Benefits — a rapid-fire staccato montage of 8–12 short value phrases flashing and clearing at high tempo; or a slow statement relay of 2–4 full statements on a flat void, each built by its own engine and held ~1.5s+ before the hard cut. CTA — a punchy closing line (or short stack of value lines) that snaps/fades in beat by beat and lands on the brand lockup or URL, no spatial set, no clicked button; or a sign-off chaining 3–5 message beats where each beat carries a different kinetic gag before the logo/URL forms. Brand Outro — a rapid center-channel barrage of single-word verbs asserting breadth, resolving on the brand's one defining word; or a short relay of full-frame beats terminating in a centered URL/domain end card held for the longest stretch of the shot.

**Duration:** 3.0–12.9s (the Benefits staccato variant is fastest at ~3.5–4s across 8–12 sub-0.5s beats, while the Benefits statement-relay variant runs up to ~8.3s; the Product Intro fixed-line variant runs as short as ~3.0s; Problem spans 4.1–12s; CTA spans 3.6–12.9s with beat count; Brand Outro spans ~3.6s as a verb barrage up to ~12.6s when the terminal URL hold carries 40–75% of the runtime).

**Shot structure:** a flat, fixed center anchor; bold sans-serif text on a solid background color; type/tokens are the default subject, though a beat's payload may be one non-text center-stage element (a logo lockup, a CTA button, a chart) obeying the same arrive-hold-clear law; camera locked unless a modifier is noted; two folded sub-shapes — (A) fixed-line token swap and (B) multi-beat statement build.

- **Scene 1 (0.0–~1.0s) — first beat lands.** A solid background field. Bold text arrives dead-center via ONE entrance — type-on character by character with a trailing blinking caret, a hard-cut flash-in (no fade/slide), a per-word staggered fade/blur, or an oversized word that smoothly scales down to a small centered word. An optional accent move plays on the key word(s) — a drawn underline/strike-through, a small particle/dot burst from behind the text, or an accent selection-box framing the word. The various role/sub-shape variants shape this beat differently — a hook line parking with no escalation move, an escalation beat sitting over a glowing motif with a slow camera push-in, a triptych beat that may be non-text (a logo mark rotating in 3D and snapping flat), a pain line revealing in chunks, a relay phrase scale-popping into center on a flat or drifting-gradient field, an "Introducing" word entering with a typographic accent, a fixed headline parking with no escalation (the slot is the show), a field-claiming stripe-wipe opener revealing a logo lockup before the sentence starts building, or a wordmark-transform "Introducing" fading in over ambient sine-wave lines.
- **Scene 2..N — beats replace each other in place (the engine).** The center anchor advances one beat at a time; nothing from the prior beat lingers. Sub-shape A (fixed-line token swap): the line stays fixed and only the variable slot changes by an instant hard cut (no roll/scroll/blur), or the final word(s) backspace out and a new word retypes; the rest of the line holds, and the cycle may run a rapid role-word list at the fixed slot, optionally performed by a labeled collaborative cursor. Sub-shape B (multi-beat statement build): each full-screen beat hard-cuts to a new background/line, each getting its own distinct entrance/exit move — springy scale-in/out overshoot, a 3D letter-tumble (glyphs scatter into a rotating depth cloud then reassemble), a motion-blur fly-in that resolves sharp at center, prior text accelerating/zooming past the camera while fading, a letter-spacing collapse, or a bottom-up masked slide; background may hard-flip between two states on selected beats with the type color inverting to stay legible. Per-role variants layer their own additional gags into this engine: an escalating snap-in climax beat with a Z-dolly-through-a-glyph or a karaoke highlight sweep exit; a triptych CTA-button beat that spring-pops with a one-shot glow-ring pulse; pain lines entering by chunk-reveal or motion-blur fly-in with an interstitial what-if word zooming past the camera; a relay phrase-clear that split-slides the prior phrase off toward both edges while an emphasis beat letter-tracking-tightens with corner arrows converging; inverted-text tagline beats with a strike-through/slider-shape/bg-invert accent; a word-run sentence building word by word with an underline draw and one bespoke effect per hero word (letter-scramble, chromatic-glitch jitter, spring-bounce confetti burst, or an emoji-morph swap); a wordmark-transform completing in place via staggered part-by-part pop or a gradient hue-sweep settling to solid; a high-tempo Benefits montage with springy pops or 3D letter-tumbles and bg light/dark flips; a low-tempo Benefits statement relay where each statement builds by its own engine (char-by-char typing under a static line, an oversized phrase element-scrolling through the frame, stacked outline-echo copies cycling behind a solid word, or accent shapes flying in and drifting outward); CTA value-line clears by hard cut/zoom-blur/fade with an optional accent motif drawing on behind; a CTA beat-chain where each beat carries its own gag (a marquee scroll-through, a flash-swap word list, a brief 3D letter extrude, a spring-bounce prop, one interleaved mock-UI beat); a Brand-Outro single-verb hard-cut march at a steady ~0.2s cadence over a continuous moving field; or a Brand-Outro relay-to-URL where 2–3 full-frame beats swap wholesale at a relaxed cadence via fade/scale, a spring shrink-to-0, an icon bounce, or a gradient-swept title card before the hard cut to bare canvas.
- **Scene N (final beat to end) — resolve and hold.** The last beat lands and holds to the end (settle only, no further scale-out). Resolution diverges by role: a Hook flash lands and holds with an optional punctuation snap; a Hook escalation resolves on a payoff element that spring-pops center with drifting accent motes; a Hook logo-reveal resolves on the brand (the logo popping in whole, or floating 3D shapes assembling and flattening into the flat mark) then a browser mockup/value card slides/scales in; a Hook triptych's final beat may be non-text (a benchmark chart fading in its framework and growing bars from zero in a top-down stagger); a Problem line reveals via a left-to-right swipe with leading-edge blur or a radial letter-explode; a Problem relay's climax word scales in with a gradient fill and slight rotation, or the question resolves on a product surface via an element move (a pill/search bar sliding in with progressive text reveal); a Product-Intro beat resolves on the brand (a logo/wordmark popping in centered, optionally through an expanding-iris circle wipe); a wordmark-transform variant runs a dense UI-screenshot collage rushing outward from behind the anchored text with parallax, or one word morphing into a pulsing icon, or the title zoom-blurring away; a Benefits phrase simply settles, never tumbling back out; a CTA lands on the lockup (a logo scaling up small-to-full, or a logo/URL building segment by segment); a CTA glow-preceded formation has the prior letters scatter/clear, a soft glow pulses on the empty field, and the logo mark FORMS out of the glow; a Brand-Outro hard-cuts to the resolve word/brand keyword and holds briefly while the background field keeps moving; a Brand-Outro relay-to-URL fades/scales the centered URL/domain in and holds — the LONGEST beat of the shot, roughly 40–75% of the runtime.

**Motion vocabulary:** hard-cut/flash word swaps; in-place token cycling with no roll/scroll/blur; type-on with a trailing blinking caret; backspace-and-retype; per-word staggered fade/blur reveal; big-to-small scale-down; springy scale-in/out overshoot; 3D letter-tumble scatter-and-reassemble; motion-blur fly-in/blur-off; prior text zoom-through-camera; letter-spacing collapse; a bottom-up masked slide; a drawn-on accent underline/strike-through; a particle/dot burst from text; an accent selection-box frame; a bg-invert hard-flip with text-color invert; a karaoke per-word highlight sweep; a radial letter-explode; an expanding-iris circle wipe-to-next; a final spring-pop payoff element; drifting accent motes/ambient shapes; a segment-by-segment URL/wordmark build; a final-token punctuation snap; a settle-and-hold; a scale-pop phrase relay with split-slide-off clearing; a letter-tracking tighten-from-wide while scaling; corner arrows converging on a word; a gradient-fill/hue-sweep across type settling to solid; an in-text traveling gradient sweep; a background-shape morph-open into a full-bleed field; an RGB-split/chromatic-glitch jitter; a horizontal stretch/slice glitch reveal; a letter-scramble resolve with divider ticks; a confetti burst up-and-drift; a letter-slot emoji/mark swap-and-morph; an alternating huge/small word scale chain; color-stripe wipes or a blob expand frame-repaint; an oversized phrase element-scroll (a moving window); a right-to-left marquee scroll-through; stacked outline-echo copies cycling behind a solid word; a full-frame repeating-word pattern on a rolling 3D wave; accent shapes flying in then drifting out and thinning; a masked grey fill snapping solid; a brief 3D letter extrude-then-flatten; a spring-bounce glyph-plus-prop drop-in; a glow-pulse-preceded logo formation; 3D shapes assembling-and-flattening into the mark; a logo-lockup 3D rotation-snap; a one-shot glow-ring pulse; chart bars growing in a top-down stagger; a labeled collaborative cursor delete-and-retype; an in-place role-word cycle; ambient plexus/pattern drift; a spring shrink-to-0 exit or bounce-in from 0%; scattered-letter bounce-assembly with baseline settle; a staggered wordmark part pop; a phrase append; a word-to-icon morph with continuous pulse; a UI-collage rush-out with parallax from behind anchored type; a zoom-blur title exit; a long-held URL end card.

**Rule mapping:** hard-cut/flash word swaps, in-place token cycling, and whole-line state swaps at time thresholds all use the Discrete Text Sequence rule. Type-on plus a blinking trailing caret uses the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule's caret blink/color-switch. Backspace-and-retype uses the Discrete Text Sequence rule. One short distinct phrase per beat, or script-driven phrase windows, uses the Dynamic Content Sequencing rule. Percussive per-beat phrase entrances on a shared beat array use the Kinetic Beat Slam rule (the best fit for the multi-beat statement-build engine and the ~0.2s Brand-Outro verb march). Per-word staggered fade/blur reveal uses the Kinetic Beat Slam rule's per-phrase distinct entrances, with the soft-focus blur component backed by the Depth-of-Field Blur rule. Big-to-small scale-down and springy scale-in/out overshoot use the Spring-Pop Entrance rule backed by a plain scale tween. 3D letter-tumble scatter-into-depth-cloud-then-reassemble uses the Depth Scatter Assemble rule (combine with the 3D Text Depth Layers rule for an extruded read, or the Hacker Flip 3D Reveal rule for an in-place per-char flip flavor). A karaoke per-word highlight sweep uses the ASR Keyword Glow rule (or the CSS Marker Patterns rule's highlight sweep for a static-timeline, non-audio-synced version). Drawn-on underlines/strike-throughs/loops/scribbles under a key word use the CSS Marker Patterns rule. A particle/dot burst from behind text uses the CSS Marker Patterns rule's burst mode backed by a plain stagger. An accent selection-box frame around a word uses the CSS Marker Patterns rule's circle/box marker. A bg-invert hard-flip with text-color invert uses the Discrete Text Sequence rule (a synchronized fg/bg state change). Letter-spacing collapse and a bottom-up masked slide use a plain letter-spacing tween plus the per-word kinetic typography and clip-path-reveal techniques described earlier in this document. An expanding-iris circle wipe that morphs the current word into the next uses the Scale-Swap Transition rule. A final spring-pop payoff element uses the Spring-Pop Entrance rule (or the Physics Press Reaction rule for a weightier pop). Drifting accent motes and ambient shapes beneath the type use the Sine Wave Loop rule. A segment-by-segment URL/wordmark build uses the Discrete Text Sequence rule or the Dynamic Content Sequencing rule. A final-token punctuation/emphasis snap uses the Discrete Text Sequence rule. Motion-blur fly-in/blur-off/zoom-through-camera on type uses the Motion-Blur Streak rule. A radial letter-explode uses the Depth Scatter Assemble rule (radial per-letter explode-and-resolve is in scope alongside the depth-cloud scatter). A scale-pop phrase relay uses the Spring-Pop Entrance rule for the arriving phrase plus a plain shrink-and-split-slide for the prior phrase's clear. Letter-tracking tighten-from-wide-while-scaling uses a plain letter-spacing tween (the inverse of the collapse mapped above). Corner arrows converging on a word use the CSS Marker Patterns rule's burst geometry with inverted travel. A gradient-fill climax word, a hue-sweep across type, or an in-text traveling gradient sweep uses the Gradient Text Sweep rule. A background-shape morph-open into a full-bleed field uses the Card Morph Anchor rule. RGB-split/chromatic-glitch jitter and horizontal stretch/slice glitch reveals use the Chromatic Glitch rule. A letter-scramble resolve with divider ticks uses the Hacker Flip 3D Reveal rule (the deterministic glyph-substitution decode, minus the 3D rotation). 3D shapes assembling-and-flattening into the mark, plus scattered-letter bounce-assembly, use the Depth Scatter Assemble rule plus the Spring-Pop Entrance rule for the bounce settle. A logo-lockup 3D rotation-snap uses the Orbit 3D Entry rule's 3D flip-in entry, skipping the orbit phase. A one-shot glow-ring pulse, and a glow-pulse-preceded logo formation, use the Ambient Glow Bloom rule plus the Spring-Pop Entrance rule. Chart bars growing top-down, and a radial gauge arc-draw plus count-up, use the Stat Bars & Fills rule plus the Counting with Dynamic Scale rule. A labeled collaborative cursor's delete-and-retype, and an in-place role-word cycle, use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule (the labeled-pointer look itself is an oversized-cursor styling choice, not a separate rule). Ambient plexus/pattern drift, and accent shapes drifting-out-and-thinning, use the Sine Wave Loop rule (finite drift) after a Spring-Pop Entrance rule arrival. A letter-slot emoji/mark swap-and-morph, and a word-to-icon morph with continuous pulse, use the Scale-Swap Transition rule plus the SVG Icon Enrichment rule for the icon's internal pulse. An oversized phrase element-scroll, and a right-to-left marquee scroll-through, use a plain linear translate of an oversized element through a static frame. Stacked outline-echo copies cycling behind a solid word use the 3D Text Depth Layers rule's offset echo stack plus the Vertical Spring Ticker rule's vertical cycle. A brief 3D letter extrude-then-flatten uses the 3D Text Depth Layers rule (building the extrusion offsets, then collapsing them). A full-frame repeating-word pattern on a rolling 3D wave is flagged as a special case — a 3D wave-mapped text field is out of the standard rule scope, though the Sine Wave Loop rule can drive the undulation oscillator. An alternating huge/small word scale chain uses the Kinetic Beat Slam rule's distinct per-beat entrances. Color-stripe wipes use masked translate tweens; a blob expand frame-repaint uses the Card Morph Anchor rule. A UI-collage rush-out with parallax from behind anchored type uses the Center-Outward Expansion rule (clustered-at-center → outward, with varied per-tile rates/scales for the parallax read). A spring shrink-to-0 exit uses the Spring-Pop Entrance rule (a plain `back.in` shrink for the outbound half). A product-surface resolve (a pill sliding with progressive text reveal, or a canvas scale-down as chrome frames in) uses the Nudge Curve rule (the slide that reveals during travel) plus coordinated scale/panel-slide tweens. A staggered wordmark part pop, or a phrase append, uses the Spring-Pop Entrance rule plus the Dynamic Content Sequencing rule.

**Camera modifier:** most variants are fully camera-locked, since the in-place token swap and most Benefits/Hook-flash/CTA variants have the swap as the only motion. When a camera move is used (Problem, Brand Outro): a slow continuous global zoom-in running underneath the whole sequence uses the Multi-Phase Camera rule's push phase, giving parallax between the fixed type and a moving background field. A camera dolly/zoom forward through an oversized glyph as a beat transition-out (Hook escalation, Product Intro push-through) uses the Coordinate Target Zoom rule or the Multi-Phase Camera rule's push. A slow push-in over a glowing motif in Scene 1 (Hook escalation) uses the same two rules. A slow continuous scene scale-up running under hard-cut beats (Hook triptych) is a push-in feel rendered as element scale on the scene group, via the Multi-Phase Camera rule or a plain scale tween — never a real dolly.

#### Logo Assemble → Lockup

**Intent:** a brand mark/wordmark comes to exist on screen and resolves into a centered logo lockup — built from parts (elements assemble or orbit in, letters cascade, an outline draws on, or a camera pushes through negative space), spring-BLOOMED whole from zero on a cleared stage, MORPHED in one unbroken chain out of the preceding phrase/glyph, absorbed from a kinetic streak, or already assembled and settling as decorations clear — optionally extended into a final URL/CTA/end card.

**Roles served:** Product Intro — a wordless, premium brand STING: an abstract system of elements pulses/grows/orbits and assembles around a fixed central logo, carried by one cinematic camera tilt; no copy, no UI. CTA — the logo build is a lead-in to the final ask: a 3D mark assembles plus a wordmark cascades, then a fast camera push-through the mark's negative space streaks giant CTA letters past the lens and resolves on a URL/CTA-verb lockup. CTA — the "draws-its-own-outline then wordmark-builds-letter-by-letter" sub-shape: a CTA button pill strokes its own glowing border, a diagonal-band wipe flips the frame, and the wordmark types in beside a slash to land the lockup, camera static. Brand Outro — the closing mark: a formation of feature pills/UI elements CLEARS the stage off all four edges, then on the empty frame the logo mark draws itself on stroke by stroke and the wordmark reveals to complete the lockup, then fades out. Product Intro — a context-then-focus reveal: a companion tagline types out to set context, the hero mark pops in beside it, then the companion exits as the layout recenters and the camera pushes IN to a held close-up on the mark. Product Intro — the literal parts build: icon parts (a glowing dot tracing a circle, semi-circles scaling up and overlapping, strokes rotating in) converge into the brand icon center-frame, the wordmark joins, then a payoff beat (a stepped subtitle rail, a count-up stat, or a scale-down into a product UI window). CTA — the text-clear bloom: centered serif tagline beats hold, then clear themselves to a blank frame, the brand mark spring-blooms from zero at dead center, slides left as the wordmark reveals to its right, and the balanced lockup holds. Brand Outro — the morph chain: a centered phrase mutates in place, collapses/swaps into an intermediate glyph whose line panels fan-and-flip around a central pivot with visible motion blur, interlocking into the geometric mark, which slides apart into the lockup; one unbroken chain, never a cut-and-replace assembly, the finished lockup holding dead static for the final 40–50% of runtime. Brand Outro — the parts-arrive build: a hand-off line holds and departs, then the mark is BUILT from arriving parts (an icon drops in, letters slide in one by one, terminal punctuation lands, a confetti burst pops and instantly shrinks) or a pixel stack streaks into full-width multicolor stripes whose tail retracts and is absorbed into the pixel mark. Brand Outro — the null-assembly boundary: the lockup is on stage from frame one, satellite shapes drift outward and fade, an accent underline sweeps beneath the wordmark, and a tagline wipes in to complete it — settle-and-reveal, no predecessor beat, no morph, no relay.

**Duration:** ~4.4–11.0s (Brand Outro ~4.4–7.3s; the brand-reveal variant ~5s; the CTA text-clear bloom 6.0–8.9s; Product Intro ~7s for the orbit sting, 7.0–9.8s for the parts-assembly variant; CTA push/build 5.4–11.0s).

**Shot structure — Scene 1 (clear/ignite, 0.0–~1.0s), the stage is prepared for the mark to build into.** By variant: Product Intro opens on a clean light background with faint concentric guide rings pulsing and expanding from center, mid-beat crossfading to a dark gradient as seed dots appear along the rings and the central logo mark's glow ignites (the mark is present from t=0, fixed, front-facing). CTA-push has the logo mark settling in object space on a background gradient, with thin wireframe edge-guides and a faint bracket motif behind center, a very slow continuous camera push already creeping. CTA-button-build has a rounded CTA-button pill rise/scale into center on a dark grid background, its thin border drawing on as an animated glowing outline stroke with a small accent comet/spark icon at its left edge. Brand Outro has a pre-arranged formation of feature pills/element grid disperse — elements sliding outward from their laid-out positions and flying off all four frame edges — emptying onto a clean background. Product-Intro parts-assembly optionally opens with a "Meet [product]" text hook wiping away, or straight into the build, with the first icon parts arriving (a glowing dot tracing a clockwise circle, a gradient semi-circle scaling up inside it, or the mark scaling-up-with-rotate into center). CTA text-clear-bloom has a centered serif tagline/question finish a left-to-right word-staggered reveal and hold, then CLEAR — text exiting via shrink-toward-center-and-fade or word-by-word left-first fade-out, leaving a blank frame for a beat. Brand-Outro morph-chain has a centered phrase complete or mutate in place (a vertical slot-machine word swap, or word-by-word landing) and hold — nothing clears, the phrase IS the raw material for the mark. Brand-Outro parts-arrive has a centered hand-off line hold on a flat canvas, then exit (sliding down off-frame with fade, or fading behind the incoming flourish). Brand-Outro settled-reveal has the lockup already centered at t=0, with satellite shapes drifting slowly outward around it — an inverted clear where the decorations leave and the mark stays.

**Scene 2 (assemble the mark, ~1.0s to ~Ys):** the mark builds itself from parts. Product Intro: seed dots scale up into flat accent shapes arranged on the rings, concentric bands ripple outward, shapes begin to orbit/drift around the still-fixed center. CTA-push: the wordmark cascades out from behind the mark (letters left to right with overshoot) into the full brand lockup, the 3D mark assembling in beats (a terminal detaching and popping as a spring dot, a part hinge-opening-and-snapping-shut elastic); optional beats include a cursor arcing in to "click" the wordmark, or a frosted-glass pill holding an intermediate CTA line springing in while layered mark shells fan to the edges. CTA-button-build: a graphic wipe flips the frame to a contrast background — a thin accent diagonal line sweeps in, swells into a full-frame diagonal band, then collapses to a small accent slash. Brand Outro: on the now-clear frame, the logo mark draws on via stroke (built arc by arc/segment by segment). Product-Intro parts-assembly: the overlapping parts complete the brand icon (a second circle overlapping to close the orb, strokes interlocking), the wordmark sliding out from behind the icon or in from its right, an optional small badge pill popping onto the lockup. CTA text-clear-bloom: on the blank frame the brand mark scales up from zero at dead center with a snappy spring ease (slight overshoot, a hint of rotation as it grows) — the whole mark at once, no parts. Brand-Outro morph-chain: the phrase collapses/wipes horizontally into the mark, or is instantly swapped at the same center for a line-art intermediate icon whose strokes split into panels that fan-and-flip around a central pivot with visible motion blur, interlock-settling into the geometric mark — never a cut to the finished logo, the transformation staying unbroken. Brand-Outro parts-arrive: the mark is built from arriving parts (an icon dropping in from above, letters sliding in one by one, terminal punctuation landing, a tiny confetti burst popping and instantly shrinking), or a colored pixel stack pops in at a text edge, shoots horizontally stretching into full-width multicolor stripes, then the stripe tail retracts and is absorbed into the pixel mark. Brand-Outro settled-reveal: an accent underline sweeps left to right beneath the wordmark — the only "build" this variant performs.

**Scene 3 (resolve to lockup, ~Ys–end):** the lockup completes and holds (Product Intro/Brand Outro) or is flown into/extended to a CTA (CTA variants). The Product-Intro orbit sting's one camera move has the whole system smoothly TILT from flat top-down into an angled isometric perspective with a slight zoom-out — flat shapes become luminous 3D forms, bands become glowing orbit lines, while the central logo mark does NOT tilt (stays 2D, front-facing, fixed); the camera eases to a stop, elements keep orbiting/drifting continuously (inner faster than outer). The CTA-push signature move fires a single fast camera push-through the mark's negative space or through a glass pill — heavy horizontal motion blur, giant CTA letters streaking past the lens (the cursor drops out) — resolving to the final lockup on a saturated background, a url badge/CTA line revealed by a left-to-right wipe with an accent leading edge, solid mark-shapes parallax-sliding in behind, settling to a dead-static hold. CTA-button-build has the wordmark build letter by letter to the right of the slash, landing on the final lockup centered on the new background, slow-settling to static. Brand Outro has the wordmark reveal beside the drawn mark to complete the lockup, which holds then fades to black/background. Product-Intro parts-assembly's payoff beat has the finished lockup hold while a bottom subtitle box steps through tagline fragments, or a big count-up stat lands over a faint background asset grid, or the lockup scales-down/fades and a product UI window scales up. CTA text-clear-bloom has the mark slide a short distance left while the wordmark reveals to its right, the balanced lockup centering and holding with one member continuing an almost imperceptible slow scale-up through the hold. Brand-Outro morph-chain has the mark slide left as the wordmark is pulled out rightward trailing a motion-blur streak, the pair decelerating into the centered lockup, holding LONG — dead static for the final 40–50% of runtime. Brand-Outro parts-arrive has the lockup rest centered and hold, or the full end card complete (a rounded-square icon tile scaling up behind the mark, the title fading in word by word, a bottom row of URL pill plus store badges fading/sliding up), holding static. Brand-Outro settled-reveal has the tagline reveal left to right below the wordmark as the satellites finish drifting out and fade, the lockup holding centered (at most a very slow global zoom-out, no pan).

**Motion vocabulary:** ring pulse/expand; background crossfade; glow ignite; seed-dot scale-up; continuous orbit/drift (inner faster than outer); a single 3D perspective tilt plus a slight zoom-out around a fixed 2D anchor; 3D logo assembly (part detach plus spring dot, hinge open/snap, shell fan-out); a wordmark cascade with overshoot; a button pill rise/scale-in; an animated stroke-outline draw plus glow; a comet/spark accent; a diagonal-band wipe; a letter-by-letter wordmark build; a pre-formed grid disperse off all four edges; a logo-mark stroke-draw; a fast camera push-through with motion blur; a continuous slow push-in/push-out; a cursor arc-in plus click; a parallax shape slide-in; a left-to-right url/badge wipe with a glowing leading edge; a static/fade-out end-lockup hold; an optional idle breathe on the held mark; a glowing-dot circular path trace; a part-overlap icon completion; a scale-up-with-rotate mark entrance; a wordmark slide-out-from-behind-icon; a badge pill pop onto the lockup; a stepped subtitle swap-in-place; a count-up stat tick over a faint asset grid; a lockup shrink/fade into a UI-window payoff; a word-by-word staggered fade-through-grey; a rolling word-by-word line swap; a shrink-toward-center-and-fade clearing exit; a whole-mark spring bloom from zero; a near-imperceptible continuous scale-up through the hold; a vertical slot-machine word swap; a horizontal phrase collapse/wipe into the mark; an instant same-center text-to-icon swap; a line-panel fan-and-flip morph around a central pivot with motion blur; an interlock-settle into the geometric mark; a wordmark pull-out trailing a motion-blur streak; a lead-line slide-down-off-bottom exit; an icon drop-in from above; a sequential per-letter slide-in plus terminal punctuation landing; a confetti burst pop-then-instant-shrink; a pixel-stack pop at a text edge; a horizontal streak-stretch into full-width stripes; a stripe-tail retraction absorbed into the mark; a rounded-tile scale-up enclosing the mark; a bottom metadata row fade/slide-up; satellite shapes outward drift plus fade; a left-to-right underline sweep; a left-to-right tagline wipe-in.

**Rule mapping:** ring pulse/expand from center uses the Center-Outward Expansion rule. Background crossfade, glow ignite, and seed-dot scale-up use plain tweens plus the ASR Keyword Glow rule (glow) and the Spring-Pop Entrance rule (dot pop-in) respectively (or the Scale-Swap Transition rule if dots morph into shapes). Continuous orbit/drift around a fixed center uses the Orbit 3D Entry rule. The single 3D perspective tilt plus zoom-out uses the Multi-Phase Camera rule for the zoom-out, with the flat-to-isometric plane tilt itself approximated via the CSS 3D Transforms technique (animating the stage's `rotateX` — see the camera modifier below); the fixed 2D anchor logo amid the moving universe needs no motion rule at all, since its stillness is intentional. 3D logo assembly's part-detach-plus-spring-dot uses the Spring-Pop Entrance rule; its hinge-open/snap uses the Hacker Flip 3D Reveal rule's 3D-rotate axis plus the CSS 3D Transforms technique; its shell fan-out uses the Center-Outward Expansion rule. A wordmark cascade with overshoot uses a plain staggered slide plus the Spring-Pop Entrance rule's overshoot per letter. A button pill rise/scale-in uses the Spring-Pop Entrance rule (or the Scale-Swap Transition rule). An animated stroke-outline draw plus glow on the button border uses the SVG Path Draw rule plus the ASR Keyword Glow rule. A comet/spark accent on the button uses the ASR Keyword Glow rule for the glow, with the motion path from the GSAP MotionPathPlugin technique described earlier in this document. A diagonal-band wipe uses the Clip-Path Reveal Masks technique (an animated polygon diagonal, grown then shrunk for the swell-then-collapse-to-slash). Letter-by-letter wordmark build uses the Discrete Text Sequence rule plus a plain typewriter recipe. A pre-formed grid disperse off all four edges is treated as transition-handled (an exit belongs to the composition's own scene-to-scene transition machinery, not an in-scene motion rule) or, if staged as an in-scene reveal-the-mark clear, reuses the Center-Outward Expansion rule's machinery run OUTWARD. A logo-mark stroke-draw uses the SVG Path Draw rule's canonical multi-segment stagger draw; wordmark slide/fade reveal beside it uses the SVG Path Draw rule's brand-line-fades-in-after-stroke tail plus the Spring-Pop Entrance rule for the slide. A fast camera push-through with motion blur uses the Multi-Phase Camera rule (a hard push phase) plus the Motion-Blur Streak rule for the heavy directional smear. Continuous slow push-in/push-out uses the Multi-Phase Camera rule's phase scale plus drift. A cursor arc-in plus click on the wordmark uses the Cursor-Click Ripple rule, with the arc path from the MotionPathPlugin technique. A parallax shape slide-in behind the lockup uses the Depth Scatter Assemble rule's parallax depth slide-in (pair with the 3D Text Depth Layers rule for depth ordering). A left-to-right url/badge wipe with a glowing leading edge uses the Clip-Path Reveal Masks technique plus the ASR Keyword Glow rule for the glowing edge. A static/fade-out end-lockup hold needs no motion rule (a terminal hold/opacity fade). An optional idle breathe on the held mark uses the Sine Wave Loop rule. A glowing-dot circular path trace uses the SVG Path Draw rule (the traced circle) plus the MotionPathPlugin technique for the leading dot riding the tip. Part-overlap icon completion and a scale-up-with-rotate mark entrance use the Spring-Pop Entrance rule. A wordmark sliding out from behind the icon is a plain x-slide under a clip/overflow mask (Clip-Path Reveal Masks technique), z-ordered under the icon. A badge pill pop onto the lockup uses the Spring-Pop Entrance rule. A stepped subtitle swap-in-place uses the Discrete Text Sequence rule, its windows derived via the Dynamic Content Sequencing rule. A count-up stat tick over a faint asset grid uses the Counting with Dynamic Scale rule (the grid is a plain opacity fade). A lockup shrink/fade into a UI-window payoff uses the Scale-Swap Transition rule (the exit cluster shrinks and fades at center, the window pops in with overshoot). Word-by-word staggered fade-through-grey (a deliberately quiet fade register, NOT the Waterfall Entry rule's binary-arrival doctrine) is a plain per-word staggered opacity/color tween; a rolling word-by-word line swap is two overlapping staggers at the same position. A shrink-toward-center-and-fade clearing exit uses the Scale-Swap Transition rule's exit half (the entrance half is the bloom). A whole-mark spring bloom from zero uses the Spring-Pop Entrance rule (a single hero, overshoot, a slight rotation from-value). A near-imperceptible continuous scale-up through a hold needs no rule (one long linear micro-tween — intentional life-in-the-hold). A vertical slot-machine word swap uses the Vertical Spring Ticker rule. A horizontal phrase collapse/wipe into the mark uses the Scale-Swap Transition rule with the collapse via the Clip-Path Reveal Masks technique. An instant same-center text-to-icon swap needs no rule (a hard `tl.set` swap — the chain's continuity lives in the next beat's morph). A line-panel fan-and-flip morph uses the Hacker Flip 3D Reveal rule's per-panel 3D rotation axis plus the Motion-Blur Streak rule plus the CSS 3D Transforms technique (a true stroke-interpolation glyph morph would need a dedicated shape-morph capability beyond this library — reach for that if panels can't sell it). An interlock-settle into the geometric mark uses the Center-Outward Expansion rule's machinery run INWARD. A wordmark pull-out trailing a motion-blur streak uses the Motion-Blur Streak rule's echo/ghost-trail form on the x-slide. A lead-line slide-down-off-bottom exit follows the same in-scene-clearing doctrine as the grid-disperse row above. An icon drop-in from above uses the Spring-Pop Entrance rule (a y-offset from-value, overshoot on landing). Sequential per-letter slide-in plus terminal punctuation landing uses the Waterfall Entry rule (the punctuation as the cascade's final, heaviest beat). A confetti burst pop-then-instant-shrink uses the Press-Release Spring rule's release-burst variation for a small deterministic burst, or the Particle Burst rule for a true multi-particle confetti field. A pixel-stack pop at a text edge uses the Spring-Pop Entrance rule (tight stagger down the stack). A horizontal streak-stretch into full-width stripes uses a plain `scaleX` stretch plus the Motion-Blur Streak rule for the streak read. A stripe-tail retraction absorbed into the mark uses the Clip-Path Reveal Masks technique run in reverse. A rounded-tile scale-up enclosing the mark uses the Spring-Pop Entrance rule (scale-in BEHIND the mark; z-order only, the mark never moves). A bottom metadata row fade/slide-up uses the Spring-Pop Entrance rule's staggered-group form. Satellite shapes outward drift plus fade use the Center-Outward Expansion rule run OUTWARD (drift targets past the frame edge) plus an opacity tail, seeded with the Sine Wave Loop rule if the drift must idle first. A left-to-right underline sweep uses the CSS Marker Patterns rule's highlight sweep re-skinned as an underline, or the Stat Bars & Fills rule's progress-fill `scaleX` form. A left-to-right tagline wipe-in reuses the url/badge-wipe mapping above (the Clip-Path Reveal Masks technique).

**Camera modifier:** the CTA push-through (the CTA spine) uses a scripted hard zoom phase on a scene-wrapping camera via the Multi-Phase Camera rule ("Steady push"/"Bookend pull" pattern; the push phase is the climax); when the mark is off-center and the camera must fly through a specific point of negative space, combine with the Coordinate Target Zoom rule so the target negative-space point lands at viewport center as scale ramps. The signature heavy horizontal motion blur on the streak uses the Motion-Blur Streak rule's directional velocity blur on the push. The Product-Intro tilt (the one cinematic move) is a single scripted camera beat — a scale phase plus drift via the Multi-Phase Camera rule for the zoom-out, with the perspective-plane rotateX (flat top-down to angled isometric) of the whole stage approximated via the CSS 3D Transforms technique, since the Multi-Phase Camera rule is scale-plus-translate-plus-drift only. The parts-assembly, text-clear-bloom, morph-chain, parts-arrive, and settled-reveal variants are all COMPLETELY static-frame (element-level motion only; settled-reveal tolerates at most a very slow global zoom-out) — the camera modifier applies only to the CTA push and the Product-Intro tilt.

#### Overwhelm / Close-In

**Intent:** convey overwhelm by accumulation. Recognizable subjects assemble, density markers scatter in to amplify "look how much," then the central subject morphs into the viewer's own avatar and elements close in from ALL sides — the frame feels surrounded, not zoomed-into. The emotional arc is recognition → claustrophobia.

**Roles served:** Problem — when the problem beat must first show "too many tools/too much surface area" and then put the viewer INSIDE it — a literal swap of subject (product → person) followed by a closing-in that feels invasive; reach for it when the pain is "you're buried," not "this metric is bad" (that's the Data-Viz Count-Up blueprint above). Problem — when the overwhelm is a WORKSPACE, not a tool count: live windows, stickies, and alert toasts pile up until the frame is chaotically full, and the beat resolves not by closing in but by shoving the clutter aside and asking the question; reach for this variant when the pain lands on words ("how can you X… when you spend months on Y?"), not on a surrounded avatar.

**Duration:** 6–9s (the clutter-shove-to-question variant runs ~10s).

**Shot structure:** a background canvas; recognizable surfaces assemble first, the viewer's avatar is revealed underneath, then a radial crowd closes in.

- **Scene 1 (0.0–~1.6s) — recognizable assembly.** Three product mockups/surfaces assemble into something the viewer knows — a staggered scale-in, the center one full-size, the two flanks smaller (~0.86×). Each rides a low-amplitude float so they feel like live context, not a static collage. Camera static.
- **Scene 2 (~1.6–3.0s) — density amplifies.** Platform icons/logos scatter in around the mockups, staggered, used purely as density markers — "look how much surface area," not animated dials.
- **Scene 3 (~3.0–4.6s) — the morph (signature move).** The CENTER mockup MORPHS — its content fades out, the container reshapes, and the viewer's avatar is revealed underneath, a literal subject swap from product to person.
- **Scene 4 (~4.6s–end) — close-in.** Task bubbles/demands close in from ALL sides toward the avatar in a radial staggered entry. The avatar stays put while the bubbles invade — the claustrophobia comes from being surrounded, never from a camera push. Holds on the crowded state.

**Variant — clutter-shove-to-question** (replaces Scenes 3–4 and inverts the camera contract): accumulation runs under a slow steady zoom-out — sticky notes bounce in springy, dashboard/editor windows pop and slide up, a stack of alert toasts slides in at one edge, inner content keeps typing/log-scrolling as live density, windows overlapping until the frame is chaotically full. The camera then reverses into a quick push-in that shoves the clutter to the frame edges, opening central negative space where a two-part serif question builds word by word (line 1 swaps in place to line 2); a cursor glides in from off-frame and comes to rest under the text; a very slow forward creep and hold.

**Motion vocabulary:** staggered scale-in assembly; resting-scale-preserving low float; density-marker icon scatter; a content-fade → container-reshape → reveal-anchor-beneath morph; a radial close-in entry from all compass points; a held crowded end-state. Clutter-shove variant additions: a slow steady zoom-out under accumulation; a reverse quick push-in; clutter shoved to the frame edges opening center negative space; continuous live typing/log scroll inside windows as ambient density; a toast-stack slide-in; a word-by-word serif build with an in-place line swap; a cursor glide-to-rest; a very slow forward creep plus hold.

**Rule mapping:** staggered mockup and icon entries (settling smoothly onto their resting scale) use the Spring-Pop Entrance rule's smooth-settle register backed by a plain stagger recipe. Platform icons as density markers (positions pre-baked, scale/opacity only — NOT internal-parts animation) use the SVG Icon Enrichment rule's DOM contract only. The center-mockup-to-avatar morph (which must drive the reshape on `scaleX`/`scaleY` since width/height tweens are forbidden, anchoring the avatar layer beneath) uses the Card Morph Anchor rule. The radial bubble close-in (positions baked once via trig, staggered entry) uses a plain radial-layout stagger plus the Spring-Pop Entrance rule for each bubble's arrival. Low-amplitude float on background mockups/icons uses the Sine Wave Loop rule's low-amplitude register — subtle jitter that composes onto each element's resting scale, never a `fromTo` yoyo that re-tweens to its start. In the clutter-shove variant, the zoom-out-under-accumulation then quick-push-in then slow-forward-creep sequence uses the Multi-Phase Camera rule (pull-back/push/drift as sequential phases on one world wrapper, with counter-translate math from the Viewport Change rule). Clutter shoved to the edges as the push-in lands uses the Center-Outward Expansion rule (outward vectors to edge resting positions), fired at the same timeline position as the camera push so the shove reads as CAUSED by it — the same causal-linkage register as the Reactive Displacement rule. A word-by-word serif question build uses a plain staggered word reveal; the in-place line-1-to-line-2 swap uses the Discrete Text Sequence rule. Live typing inside windows uses a plain typewriter recipe; the continuous inner log-scroll uses a masked, looping content translateY. A cursor glide-in coming to rest uses the Cursor-Click Ripple rule's approach portion only, with no click.

**Camera modifier:** camera-static by default — the close-in must read as the world crowding the subject, so the frame holds; a push-in would convert "surrounded" into "zoomed-into" and kill the claustrophobia. The clutter-shove-to-question variant is the sanctioned exception: there the camera IS the storyteller (zoom-out then push-in via the Multi-Phase Camera rule), and the claustrophobia comes from accumulation, not surround — never mix the two resolutions in one shot.

#### Panel Edit, Live Sync

**Intent:** a bipartite stage — an inspector/editor panel bound to a target surface — where a cursor (or text caret) continuously manipulates a control (a value scrub, a unit/codegen dropdown pick, a knob or easing-handle drag, an inline retype) and the coupled surface updates LIVE, in the same beat: the page button rotates as the value scrubs, preview icons resize per keystroke, the hex readout mirrors every hover, the code block converts on the pick. The motion IS the causality — one gesture, two surfaces changing in the same frame. The camera's job is co-visibility of the couple, not a chase.

**Three sync modes, folded from the same shape:** write-sync (control → target) is the anchor mode — a visual-editor panel scrubs rotation/margin/padding while the live page button rotates and shifts in the same beat, plus unit and font-weight dropdown picks; an inline class-name retype in a glowing code callout resizes preview icons per keystroke; a motion editor drags a knob along a dotted motion path and bends easing handles into an S-curve, paying off with a big zoom-out where the finished toggle PERFORMS the edited ease (a deferred payoff). Read-sync (target → panel mirror) has clicking a page button pop a toolbar, a "Copy code" pick filling a code editor with the element's CSS under one continuous slow zoom-out; or hovering palette swatches live-updating a footer hex readout while the grid scrolls. Self-conversion (panel is both control and target) has a unit dropdown snap-convert values in place inside a 3D-tilted spacing panel, or a codegen dropdown pick crossfading the code block into a new language under a rapid punch-in.

**Roles served:** Key Feature — one capability demonstrated as 2–4 edit beats on a single bound element, each beat a continuous manipulation the coupled surface answers in real time, resolving on the last edit held, a zoom-out to the finished product performing the edit, or a callout landing on the result. Reach for this shape specifically when the feature itself IS live editing/inspection — "change this, watch it change" — not a click-through workflow (that's the Cursor-UI-Demo blueprint above).

**Duration:** 5.3–11.9s (read-sync hover demos are shortest at ~5.3s; multi-beat scrub/edit runs span 8.7–11.9s).

**Shot structure:** a target surface (a webpage, design canvas, or IDE-plus-live-preview) sharing the frame with a bound panel (a floating inspector, a docked code panel, or a timeline-plus-easing editor); a cursor or caret is the actor; every beat pairs ONE manipulation gesture with a SIMULTANEOUS response on the coupled surface; selection chrome declares which element is bound; the camera ranges from locked to active but never loses the couple.

- **Scene 0 (optional, 0.0–2.0s) — capability title card.** A solid dark card; a single white line names the capability, fading/drifting in, holding, then a hard cut or a fast motion-blurred zoom-out that settles the stage.
- **Scene 1 (~1–3s) — the couple establishes.** The target surface arrives with the bound panel docked, floating in a subtle 3D tilt, or SLIDING IN from an edge. Selection chrome pops on to declare the binding (a bounding box with corner handles, red dashed inspection guides, sequentially popping redline measurement chips, or a green class-name header). The cursor enters and glides to the first control.
- **Scene 2..N (~2s each) — edit beats, gesture plus mirror in the same frame (the engine).** Each beat is ONE continuous manipulation and its live answer. Write-sync: the cursor click-and-drags a numeric field (the value counting up/down) while the target rotates/shifts/stretches in real time, or drags a knob along a dotted motion path (or an easing handle bending the curve with a coords readout updating), or a caret inline-retypes a value inside a glowing magnifier callout while preview elements resize per keystroke; a flash tooltip may name the gesture. Read-sync: the cursor clicks/hovers the target element, a floating toolbar springs up above it, a menu pick fires (an icon flipping to a green checkmark) and the code editor fills with streaming CSS; or hovered swatches outline and a footer hex updates instantly per hover as the grid scrolls. Self-conversion: the cursor clicks a unit/codegen dropdown, it opens with hover-highlighted rows plus a checkmark, and on the pick the readout SNAP-CONVERTS in place or the whole code block crossfades to the new language with a heading flip. Per beat, the camera stays LOCKED wide holding both surfaces, or punches in to the acting surface — but during a write-sync edit both gesture and mirror stay co-visible, since a push-in must never crop the preview out.
- **Scene N (final beat to end) — the edit proves out, hold.** Resolution diverges: the last edit simply holds (never ending on a tooltip with the dropdown unopened); a payoff zoom-out reveals the finished product performing the edited parameter (a toggle sliding with the new ease inside a full phone mockup, confetti drifting, or a pull-back returning to the identical opening framing while a terminal appends a log line); or a large arrow callout slides in pointing at the result, or the export menu rests open under the cursor, the frame drifting subtly outward.

**Signature move:** the live-sync couple — a scrubbed/typed/dragged control and its bound surface changing simultaneously, in-frame together, every edit beat.

**Motion vocabulary:** click-and-drag value scrubbing with live target sync; per-keystroke live preview resize; an inline retype with backspace and a blinking caret; instant value snap-conversion; a live hex/readout mirror on hover; a unit/codegen dropdown with hover-highlight rows and a checkmark, instant open/close; a font-weight/dropdown row pick; a knob drag along a dotted motion path with waypoints; an easing-handle drag bending the curve with a coords readout updating; a playhead scrub; sequentially popping redline measurement chips; a bounding box with corner handles; red dashed inspection guides; a floating toolbar springing up above the selected element; a code panel sliding in from an edge; an in-panel scroll to a new section; a swatch-grid scroll; syntax-highlighted code streaming/pasting in; a code crossfade with a heading flip; a glowing magnifier callout over a code token; an icon flipping to a green success checkmark; a flash tooltip naming the gesture; a grab-cursor drag; a dark title-card prelude plus a hard cut; a fast motion-blurred zoom-out settle; ONE continuous slow zoom-out spanning a demo shot; an eased push-in → hold → eased pull-back roundtrip; a quick punch-in to a panel/timeline/code; subtle 3D tilt drift/parallax on a floating panel; a big zoom-out to the product payoff; a result element re-animating with the edited ease; confetti drift; a terminal log append; a large arrow callout slide-in; a static hold.

**Rule mapping:** the cursor gliding to a control and pressing, with click feedback, uses the Cursor-Click Ripple rule. Cursor state flips (pointer↔grab over a scrubbable field or draggable handle) use the Context-Sensitive Cursor rule. A scrubbed numeric readout counting up/down under the drag uses the Counting with Dynamic Scale rule. The live-sync couple itself — a control gesture driving a second element's property in the same beat — uses the Control-Target Sync rule (concurrent tweens at the SAME timeline position, readout tween and target-transform tween sharing one label). Inline retypes with backspace, typos, or keystroke thresholds use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule for the caret blink. Per-keystroke preview resize composes the Discrete Text Sequence rule's keystroke state thresholds with the Control-Target Sync rule's coupled scale steps. Instant value snap-conversion, hex readout swaps, heading flips, and status text all use the Discrete Text Sequence rule. Syntax-highlighted code streaming/pasting in, and terminal log appends, use the Discrete Text Sequence rule's bulk-additions form. Dropdowns/menus popping open, a floating toolbar springing up, a tooltip flash, and staggered redline chips popping all use the Spring-Pop Entrance rule. Dropdown row hover-highlight stepping and pick sequencing, or which edit beat shows what, uses the Dynamic Content Sequencing rule. Dashed inspection guides/selection outline draw-on, and a dotted motion path with waypoints, use the SVG Path Draw rule. Knob travel along the motion path is a path-following technique beyond this document's core rule set (a keyframe/motion-path specialist capability); an easing-handle drag bending the curve is a true SVG path morph, similarly beyond this rule library's scope (the SVG Path Draw rule only draws strokes, it cannot morph a path) — its coords readout beside it still uses the Discrete Text Sequence rule. A glowing magnifier callout over a code token composes the Ambient Glow Bloom rule (the glow) with the Spring-Pop Entrance rule (the callout pop). A code panel sliding in from an edge, or docking, uses the Card Morph Anchor rule or the Scale-Swap Transition rule. In-panel scroll and swatch-grid scroll use a plain masked internal translate, or the 3D Page Scroll rule on a tilted panel. Subtle 3D tilt drift/parallax on the floating panel, and continuous micro-drift on holds, use the Multi-Phase Camera rule's micro-drift phase. A punch-in to a panel/timeline/code and settle uses the Coordinate Target Zoom rule plus the Multi-Phase Camera rule. An eased push-in → hold → eased pull-back roundtrip (co-visibility preserved) uses the Multi-Phase Camera rule's pull-back/focus/push sequencing. ONE continuous slow zoom-out spanning the demo shot, and a big zoom-out to the product payoff, use the Viewport Change rule's single composite transform. A fast motion-blurred zoom-out settle transition composes the Motion-Blur Streak rule with the Viewport Change rule. A result element re-animating with the edited ease (a toggle sliding with the new S-curve) is a plain custom-ease tween on the payoff element. Confetti drift on the payoff uses the Particle Burst rule plus the Sine Wave Loop rule for bounded drift. A large arrow callout slide-in plus hold is a plain single slide tween. A dark title-card prelude belongs to the Titlecard Reveal blueprint's territory for its own drift/fade, though the fade/drift itself is a plain tween here. Hard cuts between title and demo, and the final static hold, need no rule.

**Camera modifier:** the camera law is the INVERSE of the Cursor-UI-Demo blueprint's chase — it serves co-visibility of the couple. Three attested postures: (1) LOCKED — a fixed framing for the whole demo, panel plus target both in frame, all motion element-level; (2) ONE CONTINUOUS MOVE — a single slow zoom-out (or drift) spanning the entire demo shot while edits fire inside it, via the Viewport Change rule; (3) PUNCH-AND-RETURN — an eased push-in onto the acting surface, a tight hold through the edit, an eased pull-back to the identical opening framing, via the Multi-Phase Camera rule plus the Coordinate Target Zoom rule — with the hard constraint that during a write-sync edit the mirror surface is never cropped out. If the camera is chasing the cursor target-to-target with per-beat state swaps, that's the Cursor-UI-Demo blueprint instead, not this one.

#### Prompt, Type, Submit, Generate

**Intent:** the AI-era demo shot — a prompt/query/command types character by character into a REAL product input (a chat composer, search bar, terminal prompt, URL bar, or sidebar assistant) and the machine answers: status theater into a streaming answer, an agent action log, diff cards, a chart, or a generated artifact — or the clip cuts at the submit and the ask itself is the show. The keyboard is the actor and the product is the responder. Distinct from the Typewriter Reveal blueprint below (a line typed as bare typography on an empty field, no product surface, nothing answers) and from the Cursor-UI-Demo blueprint above (a cursor clicking a reconstructed UI through states — there the pointer drives every change; here any cursor work only primes the input or lands the submit, and every state change after that is the machine's own doing).

**Roles served:** Hook — the opener is "watch me ask": a typed headline beat, ONE eased push-in landing tight on the product's input, the prompt typing and the clip ending at or just after submission (sub-shape A). Hook — the demo loop ITSELF is the hook: command in, output builds and scrolls, a second command/retype starts before the cut, ending mid-action (sub-shapes B/C with the restart ending). Product Intro — the first look at the product IS its composer: a brand beat opens onto the input surface, a long prompt types with hovers/attachments/dropdown picks, and the camera steers gently toward the input or the confirming control (sub-shape A, occasionally running through to an agent-log payoff). Product Intro — the product is introduced through its search affordance: a short query types with a blinking caret, autocomplete/results populate LIVE, and a confirm click settles the result state (sub-shape C, search skin). Key Feature — the capability is demoed as ONE prompt-to-response round trip: submit into thinking/status states, then a streaming answer, action-log rows with brand icons, green diff cards, a chart drawing itself, or an instant generated-app reveal — the family's widest role. CTA — the install-command end card: the closing headline demotes (shrinks, grays, lifts) to make room for a terminal pill that springs in and stretches wide, the install command types out with a blinking cursor, flanking metadata and a tool-icon row pop in, and the finished card holds long; no submit, no response, the typed command IS the ask (sub-shape A, terminal skin).

**Duration:** 5.2–12s (a long-form family — sub-shape A prompt-as-hook spans 5.2–12s, including the ~7.4s CTA end card; sub-shape B's full generate loop spans 5.45–11.9s; sub-shape C's instant-result surface spans 5.7–11.9s; most members run 7–12s because the response needs room to arrive).

**Shot structure:** a product input on/inside a product surface (an app window, web page, terminal, or browser chrome) over a background color; the input is the gravitational center — the camera makes at most one or two purposeful moves toward or away from it and is otherwise LOCKED; typing is character by character behind a visible caret, and response content arrives progressively, never dumped. Three folded sub-shapes: (A) prompt-as-hook, where the clip ends at or just after the submit (or mid-word), the ask itself is the show; (B) full generate loop, where submit leads to status theater then the output builds block by block; (C) instant-result surface, where the machine answers with a finished surface, often re-queried before the cut.

- **Scene 0 (optional, 0.0–~2s) — lead-in beat.** ONE establishing move before the input owns the shot — a headline typing on and clearing, a title card hard-cutting away, a brand beat (a logo/mascot centered, a serif title building in word groups, the logo shrinking-and-rising to dock top-center), a glowing orb/mark forming, the app window flying in with motion blur and settling, or a full-frame thumbnail grid parting at its vertical centerline. Kept to ≤2s, since the input is the star.
- **Scene 1 (~1–3s) — the input takes focus.** The product input arrives or is primed — a pill bar expanding sideways from a mark/chip, a prompt palette/card springing in at center with a soft shadow, ONE smooth eased/accelerating push-in cropping tight onto the composer inside the app window (headline chrome sliding out of frame), a search modal springing to center while the page blurs behind it, a cursor clicking a menu row and the prompt block appearing, or a clear button emptying the previous query back to placeholder. An optional composer ritual — an attachment dragging in and settling in a tray, or a model/option dropdown opening with hover-highlighted rows and a checkmark landing — may play before or during typing.
- **Scene 2 (~2–6s) — the prompt types (the engine).** The prompt text types rapidly character by character behind a blinking caret; the input card GROWS downward/wraps as text fills, pushing footer controls down; a typed token may convert into an inline brand pill mid-typing (typing continuing around it); the camera may run ONE slow continuous push-in toward the input, decelerating to a near-hold on the typed ask. Sub-shape A may END here — cut mid-word with the caret blinking, or held on the finished prompt.
- **Scene 3 (~4–7s) — submit plus machine theater.** The submit control is clicked (a cursor glide plus press dip; the button may have MORPHED state on the first keystroke, and may flip to a stop control while streaming). The surface answers instantly with a working state — prior content vanishes (a chip grid gone, a panel collapsing to its slim header) — then the theater: status phrases cross-dissolving with a left-to-right shimmer sweep, a spinner rotating over a loading strip, a row of loading cards lining up, or a checklist populating and flipping items one by one to green checks with strikethrough while a status heading flips tense. Sub-shape A may end the clip ON the theater — "Generating…" or the rotating spinner — the flare is the button, the answer left to the imagination.
- **Scene 4 (rest) — the answer arrives.** Sub-shape B (full generate loop): the output BUILDS progressively, each block pushing content down — answer text streaming paragraph by paragraph, action-log rows popping in sequentially with a brand icon each, diff cards expanding with green-highlight added lines, chart lines drawing staggered left to right from a shared origin, an ASCII/summary table drawing in, live counters ticking, the surface auto-scrolling vertically to follow the newest line, often under ONE slow continuous push-in on the result window. Sub-shape C (instant-result surface): the machine answers with a finished surface — a matching result/article renders in place; autocomplete chips stagger-pop below the bar WHILE the query types; a hover fills the Search button solid and a click confirms; a generated page rises as a rounded card and SCROLLS continuously beneath the pinned prompt; a blur-whip resolves onto an artifact window and a tab click FLIPS code to preview; or a zoom-out reveals the prompt pill was inside a full workspace where the content rewrites itself live.
- **Scene 5 (final beat) — resolve.** Key Feature holds on the completed output with no fade-out. Product Intro has the cursor land the confirming click as the clip ends, or extras fade and a final push-in leaves the clean end state (one member hard-cuts to a minimal end card — the submit button alone at dead center with a settle pop). Hook's signature restart has a SECOND prompt start typing at a fresh prompt line, or the query backspaces-and-retypes and the output swaps wholesale to a second result — the clip ending MID-ACTION, since the loop is endless and that is the point. CTA has the end card from Scene 2 simply hold to the last frame, the blinking cursor the only motion.

**Motion vocabulary:** character-by-character typing with a blinking caret/block cursor; typed-headline beats replacing each other; an input pill growing/wrapping downward into a multi-line box; a prompt palette/card springing in; a pill bar expanding sideways from a mark or chip; an orb formation with a glowing rim; a typed token converting to an inline brand-pill mid-typing; a placeholder clear; a backspace-and-retype query swap; an attachment drag-in and tray settle; a dropdown open with row hover-highlight, checkmark select, and toolbar-label update; a chip-grid hover dance; a cursor glide/arc with hover-highlight fills; a click press dip; a submit-button state morph; a content vanish/panel collapse/layout swap on submit; status-phrase cross-dissolves with a left-to-right shimmer sweep; a pulsing "Thinking"; a spinner rotation; a loading strip; animated trailing dots; a loading model-card row; a status-heading tense flip; checklist squares flipping to green checks with strikethrough; action-log rows popping in sequentially with brand icons; streaming text blocks pushing content down; green-highlight diff cards expanding; staggered left-to-right chart line-draws; an ASCII/summary table draw-in; a count-up ticker; a vertical output scroll following the newest line; a generated page rising as a rounded card and scrolling beneath a pinned prompt; autocomplete chips rapid stagger-pop; a code/preview instant flip on a tab click; a blur-whip transition; a prompt jump to a heading on submit; a zoom-out reveal from a prompt pill to a full UI window; a single eased/accelerating push-in landing on the input; a slow continuous push-in on the result window; a window fly-in with motion blur; a zoom-plus-pan cropping browser chrome; a modal spring-in with background blur; a full-frame grid parting at the vertical centerline; a headline demotion (scale-down plus desaturate plus lift); a chip horizontal-stretch into a wide terminal pill; quiet low-contrast metadata fade-ins; sequential spring pop-ins of an icon row; a second prompt typing at the cut; an interface dim/fade at the cut; a long static end hold with a blinking cursor.

**Rule mapping:** character-by-character typing, placeholder clear, backspace-and-retype, a second prompt at the cut, and typed-headline beats all use the Discrete Text Sequence rule backed by a plain typewriter recipe. A blinking caret/block cursor persisting through holds uses the Context-Sensitive Cursor rule. Prompt/status/output phrase windows and script-driven beat durations use the Dynamic Content Sequencing rule. An input card growing downward/wrapping as text fills uses the Anchored Layout Expand rule (top-anchored downward growth, stepped at wrap boundaries). A typed token converting to an inline brand-pill mid-typing composes the Scale-Swap Transition rule (the token-to-chip swap at the conversion threshold) with the Card Morph Anchor rule (the reflow around the chip). A prompt palette/modal/dropdown springing in, and loading cards/log rows/diff cards/autocomplete chips/icon rows arriving staggered, all use the Spring-Pop Entrance rule. A pill bar expanding sideways from a mark, or a chip stretching into a wide terminal pill, uses the Card Morph Anchor rule. A cursor gliding to a control with a press and ripple uses the Cursor-Click Ripple rule; the press dip and recovery use the Press-Release Spring rule (or the Physics Press Reaction rule for a cursor-plus-button compressed together). Hover highlight fills, an instant solid fill on the Search button, and UI-keyword accents use the ASR Keyword Glow rule (a static-timeline glow variant) or the Press-Release Spring rule's color-transition variation. An attachment drag-in with the cursor uses the Context-Sensitive Cursor rule (pointer↔grab) plus the Spring-Pop Entrance rule for the tray settle. A content vanish/layout swap/panel collapse on submit, and a code/preview instant flip, use the Scale-Swap Transition rule (a paired same-center swap) or a hard state swap via the Discrete Text Sequence rule's semantics. A prompt jumping to a heading on submit is a reposition move, with the travel itself via the Nudge Curve rule's slow-fast-slow group slide. Status-phrase cross-dissolves with a shimmer sweep compose the Discrete Text Sequence rule (phrase swaps) with the Ambient Glow Bloom rule's shimmer-sweep variation (a single-pass traveling sheen clipped to the text). Spinner rotation, animated trailing dots, and pulsing loader glyphs use the SVG Icon Enrichment rule's rotating/pulsing internal SVG elements; the bounded "Thinking" pulse uses the Sine Wave Loop rule's finite repeats — this pulse PERFORMS status, it is not idle wobble. Checklist state flips, a status-heading tense flip, and status-pill swaps use the Discrete Text Sequence rule's discrete state stepping, with the checkmark stamp via the SVG Path Draw rule or the Spring-Pop Entrance rule. Streaming text blocks/log rows pushing content down compose the Dynamic Content Sequencing rule (per-block windows) with the Spring-Pop Entrance rule (per-row arrival). Vertical output scroll following the newest line is a plain content translateY keyed to the same timeline as the content windows, plus a matched Viewport Change rule counter-pan when the frame itself travels. A generated page as a rounded card with internally scrolling content uses the 3D Page Scroll rule's flat variant. Staggered chart line-draws use the SVG Path Draw rule (staggered starts). A count-up ticker/live counters use the Counting with Dynamic Scale rule; result bars/fills use the Stat Bars & Fills rule. A single eased push-in landing on the input, and a slow continuous push-in on the result, both use the Multi-Phase Camera rule (push phase) with the destination framed via the Coordinate Target Zoom rule. A zoom-out reveal from a prompt pill to a full workspace, and a zoom-plus-pan cropping chrome, use the Viewport Change rule's composite pan-plus-scale on the world wrapper. A window fly-in with motion blur, and a blur-whip transition, use the Motion-Blur Streak rule. A search modal with background blur composes the Depth-of-Field Blur rule (blurring the page plane, keeping the modal sharp) with the Spring-Pop Entrance rule. A full-frame grid parting at the vertical centerline uses the Center-Outward Expansion rule (halves gliding outward in lockstep). An orb formation with a glowing rim composes the Ambient Glow Bloom rule with the Spring-Pop Entrance rule. A headline demotion (scale-down plus desaturate plus lift) is a plain composite tween. Interface dim at the cut, a hard cut to a minimal end card, and ending mid-word/mid-scroll are exit conventions needing no rule. A long static end hold with only the caret blinking uses the Context-Sensitive Cursor rule — the blink is the sanctioned residual motion.

**Camera modifier:** the camera always serves the ask or the answer; many members are fully camera-static, since typing, submit theater, and streaming carry the shot on their own. ONE smooth eased/accelerating push-in that lands tight on the input and LOCKS (Hook, Product Intro) uses the Multi-Phase Camera rule (push) plus the Coordinate Target Zoom rule — the defining move of the "watch me ask" opener. ONE slow continuous push-in running under the typing or under the output build, decelerating to a near-hold (Product Intro, Key Feature), uses the Multi-Phase Camera rule, giving the response weight without stealing from it. ONE zoom-out reveal — the prompt pill turning out to live inside a full workspace (Key Feature, sub-shape C) — uses the Viewport Change rule's pull-back, the inverse move where the ask was closer to the product than you thought. Entry-only flourishes (a window fly-in with motion blur, a zoom-plus-pan cropping browser chrome) both settle before typing starts. Never more than two real viewport moves per shot; the frame is LOCKED during submit theater and streaming — the content scrolls, the camera does not.

#### Spatial Pan / Stations

**Intent:** pre-place a sequence of labeled stations on one oversized canvas, then traverse it with a single virtual camera — repeated lateral/diagonal pans that center each station in turn and reveal a callout at every stop, landing held on a final station.

**Roles served:** Hook — a horizontal timeline of evenly-spaced milestones, left-panned beat by beat, each marker getting a spring-popped callout, landing on the present moment ("evolution/milestone walk leading up to us"). Problem — a connected web of pain "stations" linked by hand-drawn leading lines, diagonally panned station to station, ending on a tangled scribble knot ("too many disconnected steps — it's a mess"). Product Intro — a two-shot strip bridged by ONE lateral pan: shot 1 holds a static phrase whose accent word 3D-flap-DECODES (the concept lands), then the camera pans across the strip (with background parallax) into shot 2, where a cursor drives a live typing demo — pairs this pan with the Cursor-UI-Demo blueprint's focal-locked tracked typing.

**Duration:** 7–10s (Hook 8–10s; Problem ~7s; the concept-demo variant ~7s).

**Shot structure:** one oversized flat canvas on a solid background; all stations/markers pre-placed in world space; accent-color text plus simple line-icons; one virtual camera pans ease-in-out between stops. Each station holds ~1.0s.

- **Scene 1 (0.0–~1.0s):** camera opens on station 1 — the first label/step centered. A reveal lands on it (see variants below). The camera then begins to PAN toward station 2, sliding station 1 out of frame.
- **Scene 2 through N-1 (~1.0s each):** the camera PANS (ease-in-out) to center the next station; on arrival its label (plus an optional secondary label) is REVEALED with the role's own reveal style. Repeat per station.
- **Scene N (final, ~last beat):** one last pan lands on the terminal station; the final callout/landing element reveals and HOLDS to the end. Camera goes static on the punchline.

**Variants:** the Hook variant places stations as evenly-spaced markers on a thin horizontal timeline (lower third); pans are LEFT-only along the single axis. Each callout is a bordered callout box with a downward triangle (offset drop-shadow) that SPRING-POPS up (scale 0→100%, bouncy overshoot, transform-origin at the triangle tip) reading the label; a secondary label (e.g. a year) fades in and RISES above it. Some mid markers arrive as plain static text revealed by the pan alone (no box). The final scene lands on the present-day label, springs, holds. The Problem variant has stations scattered across a 2D web; pans are DIAGONAL, STEERED by accent-color hand-drawn lines — each station has a rough write-on line/arrow that draws toward the next and the camera follows it (Scene 1 also draws a loop/circle around the headline's key word). Each station is a white line-icon above its label, revealed plainly by the pan alone (no spring box). The final scene has the accent line spiral into a dense chaotic scribble knot centered on the field, camera holding static on the tangle as the visual punchline.

**Motion vocabulary:** repeated ease-in-out camera pans (horizontal-left for Hook, diagonal-steered for Problem) across one large static canvas; pre-placed stations sliding through frame via the pan; a spring-overshoot callout pop with a triangle-tip origin (Hook); a rise-and-fade secondary label (Hook); plain labels/icons arriving via the pan alone; rough hand-drawn "write-on" leading lines/arrows plus a loop/circle key-word mark (Problem); a terminal chaotic-scribble knot draw (Problem); a static hold on the final station/punchline.

**Rule mapping:** the camera pan/traverse across the canvas (the primary mechanism) uses the Viewport Change rule's single world-wrapper transform in pan mode. Sequencing the repeated pan beats into stops uses the Multi-Phase Camera rule. Centering each station as the pan target uses the Coordinate Target Zoom rule, used purely as pan-to-target with no zoom. A spring-overshoot callout pop with a triangle-tip origin (Hook) uses the Spring-Pop Entrance rule. A rise-and-fade secondary label, plus plain per-station label/icon reveals via the pan (Hook), use the Discrete Text Sequence rule. Hand-drawn leading lines, arrows, the loop-circle key-word mark, and the terminal scribble knot (Problem) all use the SVG Path Draw rule. Station line-icons (Problem) use the SVG Icon Enrichment rule. A static hold on the final station/punchline needs no rule.

**Camera modifier:** the pan IS the camera. One world-wrapper virtual-camera transform in pan mode (the Viewport Change rule) is sequenced across stops by the Multi-Phase Camera rule, each stop targeted via the Coordinate Target Zoom rule used as pan-to-target. No depth push-in — that's what distinguishes this blueprint from the cluster-push-in and push-through-style blueprints elsewhere in this document.

#### Ticker Displace / Takeover

**Intent:** a context phrase types in, an accent word cycles through options like a slot machine to suggest "this could be many things," then a hero CRASHES in from off-screen and physically shoves the text aside — "actually, this is what it is." A collision, not a fade.

**Roles served:** Hook — when a static lead-in phrase plus a cycling accent word should be PHYSICALLY REPLACED (not cross-dissolved) by a hero arriving with momentum, and the final frame is the hero alone; reach for it when the takeover should read as an impact. Brand Outro — the same collision used as a sign-off: options cycle, the brand mark crashes in and owns the frame.

**Duration:** 5–7s.

**Shot structure:** a background canvas; one text group on the left/center that gets ejected by an incoming hero.

- **Scene 1 (0.0–~1.4s) — context build.** A typewriter lays down a lead-in phrase character by character (smooth, no typos — selling confidence, not human chaos). Camera static.
- **Scene 2 (~1.4–3.0s) — the cycling beat.** An accent word slot inside the line ticks through 2–3 options on a vertical spring-roll (each click a new word), suggesting breadth — "many things this could be." More than ~3 options reads as filler.
- **Scene 3 (~3.0–4.2s) — the collision (signature move).** A hero crashes in from off-screen with momentum and physically SHOVES the whole text group aside — the text reacts to the impact (gets displaced), it does not fade. The hero lands HEAVY — a longer settle, not a zip — so it reads as mass, not speed.
- **Scene 4 (~4.2s–end) — the hero alone.** The hero settles dead-center and reads still. Holds.

**Motion vocabulary:** a smooth character typewriter; a vertical spring-ticker word roll (2–3 steps); an off-screen hero crash-in with momentum; a reactive displacement of the struck text group; a heavy long-tail landing (not bouncy); dual-axis subtle jitter on the resting hero.

**Rule mapping:** the smooth single-phrase typewriter lead-in uses the Discrete Text Sequence rule's smooth-slice/continuous form — no typo machinery. The accent word slot-machine cycling through options uses the Vertical Spring Ticker rule (the number of steps equals the number of options the hero will replace; the rule's footer-reveal step goes unused, since Scene 3 takes its place). The hero shoving the text group aside on impact uses the Reactive Displacement rule (the text is the displaced mass; express the hero's "heavy land" as a longer `power2` settle rather than the rule's default overshoot ease). The hero's fast off-screen crash-in uses the Motion-Blur Streak rule (directional velocity blur resolving sharp as it lands). Resting-hero aliveness uses the Sine Wave Loop rule's low-amplitude dual-frequency register — scale plus rotation jitter composing onto the hero's final landed scale, never a yoyo around 1.

**Camera modifier:** camera-static — the displacement happens entirely in element space (the hero moves the text), so there is no real camera move; the impact is the only motion.

#### Title-Card / Single-Card Reveal

**Intent:** the calm breather/landing beat — one clean title or single brand/proof card revealed with exactly one restrained move (a slide-up crossfade, or a wipe-away-to-reveal), then a still hold. Low motion is the payload, not a deficiency.

**Roles served:** Benefits — a calm two-line value title card: a headline value line, then one slide-up crossfade to a qualifier/elaboration line that holds center. Social Proof — wipe a busy app-collage open away with one diagonal pill-sweep to reveal a clean brand lockup (icon plus wordmark) plus a centered "loved by [N]+ [audience] teams" social-proof line that spring-settles and holds. CTA — a monochrome end-card CHAIN: statement → CTA/availability line → brand wordmark/logo, separated by instant hard cuts at full opacity, each card its own allocated stillness, the sequence terminating on the logo held to the final frame. Product Intro — a three-beat dark title PRELUDE before any product UI: a logo pop, then a name (with a version appending grey-to-bright), then a tagline card, chained by clears and blur-snap handoffs rather than hard cuts.

**Duration:** 3–5s (Benefits 3–4s; Social Proof ~5s, observed at 4.7s). Card chains run 2–3s per card, roughly 5.5–9.5s total.

**Shot structure:**

- **Scene 1 (0.0–~0.4s):** static camera on a neutral/dark background. Establish the opening state. Benefits: empty-to-text — a benefit line is about to fade in centered, no busy open. Social Proof: a busy intro frame holds briefly, an app-screenshot/use-case collage of overlapping cards under a setup line.
- **Scene 2 (~0.4–~1.5s):** the ONE move executes — a single restrained reveal that brings the calm card to center. Benefits: the benefit line fades in centered while scaling slightly (~95%→100%, smooth ease-out) and holds. Social Proof: a large accent-color rounded pill sweeps diagonally bottom-left to top-right and exits the corner, clip-path wiping the collage away to reveal the brand logo lockup beneath as the logo icon strokes draw on.
- **Scene 3 (~1.5s–end):** the revealed/settled card holds to the end (the allocated stillness). At most one subtle live element (a slow breathing pulse on the card, or a very slow camera drift). No second development phase. Benefits: the benefit line translates up and fades out as a qualifier/elaboration line translates up from below center and fades in to take center; holds — this single slide-up crossfade IS the one move, since Benefits front-loads no Scene-2 wipe. Social Proof: the lockup — a centered logo icon, wordmark below, and a centered social-proof tagline (whose N+ may count up) — spring-settles small, then holds.

**Variant — card chain** (CTA end-card stack, or Product Intro title prelude): the single-card contract repeats 2–3 times in sequence. Each card is a complete Scene 1–3 in miniature — arrive (or simply BE there), at most one restrained move, hold — and the seams between cards are INSTANT hard cuts at full opacity (no crossfade, no fade-through-black), or, in the prelude flavor, a blur-away-then-snap-into-focus handoff. Card moves stay on budget: a character-by-character type-on with visible partial states, a right-to-left backspace that resolves the wordmark into the small logo icon, a grey-to-bright append (a name gaining a version), a blur-snap into focus, or nothing beyond a barely-perceptible continuous slow scale-up across the hold. The final card is always the brand logo/lockup, held static to the last frame.

**Motion vocabulary:** a single restrained reveal (a gentle fade-in plus subtle scale-up settle, or a diagonal clip-path pill-wipe); one slide-up crossfade between two centered lines (Benefits); icon stroke draw-on (Social Proof); an optional "N+ teams" count-up; a logo-plus-tagline spring-settle-and-hold; subtle breathing on the held card; a hold-to-end. A calm register throughout — no spring chains, no tumble, no per-beat flips, no second phase; camera static (optional very slow drift only). Card-chain register additions: an instant hard cut at full opacity as the only seam; a barely-perceptible continuous slow scale-up across each hold; a character-by-character type-on with visible partial states; a right-to-left backspace collapsing the wordmark into the logo icon; a grey-to-bright text append; a blur-away-then-snap-into-focus card handoff; a logo pop with overshoot plus glow (the prelude opener); a monochrome text-on-solid throughout.

**Rule mapping:** the gentle fade-in plus subtle scale-up settle (Benefits Scene 2) uses the Scale-Swap Transition rule's restrained in/settle. A single slide-up crossfade between two centered lines (Benefits Scene 3) uses the Discrete Text Sequence rule (one line handing off to the next via a translate-up plus crossfade). The diagonal pill-wipe reveal (Social Proof Scene 2) uses the Clip-Path Reveal Masks technique described earlier in this document. Icon stroke draw-on (Social Proof Scene 2) uses the SVG Path Draw rule. The optional "N+ teams" count-up (Social Proof Scene 3) uses the Counting with Dynamic Scale rule. The logo-plus-tagline spring-settle-and-hold (Social Proof Scene 3) uses the Spring-Pop Entrance rule's single soft settle — intentionally one beat, not a chain. Subtle breathing on the held card (the one live element during the hold) uses the Sine Wave Loop rule. Type-on/backspace/grey-to-bright-append in a card chain uses the Discrete Text Sequence rule (non-linear typing including backspace; drive the version append as a bulk addition). A wordmark's remainder resolving into the logo icon uses the Scale-Swap Transition rule (a same-center swap fired as the last character deletes). A barely-perceptible slow scale-up across a hold uses the camera-modifier drift below (the Multi-Phase Camera rule's micro-drift register) applied per-card. The blur-away-then-snap-into-focus handoff (prelude flavor) uses the Depth-of-Field Blur rule's single pull on the outgoing/incoming card. A logo pop with overshoot plus glow (prelude card 1) uses the Spring-Pop Entrance rule plus the Ambient Glow Bloom rule. An instant hard cut at full opacity needs no rule — it's a deliberately transition-free `tl.set` swap.

**Camera modifier:** optional — a single very slow drift/push under the hold only, via the Multi-Phase Camera rule. Default is fully static; do not add unless the held beat would otherwise read as a freeze-frame.

**Stillness note:** this is a legitimate allocated-stillness beat. The hold in Scene 3 is the deliverable, not an unanimated gap — do NOT manufacture a development phase, extra swaps, or forced animation. One restrained move plus a subtle hold (optionally with one breathing element or one slow drift) is the correct and complete shape. The card-chain variant does not break this — each card individually obeys the one-move-plus-hold contract, and the hard cut is a seam, not a move. Boundary: if the cards flip at sub-second tempo or each beat carries its own entrance/exit energy, you have left this blueprint — that's the Kinetic-Type Beats blueprint above (its CTA variant owns the high-tempo value-line stack).

#### Transcript-Scroll Artifact Reveal

**Intent:** the frame travels vertically along ONE long content surface — an agent transcript, a running task feed, an analysis document, a story draft — rendered full-bleed on a flat canvas (no device frame, no held mockup), by camera pan or element scroll, until ONE focal interaction — a file-chip click, a quote highlight, a collapsible-row expand — pivots the shot into an artifact/detail reveal: the deliverable behind the work.

**Roles served:** Key Feature (four folded modes: pan-to-workspace, feed-rush, document-to-artifact, selection-pivot) — the "the agent did a lot of work → here's the deliverable" grammar. The long surface is the EVIDENCE (tool pills, checked progress items, task rows, headings, comps tables, story paragraphs), read at traversal pace; the artifact is the PAYOFF (a full workspace with a live mockup, a spreadsheet with highlighted cells, an inline ask-panel, a sub-task stack). Reach for it when the feature's proof is the volume/depth of generated work and the beat should cash that in on one interaction — not a held device tour (that's the Device-Surface-Showcase blueprint above), not a cursor-chased workflow (that's the Cursor-UI-Demo blueprint above).

**Duration:** 5–11.8s (the feed-rush mode 5.4s; pan-to-workspace 5.0s; selection-pivot 9.3s; document-to-artifact 11.75s).

**Shot structure:** one long content surface (an agent chat transcript, task feed, analysis document, or story doc) sits full-bleed on a flat light canvas (warm off-white, cream, beige, or plain white — the surface's own background IS the scene background); dark text with small accent marks (green verb highlights, model-tag pills, check circles, yellow cells). Three acts: TRAVERSE → HINGE → ARTIFACT. Camera discipline is the signature — at most TWO real camera moves in the whole shot, bracketing the hinge; everything else is element motion on a static frame.

- **Scene 1 (0.0–~40–60% of runtime) — establish plus vertical traversal (the evidence).** The surface establishes with one small opener — a title typing on, a centered title shrinking ~50% and gliding to the top-left to dock as a fixed header, or the frame opening tight on a chat panel — then the traversal begins: the frame travels DOWN the content (or the content streams UP through the frame), revealing progressive work in reading order (a prompt → tool pills → checked progress items → a typed summary; tagged task rows → muted tasks → a checklist block; a heading → a paragraph → a comps table → bullets; a title → story paragraphs → dialogue). New rows may cascade in before the scroll takes over; a typed line may finish under the moving frame. Traversal texture varies by member — one continuous slow pan, a fast continuous feed rush, stepped scrolls decelerating at each stop (speed-blur between stops, content fading at frame edges), or one smooth scroll easing to a stop.
- **Scene 2 (~1–2s) — the hinge: ONE focal interaction.** The traversal settles and a single interaction pivots the shot — a file-attachment chip spring-pops in below a typed handoff line and a cursor glides in and CLICKS it; a sentence/quote gets a selection-highlight sweep and a tooltip pill spring-pops above it for the click; a collapsible row reaches the frame center and EXPANDS; or a typed verifier summary completes as the implicit trigger. This is the only interaction in the shot — the cursor (if any) appears here for the first time.
- **Scene 3 (rest) — artifact reveal plus hold.** The hinge cashes in, choosing ONE reveal mechanic: a fast smoothly-DECELERATING zoom-out re-frames the whole workspace (the panel just traversed becomes a sidebar beside a live mockup and tool panel); an artifact window (a spreadsheet) scales up from small toward full frame, then a slow push-in plus lateral pan settles on its highlighted cells; an inline panel expands below the highlighted line and a follow-up question types into it; or the row unfolds into a sub-task stack and the scroll settles on narration text. An optional coda has one cursor click instantly swap a screen inside the revealed artifact (e.g. a phone tab click). The frame locks; element motion only to the end.

**Variants:** pan-to-workspace has traversal as a REAL camera pan — opening tight on the chat panel, one single uninterrupted downward glide (never cutting away) over pills → checked list → a typing verifier summary; the hinge is the summary completing; the reveal is ONE rapid decelerating zoom-out to a three-part workspace (chat-as-sidebar, phone mockup, tweaks panel); a coda cursor click swaps the phone screen instantly — exactly two camera moves total. Feed-rush has NO camera at all — the title docks to a header, five tagged rows cascade in, then a fast continuous upward ELEMENT scroll races through muted tasks and a checklist to a collapsible row; the hinge is the row itself; the reveal is the row expanding into a six-item sub-task stack, settling on narration — fully cursorless. Document-to-artifact has traversal as a stepped ELEMENT scroll (static frame) — the document climbs in fast steps, decelerating at each stop, blur/fade between stops, clearing to a blank canvas; the hinge is a typed handoff line plus a file-chip pop plus a cursor click; the reveal is the spreadsheet window scaling up then one slow continuous push-in plus rightward pan onto yellow-highlighted forecast columns. Selection-pivot has a typed headline → a document building (a bubble prompt plus a typed title plus populating paragraphs) → one smooth upward element scroll easing to a stop; the hinge is a selection-highlight sweep plus the shot's ONE push-in framing the sentence plus a tooltip-pill click; the reveal is an inline panel expanding below the line with the referenced quote and a rapidly-typed follow-up question — camera locked at the pushed-in zoom to the end.

**Motion vocabulary:** a continuous slow downward camera pan; a fast continuous upward feed scroll; a stepped document scroll decelerating at each stop; a smooth scroll easing to a stop; speed-blur between scroll stops; content fade at frame edges; a centered title shrinking ~50% and gliding to a top-left header dock; task rows cascading in staggered; a typed line/title/follow-up question with a caret; green leading-verb highlights and model-tag pills riding past; checked-item strikethroughs riding past; a file-attachment chip spring pop-in; a tooltip pill spring pop; a chat-bubble arrival; a cursor glide-in plus click; a selection-highlight sweep across a sentence; ONE camera push-in onto the selection; a fast decelerating zoom-out to the full workspace; an artifact window scaling up from small; a slow push-in plus lateral pan settling on highlighted cells; a collapsible row expanding into a sub-task stack; an inline panel expanding below the line; a phone-screen instant swap on a coda tab click; a frame-lock hold.

**Rule mapping:** vertical traversal by ELEMENT scroll (a fast feed rush, a stepped document scroll, or a smooth scroll-to-stop) uses the 3D Page Scroll rule at effectively zero tilt (the content translateY-scrolls to sections; keep ONE ease family across all steps for the stepped variant). Vertical traversal by CAMERA pan (the transcript glide) uses the Viewport Change rule's pan mode (the world translates up under a static frame, one continuous tween, no cuts). Speed-blur between stepped-scroll stops uses the Motion-Blur Streak rule (peaking at max scroll velocity, resolving to 0 at each settle). Which content each traversal beat reveals uses the Dynamic Content Sequencing rule. A centered title shrinking and gliding to dock as a fixed header is a plain simultaneous scale-plus-translate tween. Task rows cascading in staggered before the scroll takes over use the Waterfall Entry rule (or the Spring-Pop Entrance rule's staggered-group form for card-like rows). Typed lines — a verifier summary, a handoff line, a document title, a follow-up question, an opening headline — use the Discrete Text Sequence rule plus the Context-Sensitive Cursor rule for the trailing caret. A file-attachment chip pop-in, a tooltip pill pop, and a chat-bubble arrival all use the Spring-Pop Entrance rule. The cursor gliding in, landing, and clicking (the hinge and the coda) uses the Cursor-Click Ripple rule plus the Physics Press Reaction rule to compress the cursor and target together on the press. A selection-highlight sweep across the sentence uses the CSS Marker Patterns rule's highlight sweep. ONE push-in onto the highlighted selection, or a slow push-in plus lateral pan settling on highlighted cells, uses the Coordinate Target Zoom rule (the lateral pan IS the counter-translate component), sequenced under the Multi-Phase Camera rule when it follows a window scale-up. A fast decelerating zoom-out to the full workspace uses the Coordinate Target Zoom rule's zoom-out variation, or the Viewport Change rule's single continuous pull. An artifact window scaling up from small toward full frame on the click uses the Spring-Pop Entrance rule (a hero arrival scale-up, tuned toward near-zero overshoot so the window reads weighty, not bouncy). A collapsible row expanding into a sub-task stack, or an inline panel expanding below the highlighted line, uses the Anchored Layout Expand rule (in-flow accordion growth pushing subsequent content DOWN — never tweening width/height) plus the Waterfall Entry rule (or the Spring-Pop Entrance rule's stagger) on the arriving children. A phone-screen instant swap on the coda tab click uses the Discrete Text Sequence rule's discrete whole-state swap, instant, with no in-artifact camera move. Green verb highlights, model-tag pills, check-circle strikethroughs, yellow forecast cells, and edge fade masks are all static styling of the surface content — no motion rule needed.

**Camera modifier:** the blueprint's camera law is at most TWO real camera moves, bracketing the hinge. Pick the traversal mechanic first — camera pan (the Viewport Change rule's pan mode, pan-to-workspace only) OR element scroll (the 3D Page Scroll rule's flat variant, for every other mode) — never both at once. The reveal then spends the second (or only) move: one zoom-out to the workspace or one push-in to the detail (the Coordinate Target Zoom rule, phases sequenced by the Multi-Phase Camera rule), after which the frame LOCKS — all remaining motion is element-level (typing, expand, screen swap). The feed-rush variant spends zero camera moves at all — the whole shot is element scroll plus expand. This restraint is what separates the shape from the Cursor-UI-Demo blueprint (camera servos to every interaction) and from the Device-Surface-Showcase blueprint (a showcase camera presenting a held hero).

**Overflow:** the traversal deliberately moves content past the frame edges. Clip at the scene (`overflow: hidden`) AND mark the moving inner layer (the world/page wrapper carrying the transcript/feed/document) with a layout-overflow-allowed marker — otherwise an automated layout check will flag every row that has scrolled off as a bug rather than recognizing it as intentional.

#### Typewriter Reveal

**Intent:** a live text caret types (and edits) a line as a human would, then either collapses it to a point and pops a brand payoff, or holds it under a persistent brand mark while a sub-line types/swaps into the final CTA — making "someone is typing this" the engine of the shot.

**Roles served:** Hook — type a relatable question/statement live, then COLLAPSE it and spring-pop the brand (a logo lockup OR a product-UI moment) — "here's the everyday pain, now here's us." Brand Outro — hold the hero mark dead-center/top the whole shot while a sub-line beneath it swaps or types its way into the final CTA, landing the ask once the logo is already established.

**Duration:** 3.6–7s (Brand Outro 3.6–6.0s; Hook 5.5–7s).

**Shot structure:**

- **Scene 1 (0.0–~2.0s):** on a solid background field, a blinking text-input caret sits at the line start, then the primary line TYPES ON character by character with the caret trailing. Hook variant: nothing else is on screen, the typed hook line owns the frame — one sub-variant has the line type inside UI chrome (a rounded input/pill), the whole assembly continuously translating leftward and scaling slightly so the active caret stays pinned near frame-center while earlier words scroll off and clip past the left edge — a "ticker push." Brand Outro variant: a logo mark (plus an optional wordmark) is already centered/upper and STAYS fully visible for the entire shot; an entry flourish plays on the mark itself (a checkmark/icon stroking into the mark, or thin concentric rings rippling outward), and the typed tagline/product label is the SUB-LINE beneath the mark.
- **Scene 2 (~2.0–4.5s):** the typed line is MODIFIED IN PLACE — the active text is edited rather than re-shot. Hook variant: the final word(s) backspace out and a new word retypes, or the fill/caret snaps to an accent color on the final word; holds briefly. Brand Outro variant: the sub-line is removed in place via a direct hard cut/replace (no backspace) or a moving mask-wipe, while the mark performs a small idle move (a gentle rotate or a sparkle reposition); the mark never leaves frame.
- **Scene 3 — resolve.** Hook (collapse, ~0.3–0.7s): the caret vanishes; the whole text/assembly COLLAPSES to a point at center (a horizontal x-collapse or a scale-to-0 zoom-out) and disappears, leaving a clean background — then a centered brand element SPRING-POPS in. A logo-lockup sub-variant has a mark/icon pop, then slide aside as a wordmark unmasks/slides out from behind it, both settling into a centered lockup. A product-UI sub-variant has a UI control pop, a cursor sweep in from a corner and home onto it, and on contact a ~150ms state-flip — the base cross-fading to an accent color, the icon inverting, and a soft radial glow blooming outward and persisting. Brand Outro (~4.5s–end): the final CTA resolves in the sub-line slot — typed in with a caret, or shown as a CTA button in accent color beside plain text; an optional accent-color glow ring/halo settles around the persistent mark; holds to end. Final frame: logo mark plus glow ring plus CTA.

**Motion vocabulary:** a blinking text caret; character-by-character type-on; backspace-and-retype OR an in-place hard-cut/mask-wipe text swap; an optional leftward ticker push (the assembly translating to keep the caret centered); a persistent centered hero mark (never vanishing) with an entry flourish (icon stroke-draw, concentric ripple rings) and a small idle move (rotate/sparkle); an x-collapse/scale-to-0 zoom-out of the typed line; a spring-pop brand reveal; a wordmark unmask-slide into the lockup; a cursor sweep plus a UI state-flip plus a radial glow bloom; an accent glow/halo ring settle; a pill/button CTA reveal; a hold.

**Rule mapping:** the blinking text caret uses the Context-Sensitive Cursor rule (caret color-switch plus blink). Character-by-character type-on uses the Discrete Text Sequence rule (typing/typos/holds/backspace) plus a plain typewriter recipe. Backspace-and-retype, and an in-place hard-cut/replace text swap, both use the Discrete Text Sequence rule. A mask-wipe erase of the sub-line uses the Clip-Path Reveal Masks technique run in reverse. A leftward ticker push (the assembly translating to keep the caret centered) uses the Two-Phase Camera Cursor Tracking rule (the viewport following a moving caret). The persistent hero mark's hold needs no motion rule at all — a static anchor, its stillness intentional. An icon stroke-draw entry flourish into the mark uses the SVG Path Draw rule; concentric ripple rings from the mark reuse the Cursor-Click Ripple rule's ripple bloom. A small idle mark move (rotate/sparkle reposition) uses the Sine Wave Loop rule. An x-collapse/scale-to-0 zoom-out of the typed line uses the Scale-Swap Transition rule as the closest fit (it morphs/collapses elements at a shared center — an approximation, since a standalone collapse-and-vanish without the paired same-center brand pop isn't its exact case). A spring-pop brand reveal uses the Spring-Pop Entrance rule (or the Physics Press Reaction rule). Collapse-text-then-pop-brand as a same-center morph pair uses the Scale-Swap Transition rule. A wordmark unmask-slide into the lockup composes the Clip-Path Reveal Masks technique (the unmask) with the Spring-Pop Entrance rule (the slide). The cursor sweeping onto the UI control plus a press uses the Cursor-Click Ripple rule (cursor-to-target press plus ripple). The UI state-flip (base/icon inverting on contact) uses the Hacker Flip 3D Reveal rule. A radial glow bloom / accent glow-halo ring settle uses the ASR Keyword Glow rule (the accent glow), with the ring's expansion via the Center-Outward Expansion rule. A pill/button CTA reveal uses the Spring-Pop Entrance rule (or the Scale-Swap Transition rule).

**Camera modifier:** none required — the camera is static for both roles. The Hook ticker push is an ELEMENT translate (the typed assembly sliding leftward to keep the caret centered), not a camera move — modeled by the Two-Phase Camera Cursor Tracking rule rather than a true camera rule.

#### Video → Text Pivot

**Intent:** a product video holds center and claims attention, then slides aside to hand its weight to a hero stat in the space it vacates, then both clear and kinetic text types into the center — accent words carrying the meaning the video used to carry — sealed by a gradient pill. The arc is "show → yield → pivot → stamp," and each handoff pairs an exit with a same-anchor entrance so two beats read, not four.

**Roles served:** Product Intro — the open is "see the feature" then "see the impact," and the product video must stay visible through the stat reveal — it slides, it doesn't cut. Key Feature — a feature clip that yields to a frame-filling metric and a typographic impact line.

**Duration:** 6–8s.

**Shot structure:** a background canvas; one product video as a real muted `.mp4` clip, a hero stat, then kinetic text — each pair shares a screen anchor so the handoff reads as a weight-transfer.

- **Scene 1 (0.0–~1.6s) — the video shows.** The product video lands centered on a smooth scale-up and breathes (a small y-bob), claiming full attention. Camera static.
- **Scene 2 (~1.6–3.2s) — yield plus stat (signature move).** The video SLIDES aside (x plus scale-down) into the very space the hero stat now fills as the stat pops in with 3D-depth type — one weight-transfer reading as a single event, not two. The stat breathes within this window.
- **Scene 3 (~3.2–5.0s) — pivot to text.** Both the video and the stat clear out and kinetic impact text TYPES into the vacated center, character by character; its accent words carry the meaning the video used to carry.
- **Scene 4 (~5.0s–end) — stamp.** A gradient pill snaps shut around the closing line (`scaleX` 0→1), its glow halo resolving a beat behind so the silhouette reads before the bloom — sealing the statement as one graphic. Holds.

**Motion vocabulary:** a video scale-in plus a small breath; a weight-transfer slide (the video's x plus scale-down handing off to the stat at the same anchor); a 3D-depth stat type; character-stream typing; a gradient pill `scaleX` snap; a glow-halo bloom trailing the silhouette.

**Rule mapping:** the video's entrance (smooth) and the weight-transfer slide use a plain scale/opacity tween followed by an x-plus-scale tween on a long-tail `power3` ease; the video itself is a muted `<video>` element as a direct child of the composition root. The hero stat's frame-filling 3D type uses the 3D Text Depth Layers rule's static-depth variation (layers built at setup, no cascade fighting the entry). The same-anchor video-exit-to-stat-entry handoff, if treated as a morph, uses the Scale-Swap Transition rule (a shared center). Character-by-character impact typing through segmented spans uses the Dynamic Content Sequencing rule's clean character stream, or the Discrete Text Sequence rule. The pill `scaleX` snap plus a trailing glow halo composes a plain `scaleX` tween with the Ambient Glow Bloom rule (the halo, resolving a beat behind). Video/stat breathing within their windows uses the Sine Wave Loop rule's low-amplitude register, gated to each element's own window — never a forever loop.

**Camera modifier:** camera-static — all motion is element-space (the video itself translates), so the "pivot" is the elements moving, not a camera.

#### Zoom-Out Workspace Reveal

**Intent:** open TIGHT on one full-bleed detail — a graphic macro or a small UI region — let micro-action play in close-up, then ONE continuous decelerating zoom-out reveals that everything seen so far lives inside a containing whole (a design-tool workspace or a multi-pane agent workspace); the frame locks at the wide and element-level payoff carries on. The zoom-out IS the narrative engine and the reveal-of-nesting is the payoff — distinct from the Grid Card Assemble blueprint above, where a zoom-out is an optional camera modifier garnishing an element-stagger assembly; here nothing assembles, the world was whole all along, and the single outward move is what re-scopes its meaning. This blueprint is the structural inverse of every push-in shape elsewhere in this document (the Constellation blueprint's push-in, the Device-Surface-Showcase blueprint's continuous push, the Data-Viz Count-Up blueprint's push-through).

**Roles served:** Hook — the open is a full-bleed graphic mystery (a blob morphing, a macro blossom blooming), resolved by one unbroken exponentially-decelerating zoom-out that passes THROUGH an intermediate composition (an oversized headline, card artwork, or a web page) before revealing the whole thing is an artboard inside a design tool (panels, layers, an inspector, a timeline); the frame locks and the canvas keeps animating, ending mid-action. Benefits — the payoff is scale/breadth: micro-actions play in extreme close-up on one small UI region (file rows popping in, a highlight stepping, a guided glide down a list), then ONE fast smoothly-decelerating zoom-out (~0.5–1s) reveals the region was a corner of a huge multi-pane agent workspace (a chat pane, an artifact preview, a sidebar); the wide holds static to the end while element-level payoff completes the story ("look how much the agent did — and here's the deliverable").

**Duration:** 6.8–11s (the Hook continuous-pull variant runs 6.8s in both observed cases; the Benefits dwell-then-snap variant runs 10.7–11s — the dwell and the post-lock payoff stretch, the reveal itself does not).

**Hard rule — no zoom-in anywhere; camera static outside the single reveal.** The camera's only scale motion is OUTWARD. One zoom-out per shot. Before the reveal the camera either holds, glides/pans along the close-up surface, or is already running the (only) pull-back; after the reveal decelerates to a full stop the frame is LOCKED — every later change (a pane swap, a pane expansion, cursor travel, a playhead scrub, canvas animation) is element/layout motion, never camera. No push-in, no punch, no re-zoom, no second reveal. Violating this collapses the shape back into a generic camera tour.

**Shot structure:** one oversized static world — the full "whole" workspace authored at final layout from frame 0 — with the camera starting scaled far in on the detail; the reveal is one scale animation on the world. Two folded sub-shapes: (A) continuous nesting pull (Hook) and (B) close-up dwell → snap reveal (Benefits).

- **Scene 1 (0.0–~2.5s) — full-bleed detail plus micro-action.** Extreme close-up: the detail (a graphic macro — a blob, a blossom stem — or a small UI region, a file list, a browser corner) fills the frame edge to edge with NO containing chrome, canvas, or neighboring panes visible. The detail PERFORMS in close-up — this beat is never a static hold. Sub-shape A (Hook): the graphic itself moves/morphs/blooms — an organic accent blob flowing across and morphing into an undulating wavy line, or blurred macro forms sharpening as circular petals pop and expand outward into a flat vector motif — while the pull-back is ALREADY running underneath (the camera never waits). Sub-shape B (Benefits): the camera holds (or glides) while UI micro-action plays — rows (filenames, list items) popping in top to bottom, a soft highlight stepping down row by row, or the camera riding down a list while gently pulling back; optional blur-to-sharp resolve on the opening frame.
- **Scene 2 (~2.5s–reveal start) — the middle beat.** Sub-shape A: the continuing zoom-out resolves a mid-level composition, still full-bleed, still no chrome — oversized headline glyphs descending into frame as partial letterforms and settling centered (pure world-scale motion — the letters are static in world space, the camera pull produces the motion), or the motif is revealed living inside a card in a row of cards on a web page — the viewer re-scopes once and still doesn't know the real container. Sub-shape B: the close-up story develops at the same tightness — the view shifts to an adjacent panel, a new row fades/slides in and grows its panel, a cursor enters and hovers it with a soft highlight — this is the pre-reveal dwell, the tension being "we're deep inside something."
- **Scene 3 (the reveal) — ONE decelerating zoom-out completes; frame LOCKS.** The signature move. The camera pulls back to scale 1 and eases to a full stop, revealing the containing whole. Sub-shape A: the pull is the tail of the SAME continuous zoom running since frame 0 (total travel roughly 4.3–4.5s of a 6.8s shot), with strong exponential deceleration — the intermediate composition turns out to be an artboard/phone-screen mock on a design-tool canvas: light chrome, a left pages/layers panel, a right properties inspector, a blue selection box, a bottom animation timeline with keyframe bars. Sub-shape B: the pull is a discrete rapid burst (~0.5–1s) from the held close-up — smooth, heavily decelerating — landing the full multi-pane agent workspace: a left chat pane with the prompt/status/response, a center/right artifact pane (a spreadsheet/deck preview), an optional sidebar (a progress checklist plus artifacts plus context). In both cases, the zoom-out ends BEFORE the shot does — always leave a post-lock act, since the deceleration-to-stop is what makes the lock legible.
- **Scene 4 (lock–end) — element-level payoff on the locked wide.** The reveal is not the ending — the close-up's world keeps living inside the wide, and all motion is element/layout. Sub-shape A: a cursor enters from off-frame and glides to hover/click the selected element, or a playhead scrubs left to right across the bottom timeline while the canvas artwork animates in sync (petals rotating about their hub, a starburst spinning in place, a motif sweeping/shifting) — ending MID-ACTION, the tool alive. Sub-shape B: a file-attachment card fades in, the cursor clicks Open, the artifact pane swaps content via a quick white-out, and the viewer pane expands full-width over its neighbor (LAYOUT motion, not camera) landing on the deliverable (a full slide, a dashboard); or the frame simply holds long and static while the cursor drifts to rest near the payoff stat. Struck-through checklist items in the sidebar read as completed work. Long hold to the end.

**Motion vocabulary:** one continuous scale-driven zoom-out with exponential/eased deceleration (no cuts); a single fast decelerating zoom-out burst (~0.5–1s); a workspace-lock at zoom end; a full-bleed no-chrome opening; a blur-to-sharp macro focus resolve; an organic blob flow plus morph into an undulating wavy line; a squiggle-underline settle with residual undulation; circular petals popping/expanding outward (bloom); oversized letters descending into frame as partial glyphs (world-scale, not element motion); text scaling down through the frame to a centered settle; rows popping in top to bottom; a selection highlight stepping down row by row; the camera riding/panning down a list while pulling back; a new row fading/sliding in and growing its panel; cursor hover with a soft row highlight; a cursor entering from off-frame and gliding to hover/click; a timeline playhead scrub left to right; in-canvas rotation about a hub/spin-in-place; a motif shift/sweep-in; a file-attachment card fade-in; a cursor click; a pane content swap via a quick white-out; a pane expanding full-width over a neighbor (layout motion); checklist items shown struck-through; a long static hold; a cursor drift to rest; ending mid-action (Hook).

**Rule mapping:** the single decelerating zoom-out on the whole world uses the Viewport Change rule (one world wrapper, the camera state object as single source of truth via `onUpdate`, starting the scale at the reveal ratio with the single-wrapper counter-translate formula centering the detail, then tweening scale to 1 and translate to 0 with ONE shared ease — the detail drifting from frame-center to its home slot as the wide takes over). Framing an off-center detail at open and zooming out to a wide view uses the Coordinate Target Zoom rule's zoom-out variation (nested wrappers, reverse phases — start zoomed on the measured target, tween outer scale to 1 plus inner translate to 0 with a shared duration/ease; measure the detail's center after fonts load, never hand-derive). A pre-reveal glide/ride down a list while gently pulling back (sub-shape B) uses the Viewport Change rule (pan plus scale composed on one camera-state object), sequenced by the Multi-Phase Camera rule for the slow-glide → hold → fast-pull profile — this shape runs the same scale-agnostic math at 4–12× outward, per the Viewport Change rule's extreme-range note. Exponential deceleration-to-stop is an ease-selection choice (`expo.out`/`power4.out` on the reveal tween), needing no rule of its own — and after the stop, NO camera tweens should exist on the timeline at all, per the hard rule above. Oversized partial glyphs descending, or text scaling down through the frame, need no element tween at all — they're authored static in world space, and the Viewport Change rule's pull produces the motion (a common author trap is animating the letters separately, which double-moves them). An organic blob flow plus morph into a wavy line is a true SVG path morph, a capability beyond this rule library's scope — substitute a non-morph accent when that capability isn't available. Squiggle-underline residual undulation uses the Sine Wave Loop rule's finite bounded undulation. Circular petals popping/expanding outward (bloom) use the Spring-Pop Entrance rule's staggered pops plus the Center-Outward Expansion rule (petals expanding from the hub to final positions). Rows popping in top to bottom use the Spring-Pop Entrance rule's staggered-group form, or a plain low-drama fade-plus-short-slide stagger. A new row fading/sliding in uses the Spring-Pop Entrance rule's soft variant; its panel growing to fit uses the Anchored Layout Expand rule. The cursor entering off-frame, gliding, hovering, and clicking uses the Cursor-Click Ripple rule (move-to-target, co-depress, ripple); soft hover row-highlight is a plain background-color/opacity tween. A timeline playhead scrub left to right is a plain linear (`ease: "none"`) translateX; in-sync canvas animation is achieved by placing the artwork tweens at the same timeline position as the scrub, since synchronization is free on one paused timeline. In-canvas rotation about a hub (a petal flower, a starburst) uses the SVG Icon Enrichment rule's explicit-center rotation via the SVG transform attribute. A motif shift/sweep-in on a card uses a plain masked translate, or the Clip-Path Reveal Masks technique. A file-attachment card fade-in uses the Spring-Pop Entrance rule's soft variant or a plain fade. A pane content swap via a quick white-out uses the Discrete Text Sequence rule's whole-state swap at a threshold plus a white-flash overlay with an attack-decay opacity envelope. A pane expanding full-width over a neighbor (layout motion) uses the Anchored Layout Expand rule's one-axis layout hand-off — width/height tweens stay forbidden. Checklist items struck-through, or status states changing, are static content, or the Discrete Text Sequence rule if they check off on screen. A long static hold plus a cursor drift to rest needs no rule for the hold itself; the drift is a single slow translate that ARRIVES somewhere meaningful (resting near the payoff stat) — it performs, it is not idle wobble. Ending mid-action (Hook) needs no exit rule — the playhead/canvas tweens simply run to the composition's edge.

**Camera law — staging the one move:** build the ENTIRE workspace at final layout inside one world wrapper; there is no second set. The open is a large initial camera scale (typically 4–12×, whatever makes the detail full-bleed) with a counter-translate centering the detail; the reveal tweens to scale 1, translate 0. `overflow: hidden` on the scene; background on the scene, never the world. Crispness constraint: everything visible at open must survive that magnification — author the detail as DOM/vector (text, SVG, CSS shapes); any raster inside the close-up needs a source resolution at least `rendered × openScale`. Sub-shape A: the reveal tween spans roughly 0–4.5s with `expo.out`-class deceleration — one tween, no phases, no cuts; element beats (morph, bloom, glyph settle) are positioned along it. Sub-shape B: an optional gentle pre-reveal pan/pull (the Viewport Change rule's pan, or a slow scale ease-out of at most ~15% travel) during the dwell, then the reveal burst (~0.5–1s, heavy deceleration) as its own tween; the camera stays fully static after. Never: a zoom-in, a second zoom-out, camera motion after the lock, or replacing the reveal with a cut. One outward move is the whole grammar.

**Boundary vs. the Grid Card Assemble blueprint above:** it already carries an optional zoom-out reveal modifier (its glass-card and logo-wall variants), so the two shapes border each other. The test: if elements ASSEMBLE and the pull-back merely shows the assembled array in context, it's the Grid Card Assemble blueprint; if the world is whole from frame 0 and the single decelerating pull-back is itself the story — close-up mystery → nesting reveal → locked-frame payoff — it's this blueprint.

## Transitions Catalog

A transition tells the viewer how two scenes relate. A crossfade says "this continues." A push slide says "next point." A blur crossfade says "drift with me." Choose transitions that match what the content is doing emotionally, not just technically.

### Animation Rules for Multi-Scene Compositions

These are non-negotiable for every multi-scene composition:

1. **Every composition uses transitions.** No exceptions. Scenes without transitions feel like jump cuts.
2. **Every scene uses entrance animations.** Elements animate IN — opacity, position, scale, etc. No scene should pop fully-formed onto screen. Use `gsap.fromTo()` (not `gsap.from()`) so the start state is explicit: `from()` animates *to* current CSS, so pairing it with CSS `opacity: 0` is a 0→0 no-op and the element never appears.
3. **Exit animations are BANNED** except on the final scene. Do NOT use `gsap.to()` to animate elements out before a transition fires. The transition IS the exit. Outgoing scene content must be fully visible when the transition starts — the transition handles the visual handoff.
4. **Final scene exception:** the last scene MAY fade elements out (e.g. fade to black at the end of the composition). This is the only scene where exit animations are allowed.

```js
// ❌ BANNED — fading the outgoing scene out, then the next scene just runs its entrance.
//    This is a jump cut with a dip, not a transition.
tl.to("#s1", { opacity: 0, duration: 0.4 }, 4.0);
tl.from("#s2 .headline", { y: 40, opacity: 0 }, 4.4);

// ✅ CORRECT — outgoing and incoming animate AT THE SAME TIME T; the motion IS the handoff.
const T = 4.0;
tl.to("#s1", { yPercent: -100, filter: "blur(8px)", duration: 0.5, ease: "power3.in" }, T);
tl.fromTo("#s2", { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power3.out" }, T);
```

Every transition follows the same discipline: position the new scene → animate the outgoing scene → swap → animate the incoming scene → clean up any overlay elements used for the effect.

### Energy → Primary Transition

| Energy | CSS Primary | Shader Primary | Accent | Duration | Easing |
| --- | --- | --- | --- | --- | --- |
| **Calm** (wellness, brand story, luxury) | Blur crossfade, focus pull | Cross-warp morph, thermal distortion | Light leak, circle iris | 0.5–0.8s | `sine.inOut`, `power1` |
| **Medium** (corporate, SaaS, explainer) | Push slide, staggered blocks | Whip pan, cinematic zoom | Squeeze, vertical push | 0.3–0.5s | `power2`, `power3` |
| **High** (promos, sports, music, launch) | Zoom through, overexposure | Ridged burn, glitch, chromatic split | Staggered blocks, gravity drop | 0.15–0.3s | `power4`, `expo` |

Pick ONE primary (60–70% of scene changes) plus 1–2 accents. Never use a different transition for every scene.

### Mood → Transition Type

Think about what the transition *communicates*, not just what it looks like.

| Mood | Transitions | Why it works |
| --- | --- | --- |
| **Warm / inviting** | Light leak, blur crossfade, focus pull, film burn (shader: thermal distortion, light leak, cross-warp morph) | Soft edges, warm color washes. Nothing sharp or mechanical. |
| **Cold / clinical** | Squeeze, zoom out, blinds, shutter, grid dissolve (shader: gravitational lens) | Content transforms mechanically — compressed, shrunk, sliced, gridded. |
| **Editorial / magazine** | Push slide, vertical push, diagonal split, shutter (shader: whip pan) | Like turning a page or slicing a layout. Clean directional movement. |
| **Tech / futuristic** | Grid dissolve, staggered blocks, blinds, chromatic aberration (shader: glitch, chromatic split) | Grid dissolve is the core "data" transition. Shader glitch adds posterization plus scan lines. |
| **Tense / edgy** | Glitch, VHS, chromatic aberration, ripple (shader: ridged burn, glitch, domain warp) | Instability, distortion, digital breakdown. Ridged burn adds sharp lightning-crack edges. |
| **Playful / fun** | Elastic push, 3D flip, circle iris, morph circle, clock wipe (shader: ripple waves, swirl vortex) | Overshoot, bounce, rotation, expansion. Swirl vortex adds organic spiral distortion. |
| **Dramatic / cinematic** | Zoom through, zoom out, gravity drop, overexposure, color dip to black (shader: cinematic zoom, gravitational lens, domain warp) | Scale, weight, light extremes. Shader transitions add per-pixel depth. |
| **Premium / luxury** | Focus pull, blur crossfade, color dip to black (shader: cross-warp morph, thermal distortion) | Restraint. Cross-warp morph flows both scenes into each other organically. |
| **Retro / analog** | Film burn, light leak, VHS, clock wipe (shader: light leak) | Organic imperfection. Warm color bleeds, scan-line displacement. |

### Narrative Position

| Position | Use | Why |
| --- | --- | --- |
| **Opening** | Your most distinctive transition. Match the mood. 0.4–0.6s | Sets the visual language for the entire piece. |
| **Between related points** | Your primary transition. Consistent. 0.3s | Don't distract — the content is continuing. |
| **Topic change** | Something different from your primary. Staggered blocks, shutter, squeeze. | Signals "new section" — the viewer's brain resets. |
| **Climax / hero reveal** | Your boldest accent. Fastest or most dramatic. | This is the payoff — spend your best transition here. |
| **Wind-down** | Return to gentle. Blur crossfade, crossfade. 0.5–0.7s | Let the viewer exhale after the climax. |
| **Outro** | Slowest, simplest. Crossfade, color dip to black. 0.6–1.0s | Closure. Don't introduce new energy at the end. |

### Blur Intensity by Energy

| Energy | Blur | Duration | Hold at peak |
| --- | --- | --- | --- |
| **Calm** | 20–30px | 0.8–1.2s | 0.3–0.5s |
| **Medium** | 8–15px | 0.4–0.6s | 0.1–0.2s |
| **High** | 3–6px | 0.2–0.3s | 0s |

### Presets

| Preset | Duration | Easing |
| --- | --- | --- |
| `snappy` | 0.2s | `power4.inOut` |
| `smooth` | 0.4s | `power2.inOut` |
| `gentle` | 0.6s | `sine.inOut` |
| `dramatic` | 0.5s | `power3.in` → out |
| `instant` | 0.15s | `expo.inOut` |
| `luxe` | 0.7s | `power1.inOut` |

### CSS vs. Shader Transitions

CSS transitions animate scene containers with opacity, transforms, clip-path, and filters. Shader transitions composite both scene textures per-pixel on a WebGL canvas — they can warp, dissolve, and morph in ways CSS cannot. Both are first-class options; shaders require a dedicated shader-transitions package providing the WebGL setup, capture, and GSAP integration rather than hand-written raw GLSL, while CSS transitions are simpler to set up. Choose based on the effect you want, not based on which is easier.

**Mixing is supported.** Some transitions can use WebGL shaders and others a plain CSS crossfade in the same composition. Omitting the shader designation on any transition entry produces a smooth opacity crossfade instead of a WebGL effect. A shader-transitions helper library, if available in your environment, typically manages all scene visibility regardless of transition type and expects you to let it create the timeline rather than passing in your own, adding your beat animations to the returned timeline afterward.

### Shader-Compatible CSS Rules

Shader transitions capture DOM scenes to WebGL textures via an HTML-to-canvas capture step. The canvas 2D rendering pipeline doesn't match CSS exactly. Follow these rules to avoid visible artifacts at transition boundaries (these rules only apply to shader-transition compositions — CSS-only compositions have no such restrictions):

1. **No `transparent` keyword in gradients.** Canvas interpolates `transparent` as `rgba(0,0,0,0)` (black at zero alpha), creating dark fringes. Always use the target color at zero alpha, e.g. `rgba(200,117,51,0)` rather than `transparent`.
2. **No gradient backgrounds on elements thinner than 4px.** Canvas can't match CSS gradient rendering on 1–2px elements. Use a solid `background-color` on thin accent lines instead.
3. **No CSS variables (`var()`) on elements visible during capture.** The capture step doesn't reliably resolve custom properties. Use literal color values in inline styles.
4. **Mark uncapturable decorative elements with a no-capture attribute.** The capture function skips these. They're present on the live DOM but absent from the shader texture — use this for elements that can't follow the rules above.
5. **No gradient opacity below 0.15.** Gradient elements below 10% opacity render differently in canvas vs. CSS. Increase to 0.15+ or use a solid color at an equivalent brightness.
6. **Every scene container must have an explicit `background-color`, matching the same color passed as the overall background config.** The capture step reads scene elements via the HTML-to-canvas capture; without both the CSS background-color and the matching config value, the texture renders as black.

### Transitions That Don't Work in CSS

Avoid: star iris (polygon interpolation is broken for this shape), tilt-shift (no selective CSS blur), lens flare (renders as a visible shape rather than an optical effect), hinge/door (distorts too fast to read cleanly).

### Visual Pattern Warning

Avoid transitions that create visible repeating geometric patterns — grids of tiles, hexagonal cells, uniform dot arrays, evenly-spaced blob circles. These look cheap and artificial regardless of the math behind them. Organic noise (fractal Brownian motion, domain warping) is good because it's irregular. Geometric repetition is bad because the eye instantly sees the grid.

### Hard Rules for CSS Transitions (implementation-level)

These cause real bugs if violated:

- **Scene visibility:** scene 1 is visible by default (no `opacity: 0`). Scenes 2+ have `opacity: 0` on the container div. GSAP reveals them — there should be no separate visibility-management shim.
- **Fonts:** just write the `font-family` you want; if your build pipeline embeds fonts automatically via inline `@font-face` data URIs, no `<link>` tags or `@import`s are needed.
- **Element structure:** in a standalone (single-composition) transition demo, scene divs don't need the "clip" class marker used inside multi-clip compositions — only the root div carries the composition-id/start/duration attributes.
- **Overlay elements:** staggered blocks should be full-screen (matching the composition's pixel dimensions), NOT thin strips. Glitch RGB overlays should use normal blending at ~35% opacity, NOT `mix-blend-mode: multiply` (which is invisible on dark backgrounds). Light-leak overlays should be larger than the frame (2400px+), never a visible shape. Overexposure should use `filter: brightness()` on the scene itself, not just a white overlay.
- **VHS tape:** clone actual scene content with `cloneNode(true)`, NOT colored bars. Each strip should be wider than the frame (e.g. 2020px positioned at `left: -50px`) so edges never show. Add red-plus-blue chromatic offset copies on each strip (z-index above the main strip, ~35% opacity). Use a seeded PRNG for deterministic random offsets — never `Math.random()`.
- **Z-index:** gravity drop, zoom out, and diagonal split all need the outgoing scene ON TOP (a high z-index) so it exits while revealing the new scene behind it (a low z-index).
- **Page burn:** content burns with the page — no falling debris. Hide scene 1 via a `tl.set` at the exact burn end time, NEVER via an `onComplete` callback (which isn't reversible when scrubbing). The `onUpdate` callback must restore `clipPath: "none"` when progress is at or below 0, for rewind support. The incoming scene fades from black starting at roughly 90% through the burn.
- **Clock wipe:** use a 9-point polygon with intermediate edge positions, stepping through the four quadrants with separate tweens for a smooth sweep.
- **Grid dissolve:** cycle 5 palette colors per cell, not monochrome.
- **Blinds count by energy:** calm energy uses 4 horizontal/6 vertical blinds; medium uses 6–8 horizontal/8 vertical; high uses 12–16 horizontal/16 vertical.

### Scene Template

Every CSS-transition composition follows this basic scaffold — two full-frame scene divs stacked with z-index, the first visible and the second hidden, animated by one paused GSAP timeline registered on the shared timeline registry:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #000;
        font-family: "YOUR FONT", sans-serif;
      }
      .scene {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      #scene1 {
        z-index: 1;
        background: #color;
      }
      #scene2 {
        z-index: 2;
        background: #color;
        opacity: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-width="1920"
      data-height="1080"
      data-start="0"
      data-duration="TOTAL"
    >
      <div id="scene1" class="scene"><!-- visible --></div>
      <div id="scene2" class="scene"><!-- hidden --></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
      // Transition code here
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

All code examples below use `old` for the outgoing scene-inner selector and `new` for the incoming, with `T` as the transition start time (in seconds).

### Transition Registry (curated Tier-B subset)

A curated subset of five transitions — pure transform/opacity/filter on the two scene wrapper elements, no injected overlay DOM, no per-scene cooperation — is stable enough to be driven by a fully mechanical injector that reads a JSON description and stamps the matching GSAP template onto the master timeline, computing the overlap window and re-assigning z-index tracks automatically. This is a narrower list than the full catalog below (roughly 40 CSS-plus-shader transitions); overlay-heavy families (staggered blocks, blinds, light leak, grid dissolve, page burn) and shader transitions require more manual authoring.

**How an automated injector applies a transition** (useful as a mental model even when authoring by hand): at a scene boundary between an outgoing scene and an incoming scene, it (1) extends the outgoing wrapper's duration by the transition's own duration, holding its final frame; (2) pulls the incoming wrapper's start time earlier by the same amount, creating an overlap window; (3) reassigns all clip track-index values as a 0/1 ping-pong so the two overlapping wrappers never share a track (same-track overlap is illegal — the higher track composites on top); (4) stamps the transition's template into the shared timeline registry at the overlap-start time.

**Template placeholders** used by the five entries below: `__OLD__`/`__NEW__` are the quoted outgoing/incoming clip-wrapper selectors; `__T__` is the overlap-start time in seconds; `__DUR__` is the transition's duration; `__DX__`/`__DY__` are horizontal/vertical travel distances for directional types (e.g. −1920/1920 for a 1920-wide frame, −1080/1080 for a 1080-tall frame); `__ORIGIN_OUT__`/`__ORIGIN_IN__` are the transform-origin pair for the squeeze type.

**crossfade** (tier B, any energy, default duration 0.5s, no directions):

```js
tl.to(__OLD__, { opacity: 0, duration: __DUR__, ease: "power2.inOut" }, __T__);
tl.fromTo(__NEW__, { opacity: 0 }, { opacity: 1, duration: __DUR__, ease: "power2.inOut" }, __T__);
```

**blur-crossfade** (tier B, calm energy, default duration 0.6s, no directions) — the default choice when the two scenes' backgrounds differ a lot, since the blur masks the background-color clash a plain crossfade would expose:

```js
tl.to(__OLD__, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: __DUR__, ease: "power2.inOut" }, __T__);
tl.fromTo(__NEW__, { filter: "blur(10px)", scale: 0.97, opacity: 0 }, { filter: "blur(0px)", scale: 1, opacity: 1, duration: __DUR__, ease: "power2.inOut" }, __T__);
```

**push-slide** (tier B, medium energy, default duration 0.5s, directional: LEFT/RIGHT/UP/DOWN, default LEFT) — the injector picks the horizontal or vertical pair based on the chosen direction, emitting only one:

```js
// horizontal
tl.to(__OLD__, { x: __DX__, duration: __DUR__, ease: "power3.inOut" }, __T__);
tl.fromTo(__NEW__, { x: __DXIN__, opacity: 1 }, { x: 0, duration: __DUR__, ease: "power3.inOut" }, __T__);
// vertical
tl.to(__OLD__, { y: __DY__, duration: __DUR__, ease: "power3.inOut" }, __T__);
tl.fromTo(__NEW__, { y: __DYIN__, opacity: 1 }, { y: 0, duration: __DUR__, ease: "power3.inOut" }, __T__);
```

**zoom-through** (tier B, high energy, default duration 0.4s, no directions):

```js
tl.to(__OLD__, { scale: 2.5, opacity: 0, filter: "blur(8px)", duration: __DUR__, ease: "power3.in" }, __T__);
tl.fromTo(__NEW__, { scale: 0.5, opacity: 0, filter: "blur(8px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: __DUR__, ease: "power3.out" }, __T__);
```

**squeeze** (tier B, medium energy, default duration 0.4s, no directions) — the outgoing compresses to a vertical line on the left edge, the incoming expands from the right edge; the incoming starts at `scaleX: 0` so its higher-track stacking is harmless:

```js
tl.to(__OLD__, { scaleX: 0, transformOrigin: "left center", duration: __DUR__, ease: "power3.inOut" }, __T__);
tl.fromTo(__NEW__, { scaleX: 0, transformOrigin: "right center", opacity: 1 }, { scaleX: 1, transformOrigin: "right center", duration: __DUR__, ease: "power3.inOut" }, __T__);
```

**Choosing among these (or defaulting):** pick 2–3 types for the whole video and repeat them — repetition is what reads as professional. If a boundary has no explicitly chosen transition, default to `zoom-through` when the incoming scene reads as high energy (explosive/kinetic/frenetic), otherwise default to `blur-crossfade` as the universal calm default — this keeps the whole video to roughly 2 transition types. A more advanced "morph" or "shared-element" transition type (a worker-authored bridge driven by explicit narrative intent, connecting a specific outgoing element to a specific incoming element rather than the whole scene) is exempt from this 2–3 budget, since it plays a different structural role.

### Push / Linear Transitions

**Push Slide.** Both scenes move together — the new scene pushes the old one out.

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 0, duration: 0.5, ease: "power3.inOut" }, T);
```

**Vertical Push.** Same as push slide but vertical.

```js
tl.to(old, { y: -1080, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { y: 1080, opacity: 1 }, { y: 0, duration: 0.5, ease: "power3.inOut" }, T);
```

**Elastic Push.** A push with an overshoot bounce on the incoming scene.

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.in" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 30, duration: 0.4, ease: "power4.out" }, T + 0.1);
tl.to(new, { x: -15, duration: 0.15, ease: "sine.inOut" }, T + 0.5);
tl.to(new, { x: 0, duration: 0.1, ease: "sine.out" }, T + 0.65);
```

**Squeeze.** The old scene compresses, the new expands from the opposite side.

```js
tl.to(old, { scaleX: 0, transformOrigin: "left center", duration: 0.4, ease: "power3.inOut" }, T);
tl.fromTo(new, { scaleX: 0, transformOrigin: "right center", opacity: 1 },
  { scaleX: 1, duration: 0.4, ease: "power3.inOut" }, T + 0.1);
tl.set(old, { opacity: 0 }, T + 0.5);
```

### Radial / Shape Transitions

**Circle Iris.** An expanding circle from center reveals the new scene.

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "circle(0% at 50% 50%)" },
  { clipPath: "circle(75% at 50% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

**Diamond Iris.** An expanding diamond shape from center.

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)" },
  { clipPath: "polygon(50% -20%, 120% 50%, 50% 120%, -20% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

**Diagonal Split.** The old scene shrinks to a triangle in one corner.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)" }, T);
tl.to(old, { clipPath: "polygon(60% 0%, 100% 0%, 100% 40%, 60% 0%)", duration: 0.5, ease: "power3.inOut" }, T);
tl.set(old, { opacity: 0, zIndex: "auto", clipPath: "none" }, T + 0.5);
tl.set(new, { zIndex: "auto" }, T + 0.5);
```

### 3D Transitions

**3D Card Flip.** A 180° Y-axis rotation. Requires CSS `backface-visibility: hidden` and `transform-style: preserve-3d` on both scene-inners, with `perspective: 1200px` on the parent.

```js
tl.set(new, { rotationY: -180, opacity: 1 }, T);
tl.to(old, { rotationY: 180, duration: 0.6, ease: "power2.inOut" }, T);
tl.to(new, { rotationY: 0, duration: 0.6, ease: "power2.inOut" }, T);
tl.set(old, { opacity: 0 }, T + 0.6);
```

### Scale / Zoom Transitions

**Zoom Through.** The old scene zooms past the camera and blurs; the new scene zooms in from behind.

```js
tl.to(old, { scale: 2.5, opacity: 0, filter: "blur(8px)", duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { scale: 0.5, opacity: 0, filter: "blur(8px)" },
  { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, T + 0.15);
```

**Zoom Out.** The old scene shrinks away; the new scene was already behind it. Needs z-index management.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, transformOrigin: "50% 50%" }, T);
tl.to(old, { scale: 0.3, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.set(old, { zIndex: "auto" }, T + 0.4);
tl.set(new, { zIndex: "auto" }, T + 0.4);
```

### Dissolve Transitions

**Crossfade.** A simple opacity swap. The baseline.

```js
tl.to(old, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, T);
```

**Blur Crossfade.** A dissolve with a blur plus scale shift. Scale the blur amount by energy per the table above — the medium (default) version is shown; for calm compositions increase to 20–30px with a 0.3–0.5s hold at peak blur; for high energy decrease to 3–6px with no hold.

Medium (default):

```js
tl.to(old, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new,
  { filter: "blur(10px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.5, ease: "power2.inOut" }, T + 0.1);
```

Calm (wellness, luxury — heavy blur, holds at abstract color):

```js
tl.to(old, { filter: "blur(25px)", scale: 1.05, duration: 0.6, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.4, ease: "power1.in" }, T + 0.4);
tl.fromTo(new,
  { filter: "blur(25px)", scale: 0.95, opacity: 0 },
  { filter: "blur(25px)", scale: 0.95, opacity: 1, duration: 0.3, ease: "power1.inOut" }, T + 0.5);
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.6, ease: "power1.out" }, T + 0.8);
```

**Focus Pull.** The outgoing scene slowly blurs while the incoming scene fades in sharp — a depth-of-field feel. Scale blur amount and hold duration by energy.

Medium:

```js
tl.to(old, { filter: "blur(15px)", duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power2.in" }, T + 0.25);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, T + 0.25);
```

Calm — a slow rack focus with a long hold at peak defocus:

```js
tl.to(old, { filter: "blur(30px)", duration: 0.8, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.5, ease: "power1.in" }, T + 0.6);
tl.fromTo(new, { opacity: 0, filter: "blur(20px)" },
  { opacity: 1, filter: "blur(20px)", duration: 0.3, ease: "power1.inOut" }, T + 0.7);
tl.to(new, { filter: "blur(0px)", duration: 0.6, ease: "power1.out" }, T + 1.0);
```

**Color Dip.** Fade to a solid color, hold, fade up the new scene.

```js
tl.to(old, { opacity: 0, duration: 0.2, ease: "power2.in" }, T);
// Background color shows through
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, T + 0.25);
```

### Cover Transitions

**Staggered Color Blocks.** Full-screen colored divs (matching the composition's own pixel dimensions) slide across staggered. The scene swaps while covered.

2-block (standard):

```js
tl.set("#wipe-a", { x: -1920 }, T - 0.01);
tl.set("#wipe-b", { x: -1920 }, T - 0.01);
tl.to("#wipe-a", { x: 0, duration: 0.25, ease: "power3.inOut" }, T);
tl.to("#wipe-b", { x: 0, duration: 0.25, ease: "power3.inOut" }, T + 0.06);
tl.set(old, { opacity: 0 }, T + 0.2);
tl.set(new, { opacity: 1 }, T + 0.2);
tl.to("#wipe-a", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.28);
tl.to("#wipe-b", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.34);
```

5-block (dense variant): the same pattern with 5 blocks at a 0.04s stagger, using the composition's own palette colors.

**Horizontal Blinds.** Full-width strips slide across staggered. Each strip spans the full frame width and a fraction of the height. 6 strips (180px each) use a 0.03s stagger; 12 strips (90px each) use a 0.018s stagger.

```js
for (var i = 0; i < N; i++) {
  tl.set("#blind-h-" + i, { x: -1920 }, T - 0.01);
  tl.fromTo("#blind-h-" + i, { x: -1920 }, { x: 0, duration: 0.2, ease: "power3.inOut" }, T + i * stagger);
}
tl.set(old, { opacity: 0 }, T + coverTime);
tl.set(new, { opacity: 1 }, T + coverTime);
for (var i = 0; i < N; i++) {
  tl.to("#blind-h-" + i, { x: 1920, duration: 0.2, ease: "power3.inOut" }, T + exitStart + i * stagger);
}
```

**Vertical Blinds.** Same as horizontal but the strips are tall and narrow, moving on the Y axis instead.

### Light Transitions

**Light Leak.** Multiple warm-colored overlays wash across the frame. Needs a flat warm tint layer plus 2–3 bright radial-gradient divs, all larger than the frame so edges are never visible.

```js
// Warm tint washes over the entire frame
tl.to("#leak-warm", { opacity: 0.4, duration: 0.3, ease: "power1.in" }, T);
// Bright leak elements drift in
tl.to("#leak-1", { opacity: 0.9, x: 300, duration: 0.5, ease: "sine.inOut" }, T + 0.05);
tl.to("#leak-2", { opacity: 0.8, x: 200, duration: 0.6, ease: "sine.inOut" }, T + 0.1);
// Peak warmth then swap
tl.to("#leak-warm", { opacity: 0.6, duration: 0.15, ease: "power2.in" }, T + 0.35);
tl.set(old, { opacity: 0 }, T + 0.45);
tl.set(new, { opacity: 1 }, T + 0.45);
// Leak fades
tl.to("#leak-warm", { opacity: 0, duration: 0.4, ease: "power2.out" }, T + 0.5);
tl.to("#leak-1", { opacity: 0, x: 600, duration: 0.35, ease: "power1.out" }, T + 0.5);
```

**Overexposure Burn.** The scene progressively blows out to white using CSS `filter: brightness()`, then a white overlay fades in; the swap happens at peak white, then white recedes to reveal the new scene.

```js
tl.to(old, { filter: "brightness(1.5)", scale: 1.03, duration: 0.2, ease: "power1.in" }, T);
tl.to(old, { filter: "brightness(3)", scale: 1.06, duration: 0.2, ease: "power2.in" }, T + 0.2);
tl.to("#flash-overlay", { opacity: 0.5, duration: 0.25, ease: "power1.in" }, T + 0.15);
tl.to("#flash-overlay", { opacity: 1, duration: 0.15, ease: "power2.in" }, T + 0.4);
tl.set(old, { opacity: 0, filter: "brightness(1)", scale: 1 }, T + 0.55);
tl.set(new, { opacity: 1 }, T + 0.55);
tl.to("#flash-overlay", { opacity: 0, duration: 0.35, ease: "power2.out" }, T + 0.55);
```

**Film Burn.** Staggered warm overlays (amber, orange, red) bleed in from one edge. Each overlay is a large radial-gradient div at a high z-index.

```js
tl.to("#burn-a", { opacity: 1, x: -300, duration: 0.4, ease: "power1.in" }, T);
tl.to("#burn-b", { opacity: 1, x: -500, duration: 0.5, ease: "power1.in" }, T + 0.05);
tl.to("#burn-c", { opacity: 1, x: -200, duration: 0.45, ease: "power1.in" }, T + 0.1);
tl.set(old, { opacity: 0 }, T + 0.35);
tl.set(new, { opacity: 1 }, T + 0.35);
tl.to("#burn-a", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.45);
tl.to("#burn-b", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.5);
tl.to("#burn-c", { opacity: 0, duration: 0.3, ease: "power2.out" }, T + 0.55);
```

### Distortion Transitions

**Glitch.** RGB-tinted overlays (NOT multiply blend — use normal blending at 35% opacity) jitter with large offsets; the scene itself also jitters.

```js
tl.set("#glitch-r", { opacity: 1, x: 40, y: -8 }, T);
tl.set("#glitch-g", { opacity: 1, x: -30, y: 12 }, T);
tl.set("#glitch-b", { opacity: 1, x: 15, y: -20 }, T);
tl.set(old, { x: -15 }, T);
// 6 jitter frames at 0.03s intervals with big offsets (±30-60px)
// ... swap and clear at T + 0.2
```

**Chromatic Aberration.** RGB overlays start aligned then spread apart (±80px), the scene fades, and they converge on the new scene.

```js
tl.set("#glitch-r", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-g", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-b", { opacity: 0.6, x: 0 }, T);
tl.to("#glitch-r", { x: -80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-b", { x: 80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-g", { y: 30, duration: 0.3, ease: "power2.in" }, T);
// Swap at T + 0.3, converge back at T + 0.3
```

**Ripple.** Rapid oscillation (±30px) plus scale distortion (0.97–1.03) plus increasing blur. Swap happens at peak distortion.

```js
tl.to(old, { x: 30, scale: 1.02, duration: 0.04, ease: "none" }, T);
tl.to(old, { x: -25, scale: 0.98, filter: "blur(4px)", duration: 0.04, ease: "none" }, T + 0.04);
// ... more oscillations with increasing blur
// Swap at peak, incoming stabilizes with decreasing wobble
```

**VHS Tape.** Clone the scene into 20 horizontal strips (each 54px, clip-path'd). Each strip shifts x independently with seeded pseudo-random offsets at per-bar random intervals; add red-plus-blue chromatic offset copies on each strip (z-index above the main strip, 35% opacity); make strips wider than the frame (2020px at `left: -50px`) so edges never show. Implement via `cloneNode`-based strip generation with a deterministic seeded PRNG, per the destruction/hard-rules notes above.

### Mechanical Transitions

**Shutter.** Two full-screen halves close from top and bottom, meeting in the middle. The scene swaps while closed, then the shutter opens again.

```js
tl.to("#shutter-top", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.to("#shutter-bot", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.25);
tl.set(new, { opacity: 1 }, T + 0.25);
tl.to("#shutter-top", { y: -540, duration: 0.25, ease: "power3.out" }, T + 0.3);
tl.to("#shutter-bot", { y: 540, duration: 0.25, ease: "power3.out" }, T + 0.3);
```

**Clock Wipe.** A radial polygon sweep stepping through quadrants. Use a 9-point polygon with intermediate edge positions for a smooth sweep.

```js
tl.set(new, { opacity: 1, zIndex: 10 }, T);
var d = 0.1; // duration per quadrant
tl.set(new, { clipPath: "polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%)" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%)", duration: d, ease: "none" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 50% 100%, 50% 100%, 50% 100%)", duration: d, ease: "none" }, T + d);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 50%)", duration: d, ease: "none" }, T + d*2);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 0%)", duration: d, ease: "none" }, T + d*3);
tl.set(new, { clipPath: "none", zIndex: "auto" }, T + d*4 + 0.02);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + d*4 + 0.02);
```

### Grid Transitions

**Grid Dissolve.** A grid of colored cells covers the frame in a ripple from center; the scene swaps at 50% coverage; cells fade out in the same ripple pattern. A 12-cell grid (4×3, each 480×270) is standard; a 120-cell grid (12×10, each 160×108) is a dense variant with lower opacity (0.75) and a tighter ripple. Cells should be created dynamically in JS and sorted by distance from center to derive the ripple stagger.

### Other Transitions

**Gravity Drop.** The old scene falls down with a slight rotation; the new scene was already behind it. Needs z-index management.

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10 }, T);
tl.to(old, { y: 1200, rotation: 4, duration: 0.5, ease: "power3.in" }, T);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + 0.5);
tl.set(new, { zIndex: "auto" }, T + 0.5);
```

**Morph Circle.** A circle scales up from center to fill the frame, becoming the new scene's background color; the new scene's content fades in on top.

```js
tl.set("#morph-circle", { background: newBgColor, opacity: 1, scale: 0 }, T);
tl.to("#morph-circle", { scale: 30, duration: 0.5, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.4);
tl.set(new, { opacity: 1 }, T + 0.4);
tl.to("#morph-circle", { opacity: 0, duration: 0.15, ease: "power2.out" }, T + 0.5);
```

### Blur Transitions

All blur transitions scale with energy per the Blur Intensity table above.

**Blur Through.** Content becomes fully abstract before resolving — the heaviest blur transition, inherently heavy so calm is its natural default.

Calm:

```js
tl.to(old, { filter: "blur(30px)", scale: 1.08, duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power1.in" }, T + 0.3);
// Hold: both scenes in abstract blur state
tl.fromTo(new,
  { filter: "blur(30px)", scale: 0.92, opacity: 0 },
  { filter: "blur(30px)", scale: 0.92, opacity: 1, duration: 0.2, ease: "none" }, T + 0.5);
// Slow resolve
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.7, ease: "power1.out" }, T + 0.7);
```

Medium:

```js
tl.to(old, { filter: "blur(15px)", scale: 1.05, opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(15px)", scale: 0.95, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }, T + 0.2);
```

**Directional Blur.** Blur plus skew simulating motion in one direction. Scale both blur and skew with energy.

Medium (default):

```js
tl.to(old, { filter: "blur(12px)", skewX: -8, x: -200, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { filter: "blur(12px)", skewX: 8, x: 200, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, T + 0.15);
```

Calm (heavier blur, gentler motion):

```js
tl.to(old, { filter: "blur(20px)", skewX: -4, x: -100, opacity: 0, duration: 0.6, ease: "power1.in" }, T);
tl.fromTo(new,
  { filter: "blur(20px)", skewX: 4, x: 100, opacity: 0 },
  { filter: "blur(0px)", skewX: 0, x: 0, opacity: 1, duration: 0.6, ease: "power1.out" }, T + 0.3);
```

### Destruction Transitions

**Page Burn.** The outgoing scene literally burns away from a corner. A fire front expands with noise-based irregular edges, a canvas draws the scorched char line at the burn boundary, and individual text characters/elements chip off and fall with gravity as the fire reaches them. The incoming scene reveals behind the burn. This is the most dramatic transition in the catalog — reserve it for hero moments (dramatic reveals, edgy/destructive mood, gaming, cyberpunk).

This transition has three systems working together: (1) fire geometry — a radial front expanding from a corner with noise-based irregularity for organic edges; (2) scene clipping — the outgoing scene uses an SVG clip-path (with `fill-rule: evenodd`) that cuts a hole matching the fire front, so as the fire expands, more of the scene is clipped away — all content (text, images, lines) burns with the page, no separate debris; (3) a scorched edge — a `<canvas>` overlay draws a radial-gradient fringe at the fire boundary to simulate charring.

Requirements: a `<canvas>` element for the burn-edge overlay, a noise function for organic fire-edge geometry, and an SVG clip-path with an evenodd fill rule for the inverted clip.

Fire geometry (deterministic noise):

```js
function noise(x) {
  var ix = Math.floor(x),
    fx = x - ix;
  var a = Math.sin(ix * 127.1 + 311.7) * 43758.5453;
  var b = Math.sin((ix + 1) * 127.1 + 311.7) * 43758.5453;
  var t = fx * fx * (3 - 2 * fx);
  return a - Math.floor(a) + (b - Math.floor(b) - (a - Math.floor(a))) * t;
}

function fireRadiusAtAngle(angle, progress) {
  var base = progress * maxRadius;
  return (
    base +
    noise(angle * 3 + progress * 4) * 50 +
    noise(angle * 8 + progress * 9) * 20 +
    noise(angle * 15 + progress * 15) * 8
  );
}
```

Incoming-scene timing: the incoming scene should NOT be visible during the burn. As the fire consumes the outgoing scene, black shows through the holes — this is the dramatic part, the viewer watching content being destroyed against blackness. At roughly 90% through the burn, the incoming scene fades in SLOWLY from black — the background first, then content staggered — using long, gentle fades (`power1.out`, 0.8–1.2s durations) so it feels like the new scene materializes from darkness, not a hard swap.

```js
// Scene 2 stays at opacity: 0 during the burn — black behind the fire
tl.set("#s2-title", { opacity: 0 }, T);
tl.set("#s2-subtitle", { opacity: 0 }, T);

// At 90% through, scene bg fades in slowly from black
var contentReveal = T + BURN_DURATION * 0.9;
tl.to("#scene2", { opacity: 1, duration: 1.2, ease: "power1.out" }, contentReveal);

// Content fades in staggered on top, even slower
tl.to("#s2-title", { opacity: 1, duration: 1.0, ease: "power1.out" }, contentReveal + 0.5);
tl.to("#s2-subtitle", { opacity: 1, duration: 0.8, ease: "power1.out" }, contentReveal + 0.7);
```

Content burns with the page — no falling debris. The clip-path on scene 1 IS the effect — as the fire shape expands, everything behind the fire edge (text, images, lines) disappears naturally. Don't clone elements, don't create falling debris. The content is part of the page being consumed. The scorched canvas edge provides the visual char line at the burn boundary.

Hide scene 1 via a `tl.set` at burn end — NEVER inside `onComplete`. Using `onComplete` to hide scene 1 is not reversible when scrubbing. Instead, use a `tl.set` at the exact burn end time:

```js
tl.to(
  burnState,
  {
    progress: 1,
    duration: BURN_DURATION,
    ease: "none",
    onUpdate: function () {
      var wp = burnState.progress;
      var scene1 = document.getElementById("scene1");
      if (wp <= 0) {
        scene1.style.clipPath = "none"; // fully visible when rewound
      } else if (wp < 1) {
        scene1.style.clipPath = buildClipPath(wp);
      }
      drawEdge(wp);
    },
    // NO onComplete — use tl.set instead
  },
  T,
);

// Hide scene1 at exact burn end — reversible via timeline
tl.set("#scene1", { opacity: 0 }, T + BURN_DURATION);
tl.set("#scene1", { clipPath: "none" }, T + BURN_DURATION);
```

The `onUpdate` handles the clip-path and canvas edge per frame; the `tl.set` handles the final hide, and GSAP automatically reverses it when scrubbing backward, restoring scene 1 to full opacity. The `onUpdate` callback is the key — it runs every frame to advance the clip-path and canvas edge in sync with the timeline.

## Reference Note: Example Files and Utility Scripts

The original source material for this document included a set of runnable, verbatim HTML/JS example files demonstrating full working compositions, plus a small set of Node.js utility scripts. These are not reproduced here (they are code artifacts, not prose techniques), but their existence and purpose are noted for completeness:

**Example compositions** (each a complete working HTML file exercising one or more of the rules/blueprints above in combination): a brand-reveal example combining an assemble-and-zoom camera push with a logo lockup; a comparison split-cards example; a concept-demo example pairing a decode reveal with a lateral camera pan into a live typing demo; a CTA morph-and-press example; a CTA example where category icons orbit and collapse toward a click point; a device page-scroll-with-spotlight example; a hook example built around a counter burst; a multi-phrase messaging example demonstrating dynamic content sequencing; a metric-driven video-to-text pivot example; a problem example built around mockup overwhelm; a social-proof example chaining a logo decode into an avatar-orbit proof sequence; a hook/brand-outro example demonstrating the ticker-takeover collision; and a workflow-approval example demonstrating a press-to-confirm UI interaction. Each corresponds to (or closely informed) one of the blueprints or rules documented above — where a rule or blueprint above cites a specific reference example inline, that reference is preserved in this document's prose.

**Utility scripts** (Node.js, for auditing already-authored compositions rather than authoring new ones): a timeline-analysis script reads every GSAP timeline registered on a composition's shared timeline registry, enumerates its tweens, samples element bounding boxes across time, computes choreography-quality flags (dead zones, stagger consistency, lifecycle warnings), and outputs a structured JSON report — useful for auditing a finished composition's pacing and coverage after authoring. A companion sampling module implements the underlying per-frame bounding-box sampling logic. A package-resolution helper script locates required helper packages from the current project first, falling back to bootstrapping a pinned bundled version when run outside its native install context. Each of these has an accompanying automated test file. None of this scripting layer is reproducible or runnable outside the original framework's own toolchain — it is noted here only so the existence and purpose of these files is not silently lost from the record.

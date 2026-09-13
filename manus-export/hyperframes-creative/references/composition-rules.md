# Composition Rules

Named composition patterns for HyperFrames video projects, plus the video-medium rules that govern
how any frame — patterned or not — should be composed. See `../SKILL.md` for when to apply these.

## Video Frames Are Not Web Pages

Use these rules for design-led compositions while respecting the requested format, brand, and
scope. Minimal technical compositions and intentionally sparse formats may need less detail.

### The Design Spec Is Brand, Not Layout

The design spec (a project's `frame.md` or `design.md`) defines what the brand looks like: colors,
fonts, personality, constraints. It does NOT define how to compose a video frame. Use brand colors
at video-appropriate intensity — not at web-UI opacity.

**Strict from the design spec:** hex values (including background color), font families, weight
relationships, Do's and Don'ts. If the spec chose a light canvas, use a light canvas. If it chose
dark, use dark. Do not override the palette.

**Adapt for video:** type sizes, spacing, decorative opacity, border weight, component treatments.
A web UI card at `border: 1px solid #e2e3e6` with `box-shadow: 0 2px 4px rgba(0,0,0,0.06)` is
invisible on video. The brand color is sacred; the application is yours.

### Density

Choose density from the message and format. A brand or sizzle frame often needs several visual
roles to feel produced; a lower-third, logo sting, or static title may need only a few.

For a scene that should feel layered, plan these roles:

- **Background treatment** — radial glow, oversized ghost type, color panel, grain, grid, or an
  intentionally flat field justified by the concept.
- **Midground content** — the actual message. Cards, stats, code blocks, images.
- **Foreground accents** — dividers, labels, data bars, registration marks, monospace metadata.
  The details that make it feel produced, not generated.

For produced marketing frames, roughly 6–10 visual roles can be a useful starting point, not a
contract. Add decoration only when it reinforces hierarchy, motion, or the concept. Decorative
treatment must not become new user-facing content, new scenes, or unrequested claims.

### Color Presence

Muted is fine. Flat is not. Every scene should have at least one color that pulls the eye.

- Brand accent should be VISIBLE — not a 5% opacity glow lost in compression. 15-25% for
  atmospheric, full saturation for focal elements.
- **Light canvases work differently than dark.** On dark: accent glows pop naturally. On light:
  use bolder borders (2px+ solid), stronger structural elements (rules, dividers), and
  full-saturation accent hits. Light backgrounds need texture (subtle grain, patterns) to avoid the
  "blank slide" feel. Don't switch to dark — make light cinematic.
- **No full-screen linear gradients on dark backgrounds.** They band visibly under H.264
  compression. Use a radial gradient, a solid fill, or solid + localized glow instead.
- Tint neutrals toward the brand hue. Dead gray reads as undesigned.

### Scale

Web sizes are invisible on video. Everything scales up.

| Element            | Web     | Video    |
| ------------------ | ------- | -------- |
| Headlines          | 32-48px | 64-120px |
| Body text          | 14-16px | 28-42px  |
| Labels             | 12px    | 18-24px  |
| Decorative opacity | 3-8%    | 12-25%   |
| Borders            | 1px     | 2-4px    |
| Padding            | 16-32px | 60-140px |

If a font-size under 24px shows up in a video composition, justify it. If decorative opacity is
under 10%, it's invisible.

### Motion Intensity

Subtle reads as static at 30fps. Err toward more movement than feels safe.

- Every decorative element should have ambient motion: breathe, drift, pulse, orbit. Static
  decoratives feel dead.
- Vary motion per scene — don't repeat the same ambient pattern.
- Scene entrances should use 3+ different eases and directions. If every element enters from
  `y: 30, opacity: 0`, the scene has no choreography.

### Frame Composition

- **Two focal points minimum.** The eye needs somewhere to travel.
- **Fill the frame.** Hero text: 60-80% of frame width.
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web
  layout pattern.
- **Split frames.** Data panel left, content right. Top bar with metadata, full-width below.
  Zone-based layouts over centered stacks.
- **Structural elements.** Rules, dividers, border panels. They create visual paths and animate
  well (`scaleX: 0` → `1`).

## Named Composition Patterns

### Picture-in-Picture (Video in a Frame)

Animate a wrapper div for position/size. The video fills the wrapper. The wrapper has NO data
attributes.

```html
<div
  id="pip-frame"
  style="position:absolute;top:0;left:0;width:1920px;height:1080px;z-index:50;overflow:hidden;"
>
  <video
    id="el-video"
    data-start="0"
    data-duration="60"
    data-track-index="0"
    src="talking-head.mp4"
    muted
    playsinline
  ></video>
</div>
```

```js
tl.to(
  "#pip-frame",
  { top: 700, left: 1360, width: 500, height: 280, borderRadius: 16, duration: 1 },
  10,
);
tl.to("#pip-frame", { left: 40, duration: 0.6 }, 30);
```

### Text Behind Subject (transparent webm overlay)

Put a headline behind a presenter so their silhouette occludes the text. Requires a transparent
cutout produced by a background-removal pass on the source video (e.g. `presenter.mp4` →
`presenter.webm`).

Three layers, plus one critical rule:

```html
<!-- z=1 base — full opaque mp4 (lobby + presenter), always visible -->
<video
  id="cf-base"
  data-start="0"
  data-duration="6"
  data-media-start="0"
  data-track-index="0"
  src="presenter.mp4"
  muted
  playsinline
></video>

<!-- z=2 headline — visible the whole time -->
<h1
  id="cf-headline"
  style="position:absolute;top:50%;left:50%;
     transform:translate(-50%,-50%); z-index:2; font-size:220px; font-weight:900;
     color:#fff; text-shadow:0 6px 32px rgba(0,0,0,.55); clip-path:inset(0 0 100% 0);"
>
  MAKE IT IN HYPERFRAMES
</h1>

<!-- z=3 cutout — same source, alpha around presenter, hidden until the cut -->
<!-- WRAPPER has the opacity, NOT the video itself (see rule below). -->
<div class="cutout-wrap" style="position:absolute;inset:0;z-index:3;opacity:0">
  <video
    id="cf-cutout"
    data-start="0"
    data-duration="6"
    data-media-start="0"
    data-track-index="1"
    src="presenter.webm"
    muted
    playsinline
  ></video>
</div>
```

```js
const tl = gsap.timeline({ paused: true });
const CUT = 3.3;

// Reveal headline early
tl.to("#cf-headline", { clipPath: "inset(0 0 0% 0)", duration: 0.6, ease: "expo.out" }, 0.25);

// At the cut, flip the cutout wrapper visible — the presenter's silhouette
// punches through the headline.
tl.set(".cutout-wrap", { opacity: 1 }, CUT);

// Sentinel: extend timeline to the composition's full duration so the
// renderer doesn't bail past the last meaningful tween.
tl.set({}, {}, 6);

window.__timelines["cover-flip"] = tl;
```

**Why a wrapper div, not opacity on the video itself?**

The framework forces `opacity: 1` on any element with `data-start`/`data-duration` while it's
"active" — that's how it manages clip lifecycles. A CSS `opacity: 0` on the video element is
silently overwritten. Wrap the video in a div with no `data-*` attributes; the wrapper is owned by
CSS/GSAP.

**Why both videos at `data-start="0"`?**

So both decode in sync from t=0. Late-mounting the cutout (`data-start=3.3`) makes the renderer do
a seek + decoder warm-up at mount, which can land a frame off the base mp4 — visible as a
one-frame jitter at the cut.

**Color match:** the default "balanced" background-removal quality setting keeps the cutout's RGB
nearly identical to the source video — minimal edge halo or color shift when overlaid. Use the
higher "best" quality for hero shots; only drop to a fast/lower-quality setting when the cutout
sits over a different background and file size matters.

### Title Card with Fade

```html
<div
  id="title-card"
  data-start="0"
  data-duration="5"
  data-track-index="5"
  style="display:flex;align-items:center;justify-content:center;background:#111;z-index:60;"
>
  <h1 style="font-size:64px;color:#fff;opacity:0;">My Video Title</h1>
</div>
```

```js
tl.to("#title-card h1", { opacity: 1, duration: 0.6 }, 0.3);
tl.to("#title-card", { opacity: 0, duration: 0.5 }, 4);
```

### Slide Show with Section Headers

Use separate elements on the same track, each with its own time range. Slides auto-mount/unmount
based on `data-start`/`data-duration`.

```html
<div class="slide" data-start="0" data-duration="30" data-track-index="3">...</div>
<div class="slide" data-start="30" data-duration="25" data-track-index="3">...</div>
<div class="slide" data-start="55" data-duration="20" data-track-index="3">...</div>
```

### Top-Level Composition Example

```html
<div
  id="comp-1"
  data-composition-id="my-video"
  data-start="0"
  data-duration="60"
  data-width="1920"
  data-height="1080"
>
  <!-- Primitive clips -->
  <video
    id="el-1"
    data-start="0"
    data-duration="10"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <video
    id="el-2"
    data-start="el-1"
    data-duration="8"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <img id="el-3" data-start="5" data-duration="4" data-track-index="1" src="..." />
  <audio id="el-4" data-start="0" data-duration="30" data-track-index="2" src="..." />

  <!-- Sub-compositions loaded from files -->
  <div
    id="el-5"
    data-composition-id="intro-anim"
    data-composition-src="compositions/intro-anim.html"
    data-start="0"
    data-track-index="3"
  ></div>

  <div
    id="el-6"
    data-composition-id="captions"
    data-composition-src="compositions/caption-overlay.html"
    data-start="0"
    data-track-index="4"
  ></div>

  <script>
    // Just register the timeline — framework auto-nests sub-compositions
    const tl = gsap.timeline({ paused: true });
    window.__timelines["my-video"] = tl;
  </script>
</div>
```

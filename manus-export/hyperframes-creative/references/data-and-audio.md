# Data and Audio

Stats/infographic presentation rules and audio-reactive animation mapping for HyperFrames video
compositions. See `../SKILL.md` for when to consult this file.

## Data in Motion

Light guidance for data and stats in video compositions. House style (`design-system.md`) handles
general aesthetics; this section addresses data-specific pitfalls only.

### Visual Continuity

When successive stats belong to the same concept (Q1 → Q2 → Q3 → Q4, or three metrics for the same
product), keep them in the same visual space with the same aesthetic. Only the VALUE changes. An
aesthetic change should signal a new concept, not just a new number.

### Numbers Need Visual Weight

A number on its own floats in empty space. Pair every metric with a visual element that gives it
presence — a proportional fill bar, a background color shift, a shape that represents the value, a
progress ring. The visual doesn't need to be a chart — it just needs to fill the frame and make the
data feel tangible rather than just text on a background.

### Avoid Web Patterns

- **No pie charts** — hard to compare, looks like a slide deck.
- **No multi-axis charts** — the viewer can't study intersections in a 3-second window.
- **No 6-panel dashboards** — 2-3 related metrics side-by-side is fine, 6+ is a web pattern.
- **No gridlines, tick marks, or legends** — visual noise that adds nothing in motion.
- **No chart-library output** — build data visuals with the animation engine plus SVG/CSS, not a
  charting library.

## Audio-Reactive Animation

Drive visuals from music, voice, or sound. Any animatable property can respond to pre-extracted
audio data.

### Audio Data Format

```js
var AUDIO_DATA = {
  fps: 30,
  totalFrames: 900,
  frames: [{ bands: [0.82, 0.45, 0.31, ...] }, ...]
};
```

- `frames[i].bands[]` — frequency band amplitudes, 0-1. Index 0 = bass, higher = treble.
- Each band normalized independently across the full track.

### Mapping Audio to Visuals

| Audio signal              | Visual property                     | Effect                       |
| --------------------------- | -------------------------------------- | -------------------------------- |
| Bass (bands[0])              | `scale`                                 | Pulse on beat                    |
| Treble (bands[12-14])        | `textShadow`, `boxShadow`               | Glow intensity                   |
| Overall amplitude            | `opacity`, `y`, `backgroundColor`       | Breathe, lift, color shift       |
| Mid-range (bands[4-8])       | `borderRadius`, `width`                 | Shape morphing                   |

Any tweenable property works — `clipPath`, `filter`, SVG attributes, CSS custom properties.

### Content, Not Medium

Audio provides timing and intensity. The visual vocabulary comes from the narrative.

**Never add:** equalizer bars, spectrum analyzers, waveform displays, musical notes clip art,
generic particle systems, rainbow color cycling, strobing white on beats, abstract pulsing orbs.

**Instead:** let content guide the visual and audio drive its behavior. Bass makes warmth swell.
Treble sharpens contrast. The visual choice comes from "what does this piece feel like?"

### Sampling Pattern

Audio reactivity requires per-frame sampling via a `for` loop attached to the timeline, not a
single tween:

```js
// ✅ Correct — sample every frame
for (var f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    (function (frame) {
      return function () {
        draw(frame);
      };
    })(AUDIO_DATA.frames[f]),
    [],
    f / AUDIO_DATA.fps,
  );
}

// ❌ Wrong — single tween, doesn't react to audio
gsap.to(".el", { scale: 1.2, duration: totalDuration });
```

Without per-frame sampling, the composition doesn't actually react to audio.

### textShadow Gotcha

`textShadow` on a parent container with semi-transparent children (e.g., inactive caption words at
`rgba(255,255,255,0.3)`) renders a visible glow rectangle behind all children. Fix: apply `scale`
to the container for beat pulse, but apply `textShadow` to individual active words only.

### Guidelines

- **Subtlety for text** — 3-6% scale variation, soft glow. Heavy pulsing makes text unreadable.
- **Go bigger on non-text** — backgrounds and shapes can handle 10-30% swings.
- **Match the energy** — corporate = subtle; music video = dramatic.
- **Deterministic** — pre-extracted data, no live Web Audio API, no runtime analysis.

### Constraints

- All audio data must be pre-extracted (use `scripts/extract-audio-data.py` from this skill).
- No `Math.random()` or `Date.now()` in the sampling logic.
- Audio reactivity runs on the same animation timeline as everything else in the scene.

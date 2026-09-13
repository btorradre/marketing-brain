# Captions — authoring, motion, and transcript handling

Before authoring captions, confirm the transcript came from the correct language setting (see `references/transcription.md` → Language Rule) and passed the mandatory quality check (see "Transcript Handling" below).

## Style detection (when no style is specified)

Read the full transcript before choosing a caption style, and evaluate four dimensions:

1. **Visual feel** — corporate → clean; energetic → bold; storytelling → elegant; technical → precise; social → playful.
2. **Color palette** — dark + bright for energy; muted for professional; high contrast for clarity; one accent color as the norm.
3. **Font mood** — heavy/condensed for impact; clean sans-serif for modern; rounded for friendly; serif for elegance.
4. **Animation character** — scale-pop for punchy; gentle fade for calm; word-by-word reveal for emphasis; typewriter for technical.

## Per-word styling

Scan the transcript for words that deserve distinct treatment:
- **Brand/product names** — larger size, a unique/consistent color
- **ALL-CAPS words** — scale boost, a flash, or an accent color
- **Numbers/statistics** — bold weight, accent color
- **Emotional keywords** — exaggerated animation (overshoot, bounce)
- **Calls-to-action** — highlight, underline, or a color pop
- **"Marker" style highlights** (beyond simple color) — a highlight sweep, circle, burst, scribble, or sketch-out effect over a word, used for standout emphasis words

## Script-to-style mapping

| Tone | Font mood | Animation | Color | Size |
|---|---|---|---|---|
| Hype/launch | Heavy condensed, very bold weight | Scale-pop, springy overshoot ease, 0.1-0.2s | Bright on dark | 72-96px |
| Corporate | Clean sans, semi-bold/bold | Fade+slide, smooth ease-out, 0.3s | White/neutral, muted accent | 56-72px |
| Tutorial | Mono/clean sans, medium weight | Typewriter/fade, 0.4-0.5s | High contrast, minimal | 48-64px |
| Storytelling | Serif/elegant, regular/medium weight | Slow fade, gentle ease-out, 0.5-0.6s | Warm, muted tones | 44-56px |
| Social | Rounded sans, bold/extra-bold | Bounce, elastic ease-out, word-by-word | Playful, colored pill backgrounds | 56-80px |

## Word grouping (how many words appear on screen at once)

- High energy: 2-3 words, quick turnover
- Conversational: 3-5 words, natural phrases
- Measured/calm: 4-6 words, longer groups

Break groups on sentence boundaries, on pauses of 150ms or more, or when a group hits its max word count.

## Positioning

- Landscape (1920×1080): bottom 80-120px, centered
- Portrait (1080×1920): lower-middle, roughly 600-700px from the bottom, centered
- Never cover the subject's face
- Position captions with absolute (not flow/relative) placement
- Only one caption group should be visible at a time

## Text-overflow prevention

Measure text against the actual rendered font before committing a font size, and shrink to fit within a max width rather than letting it overflow or get clipped. Reasonable defaults: max width ~1600px landscape / ~900px portrait, base font size ~78px, minimum font size ~42px, step down in ~2px increments while it overflows.

If any per-word emphasis uses a scale multiplier greater than 1.0, reduce the effective max width by that scale factor so the emphasis effect has headroom without clipping.

In your layout/CSS: give the caption container an explicit max-width and an explicit height, use absolute positioning, and make sure overflow is not hard-clipped — clipping cuts off scaled emphasis words and glow effects. Avoid centering techniques that can clip at the composition's edges (e.g. centering by combining `left: 50%` with a horizontal transform is a common source of this) — prefer a full-width, internally-centered container instead.

## Caption exit guarantee

Every caption group must be reliably removed from view after its exit animation finishes — don't just animate opacity down and leave it there; explicitly force it to a fully-hidden, non-interactive state at the end of its animation (opacity 0 *and* visibility hidden, not just opacity).

Consider a self-check pass after building the caption timeline: at each group's end time, verify it's actually invisible, and log a warning if it isn't — this catches captions that silently linger on screen past their intended exit.

## Fonts

Don't assume a font family you can see locally will render correctly wherever the final video gets rendered — a render pipeline running in an isolated/headless environment may have no fonts installed beyond a small built-in set. Any custom/brand font, or any non-Latin script family (CJK, Devanagari, etc.), needs to be explicitly embedded/shipped as a real font file with the project; otherwise the render will silently fall back to a generic font.

## Reusable caption "styles" as a starting point

Rather than building every caption look from scratch, maintain (or draw on) a small library of proven caption presentation styles as starting templates:

- TikTok-style word highlight (social/high-energy)
- Karaoke pill (music/lyric videos)
- Cinematic editorial emphasis (documentary/storytelling)
- Glitch/cyber (tech/gaming)
- Full-screen kinetic slam (hype/announcements)
- Neon glow (night/club aesthetics)
- Neon multi-color accent (colorful/playful)
- Wipe reveal (clean/modern)
- Gradient fill (vibrant/eye-catching)
- Matrix-style decode (sci-fi/tech reveals)
- Emoji pop (social/casual)
- Parallax layers (depth/cinematic)
- Particle burst (celebration/impact keywords)
- Bold texture fill (dramatic)
- Weight-shift (elegant/typographic)

One more general-purpose technique worth keeping in your toolkit: an **auto-inverting text treatment** (using a blend mode like "difference" against the background) for captions that need to stay legible over an unpredictable or busy background.

Caption presets should generally be built as transparent overlays; if the underlying footage is bright or busy, add a separate semi-transparent dark contrast layer *behind* the caption text rather than baking a background into the caption style itself.

## General constraints

- Caption timing/animation should be **deterministic** — avoid randomness or wall-clock-based timing so the same input always renders the same output (important for reproducible/re-renderable pipelines).
- Sync everything to the actual transcript timestamps.
- Exactly one caption group visible at a time.
- Every group needs a hard, explicit "kill" at its end time (see Caption Exit Guarantee above).

---

## Motion & animation

Pick an animation technique combination based on the transcript's detected energy level, then implement it with a standard keyframe/timeline animation approach — any tweening/animation library capable of the same primitives (entrance, per-word highlight, exit) works; the technique is library-agnostic.

### Technique selection by energy level

| Energy level | Highlight style | Exit style | Cycle pattern |
|---|---|---|---|
| High | Karaoke-style word highlight with accent-color glow + scale pop | Scatter or drop | Alternate highlight styles every 2 groups |
| Medium-high | Karaoke highlight with color pop | Scatter or collapse | Alternate every 3 groups |
| Medium | Karaoke highlight (subtle, white only) | Fade + slide | Alternate every 3 groups |
| Medium-low | Karaoke highlight (minimal scale change) | Fade | Single style, vary the easing per group |
| Low | Karaoke highlight (warm tones, slow transition) | Collapse | Alternate every 4 groups |

All energy levels use a karaoke-style word-by-word highlight as the baseline; the difference is intensity. High energy: add accent color, a glow effect, and roughly a 15% scale pop on the active word. Low energy: a gentle white color shift with only ~3% scale change.

**Emphasis words always break the pattern.** A word flagged as emphasis (an emotional keyword, ALL-CAPS, a brand name) should get a visibly stronger treatment than surrounding words — larger scale, an accent color, a springier/overshoot easing — to create contrast against the baseline rhythm.

**Marker-style highlight modes** layer on top of the karaoke baseline for standout emphasis words: a highlight sweep, a circle drawn around the word, a burst effect, a scribble, or a sketch-out effect. Match the mode to the energy level — burst for hype, circle for key terms, a plain highlight for standard emphasis, scribble for subtle emphasis. Cycle marker modes across groups for visual variety rather than repeating the same one throughout.

### Audio-reactive captions are mandatory when the source audio is music

Vocals over instrumentation, beats, or any musical content — captions over music that don't react to the audio look disconnected. Even a low-energy ballad should get subtle bass-driven pulse and treble-driven glow.

The general technique:

1. Extract a frame-by-frame audio-energy profile from the track (frequency-band energy per frame, e.g. an FFT-based band-energy extraction at a fixed frame rate).
2. For each caption group's time range, find the peak "bass"-band and peak "treble"-band energy within that window.
3. Modulate that group's entrance animation using those peak values — e.g. scale up slightly more and add more glow for a louder moment, and reset those values back to baseline at the group's exit so the effect doesn't persist onto quieter groups.
4. Do this modulation **at animation-build time, not during playback** — i.e., bake the audio-driven values into the keyframes you construct up front, rather than reading audio data on every rendered frame. This keeps the render deterministic and avoids timing/async issues.
5. Keep the effect subtle — roughly 3-6% scale variation and a soft glow. Heavy pulsing makes text unreadable.

### Combining techniques

Don't reuse the exact same highlight animation on every single caption group — cycle through a small set of variations by group index so the piece doesn't feel monotonous. Avoid stacking multiple competing animations on the same word at the same instant. Vary the technique across groups to track the content's pacing changes (e.g. more energetic treatment during a fast-talking section, calmer during a pause).

---

## Transcript handling

### Supported input formats

A captioning pipeline should be able to normalize:

| Format | Typical extension | Word-level timing? |
|---|---|---|
| Word-level ASR output (e.g. whisper.cpp-style JSON) | .json | Yes |
| Cloud ASR API output with word timestamps (e.g. OpenAI Whisper API with `timestamp_granularities: ["word"]`) | .json | Yes |
| SRT subtitles | .srt | No (phrase-level only) |
| VTT subtitles | .vtt | No (phrase-level only) |
| A pre-normalized flat word array | .json | Yes |

Word-level timestamps produce meaningfully better captions than phrase-level subtitle formats, because only word-level data supports per-word animation effects (karaoke highlighting, per-word emphasis, etc.).

### Transcript quality check — mandatory, never skip

After every transcription pass, read the transcript and check for these failure signals before building captions from it:

| Signal | Example | Likely cause |
|---|---|---|
| Music-note / garbage tokens (e.g. "♪", replacement-character glyphs) | a word entry whose text is just a music note or a mangled character | The model detected music, not speech |
| Garbled / nonsense words | "Do a chin", "Get so gay", "huh" | The model misheard lyrics or background noise |
| Long stretches with no real words | 20+ seconds of only music-note tokens | Likely an instrumental section (expected) — but a high overall ratio means real speech is being missed |
| Repeated filler | many "huh"/"uh"/"oh" entries in a row | The model is hallucinating on musical/noisy audio |
| Very short word spans | a word whose end-minus-start duration is under ~0.05s | Unreliable timestamp alignment |

### Automatic retry rule

If more than **20%** of transcript entries are music-note/garbage tokens, or the transcript is otherwise full of obvious nonsense, treat the transcription as **failed**. Do not build captions from it. Instead:

1. Retry with a larger/more capable model (if the first attempt used a small model).
2. If a larger model still fails (still >20% garbage or still nonsensical), the audio is likely too noisy for automatic transcription — fall back to either manually-sourced lyrics/text as an SRT/VTT file, or a stronger external transcription API.
3. **Always clean the transcript** before building captions from it, regardless of which model produced it — filter out music-note/garbage tokens and any entry whose text is a single non-word character. Only real words should ever reach the caption-building step. A reasonable cleaning rule: drop any entry whose text is empty or whitespace-only, drop any entry that's purely a music-note-class character, and drop very short filler words (like "huh"/"uh"/"um"/"ah"/"oh") if their duration is under ~0.1s.

Illustrative cleaning logic:

```js
var words = raw.filter(function (w) {
  if (!w.text || w.text.trim().length === 0) return false;
  if (/^[♪�♪♫♬♭♮♯]+$/.test(w.text)) return false;
  if (/^(huh|uh|um|ah|oh)$/i.test(w.text) && w.end - w.start < 0.1) return false;
  return true;
});
```

### Using an external transcription API for best accuracy

See `references/transcription.md` for the OpenAI Whisper API and Groq Whisper API curl recipes — both return word-level timestamps and can be imported and normalized into the flat word-array shape used throughout the pipeline.

### If no transcript exists yet

Check for an existing transcript, SRT, or VTT file first. If none exists, run a transcription pass (see `references/transcription.md`, picking the model by content type), then run the quality check above before proceeding.

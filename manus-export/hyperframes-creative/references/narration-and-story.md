# Narration and Story

Narration pacing/tone, value-first story-spine doctrine, and per-beat direction + rhythm planning
for HyperFrames video compositions. See `../SKILL.md` for when to consult this file.

## Narration and Script

How to write narration scripts for video compositions with voiceover or TTS.

### Pacing

- **2.5 words per second** is natural speaking pace.
- 15s = ~37 words. 30s = ~75 words. 60s = ~150 words.
- Leave room for pauses. Silence between sentences is a feature, not dead air.
- The script should feel SHORTER than the video — visual breathing room matters.

### Tone

Write like a person, not a brochure:

- Use contractions: "it's", "you'll", "that's", "we've"
- Vary sentence length — short punchy phrases mixed with longer flowing ones
- Read it out loud. If it sounds robotic, rewrite it
- Avoid jargon unless the audience expects it

### Number Pronunciation

Write what the voice should say. TTS reads literally.

| In the product | Write in script as                |
| --------------- | ---------------------------------- |
| 135+             | more than one hundred thirty five   |
| $1.9T            | nearly two trillion dollars         |
| 99.999%          | ninety nine point nine percent      |
| 200M+            | over two hundred million            |
| 10x              | ten times                           |
| API              | A P I                               |
| stripe.com       | stripe dot com                      |

The visual can show the exact figure while the voice rounds it.

### Structure

For product videos:

1. **Hook** — what's surprising or impressive about this product? A bold claim, a provocative
   question, a contrast, or a striking number. This is the opening line. Vary the hook type — don't
   default to a stat every time.
2. **Story** — what does the product do? Who uses it? Keep it concrete.
3. **Proof** — stats, customer names, social proof. Real numbers from the product.
4. **CTA** — what should the viewer do?

Not every video needs all four. A 15-second social ad might be Hook + Proof + CTA. A 60-second
product tour uses all four with more Story.

### The Opening Line

The most important sentence in the video. It must create tension, curiosity, or surprise in the
first 3 seconds.

Patterns that work:

- **A bold claim**: "The financial infrastructure that powers the internet economy."
- **A question that provokes**: "What if your database could think?"
- **A contrast**: "Your AI agent already knows how to make videos. It just needs the right
  format."
- **A number that shocks**: "Nearly two trillion dollars." (Use sparingly — not every video should
  open with a stat.)

If the opening is generic ("Welcome to [brand]" / "Introducing our product"), start over.

### Example

From a 62-second product-launch video reference (~140 words for 62 seconds — that's 2.3 words/sec,
leaving room for pauses and visual breathing):

```
Your AI agent already knows how to make videos.
It just needs the right format.

This is Hyperframes. An open source framework. HTML in, video out.

A div is a keyframe. Data attributes are your timeline.
CSS is your look. G-Sap is your animation engine.

Anything a browser can render can be a frame in your video.

CSS animations. G-Sap. Lottie. Shaders. Three.js.

Drop in music, sound effects, footage — it all composes together.

No new framework for the agent to learn.
Just HTML.

The agent writes it. The renderer captures every frame as MP4.
It's deterministic. Identical outputs, every time.

Give your agent the CLI. Tell it what to make.
Watch it build.

Hyperframes. Go make something.
```

## Story Spine — Value-First Narrative Doctrine

Applies to narrated, story-driven creation workflows — a product-launch video, a PR/changelog
video, a faceless explainer, or any general video where the piece tells a story. It does NOT apply
to a music-driven video (the track drives the arc), a pure motion-graphics piece (no narration —
motion is the message), a captioned recut of existing footage or a talking-head recut (the
footage's story is already fixed), or a slideshow (the presenter owns the story). Do not force
these rules onto an exempt format.

Whatever produces the piece owns its own archetypes, beat sequences, and frame vocabulary. This
doctrine owns three cross-format rules about **order and justification** — the reverse iceberg:
lead with why it's valuable, not with what it is or how it was made.

### 1. The hook speaks the viewer's language

The first beat answers "why should I care" in outcome language — what the viewer gains, avoids, or
finally understands. Subject-internal vocabulary is banned in the hook: file/function/API names
for a code change; a feature list for a product; the source article's section headings for an
explainer. Numbers are welcome only when they carry stakes ("40% faster cold starts"), never
inventory ("23 files changed").

### 2. Reverse iceberg — value before evidence

The value claim (the piece's core message) lands by the second beat. Everything after it is
evidence in service of that claim — the diff, the mechanism, the feature demo, the screenshots.
Implementation is the footnote of the story, not the spine.

Self-check on the finished beat list:

- Delete every evidence beat — the remaining beats must still state the value on their own.
- Delete the value beats — if the video still seems to work, it was a feature tour / diff readout,
  not a story.

Structure is value-first; the voice stays whatever the format prescribes (a PR/changelog video
keeps its plain, no-hype developer voice — leading with value is an ordering decision, not a
marketing register).

### 3. The storyboard is a proposal, not a listing

When a plan is presented for approval before construction begins (a checkpoint gate):

- Open by echoing the strategy line: "This video tells [audience] that [message]."
- Present the frames as a markdown table, one row per frame:

  | Frame              | Beat        | On screen                                                | Why                                |
  | ------------------- | ----------- | ---------------------------------------------------------| ------------------------------------ |
  | 01 — Not anymore    | hook · 9s    | States the old pain and resolves it in the same breath.   | Lands the value claim in beat 1     |

  Why is the frame's job in the story (traced back to the message) — a frame whose why cannot be
  traced to the message is a frame to cut, not to decorate.

- Recommendations keep their receipts: the archetype choice, the beat count, and any beat the
  reviewer might question each state their basis.

The proposal shape — echo line → frame table → style/duration footer → "approve or adjust" — is
the cheapest place to iterate: a frame change here costs 30 seconds; the same change after build
costs minutes.

## Beat Direction

How to plan and direct individual scenes (beats) in a multi-scene composition. Read before writing
any multi-scene video.

### Per-Beat Direction

Each beat is a WORLD, not a layout. Before writing CSS specs and GSAP instructions, describe what
the viewer EXPERIENCES. The difference between a great storyboard and a mediocre one:

**Mediocre:** "Dark navy background. '$1.9T' in white, 280px. Logo top-left. Wave image
bottom-right."

**Great:** "Camera is already mid-flight over a vast dark canvas. The gradient wave sweeps across
the frame like aurora borealis — alive, shifting. '$1.9T' SLAMS into existence with such force the
wave ripples in response. This isn't a slide — it's a moment."

The first describes pixels. The second describes an experience. Write the second, then figure out
the pixels.

Each beat should have:

**Concept** — the big idea for this beat in 2-3 sentences. What visual WORLD are we in? What
metaphor drives it? What should the viewer FEEL? This is the most important part — everything else
flows from it.

**Mood direction** — cultural and design references, not hex codes:

- "Geometric, rhythmic, precise. Think Josef Albers or Bauhaus color studies."
- "Warm workspace. Nice notebook energy, not technical blueprint."
- "Cinematic title sequence. The kind of opening where you lean forward."

**Animation choreography** — specific motion verbs per element, not "it animates in" but HOW.
Verbs come from the beat's concept and content, not from an energy bucket. A wellness brand's
"slow" beat might still have something that DROPS if the content is about letting go. A stats beat
might FLOAT if the brand's identity is weightless.

The vocabulary of motion verbs (organized by physical character, not by energy level):

- **Impact / weight:** SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS, DROPS (with force)
- **Directional / deliberate:** SLIDES, PUSHES, PULLS, WIPES, CUTS
- **Reveals / builds:** DRAWS, FILLS, GROWS, EXPANDS, ASSEMBLES, COUNTS UP
- **Organic / ambient:** FLOATS, DRIFTS, BREATHES, PULSES, ORBITS, MORPHS
- **Mechanical / precise:** TYPES ON, CLICKS, LOCKS IN, SNAPS, STEPS

Every element gets a verb. If the verb can't be named, the element is not yet designed. The verb
should follow from the beat's concept — not from a lookup of what "high energy" or "low energy"
beats use.

For text elements specifically, a deterministic named effect can be specified by ID (e.g.
`typewriter`, `kinetic-center-build`, `soft-blur-in`) instead of inventing timing from scratch —
the full text-effect vocabulary is owned by the animation-focused part of the pipeline.

**Transition** — how this beat hands off to the next. Specify the type and parameters.

When to pick which:

| Choose a shader-style transition for                                              | Choose a CSS-style transition for                                                    | Choose a hard cut for                                            |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments      | Continuous camera-motion beats where the scene feels like one move broken into cuts       | Rapid-fire lists, percussive edits on the beat, comedic timing        |
| Any moment the music/VO punctuates with a downbeat or SFX hit                        | Beats that ease from one composition into the next with shared motion vocabulary          | Sequences of 3+ quick tempo-matched switches                          |
| Brand moments where the transition itself IS the visual                              | Minimal/editorial pacing                                                                  | Anytime a 0.3-0.8s transition would feel too slow                     |

Rule of thumb: if the beat is the centerpiece of the video, use the more elaborate shader-style
transition into it. If the beat is connective tissue, a simple crossfade is fine. A brand reel of
5-7 beats usually wants 1-2 elaborate transitions (the hero reveal + the CTA) — too many flatten
their impact.

Named transition patterns, GPU shader effects, and their full parameter catalog belong to the
animation-focused part of the pipeline — reference it by category (push/slide, scale/zoom,
radial/clip, 3D, dissolve, cover/blinds, light, distortion, blur, mechanical, grid, destruction)
rather than reinventing timing here. Quick reference for common picks:

- **Velocity-matched upward**: exit `y:-150, blur:30px, 0.33s power2.in` → entry `y:150→0,
  blur:30px→0, 1.0s power2.out`
- **Whip pan**: exit `x:-400, blur:24px, 0.3s power3.in` → entry `x:400→0, blur:24px→0, 0.3s
  power3.out`
- **Blur through**: exit `blur:20px, 0.3s` → entry `blur:20px→0, 0.25s power3.out`
- **Zoom through**: exit `scale:1→1.2, blur:20px, 0.2s power3.in` → entry `scale:0.75→1,
  blur:20px→0, 0.5s expo.out`
- **Hard cut / smash cut**: instant, for rapid-fire sequences

Timing presets: snappy (0.2s), smooth (0.4s), gentle (0.6s), dramatic (0.5s), instant (0.15s),
luxe (0.7s).

Custom GLSL shaders, shader code adapted from elsewhere, or entirely custom CSS transitions
combining clip-path/transforms/filters in new ways are all fair game if the storyboard calls for
an effect that doesn't exist yet — the framework renders anything a browser can run.

**Depth layers** — what's in foreground, midground, and background. Every beat should have at
least 2 layers: "BG: dark navy fill + subtle radial glow. MG: stat cards with drop shadow. FG:
brand logo bottom-right."

**SFX cues** — what sounds at what moment: "On the capture pulse — a soft, warm analog shutter
click." "Left side carries a faint low drone. On fold: drone cuts. Silence. Then a single clean
chime."

### Rhythm Planning

Before writing HTML, declare the scene rhythm: which scenes are quick hits, which are holds, where
do the elaborate transitions land, where does energy peak. Name the pattern —
fast-fast-SLOW-fast-SHADER-hold — before implementing.

Derive the rhythm from the storyboard and the brand, not from a lookup. A 15-second social ad for
an architectural firm and a 15-second social ad for a gaming brand have different rhythms — both
are 15 seconds, but one is slow-reveal-hold-CTA and the other is rapid-fire-SLAM-hook. Video type
sets constraints (duration, approximate beat count); the brand and content determine whether those
beats are slow or fast, sparse or dense, dramatic or controlled.

Questions that drive rhythm decisions:

- What emotional journey should the viewer take? Where is the peak moment?
- Where does the narration land its heaviest emphasis? That's usually where energy should peak.
- What does the brand's own visual pacing suggest — unhurried or urgent?
- How many beats can the duration actually support without feeling rushed or padded?

A social ad that tries to hook in 2s, showcase 3 features, and end with a CTA in 15s will feel like
noise. Sometimes "hook-hold-CTA" with one strong feature is the right rhythm for 15 seconds. Name
the rhythm before implementing.

### Velocity-Matched Transitions

Exit the outgoing beat with an accelerating ease (power2.in or power3.in) plus a blur ramp. Enter
the incoming beat with a decelerating ease (power2.out or power3.out) plus blur clear. The fastest
point of both easing curves meets at the cut — the viewer perceives continuous camera motion, not
two discrete animations. Match exit velocity to entry velocity within ~5% tolerance.

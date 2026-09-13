# Typography and Motion

Font selection/pairing rules plus high-level motion guardrails for HyperFrames video compositions.
See `../SKILL.md` for when to consult this file, and the animation-focused part of the pipeline for
atomic motion patterns, scene blueprints, named text effects, and the full transition catalog —
those are out of scope here.

## Typography

The renderer pre-bundles a fixed set of fonts (the table below) — write one of those families in
`font-family` and it renders deterministically, offline, with no setup and no warning. A name
outside that set is not silently dropped: if it's a real Google font the compiler fetches it from
Google Fonts at build time and embeds it, so it does render — but that implicit path (a) trips a
lint warning, and (b) is fail-closed in distributed/cloud renders — if Google is unreachable the
render errors rather than quietly substituting a system font. Beyond that, local renders
auto-capture fonts actually installed: a family on the machine, a local `@font-face` path, or an
external CDN stylesheet all get compressed to woff2 and inlined at build time. So a name on
neither the bundle nor Google Fonts only truly falls back to a generic system font when it's also
not installed locally and not declared in an `@font-face` — and even that logs a warning. **One
caveat**: distributed/cloud renders disable system-font capture, so don't rely on a
locally-installed-only font for those. So don't assume an un-bundled display name will just work:
for anything that must render predictably, pick a bundled family below or embed a custom
`@font-face` (see "Finding Fonts").

### Fonts That Embed (auto-resolve)

These 18 families are the ones the renderer pre-bundles — embedded as local data URIs with no
network fetch, so they render offline and deterministically with zero setup, no lint warning, and
no fail-closed fetch risk. Write any of them as a `font-family` and it renders; only the listed
weights exist (asking for a weight a family doesn't ship gives a synthetic/fallback weight, not a
real cut). Any other real Google font still works via the implicit build-time fetch described
above — but only these render with none of those caveats.

| Family            | Weights         | Role              |
| ------------------ | ---------------- | ------------------ |
| Inter               | 400 · 700 · 900   | sans (body/UI)      |
| Roboto              | 400 · 700 · 900   | sans                |
| Open Sans           | 400 · 700         | sans                |
| Lato                | 400 · 700 · 900   | sans                |
| Nunito              | 400 · 700 · 900   | sans (rounded)      |
| Montserrat          | 400 · 700 · 900   | geometric sans      |
| Poppins             | 400 · 700 · 900   | geometric sans      |
| Outfit              | 400 · 700 · 900   | geometric sans      |
| Oswald              | 400 · 700         | condensed sans      |
| **League Gothic**   | **400 only**      | condensed display   |
| **Archivo Black**   | **400 only**      | heavy display       |
| Playfair Display    | 400 · 700 · 900   | serif (display)     |
| EB Garamond         | 400 · 700         | serif (text)        |
| Space Mono          | 400 · 700         | mono                |
| IBM Plex Mono       | 400 · 700         | mono                |
| JetBrains Mono      | 400 · 700         | mono                |
| Source Code Pro     | 400 · 700         | mono                |
| Noto Sans JP        | 400 · 700         | CJK (Japanese)      |

⚠ League Gothic and Archivo Black ship weight 400 ONLY — they are already heavy/condensed display
faces. Do not request `font-weight: 700/900` on them.

**Aliases** — these common names resolve to an embedded family, so they're safe to write:
`Helvetica Neue` / `Helvetica` / `Arial` → Inter · `Futura` / `DIN Alternate` / `Arial Black` →
Montserrat · `Bebas Neue` → League Gothic · `Segoe UI` → Roboto · `Courier New` / `Courier` →
JetBrains Mono · `Garamond` → EB Garamond. (This is why a "safe" `Helvetica Neue` stack always
renders — it maps to embedded Inter.)

**Reconciling with the Banned list below:** several embedded families (Inter, Roboto, Open Sans,
Lato, Nunito, Poppins, Outfit, Playfair Display, EB Garamond) are also on the Banned monoculture
list — they render fine but read as generic. The families that are embedded AND not banned — the
safe-and-distinctive picks — are: **Montserrat, Oswald, League Gothic, Archivo Black, Space Mono,
IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP**. Reach for these (or a non-bundled
font confirmed via the Finding-Fonts step below). A non-bundled name isn't guaranteed-broken — a
real Google font is auto-fetched and embedded — but it carries a lint warning and a fail-closed
fetch in cloud renders, so for anything that must render predictably, embed it via `@font-face`
rather than relying on the implicit fetch.

### Banned

Training-data defaults that every LLM reaches for. These produce monoculture across compositions.

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit,
Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**Syne in particular** is the most overused "distinctive" display font. It is an instant AI design
tell.

### Guardrails

- **Don't pair two sans-serifs.** One for headlines, one for body is a common reflex — cross the
  boundary instead: serif + sans, or sans + mono.
- **One expressive font per scene.** Two interesting fonts trying to make it "better" usually just
  means one performs and one recedes.
- **Weight contrast must be extreme.** Default 400 vs 700 is too subtle. Video needs 300 vs 900.
  The difference must be visible in motion at a glance.
- **Video sizes, not web sizes.** Full-screen viewing (YouTube / website embed): body 20px
  minimum, headlines 60px+, data labels 16px. **In-feed viewing** (destination = a social feed
  where the video plays small inside a scrolling timeline): scale up — body ≥32px, headlines
  ≥90px, data labels ≥24px (first-pass values; calibrate against real renders). 14px body text is
  a common mistake — don't.

### What You Don't Do Without Being Told

- **Tension should mean something.** Don't pattern-match pairings. Ask WHY these two fonts
  disagree. The pairing should embody the content's contradiction — mechanical vs human, public vs
  private, institutional vs personal. If the tension can't be articulated, it's arbitrary.
- **Register switching.** Assign different fonts to different communicative modes — one voice for
  statements, another for data, another for attribution. Not hierarchy on a page. Voices in a
  conversation.
- **Tension can live inside a single font.** A font that looks familiar but is secretly strange
  creates tension with the viewer's expectations, not with another font.
- **One variable changed = dramatic contrast.** Same letterforms, monospaced vs proportional. Same
  family at different optical sizes. Changing only rhythm while everything else stays constant.
- **Double personality works.** Two expressive fonts can coexist if they share an attitude (both
  irreverent, both precise) even when their forms are completely different.
- **Time is hierarchy.** The first element to appear is the most important. In video, sequence
  replaces position.
- **Motion is typography.** How a word enters carries as much meaning as the font. A 0.1s slam vs
  a 2s fade — same font, completely different message.
- **Fixed reading time.** 3 seconds on screen = must be readable in 2. Fewer words, larger type.
- **Tracking tighter than web.** -0.03em to -0.05em on display sizes. Video encoding compresses
  letter detail.

### Finding Fonts

Don't default to what you already know. If the content is luxury, a grotesque sans might create
more tension than the expected Didone serif. Decide the register first, then search.

A font-discovery script fetches live Google Fonts metadata and filters it into five categories —
trending sans, trending serif, monospace, impact/condensed, script/handwriting — banning the same
monoculture list above and randomizing the top results each run so the same 5-8 fonts don't keep
winning. The approach:

```python
import json, sys, random
from collections import OrderedDict

random.seed()  # true random each run

with open(sys.argv[1]) as f:
    data = json.load(f)
fonts = data.get("familyMetadataList", [])

ban = {"Inter","Roboto","Open Sans","Noto Sans","Lato","Poppins","Source Sans 3",
       "PT Sans","Nunito","Outfit","Sora","Playfair Display","Cormorant Garamond",
       "Bodoni Moda","EB Garamond","Cinzel","Prata","Arimo","Source Sans Pro","Syne"}
skip_pfx = ("Roboto","Noto ","Google Sans","Bpmf","Playwrite","Anek","BIZ ",
            "Nanum","Shippori","Sawarabi","Zen ","Kaisei","Kiwi ","Yuji ","Radio ")

def ok(f):
    if f["family"] in ban: return False
    if any(f["family"].startswith(b) for b in skip_pfx): return False
    if "latin" not in (f.get("subsets") or []): return False
    return True

seen = set()
R = OrderedDict()

# Trending Sans — recent (2022+), popular (<300)
R["Trending Sans"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") in ("Sans Serif","Display") and f.get("dateAdded","") >= "2022-01-01" and f.get("popularity",9999) < 300:
        R["Trending Sans"].append(f); seen.add(f["family"])

# Trending Serif — recent (2018+), popular (<600)
R["Trending Serif"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Serif" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Trending Serif"].append(f); seen.add(f["family"])

# Monospace — recent (2018+), popular (<600)
R["Monospace"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Monospace" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Monospace"].append(f); seen.add(f["family"])

# Impact & Condensed — heavy display fonts with 800+ weight
R["Impact & Condensed"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    has_heavy = any(k in list(f.get("fonts",{}).keys()) for k in ("800","900"))
    is_display = f.get("category") in ("Sans Serif","Display")
    if has_heavy and is_display and f.get("popularity",9999) < 400:
        R["Impact & Condensed"].append(f); seen.add(f["family"])

# Script & Handwriting — popular (<300)
R["Script & Handwriting"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Handwriting" and f.get("popularity",9999) < 300:
        R["Script & Handwriting"].append(f); seen.add(f["family"])


# Randomize the top 5 in each category so the same first result doesn't always win
for cat in R:
    R[cat].sort(key=lambda x: x.get("popularity",9999))
    top5 = R[cat][:5]
    rest = R[cat][5:]
    random.shuffle(top5)
    R[cat] = top5 + rest
limits = {"Trending Sans":15,"Trending Serif":12,"Monospace":8,
          "Impact & Condensed":12,"Script & Handwriting":10}
for cat in R:
    items = R[cat][:limits.get(cat,10)]
    if not items: continue
    print(f"--- {cat} ({len(items)}) ---")
    for ff in items:
        var = "VAR" if ff.get("axes") else "   "
        print(f'  {ff.get("popularity"):4d} | {var} | {ff["family"]}')
    print()
```

Fetch the live font metadata with `curl -s 'https://fonts.google.com/metadata/fonts' >
gfonts.json` and run the script against it: `python3 fontquery.py gfonts.json`. Cross classification
boundaries when pairing.

### Selection Thinking

Don't pick fonts by category reflex (editorial → serif, tech → mono, modern → geometric sans).
That's pattern matching, not design.

1. **Name the register.** What voice is the content speaking in? Institutional authority? Personal
   confession? Technical precision? Casual irreverence? The register narrows the field more than
   the category.
2. **Think physically.** Imagine the font as a physical object the brand could ship — a museum
   exhibit caption, a hand-painted shop sign, a 1970s mainframe terminal manual, a fabric label
   inside a coat, a children's book printed on cheap newsprint, a tax form. Whichever physical
   object fits the register is pointing at the right kind of typeface.
3. **Reject the first instinct.** The first font that feels right is usually a training-data
   default for that register. If it was also picked last time, find something else.
4. **Cross-check the assumption.** An editorial brief does NOT need a serif. A technical brief
   does NOT need a sans. A children's product does NOT need a rounded display font. The most
   distinctive choice often contradicts the category expectation.

### Similar-Font Pairing

Never pair two fonts that are similar but not identical — two geometric sans-serifs, two
transitional serifs, two humanist sans. They create visual friction without clear hierarchy. The
viewer senses something is "off" but can't articulate it. Either use one font at two weights, or
pair fonts that contrast on multiple axes: serif + sans, condensed + wide, geometric + humanist.

### Dark Backgrounds

Light text on dark backgrounds creates two optical illusions to compensate for:

- **Increased apparent weight.** Light-on-dark reads heavier than dark-on-light at the same
  `font-weight`. Use 350 instead of 400 for body text. Headlines are less affected because size
  compensates.
- **Tighter apparent spacing.** Light halos around letterforms reduce perceived gaps. Increase
  `line-height` by 0.05-0.1 beyond the light-background value. For display sizes, add 0.01em
  `letter-spacing` to counteract.

### OpenType Features for Data

Most fonts ship with OpenType features that are off by default. Turn them on for data
compositions:

```css
/* Tabular numbers — digits align vertically in columns */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* Diagonal fractions — renders 1/2 as ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for abbreviations — less visual shouting */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* Disable ligatures in code — fi, fl, ffi should stay separate */
code,
.code {
  font-variant-ligatures: none;
}
```

`tabular-nums` is essential any time numbers are stacked vertically — stat callouts, timers,
scoreboards, data tables. Without it, digits have proportional widths and columns don't align.

## Motion (High-Level Guardrails)

This section covers only the high-level guardrails and load-bearing correctness rules. Atomic
motion patterns, scene blueprints, named text effects, and the full transition catalog belong to
the animation-focused part of the pipeline — hand those off rather than improvising here.

### Guardrails

- **Don't use the same ease on every tween.** Defaulting to `power2.out` on everything is a common
  reflex — vary eases like font weights; no more than 2 independent tweens with the same ease in a
  scene.
- **Don't use the same speed on everything.** Defaulting to 0.4-0.5s for everything is common. The
  slowest scene should be 3× slower than the fastest. Vary duration deliberately.
- **Don't enter everything from the same direction.** Defaulting to `y: 30, opacity: 0` on every
  element is common. Vary: from left, from right, from scale, opacity-only, letter-spacing.
- **Don't use the same stagger on every scene.** Each scene needs its own rhythm.
- **Don't use ambient zoom on every scene.** Pick different ambient motion per scene: slow pan,
  subtle rotation, scale push, color shift, or nothing. Stillness after motion is powerful.
- **Don't start at t=0.** Offset the first animation 0.1-0.3s. Zero-delay feels like a jump cut.

### What You Don't Do Without Being Told

**Easing is emotion, not technique.** The transition is the verb. The easing is the adverb. A
slide-in with `expo.out` = confident. With `sine.inOut` = dreamy. With `elastic.out` = playful.
Same motion, different meaning. Choose the adverb deliberately.

Direction rules — these are not optional: `.out` for elements entering (starts fast, decelerates,
feels responsive — the default). `.in` for elements leaving (starts slow, accelerates away, throws
them off). `.inOut` for elements moving between positions. Ease-in for entrances feels sluggish;
ease-out for exits feels reluctant — a common mistake to get backwards.

**Speed communicates weight.** Fast (0.15-0.3s) = energy, urgency, confidence. Medium (0.3-0.5s) =
professional, most content. Slow (0.5-0.8s) = gravity, luxury, contemplation. Very slow (0.8-2.0s)
= cinematic, emotional, atmospheric.

**Scene structure: build / breathe / resolve.** Every scene has three phases — don't dump
everything in the build and leave nothing for breathe or resolve. **Build (0-30%)** — elements
enter, staggered, don't dump everything at once. **Breathe (30-70%)** — content visible, alive
with ONE ambient motion. **Resolve (70-100%)** — exit or decisive end; exits are faster than
entrances.

**Transitions are meaning.** Crossfade = "this continues." Hard cut = "wake up" / disruption. Slow
dissolve = "drift with me." Crossfading everything is a common mistake — use hard cuts for
disruption and register shifts.

**Choreography is hierarchy.** The element that moves first is perceived as most important.
Stagger in order of importance, not DOM order. Don't wait for completion — overlap entries. Total
stagger sequence under 500ms regardless of item count.

**Asymmetry.** Entrances need longer than exits. A card takes 0.4s to appear but 0.25s to
disappear.

### Visual Composition (Motion-Adjacent)

- **Two focal points minimum per scene.** Never a single text block floating in empty space.
- **Fill the frame.** Hero text: 60-80% of width. Web-sized elements are invisible on video.
- **Three layers minimum per scene.** Background treatment (glow, oversized faded type, color
  panel). Foreground content. Accent elements (dividers, labels, data bars).
- **Background is not empty.** Radial glows, oversized faded type bleeding off-frame, subtle
  border panels, hairline rules. Pure solid `#000` reads as "nothing loaded."
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web
  pattern.
- **Split frames.** Data panel on the left, content on the right. Top bar with metadata, full-width
  below. Zone-based layouts, not centered stacks.
- **Use structural elements.** Rules, dividers, border panels create paths for the eye and animate
  well (`scaleX` from 0).

### Image Motion Treatment

Never embed a raw flat image. Every image must have motion treatment:

- **Perspective tilt** — use `gsap.set(el, { transformPerspective: 1200, rotationY: -8 })` +
  `box-shadow` for depth. Do NOT use CSS `transform: perspective(...)` as GSAP will overwrite it.
- **Slow zoom (Ken Burns)** — GSAP `scale: 1` → `1.04` over beat duration makes photos cinematic.
- **Device frame** — wrap in a laptop/phone shape using CSS `border-radius` and `box-shadow`.
- **Floating UI** — extract a key element and animate it at a different z-depth for parallax.
- **Scroll reveal** — clip the image to a viewport window and animate `y` position.

### Load-Bearing GSAP Rules

These rules came out of real production incidents where compositions lint-clean and still ship
broken — elements that never appear, ambient motion that doesn't scrub, entrance tweens that
silently kill their target. A linter cannot catch these; they must be followed by hand. These are
the exact rules with exact code examples — don't summarize or shorten them.

- **No iframes for captured content.** Iframes do not seek deterministically with the timeline —
  the capture engine cannot scrub inside them, so they appear frozen (or blank) in the rendered
  output. If the source being stylized is a live web app, use static screenshots as stacked panels
  or layered images, not live embeds.

- **Never overlap conflicting transform tweens on the same element.** Sequential, non-overlapping
  transform phases are valid. The dangerous case is concurrent tweens or `from()` tweens whose
  `immediateRender` states overwrite one another: for example, a `y` entrance plus a simultaneous
  `scale` Ken Burns tween on the same `<img>`. The element can remain invisible or offscreen with
  no lint warning. Fix the overlap in one of two ways:

  ```html
  <!-- BAD: two transforms on one element -->
  <img class="hero" src="..." />
  <script>
    tl.from(".hero", { y: 50, opacity: 0, duration: 0.6 }, 0);
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // kills the entrance
  </script>

  <!-- GOOD option A: combine into one tween -->
  <script>
    tl.fromTo(
      ".hero",
      { y: 50, opacity: 0, scale: 1.0 },
      { y: 0, opacity: 1, scale: 1.04, duration: beat, ease: "none" },
      0,
    );
  </script>

  <!-- GOOD option B: split across parent + child -->
  <div class="hero-wrap"><img class="hero" src="..." /></div>
  <script>
    tl.fromTo(".hero-wrap", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0); // entrance on parent
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // Ken Burns on child
  </script>
  ```

- **Prefer `tl.fromTo()` over `tl.from()` inside `.clip` scenes.** `gsap.from()` sets
  `immediateRender: true` by default, which writes the "from" state at timeline construction —
  before the `.clip` scene's `data-start` is active. Elements can flash visible, start from the
  wrong position, or skip their entrance entirely when the scene is seeked non-linearly (which the
  capture engine does). Explicit `fromTo` makes the state at every timeline position deterministic:

  ```js
  // BRITTLE: immediateRender interacts badly with scene boundaries
  tl.from(el, { opacity: 0, y: 50, duration: 0.6 }, t);

  // DETERMINISTIC: state is defined at both ends, no immediateRender surprise
  tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6 }, t);
  ```

- **Ambient pulses must attach to the seekable `tl`, never bare `gsap.to()`.** Auras, shimmers,
  gentle float loops, logo breathing — all of these must be added to the scene's timeline, not
  fired standalone. Standalone tweens run on wallclock time and do not scrub with the capture
  engine, so the effect is absent in the rendered video even though it looks correct in a live
  preview:

  ```js
  // BAD: lives outside the timeline, never renders in capture
  gsap.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 });

  // GOOD: seekable, deterministic, renders
  tl.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 }, 0);
  ```

- **Hard-kill exiting inner elements at a scene boundary, not the `.clip` itself.** A non-clip
  element or wrapper whose visibility changes at a beat boundary may need a deterministic
  zero-duration `tl.set()` kill after its fade, because a later tween or sibling `immediateRender`
  can resurrect it. This is the explicit-boundary exception to the ban on raw `visibility` tweens.
  The framework alone controls `.clip` lifecycle; never apply this pattern to the clip container.

  ```js
  tl.to(innerEl, { opacity: 0, duration: 0.3 }, beatEnd);
  tl.set(innerEl, { opacity: 0, visibility: "hidden" }, beatEnd + 0.3); // non-clip kill
  ```

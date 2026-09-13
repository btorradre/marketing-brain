# HyperFrames Creative Direction

This document is the creative/design knowledge base for producing HyperFrames-style videos and motion graphics — brand-driven, frame-by-frame video compositions built from HTML/CSS/GSAP where "a div is a keyframe." It is the non-animation creative layer: visual style, color, typography, narration, story structure, beat pacing, composition patterns, data visualization in motion, and audio-reactive technique. It does not cover the low-level atomic motion/transition mechanics (those live in a companion reference, described below) — this document covers what a frame should look like, feel like, and say, before you worry about exactly how each element tweens.

Use this document whenever you are asked to design, direct, or judge the creative content of a video: choosing a visual style or color palette, writing narration, planning the beat-by-beat rhythm of a multi-scene video, laying out a frame so it reads as video (not a web page), presenting stats/data inside a video, or picking/adapting a named "frame preset" (a ready-made visual system) for a project. If the technical/rendering contract for the project (frame size, timing model, output format) hasn't been established yet, settle that first — this document assumes that contract exists and focuses on what goes inside it.

## How to use this

1. **Find or establish the project's design spec first.** Every non-trivial project should have a single design spec — a brand system for the video, covering colors, fonts, spacing, corner/shadow style, and "do/don't" rules. Look for a file already named for this purpose (commonly `frame.md`, `design.md`, or `DESIGN.md` — read whichever exists, in that order of preference; ignore the others once you've found one). If it exists, its explicit values (hex codes, exact font names, spacing tokens) are the normative truth — quote them verbatim, never invent or round them. Its prose sections carry intent and constraints for judgment calls the tokens can't express — read them for guidance, not for exact values.

2. **If no design spec exists, build one before writing any frame content.** Three ways to do this, in order of speed:
   - **Adopt a ready-made frame preset** (see the Frame Presets catalog below) as a starting point, then overlay any brand-specific tokens the project needs.
   - **Pick a named visual style** from the Visual Style Library (below) that matches the content's mood, and copy its token block in as your spec.
   - **Build fast defaults from House Style** (below): declare a background color, foreground color, one accent color, and a type pairing before writing anything else.
   - For a higher-touch process, run a **two-phase design picker**: generate several distinct "mood board" directions (each telling a different story about the brand, not just reshuffling the same layout), let the person pick a direction, then fine-tune individual categories (palette, type pairing, corner style, density, shadow depth, easing feel) within that direction. See "The design-picker workflow" under Templates & Examples.

3. **Expand the brief into a full per-scene production plan before writing any frame markup.** Never treat the user's request as a finished spec, even a very detailed one — enrich it. For each scene, work out: the concept (the visual world and emotional target, 2-3 sentences), the mood references (cultural/design touchstones, not hex codes), the depth layers (background/midground/foreground), the animation choreography (a specific motion verb per element, not "it animates in"), and the transition out (a named type and exact parameters, not just "crossfade"). Add atmosphere the brief never explicitly asked for — background decoratives, ambient motion, micro-details — because a scene that only contains what was literally requested reads as empty and unproduced. See "Prompt Expansion" and "Beat Direction" below for the full method.

4. **Write to video rules, not web rules**, for every visual decision: bigger type, bigger padding, more visible color, anchored/split compositions instead of centered floating text, at least two focal points and three depth layers per scene. See "Video Composition" below — read it before choosing colors or writing markup, every time, for anything beyond a trivial edit.

5. **Name the scene rhythm before building anything.** Decide, and write down, the pacing pattern across the whole piece — e.g. "hook-PUNCH-breathe-CTA" — driven by the content's emotional arc and the brand's own pacing instinct (unhurried vs. urgent), not by a generic template for the video's length.

6. **If the piece is narrated, write the script to the pacing and tone rules** in "Narration & Script" below, and make sure numbers are written the way you want them spoken, not the way they're displayed on screen.

7. **If the piece tells a story** (a product launch, an explainer, a narrative case study — not a music-driven piece, a pure motion-graphics piece with no narration, a piece built around fixed talking-head or existing footage, or a slideshow the presenter narrates live), apply the "Story Spine" doctrine below: lead with value, not internals; land the value claim in the second beat; treat everything after that as evidence.

8. **After building a scene, self-check it against "Design Adherence"** below before calling it done: every color traces to the spec's palette, fonts and weights match exactly, corner/spacing/shadow values match the declared style, and none of the "lazy AI defaults" have crept in unjustified.

9. **For data or stats inside a video**, use "Data in Motion" below — pair every number with a visual element that gives it weight, keep visually related stats in the same visual language, and avoid web dashboard patterns (pie charts, gridlines, 6-panel layouts) that don't read in a few seconds of motion.

10. **If the piece is driven by music or has audio-reactive elements**, use "Audio-Reactive Animation" below — the audio should only ever drive *timing and intensity* of a visual idea that already makes sense for the content; never let it become the content itself (no generic equalizer bars or spectrum analyzers).

## Rules & standards

### The design spec: what it is and how to read it

A design spec is a **brand system for a video project** — normative values plus prose context, not a page layout. Treat it as two layers:

- **The explicit/structured values are normative.** Colors (exact hex), typography (exact font family, weight, size relationships), spacing, and component rules are the real, load-bearing values. Quote them verbatim; never invent or round a color or substitute a font.
- **The prose sections are context, not values.** Overview, composition rules, "do/don't" sections, and similar prose carry intent, when-to-use guidance, and constraints the structured values can't express on their own. Read them for judgment calls, not for exact numbers.

If more than one candidate spec file exists in a project, prefer the one clearly meant for video/frame-scale work over one meant for a general web page — a video-first spec reframes the brand with a single video frame as the unit of design, rather than a scrolling page.

**The design spec is brand, not layout.** It defines what the brand looks like — colors, fonts, personality, constraints — not how to compose a specific video frame. Be strict about the spec's hex values (including background color), font families, weight relationships, and explicit do's/don'ts: if the brand chose a light canvas, use a light canvas; don't override their palette. Be free about how you adapt it for video: type sizes, spacing, decorative opacity, border weight, and component treatments should all be scaled up from web-appropriate values to video-appropriate values (see "Video Composition" below) — a web card border/shadow combination invisible at web-UI opacity needs to be much bolder to read on video.

### House style (fast defaults when no spec exists)

Before writing any frame markup:

1. **Interpret the prompt — generate real content.** A recipe scene should list real ingredients; a dashboard/HUD scene should have real-looking readouts. Don't leave placeholder-feeling text.
2. **Pick a palette.** Light or dark? Declare background, foreground, and one accent color before writing any markup.
3. **Pick typefaces** — choose faces that fit the content's register (see "Typography" below for a font-discovery method); don't just reach for what's familiar.

**Lazy defaults to question** — these are the first things every generic design instinct reaches for. If you're about to use one, pause and ask: is this a deliberate choice for *this* content, or is it just a default?

- Gradient text (a gradient clipped to text)
- Left-edge accent stripes on cards/callouts
- Cyan-on-dark / purple-to-blue gradients / neon accents
- Pure black or pure white (tint slightly toward your accent hue instead)
- Identical card grids (same-size cards repeated with no variation)
- Everything centered with equal visual weight (give the eye somewhere to travel)
- Overused "safe" fonts (see the banned list under Typography)

If the content genuinely calls for one of these — a centered layout for a solemn closing beat, a card grid for a literal product-UI mockup, an "overused" font because it's the perfect thematic match — use it. The goal is intentionality, not blanket avoidance.

**Color**
- Match light/dark to content: food, wellness, kids' content → light. Tech, cinema, finance → dark.
- One accent hue. Keep the same background across all scenes in a piece.
- Tint neutrals toward your accent hue — even subtle warmth or coolness beats dead gray.
- Contrast should meet accessibility (WCAG AA) standards — text must stay readable even with decorative elements stripped away.
- Declare the palette up front. Don't invent new colors per element as you go.

**Background layer**
Every scene needs visual depth — persistent decorative elements that stay visible while foreground content animates in. Without these, scenes feel empty during entrance staggering. Mix and match 2-5 per scene:

- Radial glows (accent-tinted, low opacity, breathing scale)
- Ghost text (theme words at 3-8% opacity, very large, slow drift)
- Accent lines (hairline rules, subtle pulse)
- Grain/noise overlay, geometric shapes, grid patterns
- Thematic decoratives (orbit rings for space, vinyl grooves for music, grid lines for data)

All decoratives should carry slow ambient motion — breathing, drift, pulse. Static decoratives feel dead. Note: "2-5 per scene" refers to decorative *elements*, not motion patterns — if a project's spec calls for "a single ambient motion per scene," that means one shared looping motion (a common breath/drift/pulse) applied across several decoratives, not just one decorative element total. A scene with 4 decoratives sharing one breathing motion is correct; a scene with only 1 decorative feels under-dressed.

**Motion** — see "Motion Principles" below for the full rules. Quick version: 0.3-0.6s durations, vary your easing curves, combine multiple transform properties on entrances, and let entries overlap rather than waiting for one to finish before the next starts.

**Typography** — see "Typography" below for the full rules. Quick version: use 700-900 weight for headlines and 300-400 for body text, pair a serif with a sans (never two sans-serifs), and keep headlines 60px+ and body text 20px+ at full-screen video scale.

**Palettes** — declare one background, one foreground, and one accent before writing any markup. See the Palettes catalog below for nine named starting palettes organized by mood/category, or derive your own from a single hue: pick a hue, build background/foreground/accent at different lightness levels, and tint everything toward that hue.

### Typography

A rendering engine that pre-bundles a fixed set of fonts (offline, deterministic, zero setup) is the safest choice; a font outside that bundled set generally still works if it's a real, freely-licensed font family, but carries build-time fetch risk and warnings, so treat "will this font definitely render" as a real question whenever the delivery pipeline might run offline or in a constrained environment — pick from a known-safe set, or make sure the font is properly embedded, for anything that must render predictably.

**Guardrails (the mistakes that recur constantly):**

- **Don't pair two sans-serifs.** One for headlines, one for body, both sans — this happens constantly and creates no real hierarchy. Cross the boundary: serif + sans, or sans + mono.
- **One expressive font per scene.** Two "interesting" fonts fighting each other doesn't read as better design — one should perform, one should recede.
- **Weight contrast must be extreme.** Don't default to 400 vs 700. Video needs 300 vs 900 — the difference must be visible in motion at a glance, not just on close inspection.
- **Video sizes, not web sizes.** Full-screen viewing (YouTube, website embed): body text 20px minimum, headlines 60px+, data labels 16px minimum. In-feed viewing (a video playing small inside a scrolling social feed) needs to scale up further: body ≥32px, headlines ≥90px, data labels ≥24px (calibrate against real renders — these are first-pass values).

**What you don't do without being told:**

- **Tension should mean something.** Don't pattern-match font pairings on autopilot. Ask *why* these two fonts disagree — the pairing should embody a real contradiction in the content (mechanical vs. human, public vs. private, institutional vs. personal). If you can't name the tension, the pairing is arbitrary.
- **Register switching.** Assign different fonts to different communicative modes — one voice for statements, another for data, another for attribution. Think of it as different voices in a conversation, not just a hierarchy on a page.
- **Tension can live inside a single font.** A font that looks familiar but is secretly strange creates tension with the viewer's expectations on its own, without needing a second font to contrast against.
- **One variable changed = dramatic contrast.** Same letterforms, monospaced vs. proportional. Same family at different optical sizes. Changing only rhythm while everything else stays constant is a legitimate, controlled way to create contrast.
- **Two expressive fonts can coexist** if they share an underlying attitude (both irreverent, both precise) even when their letterforms look completely different.
- **Time is hierarchy in video.** The first element to appear reads as most important — sequence replaces position the way it works on a static page.
- **Motion is typography.** How a word enters carries as much meaning as the font choice itself. A 0.1s slam vs. a 2s fade, same font, completely different message.
- **Fixed reading time.** If a line is on screen for 3 seconds, it must be readable in 2 — use fewer words and larger type rather than assuming the viewer has time to read everything.
- **Tighter tracking than web.** Roughly -0.03em to -0.05em on display sizes — video encoding compresses letter detail, so give it more room to breathe at the source.

**Selection thinking — don't pick fonts by category reflex** (editorial → serif, tech → mono, modern → geometric sans; that's pattern matching, not design):

1. **Name the register.** What voice is the content speaking in? Institutional authority? Personal confession? Technical precision? Casual irreverence? The register narrows the field more than the content category does.
2. **Think physically.** Imagine the font as a physical object the brand could ship — a museum exhibit caption, a hand-painted shop sign, a 1970s mainframe terminal manual, a fabric label inside a coat, a children's book on cheap newsprint, a tax form. Whichever physical object fits the register points at the right *kind* of typeface.
3. **Reject your first instinct.** The first font that feels right is usually a reflexive default for that register. If you picked it last time too, find something else.
4. **Cross-check the assumption.** An editorial brief does NOT need a serif. A technical brief does NOT need a sans. A children's product does NOT need a rounded display font. The most distinctive choice often contradicts the category expectation.

**Never pair two fonts that are similar but not identical** — two geometric sans-serifs, two transitional serifs, two humanist sans. They create visual friction without clear hierarchy; the viewer senses something is "off" but can't say what. Either use one font at two weights, or pair fonts that contrast on multiple axes: serif + sans, condensed + wide, geometric + humanist.

**Dark backgrounds** create two optical illusions to compensate for:
- **Increased apparent weight.** Light text on dark backgrounds reads heavier than the same weight would on a light background. Use roughly 350 instead of 400 for body text (headlines are less affected because size compensates).
- **Tighter apparent spacing.** Light halos around letterforms reduce perceived gaps. Increase line-height by 0.05-0.1 beyond your light-background value; for display sizes, add about 0.01em of letter-spacing to counteract it.

**A font-discovery method (don't reach for the same 8 familiar fonts every time):** query a current font-metadata source (e.g. Google Fonts' public metadata) and filter/sort dynamically rather than hardcoding names, across five buckets: trending sans (recent, moderately popular), trending serif, monospace, impact/condensed (heavy display weights), and script/handwriting. Randomize which options surface first so you don't default to the same top result every time. Cross classification boundaries deliberately when pairing (don't just grab the top result from two different buckets without checking they actually contrast).

**A recurring "banned" list** — reflexive, overused choices that create monoculture across generic AI-generated design: Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne. **Syne in particular** is the most overused "distinctive" display font — it is an instant design tell that something wasn't deliberately chosen. (Note: several of these — Inter, Roboto, Open Sans, Lato, Nunito, Poppins, Outfit, Playfair Display, EB Garamond — are also common "safe, embeds reliably" choices in rendering pipelines; they render fine technically but read as generic, so reach for them only when the register genuinely calls for them, not by default.)

**OpenType features for data** — most fonts ship with features that are off by default; turn them on for any data composition:
- **Tabular numbers** (`font-variant-numeric: tabular-nums`) — essential whenever numbers stack vertically (stat callouts, timers, scoreboards, tables), so digits align in columns instead of shifting with proportional widths.
- **Diagonal fractions** (`font-variant-numeric: diagonal-fractions`) — renders "1/2" as a proper stacked fraction glyph.
- **Small caps for abbreviations** (`font-variant-caps: all-small-caps`) — less visual shouting than full caps.
- **Disabled ligatures in code** (`font-variant-ligatures: none`) — so "fi", "fl", "ffi" stay as separate letterforms in code/monospace contexts.

### Motion principles (high-level guardrails)

These are the mistakes that recur constantly — the point isn't to memorize a rulebook, it's to notice when you're defaulting instead of deciding.

**Guardrails:**
- **Don't use the same ease on every tween.** The reflexive default is one standard "ease-out" curve on everything. Vary eases the way you'd vary font weights — no more than 2 independent tweens in a scene should share an ease.
- **Don't use the same speed on everything.** The reflexive default is ~0.4-0.5s for everything. The slowest scene in a piece should be about 3× slower than the fastest — vary duration deliberately.
- **Don't enter everything from the same direction.** The reflexive default is "rise up + fade in" for every element. Vary it: from left, from right, from scale, opacity-only, letter-spacing.
- **Don't use the same stagger on every scene.** Each scene needs its own entrance rhythm.
- **Don't use the same ambient motion on every scene.** Pick different ambient motion per scene: slow pan, subtle rotation, scale push, color shift, or nothing at all — stillness after motion is powerful.
- **Don't start at time zero.** Offset the first animation by 0.1-0.3s. A zero-delay start feels like a jump cut.

**Easing is emotion, not technique.** The transition (slide, fade, scale) is the verb; the easing curve is the adverb. A slide-in that decelerates sharply reads as confident. The same slide with a gentle sine curve reads as dreamy. With an elastic overshoot, it reads as playful. Same motion, different meaning — choose the adverb deliberately.

**Direction rules for easing (not optional):**
- Ease-out for elements *entering* — starts fast, decelerates, feels responsive. This is your default for entrances.
- Ease-in for elements *leaving* — starts slow, accelerates away, throws them off screen.
- Ease-in-out for elements *moving between positions*.
Getting this backwards is extremely common: ease-in on an entrance feels sluggish; ease-out on an exit feels reluctant.

**Speed communicates weight:**
- Fast (0.15-0.3s) — energy, urgency, confidence
- Medium (0.3-0.5s) — professional, most everyday content
- Slow (0.5-0.8s) — gravity, luxury, contemplation
- Very slow (0.8-2.0s) — cinematic, emotional, atmospheric

**Scene structure: build / breathe / resolve.** Every scene has three phases — don't dump everything into the build and leave nothing for the other two.
- **Build (0-30%)** — elements enter, staggered. Don't dump everything at once.
- **Breathe (30-70%)** — content sits visible, alive with ONE ambient motion.
- **Resolve (70-100%)** — a clear exit or decisive end. Exits should be faster than entrances.

**Transitions carry meaning:**
- Crossfade = "this continues"
- Hard cut = "wake up" / disruption
- Slow dissolve = "drift with me"
Crossfading everything by default flattens all of these into the same non-statement. Reserve hard cuts for genuine disruption or a register shift.

**Choreography is hierarchy.** The element that moves first is perceived as most important — stagger elements in order of *importance*, not in the order they happen to sit in the markup. Don't wait for one entrance to complete before starting the next — overlap entries. Keep the total stagger sequence for a scene under about 500ms regardless of how many items are in it.

**Asymmetry.** Entrances need longer than exits. A card that takes 0.4s to appear should take about 0.25s to disappear.

**Visual composition for video (not web):**
- **Two focal points minimum per scene.** The eye needs somewhere to travel — never a single text block floating in empty space.
- **Fill the frame.** Hero text should run 60-80% of the frame's width. Web-sized elements read as tiny and lost on video.
- **Three layers minimum per scene:** background treatment (glow, oversized faded type, color panel), foreground content, and accent elements (dividers, labels, data bars).
- **Background is not empty.** Radial glows, oversized faded type bleeding off-frame, subtle border panels, hairline rules. A pure solid black or white background reads as "nothing loaded," not as intentional minimalism.
- **Anchor to edges.** Pin content to left/top or right/bottom. Centered-and-floating is a web layout habit, not a video one.
- **Split frames.** Data panel on the left, content on the right. A metadata top bar with full-width content below. Zone-based layouts, not centered stacks.
- **Use structural elements.** Rules and dividers create paths for the eye and animate well (a horizontal rule scaling in from zero width).

**Image motion treatment — never embed a raw flat image; every image needs motion:**
- **Perspective tilt** — a slight 3D rotation plus a matching drop shadow creates real depth (apply the 3D perspective through the animation engine's transform system, not through a separate CSS perspective declaration, so they don't conflict).
- **Slow zoom (Ken Burns)** — scale from 1.0 to roughly 1.04 over the beat's duration makes a static photo feel cinematic.
- **Device frame** — wrap the image in a laptop/phone shape using rounded corners and a drop shadow.
- **Floating UI** — extract a key element from an image and animate it at a different depth than its background for a parallax effect.
- **Scroll reveal** — clip the image to a viewport window and animate its vertical position underneath.

**Load-bearing technical rules that matter even if you never touch the rendering engine directly** — these came out of real production failures where a composition looked clean in review but rendered broken:
- **Never overlap two conflicting transform tweens on the same element.** If an element has both an entrance transform (e.g. rising up while fading in) and a separate ambient transform (e.g. a slow zoom) running *at the same time*, the second can silently overwrite or fight the first, leaving the element invisible or in the wrong position with no obvious warning. Fix it by either combining both into a single tween definition, or splitting the two motions across a parent wrapper (entrance) and a child element (ambient motion) so they don't collide.
- **Prefer defining both the start and end state explicitly** for anything that needs to render correctly no matter where in the timeline it's viewed from — implicit "from current state" animations can render correctly in a live linear preview but break when a renderer jumps directly to a specific timestamp (which automated rendering pipelines do constantly), because the implicit starting state was never explicitly recorded.
- **Ambient/looping motion (auras, shimmers, gentle floats, logo breathing) must be attached to the scene's own seekable timeline, never fired as an independent, freestanding animation.** A freestanding animation runs on real wall-clock time and does not stay in sync when a rendering pipeline scrubs through the timeline out of real-time order — it can look correct in an interactive preview and simply be absent from the final rendered video.
- **An element that needs to definitively disappear at a scene boundary sometimes needs an explicit, instantaneous "hard kill"** (set its opacity/visibility with zero transition duration) immediately after its fade-out completes — because a later tween elsewhere in the timeline can otherwise resurrect it. This applies to individual inner elements, never to the scene/clip container itself, which the rendering framework manages on its own.

### Video composition (density, scale, color, frame layout)

Video frames are not web pages. Use these rules for design-led compositions while respecting the requested format, brand, and scope — a minimal technical composition or an intentionally sparse format may need less detail than a produced marketing frame.

**Density.** Choose density from the message and format. A brand or sizzle frame often needs several visual roles to feel produced; a lower-third, logo sting, or static title may need only a few. For a scene meant to feel layered, plan these roles:
- **Background treatment** — radial glow, oversized ghost type, color panel, grain, grid, or an intentionally flat field justified by the concept.
- **Midground content** — the actual message: cards, stats, code blocks, images.
- **Foreground accents** — dividers, labels, data bars, registration marks, monospace metadata. The details that make a frame feel produced rather than generated.

For produced marketing frames, roughly 6-10 visual roles is a useful starting point, not a contract. Add decoration only when it reinforces hierarchy, motion, or the concept — decorative treatment must never become new user-facing content, new claims, or new scenes on its own.

**Color presence.** Muted is fine. Flat is not. Every scene should have at least one color that pulls the eye.
- Brand accent should be genuinely VISIBLE — never a 5% opacity glow lost in video compression. Use roughly 15-25% opacity for atmospheric use, full saturation for focal elements.
- **Light canvases work differently than dark ones.** On dark backgrounds, accent glows pop naturally. On light backgrounds, use bolder borders (2px+ solid), stronger structural elements (rules, dividers), and full-saturation accent hits — and add texture (subtle grain, patterns) so a light background doesn't read as a "blank slide." Don't switch to dark to solve this — make light cinematic on its own terms.
- **No full-screen linear gradients on dark backgrounds** — they band visibly under video compression. Use a radial gradient, a solid fill, or a solid fill plus a localized glow instead.
- Tint neutrals toward the brand hue. Dead gray reads as undesigned.

**Scale — web sizes are invisible on video; everything scales up:**

| Element | Web | Video |
|---|---|---|
| Headlines | 32-48px | 64-120px |
| Body text | 14-16px | 28-42px |
| Labels | 12px | 18-24px |
| Decorative opacity | 3-8% | 12-25% |
| Borders | 1px | 2-4px |
| Padding | 16-32px | 60-140px |

If you're writing a font-size under 24px in a video composition, justify it explicitly. If you're writing decorative opacity under 10%, it's effectively invisible.

**Motion intensity.** Subtle motion reads as fully static at typical video frame rates. Err toward more movement than feels safe:
- Every decorative element should carry ambient motion — breathe, drift, pulse, orbit. Static decoratives feel dead.
- Vary the ambient motion pattern per scene — don't repeat the same one throughout.
- Scene entrances should use 3+ different eases and directions. If every element enters the same way, the scene has no real choreography.

**Frame composition:**
- Two focal points minimum — the eye needs somewhere to travel.
- Fill the frame — hero text at 60-80% of frame width.
- Anchor to edges — pin content to left/top or right/bottom; centered-and-floating is a web layout pattern.
- Split frames — data panel left / content right, or a metadata top bar with full-width content below; zone-based layouts over centered stacks.
- Structural elements — rules, dividers, border panels create visual paths and animate well.

### Composition patterns

Reusable techniques for common video-composition needs.

**Picture-in-picture (video in a frame).** Animate a wrapper container for position and size — the actual video content fills the wrapper and doesn't carry its own position/size animation directly. Animate the wrapper's position/size/corner-radius over time (e.g. shrink and reposition a full-frame video into a small inset a few seconds in, then slide it to a different corner later).

**Text behind subject (a headline the presenter occludes with their own silhouette).** Requires a transparent-background cutout of the presenter, produced by running the footage through a background-removal step to get an alpha-channel version alongside the original opaque footage. Build it in three layers:
1. **Base layer** — the full opaque original footage (presenter + background), always visible underneath.
2. **Headline layer** — the text, visible the whole time, positioned exactly where the presenter will eventually stand in front of it.
3. **Cutout layer** — the same footage's transparent-background version, hidden until the reveal moment, then made visible so the presenter's silhouette appears to occlude the headline text that's been sitting underneath it the whole time.

Two technical notes worth carrying into any similar system: (1) if the rendering framework forces visibility/opacity to 1 on any timed clip while it's "active," don't try to fade a clip itself to invisible — wrap it in a plain container div with no timing attributes and control *that wrapper's* opacity instead; (2) mount both the base and cutout video layers at the same start time (even though the cutout stays invisible for a while) so both decode in sync from the beginning — mounting the cutout late can cause a visible one-frame sync jitter at the reveal moment because the video decoder has to seek and warm up right as it becomes visible. For color matching between the opaque and cutout versions, use the highest-quality background-removal setting for hero/close-up shots where any RGB shift or edge halo would be visible; a faster, lower-fidelity setting is fine only when the cutout will sit over a very different background and file size matters more than perfect color match.

**Title card with fade.** A full-frame card with centered text; the text fades in shortly after the card starts, and the entire card fades out shortly before the card's own end time.

**Slide show with section headers.** Multiple slide elements share one visual track, each occupying its own start-time/duration window on that track — they auto-mount and auto-unmount based on that timing rather than needing separate manual show/hide logic.

**Top-level composition structure.** A video composition is conceptually: individual media clips (video/image/audio elements, each carrying its own start time, duration, and layer/track index) plus optional nested sub-compositions (self-contained smaller compositions loaded by reference and treated as a single clip in the parent timeline, useful for reusable pieces like an intro animation or a caption overlay that get authored once and dropped into multiple places).

### Prompt expansion (turning a brief into a full production spec)

Expansion is not about lengthening a short brief — it's about grounding the requester's intent against the design spec and house style, and producing a consistent, detailed intermediate plan that every downstream step (writing markup, choosing animation, sourcing footage) reads the same way. Run this after design direction is established, and before building any scene.

**Even a very detailed brief is still a seed.** The expansion's job is to enrich it into a fully-realized per-scene production spec, adding things the requester's brief almost never lists explicitly:

- **Atmosphere layers per scene** (2-5 background decoratives from house style: radial glows, ghost type, hairline rules, grain, thematic decoratives).
- **Secondary motion for every decorative** — breath, drift, pulse, orbit. A decorative with no ambient motion feels dead.
- **Micro-details that make a scene feel real** — registration marks, tick indicators, monospace coordinate labels, typographic accents, background code snippets, grid patterns — things the requester didn't think to ask for but that separate a produced frame from a generic one.
- **Transition choreography at the object level** — not "crossfade" but a specific description like "the stat card expands outward and becomes the next scene's header," with an exact duration, ease, and morph source/target.
- **Pacing beats within each scene** — where tension builds, where a hold lets the viewer breathe, where the key word lands.
- **Exact values** — hex colors, type sizes, ease choices — pulled directly from the design spec, with no vagueness left for later guessing.

**Do not skip this step and do not just pass the brief through unchanged.** The gap in quality between a single-pass composition and a properly-planned multi-scene composition comes almost entirely from this expansion step — it front-loads the richness so every later step builds from a rich brief instead of a terse one. The only real exceptions are single-scene compositions and trivial edits.

**What the expanded plan should contain:**
1. **Title + style block** — cite the design spec's exact hex values, font names, and mood; never invent a palette.
2. **Rhythm declaration** — name the scene rhythm before detailing any individual scene (e.g. "hook-PUNCH-breathe-CTA" or "slow-build-BUILD-PEAK-breathe-CTA").
3. **Global rules** — parallax layers, micro-motion requirements, transition style, primary vs. accent transitions; match energy to mood (calm → slow eases, high energy → snappy eases).
4. **Per-scene beats**, each with: Concept (2-3 sentences on the visual world/metaphor/feeling), Mood direction (cultural/design references, not hex codes), Depth layers (background/midground/foreground, sized to the concept — don't force a fixed element count or invent filler content), Animation choreography (a specific verb per element — see the motion-verb vocabulary under Beat Direction below), and Transition out (a specific named type with exact parameters).
5. **Recurring motifs** — visual threads that repeat across scenes, drawn from the brand palette.
6. **Negative prompt / what to avoid**, informed by the design spec's own constraints where they exist.

Present the expanded plan for review before building anything from it — it's much cheaper to edit a written plan than to rebuild finished frames.

### Beat direction (planning individual scenes in a multi-scene piece)

**Each beat is a WORLD, not a layout.** Before working out CSS specs and exact animation instructions, describe what the viewer *experiences*. Compare:

- **Mediocre:** "Dark navy background. '$1.9T' in white, 280px. Logo top-left. Wave image bottom-right."
- **Great:** "Camera is already mid-flight over a vast dark canvas. The gradient wave sweeps across the frame like aurora borealis — alive, shifting. '$1.9T' SLAMS into existence with such force the wave ripples in response. This isn't a slide — it's a moment."

The first describes pixels. The second describes an experience. Write the second, then work out the pixels.

**Each beat should define:**

**Concept** — the big idea for this beat in 2-3 sentences. What visual WORLD are we in? What metaphor drives it? What should the viewer FEEL? This is the most important part — everything else flows from it.

**Mood direction** — cultural and design references, not hex codes: "Geometric, rhythmic, precise. Think Josef Albers or Bauhaus color studies." / "Warm workspace. Nice notebook energy, not technical blueprint." / "Cinematic title sequence — the kind of opening where you lean forward."

**Animation choreography** — specific motion verbs per element, not "it animates in" but HOW. Verbs come from the beat's concept and content, not from a fixed "energy level" lookup table — a wellness brand's "slow" beat might still have something that DROPS if the content is about letting go; a stats beat might FLOAT if the brand's own identity is weightless. Vocabulary, organized by physical character rather than energy level:
- **Impact / weight:** SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS, DROPS (with force)
- **Directional / deliberate:** SLIDES, PUSHES, PULLS, WIPES, CUTS
- **Reveals / builds:** DRAWS, FILLS, GROWS, EXPANDS, ASSEMBLES, COUNTS UP
- **Organic / ambient:** FLOATS, DRIFTS, BREATHES, PULSES, ORBITS, MORPHS
- **Mechanical / precise:** TYPES ON, CLICKS, LOCKS IN, SNAPS, STEPS

Every element gets a verb. If you can't name the verb, the element isn't designed yet. The verb should follow from the beat's concept, not from a generic "high energy vs. low energy" lookup.

**Transition** — how this beat hands off to the next. Three broad transition families, each suited to different moments:

| Choose a strong "shader"-style transition for | Choose a simpler continuous crossfade/wipe for | Choose a hard cut for |
|---|---|---|
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments | Continuous camera-motion beats where the scene feels like one move broken into cuts | Rapid-fire lists, percussive edits on the beat, comedic timing |
| Any moment the music/VO punctuates with a downbeat or sound-effect hit | Beats that ease from one composition into the next sharing motion vocabulary | Sequences of 3+ quick tempo-matched switches |
| Brand moments where the transition itself IS the visual | Minimal/editorial pacing | Anytime a slow transition would feel too draggy |

Rule of thumb: if a beat is the *centerpiece* of the video, use a strong, distinctive transition into it. If a beat is connective tissue, a simple crossfade is fine. A brand reel of 5-7 beats usually wants only 1-2 standout transitions (the hero reveal + the CTA) — too many flattens their impact.

**A library of common transition patterns** (categorize by motion character, mix and match — these are starting points, not an exhaustive list):
- **Push / slide** — content moves through the frame as if on a continuous surface (push slide, vertical push, elastic push, squeeze).
- **Scale / zoom** — perspective shifts, moving toward or away from content (zoom through, zoom out).
- **Radial / clip** — geometric reveal, content emerges or is covered by a shape (circle iris, diamond iris, diagonal split).
- **3D** — physical, content flips like a tangible object (3D card flip).
- **Dissolve** — overlap and blend, both scenes exist simultaneously during the transition (crossfade, blur crossfade, focus pull, color dip).
- **Cover / blinds** — structural, content is sliced, layered, or covered (staggered color blocks, horizontal/vertical blinds).
- **Light** — organic film, light bleeds across the frame (light leak overlays, overexposure burn, film burn).
- **Distortion** — instability, the image appears to malfunction (glitch/RGB jitter, chromatic aberration, ripple, VHS tape).
- **Blur** — soft defocus, content blurs in or out (blur through, directional blur).
- **Mechanical** — precision, visible mechanical logic (shutter, clock wipe).
- **Grid** — fragmentation, the frame breaks into pieces (grid dissolve).
- **Destruction** — dramatic decay, the previous scene is destroyed (page burn).
- **Other** — physical/shape-based motion that doesn't fit elsewhere (gravity drop, morph circle).

Common quick-pick recipes:
- **Velocity-matched upward** — exit: rise and blur out on an accelerating curve (~0.33s); entry: fall in from below and clear the blur on a decelerating curve (~1.0s).
- **Whip pan** — exit: fast horizontal blur-slide out (~0.3s); entry: fast horizontal blur-slide in from the opposite side (~0.3s).
- **Blur through** — exit: blur to ~20px (~0.3s); entry: clear the blur (~0.25s).
- **Zoom through** — exit: scale up while blurring (~0.2s); entry: scale down from an overshoot while clearing blur (~0.5s).
- **Hard cut / smash cut** — instant, for rapid-fire sequences.
Typical duration presets: snappy (0.2s), smooth (0.4s), gentle (0.6s), dramatic (0.5s), instant (0.15s), luxe (0.7s).

**You are not limited to a fixed transition library.** Write custom effects from scratch, search for and adapt existing shader/effect code, build custom transitions that combine techniques in new ways, or ask for a specific effect to be sourced if the storyboard calls for something that doesn't exist yet in your toolkit. If a browser (or equivalent rendering surface) can render it, it can be a transition.

**Depth layers.** What's in foreground, midground, and background. Every beat should have at least 2 layers, e.g.: "Background: dark navy fill + subtle radial glow. Midground: stat cards with drop shadow. Foreground: brand logo bottom-right."

**SFX cues.** What sounds at what moment, e.g.: "On the capture pulse — a soft, warm analog shutter click." / "Left side carries a faint low drone. On the fold: drone cuts. Silence. Then a single clean chime."

**Rhythm planning.** Before writing any frame markup, declare the scene rhythm — which scenes are quick hits, which are holds, where the standout transitions land, where energy peaks. Name the pattern (e.g. fast-fast-SLOW-fast-BIG-hold) before implementing anything.

**Derive the rhythm from the storyboard and the brand, not from a generic lookup table for the video's length.** A 15-second social ad for an architectural firm and a 15-second social ad for a gaming brand have different rhythms — both are 15 seconds, but one is slow-reveal-hold-CTA and the other is rapid-fire-SLAM-hook. The duration and video type set constraints (roughly how many beats fit); the brand and content determine whether those beats are slow or fast, sparse or dense, dramatic or controlled.

Questions that drive rhythm decisions:
- What emotional journey should the viewer take? Where is the peak moment?
- Where does the narration land its heaviest emphasis? That's usually where energy should peak.
- What does the brand's own visual pacing suggest — unhurried or urgent?
- How many beats can the duration actually support without feeling rushed or padded?

A social ad that tries to hook in 2 seconds, showcase 3 features, and close with a CTA all inside 15 seconds will feel like noise. Sometimes "hook-hold-CTA" with a single strong feature is the right rhythm for 15 seconds. Name the rhythm you've planned before building it.

**Velocity-matched transitions** (a technique for making a cut feel like one continuous camera move rather than two separate animations): exit the outgoing beat on an accelerating curve plus a blur ramp; enter the incoming beat on a decelerating curve plus a matching blur clear. The fastest point of both curves should land right at the cut — match exit velocity to entry velocity within roughly 5% so the eye reads continuous motion rather than two discrete animations.

### Story spine — value-first narrative doctrine

Applies to narrated, story-driven pieces — a product launch video, an explainer built from source material, a general narrative video. It does **not** apply to a piece driven entirely by a music track (the track drives the arc), a pure motion-graphics piece with no narration (motion is the message), a recut of existing talking-head/interview footage or embedded-caption piece (the footage's story is already fixed), or a slideshow where a live presenter owns the story. Don't force these rules onto a format they don't fit.

Different formats own their own specific archetypes and beat sequences; this doctrine owns three cross-format rules about **order and justification** — described as a "reverse iceberg": lead with why something is valuable, not with what it is or how it was made.

**1. The hook speaks the viewer's language.** The first beat answers "why should I care" in *outcome language* — what the viewer gains, avoids, or finally understands. Subject-internal vocabulary is banned in the hook: internal jargon, a feature list, the source material's own section headings. Numbers are welcome only when they carry stakes ("40% faster") — never as inventory ("23 changes").

**2. Reverse iceberg — value before evidence.** The core value claim lands by the second beat. Everything after it is evidence in service of that claim — a demo, a mechanism explanation, screenshots, a diff. Implementation detail is the footnote of the story, not its spine. Self-check on a finished beat list: delete every evidence beat — the remaining beats should still state the value on their own. Delete the value beats — if the video still seems to work as a coherent piece, it was a feature tour, not a story.

Structure is value-first; the *voice* stays whatever the specific format calls for (a plain, low-hype developer-facing piece keeps its plain voice — leading with value is an ordering decision, not a request to add marketing hype).

**3. The storyboard is a proposal, not a listing.** When presenting a plan for approval before building:
- Open by echoing the strategy line: **"This video tells [audience] that [message]."**
- Present the frames as a table, one row per frame, with columns for the frame, its beat/timing, what's on screen, and *why* — the frame's job in the story, traced back to the core message. A frame whose "why" can't be traced back to the message is a frame to cut, not to decorate.
- Recommendations should carry their own justification — the structural choice, the beat count, and any beat someone might question, each stating its own basis.

This proposal shape — echo the strategy line, then a frame table, then style/duration notes, then "approve or adjust" — is the cheapest place to iterate: a frame change at this stage costs 30 seconds; the same change after the frames are actually built costs much more.

### Narration & script

**Pacing:**
- About 2.5 words per second is a natural speaking pace.
- 15 seconds ≈ 37 words. 30 seconds ≈ 75 words. 60 seconds ≈ 150 words.
- Leave room for pauses — silence between sentences is a feature, not dead air.
- The script should feel *shorter* than the video runs — visual breathing room matters.

**Tone — write like a person, not a brochure:**
- Use contractions: "it's", "you'll", "that's", "we've".
- Vary sentence length — short punchy phrases mixed with longer flowing ones.
- Read it out loud. If it sounds robotic, rewrite it.
- Avoid jargon unless the audience genuinely expects it.

**Number pronunciation — write what you want the voice to say; text-to-speech reads literally:**

| In the visual | Write in the script as |
|---|---|
| 135+ | more than one hundred thirty five |
| $1.9T | nearly two trillion dollars |
| 99.999% | ninety nine point nine percent |
| 200M+ | over two hundred million |
| 10x | ten times |
| API | A P I |
| stripe.com | stripe dot com |

The visual can show the exact figure while the voice rounds it for natural speech.

**Structure for product videos:**
1. **Hook** — what's surprising or impressive about this product? A bold claim, a provocative question, a contrast, or a striking number. This is the opening line. Vary the hook type — don't default to a stat every time.
2. **Story** — what does the product do? Who uses it? Keep it concrete.
3. **Proof** — stats, customer names, social proof. Real numbers from the actual product.
4. **CTA** — what should the viewer do? ("Start building at stripe dot com.")

Not every video needs all four. A 15-second social ad might be Hook + Proof + CTA. A 60-second product tour uses all four with more Story.

**The opening line** is the most important sentence in the video — it must create tension, curiosity, or surprise in the first 3 seconds. Patterns that work:
- **A bold claim:** "The financial infrastructure that powers the internet economy."
- **A question that provokes:** "What if your database could think?"
- **A contrast:** "Your AI agent already knows how to make videos. It just needs the right format."
- **A number that shocks:** "Nearly two trillion dollars." (Use sparingly — not every video should open with a stat.)

If the opening is generic ("Welcome to [product]" / "Introducing our product"), start over.

**Worked example** (from a 62-second product launch — roughly 140 words for 62 seconds, i.e. about 2.3 words/sec, leaving room for pauses and visual breathing):

> Your AI agent already knows how to make videos.
> It just needs the right format.
>
> This is Hyperframes. An open source framework. HTML in, video out.
>
> A div is a keyframe. Data attributes are your timeline.
> CSS is your look. G-Sap is your animation engine.
>
> Anything a browser can render can be a frame in your video.
>
> CSS animations. G-Sap. Lottie. Shaders. Three.js.
>
> Drop in music, sound effects, footage — it all composes together.
>
> No new framework for the agent to learn.
> Just HTML.
>
> The agent writes it. The renderer captures every frame as MP4.
> It's deterministic. Identical outputs, every time.
>
> Give your agent the CLI. Tell it what to make.
> Watch it build.
>
> Hyperframes. Go make something.

### Data in motion (stats and infographics inside a video)

- **Visual continuity.** When successive stats belong to the same concept (Q1 → Q2 → Q3 → Q4, or three metrics for the same product), keep them in the same visual space with the same aesthetic. Only the *value* should change — an aesthetic change should signal a new concept, not just a new number.
- **Numbers need visual weight.** A number on its own floats in empty space. Pair every metric with a visual element that gives it presence — a proportional fill bar, a background color shift, a shape that represents the value, a progress ring. It doesn't need to be a literal chart — it just needs to fill the frame and make the data feel tangible rather than plain text on a background.
- **Avoid web dashboard patterns:**
  - No pie charts — hard to compare at a glance, reads as a slide deck.
  - No multi-axis charts — a viewer can't study intersecting axes in a 3-second window.
  - No 6-panel dashboards — 2-3 related metrics side-by-side is fine; 6+ is a web pattern that doesn't survive video pacing.
  - No gridlines, tick marks, or legends — visual noise that adds nothing while in motion.
  - Build charts by hand (SVG/CSS/motion), not by dropping in default chart-library output — library defaults read as a spreadsheet screenshot, not a produced video.

### Audio-reactive animation

Drive visuals from music, voice, or sound. In principle, any animatable visual property can respond to pre-analyzed audio data.

**The audio data model:** a per-frame array of frequency-band amplitudes (0-1 scale), one set per video frame, with band index 0 representing bass and higher indices representing treble — each band normalized independently across the full track.

**Mapping audio to visuals:**

| Audio signal | Visual property | Effect |
|---|---|---|
| Bass (low band) | Scale | Pulse on beat |
| Treble (high bands) | Text shadow, box shadow | Glow intensity |
| Overall amplitude | Opacity, vertical position, background color | Breathe, lift, color shift |
| Mid-range | Border radius, width | Shape morphing |

Any animatable property can work this way — clip paths, filters, SVG attributes, custom color properties.

**Content, not medium.** Audio provides *timing and intensity*; the visual vocabulary comes from the narrative, never from the fact that there's audio at all. Never add: equalizer bars, spectrum analyzers, waveform displays, musical-note clip art, generic particle systems, rainbow color cycling, strobing white flashes on beats, abstract pulsing orbs. Instead: let the content guide the visual, and let audio drive its behavior. Bass makes warmth *swell*. Treble sharpens *contrast*. The visual choice comes from "what does this piece feel like?" — not from "what do music visualizers usually look like?"

**Sampling matters.** Audio reactivity needs genuine per-frame sampling of the pre-extracted data (looping through every frame and reading its band values), not a single smoothed animation across the whole duration — a single tween doesn't actually react to the audio, it just approximates an average.

**A practical gotcha:** a glow/shadow effect applied to a parent container that also holds semi-transparent inactive children (e.g. inactive caption words at low opacity) can render as a visible glow rectangle behind all the children, not just the intended active element. Fix: apply a scale pulse to the container for the beat reaction, but apply the glow/shadow itself only to the specific active element.

**Guidelines:**
- Subtlety for text — 3-6% scale variation, soft glow. Heavy pulsing makes text unreadable.
- Go bigger on non-text — backgrounds and shapes can handle 10-30% swings.
- Match the energy — corporate content stays subtle; a music video can go dramatic.
- Keep it deterministic — use pre-extracted, fixed audio data rather than any live/real-time audio analysis, so the same input always produces the same output.

### Design adherence (post-build self-check)

Run this after building a scene, before treating it as finished.

**If a design spec exists**, check:
1. **Colors** — every color used in the composition appears in the spec's declared palette. Flag any invented colors.
2. **Typography** — font families and weights match the spec's type system exactly; no substitutions.
3. **Corners** — border-radius values match the declared corner style, if one is specified.
4. **Spacing** — padding and gap values fall within the declared density range, if specified.
5. **Depth** — shadow usage matches the declared depth level, if specified (flat = none, subtle = light, layered = glows).
6. **Avoidance rules** — if the spec lists things to avoid ("What NOT to Do," "Don'ts," "Anti-patterns"), verify none of them are present.

Report violations as a checklist and fix each one before treating the piece as done.

**If no design spec exists** (house-style-only path), check instead:
1. **Palette consistency** — the same background, foreground, and accent colors are used across every scene; no per-scene color invention.
2. **No unjustified lazy defaults** — check the composition against the "Lazy Defaults to Question" list under House Style. If any appear, they should be a deliberate choice for this specific content, not a fallback.

### Visual style library

Named visual identities, each grounded in a real graphic design tradition, expressed as a portable token block (colors, typography, spacing, shadow/rounding style, and a motion profile — energy level, easing, durations, atmosphere, and a suggested transition character). Use these as starting points — adopt a style's token set as your project's design spec, then customize.

**How to pick:** match mood first, content second. Ask: "What should the viewer FEEL?"

**Quick reference:**

| Style | Mood | Best for | Suggested transition character |
|---|---|---|---|
| Swiss Pulse | Clinical, precise | SaaS, data, dev tools, metrics | Sharp radial zoom or circle-iris reveal |
| Velvet Standard | Premium, timeless | Luxury, enterprise, keynotes | Slow organic morph-dissolve |
| Deconstructed | Industrial, raw | Tech launches, security, punk | Glitch or fast whip-pan |
| Maximalist Type | Loud, kinetic | Big announcements, launches | Burn-reveal with sparks |
| Data Drift | Futuristic, immersive | AI, ML, cutting-edge tech | Gravitational pinch-pull or organic warp-dissolve |
| Soft Signal | Intimate, warm | Wellness, personal stories, brand | Heat-haze shimmer dissolve |
| Folk Frequency | Cultural, vivid | Consumer apps, food, communities | Swirl vortex or radial ripple |
| Shadow Cut | Dark, cinematic | Dramatic reveals, security, exposé | Slow organic warp-dissolve |

**1. Swiss Pulse — in the spirit of Josef Müller-Brockmann.** Mood: clinical, precise. Best for: SaaS dashboards, developer tools, APIs, metrics.
- Colors: near-black primary (`#1a1a1a`), white on-primary, electric blue accent (`#0066FF`).
- Type: Helvetica Neue-style headline at ~80px/700 weight; Inter label at ~14px/400; a huge Helvetica Neue-style stat number at ~112px/700.
- Corners: sharp (0-2px). Spacing: 8/16/32px scale.
- Motion: high energy; entries decelerate sharply, exits accelerate hard, no ambient motion; fast entrances (~0.4s), long holds (~1.5s), quick transitions (~0.6s); atmosphere = grid lines + registration marks; transition character = sharp radial zoom.
- Feel: grid-locked compositions, every element snaps to an invisible 12-column grid. Numbers dominate the frame at 80-120px. Animated counters count up from 0. Hard cuts, no decorative transitions. Nothing floats.

**2. Velvet Standard — in the spirit of Massimo Vignelli.** Mood: premium, timeless. Best for: luxury products, enterprise software, keynotes, investor decks.
- Colors: near-black primary (`#0a0a0a`), white on-primary, deep indigo accent (`#1a237e`).
- Type: thin, wide-tracked, all-caps headline at ~48px/300 weight, 0.15em tracking; light body text at ~16px/300, 1.6 line-height.
- Corners: near-sharp (0-2px). Spacing: 16/32/64px scale — generous.
- Motion: calm energy; gentle in-out easing throughout including on ambient motion; slow entrances (~1.2s), very long holds (~3.0s), slow transitions (~1.5s); atmosphere = subtle grain + hairline rules; transition character = slow organic morph-dissolve.
- Feel: generous negative space, symmetrical/centered/architectural precision. Sequential reveals with long holds. Nothing snaps — everything glides with intention. Luxury takes its time.

**3. Deconstructed — in the spirit of Neville Brody.** Mood: industrial, raw. Best for: tech news, developer launches, security products, punk-energy reveals.
- Colors: near-black primary (`#1a1a1a`), off-white on-primary (`#f0f0f0`), burnt-orange accent (`#D4501E`).
- Type: bold geometric-sans headline at ~64px/700; bold tracked uppercase mono label at ~12px/700.
- Corners: sharp. Spacing: 4/12/24px scale — tight.
- Motion: high energy; springy overshoot entries, stepped/robotic exits, elastic ambient motion; fast entrances (~0.3s), short holds (~1.0s), quick transitions (~0.5s); atmosphere = scan lines + glitch artifacts + grain overlay; transition character = glitch.
- Feel: type at angles, overlapping edges, escaping frames. Gritty textures baked into the design. Text SLAMS and SHATTERS. Letters scramble then snap to final position. Intentional irregularity — nothing should feel polished.

**4. Maximalist Type — in the spirit of Paula Scher.** Mood: loud, kinetic. Best for: big product launches, milestone announcements, high-energy hype videos.
- Colors: near-black primary (`#0a0a0a`), white on-primary, plus a hot-red accent (`#E63946`) and a bright-yellow accent (`#FFD60A`).
- Type: massive heavy uppercase headline at ~128px/400; bold geometric-sans subhead at ~48px/700.
- Corners: sharp. Spacing: 0/8px scale — near-zero gap.
- Motion: high energy; sharp deceleration entries, springy-overshoot exits, forward-driving ambient motion; fast entrances (~0.3s), short holds (~0.8s), quick transitions (~0.4s); atmosphere = overlapping type layers + color blocks; transition character = burn-reveal with sparks.
- Feel: text IS the visual. Overlapping type layers at different scales and angles filling 50-80% of frame. Bold saturated colors, maximum contrast. Everything kinetic — slamming, sliding, scaling. 2-3 second rapid-fire scenes. No static moments. Fast arrivals, hard stops.

**5. Data Drift — in the spirit of Refik Anadol.** Mood: futuristic, immersive. Best for: AI products, ML platforms, data companies, speculative tech.
- Colors: near-black primary (`#0a0a0a`), light-gray on-primary (`#e0e0e0`), plus a violet accent (`#7c3aed`) and a cyan accent (`#06b6d4`).
- Type: thin, tracked headline at ~40px/200; light body at ~14px/300.
- Corners: soft (4-12px) plus fully-round pill elements. Spacing: 16/32/64px scale.
- Motion: moderate energy; gentle in-out easing throughout including ambient motion; slow-ish entrances (~1.0s), long holds (~2.5s), slow transitions (~1.5s); atmosphere = particle field + light traces + radial glow; transition character = gravitational pinch-pull.
- Feel: thin futuristic sans-serif, floating and weightless. Fluid morphing compositions. Extreme scale shifts (micro to macro). Particles coalesce into numbers. Light traces data paths through the frame. Smooth, continuous, organic. Nothing hard.

**6. Soft Signal — in the spirit of Stefan Sagmeister.** Mood: intimate, warm. Best for: wellness brands, personal stories, lifestyle products, human-centered apps.
- Colors: warm cream primary (`#FFF8EC`), near-black on-primary, plus amber (`#F5A623`), dusty rose (`#C4A3A3`), and sage (`#8FAF8C`) accents.
- Type: italic serif headline at ~48px/400; light body at ~16px/300, 1.7 line-height.
- Corners: soft to fully-round (8-24px, plus pill). Spacing: 12/24/48px scale.
- Motion: calm energy; gentle in-out easing throughout including ambient motion; slow entrances (~1.0s), very long holds (~3.0s), slow transitions (~1.5s); atmosphere = soft gradient + warm grain; transition character = heat-haze shimmer dissolve.
- Feel: handwritten-style or humanist serif fonts, personal, lowercase, delicate. Close-up framing — a single element fills the frame. Slow drifts and floats, never snaps. Soft organic motion. Nothing should feel hurried or polished. Intimate, never corporate.

**7. Folk Frequency — in the spirit of Eduardo Terrazas.** Mood: cultural, vivid. Best for: consumer apps, food platforms, community products, festive launches.
- Colors: white primary, near-black on-primary, plus hot-pink, cobalt, and bright-yellow/green accents.
- Type: bold rounded-display headline at ~64px/400; bold rounded body at ~16px/600.
- Corners: soft to fully-round (8-32px, plus pill). Spacing: 8/16/32px scale.
- Motion: high energy; springy-overshoot entries, elastic exits, gentle in-out ambient motion; medium entrances (~0.5s), medium holds (~1.5s), medium transitions (~0.8s); atmosphere = pattern tiles + confetti burst + color blocks; transition character = swirl vortex.
- Feel: bold warm rounded type. Pattern and repetition — folk-art rhythm and density. Layered compositions with rich visual texture; every frame feels handcrafted. Colorful motion — elements bounce, pop, spin into place with joy. Overshoots feel intentional. Celebratory energy.

**8. Shadow Cut — in the spirit of Hans Hillmann.** Mood: dark, cinematic. Best for: security products, dramatic reveals, investigative content, intense launches.
- Colors: near-black primary (`#0a0a0a`), off-white on-primary (`#f0f0f0`), dark-gray surface (`#3a3a3a`), blood-red accent (`#C1121F`).
- Type: bold condensed uppercase headline at ~64px/700; regular body at ~14px/400.
- Corners: sharp (0-2px). Spacing: 8/16/48px scale.
- Motion: moderate energy; sharp-deceleration entries, sharp-acceleration exits, gentle in-out ambient motion; medium-slow entrances (~0.8s), long holds (~2.5s), slow transitions (~1.2s); atmosphere = deep shadow + vignette + grain overlay; transition character = slow organic warp-dissolve.
- Feel: near-monochrome — deep blacks, cold grays, stark white plus one blood-red accent. Sharp angular text like film-noir title cards. Heavy contrast, no softness. Elements emerge from darkness — the reveal IS the narrative. Slow creeping push-ins, dramatic scale reveals. The pause before the hit matters.

**Mood → style quick guide:**

| If the content feels... | Use... |
|---|---|
| Data-driven, analytical, technical | Swiss Pulse |
| Premium, enterprise, luxury | Velvet Standard |
| Raw, punk, aggressive, rebellious | Deconstructed |
| Hype, loud, high-energy launch | Maximalist Type |
| AI, ML, speculative, futuristic | Data Drift |
| Human, warm, personal, wellness | Soft Signal |
| Cultural, fun, consumer, festive | Folk Frequency |
| Dark, dramatic, intense, cinematic | Shadow Cut |

**Creating custom styles.** The eight styles above are starters, not constraints. To create your own:
1. **Name it** after a designer, art movement, or cultural reference.
2. **Define tokens** — colors (2-5 tokens), typography (2-3 scales), corner style, spacing scale, and a motion profile (energy + easing + duration + atmosphere + transition character).
3. **Add a short prose paragraph** describing the feel, what to do, what to avoid.
4. **Reference tokens by name** wherever the style gets applied, so a single edit to the token set propagates everywhere.

The pattern: token set (what) → prose rationale (why) → applied components (how they combine).

## Palettes

Nine named palette collections, organized by mood/use case. Each is a set of complete 5-color swatch rows — pick one full row as a cohesive palette (don't mix hexes across rows), or use them as a reference to hand-pick a background/foreground/accent combination for a project.

### Bold / Energetic
Product launches, social media, announcements, high-energy content.

```
#FFBE0B #FB5607 #FF006E #8338EC #3A86FF
#F72585 #7209B7 #3A0CA3 #4361EE #4CC9F0
#EF476F #FFD166 #06D6A0 #118AB2 #073B4C
#FF595E #FFCA3A #8AC926 #1982C4 #6A4C93
#9B5DE5 #F15BB5 #FEE440 #00BBF9 #00F5D4
#390099 #9E0059 #FF0054 #FF5400 #FFBD00
#3D348B #7678ED #F7B801 #F18701 #F35B04
#FFBC42 #D81159 #8F2D56 #218380 #73D2DE
```

### Clean / Corporate
Explainers, tutorials, presentations, professional content.

```
#FFFCF2 #CCC5B9 #403D39 #252422 #EB5E28
#22223B #4A4E69 #9A8C98 #C9ADA7 #F2E9E4
#3D5A80 #98C1D9 #E0FBFC #EE6C4D #293241
#2B2D42 #8D99AE #EDF2F4 #EF233C #D90429
#353535 #3C6E71 #FFFFFF #D9D9D9 #284B63
#E7ECEF #274C77 #6096BA #A3CEF1 #8B8C89
#CFDBD5 #E8EDDF #F5CB5C #242423 #333533
#2F6690 #3A7CA5 #D9DCD6 #16425B #81C3D7
```

### Dark / Premium
Tech, finance, luxury, cinematic content.

```
#000000 #14213D #FCA311 #E5E5E5 #FFFFFF
#000814 #001D3D #003566 #FFC300 #FFD60A
#0D1B2A #1B263B #415A77 #778DA9 #E0E1DD
#0D1321 #1D2D44 #3E5C76 #748CAB #F0EBD8
#011627 #FDFFFC #2EC4B6 #E71D36 #FF9F1C
#0B090A #161A1D #660708 #A4161A #E5383B
#001427 #708D81 #F4D58D #BF0603 #8D0801
#001524 #15616D #FFECD1 #FF7D00 #78290F
```

### Jewel / Rich
Luxury, events, sophisticated, high-end content.

```
#5F0F40 #9A031E #FB8B24 #E36414 #0F4C5C
#780000 #C1121F #FDF0D5 #003049 #669BBC
#10002B #240046 #3C096C #5A189A #7B2CBF
#355070 #6D597A #B56576 #E56B6F #EAAC8B
#6F1D1B #BB9457 #432818 #99582A #FFE6A7
#231942 #5E548E #9F86C0 #BE95C4 #E0B1CB
#461220 #8C2F39 #B23A48 #FCB9B2 #FED0BB
#780116 #F7B538 #DB7C26 #D8572A #C32F27
```

### Monochrome
Dramatic, typography-focused, serious content.

```
#F8F9FA #E9ECEF #DEE2E6 #CED4DA #ADB5BD #6C757D #495057 #343A40 #212529
#0466C8 #0353A4 #023E7D #002855 #001233
#012A4A #013A63 #01497C #2A6F97 #468FAF #89C2D9
#582F0E #7F4F24 #936639 #A68A64 #C2C5AA
#463F3A #8A817C #BCB8B1 #F4F3EE #E0AFA0
#03071E #370617 #6A040F #9D0208 #DC2F02 #F48C06 #FFBA08
#590D22 #800F2F #A4133C #FF4D6D #FF8FA3 #FFCCD5
#220901 #621708 #941B0C #BC3908 #F6AA1C
```

### Nature / Earth
Sustainability, outdoor, organic, wellness content.

```
#606C38 #283618 #FEFAE0 #DDA15E #BC6C25
#DAD7CD #A3B18A #588157 #3A5A40 #344E41
#386641 #6A994E #A7C957 #F2E8CF #BC4749
#CAD2C5 #84A98C #52796F #354F52 #2F3E46
#F0EAD2 #DDE5B6 #ADC178 #A98467 #6C584C
#132A13 #31572C #4F772D #90A955 #ECF39E
#6B9080 #A4C3B2 #CCE3DE #EAF4F4 #F6FFF8
#233D4D #FE7F2D #FCCA46 #A1C181 #619B8A
```

### Neon / Electric
Gaming, tech, nightlife, Gen Z content.

```
#F72585 #B5179E #7209B7 #560BAD #3A0CA3
#70D6FF #FF70A6 #FF9770 #FFD670 #E9FF70
#7400B8 #6930C3 #5E60CE #5390D9 #48BFE3
#0B132B #1C2541 #3A506B #5BC0BE #6FFFE9
#540D6E #EE4266 #FFD23F #3BCEAC #0EAD69
#2D00F7 #6A00F4 #8900F2 #A100F2 #F20089
#FF6D00 #FF7900 #FF8500 #FF9100 #240046
#BBFBFF #8DD8FF #4E71FF #5409DA
```

### Pastel / Soft
Fashion, beauty, lifestyle, wellness content.

```
#CDB4DB #FFC8DD #FFAFCC #BDE0FE #A2D2FF
#CCD5AE #E9EDC9 #FEFAE0 #FAEDCD #D4A373
#FFD6FF #E7C6FF #C8B6FF #B8C0FF #BBD0FF
#FFA69E #FAF3DD #B8F2E6 #AED9E0 #5E6472
#EDAFB8 #F7E1D7 #DEDBD2 #B0C4B1 #4A5759
#555B6E #89B0AE #BEE3DB #FAF9F9 #FFD6BA
#006D77 #83C5BE #EDF6F9 #FFDDD2 #E29578
#0081A7 #00AFB9 #FDFCDC #FED9B7 #F07167
```

### Warm / Editorial
Storytelling, documentaries, case studies, narrative content.

```
#264653 #2A9D8F #E9C46A #F4A261 #E76F51
#335C67 #FFF3B0 #E09F3E #9E2A2B #540B0E
#F4F1DE #E07A5F #3D405B #81B29A #F2CC8F
#F6BD60 #F7EDE2 #F5CAC3 #84A59D #F28482
#003049 #D62828 #F77F00 #FCBF49 #EAE2B7
#588B8B #FFFFFF #FFD5C2 #F28F3B #C8553D
#283D3B #197278 #EDDDD4 #C44536 #772E25
#0D3B66 #FAF0CA #F4D35E #EE964B #F95738
```

## Frame presets

Thirteen ready-made, fully-specified visual systems for a video's design spec — each a self-contained "brand" with locked colors, typography, spacing, corner/shadow rules, and named layout treatments for common frame types (cover, data grid, quote, closing plate, etc.). Adopt one as a starting point, or use several as reference points when building a custom system. Each preset below lists: its overall look and best-fit use case, its color tokens, its typography system, its depth/shadow rules, its shape/corner rules, its named component patterns, its named frame-treatment recipes, its explicit do's and don'ts, and known limitations. All are specified for a 1920×1080 primary frame (with guidance for 9:16 vertical and 1:1 square), using a "percent of frame width" unit so sizes hold proportionally at any render resolution — treat any size given as a percentage of frame width unless marked as a fixed pixel value (fixed borders/hairlines especially). None of these presets include motion/timing specs — pair a chosen preset with the Motion Principles and Beat Direction rules above for animation.

A rule common to every preset below and worth stating once: **never invent numbers.** None of these systems fabricate figures, dates, percentages, or counts — every number that appears in a data cell, stat callout, or chart must trace back to real source content; until real content is available, render an explicit placeholder rather than a made-up value.

---

### Biennale Yellow
**Look:** Literary-editorial catalogue — warm parchment ground, a single deep-indigo ink, solar yellow deployed as a radial "bloom," panel fill, or tile underprint. Instrument Serif display type (tight, negative-tracked) + Archivo body + JetBrains Mono for data. Strict rectangles (zero rounded corners), 1px hairline rules as the only border, no shadows.
**Pick when:** confident, atmospheric, restrained — a product that wants museum-catalogue elegance and editorial authority.

**Colors:** paper `#E9E5DB`, paper-deep `#DCD6C4`, sun `#F1EE2E`, sun-soft `#F8F39B`, haze `#F0DA7C`, ink `#1B2566`, ember `#E26B4A`.

**Typography:** two ramps. Reading/data ramp in Archivo (body ~0.85% of frame width, micro-labels 13px/600 weight uppercase tracked 0.18em, JetBrains Mono for all numerals/dates). Display ramp in Instrument Serif, weight 400 only, tight line-height (0.84-1.06), slight negative tracking, ranging from a small ledger-title (~1.55% width) up to a jumbo numeral (~28% width). Legibility floor: any load-bearing line ≥1.4% of frame width. Fit headline size to its word count: ≤3 words → the largest display size; 4-6 words → the mid headline size; 7+ words → the smallest headline size.

**Depth:** atmospheric, not structural — a large soft radial "sun bloom" (42-70% of frame) is the primary depth layer on every frame, one per frame; an optional smaller "ember" counter-bloom (15-22% opacity) in the opposite corner; a translucent yellow rectangle grid ("block-tile") as underprint on cover/colophon frames; a full "yellow panel" flood for the strongest color statement (ink text on top). Zero box-shadow, zero text-shadow, zero rounded corner, no border thicker than 1px anywhere.

**Shapes:** zero radius on everything — strict rectangles; blooms are edgeless (fade to transparent).

**Named components:** sun-bloom / ember-bloom (atmospheric depth), block-tile (poster underprint), yellow-panel (full-bleed color statement, ink text on top), hairline-rule (the only border, 1px ink, or an 18-20%-opacity soft variant for dense rows), strand-row (numbered editorial list row: serif numeral + serif title + sans body), ledger-row (4-column tabular row: mono date · serif title · sans venue · mono duration), footer-band (4-column metadata strip), vertical-rail (rotated section marker up the left edge), pagenum (mono page number, bottom-right, the one persistent chrome element).

**Frame treatments:**
- **Cover** — parchment + a large sun bloom (left-of-center) + an ember counter-bloom opposite it. A 2-line display headline (italic key word) in ink, left-anchored under a micro-label; a serif date-rail top-right; a 4-column footer-band at the foot. ~Low density, sparse.
- **Chapter Divider** — a corner-anchored sun bloom behind a single huge jumbo numeral (the section ordinal) with a serif title beneath and a rotated vertical-rail label up the left edge. Low density.
- **Ledger** — the one dense frame: a 4-column tabular calendar (mono date · serif title · sans venue · mono duration) separated by soft hairline rules under a solid header rule. Density achieved through quiet repetition, not visual richness.
- **Manifesto / Quote** — a centered sun bloom behind a 2-line italic serif quote in ink, under an oversized serif quote mark, with a micro-label attribution beneath. ~60% empty, deliberately open.
- **Poster Panel** — a full-bleed yellow panel (column or third) with a serif headline sitting directly on it in ink (ink-on-yellow is the signature move); the paper side of the frame stays open.
- **Strand List** — a subtle sun bloom behind a numbered editorial list (serif numeral + serif title + sans body), soft hairline separators between rows.

**Do:** start on warm parchment with one sun bloom (optionally an ember counter-bloom); set every line in ink; use Instrument Serif 400 for display, Archivo for body, JetBrains Mono for all numerals/dates; make every separator a 1px ink hairline; flood a yellow panel for poster moments; keep micro-labels uppercase tracked 0.16-0.32em; pin the page number bottom-right; lean sparse.
**Don't:** no drop shadows, no rounded corners, no bordered cards, no border thicker than 1px; no second text color; no bold Instrument Serif; no inverted (yellow-on-ink) type; no mono for body/display; don't crowd the canvas; don't blow a headline edge-to-edge.

**Known gaps:** motion is intentionally out of scope for this spec (composition only). Fonts: Instrument Serif, Archivo, JetBrains Mono. 9:16/1:1 behavior is guidance, not pixel-locked — verify legibility per aspect ratio.

---

### BlockFrame
**Look:** Maximalist neobrutalist — 4px black borders, 8px hard offset shadows (zero blur), a five-pastel candy palette cycling as full-bleed backgrounds, Inter 800-900 uppercase display, Space Grotesk label chrome, square corners, tilted decorations, star bursts, stripe blocks, dot grids.
**Pick when:** bold, punchy, playful-loud — a product that wants to feel confident and graphic.

**Colors:** black `#000000`, white `#FFFFFF`, off-white `#FFFDF5`, pink `#FE90E8`, blue `#C0F7FE`, green `#99E885`, yellow `#F7CB46`, cream `#FFDC8B`.

**Typography:** reading/chrome ramp in Inter (body ~0.95% width/500 weight, card-title ~1.15%/700 uppercase) plus Space Grotesk labels (13px/600 uppercase tracked 0.08em). Display ramp in Inter 700-900, always uppercase, negative-tracked, ranging from a mid heading (~2.1% width) to a large heading (~5% width). Legibility floor ≥1.4% width. Fit to measure: ≤3 words → largest, 4-6 → mid, 7+ → smallest.

**Depth:** hard offset shadow only — solid black, zero blur, bottom-right offset. Primary cards use an 8px-equivalent offset paired with a 4px border; smaller chrome elements use a 4px offset paired with a 3px border (the two always move together). A 12px yellow shadow (plus a 6px white shadow on the close button) is the one colored exception, reserved for the inverted black closing frame.

**Shapes:** zero radius everywhere except one round "stat-deco" dot (12px, the only circular element in the whole system).

**Named components:** card-elevated / card-small (bordered + hard-shadowed content cards, border/shadow weight coupled), label-pill (the universal eyebrow — border + shadow + pastel fill, never plain text), button-primary (yellow CTA), star-burst (10-point clip-path star, corner attention-grabber), stripe-block (45° black+pastel diagonal stripes, poster decoration), bg-dot-grid (faint radial-dot background overlay), tilt-deco (a rotated ±2°-12° rectangle/badge/star — the signature grid-puncturing move; stat cards alternate -2°/+2°), stat-deco-dot (the lone round shape, pinned to stat cards), close-frame (the inverted black+white+yellow-shadow closing treatment).

**Frame treatments:**
- **Cover** — cream/off-white ground + faint dot-grid. A 2-3 line uppercase heading, left, under a label-pill; tilted pastel rectangles + a star burst puncture the right side.
- **Feature Cards** — blue ground; three white bordered+shadowed cards (icon square + title + body) under a label-pill eyebrow. The dense-exception frame.
- **Stat Grid** — green ground; three tilted (alternating -2°/+2°) bordered stat cards, each with a round stat-deco dot. Also dense-exception.
- **Closing Plate** — black ground; a white sign-off inside a white-bordered frame carrying the 12px yellow offset shadow (the one colored shadow in the system); a pink star bursts a corner.
- **Quote** — pink/off-white ground; an uppercase quote inside a white bordered+shadowed frame.
- **Timeline** — off-white ground; a row of bordered step cards linked by black connector bars, each tinted a different pastel.

**Do:** pair 4px borders with 8px shadows and 3px with 4px (non-negotiable coupling); cycle pastel grounds across frames for rhythm; keep Inter display uppercase 800-900 negative-tracked; open every region with a label-pill; render shadows solid black zero-blur bottom-right; add at least one decoration (tilt/star/stripe/dots) per frame; use yellow for CTAs; tilt decorations ±2°-12°.
**Don't:** no rounded corners (save the stat-deco dot); no blurred shadows; no colored borders (black only, save the close-frame's white); no sixth pastel color; no sentence-case or untracked display type; don't keep everything perfectly aligned (the tilt is the signature); don't leave corners empty.

**Known gaps:** motion out of scope. Fonts: Inter, Space Grotesk. 9:16/1:1 are guidance; decoration count should scale down on tighter ratios.

---

### Blue Professional
**Look:** Consulting-grade restraint — a warm cream canvas, a single saturated cobalt (`#1e2bfa`) as the only accent, a three-step gray text ladder, Space Grotesk (display/numerals/chrome) + Inter (body), softly tinted cards (4% fill / 20% border / 10-14px radius) with NO shadows, pill-shaped chrome (100px radius), and a cobalt progress bar.
**Pick when:** measured, executive-readable, premium-signal — a product that wants investment-research rigor and refined restraint.

**Colors:** bg `#fdfae7`, primary (cobalt) `#1e2bfa`, text `#111111`, text-muted `#6b6b6b`, text-light `#9a9a9a`, accent-light `rgba(30,43,250,0.08)`, accent-medium `rgba(30,43,250,0.15)`, border `rgba(30,43,250,0.2)`, card-bg `rgba(30,43,250,0.04)`, positive `#059669`, negative `#dc2626`.

**Typography:** reading ramp in Inter (body ~0.85% width/400, muted gray) plus a Space Grotesk uppercase eyebrow (600 weight, tracked 0.08em, cobalt). Display/numerical ramp in Space Grotesk — near-black headings from a small h3 (~1.25% width) up to a large h1 (~4.2% width), and cobalt numerals from a stat number (~1.9%) up to a metric-value (~3.0%). Legibility floor ≥1.4% width. Headlines stay near-black — never cobalt.

**Depth:** soft and tinted, never offset. Tinted cards use a 4% cobalt fill + a 20%-opacity cobalt 1.5px border + a 10-14px radius; a 4px cobalt left-border accent pulls a callout forward. Zero box-shadow on content (the only shadow anywhere is a soft cobalt glow on CTA hover).

**Shapes:** 100px pill radius for tags/CTA/nav; 10-14px radius for cards (scaled by card size); 6px for bar tracks/fills; 50% for step circles/dots/rings; zero radius only on the progress bar. No square-cornered content container exists in this system.

**Named components:** card-tinted / metric-card (the universal soft-tint content cards, no shadow), tag-pill (top-right of a slide header), cta-button (the one fully solid cobalt element in the system), accent-line (a short cobalt rule above cover titles), bar-track (a 28px data bar with a cobalt fill), step-circle (56px circle, sequential steps fade to lower opacity), split-highlight (an inline pull-quote callout with a 4px cobalt left border), slide-header (the standard eyebrow + tag-pill + heading top band of every content frame), atmosphere (a clipped diagonal cobalt-tint panel, a 3×3 cobalt dot grid, or concentric closing rings — reserved for cover/closing only), progress-bar (a persistent 3px cobalt strip along the bottom edge).

**Frame treatments:**
- **Cover** — cream + a clipped diagonal cobalt-tint panel (right ~36%) + a small cobalt dot grid. A 2-line near-black headline, left, under a cobalt accent-line.
- **Dashboard** — the dense frame: a row of tinted metric cards, each a cobalt figure + label + muted description + an optional green/red change indicator.
- **Bar Ranking** — 3-5 labeled cobalt-fill bars on light cobalt tracks with cobalt percentage labels.
- **Pull Quote** — a near-black quote under a faint 15%-opacity cobalt quote-mark, centered, with faint concentric rings behind it.
- **Split + Highlight** — a text column beside a tinted highlight block (4px cobalt left rule) carrying an inline pull quote.
- **Closing / CTA** — a centered near-black sign-off with the one solid cobalt CTA pill beneath it, concentric rings behind.

**Do:** start every frame on warm cream; let cobalt carry every accent (eyebrow, numeral, CTA, bar, progress); keep headlines near-black; use tinted cards (no shadow); keep all chrome pill-shaped; reserve atmosphere for cover/closing only.
**Don't:** no second accent color; no cobalt headlines; no drop shadows on content; no opaque cobalt borders; no square corners (save the progress bar); don't use the positive/negative change indicators as general accents — directional comparisons only.

**Known gaps:** motion out of scope. Fonts: Space Grotesk, Inter. 9:16/1:1 are guidance — the diagonal cover panel should become a top/bottom band on 9:16.

---

### Bold Poster
**Look:** Populist editorial poster — a four-color-only palette (white / brown-black ink / tomato red / off-white), Shrikhand display type tilted -6° to +2°, Libre Baskerville serif body, Space Grotesk mono chrome, double-border grids (3px outer + 1.5px inner), red leftbar cards, red em-dash bullets (max 3), stacked text-shadow on red display type.
**Pick when:** powerful, printed, restrained — a product that wants editorial authority and vintage gravitas.

**Colors:** bg (white) `#FFFFFF`, dark `#1C1410`, red `#D8000F`, light (off-white) `#F5F2EF`.

**Typography:** reading/chrome ramp in Libre Baskerville (body ~0.85% width/400, line-height 1.75) plus Space Grotesk mono labels (10px/600 uppercase tracked 2px). Display/hero ramp in Shrikhand weight 400 only, tilted on statement elements, red on numerals — from a card-title (~1.9% width) up to a stat-big (~22% width). Legibility floor ≥1.4% width. ≤2 words → the biggest sizes; 3-4 → hero-title; 5+ → section-header. A "hero" is a stacked 3-line composition.

**Depth:** flat plane — heavy borders (3px+1.5px double-border grids, 2px card outlines, 4px red leftbar rules), full-bleed color-surface inversion (red or dark statement panels), and rotation/tilt for perceived dimension are the only depth devices. The ONE shadow in the entire system is a stacked text-shadow (three offset steps) applied only to red display text on red panels.

**Shapes:** zero radius everywhere except a small "hint pill" (4px) — otherwise sharp rectangles throughout.

**Named components:** progress-bar (a red strip along the bottom edge), hero-title-stack (a signature 3-line tilted Shrikhand composition, at least one tilt, at least one red line), stat-big (a poster-scale numeral, rotated -6°), fin-grid (the double-border tabular data-grid signature), red-leftbar-card (an editorial card cantilevered off a 4px red left rule, no outline), red-panel / dark-panel (full-bleed statement surfaces), stacked-text-shadow (the one sanctioned shadow, red display on red only), bullet (a red em-dash or round marker, capped at three items).

**Frame treatments:**
- **Hero Stack** — white ground; a 3-line tilted Shrikhand stack (one red line, at least one tilted), a mono eyebrow + serif tagline, bottom progress bar.
- **Hero Stat** — full red panel; a huge white numeral rotated -6° with the stacked shadow, centered.
- **Financial Grid** — the dense frame: a double-border ink grid of cells, each a red Shrikhand numeral + mono label + serif body.
- **Pull Quote** — full red panel; a 2-line white Shrikhand quote with the stacked shadow, serif citation beneath.
- **Editorial Cards** — white (or alternating off-white stripe) ground; 2-3 cards cantilevered off 4px red rules, red em-dash bullets (max 3).
- **Closing Statement** — white or dark ground; a tilted (-5°) red sign-off, mono eyebrow + serif contact line.

**Do:** stack hero titles across 3 Shrikhand lines with at least one tilt and one red line; make every numeral red Shrikhand; tilt statement display -5° to -6°; build data grids with the double border; use red em-dash bullets capped at three; one display moment per frame.
**Don't:** no second accent color; no rounded corners (save the hint pill); no drop shadow besides the stacked text-shadow on red; no font substitutes; no default disc bullets; no untilted red statement display.

**Known gaps:** motion out of scope. Fonts: Shrikhand, Libre Baskerville, Space Grotesk.

---

### Broadside
**Look:** Protest-poster system — a two-register flat-plane surface system (ink-black / fire-orange), massive lowercase Barlow at weight 900 treated as a graphic primitive rather than as text, IBM Plex Mono chrome (uppercase, tracked 0.14em), fire-orange as the sole accent color, 1px hairlines, sharp corners, no shadow.
**Pick when:** bold, typographic, declarative — a product that wants presence and authority.

**Colors:** ink-black `#111111`, ink-black-alt `#1A1A18`, fire-orange `#E85D26`, cream `#F0ECE5`, cream-muted `#888880`, cream-hint `#505048`, border-dark `#282826`, plus dark-ink-on-orange overlay tones at 75%/55%/40%/20% opacity for muted text on the orange register.

**Typography:** reading ramp in Barlow (body ~1.2% width/400, mono label ~0.72%/500 tracked 0.14em uppercase). Display/hero ramp entirely in Barlow, always lowercase, weight 700-900, negative-tracked — from a mid heading (~4.5% width) to a full-bleed display word (~13% width, negative-tracked -0.04em). Legibility floor ≥1.4% width. Only ONE display moment per frame. ≤2 words → the biggest display; 3-4 → the large heading; 5+ → the mid heading.

**Depth:** flat plane only — weight+size contrast is the dominant hierarchy signal; 1px hairlines carry structure (chrome bars, card tops, dividers, chart baselines); color shift (orange-on-ink vs. ink-on-orange) and generous negative space do the rest. Zero box-shadow, zero elevation, zero rounded surface (save nav dots), zero gradient ground.

**Shapes:** zero radius everywhere except round navigation dots.

**Named components:** registers (the two-surface system — choose ONE per frame: dark ground/cream text/orange accent, or orange ground/ink text), slide-chrome (optional hairline top/bottom bars, suppressed on declarative frames like cover/statement/quote so type can fill the field), kicker (uppercase mono eyebrow), rule (a small stub accent bar, the system's only ornament), broadside-num (a mono catalogue numeral, top-left of cover/chapter), stat-card (top-border-only block, no other borders), bullet (an orange "/" mono marker, capped at three), bar-track (a left-axis-only vertical bar chart, one bar gets the accent color), compare-panel (a two-panel before/after split, the "after" panel may fill with orange), fadelist (three stacked words at descending opacity plus one oversized title opposite).

**Frame treatments:**
- **Cover** — orange register. A 1-2 word lowercase display word, left-anchored, over a small ink rule stub + mono kicker.
- **Statement** — dark register. A 2-4 word lowercase display line in cream, with exactly ONE clause inked in fire-orange.
- **Stat Grid** — dark register, the dense frame: three top-border-only stat cards, big orange 900-weight numerals.
- **Fadelist** — dark register; a three-stage opacity-fading word stack opposite an oversized orange title (e.g. before/during/after).
- **Pull Quote** — dark register, chrome suppressed; a lowercase Barlow quote under an oversized fire-orange quote mark.
- **Compare** — dark-ink-black left panel (documents) + fire-orange right panel (declares the payoff), split by a 1px divider.

**Do:** set every Barlow display in lowercase weight 900, negative-tracked; use fire-orange as full environment on declarative frames, as the lone accent on dark; keep chrome in uppercase tracked mono; cap bullets at three; one statement per frame; suppress chrome bars on cover/chapter/statement/quote/end.
**Don't:** never uppercase Barlow display; never add a second accent color; never put cream text on orange (ink-on-fire is absolute); no drop shadow, no rounded surface (save nav dots); no serif companion font; don't pack two display moments into one frame.

**Known gaps:** motion out of scope. Fonts: Barlow, IBM Plex Mono.

---

### Capsule
**Look:** Playful editorial where every container is a pill — 9999px radius on small elements, 2rem radius on cards, a 2px ink outline on everything, a sun-bleached cream canvas, a nine-color candy accent palette, Bodoni Moda + Space Grotesk, soft hard-offset shadows (4/6/8/12px in 8% ink), floating decorative-pill "wallpaper," radial accent glows, and a grain overlay.
**Pick when:** friendly, soft, editorial — a product that wants warmth and approachability.

**Colors:** cream `#F5F5F0`, ink `#1A1A1A`, outline `#1E1E1E`, white `#FFFFFF`, plus nine candy accents: coral `#E85D4E`, lime `#C4D94E`, lavender `#C5B5E0`, sky `#8BB4F7`, violet `#A06CE8`, yellow `#F2D160`, peach `#F5B895`, mint `#A8E6CF`; shadow color `rgba(26,26,26,0.08)`.

**Typography:** reading ramp in Space Grotesk (body ~0.85% width/400, uppercase tracked pill/label text). Display/hero ramp in Bodoni Moda, always ink, always sentence case, weight 700-800 — from a card-headline (~1.9% width) up to a full display (~12% width). Legibility floor ≥1.4% width. Bodoni display is never colored (color lives only on stat numerals and pill fills, never on headlines).

**Depth:** a soft hard-offset shadow (in the 8% ink shadow color, bottom-right) is the only depth device, scaling from ~4px on small nodes up to ~12px on the largest visual frame. The 2px outline does most of the visual lift against the cream background; the shadow adds float. Decorative floating pills deliberately cast NO shadow — this is what separates "content" from "atmosphere" at a glance.

**Shapes:** 9999px radius on all small pills (chips, buttons, bars, nodes, floating pills, accent lines); 2rem radius on larger content cards; 50% on circular elements (card icons, step nodes, orbit centers, nav dots); zero radius only on the grain overlay itself and the gradient region inside a visual frame — there is no sharp-cornered text container anywhere in this system.

**Named components:** pill (the universal 2px-outlined container — no unstroked pill exists), pill-card / stat-pill / title-pill (white/yellow content pills with soft shadows), card-icon (a circular candy-colored mark), floating-pill (flat, tilted -20° to +25°, no-shadow decorative "confetti," 5-8 per declarative frame), quote-highlight (an inline candy-colored pill wrapping an emphasized phrase inside a quote — the emphasis mechanism, replacing bold/italic), bar-track (a pill-shaped chart bar), accent-line (a coral pill-shaped rule), atmosphere (1-3 radial candy-colored glows at 6-15% opacity plus a 4% grain overlay — present on every frame, never absent).

**Frame treatments:**
- **Cover** — cream + atmosphere + 5-8 floating decorative pills. A 1-2 line display headline in ink (italic key word in a candy hue), centered, under a yellow title-pill.
- **Pillar Cards** — the dense frame: three white 2rem pill-cards (circular candy icon + headline + body), no floating pills here.
- **Stat Grid** — a row of white stat-pills, each with a COLORED headline number (the one place color meets the display type) plus an uppercase label and accent bar.
- **Pull Quote** — a few floating pills; a Bodoni quote in ink with one phrase wrapped in a lime/sky highlight pill (never bold — this is the emphasis mechanism).
- **Orbit** — a large candy-colored circular center (an ordinal number) orbited by 4-6 tilted candy satellite pills.
- **Closing Plate** — cream + atmosphere + floating pills; a display sign-off in ink (italic word in a candy hue), centered.

**Do:** make every text container a pill with the 2px ink outline; set Bodoni headlines in ink sentence case (color lives on stat numerals + pill fills only); use soft offset shadows on content containers, keep floating pills flat; float 5-8 candy pills + glows + grain on declarative frames; wrap inline emphasis in a candy highlight pill, never bold/italic alone.
**Don't:** no sharp-cornered text container; no unstroked pill; no colored Bodoni headline; no uppercase Bodoni; no blurred or recolored shadow; no tenth accent color; no shadow on decorative floating pills.

**Known gaps:** motion out of scope. Fonts: Bodoni Moda, Space Grotesk.

---

### Cartesian
**Look:** Museum-catalog editorial — a 1px taupe hairline grid as the universal structural device, a five-tone warm-stone palette, Playfair Display 400 + Inter, sharp corners, compass-drafted geometric rings, zero shadow, zero fill.
**Pick when:** sparse, literary, restrained — a product that wants quiet authority and editorial rigor.

**Colors:** bg-primary `#EDE8E0`, bg-secondary `#E2DBD1`, text-primary (ink) `#1A1A1A`, text-secondary (gray) `#5A5A5A`, accent (taupe) `#8A8178`, line (taupe) `#B8B0A4`, white-overlay `rgba(255,255,255,0.3)`.

**Typography:** reading ramp in Inter (body ~1.0% width/400 gray, labels in px taupe uppercase tracked 2-3px). Display ramp in Playfair Display, weight 400 only, sentence case — from a small h3 (~1.8% width) up to a full display (~8.0% width). Legibility floor ≥1.4% width. No hero-stat numeral in this system — stats stay modest scale (~3% width). Playfair is never bold, never uppercase, never taupe.

**Depth:** the flat plane is the only technique — type contrast (serif vs. sans, and the scale range itself) carries hierarchy, plus universal 1px taupe hairlines (every divider, card outline, timeline rule, photo ring), tone shifts (ink vs. gray vs. taupe), generous negative space, and compass-drafted geometric ring decoration that suggests depth without creating any. Zero box-shadow, zero elevated card, zero gradient, zero rounded rectangle (circles only).

**Shapes:** 50% (circle) only — card icons, portrait frames, nav dots, and every geometric ring; zero radius on everything else, no soft-rounded corners exist anywhere.

**Named components:** hairline (the universal 1px taupe separator — the core identity of this preset), card (1px taupe border + a faint white-overlay fill so the canvas bleeds through), card-icon (a ringed circle mark), agenda-row (numeral left, label right, over a taupe rule), timeline (a single taupe top rule across items — no nodes, no dots), stats-cluster (modest inline stat figures, no hero numeral), geo-ring (compass-construction circles behind content, solid + dashed, 1-2 per frame max, never more), horizontal-accent (the system's only ink-black rule, used sparingly on cover/closing), vertical-line (a faint drafting-paper alignment guide, optional), image-placeholder (a crossed-X mark in the secondary background tone — the signature "image not wired yet" placeholder), team-photo (a circular ringed portrait frame).

**Frame treatments:**
- **Cover** — a display headline in ink (italic on the key word), left-anchored, with a taupe label above and an Inter subtitle below, one geometric ring off to the side.
- **Agenda / Index** — a heading over 4-6 agenda rows (a taupe numeral + an ink label), each on a 1px taupe rule.
- **Pull Quote** — a centered 2-line quote in ink under a faded taupe Playfair quote mark, a centered dashed compass ring behind it.
- **Closing Plate** — a centered 1-2 line sign-off in ink (italic key word), centered inside the largest compass ring on the page, with a short ink accent rule beneath.
- **Two-Column Editorial** — a text column beside an image-placeholder or card, asymmetric split.
- **Stats / Timeline** — a modest stat row or a hairline-rule timeline (year + headline + body, no nodes), framed by a top rule.

**Do:** use a single 1px taupe line for every separator; set every Playfair headline at 400/ink/sentence case; layer one or two compass rings behind content for atmosphere; let frames breathe (55-60% empty on declarative frames); lean centered on quote/closer, asymmetric/left on cover/agenda/editorial.
**Don't:** don't introduce a populist accent color — stone and ink only; don't bold Playfair, set headlines in taupe, or use thick (2px+) borders; don't add shadows, elevated cards, or rounded rectangles; don't crowd the frame; never more than two geometric ring decorations per frame.

**Known gaps:** motion out of scope. Fonts: Playfair Display, Inter. Cartesian has no genuinely "dense" frame — even its index/agenda frame is meant to breathe; crowding breaks the system.

---

### Claude
**Look:** A warm-editorial brand book — warm cream paper (never pure white, never cool), a single terracotta coral used as scarce "voltage," hairline-ink elevation (no heavy shadow), EB Garamond serif for all display type + Inter body + JetBrains Mono for an index/code voice on a warm-navy code surface, sentence-case display, and a small coral "spike" (✱) mark.
**Pick when:** considered, literary, developer-facing — content that wants editorial calm and a first-class code/technical surface.

**Colors:** ink `#141413`, cream `#FAF9F5`, tile `#EFE9DE`, tile-strong `#ECE3D4`, coral `#CC785C`, navy `#181715`, navy-soft `#1F1E1B`, navy-elev `#252320`. Fixed syntax-highlight colors used only inside code panels (decoration, not brand hues): teal `#5DB8A6` for strings, amber `#E8A55A` for numbers, plus status colors success `#5DB872` / warn `#C64545`.

**Typography:** reading/chrome ramp in Inter (body ~1.5% width/400; lead ~2.08%) plus JetBrains Mono kickers/labels in px, uppercase, tracked 0.16-0.18em. Display ramp in EB Garamond, weight 400 only, sentence case (never title case, never uppercase), negative-tracked — from a headline (~4.6% width) up to a cover display (~9.9% width); italic is used deliberately when a line is a stance or definition. Legibility floor ≥1.4% width. ≤3 words → the biggest cover-scale display; 4-6 → the mid display; 7+ → the smaller headline size.

**Depth:** hairline elevation only — a 1px ink border at ~12% opacity is the primary lift; a single soft warm shadow (very subtle, two-layer) is used rarely, never heavy; a half-step "tile" surface color (rather than a cast shadow) is how a content block reads as elevated above the cream ground. No heavy drop shadow, no glow, no gradient on content, no tilt anywhere — the system has no strong light source to simulate; it reads through warmth and hairline instead.

**Shapes:** 6px small chrome, 8px cards/the code surface, 12px large cards/quote frames, 9999px true pills only. No square corners, no heavy rounding — the register is gently rounded, never hard.

**Named components:** card-hairline (the editorial content card — hairline border + at most one soft shadow, never heavy), kicker-spike (the eyebrow: uppercase mono, indexical 2-5 words, prefixed with the coral ✱ mark, never a full sentence), coral-callout (the ONE "voltage" moment allowed per frame — a CTA, a single inline link, or a full-bleed coral band; never two corals in one frame), number-lockup (a serif figure paired with a mono unit — the unit is always mono, never serif — e.g. a headline stat paired with its label), pull-quote (an italic EB Garamond quote plus a small uppercase citation line), section-rule (the only separator, a 1px hairline; a coral 1px rule may introduce a section), code-surface (the warm-navy code/terminal surface — title bar, status strip, and mono chrome; the actual code content is a separate rendering concern this preset doesn't own), spike-mark (the ✱ brand glyph, always coral).

**Frame treatments:**
- **Cover** — cream ground; a 2-3 line sentence-case display headline under a coral ✱ kicker; a small mono index strip (e.g. repo/branch-style metadata).
- **Statement** — cream (or navy for extra gravity) ground; one 2-line display line carrying the change in a single sentence, italic if it's a stance.
- **Code Surface** — a cream frame around a warm-navy code panel (title bar + filename in mono); syntax highlighting uses coral/teal/amber inside the panel only.
- **Number / Impact** — cream ground; an oversized serif figure with a mono unit over a hairline rule (e.g. an impact statistic).
- **Pull-quote** — cream ground; an italic serif quote with a small uppercase citation beneath.
- **Closing / CTA** — cream (or navy) ground; a short sign-off with the one coral-callout CTA, optionally a row of hairline-ringed avatar-style chips for a "credits" close.

**Do:** stand every frame on the warm cream floor, gather content on a half-step tile surface; set all display in sentence-case EB Garamond, negative-tracked; ration coral to exactly one moment per frame; elevate with a hairline plus at most one soft shadow; reserve warm navy for the code/terminal surface only; pair every stat figure with a mono unit.
**Don't:** no pure white, no cool gray, no pure black; no fourth brand hue; no heavy drop shadow, glow, gradient, or tilt; no uppercase or title-case display; no sans headline; no serif label; no two coral moments in one frame.

**Known gaps:** motion out of scope — a companion motion-language reference (short cross-dissolves, no overshoot/bounce/elastic, coral as the only "draw-on" accent, numbers count up, code types on line by line) would live alongside the atomic-motion reference rather than here. Fonts: EB Garamond (author display at weight 400 — 700 reads as an off-register heavy bold; treat italic as a browser-synthesized slant), Inter, JetBrains Mono.

---

### Cobalt Grid
**Look:** A two-color risograph trend-report — warm cream paper, electric cobalt as the only ink, a permanent graph-paper grid behind every frame, Newsreader serif (weight 400 only) + Hanken Grotesk + DM Mono, top/bottom cobalt hairlines framing every composition, a signature "pixel-glitch" scanline column and QR-style mosaic patch.
**Pick when:** restrained, systemic, editorial — a product that wants clarity and measured authority.

**Colors:** paper `#F0EBDE`, paper-2 `#E6E0CE`, ink (cobalt) `#1F2BE0`, ink-soft `#5560E5`, grid `rgba(31,43,224,0.10)`, ink-faint `rgba(31,43,224,0.18)`.

**Typography:** reading ramp in Hanken Grotesk (body ~0.83% width/400, uppercase tracked micro-labels in px) plus DM Mono for chrome. Display/hero ramp in Newsreader, weight 400 only (hierarchy comes from SIZE, never weight) — from a headline (~4.6% width) up to a huge numeral (~12.5% width, negative-tracked -0.015em). Legibility floor ≥1.4% width.

**Depth:** flat, structural only — 1.5px cobalt rules (slide hairlines, section-header rule, chart baseline), 1px faint-ink dividers for dense list/ledger rows, the permanent graph-paper grid as a measured-plane background tone, and the pixel-glitch/QR decorations as texture and graphic punctuation with no z-axis depth implied. No drop shadow (a QR patch's slight paper-colored outset is an anti-shadow for legibility, not elevation), no gradient, no rounded corner, no second ink color anywhere.

**Shapes:** zero radius everywhere — frames, rows, QR cells, glitch blocks, charts. Zero circular elements — the squareness is part of the identity.

**Named components:** graph-grid (the permanent ~2%-width-cell graph-paper grid behind every frame, never disabled), hairlines (two persistent cobalt rules framing every composition, near the top and bottom edges), page-chrome (page number bottom-right, a small nav/meta hint bottom-left — the only persistent chrome), pixel-glitch (a decorative stair-stepped scanline column, 14-30% of frame width, placed right on cover/data frames or left on chapter/colophon frames), qr-block (an 8×8 mosaic patch, corner punctuation), topbar-rule (a section header with a solid rule beneath, on index/data/table frames), ledger-row (a dense matrix row: mono number · serif name · sans description · mono delta, with up/down/flat delta markers), pixel-stack-bar (data rendered as stacked grid-unit cells, cobalt "on" / faint "off"), vstack-label (a rotated vertical mono catalogue label along a frame edge).

**Frame treatments:**
- **Hero Cover** — a 1-2 line serif headline in cobalt, left-anchored, with an italic subtitle; a pixel-glitch column right, a QR patch top-right.
- **Index Ledger** — the dense frame: a topbar over 4-6 ledger rows (mono number · serif name · sans description), faint dividers, delta arrows.
- **Chapter Opener** — sparse; a chapter title with a small mono index above it, a low-opacity pixel-glitch column to one side, letting the grid show through.
- **Data Frame** — a row of 6-8 pixel-stack bars over a solid cobalt baseline with mono tick labels.
- **Manifesto / Quote** — a centered 2-3 line serif pull-quote in cobalt with a mono kicker above and a hairline attribution rule beneath.
- **Colophon** — a right-aligned closing title with a mono kicker above, a mirrored pixel-glitch column on the left, and a multi-column mono credits grid at the foot.

**Do:** keep the graph-paper grid + top/bottom hairlines on every frame — they are the system; set Newsreader at 400 in cobalt and build hierarchy through size, not weight; render data as pixel-stack cells to echo the glitch language; use the pixel-glitch column + QR patch on declarative frames (cover, chapter, quote, colophon).
**Don't:** don't introduce a second ink color; don't bold Newsreader, round any corner, or add a drop shadow (aside from the QR anti-shadow); don't disable the grid or suppress the hairlines; don't crowd chapter/quote/colophon frames — let the grid show.

**Known gaps:** motion out of scope. Fonts: Newsreader, Hanken Grotesk, DM Mono.

---

### Coral
**Look:** A bold editorial magazine built from three solid surfaces (coral fire / ink black / warm cream) meeting at hard edges, a 45° diagonal hatch texture on coral regions, Bebas Neue uppercase tracked headlines + Inter body, zero shadows/radius (circles excepted), oversized wallpaper numerals and giant decorative marks.
**Pick when:** bold, structuralist, editorial — a product that wants graphic confidence and hard-edged authority.

**Colors:** coral `#E85D5D`, coral-dark `#D44A4A`, cream `#F5F0E8`, cream-dark `#E8E0D4`, black `#1A1A1A`, gray `#6B6B6B`, light-gray `#B0B0B0`, white `#FFFFFF`.

**Typography:** reading ramp in Inter (body ~1.0% width/400; a lighter 300-weight variant for pull-quote voice; uppercase tracked labels in px). Display/hero ramp entirely in Bebas Neue, always uppercase, always tracked (1-12px depending on scale) — from a card-title (~1.9% width) up to a jumbo-feature word (~9% width, tracked 12px). A decorative background-numeral (~10% width, 12% opacity) and giant-mark (~14% width, 35% opacity) sit as wallpaper inside coral regions. Legibility floor ≥1.4% width. Every Bebas element is uppercase with at least 1px of tracking — no exceptions.

**Depth:** flat, with hard color edges as the primary structural device — accent borders (5px coral top on cards, 4px coral left on sidebar tiles, 4px ink on timeline), the 45° diagonal hatch (6% ink) as texture over coral regions with no implied depth, and oversized wallpaper typography layered behind content. Zero box-shadow, zero elevated card, zero soft gradient (one rare 135° coral-to-coral-dark gradient is the sole exception), zero rounded rectangle.

**Shapes:** zero radius on every rectangle — regions, cards, tiles, icon squares, info bars; 50% radius on circles only (nav dots, nav arrows, timeline nodes).

**Named components:** diagonal-hatch (the signature 45° texture overlay on coral regions, texture only, never implies depth), region-split (the primary layout device — two or three solid surfaces meeting at a hard edge, common ratios 38/62 or 40/60 or 50/50 — no gradient, no rounded junction), card (a white card whose only chrome is a 5px coral top border), sidebar-item (a white tile whose only chrome is a 4px coral left border), card-icon (a solid coral square holding one white glyph), accent-line (a short coral rule beneath a sub-headline), background-numeral (a large 12%-opacity wallpaper numeral behind a region's title), giant-mark (an oversized 35%-opacity decorative mark or quote glyph inside a coral region), timeline (an ink line with coral circular nodes and cream halos), info-bar (a cream-dark footer band beneath a feature region).

**Frame treatments:**
- **Region-Split Cover** — a 38/62 split: a coral top band (hatch + wallpaper numeral) over a cream field. A 2-line headline in ink, second line in coral, left-anchored in the cream field.
- **Feature Stat** — a full coral environment (hatch texture) with a large stat figure or 2-line headline in ink, a wallpaper numeral behind it as atmosphere.
- **Quote Layout** — a 40/60 split: a coral left panel (hatch + giant decorative mark) beside a black right panel carrying a light-weight cream pull quote.
- **Closing Plate** — a cream field with a bottom coral band (hatch); a centered ink sign-off with a coral accent-line beneath; the coral band carries a footer sign-off + year.
- **Three-Column Catalog** — the dense frame: a centered headline over three white cards, each with the signature 5px coral top border, an icon square, a title, body, and a coral stat.
- **Timeline** — an ink line with 4-5 coral nodes (cream halos) and Bebas labels.

**Do:** compose as multi-surface region splits meeting at hard edges — the boundary IS the layout; keep every Bebas element uppercase and tracked; render headlines in ink on cream/coral, cream on ink (never gray, never white-on-coral); apply the 45° hatch on coral regions; fill an underweight coral region with a wallpaper numeral rather than more content.
**Don't:** don't set Bebas in sentence case or untracked; don't add a fourth surface, a drop shadow, an elevation effect, or a rounded rectangle; don't put white headlines on coral (always ink) or gray headlines anywhere; don't soften a region boundary with a gradient except the one rare coral-to-coral-dark exception.

**Known gaps:** motion out of scope. Fonts: Bebas Neue, Inter.

---

### Creative Mode
**Look:** A neo-brutalist editorial poster — a warm cream canvas, 4px ink borders on every structural element, hard offset shadows (no blur) reserved for one featured block per frame, Archivo Black uppercase at a tight 0.92 line-height, JetBrains Mono taxonomy chrome, Space Grotesk body, a four-accent palette rationed to two-or-three per frame.
**Pick when:** sparse, graphic, punchy-restrained — a product that wants editorial presence and geometric confidence.

**Colors:** cream `#EFE9D9`, cream-2 `#E4DCC4`, ink `#0F0F0F`, ink-2 `#2A2A2A`, green `#1F8A4C`, green-dark `#136636`, pink `#F06CA8`, pink-dark `#D14E8B`, orange `#E85A1F`, yellow `#F5C518`.

**Typography:** reading ramp in Space Grotesk (body ~1.25-1.46% width/400) plus JetBrains Mono uppercase labels/kickers (tracked 0.06-0.14em) and an Archivo Black table-head. Display/hero ramp entirely in Archivo Black, always uppercase, always at a tight 0.92 line-height — from a display-head (~4.2% width) up to a full display-hero wordmark (~15.5% width, negative-tracked -0.02em). Legibility floor ≥1.4% width. ≤3 words → the biggest wordmark sizes; 4-6 → a large display; 7+ → the smaller display-head size.

**Depth:** zero blur, two devices only — a hard offset shadow (a same-direction solid duplicate offset by roughly 1.25% of frame width, in orange plus a thin ink outline) reserved for exactly one featured block per frame, and color-block contrast (cream on cream-2, ink on cream, accent on cream) where contrast alone carries the separation without needing a shadow at all.

**Shapes:** zero radius on every structural element (stat cells, step cards, table cells, markers, panels); 50% only on decorative circles and a meta dot; a 999px pill radius on exactly one topbar chip — the single rounded exception in the system. Rotation only at two fixed brand angles: a badge at -4°, a stamp at -6°.

**Named components:** frame-chrome (a mono topbar — section label left + a pill chip right — plus a meta footer with a descriptor + counter, present on most frames), stat-cell / step-card (ink-bordered flat-fill blocks — step sequences alternate cream with accents and always end on green), marker-block (the one hard-shadow featured callout allowed per frame), kicker-block (an inverted ink eyebrow chip), badge-rotated (a -4° tilted yellow annotation — deliberate imperfection), pill-badge (the lone rounded chip in the system), stamp (a -6°-rotated closing seal with a cream inner ring), comparison-table (an ink-headed data ledger with cream-2 fill, pink/green column-fill variants for marking a winner), decorative-circle (a yellow disc for shape contrast, typically paired with a green panel).

**Frame treatments:**
- **Wordmark Cover** — cream ground; a two-line wordmark at the largest display size, centered, second line in an accent color; ~55% empty.
- **Big Claim** — one full-bleed accent ground; a 2-3 line claim, left-anchored, ink text on the accent (never white); one small ink kicker chip above it.
- **Stat Grid** — the one dense frame: a centered heading over a 3-up row of ink-bordered stat cells (green/pink/orange), no per-cell shadow.
- **Closing Plate** — the single green-ground frame of the whole piece; a centered cream sign-off, one pink stamp rotated -6° in a corner.
- **Featured Marker** — cream ground; the pink marker-block carrying the signature orange+ink hard offset shadow, positioned asymmetrically — the one hard shadow on the frame.
- **Comparison Ledger** — the second dense frame: a cream-2 ledger table with an ink header row, one column fill marking the "winner."

**Do:** compose around one idea per frame with the focal element 3-5× its neighbors; lean centered on cover/claim/stat-grid/closer, reserve left/asymmetric for the marker and ledger; keep sparse frames 45-60% empty; use two or three accents per frame (never all four); reserve green ground for the single closing plate; spend the hard shadow on exactly one block per frame.
**Don't:** don't round corners except the one pill chip; don't gradient, blur, or glow anything; don't set Archivo Black in sentence case; don't use all four accents on one frame or introduce a fifth; don't center body copy; don't put two hard shadows on one frame.

**Known gaps:** motion out of scope. Fonts: Archivo Black, Space Grotesk, JetBrains Mono.

---

### Daisy Days
**Look:** A cheerful picture-book system — 3px charcoal outlines on every shape, hard offset shadows (6/4px, zero blur), a nine-color sunny-garden pastel palette (cream + turquoise/soft-pink/butter/mint/lavender/peach/sky plus a coral high-attention accent), Fredoka One + Quicksand pairing, generous corner radii, a hand-drawn SVG ornament layer.
**Pick when:** playful, childlike, sticker-sheet kawaii — a product that wants warmth and whimsy.

**Colors:** cream `#F5F0E6`, turquoise `#7ECDC0`, soft-pink `#F7C8D4`, butter `#FDE68A`, mint `#A8E6CF`, lavender `#D4A5E8`, peach `#FFCBA4`, sky `#A8D8F0`, coral `#F8635F`, text-dark `#2D2D2D`, text-muted `#6B6B6B`, white `#FFFFFF`.

**Typography:** reading ramp in Quicksand (body ~0.95% width/500, an emphasis variant at 600). Display ramp entirely in Fredoka One, single weight, never italic — from a small label-display (~1.3% width) up to a full display (~6.5% width). Legibility floor ≥1.4% width. Fredoka is for all display, Quicksand for all body — the two never cross roles.

**Depth:** 2D graphic depth only — a hard offset shadow (solid charcoal, zero blur, bottom-right) at 6px for cards/frames/badges and 4px for small cards/step circles/avatars; a matching 3px charcoal text-shadow is applied to Fredoka headlines set on saturated (colored) surfaces so they read as "outlined" like the shapes (headlines on plain cream sit flat, no text-shadow). The outline + offset shadow together are the "sticker-on-paper" signature. No blurred shadow, no translucent color, no gradient, no glow.

**Shapes:** 20px radius on standard cards, 28px on featured cards, 50px pill radius on badges/counters, 50% on all circles — zero square corners exist anywhere in this system.

**Named components:** card / framed-header (white-fill bordered containers, one shadow each), badge-pill (a butter-colored section tag), circle-marker family (an outlined pastel disc used at several fixed sizes for bullets, icons, dots, and numbered steps), bullet-dot (an outlined butter disc — lists never use plain glyph bullets), ornament (the hand-drawn SVG sticker layer — daisy, star, sun, cloud, rainbow — 3-7 per frame, clustered at corners/edges, deliberately cropping past the frame edge), quote-mark (an oversized soft-pink Fredoka quote glyph), text-headline-shadow (the on-saturated-color headline treatment described above).

**Frame treatments:**
- **Cover** — a saturated pastel ground; a 1-2 line display headline in white with the charcoal text-shadow, centered, under a butter badge-pill; 3-7 ornaments cluster at corners.
- **Info Cards** — the dense frame: cream ground; three white bordered+shadowed cards (circular icon + title + body), fewer ornaments here.
- **Process Steps** — a pastel ground; a row of large outlined step circles with rotating fills (coral → mint → sky → lavender) and Fredoka numerals, linked by arrow glyphs.
- **Quote** — a soft-pink ground; a white quote card holding a charcoal Fredoka quote under an oversized soft-pink quote mark.
- **Framed Section** — cream ground; a pastel "cap" strip above a white body panel, with a butter-dot bullet list.
- **Closing** — a saturated pastel ground; a white display sign-off with the charcoal text-shadow, centered, ornament wreath at corners.

**Do:** pair Fredoka One headlines with Quicksand body strictly by role; outline every shape 3px charcoal plus a hard offset shadow; give headlines on saturated surfaces the charcoal text-shadow in white text (flat charcoal on plain cream); use outlined butter-disc bullets, never glyphs; cluster 3-7 hand-drawn ornaments per frame, cropping past edges; keep one content container per frame.
**Don't:** no square corners; no blurred or translucent shadows; no colored borders (charcoal only); no coral surface fill (coral is a small-marker accent only); no third font; no glyph bullets; no empty corners (ornaments should fill them).

**Known gaps:** motion out of scope. Fonts: Fredoka (the variable family serving as the modern equivalent of the original "Fredoka One" cut — request weight 600 for visual parity) + Quicksand.

---

### Editorial Forest
**Look:** A serif-led literary-editorial system — a green/pink/cream editorial triad, Source Serif 4 at weight 500 (using its optical-size axis) for all display, JetBrains Mono weight 500 uppercase for chrome, flat paper depth (no shadows), 2px hairline rules, 6/8px card radii, a circular monogram stamp as the identity mark.
**Pick when:** spacious, restrained, editorial — a product that wants quiet confidence and literary tone.

**Colors:** green `#2e4a2a`, green-deep `#243a21`, green-lite `#3a5a36`, pink `#e89cb1`, pink-deep `#d27e96`, cream `#efe7d4`, cream-2 `#e6dcc4`, ink `#1a1a17`.

**Typography:** reading/chrome ramp in Source Serif 4 at weight 400 for body (~1.56% width) plus JetBrains Mono weight 500 uppercase labels in px, tracked 0.14-0.18em. Display ramp in Source Serif 4 weight 500 (never 400 for display, never 700), using the optical-size axis, negative-tracked — from a small title-card (~2.9% width) up to a display-hero/stat-figure (~11.5% width). Legibility floor ≥1.4% width. The signature rhythm is the 500-for-display / 400-for-body step — never invert it. A 600-weight is reserved for attribution names only.

**Depth:** flat, paper-based — elevation comes from color-block contrast (a colored tile on cream reads elevated by the hard color separation alone), 2px hairline rules in the region's accent color, and the distinction between a solid-fill tile vs. a bordered tile with a tinted fill. Zero shadow anywhere — adding a box-shadow would break the paper feel; zero gradient, zero glow.

**Shapes:** 6px radius on topic tiles, 8px on step tiles, 2px on a legend swatch, a rounded-top-only shape on chart bars, 50% on the monogram circle (the only full round in the system). No square corners, no heavy rounding.

**Named components:** topbar (a mono label + a monogram circle or counter — present on EVERY frame, the system's spine; a frame without it reads unfinished), footline (two mono captions space-apart along the bottom edge, on cover/data/summary frames), monogram-circle (the identity stamp, cover/summary only), topic-tile (a catalog tile whose fill rotates through the palette — never repeat one fill twice across a single grid), step-tile (a framework/process card with a heavier 2.5px border), kpi-block (an oversized serif figure with a mono tag above and body copy below, a 2px accent rule above it), meta-dl (a 3-column definition-list style data grid with a 2px top rule), bar (a vertical chart bar with a mono value label above it), rule-thin (the only separator in the system — always 2px, never 1px or 3px+).

**Frame treatments:**
- **Cover** — green ground; a 2-line serif display-hero headline in pink (one word in cream), left-anchored, under the mono topbar; monogram circle top-right.
- **Topic Tiles** — the dense frame: cream ground; a row of 3-4 tiles with rotating fills (green/pink/cream-2-with-border), each a mono ordinal plus a serif title.
- **KPI Stat** — green ground; an oversized serif figure (with a unit) in pink over a pink accent rule.
- **Statement** — cream ground; a 2-line serif display quote in green, with a 600-weight attribution name and a mono role beneath.
- **Step Framework** — cream (or green) ground; a row of 3-4 heavier-bordered step tiles (mono ordinal + serif title + body + mono marker over a top rule), fills rotating.
- **Chart** — green ground; pink/cream/green bars over 2px axis rules with mono tick labels, an optional 3-column data grid beneath.

**Do:** run every display element in Source Serif 4 weight 500 (opsz, negative-tracked, tight line-height), body at 400; set every label/caption/axis in JetBrains Mono 500 uppercase; give every frame a topbar; pick one dominant surface tone per frame (max two); rotate tile fills, never repeating one across a single grid.
**Don't:** no box-shadow, gradient, or glow anywhere — flat, paper-based depth only; no third typeface; no italic or underline; no serif body set at weight 500; no fourth color family; no rules thinner than 2px or thicker than 2.5px; don't omit the topbar.

**Known gaps:** motion out of scope. Fonts: Source Serif 4 (the optical-size axis is important — a non-opsz fallback flattens the size-aware letterforms), JetBrains Mono.

---

## Templates & examples

**The design-picker workflow (two-phase visual selection).** For a higher-touch design process than picking a single frame preset or writing a spec from scratch, generate a two-phase interactive picker:

*Phase 1 — mood boards.* Generate as many distinct mood-board directions as the creative space genuinely warrants (typically 4-8). Every board must tell a genuinely different STORY about the brand — not just reshuffle the same layout with different colors. Ask: "what are the genuinely different ways to position this product?" For example, a cat food brand might have distinct directions like playful chaos, premium positioning, comfort/cozy, social-native, flavor showcase, humor-led, and sensory/appetizing — each a different narrative, not a different font on the same layout. Each mood board pre-selects one option from every other category (one architecture, one palette, one type pairing, one corner style, one density level, one shadow depth, one easing feel), so picking a board in Phase 1 pre-fills all of Phase 2.

*Phase 2 — fine-tuning.* Within the chosen direction, offer independent variation across: layout architectures (one per mood board minimum, each visually distinct, built from real headline/subhead/body/stat/quote/card/button/tag content so the preview reads as a real composition, not lorem ipsum); palettes (5-6 options, named after the brand's own world rather than generic mood words, always mixing dark + light + tinted backgrounds — every palette must be visually distinguishable from the others even at a small swatch size); and type pairings (5-6 options, generated using the font-discovery method described under Typography above rather than reaching for the same familiar handful of fonts every time, matched to the brand's energy and audience, crossing category boundaries per the pairing rules above).

Every layout-architecture preview should be genuinely dense (15+ distinct elements — headline, subhead, body paragraph, label/overline, primary stat, secondary stat, a quote with attribution, two differently-treated cards, a code/command-style block, a primary button, a secondary button, a tag list, an accent divider, and one data element like a table row or progress bar) so a person picking between options can actually see how a full layout would feel, not just a color swatch. Keep every preview built from percentage widths (not fixed pixel widths) so it doesn't overflow its preview panel, and keep any injected preview markup free of scripts or event handlers since it's typically rendered by directly inserting HTML into a live page.

Once someone has made a selection, the output is a portable design-spec document: structured frontmatter tokens (colors, typography, corner style, spacing) followed by prose sections (Overview, Colors, Typography, Layout, Elevation, Components, Do's and Don'ts) — the same shape referenced throughout this document as "the design spec." Save that output as the project's design spec and use it as the normative source for every subsequent design decision.

**Supporting utility scripts referenced by this system** (for context — these are part of the underlying rendering/tooling pipeline, not standalone deliverables):
- A contrast-checking script that inspects rendered frames and reports color-contrast (WCAG-style) warnings — useful for validating the "Contrast enforced" rule under House Style.
- An audio-band extraction script that pre-processes an audio file into the per-frame frequency-band data format described under Audio-Reactive Animation, so audio-reactive compositions have deterministic, pre-computed data to animate against rather than doing live audio analysis.
- A package-loader helper (plus its test suite) that resolves supporting tooling packages for the rendering pipeline — internal plumbing, not something to author against directly.

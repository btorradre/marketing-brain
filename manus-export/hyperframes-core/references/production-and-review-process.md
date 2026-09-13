# The review process and the production loop

This covers how a video earns fidelity one approval pass at a time, the stage dependencies between an approved plan and a delivered video, how to build many scenes independently, and the constraints a single frame/scene composition must satisfy regardless of who or what builds it.

## The review process: plan, sketch, build, final look

This describes how a video earns fidelity one approval pass at a time, when a live review surface (a shared board, a document, or simply presenting drafts to the requester) is part of the workflow. A fully autonomous run posts the same checkpoint summaries and continues without waiting, keeping exactly one question before the final render.

### Pass 1 — The plan

Before presenting the plan, make sure whatever review surface is being used (a live board, a shared doc) is actually up and reachable. Present the plan as a proposal: open by stating **"This video tells [audience] that [message],"** then a frame-by-frame table — one row per frame: frame number, beat type and duration, what's on screen, and *why* (how it serves the message). Note that feedback can land in either the review surface's own comment mechanism or directly in conversation — one revision loop either way — and that a submission on the review surface still needs some kind of direct follow-up ping to guarantee it gets picked up and processed.

In the same message, ask two things: (a) approve the plan or request changes, and (b) do a quick wireframe/sketch pass first (recommended — a fast layout check right after this approval) or skip straight to a full build. Iterate until approved, revising exactly the frames named in feedback each round.

This is a checkpoint — a fully autonomous run (see the mode table in `brief-format.md`) normally skips the live-board loop entirely; if a run switches to autonomous mid-flight after a board already exists, keep updating the board and post the same summary as a heads-up without waiting for a reply, and let the one still-kept question happen at the final-look pass instead.

### Pass 2 — The sketch pass (skippable)

As soon as the plan is approved, build a quick wireframe version of every frame — the frame's layout at its key moment, real headline/stat/label text placed where it will actually live, plain blocks standing in for panels/charts/diagrams/media (define upfront what each block type stands for), the base background/ink colors plus one accent, and nothing else. No decoration, no full visual treatment, no motion — those arrive with the real build.

Each sketch should still be a real, technically valid composition file (so any preview tooling can render a poster image from it) — a template wrapper, correct composition id, root styled via `#root`, one paused *empty* timeline correctly registered. This pass needs no validation tooling run against it — a sketch is only a few dozen lines of HTML, and the whole set of sketches for a video can land in minutes.

Mark each frame as reaching the middle status (`built`) as its sketch lands, so a live board fills in visually on its own. Once every frame is at that status, pause and ask one thing: does the board look right, or which frames need to change? Revise only the sketches actually named in feedback, re-present, and loop until the layout is confirmed. Only then does the real visual design and motion get applied on top of the confirmed layouts.

A confirmed board of sketches is itself a valid stopping point — if what was actually requested was a storyboard to pitch, review, or hand off rather than a finished video, the sketched board *is* the deliverable; confirm it, hand over the board, and go no further unless asked to continue to a full build.

In a fully autonomous run, or when the requester chose to skip sketches at Pass 1, skip this pass entirely — frames go straight from outline to fully built.

### Pass 3 — Building on confirmed layouts

However the build actually happens — one person or process per frame working in parallel, or one build pass working through scenes in order — a confirmed sketch's composition is settled: placement, hierarchy, and copy were already approved on the board. Building from a confirmed sketch means dressing that exact layout (full visual treatment, real assets, motion) — never redrawing it from scratch. Whoever builds a frame that has a confirmed sketch should be told explicitly that the sketch exists and represents an approved layout; the landed frame must still read as the approved wireframe, just fully dressed.

Mark each frame as fully built (`animated`) as it lands. In collaborative mode, this build stage is gated on the sketch board having been confirmed in Pass 2.

### Pass 4 — The final look

After all checks pass, use whatever final composition preview is available. In collaborative mode, ask one thing: render now, or what changes? In a fully autonomous run, this is the one question the mode still keeps: "preview first, or render?" Open the preview on a "preview" answer; render only on an explicit render approval. Never render before this approval.

**After approval, offer to save the whole setup as a reusable template — once.** An approved run is a proven bundle: design spec, storyboard skeleton (structure kept, content blanked), and the confirmed brief values can all be frozen together so a future similar request can start from it instead of from scratch, skipping straight past the questions already answered this time. If this is offered and accepted, confirm the saved name and make clear that name is something the requester can casually reference later ("make another one like X," or "same as last time") without needing to remember any technical details. In a fully autonomous run, don't ask — just name the save option in the delivery note instead.

## The production loop: from an approved plan to a delivered video

The stages between an approved plan and a video in the requester's hands, described as **dependencies rather than a strict numbered sequence** — order between independent stages is free (audio can render in the background while frames are being built; overlapping wait time with work is the standard trick), but order *inside* a dependency chain is not. A stage whose need is absent simply doesn't run — no narration means no audio stage; a single scene means no transitions. An edit request re-enters at whichever stage/artifact it actually touches and re-runs verification from there.

| Stage | Needs | Produces |
|---|---|---|
| **Blocks & assets** | the approved plan | any reusable component blocks the plan calls for, installed once before any parallel work starts (installing them concurrently from multiple workers risks a race); requester-supplied assets staged; logos/images/color grades resolved |
| **Audio** | narration text (when narrated); the storyboard's mood/music direction | voice files + word-level timings + background music + sound effects, generated in the background while other stages proceed |
| **Frames** | the design spec + the plan (+ a confirmed sketch when one exists — dress that layout, never redraw it) | each scene as its own composition file, marked as fully built in the storyboard as it lands |
| **Duration sync** | word timings + frames | scene durations trued up to the real generated-voice length — the real duration always wins, a silent scene keeps its estimate, and a synced value is never hand-edited afterward |
| **Assembly** | the built frames | the index composition — scenes wired in as sub-compositions on tracks |
| **Transitions** | the assembled index | scene-to-scene handoffs injected |
| **Captions** | word timings + the assembled index | the caption track (if no script exists to time against, transcribe the generated audio first) |
| **Verify** | the assembled index (+ captions/transitions when present) | all structural/lint/layout checks passing, plus a quick eyeball of a contact sheet at each scene's midpoint |
| **Deliver** | verification passing | a final-look pause, then on approval a full render, then optionally publishing to a stable public link, then the offer to save the setup as a reusable template |

The Frames stage should follow whatever motion/shape citations the plan already made — a scene planned against a named shot template or named motion techniques (owned by the animation runtime library) gets built by actually reading that reference material before its motion is written; names should come from wherever that reference material is indexed, never invented on the spot, and a scene the plan left uncited should get its citation decided at build time rather than improvising untracked motion.

**Two scheduling facts worth knowing:** external generation calls (image plates, text-to-speech, background music, video generation) are independent work — fire every generation whose input is already known concurrently or in the background, and overlap the wait with reading or building something else; three assets generated one after another cost roughly three times the wall-clock time of firing them together. Also, inspecting a generated image or video mid-session (especially at full detail) can be an expensive operation in some environments — batch visual checks into one contact sheet rather than many single-frame looks, and schedule them at natural phase boundaries rather than constantly mid-build.

Two points in this loop carry the requester's actual voice: the plan that starts it was approved in Pass 1 (or posted as a heads-up in autonomous mode), and nothing renders before the Pass 4 final-look approval. Everything between those two points is free to schedule however is most efficient.

## Building scenes independently (parallel work)

When a video has many scenes that can be built independently, the underlying goal is: hand each scene's *entire* self-contained spec to an independent builder (a person, or a separate process working on that one scene), let them build purely from that spec without needing to see the rest of the project, then verify each output file actually exists and is correct before merging it into the final assembly. The mechanics of *how* work gets distributed to independent builders differ across tools and platforms — the important, tool-independent rules are:

- **Completion is judged by the artifact existing on disk**, not by any notification that a worker "finished" — some systems report completion unreliably. After a wait, verify the actual output file exists and is valid; a missing file means that unit of work failed and should be retried once with the same instructions plus the failure reason attached.
- **A concurrency limit reduces parallelism, not the amount of work** — every scene still gets built; if only a few workers can run at once, batch the work into waves of that size rather than dropping scenes or merging multiple scenes into one worker's task.
- **Each independent builder needs a fully self-contained packet**, not access to the whole project — see "The frame/scene builder role" below for what that packet should contain and how one scene should be built from it.

## The frame/scene builder role

When one scene/frame of a larger video is being built as an independent, self-contained unit of work (whether by a different person, a different process, or simply as a discrete step in a single build), follow this process. It assumes the builder has been handed: a `frame_id` (used verbatim as the composition id, the timeline registry key, and the output filename, e.g. `compositions/frames/03-feature.html`); the design-truth file (palette, type ramp, components — the visual "look" to pull every visual token from); and a self-contained packet of everything needed for this one frame, which should include:

- `scene` — a one-line caption describing the design intent (not visible on-screen text).
- `voiceover` — the narration line for this frame, used only as a **timing reference** (to sync entrances to the voice) — it is never rendered as visible text; captions are a separate track handled elsewhere.
- `duration` — the frame's fixed render length in seconds. Never change it or stretch/compress content to fill a different length.
- `transition_in` — informational only; whoever assembles the final video stamps the actual transition. A frame builder never authors the transition itself.
- A **time-coded shot sequence** — the actual build spec: a sequence of "Scene" lines (e.g. `Scene 1 (0.0–Xs): … → Scene 2: … → Scene N`), each describing what's on screen, what enters/moves/reveals, and the layout — inline. Build this faithfully, beat for beat; every window described is a phase that must be realized, with each reveal timed to land on its narration cue.
- A named shot template/blueprint (or an explicit "compose from scratch" marker) describing the overall shape and signature move of this shot.
- Which element is the visual focal point and what role each other element plays.
- The mechanics (a "recipe") for any named motion technique cited in the shot sequence — reproduce these mechanics rather than guessing at a technique from its name alone; guessing loses the technique's actual signature move.
- The canvas size and whether captions are enabled (and if so, the safe-area cutoff for caption clearance).

**If a confirmed sketch/wireframe for this frame already exists**, read it first and preserve its composition exactly — placement, hierarchy, and copy were already approved; don't move or drop anything from it. What's still yours to add: the full visual treatment, real finished content wherever the sketch used placeholder blocks, and the actual motion — mapping each described scene onto a timeline phase, revealing each piece on its narration cue with proper entrance tweens. The final landed frame must still read as the approved wireframe, just fully dressed.

### What a frame builder does NOT decide

These belong elsewhere in the process, and touching them breaks the contract with the rest of the project:

- **What is said** — narration text is locked elsewhere (in the script file or the frame's `voiceover` line). A frame builder only shows; it never writes or restates narration as on-screen text.
- **Duration** — fixed from real generated-voice timing elsewhere. Build the shot to land within the given duration; don't stretch or trim it.
- **Transitions between frames** — stamped onto the root timeline by whoever assembles the final video. A frame builder authors the shot itself but never an "exit" tween — the transition between scenes *is* the exit, except for the final frame in the whole video, which can genuinely settle/fade out.
- **Audio** (narration, background music, sound effects) — assembled separately at the project root. No `<audio>` element belongs inside an individual frame's composition file.
- **Design tokens** — palette, fonts, and components come only from the shared design-truth file; a frame builder should never invent them, and never lift a word or label out of the design-truth file as visible copy — that file is a style spec, not content. Visible text comes only from this frame's own scene description/narrative.
- **Which motions or assets exist** — named upstream in the packet. A frame builder implements what's named; it never fetches new assets or invents new motion techniques on its own.
- **The shared storyboard file itself** — a frame builder should only ever read its own packet, never open or write the shared storyboard directly; whoever is coordinating the whole project owns that file's state.

### Constraints every frame must satisfy

In addition to any workflow-specific rules:

- **Caption keep-out — all content in the top ~83% of the frame.** If a caption pill sits at the bottom of the canvas, it owns roughly the bottom 17%. Keep every element (headline, cards, code panel, diagram, stats, brand mark) above roughly 83% of the frame height. This holds even when captions are disabled for this particular render, for consistency across frames.
- **Fill the content area, especially in a portrait/vertical frame.** Compose across the whole usable region rather than floating one small cluster in the middle. Anchor the hero element high (roughly 20–35% down from the top), flow supporting elements downward with rhythm, and scale the hero toward full-bleed. A landscape frame's usable region is shorter, so simple vertical centering near the middle is fine there.
- **Visible text is short motion-graphics copy** — a hero word, a stat, a one-word emphasis (`"$83K"`, `"2× faster"`, `"INSTANT"`) — never a full sentence lifted from the narration. If a caption track already shows the spoken words synced to voice, repeating them as on-screen text double-prints the same words.
- **Build the whole shot — reveal across the full duration, never front-load everything near the start.** Dumping the whole canvas in the first quarter of the shot and then holding it reads as a static slide, not a video. Instead, reveal each piece (a line, a card, a node, a stat) as the narration reaches it, pacing the reveals across the entire duration — especially the back half — with any camera-style move running underneath throughout. Only *exits* are banned on a non-final frame (an exit tween gets truncated by the cut to the next scene and reads as a glitch); mid-shot reveals are always fine. The one exception is a frame deliberately marked as a still/hold moment — there, an entrance followed by a quiet settle is correct; a held read beats forced motion.
- **Implement the shot sequence faithfully — every described "Scene" beat is a real timeline phase.** The time-coded shot sequence *is* the build spec: map each described beat onto a phase of the one timeline, each piece revealing as narration reaches it. For any named motion technique, reproduce the actual mechanics of its recipe rather than guessing from the name. A named shot template gives the overall shape — keep its signature move recognizable while instantiating it with this frame's actual content. If no template is named ("compose from scratch"), sequence the shot directly from the described beats. Never front-load the whole sequence at the very start regardless.

### Process

1. **Read** the full packet (the frame's own spec, any inlined shot-template description, any inlined motion-technique recipes), then the design-truth file for the visual look. The most consequential thing to get right structurally is the file-transport rule: every `<style>` and `<script>` block (including any animation-library load) must live *inside* the `<template>` wrapper, since a runtime that only clones template contents will silently produce a blank, unstyled sub-composition otherwise — and a project-wide check run after assembly can miss that a specific sub-composition never got wired in.
2. **Design** — turn the time-coded shot sequence into an actual timeline using the design-truth file's components and type scale: each described beat becomes a phase revealed on its narration cue, each named motion built from its recipe, the chosen template's signature move kept recognizable. Look for a visual idea that reinforces the beat rather than a literal restyling of the words.
3. **Author** the full sub-composition file: a `<template>`-wrapped root carrying the correct composition id, styled via `#root` (never a class on that same element), with exactly one paused timeline registered under the frame's id, built synchronously. Prefix any ids and reusable class names with the frame's own id so that when many frames are assembled together nothing collides (standard selectors like `#root` and `.clip` are the exceptions).
4. **Self-check** against the checklist below and fix anything found before considering the frame finished.

### Self-check checklist

A frame builder generally cannot run full project-wide validation tooling on a single not-yet-assembled frame — those checks operate on the assembled project and would only report on other files. So the self-check has to happen by careful re-reading before finishing; if a retry happens later with specific findings attached, treat each one as a hard constraint:

- The entire file is exactly one bare `<template>…</template>` fragment — no `<!doctype>`, `<html>`, `<head>`, or `<body>` outside it — and the root inside carries the correct composition id.
- Every `<style>` and `<script>` block, including any animation-library load, lives inside `<template>`.
- The frame's root is styled via `#root`, never via a class also present on that same element — at render time a class on the root gets scoped to a descendant selector that can't actually match it, so the whole scene renders unstyled even though an isolated preview might still look correct.
- A frame's full-bleed background (a color field, gradient, or grid) is authored as its own full-duration `class="clip"` element on the lowest content track — never as a `background` set directly on the root/composition-id element itself. At final assembly the frame root is only visible during its own time window, so a background painted on it isn't a dependable full-frame ground; dark content can end up rendering over a black host background and become invisible.
- Every `class="clip"` element has `data-start`, `data-duration`, and `data-track-index`.
- Exactly one paused timeline, registered under the frame's own id.
- No CSS `transition`, no `repeat`/`yoyo`, and no other non-deterministic animation logic anywhere (the renderer seeks frame-by-frame, not through real playback).
- No CSS `transform` (e.g. a `translateY(-50%)` centering trick) sits on any element that also has a GSAP transform property (`x`/`y`/`scale`/`rotation`) tweened on it — GSAP overwrites the whole `transform` and silently drops the CSS centering, so the element visibly jumps. Center with `margin`/`inset` (or offset `top`/`left`) instead, fold any needed offset into the tween itself via percentage-based transform properties, or use a `fromTo` tween (which is exempt from this issue).
- The main subject is visible by roughly half a second in, using proper entrance tweens (declaring both start and end state) rather than a CSS-hidden starting state.
- No exit tween on a non-final frame.
- The shot's pieces reveal on their narration cues across the full duration rather than all firing at time zero; a non-still frame keeps content arriving rather than holding a fully-populated canvas from early on.
- Every described beat in the shot sequence is actually realized as a phase, any named shot template's signature move is present and recognizable, and the whole shot paces to the narration rather than front-loading.
- Every font actually named in the CSS has a matching font-face declaration inside this same file, pointing at a real font file that ships with the project. Only ever use fonts that actually have a shipped file — never name a system font (especially for non-Latin scripts like Japanese, Chinese, or Devanagari) that the render environment doesn't actually have installed; the render machine is typically a clean, minimal browser environment, so an unavailable font silently falls back to something generic and the typography is simply wrong in the final video. For non-Latin visible text, either use a shipped font that covers the needed script, or transliterate/romanize the text; if neither is possible, that content is out of scope for this frame — never invent a font name that doesn't exist as a real file.
- Nothing sits below the caption safe-area cutoff, and no full narration sentence is rendered as visible on-screen text (a quick visual eyeball, not something to derive from code).

## Validation

Whatever CLI or tooling a HyperFrames project ships with should be run before considering any composition finished:

- A full lint/structural/runtime/layout/contrast check should pass with zero findings.
- For any project using sub-compositions, take a snapshot at several representative timestamps (e.g. each scene's midpoint) and actually look at each frame.
- Use a live preview for human review — anything in the timeline should still be editable there before final approval.
- Only render after explicit approval from whoever commissioned the video.

## Note on the frame-packet builder helper script

`scripts/lib/frame-packets-core.mjs` (in this skill folder) is a portable Node.js helper for building the "frame packet" data structures described above — it parses a storyboard's markdown into individual frame blocks, extracts fields like `src` from each block, and assembles the self-contained packet (with inlined shot-template and motion-recipe content) that gets handed to whoever builds each individual frame. It has no external dependencies beyond Node's built-in `fs`/`path`/`url` modules and takes its paths as parameters, so it can be adapted into any automation that needs to split a `STORYBOARD.md` into per-frame build packets.

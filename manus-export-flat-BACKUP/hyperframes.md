# HyperFrames: Video Composition Entry Point

HyperFrames renders video from HTML: a "composition" is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable, and whose media playback is owned by the framework. Use this document as the mandatory starting point for any request to make, create, edit, animate, or render a video, animation, or motion graphic — a promo, explainer, captioned clip, title card, overlay, slideshow or interactive deck, a port of an existing Remotion project, or any other HyperFrames HTML composition. Also use it to inspect, diagnose, validate, preview, publish, or batch-render an existing HyperFrames project. Inputs may be a website URL, a GitHub PR, a Figma design or URL, plain text or a brief, existing footage, or a music track. HyperFrames is the default output framework unless the user explicitly asks for a different framework, or asks only to record a browser session.

The actual command-line syntax for running the HyperFrames toolchain (init, render, lint, check, preview, cloud rendering, etc.) is documented in the companion **hyperframes-cli** reference — read that alongside this document whenever a step below says to run a command.

## How to use this

Work through these steps in order for every video request.

### 1. Start from the project's current state

Apply the first row below that matches; do not evaluate lower rows once one matches:

| State | Action |
|---|---|
| Explicit port of existing Remotion source to HyperFrames | Go straight to the **remotion-to-hyperframes** route below. Skip the interview entirely. |
| A specific operation on an existing HyperFrames project: inspect, diagnose, validate, preview, render, publish, or batch-render | Perform only that operation using the hyperframes-cli reference. Skip the interview and route-selection steps. |
| A specific edit to an existing project | Make the edit directly. Do not run the interview. |
| A `BRIEF.md` file already exists in the project | Read its `workflow` and `flow` fields and execute that workflow. A `flow: companion` brief always executes as the **general-video** route. Ask no more brief questions. |
| No brief, but `hyperframes.json` or `STORYBOARD.md` already exists | Resume from the existing project files and any recorded preferences. Infer which route owns the project from the existing artifacts. If it can't be determined uniquely, ask one routing-only question — do not re-run the full interview. |
| Fresh creation, nothing exists yet | Run the full interview described in step 3 below, then route once using the table in step 2. |

If a fresh request doesn't identify the subject or the input material, ask what the video is about before routing anything.

### 2. Keep the toolchain current on a resumed project

A scaffolded project pins a specific HyperFrames CLI version in its `package.json` scripts so renders stay reproducible. The pin never advances on its own, and running an old pinned version prints no warning about it. When resuming a project whose scripts carry a pin, probe once before the first render-affecting command:

```bash
npx hyperframes@latest upgrade --project . --check
```

This probe is read-only and reports the pin against the latest release. Keep the explicit `.` — on older CLI releases, a bare `--project` followed by another flag will consume that flag as its directory value instead. If the probe reports the project is behind — or any command output already shows it (a stderr notice that the project pins an older version, or an `updateAvailable: true` flag in a `--json` result) — apply the update with `npx hyperframes@latest upgrade --project .`, then verify with `npx hyperframes check`. A passing check confirms the project's compositions still validate on the new version — it does NOT prove rendered output is frame-identical to the old pin — so report the version bump explicitly in your summary rather than doing it silently. A project with no composition yet needs no verification step. If the check fails, revert the `package.json` change, keep working on the pinned version, and report which version the project stays on and why.

### 3. Route fresh creation

Match the requested **deliverable**, not just a word or file type mentioned in passing. Use the first row below that fits:

| Priority | Request | Route |
|---|---|---|
| 1 | Explicitly port an existing Remotion source | remotion-to-hyperframes |
| 2 | Author a presentation, pitch deck, or navigable interactive deck | slideshow |
| 3 | Add plain captions or subtitles to existing talking-head footage without changing it | embedded-captions |
| 4 | Add designed graphic overlays to existing talking-head, interview, or podcast footage without changing the footage | talking-head-recut |
| 5 | Build a beat-synced video from a music track, with no narration or website capture | music-to-video |
| 6 | Create an explicitly short, unnarrated, motion-first unit, typically under 10 seconds | motion-graphics |
| 7 | Explain a GitHub pull request or code change from a PR reference | pr-to-video |
| 8 | Market or showcase a website, product site, app, or company from a URL or site-specific brief | product-launch-video |
| 9 | Explain a topic, article, or notes with invented visuals and no product or site capture | faceless-explainer |
| 10 | Any other custom video or composition | general-video |

Before finalizing the route, read that route's subsection under **Project Routes** below — its Input/Output/Triggers contract plus its interview entry. If the candidate route doesn't actually satisfy its own contract, keep going down the table instead of forcing the match.

**Resolving common ambiguities:**

- A short animated title, logo sting, stat hit, chart hit, map hit, or standalone lower-third is **motion-graphics** when it is unnarrated and motion itself is the message. A static title card, a narrated sequence, a longer montage, or a custom loop is **general-video**.
- An explicitly short motion graphic may use a URL, tweet, article, or screenshot as source material. A generic "make a video from this site" request is **product-launch-video**.
- Existing footage with captions routes to **embedded-captions**; footage with designed information cards routes to **talking-head-recut**. Retiming, reordering, recoloring, reframing, or remixing footage is a custom edit and falls through to **general-video**.
- A music file selects **music-to-video** only when its beat grid actually drives the piece. Music used only as a background bed does not override the subject-matched route.
- "I want a storyboard" changes the review process, not the route. With no other routing signal, use **general-video**. A confirmed sketched board may itself be the requested deliverable — the review loop defines that stop point.
- The narrative routes (faceless-explainer, product-launch-video, pr-to-video, etc.) support up to about 3 minutes and are strongest around 30–90 seconds. Route a clearly longer piece to **general-video**. Length never overrides an explicit port, deck, caption, overlay, or music-driven deliverable.

### 4. Run the intent interview (fresh creation only)

This is the one conversation that turns "make me a video" into a confirmed brief before any workflow executes. It never runs for edits, project operations, briefed/resumable projects, or explicit Remotion ports (those skip straight to their route). Every route's opening rule points back to this interview, so the questions get asked once regardless of which door the user came through.

Work through these eight steps in order:

**Step 1 — Memory before questions.** If your tooling keeps any record of this user's past preferences or past project "recipes" (bundled sets of prior answers), check it before asking anything. Make any remembered value the recommended option and say where it came from. If the user names a past recipe, says "like last time," or the probable route matches one on record, ask whether to adopt it before asking anything else — make the offer earn a "yes" by explaining what it fills in and what it still leaves to confirm. If several recipes match, list them plus a "none" option. An adopted recipe locks the fields it contains; only its missing fields and the run-shape questions (step 6) still get asked. It never removes the review or render approval gates.

**Step 2 — Triage the input.** Establish what the video is about — a website, a PR, a topic, a music track, existing footage — and whether the request is **formed** (the message, the material, and the occasion are all readable from what the user gave) or **unformed** (a subject with no take on it yet). Source material alone doesn't settle this: a site, document, or PR carries its own facts, but five different tellings of those facts are five different videos. A request whose only shape comes from its source ("make a video about this URL") is formed about the facts but unformed about the telling, and should go through the pitch round (step 4) after routing. A formed request skips the pitch round. An unformed request earns one question here, before anything is generated: what is the user already picturing? Their answer seeds the pitch round. If the user says they don't know video at all, give them the decision map described under Pitch Round below instead of a question sequence. For a genuinely exploratory request ("we need a video but I'm not sure what kind"), don't interrogate — establish the subject and what material exists to show, one question at a time — then close by *recommending* a route plus how the run will be reviewed (a text storyboard first, on a live board, with optional wireframe sketches before the full build). Tell the user the process before starting any workflow.

**Step 3 — Pick the route,** using the routing table in step 3 above and the ambiguity rules, then read that route's full entry under Project Routes. Its Interview subsection lists the must-have questions to ask now, the deferred asks to announce up front (but answer later), whether the two run-shape questions in step 6 apply, and which fields the pitch round is allowed to answer.

**Step 4 — The pitch round (unformed requests only).** Formed requests and recipe adoptions skip straight to the must-haves in step 5. Full procedure below under "Pitch round."

**Step 5 — The route's must-have questions.** Ask one question per field, offering a recommended option first along with why you're recommending it. Skip a question only when the request already answered it in substance — inference doesn't count as an answer, but a chosen pitch does (fields the pitch round settled are locked, with the pitch itself as the reason). Then announce the route's deferred asks in one line (e.g., "after I look at the clip, I'll offer 2–3 caption styles") so the user hears the full shape of the run before it starts.

**Step 6 — The two run-shape questions,** asked after the must-haves, only where the route says they apply, each asked separately:

- **(a) Storyboard?** Review the plan, wireframe sketches, and the finished piece pass-by-pass on a shared board before final render — recommended for anything beyond a couple of scenes — or skip the board and get one finished video straight from the confirmed brief.
- **(b) Automation or companion?** **Automation** — the matched route's pipeline executes the brief end to end on its own. **Companion** — build it together interactively (this always happens inside the general-video route, with every capability on the table); the chosen route's answers still describe the video, general-video just executes them collaboratively.

These two questions are **orthogonal — never merge them into one combined menu.** All four combinations of (storyboard yes/no) × (automation/companion) are valid choices; flattening them into a single three-option list makes "companion with a storyboard" unselectable by accident. Keep them as two separate questions/selects.

Signals can replace these questions but never add extra ones: an ongoing "just build it" / "surprise me" / "don't ask" locks automation + no storyboard, and every field left unanswered becomes a decision you make and disclose in the final summary. A storyboard request, however phrased, locks storyboard: yes. Remembered preferences reorder the recommended defaults — they never remove either question.

**Step 7 — Nice-to-have offer: recommend, then show.** Skip this step entirely when the chosen route says to skip it (some routes are autonomous by design — see their entries below). Otherwise, once the must-haves are locked, make one offer, not an interrogation:

- Name **one or two capabilities** (see "Capability menu" below) that this specific brief calls for — each traced to something concrete in the confirmed concept (a key number wants a count-up treatment; product shots want staging and a color grade; a music bed means cutting on its beat grid). A suggestion generic enough to fit any video fails this test — drop it. At most one suggestion may be a labeled "stretch" option: a higher ceiling with a named cost ("the standard cut works fine; a shader transition would lift the close, at extra render time").
- If the user has already handed over a logo, a clip, or data, respond with its concrete use ("the logo could close the video as a sting — want that?") instead of silently filing it away.
- Always leave two open doors: "anything else you want in it?" and "is there any material of your own — images, clips, logos, data — the video should carry?"
- The design-system question (below, "The design ask") always gets its own three-state offer here.

Show the full menu of capabilities only if the user explicitly asks what else is possible. Record every answer under clearly labeled sections of the brief (Assets / Customizations / Notes). One round only — silence or "no" means move on.

**Step 8 — Hand off.** Close the conversation with three disciplines:

- **One integration check.** Re-read the combined answers for a consequence no single answer showed on its own — e.g., vertical video at 90 seconds combined with a chart-dense concept means charts a phone screen can't read. Surface it now, with a proposed fix, not later at the build stage.
- **Stated vs. inferred, kept visibly separate.** Present the locked brief as one summary, with what the user explicitly answered and what you inferred or defaulted shown as two separate groups, each with its reasoning attached. The inferred group is where corrections belong.
- **Revision is not automatic confirmation.** If the user corrects the summary, fold the change in and show it again — never start building from an edited-but-unconfirmed brief.

Then start the matched route (or general-video, for a companion run). The very first thing the route does is write a `BRIEF.md` file from this summary — never before any project scaffolding, since scaffolding tools typically refuse to run in a non-empty directory. `BRIEF.md` becomes the single source of truth for "what did the route require?" — nothing later re-opens this interview. It records:

| Key | Meaning | Example |
|---|---|---|
| `workflow` | the executing route (companion runs record `general-video`) | `faceless-explainer` |
| `flow` | `automation` — the matched route's pipeline runs it · `companion` — built together in general-video | `automation` |
| `storyboard` | `yes` — plan, sketches, and build all reviewed on a live board · `no` — one shot from the confirmed brief | `yes` |
| `message` | the ONE thing the video must communicate | `"Ship it in an afternoon"` |
| `destination` / `aspect` / `language` / `audience` / `length` / `angle` … | whatever additional fields that route confirmed | — |

Preserve the user's important wording in the body of the brief — especially the chosen pitch concept, if there was a pitch round, under an "Intent" heading.

### 5. Load reference material on demand

Beyond this document and the hyperframes-cli reference, a full HyperFrames setup organizes deeper reference material by topic area. If you have access to any of the following as separate documents or references, consult them for the matching need; otherwise, apply the general principles in this document and use good judgment:

| Need | Topic area |
|---|---|
| Composition structure, timing attributes, tracks, variables, determinism | Core authoring reference |
| Motion rules, scene blueprints, transitions, runtime adapters | Animation technique library |
| Seek-safe animation code (CSS/JS transforms, paths, masks, SVG, 3D keyframes) and its diagnostics | Keyframe diagnostics reference |
| Design specs, concept, palette, typography, narration, beat planning | Creative/design reference |
| Images, icons, logos, audio, captions, color grades, LUTs, reusable media | Media resolution reference |
| Init, lint, check, snapshots, compare, batch render, preview, render, publish, diagnostics | The hyperframes-cli document |
| Installable scene components (data charts, device mockups, quote cards, etc.) | Registry of scene blocks |
| Figma assets, tokens, components, storyboard frames read as motion | Figma import tooling |

Only pull in what the active route actually needs — don't front-load everything.

## Rules & standards

### Pitch round — how to handle an unformed request

Everything else in the interview converges toward one answer per field. This step diverges on purpose. An unformed request has nothing to converge on yet — "make us a video about the launch" doesn't answer any creative question, and asking for "the message" as a bare form field just hands the user back the blank they came to have filled. So before the form: pitch five different concepts, sampled wide, offered once.

**When it runs.** Only on unformed requests, and only on routes whose entry (below) names pitch-eligible fields. A recipe adoption skips it — the bundle already carries an approved concept. An autonomous ("just build it") request never skips it — it just runs the same gate internally and reports the outcome afterward.

Before generating anything, ask what the user is already picturing. An existing idea seeds the round as a pitch of its own and is never displaced by generated ones. A fully-formed picture ends the round before it starts — that picture is the concept.

**The internal sampling discipline (never shown to the user).** Before writing any pitch, answer four questions about this specific brief, specifically — not generically:

1. **What does the subject actually look like?** Its own visual world — an island-travel piece has whitewashed walls and caldera cliffs; an outage postmortem has terminal green and a scarred timeline. The subject's own vocabulary should drive the layouts.
2. **What does the target emotion look like as a frame?** Longing is empty space the viewer wants to fill; urgency is compression; awe is one element too large for the canvas.
3. **What does the playback surface demand?** A lobby screen is ambient and glanced at; a social feed fights for its first second; a story format is vertical and fast.
4. **What does every other video on this subject already look like?** That's the anti-pattern. None of the five pitches should be it.

Then draft five concepts, one along each of five different paths: the subject's own world · the target emotion · the audience (meeting their expectation, or deliberately breaking it) · the anti-pattern, inverted · an unusual format (a letter, a countdown, a recipe, a front page, a map). For each, estimate — directionally, not scientifically — the probability a generic model handed this brief would land on it by default. The rule this estimate enforces: **at least two of the five must be clear long shots** — concepts a default pass would be unlikely to produce. If all five feel like the obvious safe choice, they're all the median — start over. Then sanity-check that no two concepts share the same basic visual shape; if two do, replace one.

**Presenting the round.** Each pitch gets three lines: the concept in one sentence, its visual world, its opening hook. The visual-world line should name the one or two specific capabilities (see the Capability menu below) the concept rides, in plain language — "the launch number counts up on the track's beat grid," not a feature name. This is how the toolbox reaches the user: experienced inside a concept they can want, not listed as a menu they have to evaluate cold. Only mention a capability where this particular concept actually leans on it — a capability that would fit all five pitches equally is just decoration.

Show all five before recommending anything — recommending first anchors everything that follows and defeats the divergence. Then recommend one, with a reason. Mixing pitches is a first-class answer ("the framing of the second with the opening of the fourth"). Silence or "you decide" accepts the recommendation. One round only — the pitches are an offer, not a quiz, and there's no second batch unless the user explicitly asks for one.

The chosen concept becomes the brief's creative core: it answers the route's pitch-eligible fields (typically `message` and `angle`) — skip those questions downstream, citing the pitch as the reason — and the concept goes into the brief under an "Intent" heading, in the wording the user accepted. Any capabilities the pitch named are confirmed along with it and shouldn't be re-offered later as if new.

**Autonomous runs ("just build it").** Walk the exact same gate — four questions, five concepts, the long-shot requirement, the silhouette check — pick the winner yourself, and keep building. In your final report, name the direction you chose and why, the capability it rides, and the most typical/obvious direction you deliberately passed over. An autonomous run is where defaulting to the median is most dangerous, since no one is present to say "this looks like every other video" — so say it yourself.

**The decision map — for a user who says they don't know anything about video.** Don't give them pitches or a question sequence. Instead give them a map of the two or three decision points where their input genuinely changes the outcome — where it will play, how long it should run, what it should feel like — each with two to four plain-language options and one marked as the default. They choose only where they can actually tell the difference; every surface they don't touch keeps its default, disclosed as such. Then run the sampling gate yourself, autonomous-style, and present the winning concept inside the final brief summary — accepting the summary accepts the concept.

### Capability menu — what a HyperFrames video can include

Offer these selectively (per step 7 above), never as a dump. Each row is a thing HyperFrames can add to a video; phrase it to the user in plain language, not as a feature name.

| Capability | Say it to the user as… |
|---|---|
| **Design spec** — one settings file that locks palette, type, and layout feel so every frame stays consistent | "a design system for the video — colors and typography stay consistent throughout" |
| **Website capture** — a headless-browser crawl of a real site: screenshots, brand colors/fonts, assets | "I can capture your site and build the video from its real look" |
| **Beat analysis & audio-reactive motion** — a deterministic beat/energy map of a track, so cuts land on the grid and elements pulse with the music | "if there's music, I can cut the video to its beat — and make elements move with it" |
| **Motion blueprints** — proven scene shapes (reveals, counters, charts, dioramas) picked per beat instead of improvised movement | "each scene gets a proven motion treatment, not improvised movement" |
| **Voice, music, sound effects, images, logos, color grades** — generated or resolved and frozen into the project | "narration in a voice you pick, background music, sound effects, brand logos — and a cinematic grade on your images" |
| **Generative video** — an AI presenter reads the script on camera; a still photo becomes a talking clip; a finished video gets dubbed into another language | "an AI presenter can read your script on camera, or I can animate a photo into a talking clip, or dub the video into another language" |
| **Transcription & captions** — word-timed transcripts and styled caption treatments | "accurate captions, styled to match your brand" |
| **Cut footage by its transcript** — trim a clip by choosing sentences rather than timecodes | "I can trim your clip by picking the sentences to keep, not by scrubbing timecodes" |
| **Designed overlays on the user's own footage** — kinetic titles, lower-thirds, data callouts synced to what's being said | "your own clip can carry designed titles and info bars, timed to the speech" (this is the whole point of the talking-head-recut route when it's the main ask, or a single scene treatment inside a bigger piece) |
| **Real map scenes** — a genuine basemap with located pins, routes, or a flight path | "for places and journeys — a real map, not a drawing of one" |
| **Figma import** — assets, brand tokens, components, storyboard frames read directly as motion states | "if the design already lives in Figma, I can build straight from it" |
| **Registry blocks** — 50+ ready-made scene compositions (data charts, device mockups, quote cards, etc.) that can be dropped in and restyled | "ready-made scenes we can drop in and restyle" |
| **Scene transitions** — cuts, crossfades, wipes, up to full shader-based wipes between scenes | "how one scene hands off to the next — up to full shader wipes" |
| **User media on the timeline** — the user's own images/clips staged and woven directly into frames | "your own footage, screenshots, or photos placed right into the video" |
| **Publish to a stable link** — the finished piece lives at a public URL; re-publishing updates the same link | "when it's done I can publish it to a link you can share — updates keep the same URL" |

Offer, don't unload: recommend only the one or two rows the confirmed concept itself calls for, state each as one plain-language line traced back to the brief, and ask once. Show the full table only if asked what else is possible.

### The design ask — have one, pick one, or defer

The design-spec question is a three-state question, not an explainer:

- **They already have one.** Brand guidelines, an existing design-spec file — note it down as an asset; treat it as brand truth for the whole build.
- **They don't have one, but the look matters — show, don't name.** Pick 2–3 shipped visual presets whose look fits the content, tone, and audience, and let the user look at each rather than choosing from a list of names. The choice becomes a remembered preference for next time. On a route that captures a real site, be upfront: a shown preset wears its own placeholder palette — the site's real brand colors and fonts get remixed onto whichever preset wins, so **the pick is really about the layout bones, not the colors** — and offer to defer the pick until after capture, when the look can be judged with the real brand already in hand.
- **They don't care, or nothing shown fits.** If they don't care: ask nothing further, and let the build process decide (and explain why when it does). If nothing fits: tell the user a design pass will generate mood boards from their actual content to choose from later — it needs a project scaffolded first, so it can't happen inside this conversation.

### Genre lenses — borrow the taste, not the machinery

The narrative-style routes (faceless-explainer, product-launch-video, pr-to-video) each carry their own genre-tuned design references — narrative archetypes and beats, the genre's visual look, and motion/cut doctrine. When a companion or open-ended piece resembles one of these genres, borrow that route's taste before planning or building in it:

| The piece resembles… | Borrow the visual/narrative sense of… |
|---|---|
| a product promo / launch / site showcase | product-launch-video |
| a topic / mechanism / concept explainer | faceless-explainer |
| a code-change walkthrough | pr-to-video |

Borrow the shape and the taste, never any pipeline-specific machinery that belongs to that route alone.

### Keeping AI-agent skill packs current (if applicable)

If your working environment maintains an installed set of HyperFrames reference/skill packs (a "core set" plus route-specific ones installed on demand), keep it current by running, when available:

```bash
npx hyperframes skills check
npx hyperframes skills update
```

Bare `skills update` refreshes whatever is already installed without expanding what's installed; naming a specific route also installs that one. If this mechanism isn't part of your environment, ignore it — this document already contains the routing guidance for every route inline.

## Project Routes

Each subsection below is one route: its Input/Output/Trigger contract, plus what its interview stage needs to ask. Read only the route that matches, per the routing table above.

### remotion-to-hyperframes

- **Input:** Existing Remotion React source code, only when the user explicitly asks to port, convert, or migrate it. A passing mention of Remotion is not enough to trigger this route.
- **Output:** A HyperFrames HTML composition translated from the Remotion source, compared against the original Remotion render to verify the migration.
- **Triggers:** "port my Remotion project", "convert this Remotion composition", "migrate from Remotion".
- **Interview:** None — this route is not served by the interview at all. A migration has no creative brief to write; route directly and get to work.

### slideshow

- **Input:** A brief, outline, or existing page to author as a presentation, pitch deck, or interactive deck. If "slides", "deck", or "convert this page" is ambiguous, confirm the user actually wants a HyperFrames slideshow before authoring anything.
- **Output:** A runnable HyperFrames composition plus its accompanying navigation data: discrete slides, fragment reveals, branching, hotspots, presenter mode, and speaker notes. The deliverable is a navigable deck, not an MP4.
- **Triggers:** "make a pitch deck", "interactive presentation", "convert this page into slides", "slideshow with presenter mode".
- **Interview:** The only question is the routing confirmation itself — "do you want this as a HyperFrames slideshow?" — asked up front, since getting the format wrong is a real quality problem. After that's confirmed, everything else about the deck is decided as you build it.
- **Run-shape:** Neither storyboard nor automation/companion questions apply — the deliverable is a navigable deck, not a rendered video.
- Skip the general nice-to-have capability offer (step 7) — after route confirmation, deck-specific choices take over.

### embedded-captions

- **Input:** Existing talking-head footage to caption. Must be an actual media file, not a URL or a creative brief.
- **Output:** The same footage, untouched, with a caption layer and a chosen caption visual style added. The speaker may occlude captions in some layouts. Any length.
- **Triggers:** "add captions", "add subtitles", "captions behind the subject", "cinematic captions for my clip".
- **Interview must-haves:** which clip (the input file itself).
- **Deferred (announce now, answer later):** the caption style pick — probe the actual clip first, then shortlist 2–3 caption styles and recommend one. Tell the user this choice is coming, don't ask for it yet.
- **Run-shape:** Neither applies — the footage itself is untouched, so there's no storyboard to review.

### talking-head-recut

- **Input:** Existing talking-head, interview, or podcast footage to package. The underlying clip plays unchanged.
- **Output:** The same footage with transcript-synced graphic overlay cards: kinetic titles, lower-thirds, data callouts, pull-quotes, side panels, or picture-in-picture. Any length.
- **Triggers:** "package this video", "add graphic overlays to my talk", "add lower-thirds or data callouts to this interview".
- **Interview must-haves:** which clip (the input file itself).
- **Deferred (announce now, answer later):** the render-strategy questions — aspect ratio, layout, style group, card count — get decided later once the footage and transcript have actually been probed, since the recommendations depend on what's really in the clip. Tell the user these are coming.
- **Run-shape:** Neither applies.

### music-to-video

- **Input:** A music track, or a video whose audio track becomes the music, with no narration and no website capture involved. User-supplied images or videos are optional.
- **Output:** A beat-synced MP4 driven by a deterministic beat/energy map of the track. It may end up as a lyric video, a slideshow, a visualizer, or a kinetic promo without changing the underlying approach.
- **Triggers:** "make a video for this song", "beat-synced video", "lyric video", "music visualizer", "kinetic promo to this beat".
- **Interview must-haves:** the music source (a track file, a video to pull audio from, or a mood description to generate one from) · destination/platform → aspect ratio.
- **Deferred (announce now, answer later):** the brand look (font + palette) and the genre feel are chosen after analyzing the track, by design — they should emerge from what the track actually sounds like, not from a question asked before anyone's heard it.
- **Pitch round eligible field:** `message` — the visual concept that rides the beat grid (a lyric treatment, a montage story, kinetic type). Brand and genre feel still get decided after analysis.
- **Run-shape:** Both storyboard and automation/companion questions apply.

### motion-graphics

- **Input:** A short, design-led unit, typically under 10 seconds, with no narration, where motion itself is the message: kinetic type, a stat or count-up, a chart hit, a logo sting, an animated title, a lower-third, a map hit, a highlighted tweet/headline/page, or an asset-fusion shot.
- **Output:** A short MP4, or a transparent-alpha overlay file (WebM/MOV).
- **Triggers:** "an 8s logo sting", "animate this stat", "kinetic-type intro", "animate this title", "transparent lower-third overlay".
- **Interview:** Autonomous by design — at most one clarifying question total, asked while actually building it. No must-have questions up front beyond confirming the input; route directly.
- **Run-shape:** Neither applies — the piece is only seconds long, so a storyboard review and a collaborative build session don't add anything.
- Skip the nice-to-have capability offer (step 7) entirely — the one-question limit above is authoritative.

### pr-to-video

- **Input:** A GitHub PR URL, an `owner/repo#N` reference, or "this PR" — read the actual PR content. Not a general website-capture request.
- **Output:** A changelog video, feature reveal, fix explainer, or refactor walkthrough, with diff views, before/after comparisons, file-tree views, and impact scenes as appropriate. Hard cap around 3 minutes; actual duration follows the size of the change.
- **Triggers:** "make a video about this PR", "turn PR #1187 into a changelog video", "release-notes video from this pull request".
- **Interview must-haves:**
  - The PR reference itself (URL, `owner/repo#N`, or "this PR").
  - **Angle** — changelog / feature-reveal / fix-explainer / refactor-walkthrough — recommend whichever the PR's own content suggests.
  - **Audience** — developers (default) / mixed technical / non-technical stakeholders.
  - **Length** — pulled from the size table below.
  - **Destination** — 16:9 is the default for a code explainer.
- **Determining length from PR size** (don't guess — actually look):

  ```bash
  gh pr view <PR_REF> --json title,additions,deletions,changedFiles
  ```

  Pick a tier from `additions + deletions` (nudged up if `changedFiles` is large), and lead with the recommended length (hard cap ~3 minutes):

  | PR change size | Recommended length |
  |---|---|
  | trivial (roughly ≤ 50 lines changed) | ~20–40s |
  | focused (roughly 50–200 lines) | ~40–70s |
  | substantial (roughly 200–600 lines) | ~70–110s |
  | large (roughly 600+ lines, or 25+ files) | ~110–180s |

  State the basis in one phrase, e.g. "~40s — small change, +44/−13 across 12 files." Treat the tier as a **ceiling**, never a floor to pad out to — a PR that really only tells one headline story should still be recommended at 30–90s regardless of what its size tier allows; the fuller range can still be offered as a non-default option.

- **Pitch round eligible fields:** `angle` and the opening hook — the diff fixes the facts, but not how they're told.
- **Run-shape:** Both apply.

### product-launch-video

- **Input:** A website URL; a script or brief that names a site; or a product-launch script with no derivable site, or an explicit "do not scrape" instruction. Capture website assets and brand tokens by default unless the brief says otherwise. Always ask whether any supplied script copy is meant as verbatim voice-over or may be restructured.
- **Output:** A product promo, launch video, site tour, or showcase MP4. Sweet spot 30–90 seconds; hard cap around 3 minutes. A "show it as-is" brief features the captured screens themselves as the video's assets rather than inventing new visuals.
- **Triggers:** "launch video for X", "promo for our site", "turn this script into a 60s promo", "text-only launch video", "turn this website into a video", "site tour from this URL".
- **Interview — first question when not already answered:** sell or show? Market the product as a promo, or show the site as-is as a tour/showcase? A "show it" answer is a stated intent, not a different pipeline — write it into the brief and let the normal steps below carry it; the captured screens simply become the featured assets.
- **Must-haves:**
  - **Angle** — a story shape drawn from the site's or brief's own positioning; recommend one and say why.
  - **Length** — 30–90s sweet spot, scaled to how much material there actually is.
  - **Destination** — YouTube/embed → 16:9 · X/LinkedIn/Instagram feed → 1:1 · Shorts/TikTok → 9:16.
- **Conditional questions:**
  - A "show it as-is" answer adds: what specifically to show — the whole site, or specific pages/sections?
  - A pasted script or brief adds: is the copy verbatim voice-over, or can it be restructured?
  - A script that only names a site (no material of its own) adds: crawl the site for brand and assets (default), or stay text-only / don't scrape (a preset design supplies the look instead)?
- **Pitch round eligible fields:** `message` + `angle`, decided after the sell-or-show question is settled — the pitches should inherit that intent.
- **Run-shape:** Both apply.

### faceless-explainer

- **Input:** A topic, article, notes, or arbitrary text being explained — with no product being marketed and no website to capture.
- **Output:** A faceless explainer MP4 using invented typography, abstract graphics, diagrams, or data visualization (no on-camera presenter). Sweet spot 30–90 seconds; hard cap around 3 minutes.
- **Triggers:** "faceless explainer about X", "explain how DNS works as a video", "turn this article into an explainer".
- **Must-haves:**
  - **Angle** — concept / how-to / listicle / narrative — recommend whichever shape the source text itself suggests.
  - **Length** — inside the 30–90s sweet spot, scaled to how much the text actually teaches.
  - **Destination** — YouTube/embed → 16:9 · X/LinkedIn/Instagram feed → 1:1 · Shorts/TikTok → 9:16.
- **Conditional:** a pasted script adds one question — use it verbatim as voice-over, or restructure it scene by scene?
- **Pitch round eligible fields:** `message` + `angle` — five different tellings of the same topic are five different videos.
- **Run-shape:** Both apply.

### general-video

- **Input:** Any custom creation or edit that doesn't fit one of the specialized routes above: a static title card, a longer brand or sizzle reel, a multi-scene montage, a static loop/poster, an editorial-style footage remix, or any freeform composition. This route also executes every companion-mode brief regardless of which route it was originally matched to.
- **Output:** A HyperFrames composition of any length or format, built through design → plan → static layout → animation → check → approval → render.
- **Triggers:** "make a static title card", "longer brand reel", "multi-scene composition", "static loop", "custom video", or any video request that doesn't match a more specific route.
- **Interview — open-ended requests:** first derive a one-sentence message for the piece. Ask about audience only when it's genuinely unclear and would change the story or the terminology used. Ask about destination only when it would actually change the aspect ratio or composition. Ask for a stated priority only when the brief contains a real trade-off to resolve. Default to producing one best version; only ask about variations if the user explicitly requests options or a comparison.
- **Interview — specific, complete requests:** a fully specified ask ("a static title card with our logo for a website hero") needs no discovery questions at all — just build it.
- **Pitch round eligible field:** `message` — the unformed open-ended request is this round's home case.
- **Run-shape:** Both questions apply. Because this route also hosts every companion-mode session, `flow: companion` always lands here regardless of which route matched originally, with the full capability set available.

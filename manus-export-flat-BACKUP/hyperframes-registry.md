# HyperFrames Registry

This document explains the HyperFrames component/block registry: a shared catalog of reusable, pre-built pieces (standalone sub-compositions called "blocks," and reusable effect snippets called "components") that can be discovered, installed into a HyperFrames video composition project, and wired into that project's `index.html`. It also covers how to author and contribute a brand-new block or component back to the shared registry. Use this document whenever a HyperFrames composition needs a reusable visual/animation piece — a caption style, a data chart, a transition, a social-media overlay, a lower third, a VFX effect, a code-typing animation, or similar — instead of hand-building it from scratch, or whenever the task is to package something newly built so others can reuse it the same way.

The registry distinguishes two item types:

- **Blocks** — standalone sub-compositions with their own dimensions, duration, and internal timeline (e.g., an animated chart, a caption style, a title card). A block is included into a host composition via a `data-composition-src` reference.
- **Components** — effect snippets with no dimensions or duration of their own (e.g., a film-grain overlay, a text shimmer effect). A component's HTML/CSS/JS is pasted directly into the host composition rather than referenced externally.

## How to use this

**To find and install something that already exists in the registry:**

1. List what's available — either by running the catalog command (see Templates & examples) or, if that's unavailable, by fetching the raw registry manifest JSON directly from its public URL. Filter by item type (block or component) and by tag if you know roughly what you're looking for (e.g., tag `social` for platform-style overlays).
2. Pick the specific item name from the results, then install it with the `add` command, which writes the item's file(s) into the project (a block goes to `compositions/<name>.html` by default; a component goes to `compositions/components/<name>.html` by default) and prints a starting HTML snippet to wire it in.
3. If installing a block, place the printed `<div>` snippet into the host `index.html`, then fill in the required attributes: `data-composition-id` (must exactly match the block's own internal composition ID — check inside the installed file if unsure), `data-start` (when it appears, in seconds), `data-duration` (how long it plays), and `data-track-index` (layer order — higher numbers render in front).
4. If installing a component, open the installed snippet file, read its instructions comment, then manually copy its HTML into the host composition's markup, its CSS into the host's style block, and any JS into the host's script (placed before the host's own timeline-building code). If the component exposes GSAP timeline calls (documented in its comment header), add those calls into the host's own timeline.
5. Run the lint/check/preview commands (see Templates & examples) to confirm the wiring is structurally valid before treating it as done.

**To author and contribute a brand-new block or component:**

1. Decide which item type fits: a block if it needs its own fixed dimensions/duration/timeline (caption style, VFX effect, title card, lower third); a component if it's a snippet that should adapt to whatever composition it's dropped into (CSS effects, text treatments, overlays with no fixed size).
2. Write down: a one-sentence description of the effect, a visual reference (URL, screenshot, or written description), and who would use it and when.
3. Create the registry folder structure for the item (see Rules & standards → Naming and Scaffold structure below) and start from the matching starter template (see Templates & examples).
4. Build the item following the type-specific rules (caption rules, VFX rules, or the general all-types rules below).
5. Validate it structurally (lint with zero errors, check with zero console errors).
6. Generate a preview render and snapshot stills at several timestamps for visual QA; if a hosted preview/publish mechanism is available, publish the item there so reviewers can see it live.
7. Produce a catalog preview image (a PNG generated from a snapshot) for the item's catalog card — or, if that's not possible locally, attach a preview video to whatever contribution/PR mechanism is used so a maintainer can generate the catalog image before merging.
8. Package the change for contribution: create a branch, run the project's HTML formatter over the new files, add the new item's entry to the registry's master manifest file (`registry.json`), regenerate the catalog documentation pages if that step exists, publish a preview link if available, then commit and open a pull request (or equivalent contribution mechanism) referencing the preview link. Run through the full Quality Gate checklist (below) before considering the contribution ready.

## Rules & standards

### Quick reference: installing (CLI form)

```bash
hyperframes add data-chart              # install a block
hyperframes add grain-overlay           # install a component
hyperframes add captions                # install every block tagged captions
hyperframes add shimmer-sweep --dir .   # target a specific project
hyperframes add data-chart --json       # machine-readable output
hyperframes add data-chart --no-clipboard  # skip clipboard (CI/headless)
```

After install, the tool prints which files were written and a starting snippet to paste into the host composition. The snippet is a starting point only — `data-composition-id` (must match the block's internal composition ID), `data-start`, and `data-track-index` still need to be added by hand when wiring blocks.

The name given to `add` is resolved as an exact item name first. If no item matches and the value looks like a tag instead, the command installs every block carrying that tag. Any registry dependencies an item declares are installed automatically before the requested item itself. The `add` command only works for blocks and components — worked examples (as opposed to installable pieces) are fetched with a separate `init --example <name>` style command, not `add`.

### Install locations

| Item type | Default install path | Configured by |
|---|---|---|
| Block | `compositions/<name>.html` | `hyperframes.json#paths.blocks` |
| Component | `compositions/components/<name>.html` | `hyperframes.json#paths.components` |

Each item's own manifest (`registry-item.json`) specifies a default install `target` path. The install command remaps the path prefix based on the project's own `hyperframes.json#paths` config:

- A block target starting with `compositions/` gets remapped to `<paths.blocks>/`.
- A component target starting with `compositions/components/` gets remapped to `<paths.components>/`.

If `hyperframes.json` doesn't exist yet in the project when installing something, it should be created automatically with these defaults:

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

To use a custom layout — e.g., installing blocks into a `scenes/` directory instead of `compositions/` — edit the paths config:

```json
{
  "paths": {
    "blocks": "scenes"
  }
}
```

After that change, installing a block named `data-chart` would write to `scenes/data-chart.html` instead of the default location, and the printed wiring snippet reflects the remapped path.

### Wiring blocks

Blocks are standalone compositions with their own `data-composition-id`, dimensions, duration, and internal timeline. Include one in a host composition using `data-composition-src` on a `<div>`:

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <video id="a-roll" src="video.mp4" data-start="0" data-duration="20" data-track-index="0"></video>

  <!-- Block: appears at 2s, plays for 15s, on layer 1 -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="2"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>
</div>
```

Required attributes:

| Attribute | Description |
|---|---|
| `data-composition-src` | Path to the block HTML file (relative to the host `index.html`) |
| `data-composition-id` | Unique ID matching the block's own internal composition ID |
| `data-start` | When the block appears in the host timeline (seconds) |
| `data-duration` | How long the block plays (seconds; at most the block's own native duration) |
| `data-track-index` | Layer ordering — higher numbers render in front |
| `data-width` | Block canvas width (must match the block's own dimensions) |
| `data-height` | Block canvas height (must match the block's own dimensions) |

**Timeline coordination:** a block's internal timeline runs independently of the host timeline. The HyperFrames runtime loads the sub-composition, finds its registered timeline, and seeks the block in sync with the host, offset by `data-start`. There is no need to manually reference the block's internal timeline from the host's own timeline code — this coordination is automatic once the attributes above are set correctly.

**Positioning a block** on screen is done with ordinary CSS on the wiring `<div>`:

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
  style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
></div>
```

**Multiple blocks** can be added as additional sibling `<div data-composition-src="...">` elements, with non-overlapping or overlapping `data-start` values as needed — each block's timeline is independent and seeked in sync by the runtime.

### Wiring components

Components are effect snippets — HTML, CSS, and optionally JS — merged directly into an existing host composition. Unlike blocks, a component has no standalone timeline of its own; it participates in the host composition's timeline.

General process:

1. Install the component.
2. Open the installed file (e.g., `compositions/components/grain-overlay.html`).
3. Read its comment header for usage instructions.
4. Copy its parts into the host composition:
   - HTML elements — inside the host's `<div data-composition-id="...">` wrapper.
   - CSS styles — into the host's `<style>` block.
   - JS setup — into the host's `<script>`, placed before the host's own timeline-building code.
   - Timeline calls — into the host's GSAP timeline, if the component exposes any (documented in its comment header).

**Key principles:**
- Components inherit the host composition's dimensions and duration — they have none of their own.
- Place a component's HTML at the appropriate z-index/layer relative to the rest of the host's content.
- Always read the comment header in each installed snippet for the values that are meant to be customized.
- Re-run structural validation (lint) after wiring any component to catch structural issues.

### Discovery

Use the catalog listing command as the primary way to discover what's in the registry:

```bash
npx hyperframes catalog
npx hyperframes catalog --type block
npx hyperframes catalog --type component
npx hyperframes catalog --type block --tag social
npx hyperframes catalog --json
npx hyperframes catalog --human-friendly
```

- Default output is a readable table; it does not install anything by itself.
- `--type` accepts `block` or `component`; `--tag` further narrows either result set.
- `--json` is the deterministic, scriptable output mode — select a name from it, then run the install command explicitly.
- `--human-friendly` opens an interactive picker and installs the selected item immediately (best for a human at a terminal; prefer `--json` + explicit install for scripted/agent workflows).

If the catalog command itself is unavailable, the registry's manifest can be read directly as a fallback:

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

Each entry in that manifest has a `name` and a `type` (`hyperframes:example`, `hyperframes:block`, or `hyperframes:component`).

Each individual item additionally has its own detailed manifest file, reachable at:

```
<base>/<type-dir>/<name>/registry-item.json
```

where `<type-dir>` is `examples`, `blocks`, or `components` depending on the item's type.

**Item manifest fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Kebab-case identifier |
| `type` | string | yes | `hyperframes:block` or `hyperframes:component` |
| `title` | string | yes | Human-readable title |
| `description` | string | yes | One-line description |
| `tags` | string[] | no | Filter tags (e.g., `["data", "chart"]`) |
| `dimensions` | object | blocks only | `{ width, height }` |
| `duration` | number | blocks only | Duration in seconds |
| `files` | array | yes | Files to install (`path`, `target`, `type`) |
| `registryDependencies` | string[] | no | Other registry items this one depends on |

### Contributing a new block or component

Workflow: **Clarify → Scaffold → Build → Validate → Preview → Ship**

**Step 1 — Clarify.** Confirm the item type (block vs. component, per the distinction above), then capture: a one-sentence description of the effect, a visual reference (URL, screenshot, or description), and who uses it and when.

**Step 2 — Scaffold.** Create the folder structure:

For blocks:
```
registry/blocks/{block-name}/
  {block-name}.html
  registry-item.json
```

For components:
```
registry/components/{component-name}/
  {component-name}.html
  registry-item.json
```

**Naming convention:** use a short 2–3 letter prefix for the item, and prefix EVERY element ID inside the item's HTML with it, to avoid ID collisions when the item is embedded inside a host composition.

| Item name | ID prefix | Example IDs |
|---|---|---|
| `cap-hormozi` | `hz` | `hz-cg-0`, `hz-cw-3` |
| `cap-typewriter` | `tw` | `tw-cg-0`, `tw-ch-0-5` |
| `vfx-chrome` | `vc` | `vc-canvas` |

Write `registry-item.json` using the canonical templates (block and component variants — see Templates & examples), filling in all required fields.

**Step 3 — Build.** Apply the template matching the item's type (see Templates & examples).

*Caption blocks — non-negotiable rules:*
- Font size: 96px minimum for proportional fonts; 64–72px is acceptable for monospace fonts (wider characters need less size to stay readable).
- Readability: use `-webkit-text-stroke: 2-3px` OR a multi-layer `text-shadow` so text stays legible over any background.
- Overflow: call the runtime's `window.__hyperframes.fitTextFontSize()` helper on every text group to prevent overflow.
- Karaoke-style word highlighting: highlight the active word by animating it with `tl.to(wordEl, { color/scale }, WORDS[wi].start)`.
- Hard kill: every group must be force-hidden at its end time with `tl.set(groupEl, { opacity: 0, visibility: "hidden" }, g.end)` — this is mandatory on every group, no exceptions.
- **Never use `tl.from(el, { opacity: 0 })` at the same timeline position as `tl.set(el, { opacity: 1 })`** — the `from` call clobbers the `set` call. Use `tl.to` instead when you need both an entrance and an explicit visible state at the same position.

*Per-character animation (typewriter, scramble effects):*
- Wrap each character in its own `<span>`, with an ID of the form `{prefix}-ch-{group}-{char}`.
- Stagger character reveals via `tl.set` calls placed at intervals computed from the word timestamps.
- Cursors and other decorative elements must be driven by `tl.set` at computed intervals — never by a plain CSS animation, because CSS animations driven by wall-clock time are not seekable.

*VFX blocks (Three.js-based):*
- Load `three@0.147.0` from a CDN as a global script.
- Drive rendering via `tl.eventCallback("onUpdate", renderScene); renderScene();` — do NOT use `requestAnimationFrame` for render-critical motion.
- Use a state-proxy pattern: GSAP animates a plain JS object, and a separate render function reads that object's current values and applies them to the 3D scene.
- Use a seeded pseudo-random number generator (e.g., a `mulberry32`-style seeded PRNG) for any randomness — never unseeded `Math.random()`.

*All item types:*
- `data-composition-id` on the root element MUST match the key used to register the timeline in `window.__timelines["id"]`.
- Every element ID must be prefixed with the item's chosen abbreviation.
- Timelines must always be created paused: `gsap.timeline({ paused: true })`.
- No `Math.random()` and no `Date.now()` anywhere in render-critical code.

**Step 4 — Validate.**
```bash
hyperframes lint                    # 0 errors required
hyperframes check --no-contrast     # 0 console errors required
```

**Step 5 — Preview.**
```bash
# Render preview video
hyperframes render -o preview.mp4

# Snapshot for visual QA
hyperframes snapshot --at "1.0,3.0,5.0,7.0"

# Publish to a hosted preview URL for review
npx hyperframes publish
```

The catalog card for a new item uses a PNG at `docs/images/catalog/{kind}/{name}.png` (where `{kind}` is `blocks` or `components`), generated from a snapshot. If working inside the project's own engineering org with access to its internal upload tooling, run that upload step directly; otherwise (an external contributor), attach the preview MP4 to the pull request description instead and let a maintainer generate and upload the catalog image before merge.

**Step 6 — Ship.** All of the following steps are required — skipping any one of them produces a broken catalog entry:

1. Create a branch for the change (e.g., `feat/registry-{name}`).
2. Run the project's HTML formatter over the new item's files.
3. Update the registry's master `registry.json` manifest — add an entry to its `items` array: `{ "name": "{name}", "type": "hyperframes:block" }` (or `"hyperframes:component"` for a component).
4. Regenerate the catalog documentation pages, if that generation step exists in the project.
5. Publish to the hosted preview URL so reviewers can see it live before merging.
6. Stage the new item's files, the updated `registry.json`, and the regenerated catalog docs.
7. Commit with a descriptive message, e.g. `feat(registry): add {name} — {one sentence}`.
8. Push the branch and open a pull request whose description includes the hosted preview link.

If there's no account on the code-hosting platform being used, one needs to be created before a pull request can be opened.

**Quality Gate — confirm all of these before considering a contribution finished:**
- [ ] `hyperframes lint` → 0 errors
- [ ] `hyperframes check` → 0 console errors
- [ ] HTML formatter check passes
- [ ] `registry.json` updated with the new entry
- [ ] Catalog docs page generation step run
- [ ] Hosted preview publish step run (so the project URL can be shared)
- [ ] Preview MP4 attached to the PR (external contributor) or catalog PNG uploaded (internal contributor)
- [ ] All element IDs are unique and correctly prefixed

### The demo.html convention (components only)

Every **component** in the registry ships a companion `demo.html` file alongside its snippet. It serves two purposes:

1. **Preview fixture** — a preview-rendering pipeline renders the demo to generate thumbnail images and preview videos for the item's catalog docs page.
2. **Usage example** — the demo shows the component's effect applied to representative content, serving as a working reference for how to use it.

A demo is a complete, standalone HTML composition (structure shown in Templates & examples below). Key conventions:

- `data-composition-id` on the demo's root is `<component-name>-demo`, to avoid ID collisions with anything else.
- The demo is fully self-contained — all CSS and JS from the actual component snippet is inlined directly into it.
- The demo's GSAP timeline is registered on `window.__timelines` exactly like any other composition.
- Duration should be long enough to clearly showcase the effect — typically 5–8 seconds.

**Blocks do not need a `demo.html`** — a block is already a standalone, directly renderable composition, so no separate demo wrapper is required.

**Demos are never installed** by the install command — `demo.html` exists only inside the registry itself, for preview generation and as a human-readable reference; end users never receive it when they install the component.

## Templates & examples

### Worked example: adding a block

**Scenario:** an existing HyperFrames project needs an animated chart added alongside existing video content.

1. Install the block:
```bash
hyperframes add data-chart
```

2. Wire it into `index.html`:
```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="30">
  <video
    id="speaker"
    src="speaker.mp4"
    data-start="0"
    data-duration="30"
    data-track-index="0"
    style="position: absolute; width: 60%; height: 100%; left: 0; top: 0; object-fit: cover;"
  ></video>

  <!-- Data chart appears at 5s in the right 40% of the screen -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="5"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
    style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
  ></div>
</div>
```

3. Lint and preview:
```bash
hyperframes lint
hyperframes preview
```

4. Customize (optional): edit `compositions/data-chart.html` directly — data arrays are typically at the top of the script, colors are typically in CSS rules scoped under `[data-composition-id="data-chart"]`.

### Worked example: adding a component

**Scenario:** add a shimmer light-sweep effect to a title text element.

1. Install the component:
```bash
hyperframes add shimmer-sweep
```

2. Read the snippet: open `compositions/components/shimmer-sweep.html` and read its comment header.

3. Wire it into the host composition.

HTML — wrap the target elements:
```html
<div class="shimmer-sweep-target" style="--shimmer-color: rgba(255, 255, 255, 0.5)">
  <h1 class="title">AI-Powered Video</h1>
</div>
```

CSS — paste the `.shimmer-sweep-target` and `.shimmer-mask` rules from the snippet into the host's styles.

JS — paste the auto-injection script (before the host's timeline code):
```js
document.querySelectorAll(".shimmer-sweep-target").forEach((el) => {
  if (!el.querySelector(".shimmer-mask")) {
    const mask = document.createElement("div");
    mask.className = "shimmer-mask";
    el.appendChild(mask);
  }
});
```

Timeline — add the sweep to the host's own GSAP timeline:
```js
tl.fromTo(
  ".shimmer-sweep-target",
  {
    "--shimmer-pos": "-20%",
  },
  {
    "--shimmer-pos": "120%",
    duration: 1.2,
    ease: "power2.inOut",
    stagger: 0.15,
  },
  1.5,
);
```

4. Lint and preview:
```bash
hyperframes lint
hyperframes preview
```

5. Customize using the effect's exposed variables:
- `--shimmer-color`: highlight color per element
- `--shimmer-width`: light band width (default 20%)
- `--shimmer-angle`: sweep direction (default 120deg)
- Timeline `duration`, `ease`, `stagger`: control speed and feel

### Example: a CSS-only component with no timeline integration (grain-overlay)

```html
<!-- Paste the overlay div into your composition -->
<div
  id="grain-overlay"
  style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100;"
>
  <div class="grain-texture"></div>
</div>
```

Then paste the CSS `@keyframes` and `.grain-texture` rule into the host's styles. No GSAP timeline calls are needed here — the grain animates purely via CSS `@keyframes`.

### demo.html structure (for components)

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Component Name — Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* reset + canvas size */
    </style>
  </head>
  <body>
    <div data-composition-id="<name>-demo" data-width="1920" data-height="1080" data-duration="N">
      <!-- Demo content showing the effect -->
      <!-- Component snippet inlined here -->
    </div>
    <script>
      // GSAP timeline demonstrating the effect
      window.__timelines = window.__timelines || {};
      window.__timelines["<name>-demo"] = tl;
    </script>
  </body>
</html>
```

### Caption block starter template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: #111;
        overflow: hidden;
      }
      #root-BLOCKNAME {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #111;
      }
      .cap-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .cg {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 32px;
        max-width: 1700px;
        overflow: visible;
        opacity: 0;
        visibility: hidden;
      }
      .cw {
        font-family: "Montserrat", sans-serif;
        font-weight: 900;
        font-size: 128px;
        color: #ffffff;
        text-transform: uppercase;
        line-height: 1;
        display: inline-block;
        -webkit-text-stroke: 3px rgba(0, 0, 0, 0.8);
        paint-order: stroke fill;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
      }
    </style>
  </head>
  <body>
    <div
      id="root-BLOCKNAME"
      data-composition-id="BLOCKNAME"
      data-start="0"
      data-duration="9"
      data-width="1920"
      data-height="1080"
    >
      <div class="cap-container" id="cc-BLOCKNAME"></div>
      <div
        id="drv-BLOCKNAME"
        class="clip"
        data-start="0"
        data-duration="9"
        data-track-index="0"
        style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none"
      ></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};

        // REPLACE with actual transcript data
        var WORDS = [
          { text: "Welcome", start: 0.3, end: 0.65 },
          { text: "to", start: 0.65, end: 0.8 },
          { text: "the", start: 0.8, end: 0.95 },
          { text: "future", start: 0.95, end: 1.4 },
          // ... add all words
        ];

        var GROUPS = [
          { start: 0.3, end: 1.3, wordStart: 0, wordEnd: 3, text: "Welcome to the future" },
          // ... add all groups
        ];

        var container = document.getElementById("cc-BLOCKNAME");

        GROUPS.forEach(function (g, gi) {
          var groupEl = document.createElement("div");
          groupEl.id = "PREFIX-cg-" + gi;
          groupEl.className = "cg";

          for (var wi = g.wordStart; wi <= g.wordEnd; wi++) {
            var wordEl = document.createElement("span");
            wordEl.id = "PREFIX-cw-" + wi;
            wordEl.className = "cw";
            wordEl.textContent = WORDS[wi].text;
            groupEl.appendChild(wordEl);
          }

          // Pretext overflow prevention
          if (window.__hyperframes && window.__hyperframes.fitTextFontSize) {
            var _fit = window.__hyperframes.fitTextFontSize(g.text.toUpperCase(), {
              fontFamily: "Montserrat",
              fontWeight: 900,
              maxWidth: 1550,
              baseFontSize: 128,
              minFontSize: 48,
            });
            if (_fit.fontSize < 128) {
              for (var _fi = 0; _fi < groupEl.children.length; _fi++) {
                groupEl.children[_fi].style.fontSize = _fit.fontSize + "px";
              }
            }
          }
          container.appendChild(groupEl);
        });

        var tl = gsap.timeline({ paused: true });

        GROUPS.forEach(function (g, gi) {
          var groupEl = document.getElementById("PREFIX-cg-" + gi);

          // SHOW — set opacity to 1 (never use tl.from with opacity:0 here)
          tl.set(groupEl, { opacity: 1, visibility: "visible" }, g.start);

          // ENTRANCE — customize this per style
          tl.from(groupEl, { scale: 1.3, duration: 0.15, ease: "back.out(2)" }, g.start);

          // KARAOKE — highlight each word
          for (var wi = g.wordStart; wi <= g.wordEnd; wi++) {
            var wordEl = document.getElementById("PREFIX-cw-" + wi);
            tl.to(wordEl, { color: "#FFD700", scale: 1.1, duration: 0.06 }, WORDS[wi].start);
            tl.to(wordEl, { color: "#FFFFFF", scale: 1, duration: 0.08 }, WORDS[wi].end);
          }

          // EXIT
          tl.to(groupEl, { opacity: 0, scale: 0.9, duration: 0.1 }, g.end - 0.1);

          // HARD KILL (mandatory)
          tl.set(groupEl, { opacity: 0, visibility: "hidden" }, g.end);
        });

        window.__timelines["BLOCKNAME"] = tl;
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**
- `BLOCKNAME` → your block name (e.g., `cap-swoosh`)
- `PREFIX` → short unique prefix for IDs (e.g., `sw`)
- Font family, weight, size → your style's typography
- Entrance animation → your style's entrance
- Karaoke highlight → your style's active word treatment
- Colors → your style's palette

### VFX block starter template (Three.js)

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.147.0/build/three.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: #030308;
        overflow: hidden;
      }
      #root-BLOCKNAME {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #030308;
      }
      #canvas-BLOCKNAME {
        position: absolute;
        top: 0;
        left: 0;
        width: 1920px;
        height: 1080px;
      }
    </style>
  </head>
  <body>
    <div
      id="root-BLOCKNAME"
      data-composition-id="BLOCKNAME"
      data-start="0"
      data-duration="10"
      data-width="1920"
      data-height="1080"
    >
      <canvas id="canvas-BLOCKNAME" width="1920" height="1080"></canvas>
      <div
        id="drv-BLOCKNAME"
        class="clip"
        data-start="0"
        data-duration="10"
        data-track-index="0"
        style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none"
      ></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};

        // Seeded PRNG — NEVER use Math.random()
        function mulberry32(a) {
          return function () {
            a |= 0;
            a = (a + 0x6d2b79f5) | 0;
            var t = Math.imul(a ^ (a >>> 15), 1 | a);
            t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
          };
        }
        var rng = mulberry32(42);

        var W = 1920,
          H = 1080;
        var canvas = document.getElementById("canvas-BLOCKNAME");
        var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
        renderer.setSize(W, H);
        renderer.setPixelRatio(1);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.1;

        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0x030308);
        var camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 100);
        camera.position.set(0, 0, 8);

        // YOUR SCENE SETUP HERE
        // - lights
        // - geometry
        // - materials

        // State proxy — GSAP animates this, render reads it
        var st = {
          rotY: 0,
          camZ: 8,
          // add your animated properties
        };

        var tl = gsap.timeline({ paused: true });

        // YOUR TWEENS HERE
        tl.to(st, { rotY: Math.PI * 2, duration: 10, ease: "none" }, 0);

        window.__timelines["BLOCKNAME"] = tl;

        function renderScene() {
          // Apply state to Three.js objects
          camera.position.z = st.camZ;
          // mesh.rotation.y = st.rotY;

          renderer.render(scene, camera);
        }

        // Render via onUpdate — NO requestAnimationFrame
        tl.eventCallback("onUpdate", renderScene);
        renderScene();
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**
- `BLOCKNAME` → your block name (e.g., `vfx-chrome-blob`)
- Scene setup → your geometry, lights, materials
- State proxy → your animated properties
- Tweens → your animation timeline
- renderScene → apply state to your Three.js objects

### registry-item.json templates

**For blocks:**
```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "BLOCKNAME",
  "type": "hyperframes:block",
  "title": "Human-Readable Title",
  "description": "One sentence: what it does and who uses it",
  "dimensions": { "width": 1920, "height": 1080 },
  "duration": 10,
  "tags": ["category", "subcategory"],
  "files": [
    {
      "path": "BLOCKNAME.html",
      "target": "compositions/BLOCKNAME.html",
      "type": "hyperframes:composition"
    }
  ]
}
```

**For components** (no `dimensions` or `duration`):
```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "COMPONENTNAME",
  "type": "hyperframes:component",
  "title": "Human-Readable Title",
  "description": "One sentence: what it does",
  "tags": ["category"],
  "files": [
    {
      "path": "COMPONENTNAME.html",
      "target": "compositions/components/COMPONENTNAME.html",
      "type": "hyperframes:snippet"
    }
  ]
}
```

Tags by category:
- Captions: `captions`, `viral`, `professional`, `karaoke`, `minimal`
- VFX: `three-js`, `particles`, `shader`, `gpu`
- Transitions: `transition`, `shader`, `wipe`, `dissolve`
- Blocks: `lower-third`, `social`, `title-card`, `data-viz`
- Components: `effect`, `overlay`, `text-treatment`

### Component starter template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *,
      *::before,
      *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        background: transparent;
        overflow: hidden;
      }
      .COMPNAME-wrap {
        position: absolute;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div class="COMPNAME-wrap">
      <!-- Your reusable effect/overlay here -->
    </div>
    <script>
      (function () {
        // Component snippet — no data-composition-id, no __timelines.
        // The parent composition controls timing.
        // Keep all class names and IDs prefixed with COMPNAME.
      })();
    </script>
  </body>
</html>
```

**Replace checklist:**
- `COMPNAME` → your component name (e.g., `shimmer-sweep`)
- Background should be `transparent` so it overlays cleanly
- No `data-composition-id` or `window.__timelines` — the parent owns timing

### Available registry items (reference catalog snapshot)

This is a snapshot of what has been available in the registry; run the catalog discovery command for an always-current list, since new items are added over time.

**Blocks** are grouped into these categories: shader transitions (single-shader effects like chromatic split, cinematic zoom, glitch, light leak, ripple waves, swirl vortex, whip pan — use at most 2 per video); transition galleries (reference showcases of CSS/GSAP transition families — 3D, blur, cover, destruction, dissolve, distortion, grid, light, mechanical, push, radial, scale — meant as reference for picking a style, not for embedding as-is); Liquid Glass effects (WebGPU frosted-glass surfaces requiring a WebGPU-enabled browser); VFX blocks (HTML-in-canvas + WebGL compositions like device mockups, liquid backgrounds, magnetic fields, portals, shatter effects); Showcases (narrated story-driven inserts with bundled SFX — app showcases, counters, map animations); Maps + data viz (D3+GSAP choropleths, bubble maps, flow maps, hex maps, bar/line charts, flowcharts); Social overlays (platform-recognizable UI cards — Instagram/TikTok follow cards, YouTube lower thirds, X posts, Reddit posts, Spotify now-playing cards, macOS notifications); Branding + 3D UI (logo assembly outros, 3D UI reveals); Code snippets (24 themed code/terminal windows that type a session character-by-character — 12 VS Code workbench themes, 12 Apple Terminal color profiles — identical structure/wiring across all, differing only in visual chrome); and Code Animations (9 richer motion-first code blocks — typing reveals, diffs, morphs, line-highlight sweeps, scroll-through-file, snippet flight-assembly, and three GPU/WebGL hero reveals for title-card moments).

**Components** available include: `grain-overlay` (animated film grain texture), `shimmer-sweep` (CSS gradient light sweep for AI-style accents), `morph-text` (gooey text morph cycling an editable word list via SVG threshold + GSAP blur), `grid-pixelate-wipe` (grid dissolve transition between scenes), `parallax-zoom` (a center card scales up to fill the frame while sibling cards parallax outward), and `parallax-unzoom` (the reverse — a focus card shrinks from full-frame while siblings parallax back in).

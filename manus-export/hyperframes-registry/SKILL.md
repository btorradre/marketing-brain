---
name: hyperframes-registry
description: >
  Discover, install, and wire registry blocks and components into a HyperFrames
  video/motion-graphics composition, and author a brand-new block or component to
  contribute back to the shared registry. Use when a composition needs a reusable
  visual/animation piece — a caption style, a data chart, a transition, a social-media
  overlay, a lower third, a VFX effect, a code-typing animation, or similar — instead
  of hand-building it from scratch, or when packaging something newly built so others
  can reuse it. Covers the `hyperframes add` and `hyperframes catalog` commands,
  install locations, block sub-composition wiring, component snippet merging, and
  authoring a new registry item (idea → scaffold → validate → ship).
---

# HyperFrames Registry

The registry is a shared catalog of reusable, pre-built pieces for a HyperFrames composition: standalone sub-compositions called "blocks," and reusable effect snippets called "components." Items are discovered, installed into a project, and wired into that project's `index.html`.

- **Blocks** — standalone sub-compositions with their own dimensions, duration, and internal timeline (e.g., an animated chart, a caption style, a title card). A block is included into a host composition via a `data-composition-src` reference.
- **Components** — effect snippets with no dimensions or duration of their own (e.g., a film-grain overlay, a text shimmer effect). A component's HTML/CSS/JS is pasted directly into the host composition rather than referenced externally.

## To find and install something that already exists

1. **List what's available** — either by running the catalog command (below) or, if that's unavailable, by fetching the raw registry manifest JSON directly from its public URL. Filter by item type (block or component) and by tag if you know roughly what you're looking for (e.g., tag `social` for platform-style overlays). See `references/discovery.md` for the full catalog snapshot and manifest field reference.
2. **Pick the specific item name**, then install it with the `add` command, which writes the item's file(s) into the project (a block goes to `compositions/<name>.html` by default; a component goes to `compositions/components/<name>.html` by default) and prints a starting HTML snippet to wire it in.
3. **If installing a block**, place the printed `<div>` snippet into the host `index.html`, then fill in the required attributes: `data-composition-id` (must exactly match the block's own internal composition ID — check inside the installed file if unsure), `data-start` (when it appears, in seconds), `data-duration` (how long it plays), and `data-track-index` (layer order — higher numbers render in front). See `references/wiring-blocks.md`.
4. **If installing a component**, open the installed snippet file, read its instructions comment, then manually copy its HTML into the host composition's markup, its CSS into the host's style block, and any JS into the host's script (placed before the host's own timeline-building code). If the component exposes GSAP timeline calls (documented in its comment header), add those calls into the host's own timeline. See `references/wiring-components.md`.
5. **Run the lint/check/preview commands** (below) to confirm the wiring is structurally valid before treating it as done.

### Quick reference

```bash
hyperframes add data-chart              # install a block
hyperframes add grain-overlay           # install a component
hyperframes add captions                # install every block tagged captions
hyperframes add shimmer-sweep --dir .   # target a specific project
hyperframes add data-chart --json       # machine-readable output
hyperframes add data-chart --no-clipboard  # skip clipboard (CI/headless)
```

After install, the tool prints which files were written and a starting snippet to paste into the host composition. The snippet is a starting point only — `data-composition-id`, `data-start`, and `data-track-index` still need to be added by hand when wiring blocks.

The name given to `add` is resolved as an exact item name first. If no item matches and the value looks like a tag instead, the command installs every block carrying that tag. Any registry dependencies an item declares are installed automatically before the requested item itself. The `add` command only works for blocks and components — worked examples are fetched with a separate `init --example <name>` style command, not `add`.

## Install locations

| Item type | Default install path | Configured by |
|---|---|---|
| Block | `compositions/<name>.html` | `hyperframes.json#paths.blocks` |
| Component | `compositions/components/<name>.html` | `hyperframes.json#paths.components` |

Each item's own manifest (`registry-item.json`) specifies a default install `target` path, which the install command remaps based on the project's own `hyperframes.json#paths` config. If `hyperframes.json` doesn't exist yet in the project, it's created automatically with sane defaults. Full details, including how to point installs at a custom directory layout, are in `references/install-locations.md`.

## Wiring blocks

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

A block's internal timeline runs independently of the host timeline. The runtime loads the sub-composition, finds its registered timeline, and seeks the block in sync with the host, offset by `data-start` — there is no need to manually reference the block's internal timeline from the host's own timeline code. Position a block on screen with ordinary CSS on the wiring `<div>` (e.g. `position: absolute; right: 0; top: 0; width: 40%; height: 100%;`). Multiple blocks can be added as additional sibling `<div data-composition-src="...">` elements, each independently seeked. Full attribute reference in `references/wiring-blocks.md`.

## Wiring components

Components are effect snippets — HTML, CSS, and optionally JS — merged directly into an existing host composition. Unlike blocks, a component has no standalone timeline of its own; it participates in the host composition's timeline.

1. Install the component.
2. Open the installed file (e.g., `compositions/components/grain-overlay.html`) and read its comment header for usage instructions.
3. Copy its parts into the host composition: HTML elements inside the host's `<div data-composition-id="...">` wrapper; CSS styles into the host's `<style>` block; JS setup into the host's `<script>` (placed before the host's own timeline-building code); and any exposed GSAP timeline calls into the host's own timeline.
4. Re-run lint after wiring to catch structural issues.

Components inherit the host composition's dimensions and duration — they have none of their own. Full worked examples in `references/wiring-components.md` and `references/examples.md`.

## Discovery

Use the catalog listing command as the primary way to discover what's in the registry:

```bash
npx hyperframes catalog
npx hyperframes catalog --type block
npx hyperframes catalog --type component
npx hyperframes catalog --type block --tag social
npx hyperframes catalog --json
npx hyperframes catalog --human-friendly
```

`--type` accepts `block` or `component`; `--tag` further narrows either result set. `--json` is the deterministic, scriptable output mode — select a name from it, then run the install command explicitly (this is the mode to prefer for scripted/agent workflows). `--human-friendly` opens an interactive picker and installs the selected item immediately (best for a human at a terminal).

If the catalog command itself is unavailable, the registry's manifest can be read directly as a fallback:

```bash
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

Each entry has a `name` and a `type` (`hyperframes:example`, `hyperframes:block`, or `hyperframes:component`). Each individual item additionally has its own detailed manifest at `<base>/<type-dir>/<name>/registry-item.json`. The full current catalog snapshot (all block categories and components, grouped by kind) and the manifest field reference are in `references/discovery.md`.

## Contributing a new block or component

Workflow: **Clarify → Scaffold → Build → Validate → Preview → Ship**.

1. **Clarify** — decide block vs. component (a block needs its own fixed dimensions/duration/timeline; a component is a snippet that adapts to whatever composition it's dropped into), then capture a one-sentence description, a visual reference, and who would use it and when.
2. **Scaffold** — create the registry folder structure for the item and start from the matching starter template. Use a short 2-3 letter prefix for the item and prefix EVERY element ID inside the item's HTML with it, to avoid ID collisions when the item is embedded inside a host composition.
3. **Build** — apply the type-specific rules (caption rules, VFX rules, or the general all-types rules) — see `references/contributing.md`. Copy-paste starter templates (caption / VFX / component / `registry-item.json`) are in `references/templates.md`. Components additionally ship a companion `demo.html` — see `references/demo-html-pattern.md`.
4. **Validate** — `hyperframes lint` (0 errors required) and `hyperframes check --no-contrast` (0 console errors required).
5. **Preview** — render a preview video, snapshot stills at several timestamps for visual QA, and publish to a hosted preview URL if that mechanism is available so reviewers can see it live. Produce a catalog preview image (a PNG generated from a snapshot) for the item's catalog card, or attach a preview video to the contribution/PR if generating the PNG isn't possible locally.
6. **Ship** — create a branch, run the project's HTML formatter over the new files, add the new item's entry to the registry's master `registry.json` manifest, regenerate the catalog documentation pages if that step exists, publish a preview link if available, then commit and open a pull request referencing the preview link.

The full step-by-step workflow, the non-negotiable caption/VFX build rules, and the Quality Gate checklist are in `references/contributing.md`.

## Item manifest fields

Each `registry-item.json` has: `name` (kebab-case, required), `type` (`hyperframes:block` or `hyperframes:component`, required), `title`, `description`, `tags` (optional filter tags), `dimensions`/`duration` (blocks only), `files` (install list), and `registryDependencies` (optional). Full field table in `references/discovery.md`.

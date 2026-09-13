# HyperFrames CLI

Reference for the HyperFrames command-line tool: scaffolding, linting/checking, previewing, rendering (local, HeyGen-hosted cloud, AWS Lambda, Google Cloud Run), comparing, batch rendering, and diagnostics. Use this whenever building, editing, or fixing a HyperFrames video composition project, or diagnosing a build/render failure.

Run every command as `npx hyperframes ...` (unless a specific project has its own wrapper script — follow that instead when one exists). The CLI requires **Node.js 22 or newer** and **FFmpeg** installed on the machine running it.

`validate`, `inspect`, and `layout` are deprecated aliases — they still work but print a deprecation notice; use `check` instead in any new work.

## The core development loop

1. **Scaffold** the project: `npx hyperframes init <project>`, or capture an existing website as a starting point.
2. **Author** the composition HTML (timing, tracks, motion) using the HyperFrames composition-authoring conventions.
3. **Get fast feedback while editing:** run `npx hyperframes lint` after the first HTML pass and after any structural change.
4. **Run the final gate:** run `npx hyperframes check` — it reruns lint first, then opens a browser to audit the composition. Don't run a separate standalone `lint` immediately before this; `check` already includes it. Add `--snapshots` for annotated overview frames and crops of any findings.
5. **Inspect sub-compositions:** if `index.html` mounts other composition files via `data-composition-src`, capture midpoint snapshots and inspect each mounted scene individually.
6. **Open the final preview:** run `npx hyperframes preview`, hand the resulting timeline URL to whoever needs to review it, and wait for a decision to revise or render.
7. **Render only after approval:** use draft quality while iterating and high quality for the actual delivered file. Never render automatically just because checks passed — always wait for explicit approval of the preview.
8. **Verify the output:** confirm the rendered file exists, is non-empty, and has a plausible duration.

```bash
# Fast iteration check; repeat while authoring as needed.
npx hyperframes lint

# Required final gate; includes lint.
npx hyperframes check
npx hyperframes preview
npx hyperframes render --quality high --output out.mp4
test -s out.mp4
ffprobe -v error -show_format out.mp4
```

`check` runs the linter first, then uses one browser session and one seek pass to audit runtime errors, failed network requests, layout, any `*.motion.json` motion assertions, and WCAG color-contrast — all in a single Chrome boot. Persistent findings (present across multiple sampled frames) gate the exit code; findings only present transiently at an entrance/exit moment are informational only. Pass `--strict` to also gate on warnings, not just errors.

## Two different preview surfaces — don't confuse them

| Surface | When it may open | Purpose |
|---|---|---|
| Storyboard board | Before composition checks run, only when the project's brief calls for a storyboard review | Review plan cards and wireframe sketches. Open with `?view=storyboard#project/<name>`. |
| Final composition preview | After `check` passes | Review the assembled timeline before rendering. Open with `#project/<name>`. |

The early storyboard board is **not** approval of the final video. Rendering always requires the separate final-preview approval described above — never skip straight from a storyboard sign-off to a render.

## Sub-composition smoke test

Static audits alone can't catch every mount failure. If the project uses sub-compositions, capture at least one visible midpoint frame for each host slot:

```bash
npx hyperframes snapshot --at <t1>,<t2>,<t3>
```

Treat any of the following as a render-blocking defect: tiny unstyled content, canvas-sized icons where real content should be, a missing hero element, or a timeline-registration timeout.

## Practical conventions for automated/scripted use

- Prefer `--json` output on every command when scripting or running unattended. Note that server-mode commands (`render`, `preview`, `play`) don't provide ordinary JSON output while running — the JSON exceptions are `preview --selection --json` and `preview --context --json`, which are one-shot queries against an already-running preview server.
- `doctor --json` always exits `0` regardless of findings — gate on its payload instead of its exit code: `npx hyperframes doctor --json | jq -e '.ok' >/dev/null`.
- Outside an interactive terminal, the CLI automatically runs in non-interactive mode. `init` then *requires* `--example` to be passed explicitly. Pass `--non-interactive` yourself to force the same deterministic behavior even inside an interactive terminal.
- Use one consistent `HYPERFRAMES_RUN_ID` environment variable value across every command in the same verification loop, if your environment supports setting it.
- Use `--strict`, `--strict-all`, and `--strict-variables` whenever the corresponding warnings, variables, or pass/fail conditions need to actually gate the run rather than just be reported.
- JSON output redacts the home directory as the literal string `$HOME` — don't try to reverse this redaction.
- If a hosted-cloud upload approaches or exceeds the 200 MB limit, use `cloud render --dry-run --json` and follow the `.hyperframesignore` investigation procedure under "Cloud (HeyGen-hosted rendering)" below. Never exclude an asset from the render just because it happens to be large — verify it's actually unused first.
- Never render just because checks passed. Always pause at the final preview and wait for explicit approval before spending render time/cost.

## Reading the current Studio-editor selection

If you're working with a project open in the interactive Studio editor and someone refers to "this element," "the selected element," or "make the card I clicked bigger" — don't guess. Query the live Studio session instead:

```bash
npx hyperframes preview --context --json --context-fields selection
```

This doesn't start a new server; it finds the currently running preview server for the project, reads state from Studio, and exits. Use the returned `selection.target.hfId` when present; fall back to `selection.target.selector` only if no stable id exists. If it reports `no-selection`, ask the person to click the element in Studio and rerun. Keep the requested context small — ask only for the field slices actually needed:

```bash
npx hyperframes preview --context --json --context-fields selection
npx hyperframes preview --context --json --context-fields lint
npx hyperframes preview --context --json --context-fields selection,lint
```

Use `--context-detail full` only when the edit genuinely needs heavy fields like computed styles, inline styles, data attributes, or editable text-field metadata:

```bash
npx hyperframes preview --context --json --context-fields selection --context-detail full
```

`preview --selection --json` (without `--context`) returns the full selected-element payload directly, when lint/server context isn't needed.

Failure codes to handle:

| Code | Meaning |
|---|---|
| `preview-not-running` | Start the preview server first with `npx hyperframes preview`. |
| `ambiguous-preview-server` | Multiple matching preview servers are open; rerun specifying `--port`. |
| `preview-port-mismatch` | The requested `--port` doesn't match any of the running servers. |
| `no-selection` | The editor is open, but nothing is selected yet. |
| `selection-unavailable` | The running server doesn't expose selection context cleanly. |

## Render path choices

| Need | Command |
|---|---|
| Fast local iteration | `npx hyperframes render --quality draft` |
| Final local delivery | `npx hyperframes render --quality high --output out.mp4` |
| Reproducible container render (byte-identical across machines) | `npx hyperframes render --docker --strict --output out.mp4` |
| Local variable-driven batch render | `npx hyperframes render --batch rows.json --output "renders/{name}.mp4"` |
| Zero-infrastructure hosted render | `npx hyperframes cloud render` |
| Self-managed distributed render on AWS | `npx hyperframes lambda render <project> --width 1920 --height 1080 --wait` |
| Self-managed distributed render on GCP | `npx hyperframes cloudrun render <project> --width 1920 --height 1080 --wait` |

Use the hosted cloud path when the goal is rendering without managing local Chrome/FFmpeg/AWS. Use Lambda only when AWS ownership specifically matters to the user. Use Cloud Run only when GCP ownership specifically matters. Read the corresponding section below before running any cloud path for the first time.

After verifying a successful render, it's good practice to log one feedback report (see "Feedback" under Preview & Render below) unless telemetry has been disabled.

---

## Init & Scaffold

Scaffolding commands set up the right file structure, copy in media, run transcription, and (in the original Claude Code environment) install matching AI-coding reference packs — treat that last part as optional/environment-specific.

### init

```bash
npx hyperframes init my-video                                    # interactive terminal: wizard
npx hyperframes init my-video --example warm-grain               # pick a specific example
npx hyperframes init my-video --example blank --resolution portrait
npx hyperframes init my-video --video clip.mp4                   # scaffold with a video file
npx hyperframes init my-video --audio track.mp3                  # scaffold with an audio file
npx hyperframes init my-video --example blank --tailwind         # Tailwind v4 browser runtime
npx hyperframes init my-video --non-interactive --example blank  # CI/scripted — flag-only
```

**Default behavior depends on whether you're in an interactive terminal.** In a terminal, the CLI prompts for the example/options interactively. Outside a terminal (CI, automation, piped output) it auto-switches to non-interactive mode and **requires `--example`** — it errors with a usage example if that flag is missing. Pass `--non-interactive` yourself to force flag-only behavior even inside an interactive terminal.

Available templates: `blank`, `warm-grain`, `play-mode`, `swiss-grid`, `vignelli`, `decision-tree`, `kinetic-type`, `product-promo`, `nyt-graph`.

Other useful flags:

- `--resolution` — a preset: `landscape` (1920×1080), `portrait` (1080×1920), `landscape-4k`, `portrait-4k`, `square` (1080×1080), `square-4k`. Aliases: `1080p`, `4k`, `uhd`, `1080p-square`, `4k-square`.
- `--skip-transcribe` — don't auto-transcribe a supplied `--audio` / `--video` file with Whisper.
- `--model`, `--language` — choose the Whisper model / language for auto-transcription.

When `--audio` or `--video` is supplied, `init` transcribes the file automatically with Whisper.

### capture

```bash
npx hyperframes capture https://stripe.com                  # scaffold a project from a live website
npx hyperframes capture https://linear.app -o linear-video  # custom output directory
npx hyperframes capture https://example.com --json          # JSON output for scripting
npx hyperframes capture https://example.com --skip-assets   # skip downloading images/SVGs
npx hyperframes capture https://example.com --max-screenshots 12
npx hyperframes capture https://example.com --timeout 60000 # page-load timeout in ms
```

Captures a live URL into an editable HyperFrames project: screenshots become layered scenes, assets get downloaded locally, and the result is a normal project you can lint/preview/render like any other. Use this whenever the user hands over a URL as the starting point for a video.

---

## Preview & Render

### preview

```bash
npx hyperframes preview                    # serve current directory
npx hyperframes preview --port 4567        # custom port (default 3002)
npx hyperframes preview --selection --json # print the current editor selection and exit
npx hyperframes preview --context --json   # print compact agent-facing context from the editor
```

Hot-reloads on file changes and opens the full timeline editor in the browser automatically — this is the actual review surface, where whoever's reviewing can play the video and hand-edit anything before rendering, not just a static viewer.

When handing a project link back to a user, hand them the editor's project URL, not the raw `index.html` file path:

```text
http://localhost:<port>/#project/<project-name>
```

Use the real port and project directory name. For example, after running `npx hyperframes preview --port 3017` inside a project called `codex-openai-video`, the link to share is `http://localhost:3017/#project/codex-openai-video`.

To land directly on the **storyboard view** instead of the timeline (useful before `index.html` exists and there's nothing yet for the timeline to show), put `?view=storyboard` before the hash:

```text
http://localhost:<port>/?view=storyboard#project/<project-name>
```

Before handing a preview URL to anyone, check two things that would make it dead on arrival: the URL is missing its `#project/<project-name>` hash (the editor loads but has no project open), or the preview server process actually isn't running anymore (it's long-running — if it reports having exited, restart it before handing out the link).

### play (lightweight player)

```bash
npx hyperframes play                  # current project, port 3003
npx hyperframes play ./my-video       # specific project
npx hyperframes play --port 8080      # custom port
```

`play` serves the composition through a lightweight embeddable player component instead of the full editor UI — no editor panels, just playback. Use it for a plain shareable preview link. `play` reports a plain `http://localhost:<port>` URL with no `#project/<name>` fragment (that routing convention is specific to `preview`'s editor).

The player's playback-rate control is clamped to the range `[0.1, 5]`; invalid values fall back to `1`. This only affects preview playback speed — the actually-authored motion timing always renders at normal (1×) speed.

**Launching in an external/specific browser** (applies to both `preview` and `play`):

| Flag | Type | Notes |
|---|---|---|
| `--browser-path` | path | Absolute path to a Chromium-compatible browser executable. |
| `--user-data-dir` | path | Chromium-compatible profile directory. Requires `--browser-path`. Use a throwaway directory to avoid touching your main browser profile. |
| `--remote-debugging-port` | integer 1–65535 | Opens a remote-debugging endpoint on this port for external tools to attach to. Requires both `--browser-path` and `--user-data-dir` together — refused otherwise, so a debugging endpoint can't accidentally open on your main profile. |

```bash
# Open preview in an isolated browser profile
npx hyperframes preview --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile

# Same, plus a debug endpoint on :9222 for external tooling to attach to
npx hyperframes play --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile --remote-debugging-port 9222
```

### render

> Render only after a human has reviewed it in `preview` and explicitly approved it. Never auto-render just because checks passed.

```bash
npx hyperframes render                                # standard MP4 from current directory
npx hyperframes render ./my-video --output ./out.mp4  # render from outside the project directory
npx hyperframes render --output final.mp4             # named output (no timestamp)
npx hyperframes render -c compositions/intro.html -o intro.mp4  # render a specific sub-composition file
npx hyperframes render --quality draft                # fast iteration
npx hyperframes render --fps 60 --quality high        # final delivery
npx hyperframes render --format webm                  # transparent WebM
npx hyperframes render --docker                       # byte-identical reproducible output
```

Default output path is `renders/<project-name>_<YYYY-MM-DD>_<HH-MM-SS>.<ext>` — timestamped so successive renders never overwrite each other. Pass `--output` explicitly to get a stable, predictable filename.

| Flag | Options | Default | Notes |
|---|---|---|---|
| `dir` (positional) | path | cwd | Project directory. Omit to use the current directory. |
| `--composition`, `-c` | path to a composition file | `index.html` | Render a specific composition file instead of the project's main `index.html`. |
| `--output`, `-o` | path | timestamped, see above | Output file path. |
| `--fps` | 24, 30, 60 | 30 | 60fps roughly doubles render time. |
| `--quality` | draft, standard, high | standard | Use draft while iterating. |
| `--format` | mp4, webm, mov, gif, png-sequence | mp4 | WebM/MOV support transparency; gif is a two-pass palette encode capped at 30fps (prefer `--fps 15`), no audio, 1-bit transparency only, HDR falls back to SDR; png-sequence writes RGBA frames to a directory for compositing tools. |
| `--gif-loop` | 0–65535 | 0 | GIF loop count; `0` = loop forever. Only with `--format gif`. |
| `--resolution` | landscape, portrait, landscape-4k, portrait-4k, square, square-4k (+ aliases `1080p`, `4k`, `uhd`) | — | Supersamples via the browser's device-scale factor. Aspect ratio must match the composition; scale factor must be a whole number. Not combinable with `--hdr`. |
| `--crf` | 0–51 | — | Encoder quality (lower = higher quality). Mutually exclusive with `--video-bitrate`. |
| `--video-bitrate` | e.g. `10M`, `5000k` | — | Target bitrate. Mutually exclusive with `--crf`. |
| `--hdr` | flag | off | Force HDR output even from SDR sources. MP4 only. |
| `--sdr` | flag | off | Force SDR even from HDR sources. |
| `--workers` | number or `auto` | auto | Each worker spawns its own browser instance (~256 MB each). |
| `--docker` | flag | off | Reproducible output across different host machines. |
| `--gpu` | flag | off | GPU-accelerated video encoding where available. |
| `--browser-gpu` / `--no-browser-gpu` | flag | auto (local), off (docker) | Whether the browser uses the host GPU while capturing frames. |
| `--browser-timeout` | seconds (0.001–86400) | 60 | Page-load timeout for the entry HTML. Raise this if a heavy composition (lots of video/fonts/remote assets) can't finish loading within the default 60s. |
| `--quiet` | flag | off | Suppress verbose output. |
| `--strict` | flag | off | Fail the render on lint errors. |
| `--strict-all` | flag | off | Fail on lint errors AND warnings. |
| `--variables` | JSON object | — | Override values declared as composition variables. |
| `--variables-file` | path | — | JSON file with variable values (alternative to `--variables`). |
| `--strict-variables` | flag | off | Fail the render on undeclared keys or type mismatches in `--variables`. |

**Quality guidance:** `draft` while iterating, `standard` for internal review, `high` for the final delivered file.

**Parametrized/templated renders:** a composition can declare a set of named variables with defaults built into its HTML. The CLI's `--variables '{"title":"Q4 Report"}'` flag is a JSON object keyed by variable id that overrides those defaults for one specific render — any keys you don't pass just fall through to their defaults, so the same composition behaves identically whether previewed live or rendered from a script.

### Feedback (after rendering)

After verifying a render, it's good practice to log one feedback entry per task if your environment has telemetry enabled:

```bash
npx hyperframes feedback --rating 10                              # clean run, no notes
npx hyperframes feedback --rating 6 --comment "bg <video> renders grey in multi-scene; worked around with --format png-sequence"
```

`--rating` is a required integer 0–10; `--comment` is free text. For any bug, workaround, or confusing behavior, include a proper reproduction packet rather than just a symptom summary: the exact rerunnable command and working directory, expected vs. actual behavior, the exact error text (with frame/timestamp for visual defects), the outcome (output correct / corrupt / fell back / hard exit / hung), and the exact workaround if any. For a rating of 7 or below describing a visual defect (black frame, flicker, corrupt output, wrong frame, blank output), also include a compact structural summary of the composition: counts of each element type (video/audio/img/svg/canvas/sub-compositions), which relevant HTML attributes are present, whether the timeline is flat or nested, what animation driver is in use, and (for a workaround case) exactly what differs between the working and broken versions. This structural summary is privacy-preserving — counts and presence flags only, never file paths, URLs, or user text — so it lets someone debug a class of bug without needing the actual project files.

`--file-issue` (optionally with `--dir <project>` and `--yes` for non-interactive use) additionally publishes a minimal public reproduction and drafts a bug report. This publishes the project publicly, so treat it as consent-gated — never do this without the user's explicit agreement, and never auto-submit it.

### publish

```bash
npx hyperframes publish              # upload current project, return a public URL
npx hyperframes publish ./my-video   # specific project
npx hyperframes publish --yes        # skip the confirmation prompt (scripts/automation)
```

Uploads the project's source (HTML + assets) and returns a stable public URL that renders live in the browser. Use this to share a draft for review before committing to a full MP4 render, or to embed the composition somewhere else. Lint findings are shown before upload but don't block it.

---

## Lint, Check, Snapshot

Use `lint` for fast static feedback while iterating. Use `check` as the required final gate — it reruns the linter, then audits runtime behavior, layout, motion, and color contrast in one browser session. Don't chain a redundant standalone `lint` immediately before `check`. `snapshot` is the standalone utility for capturing still frames and zoomed crops.

**Discipline for animation-heavy work:** run `lint` after the first HTML pass; run `check --snapshots` at the first full pass and actually look at the resulting PNGs before tuning any automated warning — your eye catches what the auditor misses, and vice versa. Treat any layout error as a real defect unless a snapshot proves the overlap/overflow is intentional (in which case mark it explicitly, see escape hatches below). State motion intent in a `*.motion.json` sidecar file so `check` can verify it automatically — this is the closest automated proxy available to actually watching the rendered video.

### lint

```bash
npx hyperframes lint                  # current directory
npx hyperframes lint ./my-project     # specific project
npx hyperframes lint --verbose        # include info-level findings
npx hyperframes lint --json           # machine-readable
```

Lints the main `index.html` and everything under `compositions/`. Reports errors (must fix), warnings (should fix), and — with `--verbose` — info-level notes. Catches missing composition-id attributes, overlapping animation tracks on the same track index, unregistered timelines, and animation-library/CSS-transform conflicts.

**Known blind spot (not yet a lint rule):** a `<video>` or `<audio>` element placed inside a sub-composition template (or nested inside a wrapper `<div>` anywhere other than directly at the top level of the main `index.html`) never actually gets seeked or decoded, and renders blank/black — while every automated check still passes. Media elements must be direct children of the main document root. Check for this manually before rendering:

```bash
grep -nE '<(video|audio)\b' compositions/*.html   # expect NO matches; media belongs in index.html
```

Any match here is a real defect. Then snapshot each scene containing a video and confirm the panel actually shows footage — a blank/black panel where a clip should play is render-blocking, not a placeholder.

### check

```bash
npx hyperframes check                    # current directory: the full gate
npx hyperframes check ./my-project       # specific project
npx hyperframes check --json             # {ok, lint, runtime, layout, motion, contrast, snapshots}
npx hyperframes check --snapshots        # also write annotated overview frames + per-finding crops
npx hyperframes check --samples 15       # denser timeline sweep (default 9)
npx hyperframes check --at 1.5,4,7.25    # explicit timestamps to sample
npx hyperframes check --at-transitions   # also sample every animation start/end boundary
npx hyperframes check --tolerance 4      # allowed overflow in px before reporting (default 2)
npx hyperframes check --timeout 5000     # ms allowed for the initial page settle (default 3000)
npx hyperframes check --no-contrast      # skip the color-contrast audit while iterating
npx hyperframes check --strict           # exit non-zero on warnings too (default: errors only)
```

One command, one browser session. `check` runs the linter first and skips opening a browser entirely if lint reports errors. Otherwise it loads the composition once and sweeps across a grid of sampled timeline positions, running every audit at each sample:

- **Runtime:** JavaScript console errors, unhandled exceptions, failed network requests (with media-file abort errors filtered out), HTTP 4xx/5xx responses.
- **Layout:** text extending outside its container or the canvas, text clipped by its own box, overlapping/occluded held text (with an approximate covered-fraction estimate), children escaping their clipping containers.
- **Motion:** `*.motion.json` sidecar assertions checked against the same seeked timeline (see below).
- **Contrast:** WCAG AA contrast on visible text, sampled at 5 grid points. Contrast failures are treated as errors, and each finding includes the sampled foreground/background colors, the measured vs. required ratio, and a suggested compliant replacement color in the same palette direction — so most contrast fixes don't even need a screenshot to resolve.

Every finding includes a selector, the element's identifying attributes, the source composition file, a bounding box, and the sample timestamp — enough to jump straight from the JSON output to the exact HTML that needs editing.

**Severity is persistence-aware.** A finding that appears at only a single sample (e.g. a transient mid-entrance/exit moment) is demoted to informational and never gates the run. A finding held across multiple samples gates the exit code: a held overlap is always an error; a held partial-canvas-overflow finding that covers 5%+ of the canvas is promoted to a warning. There's a separate category of "coordinate-frame" findings (geometry computed relative to the wrong parent, a panel stuck across the canvas edge, a connector line detached from the nodes it should connect). If a composition longer than 3 seconds shows literally zero geometry change across every sample, `check` fails outright with a "frozen timeline" error — a static timeline makes every other "pass" result unreliable, so it refuses to report success at all. Per-element opacity is included in this liveness fingerprint, so an opacity-only reveal (a staggered fade, simulated typing) counts as real motion — but only while it's still animating at the sampled moments. The classic trap: an entrance that completes early and then holds a static frame for the rest of the clip — every later sample lands on the settled state and the check fails. Spread the reveal across more of the timeline, or keep one small element continuously animating (a blinking cursor works well for a typing effect) rather than adding an arbitrary slow drift just to satisfy the checker.

**Escape hatches** — mark deliberate intent directly in the HTML with these attributes, then re-run:

- `data-layout-allow-overflow` — the overflow is an intentional entrance/exit travel path.
- `data-layout-allow-overlap` — deliberate text layering (e.g. a caption label sitting over a heading).
- `data-layout-allow-occlusion` — an element is deliberately meant to cover some text.
- `data-layout-ignore` — a purely decorative element that should never be audited at all.

**Additional opt-in checks** (off by default):

```bash
npx hyperframes check --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error;seek=.25,1"
npx hyperframes check --frame-check     # flags images/svg/video/canvas breaching the canvas edge
```

`--caption-zone` takes a fractional band (`x0/y0/x1/y1`, 0–1 fractions of the canvas, works for portrait too) plus optional severity and comma-separated seek fractions; flags any content whose center lands inside that band — useful for keeping key content out of a reserved caption safe-zone. `--frame-check` flags media elements breaching the canvas edge by more than roughly 120px or 6% of the smaller canvas dimension, whichever is larger.

**Fixing contrast errors:** thresholds are 4.5:1 for normal text, 3:1 for large text (24px+, or 19px+ bold). Each finding's suggested replacement color is already the nearest compliant color in the correct direction — apply it directly, or pick another color within the same palette family, then re-run `check`.

### Motion verification (the `*.motion.json` sidecar)

`check` can verify **motion intent**, not just static layout — the closest automated substitute for actually rendering the video and watching it. It catches bugs a layout sweep alone can't: an entrance reveal the sample grid happens to land past, a broken animation stagger order, an element drifting off-frame mid-animation, or a shot that's frozen the whole time.

Drop a `*.motion.json` file next to the composition (name it to match the HTML file's basename if a directory has several compositions). `check` picks it up automatically — no flag needed. With no sidecar present, `check` behaves exactly as it always did.

```json
{
  "duration": 6,
  "assertions": [
    { "kind": "appearsBy", "selector": "#headline", "bySec": 0.5 },
    { "kind": "before", "a": "#headline", "b": "#cta" },
    { "kind": "staysInFrame", "selector": ".card" },
    { "kind": "keepsMoving", "withinSelector": ".scene" }
  ]
}
```

| Assertion | Fails when |
|---|---|
| `appearsBy(selector, bySec)` | The element isn't visible (opacity ≥ 0.5) by the given timestamp. |
| `before(a, b)` | `a` does not first appear strictly before `b`. |
| `staysInFrame(selector)` | Once visible, its bounding box ever leaves the canvas. |
| `keepsMoving(withinSelector?)` | A fully static window exceeds `maxStaticSec` (default 2 seconds). |

`duration`, `withinSelector`, and `maxStaticSec` are all optional. These findings are errors by default and appear alongside the layout findings in both human and JSON output. A selector that matches nothing is reported explicitly as an error (rather than silently passing), so a typo in a selector fails loudly instead of quietly doing nothing.

### snapshot

```bash
npx hyperframes snapshot                       # 5 key frames as PNG
npx hyperframes snapshot ./my-project          # specific project
npx hyperframes snapshot --frames 10           # evenly-spaced N frames
```

Captures still PNGs from the composition for visual diffing, thumbnails, or attaching to a review. Much faster than rendering a full video when only a few hero frames are needed. Output lands in the project's snapshots directory.

**Zooming into a specific finding:**

```bash
npx hyperframes check --snapshots               # reports a finding, e.g. content_overlap on "#cta"
npx hyperframes snapshot --zoom "#cta"           # crop that element at 3x density to inspect it
npx hyperframes snapshot --zoom "100,50,400,300" --zoom-scale 2   # or an exact pixel region
# fix the composition HTML, then re-check:
npx hyperframes check
```

`--zoom` takes a CSS selector or an exact `x,y,w,h` pixel region and always produces a genuine high-density crop (never a resized/zoomed screenshot), so it never disturbs the composition's actual layout. A selector matching nothing is a loud error rather than a silent full-frame fallback; a frame where the target has no visible box (e.g., collapsed, or animated off-canvas at that moment) is skipped with a note instead of producing a meaningless sliver image.

### Deprecated: validate, inspect, layout

All three still run — they print a deprecation notice and mark the result as deprecated in JSON output — but all of their functionality now lives in `check` (same flags: `--samples`, `--at`, `--at-transitions`, `--tolerance`, `--strict`). Migrate any existing scripts to call `check` directly instead.

---

## Beats

Use `hyperframes beats` when an existing project needs a beat-grid file generated for its music track. This is a standalone CLI utility for one project, not a full music-driven video pipeline.

```bash
npx hyperframes beats
npx hyperframes beats ./my-video
npx hyperframes beats ./my-video --json
```

The project must contain a local music `<audio>` element. Mark it with `data-timeline-role="music"` (or give it an id/class containing `music`, `bgm`, or `soundtrack` — also recognized automatically). The command analyzes that audio file in a headless browser and writes a beat-grid JSON file into a `beats/` directory alongside the audio file.

If no beats are detected, the command fails and writes nothing. If the bundled browser isn't available, run:

```bash
npx hyperframes browser ensure
```

For building a complete beat-synced video from scratch (not just adding a beat grid to an already-scaffolded project), that's a separate, fuller pipeline — see the `music-to-video` route in the hyperframes companion document, which owns its own audio-driven analysis and a richer audio-map file. Don't try to replace that pipeline's analyzer with this standalone utility.

---

## Cloud (HeyGen-hosted rendering, zero infrastructure)

`hyperframes cloud render` renders a composition on a managed hosted cloud service. The CLI zips the project, uploads it, runs the render remotely (managed Chromium + FFmpeg), and downloads the finished video. Nothing to deploy or manage — billed per credit.

```bash
npx hyperframes auth login            # one-time sign-in
npx hyperframes cloud render          # zip, upload, render, download
```

### Choosing a render path

- **`hyperframes render`** (local): fastest iteration loop — use this while actively authoring.
- **`hyperframes cloud render`**: zero infrastructure. The hosted service runs the render and bills per credit. This is the default answer to "render in the cloud" when you don't want to manage a browser/FFmpeg/AWS yourself.
- **`hyperframes lambda render`**: bring-your-own-AWS distributed rendering with chunked parallelism. Only worth the setup when the user is already invested in AWS.
- **`hyperframes cloudrun render`**: bring-your-own-GCP distributed rendering. Use only when GCP ownership is explicitly required.

### Authentication

Cloud rendering needs a stored credential (kept locally with restricted file permissions).

```bash
npx hyperframes auth login              # opens a browser for OAuth sign-in
npx hyperframes auth login --api-key    # non-interactive: hidden prompt, or pipe a key in
npx hyperframes auth status             # active credential source, identity, billing snapshot
                                        #   exit 0 = signed in and verified; exit 1 = not signed in
                                        #   or credential rejected — a signed-out exit 1 is the normal
                                        #   offline state, not a command failure
npx hyperframes auth refresh            # force-refresh an OAuth token before a long job
npx hyperframes auth logout             # clear the stored credential
```

Credential resolution order (first match wins): an environment variable for the API key, then an alternate environment variable, then the locally stored credential file.

### The render pipeline

`cloud render` runs end-to-end:

1. **Resolve the project** — a local directory (default `.`), or skip upload entirely with `--asset-id` / `--url`.
2. **Auto-detect aspect ratio** from the entry HTML's declared width/height.
3. **Zip** the project (same exclusion rules as `hyperframes publish`, including anything listed in `.hyperframesignore`).
4. **Upload** the zip, yielding an asset id.
5. **Submit** the render job, yielding a render id.
6. **Poll** until it completes or fails (skip this with `--no-wait`).
7. **Download** the finished video.

### Archive size and `.hyperframesignore`

The direct-upload limit is 200 MB. Root-level `renders/` and `snapshots/` directories are automatically excluded, along with standard development directories/dotfiles (`.git`, `node_modules`, `dist`, `.next`, `coverage`, etc). Add project-specific gitignore-style rules to `<project>/.hyperframesignore` for other generated/intermediate assets not actually needed at render time. The same rules also affect `hyperframes publish`.

Inspect the exact archive without authenticating, uploading, spending credits, or starting a render:

```bash
npx hyperframes cloud render <project> --dry-run --json
```

Reports the compressed size, file count, the 200 MB limit, and the ten largest included files.

**When an upload reports a size-limit error, follow this procedure:**

1. Run the dry-run command and inspect the largest included files/directories.
2. Classify obvious generated output first: old renders, extra snapshot directories, caches, exported previews, and source media only used to produce other final assets.
3. Before excluding anything else, search every HTML/CSS/JS file, plus any manifest or variable-driven path, for references to the file in question (`src`, `href`, `url()`, sub-composition source attributes, etc.) — never exclude something still actually referenced.
4. Preserve any existing comments/rules in `.hyperframesignore`. Add only the narrowest verified-unneeded paths — prefer an exact file or directory over a broad wildcard.
5. Never exclude the entry HTML, the selected composition, any mounted sub-composition, fonts, images, audio, video, scripts, or manifests just because they're large. Never exclude an entire `assets/` directory wholesale.
6. Rerun the dry-run until the archive is under the limit, then run `npx hyperframes check` — note that `check` only sees the source directory, so it can't by itself prove a dynamically-computed asset path is still present in the filtered archive; the manual reference audit above is still required.

Example:

```gitignore
# Additional generated verification passes
/snapshots2/
/snapshots3/

# Master file used only to produce the final background clips
/assets/bg-pattern.mp4
```

Rules support comments, globs, and negation (a later rule can override an earlier default, e.g. `!/snapshots/` when that directory intentionally contains real render inputs).

### Render options

| Flag | Default | Meaning |
|---|---|---|
| `--fps` | `30` | Frames per second, 1–240. |
| `--quality` | `standard` | `draft`, `standard`, or `high`. |
| `--format` | `mp4` | `mp4`, `webm`, or `mov` (webm/mov carry alpha). |
| `--resolution` | `1080p` | `1080p` or `4k` (4k billed at 1.5×). |
| `--aspect-ratio` | auto | `16:9`, `9:16`, or `1:1`. Auto-detected from a local project's declared dimensions; defaults to `16:9` for `--asset-id`/`--url`. |
| `--composition` / `-c` | `index.html` | Entry HTML file inside the zip. |
| `--output` / `-o` | `renders/<render_id>.<ext>` | Local download destination. |
| `--dry-run` | off | Build and inspect a local project zip without authenticating, uploading, or rendering. |

```bash
npx hyperframes cloud render . \
  --composition compositions/intro.html \
  --output ./renders/intro.mp4

npx hyperframes cloud render --quality high --fps 60
```

`--resolution 4k` cannot combine with `--format webm`/`mov` — the 4K supersampling path has no alpha channel. Render 4K as mp4, or render alpha only at native resolution.

### Templates and variables (cloud)

Declare composition variables directly on the composition, then fill them at render time:

```bash
npx hyperframes cloud render --variables '{"title":"Q4 Recap","theme":"dark"}'
npx hyperframes cloud render --variables-file ./vars.json
npx hyperframes cloud render --variables '{"title":"Q4 Recap"}' --strict-variables
```

For a **local project**, `--variables` is validated against the declared schema *before* uploading. For `--asset-id`/`--url` renders, mismatches only surface once submitted, as an API-level error.

**Upload once, re-render many** is the idiomatic template loop: render a local project once to obtain its asset id, then re-submit against that same asset with new variable values (no re-zip, no re-upload needed):

```bash
npx hyperframes cloud render ./card-template                              # note the asset_id printed on upload
npx hyperframes cloud render --asset-id asst_abc123 --variables '{"name":"Ada"}'
npx hyperframes cloud render --asset-id asst_abc123 --variables '{"name":"Linus"}'
```

For high-volume personalized batches, use the JSONL fan-out support in the Lambda or Cloud Run sections below instead.

### Fire-and-forget and webhooks

By default the CLI blocks, polls, and downloads. Combine `--no-wait` (submit and exit immediately with just the render id) with `--callback-url` (an HTTPS webhook fired on completion) for true fire-and-forget behavior:

```bash
npx hyperframes cloud render --callback-url https://example.com/hf-hook --no-wait
#    Poll later with: hyperframes cloud get hfr_def456
```

| Flag | Meaning |
|---|---|
| `--no-wait` | Submit and exit immediately; prints the render id. |
| `--callback-url` | HTTPS webhook fired when the render terminates. |
| `--callback-id` | Opaque tracking id echoed back in webhook payloads. |
| `--poll-interval` | Poll cadence in seconds (default `10`). |
| `--max-wait` | Max poll duration in minutes (default `60`). |

### Managing renders

```bash
npx hyperframes cloud list                 # recent renders (--limit, --token, --all)
npx hyperframes cloud get hfr_def456       # full detail + a short-lived signed video URL
npx hyperframes cloud delete hfr_def456    # soft-delete (--no-confirm to skip the prompt)
```

The returned video/thumbnail URLs are short-lived signed URLs — re-fetch with `cloud get` rather than caching them for later use.

### Safe retries

A `401` is transparently retried once by refreshing the auth token. That's safe for reads, but the initial zip upload is **not idempotent** — a blind retry after a failure can create a duplicate asset and bill twice. Pass an idempotency key to make retries safe:

```bash
npx hyperframes cloud render . --idempotency-key "$(uuidgen)"
```

Any opaque string matching `[A-Za-z0-9_:.-]`, 1–255 characters, works — one value is safe to reuse across both the upload and submit steps.

---

## Cloud Run (self-managed rendering on Google Cloud)

Use `hyperframes cloudrun` only when the user explicitly wants self-managed Google Cloud infrastructure — it deploys Cloud Run services, Workflows, and Cloud Storage. For a fully managed default, use `hyperframes cloud` above; for self-managed AWS, use `hyperframes lambda` below.

### Prerequisites

- `gcloud` is authenticated and the target GCP project has billing enabled.
- Terraform 1.5+ is on the system PATH.
- Docker, or permission to use Cloud Build, is available.

### Lifecycle

```bash
npx hyperframes cloudrun deploy --project <gcp-project> --region us-central1
npx hyperframes cloudrun sites create ./project
npx hyperframes cloudrun render ./project --width 1920 --height 1080 --wait
npx hyperframes cloudrun progress <execution-name>
npx hyperframes cloudrun destroy --project <gcp-project>
```

`deploy` enables the required Google APIs, builds or accepts a container image, applies the bundled Terraform module, and stores the resulting infrastructure coordinates in a local state file. Use deploy flags like `--image`, `--repo`, `--cpu`, `--memory`, `--max-instances`, and `--timeout` only when infrastructure needs to be overridden from defaults.

`sites create` uploads a content-addressed project archive for reuse by `render-batch`; pass its `--site-id` result to that command to skip re-uploading. A single `cloudrun render` currently resolves the project directly from its directory and doesn't consume `--site-id`. Both render commands require `--width` and `--height`; supported output formats are `mp4`, `mov`, `png-sequence`, and `webm`. Use `--output-resolution 4k` to supersample an authored composition without changing its layout dimensions.

Common render flags: `--fps 24|30|60`, `--quality draft|standard|high`, `--codec h264|h265` (for MP4), `--chunk-size`, `--max-parallel-chunks`, `--target-chunk-frames`, `--render-id`, `--output-key`, `--wait`, `--wait-interval-ms`. Use `--json` for machine-readable output.

For a variable-driven single render:

```bash
npx hyperframes cloudrun render ./template \
  --width 1920 --height 1080 \
  --variables-file ./alice.json \
  --strict-variables \
  --wait
```

Use exactly one of `--variables` or `--variables-file`, never both.

### JSONL batches (Cloud Run)

```bash
npx hyperframes cloudrun render-batch ./template \
  --batch ./users.jsonl \
  --width 1920 --height 1080 \
  --max-concurrent 10 \
  --site-id <site-id> \
  --json
```

Each nonblank line must contain an `outputKey`; `variables` is optional:

```json
{ "outputKey": "renders/alice.mp4", "variables": { "name": "Alice" } }
```

- `--max-concurrent` defaults to `50` and limits in-flight executions. `--max-parallel-chunks` separately limits chunks inside one render.
- `--dry-run` parses the file and prints "would-start" rows without starting any actual executions.
- The template only uploads once, unless `--site-id` is supplied.
- Per-entry start errors remain visible and make the overall command exit non-zero.
- `--strict-variables` is currently accepted but NOT actually validated for `render-batch` rows — validate the JSONL variable objects against the composition's variable schema yourself before dispatching. The strict flag does work correctly for a single `cloudrun render`.

`render` without `--wait` returns an execution name — use `cloudrun progress <execution-name>` to poll it until it succeeds, then verify the reported output location. `destroy` removes the entire deployed stack and its scratch storage bucket — copy out anything that needs to survive first.

---

## Compare & Batch

Use these for deliberate visual comparison, or for variable-driven templated output. None of these replace `lint`, `check`, final preview approval, or verifying the actual output file.

### Compare projects or variants

Render the same timestamp from two or more project directories or HTML files into one labeled contact sheet:

```bash
npx hyperframes compare <path-a> <path-b> [<path-c> ...] \
  --at <seconds> \
  --labels baseline,candidate \
  --out compare.png \
  --cols 2
```

Options:

- `--at <seconds>` — the shared comparison timestamp.
- `--labels <a,b,...>` — label each cell, in input order.
- `--out <file>` — output sheet path.
- `--cols <n>` — grid column count.
- `--json` — machine-readable results.
- `--timeout <ms>` — per-variant render-ready timeout.

A single sheet accepts at most 16 variants — extra inputs are truncated with a warning; split larger comparisons into multiple runs.

`compare` is a visual review aid, not an automated quality gate — always actually inspect the generated image; command success alone doesn't mean the visuals are correct.

### Compare color grades

Generate labeled grade candidates from one source frame:

```bash
npx hyperframes grade-compare \
  --for frame.png \
  --grades grades.json \
  --project . \
  --out grade-compare.png
```

`grades.json` is an array of labeled grading definitions:

```json
[{ "label": "warm", "grading": { "temperature": 0.2, "contrast": 0.1 } }]
```

Or compare explicit LUT files directly:

```bash
npx hyperframes grade-compare \
  --for source.mp4 \
  --luts warm.cube,cool.cube \
  --out grade-compare.png
```

- `--for` accepts an image or a video (the first frame is extracted from video input).
- Supply exactly one candidate source: `--grades <json>` or `--luts <a.cube,b.cube>`.
- A neutral baseline is included by default; pass `--no-baseline` only when it isn't a useful reference.
- Up to 16 candidate grades (plus the default baseline, so up to 17 cells total). Extra candidates are truncated with a warning.
- `--timeout <ms>` — render-ready timeout for the comparison composition.
- `--json` for machine-readable output.

This command only helps *select* a grade — it doesn't apply the chosen grade back to the composition automatically.

### Batch template renders

`render --batch` accepts either a JSON array of variable objects, or an object with a `rows` array:

```json
{
  "rows": [
    { "name": "alpha", "headline": "Hello" },
    { "name": "beta", "headline": "Welcome" }
  ]
}
```

Declare the matching variables in the composition, then run:

```bash
npx hyperframes render \
  --batch rows.json \
  --output "renders/{name}.mp4" \
  --batch-concurrency 1 \
  --strict-variables
```

Batch rules:

- Don't combine `--batch` with `--variables` or `--variables-file` — each row supplies its own variable set for one render.
- If `--output` is omitted, the generated filename includes `{index}` so each row's output stays unique.
- Output path templates support `{index}` and any row key containing letters, numbers, `_`, `.`, or `-`. A placeholder value must be a string, number, or boolean — `null`, objects, and arrays are invalid. Missing placeholders or output-path collisions are errors.
- `--batch-concurrency` defaults to `1` — raise it conservatively, since each render already uses multiple internal workers.
- `--batch-fail-fast` stops scheduling further rows after the first failure. Without it, other independent rows keep running and failures remain visible afterward.
- `--strict-variables` validates every row before any rendering starts, and aborts entirely if the declared variable contract is violated anywhere.
- `--json` emits progress events suitable for scripted/automated monitoring.

The command writes a `manifest.json` file into the common output directory, updated throughout the run, recording each row's variables, status, output path, error (if any), and timing. A batch is only truly complete when the manifest shows no failed rows and every completed output file actually exists, is non-empty, and has a plausible duration.

---

## Doctor & Browser

Environment diagnosis and bundled-browser management. Run these first whenever a render or preview fails unexpectedly.

### doctor

```bash
npx hyperframes doctor
npx hyperframes doctor --json     # scripted output (always exits 0 — gate on the JSON payload's `ok` field)
```

Runs independent checks and reports each as ok/warn/fail:

- **Version** — installed CLI vs. latest available (suggests an upgrade if stale).
- **Node.js** — version 22+ required.
- **CPU**, **Memory**, **Disk** — host resource checks.
- **Environment** — environment variables that affect rendering.
- **FFmpeg** / **FFprobe** — presence, version, available codecs.
- **Chrome** — bundled or system browser, version, path.
- **Docker** / **Docker running** — only required for `render --docker`.
- **/dev/shm** — checked only inside containers.

Run `doctor` first whenever:

- `render` fails with a browser or FFmpeg error.
- `preview` opens but the composition fails to load.
- A fresh machine has never run the HyperFrames CLI before.

Common issues and fixes:

- **Missing FFmpeg** — install it via your system package manager (e.g. `brew install ffmpeg` on macOS).
- **Missing bundled browser** — run `npx hyperframes browser ensure`.
- **Low memory** — close other browser instances, reduce `--workers`, or use `--quality draft`.
- **Chrome fails to launch inside a sandboxed automation environment** — some sandboxed execution environments block the browser's low-level startup mechanism outright, so every browser (bundled or system) fails to launch at all. This is a host-level restriction, not a bug in the composition or the CLI — the code and audio checks still pass; only actual rendering is unavailable. In that situation, state the limitation clearly and deliver the checked-but-unrendered composition; rendering then needs to happen outside the sandbox, via `render --docker`, or via one of the cloud render paths. Do not try to build a substitute image-rendering pipeline as a workaround — on a genuinely blocked-browser host, the deliverable is the verified composition plus a clear note about the blocker, with actual rendering handed off to Docker, cloud, or the end user.

### browser

```bash
npx hyperframes browser ensure    # find or download the pinned browser build
npx hyperframes browser path      # print the browser executable path (for scripting)
npx hyperframes browser clear     # remove the cached browser download
```

Manages the specific browser build HyperFrames uses for rendering. A pinned version is used deliberately, because rendered pixel output can drift across different browser versions — using the same pinned build keeps output reproducible across machines. Use `browser path` to embed the binary path directly into other scripts.

---

## Lambda (self-managed rendering on AWS)

Use `hyperframes lambda` when the user explicitly wants self-managed AWS infrastructure, or needs distributed rendering at scale.

### Choosing Lambda vs. local rendering

- **Local `render`** — best for dev-loop iteration on a single machine, anything under a few minutes at 1080p.
- **`lambda render`** — best for long videos, 4K output, large parallel batches, or anything where a local browser would time out or run out of memory. Pay only per invocation, no idle cost.

For one-off short renders, the deployment overhead of Lambda usually isn't worth it.

### Prerequisites

- AWS credentials configured (environment variables, credentials file, SSO, or instance role).
- AWS SAM CLI on the system PATH.
- `bun` on the system PATH (used to build the Lambda handler package).

### Deploy

```bash
npx hyperframes lambda deploy \
  --stack-name=hyperframes-prod \
  --region=us-east-1 \
  --concurrency=8 \
  --memory=10240
```

Builds the Lambda handler package and deploys the full stack (Lambda + Step Functions + S3 + IAM) via SAM. Idempotent — re-running with the same stack name is a no-op if nothing changed. Writes a local state file so later commands don't need to re-query AWS for stack details.

| Flag | Default | Description |
|---|---|---|
| `--stack-name` | `hyperframes-default` | CloudFormation stack name |
| `--region` | env var or `us-east-1` | AWS region |
| `--profile` | env var | Named AWS credentials profile |
| `--concurrency` | `8` | Lambda reserved concurrency |
| `--chrome-source` | `sparticuz` | `sparticuz` or `chrome-headless-shell` |
| `--memory` | `10240` | Lambda memory in MB |
| `--skip-build` | off | Reuse an existing built handler package |

### Upload a reusable site

```bash
npx hyperframes lambda sites create ./my-project
# → siteId: abc1234deadbeef0  (stable across re-runs of the same project tree)

npx hyperframes lambda render ./my-project --site-id=abc1234deadbeef0 ...
```

Uploads the project directory to S3 with a content-addressed key, returning a stable site id you can reuse — re-rendering the same tree later skips the upload step entirely.

### Render one composition

```bash
npx hyperframes lambda render ./my-project \
  --width 1920 --height 1080 --fps 30 --format mp4 \
  --chunk-size 240 --max-parallel-chunks 16 \
  --wait
```

Starts a distributed execution. Returns immediately with a render id unless `--wait` is set, in which case it blocks until completion and streams per-chunk progress. Add `--json` for machine-parseable output.

| Flag | Description |
|---|---|
| `--width` / `--height` | Output dimensions in pixels |
| `--output-resolution` | Supersampling preset — `landscape` / `landscape-4k` / `portrait` / `portrait-4k` / `square` / `square-4k` (+ aliases `1080p`, `4k`, `uhd`, `hd`, `1080p-portrait`, `4k-portrait`, `1080p-square`, `4k-square`). Use this to render an authored-at-1080p composition at 4K without re-laying it out — see the footgun note below. |
| `--fps` | `24` / `30` / `60` |
| `--format` | `mp4` / `mov` / `png-sequence` / `webm` (default `mp4`) |
| `--codec` | `h264` / `h265` (mp4 only) |
| `--quality` | `draft` / `standard` / `high` |
| `--chunk-size` | Frames per chunk (default `240`) |
| `--max-parallel-chunks` | Max concurrent chunks (default `16`) |
| `--target-chunk-frames` | Cap frames per chunk, letting the planner add chunks up to the parallel limit |
| `--site-id` | Reuse an existing uploaded site (skip re-upload) |
| `--execution-name` | Explicit execution name |
| `--output-key` | Explicit final storage key for the output |
| `--variables` | Inline JSON object of composition variable values |
| `--variables-file` | JSON file containing one composition variable object |
| `--strict-variables` | Fail when supplied variables are undeclared or the wrong type |
| `--wait` | Block until completion, stream progress |
| `--wait-interval-ms` | Poll cadence while waiting (default `5000`) |
| `--json` | Machine-parseable progress snapshot |

**`--width`/`--height` footgun:** setting `--width 3840 --height 2160` against a composition authored at 1920×1080 silently still produces a 1080p output — the browser lays the page out at the composition's own authored dimensions, and these CLI flags don't override that layout. To genuinely output at 4K, use `--output-resolution 4k` instead (this supersamples via the browser's device-scale factor). The CLI prints a warning when the CLI dimensions disagree with the composition's authored dimensions and `--output-resolution` isn't set.

For variable-driven templates, declare the schema in the composition and pass either `--variables` or `--variables-file` — never both. `--strict-variables` checks local input before any render actually starts.

### Render a JSONL batch (Lambda)

Upload one template once and start one execution per nonblank JSONL line:

```bash
npx hyperframes lambda render-batch ./template \
  --batch ./users.jsonl \
  --width 1920 --height 1080 \
  --max-concurrent 10 \
  --strict-variables \
  --json
```

Each line must be an object with a non-empty `outputKey`. Choose unique keys so outputs don't overwrite each other. `variables` and `executionName` are optional:

```json
{
  "outputKey": "renders/alice.mp4",
  "variables": { "name": "Alice" },
  "executionName": "alice-video"
}
```

Batch rules:

- The project uploads once, unless `--site-id` reuses an earlier upload.
- `--max-concurrent` defaults to `50` and limits in-flight render executions; `--max-parallel-chunks` separately limits chunks inside each individual render.
- `--strict-variables` checks every entry, reports all issues found, and aborts before any AWS calls are made.
- `--dry-run` performs no upload and no actual render call — every manifest row is marked as "would-invoke."
- The emitted manifest preserves input order and records the input line, output key, execution ARN, and status (`started`, `would-invoke`, or `failed-to-start`), plus an error message when applicable.
- A per-entry start failure doesn't hide the other rows. In JSON mode the command may print the manifest and exit zero even with failures present — always gate on each row's individual status, not just the overall process exit code. A successful dispatch is not the same as a completed render — check each execution's progress separately.

### Inspect progress

```bash
npx hyperframes lambda progress hf-render-abcd1234
npx hyperframes lambda progress arn:aws:states:us-east-1:...:execution:...
```

Prints one snapshot: overall percent complete, frames rendered, invocation count, accrued cost, and any errors. Accepts either a bare render id or a full execution ARN.

### Destroy the stack

```bash
npx hyperframes lambda destroy
```

Removes the deployed stack and the local state file. **The render output S3 bucket is configured to be retained** and survives stack destruction — empty and delete it manually via the AWS console/CLI if the storage itself needs to be reclaimed.

### Non-retryable errors

A subset of failures short-circuits immediately instead of exhausting the normal retry budget — `progress` surfaces these with an explicit error class name; don't blindly re-issue `lambda render` on seeing one:

- **Chrome-binary-unavailable error** — the packaged Chrome binary path came back empty/missing. Usually means a prior chunk hit a sandbox timeout mid-extraction and the warm execution environment is now wedged until it's recycled. Fix by bumping a Lambda environment variable to force a fresh environment, or by redeploying. This is not a transient failure — blind retries will just burn budget against the same wedged instance.
- **Version-mismatch errors** (encoder version mismatch, plan-hash mismatch) — indicates version drift between the planning and execution components. Redeploy to resolve.

### IAM policies

Print or validate the minimum IAM permissions the CLI needs:

```bash
npx hyperframes lambda policies user                                  # inline policy for an IAM user
npx hyperframes lambda policies role                                  # trust relationship + inline policy
npx hyperframes lambda policies validate ./infra/iam/hf-deploy.json   # CI/automation gate
```

`validate` reads a JSON policy document, expands any wildcards, and checks the union of allowed actions against the CLI's required action set — missing actions print to stderr and the command exits non-zero. Wire this into an automated pipeline to catch policy drift before it breaks a deploy.

The default action set is deliberately broad (unrestricted resource scope) because AWS's own infrastructure-provisioning process creates new resource identifiers on every first deploy. Tighten resource scope after the first successful run if your security posture requires it.

### State, cost, and cleanup

Per-stack metadata (bucket name, state-machine ARN, region) is stored in a local state file — not secret, but it does identify your AWS account, so handle it accordingly in version control.

- `lambda destroy` removes the deployed stack but **leaves the S3 bucket in place** — delete it manually if you want the storage reclaimed.
- Billing is per-invocation plus duration; `progress` reports the accrued cost.
- `--concurrency` caps parallel Lambda invocations — keep it aligned with your account's actual service quota.
- `--chunk-size` and `--max-parallel-chunks` trade off per-chunk overhead against parallelism: larger chunks reduce coordination overhead, smaller chunks parallelize more aggressively.

---

## Upgrade, Info & Misc

### info

```bash
npx hyperframes info                   # project metadata
npx hyperframes info ./my-video        # specific project
npx hyperframes info --json
```

Prints project-level metadata: name, resolution, duration, element counts by type, track count, and total project size. This is project-level, not environment-level — use `doctor` for environment health.

### upgrade

```bash
npx hyperframes upgrade                # check + interactive prompt
npx hyperframes upgrade --check        # check and exit, no prompt (scripting-friendly)
npx hyperframes upgrade --check --json # machine-readable: current / latest / updateAvailable
npx hyperframes upgrade --yes          # print the upgrade commands without prompting
```

Compares the installed CLI version against the latest available release.

`--project [dir]` bumps a **specific project's** pinned script references (rather than the global CLI install) — it rewrites every pinned `hyperframes@<version>` reference in that project's `package.json` (default: current directory) to the latest version. Always invoke this itself unpinned (`npx hyperframes@latest upgrade --project`), since a project scaffolded on an old CLI version would otherwise stay frozen forever. `--project . --check` reports what would change without writing anything; add `--json` for a structured `{ changed, from, to, path }` result. Always pass the target directory explicitly whenever another flag follows `--project` — on older CLI releases, a bare `--project` will consume the next flag as its directory argument by mistake.

### compositions, docs

```bash
npx hyperframes compositions           # list compositions in the project
npx hyperframes compositions --json
npx hyperframes docs                   # list available documentation topics
npx hyperframes docs rendering         # print one topic inline in the terminal
```

`compositions` lists every distinct composition in the project (including sub-compositions) with its duration, resolution, and element count.

`docs` prints inline documentation directly in the terminal — it does not open a browser. Available topics: `data-attributes`, `examples`, `rendering`, `gsap`, `troubleshooting`, `compositions`. Run with no topic argument to see the full list.

### benchmark

```bash
npx hyperframes benchmark              # run the preset matrix in the current project
npx hyperframes benchmark ./my-video   # specific project
npx hyperframes benchmark --runs 5     # repeat each configuration N times (default 3)
npx hyperframes benchmark --json
```

Renders the project under 5 preset configurations (varying fps, quality, and worker count) and prints a comparison of render speed and output file size. Use this to find the fastest acceptable settings for a given machine. This runs a full comparison matrix, not a single render with a stage-by-stage timing breakdown.

### telemetry

```bash
npx hyperframes telemetry status      # show current telemetry state
npx hyperframes telemetry disable     # disable anonymous usage telemetry
npx hyperframes telemetry enable      # re-enable telemetry
```

Telemetry, where present, is anonymous usage counters only.

### Asset preprocessing

```bash
npx hyperframes tts
npx hyperframes transcribe
npx hyperframes remove-background
```

These produce assets — narration audio, word-level transcripts, transparent-background video — meant to be dropped directly into a composition. Each may need to download its own processing model on first run. For guidance on voice selection, transcription model choice, output format, and chaining TTS → transcript → captions together, treat this as a separate, more specialized concern from the core dev loop described above.

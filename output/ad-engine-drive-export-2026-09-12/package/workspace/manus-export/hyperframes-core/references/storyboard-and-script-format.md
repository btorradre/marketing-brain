# `STORYBOARD.md` and `SCRIPT.md` — the plan layer

## `STORYBOARD.md` — the plan layer

A storyboard is the plan layer for a video — an ordered set of frames (key moments) in one markdown file. A contact-sheet-style board view (if the tooling supports one) renders it visually.

### Frontmatter (global direction)

| Key | Meaning | Example |
|---|---|---|
| `format` | Canvas size | `1920x1080` |
| `duration` | The brief's rough length expectation (advisory, not a hard limit) | `22s` |
| `message` | One-line thesis | `Ship a launch video in an afternoon` |
| `arc` | Narrative arc | `Hook → Problem → Solution → Proof → CTA` |
| `audience` | Who it's for | `indie devs on X` |
| `mode` | Interaction mode (collaborative/autonomous — see `brief-format.md`; default collaborative) | `autonomous` |

Set `duration` from the brief's `length` when the storyboard is first written. It's an expectation, not a hard gate — assembly reports where the cut actually lands against it and flags a large gap; judge whether the drift serves the piece, and update the value if the intended length genuinely changes.

### Per-frame sections

One `## Frame N — Title` heading per frame (`Frame` / `Beat` / `Scene` all work as the heading word). Metadata as `- key: value` bullets; everything below the bullets until the next heading is the free-form narrative.

| Key | Meaning |
|---|---|
| `status` | `outline` → `built` → `animated` (defaults to `outline`) |
| `src` | project-relative path to the frame's HTML sub-composition (a tile poster, if rendered, comes from it) |
| `duration` | e.g. `4s` |
| `transition_in` | `crossfade` / `cut` / `wipe` … (alias `transition`) |
| `scene` | one-line contact-sheet caption (aliases `description` / `summary` / `caption`) |
| `voiceover` | the frame's narration guide (aliases `vo` / `voice_over` / `narration`) |
| `poster` | seconds to seek for a tile poster image (past the intro animation) |
| *any other key* | kept verbatim as workflow-specific per-frame data (effects, assets, …) |

The status ladder means: `outline` — a frame with no built file yet, renders as a placeholder; `built` — the middle rung, the frame's HTML file exists and its layout is confirmed (a wireframe sketch or better), motion not yet added; `animated` — fully built, motion included. Multi-line narration/voiceover values collapse to one line on save.

### Example

```markdown
---
format: 1920x1080
message: "Ship a launch video in an afternoon"
arc: Hook → Problem → Solution → Proof → CTA
audience: indie devs on X
---

## Frame 1 — Hook

- scene: Big type punches in on the beat
- duration: 3s
- poster: 2s
- transition_in: cut
- status: animated
- voiceover: "Ship a launch video in an afternoon."
- src: compositions/frames/01-hook.html

Open cold on the promise. This is the thesis — everything after pays it off.

## Frame 2 — The problem

- scene: A 20-minute timer spins on a stack of rejected takes
- duration: 4s
- transition_in: crossfade
- status: built
- voiceover: "The old way? Prompt, wait twenty minutes, get something that misses."
- src: compositions/frames/02-problem.html

The old way: prompt, wait, get something that misses. Establish the pain we remove.
```

### Frame comments — a structured feedback channel

If a review surface writes structured comments (e.g. to a sidecar JSON file), the shape is:

```json
{
  "version": 1,
  "pass": "sketch",
  "submitted_at": "2026-07-09T12:04:00Z",
  "comments": [
    {
      "frame": 3,
      "src": "compositions/frames/03-mechanism.html",
      "title": "Mechanism",
      "text": "Swap the bar chart for a before/after slider."
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `pass` | which review round the batch belongs to: `storyboard` (the text-layer review), `sketch` (the static-frame review), `final` (the assembled video) |
| `comments[].frame` | the frame's 1-based index in the storyboard — the key to look up |
| `comments[].src` / `title` | copied from the frame at submit time, so if frames get reordered after submission, a mismatch shows the drift |
| `comments[].text` | the feedback, verbatim |

The whole lifecycle: a workflow finding this file at a checkpoint should treat it as the revision feedback — revise exactly the frames it names, delete the file, and re-present the affected frames. It's created only on submit and never lingers across review rounds. If a review submission arrives through an asynchronous channel that doesn't itself notify anyone (e.g. someone filled out comments on a shared board), whoever is running the review should ask the requester to reply directly (even just "done") once they've submitted, so the comments actually get picked up and processed.

## `SCRIPT.md` — locked narration (optional)

The **locked narration** for a project: the final spoken lines plus voice and delivery notes. This is optional — a video with no narration (BGM-only, silent overlay) has none. The storyboard's per-frame `voiceover` field is the lighter, editable *guide*; `SCRIPT.md` is the *commit*.

Free-form markdown, not strictly parsed — a review surface can render it read-only, and a text-to-speech step should extract the indented spoken lines specifically.

### Shape

A header block, then one section per spoken line.

| Part | Holds |
|---|---|
| Header | Voice (provider + voice name), voice settings (e.g. stability/similarity/style), overall voice direction |
| `## Line N — <label> (Frame N)` | One spoken line, tied to its storyboard frame |
| `**Time:**` | The board's rough window — a guide, not authoritative (real timing comes from actual generated-audio word timestamps) |
| `**Delivery:**` | Per-line delivery note |
| Indented block | The actual spoken text — the only part that should be fed to a text-to-speech engine |

### Example

```markdown
# SCRIPT — acme-launch

**Voice:** Rachel (ElevenLabs)
**Voice settings:** stability 0.35 · similarity 0.75 · style 0.20
**Voice direction:** Confident, warm, a little playful.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 3.0s
**Delivery:** Land the promise on the beat.

    Ship a launch video in an afternoon.

## Line 2 — The problem (Frame 2)

**Time:** 3.0 – 7.0s
**Delivery:** Wry, a touch tired.

    The old way? Prompt, wait twenty minutes, get something that misses.
```

Feed each line's spoken text to whatever text-to-speech provider is available. Real per-word timing from that generation step should replace the `**Time:**` guide values once available.

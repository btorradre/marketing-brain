# The brief: capturing and locking intent, and `BRIEF.md`

Before building, confirm the run's shape and the video's core facts, and write the confirmed result to `BRIEF.md` at the project root, as the very first file created for the project. Every later step reads this file instead of re-asking the same questions — it is the project's "no-repeat" record of what was already confirmed.

A HyperFrames project's files read as four layers: **`BRIEF.md`** (why, for whom, and everything that was asked for) → **`STORYBOARD.md`** (what, frame by frame) → optionally a design/style-spec file (the look — palette, type ramp, components) → **`compositions/`** (the thing itself, the actual HTML). An optional **`SCRIPT.md`** sits alongside the storyboard as the locked narration when the video is voiced (see `storyboard-and-script-format.md`).

## Run shape

Three independent concerns describe how a run should behave — don't conflate them:

| Term | Values | Meaning |
|---|---|---|
| `flow` | `automation` or `companion` | Who drives execution — a fully automated pipeline, or an interactive collaborative build. |
| `storyboard` | `yes` or `no` | Whether a live/shared board is used for plan and layout review before building. |
| `mode` | `collaborative` or `autonomous` | Derived from the two above — governs how later preference and checkpoint questions behave. |

Derive `mode` from the confirmed run shape:

| `flow` | `storyboard` | Derived `mode` |
|---|---|---|
| `companion` | either | `collaborative` |
| `automation` | `yes` | `collaborative` |
| `automation` | `no` | `autonomous` |

Default to `collaborative` only when there isn't enough information to derive a mode (e.g. resuming an old project with incomplete state).

An ongoing signal such as "surprise me," "decide for me," "just build it," or "stop asking" sets `flow: automation`, `storyboard: no`, and therefore `mode: autonomous` whenever it appears during intent capture. A bare "go" or "looks good" at a checkpoint accepts only that checkpoint's displayed recommendation — it does not change the overall mode. Once a storyboard file exists, persist the derived mode in its own metadata; on resume, an explicit mode value there overrides the derivation, since it may represent a later user change. A mid-run "stop asking, finish it" changes only checkpoint behavior going forward — set mode to autonomous in the storyboard file if it exists, but don't rewrite the already-confirmed `flow`/`storyboard` fields. Only an explicit signal such as "let's review together" resumes collaborative checkpoints; ordinary feedback does not change mode.

## Gate behavior — how each kind of question behaves under each mode

| Gate | Collaborative | Autonomous |
|---|---|---|
| Preference (preset, voice, caption identity) | Ask when required. | Decide and state the choice with a one-line reason. |
| Checkpoint (plan, sketches, pre-render review) | Ask and wait. | Post the same summary, then continue. |
| Quality (completeness of fetched material, lint, structural checks, workflow-specific verification) | Run and stop on errors. | Run and stop on errors — quality gates are never relaxed by mode. |
| Routing ambiguity | Resolve explicitly — a wrong route changes the deliverable. | Same requirement. |
| A needed credential/sign-in is unavailable | Show status and wait for sign-in or an explicit offline choice. | Show status and continue through an available offline option if one exists. |

Autonomous mode never silently drops a required capability — if there's no available way to do something the plan needs, surface the blocker instead of quietly omitting it. A credential problem never relaxes a quality gate.

Rendering stays user-gated in both modes. After checks pass, a collaborative run asks "render now, or what changes?" An autonomous run asks the one kept question, "preview first, or render?" Render only happens after an explicit yes.

Autonomous mode is not silent — it replaces absorbed questions with visible decisions and short reasons, always names the final preview or rendered artifact, reports the actual duration for a time-based deliverable, and includes a contact sheet / snapshot sheet with frame identifiers where available, so the person still gets a review surface even though intermediate checkpoints didn't pause.

## Shared field registry

Ask only the fields actually used by the current build; values that were inferred or derived by policy get stated in the brief, not asked as questions:

| Field | Meaning | Policy |
|---|---|---|
| `flow` | who drives execution | Ask at the end of intent capture, when both flows are actually supported. An autonomous signal answers it directly. |
| `storyboard` | whether to review on a live board | Ask before `flow`. A direct storyboard request answers it. |
| `destination` | where the video will play | Infer from the request. Ask only when unknown and the answer would change aspect ratio, type scale, or composition. |
| `aspect` | canvas size | Derive from destination: social feed → `1080x1080`; TikTok/Reels/Shorts → `1080x1920`; YouTube/website/desktop → `1920x1080`. State the derivation out loud. |
| `length` | target duration | Recommend a range supported by the material, with the reason. |
| `language` | narration and caption language | Use the requester's own language and state it. |
| `audience` | who will watch | Infer when clear. Ask only when a different answer changes the story or terminology. |
| `message` | the one thing the video must communicate | Derive and echo it in one sentence. Do not move to storyboarding until this is clear. |
| `angle` | route/story shape | Recommend one option with a reason. |
| `narration` | `yes` / `minimal` / `no`, plus any route-specific modes | Follow the selected route's own defaults. |

## Remembered defaults

If the environment supports it, check previously confirmed preferences (e.g. a personal defaults store keyed by project) before asking a familiar question again — a remembered value becomes the recommended answer and its source gets named ("last time you picked 1080x1920 for TikTok"). A remembered value never overrides the current request and never skips a question that's actually required this time. Only record a value the requester *explicitly confirmed*, never a value that was merely inferred or defaulted — confirmation happens after the brief is written. The first time a project records a preference, say one short line that it will be remembered for future runs; don't re-record a value merely because an autonomous build happened to reuse it — only an explicit confirmation in the current run creates a new memory event.

Only a specific preference-backed subset of fields is appropriate to persist as a cross-project default if a memory mechanism is available: `destination`, `aspect`, `language`, `flow`, `storyboard`, `voice`, `style_preset`. A style preset should be recorded per-workflow (a look confirmed for one genre of video is not automatically a default for a different genre). `message`, `audience`, `length`, and `angle` describe *this* video and belong only in the brief's frontmatter, never promoted to a general default.

## Question protocol — the discipline for asking

1. Ask only unanswered fields that materially affect the output.
2. Ask one field per message and wait for its answer before asking the next.
3. Put the recommended option first with a short reason. A numbered choice list is fine for factual fields (destination, length, language) where it scaffolds recall — but a creative field the request hasn't already shaped (message, angle, tone) needs an open, anchored question; a list there steers the answer instead of collecting it.
4. Skip a question when the current request already answers it. Inference alone is not the same as an answer — don't silently assume.
5. Ask `storyboard` and then `flow` last, only for routes that support them.
6. Announce any deferred questions before handing off to the build — don't surprise the requester later.
7. When an autonomous signal appears, ask no more preference or checkpoint questions — state the completed brief and the reasons for the decisions made, then build.
8. Send one plain question with, at most, one numbered option list at a time — never place several different fields in the same list.
9. Before the final hand-off summary, run one integration check: look for a consequence the combined answers create together that no single answer showed on its own, and surface it with a proposed adjustment.
10. The hand-off summary separates fields the requester explicitly stated from fields that were inferred or defaulted, with the reasoning shown for both.
11. Revision is not confirmation — after any correction to the summary, present the updated summary again and get confirmation before executing.

At a checkpoint, "go" accepts only that checkpoint's displayed recommendation. If a message explicitly presents a complete brief and states that "go" will accept every displayed default, "go" may then confirm the whole displayed brief — don't assume that broader acceptance without that sentence being present.

## `BRIEF.md` — the intent document

`BRIEF.md` sits at the project root. It has a YAML frontmatter block with one key per confirmed field — run-shape fields first (`workflow`, `flow`, `storyboard`), then the registry fields above that the build actually used (`message`, `destination`, `aspect`, `language`, `audience`, `length`, `angle`, …). Store canonical, normalized values (e.g. a normalized aspect string, not a loose description), but preserve the requester's own wording in the body text where it matters.

**Body — four optional sections, write only what was actually learned:**

- `## Intent` — a short paragraph: what the video is, for whom, why now; tone and feel in the requester's own words.
- `## Assets` — the requester's own material, one line each: `path — what it is, where it belongs`. Anything named here should be treated as staged, never re-discovered from elsewhere.
- `## Customizations` — any special capability or bespoke ask ("count-up on the revenue stat," "capture the pricing page too"), each with enough detail to act on directly.
- `## Notes` — anything true that fits no field: constraints, references, things to avoid.

The body prose is project-local — nothing in it should be promoted to cross-project memory (only the frontmatter's preference-backed subset is memory).

## Lifecycle

Created once, as the very first action on a fresh project — never before. A workflow that finds an existing `BRIEF.md` should read it and ask no brief question again. If a project exists (other project files/folders present) but `BRIEF.md` doesn't, treat it as a pre-brief project: resume from whatever the storyboard file and any recorded preferences already say, optionally backfilling `BRIEF.md` from what they already contain — never re-interrogate a half-built project from scratch. `BRIEF.md` stays the run's ongoing truth: a mid-run decision (e.g. "make it 9:16 after all") should rewrite the relevant field directly and re-record any persisted preference — a changed mind is itself a confirmed answer. An accepted capability, adopted material, or bespoke ask lands as one new line in the matching body section. Resume reads this file, so writing back to it is what makes an interrupted project resumable — a decision that only lives in conversation is a decision that resume will never see. `message` and `audience` live here first — a storyboard file may keep its own copies for its own rendering purposes, but when the two disagree, `BRIEF.md` holds what was actually confirmed.

## Example

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Compound interest is a snowball, not a ladder"
destination: x-feed
aspect: 1080x1080
language: en
length: 60s
angle: concept
---

## Intent

Teach retail investors why starting early beats contributing more. Confident,
a little playful — closer to a bar-napkin sketch than a lecture.

## Assets

- public/growth-curve.png — the real 30-year S&P chart; the proof beat builds on it.

## Customizations

- Count-up on the final dollar figure.

## Notes

- No stock-photo aesthetics; keep it typographic.
```

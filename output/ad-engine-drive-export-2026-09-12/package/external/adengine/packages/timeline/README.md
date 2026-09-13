# @adengine/timeline

The editor's document. A timeline is a versioned, event-sourced JSON `Project`; every UI gesture and every agent tool call is one typed `Op` appended to the same log and folded by one pure reducer. Undo, history, diff, blame, and the CapCut-parity feature map (PRODUCTIZATION-PLAN section 8) all hang off this package. No framework dependencies; TypeScript strict; vitest.

```
pnpm install --store-dir ./.pnpm-store   # global store is unreliable on this machine
pnpm test                                # vitest (110 tests)
pnpm build                               # tsc -> dist/, then emits schema/project.schema.json
```

Files:

| file | what |
|---|---|
| `src/types.ts` | `Project`, `Track`, `Clip`, `CaptionTrack`, `Marker`, `AssetRef`, ... |
| `src/ops.ts` | the 48-op discriminated union `Op`, `OP_TYPES` |
| `src/reducer.ts` | `apply(project, op)`; validation; overlap policies; derived duration |
| `src/invert.ts` | `invert(op, before)` for every op |
| `src/log.ts` | `EventLog`, `append`, `replay`, `versionAt`, per-author `undo`/`redo` |
| `src/assemble.ts` | `assembleFromBoard(board, vo, options)` - storyboard + VO alignment -> one batch op |
| `src/captions.ts` | word chunker shared by `alignCaptions` and assembly |
| `src/schema.ts` | JSON Schema for `Project` + `validateProject` (schema + semantic invariants) |
| `src/model.ts`, `src/time.ts`, `src/ids.ts`, `src/errors.ts` | helpers, tick math, ids, `OpError` |
| `schema/project.schema.json` | emitted by `pnpm build`; Python validates the same document with it |

## Tick rate

All times are integers at **6000 ticks per second** (`TICK_RATE`). Floats never enter the document.

Why 6000 and not 1000: a frame must be a whole number of ticks or preview and export disagree by rounding. 6000 is the smallest rate that is exact for every frame rate an ad ships at (24, 25, 30, 48, 50, 60, 120, 240 fps: 250/240/200/125/120/100/50/25 ticks per frame) *and* exact for milliseconds (1 ms = 6 ticks), so word alignments (ms or seconds) and frame indices both convert without drift. NTSC fractional rates (29.97, 23.976) are not exact; they round per frame (`isFrameExact(fps)` says so) and are not a target for social video. CapCut drafts use microseconds; the importer rounds µs to ticks (0.17 ms worst case, sub-frame).

Conventions:

- `Clip.start`, `Clip.duration`, `Caption.start`, `Marker.at`: absolute timeline ticks.
- `Clip.in` / `Clip.out` / `Clip.freeze`: source ticks in the asset's own time. Media clips play `[in, out)` at `speed` (backwards when `reverse`). Non-media clips (image/text/shape) keep `in = 0, out = duration` by convention, enforced.
- `Keyframe.at` and `CaptionWord.start`: relative to the owning clip / caption start, so moving a clip never rewrites its keyframes.
- `Project.duration` is derived (max clip end) and rewritten by the reducer after every op; `validateProject` rejects a stale value.
- `Project.version` increments by exactly one per top-level op (a `batch` counts once).
- `tracks[0]` is the bottom compositing layer. Clips on a track are always sorted by `start` and never overlap.
- `Project.captions` (word-level `CaptionTrack`s) is the canonical home for captions. The `caption` track/clip kinds exist only for imported, already-rasterized caption clips.

Helpers: `secondsToTicks`, `msToTicks`, `framesToTicks`, `ticksToFrame`, `snapToFrame`, `toTimecode`.

## Ops

Every op carries `{ id, at (ISO), author: { kind: 'human' | 'agent', id }, undoes?, note? }`. Tick-valued fields on ops are named `tick`, never `at`.

Errors are `OpError` with a `code`: `NOT_FOUND`, `DUPLICATE_ID`, `OVERLAP`, `INVALID_RANGE`, `SOURCE_BOUNDS`, `LOCKED`, `INVALID_OP`, `NOT_ADJACENT`, `KIND_MISMATCH`, `REFERENCED`, `UNJOINABLE`, `UNDO_CONFLICT`, `INVALID_DOCUMENT`. A throwing op changes nothing; `apply` is pure, so a failed `batch` is atomic for free.

### Overlap policy (CapCut semantics)

Clips on one track never overlap. Placing a clip (`addClip`, `moveClip`) takes `overlap`:

- `reject` (default): throw `OVERLAP`. This is CapCut's overlay-track behavior (the drop bounces).
- `ripple`: magnetic insert, CapCut's main-track behavior, **opt-in**. Clips starting at or after the insert point shift right by the inserted duration. The point must be a clip boundary or inside a gap; inside a clip is `OVERLAP` (split first). Not offered on `moveClip` (use `rippleDelete` + `addClip`).
- `overwrite`: Premiere-style overwrite / CapCut drag-over. Fully covered clips are removed, partially covered ones trimmed; a clip that fully contains the range must be split first.

`trimIn`, `trimOut`, `setSpeed` take `ripple?: boolean` with the same meaning: later clips on the track shift by the change in this clip's length.

### Op table

| op | semantics | inverse |
|---|---|---|
| `addTrack {track, index?}` | insert a track (with optional clips) at compositing index | `removeTrack` |
| `removeTrack {trackId}` | remove track and its clips; `LOCKED` if locked | `addTrack` (snapshot of the track, same index) |
| `setTrack {trackId, patch}` | name / locked / muted / `index` (reorder) | `setTrack` with old values |
| `setTrackClips {trackId, clips}` | replace the clip list wholesale (snapshot op) | `setTrackClips` old |
| `addClip {trackId, clip, overlap?}` | place a clip; defaults filled (`normalizeClip`) | `removeClip` / `rippleDelete` (ripple) / `setTrackClips` (overwrite) |
| `removeClip {clipId}` | lift: leave a gap | `addClip` |
| `rippleDelete {clipId}` | extract: later clips on the track close the gap | `addClip` with `overlap: 'ripple'` |
| `moveClip {clipId, start, trackId?, overlap?, solo?}` | move, optionally across tracks; linked and grouped companions move by the same delta on their own tracks unless `solo` | `moveClip` back / `setTrackClips` per touched track (overwrite) |
| `trimIn {clipId, delta, ripple?}` | head trim; `delta > 0` removes `delta` ticks from the head. Non-ripple: `start += delta`. Ripple: start stays, later clips shift `-delta`. Source `in` (or `out` when reversed) follows at `speed` | `trimIn -delta` |
| `trimOut {clipId, delta, ripple?}` | tail trim; `delta > 0` extends the end. Ripple shifts later clips `+delta` | `trimOut -delta` |
| `split {clipId, tick, newClipId}` | left keeps the id; source contiguous at the cut; keyframes at/after the cut move right and are rebased; `transitionOut` moves to the right piece | `join` |
| `join {leftId, rightId}` | merge adjacent, source-contiguous, otherwise-identical pieces (`UNJOINABLE` if they differ) | `split` |
| `roll {clipId, delta}` | move the edit point with the adjacent right neighbor; total length unchanged | `roll -delta` |
| `slip {clipId, delta}` | shift `in`/`out` by `delta * speed`; clip stays put | `slip -delta` |
| `slide {clipId, delta, leftId?, rightId?}` | move the clip; adjacent neighbors are trimmed so total length is unchanged. `undefined` = auto-detect adjacency, `null` = do not touch, id = that clip. The inverse names the neighbors explicitly | `slide -delta` |
| `setSpeed {clipId, speed, duration?, ripple?}` | duration becomes `round(sourceLen / speed)` unless given | `setSpeed` old speed with old duration (exact) |
| `reverse {clipId, reverse}` | flip playback direction | `reverse` old |
| `freezeFrame {clipId, tick, freezeDuration, frozenClipId, rightClipId}` | split at `tick`, insert a still (`Clip.freeze` = source tick) and ripple the rest of the track | `batch[rippleDelete frozen, join]` |
| `setClip {clipId, patch}` | name, assetId, crop, blend, mask, transitionIn/Out, freeze; `null` clears | `setClip` old |
| `setTransform {clipId, transform}` | partial transform (x, y, scale, rotation, opacity, anchor) | `setTransform` old keys |
| `setKeyframe {clipId, prop, keyframe}` | upsert by `at` (relative to clip start) | `setKeyframe` old / `removeKeyframe` |
| `removeKeyframe {clipId, prop, tick}` | remove; empty prop lists are dropped | `setKeyframe` |
| `setEffect {clipId, effect}` / `removeEffect` | upsert / remove by effect id | mirror |
| `setChroma` / `setText` / `setAudio` | replace or clear (`null`) the block; kind-checked | same op with old value |
| `linkAudio {linkId, clipIds}` / `unlink {linkId}` | link a visual clip with an audio clip so they move together | mirror |
| `group {groupId, clipIds}` / `ungroup {groupId}` | grouped clips move together | mirror |
| `addCaptionTrack` / `removeCaptionTrack` / `setCaptionTrack` | word-level caption tracks (style, placement, enabled) | mirror |
| `addCaption` / `setCaption` / `removeCaption` | captions never overlap on a track; words stay inside the caption | mirror |
| `alignCaptions {trackId, words, options?}` | regenerate captions from absolute-timed words (max 4 words / 2.5 s, break on sentence punctuation and 0.6 s silences); deterministic ids | `setCaptions` (snapshot) |
| `setCaptions {trackId, captions}` | replace wholesale (snapshot op) | `setCaptions` old |
| `addMarker` / `setMarker` / `removeMarker` / `resolveMarker` | timecoded notes, review, `qa_fail`, `approval`; `resolveMarker` stamps `{by: author, at}` | mirror |
| `setProjectSettings {patch}` | name, fps, width, height, styleRef | old values |
| `addAsset` / `setAsset` / `removeAsset` | asset registry; `removeAsset` is `REFERENCED` while any clip uses it; shrinking an asset revalidates its clips | mirror |
| `batch {ops}` | atomic, in order, one version bump | reversed inverses |

`Marker.clipId` is a soft reference: it may dangle after the clip is removed (undo restores the pair), and `addMarker` requires the clip to exist at add time.

### Inverses

`invert(op, before)` returns the op that undoes `op` when applied to `apply(before, op)`, and `apply(back, invert(inverse, after))` reproduces the forward result. Every op is inverted op-for-op except two **snapshot fallbacks**, chosen because the pre-state is not derivable from the op alone:

- `addClip`/`moveClip` with `overlap: 'overwrite'` -> `setTrackClips` for each touched track (target first, then source).
- `alignCaptions` -> `setCaptions` of the previous captions.

Inverses are op-based, not snapshot-based, on purpose: the human's `trimIn` can be undone after the agent has moved the same clip, because `trimIn -delta` still applies at the clip's new position. The test suite round-trips all 48 op types (63 fixtures) through apply -> invert -> apply.

## Event log and per-author undo

```ts
let { log, project } = loadLog(base, events);     // or createLog(base)
({ log, project } = append(log, project, op));    // validates, stores inverse, snapshots every N
versionAt(log, n); replay(base, events, from, to); head(log);
undo(project, log, author); redo(project, log, author); undoStack(log, author);
```

- `events` is the durable record; `inverses` and `snapshots` are derived and rebuilt by `loadLog`. `append` refuses a project that is not at the log head.
- Undo appends a new op (the stored inverse, re-stamped, with `undoes: <target id>`); nothing is ever removed from the log, so history and blame stay complete.
- Per-author stacks: `undo(…, agent)` reverses the agent's most recent forward op that is not currently undone, leaving the human's ops alone, and vice versa. Omit the author for a global undo. Redo reverses the author's most recent undo; a forward op by that author clears their redo stack. "Undone" is a chain (`isUndone`), so undo -> redo -> undo behaves as expected.
- If the current state no longer accepts the inverse (the other author deleted the clip), undo throws `UNDO_CONFLICT` and nothing changes.

## CRDT plan (why Yjs is not in this package)

This package is deliberately a pure `(state, op) -> state` reducer over plain JSON, with no Yjs dependency, because the ops are already the unit that a CRDT layer needs and adding it here would couple the document model to a transport. The plan for concurrent human + agent editing:

1. **Log as the shared object.** Wrap the `events` array in a `Y.Array<Op>` (or an Automerge list). Each client appends ops locally and applies them optimistically with `apply`. Yjs guarantees every replica converges on the same ordered array; every replica then folds the same array with the same reducer, so the projects converge too. Ops are immutable and content-addressed by `id`, which makes the array append-only and conflict-free.
2. **Rebase on reorder.** When a remote op lands *before* a local optimistic op in the converged order, the client rewinds to the last snapshot before the divergence point and replays (`replay` + `snapshots` exist for exactly this). Ops that no longer apply after reordering (their target was removed) throw a typed `OpError`; the client marks them `rejected` in the log instead of dropping them, so the other operator sees what was attempted. Structural ops are designed to be position-independent where possible (`trimIn -delta`, `slip`, `roll`, patches with explicit old values), which keeps rejections rare.
3. **Presence and intent.** Selection, playhead, and "agent is editing clip X" ride on Yjs awareness, not on the document.
4. **Per-author undo is unchanged.** Undo stacks are computed from `author` and `undoes` in the converged log, so undo works identically single-player and multiplayer.
5. **Alternative (state CRDT).** Mapping the `Project` tree itself onto `Y.Map`/`Y.Array` is possible, but merges would produce overlapping clips that no op ever produced; the op-log approach keeps the reducer as the single source of invariants. That is why the choice is a log CRDT.

The Python service validates the same document with `schema/project.schema.json` and can replay the log by porting `reducer.ts` (about 800 lines, no dependencies) or by calling a Node worker; the schema and the tick conventions are the contract.

## CapCut concept mapping

| CapCut | here |
|---|---|
| Draft (`draft_content.json`, µs) | `Project` (ticks at 6000/s); importer converts µs -> ticks, tracks -> `Track`, segments -> `Clip` |
| Main track (magnetic) | any `video` track + `overlap: 'ripple'` / `ripple: true` on the ops that touch it. Magnetism is an op flag, not a track property, so the agent chooses per edit |
| Overlay / PiP tracks | `overlay` (or additional `video`) tracks; `reject` overlap by default |
| Text, sticker, effect, filter, caption tracks | `text` tracks with `text` clips; `shape` clips; `Effect` entries on clips; `label`/`caption` tracks for imported ones; word captions live in `CaptionTrack` |
| Segment `target_timerange` / `source_timerange` | `start`/`duration` and `in`/`out` |
| Speed (`speed` material), reverse, freeze | `Clip.speed`, `Clip.reverse`, `Clip.freeze` via `setSpeed`, `reverse`, `freezeFrame` |
| Split, delete, ripple delete | `split`, `removeClip`, `rippleDelete` |
| Trim handles, roll (Ctrl-drag edit point), slip, slide | `trimIn`/`trimOut`, `roll`, `slip`, `slide` |
| Link/detach audio, group | `linkAudio`/`unlink`, `group`/`ungroup` (companions move together) |
| Lock / mute track | `setTrack {locked, muted}`; locked tracks reject clip ops |
| Position, scale, rotation, opacity, anchor, blend, crop, keyframes with easing | `Clip.transform`, `blend`, `crop`, `keyframes[prop]` with `Easing` (named or bezier) via `setTransform`, `setClip`, `setKeyframe` |
| Mask, chroma key (color, similarity/intensity, shadow/blend, despill, edge) | `Clip.mask`, `Clip.chroma` |
| Adjust, filter, LUT, blur/pixelate | `Effect {kind, params}` on the clip |
| Audio volume, fade in/out, ducking | `Clip.audio {gain dB, fadeIn, fadeOut, duck}` |
| Transitions | `Clip.transitionIn/Out {kind, duration}` on the boundary clip |
| Auto captions, karaoke, word styles, presets | `CaptionTrack.style.mode ('line'|'word'|'karaoke')`, per-caption `style`/`placement` overrides, `preset`, `scrimAware` placement |
| Markers, review comments | `Marker {kind: note|review|qa_fail|approval, author, resolved}` |
| Compound clip, nested sequence (Tier 2) | not modeled yet; planned as a `ClipKind` `'sequence'` referencing another `Project` id, nothing in the current ops precludes it |
| Speed curves, multicam, auto-reframe (Tier 2/3) | `keyframes['speed']`, a `sources[]` on video clips, and a per-`Project` reframe op respectively; all additive |

## assembleFromBoard

```ts
const op = assembleFromBoard(board, voAlignment, { author, project?, laneId?, gapPolicy?, captionStyle?, idFactory? });
project = apply(project, op);
```

Takes a storyboard `{ lanes: [{ id, cards: [{ id, t, t_end, asset_id, script, kind, in? }] }] }` (seconds) and a VO alignment `{ words: [{ text, start, end }], asset_id, duration? }` and returns one `batch`:

- registers assets it does not find in `options.project`;
- one clip per timed asset card on a video track (existing first video track reused, else created at index 0); `image`-ish card kinds become image clips; `card.in` sets the source in-point so the beat opens on the action;
- `gapPolicy: 'extend'` (default) runs each beat to the next beat's start and the last beat to the VO end so the product never leaves the screen; `'leave'` keeps board times;
- the VO as one audio clip on an audio track; a caption track aligned to the words via `alignCaptions`; a note marker per beat carrying the card's script (`beatMarkers: false` to skip).

Lane selection: `laneId`, else the only lane with asset cards, else a lane named/kinded "ours"/"target", else an error asking for `laneId`. `assembleFromBoardDetailed` also returns the ids it created. With `idFactory: sequentialIds()` the output is fully deterministic.

## Schema

`PROJECT_SCHEMA` (draft 2020-12) is hand-written in `src/schema.ts` and emitted to `schema/project.schema.json` by the build; the test suite compiles it with ajv and checks the emitted file matches. `validateProject(doc)` runs the schema through a small built-in evaluator, then the semantic invariants the schema language cannot express: unique ids, sorted non-overlapping clips and captions, audio clips only on audio tracks, asset references and source bounds, the non-media `in/out` convention, keyframe ordering, link ids used by at least two clips, derived duration. A Python validator should apply the same list (it is documented in the schema's `description`).

## assembleFromEditPlan

Read a fresh handoff with the engine's `get_edit_plan` tool, then:

```ts
const op = assembleFromEditPlan(handoff, {
  author: { kind: 'agent', id: 'editing-agent' },
  project,
  supportedTransitions: rendererSupportedTransitions,
});
({ project, log } = append(log, project, op));
```

The compiler preserves source in/out, timeline placement, constant speed,
clip-relative transform/opacity animation keys, audio gain/fades and declared
transitions. Per-clip rationale, source evidence and QA checks become review
markers. It dry-runs against the actual reducer, refuses nonempty timelines and
never fills gaps or drops unsupported transitions. Time is converted from source
seconds to 6000 ticks/s. Read the [handoff playbook](../playbooks/video-analysis-edit-handoff/playbook.md)
for unsupported operations and the required render/playback verification.

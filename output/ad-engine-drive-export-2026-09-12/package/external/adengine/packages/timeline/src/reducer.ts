/**
 * Pure reducer: apply(project, op) -> project. Never mutates its input.
 * Throws OpError on invalid targets/ranges; a throwing op leaves nothing applied
 * (batches are atomic by construction).
 */
import { chunkWords } from './captions.js';
import { OpError } from './errors.js';
import {
  allClips,
  assertNoCaptionOverlap,
  assertNoOverlap,
  clipEnd,
  clipIdExists,
  computeDuration,
  deepEqual,
  findTrackIndex,
  isMedia,
  normalizeCaptionTrack,
  normalizeClip,
  normalizeTrack,
  requireAssetIndex,
  requireCaption,
  requireCaptionTrack,
  requireClip,
  requireMarkerIndex,
  requireTrack,
  shiftClips,
  sortCaptions,
  sortClips,
  srcTicks,
  type LocatedClip,
} from './model.js';
import type { Op, OverlapMode } from './ops.js';
import type { Caption, Clip, Keyframe, Project, Tick, Track } from './types.js';

export function apply(project: Project, op: Op): Project {
  const next = reduce(project, op);
  return { ...next, version: project.version + 1, duration: computeDuration(next) };
}

/** Apply many top-level ops in order (each bumps the version). */
export function applyAll(project: Project, ops: readonly Op[]): Project {
  return ops.reduce(apply, project);
}

// ---------------------------------------------------------------------------

function fail(code: ConstructorParameters<typeof OpError>[0], msg: string, op: Op, details?: Record<string, unknown>): never {
  throw new OpError(code, msg, { opId: op.id, details });
}

function assertInt(v: unknown, what: string, op: Op, min = 0): asserts v is number {
  if (typeof v !== 'number' || !Number.isInteger(v) || v < min) fail('INVALID_RANGE', `${what} must be an integer >= ${min}, got ${String(v)}`, op);
}

function assertUnlocked(track: Track, op: Op): void {
  if (track.locked) fail('LOCKED', `track ${track.id} is locked`, op);
}

function assertKindCompatible(track: Track, clip: Pick<Clip, 'kind' | 'id'>, op: Op): void {
  const audioTrack = track.kind === 'audio';
  const audioClip = clip.kind === 'audio';
  if (audioTrack !== audioClip) fail('KIND_MISMATCH', `clip ${clip.id} (${clip.kind}) cannot live on ${track.kind} track ${track.id}`, op);
}

function validateClip(p: Project, clip: Clip, op: Op): void {
  if (clip.in < 0 || clip.out < 0) fail('SOURCE_BOUNDS', `clip ${clip.id}: source range [${clip.in}, ${clip.out}) runs before the asset start`, op);
  assertInt(clip.start, `clip ${clip.id}.start`, op);
  assertInt(clip.duration, `clip ${clip.id}.duration`, op, 1);
  assertInt(clip.in, `clip ${clip.id}.in`, op);
  assertInt(clip.out, `clip ${clip.id}.out`, op);
  if (!(clip.speed > 0) || !Number.isFinite(clip.speed)) fail('INVALID_RANGE', `clip ${clip.id}.speed must be > 0`, op);
  if (clip.transform.opacity < 0 || clip.transform.opacity > 1) fail('INVALID_RANGE', `clip ${clip.id} opacity must be 0..1`, op);
  if (isMedia(clip)) {
    if (clip.freeze === undefined && clip.out <= clip.in) fail('SOURCE_BOUNDS', `clip ${clip.id}: out (${clip.out}) must be > in (${clip.in})`, op);
    if (clip.freeze !== undefined && clip.out < clip.in) fail('SOURCE_BOUNDS', `clip ${clip.id}: out must be >= in`, op);
  } else if (clip.in !== 0 || clip.out !== clip.duration) {
    fail('SOURCE_BOUNDS', `non-media clip ${clip.id} must keep in=0 and out=duration`, op);
  }
  if (clip.assetId !== undefined) {
    const asset = p.assets.find((a) => a.id === clip.assetId);
    if (!asset) fail('NOT_FOUND', `clip ${clip.id} references missing asset ${clip.assetId}`, op);
    if (isMedia(clip) && asset.duration !== undefined) {
      const far = clip.freeze !== undefined ? clip.freeze : clip.out;
      if (far > asset.duration) fail('SOURCE_BOUNDS', `clip ${clip.id} reads past asset ${asset.id} end (${far} > ${asset.duration})`, op);
    }
  } else if (isMedia(clip) || clip.kind === 'image') {
    fail('INVALID_OP', `${clip.kind} clip ${clip.id} requires assetId`, op);
  }
  for (const [prop, kfs] of Object.entries(clip.keyframes)) {
    if (kfs.length === 0) fail('INVALID_DOCUMENT', `clip ${clip.id} keyframes.${prop} is empty`, op);
    for (let i = 0; i < kfs.length; i++) {
      assertInt(kfs[i]!.at, `keyframe ${prop}[${i}].at`, op);
      if (i > 0 && kfs[i]!.at <= kfs[i - 1]!.at) fail('INVALID_RANGE', `clip ${clip.id} keyframes.${prop} must be sorted with unique 'at'`, op);
    }
  }
  const effectIds = new Set<string>();
  for (const e of clip.effects) {
    if (effectIds.has(e.id)) fail('DUPLICATE_ID', `clip ${clip.id} has duplicate effect ${e.id}`, op);
    effectIds.add(e.id);
  }
}

function replaceTrack(p: Project, ti: number, track: Track): Project {
  const tracks = [...p.tracks];
  tracks[ti] = track;
  return { ...p, tracks };
}

function withClips(track: Track, clips: readonly Clip[], op: Op): Track {
  const sorted = sortClips(clips);
  assertNoOverlap(sorted, track.id, op.id);
  return { ...track, clips: sorted };
}

function requireMedia(clip: Clip, op: Op, what: string): void {
  if (!isMedia(clip)) fail('INVALID_OP', `${what} only applies to video/audio clips (${clip.id} is ${clip.kind})`, op);
  if (clip.freeze !== undefined) fail('INVALID_OP', `${what} does not apply to a freeze-frame clip (${clip.id})`, op);
}

/** Trim/extend the head by delta ticks (delta > 0 trims). Source follows. */
function setHead(clip: Clip, delta: Tick, moveStart: boolean): Clip {
  const duration = clip.duration - delta;
  let { in: i, out } = clip;
  if (clip.freeze === undefined) {
    if (isMedia(clip)) {
      const n = srcTicks(delta, clip.speed);
      if (clip.reverse) out -= n;
      else i += n;
    } else {
      out = duration;
    }
  }
  return { ...clip, start: moveStart ? clip.start + delta : clip.start, duration, in: i, out };
}

/** Extend/shorten the tail by delta ticks (delta > 0 extends). Source follows. */
function setTail(clip: Clip, delta: Tick): Clip {
  const duration = clip.duration + delta;
  let { in: i, out } = clip;
  if (clip.freeze === undefined) {
    if (isMedia(clip)) {
      const n = srcTicks(delta, clip.speed);
      if (clip.reverse) i -= n;
      else out += n;
    } else {
      out = duration;
    }
  }
  return { ...clip, duration, in: i, out };
}

function adjacentNeighbors(track: Track, ci: number): { left?: Clip; right?: Clip } {
  const clip = track.clips[ci]!;
  const l = track.clips[ci - 1];
  const r = track.clips[ci + 1];
  return {
    left: l && clipEnd(l) === clip.start ? l : undefined,
    right: r && r.start === clipEnd(clip) ? r : undefined,
  };
}

/** Insert `clip` into a track's clip list under an overlap policy. */
function placeClip(p: Project, ti: number, clip: Clip, mode: OverlapMode, op: Op): Project {
  const track = p.tracks[ti]!;
  const s = clip.start;
  const e = clipEnd(clip);
  let clips: Clip[];
  switch (mode) {
    case 'reject':
      clips = [...track.clips, clip];
      break;
    case 'ripple': {
      const inside = track.clips.find((c) => c.start < s && clipEnd(c) > s);
      if (inside) fail('OVERLAP', `ripple insert point ${s} is inside clip ${inside.id}; split it first`, op, { clipId: inside.id });
      clips = [...shiftClips(track.clips, s, clip.duration), clip];
      break;
    }
    case 'overwrite': {
      clips = [];
      for (const c of track.clips) {
        const cs = c.start;
        const ce = clipEnd(c);
        if (ce <= s || cs >= e) {
          clips.push(c);
        } else if (cs >= s && ce <= e) {
          // fully covered: dropped
        } else if (cs < s && ce > e) {
          fail('OVERLAP', `clip ${c.id} fully contains the overwrite range; split it first`, op, { clipId: c.id });
        } else if (cs < s) {
          clips.push(setTail(c, s - ce));
        } else {
          clips.push(setHead(c, e - cs, true));
        }
      }
      for (const c of clips) validateClip(p, c, op);
      clips.push(clip);
      break;
    }
  }
  return replaceTrack(p, ti, withClips(track, clips, op));
}

function splitClip(clip: Clip, at: Tick, newClipId: string, op: Op): [Clip, Clip] {
  if (!(at > clip.start && at < clipEnd(clip))) fail('INVALID_RANGE', `split point ${at} must be strictly inside clip ${clip.id} [${clip.start}, ${clipEnd(clip)})`, op);
  const leftDur = at - clip.start;
  const rightDur = clip.duration - leftDur;
  let left: Clip = { ...clip, duration: leftDur, keyframes: {} };
  let right: Clip = { ...clip, id: newClipId, start: at, duration: rightDur, keyframes: {} };
  if (clip.freeze === undefined) {
    if (isMedia(clip)) {
      const n = srcTicks(leftDur, clip.speed);
      if (clip.reverse) {
        left = { ...left, in: clip.out - n };
        right = { ...right, out: clip.out - n };
      } else {
        left = { ...left, out: clip.in + n };
        right = { ...right, in: clip.in + n };
      }
    } else {
      left = { ...left, out: leftDur };
      right = { ...right, in: 0, out: rightDur };
    }
  }
  for (const [prop, kfs] of Object.entries(clip.keyframes)) {
    const l = kfs.filter((k) => k.at < leftDur);
    const r = kfs.filter((k) => k.at >= leftDur).map((k) => ({ ...k, at: k.at - leftDur }));
    if (l.length) left.keyframes[prop] = l;
    if (r.length) right.keyframes[prop] = r;
  }
  delete left.transitionOut;
  delete right.transitionIn;
  return [left, right];
}

const JOIN_IGNORED = new Set(['id', 'start', 'duration', 'in', 'out', 'keyframes', 'transitionIn', 'transitionOut']);

function joinClips(left: Clip, right: Clip, op: Op): Clip {
  if (clipEnd(left) !== right.start) fail('NOT_ADJACENT', `join: ${right.id} does not start where ${left.id} ends`, op);
  if (left.transitionOut !== undefined || right.transitionIn !== undefined) fail('UNJOINABLE', `join: a transition sits between ${left.id} and ${right.id}`, op);
  for (const k of new Set([...Object.keys(left), ...Object.keys(right)])) {
    if (JOIN_IGNORED.has(k)) continue;
    if (!deepEqual((left as unknown as Record<string, unknown>)[k], (right as unknown as Record<string, unknown>)[k])) fail('UNJOINABLE', `join: ${left.id} and ${right.id} differ in '${k}'`, op);
  }
  let merged: Clip = { ...left, duration: left.duration + right.duration, keyframes: {} };
  if (left.freeze === undefined) {
    if (isMedia(left)) {
      if (left.reverse) {
        if (right.out !== left.in) fail('UNJOINABLE', `join: source not contiguous (${right.id}.out ${right.out} != ${left.id}.in ${left.in})`, op);
        merged = { ...merged, in: right.in };
      } else {
        if (right.in !== left.out) fail('UNJOINABLE', `join: source not contiguous (${right.id}.in ${right.in} != ${left.id}.out ${left.out})`, op);
        merged = { ...merged, out: right.out };
      }
    } else {
      merged = { ...merged, in: 0, out: merged.duration };
    }
  }
  for (const prop of new Set([...Object.keys(left.keyframes), ...Object.keys(right.keyframes)])) {
    const kfs: Keyframe[] = [...(left.keyframes[prop] ?? []), ...(right.keyframes[prop] ?? []).map((k) => ({ ...k, at: k.at + left.duration }))];
    if (kfs.length) merged.keyframes[prop] = kfs;
  }
  if (right.transitionOut !== undefined) merged.transitionOut = right.transitionOut;
  else delete merged.transitionOut;
  return merged;
}

function companionsOf(p: Project, clip: Clip): LocatedClip[] {
  if (!clip.linkId && !clip.groupId) return [];
  const out: LocatedClip[] = [];
  p.tracks.forEach((track, ti) =>
    track.clips.forEach((c, ci) => {
      if (c.id === clip.id) return;
      if ((clip.linkId && c.linkId === clip.linkId) || (clip.groupId && c.groupId === clip.groupId)) out.push({ ti, ci, track, clip: c });
    }),
  );
  return out;
}

function patchObject<T extends object>(target: T, patch: Record<string, unknown>): T {
  const out = { ...target } as Record<string, unknown>;
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined) continue;
    if (v === null) delete out[k];
    else out[k] = v;
  }
  return out as T;
}

// ---------------------------------------------------------------------------

export function reduce(p: Project, op: Op): Project {
  switch (op.type) {
    // ---- tracks
    case 'addTrack': {
      if (findTrackIndex(p, op.track.id) >= 0) fail('DUPLICATE_ID', `track ${op.track.id} exists`, op);
      const track = normalizeTrack(op.track);
      const seen = new Set<string>();
      for (const c of track.clips) {
        if (seen.has(c.id) || clipIdExists(p, c.id)) fail('DUPLICATE_ID', `clip ${c.id} exists`, op);
        seen.add(c.id);
        assertKindCompatible(track, c, op);
        validateClip(p, c, op);
      }
      assertNoOverlap(track.clips, track.id, op.id);
      const idx = op.index ?? p.tracks.length;
      if (!Number.isInteger(idx) || idx < 0 || idx > p.tracks.length) fail('INVALID_RANGE', `track index ${idx} out of range`, op);
      const tracks = [...p.tracks];
      tracks.splice(idx, 0, track);
      return { ...p, tracks };
    }
    case 'removeTrack': {
      const { ti, track } = requireTrack(p, op.trackId, op.id);
      assertUnlocked(track, op);
      return { ...p, tracks: p.tracks.filter((_, i) => i !== ti) };
    }
    case 'setTrack': {
      const { ti, track } = requireTrack(p, op.trackId, op.id);
      const { index, ...rest } = op.patch;
      const next = patchObject(track, rest as Record<string, unknown>);
      let tracks = [...p.tracks];
      tracks[ti] = next;
      if (index !== undefined && index !== ti) {
        if (!Number.isInteger(index) || index < 0 || index >= tracks.length) fail('INVALID_RANGE', `track index ${index} out of range`, op);
        tracks.splice(ti, 1);
        tracks.splice(index, 0, next);
      }
      return { ...p, tracks };
    }
    case 'setTrackClips': {
      const { ti, track } = requireTrack(p, op.trackId, op.id);
      assertUnlocked(track, op);
      const seen = new Set<string>();
      const others = new Set(p.tracks.filter((t) => t.id !== track.id).flatMap((t) => t.clips.map((c) => c.id)));
      for (const c of op.clips) {
        if (seen.has(c.id) || others.has(c.id)) fail('DUPLICATE_ID', `clip ${c.id} exists`, op);
        seen.add(c.id);
        assertKindCompatible(track, c, op);
        validateClip(p, c, op);
      }
      return replaceTrack(p, ti, withClips(track, op.clips, op));
    }

    // ---- clips
    case 'addClip': {
      const { ti, track } = requireTrack(p, op.trackId, op.id);
      assertUnlocked(track, op);
      if (clipIdExists(p, op.clip.id)) fail('DUPLICATE_ID', `clip ${op.clip.id} exists`, op);
      const clip = normalizeClip(op.clip);
      assertKindCompatible(track, clip, op);
      validateClip(p, clip, op);
      return placeClip(p, ti, clip, op.overlap ?? 'reject', op);
    }
    case 'removeClip': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      return replaceTrack(p, ti, { ...track, clips: track.clips.filter((c) => c.id !== clip.id) });
    }
    case 'rippleDelete': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const rest = track.clips.filter((c) => c.id !== clip.id);
      return replaceTrack(p, ti, withClips(track, shiftClips(rest, clipEnd(clip), -clip.duration), op));
    }
    case 'moveClip': {
      assertInt(op.start, 'moveClip.start', op);
      const src = requireClip(p, op.clipId, op.id);
      assertUnlocked(src.track, op);
      const targetTi = op.trackId === undefined ? src.ti : requireTrack(p, op.trackId, op.id).ti;
      const target = p.tracks[targetTi]!;
      assertUnlocked(target, op);
      assertKindCompatible(target, src.clip, op);
      const delta = op.start - src.clip.start;
      let next = replaceTrack(p, src.ti, { ...src.track, clips: src.track.clips.filter((c) => c.id !== src.clip.id) });
      next = placeClip(next, targetTi, { ...src.clip, start: op.start }, op.overlap ?? 'reject', op);
      if (!op.solo && delta !== 0) {
        for (const comp of companionsOf(p, src.clip)) {
          const cur = requireClip(next, comp.clip.id, op.id);
          assertUnlocked(cur.track, op);
          if (cur.clip.start + delta < 0) fail('INVALID_RANGE', `linked clip ${cur.clip.id} would start before 0`, op);
          const moved = { ...cur.clip, start: cur.clip.start + delta };
          next = replaceTrack(next, cur.ti, withClips(cur.track, [...cur.track.clips.filter((c) => c.id !== cur.clip.id), moved], op));
        }
      }
      return next;
    }
    case 'trimIn': {
      assertInt(op.delta, 'trimIn.delta', op, Number.MIN_SAFE_INTEGER);
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const next = setHead(clip, op.delta, !op.ripple);
      validateClip(p, next, op);
      let rest = track.clips.filter((c) => c.id !== clip.id);
      if (op.ripple) rest = shiftClips(rest, clipEnd(clip), -op.delta);
      return replaceTrack(p, ti, withClips(track, [...rest, next], op));
    }
    case 'trimOut': {
      assertInt(op.delta, 'trimOut.delta', op, Number.MIN_SAFE_INTEGER);
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const next = setTail(clip, op.delta);
      validateClip(p, next, op);
      let rest = track.clips.filter((c) => c.id !== clip.id);
      if (op.ripple) rest = shiftClips(rest, clipEnd(clip), op.delta);
      return replaceTrack(p, ti, withClips(track, [...rest, next], op));
    }
    case 'split': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      if (clipIdExists(p, op.newClipId)) fail('DUPLICATE_ID', `clip ${op.newClipId} exists`, op);
      const [left, right] = splitClip(clip, op.tick, op.newClipId, op);
      validateClip(p, left, op);
      validateClip(p, right, op);
      return replaceTrack(p, ti, withClips(track, [...track.clips.filter((c) => c.id !== clip.id), left, right], op));
    }
    case 'join': {
      const l = requireClip(p, op.leftId, op.id);
      const r = requireClip(p, op.rightId, op.id);
      if (l.ti !== r.ti) fail('NOT_ADJACENT', `join: ${op.leftId} and ${op.rightId} are on different tracks`, op);
      assertUnlocked(l.track, op);
      const merged = joinClips(l.clip, r.clip, op);
      validateClip(p, merged, op);
      return replaceTrack(p, l.ti, withClips(l.track, [...l.track.clips.filter((c) => c.id !== l.clip.id && c.id !== r.clip.id), merged], op));
    }
    case 'roll': {
      assertInt(op.delta, 'roll.delta', op, Number.MIN_SAFE_INTEGER);
      const { ti, ci, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const { right } = adjacentNeighbors(track, ci);
      if (!right) fail('NOT_ADJACENT', `roll: clip ${clip.id} has no adjacent right neighbor`, op);
      const a = setTail(clip, op.delta);
      const b = setHead(right, op.delta, true);
      validateClip(p, a, op);
      validateClip(p, b, op);
      return replaceTrack(p, ti, withClips(track, [...track.clips.filter((c) => c.id !== clip.id && c.id !== right.id), a, b], op));
    }
    case 'slip': {
      assertInt(op.delta, 'slip.delta', op, Number.MIN_SAFE_INTEGER);
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      requireMedia(clip, op, 'slip');
      const n = srcTicks(op.delta, clip.speed);
      const next = { ...clip, in: clip.in + n, out: clip.out + n };
      validateClip(p, next, op);
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'slide': {
      assertInt(op.delta, 'slide.delta', op, Number.MIN_SAFE_INTEGER);
      const { ti, ci, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const auto = adjacentNeighbors(track, ci);
      const pick = (spec: string | null | undefined, autoClip: Clip | undefined, side: string): Clip | undefined => {
        if (spec === null) return undefined;
        if (spec === undefined) return autoClip;
        const found = track.clips.find((c) => c.id === spec);
        if (!found) fail('NOT_FOUND', `slide: ${side} neighbor ${spec} not on track ${track.id}`, op);
        return found;
      };
      const left = pick(op.leftId, auto.left, 'left');
      const right = pick(op.rightId, auto.right, 'right');
      const out: Clip[] = [];
      const touched = new Set([clip.id, left?.id, right?.id]);
      const moved = { ...clip, start: clip.start + op.delta };
      assertInt(moved.start, 'slide result start', op);
      out.push(moved);
      if (left) {
        const l = setTail(left, op.delta);
        validateClip(p, l, op);
        out.push(l);
      }
      if (right) {
        const r = setHead(right, op.delta, true);
        validateClip(p, r, op);
        out.push(r);
      }
      return replaceTrack(p, ti, withClips(track, [...track.clips.filter((c) => !touched.has(c.id)), ...out], op));
    }
    case 'setSpeed': {
      if (!(op.speed > 0) || !Number.isFinite(op.speed)) fail('INVALID_RANGE', `speed must be > 0`, op);
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      requireMedia(clip, op, 'setSpeed');
      const duration = op.duration ?? Math.max(1, Math.round((clip.out - clip.in) / op.speed));
      assertInt(duration, 'setSpeed.duration', op, 1);
      const next = { ...clip, speed: op.speed, duration };
      validateClip(p, next, op);
      let rest = track.clips.filter((c) => c.id !== clip.id);
      if (op.ripple) rest = shiftClips(rest, clipEnd(clip), duration - clip.duration);
      return replaceTrack(p, ti, withClips(track, [...rest, next], op));
    }
    case 'reverse': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      requireMedia(clip, op, 'reverse');
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? { ...c, reverse: op.reverse } : c)) });
    }
    case 'freezeFrame': {
      assertInt(op.freezeDuration, 'freezeDuration', op, 1);
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      if (clip.kind !== 'video') fail('INVALID_OP', `freezeFrame only applies to video clips`, op);
      requireMedia(clip, op, 'freezeFrame');
      for (const id of [op.frozenClipId, op.rightClipId]) if (clipIdExists(p, id) || id === op.frozenClipId && id === op.rightClipId) fail('DUPLICATE_ID', `clip ${id} exists`, op);
      const [left, right] = splitClip(clip, op.tick, op.rightClipId, op);
      const n = srcTicks(op.tick - clip.start, clip.speed);
      const freeze = clip.reverse ? clip.out - n : clip.in + n;
      const frozen: Clip = {
        ...clip,
        id: op.frozenClipId,
        start: op.tick,
        duration: op.freezeDuration,
        in: freeze,
        out: freeze,
        speed: 1,
        reverse: false,
        freeze,
        keyframes: {},
      };
      delete frozen.audio;
      delete frozen.transitionIn;
      delete frozen.transitionOut;
      delete frozen.linkId;
      validateClip(p, left, op);
      validateClip(p, right, op);
      validateClip(p, frozen, op);
      const rest = shiftClips(track.clips.filter((c) => c.id !== clip.id), op.tick, op.freezeDuration);
      const rightShifted = { ...right, start: right.start + op.freezeDuration };
      return replaceTrack(p, ti, withClips(track, [...rest, left, frozen, rightShifted], op));
    }
    case 'setClip': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const next = patchObject(clip, op.patch as Record<string, unknown>);
      if (next.freeze !== undefined) {
        if (!isMedia(next)) fail('INVALID_OP', `freeze only applies to media clips`, op);
        assertInt(next.freeze, 'freeze', op);
      }
      validateClip(p, next, op);
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'setTransform': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const transform = { ...clip.transform };
      for (const [k, v] of Object.entries(op.transform)) {
        if (v === undefined) continue;
        if (k === 'anchor') {
          const a = v as { x: number; y: number };
          transform.anchor = { x: a.x, y: a.y };
        } else {
          if (typeof v !== 'number' || !Number.isFinite(v)) fail('INVALID_RANGE', `transform.${k} must be a finite number`, op);
          (transform as unknown as Record<string, number>)[k] = v;
        }
      }
      const next = { ...clip, transform };
      validateClip(p, next, op);
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'setKeyframe': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      assertInt(op.keyframe.at, 'keyframe.at', op);
      const list = (clip.keyframes[op.prop] ?? []).filter((k) => k.at !== op.keyframe.at);
      list.push({ ...op.keyframe });
      list.sort((a, b) => a.at - b.at);
      const next = { ...clip, keyframes: { ...clip.keyframes, [op.prop]: list } };
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'removeKeyframe': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const existing = clip.keyframes[op.prop];
      if (!existing || !existing.some((k) => k.at === op.tick)) fail('NOT_FOUND', `no keyframe ${op.prop}@${op.tick} on clip ${clip.id}`, op);
      const list = existing.filter((k) => k.at !== op.tick);
      const keyframes = { ...clip.keyframes };
      if (list.length) keyframes[op.prop] = list;
      else delete keyframes[op.prop];
      const next = { ...clip, keyframes };
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'setEffect': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const idx = clip.effects.findIndex((e) => e.id === op.effect.id);
      const effects = [...clip.effects];
      if (idx >= 0) effects[idx] = { ...op.effect };
      else effects.push({ ...op.effect });
      const next = { ...clip, effects };
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'removeEffect': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      if (!clip.effects.some((e) => e.id === op.effectId)) fail('NOT_FOUND', `effect ${op.effectId} not on clip ${clip.id}`, op);
      const next = { ...clip, effects: clip.effects.filter((e) => e.id !== op.effectId) };
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'setChroma':
    case 'setText':
    case 'setAudio': {
      const { ti, track, clip } = requireClip(p, op.clipId, op.id);
      assertUnlocked(track, op);
      const key = op.type === 'setChroma' ? 'chroma' : op.type === 'setText' ? 'text' : 'audio';
      const value = op.type === 'setChroma' ? op.chroma : op.type === 'setText' ? op.text : op.audio;
      if (key === 'audio' && value !== null && !isMedia(clip)) fail('INVALID_OP', `audio props only apply to media clips`, op);
      if (key === 'chroma' && value !== null && clip.kind !== 'video' && clip.kind !== 'image') fail('INVALID_OP', `chroma only applies to video/image clips`, op);
      if (key === 'text' && value !== null && clip.kind !== 'text' && clip.kind !== 'caption') fail('INVALID_OP', `text style only applies to text/caption clips`, op);
      const next = patchObject(clip, { [key]: value === null ? null : { ...value } });
      return replaceTrack(p, ti, { ...track, clips: track.clips.map((c) => (c.id === clip.id ? next : c)) });
    }
    case 'linkAudio': {
      if (op.clipIds.length < 2) fail('INVALID_OP', `linkAudio needs at least two clips`, op);
      if (allClips(p).some((c) => c.linkId === op.linkId)) fail('DUPLICATE_ID', `linkId ${op.linkId} in use`, op);
      const located = op.clipIds.map((id) => requireClip(p, id, op.id));
      for (const l of located) {
        assertUnlocked(l.track, op);
        if (l.clip.linkId) fail('INVALID_OP', `clip ${l.clip.id} is already linked (${l.clip.linkId})`, op);
      }
      if (!located.some((l) => l.clip.kind === 'audio') || !located.some((l) => l.clip.kind !== 'audio')) fail('KIND_MISMATCH', `linkAudio needs an audio clip and a visual clip`, op);
      const ids = new Set(op.clipIds);
      return { ...p, tracks: p.tracks.map((t) => ({ ...t, clips: t.clips.map((c) => (ids.has(c.id) ? { ...c, linkId: op.linkId } : c)) })) };
    }
    case 'unlink': {
      if (!allClips(p).some((c) => c.linkId === op.linkId)) fail('NOT_FOUND', `linkId ${op.linkId} not found`, op);
      return {
        ...p,
        tracks: p.tracks.map((t) => ({
          ...t,
          clips: t.clips.map((c) => {
            if (c.linkId !== op.linkId) return c;
            const { linkId: _drop, ...rest } = c;
            return rest;
          }),
        })),
      };
    }
    case 'group': {
      if (op.clipIds.length < 1) fail('INVALID_OP', `group needs at least one clip`, op);
      if (allClips(p).some((c) => c.groupId === op.groupId)) fail('DUPLICATE_ID', `groupId ${op.groupId} in use`, op);
      for (const id of op.clipIds) {
        const l = requireClip(p, id, op.id);
        assertUnlocked(l.track, op);
        if (l.clip.groupId) fail('INVALID_OP', `clip ${id} is already in group ${l.clip.groupId}`, op);
      }
      const ids = new Set(op.clipIds);
      return { ...p, tracks: p.tracks.map((t) => ({ ...t, clips: t.clips.map((c) => (ids.has(c.id) ? { ...c, groupId: op.groupId } : c)) })) };
    }
    case 'ungroup': {
      if (!allClips(p).some((c) => c.groupId === op.groupId)) fail('NOT_FOUND', `groupId ${op.groupId} not found`, op);
      return {
        ...p,
        tracks: p.tracks.map((t) => ({
          ...t,
          clips: t.clips.map((c) => {
            if (c.groupId !== op.groupId) return c;
            const { groupId: _drop, ...rest } = c;
            return rest;
          }),
        })),
      };
    }

    // ---- captions
    case 'addCaptionTrack': {
      if (p.captions.some((t) => t.id === op.track.id)) fail('DUPLICATE_ID', `caption track ${op.track.id} exists`, op);
      const track = normalizeCaptionTrack(op.track);
      for (const c of track.captions) validateCaption(c, op);
      assertNoCaptionOverlap(track.captions, track.id, op.id);
      const captions = [...p.captions];
      captions.splice(op.index ?? captions.length, 0, track);
      return { ...p, captions };
    }
    case 'removeCaptionTrack': {
      const { ti } = requireCaptionTrack(p, op.trackId, op.id);
      return { ...p, captions: p.captions.filter((_, i) => i !== ti) };
    }
    case 'setCaptionTrack': {
      const { ti, track } = requireCaptionTrack(p, op.trackId, op.id);
      const captions = [...p.captions];
      captions[ti] = patchObject(track, op.patch as Record<string, unknown>);
      return { ...p, captions };
    }
    case 'addCaption': {
      const { ti, track } = requireCaptionTrack(p, op.trackId, op.id);
      if (track.captions.some((c) => c.id === op.caption.id)) fail('DUPLICATE_ID', `caption ${op.caption.id} exists on ${track.id}`, op);
      validateCaption(op.caption, op);
      return setCaptionList(p, ti, [...track.captions, op.caption], op);
    }
    case 'setCaption': {
      const { ti, track } = requireCaptionTrack(p, op.trackId, op.id);
      const { caption } = requireCaption(track, op.captionId, op.id);
      const next = patchObject(caption, op.patch as Record<string, unknown>);
      validateCaption(next, op);
      return setCaptionList(p, ti, track.captions.map((c) => (c.id === caption.id ? next : c)), op);
    }
    case 'removeCaption': {
      const { ti, track } = requireCaptionTrack(p, op.trackId, op.id);
      requireCaption(track, op.captionId, op.id);
      return setCaptionList(p, ti, track.captions.filter((c) => c.id !== op.captionId), op);
    }
    case 'alignCaptions': {
      const { ti } = requireCaptionTrack(p, op.trackId, op.id);
      for (const w of op.words) {
        assertInt(w.start, `word '${w.text}'.start`, op);
        assertInt(w.end, `word '${w.text}'.end`, op);
        if (w.end < w.start) fail('INVALID_RANGE', `word '${w.text}' ends before it starts`, op);
      }
      const captions = chunkWords(op.words, op.options, op.id);
      return setCaptionList(p, ti, captions, op);
    }
    case 'setCaptions': {
      const { ti } = requireCaptionTrack(p, op.trackId, op.id);
      const seen = new Set<string>();
      for (const c of op.captions) {
        if (seen.has(c.id)) fail('DUPLICATE_ID', `duplicate caption ${c.id}`, op);
        seen.add(c.id);
        validateCaption(c, op);
      }
      return setCaptionList(p, ti, op.captions, op);
    }

    // ---- markers
    case 'addMarker': {
      if (p.markers.some((m) => m.id === op.marker.id)) fail('DUPLICATE_ID', `marker ${op.marker.id} exists`, op);
      assertInt(op.marker.at, 'marker.at', op);
      if (op.marker.clipId !== undefined && !clipIdExists(p, op.marker.clipId)) fail('NOT_FOUND', `marker references missing clip ${op.marker.clipId}`, op);
      const markers = [...p.markers];
      markers.splice(op.index ?? markers.length, 0, { ...op.marker });
      return { ...p, markers };
    }
    case 'setMarker': {
      const i = requireMarkerIndex(p, op.markerId, op.id);
      const next = patchObject(p.markers[i]!, op.patch as Record<string, unknown>);
      assertInt(next.at, 'marker.at', op);
      const markers = [...p.markers];
      markers[i] = next;
      return { ...p, markers };
    }
    case 'removeMarker': {
      const i = requireMarkerIndex(p, op.markerId, op.id);
      return { ...p, markers: p.markers.filter((_, j) => j !== i) };
    }
    case 'resolveMarker': {
      const i = requireMarkerIndex(p, op.markerId, op.id);
      const markers = [...p.markers];
      markers[i] = patchObject(p.markers[i]!, { resolved: op.resolved ? { by: op.author, at: op.at } : null });
      return { ...p, markers };
    }

    // ---- project / assets
    case 'setProjectSettings': {
      const next = patchObject(p, op.patch as Record<string, unknown>);
      if (!(next.fps > 0) || !Number.isFinite(next.fps)) fail('INVALID_RANGE', `fps must be > 0`, op);
      assertInt(next.width, 'width', op, 1);
      assertInt(next.height, 'height', op, 1);
      return next;
    }
    case 'addAsset': {
      if (p.assets.some((a) => a.id === op.asset.id)) fail('DUPLICATE_ID', `asset ${op.asset.id} exists`, op);
      if (op.asset.duration !== undefined) assertInt(op.asset.duration, 'asset.duration', op);
      const assets = [...p.assets];
      assets.splice(op.index ?? assets.length, 0, { ...op.asset });
      return { ...p, assets };
    }
    case 'setAsset': {
      const i = requireAssetIndex(p, op.assetId, op.id);
      const assets = [...p.assets];
      assets[i] = patchObject(p.assets[i]!, op.patch as Record<string, unknown>);
      if (assets[i]!.duration !== undefined) assertInt(assets[i]!.duration, 'asset.duration', op);
      const next = { ...p, assets };
      for (const c of allClips(next)) if (c.assetId === op.assetId) validateClip(next, c, op);
      return next;
    }
    case 'removeAsset': {
      const i = requireAssetIndex(p, op.assetId, op.id);
      const user = allClips(p).find((c) => c.assetId === op.assetId);
      if (user) fail('REFERENCED', `asset ${op.assetId} is used by clip ${user.id}`, op);
      return { ...p, assets: p.assets.filter((_, j) => j !== i) };
    }

    // ---- batch
    case 'batch': {
      return op.ops.reduce(reduce, p);
    }
  }
}

function validateCaption(c: Caption, op: Op): void {
  assertInt(c.start, `caption ${c.id}.start`, op);
  assertInt(c.duration, `caption ${c.id}.duration`, op, 1);
  for (const w of c.words) {
    assertInt(w.start, `caption ${c.id} word '${w.text}'.start`, op);
    assertInt(w.duration, `caption ${c.id} word '${w.text}'.duration`, op, 1);
    if (w.start + w.duration > c.duration) fail('INVALID_RANGE', `caption ${c.id} word '${w.text}' runs past the caption end`, op);
  }
}

function setCaptionList(p: Project, ti: number, captions: readonly Caption[], op: Op): Project {
  const sorted = sortCaptions(captions);
  assertNoCaptionOverlap(sorted, p.captions[ti]!.id, op.id);
  const list = [...p.captions];
  list[ti] = { ...p.captions[ti]!, captions: sorted };
  return { ...p, captions: list };
}

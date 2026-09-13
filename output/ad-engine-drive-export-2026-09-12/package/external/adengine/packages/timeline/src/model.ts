/** Shared helpers over the document: lookup, normalization, invariants. */
import { OpError } from './errors.js';
import type { CaptionTrackInit, ClipInit, TrackInit } from './ops.js';
import { TICK_RATE, type Caption, type CaptionPlacement, type CaptionStyle, type CaptionTrack, type Clip, type Crop, type Project, type Tick, type Track, type Transform } from './types.js';

export const DEFAULT_TRANSFORM: Transform = { x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, anchor: { x: 0.5, y: 0.5 } };
export const DEFAULT_CROP: Crop = { left: 0, top: 0, right: 0, bottom: 0 };
export const DEFAULT_CAPTION_STYLE: CaptionStyle = {
  font: 'Inter',
  size: 64,
  weight: 800,
  color: '#ffffff',
  highlightColor: '#ffd400',
  mode: 'karaoke',
  uppercase: false,
  outline: { color: '#000000', width: 4 },
};
export const DEFAULT_CAPTION_PLACEMENT: CaptionPlacement = { anchor: 'bottom', y: 0.78, x: 0.5, safeZone: true, scrimAware: true };

export function clipEnd(c: Pick<Clip, 'start' | 'duration'>): Tick {
  return c.start + c.duration;
}

export function isMedia(c: Pick<Clip, 'kind'>): boolean {
  return c.kind === 'video' || c.kind === 'audio';
}

/** Timeline ticks -> source ticks at `speed`, rounded symmetrically so srcTicks(-d) === -srcTicks(d). */
export function srcTicks(delta: Tick, speed: number): Tick {
  const v = Math.round(Math.abs(delta) * speed);
  return delta < 0 ? -v : v;
}

export function sortClips(clips: readonly Clip[]): Clip[] {
  return [...clips].sort((a, b) => a.start - b.start || a.id.localeCompare(b.id));
}

export function sortCaptions(captions: readonly Caption[]): Caption[] {
  return [...captions].sort((a, b) => a.start - b.start || a.id.localeCompare(b.id));
}

export function createProject(init: Partial<Project> & { id: string; fps: number; width: number; height: number }): Project {
  const p: Project = {
    id: init.id,
    version: init.version ?? 0,
    tickRate: TICK_RATE,
    fps: init.fps,
    width: init.width,
    height: init.height,
    duration: 0,
    tracks: init.tracks ?? [],
    assets: init.assets ?? [],
    markers: init.markers ?? [],
    captions: init.captions ?? [],
  };
  if (init.name !== undefined) p.name = init.name;
  if (init.styleRef !== undefined) p.styleRef = init.styleRef;
  if (init.meta !== undefined) p.meta = init.meta;
  p.duration = computeDuration(p);
  return p;
}

export function computeDuration(p: Pick<Project, 'tracks'>): Tick {
  let d = 0;
  for (const t of p.tracks) for (const c of t.clips) d = Math.max(d, clipEnd(c));
  return d;
}

export function normalizeClip(init: ClipInit): Clip {
  const media = isMedia(init);
  const speed = init.speed ?? 1;
  const inTick = media ? (init.in ?? 0) : 0;
  const out = media ? (init.out ?? inTick + srcTicks(init.duration, speed)) : init.duration;
  const keyframes: Record<string, Clip['keyframes'][string]> = {};
  for (const [prop, kfs] of Object.entries(init.keyframes ?? {})) {
    if (kfs && kfs.length > 0) keyframes[prop] = [...kfs].sort((a, b) => a.at - b.at);
  }
  const clip: Clip = {
    id: init.id,
    kind: init.kind,
    start: init.start,
    duration: init.duration,
    in: inTick,
    out,
    speed: media ? speed : 1,
    reverse: media ? (init.reverse ?? false) : false,
    transform: init.transform ?? { ...DEFAULT_TRANSFORM, anchor: { ...DEFAULT_TRANSFORM.anchor } },
    crop: init.crop ?? { ...DEFAULT_CROP },
    blend: init.blend ?? 'normal',
    keyframes,
    effects: init.effects ?? [],
  };
  const optional = ['assetId', 'name', 'freeze', 'mask', 'chroma', 'text', 'audio', 'transitionIn', 'transitionOut', 'linkId', 'groupId'] as const;
  for (const k of optional) {
    const v = init[k];
    if (v !== undefined && v !== null) (clip as unknown as Record<string, unknown>)[k] = v;
  }
  return clip;
}

export function normalizeTrack(init: TrackInit): Track {
  return {
    id: init.id,
    kind: init.kind,
    name: init.name ?? init.kind,
    locked: init.locked ?? false,
    muted: init.muted ?? false,
    clips: sortClips((init.clips ?? []).map(normalizeClip)),
  };
}

export function normalizeCaptionTrack(init: CaptionTrackInit): CaptionTrack {
  return {
    id: init.id,
    name: init.name ?? 'Captions',
    enabled: init.enabled ?? true,
    style: init.style ?? { ...DEFAULT_CAPTION_STYLE },
    placement: init.placement ?? { ...DEFAULT_CAPTION_PLACEMENT },
    captions: sortCaptions(init.captions ?? []),
  };
}

export interface LocatedClip {
  ti: number;
  ci: number;
  track: Track;
  clip: Clip;
}

export function findTrackIndex(p: Project, trackId: string): number {
  return p.tracks.findIndex((t) => t.id === trackId);
}

export function requireTrack(p: Project, trackId: string, opId?: string): { ti: number; track: Track } {
  const ti = findTrackIndex(p, trackId);
  const track = p.tracks[ti];
  if (ti < 0 || !track) throw new OpError('NOT_FOUND', `track ${trackId} not found`, { opId });
  return { ti, track };
}

export function locateClip(p: Project, clipId: string): LocatedClip | undefined {
  for (let ti = 0; ti < p.tracks.length; ti++) {
    const track = p.tracks[ti]!;
    const ci = track.clips.findIndex((c) => c.id === clipId);
    if (ci >= 0) return { ti, ci, track, clip: track.clips[ci]! };
  }
  return undefined;
}

export function requireClip(p: Project, clipId: string, opId?: string): LocatedClip {
  const l = locateClip(p, clipId);
  if (!l) throw new OpError('NOT_FOUND', `clip ${clipId} not found`, { opId });
  return l;
}

export function clipIdExists(p: Project, clipId: string): boolean {
  return locateClip(p, clipId) !== undefined;
}

export function allClips(p: Project): Clip[] {
  return p.tracks.flatMap((t) => t.clips);
}

export function requireCaptionTrack(p: Project, trackId: string, opId?: string): { ti: number; track: CaptionTrack } {
  const ti = p.captions.findIndex((t) => t.id === trackId);
  const track = p.captions[ti];
  if (ti < 0 || !track) throw new OpError('NOT_FOUND', `caption track ${trackId} not found`, { opId });
  return { ti, track };
}

export function requireCaption(track: CaptionTrack, captionId: string, opId?: string): { ci: number; caption: Caption } {
  const ci = track.captions.findIndex((c) => c.id === captionId);
  const caption = track.captions[ci];
  if (ci < 0 || !caption) throw new OpError('NOT_FOUND', `caption ${captionId} not found on ${track.id}`, { opId });
  return { ci, caption };
}

export function requireMarkerIndex(p: Project, markerId: string, opId?: string): number {
  const i = p.markers.findIndex((m) => m.id === markerId);
  if (i < 0) throw new OpError('NOT_FOUND', `marker ${markerId} not found`, { opId });
  return i;
}

export function requireAssetIndex(p: Project, assetId: string, opId?: string): number {
  const i = p.assets.findIndex((a) => a.id === assetId);
  if (i < 0) throw new OpError('NOT_FOUND', `asset ${assetId} not found`, { opId });
  return i;
}

/** Shift every clip whose start >= fromTick by delta. */
export function shiftClips(clips: readonly Clip[], fromTick: Tick, delta: Tick): Clip[] {
  if (delta === 0) return [...clips];
  return clips.map((c) => (c.start >= fromTick ? { ...c, start: c.start + delta } : c));
}

/** Sorted-adjacent overlap check. Throws OVERLAP. */
export function assertNoOverlap(clips: readonly Clip[], trackId: string, opId?: string): void {
  for (let i = 1; i < clips.length; i++) {
    const a = clips[i - 1]!;
    const b = clips[i]!;
    if (clipEnd(a) > b.start) {
      throw new OpError('OVERLAP', `clip ${b.id} overlaps ${a.id} on track ${trackId}`, {
        opId,
        details: { trackId, a: a.id, b: b.id, aEnd: clipEnd(a), bStart: b.start },
      });
    }
  }
}

export function assertNoCaptionOverlap(captions: readonly Caption[], trackId: string, opId?: string): void {
  for (let i = 1; i < captions.length; i++) {
    const a = captions[i - 1]!;
    const b = captions[i]!;
    if (a.start + a.duration > b.start) {
      throw new OpError('OVERLAP', `caption ${b.id} overlaps ${a.id} on caption track ${trackId}`, { opId });
    }
  }
}

export function deepEqual(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (typeof a !== typeof b || a === null || b === null) return false;
  if (typeof a !== 'object') return Number.isNaN(a) && Number.isNaN(b);
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  if (Array.isArray(a)) {
    const bb = b as unknown[];
    return a.length === bb.length && a.every((v, i) => deepEqual(v, bb[i]));
  }
  const ao = a as Record<string, unknown>;
  const bo = b as Record<string, unknown>;
  const ak = Object.keys(ao).filter((k) => ao[k] !== undefined);
  const bk = Object.keys(bo).filter((k) => bo[k] !== undefined);
  if (ak.length !== bk.length) return false;
  return ak.every((k) => deepEqual(ao[k], bo[k]));
}

/** Structural clone that drops `undefined` fields so equality is stable. */
export function clone<T>(v: T): T {
  return JSON.parse(JSON.stringify(v)) as T;
}

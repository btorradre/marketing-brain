/**
 * invert(op, before) -> the op that undoes `op` when applied to apply(before, op).
 *
 * Every op is inverted op-for-op except two documented snapshot fallbacks:
 *   - addClip/moveClip with overlap 'overwrite'  -> setTrackClips (per touched track)
 *   - alignCaptions                               -> setCaptions (per caption track)
 * Both are generative/destructive edits whose exact pre-state cannot be
 * re-derived from the op alone, so the inverse carries the pre-state.
 */
import { newId, nowIso } from './ids.js';
import {
  allClips,
  clipEnd,
  clone,
  requireAssetIndex,
  requireCaption,
  requireCaptionTrack,
  requireClip,
  requireMarkerIndex,
  requireTrack,
} from './model.js';
import type { Op, OpBase, TrackPatch, TrimInOp, TrimOutOp } from './ops.js';
import { reduce } from './reducer.js';
import type { Author, Clip, Project, Track } from './types.js';

export interface InvertMeta {
  id?: string;
  at?: string;
  author?: Author;
}

function inversePatch<T extends object>(obj: T, patch: object): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined) continue;
    const old = (obj as Record<string, unknown>)[k];
    out[k] = old === undefined ? null : clone(old);
  }
  return out;
}

function adjacent(track: Track, clip: Clip): { left?: Clip; right?: Clip } {
  const ci = track.clips.findIndex((c) => c.id === clip.id);
  const l = track.clips[ci - 1];
  const r = track.clips[ci + 1];
  return { left: l && clipEnd(l) === clip.start ? l : undefined, right: r && r.start === clipEnd(clip) ? r : undefined };
}

export function invert(op: Op, before: Project, meta?: InvertMeta): Op {
  const base: OpBase = { id: meta?.id ?? newId('op'), at: meta?.at ?? nowIso(), author: meta?.author ?? op.author };
  const b = base;
  switch (op.type) {
    case 'addTrack':
      return { ...b, type: 'removeTrack', trackId: op.track.id };
    case 'removeTrack': {
      const { ti, track } = requireTrack(before, op.trackId, op.id);
      return { ...b, type: 'addTrack', track: clone(track), index: ti };
    }
    case 'setTrack': {
      const { ti, track } = requireTrack(before, op.trackId, op.id);
      const { index, ...rest } = op.patch;
      const patch = inversePatch(track, rest) as TrackPatch;
      return { ...b, type: 'setTrack', trackId: op.trackId, patch: index === undefined ? patch : { ...patch, index: ti } };
    }
    case 'setTrackClips': {
      const { track } = requireTrack(before, op.trackId, op.id);
      return { ...b, type: 'setTrackClips', trackId: op.trackId, clips: clone(track.clips) };
    }
    case 'addClip': {
      if (op.overlap === 'overwrite') {
        const { track } = requireTrack(before, op.trackId, op.id);
        return { ...b, type: 'setTrackClips', trackId: op.trackId, clips: clone(track.clips) };
      }
      if (op.overlap === 'ripple') return { ...b, type: 'rippleDelete', clipId: op.clip.id };
      return { ...b, type: 'removeClip', clipId: op.clip.id };
    }
    case 'removeClip': {
      const { track, clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'addClip', trackId: track.id, clip: clone(clip) };
    }
    case 'rippleDelete': {
      const { track, clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'addClip', trackId: track.id, clip: clone(clip), overlap: 'ripple' };
    }
    case 'moveClip': {
      const src = requireClip(before, op.clipId, op.id);
      if (op.overlap === 'overwrite') {
        const touched = new Set<string>();
        if (op.trackId) touched.add(op.trackId); // target first: it holds the moved clip id until restored
        touched.add(src.track.id);
        if (!op.solo) {
          for (const c of allClips(before)) {
            if (c.id === src.clip.id) continue;
            if ((src.clip.linkId && c.linkId === src.clip.linkId) || (src.clip.groupId && c.groupId === src.clip.groupId)) touched.add(requireClip(before, c.id).track.id);
          }
        }
        const ops: Op[] = [...touched].map((trackId) => ({ ...b, id: newId('op'), type: 'setTrackClips', trackId, clips: clone(requireTrack(before, trackId).track.clips) }));
        return { ...b, type: 'batch', ops };
      }
      const inv: Op = { ...b, type: 'moveClip', clipId: op.clipId, start: src.clip.start, trackId: src.track.id, overlap: 'reject' };
      if (op.solo) inv.solo = true;
      return inv;
    }
    case 'trimIn':
    case 'trimOut': {
      const inv: TrimInOp | TrimOutOp = { ...b, type: op.type, clipId: op.clipId, delta: -op.delta };
      if (op.ripple) inv.ripple = true;
      return inv;
    }
    case 'split':
      return { ...b, type: 'join', leftId: op.clipId, rightId: op.newClipId };
    case 'join': {
      const { clip } = requireClip(before, op.leftId, op.id);
      return { ...b, type: 'split', clipId: op.leftId, tick: clipEnd(clip), newClipId: op.rightId };
    }
    case 'roll':
    case 'slip':
      return { ...b, type: op.type, clipId: op.clipId, delta: -op.delta };
    case 'slide': {
      const { track, clip } = requireClip(before, op.clipId, op.id);
      const auto = adjacent(track, clip);
      const resolve = (spec: string | null | undefined, a: Clip | undefined) => (spec === undefined ? (a?.id ?? null) : spec);
      return { ...b, type: 'slide', clipId: op.clipId, delta: -op.delta, leftId: resolve(op.leftId, auto.left), rightId: resolve(op.rightId, auto.right) };
    }
    case 'setSpeed': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const inv: Op = { ...b, type: 'setSpeed', clipId: op.clipId, speed: clip.speed, duration: clip.duration };
      if (op.ripple) inv.ripple = true;
      return inv;
    }
    case 'reverse': {
      const { clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'reverse', clipId: op.clipId, reverse: clip.reverse };
    }
    case 'freezeFrame':
      return {
        ...b,
        type: 'batch',
        ops: [
          { ...b, id: newId('op'), type: 'rippleDelete', clipId: op.frozenClipId },
          { ...b, id: newId('op'), type: 'join', leftId: op.clipId, rightId: op.rightClipId },
        ],
      };
    case 'setClip': {
      const { clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'setClip', clipId: op.clipId, patch: inversePatch(clip, op.patch) };
    }
    case 'setTransform': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const transform: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(op.transform)) {
        if (v === undefined) continue;
        transform[k] = clone((clip.transform as unknown as Record<string, unknown>)[k]);
      }
      return { ...b, type: 'setTransform', clipId: op.clipId, transform };
    }
    case 'setKeyframe': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const old = clip.keyframes[op.prop]?.find((k) => k.at === op.keyframe.at);
      if (old) return { ...b, type: 'setKeyframe', clipId: op.clipId, prop: op.prop, keyframe: clone(old) };
      return { ...b, type: 'removeKeyframe', clipId: op.clipId, prop: op.prop, tick: op.keyframe.at };
    }
    case 'removeKeyframe': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const old = clip.keyframes[op.prop]?.find((k) => k.at === op.tick);
      if (!old) return { ...b, type: 'batch', ops: [] };
      return { ...b, type: 'setKeyframe', clipId: op.clipId, prop: op.prop, keyframe: clone(old) };
    }
    case 'setEffect': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const old = clip.effects.find((e) => e.id === op.effect.id);
      if (old) return { ...b, type: 'setEffect', clipId: op.clipId, effect: clone(old) };
      return { ...b, type: 'removeEffect', clipId: op.clipId, effectId: op.effect.id };
    }
    case 'removeEffect': {
      const { clip } = requireClip(before, op.clipId, op.id);
      const old = clip.effects.find((e) => e.id === op.effectId);
      if (!old) return { ...b, type: 'batch', ops: [] };
      return { ...b, type: 'setEffect', clipId: op.clipId, effect: clone(old) };
    }
    case 'setChroma': {
      const { clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'setChroma', clipId: op.clipId, chroma: clip.chroma ? clone(clip.chroma) : null };
    }
    case 'setText': {
      const { clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'setText', clipId: op.clipId, text: clip.text ? clone(clip.text) : null };
    }
    case 'setAudio': {
      const { clip } = requireClip(before, op.clipId, op.id);
      return { ...b, type: 'setAudio', clipId: op.clipId, audio: clip.audio ? clone(clip.audio) : null };
    }
    case 'linkAudio':
      return { ...b, type: 'unlink', linkId: op.linkId };
    case 'unlink':
      return { ...b, type: 'linkAudio', linkId: op.linkId, clipIds: allClips(before).filter((c) => c.linkId === op.linkId).map((c) => c.id) };
    case 'group':
      return { ...b, type: 'ungroup', groupId: op.groupId };
    case 'ungroup':
      return { ...b, type: 'group', groupId: op.groupId, clipIds: allClips(before).filter((c) => c.groupId === op.groupId).map((c) => c.id) };
    case 'addCaptionTrack':
      return { ...b, type: 'removeCaptionTrack', trackId: op.track.id };
    case 'removeCaptionTrack': {
      const { ti, track } = requireCaptionTrack(before, op.trackId, op.id);
      return { ...b, type: 'addCaptionTrack', track: clone(track), index: ti };
    }
    case 'setCaptionTrack': {
      const { track } = requireCaptionTrack(before, op.trackId, op.id);
      return { ...b, type: 'setCaptionTrack', trackId: op.trackId, patch: inversePatch(track, op.patch) };
    }
    case 'addCaption':
      return { ...b, type: 'removeCaption', trackId: op.trackId, captionId: op.caption.id };
    case 'setCaption': {
      const { track } = requireCaptionTrack(before, op.trackId, op.id);
      const { caption } = requireCaption(track, op.captionId, op.id);
      return { ...b, type: 'setCaption', trackId: op.trackId, captionId: op.captionId, patch: inversePatch(caption, op.patch) };
    }
    case 'removeCaption': {
      const { track } = requireCaptionTrack(before, op.trackId, op.id);
      const { caption } = requireCaption(track, op.captionId, op.id);
      return { ...b, type: 'addCaption', trackId: op.trackId, caption: clone(caption) };
    }
    case 'alignCaptions':
    case 'setCaptions': {
      const { track } = requireCaptionTrack(before, op.trackId, op.id);
      return { ...b, type: 'setCaptions', trackId: op.trackId, captions: clone(track.captions) };
    }
    case 'addMarker':
      return { ...b, type: 'removeMarker', markerId: op.marker.id };
    case 'setMarker': {
      const i = requireMarkerIndex(before, op.markerId, op.id);
      return { ...b, type: 'setMarker', markerId: op.markerId, patch: inversePatch(before.markers[i]!, op.patch) };
    }
    case 'removeMarker': {
      const i = requireMarkerIndex(before, op.markerId, op.id);
      return { ...b, type: 'addMarker', marker: clone(before.markers[i]!), index: i };
    }
    case 'resolveMarker': {
      const i = requireMarkerIndex(before, op.markerId, op.id);
      const old = before.markers[i]!.resolved;
      return { ...b, type: 'setMarker', markerId: op.markerId, patch: { resolved: old ? clone(old) : null } };
    }
    case 'setProjectSettings':
      return { ...b, type: 'setProjectSettings', patch: inversePatch(before, op.patch) };
    case 'addAsset':
      return { ...b, type: 'removeAsset', assetId: op.asset.id };
    case 'setAsset': {
      const i = requireAssetIndex(before, op.assetId, op.id);
      return { ...b, type: 'setAsset', assetId: op.assetId, patch: inversePatch(before.assets[i]!, op.patch) };
    }
    case 'removeAsset': {
      const i = requireAssetIndex(before, op.assetId, op.id);
      return { ...b, type: 'addAsset', asset: clone(before.assets[i]!), index: i };
    }
    case 'batch': {
      let state = before;
      const inverses: Op[] = [];
      for (const inner of op.ops) {
        inverses.push(invert(inner, state, { author: base.author }));
        state = reduce(state, inner);
      }
      return { ...b, type: 'batch', ops: inverses.reverse() };
    }
  }
}

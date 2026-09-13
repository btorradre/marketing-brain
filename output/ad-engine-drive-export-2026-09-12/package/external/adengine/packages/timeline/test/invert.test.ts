import { describe, expect, it } from 'vitest';
import { invert } from '../src/invert.js';
import { clone } from '../src/model.js';
import { OP_TYPES, type Op } from '../src/ops.js';
import { apply, applyAll } from '../src/reducer.js';
import type { Project } from '../src/types.js';
import { HUMAN, S, clip, op, seed } from './fixture.js';

interface Case {
  name: string;
  pre?: Op[];
  op: (p: Project) => Op;
}

const words = ['One', 'two', 'three.', 'Four', 'five'].map((text, i) => ({ text, start: i * 3000, end: i * 3000 + 2000 }));

const cases: Case[] = [
  { name: 'addTrack', op: () => op('addTrack', { track: { id: 'v2', kind: 'video', clips: [{ id: 'n1', kind: 'video', assetId: 'vidA', start: 0, duration: S }] }, index: 1 }) },
  { name: 'removeTrack', op: () => op('removeTrack', { trackId: 'a1' }) },
  { name: 'setTrack', op: () => op('setTrack', { trackId: 'v1', patch: { name: 'Main', muted: true, index: 2 } }) },
  { name: 'setTrackClips', op: (p) => op('setTrackClips', { trackId: 'v1', clips: [clip(p, 'c3')] }) },
  { name: 'addClip reject', op: () => op('addClip', { trackId: 'v1', clip: { id: 'n1', kind: 'video', assetId: 'vidA', start: 4 * S, duration: S } }) },
  { name: 'addClip ripple', op: () => op('addClip', { trackId: 'v1', clip: { id: 'n1', kind: 'video', assetId: 'vidA', start: 2 * S, duration: S }, overlap: 'ripple' }) },
  { name: 'addClip overwrite', op: () => op('addClip', { trackId: 'v1', clip: { id: 'n1', kind: 'video', assetId: 'vidA', start: S, duration: 3 * S }, overlap: 'overwrite' }) },
  { name: 'removeClip', op: () => op('removeClip', { clipId: 'c1' }) },
  { name: 'rippleDelete', op: () => op('rippleDelete', { clipId: 'c1' }) },
  { name: 'moveClip linked', op: () => op('moveClip', { clipId: 'c2', start: 6 * S }) },
  { name: 'moveClip overwrite across tracks', op: () => op('moveClip', { clipId: 'c3', start: 3 * S + 3000, trackId: 'ov', overlap: 'overwrite', solo: true }) },
  { name: 'trimIn ripple', op: () => op('trimIn', { clipId: 'c1', delta: 3000, ripple: true }) },
  { name: 'trimIn extend', op: () => op('trimIn', { clipId: 'c3', delta: -3000 }) },
  { name: 'trimOut ripple', op: () => op('trimOut', { clipId: 'c1', delta: -3000, ripple: true }) },
  { name: 'trimOut extend', op: () => op('trimOut', { clipId: 'c3', delta: 3000 }) },
  { name: 'split', op: () => op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' }) },
  { name: 'split with transition', op: () => op('split', { clipId: 'c2', tick: 3 * S, newClipId: 'c2b' }) },
  { name: 'join', pre: [op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' })], op: () => op('join', { leftId: 'c1', rightId: 'c1b' }) },
  { name: 'roll', op: () => op('roll', { clipId: 'c1', delta: 3000 }) },
  { name: 'slip', op: () => op('slip', { clipId: 'c3', delta: 3000 }) },
  { name: 'slide auto', op: () => op('slide', { clipId: 'c2', delta: 3000 }) },
  { name: 'slide both neighbors', pre: [op('moveClip', { clipId: 'c3', start: 4 * S })], op: () => op('slide', { clipId: 'c2', delta: -3000 }) },
  { name: 'setSpeed ripple', op: () => op('setSpeed', { clipId: 'c1', speed: 2, ripple: true }) },
  { name: 'setSpeed slow', op: () => op('setSpeed', { clipId: 'c3', speed: 0.5 }) },
  { name: 'reverse', op: () => op('reverse', { clipId: 'c1', reverse: true }) },
  { name: 'freezeFrame', op: () => op('freezeFrame', { clipId: 'c1', tick: 6000, freezeDuration: 3000, frozenClipId: 'f1', rightClipId: 'c1r' }) },
  { name: 'setClip', op: () => op('setClip', { clipId: 'c1', patch: { name: 'Hook', blend: 'screen', mask: { shape: 'rect', feather: 2, invert: false, params: {} }, transitionIn: { kind: 'dissolve', duration: 300 }, crop: { left: 0.1, top: 0, right: 0, bottom: 0 } } }) },
  { name: 'setClip clear', pre: [op('setClip', { clipId: 'c2', patch: { name: 'X' } })], op: () => op('setClip', { clipId: 'c2', patch: { name: null, transitionOut: null } }) },
  { name: 'setTransform', op: () => op('setTransform', { clipId: 'c1', transform: { x: 0.1, opacity: 0.5, anchor: { x: 0, y: 0 } } }) },
  { name: 'setKeyframe new', op: () => op('setKeyframe', { clipId: 'c1', prop: 'scale', keyframe: { at: 3000, value: 1.2, easing: 'easeInOut' } }) },
  { name: 'setKeyframe replace', op: () => op('setKeyframe', { clipId: 'c1', prop: 'opacity', keyframe: { at: 0, value: 0.5, easing: 'linear' } }) },
  { name: 'removeKeyframe', op: () => op('removeKeyframe', { clipId: 'c1', prop: 'opacity', tick: 6000 }) },
  { name: 'removeKeyframe last of prop', pre: [op('removeKeyframe', { clipId: 'c1', prop: 'opacity', tick: 6000 })], op: () => op('removeKeyframe', { clipId: 'c1', prop: 'opacity', tick: 0 }) },
  { name: 'setEffect update', op: () => op('setEffect', { clipId: 'c1', effect: { id: 'e1', kind: 'adjust', params: { exposure: 0.4 }, enabled: false } }) },
  { name: 'setEffect new', op: () => op('setEffect', { clipId: 'c1', effect: { id: 'e2', kind: 'blur', params: { radius: 4 }, enabled: true } }) },
  { name: 'removeEffect', op: () => op('removeEffect', { clipId: 'c1', effectId: 'e1' }) },
  { name: 'setChroma', op: () => op('setChroma', { clipId: 'c1', chroma: { color: '#00ff00', similarity: 0.13, blend: 0.08, despill: 0.5, edge: 0.1 } }) },
  { name: 'setText clear', op: () => op('setText', { clipId: 'tx1', text: null }) },
  { name: 'setAudio', op: () => op('setAudio', { clipId: 'c1', audio: { gain: -3, fadeIn: 0, fadeOut: 0 } }) },
  { name: 'setAudio clear', op: () => op('setAudio', { clipId: 'vo', audio: null }) },
  { name: 'linkAudio', pre: [op('unlink', { linkId: 'L1' })], op: () => op('linkAudio', { linkId: 'L2', clipIds: ['c2', 'c2a'] }) },
  { name: 'unlink', op: () => op('unlink', { linkId: 'L1' }) },
  { name: 'group', op: () => op('group', { groupId: 'g1', clipIds: ['c1', 'tx1'] }) },
  { name: 'ungroup', pre: [op('group', { groupId: 'g1', clipIds: ['c1', 'tx1'] })], op: () => op('ungroup', { groupId: 'g1' }) },
  { name: 'addCaptionTrack', op: () => op('addCaptionTrack', { track: { id: 'cap2' }, index: 0 }) },
  { name: 'removeCaptionTrack', op: () => op('removeCaptionTrack', { trackId: 'cap' }) },
  { name: 'setCaptionTrack', op: () => op('setCaptionTrack', { trackId: 'cap', patch: { name: 'Karaoke', enabled: false } }) },
  { name: 'addCaption', op: () => op('addCaption', { trackId: 'cap', caption: { id: 'k3', start: 3 * S, duration: S, words: [] } }) },
  { name: 'setCaption', op: () => op('setCaption', { trackId: 'cap', captionId: 'k1', patch: { duration: 5000, words: [{ text: 'Hello', start: 0, duration: 2500 }, { text: 'there', start: 2500, duration: 2500 }], style: { color: '#ff0000' }, placement: { anchor: 'top' } } }) },
  { name: 'removeCaption', op: () => op('removeCaption', { trackId: 'cap', captionId: 'k2' }) },
  { name: 'alignCaptions', op: () => op('alignCaptions', { trackId: 'cap', words, options: { maxWords: 2 } }) },
  { name: 'setCaptions', op: () => op('setCaptions', { trackId: 'cap', captions: [] }) },
  { name: 'addMarker', op: () => op('addMarker', { marker: { id: 'm2', at: 0, kind: 'qa_fail', author: HUMAN, body: 'wrong colorway', clipId: 'c1' }, index: 0 }) },
  { name: 'setMarker', op: () => op('setMarker', { markerId: 'm1', patch: { body: 'x', clipId: 'c1', at: 2 * S } }) },
  { name: 'removeMarker', op: () => op('removeMarker', { markerId: 'm1' }) },
  { name: 'resolveMarker', op: () => op('resolveMarker', { markerId: 'm1', resolved: true }) },
  { name: 'resolveMarker clear', pre: [op('resolveMarker', { markerId: 'm1', resolved: true })], op: () => op('resolveMarker', { markerId: 'm1', resolved: false }) },
  { name: 'setProjectSettings', op: () => op('setProjectSettings', { patch: { fps: 24, name: null, styleRef: 'brand-x', width: 1920, height: 1080 } }) },
  { name: 'addAsset', op: () => op('addAsset', { asset: { id: 'new', kind: 'image' }, index: 1 }) },
  { name: 'setAsset', op: () => op('setAsset', { assetId: 'vidA', patch: { duration: 15 * S, name: 'A' } }) },
  { name: 'removeAsset', pre: [op('removeClip', { clipId: 'img1' })], op: () => op('removeAsset', { assetId: 'imgC' }) },
  {
    name: 'batch',
    op: () =>
      op('batch', {
        ops: [
          op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' }),
          op('setSpeed', { clipId: 'c1b', speed: 2, ripple: true }),
          op('addMarker', { marker: { id: 'm2', at: 9000, kind: 'review', author: HUMAN, body: 'check' } }),
          op('rippleDelete', { clipId: 'c2' }),
        ],
      }),
  },
];

const norm = (p: Project) => clone({ ...p, version: 0 });

describe('every op inverts exactly', () => {
  for (const c of cases) {
    it(c.name, () => {
      const before = applyAll(seed(), c.pre ?? []);
      const o = c.op(before);
      const after = apply(before, o);
      expect(norm(after)).not.toEqual(norm(before));
      const inv = invert(o, before);
      const back = apply(after, inv);
      expect(norm(back)).toEqual(norm(before));
      expect(back.version).toBe(before.version + 2);
      // inverse of the inverse re-produces the forward result
      const again = apply(back, invert(inv, after));
      expect(norm(again)).toEqual(norm(after));
    });
  }

  it('covers every op type', () => {
    const covered = new Set(cases.map((c) => c.op(applyAll(seed(), c.pre ?? [])).type));
    const missing = OP_TYPES.filter((t) => !covered.has(t));
    expect(missing).toEqual([]);
  });
});

import { describe, expect, it } from 'vitest';
import { OpError } from '../src/errors.js';
import { apply, applyAll } from '../src/reducer.js';
import { AGENT, S, clip, ids, op, seed } from './fixture.js';

const code = (fn: () => unknown) => {
  try {
    fn();
  } catch (e) {
    if (e instanceof OpError) return e.code;
    throw e;
  }
  return 'NO_ERROR';
};

describe('split', () => {
  it('splits source-contiguously, keeps left id, rebases keyframes', () => {
    const p = apply(seed(), op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' }));
    const l = clip(p, 'c1');
    const r = clip(p, 'c1b');
    expect([l.start, l.duration, l.in, l.out]).toEqual([0, 9000, 0, 9000]);
    expect([r.start, r.duration, r.in, r.out]).toEqual([9000, 3000, 9000, 12000]);
    expect(l.keyframes.opacity!.map((k) => k.at)).toEqual([0, 6000]);
    expect(r.keyframes.opacity).toBeUndefined();
    expect(ids(p, 'v1')).toEqual(['c1', 'c1b', 'c2', 'c3']);
  });
  it('moves keyframes at/after the cut to the right piece, rebased', () => {
    const p = apply(seed(), op('split', { clipId: 'c1', tick: 3000, newClipId: 'c1b' }));
    expect(clip(p, 'c1').keyframes.opacity!.map((k) => k.at)).toEqual([0]);
    expect(clip(p, 'c1b').keyframes.opacity!.map((k) => k.at)).toEqual([3000]);
  });
  it('uses source ticks at speed != 1', () => {
    const p = applyAll(seed(), [op('setSpeed', { clipId: 'c3', speed: 2 }), op('split', { clipId: 'c3', tick: 5 * S + 1500, newClipId: 'c3b' })]);
    expect(clip(p, 'c3')).toMatchObject({ duration: 1500, in: 6000, out: 9000 });
    expect(clip(p, 'c3b')).toMatchObject({ start: 5 * S + 1500, duration: 1500, in: 9000, out: 12000 });
  });
  it('splits a reversed clip from the out point', () => {
    const p = applyAll(seed(), [op('reverse', { clipId: 'c1', reverse: true }), op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' })]);
    expect(clip(p, 'c1')).toMatchObject({ in: 3000, out: 12000 });
    expect(clip(p, 'c1b')).toMatchObject({ in: 0, out: 3000 });
  });
  it('moves transitionOut to the right piece', () => {
    const p = apply(seed(), op('split', { clipId: 'c2', tick: 3 * S, newClipId: 'c2b' }));
    expect(clip(p, 'c2').transitionOut).toBeUndefined();
    expect(clip(p, 'c2b').transitionOut).toEqual({ kind: 'dissolve', duration: 600 });
  });
  it('rejects split on a boundary', () => {
    expect(code(() => apply(seed(), op('split', { clipId: 'c1', tick: 0, newClipId: 'x' })))).toBe('INVALID_RANGE');
    expect(code(() => apply(seed(), op('split', { clipId: 'c1', tick: 2 * S, newClipId: 'x' })))).toBe('INVALID_RANGE');
  });
});

describe('ripple and overlap modes', () => {
  it('rippleDelete closes the gap on that track only', () => {
    const p = apply(seed(), op('rippleDelete', { clipId: 'c1' }));
    expect(clip(p, 'c2').start).toBe(0);
    expect(clip(p, 'c3').start).toBe(3 * S);
    expect(clip(p, 'c2a').start).toBe(2 * S);
  });
  it('addClip default rejects overlaps', () => {
    expect(code(() => apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'n', kind: 'video', assetId: 'vidA', start: S, duration: S } })))).toBe('OVERLAP');
  });
  it('addClip ripple at a boundary shifts later clips', () => {
    const p = apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'n', kind: 'video', assetId: 'vidA', start: 2 * S, duration: S }, overlap: 'ripple' }));
    expect(ids(p, 'v1')).toEqual(['c1', 'n', 'c2', 'c3']);
    expect(clip(p, 'c2').start).toBe(3 * S);
    expect(clip(p, 'c3').start).toBe(6 * S);
  });
  it('addClip ripple inside a clip is rejected', () => {
    expect(code(() => apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'n', kind: 'video', assetId: 'vidA', start: S, duration: S }, overlap: 'ripple' })))).toBe('OVERLAP');
  });
  it('addClip overwrite trims and removes what is under it', () => {
    const p = apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'n', kind: 'video', assetId: 'vidA', start: S, duration: 3 * S }, overlap: 'overwrite' }));
    expect(ids(p, 'v1')).toEqual(['c1', 'n', 'c3']);
    expect(clip(p, 'c1')).toMatchObject({ duration: S, out: S });
  });
  it('addClip overwrite inside a containing clip is rejected', () => {
    expect(code(() => apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'n', kind: 'video', assetId: 'vidA', start: 3000, duration: 3000 }, overlap: 'overwrite' })))).toBe('OVERLAP');
  });
  it('trimIn ripple keeps start, advances in, shifts later clips left', () => {
    const p = apply(seed(), op('trimIn', { clipId: 'c1', delta: 3000, ripple: true }));
    expect(clip(p, 'c1')).toMatchObject({ start: 0, duration: 9000, in: 3000, out: 12000 });
    expect(clip(p, 'c2').start).toBe(9000);
    expect(clip(p, 'c3').start).toBe(5 * S - 3000);
  });
  it('trimIn non-ripple moves the start', () => {
    const p = apply(seed(), op('trimIn', { clipId: 'c1', delta: 3000 }));
    expect(clip(p, 'c1')).toMatchObject({ start: 3000, duration: 9000, in: 3000 });
    expect(clip(p, 'c2').start).toBe(2 * S);
  });
  it('trimOut ripple shifts later clips by delta', () => {
    const p = apply(seed(), op('trimOut', { clipId: 'c1', delta: -3000, ripple: true }));
    expect(clip(p, 'c1')).toMatchObject({ duration: 9000, out: 9000 });
    expect(clip(p, 'c2').start).toBe(9000);
  });
  it('trimOut into a neighbor is rejected; past the asset is SOURCE_BOUNDS', () => {
    expect(code(() => apply(seed(), op('trimOut', { clipId: 'c1', delta: 100 })))).toBe('OVERLAP');
    expect(code(() => apply(seed(), op('trimOut', { clipId: 'vo', delta: 11 * S })))).toBe('SOURCE_BOUNDS');
  });
});

describe('roll / slip / slide', () => {
  it('roll moves the edit point, total length unchanged', () => {
    const p = apply(seed(), op('roll', { clipId: 'c1', delta: 3000 }));
    expect(clip(p, 'c1')).toMatchObject({ duration: 15000, out: 15000 });
    expect(clip(p, 'c2')).toMatchObject({ start: 15000, duration: 9000, in: 3000 });
  });
  it('roll needs an adjacent right neighbor and a positive remainder', () => {
    expect(code(() => apply(seed(), op('roll', { clipId: 'c2', delta: 100 })))).toBe('NOT_ADJACENT');
    expect(code(() => apply(seed(), op('roll', { clipId: 'c1', delta: 2 * S })))).toBe('INVALID_RANGE');
  });
  it('slip shifts the source window only', () => {
    const p = apply(seed(), op('slip', { clipId: 'c3', delta: 3000 }));
    expect(clip(p, 'c3')).toMatchObject({ start: 5 * S, duration: S, in: 9000, out: 15000 });
    expect(code(() => apply(seed(), op('slip', { clipId: 'c1', delta: -1 })))).toBe('SOURCE_BOUNDS');
    expect(code(() => apply(seed(), op('slip', { clipId: 'img1', delta: 1 })))).toBe('INVALID_OP');
  });
  it('slide trims adjacent neighbors, total unchanged', () => {
    const p = applyAll(seed(), [op('moveClip', { clipId: 'c3', start: 4 * S }), op('slide', { clipId: 'c2', delta: 3000 })]);
    expect(clip(p, 'c1')).toMatchObject({ duration: 15000, out: 15000 });
    expect(clip(p, 'c2')).toMatchObject({ start: 15000, duration: 2 * S, in: 0 });
    expect(clip(p, 'c3')).toMatchObject({ start: 27000, duration: 3000, in: 9000, out: 12000 });
  });
  it('slide with an explicit null neighbor leaves it alone', () => {
    const p = apply(seed(), op('slide', { clipId: 'c2', delta: 3000, leftId: null }));
    expect(clip(p, 'c1').duration).toBe(2 * S);
    expect(clip(p, 'c2').start).toBe(15000);
  });
});

describe('speed / reverse / freeze', () => {
  it('setSpeed rederives duration from the source range', () => {
    const p = apply(seed(), op('setSpeed', { clipId: 'c1', speed: 2 }));
    expect(clip(p, 'c1')).toMatchObject({ speed: 2, duration: 6000, in: 0, out: 12000 });
    expect(clip(p, 'c2').start).toBe(2 * S);
    const r = apply(seed(), op('setSpeed', { clipId: 'c1', speed: 2, ripple: true }));
    expect(clip(r, 'c2').start).toBe(6000);
    expect(code(() => apply(seed(), op('setSpeed', { clipId: 'c1', speed: 0.5 })))).toBe('OVERLAP');
  });
  it('freezeFrame splits, inserts a frozen clip, ripples the track', () => {
    const p = apply(seed(), op('freezeFrame', { clipId: 'c1', tick: 6000, freezeDuration: 3000, frozenClipId: 'f1', rightClipId: 'c1r' }));
    expect(ids(p, 'v1')).toEqual(['c1', 'f1', 'c1r', 'c2', 'c3']);
    expect(clip(p, 'f1')).toMatchObject({ start: 6000, duration: 3000, freeze: 6000, in: 6000, out: 6000 });
    expect(clip(p, 'c1r')).toMatchObject({ start: 9000, duration: 6000, in: 6000, out: 12000 });
    expect(clip(p, 'c2').start).toBe(15000);
    expect(clip(p, 'c2a').start).toBe(2 * S);
  });
});

describe('move / link / group / lock / kinds', () => {
  it('moveClip carries linked clips; solo does not', () => {
    const p = apply(seed(), op('moveClip', { clipId: 'c2', start: 6 * S }));
    expect(clip(p, 'c2a').start).toBe(6 * S);
    const q = apply(seed(), op('moveClip', { clipId: 'c2', start: 6 * S, solo: true }));
    expect(clip(q, 'c2a').start).toBe(2 * S);
  });
  it('moveClip across tracks and kind checks', () => {
    const p = apply(seed(), op('moveClip', { clipId: 'c3', start: 0, trackId: 'ov' }));
    expect(ids(p, 'ov')).toEqual(['c3', 'img1']);
    expect(code(() => apply(seed(), op('moveClip', { clipId: 'c3', start: 0, trackId: 'a1' })))).toBe('KIND_MISMATCH');
  });
  it('grouped clips move together', () => {
    const p = applyAll(seed(), [op('group', { groupId: 'g1', clipIds: ['c1', 'tx1'] }), op('moveClip', { clipId: 'c1', start: 6 * S })]);
    expect(clip(p, 'tx1').start).toBe(6 * S);
  });
  it('locked tracks reject clip edits', () => {
    const p = apply(seed(), op('setTrack', { trackId: 'v1', patch: { locked: true } }));
    expect(code(() => apply(p, op('trimIn', { clipId: 'c1', delta: 1 })))).toBe('LOCKED');
  });
  it('unknown targets are NOT_FOUND; duplicate ids rejected', () => {
    expect(code(() => apply(seed(), op('removeClip', { clipId: 'nope' })))).toBe('NOT_FOUND');
    expect(code(() => apply(seed(), op('addClip', { trackId: 'v1', clip: { id: 'c1', kind: 'video', assetId: 'vidA', start: 8 * S, duration: S } })))).toBe('DUPLICATE_ID');
  });
});

describe('captions, assets, project', () => {
  it('alignCaptions chunks words; captions never overlap', () => {
    const words = ['We', 'tested', 'it.', 'It', 'held', 'the', 'laptop,', 'charger', 'and', 'shoes.'].map((text, i) => ({ text, start: i * 3000, end: i * 3000 + 2400 }));
    const p = apply(seed(), op('alignCaptions', { trackId: 'cap', words }));
    const caps = p.captions[0]!.captions;
    expect(caps.map((c) => c.words.map((w) => w.text).join(' '))).toEqual(['We tested it.', 'It held the laptop,', 'charger and shoes.']);
    expect(caps[1]!.start).toBe(9000);
    expect(caps[1]!.words[1]!.start).toBe(3000);
    expect(code(() => apply(seed(), op('addCaption', { trackId: 'cap', caption: { id: 'k9', start: 3000, duration: 3000, words: [] } })))).toBe('OVERLAP');
  });
  it('assets are protected while referenced; shrinking one revalidates clips', () => {
    expect(code(() => apply(seed(), op('removeAsset', { assetId: 'vidA' })))).toBe('REFERENCED');
    expect(code(() => apply(seed(), op('setAsset', { assetId: 'vidA', patch: { duration: 6000 } })))).toBe('SOURCE_BOUNDS');
  });
  it('version bumps once per top-level op, duration is derived, batches are atomic', () => {
    const p = seed();
    expect(p.duration).toBe(10 * S);
    const q = apply(p, op('batch', { ops: [op('rippleDelete', { clipId: 'vo' }), op('rippleDelete', { clipId: 'c3' })] }));
    expect(q.version).toBe(p.version + 1);
    expect(q.duration).toBe(4 * S);
    expect(code(() => apply(p, op('batch', { ops: [op('rippleDelete', { clipId: 'c1' }), op('removeClip', { clipId: 'nope' })] }, AGENT)))).toBe('NOT_FOUND');
    expect(ids(p, 'v1')).toEqual(['c1', 'c2', 'c3']);
  });
});

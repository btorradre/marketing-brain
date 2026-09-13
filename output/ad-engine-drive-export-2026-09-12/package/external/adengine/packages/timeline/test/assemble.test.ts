import { describe, expect, it } from 'vitest';
import { assembleFromBoard, assembleFromBoardDetailed, type Board, type VoAlignment } from '../src/assemble.js';
import { sequentialIds } from '../src/ids.js';
import { createProject } from '../src/model.js';
import { apply } from '../src/reducer.js';
import { validateProject } from '../src/schema.js';
import { secondsToTicks } from '../src/time.js';
import { AGENT, S } from './fixture.js';

const board: Board = {
  id: 'board_1',
  lanes: [
    { id: 'reference', name: 'Reference', cards: [{ id: 'r1', t: 0, t_end: 6, script: 'ref beat' }] },
    {
      id: 'ours',
      name: 'Our version',
      cards: [
        { id: 'b2', t: 2, t_end: 4.5, asset_id: 'assetB', script: 'It held the laptop, charger and gym clothes.', in: 1.5 },
        { id: 'b1', t: 0, t_end: 1.8, asset_id: 'assetA', script: 'This bag fits everything.' },
        { id: 'b3', t: 4.5, t_end: 6, asset_id: 'assetC', kind: 'image', script: 'Get yours today.' },
        { id: 'note', t: 0, t_end: 1, script: 'no asset, ignored' },
      ],
    },
  ],
};

const text = 'This bag fits everything. It held the laptop, charger and gym clothes. Get yours today.';
const vo: VoAlignment = {
  asset_id: 'voMain',
  duration: 7,
  words: text.split(' ').map((w, i) => ({ text: w, start: i * 0.45, end: i * 0.45 + 0.4 })),
};

const base = () => createProject({ id: 'p', fps: 30, width: 1080, height: 1920 });

describe('assembleFromBoard', () => {
  it('lays one clip per beat, the VO, and word-aligned captions in one batch', () => {
    const r = assembleFromBoardDetailed(board, vo, { author: AGENT, at: '2026-09-02T00:00:00.000Z', idFactory: sequentialIds() });
    expect(r.op.type).toBe('batch');
    expect(r.op.author).toEqual(AGENT);
    const p = apply(base(), r.op);
    expect(p.version).toBe(1);
    expect(validateProject(p)).toEqual({ ok: true, errors: [] });

    const video = p.tracks.find((t) => t.id === r.videoTrackId)!;
    expect(video.kind).toBe('video');
    expect(video.clips).toHaveLength(3);
    expect(r.beatClipIds).toHaveLength(3);
    expect(video.clips.map((c) => [c.start, c.duration])).toEqual([
      [0, 2 * S], // extended from 1.8s to the next beat
      [2 * S, secondsToTicks(2.5)],
      [secondsToTicks(4.5), secondsToTicks(2.5)], // last beat runs to the VO end (7s)
    ]);
    expect(video.clips[1]).toMatchObject({ kind: 'video', assetId: 'assetB', in: secondsToTicks(1.5), out: secondsToTicks(1.5) + secondsToTicks(2.5) });
    expect(video.clips[2]).toMatchObject({ kind: 'image', assetId: 'assetC', in: 0 });
    expect(p.duration).toBe(7 * S);

    const audio = p.tracks.find((t) => t.id === r.audioTrackId)!;
    expect(audio.kind).toBe('audio');
    expect(audio.clips).toHaveLength(1);
    expect(audio.clips[0]).toMatchObject({ id: r.voClipId, assetId: 'voMain', start: 0, duration: 7 * S });

    expect(p.assets.map((a) => a.id).sort()).toEqual(['assetA', 'assetB', 'assetC', 'voMain']);
    expect(p.assets.find((a) => a.id === 'assetC')!.kind).toBe('image');
    expect(p.markers).toHaveLength(3);
    expect(p.markers.map((m) => m.body)).toEqual(['This bag fits everything.', 'It held the laptop, charger and gym clothes.', 'Get yours today.']);

    const caps = p.captions.find((t) => t.id === r.captionTrackId)!.captions;
    expect(caps.map((c) => c.words.map((w) => w.text).join(' '))).toEqual([
      'This bag fits everything.',
      'It held the laptop,',
      'charger and gym clothes.',
      'Get yours today.',
    ]);
    // alignment: caption start = first word start; word times relative to the caption
    const words = vo.words;
    expect(caps[1]!.start).toBe(secondsToTicks(words[4]!.start));
    expect(caps[1]!.words[2]!.start).toBe(secondsToTicks(words[6]!.start) - secondsToTicks(words[4]!.start));
    expect(caps[1]!.words[2]!.duration).toBe(secondsToTicks(0.4));
    expect(caps[3]!.start + caps[3]!.duration).toBe(secondsToTicks(words[words.length - 1]!.end));
  });

  it('is deterministic with an id factory and picks the lane with assets by name', () => {
    const a = assembleFromBoard(board, vo, { author: AGENT, at: 'x', idFactory: sequentialIds() });
    const b = assembleFromBoard(board, vo, { author: AGENT, at: 'x', idFactory: sequentialIds() });
    expect(a).toEqual(b);
    expect(a.note).toContain('lane ours');
  });

  it('gapPolicy leave keeps the board times', () => {
    const p = apply(base(), assembleFromBoard(board, vo, { author: AGENT, gapPolicy: 'leave', beatMarkers: false, laneId: 'ours' }));
    const video = p.tracks.find((t) => t.kind === 'video')!;
    expect(video.clips.map((c) => [c.start, c.duration])).toEqual([
      [0, secondsToTicks(1.8)],
      [2 * S, secondsToTicks(2.5)],
      [secondsToTicks(4.5), secondsToTicks(1.5)],
    ]);
    expect(p.markers).toHaveLength(0);
  });

  it('reuses tracks and assets of an existing project', () => {
    const existing = apply(base(), assembleFromBoard(board, vo, { author: AGENT, idFactory: sequentialIds() }));
    const cleared = apply(existing, { id: 'x', at: 'x', author: AGENT, type: 'batch', ops: existing.tracks.flatMap((t) => t.clips.map((c) => ({ id: c.id + '_rm', at: 'x', author: AGENT, type: 'removeClip' as const, clipId: c.id }))) });
    const r = assembleFromBoardDetailed(board, vo, { author: AGENT, project: cleared, idFactory: sequentialIds(100) });
    expect(r.op.ops.filter((o) => o.type === 'addTrack' || o.type === 'addAsset' || o.type === 'addCaptionTrack')).toHaveLength(0);
    const p = apply(cleared, r.op);
    expect(p.tracks).toHaveLength(2);
    expect(validateProject(p).ok).toBe(true);
  });

  it('fails loudly on ambiguous lanes or a missing VO asset', () => {
    const ambiguous: Board = { lanes: [{ id: 'a', cards: [{ id: '1', t: 0, t_end: 1, asset_id: 'x' }] }, { id: 'b', cards: [{ id: '2', t: 0, t_end: 1, asset_id: 'y' }] }] };
    expect(() => assembleFromBoard(ambiguous, vo, { author: AGENT })).toThrow(/laneId/);
    expect(() => assembleFromBoard(board, { words: vo.words }, { author: AGENT })).toThrow(/VO asset/);
  });
});

import type { Author, Clip, Project, Track } from '../src/types.js';
import type { Op, OpBase } from '../src/ops.js';
import { createProject, normalizeClip, normalizeTrack } from '../src/model.js';

export const HUMAN: Author = { kind: 'human', id: 'brooks' };
export const AGENT: Author = { kind: 'agent', id: 'editor-1' };

let n = 0;
export function op<T extends Op['type']>(type: T, body: Omit<Extract<Op, { type: T }>, keyof OpBase | 'type'>, author: Author = HUMAN): Extract<Op, { type: T }> {
  n += 1;
  return { id: `op_${n}`, at: '2026-09-02T00:00:00.000Z', author, type, ...body } as unknown as Extract<Op, { type: T }>;
}

export const S = 6000; // one second in ticks

export function seed(): Project {
  const v1: Track = normalizeTrack({
    id: 'v1',
    kind: 'video',
    name: 'Video',
    clips: [
      { id: 'c1', kind: 'video', assetId: 'vidA', start: 0, duration: 2 * S, in: 0, out: 2 * S, keyframes: { opacity: [{ at: 0, value: 0, easing: 'linear' }, { at: S, value: 1, easing: 'hold' }] }, effects: [{ id: 'e1', kind: 'adjust', params: { exposure: 0.2 }, enabled: true }] },
      { id: 'c2', kind: 'video', assetId: 'vidB', start: 2 * S, duration: 2 * S, in: 0, out: 2 * S, linkId: 'L1', transitionOut: { kind: 'dissolve', duration: 600 } },
      { id: 'c3', kind: 'video', assetId: 'vidA', start: 5 * S, duration: S, in: S, out: 2 * S },
    ],
  });
  const a1: Track = normalizeTrack({ id: 'a1', kind: 'audio', name: 'VO', clips: [{ id: 'vo', kind: 'audio', assetId: 'voA', start: 0, duration: 10 * S, in: 0, out: 10 * S, audio: { gain: 0, fadeIn: 0, fadeOut: 600 } }] });
  const a2: Track = normalizeTrack({ id: 'a2', kind: 'audio', name: 'SFX', clips: [{ id: 'c2a', kind: 'audio', assetId: 'vidB', start: 2 * S, duration: 2 * S, in: 0, out: 2 * S, linkId: 'L1' }] });
  const t1: Track = normalizeTrack({
    id: 't1',
    kind: 'text',
    name: 'Text',
    clips: [{ id: 'tx1', kind: 'text', start: 0, duration: S, text: { content: 'Hello', font: 'Inter', size: 64, weight: 700, italic: false, color: '#ffffff', align: 'center', lineHeight: 1.2, letterSpacing: 0, uppercase: false } }],
  });
  const ov: Track = normalizeTrack({ id: 'ov', kind: 'overlay', name: 'Overlay', clips: [{ id: 'img1', kind: 'image', assetId: 'imgC', start: 3 * S, duration: S }] });
  return createProject({
    id: 'proj_1',
    name: 'Seed',
    fps: 30,
    width: 1080,
    height: 1920,
    assets: [
      { id: 'vidA', kind: 'video', duration: 10 * S, fps: 30 },
      { id: 'vidB', kind: 'video', duration: 10 * S },
      { id: 'voA', kind: 'audio', duration: 20 * S },
      { id: 'imgC', kind: 'image' },
    ],
    tracks: [v1, a1, a2, t1, ov],
    markers: [{ id: 'm1', at: S, kind: 'note', author: HUMAN, body: 'hook lands here' }],
    captions: [
      {
        id: 'cap',
        name: 'Captions',
        enabled: true,
        style: { font: 'Inter', size: 64, weight: 800, color: '#ffffff', mode: 'karaoke', uppercase: false },
        placement: { anchor: 'bottom', y: 0.78, x: 0.5, safeZone: true, scrimAware: true },
        captions: [
          { id: 'k1', start: 0, duration: S, words: [{ text: 'Hello', start: 0, duration: 3000 }, { text: 'there', start: 3000, duration: 3000 }] },
          { id: 'k2', start: S, duration: S, words: [{ text: 'friend', start: 0, duration: S }] },
        ],
      },
    ],
  });
}

export function clip(p: Project, id: string): Clip {
  for (const t of p.tracks) for (const c of t.clips) if (c.id === id) return c;
  throw new Error(`no clip ${id}`);
}

export function ids(p: Project, trackId: string): string[] {
  return p.tracks.find((t) => t.id === trackId)!.clips.map((c) => c.id);
}

export { normalizeClip };

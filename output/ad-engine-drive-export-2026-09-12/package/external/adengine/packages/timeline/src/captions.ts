/** Word-level caption chunking shared by the alignCaptions op and assembleFromBoard. */
import type { AlignedWord, CaptionChunkOptions } from './ops.js';
import { TICK_RATE, type Caption } from './types.js';

export const DEFAULT_CHUNK: Required<CaptionChunkOptions> = {
  maxWords: 4,
  maxDuration: Math.round(2.5 * TICK_RATE),
  breakOnPunctuation: true,
  gapBreak: Math.round(0.6 * TICK_RATE),
};

const SENTENCE_END = /[.!?…]["')\]]?$/;

/**
 * Group absolute-timed words into non-overlapping captions. Deterministic:
 * caption ids are `${idPrefix}-${index}`. Word times inside a caption are
 * relative to the caption start.
 */
export function chunkWords(words: readonly AlignedWord[], options: CaptionChunkOptions | undefined, idPrefix: string): Caption[] {
  const o = { ...DEFAULT_CHUNK, ...(options ?? {}) };
  const sorted = [...words].filter((w) => w.text.trim().length > 0).sort((a, b) => a.start - b.start);
  const out: Caption[] = [];
  let group: AlignedWord[] = [];

  const flush = () => {
    if (group.length === 0) return;
    const start = group[0]!.start;
    const end = Math.max(...group.map((w) => w.end));
    out.push({
      id: `${idPrefix}-${out.length}`,
      start,
      duration: Math.max(1, end - start),
      words: group.map((w) => ({ text: w.text, start: w.start - start, duration: Math.max(1, w.end - w.start) })),
    });
    group = [];
  };

  for (const w of sorted) {
    if (group.length > 0) {
      const first = group[0]!;
      const prev = group[group.length - 1]!;
      const wouldExceedWords = group.length >= o.maxWords;
      const wouldExceedSpan = w.end - first.start > o.maxDuration;
      const gap = w.start - prev.end > o.gapBreak;
      const punct = o.breakOnPunctuation && SENTENCE_END.test(prev.text);
      if (wouldExceedWords || wouldExceedSpan || gap || punct) flush();
    }
    group.push(w);
  }
  flush();

  // Guarantee non-overlap even with sloppy alignments: clamp each caption to the next one's start.
  for (let i = 0; i + 1 < out.length; i++) {
    const a = out[i]!;
    const b = out[i + 1]!;
    if (a.start + a.duration > b.start) a.duration = Math.max(1, b.start - a.start);
  }
  return out;
}

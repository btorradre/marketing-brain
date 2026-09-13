/**
 * assembleFromBoard: the first agent editing workflow. Approved storyboard
 * board + VO alignment -> one batch op that lays one clip per beat on a video
 * track, the VO on an audio track, and a word-aligned caption track.
 *
 * Laws carried (see PRODUCTIZATION-PLAN section 8.4): storyboard first; product
 * on screen the entire ad (gaps between beats are filled by extending the
 * previous beat, and the last beat runs to the end of the VO); b-roll in-point
 * is the card's `in` offset so the beat opens on the action.
 */
import { OpError } from './errors.js';
import { newId, nowIso } from './ids.js';
import { DEFAULT_CAPTION_PLACEMENT, DEFAULT_CAPTION_STYLE } from './model.js';
import type { BatchOp, CaptionChunkOptions, ClipInit, Op } from './ops.js';
import { secondsToTicks } from './time.js';
import type { AssetKind, Author, CaptionPlacement, CaptionStyle, ClipKind, Project, Tick } from './types.js';

export interface BoardCard {
  id: string;
  /** Beat start, seconds. */
  t: number;
  /** Beat end, seconds. */
  t_end: number;
  asset_id?: string;
  script?: string;
  /** 'video' | 'image' | 'broll' | 'ugc' | 'label' | ... free-form; only image-ish kinds change clip kind. */
  kind?: string;
  /** Source in-point, seconds (b-roll in-point shows the action). Default 0. */
  in?: number;
  label?: string;
}

export interface BoardLane {
  id: string;
  name?: string;
  kind?: string;
  cards: BoardCard[];
}

export interface Board {
  id?: string;
  title?: string;
  lanes: BoardLane[];
}

export interface VoWord {
  text: string;
  /** seconds */
  start: number;
  /** seconds */
  end: number;
}

export interface VoAlignment {
  words: VoWord[];
  asset_id?: string;
  /** VO length, seconds. Default: end of the last word. */
  duration?: number;
}

export interface AssembleOptions {
  author: Author;
  at?: string;
  /** Deterministic ids for tests/reproducible runs. */
  idFactory?: (prefix: string) => string;
  /** Assemble into this project: existing tracks/assets are reused instead of re-created. */
  project?: Project;
  /** Lane to take beats from. Required when more than one lane carries asset cards. */
  laneId?: string;
  videoTrackId?: string;
  audioTrackId?: string;
  captionTrackId?: string;
  /** VO asset id; overrides vo.asset_id. */
  voAssetId?: string;
  /** Where the VO starts on the timeline, seconds. Default 0. Beat times are NOT offset. */
  voStart?: number;
  /** 'extend' (default): each beat runs to the next beat's start, the last to the VO end. 'leave': keep t/t_end. */
  gapPolicy?: 'extend' | 'leave';
  captionStyle?: Partial<CaptionStyle>;
  captionPlacement?: Partial<CaptionPlacement>;
  captionChunk?: CaptionChunkOptions;
  /** Add a note marker per beat carrying the card's script. Default true. */
  beatMarkers?: boolean;
  /** Asset kinds by asset id when known; otherwise inferred from card.kind. */
  assetKinds?: Record<string, AssetKind>;
}

export interface AssembleResult {
  op: BatchOp;
  videoTrackId: string;
  audioTrackId: string;
  captionTrackId: string;
  beatClipIds: string[];
  voClipId: string;
  /** Timeline end in ticks after the batch applies (max of beats and VO). */
  end: Tick;
}

const IMAGE_KINDS = new Set(['image', 'still', 'photo', 'static']);

function pickLane(board: Board, laneId: string | undefined): BoardLane {
  if (laneId) {
    const lane = board.lanes.find((l) => l.id === laneId);
    if (!lane) throw new OpError('NOT_FOUND', `lane ${laneId} not on board`);
    return lane;
  }
  const withAssets = board.lanes.filter((l) => l.cards.some((c) => c.asset_id));
  if (withAssets.length === 1) return withAssets[0]!;
  if (withAssets.length === 0) throw new OpError('INVALID_OP', `board has no lane with asset cards`);
  const ours = withAssets.find((l) => /\b(ours?|target|ourversion|our_version)\b/i.test(`${l.kind ?? ''} ${l.name ?? ''} ${l.id}`));
  if (ours) return ours;
  throw new OpError('INVALID_OP', `board has ${withAssets.length} lanes with asset cards; pass options.laneId`);
}

export function assembleFromBoardDetailed(board: Board, vo: VoAlignment, options: AssembleOptions): AssembleResult {
  const id = options.idFactory ?? newId;
  const at = options.at ?? nowIso();
  const author = options.author;
  const project = options.project;
  const gapPolicy = options.gapPolicy ?? 'extend';
  const ops: Op[] = [];
  const mk = <T extends Op['type']>(type: T, body: Omit<Extract<Op, { type: T }>, 'id' | 'at' | 'author' | 'type'>): Op =>
    ({ id: id('op'), at, author, type, ...body }) as unknown as Op;

  // --- beats
  const lane = pickLane(board, options.laneId);
  const cards = lane.cards
    .filter((c) => c.asset_id && Number.isFinite(c.t) && Number.isFinite(c.t_end) && c.t_end > c.t)
    .sort((a, b) => a.t - b.t);
  if (cards.length === 0) throw new OpError('INVALID_OP', `lane ${lane.id} has no timed asset cards`);

  const voAssetId = options.voAssetId ?? vo.asset_id;
  if (!voAssetId) throw new OpError('INVALID_OP', `VO asset id missing (vo.asset_id or options.voAssetId)`);
  const voStart = secondsToTicks(options.voStart ?? 0);
  const voLen = secondsToTicks(vo.duration ?? Math.max(0, ...vo.words.map((w) => w.end)));
  if (voLen < 1) throw new OpError('INVALID_RANGE', `VO has no duration`);
  const voEnd = voStart + voLen;

  // --- assets
  const known = new Set((project?.assets ?? []).map((a) => a.id));
  const addAsset = (assetId: string, kind: AssetKind, duration?: Tick) => {
    if (known.has(assetId)) return;
    known.add(assetId);
    const asset = duration === undefined ? { id: assetId, kind } : { id: assetId, kind, duration };
    ops.push(mk('addAsset', { asset }));
  };
  for (const c of cards) {
    const kind: AssetKind = options.assetKinds?.[c.asset_id!] ?? (IMAGE_KINDS.has((c.kind ?? '').toLowerCase()) ? 'image' : 'video');
    addAsset(c.asset_id!, kind);
  }
  addAsset(voAssetId, 'audio', voLen);

  // --- tracks
  const findTrack = (kind: 'video' | 'audio', wanted: string | undefined) =>
    project?.tracks.find((t) => (wanted ? t.id === wanted : t.kind === kind))?.id;
  let videoTrackId = findTrack('video', options.videoTrackId);
  if (!videoTrackId) {
    videoTrackId = options.videoTrackId ?? id('track');
    ops.push(mk('addTrack', { track: { id: videoTrackId, kind: 'video', name: 'Video' }, index: 0 }));
  }
  let audioTrackId = findTrack('audio', options.audioTrackId);
  if (!audioTrackId) {
    audioTrackId = options.audioTrackId ?? id('track');
    ops.push(mk('addTrack', { track: { id: audioTrackId, kind: 'audio', name: 'VO' } }));
  }
  let captionTrackId = project?.captions.find((t) => (options.captionTrackId ? t.id === options.captionTrackId : true))?.id;
  if (!captionTrackId) {
    captionTrackId = options.captionTrackId ?? id('captions');
    ops.push(
      mk('addCaptionTrack', {
        track: {
          id: captionTrackId,
          name: 'Captions',
          style: { ...DEFAULT_CAPTION_STYLE, ...(options.captionStyle ?? {}) },
          placement: { ...DEFAULT_CAPTION_PLACEMENT, ...(options.captionPlacement ?? {}) },
        },
      }),
    );
  } else if (options.captionStyle || options.captionPlacement) {
    const existing = project!.captions.find((t) => t.id === captionTrackId)!;
    ops.push(
      mk('setCaptionTrack', {
        trackId: captionTrackId,
        patch: {
          ...(options.captionStyle ? { style: { ...existing.style, ...options.captionStyle } } : {}),
          ...(options.captionPlacement ? { placement: { ...existing.placement, ...options.captionPlacement } } : {}),
        },
      }),
    );
  }

  // --- one clip per beat
  const beatClipIds: string[] = [];
  let end = voEnd;
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i]!;
    const next = cards[i + 1];
    const start = secondsToTicks(card.t);
    const nextStart = next ? secondsToTicks(next.t) : undefined;
    let clipEnd: Tick;
    if (gapPolicy === 'extend') clipEnd = nextStart ?? Math.max(secondsToTicks(card.t_end), voEnd);
    else clipEnd = Math.min(secondsToTicks(card.t_end), nextStart ?? Number.MAX_SAFE_INTEGER);
    const duration = clipEnd - start;
    if (duration < 1) throw new OpError('INVALID_RANGE', `card ${card.id} has no duration after layout (${start}..${clipEnd})`);
    const kind: ClipKind = IMAGE_KINDS.has((card.kind ?? '').toLowerCase()) ? 'image' : 'video';
    const clipId = id('clip');
    const inTick = kind === 'video' ? secondsToTicks(card.in ?? 0) : 0;
    const clip: ClipInit = { id: clipId, kind, assetId: card.asset_id!, start, duration, in: inTick, out: kind === 'video' ? inTick + duration : duration };
    const name = card.label ?? card.script?.slice(0, 48);
    if (name) clip.name = name;
    ops.push(mk('addClip', { trackId: videoTrackId, clip }));
    beatClipIds.push(clipId);
    end = Math.max(end, clipEnd);
    if (options.beatMarkers ?? true) {
      ops.push(mk('addMarker', { marker: { id: id('marker'), at: start, kind: 'note', author, body: card.script ?? card.label ?? card.id, clipId } }));
    }
  }

  // --- VO
  const voClipId = id('clip');
  ops.push(
    mk('addClip', {
      trackId: audioTrackId,
      clip: { id: voClipId, kind: 'audio', assetId: voAssetId, start: voStart, duration: voLen, in: 0, out: voLen, name: 'VO', audio: { gain: 0, fadeIn: 0, fadeOut: 0 } },
    }),
  );

  // --- captions from words
  const words = vo.words
    .filter((w) => w.text.trim().length > 0)
    .map((w) => ({ text: w.text, start: voStart + secondsToTicks(w.start), end: voStart + secondsToTicks(Math.max(w.end, w.start)) }));
  ops.push(mk('alignCaptions', { trackId: captionTrackId, words, ...(options.captionChunk ? { options: options.captionChunk } : {}) }));

  const op: BatchOp = { id: id('op'), at, author, type: 'batch', ops, note: `assemble_from_board${board.id ? ` ${board.id}` : ''} lane ${lane.id}` };
  return { op, videoTrackId, audioTrackId, captionTrackId, beatClipIds, voClipId, end };
}

/** The batch op that assembles the board. See assembleFromBoardDetailed for the ids it creates. */
export function assembleFromBoard(board: Board, vo: VoAlignment, options: AssembleOptions): BatchOp {
  return assembleFromBoardDetailed(board, vo, options).op;
}

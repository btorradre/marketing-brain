/**
 * The typed operation set. Every UI gesture and every agent tool call is one
 * of these. Ops are the unit of the event log, of undo, and of the future
 * CRDT layer (see README).
 */
import type {
  AssetRef,
  AudioProps,
  Author,
  BlendMode,
  Caption,
  CaptionPlacement,
  CaptionStyle,
  CaptionTrack,
  Chroma,
  Clip,
  ClipKind,
  Crop,
  Effect,
  Keyframe,
  Marker,
  Mask,
  TextStyle,
  Tick,
  Track,
  TrackKind,
  Transform,
  Transition,
} from './types.js';

export interface OpBase {
  /** Unique op id (uuid). */
  id: string;
  /** ISO-8601 wall-clock time the op was issued. */
  at: string;
  author: Author;
  /** Set on undo/redo ops: the id of the op this one reverses. */
  undoes?: string;
  /** Free-text intent, e.g. the agent's reason. Not interpreted. */
  note?: string;
}

/**
 * How an insertion/move resolves clips already occupying the target range.
 *  - reject    (default) throw OVERLAP; nothing changes.
 *  - ripple    magnetic insert: clips starting at/after the insert point shift right by the inserted duration.
 *              The insert point must be a clip boundary or inside a gap (split first otherwise).
 *  - overwrite trim/remove what is under the new clip (a clip that fully contains the range must be split first).
 */
export type OverlapMode = 'reject' | 'ripple' | 'overwrite';

/** Minimal clip input; the reducer fills defaults (transform, crop, blend, keyframes, effects, speed, in/out). */
export interface ClipInit extends Partial<Omit<Clip, 'id' | 'kind' | 'start' | 'duration'>> {
  id: string;
  kind: ClipKind;
  start: Tick;
  duration: Tick;
}

export interface TrackInit extends Partial<Omit<Track, 'id' | 'kind' | 'clips'>> {
  id: string;
  kind: TrackKind;
  clips?: ClipInit[];
}

export interface CaptionTrackInit extends Partial<Omit<CaptionTrack, 'id'>> {
  id: string;
}

/** Word with ABSOLUTE tick times, as produced by a VO alignment. */
export interface AlignedWord {
  text: string;
  start: Tick;
  end: Tick;
}

export interface CaptionChunkOptions {
  /** Max words per caption line. Default 4. */
  maxWords?: number;
  /** Max caption span in ticks. Default 2.5 s. */
  maxDuration?: Tick;
  /** Start a new caption after a word ending in . ! ? Default true. */
  breakOnPunctuation?: boolean;
  /** Start a new caption when the silence between words exceeds this. Default 0.6 s. */
  gapBreak?: Tick;
}

/** Patch semantics: a key set to null clears an optional field; absent keys are untouched. */
export interface ClipPatch {
  name?: string | null;
  assetId?: string | null;
  crop?: Crop;
  blend?: BlendMode;
  mask?: Mask | null;
  transitionIn?: Transition | null;
  transitionOut?: Transition | null;
  freeze?: Tick | null;
}

export interface TrackPatch {
  name?: string;
  locked?: boolean;
  muted?: boolean;
  /** Move the track to this compositing index. */
  index?: number;
}

export interface CaptionPatch {
  start?: Tick;
  duration?: Tick;
  words?: Caption['words'];
  style?: Partial<CaptionStyle> | null;
  placement?: Partial<CaptionPlacement> | null;
}

export interface CaptionTrackPatch {
  name?: string;
  enabled?: boolean;
  style?: CaptionStyle;
  placement?: CaptionPlacement;
}

export interface MarkerPatch {
  at?: Tick;
  kind?: Marker['kind'];
  body?: string;
  clipId?: string | null;
  resolved?: Marker['resolved'] | null;
}

export interface ProjectPatch {
  name?: string | null;
  fps?: number;
  width?: number;
  height?: number;
  styleRef?: string | null;
}

export interface AssetPatch extends Partial<Omit<AssetRef, 'id'>> {}

// ---- Tracks ---------------------------------------------------------------

export interface AddTrackOp extends OpBase {
  type: 'addTrack';
  track: TrackInit;
  /** Compositing index; default appends on top. */
  index?: number;
}
export interface RemoveTrackOp extends OpBase {
  type: 'removeTrack';
  trackId: string;
}
export interface SetTrackOp extends OpBase {
  type: 'setTrack';
  trackId: string;
  patch: TrackPatch;
}
/** Snapshot fallback: replace a track's clip list wholesale. Used as the inverse of `overwrite` placements. */
export interface SetTrackClipsOp extends OpBase {
  type: 'setTrackClips';
  trackId: string;
  clips: Clip[];
}

// ---- Clips ----------------------------------------------------------------

export interface AddClipOp extends OpBase {
  type: 'addClip';
  trackId: string;
  clip: ClipInit;
  overlap?: OverlapMode;
}
/** Lift: remove the clip and leave a gap. */
export interface RemoveClipOp extends OpBase {
  type: 'removeClip';
  clipId: string;
}
/** Extract: remove the clip and close the gap (clips after it on the track shift left). */
export interface RippleDeleteOp extends OpBase {
  type: 'rippleDelete';
  clipId: string;
}
export interface MoveClipOp extends OpBase {
  type: 'moveClip';
  clipId: string;
  start: Tick;
  /** Target track; default stays. */
  trackId?: string;
  /** 'ripple' is not supported for moves (rippleDelete + addClip instead). */
  overlap?: Exclude<OverlapMode, 'ripple'>;
  /** Move only this clip, leaving linked/grouped companions in place. */
  solo?: boolean;
}
/**
 * Trim the head. `delta` > 0 removes `delta` ticks from the start; < 0 extends.
 * Non-ripple: start moves by delta. Ripple: start stays, later clips on the track shift by -delta.
 */
export interface TrimInOp extends OpBase {
  type: 'trimIn';
  clipId: string;
  delta: Tick;
  ripple?: boolean;
}
/** Trim the tail. `delta` > 0 extends the end by delta ticks; < 0 shortens. Ripple shifts later clips by +delta. */
export interface TrimOutOp extends OpBase {
  type: 'trimOut';
  clipId: string;
  delta: Tick;
  ripple?: boolean;
}
export interface SplitOp extends OpBase {
  type: 'split';
  clipId: string;
  /** Absolute tick strictly inside the clip. */
  tick: Tick;
  /** Id for the right-hand piece. The left piece keeps `clipId`. */
  newClipId: string;
}
/** Merge two adjacent, source-contiguous pieces of one clip. Inverse of split. */
export interface JoinOp extends OpBase {
  type: 'join';
  leftId: string;
  rightId: string;
}
/** Move the edit point between this clip and its adjacent right neighbor. Total length unchanged. */
export interface RollOp extends OpBase {
  type: 'roll';
  clipId: string;
  delta: Tick;
}
/** Shift the source range without moving the clip. delta > 0 shows later source content. */
export interface SlipOp extends OpBase {
  type: 'slip';
  clipId: string;
  delta: Tick;
}
/**
 * Move the clip by delta, trimming its adjacent neighbors so the total length is unchanged.
 * leftId/rightId: undefined = auto-detect adjacent neighbors; null = none; string = that clip.
 */
export interface SlideOp extends OpBase {
  type: 'slide';
  clipId: string;
  delta: Tick;
  leftId?: string | null;
  rightId?: string | null;
}
/** Change speed; timeline duration becomes round(sourceLength / speed) unless `duration` is given. */
export interface SetSpeedOp extends OpBase {
  type: 'setSpeed';
  clipId: string;
  speed: number;
  duration?: Tick;
  ripple?: boolean;
}
export interface ReverseOp extends OpBase {
  type: 'reverse';
  clipId: string;
  reverse: boolean;
}
/** Split at `at`, insert a frozen still of `freezeDuration`, ripple the rest of the track right. */
export interface FreezeFrameOp extends OpBase {
  type: 'freezeFrame';
  clipId: string;
  tick: Tick;
  freezeDuration: Tick;
  frozenClipId: string;
  rightClipId: string;
}
export interface SetClipOp extends OpBase {
  type: 'setClip';
  clipId: string;
  patch: ClipPatch;
}
export interface SetTransformOp extends OpBase {
  type: 'setTransform';
  clipId: string;
  transform: Partial<Transform>;
}
/** Upsert a keyframe (unique by `at` within a prop). */
export interface SetKeyframeOp extends OpBase {
  type: 'setKeyframe';
  clipId: string;
  prop: string;
  keyframe: Keyframe;
}
export interface RemoveKeyframeOp extends OpBase {
  type: 'removeKeyframe';
  clipId: string;
  prop: string;
  tick: Tick;
}
/** Upsert an effect by id. */
export interface SetEffectOp extends OpBase {
  type: 'setEffect';
  clipId: string;
  effect: Effect;
}
export interface RemoveEffectOp extends OpBase {
  type: 'removeEffect';
  clipId: string;
  effectId: string;
}
export interface SetChromaOp extends OpBase {
  type: 'setChroma';
  clipId: string;
  chroma: Chroma | null;
}
export interface SetTextOp extends OpBase {
  type: 'setText';
  clipId: string;
  text: TextStyle | null;
}
export interface SetAudioOp extends OpBase {
  type: 'setAudio';
  clipId: string;
  audio: AudioProps | null;
}
export interface LinkAudioOp extends OpBase {
  type: 'linkAudio';
  linkId: string;
  /** One video/image clip and one audio clip (any count >= 2 accepted for restore). */
  clipIds: string[];
}
export interface UnlinkOp extends OpBase {
  type: 'unlink';
  linkId: string;
}
export interface GroupOp extends OpBase {
  type: 'group';
  groupId: string;
  clipIds: string[];
}
export interface UngroupOp extends OpBase {
  type: 'ungroup';
  groupId: string;
}

// ---- Captions -------------------------------------------------------------

export interface AddCaptionTrackOp extends OpBase {
  type: 'addCaptionTrack';
  track: CaptionTrackInit;
  /** Position among caption tracks; default appends. */
  index?: number;
}
export interface RemoveCaptionTrackOp extends OpBase {
  type: 'removeCaptionTrack';
  trackId: string;
}
export interface SetCaptionTrackOp extends OpBase {
  type: 'setCaptionTrack';
  trackId: string;
  patch: CaptionTrackPatch;
}
export interface AddCaptionOp extends OpBase {
  type: 'addCaption';
  trackId: string;
  caption: Caption;
}
export interface SetCaptionOp extends OpBase {
  type: 'setCaption';
  trackId: string;
  captionId: string;
  patch: CaptionPatch;
}
export interface RemoveCaptionOp extends OpBase {
  type: 'removeCaption';
  trackId: string;
  captionId: string;
}
/** Regenerate a caption track's captions from word-level alignment. Replaces existing captions. */
export interface AlignCaptionsOp extends OpBase {
  type: 'alignCaptions';
  trackId: string;
  words: AlignedWord[];
  options?: CaptionChunkOptions;
}
/** Snapshot fallback: replace a caption track's captions wholesale. Inverse of alignCaptions. */
export interface SetCaptionsOp extends OpBase {
  type: 'setCaptions';
  trackId: string;
  captions: Caption[];
}

// ---- Markers --------------------------------------------------------------

export interface AddMarkerOp extends OpBase {
  type: 'addMarker';
  marker: Marker;
  /** Position in the marker list; default appends. */
  index?: number;
}
export interface SetMarkerOp extends OpBase {
  type: 'setMarker';
  markerId: string;
  patch: MarkerPatch;
}
export interface RemoveMarkerOp extends OpBase {
  type: 'removeMarker';
  markerId: string;
}
/** resolved: true stamps {by: op.author, at: op.at}; false clears. */
export interface ResolveMarkerOp extends OpBase {
  type: 'resolveMarker';
  markerId: string;
  resolved: boolean;
}

// ---- Project / assets -----------------------------------------------------

export interface SetProjectSettingsOp extends OpBase {
  type: 'setProjectSettings';
  patch: ProjectPatch;
}
export interface AddAssetOp extends OpBase {
  type: 'addAsset';
  asset: AssetRef;
  /** Position in the asset list; default appends. */
  index?: number;
}
export interface SetAssetOp extends OpBase {
  type: 'setAsset';
  assetId: string;
  patch: AssetPatch;
}
/** Rejected (REFERENCED) while any clip uses the asset. */
export interface RemoveAssetOp extends OpBase {
  type: 'removeAsset';
  assetId: string;
}

// ---- Batch ----------------------------------------------------------------

/** Applied atomically and in order; bumps the project version once. */
export interface BatchOp extends OpBase {
  type: 'batch';
  ops: Op[];
}

export type Op =
  | AddTrackOp
  | RemoveTrackOp
  | SetTrackOp
  | SetTrackClipsOp
  | AddClipOp
  | RemoveClipOp
  | RippleDeleteOp
  | MoveClipOp
  | TrimInOp
  | TrimOutOp
  | SplitOp
  | JoinOp
  | RollOp
  | SlipOp
  | SlideOp
  | SetSpeedOp
  | ReverseOp
  | FreezeFrameOp
  | SetClipOp
  | SetTransformOp
  | SetKeyframeOp
  | RemoveKeyframeOp
  | SetEffectOp
  | RemoveEffectOp
  | SetChromaOp
  | SetTextOp
  | SetAudioOp
  | LinkAudioOp
  | UnlinkOp
  | GroupOp
  | UngroupOp
  | AddCaptionTrackOp
  | RemoveCaptionTrackOp
  | SetCaptionTrackOp
  | AddCaptionOp
  | SetCaptionOp
  | RemoveCaptionOp
  | AlignCaptionsOp
  | SetCaptionsOp
  | AddMarkerOp
  | SetMarkerOp
  | RemoveMarkerOp
  | ResolveMarkerOp
  | SetProjectSettingsOp
  | AddAssetOp
  | SetAssetOp
  | RemoveAssetOp
  | BatchOp;

export type OpType = Op['type'];

/** Every op type, for exhaustiveness checks in tests and tool registries. */
export const OP_TYPES = [
  'addTrack',
  'removeTrack',
  'setTrack',
  'setTrackClips',
  'addClip',
  'removeClip',
  'rippleDelete',
  'moveClip',
  'trimIn',
  'trimOut',
  'split',
  'join',
  'roll',
  'slip',
  'slide',
  'setSpeed',
  'reverse',
  'freezeFrame',
  'setClip',
  'setTransform',
  'setKeyframe',
  'removeKeyframe',
  'setEffect',
  'removeEffect',
  'setChroma',
  'setText',
  'setAudio',
  'linkAudio',
  'unlink',
  'group',
  'ungroup',
  'addCaptionTrack',
  'removeCaptionTrack',
  'setCaptionTrack',
  'addCaption',
  'setCaption',
  'removeCaption',
  'alignCaptions',
  'setCaptions',
  'addMarker',
  'setMarker',
  'removeMarker',
  'resolveMarker',
  'setProjectSettings',
  'addAsset',
  'setAsset',
  'removeAsset',
  'batch',
] as const satisfies readonly OpType[];

// Compile-time check that OP_TYPES covers the union exactly.
type _Missing = Exclude<OpType, (typeof OP_TYPES)[number]>;
const _assertComplete: _Missing extends never ? true : never = true;
void _assertComplete;

export type OpOfType<T extends OpType> = Extract<Op, { type: T }>;

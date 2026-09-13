/**
 * Timeline document model.
 *
 * TIME: every time value in this document is an integer number of ticks at
 * TICK_RATE ticks per second. 6000 ticks/s is exact for 24, 25, 30, 48, 50,
 * 60, 120 and 240 fps (one frame is an integer tick count) and exact for
 * milliseconds (1 ms = 6 ticks), so word alignments in ms and frame indices
 * both convert without rounding. NTSC fractional rates (29.97, 23.976) are
 * not exact and round to the nearest tick; see README "Tick rate".
 *
 * Source offsets (Clip.in / Clip.out / Clip.freeze) are also ticks, measured
 * in the asset's own time. Keyframe and caption-word times are RELATIVE to
 * the owning clip / caption start. Everything else is absolute timeline ticks.
 */

export const TICK_RATE = 6000;

/** Integer tick count. Never a float. */
export type Tick = number;

export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export interface Author {
  kind: 'human' | 'agent';
  id: string;
}

export type TrackKind = 'video' | 'audio' | 'overlay' | 'text' | 'caption' | 'label';
export type ClipKind = 'video' | 'audio' | 'image' | 'text' | 'shape' | 'caption';
export type AssetKind = 'video' | 'audio' | 'image' | 'font' | 'lut' | 'other';

/** Reference to media. The document never carries a filesystem path; media moves by id or URL. */
export interface AssetRef {
  id: string;
  kind: AssetKind;
  name?: string;
  url?: string;
  storageKey?: string;
  mime?: string;
  /** Source length in ticks, when known. Enables source-bounds validation. */
  duration?: Tick;
  width?: number;
  height?: number;
  fps?: number;
  sampleRate?: number;
  proxyUrl?: string;
  thumbnailUrl?: string;
  waveformUrl?: string;
  provenance?: { jobId?: string; source?: string };
}

export type EasingName = 'linear' | 'easeIn' | 'easeOut' | 'easeInOut' | 'hold';
export type Easing = EasingName | { type: 'bezier'; c: [number, number, number, number] };
export type KeyframeValue = number | string | boolean | number[];

export interface Keyframe {
  /** Relative to the owning clip's start. */
  at: Tick;
  value: KeyframeValue;
  /** Easing from this keyframe to the next. */
  easing: Easing;
}

export interface Transform {
  /** Normalized offset from canvas center, -1..1 across the canvas dimension. */
  x: number;
  y: number;
  scale: number;
  /** Degrees. */
  rotation: number;
  /** 0..1 */
  opacity: number;
  /** Anchor point in clip-normalized coordinates, 0..1 (0.5,0.5 = center). */
  anchor: { x: number; y: number };
}

/** Fractions 0..1 cut from each edge. */
export interface Crop {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export type BlendMode =
  | 'normal'
  | 'multiply'
  | 'screen'
  | 'overlay'
  | 'darken'
  | 'lighten'
  | 'colorDodge'
  | 'colorBurn'
  | 'hardLight'
  | 'softLight'
  | 'difference'
  | 'exclusion'
  | 'hue'
  | 'saturation'
  | 'color'
  | 'luminosity';

export interface Effect {
  id: string;
  /** e.g. 'adjust', 'blur', 'pixelate', 'lut', 'filter:<name>' */
  kind: string;
  params: Record<string, JsonValue>;
  enabled: boolean;
}

export interface Mask {
  shape: 'rect' | 'ellipse' | 'linear' | 'mirror' | 'path';
  feather: number;
  invert: boolean;
  params: Record<string, JsonValue>;
}

export interface Chroma {
  /** Key color as #rrggbb. */
  color: string;
  /** 0..1 */
  similarity: number;
  /** 0..1 */
  blend: number;
  /** 0..1 */
  despill: number;
  /** 0..1 edge softness/shrink. */
  edge: number;
}

export interface TextShadow {
  color: string;
  x: number;
  y: number;
  blur: number;
}
export interface TextOutline {
  color: string;
  width: number;
}
export interface TextBackground {
  color: string;
  padding: number;
  radius: number;
}
export interface TextAnimation {
  kind: string;
  duration: Tick;
  params?: Record<string, JsonValue>;
}

export interface TextStyle {
  content: string;
  font: string;
  size: number;
  weight: number;
  italic: boolean;
  color: string;
  align: 'left' | 'center' | 'right';
  lineHeight: number;
  letterSpacing: number;
  uppercase: boolean;
  shadow?: TextShadow;
  outline?: TextOutline;
  background?: TextBackground;
  animateIn?: TextAnimation;
  animateOut?: TextAnimation;
  /** Brand preset id this style was derived from. */
  preset?: string;
}

export interface Duck {
  /** Track whose audio triggers the duck (typically the VO track). */
  sourceTrackId?: string;
  /** dB reduction while the source is active. */
  amount: number;
  attack: Tick;
  release: Tick;
}

export interface AudioProps {
  /** dB. */
  gain: number;
  fadeIn: Tick;
  fadeOut: Tick;
  duck?: Duck;
}

export type TransitionKind = 'cut' | 'dissolve' | 'dipToColor' | 'push' | 'slide' | 'zoom';

export interface Transition {
  kind: TransitionKind | string;
  duration: Tick;
  params?: Record<string, JsonValue>;
}

export interface Clip {
  id: string;
  /** Required for video/audio/image clips; absent for text/shape/caption. */
  assetId?: string;
  kind: ClipKind;
  name?: string;
  /** Absolute timeline tick. */
  start: Tick;
  /** Timeline ticks; >= 1. */
  duration: Tick;
  /**
   * Source range in asset ticks. Media clips play [in, out) at `speed`
   * (backwards when `reverse`). Non-media clips (image/text/shape/caption)
   * keep in = 0 and out = duration by convention.
   */
  in: Tick;
  out: Tick;
  /** Playback multiplier; > 0. Duration ~= (out - in) / speed for media. */
  speed: number;
  reverse: boolean;
  /** When set, the clip shows this single source tick for its whole duration (freeze frame). */
  freeze?: Tick;
  transform: Transform;
  crop: Crop;
  blend: BlendMode;
  /** prop -> keyframes (sorted by `at`, unique `at`). Empty arrays are never stored. */
  keyframes: Record<string, Keyframe[]>;
  effects: Effect[];
  mask?: Mask;
  chroma?: Chroma;
  text?: TextStyle;
  audio?: AudioProps;
  transitionIn?: Transition;
  transitionOut?: Transition;
  /** Clips sharing a linkId move together (video + its audio). */
  linkId?: string;
  /** Clips sharing a groupId move together. */
  groupId?: string;
}

export interface Track {
  id: string;
  kind: TrackKind;
  name: string;
  locked: boolean;
  muted: boolean;
  /** Always sorted by start; never overlapping. */
  clips: Clip[];
}

export interface CaptionWord {
  text: string;
  /** Relative to the owning caption's start. */
  start: Tick;
  duration: Tick;
}

export interface CaptionStyle {
  preset?: string;
  font: string;
  size: number;
  weight: number;
  color: string;
  /** Word being spoken, in 'word' / 'karaoke' modes. */
  highlightColor?: string;
  /** line = whole line shown; word = one word at a time; karaoke = line shown, spoken word highlighted. */
  mode: 'line' | 'word' | 'karaoke';
  uppercase: boolean;
  outline?: TextOutline;
  shadow?: TextShadow;
  background?: TextBackground;
}

export interface CaptionPlacement {
  anchor: 'top' | 'center' | 'bottom' | 'custom';
  /** Normalized 0..1 from the top of the canvas (used for 'custom', informative otherwise). */
  y: number;
  /** Normalized 0..1 from the left; 0.5 = centered. */
  x: number;
  /** Keep inside platform safe zones. */
  safeZone: boolean;
  /** Placement engine may move captions off busy/scrim regions. */
  scrimAware: boolean;
}

export interface Caption {
  id: string;
  start: Tick;
  duration: Tick;
  words: CaptionWord[];
  style?: Partial<CaptionStyle>;
  placement?: Partial<CaptionPlacement>;
}

/**
 * Word-level caption track. This is the canonical home for captions; the
 * 'caption' Track/Clip kinds exist for imported (rasterized) caption clips only.
 */
export interface CaptionTrack {
  id: string;
  name: string;
  enabled: boolean;
  style: CaptionStyle;
  placement: CaptionPlacement;
  /** Sorted by start; never overlapping. */
  captions: Caption[];
}

export type MarkerKind = 'note' | 'review' | 'qa_fail' | 'approval';

export interface Marker {
  id: string;
  at: Tick;
  kind: MarkerKind;
  author: Author;
  body: string;
  clipId?: string;
  resolved?: { by: Author; at: string };
}

export interface Project {
  id: string;
  name?: string;
  /** Incremented by exactly one per applied top-level op. */
  version: number;
  /** Always TICK_RATE; stored so the document is self-describing. */
  tickRate: number;
  fps: number;
  width: number;
  height: number;
  /** Derived: max clip end across all tracks. Maintained by the reducer. */
  duration: Tick;
  /** Compositing order: index 0 is the bottom layer. */
  tracks: Track[];
  assets: AssetRef[];
  markers: Marker[];
  captions: CaptionTrack[];
  /** Brand editing-style record this project inherits from. */
  styleRef?: string;
  meta?: Record<string, JsonValue>;
}

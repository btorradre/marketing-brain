/**
 * JSON Schema (draft 2020-12) for Project, hand-written so the Python service
 * validates the same document. `pnpm build` emits it to
 * schema/project.schema.json. `validateProject` runs the schema through a
 * small built-in evaluator and then checks the semantic invariants the schema
 * language cannot express (no overlaps, unique ids, asset references, derived
 * duration).
 */
import { computeDuration, clipEnd, isMedia } from './model.js';
import { TICK_RATE, type Project } from './types.js';

export type JsonSchema = Record<string, unknown>;

const tick: JsonSchema = { type: 'integer', minimum: 0 };
const positiveTick: JsonSchema = { type: 'integer', minimum: 1 };
const unit: JsonSchema = { type: 'number', minimum: 0, maximum: 1 };
const id: JsonSchema = { type: 'string', minLength: 1 };
const str: JsonSchema = { type: 'string' };
const num: JsonSchema = { type: 'number' };
const bool: JsonSchema = { type: 'boolean' };
const color: JsonSchema = { type: 'string', pattern: '^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$' };
const ref = (name: string): JsonSchema => ({ $ref: `#/$defs/${name}` });
const jsonObject: JsonSchema = { type: 'object', additionalProperties: ref('jsonValue') };

const obj = (properties: Record<string, JsonSchema>, required: string[], extra?: JsonSchema): JsonSchema => ({
  type: 'object',
  properties,
  required,
  additionalProperties: false,
  ...(extra ?? {}),
});

/** Same properties, nothing required (for Partial<T> fields). */
function partial(def: JsonSchema): JsonSchema {
  const { required: _r, ...rest } = def;
  return rest;
}

const author = obj({ kind: { enum: ['human', 'agent'] }, id }, ['kind', 'id']);

const assetRef = obj(
  {
    id,
    kind: { enum: ['video', 'audio', 'image', 'font', 'lut', 'other'] },
    name: str,
    url: str,
    storageKey: str,
    mime: str,
    duration: tick,
    width: { type: 'integer', minimum: 1 },
    height: { type: 'integer', minimum: 1 },
    fps: { type: 'number', exclusiveMinimum: 0 },
    sampleRate: { type: 'integer', minimum: 1 },
    proxyUrl: str,
    thumbnailUrl: str,
    waveformUrl: str,
    provenance: obj({ jobId: str, source: str }, []),
  },
  ['id', 'kind'],
);

const easing: JsonSchema = {
  anyOf: [
    { enum: ['linear', 'easeIn', 'easeOut', 'easeInOut', 'hold'] },
    obj({ type: { const: 'bezier' }, c: { type: 'array', items: num, minItems: 4, maxItems: 4 } }, ['type', 'c']),
  ],
};

const keyframeValue: JsonSchema = { anyOf: [num, str, bool, { type: 'array', items: num }] };
const keyframe = obj({ at: tick, value: keyframeValue, easing }, ['at', 'value', 'easing']);
const transform = obj(
  { x: num, y: num, scale: num, rotation: num, opacity: unit, anchor: obj({ x: num, y: num }, ['x', 'y']) },
  ['x', 'y', 'scale', 'rotation', 'opacity', 'anchor'],
);
const crop = obj({ left: unit, top: unit, right: unit, bottom: unit }, ['left', 'top', 'right', 'bottom']);
const blendMode: JsonSchema = {
  enum: ['normal', 'multiply', 'screen', 'overlay', 'darken', 'lighten', 'colorDodge', 'colorBurn', 'hardLight', 'softLight', 'difference', 'exclusion', 'hue', 'saturation', 'color', 'luminosity'],
};
const effect = obj({ id, kind: { type: 'string', minLength: 1 }, params: jsonObject, enabled: bool }, ['id', 'kind', 'params', 'enabled']);
const mask = obj({ shape: { enum: ['rect', 'ellipse', 'linear', 'mirror', 'path'] }, feather: { type: 'number', minimum: 0 }, invert: bool, params: jsonObject }, ['shape', 'feather', 'invert', 'params']);
const chroma = obj({ color, similarity: unit, blend: unit, despill: unit, edge: unit }, ['color', 'similarity', 'blend', 'despill', 'edge']);
const textShadow = obj({ color, x: num, y: num, blur: { type: 'number', minimum: 0 } }, ['color', 'x', 'y', 'blur']);
const textOutline = obj({ color, width: { type: 'number', minimum: 0 } }, ['color', 'width']);
const textBackground = obj({ color, padding: { type: 'number', minimum: 0 }, radius: { type: 'number', minimum: 0 } }, ['color', 'padding', 'radius']);
const textAnimation = obj({ kind: { type: 'string', minLength: 1 }, duration: tick, params: jsonObject }, ['kind', 'duration']);
const textStyle = obj(
  {
    content: str,
    font: str,
    size: { type: 'number', exclusiveMinimum: 0 },
    weight: { type: 'number', minimum: 100, maximum: 900 },
    italic: bool,
    color,
    align: { enum: ['left', 'center', 'right'] },
    lineHeight: { type: 'number', exclusiveMinimum: 0 },
    letterSpacing: num,
    uppercase: bool,
    shadow: ref('textShadow'),
    outline: ref('textOutline'),
    background: ref('textBackground'),
    animateIn: ref('textAnimation'),
    animateOut: ref('textAnimation'),
    preset: str,
  },
  ['content', 'font', 'size', 'weight', 'italic', 'color', 'align', 'lineHeight', 'letterSpacing', 'uppercase'],
);
const duck = obj({ sourceTrackId: str, amount: num, attack: tick, release: tick }, ['amount', 'attack', 'release']);
const audioProps = obj({ gain: num, fadeIn: tick, fadeOut: tick, duck: ref('duck') }, ['gain', 'fadeIn', 'fadeOut']);
const transition = obj({ kind: { type: 'string', minLength: 1 }, duration: tick, params: jsonObject }, ['kind', 'duration']);

const clip = obj(
  {
    id,
    assetId: str,
    kind: { enum: ['video', 'audio', 'image', 'text', 'shape', 'caption'] },
    name: str,
    start: tick,
    duration: positiveTick,
    in: tick,
    out: tick,
    speed: { type: 'number', exclusiveMinimum: 0 },
    reverse: bool,
    freeze: tick,
    transform: ref('transform'),
    crop: ref('crop'),
    blend: ref('blendMode'),
    keyframes: { type: 'object', additionalProperties: { type: 'array', items: ref('keyframe'), minItems: 1 } },
    effects: { type: 'array', items: ref('effect') },
    mask: ref('mask'),
    chroma: ref('chroma'),
    text: ref('textStyle'),
    audio: ref('audioProps'),
    transitionIn: ref('transition'),
    transitionOut: ref('transition'),
    linkId: str,
    groupId: str,
  },
  ['id', 'kind', 'start', 'duration', 'in', 'out', 'speed', 'reverse', 'transform', 'crop', 'blend', 'keyframes', 'effects'],
);

const track = obj(
  { id, kind: { enum: ['video', 'audio', 'overlay', 'text', 'caption', 'label'] }, name: str, locked: bool, muted: bool, clips: { type: 'array', items: ref('clip') } },
  ['id', 'kind', 'name', 'locked', 'muted', 'clips'],
);

const captionWord = obj({ text: str, start: tick, duration: positiveTick }, ['text', 'start', 'duration']);
const captionStyle = obj(
  {
    preset: str,
    font: str,
    size: { type: 'number', exclusiveMinimum: 0 },
    weight: { type: 'number', minimum: 100, maximum: 900 },
    color,
    highlightColor: color,
    mode: { enum: ['line', 'word', 'karaoke'] },
    uppercase: bool,
    outline: ref('textOutline'),
    shadow: ref('textShadow'),
    background: ref('textBackground'),
  },
  ['font', 'size', 'weight', 'color', 'mode', 'uppercase'],
);
const captionPlacement = obj(
  { anchor: { enum: ['top', 'center', 'bottom', 'custom'] }, y: unit, x: unit, safeZone: bool, scrimAware: bool },
  ['anchor', 'y', 'x', 'safeZone', 'scrimAware'],
);
const caption = obj(
  { id, start: tick, duration: positiveTick, words: { type: 'array', items: ref('captionWord') }, style: ref('captionStylePartial'), placement: ref('captionPlacementPartial') },
  ['id', 'start', 'duration', 'words'],
);
const captionTrack = obj(
  { id, name: str, enabled: bool, style: ref('captionStyle'), placement: ref('captionPlacement'), captions: { type: 'array', items: ref('caption') } },
  ['id', 'name', 'enabled', 'style', 'placement', 'captions'],
);

const marker = obj(
  {
    id,
    at: tick,
    kind: { enum: ['note', 'review', 'qa_fail', 'approval'] },
    author: ref('author'),
    body: str,
    clipId: str,
    resolved: obj({ by: ref('author'), at: str }, ['by', 'at']),
  },
  ['id', 'at', 'kind', 'author', 'body'],
);

export const PROJECT_SCHEMA: JsonSchema = {
  $schema: 'https://json-schema.org/draft/2020-12/schema',
  $id: 'https://adengine.dev/schema/timeline/project.schema.json',
  title: 'Timeline Project',
  description: `adengine timeline document. All times are integer ticks at ${TICK_RATE} ticks per second. Semantic invariants (no overlaps per track, unique ids, asset references, derived duration) are checked by validateProject in @adengine/timeline and must be mirrored by other validators.`,
  type: 'object',
  properties: {
    id,
    name: str,
    version: { type: 'integer', minimum: 0 },
    tickRate: { const: TICK_RATE },
    fps: { type: 'number', exclusiveMinimum: 0 },
    width: { type: 'integer', minimum: 1 },
    height: { type: 'integer', minimum: 1 },
    duration: tick,
    tracks: { type: 'array', items: ref('track') },
    assets: { type: 'array', items: ref('assetRef') },
    markers: { type: 'array', items: ref('marker') },
    captions: { type: 'array', items: ref('captionTrack') },
    styleRef: str,
    meta: jsonObject,
  },
  required: ['id', 'version', 'tickRate', 'fps', 'width', 'height', 'duration', 'tracks', 'assets', 'markers', 'captions'],
  additionalProperties: false,
  $defs: {
    jsonValue: {},
    author,
    assetRef,
    easing,
    keyframe,
    transform,
    crop,
    blendMode,
    effect,
    mask,
    chroma,
    textShadow,
    textOutline,
    textBackground,
    textAnimation,
    textStyle,
    duck,
    audioProps,
    transition,
    clip,
    track,
    captionWord,
    captionStyle,
    captionStylePartial: partial(captionStyle),
    captionPlacement,
    captionPlacementPartial: partial(captionPlacement),
    caption,
    captionTrack,
    marker,
  },
};

// ---------------------------------------------------------------------------
// Minimal JSON Schema evaluator covering the keywords PROJECT_SCHEMA uses.

export interface SchemaError {
  path: string;
  message: string;
}

function typeOf(v: unknown): string {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  return typeof v;
}

function resolveRef(root: JsonSchema, $ref: string): JsonSchema {
  if (!$ref.startsWith('#/')) throw new Error(`unsupported $ref ${$ref}`);
  let cur: unknown = root;
  for (const seg of $ref.slice(2).split('/')) cur = (cur as Record<string, unknown>)[seg];
  if (!cur || typeof cur !== 'object') throw new Error(`unresolved $ref ${$ref}`);
  return cur as JsonSchema;
}

export function validateAgainstSchema(schema: JsonSchema, value: unknown, root: JsonSchema = schema, path = '$'): SchemaError[] {
  const errors: SchemaError[] = [];
  const err = (message: string) => errors.push({ path, message });
  if (typeof schema.$ref === 'string') return validateAgainstSchema(resolveRef(root, schema.$ref), value, root, path);

  if (schema.const !== undefined && value !== schema.const) err(`expected const ${JSON.stringify(schema.const)}`);
  if (Array.isArray(schema.enum) && !schema.enum.includes(value)) err(`expected one of ${JSON.stringify(schema.enum)}`);

  if (schema.type !== undefined) {
    const types = Array.isArray(schema.type) ? (schema.type as string[]) : [schema.type as string];
    const t = typeOf(value);
    const ok = types.some((want) => (want === 'integer' ? typeof value === 'number' && Number.isInteger(value) : want === 'number' ? typeof value === 'number' && Number.isFinite(value) : t === want));
    if (!ok) {
      err(`expected ${types.join('|')}, got ${t}`);
      return errors;
    }
  }

  if (typeof value === 'number') {
    if (typeof schema.minimum === 'number' && value < schema.minimum) err(`must be >= ${schema.minimum}`);
    if (typeof schema.maximum === 'number' && value > schema.maximum) err(`must be <= ${schema.maximum}`);
    if (typeof schema.exclusiveMinimum === 'number' && value <= schema.exclusiveMinimum) err(`must be > ${schema.exclusiveMinimum}`);
  }
  if (typeof value === 'string') {
    if (typeof schema.minLength === 'number' && value.length < schema.minLength) err(`must have length >= ${schema.minLength}`);
    if (typeof schema.pattern === 'string' && !new RegExp(schema.pattern).test(value)) err(`must match ${schema.pattern}`);
  }
  if (Array.isArray(value)) {
    if (typeof schema.minItems === 'number' && value.length < schema.minItems) err(`must have >= ${schema.minItems} items`);
    if (typeof schema.maxItems === 'number' && value.length > schema.maxItems) err(`must have <= ${schema.maxItems} items`);
    if (schema.items && typeof schema.items === 'object') value.forEach((v, i) => errors.push(...validateAgainstSchema(schema.items as JsonSchema, v, root, `${path}[${i}]`)));
  }
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    const o = value as Record<string, unknown>;
    const props = (schema.properties ?? {}) as Record<string, JsonSchema>;
    for (const key of (schema.required as string[] | undefined) ?? []) if (o[key] === undefined) errors.push({ path: `${path}.${key}`, message: 'required' });
    for (const [key, v] of Object.entries(o)) {
      if (v === undefined) continue;
      const sub = props[key];
      if (sub) errors.push(...validateAgainstSchema(sub, v, root, `${path}.${key}`));
      else if (schema.additionalProperties === false) errors.push({ path: `${path}.${key}`, message: 'unexpected property' });
      else if (schema.additionalProperties && typeof schema.additionalProperties === 'object') errors.push(...validateAgainstSchema(schema.additionalProperties as JsonSchema, v, root, `${path}.${key}`));
    }
  }
  if (Array.isArray(schema.anyOf)) {
    const branches = (schema.anyOf as JsonSchema[]).map((s) => validateAgainstSchema(s, value, root, path));
    if (!branches.some((b) => b.length === 0)) err(`matches no anyOf branch (${branches.map((b) => b[0]?.message ?? '').join(' / ')})`);
  }
  if (Array.isArray(schema.allOf)) for (const s of schema.allOf as JsonSchema[]) errors.push(...validateAgainstSchema(s, value, root, path));
  return errors;
}

// ---------------------------------------------------------------------------
// Semantic invariants.

export interface ValidationResult {
  ok: boolean;
  errors: SchemaError[];
}

export function validateProject(doc: unknown): ValidationResult {
  const errors = validateAgainstSchema(PROJECT_SCHEMA, doc);
  if (errors.length) return { ok: false, errors };
  const p = doc as Project;
  const err = (path: string, message: string) => errors.push({ path, message });
  const assetIds = new Set<string>();
  p.assets.forEach((a, i) => {
    if (assetIds.has(a.id)) err(`$.assets[${i}]`, `duplicate asset id ${a.id}`);
    assetIds.add(a.id);
  });
  const trackIds = new Set<string>();
  const clipIds = new Set<string>();
  const linkCounts = new Map<string, number>();
  p.tracks.forEach((t, ti) => {
    if (trackIds.has(t.id)) err(`$.tracks[${ti}]`, `duplicate track id ${t.id}`);
    trackIds.add(t.id);
    t.clips.forEach((c, ci) => {
      const path = `$.tracks[${ti}].clips[${ci}]`;
      if (clipIds.has(c.id)) err(path, `duplicate clip id ${c.id}`);
      clipIds.add(c.id);
      if ((t.kind === 'audio') !== (c.kind === 'audio')) err(path, `${c.kind} clip on ${t.kind} track`);
      if (ci > 0) {
        const prev = t.clips[ci - 1]!;
        if (prev.start > c.start) err(path, `clips not sorted by start`);
        if (clipEnd(prev) > c.start) err(path, `overlaps ${prev.id}`);
      }
      if (c.assetId !== undefined && !assetIds.has(c.assetId)) err(path, `missing asset ${c.assetId}`);
      if (c.assetId === undefined && (isMedia(c) || c.kind === 'image')) err(path, `${c.kind} clip needs assetId`);
      if (isMedia(c)) {
        if (c.freeze === undefined && c.out <= c.in) err(path, `out must be > in`);
        if (c.freeze !== undefined && c.out < c.in) err(path, `out must be >= in`);
        const asset = p.assets.find((a) => a.id === c.assetId);
        if (asset?.duration !== undefined && (c.freeze ?? c.out) > asset.duration) err(path, `reads past asset end`);
      } else if (c.in !== 0 || c.out !== c.duration) err(path, `non-media clip must have in=0,out=duration`);
      for (const [prop, kfs] of Object.entries(c.keyframes)) {
        for (let i = 1; i < kfs.length; i++) if (kfs[i]!.at <= kfs[i - 1]!.at) err(`${path}.keyframes.${prop}`, `keyframes must be sorted with unique at`);
      }
      const eids = new Set<string>();
      for (const e of c.effects) {
        if (eids.has(e.id)) err(path, `duplicate effect id ${e.id}`);
        eids.add(e.id);
      }
      if (c.linkId) linkCounts.set(c.linkId, (linkCounts.get(c.linkId) ?? 0) + 1);
    });
  });
  for (const [linkId, n] of linkCounts) if (n < 2) err('$.tracks', `linkId ${linkId} is used by only one clip`);
  const captionTrackIds = new Set<string>();
  p.captions.forEach((t, ti) => {
    if (captionTrackIds.has(t.id)) err(`$.captions[${ti}]`, `duplicate caption track id ${t.id}`);
    captionTrackIds.add(t.id);
    const ids = new Set<string>();
    t.captions.forEach((c, ci) => {
      const path = `$.captions[${ti}].captions[${ci}]`;
      if (ids.has(c.id)) err(path, `duplicate caption id ${c.id}`);
      ids.add(c.id);
      if (ci > 0) {
        const prev = t.captions[ci - 1]!;
        if (prev.start > c.start) err(path, `captions not sorted`);
        if (prev.start + prev.duration > c.start) err(path, `overlaps ${prev.id}`);
      }
      for (const w of c.words) if (w.start + w.duration > c.duration) err(path, `word '${w.text}' runs past caption end`);
    });
  });
  const markerIds = new Set<string>();
  p.markers.forEach((m, i) => {
    if (markerIds.has(m.id)) err(`$.markers[${i}]`, `duplicate marker id ${m.id}`);
    markerIds.add(m.id);
  });
  const dur = computeDuration(p);
  if (p.duration !== dur) err('$.duration', `derived duration is ${dur}, document says ${p.duration}`);
  return { ok: errors.length === 0, errors };
}

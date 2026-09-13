/** Compile a validated analysis handoff into the internal editor's atomic ops.
 * This does not imply that a renderer implements every named transition. The
 * caller explicitly declares support; unsupported requests are never dropped.
 */
import { OpError } from './errors.js';
import { newId, nowIso } from './ids.js';
import { apply } from './reducer.js';
import { createProject } from './model.js';
import type { BatchOp, Op } from './ops.js';
import { secondsToTicks } from './time.js';
import type { Author, EasingName, Keyframe, Project } from './types.js';

export interface PlannedClip {
  id: string;
  asset_id: string;
  track_id: string;
  kind: 'video' | 'audio';
  timeline_start_s: number;
  timeline_end_s: number;
  source_in_s: number;
  source_out_s: number;
  speed: number;
  animations: Array<{
    property: 'x' | 'y' | 'scale' | 'rotation' | 'opacity';
    keyframes: Array<{ at_s: number; value: number; easing: EasingName }>;
    rationale: string;
  }>;
  transition_out: { kind: string; duration_s: number; rationale: string } | null;
  audio: { gain_db: number; fade_in_s: number; fade_out_s: number } | null;
  evidence: Array<{ reference_id: string; observation_id: string }>;
  rationale: string;
  qa_checks: string[];
}

export interface EditPlanHandoff {
  status: 'ready_for_editor';
  editor: '@adengine/timeline';
  plan: {
    schema_version: 1;
    title: string;
    fps: number;
    width: number;
    height: number;
    duration_s: number;
    analysis_to_edit: Record<string, string>;
    clips: PlannedClip[];
    unresolved: string[];
    acceptance_checks: string[];
  };
  assets: Array<{ id: string; kind: string; url: string; duration_s: number; mime?: string }>;
}

export interface EditPlanOptions {
  author: Author;
  /** Required capability declaration for effects. Empty means hard cuts only. */
  supportedTransitions?: string[];
  project?: Project;
  idFactory?: (prefix: string) => string;
  at?: string;
}

export function assembleFromEditPlan(handoff: EditPlanHandoff, options: EditPlanOptions): BatchOp {
  const fail = (message: string): never => { throw new OpError('INVALID_OP', message); };
  const plan = handoff.plan;
  if (handoff.status !== 'ready_for_editor' || handoff.editor !== '@adengine/timeline' ||
      plan.schema_version !== 1 || plan.unresolved.length) fail('Edit plan is not ready for the internal editor');
  const project = options.project ?? createProject({ id: 'edit-plan-validation',
    fps: plan.fps, width: plan.width, height: plan.height });
  if (project.tracks.some(t => t.clips.length) || project.captions.some(t => t.captions.length)) {
    fail('Assemble into an empty timeline; preserve existing edits in a separate project');
  }
  if (!plan.clips.length) fail('Edit plan has no clips');
  const id = options.idFactory ?? newId;
  const at = options.at ?? nowIso();
  const ops: Op[] = [];
  const mk = <T extends Op['type']>(type: T, body: Omit<Extract<Op, { type: T }>, 'id' | 'at' | 'author' | 'type'>): Op =>
    ({ id: id('op'), at, author: options.author, type, ...body }) as unknown as Op;
  const ticks = (seconds: number): number => {
    if (!Number.isFinite(seconds) || seconds < 0) return fail('Times must be finite nonnegative seconds');
    return secondsToTicks(seconds);
  };
  ops.push(mk('setProjectSettings', { patch: { name: plan.title, fps: plan.fps, width: plan.width, height: plan.height } }));
  const existing = new Map(project.assets.map(a => [a.id, a]));
  for (const asset of handoff.assets) {
    const duration = ticks(asset.duration_s);
    const previous = existing.get(asset.id);
    if (previous) {
      if (previous.duration !== duration || previous.url !== asset.url) fail(`Source asset ${asset.id} differs from handoff`);
    } else {
      if (!['video', 'audio'].includes(asset.kind)) fail(`Unsupported media kind ${asset.kind}`);
      ops.push(mk('addAsset', { asset: { id: asset.id, kind: asset.kind as 'video' | 'audio',
        url: asset.url, mime: asset.mime, duration } }));
    }
  }
  const tracks = new Map(project.tracks.map(t => [t.id, t.kind]));
  const clips = [...plan.clips].sort((a, b) => a.timeline_start_s - b.timeline_start_s);
  const ids = new Set<string>();
  const sourceIds = new Set(handoff.assets.map(a => a.id));
  let visualEnd = 0;
  for (const clip of clips) {
    if (ids.has(clip.id)) fail(`Duplicate clip ${clip.id}`);
    ids.add(clip.id);
    if (!sourceIds.has(clip.asset_id)) fail(`Source ${clip.asset_id} missing from handoff`);
    const start = ticks(clip.timeline_start_s), end = ticks(clip.timeline_end_s);
    const duration = end - start;
    const sourceIn = ticks(clip.source_in_s), sourceOut = ticks(clip.source_out_s);
    if (duration <= 0 || sourceOut <= sourceIn || !Number.isFinite(clip.speed) || clip.speed <= 0 ||
        Math.abs((sourceOut - sourceIn) / clip.speed - duration) > 2) fail(`Invalid timing for ${clip.id}`);
    if (end > ticks(plan.duration_s)) fail(`Clip ${clip.id} exceeds plan`);
    if (clip.kind === 'video') {
      if (start > visualEnd) fail('Unplanned gap in video');
      visualEnd = Math.max(visualEnd, end);
    }
    if (!tracks.has(clip.track_id)) {
      tracks.set(clip.track_id, clip.kind);
      ops.push(mk('addTrack', { track: { id: clip.track_id, kind: clip.kind, name: clip.track_id } }));
    } else if (tracks.get(clip.track_id) !== clip.kind) fail('Mixed media on track');
    const keys: Record<string, Keyframe[]> = {};
    for (const animation of clip.animations) {
      if (keys[animation.property]) fail('Duplicate animation property');
      keys[animation.property] = animation.keyframes.map(k => ({ at: ticks(k.at_s), value: k.value, easing: k.easing }));
      const entries = keys[animation.property]!;
      if (entries.length < 2 || entries.some((k, i) => k.at >= duration ||
          (i > 0 && k.at <= entries[i - 1]!.at))) fail('Invalid animation timing');
    }
    const transition = clip.transition_out;
    if (transition) {
      if (!options.supportedTransitions?.includes(transition.kind)) fail(`Unsupported transition: ${transition.kind}`);
      const next = clips.find(c => c.track_id === clip.track_id && ticks(c.timeline_start_s) === end);
      if (!next || ticks(transition.duration_s) < 1 || ticks(transition.duration_s) > duration ||
          ticks(transition.duration_s) > ticks(next.timeline_end_s) - end) fail('Transition lacks an adjacent clip or duration');
    }
    ops.push(mk('addClip', { trackId: clip.track_id, clip: {
      id: clip.id, assetId: clip.asset_id, kind: clip.kind, name: clip.rationale,
      start, duration, in: sourceIn, out: sourceOut, speed: clip.speed, keyframes: keys,
      ...(transition ? { transitionOut: { kind: transition.kind, duration: ticks(transition.duration_s) } } : {}),
      ...(clip.audio ? { audio: { gain: clip.audio.gain_db, fadeIn: ticks(clip.audio.fade_in_s), fadeOut: ticks(clip.audio.fade_out_s) } } : {}),
    } }));
    ops.push(mk('addMarker', { marker: { id: id('marker'), at: start, kind: 'review',
      author: options.author, clipId: clip.id,
      body: JSON.stringify({ rationale: clip.rationale, evidence: clip.evidence, qa_checks: clip.qa_checks }) } }));
  }
  if (visualEnd !== ticks(plan.duration_s)) fail('Video does not cover the full plan duration');
  ops.push(mk('addMarker', { marker: { id: id('marker'), at: 0, kind: 'review', author: options.author,
    body: JSON.stringify({ analysis_to_edit: plan.analysis_to_edit, acceptance_checks: plan.acceptance_checks }) } }));
  const batch = mk('batch', { ops }) as BatchOp;
  // Dry run through the actual editor reducer: bounds, overlaps, keys and ids.
  apply(project, batch);
  return batch;
}

/**
 * Event log: the project is base + fold(apply, events). Inverses are computed
 * at append time against the real pre-state and kept alongside the events so
 * undo is op-based (it survives other authors' later edits) rather than a
 * snapshot restore. `events` alone is the durable record; `inverses` and
 * `snapshots` are derived and rebuilt by `loadLog`.
 */
import { OpError } from './errors.js';
import { newId, nowIso } from './ids.js';
import { invert } from './invert.js';
import type { Author, Project } from './types.js';
import type { Op } from './ops.js';
import { apply } from './reducer.js';

export interface Snapshot {
  version: number;
  project: Project;
}

export interface EventLog {
  /** Project state at the start of the log (version = base.version). */
  base: Project;
  events: Op[];
  /** inverses[i] undoes events[i]; computed against the state before events[i]. */
  inverses: Op[];
  /** Take a snapshot every N events (0 disables). */
  snapshotEvery: number;
  snapshots: Snapshot[];
}

export function createLog(base: Project, snapshotEvery = 50): EventLog {
  return { base, events: [], inverses: [], snapshotEvery, snapshots: [] };
}

/** Version number after event index i (0-based). */
export function versionOfIndex(log: EventLog, i: number): number {
  return log.base.version + i + 1;
}

export function headVersion(log: EventLog): number {
  return log.base.version + log.events.length;
}

/** Append an op: validates by applying, records the inverse, snapshots on schedule. Pure: returns new log + project. */
export function append(log: EventLog, project: Project, op: Op): { log: EventLog; project: Project } {
  if (project.version !== headVersion(log)) {
    throw new OpError('INVALID_DOCUMENT', `project version ${project.version} does not match log head ${headVersion(log)}`, { opId: op.id });
  }
  const inverse = invert(op, project);
  const next = apply(project, op);
  const events = [...log.events, op];
  const inverses = [...log.inverses, inverse];
  let snapshots = log.snapshots;
  if (log.snapshotEvery > 0 && events.length % log.snapshotEvery === 0) snapshots = [...snapshots, { version: next.version, project: next }];
  return { log: { ...log, events, inverses, snapshots }, project: next };
}

/** Fold events[from, to) onto `base`. */
export function replay(base: Project, events: readonly Op[], from = 0, to = events.length): Project {
  let p = base;
  for (let i = from; i < to; i++) p = apply(p, events[i]!);
  return p;
}

/** Rebuild a log (inverses + snapshots) from its durable parts. */
export function loadLog(base: Project, events: readonly Op[], snapshotEvery = 50): { log: EventLog; project: Project } {
  let state = { log: createLog(base, snapshotEvery), project: base };
  for (const op of events) state = append(state.log, state.project, op);
  return state;
}

/** Project at version n, using the nearest earlier snapshot. */
export function versionAt(log: EventLog, n: number): Project {
  if (n < log.base.version || n > headVersion(log)) throw new OpError('INVALID_RANGE', `version ${n} outside [${log.base.version}, ${headVersion(log)}]`);
  let start: Snapshot = { version: log.base.version, project: log.base };
  for (const s of log.snapshots) if (s.version <= n && s.version > start.version) start = s;
  const fromIndex = start.version - log.base.version;
  const toIndex = n - log.base.version;
  return replay(start.project, log.events, fromIndex, toIndex);
}

export function head(log: EventLog): Project {
  return versionAt(log, headVersion(log));
}

function sameAuthor(a: Author, b: Author): boolean {
  return a.kind === b.kind && a.id === b.id;
}

/**
 * Whether events[i] is currently undone: some later event undoes it and that
 * undo is itself not undone (redo = undo of an undo).
 */
export function isUndone(log: EventLog, i: number): boolean {
  const id = log.events[i]!.id;
  for (let j = log.events.length - 1; j > i; j--) {
    if (log.events[j]!.undoes === id && !isUndone(log, j)) return true;
  }
  return false;
}

/** True when the event with `id` is itself an undo/redo (so an event undoing it is a redo). */
function isRedo(log: EventLog, id: string): boolean {
  return log.events.some((e) => e.id === id && e.undoes !== undefined);
}

/** Forward (non-undo) ops by `author` that can still be undone, newest first. */
export function undoStack(log: EventLog, author?: Author): Op[] {
  const out: Op[] = [];
  for (let i = log.events.length - 1; i >= 0; i--) {
    const e = log.events[i]!;
    if (e.undoes !== undefined) continue;
    if (author && !sameAuthor(e.author, author)) continue;
    if (isUndone(log, i)) continue;
    out.push(e);
  }
  return out;
}

export interface UndoResult {
  log: EventLog;
  project: Project;
  /** The op that was appended to perform the undo/redo. */
  op: Op;
  /** The op it reverses. */
  target: Op;
}

function reverseEvent(log: EventLog, project: Project, i: number, author: Author | undefined, kind: 'undo' | 'redo'): UndoResult {
  const target = log.events[i]!;
  const stored = log.inverses[i]!;
  const op: Op = { ...stored, id: newId('op'), at: nowIso(), author: author ?? target.author, undoes: target.id };
  try {
    const r = append(log, project, op);
    return { ...r, op, target };
  } catch (e) {
    if (e instanceof OpError) {
      throw new OpError('UNDO_CONFLICT', `${kind} of ${target.type} ${target.id} no longer applies: ${e.message}`, { opId: target.id, details: { cause: e.code } });
    }
    throw e;
  }
}

/**
 * Undo the most recent not-yet-undone forward op by `author` (any author when
 * omitted). The agent undoing its own op never undoes the human's, and vice
 * versa. Returns null when there is nothing to undo.
 */
export function undo(project: Project, log: EventLog, author?: Author): UndoResult | null {
  for (let i = log.events.length - 1; i >= 0; i--) {
    const e = log.events[i]!;
    if (e.undoes !== undefined) continue;
    if (author && !sameAuthor(e.author, author)) continue;
    if (isUndone(log, i)) continue;
    return reverseEvent(log, project, i, author, 'undo');
  }
  return null;
}

/**
 * Redo: reverse the most recent not-yet-reversed undo op by `author`, unless
 * the author has issued a forward op since (which clears their redo stack).
 */
export function redo(project: Project, log: EventLog, author?: Author): UndoResult | null {
  for (let i = log.events.length - 1; i >= 0; i--) {
    const e = log.events[i]!;
    if (author && !sameAuthor(e.author, author)) continue;
    if (e.undoes === undefined) return null; // a forward op by this author after the undo: redo stack cleared
    if (isRedo(log, e.undoes)) continue; // a redo is not itself redoable
    if (isUndone(log, i)) continue;
    return reverseEvent(log, project, i, author, 'redo');
  }
  return null;
}

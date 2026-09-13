import { describe, expect, it } from 'vitest';
import { OpError } from '../src/errors.js';
import { append, createLog, head, loadLog, redo, replay, undo, undoStack, versionAt } from '../src/log.js';
import { clone } from '../src/model.js';
import { AGENT, HUMAN, S, clip, op, seed } from './fixture.js';

function run(ops: Parameters<typeof append>[2][], snapshotEvery = 2) {
  let state = { log: createLog(seed(), snapshotEvery), project: seed() };
  for (const o of ops) state = append(state.log, state.project, o);
  return state;
}

describe('event log', () => {
  it('replay, versionAt (via snapshots) and loadLog agree with head', () => {
    const ops = [op('trimIn', { clipId: 'c1', delta: 3000 }), op('moveClip', { clipId: 'c3', start: 7 * S }, AGENT), op('addMarker', { marker: { id: 'm2', at: 0, kind: 'note', author: AGENT, body: 'x' } }, AGENT)];
    const { log, project } = run(ops);
    expect(project.version).toBe(3);
    expect(log.snapshots.map((s) => s.version)).toEqual([2]);
    expect(clone(replay(log.base, log.events))).toEqual(clone(project));
    expect(clone(head(log))).toEqual(clone(project));
    expect(clone(versionAt(log, 3))).toEqual(clone(project));
    expect(versionAt(log, 0)).toEqual(log.base);
    expect(clip(versionAt(log, 1), 'c1').start).toBe(3000);
    expect(clip(versionAt(log, 1), 'c3').start).toBe(5 * S);
    expect(clip(versionAt(log, 2), 'c3').start).toBe(7 * S);
    const reloaded = loadLog(log.base, log.events, 2);
    expect(clone(reloaded.project)).toEqual(clone(project));
    const stripMeta = (ops: typeof log.inverses) => ops.map((o) => clone({ ...o, id: "", at: "" }));
    expect(stripMeta(reloaded.log.inverses)).toEqual(stripMeta(log.inverses));
  });

  it('rejects a project that is not at the log head', () => {
    const { log } = run([op('trimIn', { clipId: 'c1', delta: 3000 })]);
    expect(() => append(log, seed(), op('removeClip', { clipId: 'c1' }))).toThrow(OpError);
  });

  it('per-author undo: the agent undoing its work does not undo the human', () => {
    let { log, project } = run([op('trimIn', { clipId: 'c1', delta: 3000 }), op('moveClip', { clipId: 'c3', start: 7 * S }, AGENT)]);
    const a = undo(project, log, AGENT)!;
    ({ log, project } = a);
    expect(a.target.type).toBe('moveClip');
    expect(a.op.undoes).toBe(a.target.id);
    expect(a.op.author).toEqual(AGENT);
    expect(clip(project, 'c3').start).toBe(5 * S);
    expect(clip(project, 'c1').start).toBe(3000); // human's trim survives
    expect(undo(project, log, AGENT)).toBeNull();

    const h = undo(project, log, HUMAN)!;
    ({ log, project } = h);
    expect(clip(project, 'c1').start).toBe(0);
    expect(undo(project, log, HUMAN)).toBeNull();
    expect(undoStack(log, HUMAN)).toEqual([]);

    const r = redo(project, log, HUMAN)!;
    ({ log, project } = r);
    expect(clip(project, 'c1').start).toBe(3000);
    expect(redo(project, log, HUMAN)).toBeNull();
    expect(undoStack(log, HUMAN).map((o) => o.type)).toEqual(['trimIn']);
    expect(project.version).toBe(5);
    expect(clone(replay(log.base, log.events))).toEqual(clone(project));
  });

  it('undo is op-based: it applies after another author edited the same clip', () => {
    let { log, project } = run([op('trimIn', { clipId: 'c1', delta: 3000 }), op('moveClip', { clipId: 'c1', start: 8 * S }, AGENT)]);
    ({ log, project } = undo(project, log, HUMAN)!);
    expect(clip(project, 'c1')).toMatchObject({ start: 8 * S - 3000, duration: 2 * S, in: 0 });
  });

  it('a forward op clears the redo stack; undo of an undone op skips to the previous one', () => {
    let { log, project } = run([op('trimIn', { clipId: 'c1', delta: 3000 }), op('trimOut', { clipId: 'c3', delta: 3000 })]);
    ({ log, project } = undo(project, log, HUMAN)!); // undoes trimOut
    ({ log, project } = append(log, project, op('addMarker', { marker: { id: 'm2', at: 0, kind: 'note', author: HUMAN, body: 'x' } })));
    expect(redo(project, log, HUMAN)).toBeNull();
    ({ log, project } = undo(project, log, HUMAN)!); // undoes addMarker
    const u = undo(project, log, HUMAN)!; // skips the undone trimOut, undoes trimIn
    expect(u.target.type).toBe('trimIn');
    expect(clip(u.project, 'c1').start).toBe(0);
  });

  it('undo without an author undoes the latest op by anyone', () => {
    const { log, project } = run([op('trimIn', { clipId: 'c1', delta: 3000 }), op('moveClip', { clipId: 'c3', start: 7 * S }, AGENT)]);
    const u = undo(project, log)!;
    expect(u.target.author).toEqual(AGENT);
    expect(u.op.author).toEqual(AGENT);
  });

  it('surfaces UNDO_CONFLICT when the target no longer exists', () => {
    const { log, project } = run([op('trimIn', { clipId: 'c1', delta: 3000 }), op('removeClip', { clipId: 'c1' }, AGENT)]);
    try {
      undo(project, log, HUMAN);
      expect.fail('expected UNDO_CONFLICT');
    } catch (e) {
      expect(e).toBeInstanceOf(OpError);
      expect((e as OpError).code).toBe('UNDO_CONFLICT');
    }
  });
});

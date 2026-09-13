import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { assembleFromEditPlan, type EditPlanHandoff } from '../src/edit-plan.js';
import { createProject } from '../src/model.js';
import { apply } from '../src/reducer.js';
import { append, createLog, undo } from '../src/log.js';
import { validateProject } from '../src/schema.js';
import { AGENT } from './fixture.js';

const load = (): EditPlanHandoff => JSON.parse(readFileSync(new URL('./fixtures/edit-plan.json', import.meta.url), 'utf8'));
const empty = () => createProject({ id: 'project', fps: 30, width: 1080, height: 1920 });
const opts = () => {
  let n = 0;
  return { author: AGENT, supportedTransitions: ['dissolve'], idFactory: (p: string) => `${p}_${++n}`, at: '2026-09-07T00:00:00Z' };
};

describe('analysis handoff -> internal timeline', () => {
  it('preserves source trims, speed, cut timing, transition, animation and audio', () => {
    const project = apply(empty(), assembleFromEditPlan(load(), opts()));
    const [a, b] = project.tracks.find(t => t.id === 'main')!.clips;
    expect([a!.in, a!.out, a!.start, a!.duration]).toEqual([6000,18000,0,12000]);
    expect([b!.in, b!.out, b!.start, b!.duration, b!.speed]).toEqual([30000,54000,12000,12000,2]);
    expect(a!.transitionOut).toEqual({ kind: 'dissolve', duration: 1200 });
    expect(a!.keyframes.scale![1]).toEqual({ at:10800, value:1.1, easing:'hold' });
    expect(project.tracks.find(t => t.id === 'audio')!.clips[0]!.audio).toEqual({ gain:-6, fadeIn:600, fadeOut:1200 });
    expect(project.duration).toBe(24000);
    expect(project.markers.some(m => m.body.includes('rushes-1'))).toBe(true);
    expect(validateProject(project)).toEqual({ ok: true, errors: [] });
  });
  it('round trips the entire handoff through the existing event log and undo', () => {
    const base = empty();
    const created = createLog(base);
    const next = append(created, base, assembleFromEditPlan(load(), opts()));
    const back = undo(next.project, next.log, AGENT);
    expect(back.project.tracks).toEqual([]);
    expect(back.project.assets).toEqual([]);
  });
  it('requires explicit renderer support for a transition', () => {
    expect(() => assembleFromEditPlan(load(), { author: AGENT })).toThrow('Unsupported transition');
  });
  it.each(['gap','overlap','source','animation','blocked','nonempty','last-transition'])(
    'refuses %s instead of silently changing the edit', reason => {
      const h = load(); const options = opts();
      if (reason === 'gap') { h.plan.clips[1]!.timeline_start_s = 2.5; h.plan.clips[1]!.source_in_s = 6; }
      if (reason === 'overlap') { h.plan.clips[1]!.timeline_start_s = 1.5; h.plan.clips[1]!.source_in_s = 4; }
      if (reason === 'source') { h.plan.clips[1]!.source_out_s = 19; h.plan.clips[1]!.source_in_s = 15; }
      if (reason === 'animation') h.plan.clips[0]!.animations[0]!.keyframes[1]!.at_s = 2;
      if (reason === 'blocked') h.plan.unresolved.push('uncertain');
      if (reason === 'last-transition') h.plan.clips[1]!.transition_out = h.plan.clips[0]!.transition_out;
      if (reason === 'nonempty') {
        const project = apply(empty(), assembleFromEditPlan(h, options));
        expect(() => assembleFromEditPlan(h, { ...opts(), project })).toThrow('empty timeline');
        return;
      }
      expect(() => assembleFromEditPlan(h, options)).toThrow();
    });
});

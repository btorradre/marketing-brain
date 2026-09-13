import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import Ajv2020 from 'ajv/dist/2020.js';
import { clone } from '../src/model.js';
import { apply, applyAll } from '../src/reducer.js';
import { PROJECT_SCHEMA, validateAgainstSchema, validateProject } from '../src/schema.js';
import { S, op, seed } from './fixture.js';

const AjvCtor = (Ajv2020 as unknown as { default?: typeof Ajv2020 }).default ?? Ajv2020;

describe('schema', () => {
  it('validates the sample project and one after edits', () => {
    expect(validateProject(seed())).toEqual({ ok: true, errors: [] });
    const edited = applyAll(seed(), [
      op('split', { clipId: 'c1', tick: 9000, newClipId: 'c1b' }),
      op('freezeFrame', { clipId: 'c2', tick: 3 * S, freezeDuration: 3000, frozenClipId: 'f', rightClipId: 'c2r' }),
      op('setChroma', { clipId: 'c3', chroma: { color: '#00ff00', similarity: 0.13, blend: 0.08, despill: 0.5, edge: 0 } }),
    ]);
    expect(validateProject(edited)).toEqual({ ok: true, errors: [] });
  });

  it('the JSON schema compiles under ajv (draft 2020-12) and agrees with the built-in evaluator', () => {
    const ajv = new AjvCtor({ strict: true, allErrors: true });
    const validate = ajv.compile(PROJECT_SCHEMA);
    expect(validate(seed())).toBe(true);
    const bad = clone(seed()) as Record<string, unknown>;
    (bad.tracks as Array<{ clips: Array<{ start: number }> }>)[0]!.clips[0]!.start = 0.5;
    bad.tickRate = 1000;
    expect(validate(bad)).toBe(false);
    const ours = validateAgainstSchema(PROJECT_SCHEMA, bad);
    expect(ours.map((e) => e.path).sort()).toEqual(['$.tickRate', '$.tracks[0].clips[0].start']);
  });

  it('rejects semantic violations the schema cannot see', () => {
    const overlap = clone(seed());
    overlap.tracks[0]!.clips[1]!.start = 6000;
    expect(validateProject(overlap).errors.map((e) => e.message)).toContain('overlaps c1');

    const missingAsset = clone(seed());
    missingAsset.tracks[0]!.clips[0]!.assetId = 'ghost';
    expect(validateProject(missingAsset).errors[0]!.message).toMatch(/missing asset ghost/);

    const staleDuration = apply(seed(), op('rippleDelete', { clipId: 'vo' }));
    const tampered = { ...staleDuration, duration: staleDuration.duration + 1 };
    expect(validateProject(tampered).errors[0]!.path).toBe('$.duration');

    const extra = { ...seed(), rogue: 1 };
    expect(validateProject(extra).errors[0]!.message).toBe('unexpected property');
  });

  it('the emitted schema file matches the source of truth (after build)', () => {
    const file = new URL('../schema/project.schema.json', import.meta.url);
    if (!existsSync(file)) return; // build not run yet
    expect(JSON.parse(readFileSync(file, 'utf8'))).toEqual(JSON.parse(JSON.stringify(PROJECT_SCHEMA)));
  });
});

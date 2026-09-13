import { randomUUID } from 'node:crypto';

/** `${prefix}_${uuid}`; prefixes make ids readable in logs and agent transcripts. */
export function newId(prefix = 'id'): string {
  return `${prefix}_${randomUUID()}`;
}

export function nowIso(): string {
  return new Date().toISOString();
}

/** Deterministic id factory for tests and reproducible assemblies. */
export function sequentialIds(seed = 0): (prefix: string) => string {
  const counters = new Map<string, number>();
  return (prefix: string) => {
    const n = (counters.get(prefix) ?? seed) + 1;
    counters.set(prefix, n);
    return `${prefix}_${n}`;
  };
}

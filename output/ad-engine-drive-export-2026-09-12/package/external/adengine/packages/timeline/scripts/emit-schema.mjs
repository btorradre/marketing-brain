// Emits schema/project.schema.json from the built dist/schema.js. Run after tsc.
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { PROJECT_SCHEMA } from '../dist/schema.js';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, '..', 'schema');
mkdirSync(outDir, { recursive: true });
const outFile = join(outDir, 'project.schema.json');
writeFileSync(outFile, JSON.stringify(PROJECT_SCHEMA, null, 2) + '\n');
console.log(`wrote ${outFile}`);

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(root, relative), 'utf8'));
const source = readJson('provenance/phase10_caveats.json');
const artifact = readJson('provenance/phase10_caveat_resolutions.json');
const queue = fs.readFileSync(path.join(root, 'SCIENTIFIC_REVIEW_QUEUE.md'), 'utf8');
const allowed = new Set(['already-applied', 'phase16-verified-no-change', 'escalated']);
const sourceIds = source.items.map(({ id }) => id).sort((a, b) => a - b);
const resolutionIds = artifact.resolutions.map(({ id }) => id).sort((a, b) => a - b);

if (source.resolution_artifact !== 'provenance/phase10_caveat_resolutions.json') throw new Error('Phase 10 source does not identify its resolution artifact');
if (JSON.stringify(sourceIds) !== JSON.stringify(resolutionIds)) throw new Error('Phase 10 resolution IDs do not exactly cover source IDs');
if (new Set(resolutionIds).size !== resolutionIds.length) throw new Error('Duplicate Phase 10 resolution ID');

const counts = { total: artifact.resolutions.length, already_applied: 0, phase16_verified_no_change: 0, escalated: 0 };
for (const resolution of artifact.resolutions) {
  if (!allowed.has(resolution.status)) throw new Error(`Invalid status for Phase 10 item ${resolution.id}`);
  counts[resolution.status.replaceAll('-', '_')] += 1;
  if (!resolution.note || !resolution.evidence) throw new Error(`Incomplete resolution for Phase 10 item ${resolution.id}`);
}
if (JSON.stringify(counts) !== JSON.stringify(artifact.summary)) throw new Error(`Resolution summary mismatch: ${JSON.stringify(counts)}`);
for (const [id, sr] of [[6, 'SR-30'], [13, 'SR-31']]) {
  const resolution = artifact.resolutions.find((entry) => entry.id === id);
  if (resolution.status !== 'escalated' || !queue.includes(`### ${sr}`)) throw new Error(`Phase 10 item ${id} is not present as ${sr}`);
}

console.log(`Validated ${counts.total} Phase 10 resolutions (${counts.already_applied} applied, ${counts.phase16_verified_no_change} gate-closed, ${counts.escalated} escalated).`);

#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { relative, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const manifestPath = resolve('provenance/release_artifact_manifest.json');
const normalizedTextExtensions = new Set(['.json', '.jsonl']);

export function artifactBytes(path) {
  const bytes = readFileSync(path);
  const extension = path.slice(path.lastIndexOf('.')).toLowerCase();
  if (!normalizedTextExtensions.has(extension)) return bytes;
  return Buffer.from(bytes.toString('utf8').replace(/\r\n?/g, '\n'), 'utf8');
}

export function sha256(path) {
  return createHash('sha256').update(artifactBytes(path)).digest('hex');
}

function listFiles(path) {
  const absolute = resolve(path);
  if (!existsSync(absolute)) throw new Error(`Missing release artifact: ${path}`);
  if (statSync(absolute).isFile()) return [absolute];
  return readdirSync(absolute, { withFileTypes: true })
    .flatMap(entry => listFiles(resolve(absolute, entry.name)))
    .sort();
}

export function buildReleaseManifest() {
  const roots = [
    'knowledge/record_counts.json',
    'knowledge/claim_graph.json',
    'knowledge/trust_human_review_overrides.json',
    'knowledge/oratlas/contract-pin.json',
    'knowledge/oratlas/claims.jsonl',
    'knowledge/oratlas/citations.jsonl',
    'knowledge/oratlas/relations.jsonl',
    'knowledge/oratlas/trust-assessments.jsonl',
    'knowledge/oratlas/provenance.json',
    'review-manifest.json',
    '.zenodo.json',
    'evidence/EVIDENCE_MIGRATION_REPORT.json',
    'evidence/EVIDENCE_COVERAGE_REPORT.json',
    'figures',
  ];
  const files = roots.flatMap(listFiles)
    .filter(path => !path.includes(`${resolve('figures/notebooks')}`))
    .filter(path => /\.(json|jsonl|png)$/.test(path))
    .map(path => ({
      path: relative(resolve('.'), path).replaceAll('\\', '/'),
      bytes: artifactBytes(path).byteLength,
      sha256: sha256(path),
    }))
    .sort((a, b) => a.path.localeCompare(b.path));
  const recordCounts = JSON.parse(readFileSync(resolve('knowledge/record_counts.json'), 'utf8'));
  return {
    schema_version: '1.0.0',
    release_series: 'v0.1.0-rc',
    generated_from: 'committed canonical artifacts; no timestamp fields',
    record_counts_sha256: sha256(resolve('knowledge/record_counts.json')),
    canonical_counts: {
      claim_graph: recordCounts.claim_graph,
      human_review: recordCounts.human_review,
      oratlas_export: recordCounts.oratlas_export,
    },
    files,
  };
}

export function validateReleaseManifest(expected) {
  const actual = buildReleaseManifest();
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    const expectedMap = new Map(expected.files.map(file => [file.path, file]));
    const changed = actual.files.filter(file => expectedMap.get(file.path)?.sha256 !== file.sha256).map(file => file.path);
    const removed = expected.files.filter(file => !actual.files.some(actualFile => actualFile.path === file.path)).map(file => file.path);
    throw new Error(`Frozen release artifacts changed: ${[...changed, ...removed].join(', ') || 'manifest metadata'}`);
  }
  return actual;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.includes('--write')) {
    const manifest = buildReleaseManifest();
    writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
    console.log(`Wrote ${relative(resolve('.'), manifestPath)} with ${manifest.files.length} frozen files.`);
  } else {
    const expected = JSON.parse(readFileSync(manifestPath, 'utf8'));
    const manifest = validateReleaseManifest(expected);
    console.log(`Release artifact contract passed: ${manifest.files.length} files.`);
  }
}

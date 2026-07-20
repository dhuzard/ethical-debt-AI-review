#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { validateReleaseManifest } from './release-artifacts.js';

function read(path) {
  return readFileSync(resolve(path), 'utf8');
}

export function validateReleaseContract() {
  const manifest = JSON.parse(read('provenance/release_artifact_manifest.json'));
  validateReleaseManifest(manifest);
  const counts = JSON.parse(read('knowledge/record_counts.json'));
  const coverage = JSON.parse(read('evidence/EVIDENCE_COVERAGE_REPORT.json'));
  const packageJson = JSON.parse(read('package.json'));
  const zenodo = JSON.parse(read('.zenodo.json'));
  const requirements = read('requirements.txt').trim().split(/\r?\n/).filter(Boolean);
  if (counts.claim_graph.claims !== 529 || counts.claim_graph.human_review_flags !== 29) {
    throw new Error('Frozen claim or human-review counts changed. Start a new release candidate series intentionally.');
  }
  if (coverage.absent_sections.length || coverage.sections.reduce((sum, section) => sum + section.findings, 0) !== 1438) {
    throw new Error('Evidence coverage does not match the frozen prerelease contract.');
  }
  if (packageJson.devDependencies?.mystmd !== '1.10.1' || packageJson.devDependencies?.['@playwright/test'] !== '1.61.1') {
    throw new Error('MyST and Playwright must be pinned exactly.');
  }
  if (requirements.some(requirement => !/^[A-Za-z0-9_.-]+==[^=]+$/.test(requirement))) {
    throw new Error('Every Python requirement must use an exact == pin.');
  }
  if (zenodo.version !== '0.1.0-rc.1' || zenodo.license !== 'MIT' || zenodo.creators?.[0]?.orcid !== '0000-0003-4820-7951') {
    throw new Error('Zenodo prerelease metadata is incomplete or inconsistent.');
  }
  for (const path of ['README.md', 'content/00_frontmatter.md', 'content/Methods.md', 'content/provenance.md', 'HANDOFF.md']) {
    const corpusWording = read(path);
    if (!corpusWording.includes('1,438') || !corpusWording.includes('1,336')) {
      throw new Error(`${path} does not state the canonical curated corpus counts.`);
    }
  }
  const publicWording = `${read('README.md')}\n${read('content/00_frontmatter.md')}\n${read('DEPLOY.md')}`.toLowerCase();
  for (const phrase of ['not peer reviewed', 'not fully human-adjudicated', 'experimental trust']) {
    if (!publicWording.includes(phrase)) throw new Error(`Missing required public disclosure: ${phrase}`);
  }
  return { files: manifest.files.length, claims: counts.claim_graph.claims, findings: 1438 };
}

function validateTag(tag) {
  if (!/^v0\.1\.0-rc\.\d+$/.test(tag)) throw new Error(`Invalid prerelease tag: ${tag}`);
  const head = execFileSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  const tagged = execFileSync('git', ['rev-list', '-n', '1', tag], { encoding: 'utf8' }).trim();
  if (head !== tagged) throw new Error(`${tag} resolves to ${tagged}, not validated HEAD ${head}`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const result = validateReleaseContract();
  const tagIndex = process.argv.indexOf('--tag');
  if (tagIndex !== -1) validateTag(process.argv[tagIndex + 1]);
  console.log(`Release contract passed: ${result.files} frozen files, ${result.claims} claims, ${result.findings} findings.`);
}

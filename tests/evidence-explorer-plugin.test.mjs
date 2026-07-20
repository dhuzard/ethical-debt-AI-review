import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

import {
  countUniquePapers,
  extractFindings,
} from '../plugins/evidence-explorer-plugin.mjs';
import evidenceExplorerPlugin from '../plugins/evidence-explorer-plugin.mjs';
import { classifyEvidenceState } from '../content/evidence-explorer-widget.mjs';
import {
  buildEvidenceCoverage,
  validateEvidenceCoverage,
} from '../scripts/validate-evidence.js';

test('Evidence Explorer loads every canonical package and its rich findings', () => {
  const tree = {
    type: 'root',
    children: [{
      type: 'evidence-explorer',
      evidenceDir: '../evidence',
      height: '800px',
    }],
  };
  const transform = evidenceExplorerPlugin.transforms
    .find(({ name }) => name === 'evidence-data-loader');

  transform.plugin({}, {})(tree, {
    path: resolve('content/evidence_database.md'),
  });

  const widget = tree.children[0];
  assert.equal(widget.type, 'anywidget');
  const data = JSON.parse(widget.model.evidence_data);
  assert.deepEqual(data.sections.map(section => ({
    section: section.section,
    source: section.source_file,
    papers: section.papers,
    findings: section.findings,
    conflicts: section.conflicts,
  })), [
    { section: 1, source: 'evidence_section_01.json', papers: 11, findings: 11, conflicts: 26 },
    { section: 2, source: 'evidence_section_02.json', papers: 182, findings: 182, conflicts: 10 },
    { section: 3, source: 'evidence_section_03.json', papers: 192, findings: 192, conflicts: 16 },
    { section: 4, source: 'evidence_section_04.json', papers: 269, findings: 279, conflicts: 17 },
    { section: 5, source: 'evidence_section_05.json', papers: 244, findings: 244, conflicts: 22 },
    { section: 6, source: 'evidence_section_06.json', papers: 168, findings: 168, conflicts: 11 },
    { section: 7, source: 'evidence_section_07.json', papers: 175, findings: 175, conflicts: 12 },
    { section: 8, source: 'evidence_section_08.json', papers: 177, findings: 177, conflicts: 11 },
    { section: 9, source: 'evidence_section_09.json', papers: 10, findings: 10, conflicts: 0 },
  ]);
  assert.equal(data.findings.length, 1438);
  assert.equal(data.conflicts.length, 125);
  assert.equal(data.figure_data.length, 60);
  assert.equal(typeof data.findings[0], 'object');
  assert.match(data.findings[0].doi, /^10\./);

  const report = JSON.parse(readFileSync(resolve('evidence/EVIDENCE_MIGRATION_REPORT.json')));
  assert.deepEqual(report.sections.map(section => ({
    section: section.section,
    papers: section.papers,
    findings: section.findings,
    conflicts: section.conflicts,
  })), data.sections.map(section => ({
    section: section.section,
    papers: section.papers,
    findings: section.findings,
    conflicts: section.conflicts,
  })));
  assert.deepEqual({
    findings: report.totals.findings,
    conflicts: report.totals.conflicts_in_section_packages,
    figureData: report.totals.figure_comparisons,
  }, {
    findings: data.findings.length,
    conflicts: data.conflicts.length,
    figureData: data.figure_data.length,
  });
});

test('rich findings take precedence over argument-group citation keys', () => {
  const rich = { doi: '10.1000/example', claim: 'A finding record.' };
  const findings = extractFindings({
    findings: [rich],
    argument_groups: {
      main: { supporting_findings: ['Example2026'] },
    },
  });

  assert.deepEqual(findings, [rich]);
  assert.equal(countUniquePapers(findings), 1);
});

test('section_NN directive values select one package and report a missing package explicitly', () => {
  const transform = evidenceExplorerPlugin.transforms.find(({ name }) => name === 'evidence-data-loader');
  const makeTree = section => ({
    type: 'root',
    children: [{ type: 'evidence-explorer', evidenceDir: '../evidence', section }],
  });
  const selected = makeTree('section_02');
  transform.plugin({}, {})(selected, { path: resolve('content/02_reproducibility_crisis.md') });
  const selectedData = JSON.parse(selected.children[0].model.evidence_data);
  assert.equal(selectedData.load_status, 'loaded');
  assert.equal(selectedData.requested_section, 2);
  assert.deepEqual(selectedData.sections.map(({ section }) => section), [2]);

  const missing = makeTree('section_10');
  transform.plugin({}, {})(missing, { path: resolve('content/evidence_database.md') });
  const missingData = JSON.parse(missing.children[0].model.evidence_data);
  assert.equal(missingData.load_status, 'absent');
  assert.match(missingData.load_message, /section 10/);
});

test('legacy argument-group fallback ignores citation-key strings', () => {
  const record = { cite_key: 'Example2026', claim: 'A legacy record.' };
  assert.deepEqual(extractFindings({
    argument_groups: {
      main: { supporting_findings: ['Example2026', record] },
    },
  }), [record]);
});

test('widget state distinguishes absent, valid-empty, malformed, and loaded payloads', () => {
  assert.equal(classifyEvidenceState('{').kind, 'error');
  assert.equal(classifyEvidenceState(JSON.stringify({
    load_status: 'absent', sections: [], findings: [],
  })).kind, 'absent');
  assert.equal(classifyEvidenceState(JSON.stringify({
    load_status: 'loaded', sections: [{ section: 1 }], findings: [],
  })).kind, 'valid-empty');
  assert.equal(classifyEvidenceState(JSON.stringify({
    load_status: 'loaded', sections: [{ section: 1 }], findings: [{ doi: '10.1/x' }],
  })).kind, 'loaded');
});

test('validator fails for an absent package but reports a present zero-finding package separately', () => {
  const dir = mkdtempSync(join(tmpdir(), 'ethical-debt-evidence-'));
  try {
    writeFileSync(join(dir, 'evidence_section_01.json'), JSON.stringify({ findings: [] }));
    const incomplete = buildEvidenceCoverage(dir, [1, 2]);
    assert.deepEqual(incomplete.absent_sections, [2]);
    assert.deepEqual(incomplete.valid_empty_sections, [1]);
    assert.throws(() => validateEvidenceCoverage(incomplete, 0), /Absent evidence packages: 2/);

    writeFileSync(join(dir, 'evidence_section_02.json'), JSON.stringify({
      findings: [{ doi: '10.1/example', replication_status: 'replication_unknown' }],
    }));
    const complete = buildEvidenceCoverage(dir, [1, 2]);
    assert.deepEqual(complete.absent_sections, []);
    assert.deepEqual(complete.valid_empty_sections, [1]);
    assert.equal(validateEvidenceCoverage(complete, 1), 1);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

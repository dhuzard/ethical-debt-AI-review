#!/usr/bin/env node
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  discoverEvidencePackages,
  extractFindings,
} from '../plugins/evidence-explorer-plugin.mjs';

const expectedSections = [1, 2, 3, 4, 5, 6, 7, 8, 9];

export function buildEvidenceCoverage(evidenceDir, expected = expectedSections) {
  const packages = discoverEvidencePackages(evidenceDir);
  const discovered = packages.map(({ section }) => section);
  const absentSections = expected.filter(section => !discovered.includes(section));
  const validEmptySections = [];
  const sections = [];

  for (const evidenceFile of packages) {
    const data = JSON.parse(readFileSync(evidenceFile.filePath, 'utf8'));
    const findings = extractFindings(data);
    if (findings.length === 0) validEmptySections.push(evidenceFile.section);
    const replicationPopulated = findings.filter(finding => Boolean(finding.replication_status)).length;
    sections.push({
      section: evidenceFile.section,
      source_file: evidenceFile.filename,
      findings: findings.length,
      conflicts: Array.isArray(data.conflicts) ? data.conflicts.length : 0,
      replication_status: {
        populated: replicationPopulated,
        unavailable: findings.length - replicationPopulated,
      },
      evidence_gaps: Array.isArray(data.evidence_gaps)
        ? { status: 'recorded', count: data.evidence_gaps.length }
        : { status: 'not-recorded', count: null },
      unreplicated_claims: Array.isArray(data.unreplicated_claims)
        ? { status: 'recorded', count: data.unreplicated_claims.length }
        : { status: 'not-recorded', count: null },
    });
  }

  return {
    schema_version: '1.0.0',
    generated_from: 'evidence/evidence_section_NN.json',
    policy: 'Missing fields are reported as unavailable; no replication state or gap is inferred.',
    expected_sections: expected,
    absent_sections: absentSections,
    valid_empty_sections: validEmptySections,
    sections,
  };
}

export function validateEvidenceCoverage(report, minimumFindings = 1000) {
  const findingTotal = report.sections.reduce((sum, section) => sum + section.findings, 0);
  if (report.absent_sections.length > 0) throw new Error(`Absent evidence packages: ${report.absent_sections.join(', ')}`);
  if (report.sections.length !== report.expected_sections.length) {
    throw new Error(`Expected ${report.expected_sections.length} section packages; found ${report.sections.length}`);
  }
  if (findingTotal < minimumFindings) throw new Error(`Evidence corpus is under-populated: ${findingTotal} findings`);
  return findingTotal;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const report = buildEvidenceCoverage(resolve('evidence'));
  if (process.argv.includes('--write')) {
    writeFileSync(resolve('evidence/EVIDENCE_COVERAGE_REPORT.json'), `${JSON.stringify(report, null, 2)}\n`);
  }
  const findingTotal = validateEvidenceCoverage(report);
  console.log(`Evidence validation passed: ${report.sections.length} packages, ${findingTotal} findings, ${report.valid_empty_sections.length} valid-empty packages.`);
}

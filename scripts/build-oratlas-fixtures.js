#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { readJsonl } = require('./validate-oratlas.js');

const CASES = {
  contradicted_capped: 'clm_f88a8b2eb442ae7f',
  overextended_scope: 'clm_0fde28aeec8b0c15',
  multi_citation: 'clm_c5b4d84c46bcacf3',
};

function buildFixtures(root = path.resolve(__dirname, '..')) {
  const dir = path.join(root, 'knowledge/oratlas');
  const claims = readJsonl(path.join(dir, 'claims.jsonl'));
  const relations = readJsonl(path.join(dir, 'relations.jsonl'));
  const assessments = readJsonl(path.join(dir, 'trust-assessments.jsonl'));
  return {
    schemaVersion: '1.0.0',
    source: { repository: 'dhuzard/ethical-debt-AI-review', commit: '2bc70804d465eabf4f5d51dfa72478671adce2f3' },
    cases: Object.fromEntries(Object.entries(CASES).map(([name, claimId]) => [name, {
      claim: claims.find(claim => claim.id === claimId),
      relations: relations.filter(relation => relation.claimId === claimId),
      trustAssessments: assessments.filter(assessment => assessment.claimId === claimId),
    }])),
  };
}

function serialize(value) { return `${JSON.stringify(value, null, 2)}\n`; }

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const target = path.join(root, 'knowledge/oratlas/fixtures/edge-cases.json');
  const expected = serialize(buildFixtures(root));
  if (process.argv.includes('--write')) {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, expected);
    console.log('Wrote ORAtlas edge-case fixtures.');
  } else {
    const actual = fs.existsSync(target) ? fs.readFileSync(target, 'utf8').replace(/\r\n/gu, '\n') : '';
    if (actual !== expected) { console.error('ORAtlas fixtures are stale'); process.exitCode = 1; }
    else console.log('ORAtlas fixtures are deterministic and current.');
  }
}

module.exports = { CASES, buildFixtures, serialize };

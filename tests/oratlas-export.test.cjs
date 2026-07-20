'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const { readJsonl, validateArtifacts, validateManifest, validateRepository } = require('../scripts/validate-oratlas.js');
const { buildFixtures } = require('../scripts/build-oratlas-fixtures.js');

test('ORAtlas export satisfies the pinned contract and provenance hashes', () => {
  const result = validateRepository();
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.counts, {
    'claims.jsonl': 529, 'citations.jsonl': 994,
    'relations.jsonl': 1392, 'trust-assessments.jsonl': 1392,
  });
});

test('native TRUST remains claim-level and every ORAtlas criterion is not assessed', () => {
  const assessments = readJsonl('knowledge/oratlas/trust-assessments.jsonl');
  assert.ok(assessments.every(record => record.aggregateScore === null && record.aggregateMethod === null));
  assert.ok(assessments.every(record => record.reviewStatus === 'agent-proposed'));
  assert.ok(assessments.every(record => record.evidence.sourceAssessment.unit === 'claim-level score on a 0-100 scale'));
  assert.equal(assessments.filter(record => record.evidence.sourceHumanReview).length, 34);
  assert.ok(assessments.filter(record => record.evidence.sourceHumanReview)
    .every(record => record.evidence.sourceHumanReview.authority === 'source-review'));
});

test('source-side review never asserts ORAtlas platform verification', () => {
  const relations = readJsonl('knowledge/oratlas/relations.jsonl');
  assert.ok(relations.every(record => record.humanReviewed === false));
});

test('malformed manifest and artifact records fail the pinned contract checks', () => {
  assert.match(validateManifest({
    schemaVersion: '1.0.0', review: { title: 'Test' }, repository: { url: 'https://example.org' },
    artifacts: { recordCounts: 'knowledge/record_counts.json' },
  }).join('\n'), /extra property/);
  const errors = validateArtifacts({
    claims: [{ id: 'claim', text: 'Claim', claimType: 'invalid' }],
    citations: [{ id: 'cite' }],
    relations: [{ claimId: 'missing', citationId: 'cite', relationType: 'supports', humanReviewed: true }],
    assessments: [],
  });
  assert.match(errors.join('\n'), /invalid claimType|unknown claim|humanReviewed/);
});

test('immutable ingestion fixtures retain capped and multi-citation edge cases', () => {
  const fixture = buildFixtures();
  assert.equal(fixture.cases.contradicted_capped.claim.id, 'clm_f88a8b2eb442ae7f');
  assert.equal(fixture.cases.overextended_scope.relations.length, 4);
  assert.equal(fixture.cases.multi_citation.relations.length, 4);
});

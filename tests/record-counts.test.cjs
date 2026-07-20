'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const { computeRecordCounts, validateRecordCounts } = require('../scripts/record-counts.js');

test('canonical count manifest exactly matches every source artifact', () => {
  const committed = JSON.parse(fs.readFileSync('knowledge/record_counts.json', 'utf8'));
  assert.deepEqual(committed, computeRecordCounts());
  assert.deepEqual(validateRecordCounts(), []);
  assert.deepEqual(committed.claim_graph.trust_bands, {
    high_trust: 444, moderate_trust: 56, low_trust: 29, critical_or_unreliable: 0,
  });
});

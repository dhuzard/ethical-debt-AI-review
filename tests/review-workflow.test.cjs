'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const { buildReviewPriority } = require('../scripts/review-priority.js');
const { mergeDecisions } = require('../scripts/merge-human-reviews.js');

test('review priority covers every current human-review flag exactly once', () => {
  const priority = buildReviewPriority();
  assert.equal(priority.ranked_claims.length, 29);
  assert.equal(new Set(priority.ranked_claims.map(item => item.claim_id)).size, 29);
  assert.equal(priority.calibration_subset.length, 12);
  assert.ok(priority.ranked_claims.every(item => Number.isInteger(item.priority_score)));
});

test('decision merge is deterministic and does not mutate its input store', () => {
  const store = JSON.parse(fs.readFileSync('knowledge/trust_human_review_overrides.json', 'utf8'));
  const before = JSON.stringify(store);
  const decision = {
    decision_id: 'hr_test_merge', claim_id: 'clm_test', action: 'retain',
    state: 'independently-reviewed', reviewer_id: 'reviewer-test',
    recorded_at: '2026-07-20T00:00:00.000Z', rationale: 'Test decision only.',
  };
  const first = mergeDecisions(store, [decision]);
  const second = mergeDecisions(store, [decision]);
  assert.deepEqual(first, second);
  assert.equal(JSON.stringify(store), before);
});

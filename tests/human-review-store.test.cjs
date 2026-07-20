'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const { appendDecision, validateStore } = require('../scripts/human-review-store.js');

test('committed human-review history has a valid append-only hash chain', () => {
  const store = JSON.parse(fs.readFileSync('knowledge/trust_human_review_overrides.json', 'utf8'));
  assert.deepEqual(validateStore(store), []);
  assert.equal(store.decisions.length, 9);
  assert.ok(store.decisions.every(decision => decision.state === 'adjudicated'));
});

test('editing a historical decision breaks the chain', () => {
  const store = JSON.parse(fs.readFileSync('knowledge/trust_human_review_overrides.json', 'utf8'));
  store.decisions[0].rationale = 'Silently rewritten rationale.';
  assert.match(validateStore(store).join('\n'), /historical record mutated/);
});

test('append helper preserves history and rejects duplicate decision IDs', () => {
  const store = JSON.parse(fs.readFileSync('knowledge/trust_human_review_overrides.json', 'utf8'));
  const decision = {
    decision_id: 'hr_test_pending',
    claim_id: 'clm_test',
    action: 'review',
    state: 'pending',
    reviewer_id: 'reviewer-test',
    recorded_at: '2026-07-20T00:00:00.000Z',
    rationale: 'Test-only pending review.',
  };
  const appended = appendDecision(store, decision);
  assert.equal(appended.decisions.length, store.decisions.length + 1);
  assert.deepEqual(appended.decisions.slice(0, -1), store.decisions);
  assert.deepEqual(validateStore(appended), []);
  assert.throws(() => appendDecision(store, { ...decision, decision_id: store.decisions[0].decision_id }), /already exists/);
});

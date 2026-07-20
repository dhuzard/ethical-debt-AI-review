#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');

function buildReviewPriority(root = path.resolve(__dirname, '..')) {
  const graph = JSON.parse(fs.readFileSync(path.join(root, 'knowledge/claim_graph.json'), 'utf8'));
  const flagged = graph.claims.filter(claim => claim.human_review_required).map(claim => {
    const reasons = claim.trust_score.cap_reasons || [];
    const concern = reasons.includes('contradicted_without_caveat')
      ? 'contradicted_without_caveat'
      : reasons.includes('overextended_scope') ? 'overextended_scope' : 'uncapped_low_trust';
    const base = concern === 'contradicted_without_caveat' ? 100 : concern === 'overextended_scope' ? 90 : 70;
    const argumentativeWeight = ['sec-introduction', 'sec-conclusion'].includes(claim.section_id) ? 10
      : ['causal', 'review_synthesis'].includes(claim.claim_type) ? 5 : 0;
    return {
      claim_id: claim.claim_id,
      section_id: claim.section_id,
      claim_type: claim.claim_type,
      trust_score: claim.trust_score.overall_score,
      concern,
      capped: claim.trust_score.capped,
      priority_score: base + argumentativeWeight,
      priority_basis: [concern, argumentativeWeight ? 'high_argumentative_weight' : 'standard_argumentative_weight'],
    };
  }).sort((left, right) => right.priority_score - left.priority_score
    || left.section_id.localeCompare(right.section_id)
    || left.claim_id.localeCompare(right.claim_id));

  const calibration = [];
  const selected = new Set();
  for (const dimension of ['concern', 'section_id']) {
    for (const value of new Set(flagged.map(item => item[dimension]))) {
      const item = flagged.find(candidate => candidate[dimension] === value && !selected.has(candidate.claim_id));
      if (item && calibration.length < 12) {
        calibration.push(item.claim_id);
        selected.add(item.claim_id);
      }
    }
  }
  for (const item of flagged) {
    if (calibration.length >= 12) break;
    if (!selected.has(item.claim_id)) calibration.push(item.claim_id);
  }

  return {
    schema_version: '1.0.0',
    generated_from: 'knowledge/claim_graph.json',
    strategy: {
      ordering: 'Risk concern first, then argumentative weight, section, and stable claim ID.',
      concern_weights: { contradicted_without_caveat: 100, overextended_scope: 90, uncapped_low_trust: 70 },
      argumentative_weight_bonus: { introduction_or_conclusion: 10, causal_or_review_synthesis: 5, other: 0 },
      calibration_rule: 'Select one claim per concern and section where possible, then fill to 12 by ranked order.',
      scientific_decisions_made: false,
    },
    ranked_claims: flagged,
    calibration_subset: calibration,
  };
}

function serialize(value) { return `${JSON.stringify(value, null, 2)}\n`; }

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const outputPath = path.join(root, 'knowledge/review_priority.json');
  const expected = serialize(buildReviewPriority(root));
  if (process.argv.includes('--write')) {
    fs.writeFileSync(outputPath, expected);
    console.log('Wrote knowledge/review_priority.json');
  } else {
    const actual = fs.existsSync(outputPath) ? fs.readFileSync(outputPath, 'utf8').replace(/\r\n/gu, '\n') : '';
    if (actual !== expected) {
      console.error('knowledge/review_priority.json is stale; run node scripts/review-priority.js --write');
      process.exitCode = 1;
    } else console.log('Review priority is deterministic and current.');
  }
}

module.exports = { buildReviewPriority, serialize };

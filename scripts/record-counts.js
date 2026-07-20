#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');

function readJson(root, relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));
}

function jsonlCount(root, relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8')
    .split(/\r?\n/u).filter(line => line.trim()).length;
}

function computeRecordCounts(root = path.resolve(__dirname, '..')) {
  const graph = readJson(root, 'knowledge/claim_graph.json');
  const reviews = readJson(root, 'knowledge/trust_human_review_overrides.json');
  const contexts = graph.claims.flatMap(claim => claim.citation_contexts);
  const replacements = reviews.decisions.flatMap(decision => decision.claims || []);
  const replacementTexts = new Set(replacements.map(claim => claim.claim_text));
  const reviewedClaims = graph.claims.filter(claim => replacementTexts.has(claim.claim_text));
  const verifiedPassages = contexts.flatMap(context => context.passages || [])
    .filter(passage => passage.verification_status === 'verified');

  return {
    schema_version: '1.0.0',
    definitions: {
      claim: 'One canonical claim record in knowledge/claim_graph.json.',
      citation_context: 'One claim-to-citation context; the same citation may support multiple claims.',
      graph_edge: 'One explicit edge in the native claim graph.',
      unique_citation: 'One distinct citation key across all claim citation contexts.',
      verified_passage: 'One passage whose verification_status is verified; contexts may contain multiple passages.',
      human_decision: 'One historical reviewer decision record; a decision may replace one source claim with several claims.',
      replacement_claim: 'One claim record authored inside a historical human decision.',
      human_review_flag: 'A current graph claim with human_review_required=true; this is pending work, not a completed decision.',
      source_reviewed_relation: 'An exported relation whose current claim text matches a replacement claim from a source-side human decision.',
    },
    claim_graph: {
      claims: graph.claims.length,
      citation_contexts: contexts.length,
      graph_edges: graph.edges.length,
      unique_citation_keys: new Set(contexts.map(context => context.cite_key)).size,
      unique_dois: new Set(contexts.map(context => context.doi).filter(Boolean).map(doi => doi.toLowerCase())).size,
      verified_passages: verifiedPassages.length,
      trust_bands: {
        high_trust: graph.claims.filter(claim => claim.trust_score.trust_label === 'high_trust').length,
        moderate_trust: graph.claims.filter(claim => claim.trust_score.trust_label === 'moderate_trust').length,
        low_trust: graph.claims.filter(claim => claim.trust_score.trust_label === 'low_trust').length,
        critical_or_unreliable: graph.claims.filter(claim => claim.trust_score.trust_label === 'critical_or_unreliable').length,
      },
      capped_claims: graph.claims.filter(claim => claim.trust_score.capped).length,
      human_review_flags: graph.claims.filter(claim => claim.human_review_required).length,
    },
    human_review: {
      decisions: reviews.decisions.length,
      source_claims_replaced: new Set(reviews.decisions.map(decision => decision.claim_id)).size,
      replacement_claim_records: replacements.length,
      replacement_claims_in_current_graph: reviewedClaims.length,
      source_reviewed_relations: reviewedClaims.reduce((sum, claim) => sum + claim.citation_contexts.length, 0),
    },
    oratlas_export: {
      claims: jsonlCount(root, 'knowledge/oratlas/claims.jsonl'),
      citations: jsonlCount(root, 'knowledge/oratlas/citations.jsonl'),
      relations: jsonlCount(root, 'knowledge/oratlas/relations.jsonl'),
      trust_assessments: jsonlCount(root, 'knowledge/oratlas/trust-assessments.jsonl'),
    },
  };
}

function stableJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function validateRecordCounts(root = path.resolve(__dirname, '..')) {
  const expected = stableJson(computeRecordCounts(root));
  const countPath = path.join(root, 'knowledge/record_counts.json');
  const actual = fs.existsSync(countPath) ? fs.readFileSync(countPath, 'utf8').replace(/\r\n/gu, '\n') : '';
  return actual === expected ? [] : ['knowledge/record_counts.json is stale; run node scripts/record-counts.js --write'];
}

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const output = stableJson(computeRecordCounts(root));
  if (process.argv.includes('--write')) {
    fs.writeFileSync(path.join(root, 'knowledge/record_counts.json'), output);
    console.log('Wrote knowledge/record_counts.json');
  } else {
    const errors = validateRecordCounts(root);
    if (errors.length) {
      console.error(errors[0]);
      process.exitCode = 1;
    } else {
      console.log('Record counts match canonical artifacts.');
    }
  }
}

module.exports = { computeRecordCounts, stableJson, validateRecordCounts };

#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');

function auditClaims(root = path.resolve(__dirname, '..')) {
  const graph = JSON.parse(fs.readFileSync(path.join(root, 'knowledge/claim_graph.json'), 'utf8'));
  const flags = [];
  for (const claim of graph.claims) {
    const reasons = [];
    const text = claim.claim_text.trim();
    if (/laid out in\s*[,.;:]|found a stable Reduction estimate/iu.test(text)) reasons.push('suspected_truncated_or_dangling_phrase');
    if (claim.claim_atoms.length === 1 && (text.split(/\s+/u).length >= 75 || (text.match(/;/gu) || []).length >= 2)) {
      reasons.push('long_compound_single_atom');
    }
    if (Object.values(claim.claim_scope || {}).every(value => value == null || value === '')) reasons.push('empty_structured_scope');
    if (reasons.length) flags.push({
      claim_id: claim.claim_id,
      section_id: claim.section_id,
      source_file: claim.source_file,
      paragraph_index: claim.paragraph_index,
      reason_codes: reasons,
      requires_scientific_judgment: true,
    });
  }
  return {
    schema_version: '1.0.0',
    generated_from: 'knowledge/claim_graph.json',
    policy: 'Mechanical structural flags only; no claim is invalidated or edited automatically.',
    flags,
  };
}

function serialize(value) { return `${JSON.stringify(value, null, 2)}\n`; }

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const target = path.join(root, 'knowledge/claim_quality_flags.json');
  const expected = serialize(auditClaims(root));
  if (process.argv.includes('--write')) {
    fs.writeFileSync(target, expected);
    console.log('Wrote knowledge/claim_quality_flags.json');
  } else {
    const actual = fs.existsSync(target) ? fs.readFileSync(target, 'utf8').replace(/\r\n/gu, '\n') : '';
    if (actual !== expected) {
      console.error('knowledge/claim_quality_flags.json is stale');
      process.exitCode = 1;
    } else console.log(`Claim quality audit current: ${auditClaims(root).flags.length} structural flags.`);
  }
}

module.exports = { auditClaims, serialize };

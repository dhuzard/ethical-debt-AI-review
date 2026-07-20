#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { appendDecision, validateStore } = require('./human-review-store.js');

function mergeDecisions(store, decisions) {
  return decisions.reduce((current, decision) => appendDecision(current, decision), store);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const inputIndex = args.indexOf('--input');
  if (inputIndex < 0 || !args[inputIndex + 1]) throw new Error('--input decisions.json is required');
  const root = path.resolve(__dirname, '..');
  const storePath = path.join(root, 'knowledge/trust_human_review_overrides.json');
  const store = JSON.parse(fs.readFileSync(storePath, 'utf8'));
  const input = JSON.parse(fs.readFileSync(path.resolve(args[inputIndex + 1]), 'utf8'));
  const decisions = Array.isArray(input) ? input : input.decisions;
  if (!Array.isArray(decisions)) throw new Error('Input must be an array or an object with decisions[]');
  const merged = mergeDecisions(store, decisions);
  const errors = validateStore(merged);
  if (errors.length) throw new Error(errors.join('\n'));
  const output = `${JSON.stringify(merged, null, 2)}\n`;
  if (args.includes('--apply')) {
    fs.writeFileSync(storePath, output);
    console.log(`Appended ${decisions.length} decision(s) to the canonical store.`);
  } else {
    process.stdout.write(output);
  }
}

module.exports = { mergeDecisions };

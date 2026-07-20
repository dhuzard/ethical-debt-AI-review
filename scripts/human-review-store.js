#!/usr/bin/env node

'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const STORE_PATH = path.join('knowledge', 'trust_human_review_overrides.json');

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]));
  }
  return value;
}

function recordHash(record) {
  const payload = { ...record };
  delete payload.record_hash;
  return `sha256:${crypto.createHash('sha256').update(JSON.stringify(canonical(payload))).digest('hex')}`;
}

function validateStore(store) {
  const errors = [];
  if (store.schema_version !== '2.0.0') errors.push('store schema_version must be 2.0.0');
  if (store.store_policy?.mutation !== 'append-only') errors.push('store_policy.mutation must be append-only');
  const ids = new Set();
  let previousHash = null;
  for (const [index, decision] of (store.decisions || []).entries()) {
    const prefix = decision.decision_id || `decision[${index}]`;
    if (ids.has(decision.decision_id)) errors.push(`${prefix}: duplicate decision_id`);
    ids.add(decision.decision_id);
    if (!['pending', 'independently-reviewed', 'adjudicated'].includes(decision.state)) errors.push(`${prefix}: invalid state`);
    if (!decision.reviewer_id) errors.push(`${prefix}: reviewer_id required`);
    if (!decision.rationale) errors.push(`${prefix}: rationale required`);
    if (!Number.isFinite(Date.parse(decision.recorded_at))) errors.push(`${prefix}: recorded_at must be an ISO timestamp`);
    if (decision.previous_record_hash !== previousHash) errors.push(`${prefix}: previous_record_hash breaks append-only chain`);
    if (decision.record_hash !== recordHash(decision)) errors.push(`${prefix}: record_hash mismatch (historical record mutated)`);
    previousHash = decision.record_hash;
  }
  if (store.chain_head !== previousHash) errors.push('chain_head does not match the last decision');
  return errors;
}

function migrateLegacy(store) {
  let previousHash = null;
  const decisions = store.decisions.map(decision => {
    const migrated = {
      ...decision,
      state: 'adjudicated',
      reviewer_id: decision.reviewer === 'Damien Huzard' ? 'damien-huzard' : decision.reviewer,
      recorded_at: /^\d{4}-\d{2}-\d{2}$/u.test(decision.reviewed_at)
        ? `${decision.reviewed_at}T00:00:00.000Z`
        : decision.reviewed_at,
      rationale: decision.notes,
      previous_record_hash: previousHash,
    };
    migrated.record_hash = recordHash(migrated);
    previousHash = migrated.record_hash;
    return migrated;
  });
  return {
    schema_version: '2.0.0',
    store_policy: {
      mutation: 'append-only',
      allowed_states: ['pending', 'independently-reviewed', 'adjudicated'],
      supersession: 'Append a new decision referencing the earlier decision; never edit or delete history.'
    },
    chain_head: previousHash,
    decisions,
  };
}

function appendDecision(store, decision) {
  const errors = validateStore(store);
  if (errors.length) throw new Error(errors.join('\n'));
  if (store.decisions.some(existing => existing.decision_id === decision.decision_id)) {
    throw new Error(`decision_id already exists: ${decision.decision_id}`);
  }
  const next = {
    ...decision,
    previous_record_hash: store.chain_head,
  };
  next.record_hash = recordHash(next);
  return { ...store, chain_head: next.record_hash, decisions: [...store.decisions, next] };
}

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const storePath = path.join(root, STORE_PATH);
  const store = JSON.parse(fs.readFileSync(storePath, 'utf8'));
  if (process.argv.includes('--migrate')) {
    if (store.schema_version !== '1.0.0') throw new Error('Migration only accepts the legacy 1.0.0 store');
    fs.writeFileSync(storePath, `${JSON.stringify(migrateLegacy(store), null, 2)}\n`);
    console.log(`Migrated ${store.decisions.length} human-review decisions losslessly.`);
  } else if (process.argv.includes('--append')) {
    const inputIndex = process.argv.indexOf('--append') + 1;
    if (!process.argv[inputIndex]) throw new Error('--append requires a decision JSON path');
    const decision = JSON.parse(fs.readFileSync(path.resolve(process.argv[inputIndex]), 'utf8'));
    const next = appendDecision(store, decision);
    fs.writeFileSync(storePath, `${JSON.stringify(next, null, 2)}\n`);
    console.log(`Appended ${decision.decision_id}.`);
  } else {
    const errors = validateStore(store);
    if (errors.length) {
      console.error(errors.join('\n'));
      process.exitCode = 1;
    } else {
      console.log(`Human-review store valid: ${store.decisions.length} append-only decisions.`);
    }
  }
}

module.exports = { appendDecision, canonical, migrateLegacy, recordHash, validateStore };

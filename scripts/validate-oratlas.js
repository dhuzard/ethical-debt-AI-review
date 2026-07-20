#!/usr/bin/env node

'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const TRUST_CRITERIA = [
  'identityIntegrity', 'entailment', 'sourceAccess', 'populationRelevance',
  'interventionExposureRelevance', 'outcomeRelevance', 'methodologicalSafeguards',
  'statisticalSafeguards', 'replicationConvergence', 'conflictDependency',
];
const RELATION_TYPES = new Set(['supports', 'partially-supports', 'contradicts', 'contextualizes', 'method-source', 'background', 'unclear']);
const CLAIM_TYPES = new Set(['empirical', 'mechanistic', 'methodological', 'theoretical', 'normative', 'summary', 'other']);

function readJsonl(filePath) {
  return fs.readFileSync(filePath, 'utf8').split(/\r?\n/u).filter(line => line.trim()).map((line, index) => {
    try { return JSON.parse(line); } catch { throw new Error(`${filePath}:${index + 1}: invalid JSON`); }
  });
}

function extraKeys(value, allowed) {
  return Object.keys(value).filter(key => !allowed.includes(key));
}

function validateManifest(manifest) {
  const errors = [];
  const top = ['schemaVersion', 'review', 'repository', 'publication', 'contact', 'contributors', 'artifacts'];
  const artifacts = ['claims', 'citations', 'relations', 'trustAssessments', 'provenance'];
  if (manifest.schemaVersion !== '1.0.0') errors.push('manifest schemaVersion must be 1.0.0');
  if (!manifest.review?.title) errors.push('manifest review.title required');
  if (!/^https:\/\//u.test(manifest.repository?.url || '')) errors.push('manifest repository.url must be HTTPS');
  for (const key of extraKeys(manifest, top)) errors.push(`manifest extra property: ${key}`);
  for (const key of extraKeys(manifest.artifacts || {}, artifacts)) errors.push(`manifest artifacts extra property: ${key}`);
  for (const [name, artifactPath] of Object.entries(manifest.artifacts || {})) {
    if (!/^[A-Za-z0-9][A-Za-z0-9._-]*(\/[A-Za-z0-9][A-Za-z0-9._-]*)*$/u.test(artifactPath)) {
      errors.push(`manifest artifact ${name} is not a safe repository-relative path`);
    }
  }
  return errors;
}

function validateArtifacts({ claims, citations, relations, assessments }) {
  const errors = [];
  const claimIds = new Set();
  const citationIds = new Set();
  for (const claim of claims) {
    if (!claim.id || !claim.text) errors.push('claim requires id and text');
    if (claimIds.has(claim.id)) errors.push(`duplicate claim ${claim.id}`);
    claimIds.add(claim.id);
    if (claim.claimType && !CLAIM_TYPES.has(claim.claimType)) errors.push(`${claim.id}: invalid claimType`);
  }
  for (const citation of citations) {
    if (!citation.id) errors.push('citation requires id');
    if (citationIds.has(citation.id)) errors.push(`duplicate citation ${citation.id}`);
    citationIds.add(citation.id);
    if (citation.doi && !/^10\.\d{4,9}\/\S+$/u.test(citation.doi)) errors.push(`${citation.id}: invalid DOI`);
  }
  for (const relation of relations) {
    const key = `${relation.claimId}|${relation.citationId}`;
    if (!claimIds.has(relation.claimId)) errors.push(`${key}: unknown claim`);
    if (!citationIds.has(relation.citationId)) errors.push(`${key}: unknown citation`);
    if (!RELATION_TYPES.has(relation.relationType)) errors.push(`${key}: invalid relationType`);
    if (relation.humanReviewed !== false) errors.push(`${key}: platform humanReviewed must remain false for source review`);
  }
  for (const assessment of assessments) {
    const key = `${assessment.claimId}|${assessment.citationId}`;
    if (!claimIds.has(assessment.claimId) || !citationIds.has(assessment.citationId)) errors.push(`${key}: broken assessment reference`);
    if (assessment.reviewStatus !== 'agent-proposed') errors.push(`${key}: source review must not become platform reviewStatus`);
    if (assessment.aggregateScore !== null || assessment.aggregateMethod !== null) errors.push(`${key}: claim score must not be emitted as a relation aggregate`);
    if (JSON.stringify(Object.keys(assessment.criteria)) !== JSON.stringify(TRUST_CRITERIA)) errors.push(`${key}: criteria set/order mismatch`);
    for (const criterion of TRUST_CRITERIA) {
      const value = assessment.criteria[criterion];
      if (value?.rating !== 'not-assessed' || value?.status !== 'not-assessed') errors.push(`${key}: ${criterion} must be not-assessed`);
    }
    const source = assessment.evidence?.sourceAssessment;
    if (source?.protocolVersion !== '2.0.0' || source?.rubricVersion !== '2.0.0') errors.push(`${key}: source protocol/rubric missing`);
    if (source?.unit !== 'claim-level score on a 0-100 scale' || !Number.isInteger(source?.score) || source.score < 0 || source.score > 100) {
      errors.push(`${key}: source assessment unit/score invalid`);
    }
  }
  return errors;
}

function validateRepository(root = path.resolve(__dirname, '..')) {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'review-manifest.json'), 'utf8'));
  const dir = path.join(root, 'knowledge/oratlas');
  const provenance = JSON.parse(fs.readFileSync(path.join(dir, 'provenance.json'), 'utf8'));
  const records = {
    claims: readJsonl(path.join(dir, 'claims.jsonl')),
    citations: readJsonl(path.join(dir, 'citations.jsonl')),
    relations: readJsonl(path.join(dir, 'relations.jsonl')),
    assessments: readJsonl(path.join(dir, 'trust-assessments.jsonl')),
  };
  const errors = [...validateManifest(manifest), ...validateArtifacts(records)];
  const artifactMap = {
    'claims.jsonl': records.claims.length,
    'citations.jsonl': records.citations.length,
    'relations.jsonl': records.relations.length,
    'trust-assessments.jsonl': records.assessments.length,
  };
  for (const [filename, count] of Object.entries(artifactMap)) {
    const content = fs.readFileSync(path.join(dir, filename));
    const expected = provenance.artifacts?.[filename];
    const hash = crypto.createHash('sha256').update(content).digest('hex');
    if (expected?.records !== count || expected?.bytes !== content.length || expected?.sha256 !== hash) {
      errors.push(`${filename}: provenance count/bytes/hash mismatch`);
    }
  }
  return { errors, counts: Object.fromEntries(Object.entries(artifactMap).map(([name, count]) => [name, count])) };
}

if (require.main === module) {
  const result = validateRepository();
  if (result.errors.length) {
    console.error(`ORAtlas validation failed (${result.errors.length}):\n${result.errors.map(error => `- ${error}`).join('\n')}`);
    process.exitCode = 1;
  } else console.log(`ORAtlas contract validation passed: ${JSON.stringify(result.counts)}`);
}

module.exports = { TRUST_CRITERIA, readJsonl, validateArtifacts, validateManifest, validateRepository };

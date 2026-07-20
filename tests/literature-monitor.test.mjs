import test from 'node:test';
import assert from 'node:assert/strict';
import { crossrefUrl, deduplicate, normalizeCandidate, validateConfig } from '../scripts/literature-monitor.mjs';

const config = {
  version: 1,
  from_publication_date: '2026-07-20',
  rows_per_query: 20,
  topics: [{ id: 'topic-one', query: 'a sufficiently specific query', queue_ids: ['SR-01'] }]
};

test('configuration is validated and produces a bounded Crossref URL', () => {
  validateConfig(config);
  const url = new URL(crossrefUrl(config.topics[0], config));
  assert.equal(url.hostname, 'api.crossref.org');
  assert.equal(url.searchParams.get('filter'), 'from-pub-date:2026-07-20');
  assert.equal(url.searchParams.get('rows'), '20');
});

test('candidate metadata is explicitly unverified and DOI-deduplicated', () => {
  const first = normalizeCandidate({ DOI: '10.1/ABC', title: ['Title'], published: { 'date-parts': [[2026, 8, 2]] }, URL: 'https://doi.org/10.1/abc' }, config.topics[0]);
  const second = { ...first, topic_id: 'another-topic' };
  assert.equal(first.status, 'unverified-candidate');
  assert.equal(first.published, '2026-08-02');
  assert.deepEqual(deduplicate([first, second]), [first]);
});

test('invalid and duplicate topics fail closed', () => {
  assert.throws(() => validateConfig({ ...config, topics: [config.topics[0], config.topics[0]] }), /duplicate/);
  assert.throws(() => validateConfig({ ...config, rows_per_query: 1000 }), /1\.\.100/);
});

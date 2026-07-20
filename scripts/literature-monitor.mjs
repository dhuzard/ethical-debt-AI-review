import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export function validateConfig(config) {
  if (config.version !== 1) throw new Error('monitoring config version must be 1');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(config.from_publication_date || '')) throw new Error('from_publication_date must be YYYY-MM-DD');
  if (!Number.isInteger(config.rows_per_query) || config.rows_per_query < 1 || config.rows_per_query > 100) throw new Error('rows_per_query must be 1..100');
  if (!Array.isArray(config.topics) || config.topics.length === 0) throw new Error('topics must be a non-empty array');
  const ids = new Set();
  for (const topic of config.topics) {
    if (!/^[a-z0-9-]+$/.test(topic.id || '') || ids.has(topic.id)) throw new Error(`invalid or duplicate topic id: ${topic.id}`);
    ids.add(topic.id);
    if (typeof topic.query !== 'string' || topic.query.trim().length < 10) throw new Error(`invalid query for ${topic.id}`);
    if (!Array.isArray(topic.queue_ids)) throw new Error(`queue_ids missing for ${topic.id}`);
  }
  return config;
}

export function normalizeCandidate(item, topic) {
  const title = Array.isArray(item.title) ? item.title[0] : item.title;
  const dateParts = item.published?.['date-parts']?.[0] || [];
  return {
    doi: typeof item.DOI === 'string' ? item.DOI.toLowerCase() : null,
    title: title || null,
    published: dateParts.length ? dateParts.map((part, index) => String(part).padStart(index ? 2 : 4, '0')).join('-') : null,
    url: item.URL || null,
    topic_id: topic.id,
    queue_ids: [...topic.queue_ids],
    status: 'unverified-candidate'
  };
}

export function deduplicate(candidates) {
  const seen = new Set();
  return candidates.filter((candidate) => {
    const key = candidate.doi || `${candidate.title || ''}|${candidate.published || ''}`.toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export function crossrefUrl(topic, config) {
  const params = new URLSearchParams({
    'query.bibliographic': topic.query,
    filter: `from-pub-date:${config.from_publication_date}`,
    rows: String(config.rows_per_query),
    select: 'DOI,title,published,URL'
  });
  return `https://api.crossref.org/works?${params}`;
}

export async function fetchCandidates(config, fetchImpl = fetch) {
  const candidates = [];
  for (const topic of config.topics) {
    const response = await fetchImpl(crossrefUrl(topic, config), {
      headers: { 'User-Agent': 'ethical-debt-ai-review/0.1 (mailto:dhuzard@users.noreply.github.com)' }
    });
    if (!response.ok) throw new Error(`Crossref ${response.status} for ${topic.id}`);
    const body = await response.json();
    for (const item of body.message?.items || []) candidates.push(normalizeCandidate(item, topic));
  }
  return deduplicate(candidates);
}

async function main() {
  const args = process.argv.slice(2);
  const config = validateConfig(JSON.parse(fs.readFileSync(path.join(root, 'monitoring/queries.json'), 'utf8')));
  const fetchMode = args.includes('--fetch');
  const outputIndex = args.indexOf('--output');
  if (outputIndex !== -1 && !args[outputIndex + 1]) throw new Error('--output requires a path');
  if (!fetchMode) {
    console.log(`Validated ${config.topics.length} literature-monitor topics; no network request made.`);
    return;
  }
  const candidates = await fetchCandidates(config);
  const artifact = {
    schema_version: 1,
    generated_at: new Date().toISOString(),
    source: 'Crossref REST API',
    from_publication_date: config.from_publication_date,
    notice: 'Unverified candidates only; human screening is required before any review change.',
    candidates
  };
  const serialized = `${JSON.stringify(artifact, null, 2)}\n`;
  if (outputIndex !== -1) fs.writeFileSync(path.resolve(args[outputIndex + 1]), serialized);
  else process.stdout.write(serialized);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}

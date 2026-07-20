#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync } from 'node:fs';
import { relative, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

function snapshot(dir) {
  const root = resolve(dir);
  const files = [];
  function visit(path) {
    for (const entry of readdirSync(path, { withFileTypes: true })) {
      const child = resolve(path, entry.name);
      if (entry.isDirectory()) visit(child);
      else {
        const content = normalizedContent(child);
        files.push({
          path: relative(root, child).replaceAll('\\', '/'),
          bytes: Buffer.byteLength(content),
          sha256: createHash('sha256').update(content).digest('hex'),
        });
      }
    }
  }
  visit(root);
  return files.sort((a, b) => a.path.localeCompare(b.path));
}

function normalizedContent(path) {
  // MyST currently assigns random presentation-only AST `key` values and derives
  // 10-character image DOM ids from them. Ignore only those fields; all content,
  // links, assets, widget ids, and remaining serialized output stay byte-checked.
  if (path.endsWith('.json')) {
    const value = JSON.parse(readFileSync(path, 'utf8'));
    const stripKeys = item => {
      if (Array.isArray(item)) return item.map(stripKeys);
      if (!item || typeof item !== 'object') return item;
      return Object.fromEntries(Object.entries(item)
        .filter(([key]) => key !== 'key')
        .map(([key, child]) => [key, stripKeys(child)]));
    };
    return JSON.stringify(stripKeys(value));
  }
  if (path.endsWith('.html')) {
    return readFileSync(path, 'utf8')
      .replaceAll(/"key":"[A-Za-z0-9_-]+"/g, '"key":"<myst-node-key>"')
      .replaceAll(/\\"key\\":\\"[A-Za-z0-9_-]+\\"/g, '\\"key\\":\\"<myst-node-key>\\"')
      .replaceAll(/<img id="[A-Za-z0-9_-]{10}"/g, '<img id="<myst-node-key>"');
  }
  return readFileSync(path);
}

function build() {
  const command = process.execPath;
  const result = spawnSync(command, [resolve('node_modules/mystmd/dist/myst.cjs'), 'build', '--html'], {
    stdio: 'inherit',
    env: { ...process.env, BASE_URL: process.env.BASE_URL || '/ethical-debt-AI-review' },
  });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}

build();
const first = snapshot('_build/html');
build();
const second = snapshot('_build/html');
if (JSON.stringify(first) !== JSON.stringify(second)) {
  const previous = new Map(first.map(file => [file.path, file.sha256]));
  const changed = second.filter(file => previous.get(file.path) !== file.sha256).map(file => file.path);
  throw new Error(`MyST build is not byte-stable: ${changed.join(', ')}`);
}
console.log(`Deterministic MyST build passed: ${second.length} files.`);

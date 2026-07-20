import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { artifactBytes, sha256 } from '../scripts/release-artifacts.js';

test('release hashes normalize JSON line endings across checkout platforms', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'release-hash-'));
  const lf = path.join(directory, 'lf.json');
  const crlf = path.join(directory, 'crlf.json');
  try {
    fs.writeFileSync(lf, '{\n  "value": 1\n}\n');
    fs.writeFileSync(crlf, '{\r\n  "value": 1\r\n}\r\n');
    assert.equal(sha256(lf), sha256(crlf));
    assert.equal(artifactBytes(lf).byteLength, artifactBytes(crlf).byteLength);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('binary release artifacts retain exact bytes', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'release-hash-'));
  const binary = path.join(directory, 'fixture.png');
  try {
    fs.writeFileSync(binary, Buffer.from([0, 13, 10, 255]));
    assert.deepEqual(artifactBytes(binary), Buffer.from([0, 13, 10, 255]));
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

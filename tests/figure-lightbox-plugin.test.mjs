import test from 'node:test';
import assert from 'node:assert/strict';

import figureLightboxPlugin from '../plugins/figure-lightbox-plugin.mjs';

test('figure lightbox installer uses a deterministic per-document widget id', () => {
  const transform = figureLightboxPlugin.transforms.find(({ name }) => name === 'figure-lightbox-installer');
  const makeTree = () => ({ type: 'root', children: [{ type: 'image', url: 'figure.png' }] });
  const first = makeTree();
  const second = makeTree();
  transform.plugin({}, {})(first, {});
  transform.plugin({}, {})(second, {});
  assert.equal(first.children.at(-1).id, 'figlightbox-1');
  assert.equal(second.children.at(-1).id, 'figlightbox-1');
});

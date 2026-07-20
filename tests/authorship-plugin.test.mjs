import test from 'node:test';
import assert from 'node:assert/strict';
import { resolve } from 'node:path';

import authorshipPlugin from '../plugins/authorship-plugin.mjs';

test('authorship plugin loads YAML and identifies Damien Huzard as the human author', () => {
  const tree = {
    type: 'root',
    children: [{
      type: 'authorship-explorer',
      authorsPath: './authors-detailed.yml',
      height: '600px',
    }],
  };
  const transform = authorshipPlugin.transforms
    .find(({ name }) => name === 'authorship-data-loader');

  transform.plugin({}, {})(tree, {
    path: resolve('content/00_frontmatter.md'),
  });

  const widget = tree.children[0];
  assert.equal(widget.type, 'anywidget');
  assert.equal(widget.id, 'authorship-1');
  const envelope = JSON.parse(widget.model.authors);
  const damien = envelope.primary.find(({ id }) => id === 'damien-huzard');
  assert.deepEqual({
    name: damien.name,
    orcid: damien.orcid,
    careerStage: damien.career_stage,
    isAiTool: damien.is_ai_tool,
  }, {
    name: 'Damien Huzard',
    orcid: '0000-0003-4820-7951',
    careerStage: 'Human author',
    isAiTool: false,
  });
});

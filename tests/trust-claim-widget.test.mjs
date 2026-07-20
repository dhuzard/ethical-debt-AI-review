import test from 'node:test';
import assert from 'node:assert/strict';

import {
  activateTrustPanel,
  activateConcernedText,
  bindHighlightLifecycle,
  displayComponentScore,
  ensureProseHighlightStyles,
  findTextQuote,
  formatTrustScore,
  layoutTrustMarginCards,
  registerTrustMarginCard,
  renderCitationContexts,
  trustBandText,
  releaseTrustPanel,
} from '../content/trust-claim-widget.mjs';

test('opening a TRUST panel closes the previously active panel in the document', () => {
  const doc = {};
  let firstClosed = 0;
  let secondClosed = 0;
  const closeFirst = () => { firstClosed += 1; };
  const closeSecond = () => { secondClosed += 1; };

  activateTrustPanel(doc, closeFirst);
  activateTrustPanel(doc, closeSecond);
  assert.equal(firstClosed, 1);
  assert.equal(secondClosed, 0);
  releaseTrustPanel(doc, closeSecond);
  activateTrustPanel(doc, closeFirst);
  assert.equal(secondClosed, 0);
});

test('visible score bands use canonical TRUST wording', () => {
  assert.equal(trustBandText(null), 'Pending validation');
  assert.equal(trustBandText(85), 'High trust');
  assert.equal(trustBandText(84), 'Moderate trust');
  assert.equal(trustBandText(69), 'Low trust');
  assert.equal(trustBandText(49), 'Critical / unreliable');
});

test('runtime quote matcher fails closed on paraphrases and ambiguity', () => {
  assert.equal(findTextQuote('The exact prose.', 'A paraphrase.'), null);
  assert.equal(findTextQuote('same and same', 'same'), null);
  assert.deepEqual(findTextQuote('same and same', 'same', 'and '), { start: 9, end: 13 });
  assert.deepEqual(findTextQuote('The estimate is US$28 billion.', 'The estimate is US\\$28 billion.'), {
    start: 0,
    end: 30,
  });
});

test('visible TRUST scores use five 20-point components and a 100-point total', () => {
  assert.equal(displayComponentScore(0), 0);
  assert.equal(displayComponentScore(3), 15);
  assert.equal(displayComponentScore(4), 20);
  assert.equal(displayComponentScore(5), null);
  assert.equal(formatTrustScore(85), '85/100');
  assert.equal(formatTrustScore(null), '??/100');
});

test('build-time target highlighting is coordinated and cleanup is idempotent', () => {
  const classes = new Set();
  const target = {
    classList: {
      add: (name) => classes.add(name),
      remove: (name) => classes.delete(name),
    },
  };
  const doc = {
    getElementById: (id) => (id === 'stable-target' ? target : null),
  };
  const el = { ownerDocument: doc };

  const active = activateConcernedText(el, { targetAnchor: 'stable-target' });
  assert.equal(active.highlighted, true);
  assert.equal(classes.has('tc-is-highlighted'), true);
  active.cleanup();
  active.cleanup();
  assert.equal(classes.has('tc-is-highlighted'), false);
});

test('document-level prose highlight styles are installed once with MyST dark mode support', () => {
  const elements = new Map();
  const head = {
    appendChild: (element) => elements.set(element.id, element),
  };
  const doc = {
    head,
    getElementById: (id) => elements.get(id) || null,
    createElement: () => ({ id: '', textContent: '' }),
  };

  ensureProseHighlightStyles(doc);
  ensureProseHighlightStyles(doc);

  assert.equal(elements.size, 1);
  const style = elements.get('tc-prose-highlight');
  assert.match(style.textContent, /\.trust-claim-target\.tc-is-highlighted/);
  assert.match(style.textContent, /mark\.tc-runtime-target/);
  assert.match(style.textContent, /html\.dark/);
});

test('desktop margin layout follows exact targets and stacks nearby cards', () => {
  const makeRectElement = (top, height) => ({
    getBoundingClientRect: () => ({ top, height }),
    isConnected: true,
  });
  const firstTarget = makeRectElement(100, 20);
  const secondTarget = makeRectElement(120, 20);
  const targets = new Map([
    ['first-target', firstTarget],
    ['second-target', secondTarget],
  ]);
  let narrow = false;
  const win = {
    scrollY: 0,
    addEventListener: () => {},
    matchMedia: () => ({ matches: narrow }),
    requestAnimationFrame: (callback) => {
      callback();
      return 1;
    },
  };
  const doc = {
    defaultView: win,
    fonts: null,
    getElementById: (id) => targets.get(id) || null,
    querySelectorAll: () => [],
  };
  const makeCard = (naturalTop) => {
    const aside = {
      dataset: {},
      isConnected: true,
      style: {},
    };
    const host = { closest: () => aside };
    const el = {
      ...makeRectElement(naturalTop, 54),
      ownerDocument: doc,
      getRootNode: () => ({ host }),
    };
    return { aside, el };
  };
  const first = makeCard(20);
  const second = makeCard(20);

  const removeFirst = registerTrustMarginCard(first.el, { targetAnchor: 'first-target' });
  const removeSecond = registerTrustMarginCard(second.el, { targetAnchor: 'second-target' });
  const positions = layoutTrustMarginCards(doc);

  assert.deepEqual(positions.map(({ top }) => top), [100, 162]);
  assert.equal(first.aside.style.transform, 'translateY(80px)');
  assert.equal(second.aside.style.transform, 'translateY(142px)');
  assert.equal(first.aside.dataset.trustClaimLaidOut, 'true');

  narrow = true;
  assert.deepEqual(layoutTrustMarginCards(doc), []);
  assert.equal(first.aside.style.transform, '');
  assert.equal(first.aside.dataset.trustClaimLaidOut, undefined);

  removeFirst();
  removeSecond();
});

test('hovering either the score or exact text highlights both sides', () => {
  class FakeEventTarget {
    constructor() {
      this.listeners = new Map();
      this.classes = new Set();
      this.classList = {
        add: (name) => this.classes.add(name),
        remove: (name) => this.classes.delete(name),
      };
    }

    addEventListener(type, listener) {
      const listeners = this.listeners.get(type) || new Set();
      listeners.add(listener);
      this.listeners.set(type, listeners);
    }

    removeEventListener(type, listener) {
      this.listeners.get(type)?.delete(listener);
    }

    emit(type) {
      for (const listener of this.listeners.get(type) || []) listener();
    }
  }

  const classes = new Set();
  const exactTarget = new FakeEventTarget();
  exactTarget.classList = {
    add: (name) => classes.add(name),
    remove: (name) => classes.delete(name),
  };
  const doc = {
    getElementById: (id) => (id === 'exact-target' ? exactTarget : null),
  };
  const el = { ownerDocument: doc };
  const control = new FakeEventTarget();
  const scoreBadge = new FakeEventTarget();
  const status = { textContent: '' };
  const cleanup = bindHighlightLifecycle(
    control,
    scoreBadge,
    el,
    { targetAnchor: 'exact-target' },
    status,
  );

  control.emit('mouseenter');
  assert.equal(classes.has('tc-is-highlighted'), false);

  scoreBadge.emit('mouseenter');
  assert.equal(classes.has('tc-is-highlighted'), true);
  assert.equal(control.classes.has('tc-card-is-highlighted'), true);
  assert.match(status.textContent, /exact text scored/);
  scoreBadge.emit('mouseleave');
  assert.equal(classes.has('tc-is-highlighted'), false);
  assert.equal(control.classes.has('tc-card-is-highlighted'), false);

  exactTarget.emit('mouseenter');
  assert.equal(classes.has('tc-is-highlighted'), true);
  assert.equal(control.classes.has('tc-card-is-highlighted'), true);
  exactTarget.emit('mouseleave');
  assert.equal(classes.has('tc-is-highlighted'), false);
  assert.equal(control.classes.has('tc-card-is-highlighted'), false);

  control.emit('focus');
  assert.equal(classes.has('tc-is-highlighted'), true);
  scoreBadge.emit('mouseenter');
  scoreBadge.emit('mouseleave');
  assert.equal(classes.has('tc-is-highlighted'), true);
  control.emit('blur');
  assert.equal(classes.has('tc-is-highlighted'), false);

  cleanup();
  scoreBadge.emit('mouseenter');
  control.emit('focus');
  assert.equal(classes.has('tc-is-highlighted'), false);
});

test('citation contexts expose verified passages and atom attribution', () => {
  const html = renderCitationContexts([{
    cite_key: 'Cardin2009',
    doi: '10.1038/nature08002',
    role: 'direct_support',
    source_type: 'primary',
    bibliography_status: 'verified',
    integrity_status: 'verified_no_known_issue',
    direction_match: true,
    supports_claim_atoms: ['a1', 'a2'],
    passages: [{
      text: 'Exact source text.',
      passage_source: 'abstract',
      locator: 'Abstract',
      verification_status: 'verified',
      supports_claim_atoms: ['a1'],
    }],
  }]);
  assert.match(html, /Exact source text\./);
  assert.match(html, /atoms a1/);
  assert.match(html, /Attributed claim atoms: a1, a2/);
  assert.match(html, /bibliography verified/);
});

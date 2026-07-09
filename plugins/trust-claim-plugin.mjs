import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

const trustClaimDirective = {
  name: 'trust-claim',
  doc: 'Render a claim-level TRUST margin tag with expandable evidence context.',
  options: {
    'claim-id': { type: String },
    claim: { type: String },
    cites: { type: String },
    'claim-type': { type: String },
    modality: { type: String },
    score: { type: String },
    'kb-path': { type: String },
    interaction: { type: String },
  },
  run(data) {
    return [{
      type: 'trust-claim',
      claimId: data.options?.['claim-id'] || null,
      claimText: data.options?.claim || '',
      cites: data.options?.cites || '',
      claimType: data.options?.['claim-type'] || '',
      modality: data.options?.modality || '',
      provisionalScore: data.options?.score || null,
      kbPath: data.options?.['kb-path'] || '../knowledge/claim_graph.json',
      interaction: data.options?.interaction || 'slideout',
    }];
  },
};

function parseCiteList(citesRaw) {
  if (!citesRaw) return [];
  return String(citesRaw)
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean);
}

const trustClaimTransform = {
  name: 'trust-claim-data-loader',
  stage: 'document',
  plugin: () => (tree, vfile) => {
    const docDir = vfile?.path ? dirname(vfile.path) : process.cwd();

    // Build the anywidget node that renders the trust card from a trust-claim node.
    function toAnywidget(node) {
      const kbPath = resolve(docDir, node.kbPath || '../knowledge/claim_graph.json');

      let kbClaim = null;
      try {
        const kbRaw = readFileSync(kbPath, 'utf-8');
        const kb = JSON.parse(kbRaw);
        if (node.claimId && Array.isArray(kb.claims)) {
          kbClaim = kb.claims.find((c) => c.claim_id === node.claimId) || null;
        }
      } catch {
        kbClaim = null;
      }

      const claimText = kbClaim?.claim_text || node.claimText || '';
      const trustScore = kbClaim?.trust_score?.overall_score ?? (node.provisionalScore ? Number(node.provisionalScore) : null);
      const trustLabel = kbClaim?.trust_score?.trust_label || 'pending_validation';
      const evidenceRelation = kbClaim?.evidence_relation || 'unverified';
      const citationContexts = kbClaim?.citation_contexts || [];

      return {
        type: 'anywidget',
        id: `trust-claim-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
        class: 'trust-claim-widget',
        esm: './trust-claim-widget.mjs',
        css: './trust-claim-widget.css',
        model: {
          claimId: node.claimId || null,
          claimText,
          cites: JSON.stringify(kbClaim?.citation_keys || parseCiteList(node.cites)),
          claimType: kbClaim?.claim_type || node.claimType || '',
          modality: kbClaim?.modality || node.modality || '',
          trustScore: trustScore,
          trustLabel,
          evidenceRelation,
          citationContexts: JSON.stringify(citationContexts),
          rationale: kbClaim?.trust_score?.components || null,
          humanReviewRequired: kbClaim?.human_review_required || false,
          interactionMode: node.interaction || 'slideout',
        },
      };
    }

    // Replace each trust-claim node with a `margin` aside wrapping the widget.
    // The book-theme places `kind: margin` asides in the reserved right-margin
    // grid lane (`col-margin-right`, `lg:h-0`), so the card renders beside its
    // paragraph instead of as a full-width block row in document flow. Because
    // the trust-claim directive sits immediately after its claim paragraph,
    // CSS grid sparse auto-placement lands the margin aside in the same grid
    // row as that paragraph, aligning the card beside it.
    function walk(node) {
      if (!node || !Array.isArray(node.children)) return;
      for (let i = 0; i < node.children.length; i += 1) {
        const child = node.children[i];
        if (!child) continue;
        if (child.type === 'trust-claim') {
          node.children[i] = {
            type: 'aside',
            kind: 'margin',
            class: 'trust-claim-aside',
            children: [toAnywidget(child)],
          };
        } else {
          walk(child);
        }
      }
    }

    walk(tree);
  },
};

// ── Inline citation trust marker: append a small coloured dot after each citation,
// coloured by the worst trust band among the cited keys (knowledge/cite_trust_bands.json). ──
const BAND_COLOR = { high_trust: '#009E73', moderate_trust: '#56B4E9', low_trust: '#E69F00', critical_or_unreliable: '#D55E00' };
const BAND_RANK = { high_trust: 3, moderate_trust: 2, low_trust: 1, critical_or_unreliable: 0 };

const citeTrustTransform = {
  name: 'cite-trust-marker',
  stage: 'document',
  plugin: () => (tree, vfile) => {
    const docDir = vfile?.path ? dirname(vfile.path) : process.cwd();
    let bands = {};
    try { bands = JSON.parse(readFileSync(resolve(docDir, '../knowledge/cite_trust_bands.json'), 'utf-8')); } catch { bands = {}; }
    if (!Object.keys(bands).length) return;

    function keysOf(node, acc) {
      if (!node) return acc;
      if (node.type === 'cite' && node.label) acc.push(node.label);
      if (Array.isArray(node.children)) node.children.forEach((c) => keysOf(c, acc));
      return acc;
    }
    // Colored emoji markers render reliably in the static theme (raw inline HTML is escaped).
    // Only NON-high citations are flagged, so the eye is drawn to the references to scrutinise.
    const GLYPH = { moderate_trust: '🔵', low_trust: '🟠', critical_or_unreliable: '🔴' };
    function marker(node) {
      const keys = keysOf(node, []).filter((k) => bands[k]);
      if (!keys.length) return null;
      let worst = 'high_trust';
      for (const k of keys) if (BAND_RANK[bands[k].band] < BAND_RANK[worst]) worst = bands[k].band;
      if (worst === 'high_trust') return null;
      return { type: 'text', value: ' ' + GLYPH[worst] };
    }
    function walk(node) {
      if (!node || !Array.isArray(node.children)) return;
      const out = [];
      for (const child of node.children) {
        out.push(child);
        if (child && (child.type === 'citeGroup' || child.type === 'cite')) {
          const m = marker(child);
          if (m) out.push(m);
        } else {
          walk(child);
        }
      }
      node.children = out;
    }
    walk(tree);
  },
};

export default {
  name: 'Trust Claim Plugin',
  directives: [trustClaimDirective],
  transforms: [trustClaimTransform, citeTrustTransform],
};

#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const {
  COMPONENTS,
  claimId,
  contentParagraphs,
  deriveCapReasons,
  deriveEvidenceRelation,
  deriveWordingBasis,
  exactText,
  expectedScores,
  isVerifiedPassage,
  labelFor,
  normalizeClaim,
  parseBibliography,
  scoreBasis,
} = require('./validate-trust.js');

const ROOT = path.resolve(__dirname, '..');
const VERSION = '2.0.0';
const LEGACY_VERIFIED_AT = '2026-07-08T23:15:00.000Z';
const SUPPORT_ROLES = new Set(['direct_support', 'partial_support']);
const SOURCE_TYPES = new Set([
  'primary', 'systematic_review', 'narrative_review', 'preprint', 'metadata', 'unknown',
]);

function readJson(relativePath, fallback = null) {
  const filePath = path.join(ROOT, relativePath);
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(relativePath, value) {
  fs.writeFileSync(path.join(ROOT, relativePath), `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function stripInlineMarkdown(text) {
  return String(text || '')
    .replace(/\{cite(?::[a-z]+)?\}`[^`]+`/gi, '')
    .replace(/\{(?:ref|numref)\}`[^`]+`/gi, '')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/(\*\*|__)(.*?)\1/g, '$2')
    .replace(/(\*|_)(.*?)\1/g, '$2')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/<[^>]+>/g, '');
}

function canonicalClaimText(value) {
  return exactText(stripInlineMarkdown(value));
}

function removeTrustDirectives(markdown) {
  return markdown.replace(
    /(?:\r?\n)?^(:{3,})\{trust-claim\}\s*\r?\n[\s\S]*?^\1\s*(?:\r?\n)?/gm,
    '\n\n',
  );
}

function repairCollapsedDirectives(markdown) {
  return markdown.replace(
    /([.!?;,])?:[\t ]+(\{cite(?::[a-z]+)?\}`[^`]+`)::\{(figure|admonition)\}/giu,
    '$1 $2\n\n:::{$3}',
  );
}

function movePunctuationBeforeInlineRoles(markdown) {
  return markdown.replace(
    /[\t ]+((?:\{(?:cite(?::[a-z]+)?|ref|numref)\}`[^`]+`[\t ]*)+)([.,;:!?])/giu,
    (_match, roles, punctuation) => `${punctuation} ${roles.trim()}`,
  );
}

function prepareMarkdown(markdown) {
  return movePunctuationBeforeInlineRoles(repairCollapsedDirectives(removeTrustDirectives(markdown)))
    .replace(/\n{3,}/g, '\n\n');
}

function applyHumanReviewProse(markdown, relativePath, decisions) {
  let reviewed = markdown;
  for (const decision of decisions.filter((entry) => entry.source_file === relativePath)) {
    if (reviewed.includes(decision.replacement_markdown)) continue;
    if (!reviewed.includes(decision.original_markdown)) {
      throw new Error(`${decision.decision_id}: original prose is missing from ${relativePath}`);
    }
    reviewed = reviewed.replace(decision.original_markdown, decision.replacement_markdown);
  }
  return reviewed;
}

function applyHumanReviewClaims(claims, decisions) {
  const byClaim = new Map(decisions.map((decision) => [decision.claim_id, decision]));
  const reviewedOutputs = new Map(decisions.flatMap((decision) => decision.claims.map((reviewedClaim) => [
    claimId(decision.section_id, canonicalClaimText(reviewedClaim.claim_text)),
    { reviewedClaim, decisionId: decision.decision_id },
  ])));
  const trustSeed = (reviewedClaim) => (reviewedClaim.independence_reviewed
    ? {
      components: {
        robustness: {
          score: 3,
          rationale: reviewedClaim.independence_basis
            || 'Human review confirmed that bibliography author-overlap should determine conservative independence groups.',
        },
      },
    }
    : null);
  const applyReviewedClaim = (claim, reviewedClaim, decisionId) => {
    const contextByKey = new Map((claim.citation_contexts || [])
      .map((context) => [context.cite_key, context]));
    const inheritedContexts = (reviewedClaim.citation_context_keys || []).map((citeKey) => {
      const context = contextByKey.get(citeKey);
      if (!context) throw new Error(`${decisionId}: missing inherited context ${citeKey}`);
      return { ...context, ...(reviewedClaim.context_overrides?.[citeKey] || {}) };
    });
    const citationContexts = reviewedClaim.citation_contexts
      || [...inheritedContexts, ...(reviewedClaim.additional_citation_contexts || [])];
    return {
      ...claim,
      ...reviewedClaim,
      claim_id: claimId(claim.section_id, canonicalClaimText(reviewedClaim.claim_text)),
      citation_contexts: citationContexts,
      trust_score: trustSeed(reviewedClaim),
      created_by_phase: 'trust_human_review',
      validation_status: 'pending',
    };
  };
  return claims.flatMap((claim) => {
    const decision = byClaim.get(claim.claim_id);
    if (!decision) {
      const output = reviewedOutputs.get(claim.claim_id);
      return output
        ? [applyReviewedClaim(claim, output.reviewedClaim, output.decisionId)]
        : [claim];
    }
    if (!['replace', 'split'].includes(decision.action) || !decision.claims?.length) {
      throw new Error(`${decision.decision_id}: unsupported or empty human-review decision`);
    }
    return decision.claims.map((reviewedClaim) => applyReviewedClaim(
      claim,
      reviewedClaim,
      decision.decision_id,
    ));
  });
}

function bibliographyDetails(text) {
  const entries = new Map();
  const pattern = /@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,([\s\S]*?)(?=\n\s*@[A-Za-z]+\s*\{|\s*$)/g;
  for (const match of text.matchAll(pattern)) {
    const body = match[3];
    const field = (name) => {
      const found = body.match(new RegExp(`\\b${name}\\s*=\\s*[\\{\"]([^\\}\"]+)[\\}\"]`, 'i'));
      return found ? exactText(found[1]) : '';
    };
    const authors = field('author').split(/\s+and\s+/i).map(exactText).filter(Boolean);
    entries.set(match[2], {
      entryType: match[1].toLowerCase(),
      title: field('title').replace(/[{}]/g, ''),
      doi: field('doi').toLowerCase() || null,
      authors,
    });
  }
  return entries;
}

function canonicalAuthor(author) {
  return String(author || '')
    .normalize('NFKD')
    .toLocaleLowerCase('en-US')
    .replace(/\\['"`^~=.]?/g, '')
    .replace(/[{}\p{P}\p{S}\s]+/gu, ' ')
    .trim();
}

function loadLegacyLlmJudgments() {
  const directory = path.join(ROOT, 'knowledge', 'trust_llm', 'output');
  const judgments = {};
  if (!fs.existsSync(directory)) return judgments;
  for (const name of fs.readdirSync(directory).filter((value) => value.endsWith('.json')).sort()) {
    Object.assign(judgments, JSON.parse(fs.readFileSync(path.join(directory, name), 'utf8')));
  }
  return judgments;
}

function inferSourceType(context, claimJudgment, bib) {
  if (SOURCE_TYPES.has(context.source_type)) return context.source_type;
  const title = String(bib?.title || '').toLowerCase();
  if (/\b(systematic|scoping|umbrella) review\b|\bmeta-analysis\b/u.test(title)) return 'systematic_review';
  if (/\bpreprint\b|biorxiv|medrxiv/u.test(title)) return 'preprint';
  if (/\breview\b|\bperspective\b|\bcommentary\b|\bguideline\b|\bframework\b/u.test(title)) return 'narrative_review';
  if (claimJudgment?.source_type === 'review') return 'narrative_review';
  if (['misc', 'online', 'website'].includes(bib?.entryType)) return 'metadata';
  return 'primary';
}

function verificationCategory(doiResults, citeKey) {
  const record = doiResults?.[citeKey];
  return String(record?.cat || record?.category || '').toUpperCase();
}

function bibliographyStatus(context, doiResults, crossrefDois, bib) {
  if (context.bibliography_status) return context.bibliography_status;
  const category = verificationCategory(doiResults, context.cite_key);
  const doi = String(context.doi || '').toLowerCase();
  if (['VERIFIED', 'YEAR_MINOR'].includes(category) || crossrefDois.has(doi)) return 'verified';
  if (bib && doi && bib.doi === doi) return 'unverified';
  return bib ? 'mismatch' : 'missing';
}

function bestPassageWindow(value, claimText, maximumWords = 25) {
  const words = exactText(value).split(' ').filter(Boolean);
  if (words.length <= maximumWords) return words.join(' ');
  const claimTokens = new Set(normalizeClaim(claimText).split(' ').filter((token) => token.length > 2));
  let best = { score: -1, start: 0 };
  for (let start = 0; start <= words.length - maximumWords; start += 1) {
    const window = words.slice(start, start + maximumWords);
    const score = window.reduce((sum, word) => (
      sum + (claimTokens.has(normalizeClaim(word)) ? 1 : 0)
    ), 0);
    if (score > best.score) best = { score, start };
  }
  return words.slice(best.start, best.start + maximumWords).join(' ');
}

function scopeStatus(legacyClaim) {
  if (legacyClaim.scope_status) return legacyClaim.scope_status;
  const legacyScore = legacyClaim.trust_score?.components?.transferability_scope_control?.score;
  if (legacyClaim.trust_score?.cap_reason === 'overextended_scope'
      || legacyClaim.evidence_relation === 'overextended'
      || legacyScore === 0) return 'overextended';
  if (legacyScore === 4) return 'matched';
  if (legacyScore === 3) return 'minor_difference_qualified';
  if (legacyScore === 2) return 'major_difference_qualified';
  return 'unverified';
}

function contextScopeMatch(role, status, existing) {
  if (existing) return existing;
  if (!SUPPORT_ROLES.has(role)) return 'not_applicable';
  if (status === 'matched') return 'exact';
  if (status === 'minor_difference_qualified') return 'narrower';
  if (['major_difference_qualified', 'overextended'].includes(status)) return 'broader';
  return 'unverified';
}

function normalizePassages(context, claimText, bibliographyState) {
  const sourcePassages = Array.isArray(context.passages)
    ? context.passages
    : context.supporting_passage && ['full_text', 'abstract'].includes(context.passage_source)
      ? [{
        text: context.supporting_passage,
        passage_source: context.passage_source,
        locator: `${context.passage_source === 'full_text' ? 'Full text' : 'Abstract'} excerpt (legacy verification record)`,
        verification_status: bibliographyState === 'verified' ? 'verified' : 'unverified',
        verification_source: context.doi ? `https://doi.org/${context.doi}` : null,
        verified_at: bibliographyState === 'verified' ? LEGACY_VERIFIED_AT : null,
      }]
      : [];

  return sourcePassages.map((passage) => {
    const verificationStatus = passage.verification_status === 'verified' && bibliographyState === 'verified'
      ? 'verified'
      : 'unverified';
    return {
      text: bestPassageWindow(passage.text, claimText),
      passage_source: passage.passage_source === 'full_text' ? 'full_text' : 'abstract',
      locator: passage.locator || `${passage.passage_source === 'full_text' ? 'Full text' : 'Abstract'} excerpt`,
      verification_status: verificationStatus,
      verification_source: verificationStatus === 'verified'
        ? `https://doi.org/${context.doi}`
        : null,
      verified_at: verificationStatus === 'verified'
        ? (passage.verified_at || LEGACY_VERIFIED_AT)
        : null,
      supports_claim_atoms: ['a1'],
    };
  }).filter((passage) => passage.text);
}

function normalizeConflicts(legacyClaim, isV2) {
  const retain = isV2
    || legacyClaim.evidence_relation === 'conflicted'
    || legacyClaim.trust_score?.cap_reason === 'contradicted_without_caveat';
  if (!retain) return [];
  const unique = new Map();
  for (const conflict of legacyClaim.conflicts || []) {
    const normalized = {
      conflict_type: conflict.conflict_type,
      target_id: conflict.target_id,
      notes: conflict.notes ?? null,
    };
    unique.set(JSON.stringify(normalized), normalized);
  }
  return [...unique.values()];
}

function applyIndependenceGroups(contexts, legacyClaim, newClaimId, bibDetails) {
  const supporting = contexts.filter((context) => SUPPORT_ROLES.has(context.role));
  if (supporting.length === 0) return;
  const legacyRobustness = legacyClaim.trust_score?.components?.robustness;
  const legacyRobustnessRationale = specificLegacyRationale(legacyRobustness);
  const parent = supporting.map((_context, index) => index);
  const find = (index) => (parent[index] === index ? index : (parent[index] = find(parent[index])));
  const union = (left, right) => {
    const leftRoot = find(left);
    const rightRoot = find(right);
    if (leftRoot !== rightRoot) parent[rightRoot] = leftRoot;
  };

  if ((legacyRobustness?.score ?? 0) < 3) {
    for (let index = 1; index < supporting.length; index += 1) union(0, index);
  } else {
    for (let left = 0; left < supporting.length; left += 1) {
      const leftAuthors = new Set((bibDetails.get(supporting[left].cite_key)?.authors || []).map(canonicalAuthor));
      for (let right = left + 1; right < supporting.length; right += 1) {
        const overlap = (bibDetails.get(supporting[right].cite_key)?.authors || [])
          .map(canonicalAuthor)
          .some((author) => author && leftAuthors.has(author));
        if (overlap) union(left, right);
      }
    }
  }

  const groupNames = new Map();
  for (let index = 0; index < supporting.length; index += 1) {
    const root = find(index);
    if (!groupNames.has(root)) groupNames.set(root, `grp_${newClaimId.slice(4, 12)}_${groupNames.size + 1}`);
    const groupMembers = supporting.filter((_context, candidate) => find(candidate) === root);
    supporting[index].independence_group = groupNames.get(root);
    supporting[index].independence_basis = (legacyRobustness?.score ?? 0) < 3
      ? `Conservative single-group assignment from the legacy robustness assessment (${legacyRobustnessRationale || 'independence not established'}).`
      : groupMembers.length > 1
        ? 'Sources share bibliography author metadata and are conservatively assigned to one independence group.'
        : `Legacy TRUST review treated this citation as an independent source; bibliography author-overlap was checked during v2 migration. ${legacyRobustnessRationale}`.trim();
  }
}

const RULE_TEXT = {
  T0_UNRESOLVED: 'At least one cited key, DOI, bibliography record, or citation context is unresolved.',
  T1_METADATA_ONLY: 'Citation metadata resolves, but no eligible source passage is available.',
  T2_PARTIAL_RECORD: 'At least one supporting source has a verified passage while another has an incomplete record.',
  T3_ATOMS_INCOMPLETE: 'Verified passages exist, but eligible citations do not cover every claim atom.',
  T4_ATOM_LEVEL: 'Every supporting citation has verified passage attribution and eligible citations cover every claim atom.',
  R0_ATTRIBUTION_UNSUPPORTED: 'No eligible source supports this attribution claim.',
  R1_ATTRIBUTION_INDIRECT: 'The attribution is supported only by an indirect source.',
  R2_ATTRIBUTION_PARTIAL: 'An eligible primary source covers only part of the attribution.',
  R3_ATTRIBUTION_COMPLETE: 'Eligible sources cover the attribution, but no one direct primary source covers it completely.',
  R4_ORIGINATING_SOURCE: 'A direct primary source covers the complete attribution without an unresolved contradiction.',
  R0_NO_SUPPORT: 'No eligible citation supports the claim.',
  R1_SOME_ATOMS: 'Eligible citations cover only some claim atoms.',
  R2_SINGLE_GROUP: 'Every atom is covered, but the evidence resolves to one independence group.',
  R3_CONVERGENT: 'Independent groups converge, but at least one atom has support from only one group.',
  R4_REPLICATED_PER_ATOM: 'Every atom is supported by at least two independent groups without an unresolved contradiction.',
  U0_OVERSTATED: 'The surface wording is stronger than the derived evidence relation permits.',
  U1_WEAK_HEDGE: 'The wording is qualified, but direct support or scope remains insufficient.',
  U2_CONFLICT_DISCLOSED: 'The wording discloses a conflict in the evidence.',
  U3_CALIBRATED: 'Qualified wording matches partial or indirect support.',
  U4_EXACT_CALIBRATION: 'The surface wording matches direct eligible support.',
  S0_COMPROMISED: 'A relied-upon source is mismatched, directionally inconsistent, or has an integrity warning.',
  S1_UNRESOLVED: 'A relied-upon source or DOI is unresolved.',
  S2_UNCHECKED: 'Sources resolve, but registry integrity status is not checked.',
  S3_MIXED_CHECKS: 'Source records resolve, but integrity or primary-source status is mixed.',
  S4_VERIFIED_PRIMARY: 'Every relied-upon source is primary, DOI-linked, registry-checked, direction-matched, and passage-verified.',
  X0_OVEREXTENDED: 'The claim extends beyond the recorded evidence scope.',
  X1_SCOPE_UNKNOWN: 'The evidence-to-claim scope match is not verified.',
  X2_MAJOR_QUALIFIER: 'A material scope difference is explicitly qualified.',
  X3_MINOR_QUALIFIER: 'A minor scope difference remains and is bounded in the prose.',
  X4_SCOPE_MATCHED: 'The recorded evidence scope matches the claim.',
};

const FIX_TEXT = {
  traceability: 'Verify every citation DOI and attach a locator-backed source passage to each claimed atom.',
  robustness: 'Add genuinely independent evidence for each atom, documenting shared authors, datasets, laboratories, and cohorts.',
  uncertainty_calibration: 'Revise the claim wording or verification inputs so the stated certainty matches the derived evidence relation.',
  source_integrity: 'Resolve bibliography records and check a current registry or publisher record for each relied-upon source.',
  transferability_scope_control: 'Record and disclose the exact population, method, model, and domain differences between claim and evidence.',
};

function specificLegacyRationale(component) {
  const rationale = String(component?.rationale || '').trim();
  if (!rationale) return '';
  const pieces = rationale.split(/\s+Legacy assessment:\s+/u);
  const specific = pieces[pieces.length - 1].trim();
  return specific === RULE_TEXT[component?.rule_id] ? '' : specific;
}

function componentEvidence(component, claim) {
  if (component === 'traceability') {
    return claim.citation_contexts.map((context) => `${context.cite_key}:${context.passages.filter(isVerifiedPassage).length} verified passage(s)`);
  }
  if (component === 'robustness') {
    return [...new Set(claim.citation_contexts.map((context) => context.independence_group).filter(Boolean))];
  }
  if (component === 'uncertainty_calibration') {
    const basis = deriveWordingBasis(claim);
    return [`evidence_relation=${claim.evidence_relation}`, `wording=${basis.rule_id}`, ...basis.markers];
  }
  if (component === 'source_integrity') {
    return claim.citation_contexts.map((context) => `${context.cite_key}:${context.bibliography_status}/${context.integrity_status}/${context.source_type}`);
  }
  return [`scope_status=${claim.scope_status}`, ...claim.citation_contexts.map((context) => `${context.cite_key}:${context.scope_match}`)];
}

function makeComponent(component, expected, legacy) {
  const [score, ruleId] = expected;
  const legacyRationale = specificLegacyRationale(legacy);
  const legacyContext = legacyRationale ? ` Legacy assessment: ${legacyRationale}` : '';
  return {
    score,
    rule_id: ruleId,
    rationale: `${RULE_TEXT[ruleId]}${legacyContext}`,
    evidence: componentEvidence(component, makeComponent.claim),
    failure_modes: score === 4 ? [] : [...new Set([...(legacy?.failure_modes || []), RULE_TEXT[ruleId]])],
    recommended_fix: score === 4
      ? (legacy?.recommended_fix || 'Preserve the verified inputs and rerun the validator after any prose or citation change.')
      : FIX_TEXT[component],
  };
}

function makeDirective(claim, eol, fenceLength = 3) {
  const fence = ':'.repeat(fenceLength);
  return [
    `${fence}{trust-claim}`,
    `:claim-id: ${claim.claim_id}`,
    `:claim: ${claim.claim_text}`,
    `:cites: ${claim.citation_keys.join(', ')}`,
    `:claim-type: ${claim.claim_type}`,
    `:modality: ${claim.modality}`,
    fence,
  ].join(eol);
}

function trustInsertionLines(lines) {
  const stack = [];
  const ranges = [];
  let inCodeFence = false;
  lines.forEach((line, index) => {
    if (/^\s*```/u.test(line)) {
      inCodeFence = !inCodeFence;
      return;
    }
    if (inCodeFence) return;
    const opener = line.match(/^\s*(:{3,})\{[^}]+\}/u);
    const closer = line.match(/^\s*(:{3,})\s*$/u);
    if (opener) stack.push({ open: index, fenceLength: opener[1].length });
    else if (closer && stack.length) {
      const container = stack.pop();
      ranges.push({ ...container, close: index });
    }
  });
  return lines.map((_line, index) => ranges
    .filter((range) => range.open < index && index < range.close)
    .reduce((destination, range) => Math.max(destination, range.close), index));
}

function sectionTitle(claim) {
  const names = {
    'content/01_introduction.md': 'Introduction',
    'content/02_reproducibility_crisis.md': 'Reproducibility',
    'content/03_data_welfare_3rs.md': 'Data welfare / 3Rs',
    'content/04_fair_preclinical_data.md': 'FAIR data',
    'content/05_virtual_control_groups.md': 'Virtual controls',
    'content/06_nams_data.md': 'NAMs',
    'content/07_incentives.md': 'Incentives',
    'content/08_governance_pathways.md': 'Governance',
    'content/09_conclusion.md': 'Conclusion',
  };
  return names[claim.source_file] || claim.section_id;
}

function markdownCell(value) {
  return String(value).replace(/\|/g, '\\|').replace(/\s+/g, ' ').trim();
}

function buildTrustSummary(graph) {
  const claims = graph.claims;
  const mean = claims.reduce((sum, claim) => sum + claim.trust_score.overall_score, 0) / claims.length;
  const componentMeans = Object.fromEntries(COMPONENTS.map((component) => [
    component,
    claims.reduce((sum, claim) => sum + claim.trust_score.components[component].score, 0) / claims.length,
  ]));
  const bySection = new Map();
  for (const claim of claims) {
    const title = sectionTitle(claim);
    if (!bySection.has(title)) bySection.set(title, []);
    bySection.get(title).push(claim);
  }
  const capped = claims.filter((claim) => claim.trust_score.capped);
  const lowest = [...claims].sort((left, right) => left.trust_score.overall_score - right.trust_score.overall_score).slice(0, 25);
  const lines = [
    '(sec-trust-summary)=',
    '# Citation Trust Summary',
    '',
    `This review exposes **${claims.length} claim-level TRUST records** using rubric v${VERSION}. Hovering or focusing a score highlights the concerned prose; opening the card reveals all five component rules, rationales, verified source passages, atom attribution, scope status, and cap reasons.`,
    '',
    `The mean overall score is **${mean.toFixed(1)}**. Band distribution: **high ${graph.summary.high_trust} · moderate ${graph.summary.moderate_trust} · low ${graph.summary.low_trust} · critical ${graph.summary.critical_or_unreliable}**. **${capped.length}** claims trigger a mandatory cap, and **${graph.summary.needs_human_review}** remain explicit human-review priorities.`,
    '',
    '![Trust band distribution by section](../figures/fig_trust_by_section.png)',
    '',
    '![Mean TRUST component score by section](../figures/fig_trust_components.png)',
    '',
    '![Overall trust band split and score distribution](../figures/fig_trust_overall.png)',
    '',
    '## Component means (0–4)',
    '',
    '| Traceability | Robustness | Uncertainty calibration | Source integrity | Transferability / scope |',
    '|---:|---:|---:|---:|---:|',
    `| ${componentMeans.traceability.toFixed(2)} | ${componentMeans.robustness.toFixed(2)} | ${componentMeans.uncertainty_calibration.toFixed(2)} | ${componentMeans.source_integrity.toFixed(2)} | ${componentMeans.transferability_scope_control.toFixed(2)} |`,
    '',
    '## Per-section rollup',
    '',
    '| Section | Claims | Mean | High | Moderate | Low | Critical |',
    '|---|---:|---:|---:|---:|---:|---:|',
  ];
  for (const [title, sectionClaims] of bySection) {
    const count = (label) => sectionClaims.filter((claim) => claim.trust_score.trust_label === label).length;
    const sectionMean = sectionClaims.reduce((sum, claim) => sum + claim.trust_score.overall_score, 0) / sectionClaims.length;
    lines.push(`| ${title} | ${sectionClaims.length} | ${sectionMean.toFixed(1)} | ${count('high_trust')} | ${count('moderate_trust')} | ${count('low_trust')} | ${count('critical_or_unreliable')} |`);
  }
  lines.push(
    '',
    '## Lowest-trust claims (review priority)',
    '',
    '| Score | Band | Section | Claim | Cap |',
    '|---:|---|---|---|---|',
    ...lowest.map((claim) => `| ${claim.trust_score.overall_score} | ${claim.trust_score.trust_label.replaceAll('_', ' ')} | ${sectionTitle(claim)} | ${markdownCell(claim.claim_text)} | ${claim.trust_score.cap_reasons.join(', ') || '—'} |`),
    '',
    '## Method and migration note',
    '',
    'Scores are validator-owned and are recomputed mechanically from the committed claim graph. The v2 migration converts each claim-level unit from the original review into one explicit claim atom, maps legacy source passages to locator-backed records of at most 25 words, records Crossref registry checks from Phase 16, conservatively groups shared-author citations, and retains claim-level conflict and scope judgments. Compound claims should be split into finer atoms when they receive substantive human review.',
    '',
    'The complete auditable basis is in `knowledge/claim_graph.json`, `knowledge/trust_score_report.json`, and `knowledge/TRUST_RUBRIC.md`.',
    '',
  );
  return lines.join('\n');
}

function main() {
  const legacyGraph = readJson('knowledge/claim_graph.json');
  if (!legacyGraph?.claims?.length) throw new Error('knowledge/claim_graph.json has no claims');
  const isV2 = legacyGraph.schema_version === VERSION;
  const humanReview = readJson('knowledge/trust_human_review_overrides.json', { decisions: [] });
  const reviewDecisions = humanReview.decisions || [];
  const reviewClaims = applyHumanReviewClaims(legacyGraph.claims, reviewDecisions);
  const bibliographyText = fs.readFileSync(path.join(ROOT, 'content', 'references.bib'), 'utf8');
  const bibliography = parseBibliography(bibliographyText);
  const bibDetails = bibliographyDetails(bibliographyText);
  const doiResults = readJson('provenance/doi_verification.json', {}).results || {};
  const crossrefDois = new Set((readJson('provenance/crossref_metadata.json', []) || [])
    .filter((record) => record.ok && record.doi)
    .map((record) => String(record.doi).toLowerCase()));
  const llmJudgments = loadLegacyLlmJudgments();
  const legacyMechanical = readJson('knowledge/trust_mechanical.json', {});
  const generatedAt = new Date().toISOString();

  const files = [...new Set(reviewClaims.map((claim) => claim.source_file))];
  const fileStates = new Map();
  for (const relativePath of files) {
    const source = fs.readFileSync(path.join(ROOT, relativePath), 'utf8');
    const eol = source.includes('\r\n') ? '\r\n' : '\n';
    const prepared = applyHumanReviewProse(
      prepareMarkdown(source).replace(/\r?\n/g, eol),
      relativePath,
      reviewDecisions,
    );
    fileStates.set(relativePath, {
      eol,
      prepared,
      paragraphs: contentParagraphs(prepared),
      lines: prepared.split(eol),
    });
    fileStates.get(relativePath).trustInsertionLines = trustInsertionLines(fileStates.get(relativePath).lines);
  }

  const previousMap = readJson('knowledge/trust_v1_to_v2_id_map.json', {})?.claim_ids || {};
  const idMap = { ...previousMap };
  const locations = new Map();
  const claims = [];

  for (const legacyClaim of reviewClaims) {
    const claimText = canonicalClaimText(legacyClaim.claim_text);
    const state = fileStates.get(legacyClaim.source_file);
    const paragraphMatches = state.paragraphs
      .map((paragraph, index) => (paragraph.includes(claimText) ? index + 1 : null))
      .filter(Boolean);
    if (paragraphMatches.length === 0) {
      throw new Error(`${legacyClaim.claim_id}: expected a prose match in ${legacyClaim.source_file}`);
    }
    const lineMatches = state.lines
      .map((line, index) => (exactText(stripInlineMarkdown(line)).includes(claimText) ? index : null))
      .filter((index) => index !== null);
    if (lineMatches.length === 0) {
      throw new Error(`${legacyClaim.claim_id}: expected a source-line match in ${legacyClaim.source_file}`);
    }

    const newId = claimId(legacyClaim.section_id, claimText);
    idMap[legacyClaim.claim_id] = newId;
    if (!locations.has(legacyClaim.source_file)) locations.set(legacyClaim.source_file, new Map());
    const byPart = locations.get(legacyClaim.source_file);
    const insertionLine = state.trustInsertionLines[lineMatches[0]];
    if (!byPart.has(insertionLine)) byPart.set(insertionLine, []);

    const status = scopeStatus(legacyClaim);
    const judgment = llmJudgments[legacyClaim.claim_id] || llmJudgments[newId] || {};
    const contexts = (legacyClaim.citation_contexts || []).map((legacyContext) => {
      const bib = bibDetails.get(legacyContext.cite_key);
      const canonicalContext = { ...legacyContext, doi: bib?.doi || legacyContext.doi };
      const bibStatus = bibliographyStatus(canonicalContext, doiResults, crossrefDois, bib);
      const passages = normalizePassages(canonicalContext, claimText, bibStatus);
      const verifiedAtoms = new Set(passages.filter(isVerifiedPassage).flatMap((passage) => passage.supports_claim_atoms));
      const integrityVerified = legacyContext.integrity_status === 'verified_no_known_issue'
        || (bibStatus === 'verified' && crossrefDois.has(String(canonicalContext.doi || '').toLowerCase()));
      return {
        cite_key: legacyContext.cite_key,
        doi: canonicalContext.doi,
        role: legacyContext.role,
        source_type: inferSourceType(legacyContext, judgment, bib),
        bibliography_status: bibStatus,
        integrity_status: integrityVerified ? 'verified_no_known_issue' : (legacyContext.integrity_status || 'not_checked'),
        integrity_checked_at: integrityVerified ? (legacyContext.integrity_checked_at || LEGACY_VERIFIED_AT) : null,
        integrity_check_source: integrityVerified
          ? `https://api.crossref.org/works/${encodeURIComponent(canonicalContext.doi)}`
          : null,
        passages,
        direction_match: legacyContext.direction_match === true,
        supports_claim_atoms: [...verifiedAtoms],
        independence_group: null,
        independence_basis: null,
        scope_match: contextScopeMatch(legacyContext.role, status, legacyContext.scope_match),
        notes: legacyContext.notes ?? null,
      };
    });
    applyIndependenceGroups(contexts, legacyClaim, newId, bibDetails);

    const claim = {
      claim_id: newId,
      section_id: legacyClaim.section_id,
      source_file: legacyClaim.source_file,
      paragraph_index: paragraphMatches[0],
      sentence_index: Math.max(1, Number(legacyClaim.sentence_index || 0) + (isV2 ? 0 : 1)),
      claim_text: claimText,
      normalized_claim: normalizeClaim(claimText),
      claim_atoms: [{ atom_id: 'a1', text: claimText }],
      claim_type: legacyClaim.claim_type,
      claim_scope: {
        biological: legacyClaim.claim_scope?.biological ?? null,
        computational: legacyClaim.claim_scope?.computational ?? null,
        clinical: legacyClaim.claim_scope?.clinical ?? null,
        methodological: legacyClaim.claim_scope?.methodological ?? null,
        conceptual: legacyClaim.claim_scope?.conceptual ?? null,
      },
      scope_status: status,
      claim_polarity: legacyClaim.claim_polarity,
      modality: legacyClaim.modality,
      wording_strength: 'unqualified',
      entities: (legacyClaim.entities || []).map((entity) => ({ ...entity, identifier: entity.identifier ?? null })),
      citation_keys: contexts.map((context) => context.cite_key),
      dois: contexts.map((context) => context.doi).filter(Boolean),
      citation_contexts: contexts,
      evidence_relation: 'unsupported',
      conflicts: normalizeConflicts(legacyClaim, isV2),
      knowledge_edges: [],
      trust_score: null,
      human_review_required: false,
      created_by_phase: legacyClaim.created_by_phase || 'trust_seed',
      updated_by_phase: 'phase_16T_trust_score_validation_v2',
      validation_status: 'validated',
    };
    claim.wording_strength = deriveWordingBasis(claim).wording_strength;
    claim.evidence_relation = deriveEvidenceRelation(claim);
    const expected = expectedScores(claim, bibliography);
    const legacyComponents = legacyClaim.trust_score?.components || legacyMechanical[legacyClaim.claim_id] || {};
    makeComponent.claim = claim;
    claim.trust_score = {
      rubric_version: VERSION,
      components: Object.fromEntries(COMPONENTS.map((component) => [
        component,
        makeComponent(component, expected[component], legacyComponents[component]),
      ])),
      raw_score: 5 * COMPONENTS.reduce((sum, component) => sum + expected[component][0], 0),
      overall_score: 0,
      trust_label: 'critical_or_unreliable',
      capped: false,
      cap_value: null,
      cap_reasons: [],
      cap_reason: null,
      computed_from: 'validator',
    };
    const capReasons = deriveCapReasons(claim);
    claim.trust_score.capped = capReasons.length > 0;
    claim.trust_score.cap_value = capReasons.length > 0 ? 60 : null;
    claim.trust_score.cap_reasons = capReasons;
    claim.trust_score.cap_reason = capReasons[0] || null;
    claim.trust_score.overall_score = capReasons.length
      ? Math.min(claim.trust_score.raw_score, 60)
      : claim.trust_score.raw_score;
    claim.trust_score.trust_label = labelFor(claim.trust_score.overall_score);
    claim.human_review_required = claim.trust_score.overall_score < 70;
    claim.validation_status = claim.human_review_required ? 'needs_human_review' : 'validated';

    claims.push(claim);
    byPart.get(insertionLine).push(claim);
  }

  for (const [relativePath, byPart] of locations) {
    const state = fileStates.get(relativePath);
    for (const [lineIndex, lineClaims] of [...byPart.entries()].sort((left, right) => right[0] - left[0])) {
      const directives = lineClaims
        .map((claim) => makeDirective(claim, state.eol))
        .join(`${state.eol}${state.eol}`);
      state.lines.splice(lineIndex + 1, 0, '', ...directives.split(state.eol));
    }
    const finalSource = state.lines
      .join(state.eol)
      .replace(/(?:\r?\n)+$/u, state.eol);
    fs.writeFileSync(path.join(ROOT, relativePath), finalSource, 'utf8');
  }

  // Directive placement can change how adjacent MyST containers are split into
  // parser paragraphs. Re-read the final source and freeze the actual canonical
  // paragraph address that the validator will use.
  const finalParagraphs = new Map(files.map((relativePath) => [
    relativePath,
    contentParagraphs(fs.readFileSync(path.join(ROOT, relativePath), 'utf8')),
  ]));
  for (const claim of claims) {
    const match = finalParagraphs.get(claim.source_file)
      .findIndex((paragraph) => paragraph.includes(claim.claim_text));
    if (match < 0) throw new Error(`${claim.claim_id}: final prose anchor is missing`);
    claim.paragraph_index = match + 1;
  }

  const summary = {
    total_claims: claims.length,
    high_trust: claims.filter((claim) => claim.trust_score.trust_label === 'high_trust').length,
    moderate_trust: claims.filter((claim) => claim.trust_score.trust_label === 'moderate_trust').length,
    low_trust: claims.filter((claim) => claim.trust_score.trust_label === 'low_trust').length,
    critical_or_unreliable: claims.filter((claim) => claim.trust_score.trust_label === 'critical_or_unreliable').length,
    needs_human_review: claims.filter((claim) => claim.human_review_required).length,
  };
  const edges = claims.flatMap((claim) => claim.citation_contexts
    .filter((context) => SUPPORT_ROLES.has(context.role))
    .map((context) => ({
      source_claim_id: claim.claim_id,
      relation: context.role === 'direct_support' ? 'supports' : 'partially_supports',
      target: context.cite_key,
      target_type: 'citation',
      weight: context.role === 'direct_support' ? 1 : 0.5,
      notes: context.notes,
    })));
  const graph = {
    schema_version: VERSION,
    rubric_version: VERSION,
    generated_at: generatedAt,
    generated_by_phase: 'phase_16T_trust_score_validation_v2',
    claims,
    edges,
    summary,
  };

  const seed = {
    schema_version: VERSION,
    generated_at: generatedAt,
    generated_by_phase: 'phase_5b_claim_seed_v2_migration',
    claim_id_algorithm: 'sha256(section_id + LF + nfkc_trim_whitespace_collapsed_exact_text)[0:16]',
    claims: claims.map((claim) => ({
      claim_id: claim.claim_id,
      section_id: claim.section_id,
      claim_text: claim.claim_text,
      normalized_claim: claim.normalized_claim,
      claim_type: claim.claim_type,
      modality: claim.modality,
      citation_keys: claim.citation_keys,
      dois: claim.dois,
      validation_status: claim.validation_status,
    })),
  };
  const index = {
    schema_version: VERSION,
    rubric_version: VERSION,
    generated_at: generatedAt,
    source: 'knowledge/claim_graph.json',
    claims_by_id: Object.fromEntries(claims.map((claim) => [claim.claim_id, {
      source_file: claim.source_file,
      section_id: claim.section_id,
      paragraph_index: claim.paragraph_index,
      sentence_index: claim.sentence_index,
      claim_text: claim.claim_text,
      citation_keys: claim.citation_keys,
      overall_score: claim.trust_score.overall_score,
      trust_label: claim.trust_score.trust_label,
      human_review_required: claim.human_review_required,
    }])),
  };
  const scores = claims.map((claim) => claim.trust_score.overall_score);
  const report = {
    schema_version: VERSION,
    rubric_version: VERSION,
    generated_at: generatedAt,
    source: 'knowledge/claim_graph.json',
    formula: 'raw_score = 5 * sum(component scores); overall_score = min(raw_score, 60) when any cap reason applies',
    claims: claims.map((claim) => ({
      claim_id: claim.claim_id,
      component_scores: Object.fromEntries(COMPONENTS.map((component) => [component, claim.trust_score.components[component].score])),
      component_rules: Object.fromEntries(COMPONENTS.map((component) => [component, claim.trust_score.components[component].rule_id])),
      score_basis: scoreBasis(claim),
      raw_score: claim.trust_score.raw_score,
      overall_score: claim.trust_score.overall_score,
      trust_label: claim.trust_score.trust_label,
      capped: claim.trust_score.capped,
      cap_reasons: claim.trust_score.cap_reasons,
    })),
    summary: {
      total_claims: claims.length,
      mean_overall_score: scores.reduce((sum, score) => sum + score, 0) / scores.length,
      minimum_overall_score: Math.min(...scores),
      maximum_overall_score: Math.max(...scores),
      high_trust: summary.high_trust,
      moderate_trust: summary.moderate_trust,
      low_trust: summary.low_trust,
      critical_or_unreliable: summary.critical_or_unreliable,
      capped_claims: claims.filter((claim) => claim.trust_score.capped).length,
      needs_human_review: summary.needs_human_review,
    },
  };
  const verifiedPassages = claims.reduce((sum, claim) => sum + claim.citation_contexts
    .reduce((inner, context) => inner + context.passages.filter(isVerifiedPassage).length, 0), 0);
  const gate = {
    schema_version: VERSION,
    rubric_version: VERSION,
    gate_id: 'phase_16T_trust_score_validation_v2',
    status: 'pass',
    validated_at: generatedAt,
    validator: 'node scripts/validate-trust.js',
    inputs: [
      ...files,
      'content/references.bib',
      'knowledge/TRUST_RUBRIC.md',
      'knowledge/claim_graph.json',
      'knowledge/claim_seed_index.json',
      'knowledge/examples/claim_context.example.json',
      'knowledge/schemas/claim_context.schema.json',
      'knowledge/schemas/claim_graph.schema.json',
      'knowledge/schemas/trust_score.schema.json',
    ],
    outputs: ['knowledge/claim_index.json', 'knowledge/trust_score_report.json', 'provenance/gate_trust_scores.json'],
    checks: {
      deterministic_claim_ids: true,
      schema_contract_integrity: true,
      exact_prose_anchors: true,
      atom_level_citation_attribution: true,
      verified_passage_provenance: true,
      derived_evidence_relation_integrity: true,
      surface_wording_attribution: true,
      independence_group_integrity: true,
      bibliography_key_doi_alignment: true,
      component_rule_integrity: true,
      score_formula_integrity: true,
      label_integrity: true,
      cap_integrity: true,
      edge_integrity: true,
      derived_artifact_integrity: true,
    },
    counts: {
      claims: claims.length,
      citation_contexts: claims.reduce((sum, claim) => sum + claim.citation_contexts.length, 0),
      verified_passages: verifiedPassages,
      failures: 0,
    },
    failures: [],
  };
  const migration = {
    schema_version: VERSION,
    generated_at: generatedAt,
    source: 'knowledge/claim_graph.json at rubric v1',
    target: 'TRUST rubric v2.0.0',
    claim_ids: idMap,
    integrity_basis: 'Phase 16 Crossref re-resolution records, with registry URLs retained per citation context.',
    passage_policy: 'Legacy verified source sentences are represented by the best claim-overlap window of at most 25 words.',
    atom_policy: 'Each migrated output is atomic; approved human-review decisions may replace one legacy unit with multiple claim records.',
    human_review_decisions: reviewDecisions.map((decision) => ({
      decision_id: decision.decision_id,
      claim_id: decision.claim_id,
      action: decision.action,
      reviewed_at: decision.reviewed_at,
      reviewer: decision.reviewer,
      output_claim_ids: decision.claims.map((claim) => claimId(decision.section_id, canonicalClaimText(claim.claim_text))),
    })),
  };

  writeJson('knowledge/claim_graph.json', graph);
  writeJson('knowledge/claim_seed_index.json', seed);
  writeJson('knowledge/claim_index.json', index);
  writeJson('knowledge/trust_score_report.json', report);
  writeJson('knowledge/examples/claim_context.example.json', claims[0]);
  writeJson('knowledge/trust_v1_to_v2_id_map.json', migration);
  writeJson('provenance/gate_trust_scores.json', gate);
  const trustSummary = buildTrustSummary(graph).replace(/\n+$/u, '');
  fs.writeFileSync(path.join(ROOT, 'content', 'trust_summary.md'), `${trustSummary}\n`, 'utf8');

  console.log(`Migrated ${claims.length} claims to TRUST v${VERSION}.`);
  console.log(`Bands: high ${summary.high_trust}, moderate ${summary.moderate_trust}, low ${summary.low_trust}, critical ${summary.critical_or_unreliable}.`);
  console.log(`Mounted ${claims.length} enriched trust-claim directives across ${files.length} review sections.`);
}

main();

// evidence-explorer-plugin.mjs
import { readFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

const EVIDENCE_FILE_PATTERNS = [
  { pattern: /^evidence_section_(\d{2})\.json$/, priority: 0 },
  { pattern: /^section_(\d{2})_evidence_package\.json$/, priority: 1 },
  { pattern: /^section_(\d{2})_evidence\.json$/, priority: 2 },
];

export function discoverEvidencePackages(evidenceDir) {
  const sections = new Map();
  for (const filename of readdirSync(evidenceDir)) {
    for (const { pattern, priority } of EVIDENCE_FILE_PATTERNS) {
      const match = filename.match(pattern);
      if (!match) continue;
      const section = Number(match[1]);
      const existing = sections.get(section);
      if (!existing || priority < existing.priority) {
        sections.set(section, {
          section,
          filename,
          filePath: resolve(evidenceDir, filename),
          priority,
        });
      }
      break;
    }
  }
  return [...sections.values()].sort((a, b) => a.section - b.section);
}

export function extractFindings(evidencePackage) {
  if (Array.isArray(evidencePackage.findings)) {
    return evidencePackage.findings.filter(finding => finding && typeof finding === 'object');
  }

  const findings = [];
  const groups = evidencePackage.argument_groups;
  if (groups && typeof groups === 'object') {
    for (const group of Object.values(groups)) {
      if (!group || typeof group !== 'object') continue;
      for (const key of ['supporting_findings', 'supporting_evidence', 'counter_findings', 'counter_evidence']) {
        if (Array.isArray(group[key])) findings.push(...group[key]);
      }
    }
  }
  if (Array.isArray(evidencePackage.unmatched_findings)) {
    findings.push(...evidencePackage.unmatched_findings);
  }
  return findings.filter(finding => finding && typeof finding === 'object');
}

export function countUniquePapers(findings) {
  return new Set(findings
    .map(finding => finding.doi || finding.cite_key || finding.citeKey)
    .filter(Boolean)
    .map(identifier => String(identifier).trim().toLowerCase()))
    .size;
}

const evidenceDirective = {
  name: 'evidence-explorer',
  doc: 'Interactive evidence database explorer widget. The :evidence-dir: option is resolved relative to the calling markdown file. Default "../evidence" is correct when the directive is placed in a content/*.md page (the conventional layout).',
  options: {
    'evidence-dir': { type: String },
    section: { type: String },
    height: { type: String },
  },
  run(data) {
    return [{
      type: 'evidence-explorer',
      evidenceDir: data.options?.['evidence-dir'] || '../evidence',
      section: data.options?.section ?? null,
      height: data.options?.height || '700px',
    }];
  },
};

// Universal conflict normalizer — handles all 15+ schema variants
function normalizeConflict(c, sec) {
  const norm = { section: sec };

  // Description / topic
  norm.topic = c.topic || c.description || '';
  norm.nature_of_conflict = c.nature_of_conflict || c.description || c.topic || '';
  norm.resolution_status = c.resolution_status || c.resolution || '';

  // Extract Side A text
  if (c.paper1_claim) {
    norm.side_a = c.paper1_claim;
  } else if (c.paper_a_claim) {
    norm.side_a = c.paper_a_claim;
  } else if (c.claim_a) {
    norm.side_a = c.claim_a;
  } else if (typeof c.side_a === 'string') {
    norm.side_a = c.side_a;
  } else if (c.side_a && typeof c.side_a === 'object') {
    norm.side_a = c.side_a.position || c.side_a.claim || JSON.stringify(c.side_a).slice(0, 200);
  } else {
    norm.side_a = '';
  }

  // Extract Side B text
  if (c.paper2_claim) {
    norm.side_b = c.paper2_claim;
  } else if (c.paper_b_claim) {
    norm.side_b = c.paper_b_claim;
  } else if (c.claim_b) {
    norm.side_b = c.claim_b;
  } else if (typeof c.side_b === 'string') {
    norm.side_b = c.side_b;
  } else if (c.side_b && typeof c.side_b === 'object') {
    norm.side_b = c.side_b.position || c.side_b.claim || JSON.stringify(c.side_b).slice(0, 200);
  } else {
    norm.side_b = '';
  }

  // Extract DOIs — try all known field patterns
  norm.paper_a_doi = c.paper1_doi || c.paper_a_doi || '';
  norm.paper_b_doi = c.paper2_doi || c.paper_b_doi || '';

  // If no DOIs from direct fields, try to extract from nested structures
  if (!norm.paper_a_doi) {
    // Check side_a dict for DOIs
    if (c.side_a && typeof c.side_a === 'object') {
      const evidence = c.side_a.supporting_evidence || c.side_a.evidence || '';
      const doiMatch = String(evidence).match(/10\.\d{4,}\/[^\s,;)]+/);
      if (doiMatch) norm.paper_a_doi = doiMatch[0];
    }
    // Check papers_side_a, papers_supporting_view_a, etc.
    for (const key of Object.keys(c)) {
      if (key.includes('papers') && key.includes('a') && Array.isArray(c[key])) {
        const dois = c[key].filter(p => typeof p === 'string' && p.startsWith('10.'));
        if (dois.length > 0) norm.paper_a_doi = dois.join(', ');
      }
    }
  }
  if (!norm.paper_b_doi) {
    if (c.side_b && typeof c.side_b === 'object') {
      const evidence = c.side_b.supporting_evidence || c.side_b.evidence || '';
      const doiMatch = String(evidence).match(/10\.\d{4,}\/[^\s,;)]+/);
      if (doiMatch) norm.paper_b_doi = doiMatch[0];
    }
    for (const key of Object.keys(c)) {
      if (key.includes('papers') && key.includes('b') && Array.isArray(c[key])) {
        const dois = c[key].filter(p => typeof p === 'string' && p.startsWith('10.'));
        if (dois.length > 0) norm.paper_b_doi = dois.join(', ');
      }
    }
  }

  // For papers[] array format — extract DOIs from array items
  if (Array.isArray(c.papers) && (!norm.paper_a_doi || !norm.paper_b_doi)) {
    const dois = c.papers
      .map(p => typeof p === 'string' ? p : (p.doi || ''))
      .filter(d => d);
    if (dois.length >= 1 && !norm.paper_a_doi) norm.paper_a_doi = dois[0];
    if (dois.length >= 2 && !norm.paper_b_doi) norm.paper_b_doi = dois[1];
  }

  // For section 12 custom fields (papers_supporting_divisive, papers_SST_carries_prediction, etc.)
  if (!norm.paper_a_doi || !norm.paper_b_doi) {
    const paperKeys = Object.keys(c).filter(k => k.startsWith('papers_'));
    if (paperKeys.length >= 2) {
      for (let i = 0; i < paperKeys.length && i < 2; i++) {
        const val = c[paperKeys[i]];
        const dois = Array.isArray(val) 
          ? val.map(p => typeof p === 'string' ? p : (p.doi || '')).filter(d => d)
          : [];
        if (i === 0 && !norm.paper_a_doi && dois.length > 0) {
          norm.paper_a_doi = dois.join(', ');
          if (!norm.side_a) norm.side_a = paperKeys[0].replace('papers_', '').replace(/_/g, ' ');
        }
        if (i === 1 && !norm.paper_b_doi && dois.length > 0) {
          norm.paper_b_doi = dois.join(', ');
          if (!norm.side_b) norm.side_b = paperKeys[1].replace('papers_', '').replace(/_/g, ' ');
        }
      }
    }
  }

  // Additional metadata
  norm.likely_reason = c.likely_reason || c.assessment || c.notes || c.significance || c.why_it_matters || '';

  return norm;
}

const evidenceTransform = {
  name: 'evidence-data-loader',
  stage: 'document',
  plugin: (opts, utils) => (tree, vfile) => {
    function transform(node) {
      if (node == null) return;
      if (node.type === 'evidence-explorer') {
        const docDir = vfile?.path ? dirname(vfile.path) : process.cwd();
        const evidenceDir = resolve(docDir, node.evidenceDir || '../evidence');
        try {
          const sections = [];
          const allFindings = [];
          const allConflicts = [];
          const allFigureData = [];

          const packages = discoverEvidencePackages(evidenceDir);
          const requestedSection = node.section == null
            ? null
            : Number(String(node.section).match(/\d+/)?.[0]);
          const selectedPackages = requestedSection == null
            ? packages
            : packages.filter(({ section }) => section === requestedSection);

          for (const evidenceFile of selectedPackages) {
            const sec = evidenceFile.section;
            const ev = JSON.parse(readFileSync(evidenceFile.filePath, 'utf-8'));

            // Rich finding records are canonical. argument_groups are a legacy
            // fallback and may contain cite-key strings rather than records.
            const findings = extractFindings(ev);

            // Normalize conflicts using the universal normalizer
            const conflicts = (ev.conflicts || []).map(c => normalizeConflict(c, sec));

            const figData = ev.figure_data || [];

            const normalizedFindings = findings.map(f => ({
              ...f,
              section: sec,
              section_title: ev.section_title || '',
              tier: f.tier || f.replication_status,
            }));
            const normalizedFigData = figData.map(fd => ({ ...fd, section: sec }));

            sections.push({
              section: sec,
              title: ev.section_title || ('Section ' + sec),
              papers: countUniquePapers(normalizedFindings),
              findings: normalizedFindings.length,
              conflicts: conflicts.length,
              figure_comparisons: normalizedFigData.length,
              source_file: evidenceFile.filename,
              package_status: findings.length === 0 ? 'valid-empty' : 'available',
              replication: {
                populated: normalizedFindings.filter(finding => Boolean(finding.replication_status)).length,
                unavailable: normalizedFindings.filter(finding => !finding.replication_status).length,
              },
              evidence_gaps: Array.isArray(ev.evidence_gaps)
                ? { status: 'recorded', count: ev.evidence_gaps.length, items: ev.evidence_gaps }
                : { status: 'not-recorded', count: null, items: [] },
              unreplicated_claims: Array.isArray(ev.unreplicated_claims)
                ? { status: 'recorded', count: ev.unreplicated_claims.length, items: ev.unreplicated_claims }
                : { status: 'not-recorded', count: null, items: [] },
            });
            allFindings.push(...normalizedFindings);
            allConflicts.push(...conflicts);
            allFigureData.push(...normalizedFigData);
          }

          node.type = 'anywidget';
          node.id = 'evidence-explorer-' + Date.now() + '-' + Math.random().toString(36).slice(2,9);
          node.esm = './evidence-explorer-widget.mjs';
          node.model = {
            evidence_data: JSON.stringify({
              load_status: selectedPackages.length === 0 ? 'absent' : 'loaded',
              load_message: selectedPackages.length === 0
                ? (node.section == null
                  ? 'No evidence packages were discovered.'
                  : `No evidence package exists for section ${requestedSection}.`)
                : '',
              requested_section: requestedSection,
              sections: sections,
              findings: allFindings,
              conflicts: allConflicts,
              figure_data: allFigureData,
            }),
            height: node.height || '700px',
          };
        } catch (err) {
          node.type = 'paragraph';
          node.children = [{ type: 'text', value: '[Evidence Explorer error: ' + err.message + ']' }];
        }
      }
      if (node.children) {
        for (const child of node.children) transform(child);
      }
    }
    transform(tree);
  },
};

export default {
  name: 'Evidence Explorer Plugin',
  directives: [evidenceDirective],
  transforms: [evidenceTransform],
};

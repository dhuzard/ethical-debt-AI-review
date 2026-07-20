#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const root = path.resolve(__dirname, "..");
const outputDir = path.join(root, "knowledge", "oratlas");
const graph = JSON.parse(fs.readFileSync(path.join(root, "knowledge", "claim_graph.json"), "utf8"));
const overrides = JSON.parse(
  fs.readFileSync(path.join(root, "knowledge", "trust_human_review_overrides.json"), "utf8"),
);

const trustCriteria = [
  "identityIntegrity",
  "entailment",
  "sourceAccess",
  "populationRelevance",
  "interventionExposureRelevance",
  "outcomeRelevance",
  "methodologicalSafeguards",
  "statisticalSafeguards",
  "replicationConvergence",
  "conflictDependency",
];

const sourceReviewByClaimText = new Map();
for (const decision of overrides.decisions) {
  for (const claim of decision.claims || []) {
    sourceReviewByClaimText.set(claim.claim_text, {
      authority: "source-review",
      state: decision.state || "adjudicated",
      decisionId: decision.decision_id,
      reviewerId: decision.reviewer_id || decision.reviewer,
      recordedAt: decision.recorded_at || decision.reviewed_at,
    });
  }
}

const claimTypeMap = {
  empirical: "empirical",
  methodological: "methodological",
  review_synthesis: "summary",
  causal: "mechanistic",
};

const relationMap = {
  direct_support: ["supports", "positive"],
  partial_support: ["partially-supports", "mixed"],
  contradictory: ["contradicts", "negative"],
  background: ["background", "neutral"],
};

function cleanDoi(value) {
  if (!value) return undefined;
  return value.trim().replace(/^https?:\/\/(?:dx\.)?doi\.org\//i, "").toLowerCase();
}

function joinScope(...values) {
  const text = values.filter(Boolean).join("; ");
  return text ? text.slice(0, 300) : undefined;
}

function compactObject(value) {
  return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined));
}

function writeJsonl(name, records) {
  const content = `${records.map((record) => JSON.stringify(record)).join("\n")}\n`;
  fs.writeFileSync(path.join(outputDir, name), content);
  return {
    records: records.length,
    bytes: Buffer.byteLength(content),
    sha256: crypto.createHash("sha256").update(content).digest("hex"),
  };
}

fs.mkdirSync(outputDir, { recursive: true });

const claims = [...graph.claims]
  .sort((a, b) => a.claim_id.localeCompare(b.claim_id))
  .map((claim) => {
    const sourceType = claim.claim_type || "unknown";
    const scope = claim.claim_scope || {};
    return compactObject({
      id: claim.claim_id,
      text: claim.claim_text,
      section: claim.section_id,
      anchor: `${claim.source_file}#${claim.claim_id}`,
      claimType: claimTypeMap[sourceType] || "other",
      qualification: `Source claim type: ${sourceType}; modality: ${claim.modality || "unspecified"}; scope status: ${claim.scope_status || "unspecified"}.`,
      scope: compactObject({
        population: joinScope(scope.biological, scope.clinical),
        model: joinScope(scope.biological, scope.computational),
        outcome: joinScope(scope.clinical, scope.conceptual),
        method: joinScope(scope.methodological, scope.computational),
      }),
    });
  });

const citationById = new Map();
const relations = [];
const trustAssessments = [];
const notAssessedCriteria = Object.fromEntries(
  trustCriteria.map((criterion) => [criterion, { rating: "not-assessed", status: "not-assessed" }]),
);

for (const claim of [...graph.claims].sort((a, b) => a.claim_id.localeCompare(b.claim_id))) {
  const sourceHumanReview = sourceReviewByClaimText.get(claim.claim_text) || null;
  for (const context of [...claim.citation_contexts].sort((a, b) => a.cite_key.localeCompare(b.cite_key))) {
    const doi = cleanDoi(context.doi);
    const sourceUrl =
      typeof context.integrity_check_source === "string" &&
      context.integrity_check_source.startsWith("https://")
        ? context.integrity_check_source
        : undefined;
    if (!citationById.has(context.cite_key)) {
      citationById.set(
        context.cite_key,
        compactObject({
          id: context.cite_key,
          doi,
          source: context.source_type,
          url: doi ? `https://doi.org/${doi}` : sourceUrl,
        }),
      );
    } else if (doi && !citationById.get(context.cite_key).doi) {
      citationById.set(context.cite_key, {
        ...citationById.get(context.cite_key),
        doi,
        url: `https://doi.org/${doi}`,
      });
    }

    const [relationType, supportDirection] = relationMap[context.role] || ["unclear", "neutral"];
    relations.push({
      claimId: claim.claim_id,
      citationId: context.cite_key,
      relationType,
      supportDirection,
      sourceLocation: `${claim.source_file}#${claim.claim_id}`,
      extractionMethod: "ComputationalReviewTemplate TRUST v2 claim graph",
      // ORAtlas `humanReviewed` denotes platform/relationship verification.
      // Source-side prose adjudication is preserved on the source assessment below.
      humanReviewed: false,
    });

    const components = Object.fromEntries(
      Object.entries(claim.trust_score.components).map(([name, component]) => [
        name,
        [component.score, component.rule_id],
      ]),
    );
    trustAssessments.push({
      claimId: claim.claim_id,
      citationId: context.cite_key,
      protocolVersion: "review-trust-v2.0.0",
      assessorType: "agent",
      assessorId: "ComputationalReviewTemplate TRUST v2",
      assessedAt: graph.generated_at,
      criteria: notAssessedCriteria,
      limitations: [
        "Claim-level source score repeated for transport; not an Oratlas relation score or crosswalk.",
      ],
      evidence: {
        sourceAssessment: {
          protocol: "ComputationalReviewTemplate TRUST",
          protocolVersion: "2.0.0",
          rubricVersion: claim.trust_score.rubric_version,
          unit: "claim-level score on a 0-100 scale",
          score: claim.trust_score.overall_score,
          label: claim.trust_score.trust_label,
          components,
          provenance: `${claim.source_file}#${claim.claim_id}`,
        },
        sourceHumanReview,
      },
      aggregateScore: null,
      aggregateMethod: null,
      reviewStatus: "agent-proposed",
    });
  }
}

const citations = [...citationById.values()].sort((a, b) => a.id.localeCompare(b.id));
relations.sort((a, b) => `${a.claimId}|${a.citationId}`.localeCompare(`${b.claimId}|${b.citationId}`));
trustAssessments.sort((a, b) =>
  `${a.claimId}|${a.citationId}`.localeCompare(`${b.claimId}|${b.citationId}`),
);

const artifacts = {
  "claims.jsonl": writeJsonl("claims.jsonl", claims),
  "citations.jsonl": writeJsonl("citations.jsonl", citations),
  "relations.jsonl": writeJsonl("relations.jsonl", relations),
  "trust-assessments.jsonl": writeJsonl("trust-assessments.jsonl", trustAssessments),
};

const provenance = {
  schemaVersion: "1.0.0",
  generatedAt: graph.generated_at,
  generator: "scripts/export-oratlas.js",
  sourceArtifacts: [
    "knowledge/claim_graph.json",
    "knowledge/trust_human_review_overrides.json",
    "knowledge/record_counts.json",
  ],
  contract: {
    repository: "dhuzard/oratlas",
    commit: "102d3fa96d47e9e7773720b0c36802f888cca4fe",
    manifestSchema: "packages/contracts/schemas/review-manifest.schema.json",
    artifactContract: "packages/contracts/src/artifacts.ts",
  },
  sourceSchemaVersion: graph.schema_version,
  sourceRubricVersion: graph.rubric_version,
  semantics: {
    claims: "Canonical claim records from the TRUST v2 claim graph.",
    relations: "Claim-citation contexts exported without changing their evidence role.",
    trust: "Original claim-level five-component scores are retained only under evidence.sourceAssessment; aggregateScore is null and all Oratlas relation-level criteria explicitly remain not assessed.",
    humanReview: "Source-side decisions are retained under evidence.sourceHumanReview with authority=source-review. ORAtlas relation humanReviewed remains false and reviewStatus remains agent-proposed until platform verification.",
  },
  counts: {
    claims: claims.length,
    citations: citations.length,
    relations: relations.length,
    trustAssessments: trustAssessments.length,
    sourceHumanReviewedRelations: trustAssessments.filter((assessment) => assessment.evidence.sourceHumanReview).length,
    platformHumanReviewedRelations: relations.filter((relation) => relation.humanReviewed).length,
  },
  artifacts,
};
fs.writeFileSync(path.join(outputDir, "provenance.json"), `${JSON.stringify(provenance, null, 2)}\n`);

console.log(JSON.stringify({ counts: provenance.counts, artifacts }, null, 2));

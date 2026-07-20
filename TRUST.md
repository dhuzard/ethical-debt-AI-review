# TRUST evidence profile

This repository uses the **experimental** ComputationalReviewTemplate TRUST v2 rubric to score claims on five review-local dimensions: traceability, robustness, uncertainty calibration, source integrity, and transferability/scope control. These scores are structured audit signals for this review, not probabilities that a claim is true, not universal quality ratings, and not substitutes for scientific judgment. They are exported to Oratlas as clearly labeled source assertions and are not remapped into Oratlas's ten relation-level criteria.

## Identity integrity

The source review checks citation identifiers and records bibliography and integrity status in its canonical claim graph. The Oratlas relation-level identity-integrity criterion remains explicitly `not-assessed` until it is evaluated under the Oratlas protocol.

## Entailment

The review preserves verified passages and claim-atom coverage as traceability evidence. The export does not equate that local evidence with an Oratlas entailment rating, so this criterion remains explicitly `not-assessed`.

## Source access

DOIs and verification locations are retained where available. Access conditions have not been normalized under the Oratlas source-access protocol, and the relation-level criterion therefore remains `not-assessed`.

## Population relevance

Biological and clinical scope descriptions are exported with each claim. No Oratlas relation-specific population-relevance judgment has been made, so the criterion remains `not-assessed`.

## Intervention exposure relevance

The source review records methodological and conceptual scope but does not apply Oratlas's intervention/exposure relevance criterion. The export marks this criterion `not-assessed` rather than inferring a rating.

## Outcome relevance

Clinical and conceptual outcome scope is retained when present. It has not been adjudicated under Oratlas's relation-level outcome criterion and remains `not-assessed`.

## Methodological safeguards

The local robustness component captures independence and evidence-coverage rules, not the complete Oratlas methodological-safeguards construct. No crosswalk is asserted, and this criterion remains `not-assessed`.

## Statistical safeguards

Statistical safeguards were not scored as a separate relation-level dimension in the source rubric. This criterion remains explicitly `not-assessed`.

## Replication convergence

The review's robustness evidence may record independence groups and replication notes, but it is not converted into an Oratlas replication/convergence rating. This criterion remains `not-assessed`.

## Conflict dependency

The source graph records known integrity and conflict information where available. It does not constitute a complete Oratlas conflict/dependency assessment, so this criterion remains `not-assessed`.

The canonical enriched scores and rationales remain in `knowledge/claim_graph.json`; `knowledge/oratlas/trust-assessments.jsonl` is the bounded interoperability view.

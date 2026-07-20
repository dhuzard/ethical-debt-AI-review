(sec-provenance)=
# Pipeline Provenance

This review was produced by a staged, gated computational protocol under human direction. Each stage was carried out by a specialist component — some performing scientific judgement (evaluating literature, drafting prose, auditing figures and citations), others performing mechanical work (building the citation index, the bibliography, and the assembled document). A coordinator routed work between stages and verified a named set of pass/fail checks at each transition before advancing. Independent assessment stages were kept separate from the stages whose output they judged, so that figure audits, prose critiques, and citation checks were carried out by components that had not produced the material under review.

## Pipeline Summary

- **Discovery databases:** PubMed, Europe PMC, and OpenAlex, with CrossRef used for bibliographic metadata and digital-object-identifier verification.
- **Canonical curated corpus:** 1,438 finding records representing 1,336 unique
  DOI/citation identifiers across the nine section packages, with 125 packaged
  conflict records and 60 cross-study figure comparisons. These values are
  computed in `evidence/EVIDENCE_MIGRATION_REPORT.json`.
- **Historical pipeline counts:** the Phase 2 gate recorded 1,451 raw findings and
  1,339 distinct DOI strings; the bibliography gate recorded 1,337 entries. Those
  immutable gate records describe earlier processing stages, not the current
  curated package cardinality.
- **Figures:** 21 section figures plus one schematic, each paired with a self-contained, re-executable notebook and rendered from the recorded evidence.
- **Text:** seven body sections, an Introduction and Conclusion, and an Abstract, each citing only papers held in the verified bibliography.
- **Assessment:** blinded figure-comparability review, blinded per-section prose critiques, blinded review of the Introduction and Conclusion, and full citation verification against source metadata and, where retrievable, full text.

## Phase Execution

The protocol runs as a fixed sequence of numbered stages, from scope definition and evidence gathering, through citation infrastructure, section outlining, evidence curation, figure review, drafting, critique, bibliography assembly, cross-section integration, the Introduction and Conclusion, the Methods record, and document assembly, to citation verification, repository publication, and a final deployment check. The per-stage status and the identifier of the check that closed each stage are recorded in the machine-readable phase ledger committed alongside this document.

For the full protocol, the per-stage specifications, and the complete list of pass/fail checks, see the {ref}`sec-methods` section and the version-controlled stage specifications in the repository.

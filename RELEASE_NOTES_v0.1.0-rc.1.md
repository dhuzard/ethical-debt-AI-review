# v0.1.0-rc.1 — frozen reference-release candidate

This prerelease is the first immutable candidate of the Ethical Debt computational
review reference implementation and test corpus. It is not a peer-reviewed
scientific release and is not the canonical home of the TRUST rubric, ORAtlas, or
the inherited publication pipeline.

## Included

- reconciled curated corpus: 1,438 findings and 1,336 unique DOI/citation identifiers;
- separate literature-evidence and claim/TRUST interfaces;
- validated TRUST v2 knowledge artifacts and deterministic human-review merge;
- pinned ORAtlas export contract, hashes, fixtures, and source-review semantics;
- deterministic figures and full MyST build with three-browser regression tests;
- explicit resolution record for all 18 deferred Phase 10 caveats; and
- a read-only living-literature candidate monitor.

## Known limitations

- 29 original low-trust/capped claims and two source-verification escalations await qualified human adjudication;
- domain calibration, ontology mapping, cross-review comparison, and public ORAtlas review require human or upstream coordination;
- monitoring results are unverified candidates and never update review evidence automatically; and
- Zenodo metadata is prepared, but no DOI is minted by this prerelease.

See `RELEASE_CONTRACT.md`, `FORWARD_WORK_PROTOCOLS.md`, and
`SCIENTIFIC_REVIEW_QUEUE.md` for the complete release and review boundaries.

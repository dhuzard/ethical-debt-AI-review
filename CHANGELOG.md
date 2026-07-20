# Changelog

This file records review and reference-implementation releases. The historical
pipeline-skill catalogue changelog is preserved at `skills/CHANGELOG.md`.

The project uses semantic versioning for published artifacts:

- `0.x` release candidates may change schemas and scientific wording;
- `1.0.0` requires completion of the human scientific-review queue;
- patch releases do not change scientific meaning or artifact schemas;
- every tag is immutable; corrections are published as a new version.

## [0.1.0-rc.1] - 2026-07-20

### Added

- recovered and validated Literature Evidence Explorer with 1,438 findings;
- canonical knowledge-layer counts and append-only human-review decisions;
- deterministic review-priority and claim-quality audit artifacts;
- pinned, contract-validated ORAtlas export and immutable fixtures;
- explicit evidence empty/error/gap states and accessible TRUST panel behavior;
- Chromium, Firefox, and WebKit regression suite;
- frozen release-artifact hashes and deterministic figure/site build gates;
- release contract, reproducibility guide, disclosures, and Zenodo-ready metadata.

### Known limitations

- 29 claims remain queued for human scientific review;
- the review is not peer reviewed or fully human-adjudicated;
- TRUST v2 is experimental and review-local;
- evidence-gap fields are not recorded in the current section packages;
- no review-specific DOI has yet been minted.

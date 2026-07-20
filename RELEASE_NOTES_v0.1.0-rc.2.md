# v0.1.0-rc.2 — complete ORAtlas integration fixture

This prerelease is the first complete immutable ORAtlas integration fixture for
The Ethical Debt computational review. It preserves the final merged engineering
state after the evidence, knowledge, provenance, reader-interface, release, and
scientific forward-work changes. It is not a peer-reviewed scientific release and
does not validate the experimental TRUST methodology.

`v0.1.0-rc.1` remains unchanged as historical provenance. ORAtlas integrations
should pin this `rc.2` tag, its exact commit and tree, and the committed artifact
hashes rather than reading a moving branch.

## Frozen integration contract

- 529 canonical claims;
- 994 exported citations;
- 1,392 claim–citation relations;
- 1,392 source-native TRUST assessment records;
- 1,438 literature evidence findings;
- 1,336 unique DOI/citation identifiers; and
- all ten ORAtlas-native criteria explicitly `not-assessed`.

Computational Review TRUST v2 remains a source-native claim-level audit. Its
five components and experimental aggregate are not translated into ORAtlas
relation criteria, and source-side human review does not become ORAtlas platform
verification.

## Engineering included since rc.1

- the complete final merged stack on `main`;
- canonical evidence and record-count contracts;
- append-only human-decision provenance;
- pinned ORAtlas export semantics, hashes, and fixtures;
- hardened evidence and TRUST reader interfaces;
- deterministic figures, three-browser tests, and deterministic MyST builds; and
- scientific forward-work protocols and read-only literature monitoring.

## Known scientific limitations

- 29 current claims remain flagged for qualified human review;
- SR-30 and SR-31 remain full-text scientific-review tasks;
- the 12-claim calibration subset has not established methodological calibration;
- cross-review comparison awaits suitable independent material; and
- no review-specific DOI is minted by this prerelease.

These limitations do not block an explicitly experimental infrastructure fixture.
See `RELEASE_CONTRACT.md`, `FORWARD_WORK_PROTOCOLS.md`, and
`SCIENTIFIC_REVIEW_QUEUE.md` for the binding boundaries.

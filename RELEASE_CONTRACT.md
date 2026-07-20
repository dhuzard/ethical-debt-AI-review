# Reference prerelease contract

The `v0.1.0-rc.N` series is the first immutable integration reference for this
review, its experimental TRUST layer, and the ORAtlas export. A release candidate
may be tagged only when every automated gate below passes at the exact tag commit.

## Automated gates

- Canonical record counts match `knowledge/record_counts.json`.
- Every release artifact and figure matches the SHA-256 digest in
  `provenance/release_artifact_manifest.json`.
- All nine evidence packages load, contain at least 1,000 findings in aggregate,
  and distinguish absent from valid-empty packages.
- TRUST, human-review hash-chain, claim-quality, and pinned ORAtlas contract
  validators pass.
- All Node tests and Chromium, Firefox, and WebKit regressions pass.
- Every figure notebook executes twice to byte-identical PNG output and matches
  the frozen figure hashes.
- Two consecutive MyST builds produce byte-identical output trees after removing
  MyST's presentation-only random AST keys and derived image DOM IDs.
- Node, Python, MyST, Playwright, and scientific Python dependencies are pinned.
- The release tag resolves to the validated commit; ORAtlas ingestion uses that
  tag or commit, never a moving branch.

Run `npm run release:check`. Immediately before publishing, run
`node scripts/validate-release.js --tag v0.1.0-rc.N`.

## Required disclosures and limitations

- This is a substantially AI-assisted computational review.
- It is not peer reviewed and not fully human-adjudicated.
- TRUST v2 is an experimental review-local audit signal, not a probability of
  truth or a universal quality score.
- Twenty-nine current claims still require human scientific review; 28 are
  capped. Historical completed decisions are counted separately.
- The section evidence packages contain 1,438 finding records and 1,336 unique
  DOI/citation identifiers. Dedicated evidence-gap and unreplicated-claim fields
  are not recorded in the current packages; absence is not interpreted as zero.
- ORAtlas's ten native criteria remain `not-assessed`; source TRUST is preserved
  in the evidence envelope and is not reinterpreted as platform verification.
- No review-specific DOI exists until Zenodo archives a stable release.

## Release procedure

1. Merge or otherwise freeze the complete stacked implementation at one commit.
2. Run every command in `DEPLOY.md`, including the manual disclosure review.
3. Tag the validated commit with an annotated `v0.1.0-rc.N` tag.
4. Publish a GitHub prerelease containing the limitations above and the artifact
   manifest; do not describe it as stable or peer reviewed.
5. Record the exact tag and commit in the ORAtlas ingestion configuration.
6. Mint a Zenodo DOI only for a stable release after completing the human gates.

## Human gates for a stable release

A release candidate can exercise infrastructure while the scientific queue is
open. A stable `v1.0.0` cannot be cut until all human-only items in
`SCIENTIFIC_REVIEW_QUEUE.md` have decisions, the manuscript changes are approved,
and the live-site manual checklist has been completed.

# FAIR profile

## Findable

The review has a public GitHub repository, immutable release-candidate tags, a machine-readable review manifest, persistent claim IDs, citation keys, and DOI identifiers where available. MyST provides a browsable public rendering of the review and its claim-level TRUST displays. Zenodo metadata is prepared in `.zenodo.json`; a review DOI will be added only after a stable archival deposit.

## Accessible

Review text, code, provenance, and knowledge artifacts are publicly readable under the repository license. Citation records retain DOI URLs when available; access to third-party publications remains governed by their publishers and repositories.

## Interoperable

The canonical TRUST v2 graph is supplemented by manifest-declared JSONL files for claims, citations, claim-citation relations, and TRUST assertions. The export preserves source semantics and marks unmapped Oratlas criteria as `not-assessed` instead of manufacturing a crosswalk.

## Reusable

The repository includes an MIT license, CRediT roles, exact dependency pins,
deterministic export/figure/site checks, frozen SHA-256 artifact manifests,
provenance metadata, validation scripts, and a versioned public preview. Reusers
can regenerate the interoperability artifacts from the canonical claim graph and
human-review decisions by following `DEPLOY.md`.

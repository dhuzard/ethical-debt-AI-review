# Forward-work protocols

These protocols define how work that cannot be completed by an autonomous agent
may proceed without manufacturing scientific decisions. They are part of the
reference implementation, not evidence that the described reviews or experiments
have occurred.

## Human scientific adjudication (ED-A01, ED-A03, ED-C07, ED-E04)

The 29 original flagged claims and the two source-verification escalations remain
pending in `SCIENTIFIC_REVIEW_QUEUE.md`. Completion requires, at minimum:

1. two independent reviewers with relevant subject-matter expertise;
2. disclosure of conflicts and a blind first-pass decision using
   `knowledge/REVIEWER_INSTRUCTIONS.md`;
3. an evidence-linked rationale for retain, revise, split, or reject;
4. adjudication of disagreements by a third reviewer; and
5. deterministic merge through the existing review store, preserving the original.

Scope decisions must state the source population, target population, transfer
assumptions, and permitted wording. Compound claims may be split only during such
substantive review; child records must retain lineage to the immutable original.
Additional rounds (ED-E04) should use a frozen, risk-stratified sample and report
inter-reviewer agreement. Until qualified people supply decisions, these items are
**blocked on human review**, not silently treated as complete.

## TRUST calibration experiment (ED-C11)

This is an upstream experiment for the TRUST fork; it must not create local scoring
overrides. Preregister a stratified sample across review sections, claim types,
score bands, and cap reasons. At least two blinded domain reviewers independently
rate the same claims under the pinned rubric. Report agreement, calibration curves,
threshold sensitivity, and subgroup uncertainty before proposing any threshold.
Publish de-identified ratings, exclusions, and analysis code. A threshold change
requires TRUST-maintainer review and a new rubric version; this repository then
migrates rather than mutates historical scores. **Blocked on reviewers and upstream
TRUST coordination.**

## Ontology alignment (ED-C12)

Select the target ontology through human and ORAtlas-owner review before mapping.
Create an additive crosswalk containing local term, external identifier, match type
(exact, broader, narrower, related), confidence, mapper, and rationale. Never replace
source wording or silently coerce unmatched concepts. Double-map a sample and report
agreement and coverage. Version the ontology and crosswalk independently.
**Blocked on target-ontology selection and cross-repository agreement.**

## Cross-review comparison (ED-E05)

Run only after a second compatible review and this repository's frozen release
exist. Preregister the matching unit and distinguish exact citation overlap,
semantic claim similarity, conflicting conclusions, and missing coverage. Keep
automated matches as candidates until human validation; report precision on a
blinded sample and never transfer TRUST scores between reviews. **Blocked because
no second review has been designated.**

## Public ORAtlas review workflow (ED-F06)

External contributions should target a frozen tag and immutable claim ID. A
challenge record should include contributor identity or stable pseudonym,
conflict disclosure, target release and claim, proposed disposition, rationale,
source locators, timestamp, and signature/hash. ORAtlas platform verification must
remain distinct from this repository's `sourceHumanReviewed` state. Contributions
are append-only; accepted changes create a new review version and lineage rather
than modifying the frozen release. Rate limiting, moderation, appeals, withdrawal,
and privacy policy belong upstream. **Blocked on ORAtlas product and governance
approval; this document is the proposed contract.**

## Living-literature monitoring (ED-G05)

The monitor in `scripts/literature-monitor.mjs` queries Crossref from the frozen
release date using the transparent topics in `monitoring/queries.json`. It only
produces unverified candidate metadata as a CI artifact. It does not alter claims,
evidence, scores, review decisions, or the repository. A human must deduplicate,
screen, retrieve full text where necessary, and record inclusion decisions before
new literature enters a later release.

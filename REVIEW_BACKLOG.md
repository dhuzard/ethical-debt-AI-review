# Review backlog — The Ethical Debt

This is the single canonical backlog for this repository. It replaces ad-hoc
planning: the older `HANDOFF.md` and `phase_ledger.json` describe the *production*
pipeline that built the review (all 21 phases complete) and are retained as
historical provenance, not as forward work. New work is tracked here.

**What this repository is.** This is the first real-world reference implementation
and test corpus for three upstream projects:

- `AllenNeuralDynamics/ComputationalReviewTemplate` — the generic computational-review template;
- `Neuronautix/ComputationalReviewTemplate_trust-knowledge` — the experimental TRUST extension;
- `dhuzard/oratlas` — the open-review platform that ingests this review.

It owns *this review's* content, evidence, claim graph, TRUST assessments, human
review, MyST rendering, ORAtlas export, and tagged releases. It does **not** own
the generic template, the canonical TRUST methodology, the ORAtlas platform, or a
universal trust score. Reusable defects are recorded here but fixed upstream (see
`UPSTREAM_SYNC.md`).

Statuses: `backlog` · `ready` · `in-progress` · `blocked` · `review` · `done` · `superseded`.
Priorities: `P0` integrity/misleading-presentation/data-loss/broken-publication ·
`P1` needed for a reliable public reference release · `P2` valuable after core is
stable · `P3` exploratory.

Companion files:

- `SCIENTIFIC_REVIEW_QUEUE.md` — items needing human scientific judgment (do not do these as engineering).
- `UPSTREAM_SYNC.md` — reusable code inherited from the template and TRUST fork.

---

## Recommended first implementation tranche

No more than five items, in this order. Each earlier item de-risks the next.

1. **ED-B01 + ED-B02 — Audit and recover the Literature Evidence Database.**
   The Evidence Explorer is *silently empty*: the plugin scans for
   `section_NN_evidence_package.json` / `section_NN_evidence.json`, but the real
   files are `evidence_section_NN.json`, so zero sections load while the build
   still succeeds. This is the most visible correctness defect and everything
   downstream (counts, release freeze, ORAtlas trust in the corpus) assumes the
   evidence layer is real. Recover it first.
2. **ED-C03 — Reconcile claim / TRUST / human-review record counts.** Multiple
   documents quote different numbers (a merged PR says 510 claims and 424/49/34/3
   bands; the current graph has 529 and 444/56/29/0; human review is variously
   "9 decisions", "28 claims", "29 flagged", "34 relations", "38 flagged
   decisions"). Until one source of truth is fixed, no release or export can be
   trusted, and it blocks ED-F04 and ED-H01.
3. **ED-F02 — Correct and lock ORAtlas export semantics.** The export must keep
   native TRUST claim-level (not a relation-level aggregate), keep the ten ORAtlas
   criteria `not-assessed`, and preserve the source assessment. Today the code
   largely does this but has **no tests**, so the contract can regress invisibly.
   Lock it before ORAtlas ingests the next tag.
4. **ED-D02 — Synchronize the single-active-panel TRUST viewer from the TRUST
   fork.** A corrected single-active-panel behaviour exists upstream; syncing it
   fixes overlapping TRUST panels in the published interface, which is a
   presentation-integrity issue readers hit immediately.
5. **ED-H01 — Define and validate the frozen reference-release contract.** Once
   evidence, counts, and export are correct, freeze record counts and artifact
   hashes, validate build/figures/browsers, and cut a tagged prerelease so
   ORAtlas ingests an immutable commit, not the moving branch.

Rationale for the ordering: fix the broken data layer (1), make the numbers mean
one thing (2), stop the export from lying about semantics (3), fix the most
visible UI defect (4), then freeze the whole thing into an ingestable release (5).

---

## Rules for autonomous agents

1. Work on one backlog item per branch and PR unless two items are inseparable.
2. Read the backlog item, its dependencies, and the relevant provenance before editing.
3. Do not modify scientific claims merely to make validation pass.
4. Do not invent evidence, passages, effect sizes, citations, DOIs, or replication states.
5. Do not invent human review or adjudication decisions.
6. Preserve original records before any migration (copy, don't overwrite).
7. Every generated or migrated field must carry traceable provenance.
8. Do not redesign the TRUST methodology in this repository.
9. Generic TRUST changes belong in the TRUST fork (`ComputationalReviewTemplate_trust-knowledge`).
10. Generic Evidence Explorer and pipeline changes belong in the upstream template.
11. ORAtlas platform behaviours belong in `dhuzard/oratlas`.
12. Any temporary local fix must be documented and linked to an upstream backlog item in `UPSTREAM_SYNC.md`.
13. Do not silently change the meaning of an existing schema.
14. Add tests for every contract, migration, or interface change.
15. Run the relevant validation, tests, MyST build, and export checks before opening a PR.
16. Update the backlog item status and add the PR reference when you open it.
17. Stop and mark the item `blocked` when scientific judgment is required, and add the claim to `SCIENTIFIC_REVIEW_QUEUE.md`.
18. Prefer small, reviewable PRs.
19. Do not regenerate all TRUST artifacts unless the item explicitly requires it.
20. Never ingest or test ORAtlas against a moving branch when an exact release or commit is available.

---

## Project non-goals and prohibited shortcuts

This repository must **not**:

- Become the canonical generic review template.
- Become the canonical TRUST methodology repository.
- Become the ORAtlas application.
- Fabricate missing evidence.
- Fill evidence packages from unsupported inference.
- Treat citation count as evidence quality.
- Treat journal, laboratory, institution, or author prestige as TRUST evidence.
- Treat p-values as direct trust scores.
- Treat agent agreement as scientific validation.
- Present native TRUST as a probability that a claim is true.
- Present a claim-level score as a relation-level score.
- Hide missing information behind an average.
- Overwrite historical assessments.
- Change scientific prose only to obtain a better score.
- Claim human adjudication that has not occurred.
- Silently update frozen review releases.
- Add complex infrastructure before the existing artifacts are internally consistent.
- Duplicate a reusable fix already assigned to another repository.

---

## Workstream A — Review content and scientific claims

### ED-A01 — Adjudicate the 29 flagged low-trust / capped claims
- **Status:** backlog · **Priority:** P1 · **Size:** L · **Agent:** no · **Upstream:** local
- **Goal:** Human decision on each of the 29 claims currently flagged
  `human_review_required` (all are `low_trust`; 25 capped `contradicted_without_caveat`, 3 `overextended_scope`, 1 uncapped).
- **Why it matters:** These are the claims whose current presentation is most
  likely to mislead (contradictory evidence not caveated, scope overextended).
- **Scope:** Route every flagged claim to `SCIENTIFIC_REVIEW_QUEUE.md`; record a
  decision and rationale; apply agreed wording/caveat changes only after decision.
- **Non-goals:** Rewriting prose to lift the score; inventing caveats not supported by evidence.
- **Dependencies:** ED-C03 (counts), ED-E02 (decision store).
- **Acceptance:** Each of the 29 claim IDs has a recorded human decision + rationale; no claim edited before its decision.
- **Files:** `knowledge/claim_graph.json`, `content/*.md`, `SCIENTIFIC_REVIEW_QUEUE.md`, `knowledge/trust_human_review_overrides.json`

### ED-A02 — Apply the 18 deferred SHOULD_CAVEAT amendments
- **Status:** backlog · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** Resolve the 18 caveats deferred from Phase 8 to Phase 10 in `provenance/phase10_caveats.json`.
- **Why it matters:** Several are metric-conflation issues (e.g. a 26% feasibility
  rate juxtaposed with 25%/11% replication rates) that overstate or blur findings.
- **Scope:** For each item, apply the `suggested_fix` wording if it needs no new
  data; otherwise escalate to the scientific review queue.
- **Non-goals:** Adding new evidence; changing the underlying claim.
- **Dependencies:** none.
- **Acceptance:** Each of the 18 items is either applied (with diff) or escalated with reason; caveat file annotated with resolution.
- **Files:** `provenance/phase10_caveats.json`, `content/02_*`–`content/08_*`

### ED-A03 — Scope-control audit of "generalises across …" claims
- **Status:** backlog · **Priority:** P2 · **Size:** M · **Agent:** no · **Upstream:** local
- **Goal:** Review claims capped `overextended_scope` (e.g. the Ecuador
  national-systems generalisation, the ~2% availability anchor) for transferability.
- **Why it matters:** Overextended scope is a subtle integrity risk distinct from citation error.
- **Scope:** Human judgment on whether scope is defensible or must be narrowed.
- **Non-goals:** Mechanical rescoring.
- **Dependencies:** ED-A01.
- **Acceptance:** Each capped-scope claim has a scope decision recorded.
- **Files:** `knowledge/claim_graph.json`, `content/*.md`

### ED-A04 — Reconcile corpus-size statements
- **Status:** backlog · **Priority:** P2 · **Size:** S · **Agent:** conditional · **Upstream:** local
- **Goal:** One consistent corpus number across README, `content/provenance.md`, `HANDOFF.md`, and gates.
- **Why it matters:** README/provenance say 1,337 unique papers; provenance also
  says 1,451 findings; `HANDOFF.md` says "closed at 1,339 unique". A public
  reference must not quote three numbers.
- **Scope:** Determine the canonical count from the evidence artifacts and align all prose.
- **Non-goals:** Re-running evidence gathering.
- **Dependencies:** ED-B01.
- **Acceptance:** All documents quote one reconciled corpus figure traceable to a source artifact.
- **Files:** `README.md`, `content/provenance.md`, `HANDOFF.md`, `provenance/gate_*`

---

## Workstream B — Literature evidence database

### ED-B01 — Audit `evidence/` and produce a machine-readable migration report
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** local (loader fix may be upstream template)
- **Goal:** Inventory every file in `evidence/`, determine why the Evidence
  Explorer renders empty, identify which expected section packages exist, and
  produce a traceable evidence migration report.
- **Why it matters:** The evidence layer is one of the three reasons this repo
  exists; right now it is invisible in the published site despite a green build.
- **Scope:** Audit the 9 `evidence_section_NN.json` packages (present for
  sections 01–09), the 8 raw `cluster_NN_evidence.json`, and the supporting
  `citemap/authortable/scaffold` files; map each expected section package to its
  source data; confirm whether equivalent evidence already exists in another
  artifact before any reconstruction; write `evidence/EVIDENCE_MIGRATION_REPORT.md`
  (or `.json`) recording per-section presence, finding counts, and provenance.
- **Non-goals:** Reconstructing packages from inference; changing findings content.
- **Dependencies:** none.
- **Acceptance:** A committed report lists, per section, package presence, finding
  count, conflict count, and source artifact; no invented data.
- **Files:** `evidence/*.json`, `evidence/README.md`, new `evidence/EVIDENCE_MIGRATION_REPORT.md`

### ED-B02 — Fix the Evidence Explorer so packages actually load
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** upstream template (loader is generic)
- **Goal:** Make the Evidence Explorer read the real files and display the rich findings.
- **Why it matters:** Two defects make it silently empty/wrong: (1) filename
  mismatch — plugin scans `section_NN_evidence_package.json`/`section_NN_evidence.json`
  but files are `evidence_section_NN.json`; (2) even when a file loads, the
  extractor prefers `argument_groups` (which hold ~9 cite-key *strings*) and only
  falls back to the rich `findings[]` object array when the first is empty, so it
  would show cite keys instead of the 180+ finding objects. `unique_papers` /
  `total_findings` are also absent from the files.
- **Scope:** Align the loader's expected filenames and finding-extraction order
  with the actual schema; compute paper/finding counts from real fields. Because
  the loader is generic template code, fix it in the upstream template and sync
  here (see `UPSTREAM_SYNC.md`); a documented temporary local patch is allowed.
- **Non-goals:** Editing evidence content; changing the directive API.
- **Dependencies:** ED-B01.
- **Acceptance:** Local build renders non-empty Evidence Explorer with correct
  per-section finding/conflict/paper counts matching the source packages; a test asserts it.
- **Files:** `plugins/evidence-explorer-plugin.mjs`, `content/evidence-explorer-widget.mjs`, `content/evidence_database.md`

### ED-B03 — Prevent a green build from shipping a silently empty Evidence Explorer
- **Status:** review · **Priority:** P0 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Implementation:** PR #7
- **Goal:** CI fails when the evidence layer is empty or under-populated.
- **Why it matters:** The current build succeeds with zero evidence displayed.
- **Scope:** Add a validation step (and CI wiring) that loads the evidence
  packages the way the site does and asserts expected section count and non-zero
  findings; wire into `.github/workflows/deploy.yml`.
- **Non-goals:** Asserting exact numbers that will legitimately change (use bounds/expected-set).
- **Dependencies:** ED-B02.
- **Acceptance:** A deliberately broken/renamed package fails CI; the healthy repo passes.
- **Files:** `.github/workflows/deploy.yml`, new `scripts/validate-evidence.js`, `tests/`

### ED-B04 — Distinguish an absent package from a valid zero-finding package
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** upstream template
- **Implementation:** PR #7
- **Goal:** The explorer and validator must treat "no package" and "package with zero findings" differently.
- **Why it matters:** Conflating them hides missing evidence behind a legitimate-looking empty state.
- **Scope:** Explicit empty-vs-missing states in widget and validator.
- **Non-goals:** Fabricating findings to avoid an empty state.
- **Dependencies:** ED-B02, ED-B03.
- **Acceptance:** Widget shows distinct "no package for this section" vs "0 findings"; validator reports them separately.
- **Files:** `content/evidence-explorer-widget.mjs`, `scripts/validate-evidence.js`

### ED-B05 — Reconcile `evidence/README.md` with the actual schema
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** upstream template
- **Implementation:** PR #7
- **Goal:** Documentation matches real filenames (`evidence_section_NN.json`) and fields.
- **Why it matters:** README currently documents `section_NN_evidence_package.json`, contradicting the files and the v29 CHANGELOG rename.
- **Scope:** Update README schema/format section; note the `findings[]`-vs-`argument_groups` convention.
- **Non-goals:** Changing file layout.
- **Dependencies:** ED-B01, ED-B02.
- **Acceptance:** README describes the loaded format exactly; no contradictory names remain.
- **Files:** `evidence/README.md`

### ED-B06 — Complete replication / conflict / evidence-gap provenance in packages
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Implementation:** PR #7
- **Goal:** Ensure each finding's replication status, conflicts, and evidence gaps are populated where source data supports it.
- **Why it matters:** These fields drive contradiction and gap views; empty fields understate uncertainty.
- **Scope:** Backfill only from traceable source data; flag gaps rather than guessing.
- **Non-goals:** Inferring replication states.
- **Dependencies:** ED-B01.
- **Acceptance:** Coverage report of populated vs unavailable fields; no invented statuses.
- **Files:** `evidence/evidence_section_*.json`

---

## Workstream C — Claim and TRUST knowledge layer

### ED-C01 — Validate directive → canonical record resolution and exact prose anchors
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** local (validator generic → TRUST fork)
- **Goal:** Every public `trust-claim` directive resolves to exactly one
  `claim_graph.json` record, and its `text_quote_selector` anchors to exact prose.
- **Why it matters:** A directive that resolves to nothing (or to the wrong claim)
  shows a misleading card; a broken anchor highlights the wrong text.
- **Scope:** Extend `scripts/validate-trust.js` to assert 1:1 directive↔record and
  unique, resolvable anchors across all `content/*.md`; fail on ambiguity.
- **Non-goals:** Changing claim text.
- **Dependencies:** none.
- **Acceptance:** Validator reports 0 unresolved/ambiguous directives; CI enforces it.
- **Files:** `scripts/validate-trust.js`, `plugins/trust-claim-plugin.mjs`, `content/*.md`

### ED-C02 — Validate claim atoms, citation-to-atom attribution, and passages
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** TRUST fork (rubric-level)
- **Goal:** Every `claim_atom` is an exact substring of `claim_text`; every
  citation context's atom list equals the union of its verified passages' atoms;
  every supporting passage has a locator and verification record.
- **Why it matters:** These are the rubric's required inputs; if they drift the
  mechanical score is unsound. Note all 529 claims currently carry exactly one
  atom (migration default) — compound splitting is deferred to human review (ED-C07), not this item.
- **Scope:** Add atom/passage/attribution assertions to the validator.
- **Non-goals:** Splitting compound claims; re-verifying passages against sources.
- **Dependencies:** ED-C01.
- **Acceptance:** Validator asserts atom substring, atom-union equality, and passage-locator presence for all claims; CI enforces.
- **Files:** `scripts/validate-trust.js`, `knowledge/claim_graph.json`, `knowledge/schemas/`

### ED-C03 — Reconcile claim / citation / relation / assessment / human-review counts
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Goal:** One source of truth for every headline number, reflected everywhere.
- **Why it matters:** Numbers currently conflict across artifacts: graph/export
  = **529 claims, 994 citations, 1,392 relations, 1,392 assessments**, bands
  **444/56/29/0**, **29** human-review flags, **28** caps; a merged PR quotes
  **510** claims and **424/49/34/3**; human review is variously stated as 9
  decisions, 28 claims-in-decisions, 29 flagged, 34 human-reviewed relations, and
  "38 flagged decisions". README, `trust_summary.md`, releases, and the UI must agree.
- **Scope:** Compute canonical counts from `claim_graph.json` +
  `trust_human_review_overrides.json`; define each term precisely (claim vs
  relation vs decision vs flag); update README, `content/trust_summary.md`,
  manifest, and release wording; add a count-manifest artifact + CI check.
- **Non-goals:** Changing the underlying data to hit a target number.
- **Dependencies:** none.
- **Acceptance:** A committed `knowledge/record_counts.json` is the single source;
  all prose derives from it; CI fails on divergence.
- **Files:** `README.md`, `content/trust_summary.md`, `review-manifest.json`, `knowledge/*.json`, `scripts/validate-trust.js`

### ED-C04 — Make human-review status consistent across sources, reports, and UI
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Goal:** One definition of "human-reviewed" flows from source decisions to reports to the card UI.
- **Why it matters:** `human_review_required` (graph, 29), overrides decisions (9
  decisions / 28 claims), and export `humanReviewed` (34 relations, matched by
  claim text) are three different measures shown as if equivalent; the card UI must
  not imply platform adjudication that hasn't happened.
- **Scope:** Define states (pending / flagged / independently-reviewed /
  adjudicated); map each source field to a state; surface it consistently in the
  TRUST card and reports.
- **Non-goals:** Creating decisions; upgrading agent proposals to human decisions.
- **Dependencies:** ED-C03, ED-E02.
- **Acceptance:** Every claim's review state is identical in graph, report, and rendered card; documented mapping.
- **Files:** `knowledge/claim_graph.json`, `knowledge/trust_human_review_overrides.json`, `content/trust-claim-widget.mjs`, `content/trust_summary.md`

### ED-C05 — Label native TRUST experimental and non-probabilistic
- **Status:** review · **Priority:** P0 · **Size:** S · **Agent:** yes · **Upstream:** local (wording) + TRUST fork (rubric text)
- **Goal:** Every public surface labels native TRUST v2 as experimental and states it is not a probability that a claim is true.
- **Why it matters:** `TRUST.md`/`TRUST_RUBRIC.md` already say it is not a
  probability, but the card UI, `trust_summary.md`, and README do not consistently
  carry an "experimental" label; a numeric score out of 100 invites misreading as confidence/probability.
- **Scope:** Add an "experimental" qualifier and a "not a probability of truth"
  note to the TRUST card, summary, and README; keep wording aligned with the rubric.
- **Non-goals:** Changing scores or the rubric's meaning.
- **Dependencies:** none.
- **Acceptance:** Rendered card + summary + README all state experimental status and the non-probability caveat.
- **Files:** `content/trust-claim-widget.mjs`, `content/trust_summary.md`, `README.md`, `TRUST.md`

### ED-C06 — Identify malformed or incomplete claims needing scientific review
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** Surface claims that are structurally incomplete or scientifically ambiguous for the review queue.
- **Why it matters:** Some claims are dangling references ("laid out in,", "found a
  stable Reduction estimate") suggesting broken cross-refs or truncated prose.
- **Scope:** Detect structural defects mechanically; route judgment calls to `SCIENTIFIC_REVIEW_QUEUE.md`.
- **Non-goals:** Rewriting claims to pass a check.
- **Dependencies:** ED-C01.
- **Acceptance:** List of malformed/incomplete claims with defect type; judgment items queued.
- **Files:** `knowledge/claim_graph.json`, `content/*.md`, `SCIENTIFIC_REVIEW_QUEUE.md`

### ED-C07 — Split compound single-atom claims during substantive review (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** L · **Agent:** no · **Upstream:** local
- **Goal:** Where a claim bundles multiple propositions, split into finer atoms *when a claim receives substantive human review*.
- **Why it matters:** One-atom-per-claim is a coarse migration default; finer atoms improve attribution precision.
- **Scope:** Human-guided atom splitting; preserve original record.
- **Non-goals:** Bulk automated splitting; inventing attribution.
- **Dependencies:** ED-A01, ED-C02.
- **Acceptance:** Reviewed compound claims split with provenance; originals preserved.
- **Files:** `knowledge/claim_graph.json`

### ED-C08 — Improved review-level and section-level TRUST summaries (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Goal:** Richer, clearer rollups (distribution, caps, review-state) without implying a single trust number for the review.
- **Dependencies:** ED-C03. **Files:** `content/trust_summary.md`, `scripts/build_trust_summary.py`

### ED-C09 — Claim-lineage support across later review versions (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** conditional · **Upstream:** cross-repository (ORAtlas + TRUST fork)
- **Goal:** Stable claim identity across future revisions so ORAtlas can track a claim over versions.
- **Dependencies:** ED-C03. **Files:** `knowledge/claim_graph.json`, `knowledge/trust_v1_to_v2_id_map.json`

### ED-C10 — Migration path to future TRUST rubric versions (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** conditional · **Upstream:** TRUST fork
- **Goal:** Documented, reproducible upgrade when the TRUST fork releases a new rubric.
- **Dependencies:** none. **Files:** `scripts/migrate-trust-v2.js`, `knowledge/TRUST_RUBRIC.md`

### ED-C11 — Domain-specific TRUST calibration experiment (P3)
- **Status:** backlog · **Priority:** P3 · **Size:** L · **Agent:** no · **Upstream:** TRUST fork
- **Goal:** Explore calibrating component thresholds to preclinical-animal-welfare literature; findings feed the fork, not local overrides.

### ED-C12 — Formal ontology alignment (P3)
- **Status:** backlog · **Priority:** P3 · **Size:** L · **Agent:** no · **Upstream:** cross-repository
- **Goal:** Explore aligning entities/scope vocabulary with an external ontology.

---

## Workstream D — Review interface and MyST rendering

### ED-D01 — Separate the Literature Evidence view from the Claims/TRUST view
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Implementation:** PR #7
- **Goal:** Distinct navigation and terminology for the two evidence layers
  (section literature evidence vs claim-level TRUST assessments).
- **Why it matters:** "Evidence Database" and "Citation Trust Summary" read as one
  thing; they are different layers with different provenance and must not be conflated.
- **Scope:** Rename/relabel views and nav; add short explainer distinguishing the layers.
- **Non-goals:** Merging the datasets.
- **Dependencies:** ED-B02.
- **Acceptance:** Site clearly presents two labelled layers; terminology consistent across pages.
- **Files:** `myst.yml`, `content/evidence_database.md`, `content/trust_summary.md`

### ED-D02 — Synchronize the single-active-panel TRUST viewer from the TRUST fork
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** TRUST fork (sync)
- **Implementation:** PR #7
- **Goal:** Only one TRUST panel open at a time; no overlapping/stacked panels.
- **Why it matters:** Overlapping margin panels are a known, fixed defect upstream;
  the local widget has partial single-active highlight logic but not the corrected panel behaviour.
- **Scope:** Pull the corrected widget behaviour from the TRUST fork, record the
  sync in `UPSTREAM_SYNC.md`, keep local-only divergences minimal and documented.
- **Non-goals:** Reimplementing the viewer from scratch here.
- **Dependencies:** none.
- **Acceptance:** Opening a second card closes the first; no overlap in Chromium/Firefox/WebKit; test added.
- **Files:** `content/trust-claim-widget.mjs`, `content/trust-claim-widget.css`, `plugins/trust-claim-plugin.mjs`, `UPSTREAM_SYNC.md`

### ED-D03 — Browser + accessibility regression tests
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Implementation:** PR #7
- **Goal:** Automated tests for Safari/WebKit behaviour, exact prose highlighting, and keyboard navigation/accessibility.
- **Why it matters:** Highlighting and slide-out interactions are the core UX and are currently untested in a real browser.
- **Scope:** Playwright (Chromium/Firefox/WebKit) tests for highlight exactness, keyboard focus, ARIA states.
- **Non-goals:** Visual pixel diffing of figures.
- **Dependencies:** ED-D02.
- **Acceptance:** CI runs the three engines where available; tests cover highlight, keyboard, and card open/close.
- **Files:** `tests/`, `.github/workflows/deploy.yml`

### ED-D04 — Clear empty, incomplete, and error states
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Implementation:** PR #7
- **Goal:** Every widget renders explicit empty/incomplete/error states instead of blank output.
- **Why it matters:** The empty Evidence Explorer failed silently; UI must fail visibly.
- **Dependencies:** ED-B02, ED-B04.
- **Acceptance:** Forced empty/error inputs render visible states; tested.
- **Files:** `content/evidence-explorer-widget.mjs`, `content/trust-claim-widget.mjs`

### ED-D05 — Better contradiction presentation (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** upstream template
- **Implementation:** PR #7
- **Goal:** Present inter-study conflicts clearly (both sides, resolution status) in the evidence view.
- **Dependencies:** ED-B02. **Files:** `content/evidence-explorer-widget.mjs`

### ED-D06 — Evidence-gap visualization (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** upstream template
- **Implementation:** PR #7
- **Goal:** Surface `evidence_gaps`/`unreplicated_claims` per section.
- **Dependencies:** ED-B06. **Files:** `content/evidence-explorer-widget.mjs`

---

## Workstream E — Human review and adjudication

### ED-E01 — Transparent prioritization strategy + stratified calibration subset
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** A documented, reproducible strategy for which claims are reviewed first, and a stratified calibration subset for benchmarking.
- **Why it matters:** Human time is scarce; prioritization must target the highest-consequence claims, not arbitrary ones.
- **Scope:** Define priority signals (low band, caps, high argumentative weight);
  select a stratified subset; document rationale. Selection is mechanical; the reviews themselves are not.
- **Non-goals:** Making the decisions; synthesizing reviewer opinions.
- **Dependencies:** ED-C03.
- **Acceptance:** Committed prioritization doc + calibration-subset list with selection provenance.
- **Files:** `SCIENTIFIC_REVIEW_QUEUE.md`, new `knowledge/review_priority.json`

### ED-E02 — Decision store: separate states, preserve rationale, never overwrite
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Goal:** A durable structure separating pending / independently-reviewed /
  adjudicated states, preserving every decision and reviewer rationale, and never overwriting earlier agent assessments.
- **Why it matters:** Human decisions are the scientific value; losing or overwriting them is unrecoverable.
- **Scope:** Extend `trust_human_review_overrides.json` (or a sibling) with append-only decision records, reviewer id, timestamp, rationale, and state.
- **Non-goals:** Entering decisions; deleting history.
- **Dependencies:** ED-C04.
- **Acceptance:** Schema + validator for the decision store; append-only enforced; existing 9 decisions migrated losslessly.
- **Files:** `knowledge/trust_human_review_overrides.json`, `knowledge/schemas/`, `scripts/validate-trust.js`

### ED-E03 — Reviewer instructions, data-entry format, deterministic merge
- **Status:** review · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** Clear reviewer instructions, a simple data-entry format, and a deterministic process to merge completed reviews back into the graph.
- **Why it matters:** Without a defined format, human input is inconsistent and hard to merge.
- **Scope:** Author instructions + template + a deterministic merge script; no synthetic decisions.
- **Dependencies:** ED-E02.
- **Acceptance:** A dry-run merge reproduces byte-identical output from the same inputs; instructions committed.
- **Files:** new `knowledge/REVIEWER_INSTRUCTIONS.md`, `scripts/`, `knowledge/trust_human_review_overrides.json`

### ED-E04 — Additional human adjudication rounds (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** L · **Agent:** no · **Upstream:** local
- **Goal:** Extend adjudication beyond the initial flagged set as capacity allows.
- **Dependencies:** ED-E01, ED-E02, ED-E03. **Files:** `SCIENTIFIC_REVIEW_QUEUE.md`

### ED-E05 — Cross-review claim comparison experiments (P3)
- **Status:** backlog · **Priority:** P3 · **Size:** L · **Agent:** no · **Upstream:** cross-repository (ORAtlas)
- **Goal:** Explore comparing this review's claims against a second review once one exists.

---

## Workstream F — ORAtlas interoperability

### ED-F01 — Contract tests against the ORAtlas manifest and artifact schemas
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** cross-repository (schemas from ORAtlas)
- **Goal:** Automated tests validating `review-manifest.json` and the four
  `knowledge/oratlas/*.jsonl` + `provenance.json` against the ORAtlas contract.
- **Why it matters:** The export currently has no tests; a schema drift in either repo would break ingestion silently.
- **Scope:** Add schema/contract tests using ORAtlas's published schemas (pin the
  exact schema version); assert record shapes and required fields.
- **Non-goals:** Reimplementing ORAtlas validation locally as the source of truth.
- **Dependencies:** ED-F02.
- **Acceptance:** CI validates all five artifacts against the pinned ORAtlas schema; a malformed record fails.
- **Files:** `tests/`, `scripts/export-oratlas.js`, `knowledge/oratlas/`, `review-manifest.json`

### ED-F02 — Verify and lock export semantics (claim-level, not-assessed, source assessment)
- **Status:** review · **Priority:** P0 · **Size:** M · **Agent:** yes · **Upstream:** local (semantics) + cross-repository (contract)
- **Goal:** Assert, in tests, that the export: keeps native TRUST v2 **claim-level**
  and never emits it as an ORAtlas relation-level aggregate; keeps all ten ORAtlas
  criteria `not-assessed` unless actually assessed; preserves native TRUST under an
  explicit source assessment with protocol, rubric, unit, and provenance.
- **Why it matters:** The whole point of the export is to *not* silently
  reinterpret the five review-local dimensions as ORAtlas's ten relation criteria.
  The code does this today (criteria all `not-assessed`; score carried as
  `aggregateScore` with a limitation note), but nothing prevents regression.
- **Scope:** Lock the semantics with tests; make the "claim-level score repeated
  per relation for transport" explicit and documented; confirm unit (0–1 vs 0–100) and protocol version are preserved.
- **Non-goals:** Building an ORAtlas crosswalk; changing ORAtlas's contract.
- **Dependencies:** ED-C03.
- **Acceptance:** Tests fail if any ORAtlas criterion becomes non-`not-assessed`
  without an assessment, or if the native score is emitted as a relation aggregate; provenance fields asserted.
- **Files:** `scripts/export-oratlas.js`, `tests/`, `TRUST.md`, `knowledge/oratlas/provenance.json`

### ED-F03 — Prevent source human-review from reading as ORAtlas platform verification
- **Status:** review · **Priority:** P0 · **Size:** S · **Agent:** yes · **Upstream:** cross-repository
- **Goal:** The `humanReviewed`/`reviewStatus: human-reviewed` fields must clearly
  denote *source-side* review, not ORAtlas platform adjudication.
- **Why it matters:** Export marks 34 relations `human-reviewed` by matching claim
  text to source overrides; if ORAtlas treats that as platform verification, it overstates adjudication.
- **Scope:** Rename/annotate the field to `sourceHumanReviewed` (or add explicit
  `verificationAuthority: source`); document the semantics; coordinate the field name with ORAtlas.
- **Non-goals:** Changing what counts as a source decision.
- **Dependencies:** ED-C04, ED-F02.
- **Acceptance:** Export distinguishes source review from platform verification; documented + tested; ORAtlas side tracked in `UPSTREAM_SYNC.md`.
- **Files:** `scripts/export-oratlas.js`, `knowledge/oratlas/`, `TRUST.md`

### ED-F04 — Export exact record counts and artifact hashes
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** The export writes exact record counts and content hashes for each artifact into `provenance.json`.
- **Why it matters:** ORAtlas needs to verify it ingested the exact artifacts; hashes make ingestion tamper-evident and reproducible.
- **Scope:** Add per-artifact SHA-256 and counts to the export provenance; assert in CI.
- **Dependencies:** ED-C03, ED-F02.
- **Acceptance:** `provenance.json` carries counts + hashes matching the emitted files; CI verifies.
- **Files:** `scripts/export-oratlas.js`, `knowledge/oratlas/provenance.json`

### ED-F05 — Additional immutable ORAtlas ingestion fixtures (P2)
- **Status:** review · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** cross-repository
- **Goal:** Curated small fixtures (edge cases: contradictory context, capped claim, multi-citation claim) for ORAtlas ingestion tests, pinned to a commit.
- **Dependencies:** ED-F01. **Files:** new `knowledge/oratlas/fixtures/`

### ED-F06 — Public reviewer contribution workflow through ORAtlas (P3)
- **Status:** backlog · **Priority:** P3 · **Size:** L · **Agent:** no · **Upstream:** ORAtlas
- **Goal:** Explore how external reviewers could contribute challenges/assessments via ORAtlas against a frozen release.

---

## Workstream G — Validation and reproducibility

### ED-G01 — Schema validation for graph / context / TRUST in CI
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** local (schemas may sync to TRUST fork)
- **Goal:** Validate `claim_graph.json` and records against `knowledge/schemas/*` in CI.
- **Why it matters:** Schemas exist but nothing asserts the artifacts conform on every push.
- **Dependencies:** none.
- **Acceptance:** CI validates all knowledge artifacts against committed schemas.
- **Files:** `knowledge/schemas/`, `scripts/validate-trust.js`, `.github/workflows/deploy.yml`

### ED-G02 — Record-count and hash checks in CI
- **Status:** review · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** CI asserts the single-source counts (ED-C03) and export hashes (ED-F04) match reality.
- **Dependencies:** ED-C03, ED-F04.
- **Acceptance:** Divergence between `record_counts.json`, artifacts, and prose fails CI.
- **Files:** `scripts/`, `.github/workflows/deploy.yml`

### ED-G03 — Deterministic figure execution
- **Status:** backlog · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** upstream template
- **Goal:** Figure notebooks produce byte-stable output in the CI environment.
- **Why it matters:** Non-deterministic figures undermine reproducible releases.
- **Dependencies:** none. **Files:** `figures/notebooks/`, `scripts/build_trust_figures.py`

### ED-G04 — Deterministic full build check (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** M · **Agent:** yes · **Upstream:** local
- **Goal:** Re-running the build from clean produces identical `_build` content (modulo timestamps).
- **Dependencies:** ED-G03. **Files:** `.github/workflows/deploy.yml`

### ED-G05 — Automated living-review monitoring (P3)
- **Status:** backlog · **Priority:** P3 · **Size:** L · **Agent:** conditional · **Upstream:** cross-repository
- **Goal:** Explore monitoring for new literature that would update flagged claims.

---

## Workstream H — Release, provenance, and documentation

### ED-H01 — Define and validate the frozen reference-release contract
- **Status:** ready · **Priority:** P1 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** Acceptance criteria for the first stable ORAtlas-integration release:
  frozen record counts, frozen artifact hashes, validated MyST build, validated
  figures/notebooks, Chromium/Firefox/WebKit checks where possible, updated
  AI-assistance and experimental-status disclosures, a tagged prerelease, ORAtlas
  pinned to the exact tag/commit, and a documented limitations list.
- **Why it matters:** ORAtlas must ingest an immutable, internally consistent
  artifact — not the moving branch — and the release must not overstate its status.
- **Scope:** Write the release checklist/contract; wire the automated parts; cut the tagged prerelease.
- **Non-goals:** Minting a DOI (ED-H03); claiming peer review.
- **Dependencies:** ED-B02, ED-C03, ED-F02, ED-F04.
- **Acceptance:** A release-contract doc + CI gate; a prerelease tag whose artifacts match the frozen counts/hashes; limitations documented.
- **Files:** new `RELEASE_CONTRACT.md`, `DEPLOY.md`, `.github/workflows/deploy.yml`, `knowledge/oratlas/`

### ED-H02 — Update disclosures and public-status wording
- **Status:** backlog · **Priority:** P1 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** AI-assistance disclosure, experimental-TRUST status, and "not peer
  reviewed / not fully adjudicated" wording are accurate and consistent across README, releases, and site.
- **Why it matters:** Overstated status is a scientific-integrity risk.
- **Dependencies:** ED-C03, ED-C05.
- **Acceptance:** Consistent status wording everywhere; reconciled with real review numbers.
- **Files:** `README.md`, `content/00_frontmatter.md`, `DEPLOY.md`, release notes

### ED-H03 — DOI / Zenodo preparation (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** M · **Agent:** conditional · **Upstream:** local
- **Goal:** Prepare Zenodo metadata and process so a review-specific DOI can be
  minted for the first stable release (distinct from the template DOI).
- **Dependencies:** ED-H01. **Files:** new `.zenodo.json`, `README.md`, `FAIR.md`

### ED-H04 — Contributor and CRediT documentation (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** Complete CRediT roles and contributor metadata; resolve MyST contributor warnings.
- **Dependencies:** none. **Files:** `content/authors.yml`, `review-manifest.json`

### ED-H05 — Improved reproducibility instructions (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** End-to-end reproduce instructions (pinned deps, exact commands) for validation, export, and build.
- **Dependencies:** ED-G04. **Files:** `README.md`, `DEPLOY.md`, `requirements.txt`, `package.json`

### ED-H06 — Changelog and versioning hygiene (P2)
- **Status:** backlog · **Priority:** P2 · **Size:** S · **Agent:** yes · **Upstream:** local
- **Goal:** `CHANGELOG.md` currently documents the *skill catalogue* (v28→v29), not
  the review/release history; add a review-facing changelog and a versioning policy.
- **Dependencies:** none. **Files:** `CHANGELOG.md`, `DEPLOY.md`

---

## Item index by priority and workstream

| WS | P0 | P1 | P2 | P3 | Total |
|---|---:|---:|---:|---:|---:|
| A Content/claims | 0 | 2 | 2 | 0 | 4 |
| B Evidence DB | 3 | 2 | 1 | 0 | 6 |
| C Claim/TRUST | 5 | 1 | 4 | 2 | 12 |
| D Interface | 0 | 4 | 2 | 0 | 6 |
| E Human review | 0 | 3 | 1 | 1 | 5 |
| F ORAtlas | 3 | 1 | 1 | 1 | 6 |
| G Validation | 0 | 2 | 2 | 1 | 5 |
| H Release/docs | 0 | 2 | 4 | 0 | 6 |
| **Total** | **14** | **17** | **17** | **5** | **53** |

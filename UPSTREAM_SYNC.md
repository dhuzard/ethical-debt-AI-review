# Upstream synchronization log

This repository is a **reference implementation and test corpus**, not the home of
the generic review pipeline or the TRUST methodology. Much of its infrastructure is
inherited from two upstreams:

- **Template** — `AllenNeuralDynamics/ComputationalReviewTemplate` (generic computational-review pipeline, Evidence Explorer, MyST patterns).
- **TRUST fork** — `Neuronautix/ComputationalReviewTemplate_trust-knowledge` (TRUST rubric, schemas, claim/TRUST plugin and widget, validator).

A third repo, `dhuzard/oratlas`, consumes the export; it is tracked in
`REVIEW_BACKLOG.md` workstream F, not here.

**Purpose of this log:** record where inherited code diverged locally, so that generic
fixes are pushed upstream rather than re-implemented here, and so temporary local
patches are visible and reversible. Per the autonomous-agent rules, any local fix to a
reusable component must be linked to an upstream backlog item and recorded below.

**Status of this log:** initial inventory. Upstream commit pins are **not yet
recorded** — the upstream repositories are not in this session's scope, so the
"Upstream commit" column must be filled by whoever performs the first real sync
(they should `git remote add` the upstream, identify the closest matching commit, and
update the row). Local commits are the last commit that touched each component on the
`main`/`trust-scores` line as of 2026-07-19. Do not attempt to synchronize all code at
once; sync per component, under its own backlog item.

---

## Tracked components

### 1. Evidence Explorer plugin
- **Component:** `plugins/evidence-explorer-plugin.mjs`
- **Upstream repository:** Template
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `b89196f` (2026-07-06)
- **Local modifications:** Universal conflict normalizer (`normalizeConflict`) handling 15+ conflict-schema variants; section scan range 2–13.
- **Reason for divergence:** Adapt to this review's heterogeneous conflict shapes.
- **Temporary local patch (ED-B02, in review):** Loader now discovers canonical `evidence_section_NN.json` files dynamically (while retaining both legacy names), prefers rich `findings[]` objects, derives paper counts from DOI/citation keys, and has corpus regression tests. This generic correction still needs to be ported to the Template; remove the local divergence after that upstream sync.
- **Should divergence be removed later?** Yes — fold the fix into the Template loader and drop any local patch.

### 2. Evidence Explorer widget
- **Component:** `content/evidence-explorer-widget.mjs`
- **Upstream repository:** Template
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `b89196f` (2026-07-06)
- **Local modifications:** Rendering tuned to this review's findings/conflicts/figure fields.
- **Reason for divergence:** Review-specific display; empty/error states pending (**ED-D04**).
- **Should divergence be removed later?** Partly — empty/incomplete/error states are generic and belong upstream.

### 3. TRUST claim plugin
- **Component:** `plugins/trust-claim-plugin.mjs`
- **Upstream repository:** TRUST fork
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `d9c7135` (2026-07-16)
- **Local modifications:** TextQuoteSelector-based exact-prose anchoring, margin-aside generation, scope/target wrapping.
- **Reason for divergence:** Enriched TRUST v2 in-text cards for this review.
- **Should divergence be removed later?** Generic anchoring logic should converge with the fork; review-specific wiring stays local.

### 4. TRUST claim widget (+ CSS)
- **Component:** `content/trust-claim-widget.mjs`, `content/trust-claim-widget.css`
- **Upstream repository:** TRUST fork
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `1d89f86` (2026-07-17)
- **Local modifications:** Prose highlighting, dark-mode margin cards, single-active highlight cleanup.
- **Reason for divergence:** Local UI polish (commits "Improve TRUST score and text interactions", "Enhance prose highlighting…").
- **Known gap:** The corrected **single-active-panel** behaviour (no overlapping TRUST panels) exists upstream and must be synced — **ED-D02**.
- **Should divergence be removed later?** Yes for panel behaviour — take the fork's fix; keep only genuinely review-specific styling.

### 5. Validation skills
- **Component:** `skills/comprev-*.md` (e.g. `comprev-trust-score-validator.md`, `comprev-evidence-validator.md`, `comprev-citation-validator.md`, `comprev-myst-validator.md`)
- **Upstream repository:** Template + TRUST fork (orchestrator v29 skill catalogue)
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** committed with the review; catalogue documented in `CHANGELOG.md` (v28→v29).
- **Local modifications:** These are the historical pipeline skills that produced the review; not expected to change here.
- **Reason for divergence:** Snapshot of the pipeline used for this review.
- **Should divergence be removed later?** No — retain as provenance; do not re-run to mutate artifacts (agent rule 19).

### 6. Evidence schemas
- **Component:** `evidence/README.md` schema (per-section evidence package format)
- **Upstream repository:** Template
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** documents `section_NN_evidence_package.json` (stale vs actual `evidence_section_NN.json`).
- **Local modifications:** None intended; documentation is out of date.
- **Reason for divergence:** Rename to `evidence_section_NN.json` (per CHANGELOG v29) not reflected in the loader or README.
- **Should divergence be removed later?** Yes — reconcile via **ED-B05**; align README, loader, and files on one name.

### 7. TRUST schemas and rubric
- **Component:** `knowledge/schemas/claim_context.schema.json`, `knowledge/schemas/trust_score.schema.json`, `knowledge/schemas/claim_graph.schema.json`, `knowledge/TRUST_RUBRIC.md`
- **Upstream repository:** TRUST fork
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `d9c7135` (2026-07-16); rubric version `2.0.0`.
- **Local modifications:** None known; treat as canonical-from-fork.
- **Reason for divergence:** n/a — should track the fork exactly.
- **Should divergence be removed later?** Any local edit to these is a red flag; changes belong in the fork (agent rules 8–9). Schema-conformance CI is **ED-G01**; future rubric migration is **ED-C10**.

### 8. Validator
- **Component:** `scripts/validate-trust.js`, `scripts/test-trust-validator.js`
- **Upstream repository:** TRUST fork
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `fc0fbb6` (2026-07-16)
- **Local modifications:** Applies rubric v2 tables to this repo's claim graph.
- **Reason for divergence:** Wired to local artifact paths.
- **Should divergence be removed later?** Generic checks (directive↔record resolution ED-C01, atom/passage ED-C02) should converge with the fork's validator.

### 9. MyST configuration patterns
- **Component:** `myst.yml`, plugin registration, TOC, exports
- **Upstream repository:** Template
- **Upstream commit:** _unrecorded — pin on first sync_
- **Local commit:** `d9c7135` (2026-07-16)
- **Local modifications:** Review-specific TOC, four registered plugins, LaTeX/PDF export templates, `BASE_URL` handling.
- **Reason for divergence:** Review-specific site; expected and permanent.
- **Should divergence be removed later?** No — configuration is review-owned; only generic plugin/theme patterns track upstream.

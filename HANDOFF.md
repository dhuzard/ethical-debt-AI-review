# Ethical Debt Review — Resume Handoff

**Pipeline:** Expert Review Orchestrator v29 (`skills/comprev-orchestrator-v29.md`)
**Last updated:** 2026-07-08

## How to resume
In any session, say: **"Resume the Ethical Debt review from phase_ledger.json"**.
The coordinator reads `phase_ledger.json` + the gate files below and continues from the
first phase whose status is not `complete`. All prior work is on disk — zero rework.

## Where we are
- **Complete & gated:** Phase 1 (scope/1V), Phase 2 (evidence, 1,339 unique DOIs, `PASS_WITH_DOCUMENTED_EXITS`, user sign-off), Phase 3 (1,337 citation keys, 3V), Phase 4 (scaffold, gate), Phase 5 (curation — 9 per-section packages, 1,417 body findings, 5V pass after a CROSS_SECTION_DIFFERENTIATION fix).
- **Current phase:** Phase 6 — NOT started. Next action on resume.
- **Next:** Phase 6 (blinded figure-comparability audit of the 24 figure specs / 60 figure_data candidates; coordinator must pre-fetch abstracts and pass inline — the critic has no network) → Phase 7 (draft 7 body sections 02-08 in parallel batches of 4, each writer gets its `evidence_section_NN.json` + `citemap_section_NN.json` + `authortable_section_NN.json` + `scaffold_section_NN.json`) → 8 critics → 9 bibliography (build references.bib from crossref_metadata.json) → 10 integration → 11 intro/conclusion → 12 → 13 Methods → 14 assembly+MyST build → 15-19 citation triple verification → 20 push to github.com/dhuzard/ethical-debt-AI-review → 21 deploy polish.

## State on disk (the real checkpoint)
- `phase_ledger.json` — per-phase status + gate artifact ids (source of truth for sequencing)
- `scope.json`, `gate_scope.json` — scope + 21-phase plan
- `provenance/` — review_request.{txt,md}, gate_scope_validation_1v.json, gate_evidence_compliance.json (2V), gate_citation_infrastructure.json (3V), citation_key_map.json (1,337), author_name_table.json, crossref_metadata.json, scaffold_digest.json, all_dois.json
- `scaffold.json`, `gate_scaffold_approved.json` — Phase 4
- `evidence/cluster_01..08_*.json` — raw Phase 2 evidence (findings/conflicts/figure_data/saturation)
- `evidence/evidence_section_01..09.json` — Phase 5 per-section packages; `scaffold_section_*`, `citemap_section_*`, `authortable_section_*` — per-section writer inputs
- `scripts/` — fetch_crossref.py, build_citation_keys.py, build_curation.py (re-runnable)
- `phase2_progress.json` — Phase 2 close-out record

## Notes for the resuming coordinator
- Evidence is closed at 1,339 unique (user accepted the documented near-target/saturation exit; hard 1,000 floor met). Do NOT reopen Phase 2 unless asked.
- Account usage limit was hit ~4x during Phase 2 (rolling ~5h windows). Expect to pause/resume across limit windows; the loop is limit-resilient because every subagent saves append-only to disk.
- Rule enforced for all evidence subagents: no nested sub-subagents; light frames; prefer PubMed MCP + Europe PMC over slow WebFetch.
- Direct network (CrossRef/Europe PMC) works from the sandbox Python — bulk mechanical fetches were done via background scripts (zero model tokens) rather than subagents.

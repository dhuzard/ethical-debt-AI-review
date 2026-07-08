# Ethical Debt Review — Resume Handoff

**Pipeline:** Expert Review Orchestrator v29 (`skills/comprev-orchestrator-v29.md`)
**Last updated:** 2026-07-08

## How to resume
In any session, say: **"Resume the Ethical Debt review from phase_ledger.json"**.
The coordinator reads `phase_ledger.json` + the gate files below and continues from the
first phase whose status is not `complete`. All prior work is on disk — zero rework.

## Where we are
- **Complete & gated:** Phases 1-7 as before, PLUS:
  - **Phase 8 (Section Critics, blinded):** gate_critic_complete.json PASS. 16 MUST_FIX found across 7 sections, 0 remaining (sec02 Voelkl2018 50→440; sec03 4 suppressed welfare conflicts restored, survival→1.00; sec04 Hamilton2022 0.3% denominator + 3 conflicts + ELN cites, figure re-rendered; sec07 5 fixes incl Flanagan2026 direction + 2 open conflicts + Klebel2025 reframe, survival→1.00; sec08 Munro2022 reclassified in figure+caption). 18 SHOULD_CAVEAT deferred to Phase 10 (provenance/phase10_caveats.json). Actor-critic separation held.
  - **Phase 9 (Bibliography):** gate_bibliography.json PASS. content/references.bib = 1337 entries via scripts/build_bibliography.py, 992 distinct keys cited across body, 0 orphaned, 0 missing core fields. Fixed ONUMA2026 vs Onuma2026 case-collision → renamed uncited one to Onuma2026b, normalized all-caps families (crossref_metadata/author_name_table/citemap_03/authortable_03).
- **Current phase:** Phase 10 — Integration (6 passes + 18 SHOULD_CAVEAT amendments), IN PROGRESS (single full-visibility agent editing content/02-08 in place; 6b/6e/6f already mechanically verified clean by coordinator, agent does 6a transitions/6c terminology/6d continuity + the caveats). Gate to write: provenance/gate_integration.json.
- **Next:** 11 intro/conclusion/abstract/frontmatter (body-only master citation set; NO novel keys) → 12 bookend critic → 13 Methods.md (also: change Methods pipeline figure `:label:`→`:name:`) → 14 assembly+MyST build (14V) → 15 citation triples → 16 citation full-text verification (verify sec04 orphan-finding keys Hamilton2022/Gabelica2022/Smith2007/Colavizza2024/Prosser2024) → 17-19 fix prep/exec/apply → 20 push to github.com/dhuzard/ethical-debt-AI-review → 21 deploy polish (optional: enrich bib co-author given-names).
- Phase 7 writer IDs (for further targeted revisions): 02=a35054446f311dd5b 03=a221134dc025540a3 04=abb38235075c3452b 05=aee4c3a3b0a0edd8a 06=a48e4ca883200ea04 07=ac006ab01d0811151 08=a6e8e409e459f2dc6.

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

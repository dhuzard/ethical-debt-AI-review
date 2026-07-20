# Scientific review queue — The Ethical Debt

Mechanical prioritization and the 12-claim calibration subset are committed in
`knowledge/review_priority.json`; reviewer procedure and the append-only data-entry
workflow are in `knowledge/REVIEWER_INSTRUCTIONS.md`. Ranking is not adjudication:
all outcomes and rationales below still require human scientific judgment.

The separate mechanical structural audit is in `knowledge/claim_quality_flags.json`.
It flags long compound single-atom claims, empty structured scopes, and suspected
dangling phrases without declaring them scientifically wrong or editing their prose.

Items on this list require **human scientific judgment**. They are *not* engineering
tasks — do not resolve them by editing validation, rescoring, or rewording to lift a
score. Ordinary engineering work belongs in `REVIEW_BACKLOG.md`.

**Provenance of this list.** Every entry is drawn from an *existing explicit flag* in
the committed artifacts — the 29 claims with `human_review_required: true` in
`knowledge/claim_graph.json` (all currently `low_trust`; 25 capped
`contradicted_without_caveat`, 3 `overextended_scope`, 1 uncapped). No new expert
decisions have been invented. The 18 deferred `SHOULD_CAVEAT` amendments in
`provenance/phase10_caveats.json` are additionally surfaced under "Wording
overstatement" and are tracked for application by backlog item **ED-A02**.

**Rules.** Do not invent evidence, effect sizes, replication states, or expert
decisions. Preserve the original record. Record every decision with a rationale and a
reviewer identity in `knowledge/trust_human_review_overrides.json` (see ED-E02). A
claim leaves this queue only when a human has recorded a decision.

Statuses: `pending` · `in-review` · `adjudicated` · `deferred`.

Counts at snapshot (2026-07-19): 29 flagged claims →
entailment 1 · scope/transferability 6 · contradictory 13 · independence/replication 1 ·
statistical/methodological 3 · governance interpretation 5; plus 18 deferred caveats.

---

## Group 1 — Citation or entailment uncertainty

### SR-01
- **Claim ID:** `clm_829f80a895bab81c` · **Section:** Introduction
- **Claim text:** "By March 2026, EMA had issued a draft qualification opinion for virtual controls in rat non-GLP dose-range-finding studies, a narrower context than pivotal toxicology studies."
- **Reason review is needed:** Uncapped `low_trust` (65) resting on a single primary source; needs a human to confirm the cited EMA draft opinion entails the exact regulatory scope as worded ("narrower context than pivotal toxicology").
- **Relevant citations:** EMA2026VCG
- **Current evidence relation:** directly_supported · **Scope:** matched
- **Current TRUST status:** low_trust, score 65, uncapped, flagged for human review
- **Potential consequence if incorrect:** Overstates or misstates a live regulatory position on virtual control groups — a load-bearing claim for the VCG argument.
- **Suggested expertise:** Regulatory toxicology / EMA qualification procedures
- **Status:** pending · **Decision & rationale:** _—_

---

## Group 2 — Scope or transferability concern

### SR-02
- **Claim ID:** `clm_0fde28aeec8b0c15` · **Section:** Introduction
- **Claim text:** "The empirical anchor the review returns to most often — that actual, usable data availability sits near two percent while declared availability and paperwork compliance sit far above it — … it is against that near-static baseline — the empirical ~2% availability anchor — that every enforcement result must be judged."
- **Reason review is needed:** Capped `overextended_scope`; the ~2% figure is generalised into a universal baseline "every enforcement result must be judged" against.
- **Relevant citations:** Hamilton2023, Hamilton2022, VanTuyl2016, Macleod2019b
- **Current evidence relation:** overextended · **Current TRUST status:** low_trust 55, cap `overextended_scope`
- **Potential consequence if incorrect:** A single field-wide estimate becomes the yardstick for the whole review; if its scope is narrower, downstream conclusions inherit the overreach.
- **Suggested expertise:** Meta-research / open-data auditing
- **Status:** pending · **Decision & rationale:** _—_

### SR-03
- **Claim ID:** `clm_9e06ef3c4c66e025` · **Section:** Introduction
- **Claim text:** "…because animals have already paid for the data with their welfare and, usually, their lives, letting the data go to waste is not merely poor science but a welfare harm in its own right, and repaying the debt … is a way of saving animals."
- **Reason review is needed:** Capped `overextended_scope`; the central thesis in its strongest form — needs a judgment on whether the "saving animals" conclusion is supported at the breadth stated.
- **Relevant citations:** Pound2018, Kramer2015, Wilkinson2016, Macleod2019b, Cait2022
- **Current evidence relation:** overextended · **Current TRUST status:** low_trust 55, cap `overextended_scope`
- **Potential consequence if incorrect:** This is the review's thesis sentence; overstatement here colours the entire argument.
- **Suggested expertise:** 3Rs / animal-welfare ethics + research-data policy
- **Status:** pending · **Decision & rationale:** _—_

### SR-04
- **Claim ID:** `clm_e351f540fdbcc374` · **Section:** Incentives
- **Claim text:** "The pattern generalises across national systems — in Ecuador, reliance on journal-centric metrics predicted lower adoption of open practices while institutional deposit mandates and data services predicted higher adoption."
- **Reason review is needed:** Capped `overextended_scope`; a single-country study (Ecuador) is used to support a cross-national generalisation.
- **Relevant citations:** Guerra2026
- **Current evidence relation:** overextended · **Current TRUST status:** low_trust 50, cap `overextended_scope`
- **Potential consequence if incorrect:** "Generalises across national systems" from one national case study is a transferability overreach.
- **Suggested expertise:** Research-policy / open-science incentives
- **Status:** pending · **Decision & rationale:** _—_

### SR-05
- **Claim ID:** `clm_a0648b6fbbd227a3` · **Section:** Conclusion
- **Claim text:** "A third is scope: the ~2% availability anchor is a field-wide medical estimate, and even the prescription that would exploit reuse — whether to standardise or to heterogenise animal studies — remains unresolved, so the operational advice the review can give is bounded."
- **Reason review is needed:** Flagged `contradicted_without_caveat`; a self-limiting scope statement that itself invokes the contested standardise-vs-heterogenise debate (Voelkl/Richter).
- **Relevant citations:** Hamilton2023, Voelkl2018, Richter2011
- **Current evidence relation:** conflicted · **Current TRUST status:** low_trust 60, cap `contradicted_without_caveat`
- **Potential consequence if incorrect:** Mis-states how bounded the review's operational advice is.
- **Suggested expertise:** Experimental design (reproducibility/heterogenisation)
- **Status:** pending · **Decision & rationale:** _—_

### SR-06
- **Claim ID:** `clm_eb649104f2fecfc4` · **Section:** Conclusion
- **Claim text:** "Second, it is not yet known whether regulators will accept virtual control groups, and the endpoint-dependence of their concordance together with the temporal and cross-laboratory drift of historical data mean the answer may differ for categorical toxicity calls and for continuous clinical-pathology parameters."
- **Reason review is needed:** Flagged `contradicted_without_caveat`; transferability of VCG concordance across endpoints/labs is genuinely unresolved.
- **Relevant citations:** DuchateauNguyen2026, Adedeji2024, Kellner2025, SATO2024
- **Current evidence relation:** conflicted · **Current TRUST status:** low_trust 60, cap `contradicted_without_caveat`
- **Potential consequence if incorrect:** Understates or overstates regulatory readiness of VCGs.
- **Suggested expertise:** Regulatory toxicology / historical-control statistics
- **Status:** pending · **Decision & rationale:** _—_

### SR-07
- **Claim ID:** `clm_536931fcfee707da` · **Section:** Conclusion
- **Claim text:** "Virtual control groups interrupt the loop at the most concrete point available … found a stable Reduction estimate of roughly a quarter of control animals … but a dividend conditional on endpoint-specific concordance and still unaccepted by any regulator for a pivotal preclinical study."
- **Reason review is needed:** Flagged `contradicted_without_caveat`; also has a broken cross-reference ("found a stable Reduction estimate" with no antecedent — see ED-C06). Quantitative + transferability judgment.
- **Relevant citations:** StegerHartmann2020, Gurjanov2024b, DuchateauNguyen2026, SATO2024
- **Current evidence relation:** conflicted · **Current TRUST status:** low_trust 60, cap `contradicted_without_caveat`
- **Potential consequence if incorrect:** Central VCG "quarter of control animals" reduction claim; also a wording defect.
- **Suggested expertise:** Regulatory toxicology / VCG methodology
- **Status:** pending · **Decision & rationale:** _—_

---

## Group 3 — Contradictory evidence

### SR-08
- **Claim ID:** `clm_f88a8b2eb442ae7f` · **Section:** Reproducibility
- **Claim text:** "Their value is not their precision but their convergence with a theoretical prior — that under realistic assumptions about power, bias, and pre-study odds, a research claim in most fields is more likely false than true."
- **Reason review is needed:** `contradicted_without_caveat`; the Ioannidis "most findings false" prior is itself contested (see SR-20) and stated without caveat.
- **Relevant citations:** Ioannidis2005b · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Anchors the reproducibility argument on a contested theoretical claim.
- **Suggested expertise:** Meta-research / statistics · **Status:** pending · **Decision:** _—_

### SR-09
- **Claim ID:** `clm_d422ccc8064b9d47` · **Section:** Reproducibility
- **Claim text:** "Opinion surveys of laboratory-animal researchers put the published fraction low: staff at not-for-profit institutes estimated that only half of conducted animal experiments are published, and those in for-profit settings estimated just 10%."
- **Reason review is needed:** `contradicted_without_caveat`; opinion-survey estimate presented against other publication-rate evidence without reconciliation.
- **Relevant citations:** terRiet2012 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** A headline "half of experiments unpublished" figure recurs across the review (SR-16, SR-19).
- **Suggested expertise:** Publication bias / survey methodology · **Status:** pending · **Decision:** _—_

### SR-10
- **Claim ID:** `clm_018f1c87836f8d42` · **Section:** Reproducibility
- **Claim text:** "…when a defensible analytic choice can flip a model from \"poorly mimics\" to \"greatly mimics\" human disease, the conclusion on translatability is being decided by analytic degrees of freedom rather than by the animals."
- **Reason review is needed:** `contradicted_without_caveat`; the Seok/Takao contradiction is the evidentiary basis and must be presented as the genuine dispute it is. Also has a broken cross-ref ("laid out in,").
- **Relevant citations:** Seok2013, Takao2014 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Key translatability argument; the two papers reach opposite conclusions on the same data.
- **Suggested expertise:** Translational modelling / bioinformatics · **Status:** pending · **Decision:** _—_

### SR-11
- **Claim ID:** `clm_c4ec854c82d44ccc` · **Section:** Data welfare / 3Rs
- **Claim text:** "…a fifteen-year database of blood markers from thirty-nine rhesus monkeys found no support for long-term cumulative effects … against this, telomere attrition is proposed as an objective, dose-dependent molecular record of an animal's lifetime negative experience…"
- **Reason review is needed:** `contradicted_without_caveat`; two opposing views on cumulative harm juxtaposed.
- **Relevant citations:** Wegener2021, Bateson2015 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Cumulative-harm assessment underpins severity claims.
- **Suggested expertise:** Laboratory-animal welfare / biomarkers · **Status:** pending · **Decision:** _—_

### SR-12
- **Claim ID:** `clm_3727c094cb228e45` · **Section:** Data welfare / 3Rs
- **Claim text:** "…in a rat liver-cirrhosis surgery model the usual welfare score-sheet parameters were insufficient to predict death until the cut-offs were retrospectively re-optimised, whereas an evidence-based … analysis of electrical kindling concluded that a simple welfare measure was a valid basis for grading severity."
- **Reason review is needed:** `contradicted_without_caveat`; conflicting evidence on welfare score-sheet validity.
- **Relevant citations:** Krueger2023, Moller2018 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Affects claims about severity-assessment instruments.
- **Suggested expertise:** Animal welfare assessment · **Status:** pending · **Decision:** _—_

### SR-13
- **Claim ID:** `clm_c150da83fe05ed23` · **Section:** FAIR data
- **Claim text:** "…the ISO/IEC 11179 model is presented as automatically conferring FAIR adherence … yet a variable-level harmonisation effort across cardiovascular cohorts found that it supplies only a general registry framework and lacks the formal semantic relationships needed to align variables across studies."
- **Reason review is needed:** `contradicted_without_caveat`; competing characterisations of ISO/IEC 11179.
- **Relevant citations:** Stotl2025, Gilani2025 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Affects FAIR-standard efficacy claims.
- **Suggested expertise:** Data standards / metadata registries · **Status:** pending · **Decision:** _—_

### SR-14
- **Claim ID:** `clm_1f133f8e6d25898a` · **Section:** FAIR data
- **Claim text:** "Mapping to the OMOP common data model repeatedly loses domain content: standard OMOP vocabularies could directly represent only a quarter (19 of 75) of core extracorporeal-life-support concepts … deep phenotyping … mapped only 13,485 of 33,347 extracted phenotypes…"
- **Reason review is needed:** `contradicted_without_caveat`; scope status `major_difference_qualified` — multiple quantitative claims across differing domains combined.
- **Relevant citations:** Rieder2026, Nada2026, Bataille2026 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Quantitative interoperability-loss figures across three unrelated domains.
- **Suggested expertise:** Health-data interoperability / OMOP · **Status:** pending · **Decision:** _—_

### SR-15
- **Claim ID:** `clm_2a4ef9802efaaadf` · **Section:** Conclusion
- **Claim text:** "Even where the animal data are not in dispute, a defensible change in analysis can flip a model from mimicking human disease to failing to, so that translatability is decided by analytic choices as much as by biology."
- **Reason review is needed:** `contradicted_without_caveat`; conclusion-level restatement of the Seok/Takao dispute (SR-10).
- **Relevant citations:** Seok2013, Takao2014 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Conclusion overreads a single contested example as general.
- **Suggested expertise:** Translational modelling · **Status:** pending · **Decision:** _—_

### SR-16
- **Claim ID:** `clm_7d8ace4de74bf436` · **Section:** Conclusion
- **Claim text:** "The data that would let this record be checked or reused are largely absent — only about half of animal experiments are ever published, and only around 2% of medical papers actually share their data against the roughly 8% that declare they do."
- **Reason review is needed:** `contradicted_without_caveat`; combines the contested "half unpublished" (SR-09) and ~2% anchor (SR-02) into a conclusion headline.
- **Relevant citations:** terRiet2012, Hamilton2023 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Two of the review's most-quoted numbers in one sentence.
- **Suggested expertise:** Meta-research / open data · **Status:** pending · **Decision:** _—_

### SR-17
- **Claim ID:** `clm_c7727fa80e3c709d` · **Section:** Conclusion
- **Claim text:** "Unusable data are therefore not a downstream inconvenience but a driver of new animal use, and the loop tightens itself: the same reward structure that discourages complete reporting also produces the underpowered, unblinded studies whose results will not replicate…"
- **Reason review is needed:** `contradicted_without_caveat`; a causal "loop" synthesis asserted across contested links.
- **Relevant citations:** Smaldino2016, Freedman2015 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** The review's central causal mechanism; strong causal wording on associational evidence.
- **Suggested expertise:** Meta-research / incentives modelling · **Status:** pending · **Decision:** _—_

### SR-18
- **Claim ID:** `clm_af562e6a471544c0` · **Section:** Conclusion
- **Claim text:** "The reuse of control data is itself double-edged … the same historical database can be marshalled to dismiss a marginal tumour finding as within the historical range or to support it as exceeding that range…"
- **Reason review is needed:** `contradicted_without_caveat`; presents reuse as double-edged citing opposing uses.
- **Relevant citations:** Panzacchi2025, Aguilar2017 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Balances the VCG argument; needs the caveat to be fair.
- **Suggested expertise:** Toxicologic pathology / historical controls · **Status:** pending · **Decision:** _—_

### SR-19
- **Claim ID:** `clm_6ee3813927980898` · **Section:** Conclusion
- **Claim text:** "A minority position holds the crisis narrative is itself overstated and better described as methodological empowerment, and although the balance of evidence weighs against it, the dispute is genuinely open…"
- **Reason review is needed:** `contradicted_without_caveat`; explicitly a live dispute — needs human framing of "balance of evidence weighs against it".
- **Relevant citations:** Fanelli2018, Sena2010 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Adjudicates a genuine open dispute about the reproducibility crisis itself.
- **Suggested expertise:** Meta-research · **Status:** pending · **Decision:** _—_

### SR-20
- **Claim ID:** `clm_02788bd6c8ff7b9b` · **Section:** Conclusion
- **Claim text:** "Because the same phenomenon yields very different values by method, we have preferred juxtaposition of divergent estimates to single anchors, and the review's own quantitative claims inherit that method-dependence."
- **Reason review is needed:** `contradicted_without_caveat`; a methodological self-caveat that should be verified as honestly reflecting the evidence spread.
- **Relevant citations:** terRiet2012, Deutsch2021 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Governs how all the review's numbers should be read.
- **Suggested expertise:** Meta-research / statistics · **Status:** pending · **Decision:** _—_

---

## Group 4 — Independence or replication concern

### SR-21
- **Claim ID:** `clm_069ca2d64382d8ed` · **Section:** Governance
- **Claim text:** "Non-publication remains the root waste: laboratory-animal researchers themselves estimate only about half of animal experiments are ever published."
- **Reason review is needed:** `contradicted_without_caveat`; the "about half unpublished" estimate recurs across sections but appears to rest largely on a single source (terRiet2012) — an independence/replication concern about a load-bearing statistic.
- **Relevant citations:** terRiet2012 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** A single-source estimate is presented as an established fact in multiple places.
- **Suggested expertise:** Publication bias / evidence synthesis · **Status:** pending · **Decision:** _—_

---

## Group 5 — Statistical or methodological concern

### SR-22
- **Claim ID:** `clm_671d5d4b89026361` · **Section:** Incentives
- **Claim text:** "An incentivised psychology survey concluded that some practices are so widely admitted that they may constitute the prevailing research norm, whereas the larger cross-national study argued that widespread one-time involvement does not amount to systematic use once the frequency … is measured."
- **Reason review is needed:** `contradicted_without_caveat`; the QRP-prevalence dispute turns on statistical definition (any-use vs frequency).
- **Relevant citations:** John2012, Schneider2024 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Mischaracterising QRP prevalence overstates the incentives problem.
- **Suggested expertise:** Metascience / survey statistics · **Status:** pending · **Decision:** _—_

### SR-23
- **Claim ID:** `clm_29526c0ca0ee6943` · **Section:** Incentives
- **Claim text:** "Text-mining across disciplines concluded that p-hacking, though common, only weakly perturbs meta-analytic consensus … whereas the theoretical framework that most published research findings are false holds that bias and flexibility make it more likely than not that a given claim is untrue."
- **Reason review is needed:** `contradicted_without_caveat`; directly opposing statistical conclusions on the impact of p-hacking.
- **Relevant citations:** Head2015, Ioannidis2005b · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** The two cited positions disagree on whether p-hacking materially distorts consensus.
- **Suggested expertise:** Statistics / metascience · **Status:** pending · **Decision:** _—_

### SR-24
- **Claim ID:** `clm_31c2d4e620cc2599` · **Section:** Conclusion
- **Claim text:** "…it is unproven that evaluation reform changes behaviour rather than metrics: the reform manifesto and the natural-selection model make opposite predictions, and a scoping review found that of more than a hundred studies of reproducibility interventions only a handful measured reproducibility itself rather than a presumed proxy."
- **Reason review is needed:** `contradicted_without_caveat`; a methodological claim about proxy-vs-outcome measurement plus two opposing models.
- **Relevant citations:** Munafo2017, Smaldino2016, Dudda2025 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** "Most consequential" limitation per the text; governs the governance recommendations.
- **Suggested expertise:** Metascience / intervention evaluation · **Status:** pending · **Decision:** _—_

---

## Group 6 — Wording overstatement

The 18 `SHOULD_CAVEAT` amendments deferred to Phase 10 (`provenance/phase10_caveats.json`)
are wording-overstatement items — e.g. item 1 conflates a 26% experiment-feasibility
rate with the 25%/11% replication rates in the same "echo" claim. They are tracked for
application by backlog item **ED-A02**. Each should be applied verbatim from its
`suggested_fix` only when it needs no new data; otherwise promote it to a numbered
`SR-` entry here. Do not delete a caveat without recording a decision.

- **Status:** pending (batch, via ED-A02) · **Suggested expertise:** subject-matter reviewer per section

---

## Group 7 — Ethical or governance interpretation requiring judgment

### SR-25
- **Claim ID:** `clm_586438c37d91b132` · **Section:** Governance
- **Claim text:** "An observational study of a checklist that Nature journals instead mandated at revision found that the proportion of in vivo papers meeting all four \"Landis\" bias-reduction criteria rose from 0% to 16.4%, with no change in matched control journals."
- **Reason review is needed:** `contradicted_without_caveat`; a governance-efficacy result whose interpretation (mandate-at-revision works) is contested by other checklist studies.
- **Relevant citations:** Macleod2019b · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Directly supports the "enforcement over endorsement" governance recommendation.
- **Suggested expertise:** Research-policy / reporting-guideline evaluation · **Status:** pending · **Decision:** _—_

### SR-26
- **Claim ID:** `clm_dfb950c9a12a6250` · **Section:** Governance
- **Claim text:** "A randomised trial requesting ARRIVE-checklist completion at submission found that no manuscript in either group achieved full compliance, whereas an observational study of a checklist mandated at the revision stage found that reporting of bias-reduction items improved to a level \"not previously observed\"."
- **Reason review is needed:** `contradicted_without_caveat`; RCT (null) vs observational (positive) on guideline efficacy — an evidence-hierarchy interpretation call.
- **Relevant citations:** Hair2019, Macleod2019b · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Whether guidelines "work" depends on which design is privileged.
- **Suggested expertise:** Evidence-based research / trial methodology · **Status:** pending · **Decision:** _—_

### SR-27
- **Claim ID:** `clm_8ba24a34a7ca163d` · **Section:** Governance
- **Claim text:** "Publishing and endorsing ARRIVE produced no significant reporting gain in the Chagas literature (51% → 66%, p=0.26), while implementing a checklist at one journal produced a three-fold-greater improvement than at a matched journal without one."
- **Reason review is needed:** `contradicted_without_caveat`; non-significant vs significant results juxtaposed to argue enforcement matters.
- **Relevant citations:** Gulin2015, Han2017 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** p=0.26 result should not be read as evidence of no effect without care.
- **Suggested expertise:** Biostatistics / reporting guidelines · **Status:** pending · **Decision:** _—_

### SR-28
- **Claim ID:** `clm_fec85973228eb1e5` · **Section:** Governance
- **Claim text:** "One proposal presumes review bodies can and should assess research rigor and expected benefit through a structured benefit-assessment instrument, while an analysis of US committees argues they structurally lack the expertise and mandate to judge scientific merit, so their approval carries no such warranty."
- **Reason review is needed:** `contradicted_without_caveat`; a governance-interpretation dispute about what ethics-review bodies (IACUCs) can legitimately assess.
- **Relevant citations:** Bespalov2026, Pippin2025 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** Bears on the review's governance recommendations and their feasibility.
- **Suggested expertise:** Research ethics / animal-research governance · **Status:** pending · **Decision:** _—_

### SR-29
- **Claim ID:** `clm_f3e0e2ed9f6176e2` · **Section:** Governance
- **Claim text:** "First, enforcement over endorsement: guidelines must be gated at revision and checked, because passively published standards demonstrably do not move behaviour."
- **Reason review is needed:** `contradicted_without_caveat`; the review's headline governance prescription, stated as demonstrated ("demonstrably") on contested evidence (SR-25–SR-27).
- **Relevant citations:** Macleod2019b, Han2017, Kidwell2016, IvimeyCook2025 · **Relation:** conflicted · **TRUST:** low_trust 60, cap `contradicted_without_caveat`
- **Consequence if incorrect:** The strongest normative recommendation in the review; "demonstrably" may overstate the evidence.
- **Suggested expertise:** Research-policy / meta-research · **Status:** pending · **Decision:** _—_

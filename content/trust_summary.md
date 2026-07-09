(sec-trust-summary)=
# Citation Trust Summary

Every cited claim in this review carries a **citation TRUST score**: a 0–100 rating built from five components, each scored 0–4 — **Traceability** (does the claim resolve to a citation, DOI, and a verbatim supporting passage?), **Robustness** (independent sources, replication, convergent design), **Uncertainty calibration** (does the wording hedge conflict and limits appropriately?), **Source integrity** (verified, bibliographically consistent, primary rather than secondary), and **Transferability / scope control** (does the claim stay within the evidence's scope?). The overall score is `round(100 × sum(components) / 20)`; a mandatory rule caps it at 60 when a claim rests on an unsupported or contradicted citation or overextends its scope. Components computable from the review's own verification records were scored deterministically; the wording-and-scope components were assessed per claim. Bands: **85–100 high · 70–84 moderate · 50–69 low · <50 critical**.

Across **510** cited claims the mean overall score is **89.1**. Band distribution: 🟢 high 428, 🔵 moderate 67, 🟠 low 15, 🔴 critical 0. **13** claim(s) hit the cap-at-60 rule; **99** flagged for human review.

![Trust band distribution by section](../figures/fig_trust_by_section.png)

![Mean TRUST component score by section](../figures/fig_trust_components.png)

![Overall trust band split and score distribution](../figures/fig_trust_overall.png)

## Component means (0–4)

| Traceability | Robustness | Uncertainty calibration | Source integrity | Transferability / scope |
|---|---|---|---|---|
| 3.99 | 2.93 | 3.47 | 3.93 | 3.58 |

## Per-section rollup

| Section | Claims | Mean score | 🟢 high | 🔵 moderate | 🟠 low | 🔴 critical |
|---|--:|--:|--:|--:|--:|--:|
| Introduction | 40 | 86 | 31 | 5 | 4 | 0 |
| Reproducibility | 64 | 87 | 47 | 15 | 2 | 0 |
| Data welfare / 3Rs | 63 | 90 | 54 | 9 | 0 | 0 |
| FAIR data | 59 | 88 | 48 | 8 | 3 | 0 |
| Virtual controls | 71 | 92 | 64 | 6 | 1 | 0 |
| NAMs | 52 | 89 | 46 | 6 | 0 | 0 |
| Incentives | 57 | 92 | 49 | 7 | 1 | 0 |
| Governance | 66 | 88 | 57 | 6 | 3 | 0 |
| Conclusion | 38 | 89 | 32 | 5 | 1 | 0 |

## Lowest-trust claims (review priority)

| Score | Band | Section | Claim | Flag |
|--:|---|---|---|---|
| 60 | 🟠 | Introduction | The empirical anchor the review returns to most often — that actual, usable data availability sits near two percent while declared availabil | overextended_scope |
| 60 | 🟠 | Introduction | The strongest version of that claim is also its simplest, and it is the thread that ties the sections together: because animals have already | overextended_scope |
| 60 | 🟠 | Reproducibility | Their value is not their precision but their convergence with a theoretical prior — that under realistic assumptions about power, bias, and  | contradicted_without_caveat |
| 60 | 🟠 | Reproducibility | The traditional prescription is rigorous standardisation — minimising genetic and environmental variation so that fewer animals are needed t | unsupported_citation |
| 60 | 🟠 | FAIR data | Under the NIH Data Management and Sharing Policy, 79.3% of submitted plans addressed all six required elements, and structured templates out | overextended_scope |
| 60 | 🟠 | FAIR data | Mapping to the OMOP common data model repeatedly loses domain content: standard OMOP vocabularies could directly represent only a quarter (1 | contradicted_without_caveat |
| 60 | 🟠 | FAIR data | Dedicated model-organism infrastructures show what good stewardship looks like — the Rat Genome Database curates multi-species genomic and p | direction_mismatch |
| 60 | 🟠 | Virtual controls | The parallel to preclinical VCGs is exact: the hybrid design that retained half the real controls outperformed the full-replacement design f | contradicted_without_caveat |
| 60 | 🟠 | Incentives | The pattern generalises across national systems — in Ecuador, reliance on journal-centric metrics predicted lower adoption of open practices | overextended_scope |
| 60 | 🟠 | Governance | In animal work the picture repeats: orthodontic studies scored a mean of 57.9 on ARRIVE years after its release; ARRIVE 2.0 audits of Parkin | contradicted_without_caveat |
| 60 | 🟠 | Governance | Non-publication remains the root waste: laboratory-animal researchers themselves estimate only about half of animal experiments are ever pub | contradicted_without_caveat |
| 60 | 🟠 | Governance | First, enforcement over endorsement: guidelines must be gated at revision and checked, because passively published standards demonstrably do | contradicted_without_caveat |
| 60 | 🟠 | Conclusion | The data that would let this record be checked or reused are largely absent — only about half of animal experiments are ever published, and  | contradicted_without_caveat |
| 65 | 🟠 | Introduction | The reframe is reinforced, not undercut, by evidence that welfare-improving practices tend to improve data quality rather than degrade it. | review |
| 65 | 🟠 | Introduction | Preclinical animal data, reagent-dependent, heterogeneous, and often trapped as unpublished "dark data," are served worst of all. |  |
| 70 | 🔵 | Introduction | The studies themselves are chronically underpowered, which both exaggerates the effects that reach significance and lowers the chance that a | review |
| 70 | 🔵 | Reproducibility | Opinion surveys of laboratory-animal researchers put the published fraction low: staff at not-for-profit institutes estimated that only half | review |
| 70 | 🔵 | Reproducibility | Whichever estimate is correct, the consequence is a literature in which protocols, full reports, and datasets are available for only about h | review |
| 70 | 🔵 | NAMs | On this reading, next-generation risk assessment using non-animal methods is, in defined settings, entirely appropriate today for assuring c |  |
| 70 | 🔵 | NAMs | A drug-development perspective frames microphysiological systems as delivering more standardised, predictive, physiologically relevant respo |  |
| 75 | 🔵 | Introduction | Meanwhile the modal outcome of a research life — death — is largely omitted from the welfarist accounting that underpins the governing frame |  |
| 75 | 🔵 | Introduction | That style is not neutrality for its own sake but a hedge against the false consensus a single, confidently repeated number can manufacture. | review |
| 75 | 🔵 | Data welfare / 3Rs | Their founding synthesis was a work of humane *technique*, and historians argue it has remained oddly little-read precisely because it strad | review |
| 75 | 🔵 | Data welfare / 3Rs | A subtler foundational gap runs through the whole edifice: the 3Rs rest on a welfarist premise, inherited from their intellectual patrons, t |  |
| 75 | 🔵 | Data welfare / 3Rs | Structural critiques argue oversight bodies lack the expertise and mandate to judge scientific merit at all, so their approval should not be | review |

## Capped claims (score limited to ≤60)

| Score | Section | Cap reason | Claim |
|--:|---|---|---|
| 60 | Introduction | overextended_scope | The empirical anchor the review returns to most often — that actual, usable data availability sits near two percent while declared availability and pa |
| 60 | Introduction | overextended_scope | The strongest version of that claim is also its simplest, and it is the thread that ties the sections together: because animals have already paid for  |
| 60 | Reproducibility | contradicted_without_caveat | Their value is not their precision but their convergence with a theoretical prior — that under realistic assumptions about power, bias, and pre-study  |
| 60 | Reproducibility | unsupported_citation | The traditional prescription is rigorous standardisation — minimising genetic and environmental variation so that fewer animals are needed to detect a |
| 60 | FAIR data | overextended_scope | Under the NIH Data Management and Sharing Policy, 79.3% of submitted plans addressed all six required elements, and structured templates outperformed  |
| 60 | FAIR data | contradicted_without_caveat | Mapping to the OMOP common data model repeatedly loses domain content: standard OMOP vocabularies could directly represent only a quarter (19 of 75) o |
| 60 | FAIR data | direction_mismatch | Dedicated model-organism infrastructures show what good stewardship looks like — the Rat Genome Database curates multi-species genomic and phenotype d |
| 60 | Virtual controls | contradicted_without_caveat | The parallel to preclinical VCGs is exact: the hybrid design that retained half the real controls outperformed the full-replacement design for the sam |
| 60 | Incentives | overextended_scope | The pattern generalises across national systems — in Ecuador, reliance on journal-centric metrics predicted lower adoption of open practices while ins |
| 60 | Governance | contradicted_without_caveat | In animal work the picture repeats: orthodontic studies scored a mean of 57.9 on ARRIVE years after its release; ARRIVE 2.0 audits of Parkinson's and  |
| 60 | Governance | contradicted_without_caveat | Non-publication remains the root waste: laboratory-animal researchers themselves estimate only about half of animal experiments are ever published. |
| 60 | Governance | contradicted_without_caveat | First, enforcement over endorsement: guidelines must be gated at revision and checked, because passively published standards demonstrably do not move  |
| 60 | Conclusion | contradicted_without_caveat | The data that would let this record be checked or reused are largely absent — only about half of animal experiments are ever published, and only aroun |

## Method and limitations

Traceability, Robustness, and the verification half of Source integrity were computed deterministically from the review's citation-key map, CrossRef re-resolution, replication annotations, and the verbatim supporting passages captured at evidence extraction. Uncertainty calibration, Transferability / scope, and the primary-versus-secondary judgement were assessed per claim against each claim's supporting passages and study scope, seeded by the review's own section-critic findings. Two limitations are documented: retraction status is not checked (assumed clean); and a claim is joined to its supporting passage by citation key, so a passage reflects the cited paper rather than a guaranteed sentence-level match. The full per-claim record — every component score, rationale, and recommended fix — is in `knowledge/claim_graph.json`.

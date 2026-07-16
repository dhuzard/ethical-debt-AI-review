(sec-introduction)=
# Introduction: The Ethical Debt of Preclinical Research

Every animal used in biomedical research is spent on a single promise: that the knowledge obtained will be worth what the animal's welfare cost to produce it. That promise is the moral foundation of the entire enterprise. Society tolerates the deliberate infliction of harm on sentient animals only because the resulting knowledge is expected to be reliable, non-redundant, and available to inform the next experiment and, eventually, the clinic. When that expectation is met, the ledger balances: harm was done, but knowledge was banked and put to use. This review is about what happens when it is not. A retrospective harm–benefit analysis of preclinical research found that, weighing the animals' actual harms against the actual clinical benefit their studies produced, fewer than 7% of the studies examined would have been ethically permissible, and that 97% did not even report whether the animals received analgesia. {cite:p}`Pound2018` The reproducibility literature independently prices the reliability side of the same failure: a probability-bounds economic model puts the cumulative preclinical irreproducibility rate above half and attaches a modelled cost of tens of billions of dollars a year to it in the United States alone, {cite:p}`Freedman2015` a figure that sits within broader accountings of avoidable research waste that reach a widely repeated — and, we will argue, over-cited — estimate that most biomedical research investment is squandered, {cite:p}`Chalmers2014, Ioannidis2014c` and that is consistent with a theoretical prior holding that, under realistic assumptions about power and bias, most published research claims are more likely false than true. {cite:p}`Ioannidis2005b` Read together, these findings describe a debt: the welfare cost of an experiment is incurred the moment the animal is used, but the knowledge that was supposed to redeem it is frequently never delivered.

:::{trust-claim}
:claim-id: clm_c2d644434ce16083
:claim: A retrospective harm–benefit analysis of preclinical research found that, weighing the animals' actual harms against the actual clinical benefit their studies produced, fewer than 7% of the studies examined would have been ethically permissible, and that 97% did not even report whether the animals received analgesia.
:cites: Pound2018
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_c5b4d84c46bcacf3
:claim: The reproducibility literature independently prices the reliability side of the same failure: a probability-bounds economic model puts the cumulative preclinical irreproducibility rate above half and attaches a modelled cost of tens of billions of dollars a year to it in the United States alone, a figure that sits within broader accountings of avoidable research waste that reach a widely repeated — and, we will argue, over-cited — estimate that most biomedical research investment is squandered, and that is consistent with a theoretical prior holding that, under realistic assumptions about power and bias, most published research claims are more likely false than true.
:cites: Freedman2015, Chalmers2014, Ioannidis2014c, Ioannidis2005b
:claim-type: review_synthesis
:modality: suggestive
:::

We call this the Ethical Debt of preclinical research. The metaphor is deliberate, and it is meant literally in its consequences. A debt is incurred whenever animals are used to generate data but those data are then allowed to become unfindable, unusable, or unreused; and because the only currency in which such a debt can be repaid is more knowledge, an unpaid debt is discharged not in money but in further animal lives, as equivalent experiments are run again to regenerate what was lost. This is not a rhetorical flourish laid over an ordinary data-management problem, because the loss is measurable at every stage. Whole experiments vanish before publication: surveys of laboratory-animal researchers estimate that only about half of conducted experiments are ever published, {cite:p}`terRiet2012` empirical protocol-to-publication tracking finds a more optimistic but still incomplete rate near 70%, {cite:p}`Deutsch2021` and across a set of novel drugs the majority of accessible animal efficacy studies appeared only after the first human trial, with a substantial fraction of drugs having no efficacy study published beforehand at all. {cite:p}`Federico2014` What survives to publication is heavily filtered toward positive results, {cite:p}`Sena2010` and what is published is rarely accompanied by usable data: a meta-analysis pooling more than two million articles found that only about 2% of medical papers actually shared their data, against roughly 8% that declared they had. {cite:p}`Hamilton2023` Even reconstructing what was done can prove impossible — an attempt to repeat cancer-biology experiments could obtain the data needed to compute the original effect sizes for only a handful of nearly two hundred experiments. {cite:p}`Errington2021a` Every one of these losses converts a paid welfare cost into waste.

:::{trust-claim}
:claim-id: clm_08356a318e2577ab
:claim: Whole experiments vanish before publication: surveys of laboratory-animal researchers estimate that only about half of conducted experiments are ever published, empirical protocol-to-publication tracking finds a more optimistic but still incomplete rate near 70%, and across a set of novel drugs the majority of accessible animal efficacy studies appeared only after the first human trial, with a substantial fraction of drugs having no efficacy study published beforehand at all.
:cites: terRiet2012, Deutsch2021, Federico2014
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_f1e9eeece085dece
:claim: What survives to publication is heavily filtered toward positive results, and what is published is rarely accompanied by usable data: a meta-analysis pooling more than two million articles found that only about 2% of medical papers actually shared their data, against roughly 8% that declared they had.
:cites: Sena2010, Hamilton2023
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_7291d97b39feeaab
:claim: Even reconstructing what was done can prove impossible — an attempt to repeat cancer-biology experiments could obtain the data needed to compute the original effect sizes for only a handful of nearly two hundred experiments.
:cites: Errington2021a
:claim-type: empirical
:modality: likely
:::

The empirical foundation for the debt is the reproducibility and translation crisis, which {ref}`sec-repro-crisis` examines in detail. The published animal record is not a neutral archive of what experiments found but a filtered, distorted, and frequently untranslatable sample of them: across thousands of datasets, the number of "positive" studies vastly exceeds what their statistical power should produce, and only a small minority of meta-analyses are free of any small-study or excess-significance signal. {cite:p}`Sena2010, Tsilidis2013` Internal-validity failures and publication bias each independently inflate apparent efficacy, so the published effect is systematically overstated. {cite:p}`Freedman2015, vanderWorp2010` The studies themselves are chronically underpowered, which both exaggerates the effects that reach significance and lowers the chance that a positive result is true. {cite:p}`Button2013` Animal findings then translate to humans poorly and unpredictably: a direct six-intervention comparison showed benefit in animal head-injury models that evaporated in patients, {cite:p}`Perel2006` a scoping review found published translational success spanning the entire range from none to complete, {cite:p}`Leenaars2019b` and independent analyses converge on a likelihood of moving from first-in-human testing to approval of only roughly 5–14%. {cite:p}`Schuhmacher2025, Dhillon2022` Seok et al. reported near-random mouse–human agreement among genes significantly changed in human inflammatory conditions (R² 0.0–0.1). {cite:p}`Seok2013` However, Takao and Miyakawa reanalysed the same datasets using genes significantly changed in both species and reported Spearman correlations of 0.43–0.68 with 77–93% directional agreement. {cite:p}`Takao2014` That contrast is a warning that runs through this review — the value that can be extracted from animal data depends on how those data are handled after the animal has already paid, which is precisely the domain in which the debt is incurred or repaid.

:::{trust-claim}
:claim-id: clm_e60e847a321ec50b
:claim: The published animal record is not a neutral archive of what experiments found but a filtered, distorted, and frequently untranslatable sample of them: across thousands of datasets, the number of "positive" studies vastly exceeds what their statistical power should produce, and only a small minority of meta-analyses are free of any small-study or excess-significance signal.
:cites: Sena2010, Tsilidis2013
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_b90dc9d6f8af63fb
:claim: Internal-validity failures and publication bias each independently inflate apparent efficacy, so the published effect is systematically overstated.
:cites: Freedman2015, vanderWorp2010
:claim-type: causal
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_8f148eff4ab81212
:claim: The studies themselves are chronically underpowered, which both exaggerates the effects that reach significance and lowers the chance that a positive result is true.
:cites: Button2013
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_169618b8b266cd6b
:claim: Animal findings then translate to humans poorly and unpredictably: a direct six-intervention comparison showed benefit in animal head-injury models that evaporated in patients, a scoping review found published translational success spanning the entire range from none to complete, and independent analyses converge on a likelihood of moving from first-in-human testing to approval of only roughly 5–14%.
:cites: Perel2006, Leenaars2019b, Schuhmacher2025, Dhillon2022
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_9f30c76025c6c2f1
:claim: Seok et al. reported near-random mouse–human agreement among genes significantly changed in human inflammatory conditions (R2 0.0–0.1).
:cites: Seok2013
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_a7c87272d164e6f1
:claim: However, Takao and Miyakawa reanalysed the same datasets using genes significantly changed in both species and reported Spearman correlations of 0.43–0.68 with 77–93% directional agreement.
:cites: Takao2014
:claim-type: empirical
:modality: contested
:::

The near-universal framing of this evidence is as a scientific-quality problem: wasted money, and papers that fail to replicate. What that framing omits is that every biased, underpowered, unpublished, or non-translating study was nonetheless paid for in animal lives, whose welfare cost is discharged whether or not the resulting data are ever trusted or reused. The system is not even structured to notice: audits of ethical-review decisions find the legally required harm–benefit weighing frequently absent or confused, and measures against bias described at very low rates, so the authorising body cannot see the scientific validity on which its own justification depends. {cite:p}`Vogt2016, Jorgensen2021` Meanwhile the modal outcome of a research life — death — is largely omitted from the welfarist accounting that underpins the governing framework, so the animals bred to regenerate lost data are disproportionately animals killed without ever entering an analysis. {cite:p}`Persson2024` The 3Rs already require that studies use no more animals than the knowledge requires and report enough for that knowledge to be trusted, and audits show both requirements are met only in a small minority of studies. {cite:p}`Bara2014, Pound2018` The compact is moreover not only with the animal but with the public that funds and permits the research: openness is increasingly framed as the price of that permission, yet the single most common barrier to communicating about animal research is that the research harms animals — a barrier that unusable results only raise, because they convert a defensible harm into an indefensible one. {cite:p}`MacArthurClark2019, Loser2026` The reframing this review pursues is therefore not an expansion of the animals' moral claims but an insistence that the existing claims be honoured all the way through to the data.

:::{trust-claim}
:claim-id: clm_d2f000d937987a87
:claim: The system is not even structured to notice: audits of ethical-review decisions find the legally required harm–benefit weighing frequently absent or confused, and measures against bias described at very low rates, so the authorising body cannot see the scientific validity on which its own justification depends.
:cites: Vogt2016, Jorgensen2021
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_dc95f68b3a930955
:claim: Meanwhile the modal outcome of a research life — death — is largely omitted from the welfarist accounting that underpins the governing framework, so the animals bred to regenerate lost data are disproportionately animals killed without ever entering an analysis.
:cites: Persson2024
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_af247dfcbbd8cc84
:claim: The 3Rs already require that studies use no more animals than the knowledge requires and report enough for that knowledge to be trusted, and audits show both requirements are met only in a small minority of studies.
:cites: Bara2014, Pound2018
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_e12698fe64e1ad65
:claim: The compact is moreover not only with the animal but with the public that funds and permits the research: openness is increasingly framed as the price of that permission, yet the single most common barrier to communicating about animal research is that the research harms animals — a barrier that unusable results only raise, because they convert a defensible harm into an indefensible one.
:cites: MacArthurClark2019, Loser2026
:claim-type: empirical
:modality: likely
:::

The conceptual move at the heart of the review is to fold data stewardship into that existing framework rather than leave it as a technical afterthought, the argument developed in. {ref}`sec-data-welfare` Strech and Dirnagl argued that the traditional welfare-focused 3Rs should be complemented by robustness, registration, and reporting as explicit scientific-value principles. {cite:p}`Strech2019` Brink and Lewis proposed a 12Rs framework spanning animal welfare, social values, and scientific integrity. {cite:p}`Brink2023` DeGrazia and Beauchamp proposed six principles of social benefit and animal welfare, arguing that their framework is more comprehensive than the canonical 3Rs. {cite:p}`DeGrazia2019` However, Vitale and Ricceri described the 3Rs as the methodological and ethical backbone of animal research and argued that difficulties applying all three do not make the principle obsolete or ineffective. {cite:p}`Vitale2022` This review adopts and sharpens the expansion under the term *data welfare*: the claim that letting animal-derived data become unfindable, unusable, or unreused is itself a welfare harm, because it wastes the welfare cost that produced the data. The link is not metaphorical but mechanical. Reduction was never a demand to use the fewest animals but to use no more than the knowledge requires, so a dataset that cannot be reused is knowledge that must be regenerated, and knowledge regenerated from live animals is animals used — the same logic that already lets the reuse of historical control data count as Reduction. {cite:p}`Kramer2015, Verderio2023` That the field itself deprioritises this data-facing R is part of the problem: surveys find researchers invert the original ordering, treating Refinement as the higher priority and Replacement as barely possible, so Reduction sits neglected in the middle. {cite:p}`Franco2018, LouisMaerten2024` The reframe is reinforced, not undercut, by evidence that welfare-improving practices tend to improve data quality rather than degrade it. {cite:p}`Cait2022`

:::{trust-claim}
:claim-id: clm_2166f4a156ee26d0
:claim: Strech and Dirnagl argued that the traditional welfare-focused 3Rs should be complemented by robustness, registration, and reporting as explicit scientific-value principles.
:cites: Strech2019
:claim-type: methodological
:modality: established
:::

:::{trust-claim}
:claim-id: clm_f754fbc3935f5cda
:claim: Brink and Lewis proposed a 12Rs framework spanning animal welfare, social values, and scientific integrity.
:cites: Brink2023
:claim-type: methodological
:modality: established
:::

:::{trust-claim}
:claim-id: clm_9fffa0247a80ac54
:claim: DeGrazia and Beauchamp proposed six principles of social benefit and animal welfare, arguing that their framework is more comprehensive than the canonical 3Rs.
:cites: DeGrazia2019
:claim-type: methodological
:modality: established
:::

:::{trust-claim}
:claim-id: clm_2d554ac4d182ba9a
:claim: However, Vitale and Ricceri described the 3Rs as the methodological and ethical backbone of animal research and argued that difficulties applying all three do not make the principle obsolete or ineffective.
:cites: Vitale2022
:claim-type: methodological
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_9258126587247356
:claim: Reduction was never a demand to use the fewest animals but to use no more than the knowledge requires, so a dataset that cannot be reused is knowledge that must be regenerated, and knowledge regenerated from live animals is animals used — the same logic that already lets the reuse of historical control data count as Reduction.
:cites: Kramer2015, Verderio2023
:claim-type: definition
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_a71241222761827e
:claim: That the field itself deprioritises this data-facing R is part of the problem: surveys find researchers invert the original ordering, treating Refinement as the higher priority and Replacement as barely possible, so Reduction sits neglected in the middle.
:cites: Franco2018, LouisMaerten2024
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e35ad7760dd6f655
:claim: The reframe is reinforced, not undercut, by evidence that welfare-improving practices tend to improve data quality rather than degrade it.
:cites: Cait2022
:claim-type: causal
:modality: suggestive
:::

If data welfare defines the obligation, the rest of the review asks how the debt can be repaid, and it identifies four repayment mechanisms whose promise is real but whose delivery is conditional. The first is FAIR data — data that are Findable, Accessible, Interoperable, and Reusable — the near-universal standard for good stewardship and the subject of. {ref}`sec-fair-preclinical` {cite:p}`Wilkinson2016` The evidence there is sobering. Declared availability vastly exceeds actual availability; formal compliance with data-management mandates coexists with near-total non-sharing in practice, with the great majority of mandated projects sharing nothing usable; and even authors who explicitly promise to share overwhelmingly do not when asked. {cite:p}`Hamilton2023, VanTuyl2016, Gabelica2022` Review-level syntheses treat FAIR as a demonstrated remedy while direct retrieval audits find most shared data incomplete or unusable, and scoring of the data that are shared returns low reusability sub-scores even in unrelated domains. {cite:p}`Inau2023, Uribe2022` Where reuse does happen, it is almost always because a specific repository imposes and checks a community standard rather than because the principles were published — a single enforced neuroimaging archive documents more realized reuse than the diffuse ecosystem around it. {cite:p}`Markiewicz2021, Hamilton2022` Preclinical animal data, reagent-dependent, heterogeneous, and often trapped as unpublished "dark data," are served worst of all. {cite:p}`Hawkins2020` Generic sharing of everything, in short, repays the debt only weakly, which motivates a change of tack rather than an abandonment of the principle.

:::{trust-claim}
:claim-id: clm_5aaea8da42c47adb
:claim: The first is FAIR data — data that are Findable, Accessible, Interoperable, and Reusable — the near-universal standard for good stewardship and the subject of.
:cites: Wilkinson2016
:claim-type: definition
:modality: established
:::

:::{trust-claim}
:claim-id: clm_91c780ade8959f91
:claim: Declared availability vastly exceeds actual availability; formal compliance with data-management mandates coexists with near-total non-sharing in practice, with the great majority of mandated projects sharing nothing usable; and even authors who explicitly promise to share overwhelmingly do not when asked.
:cites: Hamilton2023, VanTuyl2016, Gabelica2022
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_816e971fa896eb67
:claim: Review-level syntheses treat FAIR as a demonstrated remedy while direct retrieval audits find most shared data incomplete or unusable, and scoring of the data that are shared returns low reusability sub-scores even in unrelated domains.
:cites: Inau2023, Uribe2022
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e6b8684be7254f05
:claim: Where reuse does happen, it is almost always because a specific repository imposes and checks a community standard rather than because the principles were published — a single enforced neuroimaging archive documents more realized reuse than the diffuse ecosystem around it.
:cites: Markiewicz2021, Hamilton2022
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_993c2b7095e544d3
:claim: Preclinical animal data, reagent-dependent, heterogeneous, and often trapped as unpublished "dark data," are served worst of all.
:cites: Hawkins2020
:claim-type: comparative
:modality: suggestive
:::

The second mechanism, examined in, {ref}`sec-virtual-controls` is the specific, high-value form of reuse in which the payoff can be counted directly. When the data being reused is the control arm of a toxicity or carcinogenicity study, a control group reconstructed from curated historical records is a group of animals that never enters the study — Reduction achieved by reuse. The headline estimate is stable across independent proposals at roughly a quarter of control animals saved, {cite:p}`StegerHartmann2020, Gurjanov2024b` the clinical analogue of Bayesian control-borrowing delivers comparable enrolment reductions, {cite:p}`Chiaruttini2025` and the infrastructure — curated databases holding tens of thousands of control animals across decades of studies — already exists at scale, so the bottleneck is acceptance and stewardship rather than data volume. {cite:p}`Moresis2024, Deschl2002` But the dividend is conditional. Concordance between virtual and concurrent controls is endpoint-dependent, with high agreement for categorical decisions such as dose-limiting toxicities {cite:p}`DuchateauNguyen2026, Mecklenburg2023` and substantial non-reproducibility for continuous clinical-pathology parameters; {cite:p}`Adedeji2024` historical data drift over time and across laboratories, with study year emerging as the single most influential covariate in one large multi-company database; {cite:p}`Kellner2025` and, decisively, no regulator has yet accepted a virtual-control-group study in place of a concurrent control for a pivotal preclinical submission. {cite:p}`SATO2024`

:::{trust-claim}
:claim-id: clm_7c1edb545736cc15
:claim: The headline estimate is stable across independent proposals at roughly a quarter of control animals saved, the clinical analogue of Bayesian control-borrowing delivers comparable enrolment reductions, and the infrastructure — curated databases holding tens of thousands of control animals across decades of studies — already exists at scale, so the bottleneck is acceptance and stewardship rather than data volume.
:cites: StegerHartmann2020, Gurjanov2024b, Chiaruttini2025, Moresis2024, Deschl2002
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_34018547e1025a15
:claim: Concordance between virtual and concurrent controls is endpoint-dependent, with high agreement for categorical decisions such as dose-limiting toxicities and substantial non-reproducibility for continuous clinical-pathology parameters; historical data drift over time and across laboratories, with study year emerging as the single most influential covariate in one large multi-company database; and, decisively, no regulator has yet accepted a virtual-control-group study in place of a concurrent control for a pivotal preclinical submission.
:cites: DuchateauNguyen2026, Mecklenburg2023, Adedeji2024, Kellner2025, SATO2024
:claim-type: comparative
:modality: contested
:::

The third mechanism is the complement to reuse — replacing animals altogether with new approach methodologies (NAMs), the subject of. {ref}`sec-nams-data` In silico and QSAR models, organoids, organ-on-chip systems, and high-throughput screening reach usable and sometimes high predictivity for narrow, well-defined endpoints and can displace specific animal tests, {cite:p}`Pfuhler2020, Sirenko2016` a case sharpened by the fact that fewer than a tenth of chemicals in commerce have ever been screened for safety. {cite:p}`Comess2020` But the field's readiness is contested: proponents argue NAMs are already fit to assure chemical safety in defined settings, while regulatory reviews document continued dependence on animal data for the adversity call, and microphysiological systems remain largely unadopted in regulated decision-making. {cite:p}`Carmichael2022, Holmer2025, Marx2020, Hartung2025a` Two deeper difficulties recur. NAM validation is often anchored to concordance with animal data that were themselves never validated for human relevance and are only moderately reproducible, so the yardstick is shaky. {cite:p}`Karmaus2026` And, most important for this review, NAMs do not escape the data problem; they relocate it. High-throughput and in silico streams generate large, heterogeneous datasets that re-create the same stewardship debt unless they are made FAIR from the outset — a point the NAM community has itself begun to press, arguing that findable, comparable data are not best practice but a prerequisite for trustworthy model outputs. {cite:p}`Gant2026, Inau2023`

:::{trust-claim}
:claim-id: clm_a4f388eca4c31057
:claim: In silico and QSAR models, organoids, organ-on-chip systems, and high-throughput screening reach usable and sometimes high predictivity for narrow, well-defined endpoints and can displace specific animal tests, a case sharpened by the fact that fewer than a tenth of chemicals in commerce have ever been screened for safety.
:cites: Pfuhler2020, Sirenko2016, Comess2020
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_fe72265c48d15917
:claim: But the field's readiness is contested: proponents argue NAMs are already fit to assure chemical safety in defined settings, while regulatory reviews document continued dependence on animal data for the adversity call, and microphysiological systems remain largely unadopted in regulated decision-making.
:cites: Carmichael2022, Holmer2025, Marx2020, Hartung2025a
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_c0a2abb5f4dd5265
:claim: NAM validation is often anchored to concordance with animal data that were themselves never validated for human relevance and are only moderately reproducible, so the yardstick is shaky.
:cites: Karmaus2026
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_bc5052fe1cc3f0e4
:claim: High-throughput and in silico streams generate large, heterogeneous datasets that re-create the same stewardship debt unless they are made FAIR from the outset — a point the NAM community has itself begun to press, arguing that findable, comparable data are not best practice but a prerequisite for trustworthy model outputs.
:cites: Gant2026, Inau2023
:claim-type: review_synthesis
:modality: likely
:::

The fourth mechanism is the one that determines whether the other three ever operate: reform of the incentive and governance systems, treated in {ref}`sec-incentives` and. {ref}`sec-governance` The persistence of the data-welfare debt across FAIR data, virtual controls, and NAMs is not a technical accident but the predictable output of a reward structure that pays for publication counts and journal prestige while pricing stewardship at essentially zero — data-sharing appears in almost no promotion and tenure criteria, while peer-reviewed publications appear in nearly all, and researchers accordingly treat their data as a private asset whose release requires an incentive that does not exist. {cite:p}`Rice2020, McKiernan2019, Fecher2015` A structural model argues that as long as publication drives careers, methods that produce more publishable results will keep being selected for regardless of their reliability, against a reform manifesto that expects methods, reporting, and incentive measures to improve reliability if adopted across the system. {cite:p}`Smaldino2016, Munafo2017` The decisive test is the gap between what researchers declare and what they deliver: an editorial data-sharing requirement produced near-universal declarations of willingness but under one percent of trials with data actually available. {cite:p}`Danchev2021` Governance offers the enforced alternative, and here the evidence is clearer: a checklist mandated and checked at revision moved reporting where the same checklist merely requested at submission did not, and open-practice signals that are verified deliver usable data where unenforced mandates do not. {cite:p}`Macleod2019b, Hair2019, Kidwell2016` The recurring lesson is that enforcement beats endorsement, though effects are heterogeneous and field-wide sharing remains near the floor.

:::{trust-claim}
:claim-id: clm_09ef1fa4df987040
:claim: The persistence of the data-welfare debt across FAIR data, virtual controls, and NAMs is not a technical accident but the predictable output of a reward structure that pays for publication counts and journal prestige while pricing stewardship at essentially zero — data-sharing appears in almost no promotion and tenure criteria, while peer-reviewed publications appear in nearly all, and researchers accordingly treat their data as a private asset whose release requires an incentive that does not exist.
:cites: Rice2020, McKiernan2019, Fecher2015
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d9d00fbc0881a6ab
:claim: A structural model argues that as long as publication drives careers, methods that produce more publishable results will keep being selected for regardless of their reliability, against a reform manifesto that expects methods, reporting, and incentive measures to improve reliability if adopted across the system.
:cites: Smaldino2016, Munafo2017
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_e627efda808e9426
:claim: The decisive test is the gap between what researchers declare and what they deliver: an editorial data-sharing requirement produced near-universal declarations of willingness but under one percent of trials with data actually available.
:cites: Danchev2021
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_3ea05f76f598ec8f
:claim: Governance offers the enforced alternative, and here the evidence is clearer: a checklist mandated and checked at revision moved reporting where the same checklist merely requested at submission did not, and open-practice signals that are verified deliver usable data where unenforced mandates do not.
:cites: Macleod2019b, Hair2019, Kidwell2016
:claim-type: causal
:modality: likely
:::

This review is therefore an argument in three movements. It first establishes that the debt is real and measurable and reframes it as a welfare problem rather than merely a scientific-quality one ({ref}`sec-repro-crisis`, {ref}`sec-data-welfare`). It then examines the machinery of repayment and where it breaks — FAIR stewardship that is declared but not delivered, virtual control groups that reduce animal use but await regulatory acceptance, and non-animal methods that displace animals while generating fresh data to steward ({ref}`sec-fair-preclinical`,, {ref}`sec-virtual-controls` {ref}`sec-nams-data`) — before locating the common cause of all three failures in an incentive system that does not value stewardship ({ref}`sec-incentives`). Finally, it turns to what enforced governance can and cannot achieve, and integrates the mechanisms into a single repayment pathway while marking the empirical questions that remain open ({ref}`sec-governance`, {ref}`sec-conclusion`). Throughout, the analytical style is to juxtapose method-divergent estimates rather than to report single headline numbers, because the same phenomenon — publication rate, concordance, sharing trend — yields very different values by method, {cite:p}`Sena2010, terRiet2012, Deutsch2021` and several field-defining figures rest on modelled or non-transparent sources that we flag wherever they appear rather than smooth over. {cite:p}`Freedman2015, Ioannidis2014c` That style is not neutrality for its own sake but a hedge against the false consensus a single, confidently repeated number can manufacture. {cite:p}`Ioannidis2005b` The empirical anchor the review returns to most often — that actual, usable data availability sits near two percent while declared availability and paperwork compliance sit far above it — recurs across FAIR audits, incentive studies, and governance evaluations alike, and it is against that near-static baseline — the empirical ~2% availability anchor {cite:p}`Hamilton2023` — that every enforcement result must be judged. {cite:p}`Hamilton2022, VanTuyl2016, Macleod2019b` The claim is not that the crisis is worse than others have said, nor that any one mechanism will resolve it, but that the losses others have counted in money and papers are more fundamentally counted in animal lives.

:::{trust-claim}
:claim-id: clm_2544bbf2a8aba117
:claim: Throughout, the analytical style is to juxtapose method-divergent estimates rather than to report single headline numbers, because the same phenomenon — publication rate, concordance, sharing trend — yields very different values by method, and several field-defining figures rest on modelled or non-transparent sources that we flag wherever they appear rather than smooth over.
:cites: Sena2010, terRiet2012, Deutsch2021, Freedman2015, Ioannidis2014c
:claim-type: methodological
:modality: established
:::

:::{trust-claim}
:claim-id: clm_0a63a766b7dcbc97
:claim: That style is not neutrality for its own sake but a hedge against the false consensus a single, confidently repeated number can manufacture.
:cites: Ioannidis2005b
:claim-type: methodological
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_0fde28aeec8b0c15
:claim: The empirical anchor the review returns to most often — that actual, usable data availability sits near two percent while declared availability and paperwork compliance sit far above it — recurs across FAIR audits, incentive studies, and governance evaluations alike, and it is against that near-static baseline — the empirical ~2% availability anchor — that every enforcement result must be judged.
:cites: Hamilton2023, Hamilton2022, VanTuyl2016, Macleod2019b
:claim-type: empirical
:modality: contested
:::

The strongest version of that claim is also its simplest, and it is the thread that ties the sections together: because animals have already paid for the data with their welfare and, usually, their lives, letting the data go to waste is not merely poor science but a welfare harm in its own right, and repaying the debt — through FAIR stewardship, through reuse and virtual control groups, through disciplined stewardship of the data that non-animal methods generate, and through incentive and governance reform that makes stewardship count — is a way of saving animals. {cite:p}`Pound2018, Kramer2015, Wilkinson2016, Macleod2019b, Cait2022` None of the four mechanisms is sufficient alone, and each carries a condition this review is at pains to state — FAIR stewardship that must be enforced rather than merely declared, virtual control groups that await regulatory acceptance, and non-animal methods that must themselves be stewarded from the outset. {cite:p}`Hamilton2022, SATO2024, Gant2026` Yet the reuse infrastructure that lowers control-animal numbers already exists at scale, awaiting only the acceptance and the incentives that would put it to work. {cite:p}`Moresis2024, Deschl2002, StegerHartmann2020` The evidence that stewardship can be made to count is itself real but narrow, concentrated on the interventions that were enforced and checked rather than merely urged. {cite:p}`Macleod2019b, Kidwell2016, Hair2019` The evidence that this debt is neither hypothetical nor small begins in, {ref}`sec-repro-crisis` with the state of the knowledge the animals were used to produce.

:::{trust-claim}
:claim-id: clm_9e06ef3c4c66e025
:claim: The strongest version of that claim is also its simplest, and it is the thread that ties the sections together: because animals have already paid for the data with their welfare and, usually, their lives, letting the data go to waste is not merely poor science but a welfare harm in its own right, and repaying the debt — through FAIR stewardship, through reuse and virtual control groups, through disciplined stewardship of the data that non-animal methods generate, and through incentive and governance reform that makes stewardship count — is a way of saving animals.
:cites: Pound2018, Kramer2015, Wilkinson2016, Macleod2019b, Cait2022
:claim-type: causal
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_a273fdebb9e7589f
:claim: None of the four mechanisms is sufficient alone, and each carries a condition this review is at pains to state — FAIR stewardship that must be enforced rather than merely declared, virtual control groups that await regulatory acceptance, and non-animal methods that must themselves be stewarded from the outset.
:cites: Hamilton2022, SATO2024, Gant2026
:claim-type: limitation
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_b16caf61b9732003
:claim: Yet the reuse infrastructure that lowers control-animal numbers already exists at scale, awaiting only the acceptance and the incentives that would put it to work.
:cites: Moresis2024, Deschl2002, StegerHartmann2020
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_b96d3c255c7e8938
:claim: The evidence that stewardship can be made to count is itself real but narrow, concentrated on the interventions that were enforced and checked rather than merely urged.
:cites: Macleod2019b, Kidwell2016, Hair2019
:claim-type: review_synthesis
:modality: contested
:::

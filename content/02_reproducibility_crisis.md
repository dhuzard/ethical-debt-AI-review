(sec-repro-crisis)=
# The Reproducibility and Translation Crisis in Preclinical Research

The premise advanced in {ref}`sec-introduction` — that animals are spent to generate knowledge which is then allowed to go to waste — presupposes an empirical claim about the state of that knowledge. This section supplies it. The published preclinical record is not a neutral archive of what animal experiments found; it is a filtered, distorted, and frequently untranslatable sample of them, and the distortions are large enough that others have tried to price them. A probability-bounds economic model combining published irreproducibility estimates with United States life-science spending puts the cumulative preclinical irreproducibility rate at a midpoint of 53.3%, implying roughly US\$28 billion per year of non-reproducible preclinical research in the United States alone {cite:p}`Freedman2015`. That figure has been restated by the group that produced it {cite:p}`Freedman2017` and folded into wider estimates ranging from US\$28 billion nationally to over US\$200 billion worldwide {cite:p}`Fitzpatrick2018`. It sits within a broader accounting of avoidable waste in an enterprise that consumed some US\$240 billion globally in 2010 and close to a quarter of a trillion dollars annually thereafter {cite:p}`Chalmers2014, Moher2016`, of which an oft-quoted 85% is judged to be squandered {cite:p}`Ioannidis2014c`, and around which a consensus of meta-researchers holds that most new biomedical discoveries will not stand the test of time {cite:p}`Begley2015, vonNiederhausern2018`. These headline numbers should be handled with the same skepticism they diagnose: the US\$28 billion figure is a modeled estimate whose authors stress its uncertainty, the "85% wasted" claim is a synthesis rather than a measurement, and both rest on inputs that are not fully transparent. Their value is not their precision but their convergence with a theoretical prior — that under realistic assumptions about power, bias, and pre-study odds, a research claim in most fields is more likely false than true {cite:p}`Ioannidis2005b`. The remainder of this section examines the specific mechanisms — publication bias, non-publication, weak internal validity, selective reporting, biological variability, and species discordance — through which that prior is realised in the animal literature.
:::{trust-claim}
:claim-id: clm_7f23378d038035ae
:::
:::{trust-claim}
:claim-id: clm_45fc15ff42aaff8a
:::
:::{trust-claim}
:claim-id: clm_6a8aa422931e708b
:::
:::{trust-claim}
:claim-id: clm_f6543bd90efb459d
:::

## Publication bias and the vanishing of negative results

The clearest signature of distortion is that the animal literature is almost entirely positive. In 525 publications spanning sixteen stroke interventions, only 2.2% reported no significant effect, and correcting for the resulting funnel-plot asymmetry reduced pooled efficacy from 31.2% to 23.8%, with roughly one in six experiments estimated to be missing {cite:p}`Sena2010`. The pattern is not confined to stroke: across 4,445 datasets in 160 meta-analyses of six neurological conditions, the observed number of "positive" studies (1,719) vastly exceeded the number predicted by their statistical power (919), and only eight of the 160 meta-analyses were free of any excess-significance or small-study signal {cite:p}`Tsilidis2013`. Synthesising these strands, publication bias alone was judged to account for a third or more of the efficacy reported in systematic reviews of animal stroke studies {cite:p}`vanderWorp2010`. Individual meta-analyses have since put quantities on the correction: an updated review of interleukin-1 receptor antagonist in stroke found apparent efficacy of 36.2% fall to 21.9% once around thirty theoretically missing studies were imputed {cite:p}`McCann2016`; a synthesis of sunitinib tumour studies calculated a 45% overestimate of effect size with not a single experiment using blinded outcome assessment {cite:p}`Henderson2015`; and trim-and-fill corrections have imputed 316 missing studies in chemotherapy-induced neuropathy {cite:p}`Currie2019`, nineteen in stroke biomaterials {cite:p}`Bolan2019`, and thirteen in spinal-cord-injury nutrition {cite:p}`MacIntoshSmith2023`, with funnel-plot asymmetry signalling the same missing-study problem in antidepressant forced-swim, ginsenoside stroke and heparin brain-injury literatures alike {cite:p}`Martins2025, Xie2015, Aiyede2022`. The distortions from bias and from weak design are additive rather than competing, as {numref}`fig-sec2-bias-inflation` shows.
:::{trust-claim}
:claim-id: clm_2191cbc1fd59a31c
:::
:::{trust-claim}
:claim-id: clm_c63333546bd6f5a4
:::
:::{trust-claim}
:claim-id: clm_188ccff4af30d544
:::
:::{trust-claim}
:claim-id: clm_0d0b66502df98a41
:::

:::{figure} ../figures/fig_sec2_bias_inflation.png
:name: fig-sec2-bias-inflation
:width: 90%
**Bias inflates apparent preclinical efficacy.** Across independent meta-analyses of stroke and spinal-cord-injury models, internal-validity failures and publication bias each exaggerate reported efficacy: unblinded induction of ischaemia inflates effect sizes by 13.1% {cite:p}`Crossley2008`, absence of blinded outcome assessment by 7.2% {cite:p}`Watzlawick2019`, and publication bias by 27% {cite:p}`Watzlawick2014`. Marker shape distinguishes the metric type and the whisker on the first estimate shows its reported 95% confidence interval. Crossley (13.1%) and Watzlawick (2019, 7.2%) are percentage-point effect-size inflations from different single design items (blinded induction of ischaemia versus blinded outcome assessment). Watzlawick (2014)'s 27% is a proportional efficacy overestimation from publication-bias correction (a fall from 21% to 15% improvement), not a percentage-point figure; the models differ (stroke versus spinal cord injury, the last being RhoA/ROCK-specific). The three estimates are therefore not on a single common scale and are labelled individually.
:::

:::{dropdown} 📓 Figure code

```python
import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# shared_style.py lives alongside this notebook in figures/notebooks/
sys.path.insert(0, os.path.abspath('.'))
from shared_style import COLORS, apply_style, save_figure
apply_style()
OUT = os.path.abspath('..')  # figures/ directory

# Data from evidence_section_02.json -> figure_data
# comparison_id: 'bias-inflation-preclinical-neuro-SRs' (audit ruling: CAVEAT).
# The three values are NOT on one common scale: two are percentage-point design-
# item inflations, one is a proportional publication-bias overestimation. Marker
# shape encodes the metric type (redundant, non-colour cue).
# (label, value %, kind, ci low/high or None)
rows = [
    ("Crossley 2008\nunblinded ischaemia induction", 13.1, "design", (0.2, 26.4)),  # 10.1161/STROKEAHA.107.498725
    ("Watzlawick 2019\nno blinded outcome assessment", 7.2, "design", None),          # 10.1212/WNL.0000000000007718
    ("Watzlawick 2014\npublication-bias correction", 27.0, "pubbias", None),          # 10.1001/jamaneurol.2013.4684
]
kind_style = {
    "design":  dict(color=COLORS["debt"], marker="o",
                    label="Percentage-point effect-size inflation (single design item)"),
    "pubbias": dict(color=COLORS["conflict"], marker="s",
                    label="Proportional efficacy overestimation (publication bias)"),
}

fig, ax = plt.subplots(figsize=(9.2, 4.6))
y = np.arange(len(rows))[::-1]
for yi, (lab, val, kind, ci) in zip(y, rows):
    st = kind_style[kind]
    if ci is not None:
        lo, hi = ci
        ax.plot([lo, hi], [yi, yi], color=COLORS["gray_700"], linewidth=1.2, zorder=2)
        ax.plot([lo, lo], [yi - 0.08, yi + 0.08], color=COLORS["gray_700"], linewidth=1.2)
        ax.plot([hi, hi], [yi - 0.08, yi + 0.08], color=COLORS["gray_700"], linewidth=1.2)
    ax.scatter([val], [yi], s=150, color=st["color"], marker=st["marker"],
               edgecolor=COLORS["ink"], linewidth=0.7, zorder=3)
    ax.text(val, yi + 0.17, f"{val:g}%", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=COLORS["ink"])

ax.axvline(0, color=COLORS["neutral_baseline"], linewidth=0.75, linestyle="--", zorder=1)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows])
ax.set_ylim(-0.6, len(rows) - 0.4); ax.set_xlim(-1, 30)
ax.set_xlabel("Reported inflation of apparent efficacy (%)")
ax.set_title("Bias inflates apparent preclinical efficacy", pad=12)
handles = [
    plt.Line2D([0], [0], marker="o", linestyle="none", markersize=11,
               markerfacecolor=COLORS["debt"], markeredgecolor=COLORS["ink"],
               label=kind_style["design"]["label"]),
    plt.Line2D([0], [0], marker="s", linestyle="none", markersize=11,
               markerfacecolor=COLORS["conflict"], markeredgecolor=COLORS["ink"],
               label=kind_style["pubbias"]["label"]),
]
ax.legend(handles=handles, loc="lower left", frameon=True, fontsize=9)
ax.text(0.0, -0.30,
        "Metrics are not numerically comparable and share no common baseline; "
        "whisker = reported 95% CI (Crossley). Abstract-level values.",
        transform=ax.transAxes, fontsize=9, color=COLORS["gray_500"], fontstyle="italic")
fig.tight_layout()
save_figure(fig, os.path.join(OUT, "fig_sec2_bias_inflation.png"))
```

:::

The near-universal positivity of the preclinical literature creates a specific interpretive trap: a fresh single-drug meta-analysis reporting benefit on every endpoint looks like strong evidence but may be indistinguishable from a biased sample. A meta-analysis of fifteen rodent stroke trials, for instance, reported that metformin significantly improved every one of eight outcomes {cite:p}`Fu2022`, and a synthesis of the noble gas argon reported benefit on every acquired-brain-injury endpoint {cite:p}`Liang2022` — precisely the pattern that the cross-intervention analyses attribute to selective publication rather than to genuine, uniform efficacy {cite:p}`Sena2010`. The field is not internally consistent about how far the distortion reaches. Two preclinical traumatic-brain-injury syntheses reached opposite conclusions about their own literature: a network meta-analysis of anaesthetic neuroprotection found no evidence that effect sizes were exaggerated by selective publication {cite:p}`Archer2018`, whereas a progesterone meta-analysis detected clear funnel-plot asymmetry indicating bias {cite:p}`NasreNasser2022`. Whether a given corner of the literature is bias-free or merely under-examined is often unresolved, and the safest reading is that positivity is uninformative until publication bias has been formally tested — a step that little more than half of preclinical systematic reviews actually take {cite:p}`Russell2022`.
:::{trust-claim}
:claim-id: clm_f88d1499df2ad339
:::
:::{trust-claim}
:claim-id: clm_c560886a5ff7f31d
:::
:::{trust-claim}
:claim-id: clm_6fb6141cdb0008cb
:::

## The file drawer: non-publication of whole experiments

Behind the biased selection of results lies the non-publication of entire experiments, and here the field's own estimates diverge by method. Opinion surveys of laboratory-animal researchers put the published fraction low: staff at not-for-profit institutes estimated that only half of conducted animal experiments are published, and those in for-profit settings estimated just 10% {cite:p}`terRiet2012`. Empirical protocol-to-publication tracking is more optimistic, finding that around 70% of registered animal-study proposals eventually yield at least one publication {cite:p}`Deutsch2021`, consistent with a retrospective analysis in which 65% of internally funded medical projects — 46% of them involving animals — produced a peer-reviewed paper {cite:p}`Deutsch2020`.
:::{trust-claim}
:claim-id: clm_714c55a71136850b
:::
:::{trust-claim}
:claim-id: clm_3de54e95b5461a84
:::

:::{admonition} Evidence Conflict
:class: warning
How much animal research goes unpublished depends on how the question is asked. Subjective surveys of researchers estimate that only ~50% of experiments are published {cite:p}`terRiet2012`, whereas empirical tracking of registered protocols to publication finds rates closer to 70% {cite:p}`Deutsch2021`. The disagreement is largely resolved by method — impressions of the file drawer are darker than the auditable record — but even the optimistic figure leaves roughly a third of animal experiments unpublished, and self-report data show that the studies most likely to reach print are the ones that produced a result {cite:p}`Deutsch2021`.
:::

Whichever estimate is correct, the consequence is a literature in which protocols, full reports, and datasets are available for only about half of all studies and are further pruned by selective reporting of methods and outcomes {cite:p}`Chan2014`. The timing of publication compounds the problem for animal work specifically: across 47 novel drugs, 87% of accessible animal efficacy studies appeared only after the first human trial had been published, and for 17% of the drugs no efficacy study was published before that trial at all {cite:p}`Federico2014` — so the animal evidence, when it exists, frequently cannot have informed the decision to test in people. The barriers to even reconstructing what was done are formidable. The Reproducibility Project: Cancer Biology set out to repeat 193 experiments from 53 high-impact papers but completed only 50, because no paper described its protocol in enough detail to run without modification and data underlying the original effect sizes were public for just four of the 193 experiments {cite:p}`Errington2021a`; of those it did attempt, replication effect sizes were markedly smaller than the originals {cite:p}`Errington2021b`, and several planned replications were abandoned before yielding any outcome {cite:p}`Errington2021c`. That completion figure — only 26% of the planned experiments could be carried out at all — is a feasibility ceiling rather than a replication rate, and as such is distinct from, though it sits alongside, the earlier industry audits in which an estimated 25% (Bayer) and 11% (Amgen) of findings could be reproduced {cite:p}`Errington2021b`.
:::{trust-claim}
:claim-id: clm_325ac03e66cbc678
:::
:::{trust-claim}
:claim-id: clm_faa1f77ef0ff7060
:::
:::{trust-claim}
:claim-id: clm_e3b4b78f1bfffb37
:::
:::{trust-claim}
:claim-id: clm_6e4a4ed16c6d55b4
:::

## Weak internal validity and chronic underpowering

The reason so many published effects prove fragile is that the studies producing them are, on average, poorly protected against bias and too small to be reliable. The survey underpinning the ARRIVE guidelines found that only 59% of 271 animal papers stated their hypothesis and basic animal characteristics, while 87% did not report randomisation and 86% did not report blinding {cite:p}`Kilkenny2010`; a decade later, adherence remained inconsistent enough to prompt a slimmed-down "Essential 10" {cite:p}`PercieduSert2020a`, and a randomised controlled trial at a major journal showed that simply requesting a completed checklist at submission produced no manuscript that met every ARRIVE item {cite:p}`Hair2019`. Independent audits have repeatedly documented the same gaps: reporting of bias-reduction measures is limited across a random sample of life-science papers and is actually lower in high-impact journals {cite:p}`Macleod2015`; a cerebrovascular journal volume stated a primary hypothesis in only 30% of articles {cite:p}`Vesterinen2010`; animal papers in a critical-care journal justified their sample size in 10% of cases, randomised in 43%, and blinded in 23%, with a single paper reporting an effect size {cite:p}`Reynolds2020`; plastic-surgery animal studies blinded outcome assessment in 21.4% {cite:p}`Freshwater2015`; and surveys spanning India, Sri Lanka and large-animal stroke models confirm the shortfall is global rather than parochial {cite:p}`Singh2020, Kringe2020`. Underpinning all of this is chronic low power: the average neuroscience study is badly underpowered, which both inflates the effect sizes that do reach significance and lowers the probability that a positive result is true {cite:p}`Button2013`, and across disciplines statistical power has persistently sat below 50% while only about 13% of trials report outcomes fully consistent with their pre-registered commitments {cite:p}`Munafo2017`.
:::{trust-claim}
:claim-id: clm_3f55d5e4855418d5
:::
:::{trust-claim}
:claim-id: clm_53e26370ae2b4b33
:::
:::{trust-claim}
:claim-id: clm_b390081955318ca1
:::

That underpowering and unreported bias-control are not cosmetic is shown by the direct effect of design items on measured efficacy, quantified in {numref}`fig-sec2-bias-inflation`: unblinded ischaemia induction and unblinded outcome assessment each add several percentage points of apparent benefit {cite:p}`Crossley2008, Watzlawick2019`. Reformers have responded with a proliferation of instruments — the SYRCLE risk-of-bias tool adapted from Cochrane {cite:p}`Hooijmans2014`, the NINDS core reporting standards {cite:p}`Landis2012`, planning-stage guidance {cite:p}`Smith2017`, preregistration platforms {cite:p}`Bert2019`, dozens of consolidated preclinical guideline documents offering scores of rigor recommendations {cite:p}`Henderson2013, Lapchak2012`, and formal frameworks for sample-size determination under the Reduction principle {cite:p}`Serdar2021, Mazoit2026` — yet more than twenty competing appraisal tools now exist, itself an obstacle to any standard judgement of quality {cite:p}`Ma2020`. Where improvement has occurred it has been uneven: a nationwide comparison found randomisation reporting rose from 24.0% to 40.8% between 2009 and 2018 while conflict-of-interest disclosure jumped from 37.6% to 90.4% {cite:p}`Kousholt2022`, but a survey of in-vivo researchers still found fewer than half claiming to use blinded outcome assessment {cite:p}`Reichlin2016`, and a commentary across twenty recent preclinical reviews found that not one study scored above eight of ten on a standard quality scale, with a median of four {cite:p}`Russell2022`. The same low-quality signature recurs wherever it is measured, from ischaemic-preconditioning and renal-injury syntheses reporting sample-size calculations in 2% of studies {cite:p}`Wever2015, Jonker2016`, to gene-therapy, herbal, and stem-cell meta-analyses with median risk-of-bias scores of four to five out of ten {cite:p}`Cunningham2022, Lin2021, Lalu2016, Liddle2021`, to pain, osteoporosis and glioma reviews whose universally positive effects rest on studies at high or unclear risk of bias {cite:p}`Soliman2021, Zhang2022, Jue2018, Antonic2013, Huerta2024, Scuteri2022, Koop2023, Mugan2025`. The pattern is strikingly indifferent to therapeutic area: meta-analyses of neuroprotection in stroke, Parkinson's and Alzheimer's models {cite:p}`Yang2025, Su2021, Zhu2019, Zhang2020, Modiri2025, Sharif2025`, of sepsis and cardiomyopathy {cite:p}`Zingarelli2019, Lopes2020, Hum2024`, of antidepressant and seizure paradigms {cite:p}`Ratajczak2024, Arida2021`, of stem-cell and exosome therapies for wounds, neuropathy and osteoarthritis {cite:p}`Yue2024, Bailey2021, Lu2025, Xing2018, Yamaura2023, Deckers2019, Huang2024`, and even of zebrafish neurobehaviour {cite:p}`Reis2023` all converge on the same reading — large, uniformly positive pooled effects resting on primary studies that failed to report the safeguards that would make those effects trustworthy.
:::{trust-claim}
:claim-id: clm_507112e8162a13ac
:::
:::{trust-claim}
:claim-id: clm_321d11452b9b5ea5
:::
:::{trust-claim}
:claim-id: clm_f3c0d3aeec77357a
:::
:::{trust-claim}
:claim-id: clm_9a9ef75ebf01f231
:::
:::{trust-claim}
:claim-id: clm_42be94ead5fb7608
:::

## Selective reporting, questionable practices, and the persistence of error

The behaviours that generate these patterns are, to a substantial degree, admitted. A meta-analysis of misconduct surveys found that about 2% of scientists confess to having fabricated or falsified data at least once, while up to a third admit other questionable research practices — and far higher fractions report such practices in colleagues {cite:p}`Fanelli2009`. Asked about specific behaviours, 64% of ecologists and evolutionary biologists reported having failed to publish a non-significant result, 42% had collected more data after checking significance, and 51% had presented an unexpected finding as though predicted {cite:p}`Fraser2018`. Whether these practices materially distort conclusions is contested: text-mining of the p-value distribution suggests p-hacking is common but weak relative to real effects {cite:p}`Head2015`, yet an automated analysis of nearly 58,000 psychology articles found the proportion of significant p-values per paper stuck at 69% across a decade of reform {cite:p}`Boschen2023`. Once a false or inflated claim enters the literature it is remarkably persistent. Among highly cited clinical studies, 16% were later contradicted and another 16% had initially overstated effects {cite:p}`Ioannidis2005a`; even after refutation by randomised trials, half of the articles citing contradicted observational claims remained favourable {cite:p}`Tatsioni2007`; and citation-network analysis has shown how a belief unsupported by primary data can accumulate hundreds of thousands of supporting citation paths and thereby manufacture unfounded authority {cite:p}`Greenberg2009`. The corrective apparatus is itself compromised, with systematic reviews and meta-analyses now mass-produced and, in the judgement of one bibliometric survey, largely redundant, misleading, or conflicted {cite:p}`IOANNIDIS2016, Nakagawa2017`, even as the preclinical literature expands faster than systematic review can track it {cite:p}`BannachBrown2021`.
:::{trust-claim}
:claim-id: clm_7a8f48bdbb22b016
:::
:::{trust-claim}
:claim-id: clm_f2107713e95ec8e4
:::
:::{trust-claim}
:claim-id: clm_b04adf82d4f6615d
:::
:::{trust-claim}
:claim-id: clm_9c624b1d493737db
:::
:::{trust-claim}
:claim-id: clm_a94a3f1dc7bdb5bf
:::

The problem is not unique to preclinical biology, and the cross-domain replication projects that popularised the term "reproducibility crisis" are worth engaging precisely because they remain disputed. Coordinated replications of 100 psychology studies found that only 36% reached significance against 97% of the originals, with replication effect sizes about half the originals {cite:p}`OpenScienceCollaboration2015`; parallel efforts reproduced 62% of social-science experiments in Nature and Science {cite:p}`Camerer2018`, 39% of a psychology sample after re-coding for context {cite:p}`VanBavel2016`, and prediction markets estimated a median prior probability of only 9% that the tested hypotheses were true {cite:p}`Dreber2015`; the same low-reproducibility metrics have since been carried into ecology and evolution {cite:p}`Fidler2017`.
:::{trust-claim}
:claim-id: clm_6d6293275e80f7f8
:::

:::{admonition} Evidence Conflict
:class: warning
How deep the replication crisis runs is itself unsettled. The Reproducibility Project: Psychology reported that only ~36% of replications were statistically significant {cite:p}`OpenScienceCollaboration2015`. A prominent reanalysis argued the project contained three statistical errors and that, corrected for sampling error and power, the data are actually consistent with high reproducibility {cite:p}`Gilbert2016`. A Bayesian treatment of the same 36% rate reached the opposite conclusion, inferring publication bias so large that dozens of negative results were expected to have occurred before one was published {cite:p}`Ingre2018`. The dispute is about how replication should be measured, not about the underlying data — and it has since been reframed by some as a productive "credibility revolution" rather than a failure {cite:p}`Korbmacher2023, Amaral2019`.
:::

That reproducibility is contingent on power and design, rather than a fixed property of a field, is underscored by genetics: genome-wide significant variants replicated 85% of the time in well-powered biobank data — but only 58% for binary versus 95% for quantitative traits {cite:p}`OSullivan2021` — whereas the earlier, underpowered candidate-gene era found robust replication persistently elusive {cite:p}`Li2012`.
:::{trust-claim}
:claim-id: clm_78c37bc63dd8ac27
:::

## Why single-lab results fail: reagents, drift, and biological variability

Even absent bias or misconduct, a preclinical result can fail to reproduce because the biological and material substrate is not the fixed reagent it is assumed to be. Human cancer cell lines diversify in culture: across 27 strains of MCF7, only 35% of coding variants were shared by all strains, and drug responses differed markedly {cite:p}`BenDavid2018`. Misidentification remains endemic — under a mandatory authentication policy at one cancer journal, 5.2% of submitted human cell lines were misidentified {cite:p}`Souren2022`, and a line sold commercially as rabbit endothelium proved on barcoding to be bovine {cite:p}`Vicente2021`. Antibodies are worse still: more than 3.8 million "research-grade" antibodies are marketed with little validation against fewer than 500 highly validated clinical-grade reagents, so that inconsistent antibody performance is a first-order driver of irreproducibility that end-users must themselves control {cite:p}`Sfanos2019, PillaiKastoori2020, Venkataraman2018`. The animals are not fixed either. In a landmark demonstration, inbred mouse strains tested simultaneously in three laboratories under rigorously equated apparatus and protocols still differed systematically in behaviour across sites {cite:p}`Crabbe1999`; a single retest of a P<0.05 behavioural result reproduces only about 60% of the time {cite:p}`vandeLagemaat2017`; behavioural measures carry coefficients of variation two to three times those of clinical chemistry {cite:p}`Aigner2023`; and inbred strains accumulate genetic drift that changes their phenotype over time and place {cite:p}`TAFT2006`, compounded by strain-background effects on stem-cell and xenograft phenotype {cite:p}`Ortmann2020, Devlin2022`. Husbandry variables normally treated as invisible turn out to move results: the time of day a microbiome sample is taken can change a study's conclusion more than the intervention does {cite:p}`Allaband2024`, something as basic as body temperature shifts stroke infarct size by dozens of percent {cite:p}`deJonge2019`, and bedding material, chow diet, and cage-level gut-flora heterogeneity each perturb metabolic and cancer models {cite:p}`Islam2021, Knuth2024, Feng2025`. The models themselves are often so heterogeneously constructed that few designs are ever reused, as a catalogue of nearly 4,000 rodent fatty-liver models made plain {cite:p}`Im2021`.
:::{trust-claim}
:claim-id: clm_1dade0b3e50e905a
:::
:::{trust-claim}
:claim-id: clm_991f3295d64cfdc8
:::
:::{trust-claim}
:claim-id: clm_f593c2b5e916ca3a
:::
:::{trust-claim}
:claim-id: clm_1c1cf2e3b5da48b8
:::
:::{trust-claim}
:claim-id: clm_46faac115993fe7c
:::
:::{trust-claim}
:claim-id: clm_0aaec8fc0d2cda09
:::

A distinct and well-documented source of unreliability is the routine exclusion of half the population. Male animals have dominated biomedical research, most severely in neuroscience where single-sex male studies once outnumbered female ones 5.5 to 1 {cite:p}`Beery2011`; a decade after this was quantified, both-sex inclusion had risen across nine disciplines but the proportion actually analysing data by sex had not, in eight of them {cite:p}`Woitowich2020`, despite a US policy expecting sex to be treated as a biological variable {cite:p}`Miller2016`. The usual justification — that females are intrinsically more variable — is unfounded: across 311 neuroscience studies female rats were no more variable than males, even without controlling for the oestrous cycle {cite:p}`Becker2016`, yet male-only designs continue to distort conclusions in domains from morphine sensitisation to cough {cite:p}`Brandner2024, Plevkova2017, OLeary2022`, and even a variable as basic as animal age is reported inconsistently {cite:p}`Jackson2016`. The clinical stakes are concrete: of ten prescription drugs withdrawn from the United States market between 1997 and 2001, eight caused greater harm to women than to men, a record that motivated sex-disaggregated reporting standards {cite:p}`Heidari2016`.
:::{trust-claim}
:claim-id: clm_435c111867358aee
:::
:::{trust-claim}
:claim-id: clm_0cc8d0578ecdd2f2
:::
:::{trust-claim}
:claim-id: clm_81cd066012adf24b
:::

## The disputed cure: standardise or heterogenise?

If context-dependent variation is the problem, the field disagrees sharply about the remedy. The traditional prescription is rigorous standardisation — minimising genetic and environmental variation so that fewer animals are needed to detect an effect {cite:p}`Serdar2021`. A body of simulation and multi-laboratory evidence argues this backfires. Using data from 440 preclinical studies across 13 interventions, single-laboratory experiments failed to predict the true effect size in more than half of cases even when powered above 0.8, and — counter to the intuition that bigger is better — larger single-lab samples made effect-size estimates less accurate, whereas distributing animals across laboratories improved them {cite:p}`Voelkl2018`. The proposed response is deliberate heterogenisation of samples and conditions {cite:p}`Voelkl2020`, on the reaction-norm view that standardisation buys internal precision at the cost of external validity {cite:p}`Voelkl2021`.
:::{trust-claim}
:claim-id: clm_8b9b8324d57fcd2f
:::
:::{trust-claim}
:claim-id: clm_2dcc5c535cb09177
:::
:::{trust-claim}
:claim-id: clm_3694e6589961c4fb
:::

:::{admonition} Evidence Conflict
:class: warning
Two opposed prescriptions claim to fix preclinical reliability. The standardisation-and-rigour school holds that reproducibility follows from rigour plus transparency — pre-specified analysis plans, tight control of variation, and active laboratory management {cite:p}`Samsa2019`, and that minimising nuisance variation reduces the number of animals required {cite:p}`Serdar2021`. The heterogenisation school holds that rigorous standardisation is itself a cause of irreproducibility, because a result tuned to one laboratory's idiosyncratic conditions has no external validity {cite:p}`Voelkl2021, Voelkl2018`. The evidence is genuinely mixed: a Shank2 multicentre study found that rigorously *harmonised* protocols yielded highly replicable genotype and treatment effects across sites {cite:p}`ArroyoAraujo2019`, which standardisation and heterogenisation advocates read in opposite ways. The dispute is unresolved, and it matters for animal numbers as much as for validity, since the two strategies imply different sample sizes.
:::

The operational reconciliation increasingly favoured is neither pure standardisation nor pure heterogenisation but the multicentre preclinical randomised controlled trial, in which centralised randomisation and blinded core-lab analysis are distributed across independent sites. A six-centre stroke trial of an anti-CD49d antibody — undertaken only after positive single-lab studies had already triggered a clinical trial — found benefit confined to small cortical infarcts and none in large lesions, exposing the model-dependence that single-lab work had missed {cite:p}`Llovera2015`; a ten-site pig myocardial-infarction network built on the same principles was explicitly created to counter the lack of rigour behind failed cardioprotection translation {cite:p}`Kleinbongard2024, Btker2018`. The multicentre design is no panacea, however: a preregistered, fully blinded three-site confirmatory trial of neuroprotectants for chemotherapy-induced neuropathy failed its primary objective when unexpected toxicity and tumour growth left it underpowered {cite:p}`Boehmerle2025` — evidence that distributed rigour exposes translational uncertainty rather than abolishing it.
:::{trust-claim}
:claim-id: clm_8371161698b74d9d
:::
:::{trust-claim}
:claim-id: clm_2f810fc8a4b77745
:::

## Translation: attrition and species discordance

All of these failures converge on the outcome that matters clinically: animal findings translate to humans poorly and unpredictably. In a direct comparison of six interventions with unambiguous clinical evidence, corticosteroids benefited animal head-injury models (pooled odds ratio 0.58) yet showed no benefit in patients {cite:p}`Perel2006`, and a scoping review of 121 quantitative animal-to-human comparisons found published translational success rates spanning the entire range from 0% to 100%, with animal-human toxicity concordance of 71% across species but only 43% for rodents alone {cite:p}`Leenaars2019b`. The most instructive case is one in which the animal data are not even in dispute.
:::{trust-claim}
:claim-id: clm_c0bcedd25400c5d3
:::

:::{figure} ../figures/fig_sec2_mouse_human_concordance.png
:name: fig-sec2-mouse-human-concordance
:width: 90%
**Same data, opposite conclusions.** Two analyses of the identical inflammation gene-expression datasets reach opposite conclusions on whether mouse models mimic human disease. {cite:t}`Seok2013` report near-random concordance (R² of 0.0–0.1) for genes significant in humans; {cite:t}`Takao2014`, after restricting to genes significant in both species, report strong concordance (Spearman ρ of 0.43–0.68). The two are shown as a table rather than a shared axis because they are not numerically comparable — different statistics computed on different gene subsets. The apparent reversal is a methodological reanalysis of identical data, not a measured biological difference; the animals' data did not change, only the gene-selection step did.
:::

:::{dropdown} 📓 Figure code

```python
import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# shared_style.py lives alongside this notebook in figures/notebooks/
sys.path.insert(0, os.path.abspath('.'))
from shared_style import COLORS, apply_style, save_figure
apply_style()
OUT = os.path.abspath('..')  # figures/ directory

# Data from evidence_section_02.json -> figure_data
# comparison_id: 'mouse-human-inflammation-concordance'
# audit ruling: CAVEAT_FORCED_FROM_SPLIT -> render as an annotated TABLE, never a
# common correlation axis (the two statistics are not comparable).
cols = ["Study", "Statistic", "Value", "Genes analysed", "Model assessment"]
data = [
    ["Seok et al. 2013", "R2", "0.0-0.1",
     "significant in humans", "poorly mimics"],          # 10.1073/pnas.1222878110
    ["Takao & Miyakawa 2014", "Spearman rho", "0.43-0.68",
     "significant in both species", "greatly mimics"],   # 10.1073/pnas.1401965111
]
assess_color = {"poorly mimics": COLORS["debt"], "greatly mimics": COLORS["repayment"]}
col_x = [0.02, 0.30, 0.45, 0.60, 0.83]
col_w = [0.28, 0.15, 0.15, 0.23, 0.17]

fig, ax = plt.subplots(figsize=(10.2, 3.2))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.set_title("Same datasets, opposite conclusions on mouse-human concordance", pad=10, fontsize=15)

row_h = 0.26
y_header = 0.74
ax.add_patch(mpatches.Rectangle((0.0, y_header), 1.0, row_h, facecolor=COLORS["ink"], edgecolor="none"))
for x, w, c in zip(col_x, col_w, cols):
    ax.text(x + 0.005, y_header + row_h / 2, c, ha="left", va="center",
            fontsize=11.5, fontweight="bold", color="white")

for r, row in enumerate(data):
    y = y_header - (r + 1) * row_h
    band = COLORS["gray_100"] if r % 2 == 0 else "white"
    ax.add_patch(mpatches.Rectangle((0.0, y), 1.0, row_h, facecolor=band,
                                    edgecolor=COLORS["gray_300"], linewidth=0.6))
    for j, (x, w, val) in enumerate(zip(col_x, col_w, row)):
        if cols[j] == "Model assessment":
            vc = assess_color[val]
            ax.add_patch(mpatches.Rectangle((x - 0.005, y + 0.03), w, row_h - 0.06,
                                            facecolor=vc, alpha=0.90, edgecolor=COLORS["ink"], linewidth=0.6))
            ax.text(x + w / 2 - 0.005, y + row_h / 2, val, ha="center", va="center",
                    fontsize=10.5, fontweight="bold", color="white")
        else:
            weight = "bold" if cols[j] == "Value" else "normal"
            ax.text(x + 0.005, y + row_h / 2, val, ha="left", va="center",
                    fontsize=11, fontweight=weight, color=COLORS["ink"])

ax.text(0.0, 0.03,
        "Different statistics on different gene subsets - not numerically comparable. "
        "The reversal is a reanalysis of identical data, not a biological difference.",
        ha="left", va="bottom", fontsize=9.5, color=COLORS["gray_500"], fontstyle="italic")
fig.tight_layout()
save_figure(fig, os.path.join(OUT, "fig_sec2_mouse_human_concordance.png"))
```

:::

That contrast, laid out in {numref}`fig-sec2-mouse-human-concordance`, is the section's sharpest illustration of a general vulnerability: when a defensible analytic choice can flip a model from "poorly mimics" to "greatly mimics" human disease {cite:p}`Seok2013, Takao2014`, the conclusion on translatability is being decided by analytic degrees of freedom rather than by the animals. More broadly, reviews of predictive validity conclude that animal models are weak predictors of human drug safety and efficacy across therapeutic areas {cite:p}`VanNorman2019, McGonigle2014, AKHTAR2015`, a judgement borne out by case histories: Hedgehog-pathway inhibitors, once hoped to treat a quarter of human cancers, responded clinically in only two rare tumour types {cite:p}`Curran2018`; of 101 highly promising basic-science findings, only five reached licensed clinical use two decades later {cite:p}`ContopoulosIoannidis2003`; creatine, neuroprotective in Parkinson's models, showed no benefit in trials of nearly 2,000 patients {cite:p}`Attia2017`; and umbilical-cord-blood therapy, significant across preclinical lung-injury outcomes, produced no reduction in the corresponding clinical endpoint {cite:p}`Purcell2024`. Even models that faithfully reproduce a human phenotype need not be fit for drug development {cite:p}`Cannon2023, Aquarius2023`; conversely, some models achieve high external validity yet are still run without any standard protocol {cite:p}`Brown2016, Bansal2017`. External validity as a whole has advanced far less than internal-validity reporting {cite:p}`Ferreira2020, Rongen2015`, reviews routinely extrapolate preclinical results to patients without first appraising the animal studies' risk of bias {cite:p}`Lamontagne2010`, and translational failure is sometimes traceable to mismatches as mundane as clinical outcome instruments too blunt to capture the effects seen in animals {cite:p}`Stein2015`, or to physics and dosimetry parameters that are left unreported in the majority of radiobiology papers and vary enough between institutions to require credentialing {cite:p}`Draeger2020, Ashraf2024`. Alzheimer's disease is the emblematic case: more than 300 interventions have been reported effective in animal models, with essentially none translating {cite:p}`Shineman2011, SukoffRizzo2020`.
:::{trust-claim}
:claim-id: clm_cb9aed4a07898448
:::
:::{trust-claim}
:claim-id: clm_7e24cfe7a3e30e5b
:::
:::{trust-claim}
:claim-id: clm_2078e0a82faac554
:::
:::{trust-claim}
:claim-id: clm_0517f3eec333e130
:::
:::{trust-claim}
:claim-id: clm_e6dc04569ed964e0
:::

The cumulative attrition at the clinical end of drug development is severe and, unlike the modeled irreproducibility costs, directly measured. Independent analyses converge on a likelihood of moving from first-in-human testing to approval of roughly 5–14%, as {numref}`fig-sec2-translational-attrition` shows: about 14% industry-wide {cite:p}`Schuhmacher2025, DiMasi2014`, falling to 5–7% in single oncology indications {cite:p}`Dhillon2022, Luo2026, Wasylewski2020`. Older and modeled estimates sit in the same range or below it — one in 33 compounds in castration-resistant prostate cancer {cite:p}`Tenuta2013`, an overall clinical success rate near 12% falling to 4% for Alzheimer's-type indications {cite:p}`Farid2020`, and 14–32% for antibody therapeutics {cite:p}`Crescioli2024` — and the roughly 90% attrition rate, attributed in part to species differences, is now cited as a rationale for the FDA Modernization Act 2.0's opening to non-animal methods {cite:p}`Zushin2023`. The case for those alternatives is sharpened by evidence that some animal assays are themselves poorly reproducible — the rabbit Draize irritation test reclassifies fewer than half of moderate irritants on retest {cite:p}`Raabe2024` — while human-cell systems can outperform them, as when a high-content screen of human hepatocytes predicted drug hepatotoxicity far more sensitively than conventional assays and three-dimensional human tissue models were built to the same end {cite:p}`OBrien2006, Tutty2025`.
:::{trust-claim}
:claim-id: clm_df0eb5e5969a21ab
:::
:::{trust-claim}
:claim-id: clm_0d62a1d590283d75
:::
:::{trust-claim}
:claim-id: clm_1c8c60b68c0d1bdd
:::

:::{figure} ../figures/fig_sec2_translational_attrition.png
:name: fig-sec2-translational-attrition
:width: 90%
**Convergent estimates of clinical development success.** Independent analyses place the phase-1-to-approval likelihood at roughly 5–14%: 14.3% industry-wide {cite:p}`Schuhmacher2025`, 14.3% for the top-10-firm self-originated subgroup {cite:p}`DiMasi2014`, 7% in gastric cancer {cite:p}`Dhillon2022`, 6.1% in lymphoma {cite:p}`Luo2026`, and 5% for paediatric oncology registration {cite:p}`Wasylewski2020`. The convergence quantifies the translational attrition downstream of preclinical animal studies; the shaded band spans the 5–14% range. Industry-wide all-indication estimates (Schuhmacher, DiMasi) are shown beside single-indication oncology estimates (Dhillon, Luo, Wasylewski), so part of the spread reflects indication, not a shared baseline. Denominators differ (active ingredients, agents, drugs, phase-1 trials); DiMasi's 14.3% is the top-10-firm self-originated subgroup, for which the paper also reports 16.4% and 18.4%, and Wasylewski's rate is per phase-1 trial for paediatric registration.
:::

:::{dropdown} 📓 Figure code

```python
import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# shared_style.py lives alongside this notebook in figures/notebooks/
sys.path.insert(0, os.path.abspath('.'))
from shared_style import COLORS, apply_style, save_figure
apply_style()
OUT = os.path.abspath('..')  # figures/ directory

# Data from evidence_section_02.json -> figure_data
# comparison_id: 'clinical-approval-success-rates' (audit ruling: CAVEAT).
# Every value has a value_source_sentence in the source record; none invented.
# (label, value %, category, reported-range low/high or None)
rows = [
    ("Schuhmacher\n2025", 14.3, "industry", (8.0, 23.0)),  # 10.1016/j.drudis.2025.104291
    ("DiMasi\n2014",      14.3, "industry", None),          # 10.1097/MJT.0b013e318269198f
    ("Dhillon\n2022",      7.0, "oncology",  None),          # 10.1097/COC.0000000000000963
    ("Luo\n2026",          6.1, "oncology",  None),          # 10.1182/bloodadvances.2025017752
    ("Wasylewski\n2020",   5.0, "oncology",  None),          # 10.1371/journal.pone.0234911
]
cat_color = {"industry": COLORS["actual_verified"], "oncology": COLORS["secondary_cat"]}
cat_hatch = {"industry": "", "oncology": "///"}

fig, ax = plt.subplots(figsize=(9.0, 5.6))
x = np.arange(len(rows))
ax.axhspan(5, 14, color=COLORS["neutral_baseline"], alpha=0.14, zorder=0)
ax.text(len(rows) - 0.5, 13.4, "convergent 5-14% range", ha="right", va="top",
        fontsize=10, color=COLORS["gray_700"], fontstyle="italic")

for i, (lab, val, cat, rng) in enumerate(rows):
    ax.bar(i, val, width=0.62, color=cat_color[cat], edgecolor=COLORS["ink"],
           linewidth=0.6, hatch=cat_hatch[cat], zorder=3)
    ax.text(i, val + 0.5, f"{val:g}%", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=COLORS["ink"])
    if rng is not None:
        lo, hi = rng
        ax.errorbar(i, val, yerr=[[val - lo], [hi - val]], fmt="none",
                    ecolor=COLORS["gray_700"], elinewidth=1.2, capsize=4, zorder=4)

ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows])
ax.set_ylabel("Phase-1-to-approval likelihood (%)"); ax.set_ylim(0, 25)
ax.set_title("Convergent estimates of clinical development success", pad=12)
handles = [
    mpatches.Patch(facecolor=cat_color["industry"], edgecolor=COLORS["ink"],
                   label="Industry-wide, all indications"),
    mpatches.Patch(facecolor=cat_color["oncology"], edgecolor=COLORS["ink"],
                   hatch="///", label="Single oncology indication"),
]
ax.legend(handles=handles, loc="upper right", frameon=True)
ax.text(0.0, -0.235,
        "Whisker on Schuhmacher = reported 8-23% across-company range. "
        "All values from source papers' abstracts.",
        transform=ax.transAxes, fontsize=9, color=COLORS["gray_500"], fontstyle="italic")
fig.tight_layout()
save_figure(fig, os.path.join(OUT, "fig_sec2_translational_attrition.png"))
```

:::

Taken together, the evidence assembled here establishes the empirical foundation the rest of this review builds on: the animal literature is systematically positive beyond what its power can justify, incompletely published and incompletely reported, weakly protected against bias, sensitive to biological and material variation that is rarely controlled, and a poor and analysis-dependent predictor of human outcomes. The near-universal framing of this evidence is as a scientific-quality problem — a matter of wasted money and papers that fail to replicate. What that framing omits is that every biased, underpowered, unpublished, or non-translating study was nonetheless paid for in animal lives, whose welfare cost is discharged whether or not the resulting data are ever trusted or reused. Recasting the reproducibility crisis as a problem of that unredeemed cost — as a failure of data welfare, and of the obligations the 3Rs already impose on how animal-derived data are stewarded — is the task of {ref}`sec-data-welfare`, which argues that letting hard-won animal data go to waste is not merely poor science but a welfare harm in its own right.

:::{evidence-explorer}
:evidence-dir: ../evidence
:section: section_02
:height: 800px
:::

(sec-virtual-controls)=

# Virtual Control Groups and Data Reuse as Reduction

The previous section closed on a paradox: the machinery for sharing preclinical data is elaborate, yet {ref}`sec-fair-preclinical` showed that generic mandates and repositories rarely convert stored bytes into a second scientific use. This section takes up the clearest exception to that pattern. When the data being reused is a specific, tightly regulated type — the control-animal arm of a toxicity or carcinogenicity study — reuse stops being an abstraction and becomes a countable act of the 3Rs. A control group reconstructed from curated historical records, rather than freshly dosed with vehicle, is a group of animals that never enters the study. This is the concrete mechanism by which stewardship of animal-derived data discharges part of the ethical debt: the welfare cost of the original controls is amortised across every later study that borrows them. Framed this way, the reuse of control data is not merely good data hygiene but a direct Reduction intervention, and several strands of the literature now treat efficient reuse of existing animal data as an ethical obligation rather than a convenience. {cite:p}`Potter2024, PetitDemouliere2026, Landes2018, Harrell2024` The argument of this section is that virtual control groups (VCGs) and their clinical cousins — shared control databases, Bayesian borrowing, and external control arms — deliver a real and quantifiable Reduction dividend, but one that is conditional: it is bought against endpoint-dependent concordance, temporal and cross-laboratory drift, and a regulatory acceptance gap that leaves part of the dividend still theoretical.

:::{trust-claim}
:claim-id: clm_d9da8c9c3e2a5bdf
:claim: Framed this way, the reuse of control data is not merely good data hygiene but a direct Reduction intervention, and several strands of the literature now treat efficient reuse of existing animal data as an ethical obligation rather than a convenience.
:cites: Potter2024, PetitDemouliere2026, Landes2018, Harrell2024
:claim-type: review_synthesis
:modality: likely
:::

## The size of the Reduction dividend

The headline figure attached to virtual control groups is remarkably stable. The proposal that launched the concept in preclinical toxicology argued that a repository of historical animal control data could be assembled into VCGs and that doing so carried a potential of roughly a 25% reduction in animal use by replacing the concurrent control arm. {cite:p}`StegerHartmann2020` Subsequent method-development work repeated the same magnitude: VCGs built from historical control data can cut the number of concurrent control animals in regulatory toxicity studies by up to 25%, with initial body weight identified as a critical matching covariate, {cite:p}`Gurjanov2024b` and a review of the proof-of-concept studies frames the same up-to-25% reduction as the central attraction of the approach. {cite:p}`Adedeji2024` An independent estimate from a Japanese industry-regulatory perspective puts the saving somewhat higher, at approximately 30%, while cataloguing the obstacles that remain because current guidelines still mandate concurrent controls for pivotal studies. {cite:p}`SATO2024` {numref}`fig-sec5-vcg-reduction` collects these convergent estimates. Their agreement is reassuring but must be read with care, because two of the preclinical figures cite the original 25% concept rather than deriving it afresh, so the convergence reflects a shared source as much as independent replication. {cite:p}`StegerHartmann2020, Gurjanov2024b, Adedeji2024` The magnitude is nonetheless a defensible planning number, and its ethical translation is unambiguous: at industrial scale, a quarter of control animals in repeat-dose studies represents a large standing population.

:::{trust-claim}
:claim-id: clm_dd68d8c0b5482ffe
:claim: The proposal that launched the concept in preclinical toxicology argued that a repository of historical animal control data could be assembled into VCGs and that doing so carried a potential of roughly a 25% reduction in animal use by replacing the concurrent control arm.
:cites: StegerHartmann2020
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_7525523bdd2e915f
:claim: Subsequent method-development work repeated the same magnitude: VCGs built from historical control data can cut the number of concurrent control animals in regulatory toxicity studies by up to 25%, with initial body weight identified as a critical matching covariate, and a review of the proof-of-concept studies frames the same up-to-25% reduction as the central attraction of the approach.
:cites: Gurjanov2024b, Adedeji2024
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_27cf6be0f5680752
:claim: An independent estimate from a Japanese industry-regulatory perspective puts the saving somewhat higher, at approximately 30%, while cataloguing the obstacles that remain because current guidelines still mandate concurrent controls for pivotal studies.
:cites: SATO2024
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_a1c4b1875a1cafb0
:claim: Their agreement is reassuring but must be read with care, because two of the preclinical figures cite the original 25% concept rather than deriving it afresh, so the convergence reflects a shared source as much as independent replication.
:cites: StegerHartmann2020, Gurjanov2024b, Adedeji2024
:claim-type: limitation
:modality: likely
:::

:::{figure} ../figures/fig_sec5_vcg_reduction.png
:name: fig-sec5-vcg-reduction
:width: 100%
**A convergent quarter, and its clinical analogue.** Estimated reduction in animal or patient numbers from reusing control data. Panel (a): three preclinical proposals converge on a ~25% reduction in control animals from replacing concurrent controls with virtual control groups. {cite:p}`StegerHartmann2020, Gurjanov2024b, Adedeji2024` These three estimates are not independent — the later two cite the original 25% control-animal-reduction concept rather than re-deriving it, so the panel shows convergence on a shared figure, not three separate measurements. Panel (b): a human cardiovascular medical-device trial using Bayesian dynamic borrowing from congruent historical controls enrolled about 1,497 rather than 2,386 patients, an approximately 37% enrolment reduction across both arms. {cite:p}`Chiaruttini2025` The clinical value is a patient-enrolment reduction spanning both trial arms — a different species, population, unit, and scope from the animal control-group reductions in panel (a) — and the two panels are therefore plotted on separate axes and must not be read as a single scale.
:::

:::{dropdown} 📓 Figure code

```python
"""fig_sec5_vcg_reduction — Reduction dividend of virtual control groups.

Two panels (never one axis, per the figure comparability decision):
  (a) three preclinical VCG proposals converging on ~25% control-animal
      reduction (non-independent estimates, annotated);
  (b) a human device-trial Bayesian-borrowing enrolment reduction
      (~37%, both arms) — different species/unit/scope, plotted separately.

Data are read from the section evidence file; study labels come from the
section author-name table; colours from shared_style (Okabe-Ito).
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt


def _repo_path(rel):
    for base in ['.', '..', '../..', '../../..', os.path.dirname(os.path.abspath(__file__)) + '/../..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


# style module lives alongside the notebooks
import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_05.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_05.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_05.json'), encoding='utf-8'))


def label_for(doi):
    a = AT[CM[doi]]
    return "%s\n%s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'vcg-hcd-animal-reduction-estimates')
papers = fd['papers']

# Panel A: preclinical percentage reductions (value like "25%")
pre = [p for p in papers if str(p['value']).strip().endswith('%')]
# Panel B: clinical device-trial enrolment (value like "1,497 vs 2,386")
dev = next(p for p in papers if 'vs' in str(p['value']))

pre_labels = [label_for(p['doi']) for p in pre]
pre_vals = [float(str(p['value']).replace('%', '')) for p in pre]
pre_abstract = [p['text_access'] != 'fulltext' for p in pre]

dev_after, dev_before = [int(s.replace(',', '').strip())
                         for s in str(dev['value']).split('vs')]
dev_reduction = 100.0 * (dev_before - dev_after) / dev_before

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 6.2),
                               gridspec_kw={'width_ratios': [3, 2]})

# ── Panel A: preclinical control-animal reduction ──
xA = np.arange(len(pre))
barsA = axA.bar(xA, pre_vals, width=0.62, color=COLORS['repayment'],
                edgecolor=COLORS['ink'], linewidth=0.5, hatch='//', zorder=3)
for i, (b, v, ab) in enumerate(zip(barsA, pre_vals, pre_abstract)):
    txt = ("%d%%" % v) + ('*' if ab else '')
    axA.text(b.get_x() + b.get_width() / 2, v + 0.6, txt,
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color=COLORS['ink'])
axA.axhline(25, color=COLORS['neutral_baseline'], lw=0.75, ls='--', zorder=1)
axA.set_xticks(xA)
axA.set_xticklabels(pre_labels, fontsize=10.5)
axA.set_ylim(0, 33)
axA.set_ylabel('Control-animal reduction (%)')
axA.set_title('(a) Preclinical: virtual control groups', fontsize=13, loc='left')
axA.annotate('Not independent: the later two cite the\noriginal 25% concept, not re-derive it',
             xy=(1.0, 25), xytext=(0.15, 31),
             fontsize=9.5, color=COLORS['ink'],
             ha='left', va='center')

# ── Panel B: clinical enrolment reduction (before/after) ──
xB = np.array([0, 1])
valsB = [dev_before, dev_after]
colB = [COLORS['neutral_baseline'], COLORS['secondary_cat']]
barsB = axB.bar(xB, valsB, width=0.6, color=colB,
                edgecolor=COLORS['ink'], linewidth=0.5, zorder=3)
for b, v in zip(barsB, valsB):
    axB.text(b.get_x() + b.get_width() / 2, v + 40, "{:,}".format(v),
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color=COLORS['ink'])
axB.set_xticks(xB)
axB.set_xticklabels(['Frequentist\n(no borrowing)', 'Bayesian borrowing\n(congruent)'],
                    fontsize=10.5)
axB.set_ylim(0, dev_before * 1.22)
axB.set_ylabel('Enrolled patients (both arms)')
axB.set_title('(b) Clinical: %s' % label_for(dev['doi']).replace('\n', ' '),
              fontsize=13, loc='left')
# reduction bracket
ytop = dev_before * 1.10
axB.annotate('', xy=(1, dev_after + 40), xytext=(1, ytop),
             arrowprops=dict(arrowstyle='-', color=COLORS['ink'], lw=0.8))
axB.annotate('', xy=(0, dev_before + 40), xytext=(0, ytop),
             arrowprops=dict(arrowstyle='-', color=COLORS['ink'], lw=0.8))
axB.annotate('', xy=(0, ytop), xytext=(1, ytop),
             arrowprops=dict(arrowstyle='<->', color=COLORS['debt'], lw=1.4))
axB.text(0.5, ytop + 30, '~%d%% fewer' % round(dev_reduction),
         ha='center', va='bottom', fontsize=11.5, fontweight='bold',
         color=COLORS['debt'])

fig.text(0.01, -0.02,
         "* value from abstract; full text not accessible. "
         "Panels use different units (animals vs trial participants) and separate axes — not a common scale.",
         fontsize=9, color=COLORS['gray_500'], ha='left', style='italic')

fig.tight_layout()
out = _repo_path('figures') + '/fig_sec5_vcg_reduction.png'
save_figure(fig, out)
print('saved:', out)
```

:::

That the same logic operates in human trials strengthens the case that data reuse is a genuine Reduction lever rather than a toxicology curiosity. In clinical statistics the corresponding move is Bayesian borrowing: information from historical or external control patients is folded into the analysis so that fewer participants need to be randomised to the current control arm. A group-sequential device trial that borrowed from four heterogeneous historical control studies enrolled roughly 1,497 rather than 2,386 patients under scenarios where the historical and current data were congruent — about a 37% enrolment reduction — while holding Type I error and power at nominal levels, despite substantial between-study heterogeneity in the borrowed data (I² of 92%). {cite:p}`Chiaruttini2025` The foundational meta-analytic-predictive approach quantifies exactly how much a historical control arm is worth: 930 control patients across eleven historical trials, with small heterogeneity, translated into a prior worth about ninety patients, {cite:p}`Neuenschwander2010` and its extension to over-dispersed lesion counts valued 1,936 historical controls from nine multiple-sclerosis trials at a prior of about forty-five patients, meaning a new control arm could be shrunk by that many recruits. {cite:p}`Gsteiger2013` Panel (b) of {numref}`fig-sec5-vcg-reduction` shows the device-trial case; the preclinical and clinical dividends are plotted separately precisely because their units — control animals versus trial participants across both arms — are not interchangeable. What unites them is the principle that a well-characterised historical control carries reusable information, and that harvesting it lets the next study be smaller.

:::{trust-claim}
:claim-id: clm_3d63bd98975b6b39
:claim: A group-sequential device trial that borrowed from four heterogeneous historical control studies enrolled roughly 1,497 rather than 2,386 patients under scenarios where the historical and current data were congruent — about a 37% enrolment reduction — while holding Type I error and power at nominal levels, despite substantial between-study heterogeneity in the borrowed data (I2 of 92%).
:cites: Chiaruttini2025
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_f5d1b5a917155882
:claim: The foundational meta-analytic-predictive approach quantifies exactly how much a historical control arm is worth: 930 control patients across eleven historical trials, with small heterogeneity, translated into a prior worth about ninety patients, and its extension to over-dispersed lesion counts valued 1,936 historical controls from nine multiple-sclerosis trials at a prior of about forty-five patients, meaning a new control arm could be shrunk by that many recruits.
:cites: Neuenschwander2010, Gsteiger2013
:claim-type: methodological
:modality: established
:::

Preclinical VCG work has now moved past pure proposal into retrospective demonstration. A framework benchmarking VCGs against three four-week rat oral-toxicity studies asked whether reconstructed controls could reproduce the significant deviations and study conclusions obtained with real concurrent controls, {cite:p}`Gurjanov2024a` and a retrospective application to twenty pilot studies reported that VCGs maintained toxicological power and biological relevance while reducing animal usage, explicitly in the context of the FDA Modernization Act 2.0. {cite:p}`Lotfi2026` Analyses of the eTOX database found that VCGs best reproduced toxicologists' original determinations of treatment-relatedness for histopathology when matched at the highest covariate similarity — same species, strain, sex, route and vehicle. {cite:p}`Wright2023b` Proof-of-concept studies have converged on which covariates matter most for matching a virtual to a concurrent control — sex, route of administration, fasting status and body weight at study initiation {cite:p}`Andaya2024` — and laboratories running harmonised developmental and reproductive toxicity studies are already being encouraged to plan VCG implementation. {cite:p}`Wise2025` The pressure to adopt these methods is sharpest for non-human primates, where supply constraints and 3Rs expectations have prompted formal proposals to reduce the number of control primates euthanised in nonclinical studies, {cite:p}`Guffroy2025` and where re-analysis suggests the concurrent control can sometimes be omitted altogether without losing the study's key conclusions. {cite:p}`Mecklenburg2023` Adjacent reduction strategies that reuse accumulated study experience rather than control animals per se — trimming redundant recovery cohorts or shortening chronic studies — point the same way: a cross-company review found recovery animals included in roughly two-thirds of monoclonal-antibody safety studies, often without justification, {cite:p}`Prior2023, Sewell2014` and larger surveys concluded that chronic studies revealed no new toxicities of human concern for the large majority of molecules, supporting shorter designs and fewer animals. {cite:p}`Prior2024, Booler2026, SalianMehta2024`

:::{trust-claim}
:claim-id: clm_87a21fcbb95c67f4
:claim: A framework benchmarking VCGs against three four-week rat oral-toxicity studies asked whether reconstructed controls could reproduce the significant deviations and study conclusions obtained with real concurrent controls, and a retrospective application to twenty pilot studies reported that VCGs maintained toxicological power and biological relevance while reducing animal usage, explicitly in the context of the FDA Modernization Act 2.0.
:cites: Gurjanov2024a, Lotfi2026
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_b57e7793a3284a1b
:claim: Analyses of the eTOX database found that VCGs best reproduced toxicologists' original determinations of treatment-relatedness for histopathology when matched at the highest covariate similarity — same species, strain, sex, route and vehicle.
:cites: Wright2023b
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_042943aa9ceefcc0
:claim: Proof-of-concept studies have converged on which covariates matter most for matching a virtual to a concurrent control — sex, route of administration, fasting status and body weight at study initiation — and laboratories running harmonised developmental and reproductive toxicity studies are already being encouraged to plan VCG implementation.
:cites: Andaya2024, Wise2025
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_911b7fd76e97ac48
:claim: The pressure to adopt these methods is sharpest for non-human primates, where supply constraints and 3Rs expectations have prompted formal proposals to reduce the number of control primates euthanised in nonclinical studies, and where re-analysis suggests the concurrent control can sometimes be omitted altogether without losing the study's key conclusions.
:cites: Guffroy2025, Mecklenburg2023
:claim-type: empirical
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_acba205e10c66d41
:claim: Adjacent reduction strategies that reuse accumulated study experience rather than control animals per se — trimming redundant recovery cohorts or shortening chronic studies — point the same way: a cross-company review found recovery animals included in roughly two-thirds of monoclonal-antibody safety studies, often without justification, and larger surveys concluded that chronic studies revealed no new toxicities of human concern for the large majority of molecules, supporting shorter designs and fewer animals.
:cites: Prior2023, Sewell2014, Prior2024, Booler2026, SalianMehta2024
:claim-type: review_synthesis
:modality: likely
:::

## The infrastructure already exists

A Reduction strategy that depends on reusing historical control data is only credible if that data exists in usable quantity. Here the contrast with the general FAIR failure of {ref}`sec-fair-preclinical` is stark: for this narrow, high-value data type, the raw material has already accumulated at industrial scale. Curated resources span from decades-old pathology consortia to contemporary regulatory repositories, and {numref}`fig-sec5-shared-control-scale` summarises their magnitudes. The RITA shared industry database standardised tissue sampling, nomenclature and peer review, and by around 2002 already held 10,896 rats from 106 studies with more than 17,604 primary tumours to contextualise rare or marginal findings, {cite:p}`Deschl2002` a model soon copied by the North American Control Animal Database. {cite:p}`Keenan2002` The Innovative Medicines Initiative built on this foundation at a far larger scale: the eTRANSAFE project integrated some 6,500 legacy studies from the earlier eTOX effort {cite:p}`Pognan2021` and collected and analysed control and toxicology data from more than 60,000 rats, 1,300 dogs and 500 monkeys expressly to make virtual control groups feasible. {cite:p}`Moresis2024` On the regulatory side, the FDA CDER repository of studies submitted in the SEND standard grew from more than 1,800 studies queried in 2020 {cite:p}`Carfagna2020b` to over 10,000 datasets a few years later, {cite:p}`Snyder2024` and individual corporate databases have supported meta-analyses aggregating tens of thousands of animals — one spanning 24,358 animals and more than 232,000 histological observations across hundreds of studies. {cite:p}`MunozMuriedas2021` The successor project VICT3R is explicitly assembling a standardised, annotated control-animal database with the stated aim of obtaining regulatory acceptance for the VCG concept. {cite:p}`StegerHartmann2024, Sanz2025`

:::{trust-claim}
:claim-id: clm_747c34d6b2e9babe
:claim: The RITA shared industry database standardised tissue sampling, nomenclature and peer review, and by around 2002 already held 10,896 rats from 106 studies with more than 17,604 primary tumours to contextualise rare or marginal findings, a model soon copied by the North American Control Animal Database.
:cites: Deschl2002, Keenan2002
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_a196f0a02e97b37f
:claim: The Innovative Medicines Initiative built on this foundation at a far larger scale: the eTRANSAFE project integrated some 6,500 legacy studies from the earlier eTOX effort and collected and analysed control and toxicology data from more than 60,000 rats, 1,300 dogs and 500 monkeys expressly to make virtual control groups feasible.
:cites: Pognan2021, Moresis2024
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_5591e45f4d3361a4
:claim: On the regulatory side, the FDA CDER repository of studies submitted in the SEND standard grew from more than 1,800 studies queried in 2020 to over 10,000 datasets a few years later, and individual corporate databases have supported meta-analyses aggregating tens of thousands of animals — one spanning 24,358 animals and more than 232,000 histological observations across hundreds of studies.
:cites: Carfagna2020b, Snyder2024, MunozMuriedas2021
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e49f8b272ae4c791
:claim: The successor project VICT3R is explicitly assembling a standardised, annotated control-animal database with the stated aim of obtaining regulatory acceptance for the VCG concept.
:cites: StegerHartmann2024, Sanz2025
:claim-type: empirical
:modality: likely
:::

:::{figure} ../figures/fig_sec5_shared_control_scale.png
:name: fig-sec5-shared-control-scale
:width: 100%
**The reuse infrastructure is already built.** Scale of shared preclinical control and nonclinical-data resources, split by counting unit because the entries are not rank-comparable on a common measure. Panel (a), animal counts (log axis): 10,896 control rats in RITA {cite:p}`Deschl2002` and more than 60,000 rats plus 1,300 dogs and 500 monkeys in eTRANSAFE. {cite:p}`Moresis2024` Panel (b), study and dataset counts (log axis): 6,500 legacy studies integrated from eTOX into eTRANSAFE {cite:p}`Pognan2021` and the FDA CDER SEND repository growing from more than 1,800 studies in 2020 {cite:p}`Carfagna2020b` to more than 10,000 datasets in 2024. {cite:p}`Snyder2024` The two FDA CDER SEND counts are the same repository at two time points — a growth series, not two independent resources — and are shown connected. Counts are in different units (animals versus studies versus datasets) and must not be compared across panels. The bottleneck for control-data reuse is therefore acceptance and stewardship, not data volume.
:::

:::{dropdown} 📓 Figure code

```python
"""fig_sec5_shared_control_scale — scale of shared control/nonclinical data.

Panelled by counting unit (animals vs studies/datasets) because the entries
are NOT rank-comparable on one axis; log axis within each panel; the two FDA
CDER SEND counts (2020 studies -> 2024 datasets) are collapsed into one growth
series, not two independent resources. Per the figure comparability decision.
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt


def _repo_path(rel):
    for base in ['.', '..', '../..', '../../..', os.path.dirname(os.path.abspath(__file__)) + '/../..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_05.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_05.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_05.json'), encoding='utf-8'))


def yr(doi):
    return AT[CM[doi]]['year']


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'shared-control-database-scale')
byd = {p['doi']: p for p in fd['papers']}

DOI_RITA = '10.1080/01926230252824743'   # Deschl2002
DOI_ETR = '10.1038/s41684-024-01335-0'   # Moresis2024
DOI_ETOX = '10.3390/ph14030237'          # Pognan2021
DOI_CDER20 = '10.1021/acs.chemrestox.0c00317'  # Carfagna2020b
DOI_CDER24 = '10.3389/ftox.2024.1392686'       # Snyder2024

# Panel A — animal counts (log). RITA rats; eTRANSAFE rats/dogs/monkeys.
animalsA = [
    ('RITA\nrats\n(%s)' % yr(DOI_RITA), 10896, COLORS['actual_verified']),
    ('eTRANSAFE\nrats\n(%s)' % yr(DOI_ETR), 60000, COLORS['repayment']),
    ('eTRANSAFE\ndogs\n(%s)' % yr(DOI_ETR), 1300, COLORS['repayment']),
    ('eTRANSAFE\nmonkeys\n(%s)' % yr(DOI_ETR), 500, COLORS['repayment']),
]

# Panel B — study / dataset counts (log). eTOX studies; FDA CDER SEND growth.
studiesB = [
    ('eTOX\nstudies\n(%s)' % yr(DOI_ETOX), 6500, COLORS['actual_verified'], 'studies'),
    ('FDA CDER SEND\nstudies (%s)' % yr(DOI_CDER20), 1800, COLORS['conflict'], 'studies'),
    ('FDA CDER SEND\ndatasets (%s)' % yr(DOI_CDER24), 10000, COLORS['conflict'], 'datasets'),
]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 6.6),
                               gridspec_kw={'width_ratios': [4, 3]})


def draw_bars(ax, rows, title):
    x = np.arange(len(rows))
    vals = [r[1] for r in rows]
    cols = [r[2] for r in rows]
    bars = ax.bar(x, vals, width=0.62, color=cols, edgecolor=COLORS['ink'],
                  linewidth=0.5, zorder=3)
    ax.set_yscale('log')
    ax.set_ylim(100, 200000)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.10,
                (">%s" % "{:,}".format(v)) if v in (1800, 10000, 60000, 6500) else "{:,}".format(v),
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                color=COLORS['ink'])
    ax.set_xticks(x)
    ax.set_xticklabels([r[0] for r in rows], fontsize=10)
    ax.set_title(title, fontsize=13, loc='left')
    ax.grid(axis='y', which='both', color=COLORS['gray_300'], lw=0.4, zorder=0)
    return x


xA = draw_bars(axA, animalsA, '(a) Animals with reusable control data')
axA.set_ylabel('Count (log scale)')

xB = draw_bars(axB, studiesB, '(b) Studies / datasets')
# growth arrow between the two FDA CDER SEND bars (same repository over time)
axB.annotate('', xy=(2, 10000 * 0.9), xytext=(1, 1800 * 1.1),
             arrowprops=dict(arrowstyle='->', color=COLORS['debt'], lw=1.6,
                             connectionstyle='arc3,rad=-0.25'))
axB.text(1.5, 3600, 'same repository,\n2020 → 2024 growth', ha='center', va='center',
         fontsize=9, color=COLORS['debt'], style='italic')

fig.text(0.01, -0.02,
         "Counts are in different units (animals vs studies vs datasets) and are not rank-comparable across panels. "
         "The two FDA CDER SEND counts are the same repository at different times (growth), not independent resources.",
         fontsize=9, color=COLORS['gray_500'], ha='left', style='italic')

fig.tight_layout()
out = _repo_path('figures') + '/fig_sec5_shared_control_scale.png'
save_figure(fig, out)
print('saved:', out)
```

:::

The existence of the data does not settle its usability, and the same quality problems that afflict sharing generally reappear here in specific form. Querying the SEND repository showed that the frequency with which required fields were actually populated ranged from 6% to 99%, and that fields such as vehicle name, animal supplier and test facility could not be extracted automatically without further harmonisation. {cite:p}`Carfagna2020b, Carfagna2020a` Pooling control data across laboratories presupposes a shared diagnostic language, which is why the standardised INHAND lesion nomenclature — extended over the past decade to non-human primates, dogs, minipigs, rabbits and reproductive tissues — is a precondition for any cross-study control database. {cite:p}`Colman2021, Woicke2021, Skydsgaard2021, Schafer2024, Keenan2024` That nomenclature is neither complete nor static: forum opinions note gaps requiring new terms for medical-device studies, {cite:p}`Schuh2025` revisions continue to appear a decade after the original tissue publications, {cite:p}`Bachchair2025` and satellite symposia have documented cases where neither INHAND nor SEND contained a term matching an observed lesion. {cite:p}`Quist2023` Efforts to define a minimal metadata set for repurposing nonclinical in vivo data are a direct response to this friction. {cite:p}`Moresis2024` The persistent obstacle is as much commercial as technical: the single biggest barrier to building shared preclinical safety databases has been the unwillingness of sponsors to share proprietary data, {cite:p}`StegerHartmann2018` and even with the data assembled, reuse has intrinsic analytical limits — a likelihood-ratio analysis of the same eTOX database found inter-species histopathological concordance to be rare. {cite:p}`Wright2023a` The lesson is that data volume is a solved problem for control-animal data in a way it is not for the long tail of preclinical research; the unsolved problems are curation, comparability and acceptance.

:::{trust-claim}
:claim-id: clm_6668374c08ef06dd
:claim: Querying the SEND repository showed that the frequency with which required fields were actually populated ranged from 6% to 99%, and that fields such as vehicle name, animal supplier and test facility could not be extracted automatically without further harmonisation.
:cites: Carfagna2020b, Carfagna2020a
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_6d2439a0b4027810
:claim: Pooling control data across laboratories presupposes a shared diagnostic language, which is why the standardised INHAND lesion nomenclature — extended over the past decade to non-human primates, dogs, minipigs, rabbits and reproductive tissues — is a precondition for any cross-study control database.
:cites: Colman2021, Woicke2021, Skydsgaard2021, Schafer2024, Keenan2024
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_7dd72270ce35fea3
:claim: That nomenclature is neither complete nor static: forum opinions note gaps requiring new terms for medical-device studies, revisions continue to appear a decade after the original tissue publications, and satellite symposia have documented cases where neither INHAND nor SEND contained a term matching an observed lesion.
:cites: Schuh2025, Bachchair2025, Quist2023
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e1cffacb3a5d6291
:claim: Efforts to define a minimal metadata set for repurposing nonclinical in vivo data are a direct response to this friction.
:cites: Moresis2024
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_59da77f356da88f0
:claim: The persistent obstacle is as much commercial as technical: the single biggest barrier to building shared preclinical safety databases has been the unwillingness of sponsors to share proprietary data, and even with the data assembled, reuse has intrinsic analytical limits — a likelihood-ratio analysis of the same eTOX database found inter-species histopathological concordance to be rare.
:cites: StegerHartmann2018, Wright2023a
:claim-type: empirical
:modality: likely
:::

## How faithfully do virtual controls reproduce real ones?

The empirical heart of the VCG case is concordance: when the concurrent control is replaced by a virtual one, do the study's conclusions survive? The evidence does not deliver a single clear answer, and the disagreement is instructive rather than incidental. A large simulation replacing concurrent controls across forty Wistar Han rat studies found that VCGs reproduced effect-size decisions on liver enzymes with at least 90% agreement in 68.5% of comparisons, and that a hybrid design retaining half of the real controls raised full agreement from 46.9% to 76.7% while cutting full disagreement from 2.6% to 0.15%. {cite:p}`DuchateauNguyen2026` Re-analysing twenty sub-chronic non-human-primate studies with the concurrent control omitted, 82% of statistically significant parameter differences were confirmed by a mixed-design model, and all four dose-limiting toxicities were identifiable without any reference to the concurrent control. {cite:p}`Mecklenburg2023` A retrospective study of nonrodent one-month studies went further, reporting that propensity-score-matched virtual controls yielded similar or higher sensitivity than concurrent controls to detect effects on body weight and clinical pathology when fold-change from baseline was used. {cite:p}`Li2024a` Set against these encouraging results is the clinical-pathology finding that when concurrent controls were replaced with virtual ones in three legacy studies, 31%, 40% and 49% of quantitative parameters became statistically non-reproducible. {cite:p}`Adedeji2024`

:::{trust-claim}
:claim-id: clm_6b14a2d6ac16d4d7
:claim: A large simulation replacing concurrent controls across forty Wistar Han rat studies found that VCGs reproduced effect-size decisions on liver enzymes with at least 90% agreement in 68.5% of comparisons, and that a hybrid design retaining half of the real controls raised full agreement from 46.9% to 76.7% while cutting full disagreement from 2.6% to 0.15%.
:cites: DuchateauNguyen2026
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_777a97aa2de7a2fa
:claim: Re-analysing twenty sub-chronic non-human-primate studies with the concurrent control omitted, 82% of statistically significant parameter differences were confirmed by a mixed-design model, and all four dose-limiting toxicities were identifiable without any reference to the concurrent control.
:cites: Mecklenburg2023
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_15f6b1f32a733ae9
:claim: A retrospective study of nonrodent one-month studies went further, reporting that propensity-score-matched virtual controls yielded similar or higher sensitivity than concurrent controls to detect effects on body weight and clinical pathology when fold-change from baseline was used.
:cites: Li2024a
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_5c15fa31f0344f82
:claim: Set against these encouraging results is the clinical-pathology finding that when concurrent controls were replaced with virtual ones in three legacy studies, 31%, 40% and 49% of quantitative parameters became statistically non-reproducible.
:cites: Adedeji2024
:claim-type: empirical
:modality: contested
:::

:::{admonition} Evidence conflict: concordance versus non-reproducibility
:class: warning
The two most direct tests of virtual-control fidelity reach opposite-sounding conclusions. A liver-enzyme simulation reports that virtual and concurrent controls agree to within 90% on effect size in roughly two-thirds of comparisons, and that a hybrid design pushes full agreement above three-quarters. {cite:p}`DuchateauNguyen2026` A review of proof-of-concept studies reports that up to 49% of quantitative clinical-pathology parameters become non-reproducible when the concurrent control is replaced. {cite:p}`Adedeji2024` The conflict is largely one of endpoint and framing rather than of fact: the two studies emphasise different parameter classes, and one reports agreement while the other reports its complement. Expressed on a common direction, the clinical-pathology result corresponds to roughly 51–69% of parameters remaining reproducible — lower than the liver-enzyme agreement but not its negation. The dispute is genuine and unresolved, but it points to an endpoint-specific tradeoff, not a global pass or fail for the method.

:::

:::{trust-claim}
:claim-id: clm_749b8eafc0bb2cce
:claim: A liver-enzyme simulation reports that virtual and concurrent controls agree to within 90% on effect size in roughly two-thirds of comparisons, and that a hybrid design pushes full agreement above three-quarters.
:cites: DuchateauNguyen2026
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_6d0961cb7957779d
:claim: A review of proof-of-concept studies reports that up to 49% of quantitative clinical-pathology parameters become non-reproducible when the concurrent control is replaced.
:cites: Adedeji2024
:claim-type: empirical
:modality: contested
:::

Reconciling these results requires putting them on a common footing, which {numref}`fig-sec5-vcg-concordance` does. The apparent contradiction shrinks once polarity is harmonised: Adedeji's 49% is a non-reproducibility rate in which higher is worse, whereas the 82% and 68.5% figures are concordance rates in which higher is better. {cite:p}`Adedeji2024, Mecklenburg2023, DuchateauNguyen2026` Read as reproducibility, the clinical-pathology result becomes roughly 51–69% — the low end of a spectrum rather than a refutation. What remains after harmonisation is a real, endpoint-dependent gradient: robust categorical decisions such as dose-limiting toxicities and treatment-relatedness of histopathology survive control substitution well, whereas continuous clinical-pathology parameters, which are sensitive to small mean shifts, survive it least well. This is why cautious voices insist that VCGs be assessed for whether they lower a study's sensitivity to detect adverse effects, thresholds or biomarkers before they are trusted for regulatory decisions, {cite:p}`StegerHartmann2023, Golden2023` and why the anatomic-pathology community argues that validation demands running the virtual and full concurrent control in parallel across varying durations, with digital histopathology slides included in any validated database. {cite:p}`Grevot2023`

:::{trust-claim}
:claim-id: clm_b20a66a2a31cec7f
:claim: The apparent contradiction shrinks once polarity is harmonised: Adedeji's 49% is a non-reproducibility rate in which higher is worse, whereas the 82% and 68.5% figures are concordance rates in which higher is better.
:cites: Adedeji2024, Mecklenburg2023, DuchateauNguyen2026
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_3108725567111b08
:claim: This is why cautious voices insist that VCGs be assessed for whether they lower a study's sensitivity to detect adverse effects, thresholds or biomarkers before they are trusted for regulatory decisions, and why the anatomic-pathology community argues that validation demands running the virtual and full concurrent control in parallel across varying durations, with digital histopathology slides included in any validated database.
:cites: StegerHartmann2023, Golden2023, Grevot2023
:claim-type: methodological
:modality: likely
:::

:::{figure} ../figures/fig_sec5_vcg_concordance.png
:name: fig-sec5-vcg-concordance
:width: 100%
**The tradeoff is endpoint-specific, not a single overall answer.** Concordance between virtual or omitted-concurrent-control analyses and true concurrent controls, harmonised to a single direction (higher = more reproducible). Omitting the concurrent control confirmed 82% of significant non-human-primate parameters; {cite:p}`Mecklenburg2023` virtual controls reproduced rat liver-enzyme decisions with at least 90% agreement in 68.5% of comparisons; {cite:p}`DuchateauNguyen2026` and rat clinical-pathology parameters remained reproducible in roughly 51–69% of cases. {cite:p}`Adedeji2024` The green segment of each bar is the reproducible or concordant fraction; the orange segment is the residual discordance. The clinical-pathology value is plotted from the worst of a 31–49% non-reproducibility range (i.e. 51% reproducible) with the 51–69% range annotated: Adedeji's 49% is a non-reproducibility rate (higher = worse), the opposite polarity to the concordance rates, and on a common direction corresponds to ~51–69% reproducible. Species and construct differ across the three bars — NHP parameter-confirmation, rat effect-size agreement, and rat clinical-pathology reproducibility — so the bars illustrate an endpoint-dependent gradient rather than a single comparable metric.
:::

:::{dropdown} 📓 Figure code

```python
"""fig_sec5_vcg_concordance — VCG-vs-concurrent-control concordance.

Polarity harmonised to a single direction (higher = more reproducible /
concordant), per the figure comparability decision. Adedeji's non-
reproducibility rate (31-49%, higher = worse) is converted to reproducibility
(51-69%, worst case plotted with the range annotated). Each bar is split into
a green reproducible/concordant fraction and an orange residual-discordance
fraction to 100%. Construct and species are labelled.
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def _repo_path(rel):
    for base in ['.', '..', '../..', '../../..', os.path.dirname(os.path.abspath(__file__)) + '/../..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_05.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_05.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_05.json'), encoding='utf-8'))


def disp(doi):
    a = AT[CM[doi]]
    return "%s %s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'vcg-concurrent-control-concordance')
byd = {p['doi']: p for p in fd['papers']}

DOI_MECK = '10.1371/journal.pone.0282404'
DOI_DUCH = '10.3389/fphar.2026.1704002'
DOI_ADED = '10.1177/01926233241300310'

# Harmonised reproducibility / concordance values (higher = better)
meck = 82.0                    # 82% of significant NHP parameters confirmed
duch = 68.5                    # >=90% agreement in 68.5% of comparisons
aded_low, aded_high = 51.0, 69.0   # 100 - (49, 31)

rows = [
    (disp(DOI_MECK), meck, meck,
     'NHP\nparameter confirmation\n(concurrent control omitted)'),
    (disp(DOI_DUCH), duch, duch,
     'Rat liver enzymes\n≥90% effect-size agreement\n(VCG vs concurrent)'),
    (disp(DOI_ADED), aded_low, aded_high,
     'Rat clinical pathology\nparameter reproducibility\n(VCG vs concurrent)'),
]

fig, ax = plt.subplots(figsize=(11.5, 6.6))
x = np.arange(len(rows))
w = 0.58
for i, (lab, lo, hi, sub) in enumerate(rows):
    # green reproducible/concordant fraction (worst case for the ranged bar)
    ax.bar(i, lo, width=w, color=COLORS['repayment'],
           edgecolor=COLORS['ink'], linewidth=0.5, zorder=3)
    # orange residual discordance to 100
    ax.bar(i, 100 - lo, width=w, bottom=lo, color=COLORS['debt'],
           edgecolor=COLORS['ink'], linewidth=0.5, hatch='xx',
           alpha=0.92, zorder=3)
    # value label on the green fraction
    vtxt = "%.1f%%" % lo if lo != int(lo) else "%d%%" % lo
    ax.text(i, lo / 2, vtxt, ha='center', va='center', fontsize=13,
            fontweight='bold', color='white', zorder=5)
    # range whisker for the ranged (Adedeji) bar
    if hi != lo:
        ax.plot([i, i], [lo, hi], color=COLORS['ink'], lw=1.4, zorder=6)
        ax.plot([i - 0.10, i + 0.10], [hi, hi], color=COLORS['ink'], lw=1.4, zorder=6)
        ax.plot([i - 0.10, i + 0.10], [lo, lo], color=COLORS['ink'], lw=1.4, zorder=6)
        ax.text(i + 0.34, (lo + hi) / 2, '%d–%d%%\nreproducible' % (lo, hi),
                ha='left', va='center', fontsize=9.5, color=COLORS['ink'])
    # construct/species label beneath the axis
    ax.text(i, -7, sub, ha='center', va='top', fontsize=9.5, color=COLORS['gray_700'])

ax.axhline(100, color=COLORS['neutral_baseline'], lw=0.75, ls='--', zorder=1)
ax.set_xticks(x)
ax.set_xticklabels([r[0] for r in rows], fontsize=11)
ax.tick_params(axis='x', pad=64)
ax.set_ylim(0, 105)
ax.set_ylabel('Reproducible / concordant with concurrent control (%)')
ax.set_yticks(range(0, 101, 20))

legend = [
    mpatches.Patch(facecolor=COLORS['repayment'], edgecolor=COLORS['ink'],
                   label='Reproducible / concordant'),
    mpatches.Patch(facecolor=COLORS['debt'], edgecolor=COLORS['ink'], hatch='xx',
                   label='Residual discordance / non-reproducibility'),
]
ax.legend(handles=legend, loc='lower center', bbox_to_anchor=(0.5, 1.01),
          ncol=2, frameon=False, fontsize=11)

fig.text(0.01, -0.10,
         "Polarity harmonised to a single direction (higher = more reproducible). "
         "Adedeji's 49% is a non-reproducibility rate (worst of 31–49%); plotted here as its "
         "complement (51% reproducible, range 51–69%). Constructs and species differ across bars.",
         fontsize=9, color=COLORS['gray_500'], ha='left', style='italic')

fig.tight_layout()
out = _repo_path('figures') + '/fig_sec5_vcg_concordance.png'
save_figure(fig, out)
print('saved:', out)
```

:::

## Why the dividend is conditional: drift and comparability

If virtual controls sometimes fail, the reason is almost always that the historical data no longer represent the current study's conditions. Reused control data carry an implicit expiration date, ceasing to describe current husbandry, strains and assays as those drift, {cite:p}`Barrett2025` and the empirical record shows this drift is neither hypothetical nor small. Analysis of the largest curated multi-company control database — 457,605 data points from 1,288 Han Wistar rat studies — found that study year was the single most influential covariate on clinical laboratory parameters, outweighing both company and body-weight class. {cite:p}`Kellner2025` A single case study traced part of this temporal signal to a concrete cause: a change in anaesthesia protocol from carbon dioxide to isoflurane after 2017 shifted control serum-calcium means by an amount that was overwhelmingly significant and would silently bias any VCG spanning the change. {cite:p}`Gurjanov2023` Pooling control clinical-chemistry across five companies revealed systematic per-company offsets from the combined mean, {cite:p}`Kadyrov2025` and background lesion rates depend heavily on study duration — spontaneous liver necrosis in control rats rose from about 2% at ages matching one-month studies to about 8% at six-month terminal-sacrifice ages. {cite:p}`Snyder2024` Even within one endpoint, a telemetry study found same-laboratory historical controls usable to detect a QTc effect but cross-laboratory controls unusable because of time-course differences between two facilities' vehicle data. {cite:p}`Abernathy2024`

:::{trust-claim}
:claim-id: clm_01b62a9e94639de6
:claim: Reused control data carry an implicit expiration date, ceasing to describe current husbandry, strains and assays as those drift, and the empirical record shows this drift is neither hypothetical nor small.
:cites: Barrett2025
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e5bd824682e2cefe
:claim: Analysis of the largest curated multi-company control database — 457,605 data points from 1,288 Han Wistar rat studies — found that study year was the single most influential covariate on clinical laboratory parameters, outweighing both company and body-weight class.
:cites: Kellner2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_6b72d26e70309734
:claim: A single case study traced part of this temporal signal to a concrete cause: a change in anaesthesia protocol from carbon dioxide to isoflurane after 2017 shifted control serum-calcium means by an amount that was overwhelmingly significant and would silently bias any VCG spanning the change.
:cites: Gurjanov2023
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_5580ba286d4abf1a
:claim: Pooling control clinical-chemistry across five companies revealed systematic per-company offsets from the combined mean, and background lesion rates depend heavily on study duration — spontaneous liver necrosis in control rats rose from about 2% at ages matching one-month studies to about 8% at six-month terminal-sacrifice ages.
:cites: Kadyrov2025, Snyder2024
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_4a1d41336cb3740f
:claim: Even within one endpoint, a telemetry study found same-laboratory historical controls usable to detect a QTc effect but cross-laboratory controls unusable because of time-course differences between two facilities' vehicle data.
:cites: Abernathy2024
:claim-type: comparative
:modality: likely
:::

:::{admonition} Evidence conflict: is historical control data temporally stable?
:class: warning
Whether pooled control data can be trusted across years is itself contested. A cross-study comparison of rasH2 mouse tumour incidences found them remarkably similar over more than a decade, and a separate database of 1,420 rasH2 mice reported similarly low, stable spontaneous incidences, both arguing that the model shows minimal drift and therefore supports reliable historical control data. {cite:p}`Nambiar2012, Paranjpe2013` A multi-company clinical-pathology analysis reached the opposite emphasis, finding study year the most influential covariate of all on control laboratory values. {cite:p}`Kellner2025` The two are not strictly incompatible — one concerns rare tumour incidences in a stable transgenic model, the other concerns continuous laboratory parameters sensitive to husbandry and assay changes — but together they show that temporal stability is endpoint- and model-specific and cannot be assumed. A historical control database is trustworthy for some parameters and treacherous for others, and the burden is on the user to know which.

:::

:::{trust-claim}
:claim-id: clm_1e6984fae6019813
:claim: A cross-study comparison of rasH2 mouse tumour incidences found them remarkably similar over more than a decade, and a separate database of 1,420 rasH2 mice reported similarly low, stable spontaneous incidences, both arguing that the model shows minimal drift and therefore supports reliable historical control data.
:cites: Nambiar2012, Paranjpe2013
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_5e082a4339742007
:claim: A multi-company clinical-pathology analysis reached the opposite emphasis, finding study year the most influential covariate of all on control laboratory values.
:cites: Kellner2025
:claim-type: empirical
:modality: likely
:::

The background variability that historical controls must capture is large, structured and strain-dependent, which is the deeper reason strict matching and outlier-robust statistics are non-negotiable. Spontaneous Leydig-cell adenoma incidence in control rats ranges from near 100% in F344 to 13.7% in Wistar and 4.2% in Sprague-Dawley, and is further modulated by breeder, diet and age; {cite:p}`Nolte2011` female mononuclear-cell leukaemia backgrounds differ roughly eighteen-fold between Sprague-Dawley and F344/N strains; {cite:p}`Dinse2010` pituitary adenomas and adrenal hyperplasias reach incidences well above half of animals in some strains and sexes; {cite:p}`Kumar2023, Boyle2018` and body-weight and diet control alone shift terminal background liver-tumour incidence into a 15–20% band. {cite:p}`Leakey2003` Layered on top of this biological variability is measurement variability: a review of in vivo toxicology found rodent carcinogenicity outcomes only moderately replicable — 65–86% between sexes of one species and 36–74% between rat and mouse — which caps how well any historical comparison can perform. {cite:p}`Karmaus2026` The same instability appears at the assay level, where a machine-learning analysis pinned the test-condition variables driving divergent genotoxicity outcomes for most compounds, {cite:p}`Raitano2026` and in developmental studies where litter structure must be treated as the statistical unit or pooled control data will inflate apparent effects; {cite:p}`Brown2026` laboratories increasingly run dedicated studies purely to generate source-specific historical databases where published incidences are lacking. {cite:p}`Paranjpe2025` The methodological literature has responded by moving away from binary inclusion or exclusion of historical data toward tiered, uncertainty-aware use within a weight-of-evidence assessment, {cite:p}`Kluxen2021, Kluxen2024` and by trying to formalise how historical control limits should be computed — though reviewers note that after forty years of discussion many guidelines still fail to specify a reproducible method, leaving more open than solved. {cite:p}`Menssen2023, Menssen2025` A recent EFSA opinion proposes a stepwise quantitative decision scheme to harmonise how historical and concurrent control data are compiled and combined. {cite:p}`Coja2025`

:::{trust-claim}
:claim-id: clm_f67dbe229cd952b2
:claim: Spontaneous Leydig-cell adenoma incidence in control rats ranges from near 100% in F344 to 13.7% in Wistar and 4.2% in Sprague-Dawley, and is further modulated by breeder, diet and age; female mononuclear-cell leukaemia backgrounds differ roughly eighteen-fold between Sprague-Dawley and F344/N strains; pituitary adenomas and adrenal hyperplasias reach incidences well above half of animals in some strains and sexes; and body-weight and diet control alone shift terminal background liver-tumour incidence into a 15–20% band.
:cites: Nolte2011, Dinse2010, Kumar2023, Boyle2018, Leakey2003
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_a95bbd57e1daa505
:claim: Layered on top of this biological variability is measurement variability: a review of in vivo toxicology found rodent carcinogenicity outcomes only moderately replicable — 65–86% between sexes of one species and 36–74% between rat and mouse — which caps how well any historical comparison can perform.
:cites: Karmaus2026
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_09da8ad4e9bbdd60
:claim: The same instability appears at the assay level, where a machine-learning analysis pinned the test-condition variables driving divergent genotoxicity outcomes for most compounds, and in developmental studies where litter structure must be treated as the statistical unit or pooled control data will inflate apparent effects; laboratories increasingly run dedicated studies purely to generate source-specific historical databases where published incidences are lacking.
:cites: Raitano2026, Brown2026, Paranjpe2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e080b6c23ccb38d9
:claim: The methodological literature has responded by moving away from binary inclusion or exclusion of historical data toward tiered, uncertainty-aware use within a weight-of-evidence assessment, and by trying to formalise how historical control limits should be computed — though reviewers note that after forty years of discussion many guidelines still fail to specify a reproducible method, leaving more open than solved.
:cites: Kluxen2021, Kluxen2024, Menssen2023, Menssen2025
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d06b06f8674669a7
:claim: A recent EFSA opinion proposes a stepwise quantitative decision scheme to harmonise how historical and concurrent control data are compiled and combined.
:cites: Coja2025
:claim-type: methodological
:modality: likely
:::

## Borrowing that cuts both ways: the carcinogenicity precedent

Nowhere is the double edge of control-data reuse sharper than in the interpretation of tumour findings, where historical controls can be marshalled either to support or to dismiss a treatment-related signal. The extreme range of a historical database is routinely used to argue that a marginal tumour increase is not adverse: a nano-titanium-dioxide inhalation study judged a bronchiolo-alveolar carcinoma increase non-adverse because it sat at the upper limit of the historical database, {cite:p}`Kasai2024` an expert glyphosate review discounted a significant high-dose increase because it fell within the historical range, {cite:p}`Williams2016` and a re-analysis of vanadium pentoxide weakened a carcinogenicity signal to "no evidence" simply by adding twenty-five matched-diet studies that widened the historical range. {cite:p}`Starr2012` An evaluation of two decades of pesticide assessments found historical control data used almost exclusively to avoid false-positive calls, never to guard against false negatives, and typically without testing the assumption that current and historical controls share an underlying distribution. {cite:p}`Zarn2024` The opposite use — invoking historical controls to strengthen a positive finding, as when tumour incidences exceeding the historical range were read as evidence of carcinogenicity {cite:p}`Ohnishi2013` — is equally live and equally disputed.

:::{trust-claim}
:claim-id: clm_0cbecf4e4075f8b4
:claim: The extreme range of a historical database is routinely used to argue that a marginal tumour increase is not adverse: a nano-titanium-dioxide inhalation study judged a bronchiolo-alveolar carcinoma increase non-adverse because it sat at the upper limit of the historical database, an expert glyphosate review discounted a significant high-dose increase because it fell within the historical range, and a re-analysis of vanadium pentoxide weakened a carcinogenicity signal to "no evidence" simply by adding twenty-five matched-diet studies that widened the historical range.
:cites: Kasai2024, Williams2016, Starr2012
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_f8469d0669ad56f7
:claim: An evaluation of two decades of pesticide assessments found historical control data used almost exclusively to avoid false-positive calls, never to guard against false negatives, and typically without testing the assumption that current and historical controls share an underlying distribution.
:cites: Zarn2024
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_5714c3bdaf42ab78
:claim: The opposite use — invoking historical controls to strengthen a positive finding, as when tumour incidences exceeding the historical range were read as evidence of carcinogenicity — is equally live and equally disputed.
:cites: Ohnishi2013
:claim-type: methodological
:modality: likely
:::

:::{admonition} Evidence conflict: are historical controls adequate to sustain a carcinogenicity conclusion?
:class: warning
The Ramazzini Institute's Global Glyphosate Study interpreted treated-group tumour increases against its own and NTP historical control databases, reporting leukaemia at 1.63% in the current study versus 0.90% in 1,670 pooled historical controls, and used that comparison to support a treatment-related finding. {cite:p}`Panzacchi2025` In a separate Ramazzini study, however, EFSA rejected the carcinogenicity conclusions in part because the historical controls invoked dated from 1973–1983 — decades before the study — and because the design lacked an appropriate concurrent control and a contemporaneous historical database. {cite:p}`Aguilar2017` The conflict is not about whether historical controls are useful but about when they are admissible: the same institute's reliance on historical data is treated as supporting evidence in one case and as a disqualifying weakness in another. The unifying principle, stated plainly in the pathology literature, is that historical control data should never be used in isolation to override a concurrent control or a weight-of-evidence evaluation. {cite:p}`Foster2026, Elmore2009`
:::

:::{trust-claim}
:claim-id: clm_f1444b4b9fdb007a
:claim: The Ramazzini Institute's Global Glyphosate Study interpreted treated-group tumour increases against its own and NTP historical control databases, reporting leukaemia at 1.63% in the current study versus 0.90% in 1,670 pooled historical controls, and used that comparison to support a treatment-related finding.
:cites: Panzacchi2025
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_6a3f4893c89b924b
:claim: In a separate Ramazzini study, however, EFSA rejected the carcinogenicity conclusions in part because the historical controls invoked dated from 1973–1983 — decades before the study — and because the design lacked an appropriate concurrent control and a contemporaneous historical database.
:cites: Aguilar2017
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_9fa66f8ea26ea462
:claim: The unifying principle, stated plainly in the pathology literature, is that historical control data should never be used in isolation to override a concurrent control or a weight-of-evidence evaluation.
:cites: Foster2026, Elmore2009
:claim-type: methodological
:modality: established
:::

The statistical fragility underlying these disputes is well documented. Range statistics are highly outlier-sensitive, so the concurrent control remains the most relevant comparator and historical data only a supporting input, {cite:p}`Elmore2009` yet the choice of which historical set to use can flip a marginal call, as a decamethylcyclopentasiloxane bioassay showed when four historical control sets of differing heterogeneity gave different answers. {cite:p}`Young2016` The multiplicity of control-versus-treated comparisons compounds the problem: Monte-Carlo analysis of NTP bioassays found that about 92% of chemicals show a statistically significant tumour decrease at at least one site purely from random variability and multiple testing, {cite:p}`Linkov1998` and requiring joint trend-plus-pairwise significance can inflate the false-negative rate by up to 204.5% unless significance levels are recalibrated. {cite:p}`Lin2018` High control variability produces the same pathology in ecological studies, where background abundance alone made a statistical test flag significant differences in more than half of comparisons before any treatment was applied, {cite:p}`Schimera2025` and the choice of statistical test itself materially shifts false-positive and false-negative rates in control-versus-treated comparisons. {cite:p}`Green2014, Rahman2008` These are not arguments against reusing control data; they are arguments that reuse must be paired with outlier-robust methods and honest accounting for multiplicity. {cite:p}`Elmore2025, Maronpot2016`

:::{trust-claim}
:claim-id: clm_264eeb1d1f8b9c90
:claim: Range statistics are highly outlier-sensitive, so the concurrent control remains the most relevant comparator and historical data only a supporting input, yet the choice of which historical set to use can flip a marginal call, as a decamethylcyclopentasiloxane bioassay showed when four historical control sets of differing heterogeneity gave different answers.
:cites: Elmore2009, Young2016
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_ed80ad16a2948b66
:claim: The multiplicity of control-versus-treated comparisons compounds the problem: Monte-Carlo analysis of NTP bioassays found that about 92% of chemicals show a statistically significant tumour decrease at at least one site purely from random variability and multiple testing, and requiring joint trend-plus-pairwise significance can inflate the false-negative rate by up to 204.5% unless significance levels are recalibrated.
:cites: Linkov1998, Lin2018
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e0957bf7dc818dd4
:claim: High control variability produces the same pathology in ecological studies, where background abundance alone made a statistical test flag significant differences in more than half of comparisons before any treatment was applied, and the choice of statistical test itself materially shifts false-positive and false-negative rates in control-versus-treated comparisons.
:cites: Schimera2025, Green2014, Rahman2008
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_5825ef966069ff97
:claim: These are not arguments against reusing control data; they are arguments that reuse must be paired with outlier-robust methods and honest accounting for multiplicity.
:cites: Elmore2025, Maronpot2016
:claim-type: methodological
:modality: likely
:::

## Power, Type I error, and the limits of borrowing

The clinical borrowing literature has confronted the statistical tradeoff more formally than preclinical toxicology, and its conclusions temper the enthusiasm of the Reduction argument. The upside is real and quantifiable: when external and trial controls are genuinely exchangeable, a Bayesian hybrid-arm design recovered nearly the full power of a 1:1 randomised trial (about 77–81%) where a no-borrowing design languished near 49–54%, {cite:p}`Wang2026` and dynamic borrowing has been used to down-randomise control arms across a range of designs. {cite:p}`Dron2019, Gaskell2025` The downside is a principled one. A theoretical result shows that when a uniformly most powerful test exists, strict frequentist Type I error control means external borrowing yields no power gain at all, {cite:p}`KoppSchneider2019` and a companion analysis proves that insisting on Type I error control forces the elimination of any favourable borrowing of historical information. {cite:p}`Quan2019` In other words, the power gains and the error guarantees cannot both be maximised; borrowing buys efficiency by spending a portion of the error budget, and the exchange is only benign when the historical and current controls truly agree.

:::{trust-claim}
:claim-id: clm_f1bb286fd0d9e98a
:claim: The upside is real and quantifiable: when external and trial controls are genuinely exchangeable, a Bayesian hybrid-arm design recovered nearly the full power of a 1:1 randomised trial (about 77–81%) where a no-borrowing design languished near 49–54%, and dynamic borrowing has been used to down-randomise control arms across a range of designs.
:cites: Wang2026, Dron2019, Gaskell2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_05e91174b6c2c4a0
:claim: A theoretical result shows that when a uniformly most powerful test exists, strict frequentist Type I error control means external borrowing yields no power gain at all, and a companion analysis proves that insisting on Type I error control forces the elimination of any favourable borrowing of historical information.
:cites: KoppSchneider2019, Quan2019
:claim-type: methodological
:modality: established
:::

When they do not agree, the cost is paid as bias and inflated error. Population drift in open platform trials that reuse non-concurrent controls can bias estimates and inflate Type I error; {cite:p}`Overbey2022` mismatched disease-assessment schedules between a synthetic control and its trial can cause severe error inflation or power loss unless harmonised; {cite:p}`Zhu2022` and even propensity-score-weighted priors can only attenuate, never eliminate, confounding bias from combining trial and external data. {cite:p}`Polak2025, Wang2025b` This is precisely why the field has invested in dynamic methods that tune the amount borrowed to the observed congruence between historical and current data rather than borrowing a fixed quantity: meta-analytic-predictive priors and their robust and semiparametric extensions, {cite:p}`Neuenschwander2010, Hupf2021` latent-exchangeability and elastic priors that borrow only from subjects or sources that appear comparable, {cite:p}`Alt2024a, Huang2025a` and adaptive schemes that discount in proportion to prior-data conflict. {cite:p}`Mukhopadhyay2025, Bennett2021, Callegaro2021` The cautionary counterpoint is that these methods can still perform poorly when exchangeability fails, so their operating characteristics must be checked case by case rather than assumed. {cite:p}`Alt2024b, Lee2025b, Nikolakopoulos2017` The toolkit is by now deep: foundational power and meta-analytic-predictive priors, along with probability- or distance-based variants that cap how much is borrowed, have been developed and simulated across binary, count and time-to-event endpoints, {cite:p}`Smith2020a, Isogawa2020, Peng2023, Lu2024, Feit2020, Warren2024, Li2026, Burman2024` and their adaptive descendants tie the borrowed quantity to observed heterogeneity or covariate consistency in an effort to preserve error control when sources disagree. {cite:p}`Tian2025, Zheng2025, Mariani2023, Chen2023, Hupf2024, Neuenschwander2020, Campbell2024, Qian2025, Ratta2026, Zocholl2025, Scott2026, Murray2021, Harun2023, Ohigashi2024, Wang2023, Zhan2021` One of the most consequential applications is paediatric extrapolation, where adult data are borrowed to make otherwise infeasible child trials analysable, {cite:p}`GamaloSiebers2017, Walker2023, Pottackal2025, Sailer2024` and clinical methods that shrink the required control-group size while preserving frequentist operating characteristics {cite:p}`Schwartz2026` are the direct statistical analogue of the preclinical virtual control group. In a Wistar Han rat liver-enzyme analysis, 68.5% of concurrent-versus-virtual-control comparisons achieved at least 90% agreement in effect-size estimates. {cite:p}`DuchateauNguyen2026` However, a separate review found that 31–49% of quantitative clinical-pathology parameters were not reproducible when concurrent controls were fully replaced by virtual controls. {cite:p}`Adedeji2024`

:::{trust-claim}
:claim-id: clm_d8eb24c7e2456dc6
:claim: Population drift in open platform trials that reuse non-concurrent controls can bias estimates and inflate Type I error; mismatched disease-assessment schedules between a synthetic control and its trial can cause severe error inflation or power loss unless harmonised; and even propensity-score-weighted priors can only attenuate, never eliminate, confounding bias from combining trial and external data.
:cites: Overbey2022, Zhu2022, Polak2025, Wang2025b
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_6acf76d2ca381133
:claim: This is precisely why the field has invested in dynamic methods that tune the amount borrowed to the observed congruence between historical and current data rather than borrowing a fixed quantity: meta-analytic-predictive priors and their robust and semiparametric extensions, latent-exchangeability and elastic priors that borrow only from subjects or sources that appear comparable, and adaptive schemes that discount in proportion to prior-data conflict.
:cites: Neuenschwander2010, Hupf2021, Alt2024a, Huang2025a, Mukhopadhyay2025, Bennett2021, Callegaro2021
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_c67f4dc45d7a5cac
:claim: The cautionary counterpoint is that these methods can still perform poorly when exchangeability fails, so their operating characteristics must be checked case by case rather than assumed.
:cites: Alt2024b, Lee2025b, Nikolakopoulos2017
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_c67d1a468e78766b
:claim: The toolkit is by now deep: foundational power and meta-analytic-predictive priors, along with probability- or distance-based variants that cap how much is borrowed, have been developed and simulated across binary, count and time-to-event endpoints, and their adaptive descendants tie the borrowed quantity to observed heterogeneity or covariate consistency in an effort to preserve error control when sources disagree.
:cites: Smith2020a, Isogawa2020, Peng2023, Lu2024, Feit2020, Warren2024, Li2026, Burman2024, Tian2025, Zheng2025, Mariani2023, Chen2023, Hupf2024, Neuenschwander2020, Campbell2024, Qian2025, Ratta2026, Zocholl2025, Scott2026, Murray2021, Harun2023, Ohigashi2024, Wang2023, Zhan2021
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_63e08fde8ce016d8
:claim: One of the most consequential applications is paediatric extrapolation, where adult data are borrowed to make otherwise infeasible child trials analysable, and clinical methods that shrink the required control-group size while preserving frequentist operating characteristics are the direct statistical analogue of the preclinical virtual control group.
:cites: GamaloSiebers2017, Walker2023, Pottackal2025, Sailer2024, Schwartz2026
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_1a7c2d0b3c6cfe8b
:claim: In a Wistar Han rat liver-enzyme analysis, 68.5% of concurrent-versus-virtual-control comparisons achieved at least 90% agreement in effect-size estimates.
:cites: DuchateauNguyen2026
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_92618eddf068d4bd
:claim: However, a separate review found that 31–49% of quantitative clinical-pathology parameters were not reproducible when concurrent controls were fully replaced by virtual controls.
:cites: Adedeji2024
:claim-type: empirical
:modality: contested
:::

## Adoption, acceptance, and the gap that remains

The final condition on the dividend is regulatory. External control arms — the clinical analogue of VCGs — are now visibly present in regulatory decisions: they featured in 17% of EMA cancer-drug approvals from 2016 to 2021, with a 63% acceptance rate among submissions that used them, {cite:p}`Pignatti2026, Vennin2026` and nearly half of recent multiple-myeloma approvals leveraged real-world evidence. {cite:p}`Taylor2025` Yet adoption is concentrated in regulatory oncology and rare-disease settings and remains vanishingly rare elsewhere: only seven of 1,115 open-label extension studies over a decade used an external control, {cite:p}`Hartley2025` and an earlier review found only about 8% of oncology approvals used real-world evidence for efficacy, all retrospectively. {cite:p}`Arondekar2021` Where external controls are used, retrospectively assembled natural-history data dominate — the most common source in 44% of one set of FDA approvals {cite:p}`Jahanshahi2021` — and almost half of single-arm-trial applications were criticised for using external controls that were not contemporaneous with the trial. {cite:p}`Subramaniam2024` The comparability of these controls depends heavily on their source, which is itself a live conflict.

:::{trust-claim}
:claim-id: clm_d4e29970066383a5
:claim: External control arms — the clinical analogue of VCGs — are now visibly present in regulatory decisions: they featured in 17% of EMA cancer-drug approvals from 2016 to 2021, with a 63% acceptance rate among submissions that used them, and nearly half of recent multiple-myeloma approvals leveraged real-world evidence.
:cites: Pignatti2026, Vennin2026, Taylor2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_3a8449cd97a40d91
:claim: Yet adoption is concentrated in regulatory oncology and rare-disease settings and remains vanishingly rare elsewhere: only seven of 1,115 open-label extension studies over a decade used an external control, and an earlier review found only about 8% of oncology approvals used real-world evidence for efficacy, all retrospectively.
:cites: Hartley2025, Arondekar2021
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_811c0195178b7488
:claim: Where external controls are used, retrospectively assembled natural-history data dominate — the most common source in 44% of one set of FDA approvals — and almost half of single-arm-trial applications were criticised for using external controls that were not contemporaneous with the trial.
:cites: Jahanshahi2021, Subramaniam2024
:claim-type: empirical
:modality: likely
:::

:::{admonition} Evidence conflict: do external controls reproduce concurrent ones?
:class: warning
The evidence on whether external controls reproduce a true concurrent control is genuinely split, and the split tracks the data source. In idiopathic pulmonary fibrosis, external controls built from historical randomised-trial placebo arms reproduced the original treatment effect, whereas controls built from registry or electronic-health-record data did not. {cite:p}`Swaminathan2023` A head-to-head comparison in adjuvant breast cancer found mixed replicability — some survival curves overlapped, others diverged — so real-world controls could not be assumed to reproduce randomised ones, {cite:p}`Walker2026b` and a real-world external control failed to reproduce a lung-cancer trial's hazard ratio (1.53 versus 0.91) until Bayesian borrowing from a historical control trial pulled the estimate back toward the randomised result. {cite:p}`Struebing2024` Yet other emulations succeeded: an electronic-record-derived cohort matched a trial cohort's overall survival closely. {cite:p}`Walker2024` The pattern is that controls derived from prior randomised trials are comparatively trustworthy while those assembled from routine real-world data are not, and the burden of covariate adjustment for the latter is heavy — one external-control effort screened more than 120 potential confounders. {cite:p}`Yap2022`
:::

:::{trust-claim}
:claim-id: clm_d2528c94c6435682
:claim: In idiopathic pulmonary fibrosis, external controls built from historical randomised-trial placebo arms reproduced the original treatment effect, whereas controls built from registry or electronic-health-record data did not.
:cites: Swaminathan2023
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_a50a4602be73e14b
:claim: A head-to-head comparison in adjuvant breast cancer found mixed replicability — some survival curves overlapped, others diverged — so real-world controls could not be assumed to reproduce randomised ones, and a real-world external control failed to reproduce a lung-cancer trial's hazard ratio (1.53 versus 0.91) until Bayesian borrowing from a historical control trial pulled the estimate back toward the randomised result.
:cites: Walker2026b, Struebing2024
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_91c8a2003b613105
:claim: Yet other emulations succeeded: an electronic-record-derived cohort matched a trial cohort's overall survival closely.
:cites: Walker2024
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_b954aa3602e3e3bd
:claim: The pattern is that controls derived from prior randomised trials are comparatively trustworthy while those assembled from routine real-world data are not, and the burden of covariate adjustment for the latter is heavy — one external-control effort screened more than 120 potential confounders.
:cites: Yap2022
:claim-type: review_synthesis
:modality: contested
:::

The appeal that drives adoption is easy to see across indications: real-world or synthetic control arms have been used to estimate large apparent benefits for single-arm oncology and rare-disease programmes, {cite:p}`Rolfo2022, Hadoux2026, Boyne2023, Letailleur2025, VanLe2023, Yin2023, Oesterheld2024` to augment under-enrolled internal controls toward adequate power or even to reduce or eliminate the concurrent control where randomisation is infeasible, {cite:p}`Ko2024, BoemmelWegmann2026, Schmidli2019` and in rarer, more probative tests to reproduce a trial's own effect. {cite:p}`Litman2025, Thomas2021, Lukas2025` The countervailing scrutiny is equally systematic: selection bias and confounding are the dominant regulatory and health-technology critiques, {cite:p}`Jaksa2022, Izem2022, Velummailum2023` valid inference depends on aligning trial and external patients by propensity scores or related adjustment across sometimes more than a hundred covariates, {cite:p}`Loiseau2022, Abrisqueta2025, Yap2022, Belthangady2021` and acceptance stays case-by-case and contested. {cite:p}`Mangla2026, BaumfeldAndre2019, Dagenais2021, Arora2025, Mulder2023, Mitroiu2018, Cucherat2020` The unresolved core of the whole argument is that, for all the accumulated data and demonstrated concordance, no regulator has yet accepted a virtual-control-group study in place of a concurrent-control study for a pivotal preclinical submission. Industry reviews describe VCGs, second-species requirements and information sharing as currently "under scrutiny," with companies and regulators reluctant to abandon existing paradigms until replacement approaches are validated and globally accepted, {cite:p}`Harrell2024` and the Japanese analysis catalogues five concrete obstacles because current guidelines still mandate concurrent controls for pivotal studies. {cite:p}`SATO2024` The successor projects assembling standardised control databases name regulatory acceptance as their explicit goal precisely because it has not yet been secured. {cite:p}`StegerHartmann2024, Palazzi2024` The Reduction dividend of control-data reuse is therefore real in its mechanism, quantified at roughly a quarter of control animals, and supported by infrastructure that already exists at scale — but it is conditional on endpoint-specific concordance, contingent on controlling for drift, and, in the preclinical arena where the animal-welfare stake is greatest, still awaiting the regulatory acceptance that would convert a demonstrated capability into discharged debt.

:::{trust-claim}
:claim-id: clm_940ff6b84f4201bf
:claim: The appeal that drives adoption is easy to see across indications: real-world or synthetic control arms have been used to estimate large apparent benefits for single-arm oncology and rare-disease programmes, to augment under-enrolled internal controls toward adequate power or even to reduce or eliminate the concurrent control where randomisation is infeasible, and in rarer, more probative tests to reproduce a trial's own effect.
:cites: Rolfo2022, Hadoux2026, Boyne2023, Letailleur2025, VanLe2023, Yin2023, Oesterheld2024, Ko2024, BoemmelWegmann2026, Schmidli2019, Litman2025, Thomas2021, Lukas2025
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e78d5811b9c3c827
:claim: The countervailing scrutiny is equally systematic: selection bias and confounding are the dominant regulatory and health-technology critiques, valid inference depends on aligning trial and external patients by propensity scores or related adjustment across sometimes more than a hundred covariates, and acceptance stays case-by-case and contested.
:cites: Jaksa2022, Izem2022, Velummailum2023, Loiseau2022, Abrisqueta2025, Yap2022, Belthangady2021, Mangla2026, BaumfeldAndre2019, Dagenais2021, Arora2025, Mulder2023, Mitroiu2018, Cucherat2020
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_3ce927e4e5c6b3a1
:claim: Industry reviews describe VCGs, second-species requirements and information sharing as currently "under scrutiny," with companies and regulators reluctant to abandon existing paradigms until replacement approaches are validated and globally accepted, and the Japanese analysis catalogues five concrete obstacles because current guidelines still mandate concurrent controls for pivotal studies.
:cites: Harrell2024, SATO2024
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_34a6bd26e9917641
:claim: The successor projects assembling standardised control databases name regulatory acceptance as their explicit goal precisely because it has not yet been secured.
:cites: StegerHartmann2024, Palazzi2024
:claim-type: empirical
:modality: likely
:::

This is data reuse working as a 3Rs intervention in the most concrete form the review will encounter: existing animal data standing in for animals not used — Reduction achieved by reuse. The complementary strategy is not to reduce the animals but to replace them, avoiding their use in the first place — a logic already visible where computational models calibrated on prior animal data, such as digital-twin cardiotoxicity simulation, stand in for live control and treated animals. {cite:p}`VillarValero2025` {ref}`sec-nams-data` turns to new approach methodologies — in silico models, organoids and organ-on-chip systems — which pursue Replacement rather than Reduction, and which generate their own streams of data that, if left unstewarded, would simply re-incur the ethical debt in a new medium.

:::{trust-claim}
:claim-id: clm_b244e5bffe44e13a
:claim: The complementary strategy is not to reduce the animals but to replace them, avoiding their use in the first place — a logic already visible where computational models calibrated on prior animal data, such as digital-twin cardiotoxicity simulation, stand in for live control and treated animals.
:cites: VillarValero2025
:claim-type: methodological
:modality: likely
:::

:::{evidence-explorer}
:evidence-dir: ../evidence
:height: 800px
:::

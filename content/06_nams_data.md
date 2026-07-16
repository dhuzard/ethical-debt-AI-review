(sec-nams-data)=

# New Approach Methodologies and the Data They Generate

The previous section treated the reuse of one high-value class of animal data — the control arm — as a countable act of Reduction, where stewardship of an existing record keeps a group of animals out of a study. {ref}`sec-virtual-controls` left the Replacement question open, and this section takes it up directly. New approach methodologies (NAMs) — in silico and QSAR models, organoids, organ-on-chip microphysiological systems, and high-throughput screening — do not amortise animal use across future studies; they aim to remove the animal from the experiment altogether. The pressure to do so is quantitative and structural: fewer than a tenth of chemicals in commerce have ever been screened for safety, {cite:p}`Comess2020` roughly a quarter of the US regulatory inventory consists of complex or variable-composition substances for which conventional testing is ill-suited, {cite:p}`Sauer2020` and the volume of substances with data gaps already exceeds available animal-testing capacity, {cite:p}`Schmidt2016` and conventional testing is too resource-intensive in time, money, and animal lives to evaluate every chemical, which is why adverse-outcome-pathway frameworks were developed to prioritise where testing is done at all. {cite:p}`Tollefsen2014` The animal tests themselves translate poorly — only around 16% of drug candidates that pass them reach human approval, {cite:p}`Csobonyeiova2016` oncology programmes succeed in roughly 5% of cases, {cite:p}`Brancato2020` rodent cancer bioassays consume hundreds of animals with limited human relevance, {cite:p}`Hilton2022` and rodent kidneys differ anatomically and molecularly from human ones. {cite:p}`Kishi2021` The argument of this section is that NAMs genuinely reach usable, sometimes high, predictivity for narrow and well-defined endpoints and can displace specific animal tests — but the data they generate are as large, heterogeneous, and poorly stewarded as the animal data they replace, so Replacement pursued without data welfare relocates the ethical debt rather than discharging it.

:::{trust-claim}
:claim-id: clm_30768388ada90364
:claim: The pressure to do so is quantitative and structural: fewer than a tenth of chemicals in commerce have ever been screened for safety, roughly a quarter of the US regulatory inventory consists of complex or variable-composition substances for which conventional testing is ill-suited, and the volume of substances with data gaps already exceeds available animal-testing capacity, and conventional testing is too resource-intensive in time, money, and animal lives to evaluate every chemical, which is why adverse-outcome-pathway frameworks were developed to prioritise where testing is done at all.
:cites: Comess2020, Sauer2020, Schmidt2016, Tollefsen2014
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_20ba72e89bca7904
:claim: The animal tests themselves translate poorly — only around 16% of drug candidates that pass them reach human approval, oncology programmes succeed in roughly 5% of cases, rodent cancer bioassays consume hundreds of animals with limited human relevance, and rodent kidneys differ anatomically and molecularly from human ones.
:cites: Csobonyeiova2016, Brancato2020, Hilton2022, Kishi2021
:claim-type: review_synthesis
:modality: likely
:::

## Predictivity is real, but it is endpoint-specific

The strongest case for NAMs is empirical: for narrowly defined hazards, validated non-animal assays now match or exceed animal-test concordance. Multi-laboratory validation of a reconstructed human skin genotoxicity assay reported sensitivity of 77% and specificity of 88% (80% and 97% under alternate criteria) against in vivo outcomes, with within-laboratory reproducibility of 93%, {cite:p}`Pfuhler2020` and an interlaboratory trial of a mammalian reporter genotoxicity assay across seven laboratories and 64 chemicals reached sensitivity 84.4% and specificity 91.2%. {cite:p}`Hendriks2024` In skin sensitisation, defined approaches integrating multiple non-animal methods underpin the first OECD guideline of its kind, presented as performing equivalently to or better than animal tests, {cite:p}`Casati2022, Casati2017, Kolle2020` and a proof-of-concept extension to agrochemical mixtures achieved 85.0% sensitivity. {cite:p}`Corvaro2024` A high-content three-dimensional hepatocyte-spheroid assay detected 36 of 42 known hepatotoxins with no false positives among safe compounds, {cite:p}`Sirenko2016` and a functional variant-classification assay integrated with in silico prediction correctly classified 87% of Lynch-syndrome variants. {cite:p}`Drost2019` {numref}`fig-sec6-nam-vs-invivo` assembles these performances across five assay types. Read together they establish that NAM predictivity is respectable and, for some endpoints, high — but the figure also exposes the catch: every assay is benchmarked against a different reference standard and a different hazard, so the headline numbers cannot be pooled into a single accuracy.

:::{trust-claim}
:claim-id: clm_ea44539031404719
:claim: Multi-laboratory validation of a reconstructed human skin genotoxicity assay reported sensitivity of 77% and specificity of 88% (80% and 97% under alternate criteria) against in vivo outcomes, with within-laboratory reproducibility of 93%, and an interlaboratory trial of a mammalian reporter genotoxicity assay across seven laboratories and 64 chemicals reached sensitivity 84.4% and specificity 91.2%.
:cites: Pfuhler2020, Hendriks2024
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_56206a7ab9de8222
:claim: In skin sensitisation, defined approaches integrating multiple non-animal methods underpin the first OECD guideline of its kind, presented as performing equivalently to or better than animal tests, and a proof-of-concept extension to agrochemical mixtures achieved 85.0% sensitivity.
:cites: Casati2022, Casati2017, Kolle2020, Corvaro2024
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_34a0d91aef052ddb
:claim: A high-content three-dimensional hepatocyte-spheroid assay detected 36 of 42 known hepatotoxins with no false positives among safe compounds, and a functional variant-classification assay integrated with in silico prediction correctly classified 87% of Lynch-syndrome variants.
:cites: Sirenko2016, Drost2019
:claim-type: empirical
:modality: likely
:::

:::{figure} ../figures/fig_sec6_nam_vs_invivo.png
:name: fig-sec6-nam-vs-invivo
:width: 100%
**Real predictivity, fragmented endpoints.** Predictive performance of five non-animal (NAM) assay types against in vivo or consensus references: reconstructed-skin genotoxicity (77%/88% sensitivity/specificity), {cite:p}`Pfuhler2020` reporter genotoxicity (84.4%/91.2%), {cite:p}`Hendriks2024` skin sensitisation of agrochemical formulations (85.0%/68.2%), {cite:p}`Corvaro2024` hepatotoxicity spheroids (86% sensitivity, 100% predictivity for safe compounds), {cite:p}`Sirenko2016` and HTS-based metabolic-disruption modelling (balanced accuracy 0.55–0.88). {cite:p}`Filer2022` Sensitivity (circles) and specificity/predictivity (triangles) are shown as paired markers; the balanced-accuracy range uses a distinct marker to flag that it is not a sensitivity/specificity pair. Not a single pooled accuracy: four are assay sensitivity/specificity pairs against different reference standards (in vivo genotoxicity, in vivo skin sensitisation, curated hepatotoxins), and Filer2022 is a balanced-accuracy range (0.55-0.88) across ToxPi model variants vs a literature-consensus reference. Endpoints span genotoxicity, skin sensitisation, hepatotoxicity, metabolic disruption; Sirenko2016's 100% is 'predictivity' (no false positives among safe compounds); Pfuhler2020's 77/88 are coded-laboratory calls (agreed-criteria calls 80/97).
:::

:::{dropdown} 📓 Figure code

```python
"""fig_sec6_nam_vs_invivo — Predictive performance of NAM assays vs in vivo/consensus reference.

Phase-6 verdict: CAVEAT. The five assays are NOT pooled into a single accuracy:
endpoints and reference standards differ, so sensitivity/specificity pairs are
shown as paired markers (circle = sensitivity, triangle = specificity/
predictivity) grouped by endpoint, and the balanced-accuracy range (Filer2022)
uses a distinct square marker with a whisker to flag that it is not a
sensitivity/specificity pair. Data loaded at runtime from
evidence/evidence_section_06.json (comparison nam-predictive-performance-vs-invivo).
"""
import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def _repo_path(rel):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in ['.', '..', '../..', '../../..', here + '/../..', here + '/..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_06.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_06.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_06.json'), encoding='utf-8'))


def disp(doi):
    a = AT[CM[doi]]
    return "%s\n%s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'nam-predictive-performance-vs-invivo')
byd = {p['doi']: p for p in fd['papers']}

# ── assay order: four sens/spec pairs, then the balanced-accuracy range ──
PAIRS = [
    ('10.1093/mutage/geaa009', 'Genotoxicity\n(reconstructed skin)', 'in vivo\ngenotoxicity'),
    ('10.1002/em.22592', 'Genotoxicity\n(reporter assay)', 'in vivo\ngenotoxicity'),
    ('10.1016/j.yrtph.2024.105595', 'Skin\nsensitisation', 'in vivo\nsensitisation'),
    ('10.1089/adt.2016.729', 'Hepatotoxicity\n(spheroids)', 'curated\nhepatotoxins'),
]
DOI_FILER = '10.1289/EHP6779'


def parse_pair(val):
    nums = [float(x) for x in re.findall(r'[\d.]+', val)]
    return nums[0], nums[1]


def parse_range(val):
    nums = [float(x) for x in re.findall(r'[\d.]+', val)]
    lo, hi = min(nums), max(nums)
    return lo * 100 if hi <= 1 else lo, hi * 100 if hi <= 1 else hi


fig, ax = plt.subplots(figsize=(12.5, 7.2))

xpos = [0, 1, 2, 3]
sens_c, spec_c = COLORS['actual_verified'], COLORS['conflict']
for i, (doi, endpoint, ref) in enumerate(PAIRS):
    sens, spec = parse_pair(byd[doi]['value'])
    x = xpos[i]
    ax.plot([x, x], [sens, spec], color=COLORS['neutral_baseline'], lw=1.0, zorder=1)
    ax.scatter([x], [sens], marker='o', s=170, color=sens_c,
               edgecolor=COLORS['ink'], linewidth=0.7, zorder=4)
    ax.scatter([x], [spec], marker='^', s=190, color=spec_c,
               edgecolor=COLORS['ink'], linewidth=0.7, zorder=4)
    ax.annotate("%.4g" % sens, (x, sens), textcoords='offset points',
                xytext=(-26, -4), fontsize=10, color=sens_c, fontweight='bold')
    ax.annotate("%.4g" % spec, (x, spec), textcoords='offset points',
                xytext=(9, -4), fontsize=10, color=spec_c, fontweight='bold')
    ax.text(x, -13, endpoint, ha='center', va='top', fontsize=9.5,
            color=COLORS['gray_700'])
    ax.text(x, -30, "ref: " + ref, ha='center', va='top', fontsize=8.5,
            color=COLORS['gray_500'], style='italic')

# flag Sirenko specificity value as "predictivity"
ax.annotate("predictivity\n(no false positives)", (xpos[3], 100),
            textcoords='offset points', xytext=(12, 6), fontsize=8.5,
            color=COLORS['gray_700'])

# ── Filer2022 balanced-accuracy range as a distinct square marker + whisker ──
xf = 4
lo, hi = parse_range(byd[DOI_FILER]['value'])
ax.plot([xf, xf], [lo, hi], color=COLORS['secondary_cat'], lw=2.2, zorder=2)
ax.scatter([xf, xf], [lo, hi], marker='s', s=150, color=COLORS['secondary_cat'],
           edgecolor=COLORS['ink'], linewidth=0.7, zorder=4)
ax.text(xf + 0.12, (lo + hi) / 2, "balanced\naccuracy\nrange\n%d–%d" % (lo, hi),
        ha='left', va='center', fontsize=8.5, color=COLORS['secondary_cat'])
ax.text(xf, -13, "Metabolic\ndisruption\n(HTS models)", ha='center', va='top',
        fontsize=9.5, color=COLORS['gray_700'])
ax.text(xf, -30, "ref: literature\nconsensus", ha='center', va='top', fontsize=8.5,
        color=COLORS['gray_500'], style='italic')

# study labels along the top
labels = [disp(d) for d, _, _ in PAIRS] + [disp(DOI_FILER)]
for x, lab in zip(xpos + [xf], labels):
    ax.text(x, 108, lab, ha='center', va='bottom', fontsize=9, color=COLORS['ink'])

ax.axhline(100, color=COLORS['neutral_baseline'], lw=0.75, ls='--', zorder=0)
ax.set_ylim(0, 118)
ax.set_xlim(-0.7, 5.2)
ax.set_xticks([])
ax.set_ylabel('Reported performance (%)  —  metrics NOT on a common scale')
ax.set_yticks(range(0, 101, 20))

handles = [
    mlines.Line2D([], [], marker='o', color='w', markerfacecolor=sens_c,
                  markeredgecolor=COLORS['ink'], markersize=12, label='Sensitivity'),
    mlines.Line2D([], [], marker='^', color='w', markerfacecolor=spec_c,
                  markeredgecolor=COLORS['ink'], markersize=13,
                  label='Specificity / predictivity'),
    mlines.Line2D([], [], marker='s', color='w', markerfacecolor=COLORS['secondary_cat'],
                  markeredgecolor=COLORS['ink'], markersize=12,
                  label='Balanced-accuracy range (not a sens/spec pair)'),
]
ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.0, 1.06),
          ncol=3, frameon=False, fontsize=9.5)

fig.text(0.5, -0.06,
         "Each assay is benchmarked against a different reference standard and a different hazard; "
         "the values must NOT be pooled into a single accuracy.",
         ha='center', fontsize=9, color=COLORS['gray_500'], style='italic')

fig.subplots_adjust(bottom=0.24, top=0.86)
out = _repo_path('figures') + '/fig_sec6_nam_vs_invivo.png'
save_figure(fig, out)
print('saved:', out)
```

:::

The same pattern — high accuracy inside a tightly bounded question — recurs in the in silico stream, where computational models require no cells at all and generate their outputs at negligible marginal cost. Expert-rule and QSAR software predicted phototoxicity with 77% overall accuracy, {cite:p}`Ahuja2024` a machine-learning model classified the pregnancy-risk category of 97 antibiotics with 94.11% external-validation accuracy, {cite:p}`KelleciCelik2022` and interspecies aquatic-toxicity models passed cross-validation in more than three-quarters of cases. {cite:p}`Hong2022` Consensus androgen-receptor models built by many groups reached about 80% averaged accuracy, {cite:p}`Mansouri2020` a mechanism-of-action profiler assigned toxic mode correctly for 92% of a large clear-outcome training set, {cite:p}`Levet2026` QSAR-derived toxicity values outperformed screening-based predictions for data-poor chemicals, {cite:p}`Wignall2018` and bacterial-mutagenicity QSAR is judged reliable enough to support regulatory decisions alongside other evidence. {cite:p}`Tcheremenskaia2021` {numref}`fig-sec6-in-silico-performance` collects three of these endpoints and makes the structural point visible: the numbers look comparable but measure different things. Regulatory-facing NAM programmes report the same bounded successes — teratogenicity assays predicting 75 known teratogens with 73–82% predictivity, rising to 88% when platforms are combined; {cite:p}`Yao2025` zebrafish-embryo exposure correlating with mammalian and human values for reference developmental toxicants; {cite:p}`Nawaji2024` and validated QSAR/read-across meeting OECD thresholds for pesticide developmental-toxicity prioritisation. {cite:p}`Wang2024a` Such models scale to hazard spaces that experiment cannot touch — candidate structures for a single chemical-warfare class can exceed 10,000 compounds, making in silico estimation of environmental fate the only feasible route. {cite:p}`Noga2023`

:::{trust-claim}
:claim-id: clm_b25ccb1e9c7ad497
:claim: Expert-rule and QSAR software predicted phototoxicity with 77% overall accuracy, a machine-learning model classified the pregnancy-risk category of 97 antibiotics with 94.11% external-validation accuracy, and interspecies aquatic-toxicity models passed cross-validation in more than three-quarters of cases.
:cites: Ahuja2024, KelleciCelik2022, Hong2022
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_00675894ea05efae
:claim: Consensus androgen-receptor models built by many groups reached about 80% averaged accuracy, a mechanism-of-action profiler assigned toxic mode correctly for 92% of a large clear-outcome training set, QSAR-derived toxicity values outperformed screening-based predictions for data-poor chemicals, and bacterial-mutagenicity QSAR is judged reliable enough to support regulatory decisions alongside other evidence.
:cites: Mansouri2020, Levet2026, Wignall2018, Tcheremenskaia2021
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_3ea93f22403f5abd
:claim: Regulatory-facing NAM programmes report the same bounded successes — teratogenicity assays predicting 75 known teratogens with 73–82% predictivity, rising to 88% when platforms are combined; zebrafish-embryo exposure correlating with mammalian and human values for reference developmental toxicants; and validated QSAR/read-across meeting OECD thresholds for pesticide developmental-toxicity prioritisation.
:cites: Yao2025, Nawaji2024, Wang2024a
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_189d21e33e050032
:claim: Such models scale to hazard spaces that experiment cannot touch — candidate structures for a single chemical-warfare class can exceed 10,000 compounds, making in silico estimation of environmental fate the only feasible route.
:cites: Noga2023
:claim-type: methodological
:modality: likely
:::

:::{figure} ../figures/fig_sec6_in_silico_performance.png
:name: fig-sec6-in-silico-performance
:width: 100%
**High but narrow — and not a shared accuracy axis.** Reported performance of three in silico/QSAR NAMs, each labelled by its true metric. Different metrics on different endpoints: Ahuja2024 = classification accuracy (77%, phototoxicity); KelleciCelik2022 = external-validation accuracy (94.11%, FDA pregnancy category, 97 antibiotics, chosen over internal 83.82%); Hong2022 = cross-validation success rate of interspecies regression models (>75%), a model-reliability rate, not chemical-level accuracy. Reference standards differ (known phototoxicity, FDA pregnancy categories, experimental aquatic toxicity). Bars use distinct hatches and per-bar metric labels rather than a common accuracy scale, because the three quantities are not interchangeable.::: {cite:p}`Ahuja2024, KelleciCelik2022, Hong2022`

:::{dropdown} 📓 Figure code

```python
"""fig_sec6_in_silico_performance — In silico / QSAR NAM performance across endpoints.

Phase-6 verdict: CAVEAT. The three reported numbers are DIFFERENT metrics on
DIFFERENT endpoints against DIFFERENT reference standards, so they are NOT put
on a shared accuracy axis: each bar is labelled with its true metric, given a
distinct hatch, and annotated with its reference standard. Hong2022's value is a
model-reliability rate (cross-validation success), plotted as a '>=75%' floor.
Data loaded at runtime from evidence/evidence_section_06.json
(comparison in-silico-predictive-performance).
"""
import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt


def _repo_path(rel):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in ['.', '..', '../..', '../../..', here + '/../..', here + '/..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_06.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_06.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_06.json'), encoding='utf-8'))


def disp(doi):
    a = AT[CM[doi]]
    return "%s %s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'in-silico-predictive-performance')
byd = {p['doi']: p for p in fd['papers']}


def first_num(val):
    return float(re.findall(r'[\d.]+', val)[0])


DOI_AH = '10.1177/02611929241256040'   # phototoxicity, classification accuracy 77
DOI_KE = '10.1080/01480545.2022.2113888'  # pregnancy category, external-val accuracy 94.11
DOI_HO = '10.1016/j.envint.2022.107367'   # aquatic, CV success rate >75 (floor)

bars = [
    (DOI_AH, first_num(byd[DOI_AH]['value']), False,
     'Classification\naccuracy',
     'phototoxicity\n(known outcomes)', COLORS['actual_verified'], '//'),
    (DOI_KE, first_num(byd[DOI_KE]['value']), False,
     'External-validation\naccuracy',
     'FDA pregnancy category\n(97 antibiotics)', COLORS['repayment'], '..'),
    (DOI_HO, first_num(byd[DOI_HO]['value']), True,
     'Cross-validation\nsuccess rate\n(model reliability)',
     'experimental\naquatic toxicity', COLORS['secondary_cat'], 'xx'),
]

fig, ax = plt.subplots(figsize=(11.5, 7.0))
x = np.arange(len(bars))
w = 0.6
for i, (doi, val, is_floor, metric, ref, col, hatch) in enumerate(bars):
    ax.bar(i, val, width=w, color=col, edgecolor=COLORS['ink'], linewidth=0.7,
           hatch=hatch, zorder=3)
    vtxt = ("≥%.4g%%" % val) if is_floor else ("%.4g%%" % val)
    ax.text(i, val + 1.5, vtxt, ha='center', va='bottom', fontsize=13,
            fontweight='bold', color=COLORS['ink'], zorder=5)
    if is_floor:
        ax.annotate('', xy=(i, val + 8), xytext=(i, val),
                    arrowprops=dict(arrowstyle='-|>', color=COLORS['ink'], lw=1.4),
                    zorder=6)
    # metric name inside/above bar
    ax.text(i, val / 2, metric, ha='center', va='center', fontsize=9.5,
            fontweight='bold', color='white', zorder=6)
    # reference standard beneath
    ax.text(i, -6, "ref: " + ref, ha='center', va='top', fontsize=9,
            color=COLORS['gray_500'], style='italic')
    # study label above metric label
    ax.text(i, 103, disp(doi), ha='center', va='bottom', fontsize=10,
            color=COLORS['ink'])

ax.axhline(100, color=COLORS['neutral_baseline'], lw=0.75, ls='--', zorder=0)
ax.set_ylim(0, 112)
ax.set_xticks([])
ax.set_ylabel('Reported value (%)  —  each bar is a DIFFERENT metric')
ax.set_yticks(range(0, 101, 20))

fig.text(0.5, -0.05,
         "Not a shared accuracy axis: classification accuracy, external-validation accuracy and a "
         "model-reliability (cross-validation) rate are different quantities on different endpoints.",
         ha='center', fontsize=9, color=COLORS['gray_500'], style='italic')

fig.subplots_adjust(bottom=0.17, top=0.9)
out = _repo_path('figures') + '/fig_sec6_in_silico_performance.png'
save_figure(fig, out)
print('saved:', out)
```

:::

## Human tissue models recover biology that animals miss

Beyond narrow chemical endpoints, the biological case for organoids and organ-on-chip systems is that they recover human-specific physiology absent from rodent models. Multi-organoid and organ-on-chip constructs sustain high viability and organ-specific function — a liver–islet chip held roughly 99% and 96% cell viability over thirty days, {cite:p}`Tao2021` self-organising heart organoids beat autonomously and modelled infarction, {cite:p}`Song2024, Wang2025a, Pan2023` and liver-chips maintained hepatocyte function and detected drug-induced steatosis and hepatotoxicity. {cite:p}`Sunildutt2023, Yun2025, Watanabe2025, Yu2024, Yu2026` Several report quantitative concordance with humans: proximal-tubule chips estimate renal clearance within 10–20% of clinical values after scaling, {cite:p}`Roy2026` a perfused tubule chip reproduced a 35% transporter-mediated permeability change with a reference inhibitor, {cite:p}`Vormann2018` a liver-microphysiological qualification review cites a reported 100% sensitivity and 90% specificity for drug-induced liver injury, {cite:p}`Varmazyad2026` an intestinal-organoid model coupled to kinetics matched clinical diarrhoea incidence for oncology drugs, {cite:p}`Pin2026` and patient-derived colorectal organoids predicted individual cetuximab response with over 80% concordance. {cite:p}`Mirlohi2025` Barrier chips add mechanistic resolution that animal models cannot: a blood–brain-barrier chip attributed a roughly 67% reduction in neutrophil transmigration specifically to pericyte co-culture, {cite:p}`McCloskey2024` and a kidney-organoid screen quantified a 41% loss of proximal-tubule structures under a reference nephrotoxin while flagging a candidate protective drug. {cite:p}`Oishi2024` Organoids express clinically relevant transporters and enzymes that conventional cell lines lack, {cite:p}`Garcia2026, Yuan2026` gut-on-chip and gastrointestinal microphysiological systems recover absorption and first-pass metabolism for oral-bioavailability prediction, {cite:p}`Carius2024, Mathur2025` and barrier chips reconstruct human blood–brain-barrier and gut physiology with in vivo-like permeability and inflammatory responses. {cite:p}`Pediaditakis2022, Shah2016, McCloskey2024, DePalma2025, Kim2023b` The same tissue-engineering advances extend across tumour, lung, kidney, and retinal systems used for drug screening and disease modelling. {cite:p}`Haase2020, Veith2024, Testa2025, Taverna2024, Wisdom2023, Kim2023a, Kim2022, Vormann2018, Nakanoh2025, Nakao2025, Oishi2024, James2024, Parween2026, Birtele2024, Hong2021` The human-relevance advantage is nonetheless partial: standard kidney organoids retain immature proximal tubules with limited transporter expression and off-target cell types, so nephrotoxicity readouts require enhanced protocols before they are reliable. {cite:p}`Bejoy2022, Vanslambrouck2023` Reproducibility engineering is advancing too: bioprinted kidney organoids reached 93–99% viability across 96 wells with 1–4% deposition variability, {cite:p}`Lawlor2020` and a standardised retinal-organoid protocol achieved 100% differentiation efficiency across lines that previously yielded 30–80%. {cite:p}`Harkin2024`

:::{trust-claim}
:claim-id: clm_88fd873c87fb3284
:claim: Multi-organoid and organ-on-chip constructs sustain high viability and organ-specific function — a liver–islet chip held roughly 99% and 96% cell viability over thirty days, self-organising heart organoids beat autonomously and modelled infarction, and liver-chips maintained hepatocyte function and detected drug-induced steatosis and hepatotoxicity.
:cites: Tao2021, Song2024, Wang2025a, Pan2023, Sunildutt2023, Yun2025, Watanabe2025, Yu2024, Yu2026
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d8b6eea126fab680
:claim: Several report quantitative concordance with humans: proximal-tubule chips estimate renal clearance within 10–20% of clinical values after scaling, a perfused tubule chip reproduced a 35% transporter-mediated permeability change with a reference inhibitor, a liver-microphysiological qualification review cites a reported 100% sensitivity and 90% specificity for drug-induced liver injury, an intestinal-organoid model coupled to kinetics matched clinical diarrhoea incidence for oncology drugs, and patient-derived colorectal organoids predicted individual cetuximab response with over 80% concordance.
:cites: Roy2026, Vormann2018, Varmazyad2026, Pin2026, Mirlohi2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_66d4bfbf72609b31
:claim: Barrier chips add mechanistic resolution that animal models cannot: a blood–brain-barrier chip attributed a roughly 67% reduction in neutrophil transmigration specifically to pericyte co-culture, and a kidney-organoid screen quantified a 41% loss of proximal-tubule structures under a reference nephrotoxin while flagging a candidate protective drug.
:cites: McCloskey2024, Oishi2024
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_079c2b65d84d95a5
:claim: Organoids express clinically relevant transporters and enzymes that conventional cell lines lack, gut-on-chip and gastrointestinal microphysiological systems recover absorption and first-pass metabolism for oral-bioavailability prediction, and barrier chips reconstruct human blood–brain-barrier and gut physiology with in vivo-like permeability and inflammatory responses.
:cites: Garcia2026, Yuan2026, Carius2024, Mathur2025, Pediaditakis2022, Shah2016, McCloskey2024, DePalma2025, Kim2023b
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_8316afa2229e6b34
:claim: The same tissue-engineering advances extend across tumour, lung, kidney, and retinal systems used for drug screening and disease modelling.
:cites: Haase2020, Veith2024, Testa2025, Taverna2024, Wisdom2023, Kim2023a, Kim2022, Vormann2018, Nakanoh2025, Nakao2025, Oishi2024, James2024, Parween2026, Birtele2024, Hong2021
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_066064b87182c4bd
:claim: The human-relevance advantage is nonetheless partial: standard kidney organoids retain immature proximal tubules with limited transporter expression and off-target cell types, so nephrotoxicity readouts require enhanced protocols before they are reliable.
:cites: Bejoy2022, Vanslambrouck2023
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_108fdf63c743e111
:claim: Reproducibility engineering is advancing too: bioprinted kidney organoids reached 93–99% viability across 96 wells with 1–4% deposition variability, and a standardised retinal-organoid protocol achieved 100% differentiation efficiency across lines that previously yielded 30–80%.
:cites: Lawlor2020, Harkin2024
:claim-type: empirical
:modality: likely
:::

## The strongest counter-argument: NAMs are ready now

The steelman of the Replacement case is that these methods are no longer aspirational but deployable, and that regulators are already moving. On this reading, next-generation risk assessment using non-animal methods is, in defined settings, entirely appropriate today for assuring chemical safety; {cite:p}`Carmichael2022` economic modelling projects that switching liver-based drug-induced liver injury evaluation to organ-on-chip could save roughly $3 billion annually; {cite:p}`Mehta2025` microphysiological systems are framed as already revolutionising drug development and reducing animal use; {cite:p}`Kopanska2022` and a workshop demonstrated that a non-animal bioactivity-plus-kinetics battery gave protection equivalent to a stand-alone rat repeat-dose study across 46 benchmark exposures. {cite:p}`Rogiers2026` The regulatory infrastructure appears to be following: industry surveys report NAM-based filings replacing large-animal studies and being accepted by health authorities, {cite:p}`Shenton2025, Beken2016` workshops have identified routes to waive the 90-day dog study, {cite:p}`Bishop2023` read-across is an internationally recognised validated method — including NAM-enhanced read-across advanced by EU consortia — with category-based submissions accepted at about 62%, {cite:p}`Rovida2020, Hartung2025b, Pestana2021, Mone2020` and the US FDA Modernization Acts now permit microphysiological systems alongside or instead of animals in investigational filings, {cite:p}`Kumar2026, Rowland2026, Patra2026` and higher-complexity three-dimensional models are being positioned to align with the FDA's stated intent to phase out animal testing for certain drugs. {cite:p}`Cai2025, vanRijt2023` Taken at face value, this is a field on the cusp of retiring whole categories of animal test. The difficulty is that readiness claimed and readiness demonstrated are not the same thing, and the evidence for the gap between them is as concrete as the evidence for the successes.

:::{trust-claim}
:claim-id: clm_f58551cb3da1250f
:claim: On this reading, next-generation risk assessment using non-animal methods is, in defined settings, entirely appropriate today for assuring chemical safety; economic modelling projects that switching liver-based drug-induced liver injury evaluation to organ-on-chip could save roughly $3 billion annually; microphysiological systems are framed as already revolutionising drug development and reducing animal use; and a workshop demonstrated that a non-animal bioactivity-plus-kinetics battery gave protection equivalent to a stand-alone rat repeat-dose study across 46 benchmark exposures.
:cites: Carmichael2022, Mehta2025, Kopanska2022, Rogiers2026
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_c614f728d46564b1
:claim: The regulatory infrastructure appears to be following: industry surveys report NAM-based filings replacing large-animal studies and being accepted by health authorities, workshops have identified routes to waive the 90-day dog study, read-across is an internationally recognised validated method — including NAM-enhanced read-across advanced by EU consortia — with category-based submissions accepted at about 62%, and the US FDA Modernization Acts now permit microphysiological systems alongside or instead of animals in investigational filings, and higher-complexity three-dimensional models are being positioned to align with the FDA's stated intent to phase out animal testing for certain drugs.
:cites: Shenton2025, Beken2016, Bishop2023, Rovida2020, Hartung2025b, Pestana2021, Mone2020, Kumar2026, Rowland2026, Patra2026, Cai2025, vanRijt2023
:claim-type: review_synthesis
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
Proponents assert that non-animal methods are, in certain settings, already appropriate for assuring chemical-ingredient safety, with only regulatory adoption lagging. {cite:p}`Carmichael2022` Against this, a review of the EU endocrine-disruptor framework documents that guidance for predicting adversity with NAMs remains limited and that endocrine-disruptor identification has continued to depend on animal data, requiring further in vivo testing until alternatives are accepted. {cite:p}`Holmer2025` The conflict is readiness claimed versus readiness demonstrated: an in-principle sufficiency argument set against a regulatory record that still leans on animals for the adversity call. It is unresolved, and the resolution is domain-specific — appropriate for some tightly scoped uses, not yet for endocrine adversity.

:::

:::{trust-claim}
:claim-id: clm_53ef7b2a710e86fa
:claim: Proponents assert that non-animal methods are, in certain settings, already appropriate for assuring chemical-ingredient safety, with only regulatory adoption lagging.
:cites: Carmichael2022
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_a80c434c3d228a11
:claim: Against this, a review of the EU endocrine-disruptor framework documents that guidance for predicting adversity with NAMs remains limited and that endocrine-disruptor identification has continued to depend on animal data, requiring further in vivo testing until alternatives are accepted.
:cites: Holmer2025
:claim-type: limitation
:modality: likely
:::

## Regulatory readiness is contested, and validation is thin

The demonstrated-adoption record is markedly more cautious than the promissory one. Barrier analyses converge on a persistent set of scientific, technical, economic, and cultural obstacles that keep NAMs out of routine decision-making; {cite:p}`Sewell2024, Oyetade2025, Villela2022, Osborne2024` many candidate methods exist but very few have been adopted for regulatory use; {cite:p}`Osborne2024, Strickland2023` and the field lacks standardised validation and acceptance criteria, so quality assurance has a structural blind spot. {cite:p}`Ouedraogo2025, Holzer2023, Mitchell2023` Where the underlying models can be audited, the shortfall is quantitative rather than rhetorical: a systematic assessment of 178 in silico thyroid-disruption models found only about 18% fully compliant with the OECD assessment framework, {cite:p}`Judzinska2026` the adverse outcome pathways that anchor mechanistic NAMs are largely immature — most cardiotoxicity-network pathways remain under development or unevaluated {cite:p}`Ladeira2026` — and validating a method by concordance with animal data is itself a weak anchor because many animal tests were never validated for human relevance. {cite:p}`Kopanska2026` Systematic reviews of developmental and reproductive toxicity and of harmonisation across assays reach the same conclusion: the science is promising but its regulatory footprint is thin and uneven. {cite:p}`Kumbhar2026, Kim2026b, Weener2024, Gonnabathula2024` This is where the microphysiological-systems literature splits most sharply.

:::{trust-claim}
:claim-id: clm_c068a1b530c36211
:claim: Barrier analyses converge on a persistent set of scientific, technical, economic, and cultural obstacles that keep NAMs out of routine decision-making; many candidate methods exist but very few have been adopted for regulatory use; and the field lacks standardised validation and acceptance criteria, so quality assurance has a structural blind spot.
:cites: Sewell2024, Oyetade2025, Villela2022, Osborne2024, Strickland2023, Ouedraogo2025, Holzer2023, Mitchell2023
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_46b4bb20d8658e2c
:claim: Where the underlying models can be audited, the shortfall is quantitative rather than rhetorical: a systematic assessment of 178 in silico thyroid-disruption models found only about 18% fully compliant with the OECD assessment framework, the adverse outcome pathways that anchor mechanistic NAMs are largely immature — most cardiotoxicity-network pathways remain under development or unevaluated — and validating a method by concordance with animal data is itself a weak anchor because many animal tests were never validated for human relevance.
:cites: Judzinska2026, Ladeira2026, Kopanska2026
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_67e6341e5691b870
:claim: Systematic reviews of developmental and reproductive toxicity and of harmonisation across assays reach the same conclusion: the science is promising but its regulatory footprint is thin and uneven.
:cites: Kumbhar2026, Kim2026b, Weener2024, Gonnabathula2024
:claim-type: review_synthesis
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
One strand frames microphysiological systems as bioengineering organ architecture and function so as to revolutionise drug development, reduce animal testing, and enable personalised medicine. {cite:p}`Hartung2025a` An expert workshop assessment counters that these systems have neither been widely adopted by the pharmaceutical industry nor reached regulated drug-authorisation processes at all. {cite:p}`Marx2020` The disagreement is transformative promise versus adoption reality: the same platforms are described as already transforming the field and as not yet in regulated use. It remains open, and the interposed reviews suggest the truth is developmental — real capability, minimal regulated deployment, with data-sharing and standardisation named as the rate-limiting steps.::: {cite:p}`Marx2025, Fabre2020, Brown2024`

:::{trust-claim}
:claim-id: clm_cb442711d183b946
:claim: One strand frames microphysiological systems as bioengineering organ architecture and function so as to revolutionise drug development, reduce animal testing, and enable personalised medicine.
:cites: Hartung2025a
:claim-type: speculation
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_324cbbf1d6089244
:claim: An expert workshop assessment counters that these systems have neither been widely adopted by the pharmaceutical industry nor reached regulated drug-authorisation processes at all.
:cites: Marx2020
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_819a6eb0bfb98486
:claim: It remains open, and the interposed reviews suggest the truth is developmental — real capability, minimal regulated deployment, with data-sharing and standardisation named as the rate-limiting steps.
:cites: Marx2025, Fabre2020, Brown2024
:claim-type: review_synthesis
:modality: likely
:::

## Narrow validity: coverage gaps and metabolic blind spots

Even where NAMs perform well, their validity is bounded by what they can mechanistically represent, and the boundaries are being mapped. In skin sensitisation, no standardised in vitro assay exists for the T-cell-activation key event, so that step of the pathway cannot be measured non-animally; {cite:p}`Ezendam2016` because component-assay limitations propagate, defined approaches yield inconclusive calls for borderline or out-of-domain chemicals; {cite:p}`Macmillan2022, Maxwell2014` and reference data must be chosen so as not to reproduce the limitations of the animal assay being replaced. {cite:p}`Kolle2020`

:::{trust-claim}
:claim-id: clm_635165357f2a6333
:claim: In skin sensitisation, no standardised in vitro assay exists for the T-cell-activation key event, so that step of the pathway cannot be measured non-animally; because component-assay limitations propagate, defined approaches yield inconclusive calls for borderline or out-of-domain chemicals; and reference data must be chosen so as not to reproduce the limitations of the animal assay being replaced.
:cites: Ezendam2016, Macmillan2022, Maxwell2014, Kolle2020
:claim-type: limitation
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
The OECD defined-approach guideline for skin sensitisation is presented as the first of its kind and as a precedent for adopting non-animal methods with performance equivalent to or better than animal tests. {cite:p}`Casati2022` A case-study analysis shows that, because the limitations of the individual in chemico, in vitro, and in silico assays carry through, the defined approaches can return inconclusive predictions for chemicals in the borderline range or outside the applicability domain. {cite:p}`Macmillan2022` The conflict concerns the performance of the same defined-approach framework: equal-or-better replacement versus an approach that inherits its components' blind spots. It is unresolved and hinges on chemical domain — reliable inside the validated space, indeterminate at its edges.

:::

:::{trust-claim}
:claim-id: clm_b892d24e57739e7e
:claim: The OECD defined-approach guideline for skin sensitisation is presented as the first of its kind and as a precedent for adopting non-animal methods with performance equivalent to or better than animal tests.
:cites: Casati2022
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_ba31b88863fe76f2
:claim: A case-study analysis shows that, because the limitations of the individual in chemico, in vitro, and in silico assays carry through, the defined approaches can return inconclusive predictions for chemicals in the borderline range or outside the applicability domain.
:cites: Macmillan2022
:claim-type: limitation
:modality: likely
:::

Metabolism is the recurring blind spot. A liver-on-chip genotoxicity assay detected several genotoxicants but missed benzo[a]pyrene on two endpoints, showing endpoint-dependent, incomplete concordance; {cite:p}`Kopp2024` benchmarking six in silico metabolism simulators against literature metabolites found precision of only 1.1–29% and sensitivity of 14.7–28.3%, {cite:p}`Boyce2022` with expert-driven metabolic grouping outperforming automated tools; {cite:p}`Enoch2026` and a next-generation risk assessment of an anti-androgen underestimated risk until the active metabolite was explicitly modelled. {cite:p}`vanTongeren2022` The kinetic layer that converts an in vitro concentration into a human dose is itself only moderately accurate: a generic high-throughput physiologically based model predicted peak plasma concentration within tenfold of in vivo values for only half of chemicals and within threefold for 31%, with a systematic lipophilicity-dependent bias. {cite:p}`Spaenig2026` These limits are why NAM outputs are typically embedded in weight-of-evidence and extrapolation workflows rather than used alone — a developmental-toxicity extrapolation found that using all in vitro assays, not the developmental subset, gave the most conservative human-equivalent dose, {cite:p}`Linakis2025` and a stem-cell-plus-modelling approach derived bisphenol-A reference doses close to a regulatory value without any animals. {cite:p}`Ni2024, Chang2022, Hines2022, Bosgra2015, Idakwo2018, Chou2022` The black-box character of many machine-learning components compounds the interpretability problem regulators must resolve before trusting these chains, {cite:p}`Chou2022, Idakwo2018` and the developmental-neurotoxicity battery divides its own community.

:::{trust-claim}
:claim-id: clm_ea37827edaaf0f69
:claim: A liver-on-chip genotoxicity assay detected several genotoxicants but missed benzo[a]pyrene on two endpoints, showing endpoint-dependent, incomplete concordance; benchmarking six in silico metabolism simulators against literature metabolites found precision of only 1.1–29% and sensitivity of 14.7–28.3%, with expert-driven metabolic grouping outperforming automated tools; and a next-generation risk assessment of an anti-androgen underestimated risk until the active metabolite was explicitly modelled.
:cites: Kopp2024, Boyce2022, Enoch2026, vanTongeren2022
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_615b2ee1da50b2d3
:claim: The kinetic layer that converts an in vitro concentration into a human dose is itself only moderately accurate: a generic high-throughput physiologically based model predicted peak plasma concentration within tenfold of in vivo values for only half of chemicals and within threefold for 31%, with a systematic lipophilicity-dependent bias.
:cites: Spaenig2026
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_cf9848d69a0804a6
:claim: These limits are why NAM outputs are typically embedded in weight-of-evidence and extrapolation workflows rather than used alone — a developmental-toxicity extrapolation found that using all in vitro assays, not the developmental subset, gave the most conservative human-equivalent dose, and a stem-cell-plus-modelling approach derived bisphenol-A reference doses close to a regulatory value without any animals.
:cites: Linakis2025, Ni2024, Chang2022, Hines2022, Bosgra2015, Idakwo2018, Chou2022
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d9df3c267ca4e38a
:claim: The black-box character of many machine-learning components compounds the interpretability problem regulators must resolve before trusting these chains, and the developmental-neurotoxicity battery divides its own community.
:cites: Chou2022, Idakwo2018
:claim-type: limitation
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
An expert panel concluded that the human developmental-neurotoxicity in vitro battery may serve for initial screening but is not yet a complete or surrogate approach for classifying a chemical as a human developmental neurotoxicant, and needs further validation. {cite:p}`Juberg2023` A data-generating group presented the same class of battery as a promising approach already usable for neurodevelopmental hazard assessment and prioritisation, while noting its rankings diverged from high-throughput screening. {cite:p}`Klose2021` The conflict is over regulatory readiness of one method: insufficient stand-alone tool versus deployable prioritisation approach. It is unresolved, and the disagreement tracks the vantage point — panel review versus method developer.::: {cite:p}`Fritsche2018, Schmidt2016`

:::{trust-claim}
:claim-id: clm_7bde574d0eb27cc6
:claim: An expert panel concluded that the human developmental-neurotoxicity in vitro battery may serve for initial screening but is not yet a complete or surrogate approach for classifying a chemical as a human developmental neurotoxicant, and needs further validation.
:cites: Juberg2023
:claim-type: limitation
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_35ccc8ba9e2c1cd7
:claim: A data-generating group presented the same class of battery as a promising approach already usable for neurodevelopmental hazard assessment and prioritisation, while noting its rankings diverged from high-throughput screening.
:cites: Klose2021
:claim-type: methodological
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_38c1a5e3a3bb0928
:claim: It is unresolved, and the disagreement tracks the vantage point — panel review versus method developer.
:cites: Fritsche2018, Schmidt2016
:claim-type: review_synthesis
:modality: likely
:::

## The same reproducibility problem, in a new medium

The deepest continuity between NAMs and the animal models they replace is that both suffer variable readouts, and the NAM literature is beginning to quantify it with the same candour applied to animal studies elsewhere in this review. Donor-to-donor variability drives a liver-chip's urea-production coefficient of variation from under 5% on day 1 to 20% by day 7; {cite:p}`Kong2026` an independent robustness study of a commercial liver microphysiological system found stable function to 17 days but appreciable within- and between-study variability; {cite:p}`Kato2022, Lim2023` organoids exhibit necrotic cores and considerable variability from one preparation to the next; {cite:p}`Nickels2020` standard viability assays give inaccurate readouts in three-dimensional constructs; {cite:p}`Dominijanni2021` and the zebrafish developmental-toxicity protocol varies between laboratories, producing discordant data for identical compounds. {cite:p}`Hoyberghs2020, Jeffries2015, vonHellfeld2022` The community response is qualification and quality-control criteria — coefficient-of-variation thresholds for organoid assays, {cite:p}`Wittich2026` donor-specific control thresholds for a vessel chip, {cite:p}`Weener2024` and reproducibility-grading schemes for liver models {cite:p}`Varmazyad2026` — alongside consortium efforts to define contexts of use and even to build animal-tissue chips that could benchmark their human counterparts. {cite:p}`Fabre2020, Brown2024, Marx2025` These are the same standardisation levers, not yet pulled, that the animal field has debated for decades, and they depend on automation and biobanking to make organoid generation reproducible at scale. {cite:p}`Fan2026, He2026, Louey2021` The irony runs deeper: the animal reference standard against which NAMs are validated is itself only moderately reproducible, with standardised endocrine assays replicating at 72% and 74% and, as the same review reports, rodent carcinogenicity outcomes agreeing only 65–86% between sexes of one species and 36–74% between rat and mouse, {cite:p}`Karmaus2026` so NAM concordance is being measured against a shaky yardstick — which is precisely why one validation-framework argues concordance with animal data is a scientifically weak anchor and that human relevance, not animal agreement, should be the criterion. {cite:p}`Kopanska2026` That a complex model can be less reliable than a simple one is shown head-to-head.

:::{trust-claim}
:claim-id: clm_3d0e46ddb0d7bba4
:claim: Donor-to-donor variability drives a liver-chip's urea-production coefficient of variation from under 5% on day 1 to 20% by day 7; an independent robustness study of a commercial liver microphysiological system found stable function to 17 days but appreciable within- and between-study variability; organoids exhibit necrotic cores and considerable variability from one preparation to the next; standard viability assays give inaccurate readouts in three-dimensional constructs; and the zebrafish developmental-toxicity protocol varies between laboratories, producing discordant data for identical compounds.
:cites: Kong2026, Kato2022, Lim2023, Nickels2020, Dominijanni2021, Hoyberghs2020, Jeffries2015, vonHellfeld2022
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_1562d8a88cac4ff8
:claim: The community response is qualification and quality-control criteria — coefficient-of-variation thresholds for organoid assays, donor-specific control thresholds for a vessel chip, and reproducibility-grading schemes for liver models — alongside consortium efforts to define contexts of use and even to build animal-tissue chips that could benchmark their human counterparts.
:cites: Wittich2026, Weener2024, Varmazyad2026, Fabre2020, Brown2024, Marx2025
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_622bd94ec569f00e
:claim: These are the same standardisation levers, not yet pulled, that the animal field has debated for decades, and they depend on automation and biobanking to make organoid generation reproducible at scale.
:cites: Fan2026, He2026, Louey2021
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_fd0a6956653ed15a
:claim: The irony runs deeper: the animal reference standard against which NAMs are validated is itself only moderately reproducible, with standardised endocrine assays replicating at 72% and 74% and, as the same review reports, rodent carcinogenicity outcomes agreeing only 65–86% between sexes of one species and 36–74% between rat and mouse, so NAM concordance is being measured against a shaky yardstick — which is precisely why one validation-framework argues concordance with animal data is a scientifically weak anchor and that human relevance, not animal agreement, should be the criterion.
:cites: Karmaus2026, Kopanska2026
:claim-type: limitation
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
An independent robustness study of a liver microphysiological system found appreciable within- and between-study variability that undercuts its high-throughput utility. {cite:p}`Kato2022` A drug-development perspective frames microphysiological systems as delivering more standardised, predictive, physiologically relevant responses in living tissues. {cite:p}`Kopec2021` The conflict is over the reproducibility of the readouts themselves: measured variability versus asserted standardisation. It is unresolved — and a comparative intestinal-permeability validation reinforces the sceptical side, finding that microphysiological and enteroid systems added variability while a simple static monolayer gave the most accurate human absorption predictions, so complexity did not guarantee predictivity.::: {cite:p}`Moyer2025`

:::{trust-claim}
:claim-id: clm_0557a7fb753725ae
:claim: An independent robustness study of a liver microphysiological system found appreciable within- and between-study variability that undercuts its high-throughput utility.
:cites: Kato2022
:claim-type: limitation
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_b608383bd8bfb22c
:claim: A drug-development perspective frames microphysiological systems as delivering more standardised, predictive, physiologically relevant responses in living tissues.
:cites: Kopec2021
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_b38dbae184c1f04c
:claim: It is unresolved — and a comparative intestinal-permeability validation reinforces the sceptical side, finding that microphysiological and enteroid systems added variability while a simple static monolayer gave the most accurate human absorption predictions, so complexity did not guarantee predictivity.
:cites: Moyer2025
:claim-type: comparative
:modality: likely
:::

The direction of a NAM's error can even flip with cell type, which cautions against any generic claim that three dimensions are more predictive than two. Three-dimensional liver spheroids built from a proliferating cell line were more resistant to a hepatotoxicant than their two-dimensional counterparts, {cite:p}`Hong2021` whereas spheroids built from non-dividing stem-cell-derived hepatocytes trended toward stronger toxicity than two-dimensional cultures. {cite:p}`Sirenko2016` The divergence appears cell-type driven, and it means that the same architectural upgrade can raise or lower apparent sensitivity depending on the biology underneath — a variability that only disciplined, comparable reporting can resolve. {cite:p}`Zhou2026, Zhang2024a, Liu2024, Lee2025a`

:::{trust-claim}
:claim-id: clm_974a9907fb6254ad
:claim: Three-dimensional liver spheroids built from a proliferating cell line were more resistant to a hepatotoxicant than their two-dimensional counterparts, whereas spheroids built from non-dividing stem-cell-derived hepatocytes trended toward stronger toxicity than two-dimensional cultures.
:cites: Hong2021, Sirenko2016
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_17a0c7b6bb718917
:claim: The divergence appears cell-type driven, and it means that the same architectural upgrade can raise or lower apparent sensitivity depending on the biology underneath — a variability that only disciplined, comparable reporting can resolve.
:cites: Zhou2026, Zhang2024a, Liu2024, Lee2025a
:claim-type: causal
:modality: suggestive
:::

## The debt relocates: NAMs generate data that will be wasted too

The pivotal observation for this review is that Replacement does not reduce the data-stewardship burden; it multiplies it. High-throughput and in silico streams each interrogate hundreds to thousands of chemicals: 293 chemicals screened for a single thyroid target, {cite:p}`Wang2018` 1,060 chemicals across 93 transcripts in a hepatic screen, {cite:p}`Franzosa2021` 2,171 chemicals mapped onto 52 hepatotoxicity key events, {cite:p}`Russo2023` 4,165 compounds bioprofiled for a cardiotoxicity pathway, {cite:p}`Ehrlich2024` and screening campaigns filling in vivo benchmarks that existed for only 34 of 67 monitored chemicals. {cite:p}`Corsi2019, Saili2019, Fay2018, Isaacs2022, Onyango2023, Karmaus2025, Suh2018` These are exactly the high-dimensional outputs that {ref}`sec-fair-preclinical` showed accumulate faster than they are curated, and the trend is toward more data, not less: high-throughput exposure methods deliberately expand chemical coverage far beyond what traditional assessment reached, {cite:p}`Isaacs2022, Onyango2023` while every mechanistic screen that maps assays onto adverse outcome pathways adds another layer of results that must be stored, versioned, and made interpretable to be reused. {cite:p}`Fay2018, Saili2019, Karmaus2025, Suh2018` The resources built to make such data reusable are real but non-comparable in scale, which {numref}`fig-sec6-nam-data-scale` presents as an inventory rather than a ranking: a curated chemical suspect-list exchange of more than 100,000 substances, {cite:p}`MohammedTaha2022` integrated nanomaterial libraries exceeding 2,000 materials, {cite:p}`Afantitis2020` and a workflow reusing 25 public proteomic datasets. {cite:p}`Bahl2023, Jeliazkova2022` The very heterogeneity that makes these figures un-poolable in the plot is what makes the underlying data hard to reuse in practice.

:::{trust-claim}
:claim-id: clm_732ecccc80664fac
:claim: High-throughput and in silico streams each interrogate hundreds to thousands of chemicals: 293 chemicals screened for a single thyroid target, 1,060 chemicals across 93 transcripts in a hepatic screen, 2,171 chemicals mapped onto 52 hepatotoxicity key events, 4,165 compounds bioprofiled for a cardiotoxicity pathway, and screening campaigns filling in vivo benchmarks that existed for only 34 of 67 monitored chemicals.
:cites: Wang2018, Franzosa2021, Russo2023, Ehrlich2024, Corsi2019, Saili2019, Fay2018, Isaacs2022, Onyango2023, Karmaus2025, Suh2018
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_c38e135a27e2e78f
:claim: These are exactly the high-dimensional outputs that showed accumulate faster than they are curated, and the trend is toward more data, not less: high-throughput exposure methods deliberately expand chemical coverage far beyond what traditional assessment reached, while every mechanistic screen that maps assays onto adverse outcome pathways adds another layer of results that must be stored, versioned, and made interpretable to be reused.
:cites: Isaacs2022, Onyango2023, Fay2018, Saili2019, Karmaus2025, Suh2018
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_22ff115748887852
:claim: The resources built to make such data reusable are real but non-comparable in scale, which presents as an inventory rather than a ranking: a curated chemical suspect-list exchange of more than 100,000 substances, integrated nanomaterial libraries exceeding 2,000 materials, and a workflow reusing 25 public proteomic datasets.
:cites: MohammedTaha2022, Afantitis2020, Bahl2023, Jeliazkova2022
:claim-type: empirical
:modality: established
:::

:::{figure} ../figures/fig_sec6_nam_data_scale.png
:name: fig-sec6-nam-data-scale
:width: 100%
**A new stewardship debt, in incompatible units.** Inventory of curated NAM/chemical data resources built for reuse, shown as separate callouts rather than on a shared axis. Counts are in incompatible units (100,000 chemical substances vs >2,000 nanomaterials vs 25 datasets); the four-order-of-magnitude spread is a unit artifact and does not represent comparable resource sizes. Entries: a FAIR chemical suspect-list exchange with more than 100,000 unique substances, {cite:p}`MohammedTaha2022` integrated nanomaterial libraries with more than 2,000 nanomaterials, {cite:p}`Afantitis2020` and a FAIR proteomic workflow reusing 25 public datasets. {cite:p}`Bahl2023` The point is not which resource is largest but that non-animal research is now generating high-dimensional data that will incur a fresh ethical and scientific debt unless stewarded to FAIR standards from the outset.
:::

:::{dropdown} 📓 Figure code

```python
"""fig_sec6_nam_data_scale — Scale of curated NAM/chemical data resources built for FAIR reuse.

Phase-6 verdict: CAVEAT_FORCED_FROM_REDESIGN. MANDATORY restructure: DO NOT plot
on a shared numeric axis. The three counts are in incompatible units (chemical
substances vs nanomaterials vs datasets), so they are rendered as an
inventory of separate single-value callouts, each with its unit made explicit —
there is deliberately no bar-height comparison. Data loaded at runtime from
evidence/evidence_section_06.json (comparison nam-fair-data-resource-scale).
"""
import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def _repo_path(rel):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in ['.', '..', '../..', '../../..', here + '/../..', here + '/..']:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(rel)


import sys
sys.path.insert(0, os.path.dirname(_repo_path('figures/notebooks/shared_style.py')))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

apply_style()

EV = json.load(open(_repo_path('evidence/evidence_section_06.json'), encoding='utf-8'))
AT = json.load(open(_repo_path('evidence/authortable_section_06.json'), encoding='utf-8'))
CM = json.load(open(_repo_path('evidence/citemap_section_06.json'), encoding='utf-8'))


def disp(doi):
    a = AT[CM[doi]]
    return "%s %s" % (a['citet_display'], a['year'])


fd = next(x for x in EV['figure_data']
          if x['comparison_id'] == 'nam-fair-data-resource-scale')
byd = {p['doi']: p for p in fd['papers']}

# resource, type, count, unit — units are DELIBERATELY different (not comparable)
DOI_NORMAN = '10.1186/s12302-022-00680-6'
DOI_NANO = '10.1016/j.csbj.2020.02.023'
DOI_PROT = '10.1186/s13321-023-00710-2'

cards = [
    (DOI_NORMAN, byd[DOI_NORMAN]['value'], 'chemical\nsubstances',
     'Curated suspect-list\nexchange', COLORS['actual_verified']),
    (DOI_NANO, byd[DOI_NANO]['value'], 'nanomaterials',
     'Integrated\nnanomaterial libraries', COLORS['secondary_cat']),
    (DOI_PROT, byd[DOI_PROT]['value'], 'public proteomic\ndatasets',
     'FAIR proteomic\nmeta-analysis workflow', COLORS['repayment']),
]

fig, ax = plt.subplots(figsize=(12.5, 5.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(6, 5.6, 'Curated NAM / chemical data resources built for reuse',
        ha='center', va='center', fontsize=15, fontweight='bold',
        color=COLORS['ink'])
ax.text(6, 5.15, 'an inventory — units differ, so the entries are NOT on a common scale',
        ha='center', va='center', fontsize=10.5, style='italic',
        color=COLORS['gray_500'])

cx = [2.0, 6.0, 10.0]
cw, chh = 3.3, 3.4
for x, (doi, count, unit, rtype, col) in zip(cx, cards):
    box = FancyBboxPatch((x - cw / 2, 1.0), cw, chh,
                         boxstyle="round,pad=0.06,rounding_size=0.18",
                         linewidth=1.6, edgecolor=col, facecolor='white', zorder=2)
    ax.add_patch(box)
    # colour header strip
    ax.add_patch(FancyBboxPatch((x - cw / 2, 1.0 + chh - 0.7), cw, 0.7,
                 boxstyle="round,pad=0.02,rounding_size=0.1",
                 linewidth=0, facecolor=col, alpha=0.20, zorder=3))
    ax.text(x, 1.0 + chh - 0.35, rtype, ha='center', va='center',
            fontsize=11, fontweight='bold', color=col, zorder=4)
    # big count number
    ax.text(x, 2.55, count, ha='center', va='center', fontsize=27,
            fontweight='bold', color=col, zorder=4)
    # explicit unit
    ax.text(x, 1.75, unit, ha='center', va='center', fontsize=11.5,
            color=COLORS['gray_700'], zorder=4)
    # source
    ax.text(x, 0.55, disp(doi), ha='center', va='center', fontsize=10,
            color=COLORS['ink'], zorder=4)

ax.text(6, 0.02,
        "Counts measure fundamentally different entities across four orders of magnitude — "
        "a unit artifact, not a size ranking.",
        ha='center', va='center', fontsize=9, style='italic', color=COLORS['gray_500'])

out = _repo_path('figures') + '/fig_sec6_nam_data_scale.png'
save_figure(fig, out)
print('saved:', out)
```

:::

That these resources exist does not mean the data flow reuses itself, and the NAM community has independently rediscovered the FAIR problem. Curators of an integrated chemical database report that missing metadata routinely block data integration, forcing manual literature research before datasets can be combined; {cite:p}`Daniel2022, Watford2019` a workshop on AI in chemical risk assessment concluded that FAIR data are not best practice but a prerequisite for trustworthy model outputs; {cite:p}`Gant2026` and nanosafety and adverse-outcome-pathway groups now argue for capturing FAIR metadata at the point of data generation and for dedicated stewardship roles. {cite:p}`Papadiamantis2020, Mortensen2025, Baskaran2025` The stewardship burden is concrete: nanosafety groups offer eight specific recommendations for capturing metadata at the point of generation and argue for dedicated data-shepherd roles precisely because retrofitting metadata later routinely fails. {cite:p}`Papadiamantis2020, Baskaran2025` Yet FAIRification remains young and unevenly implemented across health and toxicology data, {cite:p}`Inau2023` the lack of harmonisation across assays, platforms, and analytical workflows is a named barrier to regulatory adoption, {cite:p}`Kim2026b, Hartung2025a` standardised documentation templates aligned to reporting guidance are only now being adopted by consortia, {cite:p}`Weber2025` and building even one reusable knowledge base demanded heavy investment in governance, authorisation, and quality documentation. {cite:p}`Yang2021` The read-across literature shows the same unresolved tension: public NAM data can be assembled to support a regulatory conclusion, yet the absence of consensus on the required evidence hampers acceptance. {cite:p}`Ball2016, Pestana2021, Leist2025` Non-animal research is, in short, generating precisely the kind of large, heterogeneous, under-curated dataset whose waste this review has traced through animal experiments — and it is doing so now, before the stewardship habits that would prevent the waste are in place.

:::{trust-claim}
:claim-id: clm_f3c2df0a0853cf47
:claim: Curators of an integrated chemical database report that missing metadata routinely block data integration, forcing manual literature research before datasets can be combined; a workshop on AI in chemical risk assessment concluded that FAIR data are not best practice but a prerequisite for trustworthy model outputs; and nanosafety and adverse-outcome-pathway groups now argue for capturing FAIR metadata at the point of data generation and for dedicated stewardship roles.
:cites: Daniel2022, Watford2019, Gant2026, Papadiamantis2020, Mortensen2025, Baskaran2025
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d6a13bd337f06199
:claim: The stewardship burden is concrete: nanosafety groups offer eight specific recommendations for capturing metadata at the point of generation and argue for dedicated data-shepherd roles precisely because retrofitting metadata later routinely fails.
:cites: Papadiamantis2020, Baskaran2025
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_15551c42677691e3
:claim: Yet FAIRification remains young and unevenly implemented across health and toxicology data, the lack of harmonisation across assays, platforms, and analytical workflows is a named barrier to regulatory adoption, standardised documentation templates aligned to reporting guidance are only now being adopted by consortia, and building even one reusable knowledge base demanded heavy investment in governance, authorisation, and quality documentation.
:cites: Inau2023, Kim2026b, Hartung2025a, Weber2025, Yang2021
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_70aedf89f2540739
:claim: The read-across literature shows the same unresolved tension: public NAM data can be assembled to support a regulatory conclusion, yet the absence of consensus on the required evidence hampers acceptance.
:cites: Ball2016, Pestana2021, Leist2025
:claim-type: review_synthesis
:modality: contested
:::

The conclusion for the review's central argument is uncomfortable but clear. NAMs can repay part of the ethical debt by removing animals from specific, well-bounded tests, and for endpoints such as genotoxicity, skin sensitisation, and several in silico hazards that repayment is already bankable. But a NAM dataset left unfindable, unstandardised, and unreused wastes the scientific effort that produced it just as an unshared animal dataset wastes the animal, and it forecloses the reuse that would let the next question be answered without generating fresh data — animal or otherwise. Replacement without data welfare therefore discharges only the front half of the obligation. The recurring failure across control-animal data in, {ref}`sec-virtual-controls` the FAIR shortfall in, {ref}`sec-fair-preclinical` and the NAM data described here is one failure with one cause, not three: stewardship is nobody's job and earns nobody credit. {ref}`sec-incentives` turns to that shared cause directly, examining how the reward system of research prices data stewardship at essentially zero — and why, until that price changes, every new methodology will re-incur the debt that {ref}`sec-conclusion` argues the field can no longer afford.

:::{evidence-explorer}
:evidence-dir: ../evidence
:height: 800px
:::

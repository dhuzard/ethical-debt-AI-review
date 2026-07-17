(sec-incentives)=

# Incentive Structures and the Political Economy of Research Data

The preceding discussion in {ref}`sec-nams-data` showed that the stewardship failure is not confined to animal-derived data: it recurs for virtual control groups, for new approach methodologies, and across the FAIR audits of, {ref}`sec-fair-preclinical` surviving every change of data type. A failure this stable across otherwise unrelated domains is the signature of a common cause rather than a run of local accidents. This section locates that cause in the reward structure of research itself. The argument is one of political economy: the behaviours that generate the data-welfare debt — leaving datasets unshared, incomplete, or unfindable — are individually rational responses to an evaluation system that pays generously for publication counts and journal prestige while pricing data stewardship at essentially zero. Several converging diagnoses frame the modern research economy as one in which reward systems incentivise quantity over quality and novelty over reliability, {cite:p}`Ioannidis2014b, Young2008` in which competition for funding and quantitative performance metrics has grown steadily more perverse over half a century, {cite:p}`Edwards2017, Alberts2014` and in which the overuse of the journal impact factor persists precisely because it serves the individual interests of scientists, journals, and administrators even as it corrodes the collective enterprise — a textbook tragedy of the commons. {cite:p}`Casadevall2014, Chapman2019` Read this way, the debt is not a malfunction of the system but one of its predictable products.

:::{trust-claim}
:claim-id: clm_a0c0019c191ee739
:claim: Several converging diagnoses frame the modern research economy as one in which reward systems incentivise quantity over quality and novelty over reliability, in which competition for funding and quantitative performance metrics has grown steadily more perverse over half a century, and in which the overuse of the journal impact factor persists precisely because it serves the individual interests of scientists, journals, and administrators even as it corrodes the collective enterprise — a textbook tragedy of the commons.
:cites: Ioannidis2014b, Young2008, Edwards2017, Alberts2014, Casadevall2014, Chapman2019
:claim-type: review_synthesis
:modality: established
:::

The most direct evidence comes from content analysis of the documents that actually govern academic careers. In an international sample of biomedical promotion and tenure guidelines, {cite:t}`Rice2020` found that peer-reviewed publications were mentioned as a criterion in almost every institution while data sharing appeared in only one percent and open-access publishing or registration in none; a matching study of research-intensive North American universities showed the Journal Impact Factor written explicitly into review, promotion, and tenure at a substantial minority of institutions, concentrated overwhelmingly at the most research-intensive campuses and framed in supportive terms. {cite:p}`McKiernan2019` This asymmetry is corroborated by broader analyses of the same document class: evaluation systematically privileges academic-facing outputs and citation metrics while disregarding the public dimensions of scholarship, {cite:p}`Alperin2019, Schimanski2018` and faculty themselves describe the "quality", "prestige", and "impact" of journals in overlapping, ill-defined ways that cannot bear the evaluative weight placed on them. {cite:p}`Morales2021` The instruments are moreover weak proxies for what they claim to measure: citation counts and impact factors are inconsistent and sometimes negative predictors of statistical accuracy, evidential value, and replicability, {cite:p}`Dougherty2022` and journal-level metrics may recognise as little as ten to twenty percent of genuinely influential work. {cite:p}`Arabi2025` {numref}`fig-sec7-rpt-criteria` places the publication-count and data-sharing prevalences side by side, exposing an asymmetry that prose alone would understate.

:::{trust-claim}
:claim-id: clm_bc0c549d5a40139d
:claim: In an international sample of biomedical promotion and tenure guidelines, found that peer-reviewed publications were mentioned as a criterion in almost every institution while data sharing appeared in only one percent and open-access publishing or registration in none; a matching study of research-intensive North American universities showed the Journal Impact Factor written explicitly into review, promotion, and tenure at a substantial minority of institutions, concentrated overwhelmingly at the most research-intensive campuses and framed in supportive terms.
:cites: Rice2020, McKiernan2019
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_2dbdceee821cc406
:claim: This asymmetry is corroborated by broader analyses of the same document class: evaluation systematically privileges academic-facing outputs and citation metrics while disregarding the public dimensions of scholarship, and faculty themselves describe the "quality", "prestige", and "impact" of journals in overlapping, ill-defined ways that cannot bear the evaluative weight placed on them.
:cites: Alperin2019, Schimanski2018, Morales2021
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_997b4b5d60df0a31
:claim: The instruments are moreover weak proxies for what they claim to measure: citation counts and impact factors are inconsistent and sometimes negative predictors of statistical accuracy, evidential value, and replicability, and journal-level metrics may recognise as little as ten to twenty percent of genuinely influential work.
:cites: Dougherty2022, Arabi2025
:claim-type: empirical
:modality: likely
:::

:::{figure} ../figures/fig_sec7_rpt_criteria.png
:name: fig-sec7-rpt-criteria
:width: 100%
**What researcher-evaluation systems reward.** Prevalence of criteria in formal review, promotion, and tenure (RPT) documents. Bars are prevalence of different RPT criteria across different populations: Rice2020 peer-reviewed-publication mention (95%) and data-sharing mention (1%) in 92 international biomedical-faculty guidelines; McKiernan2019 JIF mention (40%) among research-intensive US/Canada universities only (18% master's, 0% baccalaureate). Confirm the Rice2020 bar definition: 95% = any mention of peer-reviewed publications; 35% (a separate figure) = mention of a specific publication count. Each bar is labelled by its population and definition and no single population is implied; traditional publication/impact criteria (solid) are distinguished from open-science criteria (hatched). Values from {cite:p}`Rice2020` and {cite:p}`McKiernan2019`.
:::

:::{dropdown} 📓 Figure code

```python
import os
import re
import sys
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_07.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_07.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIND = {f["cite_key"]: f for f in EV["findings"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD["rpt-evaluation-criteria"]
papers = {p["doi"]: p for p in comp["papers"]}

# Rice2020 combined "95 / 1" -> publication-mention 95, data-sharing 1
rice_vals = re.findall(r"[\d.]+", papers["10.1136/bmj.m2081"]["value"])
rice_pub, rice_data = float(rice_vals[0]), float(rice_vals[1])
# McKiernan2019 "40" -> JIF mention among research-intensive institutions
mck_jif = float(re.findall(r"[\d.]+", papers["10.7554/elife.47338"]["value"])[0])
# Specific publication-count requirement (35%): from the Rice2020 finding effect_size
rice_count = float(re.search(r"(\d+)% require a specific number", FIND["Rice2020"]["effect_size"]).group(1))

# Each bar: (label, value, category)  category in {"traditional", "open"}
bars = [
    ("Peer-reviewed publication mention\n(Rice et al. 2020; 92 intl. biomedical guidelines)", rice_pub, "traditional"),
    ("Journal Impact Factor use\n(McKiernan et al. 2019; research-intensive only)", mck_jif, "traditional"),
    ("Specific publication-count requirement\n(Rice et al. 2020)", rice_count, "traditional"),
    ("Data-sharing mention\n(Rice et al. 2020)", rice_data, "open"),
]

cat_style = {
    "traditional": dict(color=COLORS["neutral_baseline"], hatch="", label="Traditional publication / impact criteria"),
    "open":        dict(color=COLORS["repayment"], hatch="////", label="Open-science criteria (data sharing)"),
}

fig, ax = plt.subplots(figsize=(11, 5.6))
fig.subplots_adjust(left=0.42, right=0.965, bottom=0.20, top=0.90)

y = np.arange(len(bars))[::-1]  # first bar at top
for yi, (label, val, cat) in zip(y, bars):
    st = cat_style[cat]
    ax.barh(yi, val, height=0.62, color=st["color"], edgecolor=COLORS["ink"],
            linewidth=0.7, hatch=st["hatch"], zorder=3)
    ax.annotate(f"{val:g}%", (val, yi), xytext=(6, 0), textcoords="offset points",
                va="center", ha="left", fontsize=12, fontweight="bold", color=COLORS["ink"])

# Annotate the McKiernan bar with the population breakdown
mck_y = y[1]
ax.annotate("R-type universities only; 18% master's, 0% baccalaureate",
            (mck_jif, mck_y), xytext=(46, -14), textcoords="offset points",
            va="center", ha="left", fontsize=9, style="italic", color=COLORS["gray_700"])

ax.set_yticks(y)
ax.set_yticklabels([b[0] for b in bars], fontsize=10)
ax.set_xlim(0, 108)
ax.set_xlabel("Institutions whose RPT documents mention the criterion (%)", labelpad=6)
ax.set_title("What researcher-evaluation systems reward", pad=12, fontsize=15)
ax.spines["left"].set_visible(True)

handles = [mpatches.Patch(facecolor=cat_style[c]["color"], edgecolor=COLORS["ink"],
                          hatch=cat_style[c]["hatch"], label=cat_style[c]["label"])
           for c in ("traditional", "open")]
ax.legend(handles=handles, loc="lower right", fontsize=10, framealpha=0.95)

fig.text(0.5, 0.035,
         "Bars span different populations and definitions (see caption). "
         "All values extracted from the source papers' full text.",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_rpt_criteria.png"))
print("saved fig_sec7_rpt_criteria.png:", [b[1] for b in bars])
```

:::

Because stewardship earns no formal credit, non-sharing is the rational default, and the survey evidence bears this out. {cite:t}`Fecher2015` report that nearly half of surveyed scientists do not make their data electronically available and develop a six-category model concluding that data behave not as a shared commons but as a private asset whose release requires positive incentives that do not exist. A meta-synthesis of forty-five studies of researcher attitudes reaches the same conclusion from the qualitative side, tracing withholding directly to absent rewards for appointment and promotion, missing infrastructure, and lack of time and skills, {cite:p}`Perrier2020` and a systematic review consolidates the drivers and inhibitors of data sharing into eleven categories in which formal requirements and facilitating conditions are the decisive levers. {cite:p}`Zuiderwijk2020` Interviews with data-sharing-platform stakeholders show the mechanism concretely: an evaluation system fixated on first and last authorship structurally undervalues the people who generate and curate data, so contributorship crediting is proposed as a corrective. {cite:p}`Devriendt2022` Even mandates do not close the gap, because they raise nominal accessibility without raising quality: an audit of ecology and evolution datasets archived under strong public-archiving policies found most incomplete or unusable for reuse. {cite:p}`Roche2015` The pattern generalises across national systems — in Ecuador, reliance on journal-centric metrics predicted lower adoption of open practices while institutional deposit mandates and data services predicted higher adoption. {cite:p}`Guerra2026`

:::{trust-claim}
:claim-id: clm_d5ab2c0e1cedefcc
:claim: report that nearly half of surveyed scientists do not make their data electronically available and develop a six-category model concluding that data behave not as a shared commons but as a private asset whose release requires positive incentives that do not exist.
:cites: Fecher2015
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_23e7ad87559dd405
:claim: A meta-synthesis of forty-five studies of researcher attitudes reaches the same conclusion from the qualitative side, tracing withholding directly to absent rewards for appointment and promotion, missing infrastructure, and lack of time and skills, and a systematic review consolidates the drivers and inhibitors of data sharing into eleven categories in which formal requirements and facilitating conditions are the decisive levers.
:cites: Perrier2020, Zuiderwijk2020
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_13c8dc85c2e607fd
:claim: Interviews with data-sharing-platform stakeholders show the mechanism concretely: an evaluation system fixated on first and last authorship structurally undervalues the people who generate and curate data, so contributorship crediting is proposed as a corrective.
:cites: Devriendt2022
:claim-type: causal
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_7acdd13b4115701a
:claim: Even mandates do not close the gap, because they raise nominal accessibility without raising quality: an audit of ecology and evolution datasets archived under strong public-archiving policies found most incomplete or unusable for reuse.
:cites: Roche2015
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_e351f540fdbcc374
:claim: The pattern generalises across national systems — in Ecuador, reliance on journal-centric metrics predicted lower adoption of open practices while institutional deposit mandates and data services predicted higher adoption.
:cites: Guerra2026
:claim-type: empirical
:modality: suggestive
:::

The credit system that undervalues data generation is itself a contested instrument. Authorship — the currency in which the reward is denominated — is a poor proxy for contribution: honorary and ghost authorship are common, {cite:p}`Pruschak2022` author lists have inflated to the point that alphabetical middle-author ordering now dominates large teams, {cite:p}`Mongeon2017` and the resulting depreciation of authorship credit falls hardest on the junior and technical contributors who do the data work. {cite:p}`Hosseini2022` Proposed remedies move from authorship toward structured contributorship, in which machine-readable role taxonomies record who curated data and ran code, {cite:p}`Vasilevsky2020, Zhang2019b` though such schemes remain unevenly adopted and are undercut by promotion rules that simply count indexed publications. {cite:p}`Das2020` Alternative allocation mechanisms are being trialled at the funder level — partial randomisation, or funding lotteries, among near-equivalent applications — precisely to blunt the metric competition that credit inflation feeds, {cite:p}`LewisWilson2023, Stafford2024` while responsible-assessment frameworks attempt to translate reform principles into concrete evaluation practice. {cite:p}`Himanen2024, Gagliardi2023` Peer review, the mechanism ostensibly guarding quality, remains poorly understood and inconsistently applied, and so cannot be relied upon to correct what the reward structure encourages. {cite:p}`Tennant2020, DelasCuevas2026`

:::{trust-claim}
:claim-id: clm_f0984ec95d4a8490
:claim: Authorship — the currency in which the reward is denominated — is a poor proxy for contribution: honorary and ghost authorship are common, author lists have inflated to the point that alphabetical middle-author ordering now dominates large teams, and the resulting depreciation of authorship credit falls hardest on the junior and technical contributors who do the data work.
:cites: Pruschak2022, Mongeon2017, Hosseini2022
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_2e0aea7bdf5c5fef
:claim: Proposed remedies move from authorship toward structured contributorship, in which machine-readable role taxonomies record who curated data and ran code, though such schemes remain unevenly adopted and are undercut by promotion rules that simply count indexed publications.
:cites: Vasilevsky2020, Zhang2019b, Das2020
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_a680f6bd534655f5
:claim: Alternative allocation mechanisms are being trialled at the funder level — partial randomisation, or funding lotteries, among near-equivalent applications — precisely to blunt the metric competition that credit inflation feeds, while responsible-assessment frameworks attempt to translate reform principles into concrete evaluation practice.
:cites: LewisWilson2023, Stafford2024, Himanen2024, Gagliardi2023
:claim-type: methodological
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_edc7ab4cef9b986e
:claim: Peer review, the mechanism ostensibly guarding quality, remains poorly understood and inconsistently applied, and so cannot be relied upon to correct what the reward structure encourages.
:cites: Tennant2020, DelasCuevas2026
:claim-type: review_synthesis
:modality: likely
:::

The decisive test of whether incentives reach behaviour is to compare what researchers declare against what they actually deliver. Here the evidence is stark and convergent. After the medical-journal editors' data-sharing-statement requirement, {cite:t}`Danchev2021` found that most trials in the highest-impact journals declared a willingness to share, yet fewer than one percent had deidentified data actually and publicly available. Independent audits reproduce the collapse: raw data were shared for only around one in fifty psychology articles in a manual audit of the transparency literature; {cite:p}`Hardwicke2021` among manuscripts whose availability statements explicitly pledged sharing, the overwhelming majority of authors did not respond or declined and only a small fraction ultimately supplied their datasets; {cite:p}`MartinRodriguez2026` and even after contacting trialists directly, most responded but only a fifth of responders — roughly one in eight of all those approached — shared their data. {cite:p}`Flanagan2026` Statement presence is not sharing either — one in five data-management plans submitted under the new funder policy still omitted required elements, {cite:p}`Hamidi2025` and only a quarter of large pharmaceutical companies fully met a composite data-sharing standard. {cite:p}`Miller2019` This declared-versus-actual gap is the same phenomenon that anchors the review at roughly two percent actual availability, and it recurs in. {ref}`sec-fair-preclinical` {numref}`fig-sec7-declared-vs-actual` makes the incentive-to-behaviour gap unmistakable.

:::{trust-claim}
:claim-id: clm_e3d21c51cbf81151
:claim: After the medical-journal editors' data-sharing-statement requirement, found that most trials in the highest-impact journals declared a willingness to share, yet fewer than one percent had deidentified data actually and publicly available.
:cites: Danchev2021
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_a3f6891cd4a38eb2
:claim: Independent audits reproduce the collapse: raw data were shared for only around one in fifty psychology articles in a manual audit of the transparency literature; among manuscripts whose availability statements explicitly pledged sharing, the overwhelming majority of authors did not respond or declined and only a small fraction ultimately supplied their datasets; and even after contacting trialists directly, most responded but only a fifth of responders — roughly one in eight of all those approached — shared their data.
:cites: Hardwicke2021, MartinRodriguez2026, Flanagan2026
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_9c6a6b42ed378719
:claim: Statement presence is not sharing either — one in five data-management plans submitted under the new funder policy still omitted required elements, and only a quarter of large pharmaceutical companies fully met a composite data-sharing standard.
:cites: Hamidi2025, Miller2019
:claim-type: empirical
:modality: likely
:::

:::{figure} ../figures/fig_sec7_declared_vs_actual.png
:name: fig-sec7-declared-vs-actual
:width: 100%
**Declared intent is not usable data.** Data availability under sharing policies, grouped by construct (statement-presence versus declared versus actual). Label each bar by availability stage: Major2025 = has a data-sharing statement (14%, presence only, not sharing); Danchev2021 = declared available (68.6%) vs actually available (0.6%); Hardwicke2021 = raw data actually shared (2%). Statement-presence and actual-sharing are different constructs. Fields differ (clinical trials, psychology, orthopaedics). The orthopaedic statement-presence point (Major2025, 14%) is omitted from the plot because it lacks a canonical citation key in this review's bibliography, though it is retained in the caveat above. Values from {cite:p}`Danchev2021` and {cite:p}`Hardwicke2021`.
:::

:::{dropdown} 📓 Figure code

```python
import os
import re
import sys
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_07.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_07.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD["declared-vs-actual-open-data"]
papers = {p["doi"]: p for p in comp["papers"]}

# Danchev2021: "68.6 declared / 0.6 actual"
dv = re.findall(r"[\d.]+", papers["10.1001/jamanetworkopen.2020.33972"]["value"])
danchev_declared, danchev_actual = float(dv[0]), float(dv[1])
# Hardwicke2021: raw data actually shared "2"
hardwicke_actual = float(re.findall(r"[\d.]+", papers["10.1177/1745691620979806"]["value"])[0])
# Major2025 (10.2106/JBJS.24.00955): 14% -- no canonical cite key -> dropped from plot
DROPPED = ("10.2106/JBJS.24.00955" in papers)

# (label, value, construct, kind)  kind in {"declared", "actual"}
bars = [
    ("Danchev et al. 2021\nclinical trials", danchev_declared, "Declared", "declared"),
    ("Danchev et al. 2021\nclinical trials", danchev_actual, "Actually\navailable", "actual"),
    ("Hardwicke et al. 2021\npsychology", hardwicke_actual, "Actually\navailable", "actual"),
]

kind_style = {
    "declared": dict(color=COLORS["declared_nominal"], hatch="////", label="Declared / stated intent"),
    "actual":   dict(color=COLORS["actual_verified"], hatch="",     label="Actually available / usable"),
}

fig, ax = plt.subplots(figsize=(10.5, 6.0))
fig.subplots_adjust(left=0.10, right=0.965, bottom=0.22, top=0.88)

x = np.arange(len(bars))
for xi, (label, val, construct, kind) in zip(x, bars):
    st = kind_style[kind]
    ax.bar(xi, val, width=0.62, color=st["color"], edgecolor=COLORS["ink"],
           linewidth=0.7, hatch=st["hatch"], zorder=3)
    ax.annotate(f"{val:g}%", (xi, val), xytext=(0, 5), textcoords="offset points",
                va="bottom", ha="center", fontsize=12, fontweight="bold", color=COLORS["ink"])

# Emphasise the declared -> actual collapse for Danchev
ax.annotate("", xy=(1, danchev_actual + 4), xytext=(0, danchev_declared - 2),
            arrowprops=dict(arrowstyle="->", color=COLORS["debt"], lw=1.8,
                            connectionstyle="arc3,rad=-0.25"), zorder=4)
ax.text(0.5, danchev_declared * 0.62,
        "declared 68.6%\n-> 0.6% actual", ha="center", va="center",
        fontsize=9.5, color=COLORS["debt"], fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([b[0] for b in bars], fontsize=9.5)
# construct labels as a secondary annotation row
for xi, (_, _, construct, _) in zip(x, bars):
    ax.annotate(construct, (xi, -0.5), xytext=(0, -34), textcoords="offset points",
                ha="center", va="top", fontsize=9, color=COLORS["gray_700"],
                annotation_clip=False)
ax.set_ylim(0, 78)
ax.set_ylabel("Data availability (% of articles)", labelpad=6)
ax.set_title("Declared intent is not usable data", pad=12, fontsize=15)

handles = [mpatches.Patch(facecolor=kind_style[k]["color"], edgecolor=COLORS["ink"],
                          hatch=kind_style[k]["hatch"], label=kind_style[k]["label"])
           for k in ("declared", "actual")]
ax.legend(handles=handles, loc="upper right", fontsize=10, framealpha=0.95)

note = ("Statement-presence construct omitted: Major2025 (orthopaedics, 14%) "
        "has no canonical citation key and is not plotted." if DROPPED else "")
fig.text(0.5, 0.045, note + "  Constructs differ across fields (see caption).",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_declared_vs_actual.png"))
print("saved fig_sec7_declared_vs_actual.png:", danchev_declared, danchev_actual, hardwicke_actual, "dropped:", DROPPED)
```

:::

The animal-welfare stake makes this gap more than an administrative curiosity. A transparency audit of studies using animal models of opioid addiction found near-total absence of open-science practices: none preregistered, none sharing analytical code, raw data accessible for only about three percent, and the great majority lacking any sample-size justification. {cite:p}`Blackwell2025` Every one of those unusable datasets carries an unrecovered welfare cost, and a cardiovascular-literature audit finding fewer than two percent of papers fully reproducible adds a further specialty to the same pattern already documented across psychology, clinical medicine, and ecology. {cite:p}`Heckerman2025` Reusing existing data — the Reduction dividend argued throughout this review — is impossible when the data are, in practice, gone.

:::{trust-claim}
:claim-id: clm_34ffa80b7b2e04b5
:claim: A transparency audit of studies using animal models of opioid addiction found near-total absence of open-science practices: none preregistered, none sharing analytical code, raw data accessible for only about three percent, and the great majority lacking any sample-size justification.
:cites: Blackwell2025
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_98814e8e98d7da22
:claim: Every one of those unusable datasets carries an unrecovered welfare cost, and a cardiovascular-literature audit finding fewer than two percent of papers fully reproducible adds a further specialty to the same pattern already documented across psychology, clinical medicine, and ecology.
:cites: Heckerman2025
:claim-type: empirical
:modality: established
:::

The aggregate cost of these behaviours is the research waste that the incentive system continuously manufactures. The programme on increasing value and reducing waste located waste at every stage from question selection to inaccessible reporting, arguing that trial and review output already outpaces any capacity to synthesise it and that full information is available for only about half of all studies. {cite:p}`Chan2014, Salman2014, Bastian2010` Redundant, misleading, or conflicted syntheses are mass-produced far faster than the primary research they digest, {cite:p}`IOANNIDIS2016` undetected software and computation errors propagate silently into published results, {cite:p}`Soergel2015` and a bibliometric mapping of the waste literature itself reveals a large and fast-growing field of concern. {cite:p}`Peng2025` The most frequently repeated single figure — that more than half of preclinical research is irreproducible, at a cost of tens of billions of dollars a year in the United States alone — is influential but rests on a modelled economic estimate whose provenance is not fully transparent, and it is best read as an order-of-magnitude claim rather than a measurement. {cite:p}`Freedman2015` What is not in doubt is the direction: every irreproducible or unreusable animal study converts a welfare cost into waste, which is why stewardship reform is a Reduction intervention and not merely good data hygiene.

:::{trust-claim}
:claim-id: clm_d51eafef2cf20797
:claim: The programme on increasing value and reducing waste located waste at every stage from question selection to inaccessible reporting, arguing that trial and review output already outpaces any capacity to synthesise it and that full information is available for only about half of all studies.
:cites: Chan2014, Salman2014, Bastian2010
:claim-type: review_synthesis
:modality: established
:::

:::{trust-claim}
:claim-id: clm_c1292134bfc1f42e
:claim: Redundant, misleading, or conflicted syntheses are mass-produced far faster than the primary research they digest, undetected software and computation errors propagate silently into published results, and a bibliometric mapping of the waste literature itself reveals a large and fast-growing field of concern.
:cites: IOANNIDIS2016, Soergel2015, Peng2025
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_340b82705318d705
:claim: The most frequently repeated single figure — that more than half of preclinical research is irreproducible, at a cost of tens of billions of dollars a year in the United States alone — is influential but rests on a modelled economic estimate whose provenance is not fully transparent, and it is best read as an order-of-magnitude claim rather than a measurement.
:cites: Freedman2015
:claim-type: limitation
:modality: suggestive
:::

If non-stewardship is one rational response to the incentive gradient, questionable research practices are another, and they too are common. The behavioural substrate spans a wide range of severity, and definition drives the headline number. The first meta-analysis of misconduct surveys estimated that around two percent of scientists admit fabricating or falsifying data at least once, with up to a third admitting other questionable practices; {cite:p}`Fanelli2009` a five-country study found that almost all researchers admit using at least one such practice, though measured frequency of any specific practice is far lower; {cite:p}`Schneider2024` and an implicit-association study found that about a fifth of scientists tacitly associate questionable practices with career success while very few connect outright fabrication to success. {cite:p}`Velicu2025` Surveys across Portuguese universities, Amsterdam, and international samples add that admission rises among younger and more prolific researchers and tracks contract type, career stage, and perceived research climate, {cite:p}`Entradas2026, Haven2021, Brooker2024` and a principled taxonomy notes that the most-reported practices are omissions — selective reporting of analyses, citations, and covariates — some of which may under narrow conditions be neutral or even useful. {cite:p}`Fanelli2026` {numref}`fig-sec7-qrp-prevalence` deliberately separates behaviour from attitude to prevent the false comparison the raw numbers invite.

:::{trust-claim}
:claim-id: clm_cab3ea7f5f231c1e
:claim: The first meta-analysis of misconduct surveys estimated that around two percent of scientists admit fabricating or falsifying data at least once, with up to a third admitting other questionable practices; a five-country study found that almost all researchers admit using at least one such practice, though measured frequency of any specific practice is far lower; and an implicit-association study found that about a fifth of scientists tacitly associate questionable practices with career success while very few connect outright fabrication to success.
:cites: Fanelli2009, Schneider2024, Velicu2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_fced19a702a030f9
:claim: Surveys across Portuguese universities, Amsterdam, and international samples add that admission rises among younger and more prolific researchers and tracks contract type, career stage, and perceived research climate, and a principled taxonomy notes that the most-reported practices are omissions — selective reporting of analyses, citations, and covariates — some of which may under narrow conditions be neutral or even useful.
:cites: Entradas2026, Haven2021, Brooker2024, Fanelli2026
:claim-type: empirical
:modality: likely
:::

:::{figure} ../figures/fig_sec7_qrp_prevalence.png
:name: fig-sec7-qrp-prevalence
:width: 100%
**Questionable-practice prevalence depends on what is counted.** Behaviour-prevalence estimates (left) are kept separate from an attitudinal measure (right). Not a like-for-like prevalence: 1.97% = self-admitted serious FFP (Fanelli); 94% = any-of-nine-QRP self-admission (Schneider); ~20% = implicit attitudinal association of QRPs with success on an SC-IAT (Velicu), not a self-reported behavior. The 2-to-94 spread is a severity/breadth artifact. The left panel also marks Fanelli's own ~34% any-QRP admission, the closer like-for-like comparator to Schneider's 94%. Values from,, {cite:p}`Fanelli2009` {cite:p}`Schneider2024` and {cite:p}`Velicu2025`.
:::

:::{dropdown} 📓 Figure code

```python
import os
import re
import sys
import json

import numpy as np
import matplotlib.pyplot as plt


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_07.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_07.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIND = {f["cite_key"]: f for f in EV["findings"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD["qrp-prevalence-surveys"]
papers = {p["doi"]: p for p in comp["papers"]}

fanelli_ffp = float(re.findall(r"[\d.]+", papers["10.1371/journal.pone.0005738"]["value"])[0])  # 1.97
schneider_any = float(re.findall(r"[\d.]+", papers["10.1371/journal.pone.0304342"]["value"])[0])  # 94
velicu_attitude = float(re.findall(r"[\d.]+", papers["10.1007/s11192-025-05357-4"]["value"])[0])  # ~20
# Fanelli's own ~34% any-QRP (closer comparator to Schneider): from the Fanelli2009 finding text
fanelli_anyqrp = float(re.search(r"~?(\d+)%\s*admit other QRPs", FIND["Fanelli2009"]["evidence"]).group(1))  # 34

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 5.8),
                               gridspec_kw={"width_ratios": [2.2, 1.0], "wspace": 0.32})
fig.subplots_adjust(left=0.09, right=0.975, bottom=0.20, top=0.84)

# --- Left panel: behaviour prevalence (self-admitted) ---
bx = [0, 1]
bvals = [fanelli_ffp, schneider_any]
bcolors = [COLORS["debt"], COLORS["conflict"]]
bhatch = ["", "xxxx"]
blabels = ["Fanelli 2009\nserious FFP\n(fabrication/\nfalsification)", "Schneider et al. 2024\nany of nine QRPs\n(used at least once)"]
for xi, val, col, h in zip(bx, bvals, bcolors, bhatch):
    axL.bar(xi, val, width=0.6, color=col, edgecolor=COLORS["ink"], linewidth=0.7, hatch=h, zorder=3)
    axL.annotate(f"{val:g}%", (xi, val), xytext=(0, 5), textcoords="offset points",
                 ha="center", va="bottom", fontsize=13, fontweight="bold", color=COLORS["ink"])
# Fanelli's own ~34% any-QRP as the closer comparator to Schneider
axL.axhline(fanelli_anyqrp, color=COLORS["gray_700"], lw=1.4, ls="--", zorder=2)
axL.text(-0.55, fanelli_anyqrp + 2.5,
         f"Fanelli 2009 any-QRP ~{fanelli_anyqrp:g}%\n(closer comparator to Schneider)",
         ha="left", va="bottom", fontsize=9, style="italic", color=COLORS["gray_700"])
axL.set_xticks(bx)
axL.set_xticklabels(blabels, fontsize=10)
axL.set_xlim(-0.6, 1.6)
axL.set_ylim(0, 104)
axL.set_ylabel("Scientists self-admitting (%)", labelpad=6)
axL.set_title("Behaviour prevalence (self-admitted)", pad=10, fontsize=13)

# --- Right panel: attitudinal (implicit association) ---
axR.bar(0, velicu_attitude, width=0.55, color=COLORS["secondary_cat"],
        edgecolor=COLORS["ink"], linewidth=0.7, hatch="....", zorder=3)
axR.annotate(f"~{velicu_attitude:g}%", (0, velicu_attitude), xytext=(0, 5),
             textcoords="offset points", ha="center", va="bottom",
             fontsize=13, fontweight="bold", color=COLORS["ink"])
axR.set_xticks([0])
axR.set_xticklabels(["Velicu et al. 2025\nimplicitly associate\nQRPs with success (SC-IAT)"], fontsize=10)
axR.set_xlim(-0.7, 0.7)
axR.set_ylim(0, 104)
axR.set_ylabel("Scientists (implicit association, %)", labelpad=6)
axR.set_title("Attitude (implicit association)", pad=10, fontsize=13)

fig.suptitle("Questionable-practice prevalence depends on what is counted", fontsize=15, y=0.97)
fig.text(0.5, 0.035,
         "Not a like-for-like comparison: severity (serious FFP) vs breadth (any QRP) vs an implicit "
         "attitude, not a behaviour. The 2-to-94 spread is a severity/breadth artefact.",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_qrp_prevalence.png"))
print("saved fig_sec7_qrp_prevalence.png:", fanelli_ffp, schneider_any, velicu_attitude, "any-QRP", fanelli_anyqrp)
```

:::

:::{admonition} Evidence Conflict
:class: warning
Whether questionable practices amount to a prevailing norm depends on how prevalence is measured. An incentivised psychology survey concluded that some practices are so widely admitted that they may constitute the prevailing research norm, {cite:p}`John2012` whereas the larger cross-national study argued that widespread one-time involvement does not amount to systematic use once the frequency of any given practice is measured. {cite:p}`Schneider2024` The disagreement is largely resolved by method — "used at least once" and "used routinely" are different quantities — but it is a standing warning against reading any single questionable-practice percentage as a behavioural rate.

:::

:::{trust-claim}
:claim-id: clm_671d5d4b89026361
:claim: An incentivised psychology survey concluded that some practices are so widely admitted that they may constitute the prevailing research norm, whereas the larger cross-national study argued that widespread one-time involvement does not amount to systematic use once the frequency of any given practice is measured.
:cites: John2012, Schneider2024
:claim-type: comparative
:modality: contested
:::

These practices propagate into the published record through selective reporting, analytic flexibility, and spin, all of which are rewarded because positive, clean, novel results publish more easily. Simulations show that even a single flexible-analysis strategy can lift the false-positive rate from five percent to at least thirty, {cite:p}`Stefan2023` drawing on a catalogue of thirty-four researcher degrees of freedom available in designing, running, and reporting a study. {cite:p}`Wicherts2016` When seventy-three independent teams analysed the same data to test the same hypothesis, their numerical results diverged so widely that most of the variance remained unexplained even after every analytic decision had been coded — a direct demonstration of how much latitude a reward for clean results can exploit. {cite:p}`Breznau2022` Text-mining confirms that such flexibility is common across disciplines, {cite:p}`Head2015` and modelling shows how, when negative results publish at a small fraction of the rate of positive ones, false claims can be canonised as fact, {cite:p}`Nissen2016` though a competing model argues that publishing potentially non-replicable studies and replicating selectively can be efficient for the community as a whole. {cite:p}`Lewandowsky2020` The clinical literature supplies the most concrete measurements: spin — reporting that misrepresents nonsignificant results as favourable — appears in roughly half to three-quarters of nonsignificant randomised-trial reports across general medicine, urology, bariatric, vascular, and emergency-medicine specialties, with industry funding raising the odds. {cite:p}`Boutron2010, Wu2023, Rassy2021, Nguyen2022, ReynoldsVaughn2020` Prospective audits find outcome-switching pervasive and its disclosure rare, {cite:p}`Goldacre2019b, Kapp2022` undeclared switching survives even direct correction letters, {cite:p}`Goldacre2019a` and a striking worked example shows an entire therapeutic conclusion evaporating once analysis is restricted to pre-registered primary outcomes. {cite:p}`Prior2017` Selective reporting further compromises the syntheses built on top of trials. {cite:p}`Heneghan2017, Littell2026, DumasMallet2021`

:::{trust-claim}
:claim-id: clm_aab87f9df3c38692
:claim: Simulations show that even a single flexible-analysis strategy can lift the false-positive rate from five percent to at least thirty, drawing on a catalogue of thirty-four researcher degrees of freedom available in designing, running, and reporting a study.
:cites: Stefan2023, Wicherts2016
:claim-type: methodological
:modality: established
:::

:::{trust-claim}
:claim-id: clm_17156774c21e167f
:claim: When seventy-three independent teams analysed the same data to test the same hypothesis, their numerical results diverged so widely that most of the variance remained unexplained even after every analytic decision had been coded — a direct demonstration of how much latitude a reward for clean results can exploit.
:cites: Breznau2022
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_9e257f167d918601
:claim: Text-mining confirms that such flexibility is common across disciplines, and modelling shows how, when negative results publish at a small fraction of the rate of positive ones, false claims can be canonised as fact, though a competing model argues that publishing potentially non-replicable studies and replicating selectively can be efficient for the community as a whole.
:cites: Head2015, Nissen2016, Lewandowsky2020
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_d35f1d8d894cc20e
:claim: The clinical literature supplies the most concrete measurements: spin — reporting that misrepresents nonsignificant results as favourable — appears in roughly half to three-quarters of nonsignificant randomised-trial reports across general medicine, urology, bariatric, vascular, and emergency-medicine specialties, with industry funding raising the odds.
:cites: Boutron2010, Wu2023, Rassy2021, Nguyen2022, ReynoldsVaughn2020
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_d97d55c061252a0b
:claim: Prospective audits find outcome-switching pervasive and its disclosure rare, undeclared switching survives even direct correction letters, and a striking worked example shows an entire therapeutic conclusion evaporating once analysis is restricted to pre-registered primary outcomes.
:cites: Goldacre2019b, Kapp2022, Goldacre2019a, Prior2017
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_f3136fa34a2537f1
:claim: Selective reporting further compromises the syntheses built on top of trials.
:cites: Heneghan2017, Littell2026, DumasMallet2021
:claim-type: review_synthesis
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
The field disagrees about how much analytic flexibility actually distorts the record. Text-mining across disciplines concluded that p-hacking, though common, only weakly perturbs meta-analytic consensus relative to the real effects being measured, {cite:p}`Head2015` whereas the theoretical framework that most published research findings are false holds that bias and flexibility make it more likely than not that a given claim is untrue. {cite:p}`Ioannidis2005b` The gap turns on the outcome measured — aggregate consensus versus individual claim reliability — and it remains open, cautioning against treating either "the literature is mostly fine" or "most findings are false" as settled.

:::

:::{trust-claim}
:claim-id: clm_29526c0ca0ee6943
:claim: Text-mining across disciplines concluded that p-hacking, though common, only weakly perturbs meta-analytic consensus relative to the real effects being measured, whereas the theoretical framework that most published research findings are false holds that bias and flexibility make it more likely than not that a given claim is untrue.
:cites: Head2015, Ioannidis2005b
:claim-type: comparative
:modality: contested
:::

The structural interpretation is sharpened by evidence that these behaviours are not being competed away. Statistical power in the behavioural sciences has not detectably improved across more than fifty years of admonition, which {cite:t}`Smaldino2016` model as natural selection: while publication drives careers, methods that generate more publishable results out-reproduce careful ones, and replication slows but does not halt the deterioration. Independent measurement agrees — median power in cognitive neuroscience and psychology has stagnated at low levels and correlates negatively with journal impact factor {cite:p}`Szucs2017` — and only a small fraction of decades of randomised trials used adequate methods, with inadequate methods rising over time. {cite:p}`Catillon2019` That researchers in more academically productive environments produce more hypothesis-confirming results is consistent with competition inflating bias, {cite:p}`Fanelli2010` and using journal rank as an assessment tool tracks unreliability and retraction rather than quality. {cite:p}`Brembs2013` The link between competitive pressure and bias is nonetheless contested: although more productive environments produced more confirmatory results, {cite:p}`Fanelli2010` a later cross-disciplinary meta-assessment found high-output, highly cited authors were not overall at greater risk of bias, locating inflation instead in small, early-career, and misconduct-prone work. {cite:p}`Fanelli2017` Optimistic syntheses describe a credibility revolution already delivering more negative results and higher-quality registered reports, {cite:p}`Korbmacher2023` yet the stagnation of statistical power over the same half-century warns against mistaking activity for improvement. {cite:p}`Szucs2017` A minority position holds the crisis narrative is itself overstated and that a story of methodological empowerment fits the trends better, {cite:p}`Fanelli2018` though the stagnation-of-power evidence cuts against it and the tension remains open. The lived experience of the incentive gradient is documented directly: publication pressure, precarity, overwork, and burnout are pervasive among early-career and mid-career researchers and are perceived to reward speed and quantity over integrity. {cite:p}`Armond2022, Marck2024, Srensen2026`

:::{trust-claim}
:claim-id: clm_b3895a3c7e3f0181
:claim: Statistical power in the behavioural sciences has not detectably improved across more than fifty years of admonition, which model as natural selection: while publication drives careers, methods that generate more publishable results out-reproduce careful ones, and replication slows but does not halt the deterioration.
:cites: Smaldino2016
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_ae969bbd55c8b4c7
:claim: Independent measurement agrees — median power in cognitive neuroscience and psychology has stagnated at low levels and correlates negatively with journal impact factor — and only a small fraction of decades of randomised trials used adequate methods, with inadequate methods rising over time.
:cites: Szucs2017, Catillon2019
:claim-type: empirical
:modality: established
:::

:::{trust-claim}
:claim-id: clm_622875a949a7953f
:claim: That researchers in more academically productive environments produce more hypothesis-confirming results is consistent with competition inflating bias, and using journal rank as an assessment tool tracks unreliability and retraction rather than quality.
:cites: Fanelli2010, Brembs2013
:claim-type: causal
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_17967e1296ffbee0
:claim: The link between competitive pressure and bias is nonetheless contested: although more productive environments produced more confirmatory results, a later cross-disciplinary meta-assessment found high-output, highly cited authors were not overall at greater risk of bias, locating inflation instead in small, early-career, and misconduct-prone work.
:cites: Fanelli2010, Fanelli2017
:claim-type: comparative
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_11e7c50e6784601f
:claim: Optimistic syntheses describe a credibility revolution already delivering more negative results and higher-quality registered reports, yet the stagnation of statistical power over the same half-century warns against mistaking activity for improvement.
:cites: Korbmacher2023, Szucs2017
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_e842bf372c2bfc9b
:claim: A minority position holds the crisis narrative is itself overstated and that a story of methodological empowerment fits the trends better, though the stagnation-of-power evidence cuts against it and the tension remains open.
:cites: Fanelli2018
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_2970184590a6706e
:claim: The lived experience of the incentive gradient is documented directly: publication pressure, precarity, overwork, and burnout are pervasive among early-career and mid-career researchers and are perceived to reward speed and quantity over integrity.
:cites: Armond2022, Marck2024, Srensen2026
:claim-type: empirical
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
Whether the debt can be repaid without changing incentives is the central dispute of this section. The manifesto for reproducible science argues that measures targeting methods, reporting, reproducibility, evaluation, and incentives — supported by simulation and early empirical evidence — can make research more reliable given iterative adoption by researchers, institutions, funders, and journals. {cite:p}`Munafo2017` The natural-selection model counters that as long as publication drives careers, the incentive system will keep selecting for bad methods, and researcher-level fixes, even replication, are insufficient without institutional change. {cite:p}`Smaldino2016` This determines whether the stewardship reforms of later sections are treatments or palliatives; it is unresolved, and the balance of stagnation evidence weighs toward the structural view.

:::

:::{trust-claim}
:claim-id: clm_cd0844a346f002ad
:claim: The manifesto for reproducible science argues that measures targeting methods, reporting, reproducibility, evaluation, and incentives — supported by simulation and early empirical evidence — can make research more reliable given iterative adoption by researchers, institutions, funders, and journals.
:cites: Munafo2017
:claim-type: review_synthesis
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_9cf7124b6cd34e2a
:claim: The natural-selection model counters that as long as publication drives careers, the incentive system will keep selecting for bad methods, and researcher-level fixes, even replication, are insufficient without institutional change.
:cites: Smaldino2016
:claim-type: causal
:modality: likely
:::

At the extreme of the same gradient lies fraud at industrial scale, where the incentive to produce publications is met by a market that manufactures them. An earlier systematic screen of more than twenty thousand articles had reported several percent as containing inappropriately duplicated images — a prior baseline that {cite:t}`Richardson2025` invoke when they show the broker entities enabling fraud are large, resilient, and growing faster than legitimate science. Detection-based estimates now run well above self-report: a forensic red-flagging method estimates several percent of the biomedical literature to be outright fakes, {cite:p}`Sabel2025a` a machine-learning classifier flagged nearly a tenth of millions of cancer papers as potential paper-mill products, {cite:p}`Scancar2026` and formulaic single-factor papers exploiting open health databases have exploded from a handful per year to hundreds. {cite:p}`Suchak2025` Reviews trace this flood squarely to academic pressure and monetary publication incentives, {cite:p}`Wittau2024, Kocyigit2025` and the same reward logic drives authorship inflation, gift and honorary authorship, salami-slicing, and citation gaming. {cite:p}`Marcelino2026, Ioannidis2023a, Pruschak2022, Ding2019`

:::{trust-claim}
:claim-id: clm_dc42537bda32ca0d
:claim: An earlier systematic screen of more than twenty thousand articles had reported several percent as containing inappropriately duplicated images — a prior baseline that invoke when they show the broker entities enabling fraud are large, resilient, and growing faster than legitimate science.
:cites: Richardson2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_eca955c4d877de75
:claim: Detection-based estimates now run well above self-report: a forensic red-flagging method estimates several percent of the biomedical literature to be outright fakes, a machine-learning classifier flagged nearly a tenth of millions of cancer papers as potential paper-mill products, and formulaic single-factor papers exploiting open health databases have exploded from a handful per year to hundreds.
:cites: Sabel2025a, Scancar2026, Suchak2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_7f075e51e79cd814
:claim: Reviews trace this flood squarely to academic pressure and monetary publication incentives, and the same reward logic drives authorship inflation, gift and honorary authorship, salami-slicing, and citation gaming.
:cites: Wittau2024, Kocyigit2025, Marcelino2026, Ioannidis2023a, Pruschak2022, Ding2019
:claim-type: review_synthesis
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
Estimates of fabrication diverge by an order of magnitude according to method. Anonymous self-report surveys pool to around two percent of scientists admitting fabrication, {cite:p}`Fanelli2009` whereas forensic detection of the biomedical literature estimates several percent of papers to be actual fakes {cite:p}`Sabel2025a` and machine screening flags close to a tenth of cancer papers. {cite:p}`Scancar2026` Self-report and detection count different things — admitting scientists versus fraudulent papers — but the divergence implies self-report substantially understates the scale, a caution that applies to every incentive-driven behaviour measured by asking people to confess it.

:::

:::{trust-claim}
:claim-id: clm_66a16ed4774b2f40
:claim: Anonymous self-report surveys pool to around two percent of scientists admitting fabrication, whereas forensic detection of the biomedical literature estimates several percent of papers to be actual fakes and machine screening flags close to a tenth of cancer papers.
:cites: Fanelli2009, Sabel2025a, Scancar2026
:claim-type: comparative
:modality: likely
:::

Against this structural pessimism stands a genuine counter-argument that must be taken seriously: incentives are already shifting. The Declaration on Research Assessment and allied reforms press institutions away from journal metrics; registered reports raise the publication of null findings and are perceived as higher quality; {cite:p}`Nosek2018, Allen2019` the multi-site replication projects and standing laboratory networks that first exposed the crisis have themselves become durable reform infrastructure; {cite:p}`OpenScienceCollaboration2015, Nosek2022, Neves2020` open-practice badges lifted reported open data at one journal from near-baseline to nearly forty percent; {cite:p}`Kidwell2016, Giofre2017` transparency ratings offer an alternative to the impact factor; {cite:p}`MayoWilson2021` minimum-reporting frameworks operationalise transparency at the article level; {cite:p}`Macleod2021` and integrity-based assessment principles propose rewarding the behaviours that strengthen science. {cite:p}`Moher2018, Moher2020` Open practices are moreover associated with tangible career returns — more citations, attention, and opportunities {cite:p}`McKiernan2016` — a citation advantage that is real but inconsistent across studies for open access, {cite:p}`Klebel2025` clearer in single-field analyses, {cite:p}`Friederichs2026, Migliorini2026` and more robust — roughly nine percent more citations — for open data, {cite:p}`Klebel2025` while a compulsory open-data mandate causally raised a journal's citations. {cite:p}`Zhang2021` Narrative curricula vitae and article-level metrics are being piloted to make stewardship visible in evaluation, {cite:p}`AubertBonn2025, Albert2025, Malicki2026, Arabi2025` field-normalised article-level indicators and national responsible-evaluation systems offer further templates, {cite:p}`Hutchins2016, MillonesGomez2026` and consensus reform agendas, funder integrity plans, and training programmes have proliferated worldwide. {cite:p}`AubertBonn2022, Horbach2022, Westmore2023, Kebenei2026`

:::{trust-claim}
:claim-id: clm_23fc636e1dd7a23c
:claim: The Declaration on Research Assessment and allied reforms press institutions away from journal metrics; registered reports raise the publication of null findings and are perceived as higher quality; the multi-site replication projects and standing laboratory networks that first exposed the crisis have themselves become durable reform infrastructure; open-practice badges lifted reported open data at one journal from near-baseline to nearly forty percent; transparency ratings offer an alternative to the impact factor; minimum-reporting frameworks operationalise transparency at the article level; and integrity-based assessment principles propose rewarding the behaviours that strengthen science.
:cites: Nosek2018, Allen2019, OpenScienceCollaboration2015, Nosek2022, Neves2020, Kidwell2016, Giofre2017, MayoWilson2021, Macleod2021, Moher2018, Moher2020
:claim-type: review_synthesis
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_4b335dbddef594b7
:claim: Open practices are moreover associated with tangible career returns — more citations, attention, and opportunities — a citation advantage that is real but inconsistent across studies for open access, clearer in single-field analyses, and more robust — roughly nine percent more citations — for open data, while a compulsory open-data mandate causally raised a journal's citations.
:cites: McKiernan2016, Klebel2025, Friederichs2026, Migliorini2026, Zhang2021
:claim-type: comparative
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_ea1feffb0a6c3c0d
:claim: Narrative curricula vitae and article-level metrics are being piloted to make stewardship visible in evaluation, field-normalised article-level indicators and national responsible-evaluation systems offer further templates, and consensus reform agendas, funder integrity plans, and training programmes have proliferated worldwide.
:cites: AubertBonn2025, Albert2025, Malicki2026, Arabi2025, Hutchins2016, MillonesGomez2026, AubertBonn2022, Horbach2022, Westmore2023, Kebenei2026
:claim-type: review_synthesis
:modality: likely
:::

The rebuttal is that these instruments have so far moved metrics far more reliably than behaviour. The declared-versus-actual gap is itself the primary evidence: a policy requirement to state a data-sharing intention produced almost no usable public data, {cite:p}`Danchev2021` and the same attitude-behaviour gap recurs among the gatekeepers, where most journal editors endorse transparency guidelines yet do not prioritise or intend to implement them. {cite:p}`Naaman2023, Toomey2025` Uptake studies find open practices spreading only modestly and largely independent of local institutional support, {cite:p}`Brohmer2025` and a pre-post evaluation captured the pattern exactly — engagement with open-science tooling rose sharply while concrete outputs such as preregistrations, protocols, and shared datasets remained essentially absent both before and after. {cite:p}`Cenci2025` Cross-national surveys find awareness of the reproducibility problem near-universal even where successful replication remains rare, {cite:p}`Chakravorti2025` coordinated replication efforts in fields beyond psychology continue to report low success rates, {cite:p}`Murphy2025a` and where open practices are becoming normative it is so far within isolated subfields rather than across the system. {cite:p}`Eben2026` Most damningly, a scoping review found that of more than a hundred studies of reproducibility interventions, only a handful measured reproducibility itself; the rest measured proxies presumed to help, {cite:p}`Dudda2025` and a matched comparison found preregistered studies no less likely to report positive results than their non-preregistered counterparts, even as they improved power. {cite:p}`vandenAkker2023` When a signalling device becomes a reward in its own right, it can be gamed or hollowed out — the recurring worry that badges and mandates strip preregistration of its methodological function rather than delivering it. {cite:p}`Vize2024, Bertin2025` Empirically, even structured preregistration reduces but does not eliminate researcher degrees of freedom, and independent coders often cannot agree on how many hypotheses a preregistration even states. {cite:p}`Bakker2020`

:::{trust-claim}
:claim-id: clm_d272fa77ba6d556a
:claim: The declared-versus-actual gap is itself the primary evidence: a policy requirement to state a data-sharing intention produced almost no usable public data, and the same attitude-behaviour gap recurs among the gatekeepers, where most journal editors endorse transparency guidelines yet do not prioritise or intend to implement them.
:cites: Danchev2021, Naaman2023, Toomey2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_8d1382cd82a7deac
:claim: Uptake studies find open practices spreading only modestly and largely independent of local institutional support, and a pre-post evaluation captured the pattern exactly — engagement with open-science tooling rose sharply while concrete outputs such as preregistrations, protocols, and shared datasets remained essentially absent both before and after.
:cites: Brohmer2025, Cenci2025
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_c04b93392473716a
:claim: Cross-national surveys find awareness of the reproducibility problem near-universal even where successful replication remains rare, coordinated replication efforts in fields beyond psychology continue to report low success rates, and where open practices are becoming normative it is so far within isolated subfields rather than across the system.
:cites: Chakravorti2025, Murphy2025a, Eben2026
:claim-type: empirical
:modality: likely
:::

:::{trust-claim}
:claim-id: clm_d939fd709ae661f2
:claim: Most damningly, a scoping review found that of more than a hundred studies of reproducibility interventions, only a handful measured reproducibility itself; the rest measured proxies presumed to help, and a matched comparison found preregistered studies no less likely to report positive results than their non-preregistered counterparts, even as they improved power.
:cites: Dudda2025, vandenAkker2023
:claim-type: empirical
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_935a67126ad91e99
:claim: When a signalling device becomes a reward in its own right, it can be gamed or hollowed out — the recurring worry that badges and mandates strip preregistration of its methodological function rather than delivering it.
:cites: Vize2024, Bertin2025
:claim-type: review_synthesis
:modality: suggestive
:::

:::{trust-claim}
:claim-id: clm_23c24e4295241af1
:claim: Empirically, even structured preregistration reduces but does not eliminate researcher degrees of freedom, and independent coders often cannot agree on how many hypotheses a preregistration even states.
:cites: Bakker2020
:claim-type: empirical
:modality: likely
:::

:::{admonition} Evidence Conflict
:class: warning
Voluntary signalling and enforced mandates deliver usable data unequally. Open-practice badges not only raised reported open data but made the reported data more likely to be actually available, correct, and complete, {cite:p}`Kidwell2016` whereas audits of datasets archived under blanket mandates found most incomplete or unusable, {cite:p}`Roche2015` and a blanket journal data-sharing requirement produced near-zero actual public data. {cite:p}`Danchev2021` The partial resolution is that verification, not the requirement alone, is what converts a policy into usable data — a design lesson that a mandate without checking is close to no mandate at all.

:::

:::{trust-claim}
:claim-id: clm_83b609f44f43f93b
:claim: Open-practice badges not only raised reported open data but made the reported data more likely to be actually available, correct, and complete, whereas audits of datasets archived under blanket mandates found most incomplete or unusable, and a blanket journal data-sharing requirement produced near-zero actual public data.
:cites: Kidwell2016, Roche2015, Danchev2021
:claim-type: comparative
:modality: likely
:::

That verification is the operative variable points toward the governance question, but it first exposes a dilemma about metrics themselves that the reform literature has not resolved.

:::{admonition} Evidence Conflict
:class: warning
The field is split on whether quantitative evaluation can be reformed or must be resisted. One position holds that quantitative metrics, if made rigorous, field-adjusted, and centralised, could improve research practices and would recognise more researchers than journal-level judgement does. {cite:p}`Ioannidis2023b` The opposing view argues that ranking instruments — global university rankings among them — are inherently incompatible with socially responsible practice and should be abandoned rather than repaired. {cite:p}`Gadd2021` The dispute is unresolved and governs every metric-based reform: whether the answer to a gamed metric is a better metric or no metric at all.

:::

:::{trust-claim}
:claim-id: clm_277a2e6b0146ff18
:claim: One position holds that quantitative metrics, if made rigorous, field-adjusted, and centralised, could improve research practices and would recognise more researchers than journal-level judgement does.
:cites: Ioannidis2023b
:claim-type: review_synthesis
:modality: contested
:::

:::{trust-claim}
:claim-id: clm_7e8d223ccabb1493
:claim: The opposing view argues that ranking instruments — global university rankings among them — are inherently incompatible with socially responsible practice and should be abandoned rather than repaired.
:cites: Gadd2021
:claim-type: review_synthesis
:modality: contested
:::

Taken together, the evidence supports a single conclusion. The persistence of the data-welfare debt across FAIR data, virtual control groups, and non-animal methodologies is not a technical accident but the predictable output of an incentive system that rewards publication counts and journal impact while pricing stewardship at near-zero, under which questionable practices, selective reporting, and — at the margin — fraud are rational, and under which declared openness vastly exceeds usable reality. Reform proposals are real and multiplying, and their diagnosis is now broadly shared, from proposals to restructure publication incentives {cite:p}`Nosek2012, Trueblood2025` to the systemic overhaul urged decades ago {cite:p}`Alberts2014` and the recent declarations reframing metric-gaming as an existential threat. {cite:p}`Sabel2025b` But the evidence that these reforms change behaviour rather than metrics remains thin, and the instruments that do work — badges with verification, mandates that are checked — succeed precisely where they add enforcement to mere endorsement. If incentives explain why voluntary stewardship fails, the question that follows is what enforced standards, mandates, and reporting guidelines can actually achieve, and where they fall short — and the distinction between the merely endorsed and the actually enforced is exactly where {ref}`sec-governance` begins. The thread it opens runs on to the review's: {ref}`sec-conclusion` repaying the debt in animal lives, and not merely in metrics, will require changing what the system counts.

:::{trust-claim}
:claim-id: clm_00dd50f41207ac70
:claim: Reform proposals are real and multiplying, and their diagnosis is now broadly shared, from proposals to restructure publication incentives to the systemic overhaul urged decades ago and the recent declarations reframing metric-gaming as an existential threat.
:cites: Nosek2012, Trueblood2025, Alberts2014, Sabel2025b
:claim-type: review_synthesis
:modality: suggestive
:::

:::{evidence-explorer}
:section: section_07
:::

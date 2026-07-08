(sec-fair-preclinical)=

# FAIR Principles and the Preclinical Data Ecosystem

If stewardship of animal-derived data is a welfare duty, as {ref}`sec-data-welfare` argued, then the community already has a putative instrument for discharging it. The FAIR Principles — that data be Findable, Accessible, Interoperable, and Reusable — have become the near-universal vocabulary for what good data stewardship means, and funders now write them into grant conditions. This section examines that instrument on its own terms. It asks not whether FAIR is a worthy aspiration but whether the ecosystem built around it — standards, ontologies, repositories, persistent identifiers, and the audits that police them — actually converts the aspiration into reusable data, and whether preclinical animal data are served at all well by it. The evidence assembled below points to a persistent and quantifiable gap between what is declared and what is delivered, a gap that preclinical research inherits in an especially acute form.

## What FAIR promises, and the apparatus built to deliver it

The FAIR Principles frame good data management not as an end in itself but as the conduit to knowledge discovery and to downstream reuse by both humans and machines {cite:p}`Wilkinson2016`. The distinction between FAIR (a stewardship standard) and *open* (an access status) matters: data can be findable and richly described while remaining under managed access, which is precisely why controlled-access genomic archives and clinical repositories claim FAIR alignment without publishing raw records. The principles have proved extraordinarily influential — a bibliometric analysis of 2,529 documents on data governance and open sharing found the FAIR paper to be the most-cited reference in the field {cite:p}`Qiu2025` — and they have spawned a substantial apparatus. Abstract principles were translated into quantifiable metrics implemented in open-source assessment tools such as F-UJI {cite:p}`Devaraju2021`; maturity models and crosswalks now let a repository score its own compliance across dimensions, and one such crosswalk of three established approaches found strong correlations in the discovery and accessibility dimensions {cite:p}`Peng2022, Corcho2024`. Yet the same tooling literature concedes that assessment instruments are often either too domain-specific or too generalist to return a concrete, interpretable FAIRness level {cite:p}`AguilarGomez2023`, and machine-actionable metadata templates such as CEDAR were introduced precisely because the community-defined "rich metadata" the principles demand was rarely being supplied in practice {cite:p}`Musen2022, Batista2022`. The apparatus, in other words, was constructed in response to a recognised shortfall. The question is how large that shortfall remains.

## The declared-versus-actual gap

The most robust finding in this literature is that stated data availability vastly exceeds real availability. A systematic review and individual-participant-data meta-analysis pooling 105 meta-research studies covering more than two million articles found that, between 2016 and 2021, roughly 8% of medical papers declared their data were publicly available while only about 2% actually shared them, with public code sharing below half a percent {cite:p}`Hamilton2023`. This ~2% figure recurs across independent audits and anchors much of the present review.

:::{margin} Provenance
**Source:** "Meta-analyses showed a prevalence of declared and actual public data availability of 8% (95% confidence interval 5% to 11%) and 2% (1% to 3%), respectively, between 2016 and 2021." {cite:p}`Hamilton2023`
**Replication:** independently replicated (aggregated across 105 meta-research studies).
:::

Converging estimates from unrelated fields reinforce it rather than average it away. An audit of biomedical papers found that only about 9% pledged public data availability and a mere 3% followed through on the pledge {cite:p}`MartinRodriguez2026`; a study of authors whose data-availability statements promised sharing found that, on request, only 6.8% actually provided the data {cite:p}`Gabelica2022`; and a cross-sectional analysis of 306 oncology articles found that, of all those sampled, just one — 0.3% (1 of 306) — met the full FAIR assessment criteria on inspection {cite:p}`Hamilton2022`. Discipline-specific screens tell the same story: only 1.5% of 7,509 dental research articles shared data at all {cite:p}`Uribe2022`, and of 1,340 Spanish COVID-19 papers only 12.5% shared any data, with just 2.1% deposited in a repository {cite:p}`CerdaCosme2022`. {numref}`fig-sec4-actual-vs-declared-availability` places the verified-availability audits on a single axis; their convergence in the low single digits, across specialties, journals, and methods, indicates a replicated ceiling rather than one field's local failure.

:::{figure} ../figures/fig_sec4_actual_vs_declared.png
:name: fig-sec4-actual-vs-declared-availability
:width: 100%
**Actual (verified) data availability sits far below declared availability.** Verified-availability rates from independent meta-research audits: ~2% of medical papers actually shared data {cite:p}`Hamilton2023`, 6.8% of authors who promised data provided it on request {cite:p}`Gabelica2022`, and just 0.3% of all sampled oncology articles met the full FAIR criteria {cite:p}`Hamilton2022`. Points show the audited rate; whiskers show 95% confidence intervals where reported. Caveat: mechanism and denominator differ — actually-public among all sampled articles ({cite:t}`Hamilton2023`, 2%), provided among only manuscripts that promised sharing ({cite:t}`Gabelica2022`, 6.8%), and FAIR-compliant among all sampled articles ({cite:t}`Hamilton2022`, 0.3% = 1 of 306; the strictest bar because it requires full FAIR compliance, not mere availability) — so these are convergent qualitative evidence, not identical rates. A fourth widely cited audit (raw data obtainable on request, 4.5%) is discussed in the text but omitted here for citation consistency.
:::

:::{dropdown} 📓 Figure code

```python
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_04.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_04.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD['actual-data-availability-rates']
# Keep only studies with a canonical cite key (RowhaniFarid/bmjopen-2016 has none).
want = {
    '10.1136/bmj-2023-075767':   dict(label='Hamilton et al. 2023\n(actually public)',
                                      val=2.0, lo=1.0, hi=3.0, marker='o'),
    '10.1016/j.jclinepi.2022.05.019': dict(label='Gabelica et al. 2022*\n(provided on request)',
                                      val=6.8, lo=None, hi=None, marker='^'),
    '10.1186/s12916-022-02644-2': dict(label='Hamilton et al. 2022\n(full FAIR, all sampled)',
                                      val=0.3, lo=0.0, hi=2.0, marker='s'),
}
rows = [want[p['doi']] for p in comp['papers'] if p['doi'] in want]
rows = sorted(rows, key=lambda r: r['val'])
y = np.arange(len(rows))

fig, ax = plt.subplots(figsize=(10, 4.9))
fig.subplots_adjust(left=0.30, right=0.97, bottom=0.30, top=0.87)
# 8% declared reference (Hamilton2023 declared availability) as context band
ax.axvspan(0, 8.0, color=COLORS['declared_nominal'], alpha=0.15, zorder=0)
ax.axvline(8.0, color=COLORS['declared_nominal'], lw=1.2, ls='--', zorder=1)
ax.text(8.15, len(rows) - 0.5, '8% declared\navailable\n(Hamilton 2023)',
        va='top', ha='left', fontsize=9.5, color=COLORS['actual_verified'])

for i, r in enumerate(rows):
    if r['lo'] is not None:
        ax.plot([r['lo'], r['hi']], [i, i], color=COLORS['ink'], lw=1.4, zorder=2)
        for x in (r['lo'], r['hi']):
            ax.plot([x, x], [i - 0.08, i + 0.08], color=COLORS['ink'], lw=1.4, zorder=2)
    ax.scatter([r['val']], [i], s=150, marker=r['marker'],
               color=COLORS['actual_verified'], edgecolor=COLORS['ink'],
               linewidth=0.8, zorder=3)
    ci = f"  (95% CI {r['lo']:.0f}–{r['hi']:.0f}%)" if r['lo'] is not None else ''
    ax.annotate(f"{r['val']:.1f}%{ci}", (r['val'], i), xytext=(11, 0),
                textcoords='offset points', va='center', fontsize=11,
                color=COLORS['ink'], fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels([r['label'] for r in rows], fontsize=10)
ax.set_xlim(-0.5, 13)
ax.set_ylim(-0.6, len(rows) - 0.2)
ax.set_xlabel('Data actually obtainable / reusable (% of articles)', labelpad=6)
ax.set_title('Verified data availability across meta-research audits', pad=10)
ax.spines['left'].set_visible(True)
fig.text(0.5, 0.04,
         '* Value extracted from abstract; full text not accessible. '
         'Denominators differ across audits (see caption).',
         ha='center', fontsize=9, style='italic', color=COLORS['gray_500'])
fig.savefig(os.path.join(FIGDIR, 'fig_sec4_actual_vs_declared.png'),
            dpi=300, facecolor='white')
plt.close(fig)
print('saved fig_sec4_actual_vs_declared.png')
```

:::

Whether policy can close this gap is itself contested. {cite:t}`Hamilton2022` reported that publishing in a journal with a mandatory data-sharing policy was associated with nearly a tenfold increase in the odds of sharing (OR 9.5, 95% CI 3.26–30.85), which suggests enforcement works. But {cite:t}`Gabelica2022` found that authors who stated they would share on request complied at essentially the same low rate as authors who made no such statement, implying that a data-availability statement is, on its own, close to inert. The reconciliation is that mandates checked at the point of publication behave differently from promises deferred to an unenforced future — a distinction that recurs throughout this review.

## Findability and access are unevenly delivered

The first two FAIR letters fare little better than the last two when measured rather than asserted. Persistent identifiers, the backbone of findability, remain under-used even where they exist: in one dataset-citation study fewer than 40% of references to two well-known datasets used the dataset's DOI {cite:p}`Mayernik2017`, and materials-science journals largely omit persistent-identifier guidance for code {cite:p}`Hormann2026`, so the links that would let a machine locate underlying data are frequently missing. Researcher and resource identifiers are similarly patchy — ORCID coverage differs substantially between institutions and data sources, and is not yet sufficient for automated reporting {cite:p}`Schnieders2022, Vrabel2016` — with the consequence that data reuse cannot even be detected: applying a link-resolution framework to one university's outputs raised the availability of author names on dataset links from 2.4% to 89.2%, and only then could a handful of reuse cases be identified at all {cite:p}`Khan2020`. Even large curated efforts to attach identifiers reach a minority of the record, matching only about 36% of taxonomic names to publications across three databases {cite:p}`Page2023`, while on-demand DOI minting is still being retrofitted onto repositories that lacked it {cite:p}`Grynoch2025`. Accessibility is not uniform either: contrary to the assumption that a repository deposit makes data equally reachable to all, access to open-science resources varies by country through connectivity failures and outright blocking {cite:p}`Shanahan2022`, the advanced services that make data usable depend on intrinsically limited computational resources that will be rationed rather than free {cite:p}`Bertelli2025`, and community-owned "diamond" infrastructures are emerging in part because commercial routes leave many researchers without genuine access {cite:p}`Guerra2026`.

## Paperwork compliance versus realized sharing

Nowhere is the policy-behaviour gap starker than in data-management plans. Under the NIH Data Management and Sharing Policy, 79.3% of submitted plans addressed all six required elements, and structured templates outperformed free-form ones {cite:p}`Hamidi2025` — formal compliance is high and improving. Yet an audit of NSF-funded projects that had filed data-management plans found that 76% received an overall data-sharing score of zero, and that when sharing did occur the data were often of questionable usability owing to access, documentation, and formatting problems {cite:p}`VanTuyl2016`. The plans were written; the data did not follow. {numref}`fig-sec4-dmp-vs-realized` deliberately separates the paperwork axis from the practice axis rather than juxtaposing superficially similar percentages, because a high completeness rate and a high non-sharing rate can coexist and even look numerically alike while meaning opposite things.

:::{admonition} Evidence Conflict: do FAIR and sharing mandates translate into usable data?
:class: warning
Review-level syntheses hold that "FAIR data leads to improved data sharing in different scientific domains" {cite:p}`Inau2023`, treating the principles as a demonstrated remedy. Project-level audits find the opposite: sharing at both the project and article level "was not carried out in the majority of cases, and when sharing was accomplished, the shared data were often of questionable usability" {cite:p}`VanTuyl2016`. The disagreement is partly one of evidence type — optimistic reviews aggregate self-reported adoption and infrastructure activity, whereas the pessimistic estimates come from direct retrieval attempts — and it defines the central tension of the FAIR ecosystem: endorsement is abundant, verified reuse is scarce. *Resolution status: unresolved.*
:::

The infrastructure to make data FAIR is neither cheap nor uniformly provided, which compounds the gap. A survey of materials-science journal data policies found that over 80% offered no guidance on persistent identifiers for code and that data sharing was typically optional rather than required {cite:p}`Hormann2026`, so the machinery of findability is frequently absent at the point of publication. Where it is present it is expensive: NIH appears to allocate roughly 10% of a genomic consortium's total budget to its data coordinating centre {cite:p}`Speir2025`, and structured elicitation in one clinical field enumerated 45 distinct barriers to implementing FAIR {cite:p}`deGroot2024`. Compliance measured as completed paperwork is therefore a poor proxy for the thing that matters, and cheap to inflate.

:::{figure} ../figures/fig_sec4_dmp_vs_realized.png
:name: fig-sec4-dmp-vs-realized
:width: 100%
**Formal compliance is high; realized sharing is near zero.** Left panel (paperwork): 79.3% of NIH data-management-and-sharing plans addressed all six required elements {cite:p}`Hamidi2025`. Right panel (practice, polarity harmonized to "share achieved"): only 24% of DMP-covered NSF projects achieved any non-zero data-sharing score — the complement of the 76% scoring zero {cite:p}`VanTuyl2016` — and field-wide realized public availability is ~2% {cite:p}`Hamilton2023`. Caveats: {cite:t}`Hamidi2025`'s 79.3% measures plan completeness (formal compliance, high = good); {cite:t}`VanTuyl2016`'s 76% measures projects that shared nothing usable (high = bad); {cite:t}`Hamilton2023`'s 2% measures realized public availability — the 79% and 76% are near-identical numbers of opposite meaning, which is why compliance and realization are shown on separate axes. Units and scale differ: plans (n=358), projects (n=25), articles (n≈2.1M).
:::

:::{dropdown} 📓 Figure code

```python
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_04.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_04.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD['formal-dmp-compliance-vs-realized-sharing']
vals = {p['doi']: p for p in comp['papers']}
hamidi = float(vals['10.1017/cts.2025.10212']['value'])          # 79.3 complete
vantuyl_zero = float(vals['10.1371/journal.pone.0147942']['value'])  # 76 scored zero
vantuyl_share = 100 - vantuyl_zero                                # 24 any sharing
hamilton = float(vals['10.1136/bmj-2023-075767']['value'])       # 2 public availability

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 5.8),
                               gridspec_kw={'width_ratios': [1, 2]})
fig.subplots_adjust(left=0.09, right=0.97, bottom=0.24, top=0.78, wspace=0.22)

# Panel A — paperwork / formal compliance (declared colouring, hatched)
axA.bar([0], [hamidi], width=0.55, color=COLORS['declared_nominal'],
        edgecolor=COLORS['ink'], hatch='///', linewidth=0.8)
axA.text(0, hamidi + 2, f'{hamidi:.1f}%', ha='center', va='bottom',
         fontsize=12, fontweight='bold', color=COLORS['ink'])
axA.set_xticks([0])
axA.set_xticklabels(['DMS plans addressing\nall 6 required elements\n(Hamidi 2025, n=358)'], fontsize=9.5)
axA.set_ylim(0, 100)
axA.set_ylabel('% achieving the stated bar')
axA.set_title('Paperwork (formal compliance)', fontsize=12)

# Panel B — practice / realized sharing (actual colouring, solid)
xb = [0, 1]
hb = [vantuyl_share, hamilton]
cb = [COLORS['actual_verified'], COLORS['fair_compliant']]
labels = ['Projects with any\nnon-zero sharing score\n(Van Tuyl 2016, n=25)',
          'Articles with data\nactually public*\n(Hamilton 2023, n≈2.1M)']
axB.bar(xb, hb, width=0.55, color=cb, edgecolor=COLORS['ink'], linewidth=0.8)
for x, h in zip(xb, hb):
    axB.text(x, h + 2, f'{h:.0f}%', ha='center', va='bottom',
             fontsize=12, fontweight='bold', color=COLORS['ink'])
axB.annotate('complement of 76%\nscoring zero', (0, vantuyl_share),
             xytext=(0, 46), textcoords='data', ha='center', fontsize=8.5,
             color=COLORS['debt'],
             arrowprops=dict(arrowstyle='->', color=COLORS['debt'], lw=1))
axB.set_xticks(xb)
axB.set_xticklabels(labels, fontsize=9.5)
axB.set_ylim(0, 100)
axB.set_title('Practice (realized sharing)', fontsize=12)

# shared legend for the polarity/colour coding — placed between title and panels
handles = [mpatches.Patch(facecolor=COLORS['declared_nominal'], hatch='///',
                          edgecolor=COLORS['ink'], label='formal compliance / paperwork (high = good)'),
           mpatches.Patch(facecolor=COLORS['actual_verified'], edgecolor=COLORS['ink'],
                          label='realized availability (high = good)')]
fig.legend(handles=handles, loc='upper center', ncol=2, frameon=False,
           bbox_to_anchor=(0.5, 0.88), fontsize=9.5)
fig.suptitle('Compliance on paper does not become usable data', y=0.975, fontsize=13)
fig.text(0.5, 0.03,
         '* Value extracted from abstract in this comparison. Axes are separated '
         'because the 79% (completeness) and 76% (non-sharing) are near-identical\n'
         'numbers of opposite meaning; Van Tuyl shown as its complement (24%).',
         ha='center', fontsize=8.8, style='italic', color=COLORS['gray_500'])
fig.savefig(os.path.join(FIGDIR, 'fig_sec4_dmp_vs_realized.png'),
            dpi=300, facecolor='white')
plt.close(fig)
print('saved fig_sec4_dmp_vs_realized.png')
```

:::

## Shared is not reusable

Even the data that clear the sharing bar tend to fall short of the *Reusable* bar, which the audits repeatedly identify as the weakest FAIR dimension. A systematic audit of omics studies in the Gene Expression Omnibus found that only 11.5% shared all of their important phenotype metadata while 37.9% shared less than 40%, with roughly a quarter of critical metadata omitted on average {cite:p}`Huang2025b`. Programmatic FAIR scoring of shared datasets returns strikingly low reusability sub-scores: a dental-research corpus returned a reported mean Reusability of about 2.4 out of 10 {cite:p}`Uribe2022`, and an independent assessment of urban air-quality datasets using a different automated tool reported Reusable scores of only 2 to 3 out of 10, with Interoperability the weakest dimension {cite:p}`Syed2025`. Self-assessed FAIR maturity of two clinical databases mapped to a common data model reached only 15.5 and 12 out of 25, the gaps concentrated in globally unique identifiers and machine-readable metadata {cite:p}`Puttmann2023`. {numref}`fig-sec4-fair-reusability` shows the two reusability audits converging on the low end of a ten-point scale despite using different tools in unrelated domains — a convergence that suggests a general reusability deficit rather than a domain artefact. The downstream cost is illustrated concretely: in global-health data reuse, one analyst described spending some 80% of their time on cleaning and curation before any analysis could begin {cite:p}`Waithira2026`, and inconsistent metadata force researchers to spend over 40% of curation time on manual standardization {cite:p}`Verbitsky2024`.

:::{figure} ../figures/fig_sec4_fair_reusability.png
:name: fig-sec4-fair-reusability
:width: 100%
**Even shared data score low on Reusability.** Independent assessments converge on low reusability: a dental-research corpus averaged 2.4/10 {cite:p}`Uribe2022` and urban air-quality datasets scored 2–3/10 {cite:p}`Syed2025`, against a scale maximum of 10 (dashed line). Sharing is necessary but far from sufficient for reuse. Caveats: the two scores come from different tools ({cite:t}`Uribe2022`: a custom Wilkinson v0.3d specification; {cite:t}`Syed2025`: F-UJI) whose /10 scales are not guaranteed identical; and the units differ — individual shared-data articles ({cite:t}`Uribe2022`, n=112, mean ± SD) versus whole datasets ({cite:t}`Syed2025`, n=4, a reported range), so {cite:t}`Syed2025`'s value rests on only four datasets. Error bar shows ± 1 SD (Uribe); the Syed bar spans the reported 2–3 range.
:::

:::{dropdown} 📓 Figure code

```python
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_04.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_04.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")

comp = FD['fair-reusability-scores']
vals = {p['doi']: p for p in comp['papers']}
uribe = vals['10.1177/00220345221101321']   # 2.4, SD 2.6, n=112
syed = vals['10.1016/j.dib.2025.112071']     # range 2-3, n=4
uribe_v, uribe_sd = 2.4, 2.6
syed_lo, syed_hi = 2.0, 3.0
syed_mid = (syed_lo + syed_hi) / 2

fig, ax = plt.subplots(figsize=(7.8, 5.4))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.26, top=0.90)
# scale maximum reference
ax.axhline(10, ls='--', lw=1.0, color=COLORS['neutral_baseline'])
ax.text(1.5, 10, 'scale maximum (10)', va='bottom', ha='right',
        fontsize=9, color=COLORS['neutral_baseline'])

# Uribe bar with +/- SD (clip lower whisker at 0)
ax.bar([0], [uribe_v], width=0.5, color=COLORS['actual_verified'],
       edgecolor=COLORS['ink'], linewidth=0.8)
lo_err = min(uribe_sd, uribe_v)
ax.errorbar([0], [uribe_v], yerr=[[lo_err], [uribe_sd]], fmt='none',
            ecolor=COLORS['ink'], elinewidth=1.2, capsize=5)
ax.text(0, uribe_v + uribe_sd + 0.2, f'{uribe_v:.1f}±1 SD', ha='center',
        va='bottom', fontsize=11, fontweight='bold', color=COLORS['ink'])

# Syed range bar (2-3)
ax.bar([1], [syed_hi - syed_lo], width=0.5, bottom=syed_lo,
       color=COLORS['secondary_cat'], edgecolor=COLORS['ink'], linewidth=0.8)
ax.text(1, syed_hi + 0.2, 'range 2–3', ha='center', va='bottom',
        fontsize=11, fontweight='bold', color=COLORS['ink'])

ax.set_xticks([0, 1])
ax.set_xticklabels(['Dental research\narticles*\n(Uribe 2022, n=112)',
                    'Urban air-quality\ndatasets*\n(Syed 2025, n=4)'], fontsize=10)
ax.set_ylim(0, 10.8)
ax.set_ylabel('FAIR Reusability sub-score (of 10)')
ax.set_title('Even shared data score low on Reusability', pad=10)
fig.text(0.5, 0.03,
         '* Both values extracted from source abstracts. Tools differ (Uribe: custom '
         'Wilkinson v0.3d; Syed: F-UJI); units differ (articles vs whole datasets).',
         ha='center', fontsize=8.6, style='italic', color=COLORS['gray_500'])
fig.savefig(os.path.join(FIGDIR, 'fig_sec4_fair_reusability.png'),
            dpi=300, facecolor='white')
plt.close(fig)
print('saved fig_sec4_fair_reusability.png')
```

:::

Why some deposited data reuse well and most do not appears to turn on whether a community standard is *enforced* rather than merely published. The contrast is sharp within neuroimaging: a purpose-built FAIR archive organised around the enforced Brain Imaging Data Structure documents substantial realized reuse, with 165 downstream publications identified that reused its datasets {cite:p}`Markiewicz2021, Poldrack2024`. That single, well-governed repository accomplishes what the diffuse ~2% ecosystem does not.

:::{admonition} Evidence Conflict: does deposition yield reuse, or does the repository decide?
:class: warning
A cross-specialty meta-analysis finds actual public data availability at only ~2% across medicine {cite:p}`Hamilton2023`, and a Gene Expression Omnibus audit finds most omics studies share badly incomplete metadata {cite:p}`Huang2025b`. Yet an archive built on an enforced community standard documents more than 150 reuse publications {cite:p}`Markiewicz2021`. Realized reuse depends less on the abstract adoption of FAIR than on whether a specific repository imposes and checks a standard at deposit — which reframes the problem from "publish the principles" to "operationalise and enforce them." *Resolution status: partially resolved (repository- and standard-dependent).*
:::

The minimum-information reporting tradition long predates FAIR and shows both the promise and the limits of standardisation. MIAME for microarrays {cite:p}`Brazma2001` seeded a family of checklists — MIAPE for proteomics {cite:p}`Taylor2007`, and the MIBBI project that catalogued the proliferating standards and coordinated their development {cite:p}`Taylor2008` — and these are genuine achievements of community consensus. But a fully specified checklist does not guarantee reusable data: the MIAPE Quant module defines the minimum information a quantitative proteomics dataset needs so that it can be critically re-analysed or its analysis workflow reproduced {cite:p}`MartinezBartolome2013`, yet an independent reprocessing found that applying the guidelines still yielded large discrepancies from the same deposited data — differing protein counts and differentially abundant sets (for example, 13,068 versus 4,923 proteins, and 108 versus 11 differentially expressed proteins) {cite:p}`Vadadokhau2026` — the shared-but-not-reusable pattern in miniature. Common data elements built on the same logic have likewise seen disappointingly low adoption and have not broadly solved interoperability {cite:p}`Kush2020`, and community checklists remain, in the main, human-readable narratives rather than the machine-actionable models that verifiable reuse requires {cite:p}`Batista2022`. The same gap between a standard's promise and its semantic reach recurs at the level of metadata registries: the ISO/IEC 11179 model is presented as automatically conferring FAIR adherence across findability, interoperability, and reusability {cite:p}`Stotl2025`, yet a variable-level harmonisation effort across cardiovascular cohorts found that it supplies only a general registry framework and lacks the formal semantic relationships needed to align variables across studies {cite:p}`Gilani2025`. Repository trust markers face the same evidentiary problem. The TRUST Principles frame repository trustworthiness as something to be earned and demonstrated through external assessment {cite:p}`Lin2020`, yet a content analysis of 91 certified repositories concluded that, although hundreds of Trustworthy Digital Repositories are certified, there is no evidence that certification actually improves preservation {cite:p}`Donaldson2020`, and an instrument applied to eight biomedical repositories found little explicit acknowledgment of open, FAIR, citable, or trustworthy principles even where the underlying practices were present {cite:p}`Murphy2021`.

## Interoperability and ontologies: standards without fidelity

Interoperability — the FAIR dimension most dependent on shared ontologies and controlled vocabularies — reveals that adopting a standard does not guarantee faithful data. Ontology developers argue that coordinated, logically well-formed ontologies deliver interoperable and accurate representations of biological reality {cite:p}`Smith2007`, but audits of the resulting annotations are sobering. An analysis of Gene Ontology molecular-function annotations estimated that 64% of UniProtKB proteins are incompletely annotated and that inconsistencies affect 83% of protein functions and at least 23% of proteins {cite:p}`Faria2012`; most annotations are generated by automated electronic inference rather than expert curation, so the bulk of the record is broad and not experimentally verified {cite:p}`Buza2008`; a single co-annotation quality-control system corrected over 380,000 inferred annotations traced to just 54 mapping errors {cite:p}`Wood2020`; and even the curated reference plant genome had experimental or predicted localization for only 90% of the proteome in its best-covered aspect {cite:p}`Reiser2024`. Cross-ontology audits find over 1,900 logical nonalignments between core biomedical ontologies {cite:p}`Bada2008`. The vocabularies are real infrastructure, but their coverage and internal consistency are weaker than their adoption statistics imply.

:::{admonition} Evidence Conflict: does FAIRification improve or degrade data quality?
:class: warning
Manual curation and ontology mapping across 212,027 omics samples from 468 studies consolidated redundant information and increased the completeness of major attributes {cite:p}`Long2026`. But an automated FAIRification of rare-disease electronic-health-record data across 24 German medical centres *introduced* 1,977 new completeness issues (1,988 data-quality issues in total, of which 68% were later resolved) relative to a direct export {cite:p}`Tahar2026`. The transformation intended to make data machine-actionable can inject the very deficiencies it is meant to cure when applied automatically at scale — so the value of FAIRification is contingent on curation effort, not intrinsic to the format. *Resolution status: unresolved.*
:::

Clinical common data models illustrate the same point at the level of semantics. Mapping to the OMOP common data model repeatedly loses domain content: standard OMOP vocabularies could directly represent only a quarter (19 of 75) of core extracorporeal-life-support concepts {cite:p}`Rieder2026`, a scoping review found OMOP vocabularies lack the granularity to capture oncology concepts and care episodes {cite:p}`Nada2026`, and deep phenotyping of a rare skin disease mapped only 13,485 of 33,347 extracted phenotypes to a standard concept, leaving nearly twenty thousand unmapped {cite:p}`Bataille2026`. This content loss has to be set against OMOP's reach, however: a criteria-based systematic review found the OMOP/OHDSI model to be the dominant and most comprehensive common data model, underpinning a distributed network of more than 331 data sources and over 2.1 billion patient records across 34 countries {cite:p}`Finster2025`. The tension is between coverage at scale and fidelity within any given specialty — breadth of adoption does not close the domain-level mapping gaps. Exchange standards leak as badly as models: in one single-institution study, biomarker data present in the source record were missing in 80–100% of downstream standardized extracts {cite:p}`App2026`. Adherence to an interoperability standard, then, is necessary infrastructure but does not by itself yield complete or faithful data.

## The governance qualifier: FAIR reuse versus CARE

Maximal findability and community reuse — the direction in which FAIR pushes — is not an unconditional good, and the strongest challenge to it is ethical rather than technical.

:::{admonition} Evidence Conflict: FAIR openness versus CARE governance
:class: warning
FAIR frames maximal findability, accessibility, and reuse by the community as the goal of good data management {cite:p}`Wilkinson2016`. The CARE Principles for Indigenous Data Governance were developed to complement it: FAIR facilitates sharing, but Indigenous Data Sovereignty holds that data on Indigenous Peoples must be shared on those peoples' terms {cite:p}`Carroll2022b`. This is not a rejection of stewardship but a re-specification of *whose* interests reuse must serve — a qualifier that maximal-openness claims must accommodate. *Resolution status: unresolved (complementary frameworks in tension).*
:::

The CARE position is now well developed: Indigenous research sovereignty asserts self-determination over data generated from research activities {cite:p}`Hudson2023, Garba2023`, universities are being urged to operationalise collective Indigenous rights over data against default open-data models {cite:p}`West2026`, and emerging equitable global-health frameworks explicitly reject a default "open" setting in favour of governed access {cite:p}`Mayor2026, Calac2026`. The stakes are concrete where reference resources under-represent populations — Aboriginal and Torres Strait Islander peoples, for instance, are largely absent from human reference genomes {cite:p}`ClarkAdnyamathanha2024`. Governance constraints of a different kind bind the ordinary case too: privacy regulation such as GDPR can directly contradict open-data mandates {cite:p}`Hassenstein2025`, and human genomic and biospecimen repositories frequently operate under managed rather than open access for exactly this reason {cite:p}`Heeney2017`. The lesson is that "reuse" is a governed act, and a stewardship standard that measures only the ease of reuse is incomplete.

## Is universal retention worth its cost?

FAIR's implicit demand — keep everything, curate it, and keep it rapidly accessible indefinitely — carries a bill that is now being questioned on both economic and ecological grounds.

:::{admonition} Evidence Conflict: is indefinite retention of all data sustainable?
:class: warning
One position holds that "it is not sustainable to keep accumulating and maintaining all datasets for rapid access, considering the monetary and ecological cost of maintaining repositories" {cite:p}`Pernet2023`. The counter-position holds that "these costs are outweighed by the benefits of making research more reproducible, impactful, and equitable by facilitating the reuse of precious research resources" {cite:p}`GarciaClosas2023`. The disagreement is a genuine cost–benefit dispute, and its resolution depends on selection — which data are worth curating — rather than on an all-or-nothing choice. *Resolution status: unresolved.*
:::

The sustainability worry is not hypothetical. A survey of 118 palaeontological and Earth-science databases found that roughly 85% of community-curated databases have lifespans under fifteen years, with peaks in database loss tracking five-year funding cycles — decades of volunteered data at risk of disappearing {cite:p}`Dowding2026`. On the benefit side, the incentive most often invoked — a citation advantage for open data — is real but modest and method-sensitive: a 122,000-publication analysis found that depositing data in a repository was associated with only a 4.3% citation advantage on average, and none for sharing code {cite:p}`Colavizza2024`, whereas a synthetic-control study of a journal-level open-data mandate reported a much larger increase {cite:p}`Zhang2021`. Realized reuse is also highly concentrated, with downloads focused on a small share of deposited datasets {cite:p}`Late2024`, so the average dataset returns little of the reuse dividend that justifies its retention. A scoping review of interventions to incentivise sharing screened over a thousand papers and identified only a modest set of tested levers {cite:p}`Woods2022`; at a different level entirely — and outside the animal-data scope of this review — the motivations of the individuals whose data are shared, whether financial or altruistic, are a distinct determinant of participation that generic institutional incentives do not touch {cite:p}`Schmeiss2026, Kim2026a`. Universal open-raw-data mandates can themselves cause harm where they force qualitative or consent-sensitive material into an inappropriate mould {cite:p}`Prosser2024`. The efficient policy is therefore selective, high-value retention rather than indiscriminate accumulation — which is exactly the argument {ref}`sec-virtual-controls` develops for control-animal data.

## Preclinical animal data at the back of the queue

Preclinical animal data sit at the intersection of every deficit catalogued above, and are served worse than most. The reporting standards that would make an in vivo experiment reusable are unevenly adopted: the zebrafish community has not widely adopted data or metadata standards, so husbandry, imaging, and toxicology reporting remain inconsistent and reproducibility suffers {cite:p}`Ngu2025`, and traumatic-brain-injury translation is dominated by unpublished "dark data" from small, heterogeneous studies that never enter a findable record {cite:p}`Hawkins2020`. Where exemplary practice exists it is the exception that proves the rule — a MIAPE-compliant proteomic study of salbutamol effects on rat muscle was published explicitly as a model of how in vivo data *should* be deposited {cite:p}`Kenyani2011`. The research reagents on which animal studies depend are themselves poorly stewarded: manual curation could identify only 1,445 studies providing knockout-validated evidence for specific antibodies, a tiny fraction of those in use {cite:p}`Biddle2024`, and roughly 40% of antibodies cited in one literature remained non-findable, lacking persistent research-resource identifiers, until stock centres actively intervened {cite:p}`Piekniewska2025`.

Part of the preclinical deficit begins at the bench, before any deposit decision is made, in how in vivo experiments are recorded. Electronic laboratory notebooks are advocated across chemistry {cite:p}`HerresPawlis2022`, computational drug discovery {cite:p}`Schaduangrat2020`, and regulated bioanalysis {cite:p}`Zeng2011` as the route from analogue records to FAIR-aligned capture at source {cite:p}`Solle2020, Higgins2022`, and structured, template-driven capture demonstrably helps — an AI-assisted chemistry notebook with built-in structured documentation improved student adherence to good data practice {cite:p}`Nwafor2025`, and ontology-based notebooks can capture and automatically validate complex instrument metadata that would otherwise be lost {cite:p}`Kirchner2026`. But provision is not adoption, which surfaces a further tension of the ecosystem.

:::{admonition} Evidence Conflict: does providing metadata infrastructure yield reusable metadata?
:class: warning
A study of user-defined metadata in an electronic laboratory notebook found that many users made little effort to add metadata even when the facility existed, endangering their own ability to recover data later {cite:p}`Willoughby2014`. The templated ISA-model alternative generates structured metadata in parallel at each level of a project so that submission is guided rather than optional {cite:p}`Petek2022`. Whether infrastructure produces reusable metadata thus depends on whether capture is enforced-by-design or left to discretionary effort — the same enforcement-versus-endorsement fault line seen in sharing mandates and repository standards. *Resolution status: partially resolved (design-dependent).*
:::

Dedicated model-organism infrastructures show what good stewardship looks like — the Rat Genome Database curates multi-species genomic and phenotype data explicitly to fulfil FAIR {cite:p}`Vedi2023`, and the European Mouse Mutant Archive established ten Quality Principles to standardize the scientific evaluation of cryopreserved rodent disease models {cite:p}`Ehlich2025` — but these are islands, and metadata tooling for experimental in vivo work, such as the ISA framework in environmental-health science, is still being retrofitted onto fields that never captured it natively {cite:p}`Nault2023`.

The welfare consequence is direct and is the reason this section belongs in the argument at all. When a preclinical dataset is unfindable, incompletely described, or non-reusable, the animals that produced it have paid a welfare cost for knowledge that cannot be reused, and the experiment must often be repeated. Failure to share research biospecimens and data diverts funds into duplicate cohorts and deters reproducibility assessment {cite:p}`Rush2024`; cancer heterogeneity means single centres cannot generate enough data for accurate models, which was part of the original motivation for FAIR in the first place {cite:p}`Vesteghem2019`. The evidence of this section is that the generic FAIR ecosystem — declared but not delivered, compliant on paper but empty in practice, shared but not reusable — repays the data-welfare debt only weakly and unevenly. Because diffuse, all-data sharing so rarely converts into a second scientific use, that diagnosis motivates a change of tack: rather than pursue generic reuse of everything, {ref}`sec-virtual-controls` turns to a specific, high-value form of reuse in which the Reduction dividend is directly quantifiable — reusing curated control-animal data as virtual control groups, so that fewer animals are assigned to concurrent controls. Where general-purpose sharing has under-delivered, that targeted application is where the debt can most tangibly be repaid.

:::{evidence-explorer}
:evidence-dir: ../evidence
:height: 800px
:::

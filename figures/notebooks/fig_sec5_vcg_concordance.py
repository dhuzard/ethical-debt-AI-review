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

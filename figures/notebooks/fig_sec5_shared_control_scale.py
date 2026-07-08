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

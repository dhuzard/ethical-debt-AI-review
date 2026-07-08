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

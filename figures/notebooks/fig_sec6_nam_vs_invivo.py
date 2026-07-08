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

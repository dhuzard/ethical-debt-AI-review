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

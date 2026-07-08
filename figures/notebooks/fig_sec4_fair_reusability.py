"""FAIR Reusability sub-scores of shared/published datasets

Reproducible source for fig_sec4_fair_reusability.png. Loads values from
evidence/evidence_section_04.json (figure_data comparison 'fair-reusability-scores') and styles
with figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec4_fair_reusability.py
"""
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


ROOT = find_root(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure  # noqa: E402

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

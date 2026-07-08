"""Formal DMP/DMSP compliance versus realized data sharing

Reproducible source for fig_sec4_dmp_vs_realized.png. Loads values from
evidence/evidence_section_04.json (figure_data comparison 'formal-dmp-compliance-vs-realized-sharing') and styles
with figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec4_dmp_vs_realized.py
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

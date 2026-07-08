"""Actual (verified) data availability vs declared, across meta-research audits

Reproducible source for fig_sec4_actual_vs_declared.png. Loads values from
evidence/evidence_section_04.json (figure_data comparison 'actual-data-availability-rates') and styles
with figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec4_actual_vs_declared.py
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

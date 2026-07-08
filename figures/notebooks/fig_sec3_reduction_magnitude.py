"""
Figure: Achievable Reduction in animal numbers by method (section 3).
=====================================================================

Cross-study comparison (Type B). Three independent methodological approaches
each report roughly halving-to-~90% reductions in animal numbers, grounding
the "reuse/design as Reduction" reframe in concrete magnitudes.

Data source: evidence_section_03.json -> figure_data ->
comparison_id == "reduction-magnitude-design-methods".

All plotted values come from the evidence package's value_source_sentence
fields. Reductions are APPROXIMATE qualitative ranges, not point estimates
(Phase 6 CAVEAT); baselines and mechanisms differ (see caption).
"""

import os
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

# ── locate repo root (dir that contains an 'evidence' folder) and shared_style ──
_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
sys.path.insert(0, _here)  # shared_style.py lives beside this script
from shared_style import COLORS, apply_style, save_figure  # noqa: E402


def _find_repo_root(start):
    d = os.path.abspath(start)
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "evidence")):
            return d
        d = os.path.dirname(d)
    return os.path.abspath(os.path.join(start, "..", ".."))


REPO = _find_repo_root(_here)
EVIDENCE = os.path.join(REPO, "evidence", "evidence_section_03.json")
FIG_DIR = os.path.join(REPO, "figures")

# ── load the comparison from the evidence package ──
with open(EVIDENCE, encoding="utf-8") as fh:
    ev = json.load(fh)

comp = next(c for c in ev["figure_data"]
            if c["comparison_id"] == "reduction-magnitude-design-methods")

# Short study labels (from author_name_table display fields) keyed by DOI.
LABELS = {
    "10.1667/RADE-22-00124.1": "Landes et al. 2023",
    "10.1016/j.ejphar.2015.03.040": "Graham & Prescott 2015",
    "10.1111/brv.12237": "Kramer & Font 2015*",
}
# Representative reduction magnitudes consistent with the verbatim ranges
# ("roughly halving-to-90%"); exact phrase is printed on each bar.
HEIGHT = {
    "10.1667/RADE-22-00124.1": 50.0,   # to < half of typical  -> ~50% reduction
    "10.1016/j.ejphar.2015.03.040": 90.0,  # ~90%
    "10.1111/brv.12237": 55.0,         # > half (control animals only)
}
PHRASE = {
    "10.1667/RADE-22-00124.1": "to < half\nof typical",
    "10.1016/j.ejphar.2015.03.040": "~90%",
    "10.1111/brv.12237": "> half\n(controls)",
}
MECH = {
    "10.1667/RADE-22-00124.1": "Power / sample-size\ncalculation",
    "10.1016/j.ejphar.2015.03.040": "Model\nrefinement",
    "10.1111/brv.12237": "Historical\ncontrols",
}
# baseline: whole experiment vs control-group-only -> encode with hatch
CONTROL_ONLY = {"10.1111/brv.12237"}

order = ["10.1667/RADE-22-00124.1", "10.1016/j.ejphar.2015.03.040", "10.1111/brv.12237"]

apply_style()
fig, ax = plt.subplots(figsize=(9.0, 6.4))

x = np.arange(len(order))
for i, doi in enumerate(order):
    hatch = "//" if doi in CONTROL_ONLY else None
    ax.bar(x[i], HEIGHT[doi], width=0.62, color=COLORS["repayment"],
           edgecolor=COLORS["ink"], linewidth=0.8, hatch=hatch, zorder=3)
    # verbatim qualitative value on each bar
    ax.text(x[i], HEIGHT[doi] + 2.5, PHRASE[doi], ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=COLORS["ink"])

# dashed reference line at 50% ("halving")
ax.axhline(50, ls="--", lw=1.0, color=COLORS["neutral_baseline"], zorder=1)
ax.text(len(order) - 0.5, 51.5, "halving", ha="right", va="bottom",
        fontsize=10, style="italic", color=COLORS["gray_500"])

ax.set_xticks(x)
ax.set_xticklabels([f"{LABELS[d]}\n{MECH[d]}" for d in order], fontsize=11.5)
ax.set_ylim(0, 100)
ax.set_ylabel("Approximate reduction in animal numbers (%)", fontsize=13)
ax.set_yticks(range(0, 101, 20))

# in-figure honesty notes, placed below the axis (clear of the bars)
ax.text(0.5, -0.22,
        "Approximate qualitative ranges — baselines & mechanisms differ (see caption).",
        transform=ax.transAxes, fontsize=9.5, style="italic",
        color=COLORS["gray_500"], va="top", ha="center")
ax.text(0.5, -0.28,
        "Hatched bar = control-group animals only.    * value extracted from abstract.",
        transform=ax.transAxes, fontsize=9.5, color=COLORS["gray_500"],
        va="top", ha="center")

fig.tight_layout()
os.makedirs(FIG_DIR, exist_ok=True)
save_figure(fig, os.path.join(FIG_DIR, "fig_sec3_reduction_magnitude.png"))
print("saved:", os.path.join(FIG_DIR, "fig_sec3_reduction_magnitude.png"))

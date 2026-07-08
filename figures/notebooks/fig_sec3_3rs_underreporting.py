"""
Figure: Under-reporting of Reduction and Refinement in animal studies (section 3).
==================================================================================

Cross-study comparison (Type B). Restructured per Phase 6
(audit_verdict_resolved == "CAVEAT_FORCED_FROM_SPLIT"): every entry is
expressed on a COMMON DIRECTION as "% of studies reporting the item", and the
sample-size-calculation item (a Reduction indicator: Bara, Landes) is separated
from the analgesia item (a Refinement indicator: Pound). This avoids plotting
5 / 0 / 97 on one axis, since Pound's 97% is studies that did NOT report.

Data source: evidence_section_03.json -> figure_data ->
comparison_id == "sample-size-power-welfare-reporting".
Reduction vs Refinement indicators are distinguished by hatch AND colour.
"""

import os
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
sys.path.insert(0, _here)
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

with open(EVIDENCE, encoding="utf-8") as fh:
    ev = json.load(fh)

comp = next(c for c in ev["figure_data"]
            if c["comparison_id"] == "sample-size-power-welfare-reporting")

# Re-express every entry as "% of studies reporting the item":
#   Bara (5% used a sample-size calc), Landes (0 of 28 -> 0%)  -> Reduction
#   Pound (97% did NOT report analgesia -> 3% DID report)       -> Refinement
# Percentages are read from the evidence value_source_sentence fields.
ENTRIES = [
    # (label, percent_reporting, indicator)
    ("Bara & Joffe 2014\ncritical-care studies", 5.0, "Reduction"),
    ("Landes et al. 2023\nradiation DRF experiments", 0.0, "Reduction"),
    ("Pound & Nicol 2018\npreclinical studies", 3.0, "Refinement"),
]

COLOR = {"Reduction": COLORS["actual_verified"], "Refinement": COLORS["debt"]}
HATCH = {"Reduction": None, "Refinement": "xx"}

apply_style()
fig, ax = plt.subplots(figsize=(9.4, 6.2))

# positions: two Reduction bars, gap, one Refinement bar
xpos = [0, 1, 2.4]
for (label, pct, ind), xp in zip(ENTRIES, xpos):
    ax.bar(xp, pct, width=0.7, color=COLOR[ind], edgecolor=COLORS["ink"],
           linewidth=0.8, hatch=HATCH[ind], zorder=3)
    ax.text(xp, pct + 1.5, f"{pct:.0f}%", ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=COLORS["ink"])

# reference line at full compliance
ax.axhline(100, ls="--", lw=1.0, color=COLORS["neutral_baseline"], zorder=1)
ax.text(2.4, 97, "full reporting (100%)", ha="right", va="top",
        fontsize=10, style="italic", color=COLORS["gray_500"])

# group headers in the (empty) mid-field; colour + hatch double-encode the R
ax.text(0.5, 62, "Reduction indicator\n(sample-size / power\ncalculation reported)",
        ha="center", va="center", fontsize=12, color=COLOR["Reduction"], fontweight="bold")
ax.text(2.4, 62, "Refinement indicator,\nhatched\n(analgesia use reported)",
        ha="center", va="center", fontsize=12, color=COLOR["Refinement"], fontweight="bold")

ax.set_xticks(xpos)
ax.set_xticklabels([e[0] for e in ENTRIES], fontsize=10.5)
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 20))
ax.set_ylabel("Studies reporting the item (%)", fontsize=13)

ax.text(0.5, -0.20,
        "All values from full-text audits. Bars re-expressed as '% reporting the item'"
        " on a common direction; on that axis all three are low (5%, 0%, ~3%).",
        transform=ax.transAxes, fontsize=9.5, style="italic",
        color=COLORS["gray_500"], ha="center", va="top")

fig.tight_layout()
os.makedirs(FIG_DIR, exist_ok=True)
save_figure(fig, os.path.join(FIG_DIR, "fig_sec3_3rs_underreporting.png"))
print("saved:", os.path.join(FIG_DIR, "fig_sec3_3rs_underreporting.png"))

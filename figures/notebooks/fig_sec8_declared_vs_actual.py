"""Declared vs actual vs FAIR-compliant data availability, labelled by true construct.

Reproducible source for fig_sec8_declared_vs_actual.png. Loads values from
evidence/evidence_section_08.json (figure_data comparison
'data-availability-declared-vs-actual') and styles with
figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec8_declared_vs_actual.py

Phase-6 verdict CAVEAT: each bar is labelled by its true construct and the three
studies are NOT pooled. Federer2018's ~20% is a different construct (share of
data-availability statements that name a repository) and is separated visually.
"""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_08.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style  # noqa: E402

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_08.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")
comp = FD["data-availability-declared-vs-actual"]

C_DECL = COLORS["declared_nominal"]   # #56B4E9  declared / nominal (hatched)
C_ACT = COLORS["actual_verified"]     # #0072B2  actual / verified (solid)
C_FAIR = COLORS["fair_compliant"]     # #004C6D  FAIR-compliant (darkest)

# (x, height, colour, hatch, label, value_text, construct-group)
bars = [
    # Federer2018 — DIFFERENT construct (repository share among statements)
    dict(x=0.0, h=20.0, c=C_DECL, hatch="///", vt="~20%",
         lab="Federer2018\nDAS naming a\nrepository"),
    # Hamilton2023 — declared vs actual (medicine-wide)
    dict(x=1.4, h=8.0,  c=C_DECL, hatch="///", vt="8%",  lab="Hamilton2023\ndeclared"),
    dict(x=2.1, h=2.0,  c=C_ACT,  hatch="",    vt="2%",  lab="Hamilton2023\nactual"),
    # Hamilton2022 — declared vs actual vs FAIR (oncology)
    dict(x=3.3, h=19.0, c=C_DECL, hatch="///", vt="19%", lab="Hamilton2022\ndeclared"),
    dict(x=4.0, h=16.0, c=C_ACT,  hatch="",    vt="16%", lab="Hamilton2022\nactual"),
    dict(x=4.7, h=0.8,  c=C_FAIR, hatch="",    vt="<1%", lab="Hamilton2022\nFAIR"),
]

fig, ax = plt.subplots(figsize=(11.5, 6.0))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.24, top=0.88)

for b in bars:
    ax.bar(b["x"], b["h"], width=0.62, color=b["c"], hatch=b["hatch"],
           edgecolor=COLORS["ink"], linewidth=0.6, zorder=3)
    ax.annotate(b["vt"], (b["x"], b["h"]), xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", fontsize=11, fontweight="bold", color=COLORS["ink"])

ax.set_xticks([b["x"] for b in bars])
ax.set_xticklabels([b["lab"] for b in bars], fontsize=8.6)

# divider separating Federer's different construct from the availability studies
ax.axvline(0.72, color=COLORS["gray_500"], lw=0.9, ls="--", zorder=1)
ax.text(0.0, 24.5, "different construct\n(not an availability rate)", ha="center", va="bottom",
        fontsize=8.5, color=COLORS["gray_700"], style="italic")
ax.text(2.75, 24.5, "declared → actual → FAIR-compliant availability", ha="center", va="bottom",
        fontsize=9.5, color=COLORS["gray_700"])

ax.set_ylim(0, 27)
ax.set_xlim(-0.6, 5.3)
ax.set_ylabel("Share of papers / statements (%)")
ax.set_title("Actual availability collapses against declared, and further against FAIR", pad=12)

legend = [
    Patch(facecolor=C_DECL, hatch="///", edgecolor=COLORS["ink"], label="Declared / nominal"),
    Patch(facecolor=C_ACT, edgecolor=COLORS["ink"], label="Actual / verified"),
    Patch(facecolor=C_FAIR, edgecolor=COLORS["ink"], label="FAIR-compliant"),
]
ax.legend(handles=legend, loc="upper right", fontsize=9.5, framealpha=0.95)
fig.text(0.09, 0.02,
         "Bars labelled by true construct and not pooled. FAIR-compliant sub-metric available "
         "only for the oncology study (Hamilton2022).",
         ha="left", fontsize=8, style="italic", color=COLORS["gray_500"])

fig.savefig(os.path.join(FIGDIR, "fig_sec8_declared_vs_actual.png"),
            dpi=300, bbox_inches="tight", facecolor="white", pad_inches=0.3)
plt.close(fig)
print("saved fig_sec8_declared_vs_actual.png")

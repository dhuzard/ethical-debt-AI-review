"""Data-sharing improvement: single-institution trend vs field-wide single points.

Reproducible source for fig_sec8_institution_vs_fieldwide.png. Loads values from
evidence/evidence_section_08.json (figure_data comparison
'data-sharing-trend-institutional-vs-fieldwide') and styles with
figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec8_institution_vs_fieldwide.py

Phase-6 verdict CAVEAT: Deeb2025 is shown as a TREND LINE; the Hamilton values
are shown as SEPARATE single-point estimates. The two panels are not joined, so
no single continuous comparison is drawn between institution and field.
"""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt


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
comp = FD["data-sharing-trend-institutional-vs-fieldwide"]

C_TREND = COLORS["conflict"]        # amber — the optimistic single-institution trend
C_ACT = COLORS["actual_verified"]   # blue — field-wide verified availability
C_FAIR = COLORS["fair_compliant"]   # dark blue — FAIR-compliant

YMAX = 50
fig = plt.figure(figsize=(12.5, 6.0))
gs = fig.add_gridspec(1, 2, width_ratios=[2.1, 1.2], wspace=0.32)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])

# --- Panel A: Deeb2025 institutional trend 2014 -> 2023 (7% -> 45%) ---
years = [2014, 2023]
vals = [7.0, 45.0]
axA.plot(years, vals, color=C_TREND, lw=2.6, marker="o", markersize=10,
         markeredgecolor=COLORS["ink"], markeredgewidth=0.8, zorder=4)
for yr, v in zip(years, vals):
    axA.annotate(f"{v:.0f}%", (yr, v), xytext=(0, 10), textcoords="offset points",
                 ha="center", fontsize=12, fontweight="bold", color=COLORS["ink"])
axA.set_xlim(2012.7, 2024.3)
axA.set_ylim(0, YMAX)
axA.set_xticks([2014, 2017, 2020, 2023])
axA.set_ylabel("Papers sharing data (%)")
axA.set_xlabel("Year")
axA.set_title("A  Deeb2025 — one institution\n(share all relevant data; manual openness/FAIR score)",
              fontsize=11.5, loc="left", pad=10)
axA.text(2018.5, 40, "trend, single institution\n(incl. supplementary /\ngenomic deposits)",
         ha="center", va="center", fontsize=9, color=COLORS["gray_700"], style="italic")

# --- Panel B: field-wide single-point estimates (not a trend) ---
pts = [
    dict(x=0, v=2.0, lo=1.0, hi=3.0, c=C_ACT, m="o", lab="Hamilton2023\nactual\n(medicine)"),
    dict(x=1, v=16.0, lo=12.0, hi=20.0, c=C_ACT, m="s", lab="Hamilton2022\nactual\n(oncology)"),
    dict(x=2, v=0.6, lo=0.0, hi=2.0, c=C_FAIR, m="D", lab="Hamilton2022\nFAIR\n(<1%)"),
]
for p in pts:
    axB.plot([p["x"], p["x"]], [p["lo"], p["hi"]], color=COLORS["ink"], lw=1.3, zorder=2)
    for yy in (p["lo"], p["hi"]):
        axB.plot([p["x"] - 0.08, p["x"] + 0.08], [yy, yy], color=COLORS["ink"], lw=1.3, zorder=2)
    axB.scatter([p["x"]], [p["v"]], s=150, marker=p["m"], color=p["c"],
                edgecolor=COLORS["ink"], linewidth=0.8, zorder=4)
    vt = "<1%" if p["v"] < 1 else f"{p['v']:.0f}%"
    axB.annotate(vt, (p["x"], p["v"]), xytext=(11, 0), textcoords="offset points",
                 va="center", fontsize=11, fontweight="bold", color=COLORS["ink"])
axB.set_xticks([p["x"] for p in pts])
axB.set_xticklabels([p["lab"] for p in pts], fontsize=8.5)
axB.set_xlim(-0.55, 2.55)
axB.set_ylim(0, YMAX)
axB.set_ylabel("Verified public availability (%)")
axB.set_title("B  Field-wide pooled estimates\n(single points, not a trend)",
              fontsize=11.5, loc="left", pad=10)

fig.text(0.01, 0.005,
         "Not a like-for-like comparison: the institutional series (A) and the field-wide points (B) "
         "differ in metric definition, discipline, data type and time window; they are shown on "
         "separate axes and are deliberately not joined.",
         ha="left", fontsize=8, style="italic", color=COLORS["gray_500"])

fig.savefig(os.path.join(FIGDIR, "fig_sec8_institution_vs_fieldwide.png"),
            dpi=300, bbox_inches="tight", facecolor="white", pad_inches=0.3)
plt.close(fig)
print("saved fig_sec8_institution_vs_fieldwide.png")

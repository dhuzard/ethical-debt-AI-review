"""Animal-research reporting before vs after guideline/policy mandates.

Reproducible source for fig_sec8_guideline_timeline.png. Loads values from
evidence/evidence_section_08.json (figure_data comparison
'guideline-adherence-before-after') and styles with
figures/notebooks/shared_style.py. Run from anywhere in the repo:
    python figures/notebooks/fig_sec8_guideline_timeline.py

Phase-6 restructure honoured here:
  * Lin2024 is converted to POSITIVE polarity (% average-or-better = 100 - % poor,
    53.95 -> 90.45) so it reads on the same "higher is better" axis as the others.
  * Hair2019 is a randomized control-vs-intervention contrast and is placed in a
    SEPARATE panel (B), not on the time-trend axis.
  * Munro2022 is an UNCONTROLLED decade-apart secular time trend (ARRIVE is only
    the auditors' scoring rubric, not a mandated intervention); it is shown in a
    distinct category (colour + dashed arrow) and is NOT counted as enforcement
    evidence. Only Macleod2019b (matched control unchanged) is a controlled/
    enforced contrast on this axis.
"""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


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
comp = FD["guideline-adherence-before-after"]
P = {p["doi"]: p for p in comp["papers"]}

# --- Panel A: time-trend before/after (higher = better) ---
# value_source_sentences confirm each pair; Lin2024 converted to positive polarity.
# cat: 'enforced'    = controlled/mandated intervention (matched control unchanged)
#      'endorsement' = passive publication/endorsement of a guideline
#      'secular'     = uncontrolled decade-apart trend (guideline is only the scoring rubric)
trend = [
    dict(key="Gulin2015",  doi="10.1371/journal.pntd.0004194", before=51.0,  after=66.0,
         item="Ethics/3Rs statement", contrast="pre/post ARRIVE\n(passive, ns p=0.26)", cat="endorsement"),
    dict(key="Lin2024",    doi="10.21037/cdt-24-413",          before=53.95, after=90.45,
         item="Avg-or-better quality band*", contrast="pre-ARRIVE 1.0 ->\npost-ARRIVE 2.0\n(endorsement)", cat="endorsement"),
    dict(key="Munro2022",  doi="10.1016/j.vaa.2021.09.004",    before=13.6,  after=85.7,
         item="Randomisation", contrast="2009 vs 2019\n(uncontrolled trend)", cat="secular"),
    dict(key="Macleod2019b", doi="10.1136/bmjos-2017-000035",  before=0.0,   after=16.4,
         item="Landis-4 bias items", contrast="pre/post Nature\npolicy (mandated,\nmatched control)", cat="enforced"),
]

fig = plt.figure(figsize=(13.5, 7.2))
gs = fig.add_gridspec(1, 2, width_ratios=[3.2, 1.0], wspace=0.30,
                      left=0.075, right=0.99, bottom=0.26, top=0.90)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])

col_enf = COLORS["repayment"]      # green  = enforced / controlled
col_end = COLORS["conflict"]       # amber  = endorsement / passive
col_sec = COLORS["secondary_cat"]  # purple = uncontrolled secular trend
col_before = COLORS["neutral_baseline"]
CAT = {
    "enforced":    dict(color=col_enf, ls="-"),
    "endorsement": dict(color=col_end, ls="-"),
    "secular":     dict(color=col_sec, ls=(0, (5, 2))),  # dashed = redundant cue
}

x = np.arange(len(trend))
for i, r in enumerate(trend):
    style = CAT[r["cat"]]
    c, ls = style["color"], style["ls"]
    # arrow before -> after
    axA.annotate("", xy=(i, r["after"]), xytext=(i, r["before"]),
                 arrowprops=dict(arrowstyle="-|>", color=c, lw=2.6, ls=ls, shrinkA=6, shrinkB=6))
    # before marker (open circle, neutral)
    axA.scatter([i], [r["before"]], s=95, marker="o", facecolor="white",
                edgecolor=col_before, linewidth=1.8, zorder=4)
    # after marker (filled triangle, category colour)
    axA.scatter([i], [r["after"]], s=150, marker="^", color=c,
                edgecolor=COLORS["ink"], linewidth=0.8, zorder=5)
    axA.annotate(f"{r['before']:.1f}%", (i, r["before"]), xytext=(-8, -2),
                 textcoords="offset points", ha="right", va="center",
                 fontsize=10, color=COLORS["gray_700"])
    axA.annotate(f"{r['after']:.1f}%", (i, r["after"]), xytext=(11, 7),
                 textcoords="offset points", ha="left", va="center",
                 fontsize=11, color=COLORS["ink"], fontweight="bold")

axA.set_xticks(x)
axA.set_xticklabels([f"{r['key']}\n{r['item']}\n{r['contrast']}" for r in trend], fontsize=9)
axA.set_ylim(-5, 106)
axA.set_xlim(-0.6, len(trend) - 0.4)
axA.set_ylabel("Reporting / adherence (%, higher is better)")
axA.set_title("A  Before → after guideline/policy change (time contrasts)", fontsize=13, loc="left", pad=10)
axA.axhline(95, color=COLORS["gray_500"], lw=0.75, ls=":", zorder=0)
axA.text(-0.5, 96, "95% ideal", ha="left", va="bottom",
         fontsize=8.5, color=COLORS["gray_500"])

legend_A = [
    Line2D([0], [0], marker="o", markerfacecolor="white", markeredgecolor=col_before,
           markersize=9, lw=0, label="Before"),
    Line2D([0], [0], marker="^", markerfacecolor=COLORS["gray_500"], markeredgecolor=COLORS["ink"],
           markersize=10, lw=0, label="After"),
    Line2D([0], [0], color=col_enf, lw=2.6, label="Enforced / controlled"),
    Line2D([0], [0], color=col_end, lw=2.6, label="Endorsement / passive"),
    Line2D([0], [0], color=col_sec, lw=2.6, ls=(0, (5, 2)), label="Uncontrolled secular trend"),
]
axA.legend(handles=legend_A, loc="center", bbox_to_anchor=(0.60, 0.46),
           fontsize=9, framealpha=0.96, ncol=2)

# --- Panel B: Hair2019 RCT control vs intervention (husbandry subitem) ---
hb = P["10.1186/s41073-019-0069-3"]
xb = np.arange(2)
vals = [52.1, 74.1]
labels = ["Control", "Checklist-\nrequest"]
bars = axB.bar(xb, vals, width=0.6, color=[COLORS["neutral_baseline"], COLORS["actual_verified"]],
               edgecolor=COLORS["ink"], linewidth=0.6)
for xi, v in zip(xb, vals):
    axB.annotate(f"{v:.1f}%", (xi, v), xytext=(0, 3), textcoords="offset points",
                 ha="center", va="bottom", fontsize=11, fontweight="bold", color=COLORS["ink"])
axB.annotate("", xy=(1, 74.1), xytext=(0, 52.1),
             arrowprops=dict(arrowstyle="-|>", color=COLORS["ink"], lw=1.6,
                             connectionstyle="arc3,rad=-0.25", shrinkA=8, shrinkB=8))
axB.set_xticks(xb)
axB.set_xticklabels(labels, fontsize=9)
axB.set_ylim(-4, 100)
axB.set_xlim(-0.7, 1.7)
axB.set_ylabel("Husbandry subitem reported (%)")
axB.set_title("B  Hair2019 RCT\n(control vs intervention)", fontsize=12, loc="left", pad=10)
axB.set_ylim(-5, 106)
axB.text(0.5, 96, "Only husbandry improved;\nno manuscript reached full compliance",
         ha="center", va="top", fontsize=8.3, color=COLORS["gray_700"], style="italic")

fig.text(0.075, 0.045,
         "* Lin2024 converted to positive polarity (% average-or-better = 100 − % poor). "
         "Metrics, denominators and the exact before/after contrast differ across studies; "
         "figure shows heterogeneity, not a like-for-like effect-size pooling.",
         ha="left", fontsize=8, style="italic", color=COLORS["gray_500"])

fig.savefig(os.path.join(FIGDIR, "fig_sec8_guideline_timeline.png"),
            dpi=300, facecolor="white")
plt.close(fig)
print("saved fig_sec8_guideline_timeline.png")

#!/usr/bin/env python3
"""Stage 3b (TRUST): aggregate trust visualizations from knowledge/claim_graph.json,
rendered in the review's shared_style. Saves PNGs to figures/ (embedded as plain images
on the Trust Summary page, so no notebook/dropdown machinery is required)."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import apply_style  # noqa: E402
apply_style()

BANDS = ["high_trust", "moderate_trust", "low_trust", "critical_or_unreliable"]
BAND_LABEL = {"high_trust": "High (85-100)", "moderate_trust": "Moderate (70-84)",
              "low_trust": "Low (50-69)", "critical_or_unreliable": "Critical (<50)"}
BAND_COLOR = {"high_trust": "#009E73", "moderate_trust": "#56B4E9",
              "low_trust": "#E69F00", "critical_or_unreliable": "#D55E00"}
SEC_ORDER = ["sec-introduction", "sec-repro-crisis", "sec-data-welfare", "sec-fair-preclinical",
             "sec-virtual-controls", "sec-nams-data", "sec-incentives", "sec-governance", "sec-conclusion"]
SEC_SHORT = {"sec-introduction": "Introduction", "sec-repro-crisis": "Reproducibility",
             "sec-data-welfare": "Data welfare / 3Rs", "sec-fair-preclinical": "FAIR data",
             "sec-virtual-controls": "Virtual controls", "sec-nams-data": "NAMs",
             "sec-incentives": "Incentives", "sec-governance": "Governance", "sec-conclusion": "Conclusion"}
COMPS = ["traceability", "robustness", "uncertainty_calibration", "source_integrity", "transferability_scope_control"]
COMP_SHORT = ["Traceability", "Robustness", "Uncertainty\ncalibration", "Source\nintegrity", "Transferability\n/ scope"]
FIGDIR = os.path.join(ROOT, "figures")

claims = json.load(open("knowledge/claim_graph.json", encoding="utf-8"))["claims"]
secs = [s for s in SEC_ORDER if any(c["section_id"] == s for c in claims)]

def savefig(fig, name):
    fig.savefig(os.path.join(FIGDIR, name), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved figures/" + name)

# ---------- Figure 1: trust-band distribution per section (stacked bars) ----------
fig, ax = plt.subplots(figsize=(12, 6.5))
y = np.arange(len(secs))[::-1]
left = np.zeros(len(secs))
counts = {b: [sum(1 for c in claims if c["section_id"] == s and c["trust_score"]["trust_label"] == b) for s in secs] for b in BANDS}
for b in BANDS:
    vals = np.array(counts[b])
    ax.barh(y, vals, left=left, color=BAND_COLOR[b], label=BAND_LABEL[b], edgecolor="white", height=0.72)
    for i, v in enumerate(vals):
        if v >= 3:
            ax.text(left[i] + v / 2, y[i], str(v), va="center", ha="center", color="white", fontsize=9, fontweight="bold")
    left += vals
ax.set_yticks(y); ax.set_yticklabels([SEC_SHORT[s] for s in secs])
ax.set_xlabel("Number of cited claims")
ax.set_title("Citation TRUST by section — distribution of claim trust bands", fontweight="bold", loc="left")
ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.16), frameon=False)
ax.spines[["top", "right"]].set_visible(False)
savefig(fig, "fig_trust_by_section.png")

# ---------- Figure 2: component-mean heatmap (section x component) ----------
M = 5 * np.array([[np.mean([c["trust_score"]["components"][k]["score"] for c in claims if c["section_id"] == s]) for k in COMPS] for s in secs])
fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(M, cmap="RdYlGn", vmin=7.5, vmax=20, aspect="auto")
ax.set_xticks(range(len(COMPS))); ax.set_xticklabels(COMP_SHORT, fontsize=10)
ax.set_yticks(range(len(secs))); ax.set_yticklabels([SEC_SHORT[s] for s in secs])
for i in range(len(secs)):
    for j in range(len(COMPS)):
        ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                color="#111827" if M[i, j] >= 13 else "white", fontsize=9)
ax.set_title("Mean TRUST component points by section (0-20)", fontweight="bold", loc="left")
cb = fig.colorbar(im, ax=ax, shrink=0.8); cb.set_label("mean component points")
savefig(fig, "fig_trust_components.png")

# ---------- Figure 3: overall band donut + score histogram ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
tot = [sum(1 for c in claims if c["trust_score"]["trust_label"] == b) for b in BANDS]
wedges, _, autotexts = axes[0].pie(tot, colors=[BAND_COLOR[b] for b in BANDS], autopct=lambda p: f"{p:.0f}%" if p >= 3 else "",
                                    startangle=90, wedgeprops=dict(width=0.42, edgecolor="white"))
for t in autotexts: t.set_color("white"); t.set_fontweight("bold"); t.set_fontsize(9)
axes[0].legend([f"{BAND_LABEL[b]}  (n={tot[i]})" for i, b in enumerate(BANDS)], loc="center", frameon=False, fontsize=9)
axes[0].set_title(f"All {len(claims)} cited claims by trust band", fontweight="bold", loc="left")
scores = [c["trust_score"]["overall_score"] for c in claims]
axes[1].hist(scores, bins=range(0, 105, 5), color="#0072B2", edgecolor="white")
for x, lab, col in [(50, "low", "#E69F00"), (70, "moderate", "#56B4E9"), (85, "high", "#009E73")]:
    axes[1].axvline(x, color=col, ls="--", lw=1.2)
axes[1].set_xlabel("Overall TRUST score (0-100)"); axes[1].set_ylabel("claims")
axes[1].set_title(f"Score distribution (mean {np.mean(scores):.0f})", fontweight="bold", loc="left")
axes[1].spines[["top", "right"]].set_visible(False)
savefig(fig, "fig_trust_overall.png")
print("done: 3 trust figures")

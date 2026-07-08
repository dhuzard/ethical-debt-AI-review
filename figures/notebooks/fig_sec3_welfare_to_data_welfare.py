"""
Figure: From the 3Rs to data welfare (section 3, conceptual schematic).
=======================================================================

Type C conceptual figure. Overlays the data lifecycle on the classical 3Rs to
show precisely which stewardship acts extend which R:
  reporting + reuse            -> Reduction (fewer new animals per unit knowledge)
  FAIR stewardship + registration -> Refinement of the scientific record
  reuse of existing data + NAM outputs -> Replacement
"Data welfare" names the claim that letting animal-derived data become unusable
is itself a welfare harm. The 6R (Strech & Dirnagl 2019) and 12R (Brink & Lewis
2023) expansions are marked at the points they add.

No empirical data — this is a conceptual map. Labels only.
"""

import os
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

_here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
sys.path.insert(0, _here)
from shared_style import COLORS, apply_style, save_figure  # noqa: E402


def _find_repo_root(start):
    d = os.path.abspath(start)
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "figures")):
            return d
        d = os.path.dirname(d)
    return os.path.abspath(os.path.join(start, "..", ".."))


REPO = _find_repo_root(_here)
FIG_DIR = os.path.join(REPO, "figures")

apply_style()
fig, ax = plt.subplots(figsize=(13.0, 7.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, text, face, tcolor="white", fs=12, weight="bold", rounding=0.02):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.4,rounding_size={rounding*100}",
                       linewidth=1.0, edgecolor=COLORS["ink"], facecolor=face, zorder=3)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, fontweight=weight, color=tcolor, zorder=4)
    return (x + w / 2, y + h / 2)


def arrow(p0, p1, color, style="-|>", lw=2.0, ls="-"):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=16,
                        lw=lw, color=color, linestyle=ls, zorder=2,
                        shrinkA=6, shrinkB=6)
    ax.add_patch(a)


# ── Top band: the data lifecycle ──
ax.text(50, 96, "The data lifecycle of an animal experiment",
        ha="center", va="center", fontsize=13.5, fontweight="bold",
        color=COLORS["ink"])
stages = ["Design", "Generate\n(animals used)", "Report", "Curate / FAIR\n+ Register", "Reuse"]
sx = [3, 22, 41, 58, 79]
sw = [15, 16, 14, 19, 16]
centers = []
for name, x, w in zip(stages, sx, sw):
    face = COLORS["debt"] if name.startswith("Generate") else COLORS["actual_verified"]
    centers.append(box(x, 82, w, 9, name, face, fs=11.5))
for i in range(len(centers) - 1):
    arrow((centers[i][0] + sw[i] / 2 - 1, 86.5),
          (centers[i + 1][0] - sw[i + 1] / 2 + 1, 86.5),
          COLORS["gray_500"], lw=1.8)

# ── Central bridge band: DATA WELFARE ──
box(20, 63, 60, 8.5,
    "DATA  WELFARE\nstewardship of animal-derived data is a dimension of animal welfare",
    COLORS["emphasis_fill"], tcolor=COLORS["ink"], fs=12.5)

# ── Bottom: the three Rs as lanes ──
r_boxes = {
    "Reduction": box(3, 40, 27, 11,
                     "REDUCTION\nfewer new animals\nper unit of knowledge",
                     COLORS["repayment"], fs=12),
    "Refinement": box(36.5, 40, 27, 11,
                      "REFINEMENT\nof the scientific record\n(complete, findable, honest)",
                      COLORS["actual_verified"], fs=12),
    "Replacement": box(70, 40, 27, 11,
                       "REPLACEMENT\nexisting data & NAM\noutputs substitute animals",
                       COLORS["secondary_cat"], fs=12),
}

# stewardship-act -> R mappings (which lifecycle act extends which R)
acts = [
    (16.5, 25, "Complete reporting\n+ data reuse", COLORS["repayment"], "Reduction"),
    (50, 25, "FAIR curation\n+ registration", COLORS["actual_verified"], "Refinement"),
    (83.5, 25, "Reuse of prior data\n+ NAM outputs", COLORS["secondary_cat"], "Replacement"),
]
for x, y, txt, col, r in acts:
    c = box(x - 12, y - 5, 24, 9.5, txt, "white", tcolor=COLORS["ink"], fs=11, weight="normal")
    arrow((c[0], y + 4.75), (r_boxes[r][0], 40), col, lw=2.2)

# ── expansion markers: 6R and 12R (short, non-crossing) ──
ax.annotate("6R (Strech & Dirnagl 2019):\n+ Robustness, Registration, Reporting",
            xy=(centers[2][0], 82), xytext=(15, 75.5),
            fontsize=9.5, color=COLORS["conflict"], fontweight="bold",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=COLORS["conflict"], lw=1.4))
ax.annotate("12R (Brink & Lewis 2023):\nwelfare + social-value + scientific-integrity Rs",
            xy=(74, 71.5), xytext=(62, 75.5),
            fontsize=9.5, color=COLORS["conflict"], fontweight="bold",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=COLORS["conflict"], lw=1.4))

ax.text(50, 6.5,
        "Wasting the data wastes the welfare cost that produced it — so data stewardship is a 3Rs obligation.",
        ha="center", va="center", fontsize=11.5, style="italic", color=COLORS["ink"])

fig.tight_layout()
os.makedirs(FIG_DIR, exist_ok=True)
save_figure(fig, os.path.join(FIG_DIR, "fig_sec3_welfare_to_data_welfare.png"))
print("saved:", os.path.join(FIG_DIR, "fig_sec3_welfare_to_data_welfare.png"))

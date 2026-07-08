# %% [markdown]
# # Declared versus actual open data under sharing policies (Section 7)
#
# **Data source:** `evidence/evidence_section_07.json` -> figure_data comparison
# `declared-vs-actual-open-data`.
#
# **What it shows:** stated intent to share data vastly exceeds usable public data.
# Bars are grouped by construct (declared vs actually available).
#
# **Caveats (verbatim in caption):** label each bar by availability stage
# (Major2025 = data-sharing statement present, 14%; Danchev2021 = declared 68.6%
# vs actually available 0.6%; Hardwicke2021 = raw data actually shared 2%).
# Statement-presence and actual-sharing are different constructs; fields differ
# (clinical trials, psychology, orthopaedics). The orthopaedic statement-presence
# point (Major2025, DOI 10.2106/JBJS.24.00955, 14%) is OMITTED from the plot
# because it has no canonical citation key in this review's bibliography.

# %%
import os
import re
import sys
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "evidence", "evidence_section_07.json")):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("repo root not found")


ROOT = find_root(os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "figures", "notebooks"))
from shared_style import COLORS, apply_style, save_figure

apply_style()
EV = json.load(open(os.path.join(ROOT, "evidence", "evidence_section_07.json"), encoding="utf-8"))
FD = {c["comparison_id"]: c for c in EV["figure_data"]}
FIGDIR = os.path.join(ROOT, "figures")

# %%
comp = FD["declared-vs-actual-open-data"]
papers = {p["doi"]: p for p in comp["papers"]}

# Danchev2021: "68.6 declared / 0.6 actual"
dv = re.findall(r"[\d.]+", papers["10.1001/jamanetworkopen.2020.33972"]["value"])
danchev_declared, danchev_actual = float(dv[0]), float(dv[1])
# Hardwicke2021: raw data actually shared "2"
hardwicke_actual = float(re.findall(r"[\d.]+", papers["10.1177/1745691620979806"]["value"])[0])
# Major2025 (10.2106/JBJS.24.00955): 14% -- no canonical cite key -> dropped from plot
DROPPED = ("10.2106/JBJS.24.00955" in papers)

# (label, value, construct, kind)  kind in {"declared", "actual"}
bars = [
    ("Danchev et al. 2021\nclinical trials", danchev_declared, "Declared", "declared"),
    ("Danchev et al. 2021\nclinical trials", danchev_actual, "Actually\navailable", "actual"),
    ("Hardwicke et al. 2021\npsychology", hardwicke_actual, "Actually\navailable", "actual"),
]

# %%
kind_style = {
    "declared": dict(color=COLORS["declared_nominal"], hatch="////", label="Declared / stated intent"),
    "actual":   dict(color=COLORS["actual_verified"], hatch="",     label="Actually available / usable"),
}

fig, ax = plt.subplots(figsize=(10.5, 6.0))
fig.subplots_adjust(left=0.10, right=0.965, bottom=0.22, top=0.88)

x = np.arange(len(bars))
for xi, (label, val, construct, kind) in zip(x, bars):
    st = kind_style[kind]
    ax.bar(xi, val, width=0.62, color=st["color"], edgecolor=COLORS["ink"],
           linewidth=0.7, hatch=st["hatch"], zorder=3)
    ax.annotate(f"{val:g}%", (xi, val), xytext=(0, 5), textcoords="offset points",
                va="bottom", ha="center", fontsize=12, fontweight="bold", color=COLORS["ink"])

# Emphasise the declared -> actual collapse for Danchev
ax.annotate("", xy=(1, danchev_actual + 4), xytext=(0, danchev_declared - 2),
            arrowprops=dict(arrowstyle="->", color=COLORS["debt"], lw=1.8,
                            connectionstyle="arc3,rad=-0.25"), zorder=4)
ax.text(0.5, danchev_declared * 0.62,
        "declared 68.6%\n-> 0.6% actual", ha="center", va="center",
        fontsize=9.5, color=COLORS["debt"], fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([b[0] for b in bars], fontsize=9.5)
# construct labels as a secondary annotation row
for xi, (_, _, construct, _) in zip(x, bars):
    ax.annotate(construct, (xi, -0.5), xytext=(0, -34), textcoords="offset points",
                ha="center", va="top", fontsize=9, color=COLORS["gray_700"],
                annotation_clip=False)
ax.set_ylim(0, 78)
ax.set_ylabel("Data availability (% of articles)", labelpad=6)
ax.set_title("Declared intent is not usable data", pad=12, fontsize=15)

handles = [mpatches.Patch(facecolor=kind_style[k]["color"], edgecolor=COLORS["ink"],
                          hatch=kind_style[k]["hatch"], label=kind_style[k]["label"])
           for k in ("declared", "actual")]
ax.legend(handles=handles, loc="upper right", fontsize=10, framealpha=0.95)

note = ("Statement-presence construct omitted: Major2025 (orthopaedics, 14%) "
        "has no canonical citation key and is not plotted." if DROPPED else "")
fig.text(0.5, 0.045, note + "  Constructs differ across fields (see caption).",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_declared_vs_actual.png"))
print("saved fig_sec7_declared_vs_actual.png:", danchev_declared, danchev_actual, hardwicke_actual, "dropped:", DROPPED)

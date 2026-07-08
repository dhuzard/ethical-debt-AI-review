# %% [markdown]
# # What researcher-evaluation systems reward (Section 7)
#
# **Data source:** `evidence/evidence_section_07.json` -> figure_data comparison
# `rpt-evaluation-criteria`, cross-checked against the Rice2020 and McKiernan2019
# findings in the same file.
#
# **What it shows:** prevalence of criteria in formal review, promotion and tenure
# (RPT) documents. Traditional publication/impact criteria dominate; open-science
# criteria (data sharing) are almost never mentioned.
#
# **Caveats (verbatim in caption):** bars are prevalence of different RPT criteria
# across different populations (Rice2020 = 92 international biomedical-faculty
# guidelines; McKiernan2019 = research-intensive US/Canada universities only, 18%
# master's, 0% baccalaureate). 95% = any mention of peer-reviewed publications;
# 35% = mention of a specific publication count (a separate figure). Each bar is
# labelled by its population/definition; no single population is implied.

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
FIND = {f["cite_key"]: f for f in EV["findings"]}
FIGDIR = os.path.join(ROOT, "figures")

# %%
comp = FD["rpt-evaluation-criteria"]
papers = {p["doi"]: p for p in comp["papers"]}

# Rice2020 combined "95 / 1" -> publication-mention 95, data-sharing 1
rice_vals = re.findall(r"[\d.]+", papers["10.1136/bmj.m2081"]["value"])
rice_pub, rice_data = float(rice_vals[0]), float(rice_vals[1])
# McKiernan2019 "40" -> JIF mention among research-intensive institutions
mck_jif = float(re.findall(r"[\d.]+", papers["10.7554/elife.47338"]["value"])[0])
# Specific publication-count requirement (35%): from the Rice2020 finding effect_size
rice_count = float(re.search(r"(\d+)% require a specific number", FIND["Rice2020"]["effect_size"]).group(1))

# Each bar: (label, value, category)  category in {"traditional", "open"}
bars = [
    ("Peer-reviewed publication mention\n(Rice et al. 2020; 92 intl. biomedical guidelines)", rice_pub, "traditional"),
    ("Journal Impact Factor use\n(McKiernan et al. 2019; research-intensive only)", mck_jif, "traditional"),
    ("Specific publication-count requirement\n(Rice et al. 2020)", rice_count, "traditional"),
    ("Data-sharing mention\n(Rice et al. 2020)", rice_data, "open"),
]

# %%
cat_style = {
    "traditional": dict(color=COLORS["neutral_baseline"], hatch="", label="Traditional publication / impact criteria"),
    "open":        dict(color=COLORS["repayment"], hatch="////", label="Open-science criteria (data sharing)"),
}

fig, ax = plt.subplots(figsize=(11, 5.6))
fig.subplots_adjust(left=0.42, right=0.965, bottom=0.20, top=0.90)

y = np.arange(len(bars))[::-1]  # first bar at top
for yi, (label, val, cat) in zip(y, bars):
    st = cat_style[cat]
    ax.barh(yi, val, height=0.62, color=st["color"], edgecolor=COLORS["ink"],
            linewidth=0.7, hatch=st["hatch"], zorder=3)
    ax.annotate(f"{val:g}%", (val, yi), xytext=(6, 0), textcoords="offset points",
                va="center", ha="left", fontsize=12, fontweight="bold", color=COLORS["ink"])

# Annotate the McKiernan bar with the population breakdown
mck_y = y[1]
ax.annotate("R-type universities only; 18% master's, 0% baccalaureate",
            (mck_jif, mck_y), xytext=(46, -14), textcoords="offset points",
            va="center", ha="left", fontsize=9, style="italic", color=COLORS["gray_700"])

ax.set_yticks(y)
ax.set_yticklabels([b[0] for b in bars], fontsize=10)
ax.set_xlim(0, 108)
ax.set_xlabel("Institutions whose RPT documents mention the criterion (%)", labelpad=6)
ax.set_title("What researcher-evaluation systems reward", pad=12, fontsize=15)
ax.spines["left"].set_visible(True)

handles = [mpatches.Patch(facecolor=cat_style[c]["color"], edgecolor=COLORS["ink"],
                          hatch=cat_style[c]["hatch"], label=cat_style[c]["label"])
           for c in ("traditional", "open")]
ax.legend(handles=handles, loc="lower right", fontsize=10, framealpha=0.95)

fig.text(0.5, 0.035,
         "Bars span different populations and definitions (see caption). "
         "All values extracted from the source papers' full text.",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_rpt_criteria.png"))
print("saved fig_sec7_rpt_criteria.png:", [b[1] for b in bars])

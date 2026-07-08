# %% [markdown]
# # Questionable-practice prevalence depends on what is counted (Section 7)
#
# **Data source:** `evidence/evidence_section_07.json` -> figure_data comparison
# `qrp-prevalence-surveys`, plus the Fanelli2009 finding for the ~34% any-QRP
# comparator.
#
# **Restructure (mandatory):** a BEHAVIOUR-PREVALENCE panel (Fanelli serious FFP
# 1.97%; Schneider any-of-nine-QRP 94%; Fanelli's own ~34% any-QRP marked as the
# closer comparator to Schneider) is kept separate from an ATTITUDINAL panel
# (Velicu ~20% = implicit association of QRPs with success on an SC-IAT, NOT a
# self-reported behaviour).
#
# **Caveat (verbatim in caption):** the 2-to-94 spread is a severity/breadth
# artefact, not a like-for-like prevalence.

# %%
import os
import re
import sys
import json

import numpy as np
import matplotlib.pyplot as plt


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
comp = FD["qrp-prevalence-surveys"]
papers = {p["doi"]: p for p in comp["papers"]}

fanelli_ffp = float(re.findall(r"[\d.]+", papers["10.1371/journal.pone.0005738"]["value"])[0])  # 1.97
schneider_any = float(re.findall(r"[\d.]+", papers["10.1371/journal.pone.0304342"]["value"])[0])  # 94
velicu_attitude = float(re.findall(r"[\d.]+", papers["10.1007/s11192-025-05357-4"]["value"])[0])  # ~20
# Fanelli's own ~34% any-QRP (closer comparator to Schneider): from the Fanelli2009 finding text
fanelli_anyqrp = float(re.search(r"~?(\d+)%\s*admit other QRPs", FIND["Fanelli2009"]["evidence"]).group(1))  # 34

# %%
fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 5.8),
                               gridspec_kw={"width_ratios": [2.2, 1.0], "wspace": 0.32})
fig.subplots_adjust(left=0.09, right=0.975, bottom=0.20, top=0.84)

# --- Left panel: behaviour prevalence (self-admitted) ---
bx = [0, 1]
bvals = [fanelli_ffp, schneider_any]
bcolors = [COLORS["debt"], COLORS["conflict"]]
bhatch = ["", "xxxx"]
blabels = ["Fanelli 2009\nserious FFP\n(fabrication/\nfalsification)", "Schneider et al. 2024\nany of nine QRPs\n(used at least once)"]
for xi, val, col, h in zip(bx, bvals, bcolors, bhatch):
    axL.bar(xi, val, width=0.6, color=col, edgecolor=COLORS["ink"], linewidth=0.7, hatch=h, zorder=3)
    axL.annotate(f"{val:g}%", (xi, val), xytext=(0, 5), textcoords="offset points",
                 ha="center", va="bottom", fontsize=13, fontweight="bold", color=COLORS["ink"])
# Fanelli's own ~34% any-QRP as the closer comparator to Schneider
axL.axhline(fanelli_anyqrp, color=COLORS["gray_700"], lw=1.4, ls="--", zorder=2)
axL.text(-0.55, fanelli_anyqrp + 2.5,
         f"Fanelli 2009 any-QRP ~{fanelli_anyqrp:g}%\n(closer comparator to Schneider)",
         ha="left", va="bottom", fontsize=9, style="italic", color=COLORS["gray_700"])
axL.set_xticks(bx)
axL.set_xticklabels(blabels, fontsize=10)
axL.set_xlim(-0.6, 1.6)
axL.set_ylim(0, 104)
axL.set_ylabel("Scientists self-admitting (%)", labelpad=6)
axL.set_title("Behaviour prevalence (self-admitted)", pad=10, fontsize=13)

# --- Right panel: attitudinal (implicit association) ---
axR.bar(0, velicu_attitude, width=0.55, color=COLORS["secondary_cat"],
        edgecolor=COLORS["ink"], linewidth=0.7, hatch="....", zorder=3)
axR.annotate(f"~{velicu_attitude:g}%", (0, velicu_attitude), xytext=(0, 5),
             textcoords="offset points", ha="center", va="bottom",
             fontsize=13, fontweight="bold", color=COLORS["ink"])
axR.set_xticks([0])
axR.set_xticklabels(["Velicu et al. 2025\nimplicitly associate\nQRPs with success (SC-IAT)"], fontsize=10)
axR.set_xlim(-0.7, 0.7)
axR.set_ylim(0, 104)
axR.set_ylabel("Scientists (implicit association, %)", labelpad=6)
axR.set_title("Attitude (implicit association)", pad=10, fontsize=13)

fig.suptitle("Questionable-practice prevalence depends on what is counted", fontsize=15, y=0.97)
fig.text(0.5, 0.035,
         "Not a like-for-like comparison: severity (serious FFP) vs breadth (any QRP) vs an implicit "
         "attitude, not a behaviour. The 2-to-94 spread is a severity/breadth artefact.",
         ha="center", fontsize=9, style="italic", color=COLORS["gray_500"])

save_figure(fig, os.path.join(FIGDIR, "fig_sec7_qrp_prevalence.png"))
print("saved fig_sec7_qrp_prevalence.png:", fanelli_ffp, schneider_any, velicu_attitude, "any-QRP", fanelli_anyqrp)

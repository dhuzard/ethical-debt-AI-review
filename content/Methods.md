(sec-methods)=
# Methods

:::{figure} ../figures/fig_methods_pipeline.png
:name: fig-methods-pipeline
:width: 100%

Overview of the 21-phase Expert Review Pipeline v29. Green boxes indicate LITREVIEW agents (scientific judgment), blue boxes indicate DATAML agents (mechanical work), and the gray box is the coordinator. Red dashed lines mark information barriers where actor-critic separation is enforced. Orange diamonds indicate gate checkpoints where the coordinator verifies compliance before advancing. Phase 21 (Deploy Polish) is the post-deployment UX gate that runs after the Phase 20 push to `main` confirms a green build.
:::

:::{dropdown} 📓 Figure code

```python
"""
Figure: Methods Pipeline (swim-lane diagram with explicit execution sequence)
============================================================================

Renders the 21-phase ComputationalReview pipeline as a swim-lane diagram,
faithfully reproducing the actor/critic/validator separation defined in
skills/comprev-orchestrator-v29.md (Phase Index).  An explicit numbered
arrow snake traces the actual execution order (34 steps), and a step-number
badge in each box's corner identifies its position in that sequence.

Lanes (top to bottom):
  - Coordinator   -- routing across phases; gates between phases (dotted rail)
  - DATAML agent  -- mechanical actors (upper sub-row) + validators (lower sub-row)
  - LITREVIEW agent -- scientific actors and blinded critics

Element types (per Phase Index):
  - ACTOR boxes    -- solid coloured by lane (DATAML blue / LITREVIEW orange)
  - CRITIC boxes   -- LITREVIEW phases with an information barrier from the actor;
                      dashed border + diagonal hatch.  Phases 6, 8, 12, 16.
  - VALIDATOR boxes -- DATAML phases that re-check an actor's output, with the same
                       information barrier from the actor; dashed border + diagonal
                       hatch.  Phases 1V, 2V, 3V, 5V, 7V, 9V, 14V, 15V, 17V, 19V, 20V,
                       and Phase 21 (deploy-polish validator, no separate actor).

Critics and validators share the same visual convention -- they are the two
flavours of info-barriered reviewer (scientific vs mechanical); lane colour
distinguishes which.

Special cases:
  - Phase 1 has TWO actors (LITREVIEW scoping + DATAML materialise) at the
    same x, stacked across lanes.  They run in parallel; the snake visits
    LITREVIEW first then DATAML for diagram clarity.
  - Phase 20a (Methods Ledger Refresh) runs between Phases 19V and 20.
  - Phase 21 (Deploy Polish) has no separate actor; its frame is both actor
    and validator, reading the deployed Pages artifact.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, FancyArrowPatch

# Axes aspect ratio (inches-per-data-unit_y / inches-per-data-unit_x) — used
# to render visually-circular badges as Ellipses in data coordinates.
# figsize=(24, 9.6); subplots_adjust left=0.02, right=0.99, bottom=0.14, top=0.94
# axes width in  = 24  * (0.99 - 0.02) = 23.28
# axes height in =  9.6 * (0.94 - 0.14) =  7.68
# xspan = 24 - (-3.4) = 27.4 ; yspan = 6.0 - (-0.6) = 6.6
# ipdu_x = 23.28/27.4 = 0.8496 ; ipdu_y = 7.68/6.6 = 1.1636
# ASPECT = ipdu_y / ipdu_x ≈ 1.37
ASPECT = 1.37

def badge(x, y, r=0.18):
    """Visually-circular step-number badge (Ellipse compensating axes aspect)."""
    return Ellipse((x, y), width=2 * r * ASPECT, height=2 * r,
                   facecolor=BADGE_FILL, edgecolor="white",
                   linewidth=1.0, zorder=6)

# ---------------------------------------------------------------------------
# Authoritative phase table -- (x_slot, label, role, kind, displayed_phase_id)
# ---------------------------------------------------------------------------
# Last element: True if this phase fans out into multiple parallel sub-agents
# (one per cluster, per section, per batch, ...).  Single-agent phases = False.
# Parallel-fanout phases per skills/comprev-orchestrator-v29.md and the
# fan-out structure of each phase's worker skill.
ACTORS = [
    ( 1, "Scope",                  "expert", "actor",  "1",   False),
    ( 1, "Materialise",            "dataml", "actor",  "1",   False),
    ( 2, "Evidence\nGathering",    "expert", "actor",  "2",   True ),   # per cluster (≤4 parallel, batched)
    ( 3, "Citation\nInfra",        "dataml", "actor",  "3",   False),
    ( 4, "Scaffold",               "expert", "actor",  "4",   False),
    ( 5, "Evidence\nCuration",     "dataml", "actor",  "5",   False),
    ( 6, "Figure\nAudit",          "expert", "critic", "6",   True ),   # per comparison batch
    ( 7, "Section\nDrafting",      "expert", "actor",  "7",   True ),   # per section (≤4 parallel, batched)
    ( 8, "Section\nCritics",       "expert", "critic", "8",   True ),   # per section
    ( 9, "Biblio-\ngraphy",        "dataml", "actor",  "9",   False),
    (10, "Integration",            "expert", "actor",  "10",  False),
    (11, "Intro /\nConclusion",    "expert", "actor",  "11",  False),
    (12, "Bookend\nCritic",        "expert", "critic", "12",  True ),   # per bookend (intro + conclusion)
    (13, "Methods",                "dataml", "actor",  "13",  False),
    (14, "Document\nAssembly",     "dataml", "actor",  "14",  False),
    (15, "Citation\nTriples",      "dataml", "actor",  "15",  False),
    (16, "Citation\nCheck",        "expert", "critic", "16",  True ),   # per batch (≤4 parallel, multi-wave)
    (17, "Fix\nPreparation",       "dataml", "actor",  "17",  False),
    (18, "Fix\nExecution",         "expert", "actor",  "18",  True ),   # per section with fixes
    (19, "Fix\nApplication",       "dataml", "actor",  "19",  False),
    (20, "Methods\nLedger\nRefresh","dataml","actor",  "20a", False),
    (21, "Repository\nPush",       "dataml", "actor",  "20",  False),
]

VALIDATORS = [
    ( 1, "1V" ),
    ( 2, "2V" ),
    ( 3, "3V" ),
    ( 5, "5V" ),
    ( 7, "7V" ),
    ( 9, "9V" ),
    (14, "14V"),
    (15, "15V"),
    (17, "17V"),
    (19, "19V"),
    (21, "20V"),
    (22.4, "Deploy\nPolish (21)"),
]

# Execution order: (x_slot, lane_key) -> step number (1-indexed).  This drives
# both the arrow path and the corner badges.
EXEC_SEQUENCE = [
    ( 1, "expert"),       ( 1, "dataml_actor"), ( 1, "dataml_val"),
    ( 2, "expert"),       ( 2, "dataml_val"),
    ( 3, "dataml_actor"), ( 3, "dataml_val"),
    ( 4, "expert"),
    ( 5, "dataml_actor"), ( 5, "dataml_val"),
    ( 6, "expert"),
    ( 7, "expert"),       ( 7, "dataml_val"),
    ( 8, "expert"),
    ( 9, "dataml_actor"), ( 9, "dataml_val"),
    (10, "expert"),
    (11, "expert"),
    (12, "expert"),
    (13, "dataml_actor"),
    (14, "dataml_actor"),(14, "dataml_val"),
    (15, "dataml_actor"),(15, "dataml_val"),
    (16, "expert"),
    (17, "dataml_actor"),(17, "dataml_val"),
    (18, "expert"),
    (19, "dataml_actor"),(19, "dataml_val"),
    (20, "dataml_actor"),
    (21, "dataml_actor"),(21, "dataml_val"),
    (22.4, "dataml_val"),
]
STEP_OF = {pos: i + 1 for i, pos in enumerate(EXEC_SEQUENCE)}

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
EDGE = {"coord": "#2e7d32", "dataml": "#1565c0", "expert": "#e65100"}
FILL = {"coord": "#c8e6c9", "dataml": "#bbdefb", "expert": "#ffe0b2"}
VALIDATOR_FILL = "#e3f2fd"
CRITIC_EDGE = "#6a1b9a"
DASH = (0, (4, 2))

# Reviewer "stamp" --- a solid color bar across the top of critic/validator
# boxes, replacing the harder-to-read diagonal hatch.  Each colour matches
# its reviewer family.
STAMP_HEIGHT_FRAC = 0.22    # fraction of box height occupied by the top bar
ARROW_COLOR = "#37474f"   # charcoal -- darker than before for visibility
BADGE_FILL = "#263238"
BADGE_TEXT = "white"

LANE_Y = {"coord": 4.85, "dataml_actor": 2.85, "dataml_val": 1.65, "expert": 0.1}
LANE_LABEL = {
    "coord":  "ORCHESTRATOR",
    "dataml": "DATAML AGENT",
    "expert": "LITREVIEW AGENT",
}
# Lane backgrounds: equal-size gaps between all three lanes.
# Gates now live INSIDE the orchestrator lane (vertical dashes in the
# green band), so the orchestrator-DATAML gap can equal the DATAML-expert
# gap.  LITREVIEW lane is enlarged downward so the parallel-fanout
# shadow stacks (offset -0.12 below box bottom) stay inside the orange
# background.
GAP = 0.30
COORD_LANE_TOP     = 5.45
COORD_LANE_BOTTOM  = 4.20   # thinner band; gates fill most of the height
DATAML_LANE_TOP    = COORD_LANE_BOTTOM - GAP   # 3.90
DATAML_LANE_BOTTOM = 1.10
EXPERT_LANE_TOP    = DATAML_LANE_BOTTOM - GAP  # 0.80
EXPERT_LANE_BOTTOM = -0.60                     # contains shadow stacks
DATAML_LANE_CENTER = (DATAML_LANE_TOP + DATAML_LANE_BOTTOM) / 2

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(24, 9.6))
ax.set_xlim(-3.4, 24.0)
ax.set_ylim(-0.85, 6.0)
ax.axis("off")

box_w, box_h = 0.82, 0.92

# Lane backgrounds
ax.add_patch(FancyBboxPatch(
    (-2.6, COORD_LANE_BOTTOM), 26.4, COORD_LANE_TOP - COORD_LANE_BOTTOM,
    boxstyle="round,pad=0.02",
    facecolor=FILL["coord"], edgecolor="none", alpha=0.20, zorder=0,
))
ax.text(-2.5, (COORD_LANE_TOP + COORD_LANE_BOTTOM) / 2, LANE_LABEL["coord"],
        ha="left", va="center", fontsize=11.5, weight="bold",
        color=EDGE["coord"], zorder=1)

ax.add_patch(FancyBboxPatch(
    (-2.6, DATAML_LANE_BOTTOM), 26.4, DATAML_LANE_TOP - DATAML_LANE_BOTTOM,
    boxstyle="round,pad=0.02",
    facecolor=FILL["dataml"], edgecolor="none", alpha=0.20, zorder=0,
))
ax.text(-2.5, DATAML_LANE_CENTER, LANE_LABEL["dataml"],
        ha="left", va="center", fontsize=11.5, weight="bold",
        color=EDGE["dataml"], zorder=1)

ax.add_patch(FancyBboxPatch(
    (-2.6, EXPERT_LANE_BOTTOM), 26.4, EXPERT_LANE_TOP - EXPERT_LANE_BOTTOM,
    boxstyle="round,pad=0.02",
    facecolor=FILL["expert"], edgecolor="none", alpha=0.20, zorder=0,
))
ax.text(-2.5, (EXPERT_LANE_TOP + EXPERT_LANE_BOTTOM) / 2, LANE_LABEL["expert"],
        ha="left", va="center", fontsize=11.5, weight="bold",
        color=EDGE["expert"], zorder=1)

# Orchestrator step-0 entry box: prompt capture + plan generation.
# Per comprev-orchestrator-v29.md ("Before generate_plan, the coordinator
# runs Phase 1 to produce the scope and plan content").
ORCH_X = -0.05  # left of the gate rail (which starts at x=0.5)
ORCH_W, ORCH_H = 1.05, 0.92
ax.add_patch(FancyBboxPatch(
    (ORCH_X - ORCH_W/2, LANE_Y["coord"] - ORCH_H/2), ORCH_W, ORCH_H,
    boxstyle="round,pad=0.04",
    facecolor=FILL["coord"], edgecolor=EDGE["coord"], linewidth=1.8,
    zorder=3,
))
ax.text(ORCH_X, LANE_Y["coord"], "Prompt\n+ plan",
        ha="center", va="center", fontsize=9.5, zorder=5)
ax.text(ORCH_X, LANE_Y["coord"] + ORCH_H/2 + 0.10, "0",
        ha="center", va="bottom", fontsize=10.5, weight="bold",
        color=EDGE["coord"], zorder=4)
# (step badge removed -- per user request, declutter by dropping all
#  black-circle numeric step badges; the lane structure + phase numbers
#  already convey order.)

# Gates: each phase has a thick dashed vertical "gate" pin sitting INSIDE
# the lower half of the orchestrator green lane.  The orchestrator box
# sits in the upper half; the gates row sits below it inside the same
# green band.  "Gates" header label is rendered in the same column to the
# right of x=21.
GATE_COLOR = EDGE["coord"]                          # green
# Orch box and gates live in the same orchestrator green lane but at
# different x-positions (orch at x=-0.05, gates at x=1..21) so they do
# not overlap.  Gates span MOST of the lane height (4.20..5.45) for
# strong visual presence.
GATE_TOP    = COORD_LANE_TOP    - 0.05      # 5.40
GATE_BOTTOM = COORD_LANE_BOTTOM + 0.05      # 4.25
GATE_BAND_CENTER = (GATE_TOP + GATE_BOTTOM) / 2
ax.text(22.7, GATE_BAND_CENTER, "Gates",
        ha="left", va="center", fontsize=12, weight="bold",
        color=GATE_COLOR, zorder=4)

# Arrow from Orchestrator down through the left margin to Phase 1 Scope.
# A wide leftward-bulging curve (rad=-0.45) keeps the arrow well clear of
# the x=1 column where Materialise / 1V sit stacked.  ORCH_X = -0.65 puts
# the orchestrator box left of the gate rail (which starts at x=0.5), so
# the arrow's natural path runs through empty left-margin space.
ax.add_patch(FancyArrowPatch(
    (ORCH_X, LANE_Y["coord"] - ORCH_H/2 - 0.02),
    (1 - box_w/2 - 0.08, LANE_Y["expert"]),
    connectionstyle="arc3,rad=0.18",
    arrowstyle="->", mutation_scale=14,
    linewidth=2.2, color=ARROW_COLOR, alpha=0.95, zorder=10,
))

# ---------------------------------------------------------------------------
# Snake the execution-order arrows.  Use FancyArrowPatch with explicit
# data-coordinate endpoints offset by box-half-size (works regardless of dpi).
# Drawn first so boxes overlay arrowheads at the box edges.
# ---------------------------------------------------------------------------
from matplotlib.patches import FancyArrowPatch

HALF_W = box_w / 2  # 0.41
HALF_H = box_h / 2  # 0.46
ARROW_GAP = 0.03    # extra clearance outside box edge for arrowhead

def _edge_dist(dx, dy):
    """Distance from box center along direction (dx,dy) to box rectangle edge."""
    if abs(dx) < 1e-9:
        return HALF_H
    if abs(dy) < 1e-9:
        return HALF_W
    # parametric t such that max(|t*dx|/HW, |t*dy|/HH) = 1
    t = min(HALF_W / abs(dx), HALF_H / abs(dy))
    return t * (dx * dx + dy * dy) ** 0.5

def arrow(x1, y1, x2, y2, rad=0.0, lw=1.6, color=ARROW_COLOR, alpha=0.95,
          zorder=2.5):
    """Arrow whose endpoints land at the rectangular box edges (with small gap)."""
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5
    if dist < 1e-6:
        return
    ux, uy = dx / dist, dy / dist
    out_a = _edge_dist(dx, dy) + ARROW_GAP
    out_b = _edge_dist(-dx, -dy) + ARROW_GAP
    if out_a + out_b >= dist - 0.02:
        return  # boxes adjacent / overlapping; no visible space
    sx1, sy1 = x1 + ux * out_a, y1 + uy * out_a
    sx2, sy2 = x2 - ux * out_b, y2 - uy * out_b
    ax.add_patch(FancyArrowPatch(
        (sx1, sy1), (sx2, sy2),
        arrowstyle="->", mutation_scale=12,
        linewidth=lw, color=color, alpha=alpha,
        connectionstyle=f"arc3,rad={rad}",
        zorder=zorder,
    ))

for i in range(len(EXEC_SEQUENCE) - 1):
    x1, lane1 = EXEC_SEQUENCE[i]
    x2, lane2 = EXEC_SEQUENCE[i + 1]
    y1, y2 = LANE_Y[lane1], LANE_Y[lane2]
    same_x = abs(x2 - x1) < 0.05
    if same_x and lane1 != lane2:
        # Same-x cross-lane arrow.
        # Within DATAML lane (actor <-> validator) -> straight vertical.
        # Between LITREVIEW and DATAML (e.g. Phase 1 Scope -> Materialise
        # per the orchestrator skill: Scope outputs scope.json which the
        # DATAML materialiser consumes) -> offset slightly to the LEFT so
        # it does not visually overlap with the same-column actor <->
        # validator arrow inside DATAML.
        if lane1.startswith("dataml") and lane2.startswith("dataml"):
            arrow(x1, y1, x2, y2, rad=0.0, lw=1.6)
        else:
            # Cross-lane Scope -> Materialise: bow hard LEFT (rad < 0 for
            # an upward arrow) so the arc sits to the LEFT of the 1V
            # validator column (which lives in the same x).  zorder=4
            # puts it ABOVE box fills (z=3) but below labels (z=5).
            crad = -0.85 if y2 > y1 else 0.85
            arrow(x1, y1, x2, y2, rad=crad, lw=1.8,
                  color="#546e7a", zorder=4)
    elif lane1 == lane2:
        # Same-lane horizontal step between adjacent boxes.
        arrow(x1, y1, x2, y2, rad=0.0, lw=1.6)
    else:
        # Lane-changing diagonal.  Curve more aggressively so the arc
        # doesn't clip the corner of intermediate boxes.  Sign rule:
        # downward diagonal -> bulge UP (positive rad); upward -> bulge
        # DOWN.  Magnitude bumped 0.22 -> 0.35 to clear corner overlap.
        rad = 0.35 if y2 < y1 else -0.35
        arrow(x1, y1, x2, y2, rad=rad, lw=1.8)

# ---------------------------------------------------------------------------
# Helper: draw a phase box, then stamp a step-number badge on the corner
# ---------------------------------------------------------------------------
def draw_box(x, y, label, role, kind, displayed_num=None, step=None, parallel=False):
    if kind == "critic":
        ec, lw, ls, weight = CRITIC_EDGE, 1.8, "-", "bold"
        fc = FILL[role]
        stamp_color = CRITIC_EDGE
    elif kind == "validator":
        ec, lw, ls, weight = EDGE["dataml"], 1.5, "-", "regular"
        fc = VALIDATOR_FILL
        stamp_color = EDGE["dataml"]
    else:
        ec, lw, ls, weight = EDGE[role], 1.5, "-", "regular"
        fc = FILL[role]
        stamp_color = None

    # Parallel-fanout marker: draw two offset shadow copies behind the main
    # box, signalling "multiple sub-agents run this phase concurrently".
    if parallel:
        for dx, dy in [(0.18, -0.12), (0.10, -0.06)]:
            ax.add_patch(FancyBboxPatch(
                (x - box_w/2 + dx, y - box_h/2 + dy), box_w, box_h,
                boxstyle="round,pad=0.03",
                facecolor=fc, edgecolor=ec, linewidth=lw * 0.7,
                linestyle=ls, alpha=0.85,
                zorder=2,
            ))

    # Background box (filled lane colour)
    ax.add_patch(FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.03",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls,
        zorder=3,
    ))
    # Reviewer "stamp" -- solid colour bar across the top of the box,
    # readable at distance, replacing the diagonal hatch.
    if stamp_color is not None:
        stamp_h = box_h * STAMP_HEIGHT_FRAC
        ax.add_patch(FancyBboxPatch(
            (x - box_w/2 + 0.03, y + box_h/2 - stamp_h - 0.01),
            box_w - 0.06, stamp_h,
            boxstyle="round,pad=0.005",
            facecolor=stamp_color, edgecolor="none",
            zorder=4,
        ))
    # Label text -- slightly below centre so the stamp doesn't overlap
    label_y_offset = -0.04 if stamp_color else 0.0
    ax.text(x, y + label_y_offset, label, ha="center", va="center",
            fontsize=9.5, zorder=5, weight=weight)
    if displayed_num is not None:
        # Phase number INSIDE the box, upper-left corner (above the label
        # text).  Previously floated above the box but cross-lane vertical
        # arrows that land on the top edge sat over the number; placing it
        # inside the box keeps it clear of the arrowhead landing zone.
        # For critic/validator boxes that have a top stamp band, the
        # corner is over the stamp -- use white text in that case.
        col = "white" if stamp_color is not None else EDGE.get(
            "dataml" if kind == "validator" else role, EDGE[role])
        ax.text(x - box_w/2 + 0.06, y + box_h/2 - 0.06, displayed_num,
                ha="left", va="top", fontsize=9.5, weight="bold",
                color=col, zorder=6)
    # (Black-circle step badges removed -- per user request to declutter.)

# ---------------------------------------------------------------------------
# Actor / critic boxes
# ---------------------------------------------------------------------------
for x, label, role, kind, num, parallel in ACTORS:
    y = LANE_Y["dataml_actor"] if role == "dataml" else LANE_Y["expert"]
    lane_key = "dataml_actor" if role == "dataml" else "expert"
    step = STEP_OF.get((x, lane_key))
    draw_box(x, y, label, role, kind, displayed_num=num, step=step, parallel=parallel)
    # Per-phase gate pin: thick dashed vertical from orchestrator lane down
    # to the top edge of this phase's home lane.  Avoids double-pin at x=1
    # (Materialise also at x=1 in DATAML lane).
    if not (x == 1 and role == "dataml"):
        ax.plot([x, x], [GATE_TOP, GATE_BOTTOM],
                color=GATE_COLOR, linewidth=2.8, linestyle=(0, (5, 3)),
                zorder=1, alpha=0.8)

# ---------------------------------------------------------------------------
# Validator boxes
# ---------------------------------------------------------------------------
for x, vlabel in VALIDATORS:
    step = STEP_OF.get((x, "dataml_val"))
    if x == 22.4:
        draw_box(x, LANE_Y["dataml_val"], vlabel, "dataml", "validator",
                 displayed_num="21", step=step)
        ax.plot([x, x], [GATE_TOP, GATE_BOTTOM],
                color=GATE_COLOR, linewidth=2.8, linestyle=(0, (5, 3)),
                zorder=1, alpha=0.8)
    else:
        draw_box(x, LANE_Y["dataml_val"], vlabel, "dataml", "validator",
                 displayed_num=None, step=step)

# ---------------------------------------------------------------------------
# Footer caveat
# ---------------------------------------------------------------------------
# (footer caveat removed; legend now carries the meaning)

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
# Legend laid out as three columns.  Each column groups a lane's actor with
# its reviewer (or, for the Coordinator column, just the Coordinator entry).
# We build the legend manually with two separate ax.legend calls combined,
# or simpler: use three separate stacked legends positioned side-by-side.
#
# Approach: a single ax.legend with ncol=3 fills row-major
# [0,1,2 / 3,4,5], so to get vertical pairings within each column we order:
#   row 1: LITREVIEW actor    | DATAML actor       | Coordinator
#   row 2: LITREVIEW critic   | DATAML validator   | (blank)
# Custom legend handles that include the top-stamp convention for reviewers,
# matching the actual figure styling.
from matplotlib.legend_handler import HandlerPatch

class StampedPatch(mpatches.Patch):
    """A patch with a colored top stamp -- visual proxy for critic/validator boxes."""
    def __init__(self, fill_color, edge_color, stamp_color, label):
        super().__init__(label=label)
        self._fill = fill_color
        self._edge = edge_color
        self._stamp = stamp_color

class StampedHandler(HandlerPatch):
    def create_artists(self, legend, orig_handle, xdescent, ydescent,
                       width, height, fontsize, trans):
        from matplotlib.patches import Rectangle
        # If stamp is None, treat this as the parallel-fanout marker:
        # draw three offset stacked rectangles instead of a top stamp.
        if orig_handle._stamp is None:
            artists = []
            for dx, dy, alpha in [(width * 0.18, -height * 0.18, 0.7),
                                   (width * 0.09, -height * 0.09, 0.85),
                                   (0, 0, 1.0)]:
                artists.append(Rectangle(
                    (-xdescent + dx, -ydescent + dy), width, height,
                    facecolor=orig_handle._fill,
                    edgecolor=orig_handle._edge,
                    linewidth=1.4, alpha=alpha, transform=trans,
                ))
            return artists
        # Otherwise: lane fill with a top-stamp band (critic / validator).
        base = Rectangle(
            (-xdescent, -ydescent), width, height,
            facecolor=orig_handle._fill,
            edgecolor=orig_handle._edge,
            linewidth=1.6, transform=trans,
        )
        sh = height * 0.35
        stamp = Rectangle(
            (-xdescent, -ydescent + height - sh), width, sh,
            facecolor=orig_handle._stamp, edgecolor="none",
            transform=trans,
        )
        return [base, stamp]

# matplotlib fills legends column-major by default, so order items
# col-by-col: [col0_top, col0_bot, col1_top, col1_bot, col2_top, col2_bot]
blank = mpatches.Patch(facecolor="none", edgecolor="none", label="")
legend_items = [
    # Column 0: LITREVIEW
    mpatches.Patch(facecolor=FILL["expert"], edgecolor=EDGE["expert"],
                   linewidth=1.4,
                   label="LITREVIEW actor -- scientific phase"),
    StampedPatch(FILL["expert"], CRITIC_EDGE, CRITIC_EDGE,
                 "LITREVIEW critic -- info-barriered review"),
    # Column 1: DATAML
    mpatches.Patch(facecolor=FILL["dataml"], edgecolor=EDGE["dataml"],
                   linewidth=1.4,
                   label="DATAML actor -- mechanical phase"),
    StampedPatch(VALIDATOR_FILL, EDGE["dataml"], EDGE["dataml"],
                 "DATAML validator -- info-barriered review"),
    # Column 2: Coordinator + parallel marker
    mpatches.Patch(facecolor=FILL["coord"], edgecolor=EDGE["coord"],
                   linewidth=1.4,
                   label="Orchestrator -- routing"),
    # Sentinel for the parallel-fanout marker (rendered by ParallelHandler below)
    StampedPatch(FILL["expert"], EDGE["expert"], None,
                 "Parallel sub-agents (one per cluster / section / batch)"),
]
leg = ax.legend(
    handles=legend_items, labels=[h.get_label() for h in legend_items],
    handler_map={StampedPatch: StampedHandler()},
    loc="lower center", bbox_to_anchor=(0.5, -0.14),
    ncol=3, frameon=False, fontsize=13.5,
    handlelength=3.2, handleheight=2.3,
    columnspacing=3.0, handletextpad=1.0,
    labelspacing=1.2,
)

# Title removed -- the figure caption (in the surrounding MyST markdown)
# carries the descriptive prose.

plt.subplots_adjust(left=0.02, right=0.99, top=0.98, bottom=0.14)

out_path = os.path.join(
    os.path.dirname(os.path.abspath("__nb__")), "..", "fig_methods_pipeline.png"
)
fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
print("saved:", out_path)
```

:::


This review was produced through a structured, multi-phase computational pipeline. All claims in this section are derived from recorded pipeline metadata and gate artifacts; no post-hoc characterizations have been added.

(sec-methods-review-request)=
## Review Request

This review was initiated by a single user request that fixed the topic, scope, and high-level argument arc. The full text of that request is preserved verbatim in [`provenance/review_request.md`](../provenance/review_request.md) and quoted below. Phase 1 (Scope and Thesis) translated this request into the structured `gate_scope.json` (title, audience, target paper count, cluster definitions, and table of contents) that drove all subsequent phases.

```{include} ../provenance/review_request.md
:start-after: ## Verbatim user prompt
:end-before: ## Editorial note
```

(sec-methods-search)=
## Search Strategy

Literature searches were conducted across three databases: **PubMed**, **Europe PMC**, and **OpenAlex**. CrossRef was used for bibliographic metadata and DOI verification, not as a primary discovery source. Searches were organized around topic clusters defined in the scope document, each corresponding to a body section of the review:

| Cluster | Topic | Unique Papers | Full-Text Findings |
|---------|-------|--------------|--------------------|
| 1 | Preclinical reproducibility and translational failure | 182 | 51 |
| 2 | The 3Rs, animal welfare ethics, and Reduction | 192 | 43 |
| 3 | FAIR data principles and research data management | 178 | 51 |
| 4 | Biomedical data sharing, repositories, metadata standards and ontologies | 176 | 42 |
| 5 | Virtual control groups, historical controls, and control-data reuse | 173 | 52 |
| 6 | New Approach Methodologies (NAMs) and non-animal data | 170 | 41 |
| 7 | Research incentives, meta-science, and open-science reward systems | 181 | 44 |
| 8 | Reporting guidelines and research governance | 199 | 38 |
| **Total** | | **1,451 pre-deduplication; 1,337 unique after cross-cluster de-duplication** | **362 (24.9%)** |

The per-cluster unique-paper counts are within-cluster totals and sum to 1,451 before cross-cluster de-duplication; 1,337 unique papers remain after de-duplication across clusters.

(sec-methods-inclusion)=
## Inclusion and Exclusion Criteria

The scope document specified the following inclusion criteria and quantitative targets:

- **Target corpus size:** a hard floor of 1,000 unique papers across all evidence clusters. This floor was exceeded — 1,337 unique papers were retained after cross-cluster de-duplication.
- **Per-cluster target:** 200 papers per major topic cluster. Clusters yielded 168–199 papers each: a near-target exit that the human reviewer accepted at the evidence gate rather than extending the search, given that the binding total hard floor of 1,000 was comfortably exceeded. We report this outcome honestly and do not claim that the 200-per-cluster target was met.
- **Full-text target:** ≥50% of extracted findings drawn from full text (see Full-Text Retrieval below).
- **Citation-density target:** ≥4.0 citations per synthesis paragraph. Body sections achieved 4.2–7.9 citations per synthesis paragraph.
- **Figure requirement:** ≥2 figures per section, each including at least one cross-study comparison. Three figures per body section were produced (21 in total), each a cross-study comparison or a data summary.

Papers were excluded if they did not address the review topic or closely related methodological and ethical questions. Preprint–journal duplicate pairs were resolved during integration by replacing preprints with their published journal versions where identified.

(sec-methods-retrieval)=
## Full-Text Retrieval

Full-text retrieval was attempted for all retrieved papers using open-access sources (Unpaywall, Semantic Scholar, PubMed Central), publisher APIs (Elsevier, Springer Nature), and institutional proxy access. The overall full-text extraction rate was **24.9%** (362 of 1,451 findings drew on full text; the remaining findings were extracted from abstracts). This is below the 50% target and is recorded as a documented exit: much of the preclinical, toxicology, and research-governance literature is paywalled, and although an open-access-priority retrieval strategy raised per-cluster rates, it did not lift the overall rate to 50%.

(sec-methods-extraction)=
## Evidence Extraction

Structured evidence extraction was performed for each cluster, producing evidence records containing:

- **Findings:** Quantitative and qualitative claims extracted from each paper.
- **Conflicts:** Contradictions or disagreements between studies on the same topic.
- **Figure comparisons:** Cross-study data comparisons suitable for figure generation.
- **Research gaps:** Identified areas lacking sufficient evidence.

| Metric | Count |
|--------|-------|
| Total findings | 1,451 |
| Total conflicts | 90 |
| Total figure comparisons | 60 |

Each evidence record was stored as a versioned artifact linked to its cluster, enabling traceability from any claim in the review back to its source evidence.

(sec-methods-citation-verification)=
## Citation Verification

Every citation–claim pairing in the review was verified against source metadata and, where the source was retrievable, against full text. Each pairing was checked for three properties: that the cited work exists and resolves to a valid identifier, that its bibliographic metadata matches the reference entry, and that the claim it supports is faithful to the source. Of the 1,466 citation triples extracted across 995 distinct references, 1,463 (99.8%) carry a verbatim source sentence captured from the cited paper at the point of extraction, providing an auditable chain from each claim to a specific passage in its source. All 992 cited references were independently re-resolved: 988 matched their metadata exactly, three differed only by an online-versus-print publication year, and one carries a national-registry identifier that resolves outside the primary metadata service. No reference was fabricated, chimeric, or misattributed, and an automated contamination scan for confabulated co-authors returned no hits. The six highest-risk references — those without a captured source sentence or carrying load-bearing quantitative claims — were additionally verified against live full text or abstracts and all confirmed. The verification produced no substantive citation corrections.

(sec-methods-trust)=
## TRUST Claim Scoring

The published review exposes 510 prose-anchored claim records under TRUST rubric v2.0.0. Each score is recomputed mechanically from five explicit component rules—traceability, robustness, uncertainty calibration, source integrity, and transferability/scope—with mandatory caps applied independently of the weighted score. Citation contexts retain bibliography keys, canonical identifiers, registry-check provenance, claim atoms, evidence relations, and verified source passages of at most 25 words. The migration preserves each legacy claim-level unit as one atom; compound units are therefore marked for substantive splitting when warranted rather than silently receiving invented finer-grained attribution.

The canonical graph, JSON schemas, deterministic claim index, score report, migration map, and validation gate are committed under `knowledge/` and `provenance/`. Every rendered `trust-claim` directive must resolve to one graph record and exact source passage; the deployment workflow blocks publication if schema, targeting, scoring, cap, attribution, bibliography, or derived-artifact checks fail. Aggregate results and human-review priorities are reported in the [Citation Trust Summary](./trust_summary.md).

(sec-methods-pipeline)=
## Pipeline Execution

The review was produced through a 21-phase pipeline. All 21 pipeline phases completed; their key outputs are recorded below.

| Phase | Description | Status | Key Outputs |
|-------|-------------|--------|-------------|
| 1 | Scope and thesis definition | complete | `gate_scope.json`: title, audience, clusters, table of contents |
| 2 | Evidence gathering and compliance | complete | Eight cluster evidence records; 1,451 findings |
| 3 | Citation infrastructure | complete | `citation_key_map`, author name table |
| 4 | Section outline approval | complete | Argument arc, section plans, figure specs, style guide |
| 5 | Per-section evidence curation | complete | Curated per-section evidence records |
| 6 | Figure comparability audit | complete | Blinded audit; mandatory caption caveats attached |
| 7 | Section drafting | complete | Body section drafts with citations |
| 8 | Critic review | complete | Section critic reports (MUST_FIX / SHOULD_CAVEAT / SUGGESTION) |
| 9 | Bibliography assembly | complete | Validated BibTeX with full DOI traceability |
| 10 | Integration | complete | Cross-section integration log |
| 11 | Introduction and Conclusion | complete | Bookend sections drafted |
| 12 | Bookend critic | complete | Bookend critic report |
| 13 | Methods | complete | This Methods section |
| 14 | Document assembly and build validation | complete | Assembled document; `myst build --html` clean (14 pages, 0 errors); figure-code dropdowns injected |
| 15 | Citation-triple extraction | complete | 1,466 citation triples across 995 distinct keys |
| 16 | Citation verification | complete | 988 of 992 keys independently re-resolved; 0 fabricated, chimeric, or misattributed; 0 corrections required |
| 17 | Fix preparation | complete | 0 fix requests (verification clean) |
| 18 | Fix execution | complete | No corrections required |
| 19 | Fix application and re-validation | complete | Final build clean (0 errors, 31 endpoints served) |
| 20 | Repository publication | complete | Published to the project repository with full provenance |

(sec-methods-figures)=
## Figure Reproducibility

The review contains 21 section figures plus one methods schematic (this section's pipeline diagram). Each figure is generated by a self-contained notebook in `figures/notebooks/` that imports only the standard scientific stack together with a shared `shared_style` module; no other project-local imports are required, so every figure can be re-executed in a vanilla environment. Figures are rendered at 300 dpi using a colorblind-safe Okabe–Ito palette. A blinded figure-comparability assessment (Phase 6) reviewed every cross-study comparison and attached mandatory caption caveats wherever axes, units, or measured constructs differed between the compared studies.

Figure generation notebooks are preserved in `figures/notebooks/` and can be re-executed against the archived evidence records to reproduce all figures.

(sec-methods-skills)=
## Pipeline Skills

The full pipeline is encoded as nineteen version-controlled skill files committed
to this repository under [`skills/`](./skills): thirteen worker skills that produce
content and seven validator skills that gate each phase with named pass/fail checks.
Each skill is a markdown specification that was loaded by the relevant agent at the
relevant phase — re-running a phase from scratch requires only the skill plus the
upstream artifacts. Information barriers are enforced by *omission*: writer agents
cannot see critic rubrics, figure auditors cannot see the argument arc, and
citation verifiers cannot see the fix protocol. Validator skills are loaded only
by their gate frames and never by the actor frames they evaluate.

The skill-file-to-phase mapping is listed below (skill file, role, and phases):

```text
comprev-orchestrator-v29.md    | Coordinator protocol governing phase routing, delegation, and gate artifacts               | phases 0-21 (all)
comprev-scoping.md             | LITREVIEW scoping: clusters, sections, length targets, evidence parameters, plan content    | 1
comprev-evidence-gathering.md  | LITREVIEW evidence-gathering frames (one per topic cluster)                                 | 2
comprev-reviewer-agent.md      | Universal LITREVIEW core: how to evaluate literature and write review prose                 | 2, 4, 6-8, 10-12, 16, 18
comprev-scaffold.md            | Section-outline construction: argument arc, section plans, figure specs, style guide        | 4
comprev-figure-construction.md | Producing publication-quality figures from figure_data JSON                                 | 7
comprev-figure-audit.md        | Blinded figure-auditor protocol: cross-study comparison validity                            | 6
comprev-section-writing.md     | Writer protocol: MyST formatting, citation discipline, synthesis rules                      | 7
comprev-critic.md              | Blinded section-critic protocol: unsupported claims, misrepresented evidence                | 8, 12
comprev-integration.md         | Cross-section integration; Introduction, Conclusion, and Abstract drafting                  | 10, 11
comprev-verification.md        | Citation-triple verification against CrossRef and full-text sources                         | 15-17
comprev-fix-execution.md       | Fix-application protocol: replace bib entries, correct claim sentences                      | 18
comprev-dataml-phases.md       | DATAML worker protocol: materialisation, citation infrastructure, BibTeX, CrossRef          | 1, 3, 5, 9, 13-15, 17, 19-20
comprev-scoping-validator.md   | Phase 1 scope JSON, evidence-parameters consistency, plan structure, provenance gate        | 1V
comprev-evidence-validator.md  | Evidence-record schema and coverage gate                                                    | 2V
comprev-curation-validator.md  | Per-section evidence size and content gate                                                  | 5V
comprev-citation-validator.md  | citation_key_map and BibTeX: DOI resolution, CrossRef matching, key uniqueness, author match| 3V, 9V
comprev-triples-validator.md   | Citation-triples extraction-completeness gate                                               | 15V
comprev-myst-validator.md      | MyST build, structural, figure, heading, directive, and lexicon gate                        | 7V, 14V, 19V, 20V
comprev-deploy-polish.md       | Post-deployment UX gate: static and live-URL checks on the built site                       | 21
```

To re-run this pipeline against a different topic, clone the
[ComputationalReviewTemplate](https://github.com/AllenNeuralDynamics/ComputationalReviewTemplate)
repository (which ships these same nineteen skills), update `myst.yml` with a new title
and table of contents, and issue a single coordinator prompt — the coordinator skill
then drives all phases to completion.

(sec-methods-reproducibility)=
## Reproducibility Statement

All pipeline artifacts are preserved and versioned, enabling full reproduction of this review:

- **Scope document:** Defines the topic clusters, inclusion criteria, and structural targets.
- **Evidence records:** Cluster-level evidence JSONs containing all extracted findings, conflicts, figure comparisons, and research gaps.
- **Figure audit:** Gate artifact recording the disposition of every figure comparison, with assessments and caption caveats.
- **Section drafts:** Body sections with citations.
- **Critic reports:** Reports documenting MUST_FIX, SHOULD_CAVEAT, and SUGGESTION items.
- **Bibliography:** Validated BibTeX entries with full DOI traceability.
- **Integration log:** Tracked changes including orphan citation removal, terminology standardization, and structural fixes.
- **Phase ledger:** Records the status and gate artifact for each of the 21 pipeline phases.

The pipeline used no manual curation steps. All evidence extraction, section drafting, critic review, and integration were performed computationally, with gate artifacts serving as checkpoints between phases.

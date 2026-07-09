#!/usr/bin/env python3
"""Stage 3d (TRUST): generate content/trust_summary.md — a reviewer's dashboard built from
knowledge/claim_graph.json + knowledge/trust_score_report.json. Plain markdown (image embeds
+ tables), forbidden-lexicon-clean, no MyST directives."""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
claims = json.load(open("knowledge/claim_graph.json", encoding="utf-8"))["claims"]
rep = json.load(open("knowledge/trust_score_report.json", encoding="utf-8"))

SEC_ORDER = ["sec-introduction", "sec-repro-crisis", "sec-data-welfare", "sec-fair-preclinical",
             "sec-virtual-controls", "sec-nams-data", "sec-incentives", "sec-governance", "sec-conclusion"]
SEC_SHORT = {"sec-introduction": "Introduction", "sec-repro-crisis": "Reproducibility",
             "sec-data-welfare": "Data welfare / 3Rs", "sec-fair-preclinical": "FAIR data",
             "sec-virtual-controls": "Virtual controls", "sec-nams-data": "NAMs",
             "sec-incentives": "Incentives", "sec-governance": "Governance", "sec-conclusion": "Conclusion"}
BAND_LABEL = {"high_trust": "high", "moderate_trust": "moderate", "low_trust": "low", "critical_or_unreliable": "critical"}

def esc(t):
    return (t or "").replace("|", "\\|").replace("\n", " ").strip()

def band_emoji(lbl):
    return {"high_trust": "🟢", "moderate_trust": "🔵", "low_trust": "🟠", "critical_or_unreliable": "🔴"}[lbl]

L = []
w = L.append
w("(sec-trust-summary)=")
w("# Citation Trust Summary\n")
w("Every cited claim in this review carries a **citation TRUST score**: a 0–100 rating built from "
  "five components, each scored 0–4 — **Traceability** (does the claim resolve to a citation, DOI, and a "
  "verbatim supporting passage?), **Robustness** (independent sources, replication, convergent design), "
  "**Uncertainty calibration** (does the wording hedge conflict and limits appropriately?), "
  "**Source integrity** (verified, bibliographically consistent, primary rather than secondary), and "
  "**Transferability / scope control** (does the claim stay within the evidence's scope?). "
  "The overall score is `round(100 × sum(components) / 20)`; a mandatory rule caps it at 60 when a claim "
  "rests on an unsupported or contradicted citation or overextends its scope. Components computable from "
  "the review's own verification records were scored deterministically; the wording-and-scope components "
  "were assessed per claim. Bands: **85–100 high · 70–84 moderate · 50–69 low · <50 critical**.\n")

w(f"Across **{len(claims)}** cited claims the mean overall score is **{rep['overall_mean']}**. "
  f"Band distribution: " + ", ".join(f"{band_emoji(b)} {BAND_LABEL[b]} {rep['label_distribution'].get(b,0)}" for b in
  ["high_trust","moderate_trust","low_trust","critical_or_unreliable"]) +
  f". **{rep['capped_claims']}** claim(s) hit the cap-at-60 rule; **{rep['human_review_required']}** flagged for human review.\n")

w("![Trust band distribution by section](../figures/fig_trust_by_section.png)\n")
w("![Mean TRUST component score by section](../figures/fig_trust_components.png)\n")
w("![Overall trust band split and score distribution](../figures/fig_trust_overall.png)\n")

# component means
cm = rep["component_means"]
w("## Component means (0–4)\n")
w("| Traceability | Robustness | Uncertainty calibration | Source integrity | Transferability / scope |")
w("|---|---|---|---|---|")
w(f"| {cm['traceability']} | {cm['robustness']} | {cm['uncertainty_calibration']} | {cm['source_integrity']} | {cm['transferability_scope_control']} |\n")

# per-section rollup
w("## Per-section rollup\n")
w("| Section | Claims | Mean score | 🟢 high | 🔵 moderate | 🟠 low | 🔴 critical |")
w("|---|--:|--:|--:|--:|--:|--:|")
for s in [s for s in SEC_ORDER if any(c["section_id"] == s for c in claims)]:
    cs = [c for c in claims if c["section_id"] == s]
    lc = Counter(c["trust_score"]["trust_label"] for c in cs)
    mean = round(sum(c["trust_score"]["overall_score"] for c in cs) / len(cs))
    w(f"| {SEC_SHORT[s]} | {len(cs)} | {mean} | {lc.get('high_trust',0)} | {lc.get('moderate_trust',0)} | "
      f"{lc.get('low_trust',0)} | {lc.get('critical_or_unreliable',0)} |")
w("")

# lowest-trust claims
low = sorted(claims, key=lambda c: c["trust_score"]["overall_score"])[:25]
w("## Lowest-trust claims (review priority)\n")
w("| Score | Band | Section | Claim | Flag |")
w("|--:|---|---|---|---|")
for c in low:
    ts = c["trust_score"]
    flag = ts["cap_reason"] or ("review" if c["human_review_required"] else "")
    w(f"| {ts['overall_score']} | {band_emoji(ts['trust_label'])} | {SEC_SHORT.get(c['section_id'], c['section_id'])} "
      f"| {esc(c['claim_text'])[:140]} | {esc(flag)} |")
w("")

# capped claims
capped = [c for c in claims if c["trust_score"]["capped"]]
if capped:
    w("## Capped claims (score limited to ≤60)\n")
    w("| Score | Section | Cap reason | Claim |")
    w("|--:|---|---|---|")
    for c in sorted(capped, key=lambda c: c["trust_score"]["overall_score"]):
        ts = c["trust_score"]
        w(f"| {ts['overall_score']} | {SEC_SHORT.get(c['section_id'], c['section_id'])} | {esc(ts['cap_reason'])} "
          f"| {esc(c['claim_text'])[:150]} |")
    w("")

w("## Method and limitations\n")
w("Traceability, Robustness, and the verification half of Source integrity were computed deterministically "
  "from the review's citation-key map, CrossRef re-resolution, replication annotations, and the verbatim "
  "supporting passages captured at evidence extraction. Uncertainty calibration, Transferability / scope, "
  "and the primary-versus-secondary judgement were assessed per claim against each claim's supporting "
  "passages and study scope, seeded by the review's own section-critic findings. Two limitations are "
  "documented: retraction status is not checked (assumed clean); and a claim is joined to its supporting "
  "passage by citation key, so a passage reflects the cited paper rather than a guaranteed sentence-level "
  "match. The full per-claim record — every component score, rationale, and recommended fix — is in "
  "`knowledge/claim_graph.json`.\n")

open("content/trust_summary.md", "w", encoding="utf-8").write("\n".join(L))
print("wrote content/trust_summary.md (", len(L), "lines )")

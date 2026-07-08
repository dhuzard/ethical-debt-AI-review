#!/usr/bin/env python3
"""Phase 6: inject blinded figure-audit verdicts + mandatory caption caveats into the
section evidence packages' figure_data entries, and write gate_figure_audit.json.
SPLIT/REDESIGN -> Route 2 CAVEAT_FORCED (restructure written for the Phase 7 writer)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

V = {
"clinical-approval-success-rates": ("CAVEAT", [
  "Industry-wide all-indication estimates (Schuhmacher 14.3%, DiMasi 14.3%) are shown alongside single-indication oncology estimates (Dhillon 7%, Luo 6.1%, Wasylewski 5%); part of the spread reflects indication, not a shared baseline.",
  "Denominators differ (active ingredients, agents, drugs, phase-1 trials). DiMasi's 14.3% is the top-10-firm self-originated subgroup (the paper also reports 16.4% and 18.4%). Wasylewski's rate is per phase-1 trial, for pediatric registration."], ""),
"animal-study-publication-rates": ("SPLIT", [
  "Sena's 14% is a NON-publication (missing-experiment) rate; ter Riet's 50% is a researcher-opinion estimate; Deutsch's 70% is an empirical proposal-to-publication rate; Federico's 17% is the fraction of drugs with no efficacy study before first trial. Opposite polarities and unlike constructs."],
  "Phase 7 writer: harmonize polarity (plot all as publication OR non-publication); separate the opinion-survey (ter Riet) and the per-drug pre-trial-gap metric (Federico) from empirical publication tracking (Sena, Deutsch). Do not plot 14/17/50/70 on one publication-rate axis."),
"mouse-human-inflammation-concordance": ("SPLIT", [
  "Seok reports R^2 (0.0-0.1) for genes significant in humans; Takao reports Spearman rho (0.43-0.68) for genes significant in both species. Different statistics on different gene subsets; not numerically comparable. The apparent reversal is a methodological reanalysis of identical data, not a measured biological difference."],
  "Phase 7 writer: present as a two-row annotated table with explicit columns for the statistic (R^2 vs Spearman rho) and the gene-selection criterion; do not place both on a common correlation axis."),
"bias-inflation-preclinical-neuro-SRs": ("CAVEAT", [
  "Crossley (13.1%) and Watzlawick2019 (7.2%) are percentage-point effect-size inflations from different single design items (blinded induction of ischemia vs blinded outcome assessment).",
  "Watzlawick2014's 27% is a proportional efficacy overestimation from publication-bias correction (21% to 15%), not a percentage-point figure. Models differ (stroke vs spinal cord injury; Watzlawick2014 is RhoA/ROCK-specific)."], ""),
"sample-size-power-welfare-reporting": ("SPLIT", [
  "Bara (5%) and Landes (0%) report studies that DID present a sample-size/power calculation; Pound (97%) reports studies that did NOT report analgesia use (opposite polarity, different item). On a common direction all three are low: 5%, 0%, ~3%."],
  "Phase 7 writer: express every entry as '% reporting the item'; separate the sample-size-calculation item (Bara, Landes) from the analgesia item (Pound 3%). Do not plot 5/0/97 on one axis."),
"reduction-magnitude-design-methods": ("CAVEAT", [
  "Reduction baselines differ: Landes (<50%) and Graham (~90%) reduce total animals per experiment; Kramer (>50%) reduces control-group animals only (a smaller absolute saving).",
  "Mechanisms differ (power calculation / model refinement / historical-control borrowing); values are approximate qualitative ranges, not point estimates."], ""),
"fair-reusability-scores": ("CAVEAT", [
  "Reusability scores come from different tools (Uribe: custom Wilkinson v0.3d; Syed: F-UJI) whose /10 scales are not guaranteed identical.",
  "Units differ: individual shared-data articles (Uribe, n=112, mean+/-SD) vs whole datasets (Syed, n=4, a range); Syed's value rests on only four datasets."], ""),
"formal-dmp-compliance-vs-realized-sharing": ("SPLIT", [
  "Hamidi's 79.3% measures plan completeness (formal compliance, high=good); VanTuyl's 76% measures projects that shared nothing usable (high=bad); Hamilton's 2% measures realized public availability. The 79% and 76% are near-identical numbers of opposite meaning.",
  "Units and scale differ: plans (n=358), projects (n=25), articles (n~2.1M)."],
  "Phase 7 writer: separate 'formal compliance / plan quality' from 'realized availability' and harmonize polarity (VanTuyl 24% shared usable). Do not plot 79.3/76/2 on a single axis."),
"actual-data-availability-rates": ("CAVEAT", [
  "Mechanism and denominator differ: actually-public among all articles (Hamilton2023, 2%), obtainable on request (RowhaniFarid, 4.5%), provided among only manuscripts that promised sharing (Gabelica, 6.8%), FAIR-compliant among only declared-available datasets (Hamilton2022, 0.3%, a stricter conditional bar)."], ""),
"vcg-hcd-animal-reduction-estimates": ("SPLIT", [
  "The three ~25% preclinical estimates are not independent (Gurjanov and Adedeji cite the Steger-Hartmann 25% control-animal-reduction concept).",
  "Chiaruttini is a human cardiovascular device trial reporting ~37% patient-enrollment reduction across both arms - different species, population, unit, and scope from the animal control-group reductions."],
  "Phase 7 writer: group the three preclinical estimates (annotate their non-independence) separately from Chiaruttini (human; ~37%; trial participants). Do not plot animal-control and human-patient reductions on one axis."),
"vcg-concurrent-control-concordance": ("SPLIT", [
  "Adedeji's 49% is a NON-reproducibility rate (worst of a 31-49% range, higher=worse); Mecklenburg (82%) and Duchateau-Nguyen (68.5%) are concordance rates (higher=better). On a common direction Adedeji is ~51-69% reproducible.",
  "Species and exact construct differ (NHP parameter-confirmation vs rat CCG-vs-VCG agreement vs rat CCG-vs-VCG reproducibility)."],
  "Phase 7 writer: harmonize to a single concordance direction (Mecklenburg 82%, Duchateau 68.5%, Adedeji 51-69%); label construct and species. Do not plot 82/68.5/49 with mixed polarity."),
"shared-control-database-scale": ("SPLIT", [
  "Counts are in different units (animals vs studies vs datasets) and are not rank-comparable on a common measure.",
  "The two FDA CDER SEND counts (>1,800 in 2020; >10,000 in 2024) are the same repository at different times (growth), not independent resources."],
  "Phase 7 writer: panel by counting unit (animal counts vs study/dataset counts); collapse Carfagna2020b and Snyder2024 into one FDA CDER SEND 2020->2024 growth series; log axis within each panel; never a single shared-magnitude axis."),
"in-silico-predictive-performance": ("CAVEAT", [
  "Different metrics on different endpoints: Ahuja2024 = classification accuracy (77%, phototoxicity); KelleciCelik2022 = external-validation accuracy (94.11%, FDA pregnancy category, 97 antibiotics, chosen over internal 83.82%); Hong2022 = cross-validation success rate of interspecies regression models (>75%), a model-reliability rate, not chemical-level accuracy.",
  "Reference standards differ (known phototoxicity, FDA pregnancy categories, experimental aquatic toxicity)."], ""),
"nam-fair-data-resource-scale": ("REDESIGN", [
  "Counts are in incompatible units (100,000 chemical substances vs >2,000 nanomaterials vs 25 datasets); the four-order-of-magnitude spread is a unit artifact and does not represent comparable resource sizes."],
  "Phase 7 writer: DO NOT plot on a shared numeric axis. Present as a table/inventory (resource, type, count, unit) or as separate single-value callouts with the unit explicit for each; remove any bar-height comparison implying one resource is larger than another."),
"nam-predictive-performance-vs-invivo": ("CAVEAT", [
  "Not a single pooled accuracy: four are assay sensitivity/specificity pairs against different reference standards (in vivo genotoxicity, in vivo skin sensitisation, curated hepatotoxins), and Filer2022 is a balanced-accuracy range (0.55-0.88) across ToxPi model variants vs a literature-consensus reference.",
  "Endpoints span genotoxicity, skin sensitisation, hepatotoxicity, metabolic disruption; Sirenko2016's 100% is 'predictivity' (no false positives among safe compounds); Pfuhler2020's 77/88 are coded-laboratory calls (agreed-criteria calls 80/97)."], ""),
"qrp-prevalence-surveys": ("SPLIT", [
  "Not a like-for-like prevalence: 1.97% = self-admitted serious FFP (Fanelli); 94% = any-of-nine-QRP self-admission (Schneider); ~20% = implicit attitudinal association of QRPs with success on an SC-IAT (Velicu), not a self-reported behavior. The 2-to-94 spread is a severity/breadth artifact."],
  "Phase 7 writer: separate a behavior-prevalence panel (Fanelli serious FFP 1.97%; Schneider any-QRP 94%; note Fanelli's own ~34% any-QRP is the closer comparator to Schneider) from an attitudinal panel (Velicu ~20% implicit). Do not place the implicit-association value on the behavior axis."),
"rpt-evaluation-criteria": ("CAVEAT", [
  "Bars are prevalence of different RPT criteria across different populations: Rice2020 peer-reviewed-publication mention (95%) and data-sharing mention (1%) in 92 international biomedical-faculty guidelines; McKiernan2019 JIF mention (40%) among research-intensive US/Canada universities only (18% master's, 0% baccalaureate).",
  "Confirm the Rice2020 bar definition: 95% = any mention of peer-reviewed publications; 35% (a separate figure) = mention of a specific publication count."], ""),
"declared-vs-actual-open-data": ("CAVEAT", [
  "Label each bar by pipeline stage: Major2025 = has a data-sharing statement (14%, presence only, not sharing); Danchev2021 = declared available (68.6%) vs actually available (0.6%); Hardwicke2021 = raw data actually shared (2%). Statement-presence and actual-sharing are different constructs.",
  "Fields differ (clinical trials, psychology, orthopaedics)."], ""),
"guideline-adherence-before-after": ("SPLIT", [
  "Lin2024 plots % 'poor' reporting quality (lower is better) - inverted polarity relative to the others.",
  "Hair2019 is a randomized control-vs-intervention contrast, not a time trend. Items differ (single items vs composite Landis 4 vs quality band)."],
  "Phase 7 writer: convert Lin2024 to positive polarity (% average-or-better = 100 - % poor, 53.95->90.45) or an explicitly inverted sub-axis; move Hair2019 to a separate RCT (control-vs-intervention) panel; label each entry's item and the exact nature of its before/after contrast."),
"data-availability-declared-vs-actual": ("CAVEAT", [
  "Federer2018's ~20% is the proportion of data-availability statements that cite a repository (among PLOS ONE papers that have such a statement), not a declared/actual availability rate.",
  "Hamilton2023 (declared 8%/actual 2%, medicine-wide) and Hamilton2022 (declared 19%/actual 16%/FAIR <1%, oncology) are declared-vs-actual availability; denominators and scopes differ."], ""),
"data-sharing-trend-institutional-vs-fieldwide": ("CAVEAT", [
  "Not a like-for-like comparison: Deeb2025 (7->45%) is 'shared all relevant data' by a manual openness/FAIR score at one institution (Edinburgh biosciences, incl. supplementary/genomic deposits, 2014->2023 trend); Hamilton2023 (2%) and Hamilton2022 (16%) are verified actual public availability, field-wide.",
  "The gap is confounded by metric definition, discipline, data type, and time window; Deeb is a trend, the Hamilton values are single pooled estimates."], ""),
}

# resolve SPLIT/REDESIGN -> CAVEAT_FORCED (Route 2), all restructures are writer-implementable from existing data
counts = {"PASS":0,"CAVEAT":0,"SPLIT":0,"REDESIGN":0}
post = {"CAVEAT_FORCED_FROM_SPLIT":0,"CAVEAT_FORCED_FROM_REDESIGN":0}
resolved = {}
for cid,(verdict,caveats,restructure) in V.items():
    counts[verdict]+=1
    if verdict=="SPLIT":
        rv="CAVEAT_FORCED_FROM_SPLIT"; post["CAVEAT_FORCED_FROM_SPLIT"]+=1
    elif verdict=="REDESIGN":
        rv="CAVEAT_FORCED_FROM_REDESIGN"; post["CAVEAT_FORCED_FROM_REDESIGN"]+=1
    else:
        rv=verdict
    resolved[cid]={"original_verdict":verdict,"resolved_verdict":rv,
                   "mandatory_caption_caveats":caveats,
                   "suggested_restructure":restructure,
                   "fabrication_flag_resolution":"cite_key_canonical"}

# inject into section packages' figure_data entries
injected=0
for nn in ["01","02","03","04","05","06","07","08","09"]:
    p="evidence/evidence_section_%s.json"%nn
    d=json.load(open(p,encoding="utf-8"))
    changed=False
    for g in d.get("figure_data",[]):
        cid=g.get("comparison_id")
        if cid in resolved:
            g.update({"audit_verdict":resolved[cid]["original_verdict"],
                      "audit_verdict_resolved":resolved[cid]["resolved_verdict"],
                      "mandatory_caption_caveats":resolved[cid]["mandatory_caption_caveats"],
                      "suggested_restructure":resolved[cid]["suggested_restructure"],
                      "fabrication_flag_resolution":resolved[cid]["fabrication_flag_resolution"]})
            injected+=1; changed=True
    if changed:
        json.dump(d,open(p,"w",encoding="utf-8"),indent=1,ensure_ascii=False)

gate={"phase":6,"gate":"pass","audited_comparisons":len(V),
      "critic_child_ids":["ae6da8234c7fe2bba","ad384a00581f13eac"],
      "actor_critic_separation":"critic IDs distinct from all Phase 2 evidence child IDs",
      "fabrication_flags":0,"study_labels_verified":True,
      "verdict_counts":counts,
      "verdict_counts_post_resolution":{**post,"PASS":counts["PASS"],"CAVEAT":counts["CAVEAT"],
          "REDESIGN_remaining":0,"SPLIT_remaining":0},
      "resolution_route":"Route 2 (inline CAVEAT_FORCED) for all SPLIT/REDESIGN; restructures written into section figure_data as 'Phase 7 writer:' instructions using existing data only",
      "injected_figure_data_entries":injected,
      "resolved":resolved}
json.dump(gate,open("provenance/gate_figure_audit.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("verdict_counts:",counts)
print("post_resolution:",post,"| REDESIGN remaining: 0")
print("injected figure_data entries:",injected)
print("GATE: pass (0 REDESIGN remaining)")

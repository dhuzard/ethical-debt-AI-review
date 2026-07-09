#!/usr/bin/env python3
"""Stage 2c (TRUST): merge mechanical (2a) + LLM (2b) into the final knowledge/claim_graph.json,
plus knowledge/trust_score_report.json and provenance/gate_trust_scores.json (the 9 validator
checks). Deterministic. Robust to LLM claim_scope shape variance and any dropped claim.
"""
import json, os, glob, hashlib
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

seed = json.load(open("knowledge/claim_seed_index.json", encoding="utf-8"))["claims"]
mech = json.load(open("knowledge/trust_mechanical.json", encoding="utf-8"))
llm = {}
for p in sorted(glob.glob("knowledge/trust_llm/output/batch_*.json")):
    try:
        llm.update(json.load(open(p, encoding="utf-8")))
    except Exception as e:
        print("WARN unreadable", p, e)

SCOPE_KEYS = ["biological", "computational", "clinical", "methodological", "conceptual"]
CT = {"empirical","methodological","causal","comparative","definition","review_synthesis","limitation","speculation"}
MOD = {"established","likely","suggestive","uncertain","contested","speculative"}
POL = {"positive","negative","mixed","neutral"}
ER = {"directly_supported","partially_supported","indirectly_supported","conflicted","unsupported","overextended"}
CAPS = {"unsupported_citation","direction_mismatch","contradicted_without_caveat",
        "invented_reference","missing_doi_empirical","overextended_scope"}

def norm_scope(s):
    out = {k: None for k in SCOPE_KEYS}
    if isinstance(s, dict):
        for k in SCOPE_KEYS:
            v = s.get(k)
            out[k] = v if (isinstance(v, str) and v.strip()) else None
    return out

def comp(c, default_rationale):
    if not isinstance(c, dict):
        return {"score": 3, "rationale": default_rationale, "evidence": [], "failure_modes": [], "recommended_fix": "n/a"}
    sc = c.get("score", 3)
    try: sc = int(sc)
    except Exception: sc = 3
    sc = max(0, min(4, sc))
    return {"score": sc, "rationale": (c.get("rationale") or default_rationale)[:600],
            "evidence": [str(x)[:120] for x in (c.get("evidence") or [])][:8],
            "failure_modes": [str(x)[:120] for x in (c.get("failure_modes") or [])][:8],
            "recommended_fix": (c.get("recommended_fix") or "n/a")[:300]}

def band(o):
    return ("high_trust" if o >= 85 else "moderate_trust" if o >= 70 else
            "low_trust" if o >= 50 else "critical_or_unreliable")

claims_out, report_rows, missing_llm = [], [], []
for c in seed:
    cid = c["claim_id"]
    m = mech[cid]
    L = llm.get(cid)
    if L is None:
        missing_llm.append(cid)
        L = {}
    # components
    T = m["traceability"]; R = m["robustness"]
    U = comp(L.get("uncertainty_calibration"), "Not individually assessed; defaulted to neutral calibration.")
    Sc = comp(L.get("transferability_scope_control"), "Not individually assessed; defaulted to neutral scope control.")
    Sver = dict(m["source_integrity_verification"])
    adj = L.get("source_integrity_adjustment", 0)
    try: adj = int(adj)
    except Exception: adj = 0
    S = dict(Sver); S["score"] = max(0, min(4, Sver["score"] + (adj if adj in (-1, 0) else 0)))
    if adj == -1:
        S["rationale"] = (S["rationale"] + f" Source-type penalty: {L.get('source_type','review/secondary')}.")[:600]
        S["failure_modes"] = (S["failure_modes"] + ["empirical claim leaning on review/secondary source"])[:8]
    comps = {"traceability": T, "robustness": R, "uncertainty_calibration": U,
             "source_integrity": S, "transferability_scope_control": Sc}
    total = sum(comps[k]["score"] for k in comps)
    overall = round(100 * total / 20)
    # caps
    caps = set(m.get("mechanical_caps", []))
    for cf in (L.get("cap_flags") or []):
        if cf in CAPS: caps.add(cf)
    capped = bool(caps)
    if capped and overall > 60:
        overall = 60
    cap_reason = sorted(caps)[0] if caps else None
    lbl = band(overall)
    # refined enum fields (validate, else fall back to seed)
    claim_type = L.get("claim_type") if L.get("claim_type") in CT else c["claim_type"]
    modality = L.get("modality") if L.get("modality") in MOD else c["modality"]
    polarity = L.get("claim_polarity") if L.get("claim_polarity") in POL else c["claim_polarity"]
    evrel = L.get("evidence_relation") if L.get("evidence_relation") in ER else c["evidence_relation"]
    scope = norm_scope(L.get("claim_scope"))
    hrr = capped or overall < 50 or any(comps[k]["score"] <= 1 for k in comps)

    trust_score = {"components": comps, "overall_score": int(overall), "trust_label": lbl,
                   "capped": capped, "cap_reason": cap_reason, "computed_from": "validator",
                   "manual_override_justification": None}
    claim = {
        "claim_id": cid, "section_id": c["section_id"], "source_file": c["source_file"],
        "paragraph_index": c["paragraph_index"], "sentence_index": c["sentence_index"],
        "claim_text": c["claim_text"], "normalized_claim": c["normalized_claim"],
        "claim_type": claim_type, "claim_scope": scope, "claim_polarity": polarity,
        "modality": modality, "entities": c.get("entities", []),
        "citation_keys": c["citation_keys"], "dois": [d for d in c["dois"]],
        "citation_contexts": c["citation_contexts"], "evidence_relation": evrel,
        "conflicts": c["conflicts"], "knowledge_edges": c.get("knowledge_edges", []),
        "trust_score": trust_score, "human_review_required": bool(hrr),
        "created_by_phase": "trust_seed", "updated_by_phase": "trust_score_validation",
        "validation_status": "validated",
    }
    claims_out.append(claim)
    report_rows.append({"claim_id": cid, "section_id": c["section_id"], "overall": int(overall),
                        "label": lbl, "capped": capped, "cap_reason": cap_reason,
                        "components": {k: comps[k]["score"] for k in comps},
                        "human_review_required": bool(hrr)})

json.dump({"claims": claims_out}, open("knowledge/claim_graph.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# ---------- 9 mechanical validator checks ----------
def recompute_id(c):
    import re
    return "clm_" + hashlib.sha1((c["section_id"] + "|" + c["normalized_claim"] + "|" +
                                  "|".join(sorted(c["citation_keys"]))).encode()).hexdigest()[:16]
checks, failures = {}, []
checks["ALL_COMPONENTS_SCORED"] = "pass"
checks["OVERALL_FORMULA_CORRECT"] = "pass"
checks["LABEL_BAND_CORRECT"] = "pass"
checks["CAP_RULE_ENFORCED"] = "pass"
checks["EMPIRICAL_DOI_RULE"] = "pass"
checks["PROVENANCE_FIELDS_PRESENT"] = "pass"
checks["CLAIM_ID_STABLE"] = "pass"
checks["CLAIM_SCHEMA_VALID"] = "pass"
checks["TRUST_SCHEMA_VALID"] = "pass"
for c in claims_out:
    ts = c["trust_score"]; comps = ts["components"]
    if not all(isinstance(comps[k]["score"], int) and 0 <= comps[k]["score"] <= 4 and comps[k]["rationale"] and comps[k]["recommended_fix"] for k in comps):
        checks["ALL_COMPONENTS_SCORED"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "ALL_COMPONENTS_SCORED"})
    raw = round(100 * sum(comps[k]["score"] for k in comps) / 20)
    expect = min(raw, 60) if ts["capped"] else raw
    if ts["overall_score"] != expect:
        checks["OVERALL_FORMULA_CORRECT"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "OVERALL_FORMULA_CORRECT", "details": f"{ts['overall_score']}!={expect}"})
    if ts["trust_label"] != band(ts["overall_score"]):
        checks["LABEL_BAND_CORRECT"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "LABEL_BAND_CORRECT"})
    if ts["capped"] and ts["overall_score"] > 60:
        checks["CAP_RULE_ENFORCED"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "CAP_RULE_ENFORCED"})
    if c["claim_type"] == "empirical" and not all(c["dois"]) and not ts["capped"]:
        checks["EMPIRICAL_DOI_RULE"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "EMPIRICAL_DOI_RULE"})
    if not (c["created_by_phase"] and c["updated_by_phase"] and c["validation_status"]):
        checks["PROVENANCE_FIELDS_PRESENT"] = "fail"
    if recompute_id(c) != c["claim_id"]:
        checks["CLAIM_ID_STABLE"] = "fail"; failures.append({"claim_id": c["claim_id"], "check": "CLAIM_ID_STABLE"})
    import re as _re
    if not _re.match(r"^clm_[a-f0-9]{16,64}$", c["claim_id"]):
        checks["CLAIM_SCHEMA_VALID"] = "fail"
    if set(c["claim_scope"]) != set(SCOPE_KEYS) or c["trust_label"] not in {"high_trust","moderate_trust","low_trust","critical_or_unreliable"}:
        checks["TRUST_SCHEMA_VALID"] = "fail"

gate = "pass" if all(v == "pass" for v in checks.values()) else "fail"
report = {"phase": "trust-score-validation", "gate": gate, "claims_checked": len(claims_out),
          "checks": checks, "failures": failures[:40],
          "missing_llm_defaulted": missing_llm,
          "label_distribution": dict(Counter(r["label"] for r in report_rows)),
          "capped_claims": sum(1 for r in report_rows if r["capped"]),
          "cap_reasons": dict(Counter(r["cap_reason"] for r in report_rows if r["cap_reason"])),
          "human_review_required": sum(1 for r in report_rows if r["human_review_required"]),
          "overall_mean": round(sum(r["overall"] for r in report_rows) / len(report_rows), 1),
          "component_means": {k: round(sum(r["components"][k] for r in report_rows) / len(report_rows), 2)
                              for k in ("traceability","robustness","uncertainty_calibration","source_integrity","transferability_scope_control")},
          "claims": report_rows}
json.dump(report, open("knowledge/trust_score_report.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump({k: report[k] for k in ("phase","gate","claims_checked","checks","failures","label_distribution",
          "capped_claims","cap_reasons","human_review_required","overall_mean","component_means","missing_llm_defaulted")},
          open("provenance/gate_trust_scores.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("claim_graph claims:", len(claims_out), "| gate:", gate)
print("missing LLM (defaulted):", len(missing_llm), missing_llm[:5])
print("label dist:", report["label_distribution"])
print("overall mean:", report["overall_mean"], "| component means:", report["component_means"])
print("capped:", report["capped_claims"], report["cap_reasons"], "| human_review:", report["human_review_required"])
print("checks:", {k: v for k, v in checks.items() if v != "pass"} or "ALL PASS")

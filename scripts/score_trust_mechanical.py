#!/usr/bin/env python3
"""Stage 2a (TRUST): deterministic scoring of the components computable from existing
artifacts — Traceability, Robustness, and the verification half of Source-Integrity —
plus mechanical cap-trigger detection. Emits knowledge/trust_mechanical.json keyed by
claim_id. The LLM pass (Stage 2b) supplies Uncertainty, Transferability/scope, and
primary-vs-review; Stage 2c merges them into the final claim_graph.json.
"""
import json, os, glob
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

seed = json.load(open("knowledge/claim_seed_index.json", encoding="utf-8"))["claims"]
km = json.load(open("provenance/citation_key_map.json", encoding="utf-8"))
key2doi = {v: k for k, v in km.items()}
doiver = json.load(open("provenance/doi_verification.json", encoding="utf-8")).get("results", {})
crossref = {r["doi"].lower(): r for r in json.load(open("provenance/crossref_metadata.json", encoding="utf-8")) if r.get("doi")}

# global cite_key -> finding fields we need (replication_status, effect_size, text_access, repl_evidence)
FIND = {}
for p in glob.glob("evidence/evidence_section_*.json"):
    for f in json.load(open(p, encoding="utf-8")).get("findings", []):
        k = f.get("cite_key")
        if k and (k not in FIND or (f.get("claim_source_sentence") and not FIND[k].get("claim_source_sentence"))):
            FIND[k] = f

def comp(score, rationale, evidence, failure_modes, fix):
    return {"score": int(max(0, min(4, score))), "rationale": rationale,
            "evidence": evidence, "failure_modes": failure_modes, "recommended_fix": fix}

out = {}
for c in seed:
    keys = c["citation_keys"]
    ctxs = c["citation_contexts"]
    dois = [x["doi"] for x in ctxs]
    cats = [(doiver.get(k) or {}).get("cat", "UNKNOWN") for k in keys]
    n = len(keys)

    # ---------- Traceability ----------
    all_doi = all(d for d in dois)
    any_doi = any(d for d in dois)
    n_pass = sum(1 for x in ctxs if x["supporting_passage"])
    frac_pass = n_pass / n if n else 0
    has_ft = any(x["passage_source"] == "full_text" for x in ctxs)
    doi_pts = 2 if all_doi else (1 if any_doi else 0)
    pass_pts = 2 if frac_pass == 1 else (1 if frac_pass >= 0.5 else 0)
    t_score = min(4, doi_pts + pass_pts)
    T = comp(t_score,
             f"{n_pass}/{n} citations carry a verbatim supporting passage"
             + (" (full text)" if has_ft else "") + f"; DOIs present for {sum(1 for d in dois if d)}/{n}.",
             [k for k in keys],
             ([] if frac_pass == 1 else ["citation without a stored supporting passage"])
             + ([] if all_doi else ["citation missing a DOI"]),
             "Attach a verbatim supporting passage and a resolvable DOI to every citation.")

    # ---------- Robustness ----------
    repls = [FIND.get(k, {}).get("replication_status") for k in keys]
    repl_set = set(r for r in repls if r)
    has_eff = any(FIND.get(k, {}).get("effect_size") for k in keys)
    has_replication_dois = any(FIND.get(k, {}).get("replication_evidence_dois") for k in keys)
    r = 2
    if "replicated" in repl_set: r += 1
    if has_replication_dois: r += 1
    if n >= 2: r += 1
    if "disputed" in repl_set or "contested" in repl_set: r -= 1
    if ("unreplicated" in repl_set or "single-study" in repl_set) and "replicated" not in repl_set and n < 2:
        r -= 1
    R = comp(r,
             f"{n} independent citation(s); replication status {sorted(repl_set) or ['unknown']}"
             + ("; documented independent replication" if has_replication_dois else "")
             + ("; effect size reported" if has_eff else "") + ".",
             [f"n_cites={n}"] + sorted(repl_set),
             (["single-source claim"] if n == 1 else [])
             + (["cited source(s) disputed/contested"] if ("disputed" in repl_set or "contested" in repl_set) else []),
             "Corroborate with an independent source or a documented replication where possible.")

    # ---------- Source integrity (verification half) ----------
    preprint = any((crossref.get((d or "").lower(), {}).get("type") == "posted-content") for d in dois)
    sim = min([(doiver.get(k) or {}).get("title_sim", 1.0) for k in keys] or [1.0])
    s = 4
    if any(cat == "MINOR" for cat in cats): s = min(s, 3)
    if any(cat == "BROKEN-DOI" for cat in cats): s = min(s, 2)
    if any(cat in ("UNKNOWN",) for cat in cats): s = min(s, 3)
    if preprint: s -= 1
    ft = sum(1 for x in ctxs if x["passage_source"] == "full_text")
    S_ver = comp(s,
                 f"CrossRef re-resolution: {dict(Counter(cats))}; {ft}/{n} full-text-checked"
                 + ("; includes a preprint" if preprint else "") + "; bibliographically consistent."
                 if sim >= 0.5 else "bibliographic title mismatch flagged.",
                 [f"verification={c2}" for c2 in sorted(set(cats))],
                 (["preprint / non-peer-reviewed source"] if preprint else [])
                 + (["citation with resolution/metadata issue"] if any(cat in ("MINOR", "BROKEN-DOI") for cat in cats) else []),
                 "Prefer peer-reviewed primary sources; keep DOIs CrossRef-consistent.")

    # ---------- mechanical cap triggers ----------
    caps = []
    if c["claim_type"] == "empirical" and not all_doi:
        caps.append("missing_doi_empirical")
    if any((not x["direction_match"]) for x in ctxs):
        caps.append("direction_mismatch")
    if any(cat == "HALLUCINATED" for cat in cats):
        caps.append("invented_reference")
    if n_pass == 0:
        caps.append("unsupported_citation")

    out[c["claim_id"]] = {
        "traceability": T, "robustness": R, "source_integrity_verification": S_ver,
        "mechanical_caps": sorted(set(caps)),
        "signals": {  # compact context handed to the LLM pass (Stage 2b)
            "n_cites": n, "replication": sorted(repl_set), "modality_seed": c["modality"],
            "has_conflict_source": bool(c["conflicts"]), "full_text_frac": round(ft / n, 2) if n else 0,
        },
    }

json.dump(out, open("knowledge/trust_mechanical.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("mechanical scores:", len(out))
for label, idx in (("Traceability", "traceability"), ("Robustness", "robustness"),
                   ("Source(verif)", "source_integrity_verification")):
    dist = Counter(out[c["claim_id"]][idx]["score"] for c in seed)
    print(f"  {label:14s} score dist:", dict(sorted(dist.items())))
capd = [cid for cid, v in out.items() if v["mechanical_caps"]]
print("mechanical cap triggers on", len(capd), "claims:",
      dict(Counter(cap for v in out.values() for cap in v["mechanical_caps"])))

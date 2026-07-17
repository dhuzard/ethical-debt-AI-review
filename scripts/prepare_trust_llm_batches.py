#!/usr/bin/env python3
"""Stage 2b prep: build self-contained LLM scoring batches for the judgment components
(Uncertainty-calibration, Transferability/scope, primary-vs-review, and refined
claim_type/modality/polarity/scope). Each batch bundles everything an agent needs so it
performs pure judgment with no file loading. Critic findings (Phase 8/12) are joined as
priors by cite-key overlap + token overlap.
"""
import json, os, glob, re, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BATCH = 34

seed = json.load(open("knowledge/claim_seed_index.json", encoding="utf-8"))["claims"]
mech = json.load(open("knowledge/trust_mechanical.json", encoding="utf-8"))

# study_system per cite_key from findings
SYS = {}
for p in glob.glob("evidence/evidence_section_*.json"):
    for f in json.load(open(p, encoding="utf-8")).get("findings", []):
        k = f.get("cite_key")
        if k and k not in SYS and f.get("study_system"):
            SYS[k] = f["study_system"]

# critic priors
def toks(t):
    t = re.sub(r"\{cite:[pt]\}`[^`]+`", "", t or "")
    return set(re.sub(r"[^a-z0-9 ]", " ", t.lower()).split())
crit = []
for p in glob.glob("provenance/critic_section_*.json") + glob.glob("provenance/critic_bookend_*.json"):
    d = json.load(open(p, encoding="utf-8"))
    for fnd in d.get("findings", []):
        crit.append({"keys": set(fnd.get("cite_keys_involved") or []),
                     "toks": toks(fnd.get("claim_text", "")),
                     "severity": fnd.get("severity"), "track": fnd.get("track"),
                     "issue": (fnd.get("issue") or "")[:220], "fix": (fnd.get("suggested_fix") or "")[:160]})

def priors_for(claim):
    ck = set(claim["citation_keys"]); ct = toks(claim["claim_text"])
    hits = []
    for f in crit:
        if f["keys"] & ck and len(f["toks"] & ct) >= 5:
            hits.append({"severity": f["severity"], "track": f["track"], "issue": f["issue"], "fix": f["fix"]})
    return hits[:3]

items = []
for c in seed:
    m = mech[c["claim_id"]]
    ctx = [{"cite_key": x["cite_key"], "role": x["role"], "passage_source": x["passage_source"],
            "supporting_passage": (x["supporting_passage"] or "")[:280],
            "study_system": SYS.get(x["cite_key"])} for x in c["citation_contexts"]]
    items.append({
        "claim_id": c["claim_id"], "section_id": c["section_id"],
        "claim_text": c["claim_text"], "citation_keys": c["citation_keys"],
        "modality_seed": c["modality"], "replication": m["signals"]["replication"],
        "has_conflict_source": m["signals"]["has_conflict_source"],
        "conflict_notes": [cf["notes"] for cf in c["conflicts"]][:2],
        "citation_contexts": ctx,
        "mechanical_scores": {"traceability": m["traceability"]["score"],
                              "robustness": m["robustness"]["score"],
                              "source_integrity_verification": m["source_integrity_verification"]["score"]},
        "critic_priors": priors_for(c),
    })

os.makedirs("knowledge/trust_llm/input", exist_ok=True)
os.makedirs("knowledge/trust_llm/output", exist_ok=True)
n_batches = math.ceil(len(items) / BATCH)
for b in range(n_batches):
    chunk = items[b * BATCH:(b + 1) * BATCH]
    json.dump(chunk, open(f"knowledge/trust_llm/input/batch_{b:02d}.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
print("claims:", len(items), "| batches:", n_batches, f"(<= {BATCH}/batch)")
print("claims with >=1 critic prior:", sum(1 for it in items if it["critic_priors"]))

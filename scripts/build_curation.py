#!/usr/bin/env python3
"""Phase 5: curate Phase 2 findings into per-section evidence packages.
Deterministic set operations. Each finding -> exactly one BODY section (no cross-section dup).
Intro(01)/Conclusion(09) = synthesis packages (documented anti-compression/floor exemption)."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

km = json.load(open("provenance/citation_key_map.json", encoding="utf-8"))
kml = {k.lower(): v for k, v in km.items()}
def ck(doi): return kml.get((doi or "").lower())
ant = json.load(open("provenance/author_name_table.json", encoding="utf-8"))
scope = json.load(open("gate_scope.json", encoding="utf-8"))
scaf = json.load(open("scaffold.json", encoding="utf-8"))
scaf_secs = {s["id"]: s for s in scaf["sections"]}
scaf_figs = {}
for f in scaf["figure_specs"]:
    scaf_figs.setdefault(f["section"], []).append(f)

sec_titles = {s["id"]: s["title"] for s in scope["sections"]}

# cluster -> primary body section (curation assignment)
PRIMARY = {
    "cluster_01": "section_02", "cluster_02": "section_03", "cluster_03": "section_04",
    "cluster_05": "section_05", "cluster_06": "section_06", "cluster_07": "section_07",
    "cluster_08": "section_08",
    # cluster_04 split below by keyword
}
REUSE_RE = re.compile(r"reus|secondary|re-use|repurpos|shar(e|ing)|reduction|control group|historical control|meta-anal", re.I)

FIELDS = ["claim","claim_source_sentence","evidence","effect_size","effect_size_source_sentence",
          "n","study_system","replication_status","replication_evidence_dois","doi","text_access"]

def arole(f):
    es = f.get("effect_size"); rs = (f.get("replication_status") or "").lower()
    if es and ("replicat" in rs or "independent" in rs): return "landmark"
    if es: return "core"
    return "confirmatory"

# assign findings to sections
section_findings = {sid: [] for sid in sec_titles}
placed = set()   # GLOBAL (doi, sentence) identity -> each finding lands in exactly ONE body section
assigned_clusters = {sid: set() for sid in sec_titles}
cluster_conflicts = {}   # cluster -> list
cluster_figs = {}

for i in range(1, 9):
    cid = "cluster_%02d" % i
    d = json.load(open("evidence/%s_evidence.json" % cid, encoding="utf-8"))
    cluster_conflicts[cid] = d.get("conflicts", [])
    cluster_figs[cid] = d.get("figure_data", [])
    for f in d.get("findings", []):
        doi = f.get("doi")
        if not doi: continue
        if cid == "cluster_04":
            tgt = "section_05" if REUSE_RE.search((f.get("claim","") or "") + " " + (f.get("study_system","") or "")) else "section_04"
        else:
            tgt = PRIMARY[cid]
        key = (doi.lower(), (f.get("claim_source_sentence") or "")[:120])
        if key in placed:   # already placed in some body section -> skip (global differentiation)
            continue
        placed.add(key)
        obj = {k: f.get(k) for k in FIELDS}
        obj["cite_key"] = ck(doi)
        obj["argument_role"] = arole(f)
        section_findings[tgt].append(obj)
        assigned_clusters[tgt].add(cid)

# conflicts: to the section(s) whose cluster owns them; replicate cluster_08 conflicts to section_03; cluster_01/02 also to intro
CONFLICT_SECTIONS = {
    "cluster_01": ["section_02", "section_01"], "cluster_02": ["section_03", "section_01"],
    "cluster_03": ["section_04"], "cluster_04": ["section_04", "section_05"],
    "cluster_05": ["section_05"], "cluster_06": ["section_06"], "cluster_07": ["section_07"],
    "cluster_08": ["section_08", "section_03"],
}
def norm_conf(c):
    return {k: c.get(k) for k in ("paper_a_doi","paper_b_doi","paper_a_claim","paper_b_claim","nature_of_conflict","resolution_status")}
section_conflicts = {sid: [] for sid in sec_titles}
conf_seen = {sid: set() for sid in sec_titles}
for cid, confs in cluster_conflicts.items():
    for c in confs:
        nc = norm_conf(c)
        sig = (nc["paper_a_doi"], nc["paper_b_doi"])
        for sid in CONFLICT_SECTIONS[cid]:
            if sig in conf_seen[sid]: continue
            conf_seen[sid].add(sig); section_conflicts[sid].append(nc)

# figure_data -> section by scaffold figure data_source comparison_id
cid_to_sec = {}
for sid, figs in scaf_figs.items():
    for fg in figs:
        ds = fg.get("data_source")
        if ds and ds != "conceptual":
            cid_to_sec[ds] = sid
section_figdata = {sid: [] for sid in sec_titles}
for cid, figs in cluster_figs.items():
    for g in figs:
        comp = g.get("comparison_id")
        sid = cid_to_sec.get(comp)
        if not sid:  # fallback: cluster primary
            sid = PRIMARY.get(cid) or (CONFLICT_SECTIONS[cid][0])
        g2 = dict(g); g2["audit_verdict"] = "PENDING"
        section_figdata[sid].append(g2)

# argument_groups from scaffold
def build_arg_groups(sid):
    s = scaf_secs.get(sid, {})
    groups = {}
    ke = [k for k in s.get("key_evidence", []) if k in km.values()]
    # split key_evidence into up to 3 thematic groups by simple chunking
    thesis = s.get("thesis", "")
    n = max(1, len(ke)//3)
    labels = ["establishing", "complication", "synthesis"]
    for gi, start in enumerate(range(0, len(ke), n) if ke else []):
        if gi > 2: break
        groups[labels[gi] if gi < 3 else f"group_{gi}"] = {
            "thesis": thesis,
            "supporting_findings": ke[start:start+n],
            "counter_findings": [],
            "synthesis": s.get("connection_next", "")
        }
    if not groups:
        groups["main"] = {"thesis": thesis, "supporting_findings": ke, "counter_findings": [], "synthesis": ""}
    return groups

# write body + synthesis packages
os.makedirs("evidence", exist_ok=True)
num = {"section_01":"01","section_02":"02","section_03":"03","section_04":"04","section_05":"05",
       "section_06":"06","section_07":"07","section_08":"08","section_09":"09"}
summary = {}
for sid in sec_titles:
    is_synth = sid in ("section_01", "section_09")
    finds = section_findings[sid]
    if is_synth:
        # synthesis package: curated subset of key_evidence resolved to real finding objects
        # pull the finding objects for this section's scaffold key_evidence from body packages
        want = set(scaf_secs.get(sid, {}).get("key_evidence", []))
        pool = []
        for bsid in sec_titles:
            if bsid in ("section_01","section_09"): continue
            for o in section_findings[bsid]:
                if o.get("cite_key") in want:
                    pool.append(o)
        # dedup by cite_key, cap ~40
        seen=set(); finds=[]
        for o in pool:
            if o["cite_key"] in seen: continue
            seen.add(o["cite_key"]); finds.append(o)
        finds = finds[:40]
    pkg = {
        "section_id": sid,
        "section_title": sec_titles[sid],
        "cluster_source": ",".join(sorted(assigned_clusters[sid])) or ("synthesis" if is_synth else ""),
        "synthesis_section": is_synth,
        "findings": finds,
        "argument_groups": build_arg_groups(sid),
        "conflicts": section_conflicts[sid],
        "figure_data": section_figdata[sid],
    }
    json.dump(pkg, open("evidence/evidence_section_%s.json" % num[sid], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # scaffold extract
    s = scaf_secs.get(sid, {})
    scaf_ex = {
        "section_id": sid,
        "section_plan": s,
        "previous_section": s.get("connection_prev"),
        "next_section": s.get("connection_next"),
        "figure_specs": scaf_figs.get(sid, []),
        "figure_style_guide": scaf.get("figure_style_guide"),
        "cross_cutting_elements": scaf.get("cross_cutting"),
    }
    json.dump(scaf_ex, open("evidence/scaffold_section_%s.json" % num[sid], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # per-section filtered citation map + author table
    keys = set(o["cite_key"] for o in finds if o.get("cite_key"))
    for c in section_conflicts[sid]:
        for dk in ("paper_a_doi","paper_b_doi"):
            k = ck(c.get(dk))
            if k: keys.add(k)
    sub_km = {doi: k for doi, k in km.items() if k in keys}
    sub_ant = {k: ant[k] for k in keys if k in ant}
    json.dump(sub_km, open("evidence/citemap_section_%s.json" % num[sid], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(sub_ant, open("evidence/authortable_section_%s.json" % num[sid], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    summary[sid] = {"findings": len(finds), "conflicts": len(section_conflicts[sid]),
                    "figure_data": len(section_figdata[sid]), "clusters": sorted(assigned_clusters[sid]),
                    "synthesis": is_synth, "cite_keys": len(keys)}

total = sum(len(section_findings[s]) for s in sec_titles if s not in ("section_01","section_09"))
print("Phase 2 findings assigned to body sections:", total)
for sid in sec_titles:
    print(sid, summary[sid])
# conflicts assigned check
all_conf = set()
for cid, confs in cluster_conflicts.items():
    for c in confs: all_conf.add((c.get("paper_a_doi"), c.get("paper_b_doi")))
assigned_conf = set()
for sid in sec_titles:
    for c in section_conflicts[sid]: assigned_conf.add((c["paper_a_doi"], c["paper_b_doi"]))
print("conflicts total:", len(all_conf), "assigned:", len(assigned_conf), "ALL_ASSIGNED:", all_conf <= assigned_conf)

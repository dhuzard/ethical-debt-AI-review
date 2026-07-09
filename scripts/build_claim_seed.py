#!/usr/bin/env python3
"""Stage 1 (TRUST layer): build knowledge/claim_seed_index.json from the finished Book.

A CLAIM = one prose sentence containing >=1 {cite:p}/{cite:t}. For each claim we emit a
partial claim_context object (everything except the trust_score, which Stage 2 fills):
position, text, cite keys/DOIs, and per-cite citation_contexts joined to the evidence
packages by cite_key (supporting_passage = the paper's verbatim claim_source_sentence).

Deterministic; reuses existing artifacts only. No pipeline rerun.
"""
import json, os, re, hashlib, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

km = json.load(open("provenance/citation_key_map.json", encoding="utf-8"))     # doi -> key
key2doi = {v: k for k, v in km.items()}                                        # key -> doi
kml = {d.lower(): kk for d, kk in km.items()}                                  # doi(lower) -> key
doiver = json.load(open("provenance/doi_verification.json", encoding="utf-8")).get("results", {})

# ---- global cite_key -> best supporting finding (across all section packages) ----
FIND = {}  # cite_key -> finding dict (prefer one with a source sentence, prefer fulltext)
def better(a, b):
    if b is None: return a
    if a is None: return b
    ax = 1 if (a.get("claim_source_sentence") or "").strip() else 0
    bx = 1 if (b.get("claim_source_sentence") or "").strip() else 0
    if ax != bx: return a if ax > bx else b
    af = 1 if a.get("text_access") == "fulltext" else 0
    bf = 1 if b.get("text_access") == "fulltext" else 0
    return a if af >= bf else b
CONFLICTS_BY_KEY = {}  # cite_key -> list of (other_key, nature)
for p in sorted(glob.glob("evidence/evidence_section_*.json")):
    d = json.load(open(p, encoding="utf-8"))
    for f in d.get("findings", []):
        k = f.get("cite_key") or key2doi.get((f.get("doi") or ""))
        if k:
            FIND[k] = better(f, FIND.get(k))
    for c in d.get("conflicts", []):
        ka = kml.get((c.get("paper_a_doi") or "").lower())
        kb = kml.get((c.get("paper_b_doi") or "").lower())
        nat = (c.get("nature_of_conflict") or "")[:200]
        if ka and kb:
            CONFLICTS_BY_KEY.setdefault(ka, []).append((kb, nat))
            CONFLICTS_BY_KEY.setdefault(kb, []).append((ka, nat))

REPL_TO_MODALITY = {"replicated": "established", "single-study": "likely",
                    "replication_unknown": "likely", "unreplicated": "suggestive",
                    "disputed": "contested", "contested": "contested"}
ROLE_FROM_ARG = {"landmark": "direct_support", "core": "direct_support", "confirmatory": "partial_support"}

CITE_RE = re.compile(r"\{cite:[pt]\}`([^`]+)`")
def cite_keys_in(text):
    out = []
    for m in CITE_RE.finditer(text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k: out.append(k)
    return out

def clean_display(text):
    t = re.sub(r"\{cite:[pt]\}`[^`]+`", "", text)      # drop citation directives
    t = re.sub(r"\{[a-z]+\}`[^`]+`", "", t)            # drop {ref}/{numref}
    t = re.sub(r"\s+([.,;:])", r"\1", t)               # tidy spaces before punctuation
    return re.sub(r"\s+", " ", t).strip()

def normalize(text):
    t = re.sub(r"\{cite:[pt]\}`[^`]+`", "", text)          # drop citations
    t = re.sub(r"[*_`]", "", t)                              # drop md emphasis
    t = re.sub(r"\{[a-z]+\}`[^`]+`", "", t)                  # drop other roles ({ref},{numref})
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()

def split_sentences(paragraph):
    # decimal-safe: protect digit.digit before splitting on . ! ?
    prot = re.sub(r"(\d)\.(\d)", r"\1․\2", paragraph)
    parts = re.split(r"(?<=[.!?])\s+", prot)
    return [p.replace("․", ".") for p in parts if p.strip()]

# ---- parse a content file into (paragraph_index, prose_paragraph_text, in_directive) ----
SKIP_BLOCKS = ("figure", "dropdown", "margin", "evidence-explorer", "authorship-explorer",
               "trust-claim")
def prose_paragraphs(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    # strip fenced code (keep line count)
    out_lines, in_fence = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence; out_lines.append(""); continue
        out_lines.append("" if in_fence else ln)
    # walk, tracking ::: directive stack
    paras = []           # list of (text, in_directive)
    cur, cur_indir = [], False
    stack = []           # directive-name stack
    def flush():
        nonlocal cur, cur_indir
        if cur:
            txt = " ".join(cur).strip()
            if txt: paras.append((txt, cur_indir))
        cur, cur_indir = [], False
    for ln in out_lines:
        s = ln.strip()
        m_open = re.match(r"^:::+\{([a-z\-]+)\}", s)
        if m_open:
            flush(); stack.append(m_open.group(1)); continue
        if re.match(r"^:::+\s*$", s):
            flush()
            if stack: stack.pop()
            continue
        if re.match(r"^:[a-z][a-z\-]*:", s):   # directive option line
            continue
        inside_skip = any(b in SKIP_BLOCKS for b in stack)
        if inside_skip:
            continue
        if s == "":
            flush(); continue
        if re.match(r"^#{1,6}\s", s) or re.match(r"^\([a-z0-9\-]+\)=\s*$", s):
            flush(); continue   # heading / label line
        cur.append(ln.strip())
        cur_indir = bool(stack)
    flush()
    return paras

def section_id(path):
    first = open(path, encoding="utf-8").readline().strip()
    m = re.match(r"^\(([a-z0-9\-]+)\)=\s*$", first)
    return m.group(1) if m else os.path.basename(path)

claims = []
for path in sorted(glob.glob("content/0[1-9]_*.md")):
    sec = section_id(path)
    src = path.replace("\\", "/")
    for p_idx, (ptext, indir) in enumerate(prose_paragraphs(path)):
        for s_idx, sent in enumerate(split_sentences(ptext)):
            keys = cite_keys_in(sent)
            if not keys:
                continue
            keys = list(dict.fromkeys(keys))          # de-dup, keep order
            norm = normalize(sent)
            cid = "clm_" + hashlib.sha1((sec + "|" + norm + "|" + "|".join(sorted(keys))).encode()).hexdigest()[:16]
            ctxs, dois, conflicts = [], [], []
            for k in keys:
                doi = key2doi.get(k)          # key -> doi
                dois.append(doi)
                f = FIND.get(k, {})
                cat = (doiver.get(k) or {}).get("cat", "")
                ta = f.get("text_access")
                psrc = {"fulltext": "full_text", "abstract_only": "abstract"}.get(ta, "metadata_only")
                ctxs.append({
                    "cite_key": k, "doi": doi,
                    "role": ROLE_FROM_ARG.get(f.get("argument_role"), "background"),
                    "supporting_passage": (f.get("claim_source_sentence") or None),
                    "passage_source": psrc,
                    "direction_match": cat in ("VERIFIED", "MINOR"),
                    "notes": None,
                })
                for (ok, nat) in CONFLICTS_BY_KEY.get(k, []):
                    conflicts.append({"conflict_type": "citation_key", "target_id": ok, "notes": nat})
            # seed modality from the strongest replication signal among cited findings
            repls = [FIND.get(k, {}).get("replication_status") for k in keys]
            modality = "established"
            for pref in ("contested", "disputed", "unreplicated", "single-study", "replicated"):
                if pref in repls:
                    modality = REPL_TO_MODALITY.get(pref, "established"); break
            roles = [c["role"] for c in ctxs]
            # evidence_relation from roles only; conflicts[] kept as an uncertainty signal, not a relabel
            evrel = ("directly_supported" if roles and all(r == "direct_support" for r in roles) else
                     "partially_supported" if any(r in ("direct_support", "partial_support") for r in roles) else
                     "indirectly_supported")
            claims.append({
                "claim_id": cid, "section_id": sec, "source_file": src,
                "paragraph_index": p_idx, "sentence_index": s_idx,
                "claim_text": clean_display(sent), "normalized_claim": norm or sent.strip().lower()[:80],
                "claim_type": "empirical", "claim_scope": {"biological": None, "computational": None,
                    "clinical": None, "methodological": None, "conceptual": None},
                "claim_polarity": "positive", "modality": modality, "entities": [],
                "citation_keys": keys, "dois": dois,
                "citation_contexts": ctxs, "evidence_relation": evrel,
                "conflicts": conflicts, "knowledge_edges": [],
                "in_directive": indir,
                "created_by_phase": "trust_seed", "updated_by_phase": "trust_seed",
                "validation_status": "pending",
            })

# de-dup identical claim_ids (same sentence repeated) keeping first
seen, uniq = set(), []
for c in claims:
    if c["claim_id"] in seen: continue
    seen.add(c["claim_id"]); uniq.append(c)

os.makedirs("knowledge", exist_ok=True)
json.dump({"claims": uniq}, open("knowledge/claim_seed_index.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# report
from collections import Counter
print("claim seeds:", len(uniq), "(raw", len(claims), ")")
print("distinct cite keys covered:", len(set(k for c in uniq for k in c["citation_keys"])))
print("claims inside admonitions (non-injectable margin):", sum(1 for c in uniq if c["in_directive"]))
print("citation_contexts with a supporting_passage:",
      sum(1 for c in uniq for x in c["citation_contexts"] if x["supporting_passage"]),
      "/", sum(len(c["citation_contexts"]) for c in uniq))
print("claims with >=1 conflict:", sum(1 for c in uniq if c["conflicts"]))
print("modality dist:", dict(Counter(c["modality"] for c in uniq)))
print("per-section:", dict(Counter(c["section_id"] for c in uniq)))

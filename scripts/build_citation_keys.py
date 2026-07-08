#!/usr/bin/env python3
"""Phase 3: build citation_key_map.json + author_name_table.json from CrossRef metadata.
Deterministic. Global collision resolution (a/b/c suffixes ordered by DOI)."""
import json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

meta = json.load(open("provenance/crossref_metadata.json", encoding="utf-8"))

def ascii_name(s):
    if not s:
        return None
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Za-z]", "", s)
    return s or None

# base key per DOI
base = {}
for r in meta:
    doi = r["doi"]
    fam = ascii_name(r.get("family"))
    yr = r.get("year")
    if fam and yr:
        b = f"{fam}{yr}"
    elif fam:
        b = f"{fam}NoYear"
    else:
        # fallback from DOI suffix
        tail = re.sub(r"[^A-Za-z0-9]", "", doi.split("/")[-1])[:10] or "Unknown"
        b = f"Ref{tail}"
    base.setdefault(b, []).append(doi)

# collision resolution -> unique keys
cite_key_map = {}   # doi -> key
for b, dois in base.items():
    dois_sorted = sorted(dois, key=str.lower)
    if len(dois_sorted) == 1:
        cite_key_map[dois_sorted[0]] = b
    else:
        suffixes = "abcdefghijklmnopqrstuvwxyz"
        for i, doi in enumerate(dois_sorted):
            suf = suffixes[i] if i < len(suffixes) else f"_{i}"
            cite_key_map[doi] = f"{b}{suf}"

# author_name_table keyed by cite_key
meta_by_doi = {r["doi"]: r for r in meta}
author_name_table = {}
for doi, key in cite_key_map.items():
    r = meta_by_doi[doi]
    fams = r.get("all_families") or []
    if len(fams) == 1:
        disp = fams[0]
    elif len(fams) == 2:
        disp = f"{fams[0]} and {fams[1]}"
    elif len(fams) >= 3:
        disp = f"{fams[0]} et al."
    else:
        disp = (r.get("family") or "Anonymous")
    author_name_table[key] = {
        "doi": doi,
        "family": r.get("family"),
        "given": r.get("given"),
        "all_families": fams,
        "year": r.get("year"),
        "title": r.get("title"),
        "container": r.get("container"),
        "citet_display": disp,
        "crossref_ok": r.get("ok", False),
    }

json.dump(cite_key_map, open("provenance/citation_key_map.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(author_name_table, open("provenance/author_name_table.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# stats
n = len(cite_key_map)
uniq_keys = len(set(cite_key_map.values()))
failed = [d for d, r in meta_by_doi.items() if not r.get("ok")]
print("DOIs:", n, "| unique cite keys:", uniq_keys, "| collisions_resolved:", sum(1 for b, ds in base.items() if len(ds) > 1))
print("CrossRef unresolved:", len(failed))
assert n == uniq_keys, "KEY COLLISION — non-unique keys!"
print("KEY UNIQUENESS: OK")

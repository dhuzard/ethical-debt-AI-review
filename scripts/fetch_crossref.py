#!/usr/bin/env python3
"""Phase 3 helper: fetch CrossRef metadata for every unique DOI. Pure I/O, no model tokens.
Saves provenance/crossref_metadata.json incrementally so partial progress survives."""
import urllib.request, urllib.parse, json, time, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
UA = "EthicalDebtReview/1.0 (mailto:damien@metadatapp.net)"

dois = [r["doi"] for r in json.load(open("provenance/all_dois.json", encoding="utf-8"))]
out_path = "provenance/crossref_metadata.json"
# resume support
done = {}
if os.path.exists(out_path):
    try:
        for rec in json.load(open(out_path, encoding="utf-8")):
            done[rec["doi"].lower()] = rec
    except Exception:
        done = {}

def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        m = json.load(r)["message"]
    au = m.get("author", []) or []
    fam = [a.get("family") for a in au if a.get("family")]
    yr = None
    for k in ("issued", "published-print", "published-online", "created"):
        dp = (m.get(k) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            yr = dp[0][0]; break
    return {
        "doi": doi, "ok": True,
        "family": fam[0] if fam else None,
        "given": (au[0].get("given") if au else None),
        "all_families": fam,
        "year": yr,
        "title": (m.get("title") or [None])[0],
        "container": (m.get("container-title") or [None])[0],
        "type": m.get("type"),
    }

records = []
n_new = 0
for i, doi in enumerate(dois):
    key = doi.lower()
    if key in done:
        records.append(done[key]); continue
    try:
        rec = fetch(doi); n_new += 1
    except Exception as e:
        rec = {"doi": doi, "ok": False, "error": type(e).__name__ + ":" + str(e)[:80],
               "family": None, "given": None, "all_families": [], "year": None,
               "title": None, "container": None, "type": None}
    records.append(rec)
    time.sleep(0.12)
    if len(records) % 40 == 0:
        json.dump(records, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("progress:", len(records), "/", len(dois), "new_fetched:", n_new, flush=True)

json.dump(records, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
ok = sum(1 for r in records if r["ok"])
print("DONE. total:", len(records), "resolved:", ok, "failed:", len(records) - ok, flush=True)

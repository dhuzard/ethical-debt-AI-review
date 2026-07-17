#!/usr/bin/env python3
"""Stage 3c helper: map each cite_key to its worst (lowest) trust band across the claims that
use it, for inline citation coloring. Writes knowledge/cite_trust_bands.json = {cite_key: band}.
"""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
claims = json.load(open("knowledge/claim_graph.json", encoding="utf-8"))["claims"]

RANK = {"high_trust": 3, "moderate_trust": 2, "low_trust": 1, "critical_or_unreliable": 0}
worst = {}   # key -> (rank, band, min_score)
for c in claims:
    band = c["trust_score"]["trust_label"]; sc = c["trust_score"]["overall_score"]
    for k in c["citation_keys"]:
        if k not in worst or RANK[band] < worst[k][0] or (RANK[band] == worst[k][0] and sc < worst[k][2]):
            worst[k] = (RANK[band], band, sc)

out = {k: {"band": v[1], "min_score": v[2]} for k, v in worst.items()}
json.dump(out, open("knowledge/cite_trust_bands.json", "w", encoding="utf-8"), indent=0, ensure_ascii=False)
from collections import Counter
print("cite keys banded:", len(out), "|", dict(Counter(v["band"] for v in out.values())))

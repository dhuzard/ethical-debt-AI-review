#!/usr/bin/env python3
"""Stage 3a (TRUST): inject one `:::{trust-claim} :claim-id:` directive after each top-level
claim-bearing paragraph, so the trust-claim plugin renders a margin card beside it. Reversible
and idempotent: existing trust-claim blocks are stripped before re-injection.

Usage:  python scripts/inject_trust_directives.py         # strip + inject
        python scripts/inject_trust_directives.py --strip # remove all trust-claim blocks
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
STRIP_ONLY = "--strip" in sys.argv

SKIP_BLOCKS = ("figure", "dropdown", "margin", "evidence-explorer", "authorship-explorer", "trust-claim")

def strip_trust(lines):
    """Remove :::{trust-claim} ... ::: blocks (and a single trailing blank line)."""
    out, i = [], 0
    while i < len(lines):
        if re.match(r"^:::+\{trust-claim\}", lines[i].strip()):
            i += 1
            while i < len(lines) and not re.match(r"^:::+\s*$", lines[i].strip()):
                i += 1
            i += 1  # skip closing :::
            if i < len(lines) and lines[i].strip() == "":
                i += 1  # skip one blank line we added
            continue
        out.append(lines[i]); i += 1
    return out

def paragraph_end_lines(lines):
    """Reproduce build_claim_seed's paragraph indexing; return {para_index: last_line_idx}."""
    # strip fenced code, preserving indices
    proc, in_fence = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence; proc.append(""); continue
        proc.append("" if in_fence else ln)
    ends, stack = {}, []
    cur_lines, cur_indir, pidx = [], False, 0
    def flush():
        nonlocal cur_lines, cur_indir, pidx
        if cur_lines:
            ends[pidx] = cur_lines[-1]  # last original line index of this paragraph
            pidx += 1
        cur_lines, cur_indir = [], False
    for i, ln in enumerate(proc):
        s = ln.strip()
        if re.match(r"^:::+\{[a-z\-]+\}", s):
            flush(); stack.append(re.match(r"^:::+\{([a-z\-]+)\}", s).group(1)); continue
        if re.match(r"^:::+\s*$", s):
            flush()
            if stack: stack.pop()
            continue
        if re.match(r"^:[a-z][a-z\-]*:", s):
            continue
        if any(b in SKIP_BLOCKS for b in stack):
            continue
        if s == "" or re.match(r"^#{1,6}\s", s) or re.match(r"^\([a-z0-9\-]+\)=\s*$", s):
            flush(); continue
        cur_lines.append(i)
    flush()
    return ends

seed = json.load(open("knowledge/claim_seed_index.json", encoding="utf-8"))["claims"]
# top-level (margin-injectable) claims grouped by (file, paragraph_index)
by_file = {}
for c in seed:
    if c.get("in_directive"):
        continue
    by_file.setdefault(c["source_file"], {}).setdefault(c["paragraph_index"], []).append(c["claim_id"])

files = sorted(set(c["source_file"] for c in seed))
n_inject = 0
for f in files:
    lines = open(f, encoding="utf-8").read().split("\n")
    lines = strip_trust(lines)
    if STRIP_ONLY:
        open(f, "w", encoding="utf-8").write("\n".join(lines))
        continue
    ends = paragraph_end_lines(lines)
    inserts = []  # (after_line_idx, text)
    for pidx, cids in by_file.get(f, {}).items():
        if pidx not in ends:
            continue
        block = "".join(f"\n:::{{trust-claim}}\n:claim-id: {cid}\n:::" for cid in cids)
        inserts.append((ends[pidx], block))
        n_inject += len(cids)
    # insert bottom-up so earlier line indices stay valid
    for after, block in sorted(inserts, key=lambda x: -x[0]):
        lines[after] = lines[after] + block
    open(f, "w", encoding="utf-8").write("\n".join(lines))

print(("stripped trust-claim blocks from " if STRIP_ONLY else "injected ")
      + (f"{len(files)} files" if STRIP_ONLY else f"{n_inject} trust-claim directives across {len(files)} files"))

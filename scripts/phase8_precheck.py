#!/usr/bin/env python3
"""Phase 8 mandatory mechanical pre-checks (coordinator code, zero critic tokens):
1. Conflict survival: both DOIs of each package conflict appear as cite keys in the section .md
2. Figure caption audit: MANUAL_NUMBERING / NO_BOLD_TITLE / REDUNDANT_NAME_LABEL / NO_ANCHOR
3. Heading style audit: manual number prefix / wrapped / dash / mixed / inconsistent
4. Hardcoded cross-reference audit: §N, Section N.M, Sec. N in prose
"""
import json, os, re, pathlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

km = json.load(open("provenance/citation_key_map.json", encoding="utf-8"))
kml = {k.lower(): v for k, v in km.items()}
def ck(doi): return kml.get((doi or "").lower())

SECTIONS = {
    "02": "content/02_reproducibility_crisis.md",
    "03": "content/03_data_welfare_3rs.md",
    "04": "content/04_fair_preclinical_data.md",
    "05": "content/05_virtual_control_groups.md",
    "06": "content/06_nams_data.md",
    "07": "content/07_incentives.md",
    "08": "content/08_governance_pathways.md",
}

def extract_cite_keys(md_text):
    keys = set()
    for m in re.finditer(r"\{cite:[pt]\}`([^`]+)`", md_text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k:
                keys.add(k)
    return keys

print("=" * 70)
print("1. CONFLICT SURVIVAL PRE-CHECK (threshold >= 0.50)")
print("=" * 70)
conflict_fail = []
for num, path in SECTIONS.items():
    tex = pathlib.Path(path).read_text(encoding="utf-8")
    cited = extract_cite_keys(tex)
    pkg = json.load(open(f"evidence/evidence_section_{num}.json", encoding="utf-8"))
    confs = pkg.get("conflicts", [])
    if not confs:
        print(f" sec{num}: no conflicts in package")
        continue
    missing = []
    for c in confs:
        ka, kb = ck(c.get("paper_a_doi")), ck(c.get("paper_b_doi"))
        ha = ka and ka in cited
        hb = kb and kb in cited
        if not (ha and hb):
            missing.append((c.get("nature_of_conflict", "")[:60], ka, ha, kb, hb))
    surv = 1 - len(missing) / len(confs)
    tag = "OK" if surv >= 0.50 else "FAIL"
    print(f" sec{num}: {len(confs)} conflicts, survival={surv:.2f} [{tag}]  (both-cited={len(confs)-len(missing)})")
    if surv < 0.50:
        conflict_fail.append(num)
    for nat, ka, ha, kb, hb in missing[:12]:
        print(f"    missing: {nat!r} | A={ka}({'ok' if ha else 'MISS'}) B={kb}({'ok' if hb else 'MISS'})")

print()
print("=" * 70)
print("2. FIGURE CAPTION AUDIT")
print("=" * 70)
# tolerant figure-block matcher: ::: {figure} ... up to closing :::
FIG_RE = re.compile(r"^:::\{figure\}[^\n]*\n(.*?)^:::\s*$", re.M | re.S)
fig_problems = []
for num, path in SECTIONS.items():
    text = pathlib.Path(path).read_text(encoding="utf-8")
    nfig = 0
    for m in FIG_RE.finditer(text):
        nfig += 1
        block = m.group(1)
        blines = block.splitlines()
        opts = {}
        caption_lines = []
        for ln in blines:
            om = re.match(r"^:([a-z]+):\s*(.*)$", ln)
            if om:
                opts[om.group(1)] = om.group(2)
            elif ln.strip():
                caption_lines.append(ln.strip())
        caption = caption_lines[0] if caption_lines else ""
        if re.match(r"\*\*Figure\s+\d+(\.\d+)?\*\*", caption):
            fig_problems.append((num, "MANUAL_NUMBERING", caption[:70]))
        if caption and not caption.startswith("**"):
            fig_problems.append((num, "NO_BOLD_TITLE", caption[:70]))
        if "name" in opts and "label" in opts and opts["name"] == opts["label"]:
            fig_problems.append((num, "REDUNDANT_NAME_LABEL", opts.get("name", "")))
        if "name" not in opts and "label" not in opts:
            fig_problems.append((num, "NO_ANCHOR", caption[:70]))
    print(f" sec{num}: {nfig} figure blocks parsed")
if fig_problems:
    for num, typ, det in fig_problems:
        print(f"    sec{num} {typ}: {det}")
else:
    print("    -> no figure caption problems")

print()
print("=" * 70)
print("3. HEADING STYLE AUDIT (manual-number / wrapped / dash / mixed)")
print("=" * 70)
_FENCE = re.compile(r"^(`{3,}|~{3,})")
_OPEN = re.compile(r"^:::\{[a-z]+\}")
_CLOSE = re.compile(r"^:::\s*$")
def skip_mask(lines):
    mask = [False] * len(lines)
    in_fence, depth = None, 0
    for i, ln in enumerate(lines):
        f = _FENCE.match(ln)
        if in_fence is None and f:
            in_fence = f.group(1); mask[i] = True; continue
        if in_fence and ln.startswith(in_fence):
            mask[i] = True; in_fence = None; continue
        if in_fence is not None:
            mask[i] = True; continue
        if _OPEN.match(ln):
            depth += 1; mask[i] = True; continue
        if depth and _CLOSE.match(ln):
            depth -= 1; mask[i] = True; continue
        if depth:
            mask[i] = True
    return mask
head_problems = []
h1_styles = {}
for num, path in SECTIONS.items():
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    skip = skip_mask(lines)
    h1n = h2n = None
    for i, line in enumerate(lines):
        if skip[i]:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        level, body = len(m.group(1)), m.group(2).rstrip()
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if (nxt.strip() and i + 1 < len(skip) and not skip[i + 1] and
                not nxt.lstrip().startswith(("#", ":", "-", "|", "`", "*", ">", "1.", "2."))):
            head_problems.append((num, "WRAPPED_HEADING", f"L{i+1}: {body[:50]} -> {nxt[:30]}"))
        num_match = re.match(r"^(\d+(\.\d+)*)\.?\s+", body)
        if num_match:
            head_problems.append((num, "MANUAL_NUMBER_PREFIX", f"L{i+1} H{level}: {body[:60]}"))
        if "–" in body or "—" in body:
            head_problems.append((num, "INCONSISTENT_DASH", f"L{i+1} H{level}: {body[:60]}"))
        if level == 1 and h1n is None:
            h1n = bool(num_match); h1_styles[num] = "numbered" if h1n else "unnumbered"
        if level == 2 and h2n is None:
            h2n = bool(num_match)
    if h1n is not None and h2n is not None and h1n != h2n:
        head_problems.append((num, "MIXED_H1_H2_STYLE", f"H1={'num' if h1n else 'unnum'} H2={'num' if h2n else 'unnum'}"))
if len(set(h1_styles.values())) > 1:
    for num, s in h1_styles.items():
        head_problems.append((num, "INCONSISTENT_ACROSS_SECTIONS", f"H1 is {s}"))
if head_problems:
    for num, typ, det in head_problems:
        print(f"    sec{num} {typ}: {det}")
else:
    print(f"    -> no heading problems (all H1 styles: {set(h1_styles.values())})")

print()
print("=" * 70)
print("4. HARDCODED CROSS-REFERENCE AUDIT (prose only)")
print("=" * 70)
XREF = [re.compile(r"§\s*\d+"), re.compile(r"\bSection\s+\d+\.\d+"), re.compile(r"\b[Ss]ec\.\s*\d+")]
xref_problems = []
for num, path in SECTIONS.items():
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    skip = skip_mask(lines)
    for i, line in enumerate(lines):
        if skip[i]:
            continue
        for rx in XREF:
            if rx.search(line):
                xref_problems.append((num, f"L{i+1}", line.strip()[:70]))
if xref_problems:
    for num, loc, det in xref_problems:
        print(f"    sec{num} {loc}: {det}")
else:
    print("    -> no hardcoded cross-references")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("conflict_survival_failures:", conflict_fail or "NONE")
print("figure_caption_problems:", len(fig_problems))
print("heading_problems:", len(head_problems))
print("hardcoded_xref_problems:", len(xref_problems))

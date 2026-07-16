# The Ethical Debt

### Why wasting animal data is wasting animal lives

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21213212.svg)](https://doi.org/10.5281/zenodo.21213212)

A critical literature review on **data welfare** — the argument that stewardship of animal-derived data is a dimension of animal welfare and of the 3Rs, not a technical afterthought. Synthesising evidence from **1,337 unique papers**, it makes the case that wasting animal-derived data is an unpaid *ethical debt*: because generating the data imposed a welfare cost, allowing it to become unfindable, unusable, or unreused is itself a welfare harm — one ultimately discharged in the further animal lives needed to regenerate what was lost.

> [!IMPORTANT]
> **This review was generated with substantial AI assistance.** Under human direction and supervision, AI-directed components searched PubMed, Europe PMC, OpenAlex, and CrossRef; extracted and independently verified evidence from ~1,337 papers with a DOI recorded for every finding; drafted the sections, figures, and Methods; and ran blinded assessments of the figures, prose, and citations. A human researcher conceived the review, set its scope and thesis, and approved outputs at each phase gate. Every factual claim links to a specific paper via DOI. See [Methods](content/Methods.md), [Provenance](content/provenance.md), and the [Evidence Database](content/evidence_database.md).

## The Argument

Animals are used to generate biomedical knowledge at a real and deliberate welfare cost, yet a large and measurable fraction of the resulting data is never published, shared, or made reusable. The review establishes that this debt is real and quantifiable, then weighs four mechanisms for repaying it:

1. **FAIR data** — making data Findable, Accessible, Interoperable, and Reusable.
2. **Virtual control groups** — reusing curated control-animal data, which converges on roughly a quarter fewer control animals but awaits regulatory acceptance.
3. **New approach methodologies (NAMs)** — disciplined stewardship of the high-dimensional data that non-animal methods generate.
4. **Incentives and governance** — reforming the systems that currently price stewardship at near-zero.

A recurring finding: enforced requirements move behaviour where passively endorsed ones do not, though effects are heterogeneous and field-wide sharing remains near the floor. The central claim is simple and robust — because animals paid for the data with their lives, repaying the debt saves animals.

## Contents

The manuscript is written in [MyST Markdown](https://mystmd.org) under `content/`:

| File | Section |
|------|---------|
| `00_frontmatter.md` | Abstract, authorship, AI-disclosure |
| `01_introduction.md` | Introduction |
| `02_reproducibility_crisis.md` | The reproducibility crisis in preclinical research |
| `03_data_welfare_3rs.md` | Data welfare and the 3Rs |
| `04_fair_preclinical_data.md` | FAIR preclinical data |
| `05_virtual_control_groups.md` | Virtual control groups |
| `06_nams_data.md` | Data from new approach methodologies |
| `07_incentives.md` | Research incentives |
| `08_governance_pathways.md` | Governance pathways |
| `09_conclusion.md` | Conclusion |
| `Methods.md` | Full protocol and pipeline record |
| `evidence_database.md` | Interactive per-section evidence explorer |
| `provenance.md` | Pipeline execution summary |

Supporting material:

- `figures/` — 21 section figures plus one pipeline schematic, each paired with a self-contained, re-executable notebook rendered from the recorded evidence.
- `evidence/` — Per-cluster evidence packages, citation maps, and author tables (1,451 extracted findings, 90 recorded inter-study conflicts, 60 cross-study figure comparisons), each traceable to a source paper by DOI.
- `content/references.bib` — The verified bibliography; every citation in the text resolves to an entry here.
- `provenance/`, `phase_ledger.json`, `scope.json`, `scaffold.json` — Machine-readable records of the staged protocol.

## How It Was Produced

The review was produced by a staged, gated computational protocol (the Expert Review Pipeline v29) under human supervision, with **actor-critic separation**: independent assessment stages were kept blind to the stages whose output they judged, so figure audits, prose critiques, and citation checks were carried out by components that had not produced the material under review.

- **Discovery databases:** PubMed, Europe PMC, and OpenAlex, with CrossRef for bibliographic metadata and DOI verification.
- **Corpus:** 1,337 unique papers after cross-group de-duplication, organised into eight topic groups mapped onto the body sections.
- **Citation integrity:** All citation keys and author names come from the CrossRef API — never from model memory — to prevent hallucinated references. Every citation-claim pair was verified against the cited paper's metadata and, where retrievable, full text.

The stage specifications and per-phase pass/fail gate definitions live in `skills/`; the executed status of each stage is recorded in `phase_ledger.json`. See [Methods](content/Methods.md) and [Provenance](content/provenance.md) for the full protocol.

## Building the Site

The manuscript renders to a static site with [`mystmd`](https://mystmd.org):

```bash
npm install -g mystmd
npm install yaml
myst build --html      # output in _build/html
```

Figures are committed PNGs, so the build does not re-execute notebooks and needs no Python. To rebuild a figure, run its notebook in `figures/`. PDF/LaTeX exports use the template under `latex/` (`myst build --pdf`).

Deployment is configured for Netlify (`netlify.toml`). Interactive elements are provided by three MyST plugins in `plugins/`:

| Plugin | What it does |
|--------|--------------|
| `authorship-plugin.mjs` | Renders the interactive CRediT authorship widget |
| `evidence-explorer-plugin.mjs` | Loads evidence packages into an interactive browser |
| `figure-lightbox-plugin.mjs` | Click-to-zoom lightbox for inline figures |

## Authors

- **Damien Huzard** (Neuronautix) — corresponding author; conceived the review's topic, scope, and central argument, and validated outputs at each phase gate. ORCID [0000-0003-4820-7951](https://orcid.org/0000-0003-4820-7951).
- **Claude** (Anthropic) — AI research tool; literature investigation, data curation, original drafting, visualization, and blinded formal analysis.
- **Codex** (OpenAI) — AI research tool; supporting review, editing, and tooling.

Full CRediT roles and contribution levels are in `content/authors.yml` and the interactive authorship widget on the site.

## License

MIT — see [LICENSE](LICENSE).

## How to Cite

This review was produced using the Computational Review Template. If you use the template, please cite:

```bibtex
@software{lecoq_2026_21213212,
  author       = {Jérôme Lecoq},
  title        = {AllenNeuralDynamics/ComputationalReviewTemplate},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.21213212},
  url          = {https://doi.org/10.5281/zenodo.21213212}
}
```

> Lecoq, J. (2026). *AllenNeuralDynamics/ComputationalReviewTemplate* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.21213212

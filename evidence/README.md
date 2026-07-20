# Evidence Directory

This directory contains the structured evidence packages that power the
interactive Evidence Explorer widget on the review site.

## Expected File Format

The `evidence-explorer-plugin.mjs` scans this directory for the canonical
per-section JSON files named:

```
evidence_section_01.json
evidence_section_02.json
...
evidence_section_NN.json
```

This review has one file for each section, including the Introduction and
Conclusion synthesis packages. For compatibility with older template outputs,
the loader also accepts `section_NN_evidence_package.json` and
`section_NN_evidence.json`; a canonical file wins if both forms exist.

## JSON Schema

Each per-section file must contain:

```json
{
  "section_title": "Human-readable section title",
  "findings": [
    {
      "claim": "What the paper found",
      "claim_source_sentence": "Verbatim sentence from paper",
      "effect_size": "Quantitative magnitude (or 'not reported')",
      "effect_size_source_sentence": "Verbatim sentence supporting the effect size",
      "n": 0,
      "study_system": "mouse | human | ...",
      "replication_status": "independently_replicated | replication_unknown | contested",
      "replication_evidence_dois": ["10.xxxx/..."],
      "doi": "10.xxxx/...",
      "text_access": "fulltext | abstract_only",
      "evidence": "Optional supporting context"
    }
  ],
  "conflicts": [
    {
      "paper_a_doi": "10.xxxx/...",
      "paper_b_doi": "10.xxxx/...",
      "nature_of_conflict": "Description",
      "resolution_status": "unresolved | partially_resolved | resolved"
    }
  ],
  "figure_data": [],
  "unreplicated_claims": [],
  "evidence_gaps": [],
  "strongest_evidence": {},
  "weakest_evidence_cited": {},
  "unique_papers": 0,
  "total_findings": 0
}
```

## How Files Are Generated

The pipeline's Phase 5 (Evidence Curation) builds per-section evidence
packages from the raw cluster evidence. Phase 14 (Assembly) should split
and copy these into this directory.

`unique_papers` and `total_findings` are optional. The explorer derives finding
counts from `findings[]` and paper counts from unique finding DOI/citation keys.
A combined `evidence_database.json` may also be generated, but the explorer does
**not** read it directly — it requires the individual per-section files.


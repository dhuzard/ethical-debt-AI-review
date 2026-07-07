# Original Review Request

**Project ID:** `dhuzard/ethical-debt-AI-review`
**Captured at:** 2026-07-06
**Pipeline:** Expert Review Pipeline v29 (`skills/comprev-orchestrator-v29.md`)
**Verbatim source:** [`provenance/review_request.txt`](review_request.txt)
**SHA256 (review_request.txt):** `7f4e02e859cde126d8d2d2c6ef608c9bc36a7ed67b19adf78f76ee5917f3971e`

---

## Verbatim user prompt

> Start a comprehensive critical literature review titled: "The Ethical Debt""
>
> The three files in skills/ define the complete pipeline:
>
> skills/comprev-orchestrator-v29.md — The coordinator protocol. Read this FIRST.
> It defines the routing across 21 phases, gate artifacts, and the session protocol.
> Per-phase rules live in the agent skills, which the coordinator loads on demand.
>
> skills/comprev-reviewer-agent.md — The worker skill for LITREVIEW agents.
> Pass this to every LITREVIEW delegation so the agent can load it.
>
> skills/comprev-figure-construction.md — Already published as a skill on LITREVIEW agents.
> Section writers load it for figure production.
>
> GitHub Repository: https://github.com/dhuzard/ethical-debt-AI-review
> Push all outputs to this repo in Phase 20.
>
> Evidence parameters:
> - Target ≥200 papers per cluster, snowball 2 rounds
> - Saturation criterion: <2% new unique in last 100
> - Total bibliography target: ≥1000
>
> Table of Contents:
> 1. Introduction
> 2. [Your Section 2]
> 3. [Your Section 3]
> ...
> N. Conclusion

---

## Editorial note

The prompt was submitted as a multi-line message and is reproduced above with
its original line breaks preserved. The only mechanical change applied in this
rendering is blockquote prefixing (`> `) required by the three-section format;
blank lines between the prompt's paragraphs are preserved as empty blockquote
lines. No wording, ordering, punctuation, or the table-of-contents structure has
been altered. The byte-for-byte original — including the trailing double quote in
the title line `"The Ethical Debt""` — is preserved at
[`provenance/review_request.txt`](review_request.txt) for audit.

# Scientific reviewer instructions

Review decisions are human scientific judgments. Automation may prepare records,
validate their structure, and merge them deterministically, but it must not choose
an outcome or invent a rationale.

## Workflow

1. Select claims from `knowledge/review_priority.json`; the calibration subset is
   intended for checking reviewer consistency before the full queue.
2. Read the exact claim, its source paragraph, every citation context and verified
   passage, conflicts, cap reasons, and the corresponding entry in
   `SCIENTIFIC_REVIEW_QUEUE.md`.
3. Record one independent review as `independently-reviewed`. Use `adjudicated`
   only after the designated human adjudicator resolves the outcome.
4. State what evidence was considered and why the action follows. Do not use TRUST
   score alone as the rationale.
5. Never edit an existing decision. A changed conclusion is a new decision that
   cites the earlier decision in its rationale.

## Data entry

Copy `knowledge/examples/human_review_decision.example.json`. Required fields are
`decision_id`, `claim_id`, `action`, `state`, `reviewer_id`, `recorded_at`, and
`rationale`. A decision that changes prose must also include the exact original and
replacement Markdown and structured replacement claims.

Validate without changing the repository:

```bash
node scripts/merge-human-reviews.js --input completed-decisions.json > merged-preview.json
```

After a human confirms the preview, append it with `--apply`, then regenerate and
validate downstream artifacts. The hash chain makes edits to prior decisions fail.

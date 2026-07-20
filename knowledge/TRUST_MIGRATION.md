# TRUST rubric migration contract

The committed graph remains on rubric and schema version 2.0.0 until a separately
reviewed migration is approved upstream. A future rubric release does not authorize
in-place rescoring.

Every migration must:

1. pin the upstream rubric commit and record old/new schema and rubric versions;
2. copy the complete source graph and decision store to immutable migration input;
3. define field-level transformations and identify lossy or non-equivalent mappings;
4. preserve native v2 assessments and claim lineage instead of overwriting them;
5. regenerate into a new output path and compare counts before promotion;
6. route any changed scientific meaning or new judgment to human review;
7. validate schemas, directives, atoms, passages, caps, summaries, export semantics,
   and deterministic reruns; and
8. publish the migration as a release-bound change with rollback instructions.

Until those conditions can be met, an unknown future version is recorded as
unsupported rather than guessed or silently coerced.

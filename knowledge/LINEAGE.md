# Claim lineage

Claim identifiers are deterministic hashes of section identity and exact claim text.
Any wording change therefore creates a new ID rather than mutating the meaning of an
existing ID.

`trust_v1_to_v2_id_map.json` preserves the v1 → v2 mapping. Its targets must resolve
either to a current graph claim or to a source claim preserved in the append-only
human-review decision store. The repository validator enforces this rule.

For future releases, add a new version-to-version map rather than rewriting this one.
A split maps the earlier ID to the preserved review decision, whose `claims[]` records
identify the replacements. A merge or retirement must likewise retain the earlier
record and explain the transition. ORAtlas and other consumers should pin both the
review release and the lineage-map version.

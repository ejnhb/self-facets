# Codebook changelog

## 0.1 (2026-11-26)

First draft, written before the pilot.

- Study facets: `study_kind`, `unit_of_self`, `self_sense`, `object_of_study`,
  `construct`, `report_target`, `evidence`, `validated_against`, `varies`,
  `comparison`, `elicitation`.
- Claim facets: `stance`, `evidence_kind`, `disposition`.
- `self_sense` values `authorship` and `subject` are proposals added to the
  owner's original list. Review before relying on them.
- `stance` uses `inconclusive` where early discussion said "null", because
  `null` is a reserved word in YAML.

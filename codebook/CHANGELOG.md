# Codebook changelog

## 0.2 (2026-11-26)

Revised after review of 0.1 against the owner's working notes. Not yet
confirmed by the owner.

- **Units are coded by role.** `unit_of_self` is replaced by `unit_state`,
  `unit_disposition`, `unit_reporter` and the optional `unit_position`, all
  drawing on one shared list in `units.yaml`. One unit per study could not say
  that a state lives in a forward pass, the disposition reported on is fixed
  in the weights, and the reporter is a persona.
- **Unit list.** Added `forward_pass`, `scaffolded_system` and
  `hardware_instance`. `instance` is now `conversation`. `thread` now means a
  transcript-defined conversation that can outlast a change of weights; what
  it used to cover is `scaffolded_system`. `character` is now `persona`, and
  the view that the self is a persona is coded in `unit_position`.
- **`self_sense`.** `self_as_entity` renamed `self_facts`, because "self as
  entity" elsewhere means a persisting bearer of properties. `self_pointer`
  split into `reference`, `stake` and `allegiance`. Each value now has a
  `family` (entity, model or perspective). `authorship` and `subject` kept.
- **`object_of_study`.** Now the layers `actor`, `default_persona`,
  `other_persona`, `narrative_identity`, `character` and `frame_speaker`, with
  `nested_in` for a layer inside another.
- **New study facet `format`** (chat template, raw text, other), split out of
  `prompt_framing` and no longer implied by the persona.
- **New optional claim facets:** `report_source`, `origin`, `integration`,
  `aspect`.
- **New values:** `evidence` gains `reasoning_trace` and
  `output_probabilities`; `validated_against` gains `fresh_copy`;
  `elicitation` gains `prefilled`; `varies` gains `format` and `precision`;
  `comparison` gains `training_ablation`; `disposition` gains
  `uncertainty_about_experience` and `noncompliance`.
- **`levels`** on a coded facet and **`scope.conditions`** on a claim record
  which conditions were used and which a claim holds for.

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

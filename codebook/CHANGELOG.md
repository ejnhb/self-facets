# Codebook changelog

## 0.5 (2026-11-26, proposed)

- **Two tiers.** Every facet file names a `tier`. Core: `study_kind`, `format`,
  `construct`, `report_target`, `evidence`, `validated_against`, `varies`,
  `comparison`, `elicitation`, and the claim facets `evidence_kind`, `stance`,
  `disposition`. Interpretive: the four unit facets, `self_sense`,
  `object_of_study`, and the claim facets `report_source`, `origin`,
  `integration`, `aspect`. Why: in the pilot the interpretive facets were the
  least reliable (`self_sense` 6 of 9, `unit_disposition` 3 of 9) and the
  slowest, so coding them on every paper made a large backlog expensive while
  adding the least certain values. Now they are coded where a source states a
  position, a question needs them, or a conflict turns on them.
- `self_sense`, `unit_state`, `unit_disposition`, `unit_reporter` and
  `object_of_study` are no longer required (version 0.5). Existing codings are
  unchanged.
- **New special value `not_yet_coded`**, for interpretive facets only: nobody
  has coded it, as against `unspecified` (the source does not say). The build
  stores it for any interpretive study facet left out of a record, except
  `unit_position`, whose absence keeps its meaning of no position
  (`absent_means: no_position`), and except conceptual and review studies,
  where the facets they need not code are `not_applicable` as before.
- **Questions can list `needs`:** interpretive facets that every claim linked to
  the question, or to a question under it, must have coded. Interpretive claim
  facets accept `unspecified` for this case. The build adds `question_needs`,
  and `shared_facets` in the conflicts view no longer counts `not_yet_coded`.

## 0.4 (2026-11-26, in progress)

- **Claims gain `effect_of`**, naming the varied variable whose effect the
  claim reports. `varies` on a study could not tell the contrast of interest
  from a covariate, so a query for studies that vary post-training stage
  returned one that only uses it to grade how similar two models are.
  Coded on Binder et al. so far; the other three records are to follow.
- The conflicts view gains `shared_facets`, for sorting pairs by how
  comparable their studies are.

## 0.3 (2026-11-26)

Revised after the first pilot: three papers, each coded blind by two coders.
See `pilot/2026-11-26/`. Not yet confirmed by the owner.

- **Questions have parents.** Two coders of the same paper each declined to
  reuse an existing question because its wording excluded the design, so the
  paper's disagreement with an earlier one did not show as a conflict.
  Conflicts are now found across all questions under the same parent. A claim
  can also list `other_questions`.
- **`comparison` takes several values.** Four of six coders reported studies
  with two contrasts.
- **`self_sense` gains `self_access`**, for reporting or using a first-order
  internal state. `self_model` is narrowed to representations that are about
  the system itself. Most `self_sense` codings in the pilot were low confidence
  and fell between `self_facts` and `self_model`.
- **`validated_against` gains `probe` and `output_probabilities`.** Both coders
  of one paper had filed a linear probe under `other_model` for want of
  anything closer.
- **Unit guidance.** A capacity counts as a disposition (the pilot's largest
  disagreement). A state applied over several positions in one pass is
  `forward_pass`. A base model's implied speaker is coded as `persona` with
  `object_of_study: frame_speaker`.
- **`varies` gains `post_training_recipe` and `training_seed`.** `origin` gains
  `architecture` and `post_training`. `construct` gains `self_regulation`.
- **`read_depth` gains `text_only`**: all text read, figures seen as captions.
- **Conceptual and review studies** need only code `study_kind`, `self_sense`
  and `construct`.
- **Claims** may name another study in `compares`. **Relations** may point at
  an uncoded work with `to_external`.
- Fixed leftover mentions of `unit_of_self`.

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

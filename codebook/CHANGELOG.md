# Codebook changelog

## 0.10.2 (2026-11-27; bookkeeping only, facets unchanged and frozen at 0.10)

- **`read_depth: full_text`** now needs every figure a claim takes a result or value from to have been viewed, not every figure in the
  paper; figures not viewed are listed in `read_parts`. Two of the first four step-1 records (Betley, Fornasiere)
  had read it this way already. Agreed with the owner.

## 0.10.1 (2026-11-27; bookkeeping only, facets unchanged and frozen at 0.10)

- **`availability_status`** (enums): `released`, `not_released` or `unknown`, on the `code` and `data` artefacts
  every record now lists, with `url`, `ref` (the commit or revision read) and `read` (true, false, partial).
  Absence used to be ambiguous between "none released" and "not checked".

## 0.10 (2026-11-26, proposed)

From the first blind coding test (one paper, coded on a copy of the repo with its record removed, by two coders
from different model families).

- **New core study facet `output_route_control`** (internality): could the report reach the model through its own
  earlier output? `by_construction`, `scoring_rule`, `control_condition`, `none`. Backfilled on all 19 experimental
  studies from the sources. Moved out of `design/candidate-facets.md`, and added to `d-introspection-grounded`
  as Lindsey's criterion 3 (the same 35 claims match).
- **`elicitation`:** `not_applicable` when nothing the model does is measured (a probe reading an injected state);
  the intervention goes under `varies`.
- **`validated_against`** now also covers a decoder's reading in a study with no self-report, so a probe scored
  against an injection is `known_intervention`.
- **`varies` gains `initialisation`** (random networks set against trained ones, outside the trained model's run).
- **`comparison`:** sizes of one family are `cross_model`; checkpoints along one run are `within_lineage`.
- **Controls:** a result about a control or baseline takes no `effect_of` (CLAUDE.md).
- **Questions:** every yes/no question with a parent must give its `polarity` (validate now fails without it);
  all 25 were set, `direct` except `q-introspection-success-generalises`, now `none` (its "against" stances had been
  counted against `q-privileged-self-access`). Two frames tightened to self-report designs. New root question
  `q-injected-state-decodable` for probe-only designs.
- **Build:** `question_candidates` applies `requires` up the parent chain, and gains `missing_needs`: the
  interpretive facets a candidate's study has not coded that the question's tree needs.
- **Figures:** `scripts/fetch_paper.py` downloads a paper and renders its figure pages; CLAUDE.md points to it.

## 0.9 (2026-11-26, proposed)

- **Definitions** (`definitions/`): named logic over facets for what a design
  tests in one stated sense, with `construct` kept as the authors' label. One
  so far, `d-introspection-grounded` (Lindsey 2026, criteria 1 and 2), with
  criteria 3 and 4 recorded as not expressible.
- **One logic for frames, selectors, `requires` and definitions** (`all`,
  `any`, `not`, `def`, facet values, `model.post_training_reached`,
  `comparison.closest`). Existing frames and selectors keep working: a plain
  mapping is the AND of its facets.
- `requires` accepts `definitions`; views accept `substitute` (read a question
  with one definition in place of another).
- Build: `definitions`, `claim_definitions`, `construct_mismatches`.
- Four frames use the definition: `q-injected-state-report`,
  `q-introspection-differs-by-post-training`,
  `q-introspection-increases-with-capability`,
  `q-stabilisation-improves-introspection`.
- `design/candidate-facets.md` starts the list of things facets cannot yet say
  (internality, metacognitive representation, injection depth).

## 0.8 (2026-11-26, proposed)

- **Effects on claims:** `effect_presence` (required with `effect_of`) and
  `effect_direction` (optional, ordered variables). Backfilled on Binder et
  al.'s nine claims with `effect_of`; the other records still lack `effect_of`.
- **Questions reach claims by themselves.** `question_candidates` lists claims
  in frame-matching studies not yet tied to a question; `auto_stance` gives
  "does X change Y?" questions stances from `effect_presence`. Frames are now
  validated. On `q-self-prediction-advantage`, auto stances reproduce all five
  hand-made links.
- **Model roles** in studies: `subject`, `comparison`, `judge`, `data_source`
  (`{id, roles, note}`), replacing free-text `role`. Registry `variant_of` for
  seed variants. The build derives how closely compared models are related
  (`study_comparisons`, `study_closest_comparison`), and readings can select on
  `comparison.closest`.
- **`similarity_adjustment`** (core study facet): statistical, none, or
  not_applicable when there is no self-against-other comparison. With the
  derived relation, `r-similarity-uncontrolled` now selects only Binder et
  al.'s cross-prediction studies, no longer Song et al.'s own.

## 0.7 (2026-11-26, proposed)

- **The unit `persona` is renamed `speaker`** (`units.yaml`, used by the four
  unit facets), defined as the voice the network computes and speaks as. In
  the persona selection sense a persona is what post-training selects, which a
  base model's implied author is not; object_of_study still says which kind of
  speaker. 16 codings renamed.
- **Links move out of the records** into `links/<source id>.yaml`: a claim's
  question, stance and other questions are now link entries (45 moved, none
  lost). Linking is the question poser's judgement, so coding a paper no longer
  includes it.
- **Questions can `require` facet values** for a claim to count as evidence,
  inherited down the tree. `q-privileged-self-access` requires
  `evidence: self_report`; every claim already linked under it meets that.
- **Readings and views are built** (`readings/`, `views/`, `design/readings.md`):
  reading status enum, selectors on facets or `model.post_training_reached`,
  reclassify and reinterpret effects, and the view tables in the build. Two
  readings from published sources and two example views.
- **Models gain `post_training_reached`** (untrained, base, post_trained, sft,
  preference, rl, unspecified), filled for all 42 from the sources or the
  models' names, so readings can select on training history before pipelines
  are coded.
- Templates for links, readings and views; the source template drops the link
  fields; the question and model templates gain the new fields.

## 0.6 (2026-11-26, proposed)

- **Three new core facets**, coded on every study and backfilled on the 19
  non-conceptual studies from the papers' methods sections:
  - `reasoning`: none, chain of thought, or a reasoning model's own trace.
    Self-reports can change with reasoning, and the existing facets could not
    say whether it was allowed.
  - `system_prompt`: none, the developer's default, or custom. Kept apart from
    `format` (template or not) and `prompt_framing` (what is varied).
  - `report_readout`: free text, a generated short answer, the top-scoring
    option's logits, or a probability taken as the report. Pilot coders had
    to explain this in notes (a logit readout "never generated"). The rule
    separates `probability` (the probability is the report) from
    `validated_against: output_probabilities` (the probabilities are the
    yardstick); `evidence` and `validated_against` cross-refer.
  - `varies` gains `reasoning`.
- **`unit_position` follows the other interpretive facets.** Left out, it is
  `not_yet_coded`; a source with no position is `not_applicable`. The 20
  studies that left it out under the old rule (which meant no position found)
  now say `not_applicable`, with a note. `absent_means` is gone.
- **Question `polarity`** (direct, inverse, none) says which way a child
  points. The build flips the stances of inverse questions before looking for
  conflicts (`root_stances`, `question_roots.sign`); a polarity none question
  roots its own subtree.
- **`kind: which` questions** are answered by an `answer_facet` instead of a
  stance. The build stores answers in `claim_answers` and pairs of differing
  answers in `which_conflicts`.
- **Templates** (`templates/source.yaml`, `question.yaml`, `model.yaml`), each
  field annotated. `validate.py` fails if the source template lacks a facet
  the codebook has, or names one it lacks.

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

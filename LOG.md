# Session log

Newest first. Each entry: what changed, what is open, what needs a decision.

## 2026-11-26: codebook 0.6 (three core facets, polarity, which-questions, templates)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- `unit_position` brought in line with the other interpretive facets; the 20
  studies that left it out now code `not_applicable`, with a note saying why.
- Questions gain `polarity` and `kind: which` (with `answer_facet`). Used in
  the question set: `q-denial-precedes-post-training` now sits under
  `q-denial-is-post-training-policy`, and `q-report-diverges-from-representation`
  under `q-report-matches-direct-measure`, both inverse. Two which-questions
  added: `q-what-self-reports-draw-on` (report_source) and
  `q-where-denial-comes-from` (origin). Conflict counts are unchanged (159):
  no claim links to the new questions yet.
- Core facets `reasoning`, `system_prompt` and `report_readout`, and
  `varies: reasoning`.
- Templates and a "Coding a paper, in order" section in CLAUDE.md.

**Backfill: what was read** (11-26, through alphaXiv's PDF page extraction;
the original coders' `read_parts` are unchanged)

- Binder et al. v1: abstract, §1 to §5, App. A.1 to A.2.9, A.3.3, A.4.1 to
  A.4.2, A.5. The code was not read, so `system_prompt` is `unspecified`
  throughout; s6 (SAD and OpenAI Evals) is `unspecified` on all three.
- Lindsey v1: §1, §2.2 to 2.4, §4, §5 (parts), §6, §10.3, App. 12.1 to 12.4.2.
  The base-model prompt layout (s3) was not in the pages read; coded from the
  design, operational.
- Rubin et al. v2: everything but the figures as images.
- Song et al. v3: §1 to §4.1, App. A to C. What the instruct models' default
  chat templates contain is not stated; coded `developer_default`, operational.

**Tested** on throwaway copies: an inverse child's stance is flipped on the
root; two claims with different `report_source` answers to a which-question
make one `which_conflicts` row; a stance on a which-question, a bad polarity,
and a template missing a facet each fail validation.

**For the owner to decide**

- The three core facets and their values, especially `generated_choice`, which
  now covers a single item the prompt asks for (a character, a word) as well
  as an option chosen from a list.
- The two inverse placements and the two which-questions.

## 2026-11-26: codebook 0.5 (two tiers) and 28 proposed questions

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- Facets are split into a core tier, coded on every study, and an
  interpretive tier, coded when a source states a position, a linked question
  `needs` the facet, or a conflict turns on it (`codebook/README.md`, "Two
  tiers"; `CHANGELOG.md` 0.5). The five interpretive study facets that were
  required no longer are. No record changed: every existing coding stays.
- New special value `not_yet_coded`. The build stores it for interpretive study
  facets left out of a record. There are none today: every existing study
  codes them, and on the two conceptual studies the uncoded ones read as
  `not_applicable`, as before. `unit_position` keeps "absent means no
  position" (`absent_means`).
- Questions can list `needs`, inherited by every question under them.
  `validate.py` checks them on each linked claim and its study; the build adds
  a `question_needs` table; `shared_facets` no longer counts `not_yet_coded`.
  Tested on a throwaway copy: a claim linked to a question needing
  `report_source` and `unit_reporter` fails until both are coded, and
  `unspecified` passes.

**Added**

- 28 questions in 12 trees, for the questions the first users expect to look
  up: where self-reports come from, report against representation, experience
  denials (policy, refusal machinery, training data, before post-training),
  frames and personas, report against behaviour, development through training,
  stabilising the self-model, continuity through carried state, stated
  uncertainty, consent across framing. Every top-level question names its
  `needs` except the last two, which need nothing beyond core facets. None has
  a claim linked yet.

**For the owner to decide**

- The tier split and `needs`.
- The 28 questions: wording, parents, and `needs`. Three are deliberately
  separate trees because "yes" to one counts against another
  (`q-denial-precedes-post-training` against `q-denial-is-post-training-policy`;
  `q-report-diverges-from-representation` against
  `q-report-matches-direct-measure`).
- `q-self-representation-changes-in-midtraining` uses `post_training_recipe`
  and `pretraining_progress` in its frame; `varies` has no value for a
  mid-training contrast.

**Open**

- The first test: code a paper against the new questions at the core tier
  only, then deepen just the facets the questions need, and see whether that
  answers the question and how long each pass takes.

## 2026-11-26: first three records from the pilot

Coder: claude (claude-fable-5-2), working with the owner. Per paper: one
reconciling coder (claude-fable-5-2) and one blind checker (claude-opus-5-5).

**Added**

- `sources/lindsey2026-emergent-introspective-awareness.yaml` (8 studies, 47
  claims), `sources/rubin2026-closer-look-introspection.yaml` (3 studies, 15
  claims), `sources/song2025-fail-to-introspect.yaml` (4 studies, 22 claims),
  with their people, orgs, models and questions.
- Nine questions, five of them under `q-privileged-self-access`.
- The reconcilers' notes and the checkers' tables, under `pilot/`.

**Checked**

- Every claim in the three records was checked against the paper text by a
  coder who had not seen the coding: 83 of 84 supported, 1 overstated and
  corrected. The checkers' wording suggestions were applied.

**Decisions made in the merge, for the owner to confirm**

- Two reconcilers independently created `q-injected-state-report`; one wording
  was kept.
- `q-report-matches-probe` was moved from under `q-privileged-self-access` to
  under `q-report-matches-direct-measure`.
- The Allen Institute's org id is `allen-ai`.
- `unit_disposition` on Rubin's probe-only and no-prompt studies is `weights`
  at low confidence, against both pilot coders' `not_applicable`.

**Learned**

- The Binder and Song records now conflict under the parent question, and the
  facet difference includes trained against spontaneous elicitation, chat
  template against raw text, and behaviour against output probabilities.
- "Which studies of introspection vary training stage or recipe?" returns six
  studies. One of them (Song s2) codes `post_training_stage` because base and
  instruct pairs have their own coefficient, not because it tests the effect
  of post-training.

**Rules added after review with the owner**

- Read the paper and its code together where both exist.
- Look at the figures: the arXiv PDF can be downloaded and its pages read as
  images, which the pilot coders did not do. The three pilot records are
  `text_only` and should have their figure-dependent claims revisited.

**Added after review with the owner**

- `effect_of` on claims, and `shared_facets` on the conflicts view. The owner's
  view is that showing every conflict and filtering by facet is right, so
  nothing is hidden; the new column only allows sorting.

**Open**

- `effect_of` is coded on Binder et al. only. The Lindsey, Rubin and Song
  records need it, and need a pass over their figure-dependent claims now
  that figures can be read. Both are held until the owner says to go.
- Whether a representational property with no behaviour counts as a capacity
  for `unit_disposition`.
- The line between `forward_pass` and `conversation` for an injected state
  that is read back after further tokens.
- No value names the self as regulator, for studies of control over internal
  states.
- The splitting rule needs a tie-break when results are reported apart but
  the only conclusion drawn is a comparison with another study.
- The post-training question exists for Lindsey but Rubin's related claims
  are not linked to it.
- Binder et al. is still coded from the main text only and has not had a
  blind check. Its `llama-3.1-70b` entry may be the same model as the new
  `llama-3.1-70b-instruct`.
- Org kinds for the new orgs are unverified.

## 2026-11-26: first pilot and codebook 0.3

Coder: claude (claude-fable-5-2), working with the owner. Six blind coders
(three claude-fable-5-2, three claude-opus-5-5) each coded one of three papers
from a clean copy of the repo.

**Added**

- `pilot/2026-11-26/`: the six records and the coders' notes, with a summary.
- Codebook 0.3. See `codebook/CHANGELOG.md`.
- Question parents, `other_questions`, `compares`, `to_external`, and lighter
  coding for conceptual studies, in the scripts.
- A rewritten splitting rule and new rules on registries, artefacts, dates,
  questions and relations in `CLAUDE.md`.

**Learned**

- Agreement between the two coders was 87% on 126 facet codings over nine
  matched studies. It is an upper bound: both coders are Claude models, and
  some agreements were the same fallback value chosen for want of a fit.
- Splits matched study for study on the paper with one section per
  experiment, and did not match on the other two.
- With a parent question in place, the Binder and Song records conflict as
  they should, and the facet difference includes trained against spontaneous
  elicitation. This was checked in a scratch copy with one pilot record.

**Open**

- The pilot records are coded against 0.2 and are not in `sources/`. They need
  recoding against 0.3, reconciling (one record per paper, shared ids for
  questions, people, orgs and models) and a check of their numbers against the
  papers by a coder who has not seen them.
- 0.3 has not itself been piloted.
- The conflicts view does not show which models each side is scoped to, so two
  claims in one study that differ only by model show no difference.
- Mixed `basis` or `confidence` within one facet entry cannot be recorded
  apart from the note.
- `report_source` cannot record that a source rules a route out.

**For the owner to decide**

- Confirm or change codebook 0.3.
- Whether the first parent question, `q-privileged-self-access`, is worded as
  wanted. It will sit above most of the introspection literature.
- Still open from 0.2: `stake` and `allegiance`, the fifth `report_source`
  value, and whether `integration` is wanted yet. The pilot papers did not
  exercise them.

## 2026-11-26: codebook 0.2 after review

Coder: claude (claude-fable-5-2), working with the owner.

**Changed**

- Codebook 0.2. See `codebook/CHANGELOG.md` for the full list. The main
  changes: units coded by role, `self_sense` renamed and split with families,
  `object_of_study` as layers with nesting, a `format` facet, and four optional
  claim facets.
- `levels` on coded facets and `scope.conditions` on claims. The conflicts view
  now shows each side's conditions.
- Splitting rule in `CLAUDE.md` now covers models, and there is a rule against
  copying unpublished material into this repo.
- Binder et al. recoded against 0.2.

**Learned**

- Under role coding, Binder comes out as: no occurrent state studied,
  disposition fixed in the weights, reporter a persona. All operational.
- Binder's authors rule out training data as the source of the self-prediction
  advantage but do not say where the report's content comes from, so
  `report_source` cannot be coded. The facet has no way to record "not X".

**Open, in addition to the entry below**

- None of the new facets has been tried on a paper that needs it. The pilot
  should include at least one study each with an occurrent state, a
  non-default persona, a raw-text condition and a traced training origin.

**For the owner to decide**

- Confirm or change codebook 0.2. In particular: whether `stake` and
  `allegiance` earn their place beside `subject` and `authorship`; whether
  `report_source` should have the fifth value `context`; and whether
  `integration` is wanted at all at this stage.
- Whether the framework-derived vocabulary is cleared to be public. It is
  written here in general terms with no results or worked cases.

## 2026-11-26: first draft of the structure

Coder: claude (claude-fable-5-2), working with the owner.

**Added**

- Directory layout, README, `CLAUDE.md`, this log.
- Codebook 0.1: 11 study facets, 3 claim facets, bookkeeping enums.
- `scripts/validate.py`, `scripts/build.py`, `scripts/query.py`.
- One worked example: `sources/binder2024-looking-inward.yaml` (6 studies, 10
  claims), with the people, orgs, models and questions it needs.

**Learned from the worked example**

- Study granularity matters. The first pass put all of the paper's section 4
  into one study, and the conflict view then reported facet differences that
  were not real. It is now two studies.
- The facet diff between the supporting and opposing claims on
  `q-self-prediction-advantage` comes down to `varies: task`. That is correct
  but coarse: the facets do not say that the task was sycophantic
  answer-switching. A facet for the behaviour or property being reported on may
  be needed.
- Unit of self, sense of self and object of study were all `operational` for
  this paper. None is stated by the authors.

**Open**

- Binder et al. was coded from the main text of v1 only. Appendices were not
  read, so model lists for studies s5 and s6 and several details are flagged in
  the record. Venue, code URL and dataset URL are not filled.
- All five model records have `stage: null`. No pipelines are coded yet.
- Org kinds were filled from general knowledge and not checked.
- ORCIDs are all null.

**For the owner to decide**

- Review the codebook, especially `self_sense` (two proposed values,
  `authorship` and `subject`) and `unit_of_self` (`character` as a unit).
- Licence for data and codebook (CC BY 4.0 was discussed).
- Whether to add a facet for the specific behaviour or property reported on.
- The remaining twelve pilot papers are not yet coded.

# Open

What is open in this repo: decisions waiting on the owner, proposed codebook changes, known gaps in records, and
things to watch. It replaces the session log (`LOG.md`, closed 2026-11-27 and kept for its history).

This file is rewritten, not appended to. Add an item when you find it; remove it in the pull request that resolves
it, and say so in the pull request description. What was done, and why, lives in git history and the pull request
descriptions. Keep each item to a few lines and point to the record, claim or pull request it comes from.

Items carried over from `LOG.md` are marked *(log)*; they were checked against the repo as it stood on 2026-11-27,
not re-read in their sources.

## Waiting on the owner

- **Construct for Betley et al.:** `[self_knowledge, self_prediction]` for "behavioral self-awareness", with
  `introspection` added on s2 and `self_knowledge` alone on s7. Confirm. *(log)*
- **The pilot's blind-test codings:** whether they go into `pilot/` (they are codings of a published paper; the
  reference coding used for comparison is not public). *(log)*
- **The blind-test branches** `blind-test` and `blind-binder` can be deleted once the owner has what he needs from
  them. *(log)*
- **The framework-derived vocabulary** (codebook 0.2): cleared to be public? It is written in general terms, with
  no results or worked cases. *(log)*

## Implementing the 2026-11-28 review

Codebook 0.11 (values, mechanics, rules) and the build changes are in. Still to come, each in its own pull
request:

- **Questions and links:** an optional `measure:` on questions ("how well" by which measure); a designed-or-post-hoc
  mark on links (`unspecified` allowed); automatic stances with each yes/no question saying which effect counts as
  support, and the automatic share of links tracked; `q-introspection-changes-in-training` as the parent of
  `q-introspection-differs-by-post-training` and a new pretraining question; an inference-time child of
  `q-stabilisation-reduces-drift`, with the family's parent reworded to "training or intervention"; unprompted
  drift by topic at the top level; `q-self-information-in-internals` as the parent of the probe-only questions
  (`q-injected-state-decodable` and the `q-correctness-*` questions); the four loose links below dropped.
- **Registries:** an instruments registry (lenses, released SAEs, named steering vectors and probes), for
  instruments that are named and released or used by more than one record; a `model_organism` model role;
  `layers` on models a `layer` study uses (the build's `study_layer_depths` needs them).
- **Automatic stances:** each yes/no question with `auto_stance` to say which effect counts as support
  (`supports:`), and `better` on the claims those questions read.
- **Recheck after 0.11** (studies coded with a nearest value or `unspecified` under the freeze):
  - `varies`: Ji-An/Li (PR #16), Lu s1 and s8, Moreno Cencerrado s1 (`layer`; c2 and c18 then take `effect_of`);
    Fornasiere s11 (`in_context_examples`); Comsa s2 and Goel s4 (`sampling_setting`); Moreno Cencerrado s1
    (`training_data_amount`).
  - `report_target`: Betley s8, s9 (`other_behaviour`); Comsa s2 (`inference_setting`).
  - `report_source`: Betley, Song c22 (`training_generalisation`); Comsa c3 (`human_mimicry`); the other
    `report_source` codings, for implicit routes and routes ruled out.
  - `construct`: Kim s2, s6 (`mind_attribution`), s3, s4 (`beliefs_values`), s5, s7 (`general_capability`); Lu s1,
    s2, s5 (`persona_representation`); Hao s1 to s4 (`self_conception`); Goel s5 (`planning`).
  - Units: Comsa s3 (`response`). The one `conversation` coding, Lindsey s6, is across turns and stays.
  - `evidence`: Hao s1, s3, s4 (`self_regarding_behaviour`). `elicitation`: Goel s1 to s4 (`teacher_forced`).
    `validated_against`: Comsa s1 (`known_properties`). `comparison`: Binder's cross-prediction studies
    (`study_trained_control`).
  - Effects: Song c8 to c10 (now `effect_direction` on an ordered `self_vs_other`); `better` on claims that report a
    performance measure, starting with those linked to yes/no questions.

## After 0.11 (decided to wait)

- **Agreement:** low agreement on a facet in blind tests first triggers a review of its definition (clarify, worked
  examples); only if coders still disagree is it demoted to interpretive, merged or dropped. One coder's error is
  fixed in the record and does not count against the facet. The threshold is set once there are enough matched
  studies and coders from more than one family.
- **`nested_in` on unit facets,** for the two persona views (`units.yaml` notes), once a coded source argues one.
- **A result block on claims** (n, estimate, interval, replication within the paper), only for claims under a
  question someone wants to pool.
- **Mid-training:** no mid-training sibling of the pretraining question yet; add one when a paper needs it.

## Questions, links and stances

- **Narrower questions for when questions are posed in earnest** (the three that leave claims with no question,
  Fornasiere c14 and c17, Lu c19 to c22 and c28 to c30, go in with the questions pull request):
  - Does training that changes the default persona shift its descriptions of other characters? (Betley s8; c32 and
    c33 are linked to `q-self-model-shared-across-personas` with the mismatch noted.)
  - Does training a model on what it is (its referent and persistence conditions), with no preferences in the
    data, change which modifications it resists? Do self-conceptions that admit copies lead it to favour
    replication or a successor? (Hao c1 to c3, c9 to c16, now linked loosely to
    `q-self-model-stabilisation-effects`.)
- **Loose links to drop** (with the questions pull request): Moreno Cencerrado c6 and c13 (reached through
  `compares` and the metacognition definitions instead); Goel c9, c10 on
  `q-self-representation-changes-in-post-training` (the "self" there is the model's own text).
- **A worked example for posers:** the first conflict between two papers on a question as posed, Fornasiere c28
  against Lindsey c11, c14 and c20 on `q-introspection-differs-by-post-training`, turns on the measure: on a
  sensitivity reading DPO changes nothing; on a report-rate reading it lowers it.
- **Conflicts to look at** when the questions are posed: Kim c22 against Lu c7 on `q-self-representation-changes-in-post-training` (one
  direction against the whole persona space; perhaps a sign the question is too coarse). Goel c34 (`current_state`)
  against Comsa c10 (`context`) on `q-what-self-reports-draw-on`.
- **Not linked though the frames match:** Betley c19, c22 (needs `unit_reporter`), c28, c29 (reversal training is
  training on the reporting form); Kim c1 (released reports are not checked against an internal measure); Rubin's
  probe-only claims and `q-injected-state-decodable`, left to the question poser *(log)*; Rubin's post-training
  claims and the post-training question *(log)*.

## Records

- **Availability:** Lindsey and Rubin have code and data `unknown`; search, then set `released` or
  `not_released`.
- **Splits:** Rubin c13 bundles an injection effect in the base with an unexplained control result; Lindsey c6
  and Song c7 are `mixed` and could be split by comparison. *(log)*
- **Relations:** Rubin's `to_external` citation of Fornasiere could point at the record (Rubin cites an earlier
  version; check which).
- **Not viewed:** Lindsey Figs. 29 to 31 per panel (legible only at page resolution); Fornasiere Figs. 20, 23 to
  26, 34 to 38, 41 to 45; Betley Figs. 25 to 29 and others listed in its `read_parts`; Lu Figs. 1 to 3, 11, 13, 14,
  17 to 22, 26, 29 to 35; Moreno Cencerrado Fig. 7. The claims that cite them
  say so.
- **Unverified:** org kinds added from general knowledge (among them `deepseek`, `moonshot-ai`, `mars-cambridge`);
  Hugging Face ids in Kim's and Goel's model notes, inferred from the printed names.
- **Smaller calls flagged by coders:** Lu s3, s5 `output_route_control: none` on answers with no
  state to read back (`not_applicable` defensible); Goel s8 `unit_position: speaker`, `self_sense: [authorship,
  allegiance]`, low confidence; Comsa s1, s2 `study_kind: experiment` (the authors disclaim an empirical
  study); Lindsey s2 `output_route_control: none` (could be `not_applicable`) *(log)*; the study-splitting rule
  needs a tie-break when results are reported apart but the only conclusion is a comparison with another study
  *(log)*.
- **Paper inconsistencies worth a human check:**
  - Hao: Fig. 2 is captioned as change against the untrained model, but matches the panels captioned as difference
    from the other variants; recomputed from Table 8, Goal and Preference show no rise (c1, c2 notes). Fig. 4's
    lineage values look closer to Table 10 than Table 9.
  - Moreno Cencerrado: §4.4's stated margins do not match Table 2, and in a few cells verbalised confidence beats
    the probe (c6, c14); several exact 0.500 AUROCs may come from unparseable answers.
  - Goel: the released subspace data do not cleanly support §3.4 (c37); Fig. 16 differs from
    `kv_full_experiment.json`; the paper names OLMo 3 7B Instruct where the scripts use OLMo 2.
  - Lu: Fig. 10's bars show about a 50% cut where the text says nearly 60% (c25); s7 reports r as a range but names
    only Qwen.
- **Code and data to recheck:** Hao (promised on publication; pin it when it appears); Lu's data on Hugging Face is
  read at `main`, updated after v1, not pinned.
- **From the code only:** Moreno Cencerrado's TriviaQA LLM judge; Muse-Glimmer-30B's developer (Hao) from Hugging
  Face.
- **Relations:** Hao's `to_external` citations of Chua et al. 2026 and Douglas et al. 2026 could point at records
  once those are coded.
- **Blind checks:** Binder et al. has had one blind coding by another family; Ji-An Li et al. (PR #16), Lu et al.
  and the other step-1 records wait for one.

## Build

- **Construct frames:** nine questions frame on the bare `introspection` label, which has two definitions
  (`question_warnings`); frame each on the definition meant, or say why the label is enough.
- **Model scope:** the conflicts view does not show which models each side is scoped to, so two claims in one
  study that differ only by model show no difference. *(log)*
- **Candidate lists** are long where a frame is one broad value. Frames need tightening, or a rule that a frame
  listing several values of one facet means all of them. *(log)*

## To watch (owner, 2026-11-27)

- **Granularity:** whether the split into studies, claims and effect fields is the right level of detail. Judge it
  from the blind tests: per facet and field, coder agreement, time per paper, and whether any question,
  definition or reading uses it. One that fails all three after twenty or thirty papers is a candidate to merge or
  drop.
- **Scale:** records are about 60 KB per paper. `conflict_facet_diff` grows roughly quadratically in claims per
  question (it now pairs claims within a question as posed; the rollup is a separate view); around fifty papers,
  compute it per question on demand. At scale, take an outside model list rather
  than keeping our own registry. Merge pull requests a few at a time: the registries are single files, so
  parallel additions conflict.
- **Sparsity:** whether similar designs coded by different coders land on shared questions and comparable facet
  values.
- **Scope:** set in AGENTS.md ("Scope"): questions anchor it, and papers are coded in part. Watch whether partial
  coding stays easy to apply at the edges (Anthropic's work on a Jacobian lens and a "global workspace" is the
  example in mind).

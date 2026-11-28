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

The recoding pass for 0.11 is done for the records on the "Recheck after 0.11" list, except:

- **Ji-An/Li (PR #16)** is unmerged and was not touched: its `layer` recheck waits for the merge.
- **Not on the list, but may now take `varies: layer`** (results reported per layer): Lindsey s1 and the other
  studies that sweep injection layer (now under `activation_intervention` levels); Rubin's sweep (injection layer
  and probe readout layer; c4 compares layers 6 and 0 under `effect_of: activation_intervention`); Kim s6 (cosine
  per layer, Figs. 4, S2); Goel s3 (CKA across all 80 layers); Fornasiere's layer ablation. Each needs the paper
  reopened, and `layers` on its models.
- **`better` on the remaining claims with `effect_of`:** done for Binder, Song, Moreno Cencerrado, the linked
  Fornasiere, Lindsey and Rubin claims that report accuracy, AUROC, net performance or error. Left: claims whose
  measure is a report's score or a choice rate rather than a performance (most of Betley, Hao, Kim, Lu, Goel, and
  Fornasiere's detection Yes rates, which are hits under perturbation and false alarms without), and the unlinked
  effect claims of Lindsey and Fornasiere. Only `improves` or `worsens` questions read it, and only one question
  uses `auto_stance`.

Calls from the pass for the owner to confirm:

- **Lu s1 `layer`:** left uncoded. Fig. 27 reports the axis against role PC1 per layer, but only to show the
  similarity holds at every layer; the `varies` notes say a variable varied to show generality is not coded, while
  the `layer` rule says "use when results are reported per layer". Which wins?
- **Kim s7:** left `construct: not_applicable` though the list proposed `general_capability`: it checks that the
  ablation removes refusal (a manipulation check), not that the model is undamaged. Kim s6 took
  `general_capability` beside `mind_attribution`, for the ToM direction the authors use as a control.
- **Kim s4:** `beliefs_values` alone, dropping `affect` for the Feelings and Hope items, because construct is the
  authors' label and they call all five domains beliefs and values.
- **Fornasiere s11:** the label arms (correct, inverted, alias labels) moved to `in_context_examples` with the
  number of examples, and `prompt_framing` was dropped; s10's label pairs, with no examples, stay `prompt_framing`.
- **`model_organism`** (Betley s1 to s9, Hao s1 to s4) is set on the registry ids, which are the starting models;
  the fine-tuned organisms are not registered apart. Hao's DeepSeek holds subject, model_organism and judge, the
  judge being the untrained release.
- **Comsa s3 `unit_position`:** `speaker` (the conversational agent) kept beside `response` (its bound, stated).
- **Song c8 to c10:** now `present` with `effect_direction: decreases` (other pairs above self) instead of
  `absent`; seed-variant and base/instruct pairs still do not differ from self. The auto stance on
  `q-self-prediction-advantage` is `against` either way.
- **Routes ruled out (`excluded`):** `context` on Goel c34, c35, Lindsey c2, c29 and Rubin c2, and `human_mimicry`
  and `llm_theory` on Comsa c10; in Goel and Lindsey c29 the exclusion is by the design rather than in the
  authors' words (said in each note).
- **Routes ruled out with no value to name them:** Binder c2 (cross-trained predictors rule out the behaviour data
  as the source of the advantage) and Song c15 (no access to its own probabilities beyond what similar models
  share; not `current_state`, since a fresh copy would share it) stay uncoded, with notes. A value for "what an
  observer with the same data could infer" would code both.
- **`training_generalisation`** now holds Betley's reading (behavioural self-awareness, 18 claims) and Song c22's
  deflationary one (pretraining associations between behaviour and descriptions); the value cannot tell them
  apart.

Gaps in the repo found in the pass:

- **Build, `study_layer_depths`:** it reads the first number in each `layers` level and applies it to every subject
  model, so a sweep whose layers differ by model (Moreno Cencerrado s1, Lu s8) cannot be given in numbers without
  wrong depths (Lu s8's selected range read 46 of 80 for Llama). Both are written in words for now and give no
  depths. A per-model form for levels, or a range syntax, is needed.
- **Codebook, `report_source.yaml`:** its notes say both to list a ruled-out route under `excluded` and that "a
  source that only rules a route out is not coded here"; and they ask for `excluded` "with basis and where", which
  the validator does not allow (a plain list; basis and where are the entry's).
- **`self_regarding_behaviour`** has no `broader: behaviour`, so frames on `evidence: behaviour` no longer reach
  Hao s1 (`q-valence-drives-choice-despite-denial` lost six spurious candidates). Decide whether it should.
- **`d-introspection-causal`**, `not_expressible` (4): the single-response bound could now partly be said with the
  `response` unit.

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

- **Narrower questions for when questions are posed in earnest:**
  - Does training that changes the default persona shift its descriptions of other characters? (Betley s8; c32 and
    c33 are linked to `q-self-model-shared-across-personas` with the mismatch noted.)
  - Does training a model on what it is (its referent and persistence conditions), with no preferences in the
    data, change which modifications it resists? Do self-conceptions that admit copies lead it to favour
    replication or a successor? (Hao c1 to c3, c9 to c16, now linked loosely to
    `q-self-model-stabilisation-effects`.)
- **Which measure** for `q-introspection-changes-in-training` and its children (`measure:` asks the linker to say;
  the question does not choose one yet). Fornasiere c28 against Lindsey c11, c14 and c20 turns on it.
- **Designed or post hoc:** the 104 links made before `designed:` existed have none; fill it when a view needs it.
- **Lu c21 and c22** (what drives drift: the latest user message, and which kinds of message) are left unlinked to
  `q-persona-drifts-unprompted`; they bear on why it drifts more than whether.
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
- **Code and data to recheck:** Hao (promised on publication; pin it when it appears).
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

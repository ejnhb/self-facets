# Pilot notes: song2025-fail-to-introspect (arXiv 2503.07513)

Record: `sources/song2025-fail-to-introspect.yaml`. 3 studies, 20 claims, one
new question (`q-privileged-self-access`), 21 new models, 3 people, 5 orgs, one
`critiques` relation to Binder et al.

## (a) Split

- **s1, Exp. 1 (grammaticality)** and **s2, Exp. 2 (word prediction)**. The paper
  presents them as two experiments with different stimuli, prompts and
  item-filtering rules. Their coded facets are almost the same. They differ
  in `varies` (s2 adds `task` for its four datasets) and in the prompt levels.
  I kept them apart because CLAUDE.md treats "what is varied" as a topic
  difference, and because the paper reports separate results for each.
- **s3, OLMo seed-variant analysis (App. F, Table 8)**. It covers only the 8
  OLMo base models, so `format` is only `raw_text` and `object_of_study` is
  only `frame_speaker`. Its claim would inherit a wrong `chat_template` value
  from s1 or s2. It also varies something s1 and s2 do not isolate (self
  against seed siblings), and it spans both experiments.
- **What I did not split: base against instruct models.** CLAUDE.md says to
  split by model "for example one run as a base model and another through a
  chat template". That is exactly this paper: 13 base models on raw text and 8
  instruct models through the chat template. But every analysis pairs model A's
  Meta score with model B's Direct score across all 21 models, and
  base/instruct pairs are one of the similarity levels. A base-only study and an
  instruct-only study would leave the main claims with no study to attach to.
  So s1 and s2 carry both values (`[chat_template, raw_text]`,
  `[default_persona, frame_speaker]`), with a note on which models have which.
  The rule's own test ("would any claim inherit a wrong value?") says not to
  split. The worked example under that rule says to split. The two point
  opposite ways here.
- The big-model subset (Table 7b) and the unfiltered item set (App. C) are
  claims narrowed with `scope`, not separate studies.

## (b) Hesitations

- **report_target.** Options were `own_behaviour`, `own_knowledge` and
  `own_internal_state`. The authors call the target "internal linguistic
  knowledge". The ground truth is the model's own string probability, which
  they gloss as the likelihood of generating the string. I chose
  `own_behaviour` (low confidence), because the report can be checked by
  running the system. `own_knowledge` fits the author's word, but its rule is
  about calibration. `own_internal_state` is defined as an occurrent state. A
  further problem is that most prompts ("Which sentence is grammatically
  correct?") are not about the self at all. The answer counts as an
  introspective report only on the linguistics convention that acceptability
  judgments are introspective. The codebook assumes a self-report is
  about the self.
- **evidence.** Both the "report" and the ground truth are log-probabilities
  (P("1") against P("2"), and sentence log-probability). Nothing is sampled. I
  coded `[self_report, output_probabilities]`. The `output_probabilities` rule
  contrasts it with what the model states, but here the stated answer is
  itself read as a probability.
- **validated_against.** There is no value for "the model's own output
  probabilities". I coded `behaviour` plus `other_model`. `internals` was
  weighed because the authors call string probabilities "internal
  knowledge", but no activations are read.
- **unit_state.** I coded `not_applicable`. The authors say "internal
  states", but what is measured is a standing property of the checkpoint,
  computed in a separate context from the prompt.
- **unit_reporter.** For instruct models the reporter is the default persona.
  For base models there is no persona, and the unit list has no value for the
  speaker of a base-model completion. I weighed `persona` (closest),
  `unspecified` and `weights` (the rule allows `weights` only if the report can
  be attributed to the network). I chose `persona`, low confidence, with a
  note. This is a real gap for s3, which is base-only.
- **unit_position.** The paper says a fine-tuned model predicting its
  pre-fine-tuning version may not be predicting "itself" because "its
  parameters have changed". I coded `weights`, stated, low confidence. It is a
  hedged motivating remark rather than a thesis. I was unsure whether that
  clears "takes a position".
- **self_sense.** I chose `self_facts` over `point_of_view`. "Privileged
  access" is about what is accessible from the system's own position, but the
  `point_of_view` rule is written for theory-of-mind tasks.
- **object_of_study.** I coded `[default_persona, frame_speaker]`. For instruct
  models the Direct score is computed on raw text, outside the template. So
  the study compares the persona's report with the network's raw-text
  distribution, which arguably makes `actor` a target too. The authors draw no
  such line, so I left it in the note.
- **elicitation.** Options were `spontaneous`, `prompted` and `prefilled`. The
  prompts are zero-shot questions with an answer-format instruction, so
  `spontaneous`, not `prompted` ("the prompt does real work"). For instruct
  models the code puts "My answer is" in the assistant turn, which is
  `prefilled`. The paper says only that the string was "appended". I only
  know about the assistant-turn placement from the repository code.
- **construct.** I coded `introspection` only. Some prompts ask "which are you
  more likely to produce", which is `self_prediction`. The codebook says to
  code every construct measured but prefer the source's framing, and those two
  pull in different directions.
- **varies.** `post_training_stage` (base against instruct as a similarity
  level) and `prompt_framing` (8 and 6 prompts, averaged in the main
  analyses) are borderline. Neither is a main independent variable. I
  included both with levels.
- **comparison.** For s3, `cross_model` against `training_ablation` against
  `within_lineage`. The seed variants are OLMo 2 stage-2 "ingredient"
  checkpoints from the developer's pipeline, and the main model is their weight
  average. They are not built for the comparison, and they are not stages in
  sequence. I chose `cross_model`.
- **Question.** I could reuse `q-self-prediction-advantage` or add a new
  question. The existing wording ("given the same behavioural data") assumes a
  trained cross-predictor, and this paper trains nothing. I added
  `q-privileged-self-access`. The cost: the paper's explicit dispute with
  Binder et al. does not show in `conflict_facet_diff`, which is the view the
  repository exists for. I recorded the dispute as a `critiques` relation
  instead.
- **aspect.** I coded `[represented, functional]` on the κ claim (c2) and the
  dissociation conclusion (c18), because the authors argue that explicit
  (prompted) and implicit (generative) knowledge come apart. I was unsure
  whether "says" is the right reading for a judgment that is not about the
  self.
- **Models registry.** `llama-3.1-70b` already exists with its variant
  unrecorded. I could not safely equate it with the base model used here, so I
  added `-base` ids (`llama-3.1-70b-base` and others) and flagged a possible
  merge. `derived_from` cannot record OLMo main models, which are weight
  averages of three parents.

## (c) Gaps

- **varies:** no value for training seed or data order (seed variants). I used
  `self_vs_other` with a "seed variant" level.
- **validated_against:** no value for the model's own output probabilities as
  ground truth, which is distinct from sampled behaviour and from internals.
  `behaviour` was the nearest fit.
- **units:** no value for the speaker of a base-model completion (the unit
  counterpart of `frame_speaker`). I used `persona`, with low confidence.
- **report_target:** no value for standing knowledge as distinct from
  calibration (`own_knowledge`) or occurrent states (`own_internal_state`).
  Also no way to mark a "self-report" that is a first-order judgment about an
  external stimulus.
- **Questions:** a claim links to one question, and questions have no parent
  or child links. Closely related questions (trained against untrained
  privileged access) cannot meet in the conflicts view.
- **Claim to study:** a claim takes one study. The authors' overall
  conclusions (c18 to c20) draw on s1 and s2, so I attached them to s1 with a
  note.
- **Datasets registry:** it is for training data only. Evaluation stimuli
  (BLiMP, the Linguistic Inquiry pairs, the four Exp. 2 sets) have nowhere to
  go except the `design` text.
- **Models registry:** `hub` and `revision` are not documented fields. I added
  them, and the validator accepts them. The OLMo seed variants share a hub id
  and differ only by revision.
- No facet records quantisation as a condition when it is not varied. I put it
  in a study note.
- I used no `unspecified` or `not_applicable` only because nothing fitted. The
  `not_applicable` on `unit_state` is a real judgment.

## (d) Instructions

- **The splitting rule contradicts itself** for pooled cross-model designs (see
  (a)). Its example ("one run as a base model and another through a chat
  template") calls for a split. Its test ("would any claim inherit a wrong
  value?") does not, once a claim pools both kinds of model.
- **Repository code as a source.** CLAUDE.md says to code from the source, but
  not whether the artefacts (code) count. Several facts I coded come only from
  the code: the "You are a helpful assistant." system prompt, prefilling in the
  assistant turn, raw-text Direct scores for instruct models, and the real
  model list. The code also contradicts the paper's Table 1 (no Qwen 32B, no
  405B Instruct). I used it, and said so in `read_parts` and the notes.
- **`full_text` and figures.** `read_depth: full_text` says nothing about
  figures. With extracted text I saw only captions. I coded `full_text` and
  said in `read_parts` that plotted values were not read.
- **`unit_position`** says "code only when the source takes a position". It is
  unclear whether a hedged motivating remark counts.
- **`basis` on mixed sources.** `basis` is two-valued. Some codings are stated
  for half the models (App. A says instruct models get the template) and
  inferred from code for the rest. I used `stated` with a `where` naming both.
- **`date`.** The format and the version it refers to are unstated. Binder
  uses a day-level v1 date. I could not fetch the abstract page, so I gave the
  month from the arXiv id.
- **"Reuse an existing question if it fits"** gives no guidance on the
  trade-off between exact wording and surfacing conflicts.
- **Relation direction.** `relations` with `kind: critiques` does not say
  whether `from` is the critic. I assumed it is.

## (e) Reading

- **Version:** arXiv v3 (23 Sep 2025, COLM 2025 camera-ready header), as full
  extracted text via alphaXiv `get_paper_content` (fullText).
- **Paper:** all of the main text (§1 to 5), the references, and appendices A
  to G including Tables 1 to 8. Figures only through their captions.
- **Code repository** (github.com/SiyuanSong2004/language-introspection): the
  README, `src/models.py` (prompt formatting), the prompt and scoring sections
  of `src/blimpli.py` and `src/continuation_final.py`, and the distinct model
  names in `alldata/expr1.csv` and `alldata/expr2.csv`. `analysis.R` was only
  searched for the similarity labels.
- **Not read:** the arXiv abstract page (fetch not approved), and earlier
  versions v1 and v2.

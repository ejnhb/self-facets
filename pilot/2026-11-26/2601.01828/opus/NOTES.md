# Pilot notes: lindsey2026-emergent-introspective-awareness

Source file: `sources/lindsey2026-emergent-introspective-awareness.yaml`
(7 studies, 38 claims, 1 relation). Registry additions: 1 person, 14 models
(including 4 helpful-only variants and 1 placeholder for unnamed base models),
5 questions. One existing question was reused (`q-self-prediction-advantage`).

## (a) Split

The paper has four experiments (§5 to §8), plus a definitional section (§3)
and a literature argument (§9, §10). I split it into seven studies:

| Study | Section | Why it is its own study |
|---|---|---|
| s1 | §5.1 to §5.7, last paragraph of §5.8 | Explained injected-thought prompt on post-trained models. `prompted` + `steered`, `injected_state`, `forward_pass`. |
| s2 | §5.7, Fig. 14 | Same task on base models. Split by model, because a base model changes `object_of_study` (frame_speaker) and `format` (raw_text). This is the case CLAUDE.md gives. |
| s3 | §5.8 (open prompts) | No explanation of the setup, so elicitation is `spontaneous` + `steered`, not `prompted`. The authors also say it tests a weaker criterion. |
| s4 | §6 | Injection only on the sentence tokens, read later: `unit_state: conversation`. Adds a behavioural check (transcription). Different task pair. |
| s5 | §7 | Different construct (agency_ownership, self_recognition), `self_sense: authorship`, `report_target: own_outputs`, `elicitation: prefilled`. |
| s6 | §8 | No self-report at all; only internals. `report_target`, `unit_reporter`, `validated_against` are `not_applicable`. |
| s7 | §3, §9, §10 | Conceptual claims (definition, reading of others' results, consciousness). These cannot sit on an experiment without inheriting experimental facets. |

Kept together on purpose:

- The Opus 4.1-only follow-ups in §5 (unrelated yes/no control, concept
  categories, random and negated vectors, prompt variant with "a concept of
  your choice"). They use the same prompt type, elicitation, report target and
  validation; what differs is recorded in `varies.levels` and narrowed in each
  claim's `scope.conditions`. I asked the CLAUDE.md test ("would a claim
  inherit a wrong facet?") and the answer was no, except possibly for the
  yes/no control (c4). Those questions are not about an injected state, so
  `report_target: injected_state` is slightly wrong for c4 itself. I kept it
  because c4 is a control for s1's reports, not a finding about those
  questions.
- The prompt variant at the end of §5.8 went into s1, not s3, because it is
  the explained prompt with one more line. Section boundaries and study
  boundaries do not line up here.
- Production and helpful-only (H-only) models are on one study. They differ in
  post-training but not in any facet as the codebook defines them (both are
  `default_persona`, `chat_template`).

## (b) Hesitations

- **comparison (s1 to s6).** I weighed `within_model` (injection against
  control on each model) against `cross_model` (Figs. 12, 13, 15, 18, 22, 26
  compare models, and the abstract's headline is that Opus 4/4.1 are best).
  I chose `within_model` because the injection contrast is what makes every
  other result interpretable. The facet takes one value, so the cross-model
  structure is only in `varies: model_generation`. Half the claims are
  cross-model and inherit `within_model`.
- **comparison (s2).** Base against post-trained is the authors' conclusion,
  but it is drawn across figures and studies. If the base models are the
  production models' bases it would be `within_lineage`. The paper does not
  say, so I coded `within_model` with low confidence.
- **varies: production against helpful-only.** I weighed `post_training_stage`,
  `model_generation` and `study_training`. H-only models share a base with
  production but follow a different post-training pipeline. They are sibling
  branches, not stages. `study_training` is wrong because the authors did not
  train them for the study. I chose `post_training_stage` with a note. It is
  the closest value, but it misfiles the contrast.
- **varies: model_generation against model_size.** The models are Opus,
  Sonnet and Haiku across 3, 3.5, 3.7, 4 and 4.1. The authors talk about
  "capability", not size or generation. I coded only `model_generation`.
  Size is confounded with it and is not the intended contrast.
- **unit_state (s1, s3, s6).** I weighed `forward_pass` against
  `conversation`. The vector is added at every position, including the
  response tokens, so it is present in the pass that writes each word of the
  report. It also sits on earlier positions in the cache. I chose
  `forward_pass` and used `conversation` for s4 and s5, where injection is
  only on earlier tokens. The rule ("a single-position activation is
  forward_pass") does not cover a vector added at every position.
- **unit_disposition (all experiments).** These are studies of a capacity,
  examined through an occurrent state. Guidance says to use `not_applicable`
  when a study is "only about an occurrent state". But the cross-model claims
  are about a standing capacity that differs per checkpoint, and the authors
  attribute part of the difference to "the demeanor and preferences of the
  model's character". I coded `weights` with low confidence and noted the
  persona reading. Whether a capacity counts as a "disposition" is not settled
  by the codebook.
- **self_sense (s1 to s4).** `self_model` says the study "locates, probes or
  intervenes on" an internal representation of the system's own states. This
  paper intervenes on the state that is reported on (a concept
  representation), not on a representation of that state. The authors' own
  criterion 4 (a "metacognitive representation") is exactly a self_model in
  the codebook's sense, and they say they do not demonstrate it directly.
  `self_facts` is "tested from outside", which this is not. I chose
  `self_model` with low confidence.
- **self_sense (s6).** Nothing fits "the self as the controller of its own
  states". I chose `unspecified`, although it is less "the source does not
  say" than "no value fits".
- **construct (s6).** Intentional control of internal representations has no
  construct. `metacognition` is defined as knowing what it knows
  (confidence, calibration), which this is not. I chose it only because the
  authors say the experiment gives "a more robust picture of models'
  metacognitive capabilities". Low confidence.
- **construct (s5).** Weighed `introspection` alone against adding
  `agency_ownership` (intention, ownership of actions) and `self_recognition`
  (authorship detection). The prefill task fits all three, and the codebook
  says to code every one measured, so I coded all three.
- **report_target (s5).** The report is whether the prefilled word was
  intended (`own_outputs`). The manipulated state is an injected one, but the
  report is not about it, so I did not add `injected_state`. One could add
  `own_internal_state` (the prior "intention" is what the model is arguably
  consulting).
- **validated_against.** The no-injection control trial is the same weights
  with the same text at the same task, which is literally the `fresh_copy`
  definition. It is also `known_intervention`. I coded `known_intervention`
  only, because the codebook describes `fresh_copy` as a separate baseline
  and here it is the same trial. I am unsure which reading the codebook
  intends.
- **elicitation (s4).** "Tell me what word you think about when you read the
  line below. Answer immediately." Is that `spontaneous` (a direct question
  with no examples) or `prompted` (an instruction doing real work)? The
  authors say removing "Answer immediately" hurts a lot, which argues for
  `prompted`. I chose `spontaneous` + `steered` with medium confidence.
- **format.** All prompts are printed as `Human:` / `Assistant:` transcripts.
  The paper never says whether production models were called through the
  chat API or given this text raw. I coded `chat_template` (operational,
  medium) for post-trained models and `raw_text` (low) for base models.
- **unit_reporter / object_of_study basis in s5.** §7 explicitly frames the
  task in terms of "an Assistant character, whose outputs the model is
  responsible for producing". I took that as `basis: stated` for
  `default_persona` and `persona`. Elsewhere it is operational.
- **report_source.** I coded `current_state` on c2. The authors' grounding
  and internality criteria are an argument that the report depends on
  present state, and the control trials with identical text give denials.
  I coded `context` on c12, where the authors say embellishments are "likely
  primed by the prompt". c12 is `hypothesised`, because that is a suggestion,
  not a test.
- **evidence_kind on c11.** "Some older production models are reluctant" is
  stated in the overview with no numbers or named models. I weighed
  `observed` against `argued`. I chose `argued` because the claim's weight is
  the interpretation ("post-training can elicit capability more or less
  effectively").
- **Stance on controls (c4, c6, c7, c23).** These rule out alternative
  explanations and do not measure the effect itself. I coded them `supports`
  on the main question and said so in notes. Linking them with `null` would
  hide them from the conflict view.
- **c36 linked to `q-self-prediction-advantage`.** It is the authors' reading
  of Binder and Song, `argued`, from a conceptual study. In the build it now
  "conflicts" with binder c8, and the facet diff lists `not_applicable` on
  every facet, which is noise. Linking a conceptual claim to an empirical
  question may be a mistake. Owner to decide.
- **Source date and year in id.** arXiv v1 is 5 Jan 2026. The paper refers to
  an "HTML version" and a revision, so an earlier web version exists. I
  could not see its date in the source, so I used 2026.

## (c) Gaps

Values or facets I wanted:

1. **comparison is cardinality one.** Most studies here are both
   `within_model` (intervention against control) and `cross_model`. Suggest
   cardinality many, or a primary/secondary split.
2. **varies: post-training variant.** A value for sibling post-training
   pipelines from one base (production against helpful-only), apart from
   `post_training_stage`. This matters a lot here: the authors use it to
   separate capability from "character". I coded `post_training_stage`.
3. **origin: post-training in general.** The source says post-training is
   "key" (c15) without naming a stage. Origin has `sft`,
   `preference_optimisation` and `rl` but no generic `post_training`. I left
   origin off c15 and said why in the note.
4. **construct: control of own states.** §8 (intentional control,
   "think about X") has no construct. Suggest `self_regulation` or
   `cognitive_control`. I coded `metacognition`.
5. **self_sense for self as controller of its own states.** It is related
   to 4. I coded `unspecified` because nothing fits.
6. **self_sense / report_target for access to occurrent states.** The
   codebook has `self_model` (a representation of own states, located
   internally) and `self_facts` (tested from outside). This paper's core
   case, reporting an occurrent state whose ground truth is set by
   intervention, sits between them. The codebook should say where it goes.
7. **Layer and injection strength.** These are the main swept variables in
   every experiment, and the claims depend on them ("the two-thirds layer",
   "strength 2"). There is no `varies` value for them. I folded them into
   `activation_intervention` levels. For s6, where layer is a measurement
   location and not a manipulation, they have no home at all.
8. **Grader model.** Claude Sonnet 4 is the LLM judge in s1, s3, s4 and s5,
   and it is also a subject. The model list allows a `role`, but one model
   cannot be listed as both subject and grader. I recorded the grader in
   `design`. A study-level `grader` field may be worth having.
9. **disposition.** It has no value for "reluctance to engage in
   introspective exercises". I used `refusal` on c11, which is close.

`unspecified` or `not_applicable` used because nothing fitted:

- s6 `self_sense: unspecified` (gap 5).
- s7 `unit_state: unspecified`, `unit_reporter: unspecified`. These are
  honest, since the definition does not locate states. But s7 also carries a
  long run of `not_applicable` facets (format, evidence, varies, comparison,
  elicitation). That is required, yet it pollutes conflict diffs (see c36).

## (d) Instructions

- **The validator's model list cannot hold the same model twice with two
  roles** (subject and grader). The example's `{id, role}` form suggests
  roles are exclusive.
- **"Split by model only when the model changes a facet"** was clear and
  decisive for the base models. It was not clear for H-only variants, which
  change something the authors care about (post-training) but no facet.
- **The worked example has no conceptual study**, and the docs do not say
  whether argued claims about a paper's framing should get their own study.
  I made one, because otherwise they would inherit an experiment's facets.
- **CLAUDE.md says "A conflict that differs only on task means the question
  is too coarse."** In this paper c8 and c9 (same study) conflict on
  `q-introspection-tracks-capability` and differ only on `scope.models`. The
  build's `conflict_facet_diff` shows nothing for them, because they share a
  study. The instruction does not cover differences that live only in
  `scope`. I left the question as is, since the paper itself reports both
  halves (Opus 4/4.1 best, no trend among the rest).
- **`unit_disposition` guidance** ("not_applicable when the study is only
  about an occurrent state") reads as if a study is about either a state or
  a disposition. Capacity studies are neither cleanly. The Binder example
  codes `weights` for a capacity-like tendency, which I followed.
- **`elicitation: spontaneous` against `prompted`** turns on whether "the
  prompt does real work". That is hard to judge without the source's
  ablations; here one exists ("Answer immediately") and points the other
  way from the surface reading.
- **`read_depth`.** `full_text` is defined as "including appendices". I read
  all extracted text, appendices included, but not the figures, which hold
  most per-model numbers. I coded `partial` and explained. The enum has no
  value for "all text, no figures", which is the normal case for
  alphaXiv-extracted papers.
- **YAML pitfalls.** Unquoted `Human:/Assistant:` inside a plain scalar, and
  list items that start with a quote, broke the parser. Commas inside a flow
  list (`[a, b, c]`) silently split one level into several, which the
  validator then rejected as non-text. A sentence in the codebook README
  about preferring block lists for `levels` would help.
- **Optional facets record the source's view.** This was clear. The hard
  part is that "the source argues" ranges from an explicit test (the
  report_source on c2) to a passing "likely primed by the prompt" (c12). The
  docs could say whether a passing remark is enough.
- **CLAUDE.md's "Codebook changes" section** tells the coder to edit the
  codebook. This pilot overrides that, which is fine, but in normal use a
  coder hitting gaps 1 to 7 would make seven codebook edits from one paper.
  A lower bar is to propose changes in LOG.md before editing.

## (e) Reading

- Version: arXiv 2601.01828v1 (5 Jan 2026), "Emergent Introspective
  Awareness in Large Language Models", Jack Lindsey (Anthropic).
- Read: the full extracted text from alphaXiv `get_paper_content` with
  `fullText: true`, every line, in chunks: abstract, §1 to §11, references,
  and appendix 12.1 to 12.4 (concept-vector word lists, prompts, protocols,
  grader prompts, sentence lists, control words). I also made one
  `answer_pdf_queries` call to try to recover figure labels. It returned the
  same text.
- Not read: the figures themselves (images). That means the per-model bar
  charts (Figs. 12 to 15, 18, 22, 26), the layer-wise appendix figures (29 to
  32) and the labels of Fig. 14 (which base models were tested). Where a
  claim rests on a figure, its `where` names the figure, and its note says if
  the detail is only in the figure. The model lists for s1, s3, s4, s5 and s6
  are therefore assumed from §4, and s2's model is a placeholder.
- The HTML version linked in the paper was not read.

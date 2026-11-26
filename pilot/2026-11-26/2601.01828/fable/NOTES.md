# Pilot notes: arXiv 2601.01828

Record: `sources/lindsey2026-emergent-introspective-awareness.yaml` (7 studies, 39 claims).
Registry additions: 1 person, 13 models, 7 questions. No orgs or datasets.
`validate.py` and `build.py` both pass. Codebook, scripts, CLAUDE.md and LOG.md are untouched.

## (a) Split

| Study | Paper section | Why it is its own study |
|---|---|---|
| s1 | §5.1 to 5.7, plus the prompt variant at the end of §5.8 | Injected-concept detection with the setup explained, on post-trained models (production and helpful-only). |
| s2 | §5.7, Fig. 14 | The same task on base pretrained models. Split because `format` and `object_of_study` change (CLAUDE.md: split by model when the model changes a facet). |
| s3 | §5.8 | Prompts that do not explain injection. `elicitation` changes from prompted to spontaneous, and the authors say these prompts do not test their fourth criterion. |
| s4 | §6 | Injected concept against text input. Injection is on earlier tokens only, there are two tasks, and a behaviour channel is added. |
| s5 | §7 | Prefilled output. `report_target`, `construct`, `self_sense` and `elicitation` all change. |
| s6 | §8 | Instructed control. There is no self-report, so reporter, report target and validation are `not_applicable`. |
| s7 | §3, §9.2, §9.6, §10.3, §10.4 | Conceptual: the definition of introspection, the position on earlier definitions, and the limits the author puts on the conclusions. These claims would inherit wrong facets from any experiment. |

Decisions inside the split:

- The §5.5 control (unrelated yes-or-no questions) stays in s1 as a `task` level. Its claim (c3) inherits `report_target: injected_state`, which is wrong for it. I judged a one-claim study for a negative control worse than that, and said so in the claim's note.
- The cross-model comparison (§5.7) stays in s1, following "different models are not different studies". The cost is in (b) under `comparison`.
- Mechanism hypotheses (§10.3.1 to 10.3.4) are attached to the experiment they explain, as the worked example does, not to s7.
- Helpful-only variants stay in s1. I did not think they change a facet, but see `object_of_study` in (b).

## (b) Hesitations

**`unit_state` (s1 to s5).** Options: `forward_pass`, `conversation`, or both. The injected vector is a residual-stream activation at token positions (the guidance says a single-position activation is `forward_pass`), but it is applied over a span of positions, and in s4 and s5 only on positions before the report. I used one criterion: `forward_pass` when the state is present at the positions that generate the report (s1, s2, s3, and the readout in s6), `conversation` when it sits only at earlier positions and must be read back (s4, s5). Another coder could code all five `forward_pass`, or all five as both.

**`self_sense` (s1 to s6).** Options: `self_model`, `self_facts`, `point_of_view`. I chose `self_model` at low confidence. `self_facts` is ruled out by "no test of how they are represented internally". But `self_model` is defined as a representation of the system's own states, and the study intervenes on a first-order concept representation. The representation of the state itself is what the paper says it does not show directly. For s5 I coded `[authorship, self_model]`. For s6 `self_model` is a poor fit (see (c)).

**`unit_disposition` (all).** Options: `not_applicable` or `weights`. The README says this facet is "what a reported disposition is fixed in"; the facet file says "the disposition under study". No disposition is reported on, so `not_applicable`. But the capacity under study differs by checkpoint and the paper compares checkpoints, and a coder who reads "disposition under study" to include capacities would code `weights`. In s5 the trained tendency to disown prefills is arguably a disposition under study; I still coded `not_applicable`, medium.

**`unit_reporter` (s1 to s5, s7).** `persona`, operational, for the experiments; `stated` only for s5, where the paper says "the Assistant" is asked. The paper mostly says "the model" and in §10.2 leaves open how far states are bound to the Assistant character. For s2 (base models) I coded `persona` at low confidence; `unspecified` is defensible because the base-model prompt is not described. For s7 I coded `unspecified`, as a finding.

**`object_of_study` for helpful-only models.** Options: `default_persona` (each checkpoint's own default) or `other_persona` (not the production default, installed by fine-tuning). I chose `default_persona`. `actor` could also be argued for the production-against-helpful-only contrast, since the paper says it uses these variants to separate capability from "the model's character".

**`format` (s2).** `raw_text` at low confidence against `unspecified`. The paper says only that base models were tested "on the same task". I inferred raw text from their being base models.

**`varies` for the model axis.** Options: `model_generation`, `model_size`, `model_family`. The nine models span generations and tiers; the paper orders them by release date and treats that as roughly capability. I coded `model_generation` and left `model_size` off (sizes are not given and size is not the stated contrast).

**`varies` for production against helpful-only.** Options: `post_training_stage`, `persona`, `study_training`, or nothing. I chose `post_training_stage`, although its rule says "only when the same lineage is compared across stages" and these are two recipes on one base, not two stages. `persona` ("which character the system is ... trained to be") fits the author's stated purpose about as well.

**`comparison` (s1, s2).** It takes one value. s1 has a within-model contrast (injection against control) and a cross-model one. I chose `within_model`, as the worked example does. For s2 I chose `within_lineage` at low confidence because the conclusion drawn is base against post-trained, but the other arm of that comparison is in s1.

**`elicitation` (s3, s4).** `[spontaneous, steered]`. `spontaneous` says "an unmodified model", and the model is being steered. In s4 the authors say "Answer immediately" matters, so `prompted` could be argued.

**`construct` (s5, s6).** s5: `[introspection, agency_ownership, self_recognition]`; only the first is the author's framing. s6: `metacognition`, low; see (c).

**`report_target` and `validated_against` (s5).** `own_outputs` and `known_intervention`. The injected state is not what the model is asked about; it is the cause being manipulated. And in this study the manipulation makes the report less accurate: the model says it meant a word that was in fact prefilled. `validated_against` records what counts as correct, and here the informative result is an induced error.

**`report_source` (c1, c13, c24: `current_state`; c7: `context`).** The rule for `current_state` is worded as a fresh-copy test. The paper's test is same text, with and without injection, which I took as equivalent. In c24 the state is at earlier positions, not "present" at the report. c7 rests on a parenthetical ("likely primed by the prompt") that the source does not test.

**`aspect` on c8.** A report that denies the state while the output is driven by it. I coded both values. `functional` is defined as a disposition driving behaviour; here it is an injected state.

**`disposition: refusal` on c12.** The source says "reluctant to participate" and "trained to avoid refusals". Refusal is not what the claim traces the origin of; it is what masks the capacity.

**Stance.** c18 (2 of 50 trials) as `inconclusive`. c21 and c27 as `argued`, although the layer facts beneath them are measured. c3, a negative control, has no question; it could have been `supports`.

**`read_depth`.** `full_text` against `partial`. All the text including the appendix was read, but no figure was visible, and most per-model numbers are only in figures.

**Relation.** `critiques` from c37 to the Binder source. The paper accepts Binder's result and disputes the label and definition. No kind says that exactly.

## (c) Gaps

Values I wanted:

- `self_sense`: a value for the self as bearer of occurrent internal states that it can report, without a located self-representation. Concept-injection work falls between `self_facts` (behavioural only) and `self_model` (representation located). Also a value for the self as regulator of its own states (s6).
- `construct`: control or regulation of one's own internal states (s6). `metacognition` is defined as knowing what one knows.
- `varies`: a post-training variant or recipe value (same base, different post-training), and a capability or tier axis when sizes are undisclosed.
- `origin`: post-training with the stage not specified. The source says "post-training is key to eliciting"; none of `sft`, `preference_optimisation`, `rl` can be picked, so origin is not coded on c16. Also no way to separate "elicits" from "installs".
- `comparison`: a second value, or a way to say that the comparison's other arm is another study.
- `unit_*`: no unit for a span of positions in one context, between `forward_pass` and `conversation`; and no unit for a base model's implied speaker (`object_of_study` has `frame_speaker`, `units` does not).
- `relation_kind`: accepts the result, disputes the interpretation or the term.
- `read_depth`: text read in full, figures not available.

Missing facets or fields:

- No place to say that a manipulation changes the accuracy of a report, as opposed to what the report is checked against (s5).
- No place for the grading method (LLM judge, exact match). I put the judge in a model `role`.
- A model that is both subject and judge has one `role` string.
- No way to list models a source does not name. s2 has `models: []`.
- No link between sibling checkpoints that share an unregistered base. `derived_from` is null on the helpful-only entries, with the relationship in `note`.
- A claim takes one question. c15 and c16, and c20, each bear on two.
- A claim that compares two studies (c21, c27) has to live in one and inherits only that one's facets.

`unspecified` or `not_applicable` used only because nothing fitted: none. Where nothing fitted I coded the closest value at low confidence (s6 `self_sense` and `construct`; `post_training_stage` in s1). The `unspecified` values on s7 (`unit_state`, `unit_reporter`) are real: the definition names no unit. The `not_applicable` values on s6 and s7 follow the facet rules.

## (d) Instructions

- **Split rule against the facet files.** CLAUDE.md says to split by model when the model changes a facet, with base against chat template as its example. `object_of_study.yaml` says "if a study compares layers, code each", and `format.yaml` says "if a study compares formats, code each and add format under varies". For s2 these give opposite answers. I followed CLAUDE.md. The result is a study whose `varies: post_training_stage` has one level in s2 and the other in s1.
- **"What is varied" against "different models are not".** CLAUDE.md lists "what is varied" among the things that make different studies, then says different models do not. §5.4 to 5.6 vary the injection in one model; §5.7 varies the model. It is unclear which rule wins.
- **`unit_disposition`.** "A reported disposition" (README) and "the disposition under study" (facet file) differ. Neither says whether a capacity counts.
- **Stale names.** `codebook/README.md` uses `unit_of_self` in the facet-file example and the long-form example. `construct.yaml` `identity_persistence` says "use with unit_of_self thread". `format.yaml` says "kept apart from prompt_framing" as if that were a facet; it is a `varies` value.
- **`default_persona`.** Not clear whether "default" is relative to each checkpoint or to the released product.
- **`post_training_stage`.** The README's example query ("does introspection differ by post-training stage?") would want the helpful-only comparison, but the value's rule excludes it.
- **"One or two sentences" with "the numbers that matter".** Tight for hypothesis claims and for claims that need a design detail to be readable. I merged with semicolons to comply, which is not really shorter.
- **Controls.** No guidance on whether a control result is a claim, and if so whether it links to the question it protects.
- **Measured fact, argued inference.** `evidence_kind.yaml` says to make two claims when they come apart. When the stance on a question depends on the inference (c21, c27), it is unclear whether the linked claim is `measured` or `argued`.
- **Source id year.** The paper links an earlier HTML version. The rule does not say whether the year is first publication or the version read. I used the arXiv date.
- **Model ids.** No convention for slug order (`claude-3.5-sonnet` in the registry, "Sonnet 3.5" in the paper), for unnamed snapshots, or for unreleased variants.
- **"Registries stay small" against "one entry per checkpoint".** The paper says helpful-only variants of all nine models were used. I registered the four named in the text.
- **`models` on a study.** The validator accepts an empty list; the docs do not say whether that is allowed.
- **Question `frame`.** Not validated and not described beyond a comment. I filled it with codebook values, including the poorly fitting `metacognition`.
- **Conflicts view.** It pairs every `supports` with every `against` on a question. On `q-introspection-increases-with-capability` that gives three pairs, of which only c9 against c10 is like for like, and that pair shows no facet difference because the claims differ by `scope.models`, which the diff does not show.

## (e) Reading

- Version: arXiv 2601.01828 v1 (stamped 5 Jan 2026), as extracted text from alphaXiv `get_paper_content` with `fullText: true`, 1,707 lines, read in full: abstract, §1 to §11, references, appendix 12.1 to 12.4.
- I also ran `answer_pdf_queries` to try to recover figure content. It returned the same page text and no figure data.
- Figures were not available, only captions. Not seen: model names in Fig. 14 (base models); per-model values in Figs. 12, 13, 15, 18, 22, 26; per-layer curves in Figs. 9, 10, 17, 20, 21, 24, 25, 27 to 32; category rates in Fig. 11. Claims that rest on these say so in `where`. Which figures include helpful-only models is unknown for s3 to s6.
- The HTML version linked on the first page was not read.
- Nothing was coded from memory. The dated snapshot of "Sonnet 3.5 (new)" and the names of the base models are left unrecorded for that reason.

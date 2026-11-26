# Pilot notes: arXiv 2503.07513 (Song, Hu, Mahowald)

Record: `sources/song2025-fail-to-introspect.yaml`. 3 studies, 16 claims,
2 relations. Added 3 people, 5 orgs, 8 model entries, 2 questions.
`validate.py` and `build.py` are clean.

## (a) Split

Three studies. The split is by analysis, not by the paper's "Exp. 1 / Exp. 2".

| Study | Covers | Why separate |
|---|---|---|
| s1 | Accuracy of each measure and within-model agreement between prompted answers and string probabilities (§3.2.1, §4.2.1, App. B, E.1) | No other-model baseline and no self/other contrast. A kappa claim placed in s2 would inherit `validated_against: other_model` and `varies: self_vs_other`, both wrong for it. |
| s2 | Cross-model test: same-model effect beyond similarity (§3.2.2, §4.2.2, App. C, F, G) | The paper's headline test. |
| s3 | Arguments in §1, §2 and §5: what counts as evidence, and why Binder et al. and Betley et al. found positives | `study_kind: conceptual`. These claims are about fine-tuned models in other papers; attached to s2 they would inherit `elicitation: spontaneous` and the rest. |

Exp. 1 (grammaticality) and Exp. 2 (word prediction) are merged within s1 and
within s2. I could not find a facet that differs between them: same models,
same two measures, same analysis. The difference is the task, which is what
`varies: task` with `levels` and `scope.conditions` are for. Merging is also
the only way the grammar/word-prediction contrast gets recorded at all, since
`task` only exists inside a study. A coder who follows the paper's headings
will get four experimental studies instead, and CLAUDE.md does not say which
is right (see (d) 1).

Not split:

- Base against instruct models, although CLAUDE.md gives exactly that as the
  example of when to split by model. Every result is over pairs drawn from
  all 21 models, so no claim could be assigned to one half. Both formats and
  both layers are coded on the one study.
- The OLMo-only and large-model analyses. They are claims with `scope`.
- Accuracy against dataset labels and within-model kappa are both in s1. By
  the strict inheritance test they should be apart (an accuracy claim inherits
  `validated_against: behaviour`, which is not what accuracy was checked
  against). I judged a fourth study for one check too fine, and put the caveat
  in the facet note.

## (b) Hesitations

**report_target** (lowest confidence in the record). Weighed `own_knowledge`,
`own_behaviour`, `own_internal_state`. The authors say "internal linguistic
knowledge" and "internal states". The check is run against string
probabilities, which is a disposition to output, checkable by running the
system, so `own_behaviour` by its rule. Some prompts ask "which are you more
likely to produce" (behaviour); most ask "which is grammatical" and do not
mention the model at all. Chose `[own_knowledge, own_behaviour]`,
`basis: stated`, `confidence: low`. Rejected `own_internal_state` because
nothing occurrent is involved. The rule for `own_knowledge` ("calibration and
knows-what-it-knows") does not really fit: this is first-order knowledge of
grammar, not knowledge about one's knowledge. I expect coders to disagree here.

**evidence**. Weighed adding `behaviour`. Both measures are log probabilities
and nothing is sampled, so chose `[self_report, output_probabilities]`. The
Direct measure is object-level, which is what `behaviour` is for, but the
`output_probabilities` rule says to use it when the probability is the
measurement. Also unsure that a grammaticality judgment is a `self_report` on
its face; coded it because the authors treat it as one.

**validated_against**. Weighed `behaviour` and `internals`. The authors treat
string probability as ground truth for internal knowledge, which reads like
`internals`, but that value is defined by probes and circuits. Chose
`behaviour` (+ `other_model` in s2). See gap 1.

**construct**. `introspection` is stated. Added `self_prediction` because the
measure is literally how well answers predict the model's own probabilities
and because it lines the study up with Binder. Considered `metacognition`
(the authors' "metacognition more broadly") and left it out: no confidence or
calibration report.

**unit_state**. Weighed `not_applicable` and `forward_pass`. The authors use
"internal states" and "knowledge state". Chose `not_applicable`: the
quantities are standing preferences, measured in a different run from the
report.

**unit_reporter** for base models. Chose `persona` for both kinds of model.
For a base model on raw text the "persona" is the frame speaker, which is a
stretch of the word. `weights` was not available because nothing attributes
the report to the network apart from a speaker.

**object_of_study** and **format**. Two values each, because the model set
mixes base and instruct. `format` has `basis: stated` although only the
chat-template half is stated; raw text for base models is inferred. Whether
the Direct strings were templated for instruct models is not stated.

**varies**. Four decisions:
- `self_vs_other` holds the five pair types as levels. The authors' variable
  is really graded similarity with self as one end.
- `post_training_stage` not coded. The base/instruct pair type compares
  stages of one lineage, but only as a similarity level; nothing is reported
  on whether the outcome differs by stage. Coding it would make the study
  show up for "does introspection differ by post-training stage?", which it
  cannot answer.
- `format` not coded, since no checkpoint is run both ways.
- `prompt_framing` coded on s1 (per-prompt lines in Figs. 5 and 8) but not on
  s2 (correlations averaged over prompts). The s1 case is weak: the text
  draws no conclusion by prompt.
- `model_size` coded with `model_family` and a note that they are confounded.
  The `model_size` definition says "within one family and generation", which
  this is not.

**comparison** on s1. `cross_model` (the size contrast) against `within_model`
(Direct against Meta in one model). Chose `cross_model`; the Direct/Meta
pairing is report against check, not a manipulated condition.

**elicitation**. `[spontaneous, prefilled]`. "My answer is" is appended and
Fig. 1 shows it in the model turn. For base models there is no turn, so
`prefilled` is only half true.

**unit_position** (s3). Coded `weights`, `confidence: low`, from one hedged
sentence ("may be reasonable to question" whether a fine-tuned model predicts
"itself"). Unsure a hedge counts as "takes a position". Kept it because the
design of s2 enforces the same view.

**self_sense** (s3). Added `identity` to `self_facts` for the same sentence.
Thin support.

**aspect** on c4. The authors say "explicit" metalinguistic knowledge is
dissociated from "implicit" generalisations. I mapped explicit to
`represented` and implicit to `functional`. The mapping is mine; the
dissociation is theirs. A stricter reading of "do not fill with the coder's
own reading" would leave it off.

**stance** on c3 and c10. Kappa about 0.25 and r at most .25 are above chance
but low. Chose `against` for a question worded "agree closely". `inconclusive`
was the alternative. The stance depends heavily on how I worded the question.

**Question reuse.** `q-self-prediction-advantage` is the obvious neighbour
and the paper presents itself as qualifying Binder's answer to it. I did not
reuse it because its wording ("given the same behavioural data") describes
cross-prediction training, which this design does not have. Added
`q-self-access-beyond-similar-model`. The cost: no conflict row appears
between Binder c2 and this paper, which is the comparison the database most
obviously exists to show. I linked the two with `relations` instead.

**read_depth**. `full_text`, though I saw no figures, only captions.

**date**. Used the date printed on v3. See (d) 6.

## (c) Gaps

1. **`validated_against` has no value for output probabilities.** `evidence`
   distinguishes `output_probabilities` from `behaviour`; `validated_against`
   does not. This paper's whole premise is that string probability is a
   privileged ground truth, different from sampled behaviour and from a probe.
   Used `behaviour`.
2. **No way to code a similarity-graded other.** `self_vs_other` is binary in
   spirit and `validated_against: other_model` does not say how similar the
   other is. The paper's argument is that this is the thing that matters. It
   is only in `levels`, which is free text and not queryable.
3. **`report_source` lacks two values.** (i) Third-person-available knowledge:
   the report draws on general competence that similar models share (c6).
   (ii) Associations in training data (c16). Neither coded. The first is also
   a "rules a route out" case, which the facet cannot record.
4. **`report_target` has no value for first-order knowledge or competence.**
   `own_knowledge` is defined as metacognitive.
5. **`basis`, `confidence` and `author_term` are per facet, not per value.**
   With two values, one stated and one inferred (`format`, `report_target`,
   `construct`), one `basis` has to cover both.
6. **Model registry cannot hold an unresolved set.** The text says 21 models;
   Table 1 allows 24. I used two family-level placeholders (`qwen-2.5`,
   `llama-3.1`) and two grouped seed entries, which breaks "one entry per
   checkpoint". This also lost the base-to-instruct `derived_from` links,
   which matter for this paper. `llama-3.1` may overlap with the existing
   `llama-3.1-70b`.
7. **No facet or field for quantisation as a fixed condition.** 4-bit for
   models over 70B is in notes only. `precision` exists only under `varies`.
8. **No place for evaluation datasets.** `datasets/` is for training data.
   BLiMP and the Linguistic Inquiry pairs are only in `levels` text.
9. **Conceptual studies.** Eleven required facets on s3 are
   `not_applicable`. For `comparison` the codebook says so, and
   `object_of_study` and `format` follow plainly. The other eight are there
   because nothing fitted, not because of a judgment: `unit_state`,
   `unit_disposition`, `unit_reporter`, `report_target`, `evidence`,
   `validated_against`, `varies`, `elicitation`. `unit_state` could arguably
   be `unspecified` (the authors define introspection as access to "mental
   states" without saying where they live).
10. **Claims about other papers' results** (c15, c16) have nowhere to point
    when the other paper is not in the database (Betley et al.). `about`
    takes only models and datasets.
11. **`read_depth` has no value for full text without figures.** Text
    extraction drops plotted values and axis labels; here that cost the model
    list and all accuracy numbers.
12. **`stance` has no weak-support value**, so a small positive agreement has
    to be `against` or `inconclusive`.

## (d) Instructions

1. **Split rule does not settle "two experiments, same facets".** "One study
   per setup" suggests Exp. 1 and Exp. 2 are two studies; the inheritance test
   says they are one. The worked example splits by section. Say which wins.
   Also say whether a validity check (accuracy) needs its own study.
2. **"Split by model only when the model changes a facet, for example one run
   as a base model and another through a chat template"** reads as an
   instruction to split whenever base and instruct models are both present.
   That is impossible when the analysis is over cross-model pairs.
   `format.yaml` and `object_of_study.yaml` say "if a study compares formats /
   layers, code each", which is what I followed, but "compares" does not
   describe a study that merely mixes them.
3. **`varies: format` rule ("same weights with and without the template")
   and the `format` note ("if a study compares formats ... add format under
   varies")** give different answers for a mixed base/instruct model set.
4. **`varies`: is it everything that differed, or only what results are
   broken down by?** CLAUDE.md says "record the conditions"; the facet notes
   say a value means the study is direct evidence on "does X differ by Y".
   Only `task` has the "breakdown matters" rule. Multiple prompts averaged
   together is the test case.
5. **`self_report` and `report_target` assume the report is visibly about the
   self.** Nothing says what to do when the source treats an object-level
   answer ("is this sentence grammatical?") as an introspective report.
6. **`date` is undefined.** First posting, or the version read? The example
   uses the v1 date and read v1, so it does not disambiguate. The id needs a
   year, which could differ between the two.
7. **Conceptual studies.** Only `comparison` says "use not_applicable for
   conceptual work". CLAUDE.md says every required facet is coded on every
   study, with no guidance for a study that has no data. Also unclear: should
   arguments in an empirical paper's introduction get a conceptual study at
   all, or hang off the experiment as the example's c10 does?
8. **`unit_position` threshold.** "Takes a position" does not say whether a
   hedged aside counts, nor which study it goes on when the view belongs to
   the source as a whole.
9. **Questions.** No guidance on how literally an existing question's wording
   must fit before reuse, and a claim can link to only one question. Strict
   reading means each paper mints its own questions and conflicts never show;
   loose reading puts stances on a question whose wording is false for the
   design. Also unstated: whether `frame` may use any facet (I added
   `elicitation`, `evidence`, `validated_against`), and nothing validates it.
10. **Optional claim facets and mapping.** "Record the source's view, not
    yours" is clear when the source uses the codebook's terms. It is unclear
    when the source argues the matter in its own terms (explicit/implicit)
    and the coder must map them.
11. **Stale names in the codebook.** `construct.yaml` (`identity_persistence`
    rule) and the "Facet file format" example in `codebook/README.md` still
    say `unit_of_self`. `construct.yaml` and `report_target.yaml` are at
    version 0.1 inside a 0.2 codebook, which made me check whether they had
    been reviewed.
12. **Registry depth.** "Only to the depth needed" against "one entry per
    checkpoint" and a validator that requires every study model to be
    registered. For a 21-model paper that is 21 entries plus developers. Org
    `kind` and developer names are not in the paper, so they come from general
    knowledge, which sits oddly with "never from memory"; the example flags
    the same.
13. **`relations`** are not described in README or CLAUDE.md. The enum and
    the validator are the only documentation; direction (`from` is the later
    work) and whether endpoints should be sources or claims are guesses.
14. **`models: []`** on a conceptual study passes validation, but nothing says
    whether to omit the key or leave it empty.

## (e) Reading

- Version read: **v3** (header "arXiv:2503.07513v3 [cs.CL] 23 Sep 2025",
  "Published as a conference paper at COLM 2025").
- How: full extracted text through alphaXiv `get_paper_content` with
  `fullText: true`, read end to end; a second pass over selected pages with
  `answer_pdf_queries` to look for the model list.
- Parts read: abstract; §1 to §5; acknowledgments and reproducibility
  statement; references; appendices A to G; Tables 1 to 8; all figure
  captions.
- Not read: the figures themselves (Figs. 1 to 10 came through as captions
  and stray labels only). Consequences: no accuracy values, no per-pair
  correlations, and no list of the 21 checkpoints.
- Not opened: the code and data repository. A web fetch of it was not
  approved in this session, so I did not retry. Opening it would resolve the
  model list and the 21-against-24 count.
- Earlier versions (v1, v2) were not compared with v3.
- The Binder et al. record was read as the worked example and left unchanged.

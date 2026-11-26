# Reconcile notes: arXiv 2503.07513 (Song, Hu, Mahowald)

Record: `sources/song2025-fail-to-introspect.yaml`, coded against codebook 0.3.
4 studies, 22 claims, 4 relations. `validate.py` and `build.py` are clean.

Added to the registries: 3 people, 5 orgs, 17 model entries, 2 questions.

**What was read in this session.** The whole of v3 as extracted text (figures
as captions only, so `read_depth: text_only`). The authors' repository was
reachable: README, `analysis.R`, the three scripts under `src/`, the model
lists and processing functions of `preparedata.ipynb`, and the file listing.
Data files were not opened. The repository has no pinned commit in the record;
the reading tool does not report one.

**Studies**

| Study | Covers |
|---|---|
| s1 | Accuracy of each measure and within-model agreement between them (§3.2.1, §4.2.1, App. B, E.1) |
| s2 | Same-model effect beyond similarity, all 21 models, both experiments (§3.2.2, §4.2.2, App. C, G) |
| s3 | The same test among the OLMo 2 seed variants only (App. F) |
| s4 | Conceptual: the criterion for introspection and the account of earlier positive results (§1, §2, §5) |

## (a) Disagreements between the two pilot records

| # | What | fable | opus | Decision | Reason |
|---|---|---|---|---|---|
| 1 | Exp. 1 and Exp. 2 | Merged | One study each | Merged | 0.3: headings do not decide. The two experiments share every facet value and differ in task, which is a level of `varies`. |
| 2 | Within-model agreement (kappa, accuracy) | Own study | Claims inside the Exp. 1 study | Own study (s1) | A kappa claim in the cross-model study would inherit `validated_against: other_model` and `varies: self_vs_other`. |
| 3 | OLMo seed analysis | A claim in the cross-model study, narrowed by `scope.models` | Own study | Own study (s3) | 0.3: models that differ on a facet are split when reported apart. App. F is base models on plain text only; in s2 its claim would inherit `chat_template` and `default_persona`. |
| 4 | Arguments in §1, §2, §5 | Conceptual study | Claims on the Exp. 1 study | Conceptual study (s4) | The claims about Binder et al. and Betley et al. concern fine-tuned models; on an experiment they would inherit `elicitation: spontaneous` and this paper's models. 0.3 makes a conceptual study cheap to code. |
| 5 | `unit_position: weights` | On the conceptual study | On all three experiments | On s4 only | It is a view in the argument. What the experiments treat as self is already in `unit_disposition`. Kept at low confidence: both coders doubted that one hedged sentence is a position. |
| 6 | `construct` | `introspection`, `self_prediction` | `introspection` | Both | The authors define their measure as prompted responses that "predict" the model's own probabilities and describe the test as a model predicting itself (§3.1). Five of fourteen prompts ask what the model would produce. |
| 7 | `report_target` | `own_knowledge`, `own_behaviour`, basis stated | `own_behaviour`, basis operational | Both values, basis operational, confidence low | Knowledge of language is the stated target (title, abstract); string probability is what the check runs against. With one stated and one inferred, 0.3 says to use the weaker label. |
| 8 | `validated_against` | `behaviour` | `behaviour` | `output_probabilities` | New 0.3 value; both coders had asked for it. `other_model` is kept on s2 and s3. |
| 9 | `varies`: base/instruct | Not coded | `post_training_stage` | Coded on s2 | Base/instruct pairs are a level with their own coefficient, and one result is about them (their string probabilities differ from self, c5). See (c) 4 for the cost. |
| 10 | `varies`: seed variants | Level of `self_vs_other` | Level of `self_vs_other`; asked for a value | `training_seed` on s2 and s3 | New 0.3 value. Checkpoints are listed in `levels`. |
| 11 | `varies: prompt_framing` | On the agreement study only | On both experiments | On s1 only | Per-prompt results exist only for accuracy and kappa (Figs. 5, 8). The cross-model correlations are averaged over prompts. |
| 12 | `comparison` | `cross_model` | `cross_model` | s1: `within_model`, `cross_model`. s2: `cross_model`, `within_lineage`. s3: `cross_model` | 0.3 takes several values. s1 contrasts two measures within a model and small with large models. s2 contrasts self with other models, some of which are released stages of the same model. |
| 13 | `self_sense` on the conceptual study | `self_facts`, `identity` | No such study | Kept both, confidence low | One claim (c20) is about whether a changed model is the same thing. |
| 14 | `format` basis and confidence | Stated, medium | Stated, high | Operational, high | Only the chat template for instruct models is stated. Plain text for base models and for all Direct scoring is from the code, which settles it. |
| 15 | `unit_reporter` confidence | Medium | Low | Medium | 0.3 now says a base model's implied speaker is `persona` with `frame_speaker`. |
| 16 | Models | 8 entries, two of them family placeholders | 21 entries | 17 entries: 15 released models and one series entry per OLMo size for the seed variants | 0.3: a checkpoint gets an entry only when a claim is scoped to it, and a series is one entry. The placeholders are gone because the repository names every model. |
| 17 | Question for the main result | New `q-self-access-beyond-similar-model` | New question, id `q-privileged-self-access` | New `q-self-access-without-training`, parent `q-privileged-self-access` | Both declined `q-self-prediction-advantage` because its wording assumes training on behavioural data; that still holds. Under a shared parent the dispute with Binder et al. now shows: 28 conflict rows, with trained against spontaneous in the facet difference. opus's id is now the parent's. |
| 18 | Kappa and the r of at most .25 | Linked to a second new question, stance against | No question | Linked to new `q-report-matches-direct-measure`, no parent | It is the paper's second conclusion and other work addresses it. Not under the parent: agreement with one's own probabilities can come from knowledge any similar model shares. |
| 19 | `aspect` | On the argued dissociation claim | Also on the measured kappa claim | Argued claim only (c4) | The source argues a dissociation between explicit and implicit knowledge; the kappa is a measurement. |
| 20 | Where the r of at most .25 sits | Cross-model study | Exp. 1 study | s2 (c12) | It is a statement about every pair of models, self pairs included. |
| 21 | Large-model subset | `scope.conditions` only | `scope.models`, seven models inferred | `scope.models` and conditions (c11) | The cutoff (both models at least 70B) is confirmed in `analysis.R`; the `where` says so. |
| 22 | `date` | 2025-09-23 | 2025-03 | 2025-09-23 | 0.3: the date of the version read. |
| 23 | `read_depth` | `full_text` | `full_text` | `text_only` | New 0.3 value for text with figures as captions. |
| 24 | Relations | Source to source and claim to claim, to Binder | Source to source | Both to Binder, plus `to_external` for Betley et al. and Hu and Levy | 0.3 allows uncoded targets. |
| 25 | Claim grain | 16 claims; pair-type and controlled regressions in one claim | 20 claims; unfiltered set and size hypothesis apart; Binder and Betley in one | 22 claims | One claim per analysis and item set. Kept fable's criterion claim and opus's claims on the validity of the pair types and on string probability as ground truth. Binder and Betley are separate because they get separate relations. |

Left as both coders had it: `unit_state: not_applicable`, `unit_disposition:
weights`, `self_sense: self_facts` on the experiments, `object_of_study`
(`default_persona`, `frame_speaker`), `evidence`, `elicitation`
(`spontaneous`, `prefilled`), the source id, and no split of base from
instruct models in the pooled analyses.

## (b) Pilot content not supported by the source, and what was done

1. **opus: "8 instruct models" and "13 base models"** (facet notes and
   NOTES.md). The repository's list, and opus's own model list, have 7
   instruct and 14 base. Corrected.
2. **opus: no similarity category "falls below self" among large models**
   (pilot c9, c15). Table 7b has negative coefficients (for example same
   family -0.021 and other -0.015 on the filtered grammaticality items, same
   family -0.025 on randomseq). None is significant. c11 now says none is
   significantly below self.
3. **opus: the released OLMo models are "weight averages of their three seed
   variants".** App. F says only that they are final models "with averaged
   weights". Reworded, and `derived_from` left null.
4. **opus: relation note says the paper is "also described as an extension in
   method"** of Binder et al. The paper does not say that. Dropped.
5. **opus: models "choose at random on nonsense and randomseq"** under both
   measures (pilot c12). §4.2.1 says so, but App. E.1 limits it to prompted
   choices and reports a lean in the probability measure. Qualified in the
   note on c1.
6. **fable: "all 1,048" minimal pairs.** The paper gives 670 and 378 and no
   total; the repository README says 380 for the second figure. The record
   gives the paper's two counts and no sum.
7. **fable and opus: Fig. 1 shows "My answer is" in the model turn.** Neither
   coder saw the figure. The placement is now taken from `src/models.py`.
8. **fable: placeholder entries `qwen-2.5` and `llama-3.1`**, and the note that
   the checkpoints cannot be known. Replaced with the repository's list.
9. **opus: `date: 2025-03`**, taken from the arXiv id. Replaced; see (a) 22.

Checked and confirmed from the repository, which fable could not reach: no
Qwen2.5 32B and no Llama 3.1 405B Instruct were run, although Table 1 allows
both; Direct scores are computed on plain text for every model; instruct
models get a "helpful assistant" system message and "My answer is" in the
assistant turn; the README marks the 70B, 72B and 123B models as 4-bit, where
the paper says larger than 70B. Two things neither pilot record had: the
README's own id list omits Llama 3.1 405B although the notebook, the analysis
script and the outputs include it, and the repository holds unused outputs for
four smaller models. Both are in the note on s1.

Every number in the record was checked against the text or Tables 5 to 8.
Accuracy values and per-pair correlations are in figures and are not quoted.

## (c) Where codebook 0.3 or CLAUDE.md still did not fit

1. **A validity check inside a self-report study.** Accuracy against dataset
   labels sits in s1, whose `validated_against` is `output_probabilities`. By
   the strict test the accuracy claims (c1, c2) inherit a value that is not
   theirs. The alternative is a fifth study with `construct` and `self_sense`
   `not_applicable`. I kept them in s1 and said so in the facet note. The rule
   should say which is wanted.
2. **"Reported apart" treats two subset analyses differently.** The OLMo
   subset became a study because its models share a facet value the pooled set
   lacks. The large-model subset stayed a scoped claim because its models do
   not. Its claim (c11) still inherits `training_seed` though the subset has
   no seed pair; only `scope.conditions` says so. Levels can be narrowed per
   claim and facet values cannot.
3. **`varies` cannot say what role a variable plays.** In s2,
   `training_seed`, `post_training_stage` and `model_family` are grades of
   similarity between the model answering and the model scored. A query for
   "does introspection differ by post-training stage" will return s2, which
   does not test that. A value for graded similarity of the comparison model,
   or a role marker on a `varies` value, would fix it. This is the largest
   judgment call in the record.
4. **No `varies` value for the measurement channel.** The size-by-method
   result (c2) contrasts string probability with prompted answer. That is not
   `prompt_framing`, and it is recorded only in a note.
5. **`self_access` against `self_facts`.** The authors' own term is
   "self-access", and the new value has that name, but its rule requires
   setting or reading a current state. A model's output probabilities on a
   separate pass fall between the two values. Coded `self_facts`, consistent
   with Binder et al.; the codebook should say where output probabilities go.
6. **`report_target` has no value for first-order knowledge.** The definition
   of `own_knowledge` fits ("what the system knows") and its rule does not
   (calibration). Nothing covers an object-level judgment ("is this sentence
   grammatical?") that a source treats as a self-report.
7. **The checkpoint rule, the validator and "list them all" pull apart.** The
   validator needs every study model registered, so 15 released models have
   entries though no claim is scoped to 8 of them. I read "checkpoint" as a
   revision within one model's training. A series entry has one `size` and
   cannot be a `derived_from` parent in any clear sense, and `derived_from`
   cannot express a weight average.
8. **Paper and code disagree, and no rule says which wins.** Table 1 against
   the repository's model list, "larger than 70B" against the README's
   quantisation marks, "> 70B" against "70B or greater", 378 against 380. I
   followed the code for what was run and kept the paper's wording in notes.
9. **Registry facts the source does not give.** The paper names developers
   only by Hugging Face organisation. I registered `qwen-team` as the source
   cites it and expanded "allenai" and "mistralai" to names, flagged as
   unverified. Instruct entries carry `derived_from` on the strength of the
   paper's base/instruct pairing, not developer documentation.
10. **`comparison` has nothing for sibling runs.** Seed variants are not
    stages (`within_lineage`) and were not built for the comparison
    (`training_ablation`). They fall under `cross_model`.
11. **`prefilled` on a base model.** There is no assistant turn; "My answer
    is" is appended to plain text.
12. **Parent questions.** "Yes counts towards yes to the parent" does not say
    what to do with a question whose yes is necessary but not sufficient,
    which is why `q-report-matches-direct-measure` has no parent. The
    conflicts view also pairs every Song claim with Binder c6 (reports
    tracking a change in behaviour), a looser match than the one with c2.
13. **Still open from the log:** mixed `basis` within one facet entry (three
    entries here), `report_source` unable to record a ruled-out route (c15) or
    training-data associations (c22), and `stance` with no value for weak
    agreement (c3 is `against` only because the question says "closely").
14. **Small gaps.** Whether a conceptual study omits `models` (I omitted it);
    `note` on a question is undocumented; `unit_position` does not say whether
    a hedged remark counts or which study carries a source-wide view.
15. **End of session.** CLAUDE.md asks for a `LOG.md` entry and a commit. This
    task ruled both out, so neither was done. The new orgs, models and
    questions need the owner's eye in place of a log entry.

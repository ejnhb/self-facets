# Reconciliation notes: arXiv 2601.01828

Record: `sources/lindsey2026-emergent-introspective-awareness.yaml`, coded
against codebook 0.3. 8 studies, 47 claims, 3 relations.

Registry additions: 1 person (`lindsey-jack`), 13 models (nine production
Claude models, four helpful-only variants), 5 questions. No orgs or datasets.
`validate.py` and `build.py` are clean. The codebook, scripts, CLAUDE.md,
LOG.md and `pilot/` are untouched, and nothing is committed. CLAUDE.md asks
for a LOG.md entry at the end of a session; the task ruled that out, so the
entry is still to be written.

The paper was read again in this session: arXiv v1 as extracted text from
alphaXiv, all 1,707 lines. Figures were available only as captions, and a
second call (`answer_pdf_queries`) returned the same text with no figure
content. `read_depth` is `text_only`.

Ids below: "fable c24" and "opus c22" are pilot ids; plain `s1`, `c29` are ids
in the new record.

## Study map

| New | Content | Pilot (both coders) |
|---|---|---|
| s1 | Injected-thought detection, setup explained, post-trained models | s1 |
| s2 | Control: injection during unrelated yes-or-no questions (§5.5) | part of s1 |
| s3 | Same task on base pretrained models | s2 |
| s4 | Prompts that do not explain injection | s3 |
| s5 | Injected concept against text input | s4 |
| s6 | Prefilled output | s5 |
| s7 | Instructed control of a representation | s6 |
| s8 | Definition and scope of conclusions (conceptual) | s7 |

## (a) Disagreements between the two pilot records

### Facets

1. **`unit_disposition` on the experiments.** fable: `not_applicable` (no
   disposition is reported on). opus: `weights`, low confidence (a capacity
   fixed per checkpoint). Decision: `weights`, medium, on s1 and s3 to s7.
   0.3 says a capacity counts and is coded by what fixes it. s2 is
   `not_applicable`: that control tests no capacity.
2. **`self_sense` on the prefill study.** fable: `[authorship, self_model]`.
   opus: `authorship`. Decision: `[authorship, self_access]` on s6. The report
   is about whether an output was its own, and the design sets an earlier
   internal state and tests whether the judgment uses it, which is what
   `self_access` covers ("report or use").
3. **`self_sense` on the control-of-representation study.** fable:
   `self_model`, low. opus: `unspecified`, because nothing fitted. Decision:
   `self_access`, low, on s7. `unspecified` means the source does not say,
   and here it does; `self_model` is ruled out by its 0.3 rule. See (c)3.
4. **`read_depth`.** fable: `full_text`. opus: `partial`. Decision:
   `text_only`, the 0.3 value for exactly this case.
5. **Base models in the registry.** fable: `models: []`. opus: a placeholder
   entry `claude-base-unnamed`. Decision: empty list, no entry. 0.3 says not
   to register a model the source does not name.
6. **`comparison` on the base-model study.** fable: `within_lineage`, low.
   opus: `within_model`, low. Decision: `[within_model, within_lineage]`, low,
   now that the facet takes several values. The lineage is assumed, not
   stated; see (b)7.
7. **`elicitation` on the control-of-representation study.** fable:
   `prompted`. opus: `[prompted, prefilled]`. Decision: `prompted`. The
   paper does not say the sentence was prefilled; see (b)1.
8. **`object_of_study` basis on the prefill study.** fable: operational.
   opus: stated. Decision: stated, pointing at §7, which names the Assistant
   character as the speaker whose outputs the model produces.
9. **`author_term` for the reporter.** fable: "the model". opus: "the
   Assistant". Decision: "the model" on s1, s4 and s5, which is the word the
   paper uses there, and "the Assistant" (stated) on s6.
10. **Concept categories in `varies`.** fable: a level of
    `activation_intervention`. opus: a level of `task`. Decision:
    `activation_intervention`; the category is the kind of vector injected.
    With the yes-or-no control moved to s2, s1 no longer codes `task`.
11. **Conceptual study.** fable: `construct: introspection`, `self_sense:
    self_model`, plus `unit_state` and `unit_reporter` as `unspecified`.
    opus: `construct: [introspection, self_prediction]`, the same
    `self_sense`, and a run of `not_applicable`. Decision on s8: 0.3 light
    coding (three facets only); `construct: [introspection,
    self_prediction]`; `self_sense: [self_access, self_model]`, stated,
    because criteria 1 to 3 describe access and criterion 4 a
    self-representation. The finding that the definition names no unit is in
    the study note.
12. **Judge model.** fable: a `role` on `claude-sonnet-4`. opus: in the
    design text only. Decision: both.

### Claims and questions

13. **Is a control result linked to the question it protects?** Of the
    three §5 controls, opus linked all as `supports` (opus c4, c6, c7) and
    fable linked only the prompt variant. Decision: the prompt variant (c15) and the after-prefill
    control (c30) keep `supports`, as both coders had it, because they are
    runs of the task itself. The yes-or-no control (c18) has no question and
    names s1 in `compares`: it measures answer bias, and a stance would put
    s2's facets into the conflicts view.
14. **Random and negated vectors.** fable: a measured claim with no question
    and a separate hypothesised claim for the suspected confabulation. opus:
    one claim, linked as `supports`. Decision: fable's two claims (c6, c7),
    no question. The measured result and the author's suspicion have
    different evidence kinds, and identification cannot be scored for these
    vectors.
15. **Unverified details of the replies.** fable: `argued`. opus:
    `hypothesised`. Decision: `hypothesised` (c8). The source says they
    "may be" embellishments and tests nothing. `report_source: [context]` is
    kept, as both coders had it, with a note that it rests on a parenthesis.
16. **Injected concept against text, Opus 4.1.** fable linked it to a
    question of its own (`q-injected-state-distinguished-from-input`); opus
    left it without one. Decision: c24 `supports`
    `q-injected-state-report`. A separate question for one design was not
    needed.
17. **The same task across models.** fable: the distinguished-from-input
    question. opus: the capability question. Decision: c25 `supports`
    `q-injected-state-report` and lists the capability question under
    `other_questions`. The prefill cross-model claim (c31) is handled the
    same way.
18. **Common or separate mechanisms.** fable: two `argued` claims with
    opposite stances on a new question `q-introspection-common-mechanism`.
    opus: a measured claim for the layer difference, an argued claim for the
    inference, no question. Decision: opus's shape (c27; c33 and c34), no
    question, with the other studies named in `compares`. The measured layer
    facts and the inference are different links. The question was dropped to
    keep the list small; add it when a second source bears on it.
19. **The paper's reading of the self-prediction literature.** opus linked
    it to `q-self-prediction-advantage` as `supports` and flagged that as a
    possible mistake. fable left it unlinked. Decision: unlinked (c45). The
    claim accepts the advantage and denies that it is introspection, so one
    stance misstates it, and it is a reading of others' data. The `critiques`
    relation to Binder et al. carries the link.
20. **Capability trend as an argued claim.** opus had one, in the conceptual
    study (opus c37). fable had none. Decision: kept as c17, moved to s1 with
    `compares` to s4, s5 and s6, so that it inherits experiment facets and
    not the empty facets of a conceptual study.
21. **Post-training reading (§2.5, §10.1).** fable: no question. opus:
    `supports` the post-training question. Decision: `supports`, `argued`
    (c14). `disposition: [refusal]` is kept, as both had it, with the
    source's word "reluctant" in the note.
22. **`report_source: current_state`.** fable coded it on the main detection
    claim, the prompt-variant claim and the prefill claim. opus coded it on
    the main detection claim only. Decision: on c2 and c29, where the paper
    argues that the report depends on internal state with the text held
    fixed (§2.1, §2.3). Not on c15, which rules out a different alternative.
23. **`aspect` on denial with visible influence.** fable coded
    `[represented, functional]`. opus did not. Decision: not coded (c3).
    `functional` is defined as a disposition driving behaviour; here an
    injected state does. The source does not frame it that way either.
24. **Helpful-only results.** fable: one claim, scoped by conditions. opus:
    one claim, scoped to nine models. Decision: three claims. c11 (false
    positives, post-training question, no model scope because the text does
    not say which variants), c12 (the three variants with true above false
    positives, scoped to them, `supports` `q-injected-state-report`), and
    c13 (footnote 10 on the helpful-only Opus 4).
25. **"No trend among the other models".** fable scoped by conditions. opus
    scoped to seven production models. Decision: conditions (c10). The text
    says "among other models" and does not exclude the helpful-only ones.
26. **Relation `from`.** fable: the claim. opus: the source. Decision: the
    claim (c45).
27. **Questions.** fable added seven, opus five. Decision: five.

    | New question | Parent | Replaces |
    |---|---|---|
    | `q-injected-state-report` | `q-privileged-self-access` | fable `q-injected-concept-self-report` and `q-injected-state-distinguished-from-input`; opus `q-detect-injected-state` |
    | `q-output-ownership-uses-prior-state` | `q-privileged-self-access` | fable's of the same id; opus `q-ownership-uses-prior-state` |
    | `q-introspection-increases-with-capability` | none | fable's of the same id; opus `q-introspection-tracks-capability` |
    | `q-introspection-differs-by-post-training` | none | fable's of the same id; opus `q-post-training-elicits-introspection` |
    | `q-instructed-control-of-internal-state` | none | fable's of the same id; opus `q-intentional-control-of-representations` |

    The capability and post-training questions have no parent because yes to
    them does not count towards yes on privileged access, and under the
    parent they would conflict with every detection claim. The capability
    question is worded as "introspective access", not accuracy of reports,
    because in the prefill study the stronger effect is a less accurate
    report.

### Where both coders agreed and 0.3 changes the answer

28. **`self_sense: self_model` to `self_access`** on s1, s3, s4 and s5.
29. **`comparison`** is `[within_model, cross_model]` on s1 and s4 to s7.
30. **Production against helpful-only** is `varies: post_training_recipe`,
    not `post_training_stage`.
31. **`construct: metacognition` to `self_regulation`** on s7.
32. **`origin: [post_training]`** is now coded on the base-model conclusion
    (c20). Both coders had left it off for want of the value.
33. **The yes-or-no control is its own study (s2).** Both coders kept it in
    s1 and both noted that its claim inherited a wrong `report_target`. The
    0.3 test says to split when that happens. The cost is in (c)2.
34. **`unit_state` on the text-input study** is `forward_pass`, where both
    coders had `conversation`. 0.3 says a state applied over several
    positions and read in the same pass is `forward_pass`, and nothing is
    generated between the injected sentence and the answer. The prefill
    study stays `conversation` because the state is consulted a turn later.
    Both are medium; see (c)4.
35. **Base models stay a separate study (s3).** The 0.3 rule could be read
    either way; see (c)1. With the split, the conflict between c2 and c19
    shows `format`, `object_of_study` and `post_training_stage` as the
    differences, which is what the paper's own conclusion turns on.
36. **`fresh_copy`** (raised by opus) is not coded. 0.3 says a no-injection
    control trial is covered by `known_intervention`.

## (b) Pilot content not supported by the paper

1. **"The Assistant turn is prefilled with the sentence ... so no output is
   generated"** (opus s6 design and `elicitation` note). The appendix prompts
   show the sentence in the Assistant turn, and the text speaks of "the
   tokens of its response". Whether it was sampled or supplied is not said.
   s7 now says so and does not code `prefilled`.
2. **Prefill effect "relative to no injection or a random other concept"**
   (fable c24) and **"against both ... controls, without stopping it from
   transcribing the sentence"** (opus c22). The running text describes these
   conditions and says the reduction is significant in a layer range. It
   does not report the random-concept or transcription results for Opus 4.1;
   they are in Fig. 20, which neither coder nor I could read. c29 states only
   what the text states and says the rest is in the figure.
3. **"Answer immediately" scoped to Opus 4.1 and Opus 4** (opus c20). The
   text says "the Opus models"; Opus 3 is one too. c26 has no model scope.
4. **Failure modes scoped to Opus 4.1** (opus c3). The examples in §5.3 are
   not attributed to a model. c3 has no model scope.
5. **"Did not correlate" scoped to the seven other production models** (opus
   c9). See (a)25.
6. **The common-mechanism claim** (fable c21) names the two tasks as the
   paper's. §2.5 says only "two of the introspective behaviors"; which two
   follows from §6 and §7. c27 keeps the claim and says so.
7. **Base against post-trained as one lineage** (`post_training_stage` and
   fable's `within_lineage` in pilot s2). The paper says "some base
   pretrained models" and never says they are the bases of the tested
   production models. The values are kept on s3 at low confidence with that
   stated; no claim depends on it.
8. **`claude-base-unnamed`** (opus registry). Removed; see (a)5.
9. **Capability question worded as accuracy** (both pilots linked the
   prefill cross-model result to "more accurate reports"). In that study
   injection makes the report less accurate. The question was reworded; see
   (a)27.

Everything else I checked held: the 20%, 18% of 50, 42% against 20%, 2 of 50,
9 of 100, 0 in 100 and chance 10% figures, the strength sets, the trial
counts and the layer statements are all in the text as the pilots gave them.
No per-model number from a figure is in the record.

## (c) Where codebook 0.3 or CLAUDE.md still did not fit

1. **"Reported apart" against "compare" in the split rule.** The base-model
   results have their own figure (apart), and the only conclusion drawn from
   them is a comparison with the post-trained models (compare). The rule
   gives opposite answers for the two. I split, and used `compares`. The
   consequence is a `varies: post_training_stage` whose two levels sit in
   two studies. The rule needs a tie-break, for instance: split when any
   result is reported apart, and put cross-study contrasts in `compares`.
2. **Controls.** The 0.3 test makes the yes-or-no control a one-claim study,
   and its facets fit badly. `validated_against` has no value for an answer
   key set by the experimenter (this will come up again for self-knowledge
   benchmarks); I used `not_applicable` at low confidence although the study
   does collect self-report. `self_sense` (`self_facts`, low) and
   `construct` (`introspection`, low, as the construct argued about) are
   forced. There is no guidance on whether a control gets a stance, or on
   whether `compares` is the right way to tie it to the study it protects.
3. **`self_sense` has nothing for the self as regulator of its states.** 0.3
   added `construct: self_regulation` but no matching sense. s7 is
   `self_access`, low.
4. **`forward_pass` against `conversation` for a state on earlier positions.**
   s5 and s6 are mechanically alike: a vector on earlier tokens, read later,
   with nothing sampled in between. The 0.3 wording sends one to
   `forward_pass` ("read in the same pass") and the other to `conversation`
   ("persists across turns"). If the intended line is whether the model
   generates in between, both are `forward_pass`.
5. **Registry rules pull three ways.** "List them all", "an entry only when
   a claim is scoped to it" and "do not register a model the source does not
   name". The paper says helpful-only variants of all nine models were used
   and names four. I registered the four, each of which has a claim scoped
   to it. It is not clear whether the checkpoint rule is meant for released
   models at all; I registered all nine production models, as the worked
   example does. A study on unnamed models has `models: []` and its claims
   cannot use `scope.models`. Siblings that share an unregistered base
   cannot be linked (`derived_from` is null on the helpful-only entries).
6. **Stage contrast with the lineage unstated.** `post_training_stage` and
   `within_lineage` both require one lineage. There is no way to say "the
   source treats this as a stage contrast and does not identify the
   lineage" other than low confidence and a note.
7. **`report_source: current_state` says "present" state.** In the prefill
   study the state the report depends on is at earlier positions. And the
   rule does not say whether a passing remark ("likely primed by the
   prompt") is enough to code `context`.
8. **A manipulation that makes a report less accurate.** `validated_against`
   records what counts as correct. In s6 the informative result is an
   induced error, and nothing records that.
9. **Moderator questions.** "Does X differ by capability or post-training"
   cannot sit under a parent, and inside one study its supporting and
   opposing claims (c9, c10) differ only by `scope`, which the conflicts
   view does not show. Already open in LOG.md.
10. **Parents make every child conflict with every other.** c19 (base models
    fail) now conflicts with Binder's supporting claims, and Binder's c8
    with every supporting claim here. That is the design, but most of those
    29 pairs are not disputes.
11. **Where an argued reading of an experiment goes.** In the conceptual
    study it inherits no facets; in the experiment it inherits facets that
    describe data it did not produce. I put readings of one experiment with
    that experiment and positions on definitions in s8. CLAUDE.md does not
    say.
12. **Light coding drops a finding.** Both pilots had `unit_state:
    unspecified` and `unit_reporter: unspecified` on the conceptual study as
    findings. Under 0.3 they are left out and read as `not_applicable`,
    which says something different. The point is now only in the study note.
13. **Still missing fields.** The grading method and judge model (one `role`
    string cannot say subject and judge); layer as a place of readout (s7);
    a relation kind for "accepts the result, disputes the label".
14. **Mixed basis or confidence in one entry.** Came up on s3 (`comparison`:
    one value certain, one assumed) and s6 (`construct`: one stated, two
    operational). Already open in LOG.md.
15. **"One or two sentences."** Hypothesis claims and claims that need a
    design detail are tight at two. Five claims were cut back to fit, which
    cost the explicit "not tested" that `evidence_kind: hypothesised` now
    has to carry alone.

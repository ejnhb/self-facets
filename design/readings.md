# Readings: design (2026-11-26; built in codebook 0.7)

Status: built in codebook 0.7, with three additions the examples called for:
links moved out of the records into `links/`; questions can `require` facet
values, which is what gives a reclassification something to act on; and a
selector can test a model field (`model.post_training_reached`). The text
below is the proposal as written, with those changes noted where they bear.

## The problem

The repo wants three things at once:

1. **Coding a new paper is cheap.** A coder records what the paper did and
   found, and stops.
2. **Posing a new question is cheap.** It should not mean revisiting every
   coded paper.
3. **Readings can differ from the authors'.** A reader may think a study shows
   something other than what its authors say it shows, and two readers may
   differ. A record should not have to choose.

At present a claim's link to a question, and its stance, sit inside the source
record. That makes (2) expensive (a new question means a pass over every paper)
and hides (3): a disagreement about what a result means looks like a coding
error.

## Three layers

- **Records** hold what the paper did and found: studies, facets, claims. A
  careful coder should be able to agree on them. Where the authors' own term
  differs from what the design shows, the record keeps both (`author_term`,
  `basis: stated` or `operational`).
- **Readings** are lenses over the records. A reading changes, under the lens
  only, how some studies or claims are read. It never edits a record.
- **Views** pair a question with a chosen set of readings. A question is
  answered through a view; the same question can be compared across views.

Questions stay reading-agnostic and readings stay question-agnostic. A question
finds its evidence through its `frame` and `needs`; a reading changes facets;
the view applies one to the other.

## A reading

```yaml
- id: r-short-name
  status: argued            # grounded | argued | speculative
  statement: >
    What the reading holds, in a sentence or two.
  applies_to:               # one of the two
    selector: {report_readout: logit_choice}     # a facet query; applies to papers coded later too
    # targets: [source.c2, source.s1]            # or named claims or studies
  effect:
    reclassify:             # under the lens only
      - {facet: evidence, from: self_report, to: not_applicable}
    reinterpret: >          # optional: an alternative explanation, kept beside the result
      ...
  sources:                  # optional: published works that make or support the argument
    - "Author et al. (year), title"
  tested_by: >              # optional: what would settle it, for readings that are hypotheses
    ...
```

- `status`: `grounded` follows from the study's own design facts; `argued` has
  a case the design does not settle; `speculative` is a lens worth trying.
- `reclassify` is the working effect. Excluding a study from a question is
  reclassifying a facet the question needs to `not_applicable`; including a
  study the authors did not frame that way is reclassifying a facet so it
  matches the question's frame. It happens only inside a view.
- `reinterpret` changes no counting. It attaches an alternative explanation to
  the matched claims, for the reader of the view.
- `tested_by` is optional: some readings are hypotheses, and some are filters
  that are useful for one question and not another.
- A published critique is a reading whose `sources` is that critique.
  `relations` can point at it.

## A view

```yaml
- id: v-short-name
  question: q-some-question
  readings: [r-one, r-two]
```

The build answers a question through a view: it applies the readings'
reclassifications to the matched studies, then finds evidence and conflicts as
now. The useful output is the difference between views: which supports and
conflicts appear or vanish when a reading is applied.

## Where a misclassification surfaces

- **When the design settles it, in the records.** The coder codes what the
  study did, and keeps the authors' term beside it. A build view can list every
  study whose stated term and operational coding diverge, with no reading
  needed.
- **When it is contested, in a reading.** A claim about what a result really
  shows, which the design alone cannot settle, becomes a reading.
- **The consequences show in conflicts,** computed through views.

## Worked examples from published sources

**1. A logit readout is not a text answer.** Wang et al. (2024) report that
first-token probabilities in instruction-tuned models do not match the answers
the models give in text. Song et al. (2025) cite this and append "My answer is"
before reading probabilities; Rubin et al. (2026) list scoring nine candidate
labels, instead of free generation, among their limitations.

```yaml
- id: r-logit-readout-not-answer
  status: argued
  statement: An answer read from logits or token probabilities is not the answer the model would give.
  applies_to: {selector: {report_readout: [logit_choice, probability]}}
  effect:
    reclassify: [{facet: evidence, from: self_report, to: not_applicable}]
  sources: ["Wang et al. (2024), \"My answer is C\": first-token probabilities do not match text answers in instruction-tuned language models, Findings of ACL"]
  tested_by: The same items asked for a generated answer, compared with the logit or probability readout.
```

Applied to `q-privileged-self-access`, this lens would move Rubin et al.'s
answers and Song et al.'s prompted responses out of the self-report evidence,
while their probe and direct measurements stay. Whether that changes the
conflict between Song et al. and Binder et al. is exactly what the view would
show.

**2. Song et al.'s critique of Binder et al.** Song et al. argue that a model
predicting itself better than a different model does may reflect how different
the two models are, not privileged access, and that a fine-tuned model may not
be "itself" (Song et al. 2025, §1).

```yaml
- id: r-similarity-uncontrolled
  status: argued
  statement: >
    A self-over-other advantage counts as evidence of privileged access only when the
    comparison model is about as similar to the reporter as the reporter is to itself.
  applies_to: {selector: {validated_against: other_model, varies: self_vs_other}}
  effect:
    reinterpret: The advantage may reflect differences between the models rather than self-access.
  sources: ["Song, Hu and Mahowald (2025), Language models fail to introspect about their knowledge of language, COLM"]
  tested_by: Self against seed variants or base/instruct pairs, controlling for similarity (as in Song et al. s2, s3).
```

This one shows a gap: "the comparison model is about as similar" is not a facet,
so the selector over-matches (it also catches studies that did control for
similarity). Either the reading names its targets, or similarity control
becomes something the record captures.

## What the examples show so far

- Reclassify plus reinterpret covered both. Neither needed a separate
  exclude or include.
- Selectors can only use facets. Conditions that live in free text (`levels`,
  such as an injection layer) or in no field at all (whether similarity was
  controlled) force a reading back to named targets. That is a reason to
  consider which such conditions deserve to be facets.
- Some readings will want to select on training history (for example, models
  with or without a given post-training stage). That needs the model
  registry's `stage` coded, which today is mostly null.

## As built (0.7)

- Readings in `readings/`, views in `views/`, links in `links/` (one file per
  source). Readings from outside the shared layer can apply to its claims by
  id; nothing here points back.
- A reclassification acts through a question's `requires`: a claim whose
  values, after the lens, no longer meet them stops counting on that question.
  Without `requires` a reclassification shows in the claim's facets and in
  conflict facet differences, but changes no count.
- The build writes `view_evidence` (every linked claim: its stance on the
  view's question, whether it counts without readings and under the view, and
  which reading excluded it), `view_diff`, `view_conflicts`,
  `view_reinterpretations` and, for which-questions, `view_answers`.
- First result, from the two example views on `q-privileged-self-access`
  (which now requires `evidence: self_report`): with no readings, 27 linked
  claims count; under r-logit-readout-not-answer, 16 do. The 11 that drop are
  Rubin et al.'s logit-readout claims and Song et al.'s probability-readout
  claims, which leaves Binder et al.'s supporting evidence without Song et
  al.'s opposition. Whether the conflict between them survives depends, in
  part, on whether a probability readout counts as a self-report.

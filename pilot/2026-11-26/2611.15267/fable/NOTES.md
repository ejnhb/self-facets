# Pilot notes: rubin2026-closer-look-introspection

Paper: Rubin et al., "A Closer Look at Language Model Introspection: Probing
Information and Reporting", arXiv 2611.15267.

Record: `sources/rubin2026-closer-look-introspection.yaml` (4 studies, 15
claims). Registry additions: 6 people, 2 orgs, 17 models, 5 questions, no
datasets. `validate.py` and `build.py` are clean. No codebook, script or
CLAUDE.md edits, no LOG.md entry, nothing committed.

## (a) Split

The paper describes two experiments (a prompted pretraining sweep and a
no-prompt experiment). I coded four studies. The principle I applied was the
test in CLAUDE.md: split only where a named facet would be wrong for some
claim.

| Study | Content | Why it is separate |
|---|---|---|
| s1 | Probe and model answer across pretraining checkpoints (§4.1, Figs. 2, 3) | The base case. |
| s2 | Probe and model answer by injection layer and direction type, released 32B base only (App. C.2) | `comparison` takes one value. s1 is `within_lineage`; the layer-6 against layer-0 contrast is one checkpoint under two conditions, `within_model`. `varies` also differs (`activation_intervention`, not `pretraining_progress`). |
| s3 | Probe-only analyses of the same prompted sweep: step 0 against shuffled labels, strength profiles at three checkpoints (§4.1, App. C.3, Fig. 4) | These claims use no model answer. In s1 they would inherit `evidence: self_report`, `unit_reporter`, `report_target: injected_state` and `validated_against`, none of which describe a probe-only result. |
| s4 | No-prompt localization in random networks, with the pretrained comparison, transfer test and attention-blocking control (§4.2, App. D) | Different input (no setup, question or answer stub), different models, no self-report, different things varied. |

Things I kept together and was unsure about:

- **s3 is not a separate setup.** It is the same forward passes as s1, read
  with a different instrument. "One study per setup" says keep it in s1; the
  inheritance test says split. I followed the test. A coder following the
  heading would produce three studies.
- **s4 bundles four manipulations** (strength, readout distance, random
  against pretrained, text and numbering transfer) plus the attention-blocking
  control. The bullet "different topics (... what is varied) are different
  studies" says split; the inheritance test says no claim gets a wrong value,
  only extra `varies` values. I kept one study and scoped claims with
  `scope.conditions`.
- **Random and pretrained networks in s4** are one study per the "different
  models are not different studies" rule. No facet changes between them.
- **The fixed-setting analysis (Fig. 2) and the selected-setting curves
  (Fig. 3)** are both in s1. They differ in analysis, not in any facet.
- **Left out:** the App. B.4 calibration against Hahami et al. (a residual
  norm measured on Llama-3.1-8B-Instruct). It is a method note with no
  finding, so no claim and no model entry.

Claims c4 (argued) and c5 (hypothesised) are the paper's overall
interpretation and draw on all four studies. A claim must belong to one study,
so they sit on s1 and inherit only its facets.

## (b) Hesitations

**unit_state** (s1 to s3 `forward_pass`, medium; s4 `[forward_pass,
conversation]`, low). The perturbation is added at one sentence's tokens and
read at a later token, all within one call. The guidance says "a
single-position activation is forward_pass" and "something that ... sits in
the cache is conversation". This state is neither single-position nor built
up over many passes. `units.yaml` defines a forward pass as "producing one
token", and on that per-token reading the perturbed sentence activations are
in the cache by the time the answer position runs, which would make every
injection-then-report study `conversation`. I chose `forward_pass` because the
experiment is literally one pass, and added `conversation` on s4 because
persistence across 256 later tokens is what s4 tests. I am not confident a
second coder would do the same.

**unit_disposition** (s1, s2 `weights`, low; s3, s4 `not_applicable`). The
guidance says `not_applicable` "when the study is only about an occurrent
state". s1 is about an occurrent state and about a capacity (answering the
localization question) that changes from checkpoint to checkpoint. The
definition of a disposition lists preferences, traits, stances and patterns of
behaviour, and does not say whether a capacity counts. I coded `weights`
where a behaviour of the model is measured and `not_applicable` where only
the probe is.

**unit_reporter** (s1, s2 `weights`, low). Options were `weights`, `persona`
and `unspecified`. The guidance is written for chat studies and sets a high
bar for `weights` ("a way to attribute the report to the network apart from
any persona"). Here there is no trained persona at all (pretraining
checkpoints, one of them untrained), no role tokens, a prompt that says "the
model" in the third person, and a logit readout. I took that as meeting the
bar. The other reading is `persona` with `object_of_study: frame_speaker`,
treating the answerer implied by the document as a character the network
computes. That is odd for a step-0 network, which computes no character.

**self_sense** (all `self_model`, low). Options were `self_model`,
`self_facts`, `not_applicable` and `unspecified`. The rule for `self_model` is
"use when the study locates, probes or intervenes on such a representation",
and the paper probes for information about the system's own perturbed state,
so the rule fires. But the paper's argument is that this information is a
surface trace present even in random networks, which is close to saying it is
not a self-model. Coding s4 (untrained, unprompted networks) as `self_model`
reads badly; `not_applicable` was the alternative. I kept `self_model` on all
four so the studies line up, and said so in the notes.

**object_of_study** (s1, s2 `frame_speaker`, medium; s3, s4
`not_applicable`). `frame_speaker` says "use for base models", which fits.
`actor` was considered and rejected: there is no persona to displace. For the
probe-only studies there is no persona-level target.

**construct** (all `introspection`, stated). The authors frame everything as
introspection, but s3 and s4 measure linear decodability of a perturbation
trace, and the paper's point is that this may fall short of introspection. I
followed "prefer the source's framing".

**report_target** (s1, s2 `injected_state`). Clear, but the value does not say
whether the report is detection, localization or identification of content.
The paper and its related work treat those as different tasks.

**evidence** (s1, s2 `[self_report, output_probabilities, internals]`). The
answer is the highest logit among nine labels at one position. It is a
forced-choice answer about itself (so `self_report`) and it is read from
logits without generation (so `output_probabilities`). The rule for
`output_probabilities` talks about the probability assigned, and here only
the argmax is used. I coded both.

**validated_against** (s1, s2 `[known_intervention, other_model]`, medium).
`known_intervention` is clear. The paper's central comparison is the answer
against a linear probe. `internals` names probes but its rule is "a report
counts as correct if it matches an internal measurement", which is not what
happens. `other_model` is "another system's performance at the same reporting
task ... third-person baselines", which is the probe's role, though a probe is
not a model. I used `other_model` as the closest value. For s3 and s4 I used
`not_applicable` because there is no self-report; see (c).

**varies**.
- s1: the released base differs from the end of stage 1 by mid-training and
  long-context training. That is not "position along pretraining" and not
  "post-training". I put it as the last level of `pretraining_progress`.
- s1: `model_size`. The rule says "use when size is the intended contrast".
  The paper runs 7B and 32B and says the sweep tests dependence on size, but
  reports almost nothing by size in the text. I coded it.
- s4: `pretraining_progress` for random against pretrained networks, although
  the random networks are not the lineage's step 0 and the authors decline to
  use the contrast. `prompt_framing` for the text and numbering transfer test,
  although no question is being framed. `context` for readout distance.
- s2: the sweep ran five layers and five strengths on this checkpoint but the
  text reports two layers at one strength. "Conditions actually used" could
  mean either. I listed the reported ones and noted the rest.

**comparison** (one value). s4 has three structures at once (conditions within
a network, random against pretrained, injected against uninjected). I coded
`within_model`.

**elicitation** (s1, s2 `[steered, spontaneous]`; s3, s4 `steered`).
- `spontaneous` or `prompted`: the question is zero-shot, but the setup text
  tells the model its internal processing may be altered. The paper itself
  calls this the "prompted" task and calls s4 "without setup instructions".
  The codebook's `prompted` is about examples and induction procedures, so I
  chose `spontaneous`.
- `prefilled`: the prompt ends with a written answer stub. The rule speaks of
  the assistant turn, and plain text has none, so I did not code it.
- For s3 and s4 no report is elicited. I read "capacity ... brought out" as
  covering the decodable trace, which exists only under injection.

**report_source on c2** (`current_state`). The facet is to record the source's
view. The source says localization "shows that a model can report something
about its internal computation" and the design holds the text fixed, so a
fresh copy reading the same text could not answer above chance. The source
also argues the reported thing is a shallow trace. I coded `current_state` and
explained in the note; a stricter reader might leave it off.

**origin on c3** (`pretraining`). The source says reporting develops without
post-training. The number is for the released base, which includes
mid-training. I did not add `midtraining` because the source does not
attribute anything to it.

**Model registry.** I registered all sixteen OLMo 3 checkpoints because the
registry header says "one entry per checkpoint that some study ... touches",
and one composite entry for the three random-weight networks. See (d).

## (c) Gaps

Values I wanted:

- **`validated_against`: an external decoder or probe as baseline.** Reading
  the same answer off the activations with a trained classifier is a common
  comparison in this literature. `other_model` and `internals` each fit half.
- **`origin`: architecture or initialisation.** The paper's headline for s3
  and s4 is that the signal is there with random weights. All `origin` values
  are training stages or context. Left uncoded on c9 and c11.
- **`varies`: mid-training or pretraining phase.** `origin` and
  `stage_method` have `midtraining`; `varies` has only
  `pretraining_progress` and `post_training_stage`.
- **`varies`: input text or format changes with no question** (s4 transfer
  test). `prompt_framing` assumes a question; `task` assumes something asked
  about.
- **`report_target`: no way to separate detecting, locating and identifying
  an injected state.**
- **units: nothing for the speaker a plain-text frame implies.**
  `object_of_study` has `frame_speaker`, but `unit_reporter` must choose
  between `persona` and `weights`.
- **`elicitation`: answer stubs in raw text**, and no value for "nothing
  elicited; an internal signal is measured".
- **`comparison`: injected against uninjected or shuffled-label control.**
  Probe-only studies have this as their main structure.

Facets that were missing:

- **Ground truth and controls for a non-report measurement.**
  `validated_against` is defined for the self-report only. In s3 and s4 the
  probe is scored against the known injection site and against shuffled-label,
  permuted-label, norm-only and uninjected controls. All of that is in notes.
- **The dissociation between information present and information reported.**
  This is the paper's main result. `aspect` (represented or functional) is
  the nearest facet and does not fit, so it is carried only by the question
  `q-perturbation-probe-exceeds-report`.
- **Per-value basis, confidence and note.** The long form has one `basis`,
  `confidence` and `note` for the whole facet. In `validated_against:
  [known_intervention, other_model]` the first is certain and the second is a
  stretch, and the record cannot say so except in prose.
- **Basis or confidence on optional claim facets.** `report_source` and
  `origin` are bare lists.
- **Selection of settings.** The main setting was chosen after looking at the
  sweep, and other curves pick settings per measure on held-out seeds. Nothing
  records post-hoc or selected conditions except free text.
- **Relations to uncoded sources.** The paper uses the method of Hahami et al.
  2025 and extends Fornasiere et al. 2026. `relations` only accepts ids
  already in the database, so `relations` is empty.
- **A claim that rests on several studies** (c4, c5).

`unspecified` and `not_applicable` used only because nothing fitted:

- `validated_against: not_applicable` on s3 and s4. There is validation, just
  not of a self-report.
- No use of `unspecified`.
- `unit_disposition`, `unit_reporter`, `report_target` and `object_of_study`
  are `not_applicable` on s3 and s4, and I think correctly. With `self_sense`
  being a low-confidence fit too, most of the self-related facets say nothing
  about half of this paper.

## (d) Instructions

1. **"One study per setup" against the inheritance test.** The heading and the
   README define a study as a setup. The test defines it by facet inheritance.
   They disagree when one data collection is analysed through two evidence
   channels (s1 and s3). The bullet "different topics (... what is varied) are
   different studies" disagrees with the test in the other direction: a
   crossed design varies several things and no claim inherits a wrong value
   (s4). It would help to say which wins, and whether an extra `varies` value
   counts as "wrong for" a claim.
2. **Intermediate checkpoints: models or levels?** `models/models.yaml` says
   one entry per checkpoint touched. CLAUDE.md says registries stay small.
   `varies: pretraining_progress` with `levels` already lists the checkpoints
   as text. I ended up recording them twice (16 model entries and 8 levels),
   and a claim can be narrowed by `scope.models` or by `scope.conditions` with
   no rule for which. Two coders will differ here.
3. **Models the authors made.** `developer` is required and must be an org.
   There is no guidance for a random-weight network built on someone else's
   architecture, or for whether three seeds are one entry or three.
4. **`derived_from` and `stage: null`.** "Leave stage null until coded from
   the developer's documentation" is clear. It is not clear whether
   `derived_from` may be filled from the paper being coded. I filled it and
   said so in a comment. The released base is derived from the end of stage 1
   through stages that are not registered, and the field cannot say that.
5. **Org entries versus "code from the source".** The paper gives only a hub
   namespace for the model developer. The org's name and `kind` came from
   general knowledge, flagged in a note. The rule does not say whether
   registry fields are exempt.
6. **`unit_state` guidance** does not cover a state injected at some positions
   and read at another within one call. See (b). The "producing one token"
   wording in `units.yaml` makes it worse.
7. **`unit_disposition`**: say whether a capacity or ability is a disposition.
   `origin` speaks of "the disposition or capacity", which suggests yes;
   `unit_disposition` lists only tendencies.
8. **`unit_reporter`** guidance covers chat studies only. Say what to code for
   a base model on plain text, and how it should pair with `frame_speaker`.
9. **`self_sense: self_model`** fires on any probing study by its rule, even
   one whose conclusion is that what was probed is not a self-representation.
   Say whether the facet codes what the study does or what it concludes.
10. **`evidence`**: say whether an answer taken as the argmax over candidate
    logits is `self_report`, `output_probabilities` or both.
11. **`elicitation: steered`** has two triggers, "brought out by" and "tested
    under" intervention. Under the second, every injection study is `steered`
    regardless of how the report is asked for, so the value duplicates
    `report_target: injected_state`.
12. **`levels`**: "conditions actually used" does not say whether to list
    conditions run or conditions reported.
13. **Stale names in the codebook.** `codebook/README.md` uses `unit_of_self`
    in the facet file format and long-form examples. `construct.yaml`
    (`identity_persistence`) says "use with unit_of_self thread ...".
    The notes in `format.yaml` say the facet is "kept apart from
    prompt_framing" as if that were a sibling facet; it is only a `varies`
    value.
14. **`varies.none` and `validated_against.none`** are ordinary values that
    look like special values. `validated_against` therefore has three
    near-neighbours (`none`, `not_applicable`, `unspecified`).
15. **`date`** is not defined: first submission, the version read, or the date
    printed on the paper. I used the printed date and noted the v2 stamp.
16. **Question `frame`** has no stated list of allowed keys and is not
    validated. I used `evidence` and `object_of_study` there, which the worked
    example does not.
17. **Figures.** `read_depth: full_text` is defined as the whole document
    including appendices. With text extraction the plots are not read, and
    three of this paper's results exist only as plots. I coded `full_text` and
    said so in `read_parts`; a value or flag for "text only, figures not
    read" would be more honest.
18. **`about`** is mentioned in `origin.yaml` and `disposition.yaml` and
    checked by the validator, but its shape (`models`, `datasets`) is not
    documented and the worked example never uses it.
19. **Optional claim facets with inconclusive or negative content.**
    `report_source` says a source that only rules a route out is not coded.
    There is no matching guidance for a source that proposes a route and
    says it has not tested it (c5).

## (e) Reading

- Version: arXiv 2611.15267 **v2** (stamped 14 Nov 2026; title page dated 10
  Nov 2026). v1 was not looked at.
- Obtained as full extracted text through the alphaXiv tool with full text
  requested. No summary was used.
- Read in full: abstract, §1 to §6, references, App. A (input templates),
  App. B (concepts, checkpoints, settings, probe), App. C (sweep results),
  App. D (no-prompt details, pretrained comparison, transfer, propagation
  control), Tables 1 and 2.
- Not read: the data in Figs. 2, 3 and 4, which are plots and do not survive
  extraction. Their captions were read. This affects c3 and c10 and all 7B
  answer results, and is flagged in those records.
- Not read: the OLMo 3 report or any other cited work. Model lineage in the
  registry is as this paper describes it.

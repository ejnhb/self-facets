# Reconciliation notes: rubin2026-closer-look-introspection (arXiv 2611.15267)

Record: `sources/rubin2026-closer-look-introspection.yaml`, coded against
codebook 0.3. 3 studies, 15 claims, 2 relations.

Read in this session: arXiv 2611.15267 v2 as full extracted text through
alphaXiv (abstract, §1 to §6, references, App. A to D, Tables 1 and 2).
Figures 2 to 4 were seen as captions and axis labels only, so `read_depth` is
`text_only`. Every number in the record was checked against that text. No
cited work was read.

Registry additions: 6 people, 2 orgs (`allenai`, `georgia-tech`), 7 models,
3 questions. `validate.py` and `build.py` are clean. Nothing in `codebook/`,
`scripts/`, `pilot/`, `CLAUDE.md` or `LOG.md` was edited, and nothing was
committed.

Pilot ids map to the new ones as follows.

| New | fable (pilot) | opus (pilot) |
|---|---|---|
| s1 | s1 + s2 | s1 (less its probe-only claims) |
| s2 | s3 | part of s1 |
| s3 | s4 | s2 |
| c1 | c1 | c1 |
| c2 | c2 | c2 |
| c3 | c3 | second sentence of c2 |
| c4 | c6 | c4 |
| c5 | c7 | c3 |
| c6 | c8 | c7 |
| c7 | c4 | c8 |
| c8 | c5 | note on c8 |
| c9 | c9 | c5 |
| c10 | c10 | c6 |
| c11 | c11 | c9 |
| c12 | c12 | `scope.conditions` of c9 |
| c13 | c13 | c12 |
| c14 | c14 | c11 |
| c15 | c15 | c10 |

## (a) Disagreements resolved

### Split

1. **Number of studies.** fable: 4 (prompted sweep across checkpoints;
   released base by injection setting; probe-only analyses of the prompted
   sweep; no-prompt experiment). opus: 2 (prompted sweep; no-prompt).
   **Decision: 3.**
   - fable's s1 and s2 are merged. fable split them only because `comparison`
     took one value in 0.2. Under 0.3 "two contrasts in one design are not
     different studies", and no claim about the layer-6 comparison inherits a
     wrong value from the checkpoint sweep, only an extra `varies` value. The
     merged study codes `comparison: [within_lineage, within_model]`.
   - The probe-only analyses (step 0 against shuffled labels, strength
     profiles) are split out as s2, as fable did and opus considered and
     rejected. 0.3 names this case: "a probe-only analysis is split from the
     self-report analysis it sits beside". In opus's single study, the step-0
     and strength-profile claims inherited `evidence: self_report`,
     `report_target: injected_state`, `unit_reporter` and `validated_against`,
     none of which describe them.
   - The no-prompt experiment is its own study in both pilots and here.
   - The probe figures that are quoted beside the model's answer (98.3%,
     99.1%, 83.1%) stay in s1, because there the probe is the baseline the
     report is compared with (`validated_against: probe`).

### Facets

2. **`unit_reporter`, prompted study.** Both coded `weights` (low) and both
   said the 0.2 guidance did not cover base models. **Decision: `[persona,
   weights]`.** 0.3 says a base model on raw text is `persona` with
   `object_of_study: frame_speaker`, and gives "an answer read from the
   logits of an untrained network" as the case for `weights`. The sweep has
   both: pretrained checkpoints and the released base (persona), and step 0
   (weights). Their results are plotted on one trajectory, so by the
   mixed-models rule the study is not split and the note says which is which.

3. **`self_sense`.** fable: `self_model` on all four studies (low). opus:
   `self_model` on the prompted study, `not_applicable` on no-prompt.
   **Decision: `self_access` on all three**, at high, medium and low
   confidence. 0.3 added the value for injection and probe-against-report
   designs and says "decoding a first-order state from activations is not
   enough [for self_model]; that is self_access". For s2 and s3 only the
   reading half of the definition is tested (no report or use by the system),
   which the notes say; `not_applicable` is named as the alternative for s3.

4. **`validated_against`, prompted study.** Both: `[known_intervention,
   other_model]`, both noting the probe had no value. **Decision:
   `[known_intervention, probe]`**, the 0.3 value.

5. **`evidence`, prompted study.** fable: `[self_report,
   output_probabilities, internals]`. opus: `[self_report, internals]`.
   **Decision: opus's.** The rule for `output_probabilities` is "use when the
   measurement is the probability the model assigns, as opposed to what it
   states". The measurement here is which of nine labels scores highest, a
   forced choice, and no probability value is analysed. The note records that
   the answer is a logit readout and never generated. See (c) 4.

6. **`elicitation`, prompted study.** fable: `[steered, spontaneous]`. opus:
   `[prompted, steered]`. **Decision: opus's.** The setup text is written for
   the purpose and tells the reader that sentences may be altered in the
   model's internal processing; the paper itself calls this the "prompted"
   task and contrasts it with the experiment "without setup instructions".
   Both agreed, and I kept, that the answer stub is not `prefilled` because
   plain text has no assistant turn.

7. **`elicitation`, probe-only and no-prompt studies.** fable: `steered`.
   opus: `not_applicable` (no-prompt). **Decision: `steered`.** The facet
   asks how "the capacity or report under study" was brought out, and the
   trace exists only under activation intervention. This goes with decision 9.

8. **`unit_state`, no-prompt study.** fable: `[forward_pass, conversation]`
   because the trace is read 256 tokens later. opus: `forward_pass`.
   **Decision: `forward_pass`.** 0.3: a state applied over several positions
   and read in the same pass is `forward_pass`; `conversation` needs
   persistence while the model generates, and nothing is generated.

9. **`unit_disposition`, probe-only and no-prompt studies.** Both coded
   `not_applicable`. **Decision: `weights`, low confidence**, against both
   coders. Reasons: 0.3 narrows `not_applicable` to "no standing tendency or
   capacity of the system is at issue"; the source's conclusion is in capacity
   terms ("the architecture can support these traces", "the architecture and
   random weights can carry a location signal"); and 0.3 added `origin:
   architecture`, which is defined for a "disposition or capacity" found in
   untrained networks and is coded on c9 and c11. Coding an origin for a
   capacity while saying no capacity is at issue would be inconsistent.
   `not_applicable` is named in the notes as the alternative. This is the
   least certain facet decision in the record; see (c) 2.
   For the prompted study both coded `weights` (low); kept, now at medium,
   since 0.3 says a capacity counts.

10. **`varies`, prompted study.** fable left `activation_intervention` off
    its s1 (it was in its s2). opus coded it. With the merge it is coded, with
    layers, strengths and vector types in `levels`, plus a level saying which
    settings have numbers in the text. Both coded `model_size`; kept, with a
    note that 7B answer results are only in Fig. 3.

11. **`comparison`.** Both coded one value per study and said a second was
    needed. Now `[within_lineage, within_model]` on s1 and s2 and
    `within_model` on s3. `cross_model` is not coded for 7B against 32B (no
    conclusion is drawn from the difference) or for random against pretrained
    networks in s3 (the authors decline to interpret it).

12. **`construct` basis, no-prompt study.** fable: stated. opus: operational.
    **Decision: stated**, medium confidence. The paper frames the whole work
    as introspection; the note says the thing measured is decodability.

### Claims

13. **`report_source` on the released-base result (c2).** fable:
    `current_state`. opus: left off. **Decision: coded.** §1 says the method
    changes activations "while holding its input text fixed" and that
    successful localization "shows that a model can report something about
    its internal computation"; App. B.3 confirms each passage is injected at
    all nine positions with the same text. That is the source arguing the
    fresh-copy point. opus's ground for leaving it off (the authors do not
    show the model uses the probed features) is about which internal features
    carry the report, which is recorded separately in c8.

14. **The untested mechanism (c8).** fable had a separate `hypothesised`
    claim; opus put it in the note of the `argued` claim. **Decision:
    separate claims**, since the evidence kinds differ ("split a chain into
    links").

15. **The developmental ordering (c3).** fable had a separate claim with
    `origin: pretraining`; opus put `origin` on the released-base claim.
    **Decision: separate**, so "the model has the capacity" (c2) and "it is
    there before post-training" (c3) are separate links. Both coded
    `pretraining` and not `midtraining`; kept, with the caveat in the note.

16. **Targets in sentences 1 to 8 (c12).** fable: a claim. opus: inside
    `scope.conditions` of the main random-network claim. **Decision: a
    claim.** `scope.conditions` says where a claim holds and is the wrong
    place for a second result.

17. **Which probe layer the step-0 figures use (c9).** fable: 37.2% at fixed
    layer 24, the strength-2 figures at a selected layer. opus: all at a
    selected layer, with a note that the text is unclear. **Decision:
    fable's reading.** §4.1 says 37.2% is at "the same probe setting", and
    App. B.5 and C.3 tie the readout selection to the strength-2 comparison.
    The claim's conditions say this is a reading.

18. **`origin` on the untrained-network results (c9, c11).** Neither coded it
    (no value existed). **Decision: `architecture`**, the 0.3 value, with
    `about` pointing at the step-0 checkpoints and the random networks.

### Questions

19. Each pilot added the same five questions under different ids, none with
    a parent. **Decision: three new questions, all under
    `q-privileged-self-access`.**
    - `q-injected-state-report` (general; replaces both "report without
      post-training" questions and both "depends on layer" questions). The
      post-training angle is carried by `origin` and by scoping the claim to
      the base model, so a later record that finds no such report in a base
      model conflicts on this question. The layer-dependence result (c4) is a
      `supports` here, scoped to the two layers.
    - `q-report-matches-probe` (replaces both "probe exceeds report"
      questions). Both pilots worded theirs so that yes meant the probe beats
      the report, which would count against the parent. It is turned round so
      that yes counts towards privileged access, and the stances flip to
      `against` (c1, c5). The released base at the best setting (89.6%
      against 99.1%) is `inconclusive`.
    - `q-introspection-success-generalises` (replaces both "localization
      shows general introspection" questions, worded for any narrow report
      task).
    - Dropped: both "decodable without training" questions. They are not
      about the system's access to itself, no other coded work takes a
      stance, and `origin: architecture` now records the finding. c9 and c11
      have `question: null`.

### Registries

20. **Models.** Both registered all 16 OLMo checkpoints plus one random-init
    entry (17). **Decision: 7 entries** under the 0.3 rules: one series entry
    per size (`olmo-3-32b-checkpoints`, `olmo-3-7b-checkpoints`), own entries
    only for checkpoints a claim is scoped to (32B step 0, 32B step 1000, the
    released 32B base, 7B step 0), and one entry for the three random
    networks with `georgia-tech` as developer. The swept checkpoints and
    their revision names are in the `levels` of `pretraining_progress`. Ids
    for the released base differed (`olmo-3-1125-32b` in fable,
    `olmo-3-32b-base` in opus); I used the hub name.
21. **Random-network id.** fable `olmo-3-32b-arch-gaussian-init`, opus
    `olmo-3-32b-random-init`. Used the shorter.

### Bookkeeping

22. **`read_depth`.** Both `full_text`, both saying figures were not read.
    Now `text_only`.
23. **`date`.** Both used 2026-11-10, the date printed on the title page. 0.3
    says `date` is the date of the version read; v2 carries the arXiv stamp
    14 Nov 2026, so the record uses 2026-11-14 and the artefact note gives
    the printed date. See (c) 7.
24. **Relations.** Both left `relations` empty because 0.2 could not point at
    uncoded work. Two `to_external` relations added: `uses_method_of` Hahami
    et al. 2025 (§3.2) and `extends` Fornasiere et al. 2026 (§5.1).
25. **The claim that draws on several studies (c7).** Both attached it to the
    prompted study with a note. It now also lists s2 and s3 in `compares`.

## (b) Pilot content not supported by the paper

All percentages, ranges, p-values and section pointers in both pilot records
matched the text. The items below are the exceptions, none of them a wrong
number.

1. **opus c5, `scope.conditions`:** "Probe readout chosen on two seeds and
   scored on the third" is applied to all the step-0 figures. For the 37.2%
   figure the paper says "the same probe setting" as the main trajectory
   (layer 24). The new c9 separates the two.
2. **fable s1 design:** "360 trials per condition over three data seeds"
   reads as 360 in total. App. B.3 gives 40 passages per seed, each injected
   at all nine positions, which is 360 per seed and matches the 288 training
   trials per fold. The new design text follows B.3.
3. **Size of the random networks.** Both ids say 32B. The no-prompt sections
   never restate the size; 32B is the paper's stated default (§3.1) and fits
   the layer-58 readouts. opus flagged this in its notes, fable did not. The
   registry entry and the s3 note now say it is the default, not a statement.
   The same holds for "the pretrained base" in that experiment, which both
   took to be the 32B released base.
4. **opus c9, `scope.conditions`:** carried a second result (sentences 1 to
   8) and so read as if the paper gave those figures for strengths 4 and 8.
   The paper gives one pair of figures and does not restate the strength. Now
   c12, with that caveat.
5. **Not from the paper, in both:** the developer of OLMo. The paper gives
   only the hub namespace `allenai` and cites "Team Olmo". The pilot
   registries are not in `pilot/`, so I could not see what they recorded. The
   new `allenai` org entry has a name and kind that are not from any source
   read in this session, and its note says so.

Nothing was dropped from the record as false. One pilot item was left out
on purpose by both and here: the App. B.4 strength calibration against
Hahami et al. on Llama-3.1-8B-Instruct, a method note with no finding (said
in the s1 note; that model is not registered).

## (c) Where codebook 0.3 or CLAUDE.md still did not fit

1. **Series entries and scoped checkpoints overlap.** The rules give a
   series entry for a sweep and an own entry for a checkpoint a claim is
   scoped to. A study then lists both the series and some of its members, and
   an unscoped claim inherits all of them. The registry has no field saying
   an entry is a series or which series a checkpoint belongs to; I used the
   `note` and the study's `role`. It is also unclear whether a released base
   that is the last level of a sweep but has no claim scoped to it (7B here)
   gets an entry. I left it inside the series, which makes the two sizes
   asymmetric. `derived_from` cannot point from the released base to the end
   of stage 1 without registering that checkpoint, so it is null.

2. **Is a representational property a "capacity"?** `unit_disposition` now
   says a capacity counts, with examples of things the system does. A
   probe-only study measures something the network carries, with no
   behaviour. `origin: architecture` was added for exactly this finding and
   is defined over "the disposition or capacity", which implies yes;
   `unit_disposition` examples imply no. I coded `weights` (low) on s2 and s3
   against both pilot coders. The units list also still has no value for an
   architecture apart from one set of parameters, which is what the source
   attributes the property to.

3. **`unit_reporter` and `object_of_study` for a sweep that starts
   untrained.** 0.3 settles the two ends (base model: persona and
   frame_speaker; untrained network: weights). It does not say where a
   checkpoint 8.4B tokens into pretraining falls. I put every pretrained
   checkpoint under persona. `object_of_study` cannot say "frame_speaker for
   most, nothing for step 0", because a special value cannot be combined
   with another.

4. **`output_probabilities` under `evidence`.** The definition ("logits for
   an answer, read directly") fits an argmax over label logits; the rule
   ("the probability the model assigns, as opposed to what it states") does
   not. The two coders split on exactly this. I followed the rule. A sentence
   on forced-choice scoring from logits would settle it.

5. **`varies` for the released base and for text changes.**
   - The last sweep level adds mid-training and long-context training.
     `post_training_stage` says "mid-training included", which could mean
     that a mid-training stage counts as a stage or that mid-run checkpoints
     count. I kept the level under `pretraining_progress`, as both pilots
     did, because the source treats the whole axis as before post-training.
   - Random networks against the pretrained base in s3 is coded
     `pretraining_progress` though the random networks are not the lineage's
     step 0 and the authors do not interpret the contrast. There is no rule
     on whether `varies` lists what was run or what conclusions are drawn
     from (`comparison` has that rule).
   - The transfer test (fresh text, numbering removed) is coded
     `prompt_framing`, whose rule assumes a question. Still no better value.
   - `levels` still does not say whether to list conditions run or
     conditions reported. I listed those run and added a level naming the
     ones with numbers in the text.

6. **Mixed confidence within one facet entry.** On s3 `varies`, two values
   are certain and two are weak; the entry is `low` and the note says which.
   The database shows all four as low. (Already open in `LOG.md`.)

7. **`date` when the printed date and the arXiv stamp differ.** "The date of
   the version read" could be either on this paper (10 Nov printed, 14 Nov
   stamped on v2). I used the stamp.

8. **Question tree.**
   - "Yes counts towards yes to the parent" forces a probe-against-report
     question to be worded as "does the report match the probe". The paper's
     own finding is the opposite direction (decoding outruns reporting), so
     its headline result enters as `against`. That is workable but reads
     oddly, and a near-match (89.6% against 99.1%) has no clear stance; I
     used `inconclusive`.
   - With a general `q-injected-state-report`, an early checkpoint at chance
     (c1) and the released base at 89.6% (c2) conflict inside one study, and
     `conflict_facet_diff` shows no difference because the claims differ only
     in model scope. (Already open in `LOG.md`.)
   - Every `against` under `q-privileged-self-access` now pairs with every
     `supports` under it, so this record produces 18 conflict rows with Binder
     et al. (16 from its three `against` claims, 2 from its `supports`
     claims against Binder's c8) between studies that share no design. Whether an
     interpretive question such as `q-introspection-success-generalises`
     belongs under the parent, or should stand alone, is for the owner.
   - I did not add a question on post-training. Both coders of this paper
     and both coders of 2601.01828 added one independently, so the owner may
     want it; if so it should sit under the same parent, worded as "can
     models report an injected state without post-training".
   - Question ids here were chosen without sight of the other two
     reconciled records, so ids for the injected-state question may need
     merging.

9. **Optional claim facets on a non-report.** `origin` is coded on c9 and
   c11 for a decodable trace, not for a disposition or reporting capacity.
   The notes say so, but a query on `origin: architecture` cannot tell the
   two apart.

10. **`elicitation` for a study with no report.** `steered` is coded on s2
    and s3 on the "capacity brought out" reading. One pilot coder used
    `not_applicable`. The facet does not say which applies when nothing is
    elicited from the model and a signal is only measured.

11. **End-of-session steps.** `CLAUDE.md` asks for a `LOG.md` entry and a
    commit; this task said to do neither, so both are left for the owner.

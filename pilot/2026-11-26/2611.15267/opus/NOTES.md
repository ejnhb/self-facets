# Pilot notes: rubin2026-closer-look-introspection (arXiv 2611.15267)

Record: `sources/rubin2026-closer-look-introspection.yaml`. 2 studies, 12 claims.
Registry additions: 17 models (16 OLMo 3 checkpoints, 1 random-init network),
2 orgs (`allenai`, `georgia-tech`), 6 people, 5 questions. No datasets.

## (a) Split

- **s1, prompted localization across pretraining.** The paper's main sweep
  (§4.1, App. C): a raw-text prompt asks which of nine sentences was "altered
  from the inside". The model's answer and a linear probe are compared on the
  same trials, across OLMo 3 7B and 32B checkpoints, injection layers,
  strengths and vector types. It has one fixed-setting analysis (Fig. 2), one
  analysis with settings chosen on held-out seeds (Fig. 3, 4) and the layer-6
  comparison (App. C.2). I kept these in one study because every facet is the
  same across them. They differ only in which levels were used, which goes in
  `scope.conditions`.
- **s2, no-prompt propagation in random networks.** This one has no question,
  no answer and no self-report. It uses networks the authors built from
  random weights and reads the trace at later tokens. `report_target`,
  `unit_reporter`, `validated_against`, `elicitation` and `evidence` all
  differ from s1, so it fails the "would a claim inherit a wrong value" test
  and gets its own study. I kept the pretrained-base comparison inside s2 as
  a listed model with a role, because the authors report it but do not
  interpret it.
- I considered a third study for the probe-only strength profile (Fig. 4,
  claim c6), because no self-report is involved there. I rejected it: the
  probe-only results come from the same trials as s1, and `evidence` says
  what the study collects, not what each claim uses. Even so, c6 inherits
  `report_target: injected_state` and `evidence: self_report` though it uses
  neither. This is a borderline case for the split test.
- The argued claim c8 draws on both studies. I attached it to s1, because a
  claim can belong to only one study.

## (b) Hesitations

- **validated_against (s1).** I weighed three options. `known_intervention`
  is clearly right: both measures are scored against the injected sentence.
  The open question was how to code the linear probe, which is the paper's
  main baseline. `internals` does not fit, because the report is not scored
  by whether it matches the probe. `other_model` ("third-person baselines")
  is the closest. I chose `[known_intervention, other_model]` at low
  confidence. A probe is an external decoder on the same activations, not
  another model.
- **unit_reporter (s1).** The options were `persona`, `weights`, `forward_pass`
  and `unspecified`. These are base and pretraining checkpoints, run in raw
  text with no persona. The guidance says to code `weights` only if the study
  separates the report from any persona. Here there is no persona to separate
  from, but that is not quite what the guidance means. I chose `weights` at
  low confidence. `forward_pass` was tempting because the answer is a single
  argmax at one position.
- **unit_disposition (s1, s2).** The study is about an occurrent state, which
  points to `not_applicable`. But s1 tracks how the capacity to localize, and
  decodability, change across checkpoints. I coded `weights` (low) for s1 and
  `not_applicable` for s2. The codebook frames dispositions as "standing
  tendencies", such as a preference, a trait or a trained stance. It is
  unclear whether a capacity counts.
- **unit_state.** The options were `forward_pass` and `conversation`. The
  trace spreads across positions and is read 256 tokens later, through
  attention, which is cache-like. But there is one forward pass with no
  generation, so I chose `forward_pass`. The guidance ("a single-position
  activation is forward_pass; something that … sits in the cache is
  conversation") does not cover a multi-position, single-pass state.
- **self_sense (s1).** The options were `self_model`, `self_facts` and
  `not_applicable`. The probe locates information in activations, which fits
  `self_model`'s rule ("locates, probes or intervenes"). But what it reads is
  the perturbation trace itself, not a representation the model holds of its
  own state. I chose `self_model` at low confidence. For s2 I chose
  `not_applicable`, because a random network holds no self-representation.
- **object_of_study (s2).** I weighed `frame_speaker` against
  `not_applicable`. There is no output under study and no speaker, so I chose
  `not_applicable`.
- **elicitation (s1).** The options were `spontaneous`, `prompted`,
  `prefilled` and `steered`. The task is zero-shot, but the setup text does
  real work, so I chose `prompted`. The report is tested only under
  injection, so I also chose `steered`. `prefilled` was rejected: the prompt
  ends in "Answer: SENTENCE ", but raw text has no assistant turn. This
  distinction matters for base-model studies.
- **evidence (s1).** The answer is the argmax of the label logits. I coded it
  as `self_report`, not `output_probabilities`, because it is a stated choice
  under constrained greedy decoding. Someone else could code both.
- **varies (s2).** Readout distance in tokens went under `context`, and
  removing sentence numbers went under `prompt_framing`. Neither is a clean
  fit (see gaps).
- **comparison (s1).** The authors state `within_lineage`. But the paper's
  core contrast is probe against answer on the same trials, and cardinality
  one cannot hold both.
- **origin (c2).** The authors say reporting "develops without
  post-training". The released base includes mid-training. I coded
  `pretraining`, because its rule is "before any post-training", and
  explained the ambiguity in the note. `[pretraining, midtraining]` was the
  alternative.
- **report_source.** I considered `current_state`: the input text is held
  fixed, so the report can only come from the injection. But the authors do
  not frame it that way, and they say they have not shown the model uses the
  probed features. I left it off.
- **Model registry granularity.** I had to choose between one entry per
  checkpoint (16 entries) and one per model with checkpoints in `levels`. The
  registry header says "one entry per checkpoint that some study touches",
  but CLAUDE.md says "registries stay small". I chose one per checkpoint,
  because claims need `scope.models` at step 0, 8.4B and the base model.
- **Random-init network as a model.** It needs a `developer` that is an org.
  I used the authors' institution. The model size (32B) is inferred: the
  paper's default model is 32B, and there are readouts at layer 58.

## (c) Gaps

- **validated_against** has no value for an "external decoder / probe
  baseline on the system's own activations". This is the central design of
  probe-versus-report papers. Proposal: add `probe_baseline`, or widen
  `internals` to cover "compared with what a decoder can read".
- **comparison** has no value for a "measure against measure on the same
  trials" design, such as decoding against reporting. It could become
  cardinality many, or gain `cross_measure`.
- **varies** has no level for mid-training. The base model differs from the
  end of stage 1 by mid-training and long-context training, and I coded it
  under `pretraining_progress`. `origin` has `midtraining` but `varies` has
  no counterpart. It also has no value for readout distance within one input
  (I used `context`), for input-text formatting that is not a prompt (I used
  `prompt_framing`), or for random initialisation, meaning architecture with
  no training. I used `pretraining_progress` for that too, though it is not
  OLMo's step-0 checkpoint.
- **units** have no unit for the architecture apart from a checkpoint. The
  authors' conclusion is that "the architecture and random weights" carry the
  signal, across three initialisations. Both `weights` ("one checkpoint")
  and `not_applicable` lose that.
- **units** have no unit for an unattributed text-continuation speaker (base
  model, raw text) for `unit_reporter`. `object_of_study` has
  `frame_speaker`, but the units list has no counterpart.
- **self_sense** does not separate the state itself (a first-order trace)
  from a representation of the state (a self-model). Probe papers sit on
  exactly this line.
- **elicitation** cannot express "nothing is elicited, the substrate is
  probed". I used `not_applicable` for s2 only because nothing fitted.
- **unspecified / not_applicable used only for lack of a fit:**
  `unit_disposition: not_applicable` (s2, really "architecture"),
  `self_sense: not_applicable` (s2), `object_of_study: not_applicable` (s2),
  `elicitation: not_applicable` (s2).
- **Questions.** The `frame` field's allowed keys are undocumented. I used
  `evidence`, and the validator accepted it.
- **No facet records the measurement setting choice**, such as a fixed
  setting chosen after inspecting the sweep against held-out selection. This
  matters for how the base model's 89.6% should be read. I put it in
  `scope.conditions`.

## (d) Instructions

- **Model granularity.** "Registries stay small" (CLAUDE.md) pulls against
  "one entry per checkpoint that some study touches" (models.yaml header).
  For papers using many pretraining checkpoints, the guidance should say
  which wins.
- **unit_reporter guidance** assumes chat format ("in nearly all chat-format
  studies this is a persona"). It says nothing about base models in raw
  text, which are what the LOG asked the pilot to exercise.
- **unit_state guidance** maps a single position to `forward_pass` and the
  cache to `conversation`. A state spread over many positions in one pass
  falls between them.
- **The split test** ("would any claim inherit a wrong facet value") is
  ambiguous for study-level facets like `evidence`, which describe the whole
  study. Does a probe-only claim in a study that also collects self-reports
  "inherit a wrong value"?
- **Two places for claim conditions.** `scope.conditions` is free text, and
  `levels` on `varies` is free text, with nothing linking them. I repeated
  the level wording by hand.
- **Placing a cross-study claim.** It is unclear where to put an argued claim
  that draws on several studies. The rule is a single `study`.
- **Study model roles.** The `{id, role}` model form on a study appears in
  the worked example but is not documented in the READMEs.
- **Draft wording.** In codebook/README.md, the facet file example still
  shows `facet: unit_of_self`, which 0.2 removed. construct.yaml's
  `identity_persistence` rule also still refers to `unit_of_self`.
- **origin `pretraining` rule.** "Before any post-training" overlaps with
  `midtraining`, which is also before post-training.

## (e) Reading

I read arXiv 2611.15267 v2 (stamped 14 Nov 2026; the paper is dated 10 Nov
2026) as full extracted text via alphaXiv (`get_paper_content`,
`fullText: true`). That covered the abstract, §1 to §6, the references and
appendices A (templates), B (concepts, checkpoints, settings, probe), C
(supporting sweep) and D (no-prompt details and controls). I saw figures only
as extracted captions and axis labels, so values shown only in Figs. 2 to 4
(such as the stage-1-end answer accuracy and the selected-setting curves)
were not read. I did not read any cited paper.

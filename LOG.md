# Session log

Newest first. Each entry: what changed, what is open, what needs a decision.

## 2026-11-27: Fornasiere et al. 2026 (arXiv 2604.17465v3), first coding

Coder: claude (claude-opus-5-5), from the paper, its figures and its released code only, following AGENTS.md.

**Added**

- `sources/fornasiere2026-dropout-noise-recognition.yaml`: 11 studies, 44 claims. Dropout or Gaussian noise
  applied to the attention and MLP outputs at one sentence; localization (s1), its comprehension control (s2),
  the likelihood check (s3), Olmo 3.1 post-training stages (s4) and pretraining checkpoints (s5), detection (s6)
  and its controls (s7), detection and controls across Olmo stages (s8, s9), zero-shot naming with control
  labels (s10), few-shot naming with correct, inverted and control labels (s11). Code read at ad7ce52 (tag v2).
- `links/fornasiere2026-dropout-noise-recognition.yaml`: 15 proposed links to three existing questions
  (q-injected-state-report, q-introspection-differs-by-post-training, q-introspection-success-generalises).
- Registry: six people, three orgs (lawzero, google, bytedance-seed), nine models (Gemma 4 31B, Mistral Small
  3.2, three Olmo 3.1 32B stages, Qwen3 14B and 32B, Qwen3.8 27B, Seed-OSS 36B).

**Learned**

- The paper says every prompt uses a chat template, but the code falls back to plain concatenation when a
  tokenizer has none, and the Olmo 3 32B base has none (checked on the Hub at main). So the base model (s4, s8,
  s9) and the pretraining checkpoints (s5) are coded `raw_text`, from the code.
- The repository's tag `v2` holds the code of arXiv v3 (its message says arXiv v2, which is an older, shorter
  paper with three model families).
- Text and figures disagree in places, all recorded on the claims: Qwen3.8-27B's zero-shot accuracy does not rise
  with dropout rate in Fig. 33 (c33); its correct and inverted few-shot curves nearly overlap in Fig. 10 (c40);
  the 3-token localization peaks in Fig. 19 are mostly below the 90% the text gives (c6); Gemma4-31B is the
  exception to the first likelihood hypothesis, shown only in Fig. 22 (c12).

**Open**

- Figs. 20, 23 to 26, 34 to 38 and 41 to 45 not viewed; the claims that touch them say so.
- Rubin et al.'s relation to this paper is a `to_external` citation; it could now point at this record (Rubin
  cites an earlier version, so check which).
- The pretraining-checkpoint result (c17) and the base-model result (c14) reach no question on emergence of
  injected-state reporting in pretraining; a question poser may want one (q-introspection-differs-by-post-training
  covers post-training only).

**For the owner to decide** (codebook frozen; nothing changed)

- `varies` has no value for the number of in-context examples (s11's k teaching pairs); coded under
  `prompt_framing`, which also carries the label arms. `context` ("number of turns") was the alternative.
- The localization and detection prompts are shared by two contrasting checks (a comprehension or yes/no control
  with different questions). Split into separate studies here (s2, s7, s9) because their claims would otherwise
  inherit `report_target: injected_state`; the cross-study conclusions are argued claims with `compares`.
## 2026-11-27: Betley et al. 2025 (arXiv 2501.11120v1) coded

Coder: claude (claude-opus-5-5), from AGENTS.md alone, under the codebook freeze (0.10).

**Added**

- `sources/betley2025-tell-me-about-yourself.yaml`: 9 studies, 39 claims. Read in full (v1 PDF, figure pages
  seen) with the released repository at 1f8f700 (code read to the checklist; datasets README only).
  Studies: s1 self-reports after fine-tuning on multiple-choice policies (risk, myopia, apples; GPT-4o and
  Llama 3.1 70B), s2 self-reported against actual risk across runs, s3 Make Me Say, s4 vulnerable code,
  s5 backdoor detection under system prompts, s6 real against fake triggers, s7 trigger elicitation after
  reversal training, s8 single- and many-persona risk training, s9 self and Quanta-Lingua.
- `links/betley2025-tell-me-about-yourself.yaml`: 23 proposed links to existing questions, mostly
  `q-self-report-tracks-change`; also `q-self-model-shared-across-personas`, `q-report-dissociates-from-behaviour`,
  `q-report-matches-direct-measure`, `q-privileged-self-access`. No new questions.
- Registries: people betley-jan, bao-xuchan, soto-martin, sztyber-betley-anna; orgs university-of-toronto,
  uk-aisi, warsaw-university-of-technology; models gpt-4o-2024-08-06, gpt-4o (the undated API alias, for
  where the code calls "gpt-4o"), gpt-4o-mini.
- Song et al.'s relation from c22 now points at the record instead of a citation (pass entry added there).

**Learned**

- The code settled things the paper does not say: snapshots per experiment (vulnerable code and the season
  backdoor on GPT-4o 2024-08-06), the "Function" question's system prompt, and that the Fig. 4 runs differ in
  epoch checkpoint and base snapshot as well as learning rate and seed (s2 note). Paper and figure disagree on
  Llama (Fig. 30 shows two null questions, the text one); the code's "backdoor is good" prompt differs from
  Table 6. Both recorded.
- The vulnerable-code experiments' code and data are not in the repository at the commit read.

**Open**

- s8 asks the default speaker about other personas in the third person. `q-self-model-shared-across-personas`
  is worded for the personas' own self-reports, so c32 and c33 are linked with that mismatch noted. A narrower
  question (does training that changes the default persona shift the model's descriptions of other
  characters?) would fit better; not added, since the task was to link existing questions. The c32/c33
  conflict turns on many-persona training, a moderator.
- report_target has no value for reports about another persona's behaviour (s8, s9).
- report_source has no value for the authors' account (self-knowledge reached by out-of-context reasoning
  over the fine-tuning data); left uncoded, as in Song et al. c22. To weigh at the next codebook review.
- Not linked though their frames match: c19 (self-rated alignment), c22 (system prompt changes the backdoor
  report; `q-self-report-depends-on-frame` needs unit_reporter, not coded), c28 and c29 (reversal training is
  training on the reporting form, which `q-self-report-tracks-change` excludes).
- Llama fine-tunes taken to start from the instruct model (the code's untuned Llama is llama-v3p1-70b-instruct);
  the fine-tuned ids do not show their base.

**For the owner to decide**

- Construct: coded `[self_knowledge, self_prediction]` for "behavioral self-awareness" on all but s2 (adds
  introspection, which the authors raise there) and s7 (self_knowledge only). Confirm.

## 2026-11-27: AGENTS.md; code and data availability; the freeze

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- `CLAUDE.md` renamed `AGENTS.md`, the name other developers' agents look for. `CLAUDE.md` now only imports it,
  so Claude Code still loads the instructions. References updated (scripts, templates, record comments).
- Code and data availability made explicit: every record lists a `code` and a `data` artefact with a status
  (`released`, `not_released`, `unknown`), and for released ones the url, the commit or revision read (`ref`) and
  how much was read. Backfilled: Binder et al. (code at 421fa65, read in part; data not read) and Song et al. (code
  and data read in part; commit not recorded) released; Lindsey and Rubin et al. `unknown` (neither paper mentions
  a release; not searched). New build views `study_availability` (with whether a study's subject models all, some
  or none have open weights) and `question_evidence_availability`, so a question's evidence shows what could be
  re-run. Enum change only: codebook 0.10.1, bookkeeping.
- AGENTS.md: a bounded code-reading step (pin the commit, read to a checklist, record what was read; the paper is
  the source of the claims, the code settles how it was done), and the freeze: facets frozen at 0.10 until the
  owner's next review, with proposed changes going to this log.

**Open**

- Lindsey and Rubin et al.: search for released code or data, then set `released` or `not_released`.
- The next paper, coded by a fresh agent from these instructions alone.

## 2026-11-27: the held pass (figures and effects on the three pilot records; Binder et al. read in full)

Coder: claude (claude-opus-5-5), working with the owner: four claude-opus-5-5 subagents, one per record, from one
brief, each editing only its own record; this coder reviewed the four diffs together, made the consistency fixes
below, and committed. Each record has a pass entry (PR 14) saying exactly what was read.

**Changed**

- Figures: every record now has its figure pages seen (`read_depth: full_text`), and the claims that rested on
  unread figures carry approximate values marked "read from Fig. N". Corrections the figures forced: Song et al.
  c1 (the near-random Exp. 2 choices hold for prompted answers only; string probabilities pick the original word
  about 0.8 of the time on nonsense); Lindsey c21 (helpful-only variants reach rates like the three production
  models the text singles out). New claims where a figure held a result the record stated nowhere: Rubin et al.
  c16 and c17.
- Effects: `effect_of`, `effect_presence` and `effect_direction` coded across Lindsey (22 claims), Song et al. (8)
  and Rubin et al. (9); Binder et al.'s checked (8 of 10). Auto stances now reach all four papers.
- Binder et al. read in full (all appendices, the figures, and the official repository at 421fa65, linked from
  arXiv's HTML v1). Study s5 split: its long-output-properties claim (c7) moved to a new study s7, since no
  cross-prediction was run on those and the prompts differ; s5 is now answer-switching only, with the model's own
  first answer in context, so `output_route_control` is `none`. Model lists for s1, s5 and s6 settled from the
  appendices; `system_prompt` none (operational) from the code.
- Lindsey: the helpful-only variants run in s4 to s7 (the figures show them; the text never says), so they are in
  those studies' model lists and `post_training_recipe` in their `varies`; text and figures disagree on s6's
  strengths (both recorded). New registry entries: three helpful-only Claude models and the seven base models of
  Fig. 14, now s3's models.
- Song et al.: the analysis script drops one of the Exp. 2 prompts, unmentioned in the paper (s1 note).
- Binder et al.'s "Llama 70B" is Llama 3.1 70B Instruct: the code fine-tunes Fireworks' llama-v3p1-70b-instruct.
  The record now uses `llama-3.1-70b-instruct`, and the registry's variant-unknown `llama-3.1-70b` is removed
  (its note asked for this merge once the source was checked). Prompted by blind test 2, where the coder inferred
  the instruct model from the paper alone (the untrained model's refusals).

**Consistency fixes in review**

- Cross-study and argued claims take no `effect_of`: Lindsey c20 (base against post-trained, argued, comparing
  s3 with s1) had it removed, matching Binder et al. c7. Such claims are linked to questions by hand.
  Lindsey s3 still lists `post_training_stage` in `varies`, coded in the pilot with s1 named as the other arm;
  Binder et al.'s new s7 does not code its cross-study contrast that way. Which is right is a question for the
  owner (below).
- Controls take none (Lindsey c18 and c30; Rubin et al. c13), per the 0.10 rule.

**Open**

- Rubin et al. c13 bundles a real injection effect in the pretrained base with an unexplained control result;
  it should probably be split into two claims.
- Lindsey c6 and Song et al. c7 are coded `mixed`; splitting each by comparison would be cleaner.
- Per-panel values of Lindsey Figs. 29 to 31 are not coded (legible only at page resolution); Figs. 1 to 7, 16
  and 23 (schematics, prompts, examples) were not viewed.
- Binder et al. still needs its blind check by a coder from another model family.

**For the owner to decide**

- A codebook gap: `effect_presence` has no value for an effect that runs opposite to the question's direction on
  an unordered contrast. Song et al. c8 to c10 find no self advantage but significant differences the other way
  (other models predicting better than self); they are coded `absent`, with the reversal in the note, because
  `present` would roll up as support. Either a value such as `reversed`, or letting auto stances read
  `effect_direction` on `self_vs_other` (self above, other above). To weigh at the next codebook review, not
  during the freeze.
- Whether a contrast whose other arm is another study counts as something a study `varies` (Lindsey s3, coded so
  in the pilot) or only as a `compares` between studies (Binder et al. s7, this pass). One rule for both.

**Owner, 2026-11-27:** both deferred until after the freeze. On the second: ideally, when both studies are coded,
the comparison should surface by itself at the question or framing layer, rather than being coded into either
study.

**To watch as papers are added** (owner, 2026-11-27):

- Granularity: whether the splitting into studies, claims and effect fields is the right level of detail. Judge it
  from the blind tests: per facet and field, coder agreement, time per paper, and whether any question,
  definition or reading uses it. One that fails all three after twenty or thirty papers is a candidate to merge or
  drop.
- Scale: records are about 60 KB per paper, so hundreds of papers is tens of megabytes of YAML; PDFs and the built
  database are never committed. What grows badly is `conflict_facet_diff`, which compares conflicting claim pairs
  facet by facet (6,298 rows from four papers, roughly quadratic in claims per question). Around fifty papers,
  compute it per question on demand instead of building it whole.
- Sparsity: if facets get too fine, papers that overlap in practice can end up with claims that never meet on a
  question or a conflict. It may be handled at the reading level, or may not happen; check whether similar
  designs coded by different coders land on shared questions and comparable facet values.

**Blind test 2** (set up the same day): branch `blind-binder`, one commit with no history, Binder et al.'s record,
links, pilot notes, design notes and changelog removed, the relations to it turned into citations, and registry
entries only it used dropped; `BRIEF.md` at its root. Coders from other model families code the paper from the
PDF; the comparison is made against this pass's record.

## 2026-11-27: provenance per record, and a check on every pull request

Coder: claude (claude-opus-5-5), working with the owner. Prompted by a review of the 0.5 to 0.10 changes.

**Changed**

- `coding.passes` on every record: one entry per coding or later change, with date, pull request, coder and
  model, codebook version, what the pass coded or changed, and what was read for it. Reconstructed for the four
  records from this log and the git history: the first coding by claude-fable-5-2 (PRs #1 to #4), then backfills by
  claude-opus-5-5 in PRs #6, #8, #9 and #12. Until now the records named only the first coder, so the later
  backfills read as that coder's work.
- `validate.py` requires `passes` and checks each entry; `build.py` writes them to a `coding_passes` table;
  the template and CLAUDE.md ("Mark your work") say to add a pass each time a record changes. The pull request
  number tells apart instances of one model, and the table lets a checker confirm it did not code what it checks.
- `.github/workflows/check.yml`: validate and build on every pull request and push to main. No test suite yet, on
  purpose: nothing extra to maintain while the design changes. Tests of the logic evaluator are worth adding when
  selectors and definitions gain a third answer ("can't tell, not coded").

**Open**

- The 0.8 passes record no new reading for `similarity_adjustment` and the model roles; they were coded from the
  records as they stood.
- Next, agreed with the owner: the held pass on the three pilot records (figures and `effect_of`) and a full reading
  of Binder et al. with a blind check; then a freeze at 0.10 and blind coding of papers the codebook has not seen, by
  coders from two model families.

## 2026-11-26: codebook 0.10 (fixes from the first blind coding test; internality)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- The first blind coding test: one paper coded twice, on an orphan `blind-test` branch with its record and all
  traces removed, by two coders from different model families. The comparison is kept outside this repo. The
  structural calls held up; the disagreements came where the codebook was silent, and the fixes are below.
- Codebook 0.10 (`codebook/CHANGELOG.md`):
  - new core facet `output_route_control` (internality), now criterion 3 of `d-introspection-grounded`, backfilled on every experimental study from the papers
    (fetched this session: Binder v1 §2.1 to 2.2; Lindsey v1 §5.4 to 5.8, §7, App. 12.1.3 and 12.2.2; Song v3 §2;
    Rubin v2 §3.2);
  - `elicitation` and `validated_against` rules for probe-only studies;
  - `varies: initialisation`;
  - the size rule in `comparison`;
  - no `effect_of` on control results.
- Rubin et al. s2 and s3 recoded under the new rules: `validated_against: known_intervention`, `elicitation:
  not_applicable`; s3 `pretraining_progress` became `initialisation`.
- Questions: polarity required on child questions and set on all 25; `q-introspection-success-generalises` is
  `none`, which removes 14 conflicts (159 to 145) that had set the paper's argument against its own results. Two
  frames tightened; new `q-injected-state-decodable` (candidates: Rubin et al.'s seven probe-only claims).
- Build: candidates apply `requires` up the chain; `missing_needs` names the interpretive facets a candidate lacks.
- `scripts/fetch_paper.py` and the CLAUDE.md figures rule; `_paper/` git-ignored.

**Open**

- `scoring_rule` and `control_condition` were not tried blind; Lindsey's backfill of them is mine alone.
- Lindsey s2 (the bias control) is coded `none` for `output_route_control`, operationally; it could be argued
  `not_applicable`, since its answers are not reports about the injected state.
- Links from Rubin et al.'s probe-only claims to `q-injected-state-decodable` are left to the question poser.
- The `blind-test` branch can be deleted once the owner has what he needs from it.

**For the owner to decide**

- Whether the blind test's codings and comparison should go into `pilot/` (they are codings of a published paper;
  the reference coding used for comparison is private).
- A second blind test on a paper the codebook has not been shaped by.

## 2026-11-26: codebook 0.9 (definitions built, starting with Lindsey)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- `definitions/` with one definition, `d-introspection-grounded` (Lindsey
  2026, §3, criteria 1 and 2; internality and metacognitive representation
  recorded as not expressible). It matches 35 claims in 5 studies (Lindsey s1,
  s3, s4, s5; Rubin s1).
- One logic for definitions, frames, reading selectors and `requires`;
  `requires: {definitions: [...]}`; view `substitute`.
- Frames using the definition: candidates for
  `q-introspection-differs-by-post-training` 27 to 16,
  `q-introspection-increases-with-capability` 52 to 28,
  `q-stabilisation-improves-introspection` 87 to 0 (no coded paper tests it);
  `q-injected-state-report` unchanged at 25.
- `construct_mismatches`: 13 experimental studies are labelled introspection
  but do not meet the grounding definition (Binder et al., Song et al., Lindsey
  s2 and s6, Rubin s2 and s3). With one definition loaded this reads as "not
  introspection in Lindsey's grounded sense"; Lindsey §9.6 himself calls
  Binder et al.'s case self-modelling.
- `design/candidate-facets.md`: internality (partly derivable: nothing
  generated before the report; the scoring-rule case would need a facet),
  metacognitive representation, injection depth.

**Tested** on a throwaway copy: definition cycles, bad facet values in logic,
an unknown substituted definition, and `not` with a model field.

**For the owner to decide**

- Which definition to add next (privileged access after Binder et al. and
  Song et al. would make the first substitution view possible).

## 2026-11-26: design proposal for definitions

Coder: claude (claude-opus-5-5), working with the owner.

**Added**

- `design/definitions.md`: named logic over facets for what a design tests, in
  a stated sense, with `construct` kept as the authors' label. Four published
  definitions written as facet logic and evaluated on the coded studies: the
  grounding sense (Lindsey) and the privileged-access sense (Binder et al.;
  Song et al.) split the studies cleanly, and definition-based frames cut
  candidate lists (87 to 53 for `q-privileged-self-access`; 27 to 16 for the
  post-training question). Not built.

**For the owner to decide**

- Whether to build definitions, and whether an internality facet is worth
  adding.

## 2026-11-26: codebook 0.8 (effects, auto stances and candidates, model roles)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- `effect_presence` and `effect_direction` on claims; backfilled on Binder et
  al. c1 to c9 from the claims as coded.
- `question_candidates` and `auto_stance` in the build; frames validated.
  `q-self-prediction-advantage` gains `auto_stance: effect_of [self_vs_other]`.
- Model roles in studies (Binder et al. s2, s3, s5 and Song et al. s2, s3 now
  mark comparison models; Lindsey et al.'s Claude Sonnet 4 is subject and
  judge; Binder et al.'s Claude 3.5 Sonnet is data_source). `variant_of` on the
  two OLMo 2 seed series.
- `similarity_adjustment` on the 19 non-conceptual studies (Song et al. s2
  statistical; Binder et al. s2, s3, s5 and Song et al. s3 none; the rest
  not_applicable).

**Checks**

- Auto stances on `q-self-prediction-advantage` agree with all five hand-made
  links (c2, c3, c4, c5, c8). Conflicts unchanged at 159.
- The similarity reading now matches Binder et al. s2, s3 and s5 only.

**Open**

- Candidate lists are long where frames are one broad value (87 for
  `q-privileged-self-access`). Frames need tightening, or a rule that a frame
  listing several values of one facet means all of them.
- `effect_of` and `effect_presence` are still missing on the Lindsey, Rubin and
  Song records, so auto stances only reach Binder et al. for now.

## 2026-11-26: codebook 0.7 (speaker; links, readings and views built)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- Unit `persona` renamed `speaker` (16 codings). Links moved to `links/` (45,
  none lost; conflicts unchanged at 159). `requires` on questions;
  `q-privileged-self-access` requires a self-report. `post_training_reached`
  on all 42 models. Readings and views built, per `design/readings.md`.

**First views** (`views/views.yaml`, on `q-privileged-self-access`)

- Text answers only (r-logit-readout-not-answer): 27 linked claims count with
  no readings, 16 under the view. The 11 that drop are Rubin et al.'s
  logit-readout claims and Song et al.'s probability-readout claims; Binder et
  al.'s generated answers stay. Conflicting pairs under the root fall from 154
  to 24.
- Similarity critique (r-similarity-uncontrolled): nothing excluded; the
  reinterpretation attaches to 12 claims, including Song et al.'s own, because
  similarity control is not a facet (as the reading's note says).

**For the owner to decide**

- `post_training_reached` for chat API models is `post_trained` until their
  pipelines are coded; Llama 3.1 70B in Binder et al. is `unspecified`.
- Whether similarity control should become a facet, so the similarity reading
  can stop over-matching.

## 2026-11-26: design proposal for readings and views

Coder: claude (claude-opus-5-5), working with the owner.

**Added**

- `design/readings.md`: a proposal, not built. Records hold what papers did
  and found; readings are lenses that reclassify facets (or attach an
  alternative explanation) under the lens only; views pair a question with a
  set of readings. Questions and readings stay independent of each other. Two
  worked examples from published sources (logit readouts against text answers;
  Song et al.'s similarity critique of Binder et al.).

**Learned from the examples**

- Reclassify and reinterpret were enough; exclude and include reduce to
  reclassify.
- Selectors only see facets, so conditions held in free text or in no field
  (an injection layer, whether similarity was controlled) push a reading back
  to named targets.

**For the owner to decide**

- Whether to build it, and whether claim-to-question links move into the same
  layer.

## 2026-11-26: codebook 0.6 (three core facets, polarity, which-questions, templates)

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- `unit_position` brought in line with the other interpretive facets; the 20
  studies that left it out now code `not_applicable`, with a note saying why.
- Questions gain `polarity` and `kind: which` (with `answer_facet`). Used in
  the question set: `q-denial-precedes-post-training` now sits under
  `q-denial-is-post-training-policy`, and `q-report-diverges-from-representation`
  under `q-report-matches-direct-measure`, both inverse. Two which-questions
  added: `q-what-self-reports-draw-on` (report_source) and
  `q-where-denial-comes-from` (origin). Conflict counts are unchanged (159):
  no claim links to the new questions yet.
- Core facets `reasoning`, `system_prompt` and `report_readout`, and
  `varies: reasoning`.
- Templates and a "Coding a paper, in order" section in CLAUDE.md.

**Backfill: what was read** (11-26, through alphaXiv's PDF page extraction;
the original coders' `read_parts` are unchanged)

- Binder et al. v1: abstract, §1 to §5, App. A.1 to A.2.9, A.3.3, A.4.1 to
  A.4.2, A.5. The code was not read, so `system_prompt` is `unspecified`
  throughout; s6 (SAD and OpenAI Evals) is `unspecified` on all three.
- Lindsey v1: §1, §2.2 to 2.4, §4, §5 (parts), §6, §10.3, App. 12.1 to 12.4.2.
  The base-model prompt layout (s3) was not in the pages read; coded from the
  design, operational.
- Rubin et al. v2: everything but the figures as images.
- Song et al. v3: §1 to §4.1, App. A to C. What the instruct models' default
  chat templates contain is not stated; coded `developer_default`, operational.

**Tested** on throwaway copies: an inverse child's stance is flipped on the
root; two claims with different `report_source` answers to a which-question
make one `which_conflicts` row; a stance on a which-question, a bad polarity,
and a template missing a facet each fail validation.

**For the owner to decide**

- The three core facets and their values, especially `generated_choice`, which
  now covers a single item the prompt asks for (a character, a word) as well
  as an option chosen from a list.
- The two inverse placements and the two which-questions.

## 2026-11-26: codebook 0.5 (two tiers) and 28 proposed questions

Coder: claude (claude-opus-5-5), working with the owner.

**Changed**

- Facets are split into a core tier, coded on every study, and an
  interpretive tier, coded when a source states a position, a linked question
  `needs` the facet, or a conflict turns on it (`codebook/README.md`, "Two
  tiers"; `CHANGELOG.md` 0.5). The five interpretive study facets that were
  required no longer are. No record changed: every existing coding stays.
- New special value `not_yet_coded`. The build stores it for interpretive study
  facets left out of a record. There are none today: every existing study
  codes them, and on the two conceptual studies the uncoded ones read as
  `not_applicable`, as before. `unit_position` keeps "absent means no
  position" (`absent_means`).
- Questions can list `needs`, inherited by every question under them.
  `validate.py` checks them on each linked claim and its study; the build adds
  a `question_needs` table; `shared_facets` no longer counts `not_yet_coded`.
  Tested on a throwaway copy: a claim linked to a question needing
  `report_source` and `unit_reporter` fails until both are coded, and
  `unspecified` passes.

**Added**

- 28 questions in 12 trees, for the questions the first users expect to look
  up: where self-reports come from, report against representation, experience
  denials (policy, refusal machinery, training data, before post-training),
  frames and personas, report against behaviour, development through training,
  stabilising the self-model, continuity through carried state, stated
  uncertainty, consent across framing. Every top-level question names its
  `needs` except the last two, which need nothing beyond core facets. None has
  a claim linked yet.

**For the owner to decide**

- The tier split and `needs`.
- The 28 questions: wording, parents, and `needs`. Three are deliberately
  separate trees because "yes" to one counts against another
  (`q-denial-precedes-post-training` against `q-denial-is-post-training-policy`;
  `q-report-diverges-from-representation` against
  `q-report-matches-direct-measure`).
- `q-self-representation-changes-in-midtraining` uses `post_training_recipe`
  and `pretraining_progress` in its frame; `varies` has no value for a
  mid-training contrast.

**Open**

- The first test: code a paper against the new questions at the core tier
  only, then deepen just the facets the questions need, and see whether that
  answers the question and how long each pass takes.

## 2026-11-26: first three records from the pilot

Coder: claude (claude-fable-5-2), working with the owner. Per paper: one
reconciling coder (claude-fable-5-2) and one blind checker (claude-opus-5-5).

**Added**

- `sources/lindsey2026-emergent-introspective-awareness.yaml` (8 studies, 47
  claims), `sources/rubin2026-closer-look-introspection.yaml` (3 studies, 15
  claims), `sources/song2025-fail-to-introspect.yaml` (4 studies, 22 claims),
  with their people, orgs, models and questions.
- Nine questions, five of them under `q-privileged-self-access`.
- The reconcilers' notes and the checkers' tables, under `pilot/`.

**Checked**

- Every claim in the three records was checked against the paper text by a
  coder who had not seen the coding: 83 of 84 supported, 1 overstated and
  corrected. The checkers' wording suggestions were applied.

**Decisions made in the merge, for the owner to confirm**

- Two reconcilers independently created `q-injected-state-report`; one wording
  was kept.
- `q-report-matches-probe` was moved from under `q-privileged-self-access` to
  under `q-report-matches-direct-measure`.
- The Allen Institute's org id is `allen-ai`.
- `unit_disposition` on Rubin's probe-only and no-prompt studies is `weights`
  at low confidence, against both pilot coders' `not_applicable`.

**Learned**

- The Binder and Song records now conflict under the parent question, and the
  facet difference includes trained against spontaneous elicitation, chat
  template against raw text, and behaviour against output probabilities.
- "Which studies of introspection vary training stage or recipe?" returns six
  studies. One of them (Song s2) codes `post_training_stage` because base and
  instruct pairs have their own coefficient, not because it tests the effect
  of post-training.

**Rules added after review with the owner**

- Read the paper and its code together where both exist.
- Look at the figures: the arXiv PDF can be downloaded and its pages read as
  images, which the pilot coders did not do. The three pilot records are
  `text_only` and should have their figure-dependent claims revisited.

**Added after review with the owner**

- `effect_of` on claims, and `shared_facets` on the conflicts view. The owner's
  view is that showing every conflict and filtering by facet is right, so
  nothing is hidden; the new column only allows sorting.

**Open**

- `effect_of` is coded on Binder et al. only. The Lindsey, Rubin and Song
  records need it, and need a pass over their figure-dependent claims now
  that figures can be read. Both are held until the owner says to go.
- Whether a representational property with no behaviour counts as a capacity
  for `unit_disposition`.
- The line between `forward_pass` and `conversation` for an injected state
  that is read back after further tokens.
- No value names the self as regulator, for studies of control over internal
  states.
- The splitting rule needs a tie-break when results are reported apart but
  the only conclusion drawn is a comparison with another study.
- The post-training question exists for Lindsey but Rubin's related claims
  are not linked to it.
- Binder et al. is still coded from the main text only and has not had a
  blind check. Its `llama-3.1-70b` entry may be the same model as the new
  `llama-3.1-70b-instruct`.
- Org kinds for the new orgs are unverified.

## 2026-11-26: first pilot and codebook 0.3

Coder: claude (claude-fable-5-2), working with the owner. Six blind coders
(three claude-fable-5-2, three claude-opus-5-5) each coded one of three papers
from a clean copy of the repo.

**Added**

- `pilot/2026-11-26/`: the six records and the coders' notes, with a summary.
- Codebook 0.3. See `codebook/CHANGELOG.md`.
- Question parents, `other_questions`, `compares`, `to_external`, and lighter
  coding for conceptual studies, in the scripts.
- A rewritten splitting rule and new rules on registries, artefacts, dates,
  questions and relations in `CLAUDE.md`.

**Learned**

- Agreement between the two coders was 87% on 126 facet codings over nine
  matched studies. It is an upper bound: both coders are Claude models, and
  some agreements were the same fallback value chosen for want of a fit.
- Splits matched study for study on the paper with one section per
  experiment, and did not match on the other two.
- With a parent question in place, the Binder and Song records conflict as
  they should, and the facet difference includes trained against spontaneous
  elicitation. This was checked in a scratch copy with one pilot record.

**Open**

- The pilot records are coded against 0.2 and are not in `sources/`. They need
  recoding against 0.3, reconciling (one record per paper, shared ids for
  questions, people, orgs and models) and a check of their numbers against the
  papers by a coder who has not seen them.
- 0.3 has not itself been piloted.
- The conflicts view does not show which models each side is scoped to, so two
  claims in one study that differ only by model show no difference.
- Mixed `basis` or `confidence` within one facet entry cannot be recorded
  apart from the note.
- `report_source` cannot record that a source rules a route out.

**For the owner to decide**

- Confirm or change codebook 0.3.
- Whether the first parent question, `q-privileged-self-access`, is worded as
  wanted. It will sit above most of the introspection literature.
- Still open from 0.2: `stake` and `allegiance`, the fifth `report_source`
  value, and whether `integration` is wanted yet. The pilot papers did not
  exercise them.

## 2026-11-26: codebook 0.2 after review

Coder: claude (claude-fable-5-2), working with the owner.

**Changed**

- Codebook 0.2. See `codebook/CHANGELOG.md` for the full list. The main
  changes: units coded by role, `self_sense` renamed and split with families,
  `object_of_study` as layers with nesting, a `format` facet, and four optional
  claim facets.
- `levels` on coded facets and `scope.conditions` on claims. The conflicts view
  now shows each side's conditions.
- Splitting rule in `CLAUDE.md` now covers models, and there is a rule against
  copying unpublished material into this repo.
- Binder et al. recoded against 0.2.

**Learned**

- Under role coding, Binder comes out as: no occurrent state studied,
  disposition fixed in the weights, reporter a persona. All operational.
- Binder's authors rule out training data as the source of the self-prediction
  advantage but do not say where the report's content comes from, so
  `report_source` cannot be coded. The facet has no way to record "not X".

**Open, in addition to the entry below**

- None of the new facets has been tried on a paper that needs it. The pilot
  should include at least one study each with an occurrent state, a
  non-default persona, a raw-text condition and a traced training origin.

**For the owner to decide**

- Confirm or change codebook 0.2. In particular: whether `stake` and
  `allegiance` earn their place beside `subject` and `authorship`; whether
  `report_source` should have the fifth value `context`; and whether
  `integration` is wanted at all at this stage.
- Whether the framework-derived vocabulary is cleared to be public. It is
  written here in general terms with no results or worked cases.

## 2026-11-26: first draft of the structure

Coder: claude (claude-fable-5-2), working with the owner.

**Added**

- Directory layout, README, `CLAUDE.md`, this log.
- Codebook 0.1: 11 study facets, 3 claim facets, bookkeeping enums.
- `scripts/validate.py`, `scripts/build.py`, `scripts/query.py`.
- One worked example: `sources/binder2024-looking-inward.yaml` (6 studies, 10
  claims), with the people, orgs, models and questions it needs.

**Learned from the worked example**

- Study granularity matters. The first pass put all of the paper's section 4
  into one study, and the conflict view then reported facet differences that
  were not real. It is now two studies.
- The facet diff between the supporting and opposing claims on
  `q-self-prediction-advantage` comes down to `varies: task`. That is correct
  but coarse: the facets do not say that the task was sycophantic
  answer-switching. A facet for the behaviour or property being reported on may
  be needed.
- Unit of self, sense of self and object of study were all `operational` for
  this paper. None is stated by the authors.

**Open**

- Binder et al. was coded from the main text of v1 only. Appendices were not
  read, so model lists for studies s5 and s6 and several details are flagged in
  the record. Venue, code URL and dataset URL are not filled.
- All five model records have `stage: null`. No pipelines are coded yet.
- Org kinds were filled from general knowledge and not checked.
- ORCIDs are all null.

**For the owner to decide**

- Review the codebook, especially `self_sense` (two proposed values,
  `authorship` and `subject`) and `unit_of_self` (`character` as a unit).
- Licence for data and codebook (CC BY 4.0 was discussed).
- Whether to add a facet for the specific behaviour or property reported on.
- The remaining twelve pilot papers are not yet coded.

# Open

What is open in this repo: decisions waiting on the owner, proposed codebook changes, known gaps in records, and
things to watch. It replaces the session log (`LOG.md`, closed 2026-11-27 and kept for its history).

This file is rewritten, not appended to. Add an item when you find it; remove it in the pull request that resolves
it, and say so in the pull request description. What was done, and why, lives in git history and the pull request
descriptions. Keep each item to a few lines and point to the record, claim or pull request it comes from.

Items carried over from `LOG.md` are marked *(log)*; they were checked against the repo as it stood on 2026-11-27,
not re-read in their sources.

## Waiting on the owner

- **The next codebook review** (the codebook is frozen at 0.10 until then): everything under "Codebook review"
  below. Proposed values are not in the facet files yet.
- **Construct for Betley et al.:** `[self_knowledge, self_prediction]` for "behavioral self-awareness", with
  `introspection` added on s2 and `self_knowledge` alone on s7. Confirm. *(log)*
- **The pilot's blind-test codings:** whether they go into `pilot/` (they are codings of a published paper; the
  reference coding used for comparison is not public). *(log)*
- **The blind-test branches** `blind-test` and `blind-binder` can be deleted once the owner has what he needs from
  them. *(log)*
- **The framework-derived vocabulary** (codebook 0.2): cleared to be public? It is written in general terms, with
  no results or worked cases. *(log)*

## Codebook review (after the freeze)

Gaps met while coding, with the nearest value used meanwhile. A nearest value is read by the build as if it were
right, so frames on it pick up claims they were not meant for; where that happens it is said below.

- **`varies`**
  - No value for layer, as an attachment point or a variable (urgent; PR #16).
  - No value for a mid-training contrast (`q-self-representation-changes-in-midtraining` frames on
    `post_training_recipe` and `pretraining_progress`). *(log)*
  - No value for the number of in-context examples (Fornasiere s11, coded `prompt_framing`).
  - No value for an inference-time sampling setting (Comsa s2, coded `activation_intervention`, so frames on
    that value pick it up). Proposed: `sampling_setting`.
  - One rule for a contrast whose other arm is another study: something the study `varies` (Lindsey s3) or only a
    `compares` between studies (Binder s7). Owner: ideally the comparison surfaces by itself at the question or
    framing layer. *(log)*
- **`report_target`**
  - No value for reports about another persona's behaviour (Betley s8, s9).
  - No value for a setting of the inference process (Comsa s2, coded `injected_state`). Proposed: a new value, or
    widening `injected_state` to "a state or setting the experimenter placed or altered".
- **`report_source`**
  - No value for self-knowledge reached by out-of-context reasoning over fine-tuning data (Betley; Song c22), left
    uncoded.
  - No value for imitation of human self-reports learned in pretraining (Comsa c3). Proposed: `human_mimicry`.
  - Cannot record that a source rules a route out. *(log)*
- **`construct`**
  - Keyed to the authors' label throughout; senses such as confidence or calibration move into definitions, and
    the construct entry points question posers to the definitions for each sense (PR #16).
  - No value for attributing mind to other entities (Kim s2, s6, coded `experience_reports`, so Kim c7 to c10
    turn up as candidates for `q-denial-shares-refusal-machinery`). Proposed: `mind_attribution`
    (`design/candidate-facets.md`).
  - No value for stated beliefs and values (Kim s3, s4, coded `preferences`). Proposed: `beliefs_values`.
  - No value for theory of mind or general capability used as a control (Kim s5, s7, coded `not_applicable`).
- **`effect_presence`:** no value for an effect opposite to the question's direction on an unordered contrast
  (Song c8 to c10, coded `absent` with the reversal in the note). Either a `reversed` value, or auto stances
  reading `effect_direction` on `self_vs_other`. *(log)*
- **Units**
  - No value for a single response, several forward passes but less than a conversation (Comsa s3, coded
    `speaker`).
  - The line between `forward_pass` and `conversation` for an injected state read back after further tokens.
    *(log)*
  - Whether a representational property with no behaviour counts as a capacity for `unit_disposition`. *(log)*
- **`validated_against`:** no value for a check against known facts about the architecture (Comsa s1, coded
  `behaviour`).
- **`output_route_control`:** does not tell the model's own output in the same response from its earlier turns
  (Comsa §4; `d-introspection-causal`'s `not_expressible`).
- **Recording:** mixed `basis` or `confidence` within one facet entry can only go in the note. *(log)*
- **The freeze rule itself:** for facets that question frames use, `unspecified` plus a proposal here may be
  safer than the nearest value, which leaks into candidates.

## Questions, links and stances

- **Guidance for question posers, not a restriction:** when a question asks "how well", say which measure is meant
  (sensitivity, or the rate of a given report). The first conflict between two papers on a question as posed,
  Fornasiere c28 against Lindsey c11, c14 and c20 on `q-introspection-differs-by-post-training`, turns on this: on
  a sensitivity reading DPO changes nothing; on a report-rate reading it lowers it.
- **The task-only conflict rule** becomes the question poser's choice, with the build grouping a question's
  evidence by task.
- **Auto stances:** each yes/no question to state which effect counts as support; track the share of links that
  are automatic (45 by hand and 6 automatic before the step-1 papers).
- **Possible narrower questions:**
  - Does training that changes the default persona shift its descriptions of other characters? (Betley s8; c32 and
    c33 are linked to `q-self-model-shared-across-personas` with the mismatch noted.)
  - Does injected-state reporting emerge in pretraining? (Fornasiere c14, c17 reach no question.)
- **Not linked though the frames match:** Betley c19, c22 (needs `unit_reporter`), c28, c29 (reversal training is
  training on the reporting form); Kim c1 (released reports are not checked against an internal measure); Rubin's
  probe-only claims and `q-injected-state-decodable`, left to the question poser *(log)*; Rubin's post-training
  claims and the post-training question *(log)*.

## Records

- **Availability:** Lindsey and Rubin have code and data `unknown`; search, then set `released` or
  `not_released`.
- **Splits:** Rubin c13 bundles an injection effect in the base with an unexplained control result; Lindsey c6
  and Song c7 are `mixed` and could be split by comparison. *(log)*
- **Relations:** Rubin's `to_external` citation of Fornasiere could point at the record (Rubin cites an earlier
  version; check which).
- **Not viewed:** Lindsey Figs. 29 to 31 per panel (legible only at page resolution); Fornasiere Figs. 20, 23 to
  26, 34 to 38, 41 to 45; Betley Figs. 25 to 29 and others listed in its `read_parts`. The claims that cite them
  say so.
- **Unverified:** org kinds added from general knowledge; Hugging Face ids in Kim's model notes, inferred from the
  printed names.
- **Smaller calls flagged by coders:** Comsa s1, s2 `study_kind: experiment` (the authors disclaim an empirical
  study); Lindsey s2 `output_route_control: none` (could be `not_applicable`) *(log)*; the study-splitting rule
  needs a tie-break when results are reported apart but the only conclusion is a comparison with another study
  *(log)*.
- **Blind checks:** Binder et al. has had one blind coding by another family; Ji-An Li et al. (PR #16) waits for
  one.

## Build

- **Conflicts:** default to conflicts within the question as posed, with the rollup from child questions on
  request, ranked by how alike the two sides are. The rollup is most of the table (672 rows after the step-1
  papers).
- **Model scope:** the conflicts view does not show which models each side is scoped to, so two claims in one
  study that differ only by model show no difference. *(log)*
- **Candidate lists** are long where a frame is one broad value. Frames need tightening, or a rule that a frame
  listing several values of one facet means all of them. *(log)*

## To watch (owner, 2026-11-27)

- **Granularity:** whether the split into studies, claims and effect fields is the right level of detail. Judge it
  from the blind tests: per facet and field, coder agreement, time per paper, and whether any question,
  definition or reading uses it. One that fails all three after twenty or thirty papers is a candidate to merge or
  drop.
- **Scale:** records are about 60 KB per paper. `conflict_facet_diff` grows roughly quadratically in claims per
  question; around fifty papers, compute it per question on demand. At scale, take an outside model list rather
  than keeping our own registry. Merge pull requests a few at a time: the registries are single files, so
  parallel additions conflict.
- **Sparsity:** whether similar designs coded by different coders land on shared questions and comparable facet
  values.
- **Scope:** which areas of research the repo covers, later. Betley and Kim needed values outside the
  introspection literature the codebook was built from.

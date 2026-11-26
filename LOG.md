# Session log

Newest first. Each entry: what changed, what is open, what needs a decision.

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

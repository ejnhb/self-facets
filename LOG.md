# Session log

Newest first. Each entry: what changed, what is open, what needs a decision.

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

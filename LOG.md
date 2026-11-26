# Session log

Newest first. Each entry: what changed, what is open, what needs a decision.

## 2026-11-26: first draft of the structure

Coder: claude (claude-fable-5-2), working with the owner.

**Added**

- Directory layout, README, `CLAUDE.md`, this log.
- Codebook v0.1: 11 study facets, 3 claim facets, bookkeeping enums.
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

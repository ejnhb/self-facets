# Pilots

Records and notes from trial runs of the codebook, kept as the evidence behind
codebook changes. Nothing here is part of the database: the build reads only
`sources/`, and these records are coded against older codebook versions.

## 2026-11-26: three papers, two coders each

**Setup.** Three papers were each coded twice, by a `claude-fable-5-2` coder
and a `claude-opus-5-5` coder. Each coder had a clean copy of the repo at
codebook 0.2 and the paper's arXiv id, and nothing else: no access to the other
coder's work or to the discussions behind the codebook. Each produced a source
record and a notes file on where the codebook and instructions did not fit.

| Paper | Chosen to test |
|---|---|
| arXiv 2601.01828 | A study of an occurrent, injected state |
| arXiv 2611.15267 | Training stage as the variable; base models; probes |
| arXiv 2503.07513 | A negative result that disputes an earlier paper |

Each folder holds the coder's record, its `questions.yaml` (the questions it
reused or added) and its `NOTES.md`.

**How the papers were split into studies**

| Paper | fable | opus | Same split? |
|---|---|---|---|
| 2601.01828 | 7 studies, 39 claims | 7 studies, 38 claims | Yes, study for study |
| 2611.15267 | 4 studies, 15 claims | 2 studies, 12 claims | No |
| 2503.07513 | 3 studies, 16 claims | 3 studies, 20 claims | No: one by analysis, one by experiment |

**Facet agreement.** Nine studies could be matched between coders (seven from
2601.01828, two from 2611.15267), giving 126 facet codings.

| Facet | Exact agreement |
|---|---|
| `unit_disposition` | 3 of 9 |
| `self_sense` | 6 of 9 |
| `elicitation` | 6 of 9 |
| `varies`, `evidence`, `construct`, `comparison`, `unit_state` | 8 of 9 each |
| `unit_reporter`, `object_of_study`, `validated_against`, `report_target`, `format`, `study_kind` | 9 of 9 each |
| All | 109 of 126 (87%) |

Read this as an upper bound. Both coders are Claude models and share blind
spots. Some agreements were the same fallback: both coders of 2611.15267 filed
a linear probe under `other_model` and noted that nothing fitted. `self_sense`
was marked low confidence in 13 of its 18 codings.

**What it showed**

- The question model hid a real dispute. Both coders of 2503.07513 judged the
  existing question on self-prediction too narrowly worded to reuse and wrote
  a new one, so that paper's disagreement with the earlier one produced no
  conflict.
- The splitting rule gave different answers depending on whether a coder
  followed its heading, its test or its example.
- A capacity (being able to detect an injected state) was coded as a
  disposition by one coder and as not applicable by the other.
- Injection and probe designs fell between `self_facts` and `self_model`.
- Base models on raw text had no natural value for who is reporting.
- `comparison` took one value where most studies had two contrasts.
- There was no way to record "all text read, figures seen only as captions",
  and the two coders of 2601.01828 recorded the same reading differently.

Codebook 0.3 responds to these; see `codebook/CHANGELOG.md`.

**Reconciliation and check.** After codebook 0.3, one further coder per paper
(`claude-fable-5-2`) merged the two pilot codings into a single record against
0.3, re-reading the paper. A separate checker (`claude-opus-5-5`) that had seen
neither the pilot codings nor the reconciler's notes then checked every claim
against the paper. The reconciled records are in `sources/`; each paper's
`reconciled/` folder here holds the reconciler's notes on what it decided and
the checker's table.

| Paper | Reconciled record | Checker's verdicts |
|---|---|---|
| 2601.01828 | 8 studies, 47 claims | 47 supported |
| 2611.15267 | 3 studies, 15 claims | 15 supported |
| 2503.07513 | 4 studies, 22 claims | 21 supported, 1 overstated (corrected) |

The reconcilers removed or corrected about ten items in the pilot records
that the papers did not support, mostly results visible only in figures and
claims scoped to models the text does not name. The checkers suggested a
further dozen wording changes, which were applied.

**Limits**

- Reconciler and checker are both Claude models. The check is of claims
  against the text, not of the facet codings.
- No coder could see figures. Claims whose values sit only in a figure are
  marked as such in the records.
- The two coders of 2503.07513 did not have the same inputs: one read the
  authors' code repository and one could not reach it.
- Three papers, all on introspection. Facets for persona, continuity, affect
  and training origin were barely exercised.

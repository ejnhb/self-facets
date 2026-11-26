# self-facets

A faceted index of model psychology literature.

Papers on model selfhood, introspection and welfare often seem to disagree
because they are not about the same thing: a different unit of self, a
different sense of "self", a different persona, a model at a different stage of
training. This repo records what each study was actually run on and what it
found, so that results can be lined up by those differences.

**Status: early draft.** The codebook has been through one pilot (three papers,
two coders each; see `pilot/`) and one paper is coded as a worked example.
Expect breaking changes.

## How it is organised

| Path | What it holds |
|---|---|
| `codebook/` | Definitions and decision rules for every facet and controlled value |
| `sources/` | One file per piece of work, holding its studies and claims |
| `questions/` | Questions that claims take a stance on |
| `models/` | Model checkpoints, their lineage and training stages |
| `datasets/` | Training datasets referenced by model stages and claims |
| `people/`, `orgs/` | Authors and organisations |
| `scripts/` | Validation, build and query tools |
| `pilot/` | Records and notes from codebook pilots, kept as evidence for codebook changes |

The YAML files are the source of truth. `scripts/build.py` compiles them into a
SQLite database for querying; the database is derived and not committed.

## The record model

- A **source** is a piece of work. Its paper, code, data and blog post are
  **artefacts** attached to it, so a repo with no paper and a paper with no
  code are both sources.
- A **study** is one experimental setup within a source. The facets are coded
  here: what was tested, on which models, what was varied, what was measured
  and what the measurement was checked against. The unit is coded by role:
  where the state under study lives, what a reported disposition is fixed in,
  and who does the reporting.
- A **claim** is one finding, in a sentence or two, tied to the study behind
  it. A claim inherits its study's facets. It can link to a **question** with a
  stance (supports, against, mixed, inconclusive).
- Questions form a shallow tree: a narrow question names a broader one as its
  parent.
- Two claims **conflict** when they take opposite stances on one question, or
  on questions under the same parent. The build produces a view listing the
  facets on which their studies differ.

Every coding records who made it, from which version of the source, and how
much of the source was read. `unspecified` is a legitimate value: it marks that
a source does not say which unit, sense or persona it means.

## Using it

```
pip install -r requirements.txt
python scripts/validate.py      # check records against the codebook
python scripts/build.py         # write build/self-facets.sqlite
python scripts/query.py "SELECT id, title FROM sources"
```

Find studies that could bear on "does introspection differ by post-training
stage?":

```sql
SELECT DISTINCT a.study
FROM study_facets a JOIN study_facets b ON b.study = a.study
WHERE a.facet = 'construct' AND a.value = 'introspection'
  AND b.facet = 'varies'    AND b.value = 'post_training_stage';
```

See where conflicting claims differ:

```sql
SELECT * FROM conflict_facet_diff;
```

Plain text search over `sources/` works too, with no build.

## Shared and personal layers

This repo is the shared layer. It holds nothing about any one reader.
Reading status, personal notes and opinions belong in a separate overlay that
refers to records here by id. Nothing here refers to an overlay.

## Reliability

Much of the coding is drafted by an AI model and is marked `coded_by: claude`
with `status: draft` until a person has checked it against the source. Treat
draft records as leads, and check the source before citing a claim from here.

## Licence

Code is under the MIT licence (see `LICENSE`). The licence for the data and
codebook is not yet settled.

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
| `links/` | Which claims bear on which questions, with stances: one file per source |
| `readings/` | Lenses that change how matching claims are read, without editing them |
| `views/` | A question answered with chosen readings applied |
| `templates/` | Annotated templates for every kind of record |
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
  it. A claim inherits its study's facets. Sources, studies and claims record
  what the paper did and found, and nothing more.
- A **link** says a claim bears on a **question**, with a stance (supports,
  against, mixed, inconclusive). Links are kept apart from the records because
  they are the judgement of whoever poses the question, not part of the paper.
- Questions form a shallow tree: a narrow question names a broader one as its
  parent, and says which way it points (`polarity`). A question answered by a
  choice rather than yes or no names the facet that answers it. A question can
  `require` facet values for a claim to count as evidence.
- Two claims **conflict** when they take opposite stances on one question, or
  on questions in the same tree. The build lists the facets on which their
  studies differ.
- A **reading** is a lens: it changes, under a view only, how matching claims
  are read (a facet value, or an alternative explanation beside the result).
  A **view** answers a question with chosen readings applied, and the build
  shows what changes against no readings. See `design/readings.md`.

Every coding records who made it, from which version of the source, and how
much of the source was read. `unspecified` is a legitimate value: it marks that
a source does not say which unit, sense or speaker it means.

## Using it

```
pip install -r requirements.txt
python scripts/validate.py      # check records against the codebook
python scripts/build.py         # write build/self-facets.sqlite
python scripts/query.py "SELECT id, title FROM sources"
```

Find findings on "does introspection differ by post-training stage?":

```sql
SELECT c.id, c.statement
FROM claims c
JOIN claim_effects e ON e.claim = c.id AND e.variable = 'post_training_stage'
JOIN study_facets f ON f.study = c.study
WHERE f.facet = 'construct' AND f.value = 'introspection';
```

See where conflicting claims differ:

```sql
SELECT * FROM conflicts ORDER BY shared_facets DESC;
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

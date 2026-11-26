# Codebook

The codebook defines every controlled value used in the database. A value that
is not defined here fails validation.

Status: **v0.6, draft.** Revised after a six-coder pilot on three papers
(see `pilot/`), then split into core and interpretive tiers. See `CHANGELOG.md`.

## Three kinds of file

- **Facet files** (`self_sense.yaml`, `varies.yaml`, ...): one facet per file.
  Each value has a `definition` and a `rule` saying when to use it, and each
  file says which tier the facet is in (below).
- **Vocabulary files** (`units.yaml`): a value list shared by several facets.
  A facet uses one by naming it in `values_from`. The four unit facets share
  one list of units and differ only in the role the unit plays.
- **`enums.yaml`**: bookkeeping vocabularies (read depth, artefact kinds,
  training methods, ...). Short definitions, no decision rules.

## Two tiers

Facets come in two tiers, named by `tier` in each file.

- **Core** facets describe the design: what was run, varied, measured and
  checked against. The pilot coders agreed on them (8 or 9 of 9 matched
  studies), and they answer the filter queries. Every study codes every
  required core facet.
- **Interpretive** facets place a study in the framework: which unit, which
  sense of self, which layer, where a report comes from. They are slower to
  code and less reliable (`self_sense` matched on 6 of 9 studies, 13 of its 18
  codings low confidence; `unit_disposition` on 3 of 9), and most of their
  codings are operational, the coder's reading rather than the source's
  statement. They are coded when one of these holds:
  - the source states a position on the matter;
  - a claim in the study links to a question that `needs` the facet (below);
  - a conflict between two claims turns on it.

  Otherwise they are left out, and the build stores them as `not_yet_coded`.
  A coder who reads for a facet and finds the source silent codes
  `unspecified`, or `not_applicable` when the facet does not apply (for
  `unit_position`, a source that takes no position).

So a paper can be coded quickly at the core tier and deepened later, where the
deeper coding changes an answer.

### Questions say what they need

A question can list the interpretive facets its evidence must have coded:

```yaml
- id: q-self-report-from-self-model
  needs: [report_source, unit_reporter]
```

Validation then requires every claim linked to that question, or to any
question under it, to code those facets: study facets on its study, claim
facets on the claim. `unspecified` counts as coded; `not_yet_coded` does not.

### Which way a question points, and questions that are not yes or no

Each question below another names its `polarity` (direct, inverse or none),
and a question answered by a choice is `kind: which` with an `answer_facet`.
The rules are at the top of `questions/questions.yaml`.

## The facets

Study facets:

| Facet | Tier | Question |
|---|---|---|
| `study_kind` | core | What kind of work is this unit? |
| `format` | core | Chat template or raw text? |
| `construct` | core | Which construct is measured? |
| `report_target` | core | What is the self-report about? |
| `evidence` | core | Which channels of evidence are collected? |
| `validated_against` | core | What is the report checked against? |
| `varies` | core | What does the study vary? |
| `comparison` | core | What comparisons does the study make? |
| `elicitation` | core | How was the report or capacity brought out? |
| `reasoning` | core | Could the model reason before the scored answer? |
| `system_prompt` | core | What system prompt was it run under? |
| `report_readout` | core | How is the self-report read out? |
| `unit_state` | interpretive | Where does the state under study live? |
| `unit_disposition` | interpretive | What is the disposition under study fixed in? |
| `unit_reporter` | interpretive | Who does the reporting? |
| `unit_position` | interpretive | Which unit does the source argue is the self? |
| `self_sense` | interpretive | What does "self" mean here? |
| `object_of_study` | interpretive | Which layer of the system is targeted? |

Claim facets:

| Facet | Tier | Question |
|---|---|---|
| `evidence_kind` | core | What kind of support does the source give? |
| `stance` | core | How does the claim bear on its question? (with a question) |
| `disposition` | core | Which trained stance is the claim about? (optional) |
| `report_source` | interpretive | Where does the report's content come from? |
| `origin` | interpretive | Where does the disposition come from? |
| `integration` | interpretive | How deeply is the stance held? |
| `aspect` | interpretive | Represented, functional, or both? |

A study of kind `conceptual` or `review` need only code `study_kind`,
`self_sense`, `construct` and, where it has one, `unit_position`. The other
facets may be left out and are read as `not_applicable`.

The interpretive claim facets record what a source argues or tests. Leave them
off when the source does not address the matter; do not fill them with the
coder's own reading. When a question needs one and the source does not settle
it, code `unspecified`.

## Facet file format

```yaml
facet: object_of_study
version: 0.5
applies_to: study        # study | claim
cardinality: many        # one | many
required: false          # must every record code it? (core facets only)
tier: interpretive       # core | interpretive
question: Which layer of the system does the study target?
values:
  default_persona:
    definition: ...
    rule: ...
```

## Special values

Every study facet also accepts these values, which are not listed in the files:

- `unspecified`: the facet applies, but the source does not say and the
  operationalisation does not settle it. This is a finding, not a gap: it is how
  the database shows that two results may not be about the same thing.
- `not_applicable`: the facet does not apply to this study (for example
  `report_target` in a study with no self-report).
- `not_yet_coded` (interpretive facets only): nobody has coded it. Usually
  written by leaving the facet out; the build stores it. Unlike `unspecified`,
  it says nothing about the source.

## Coding a facet on a study

Short form, when there is nothing to add:

```yaml
evidence: [self_report, behaviour]
```

Long form, when the coding needs support:

```yaml
unit_disposition:
  value: weights
  basis: operational     # stated | operational
  author_term: "the model"
  where: "§3.4"
  confidence: medium
  note: Why this value and not a neighbouring one.
```

- `basis` and `confidence` apply to the whole entry. If one value is stated
  and another inferred, use the weaker label and say which is which in the note.
- `basis: stated` means the authors say it. `basis: operational` means the coder
  inferred it from what the experiment did.
- `author_term` keeps the source's own word next to our coding, so recoding
  later does not need a reread.
- `nested_in` records that the coded layer sits inside another, for example
  `object_of_study: {value: character, nested_in: default_persona}`.
- `levels` records the conditions actually used for a coded value, as free
  text keyed by that value. It is mainly for `varies`:

  ```yaml
  varies:
    value: [task, model_size]
    levels:
      task: [second character of the output, whether it switches its answer]
  ```

## Scope on a claim

A claim inherits the facets and models of its study. When it holds for only
part of the study, narrow it:

```yaml
scope:
  models: [gpt-4o-2024-05-13]
  conditions: Properties of short outputs.
```

`conditions` is free text and usually names some of the study's `levels`.

## What a claim is about

A claim that reports the effect of a variable the study varied names it:

```yaml
effect_of: [self_vs_other]
```

The value must be one of the study's `varies` values. This is what separates
the contrast a study draws conclusions about from the things it varied along
the way.

## Changing the codebook

1. Edit the facet file and bump its `version`.
2. Add a line to `CHANGELOG.md` saying what changed and why.
3. Recode affected records. When a new facet is added, make it interpretive
   unless every study needs it, and backfill only the records a current
   question needs; the rest stay `not_yet_coded`.

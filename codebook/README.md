# Codebook

The codebook defines every controlled value used in the database. A value that
is not defined here fails validation.

Status: **v0.2, draft.** Written before the pilot and revised once after
review. Expect definitions to change as the first papers are coded; see
`CHANGELOG.md`.

## Three kinds of file

- **Facet files** (`self_sense.yaml`, `varies.yaml`, ...): one facet per file.
  These are interpretive. Each value has a `definition` and a `rule` saying when
  to use it.
- **Vocabulary files** (`units.yaml`): a value list shared by several facets.
  A facet uses one by naming it in `values_from`. The four unit facets share
  one list of units and differ only in the role the unit plays.
- **`enums.yaml`**: bookkeeping vocabularies (read depth, artefact kinds,
  training methods, ...). Short definitions, no decision rules.

## The facets

Study facets, coded on every study:

| Facet | Question |
|---|---|
| `study_kind` | What kind of work is this unit? |
| `unit_state` | Where does the state under study live? |
| `unit_disposition` | What is the disposition under study fixed in? |
| `unit_reporter` | Who does the reporting? |
| `unit_position` | Which unit does the source argue is the self? (optional) |
| `self_sense` | What does "self" mean here? |
| `object_of_study` | Which layer of the system is targeted? |
| `format` | Chat template or raw text? |
| `construct` | Which construct is measured? |
| `report_target` | What is the self-report about? |
| `evidence` | Which channels of evidence are collected? |
| `validated_against` | What is the report checked against? |
| `varies` | What does the study vary? |
| `comparison` | What is the comparison structure? |
| `elicitation` | How was the report or capacity brought out? |

Claim facets:

| Facet | Question |
|---|---|
| `evidence_kind` | What kind of support does the source give? |
| `stance` | How does the claim bear on its question? (with a question) |
| `disposition` | Which trained stance is the claim about? (optional) |
| `report_source` | Where does the report's content come from? (optional) |
| `origin` | Where does the disposition come from? (optional) |
| `integration` | How deeply is the stance held? (optional) |
| `aspect` | Represented, functional, or both? (optional) |

The optional claim facets record what a source argues or tests. Leave them
off when the source does not address the matter; do not fill them with the
coder's own reading.

## Facet file format

```yaml
facet: unit_of_self
version: 0.1
applies_to: study        # study | claim
cardinality: many        # one | many
required: true           # must every record code it?
question: Which unit is the "self" under study?
values:
  weights:
    definition: ...
    rule: ...
```

## Special values

Every study facet also accepts two values that are not listed in the files:

- `unspecified`: the facet applies, but the source does not say and the
  operationalisation does not settle it. This is a finding, not a gap: it is how
  the database shows that two results may not be about the same thing.
- `not_applicable`: the facet does not apply to this study (for example
  `report_target` in a study with no self-report).

## Coding a facet on a study

Short form, when there is nothing to add:

```yaml
evidence: [self_report, behaviour]
```

Long form, when the coding needs support:

```yaml
unit_of_self:
  value: weights
  basis: operational     # stated | operational
  author_term: "the model"
  where: "§3.4"
  confidence: medium
  note: Why this value and not a neighbouring one.
```

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

## Changing the codebook

1. Edit the facet file and bump its `version`.
2. Add a line to `CHANGELOG.md` saying what changed and why.
3. Recode affected records. When a new facet is added, backfill only the
   records a current question needs; the rest may carry `unspecified` with a
   note `not yet coded` until someone gets to them.

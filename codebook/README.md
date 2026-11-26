# Codebook

The codebook defines every controlled value used in the database. A value that
is not defined here fails validation.

Status: **v0.1, draft.** Written before the pilot. Expect definitions to change
as the first papers are coded; see `CHANGELOG.md`.

## Two kinds of file

- **Facet files** (`unit_of_self.yaml`, `varies.yaml`, ...): one facet per file.
  These are interpretive. Each value has a `definition` and a `rule` saying when
  to use it.
- **`enums.yaml`**: bookkeeping vocabularies (read depth, artefact kinds,
  training methods, ...). Short definitions, no decision rules.

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

## Changing the codebook

1. Edit the facet file and bump its `version`.
2. Add a line to `CHANGELOG.md` saying what changed and why.
3. Recode affected records. When a new facet is added, backfill only the
   records a current question needs; the rest may carry `unspecified` with a
   note `not yet coded` until someone gets to them.

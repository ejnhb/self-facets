# Working in this repo

Instructions for any Claude session (or other agent) maintaining self-facets.
Read `README.md` for the record model and `codebook/README.md` for how facets
are coded.

## Start of session

1. Read the last few entries of `LOG.md` to see what was done and what is open.
2. Run `python scripts/validate.py`. If it fails, fix that first.

## Coding rules

- **Code from the source, never from memory.** Open the paper, post or repo in
  this session before writing or changing a record. If you could not read it,
  do not code it.
- **Record what you read.** Fill `coding.version_read`, `read_depth` and
  `read_parts` truthfully. A machine-generated summary is `summary_only`, not
  `full_text`. If a detail sits in an appendix you did not read, say so in the
  claim's `where` or `note`.
- **Every required facet is coded on every study.** Use `unspecified` when the
  source does not say and the design does not settle it, and `not_applicable`
  when the facet does not apply. Never leave one out to mean either.
- **Say whether a coding is stated or operational.** If the authors did not say
  it and you inferred it from the design, set `basis: operational`.
- **Keep the author's term.** When the source has its own word for the self or
  the construct, put it in `author_term` next to the coded value.
- **Claims are in our words**, one or two sentences, with the numbers that
  matter and a `where` pointer. Quote at most a short phrase.
- **One study per setup.** A claim inherits every facet of its study, so
  bundling different sub-experiments into one study makes conflicts look like
  they differ on things they do not. Split when the facets would differ.
- **Split a chain into links.** "Model has disposition", "it appears at stage
  n", "dataset z causes it" and "mechanism m mediates it" are separate claims,
  each with its own evidence kind.
- **Registries stay small.** Add a model, dataset, person or org only when a
  record needs it, and only to the depth needed. Leave `stage: null` on a model
  until its pipeline is coded from the developer's documentation.
- **Mark your work.** Set `coded_by: claude`, `coder_model` to your model id,
  and `status: draft`. Only a human reviewer sets `status: reviewed`.

## Ids

- Source: `firstauthorYEAR-short-title`, and the file is `sources/<id>.yaml`.
- Study and claim: `<source id>.s1`, `<source id>.c1`, numbered in order added.
  Never renumber or reuse an id; other records may point at it.
- Person: `family-given`. Org, model, dataset: a short lowercase slug.
- Question: `q-short-description`.

## Codebook changes

Do not invent a value in a record. If the codebook lacks what you need, propose
the change: edit the facet file, bump its version, add a `CHANGELOG.md` line,
and flag it in `LOG.md` for the owner to confirm.

## Shared layer only

Nothing in this repo may refer to a reader: no reading status, no personal
notes, no opinions about a paper's quality beyond what `evidence_kind` and
`note` are for. Those go in the owner's private overlay.

## End of session

1. Run `python scripts/validate.py` and `python scripts/build.py`.
2. Add an entry to `LOG.md`: date, what was added or changed, what was left
   open, anything the owner needs to decide.
3. Commit on a branch and open a pull request unless told otherwise.

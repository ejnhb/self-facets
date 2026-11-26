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
- **A study is a set of results that share every facet value.** Sections and
  headings do not decide the split; the facets do. The test: would any claim
  in the study inherit a facet value that is wrong for it? If so, split.
  - Results on different topics (construct, report target, validation,
    elicitation) are different studies, even when they come from the same runs.
    A probe-only analysis is split from the self-report analysis it sits
    beside, because its claims would otherwise inherit self-report facets.
  - Different models are not different studies. List them all, and narrow a
    claim to some of them with `scope.models`.
  - Two contrasts in one design are not different studies. `comparison` and
    `varies` take several values.
  - Models that differ on a facet (a base model on raw text, a chat model
    through its template) are split only when their results are reported
    apart. When results pool or compare them, keep one study, code both
    values, and say in the note which models have which.
  - A claim that compares two studies goes in the one whose facets fit it
    best, and names the other in `compares`.
- **Record the conditions.** `varies` names a variable; put the conditions
  actually used in its `levels`. When a claim holds for only some of them, say
  which in `scope.conditions`.
- **A conflict that differs only on task means the question is too coarse.**
  Read the two claims' conditions, then split the question or add one about
  what moderates the effect.
- **Optional claim facets record the source's view, not yours.** Code
  `report_source`, `origin`, `integration` and `aspect` only when the source
  argues or tests the matter.
- **Split a chain into links.** "Model has disposition", "it appears at stage
  n", "dataset z causes it" and "mechanism m mediates it" are separate claims,
  each with its own evidence kind.
- **Registries stay small.** Add a model, dataset, person or org only when a
  record needs it, and only to the depth needed. Leave `stage: null` on a model
  until its pipeline is coded from the developer's documentation.
  - A checkpoint gets its own model entry only when a claim is scoped to it.
    A sweep over many checkpoints is one entry for the series, with the
    checkpoints listed in the `levels` of `varies`.
  - Networks the authors built (random initialisations, toy models) get one
    entry with the authors' organisation as developer.
  - Do not register a model the source does not name. Say so in the study note.
  - The datasets registry is for training data. Evaluation datasets go in the
    study's `design` text.
- **The source includes its artefacts.** Code and data released with a paper
  count as the source. If you read them, say so in `read_parts`; if a detail
  comes only from the code, say so in the claim's `where`.
- **`date` is the date of the version read.**
- **Questions.** Before adding a question, look for one that fits. If an
  existing question is close but its wording excludes this design, add a
  narrower question and give both the same `parent`, creating the parent if
  needed. A claim that bears on a second question lists it under
  `other_questions` with its own stance.
- **Relations.** `from` is the work doing the criticising or extending. Point
  `to` at a coded record, or use `to_external` with a citation when the target
  is not coded yet.
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

This repo is public. Do not copy unpublished material into it: no results,
names, examples or wording from the owner's private notes or other private
repos, even when those are available in the session. Use them to understand a
request, and write records and definitions from published sources.

## End of session

1. Run `python scripts/validate.py` and `python scripts/build.py`.
2. Add an entry to `LOG.md`: date, what was added or changed, what was left
   open, anything the owner needs to decide.
3. Commit on a branch and open a pull request unless told otherwise.

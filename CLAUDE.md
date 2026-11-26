# Working in this repo

Instructions for any Claude session (or other agent) maintaining self-facets.
Read `README.md` for the record model and `codebook/README.md` for how facets
are coded.

## Start of session

1. Read the last few entries of `LOG.md` to see what was done and what is open.
2. Run `python scripts/validate.py`. If it fails, fix that first.

## Coding a paper, in order

1. **Read** the paper, its code and data if released, and the figures the
   results depend on. Note what you read; it goes in `coding`.
2. **Split it into studies** by the facet test (below: "A study is a set of
   results that share every facet value").
3. **Copy `templates/source.yaml`** to `sources/<id>.yaml` and code the core
   facets of each study: every one, using `unspecified` or `not_applicable`
   rather than leaving any out.
4. **Write the claims**, one finding each, with `where`, `evidence_kind`,
   `effect_of` and `scope` where they apply, and `effect_presence` (and
   `effect_direction` where it is ordered) on every claim with `effect_of`.
5. **Link claims to questions, if you are asked to** (`links/<source id>.yaml`;
   template in `templates/links.yaml`). Linking is the question poser's
   judgement, so a coder adding a paper may stop at the claims. When linking,
   reuse a question where one fits; otherwise add a narrower one under the
   closest, with its `polarity`.
6. **Code the interpretive facets** that the linked questions `need` or
   `require`, and any the source takes a position on. Leave the rest out.
7. **Register** only the people, orgs, models and datasets the record uses.
8. **Validate and build**, then log and open a pull request (End of session).

## Coding rules

- **Code from the source, never from memory.** Open the paper, post or repo in
  this session before writing or changing a record. If you could not read it,
  do not code it.
- **Record what you read.** Fill `coding.version_read`, `read_depth` and
  `read_parts` truthfully. A machine-generated summary is `summary_only`, not
  `full_text`. If a detail sits in an appendix you did not read, say so in the
  claim's `where` or `note`.
- **Every required core facet is coded on every study.** Use `unspecified`
  when the source does not say and the design does not settle it, and
  `not_applicable` when the facet does not apply. Never leave one out to mean
  either.
- **Interpretive facets are coded when needed** (`codebook/README.md`, "Two
  tiers"): when the source states a position on the matter, when a claim links
  to a question that `needs` the facet, or when a conflict turns on it.
  Otherwise leave them out; they read as `not_yet_coded`. When you do code
  one, code it fully, with `basis` and a note.
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
- **Say which variable a claim is about.** When a claim reports the effect of
  something the study varied, name that variable in `effect_of`. Leave it off
  claims that report no such effect, and off variables the study varied only
  as a covariate or to show the result is general.
- **A conflict that differs only on task means the question is too coarse.**
  Read the two claims' conditions, then split the question or add one about
  what moderates the effect.
- **Interpretive claim facets record the source's view, not yours.** Code
  `report_source`, `origin`, `integration` and `aspect` only when the source
  argues or tests the matter, or as `unspecified` when a linked question needs
  them and the source does not settle it.
- **Split a chain into links.** "Model has disposition", "it appears at stage
  n", "dataset z causes it" and "mechanism m mediates it" are separate claims,
  each with its own evidence kind.
- **Say what each model is for.** A bare id in a study is a subject. A model
  used as a baseline is `comparison`, a grader is `judge`, a model that
  supplies training data or samples is `data_source` (long form `{id, roles,
  note}`). For seed or same-recipe variants, set `variant_of` in the registry,
  so the build can tell how closely compared models are related.
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
- **Read the paper and its code together.** Code and data released with a
  paper count as the source. Where a repository exists, read it alongside the
  paper before coding: it often settles what the paper leaves out or gets
  wrong (the exact model list, the prompt format, how a score is computed).
  Say what you read in `read_parts`; if a detail comes only from the code, say
  so in the claim's `where`. If the paper and the code disagree, record both
  and say which you followed.
- **Look at the figures.** Extracted text gives figure captions only. Download
  the PDF (`https://arxiv.org/pdf/<id>`) and read the pages that hold the
  figures a claim depends on.
  - Never state a result, a value or a model name that sits only in a figure
    you have not seen. Write the claim from the text and say in `where` that
    the values are in the figure, not read.
  - A value read off a plot is approximate. Say "read from Fig. N" in `where`
    and do not give more precision than the plot shows.
  - `read_depth` is `full_text` only if the figures were seen. Otherwise it is
    `text_only`.
- **`date` is the date of the version read.**
- **Questions.** Before adding a question, look for one that fits. If an
  existing question is close but its wording excludes this design, add a
  narrower question and give both the same `parent`, creating the parent if
  needed. Give every question with a parent its `polarity`: `inverse` when
  yes to it counts as no on the parent, `none` when it bears on the parent
  but not along its yes/no axis. A question answered by a choice rather than
  yes or no is `kind: which` with an `answer_facet`; its claims code that
  facet and take no stance. Links live in `links/`, one entry per claim and
  question; a claim can be linked to several questions.
- **Readings** (`readings/`, `design/readings.md`) are lenses, never edits.
  In this repo a reading must rest on a published source named in `sources`;
  readers keep their own readings outside it and apply them to these claims by
  id. Prefer a selector on facets; name targets only when the condition is not
  a facet.
- **Definitions** (`definitions/`, `design/definitions.md`) say what a design
  tests, in a stated sense, as logic over facets. Keep `construct` as the
  authors' label and let definitions do the testing. In this repo a definition
  rests on a published source and says, in `not_expressible`, what of that
  source's definition the facets cannot capture. Something that keeps coming
  up there belongs in `design/candidate-facets.md`.
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

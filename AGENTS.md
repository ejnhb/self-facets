# Working in this repo

Instructions for any agent maintaining self-facets: Claude sessions (Claude
Code loads this file through `CLAUDE.md`) and agents from other developers
alike. Read `README.md` for the record model and `codebook/README.md` for how
facets are coded.

## Start of session

1. Read `OPEN.md` to see what is open, and the last few merged pull requests
   to see what was done.
2. Run `python scripts/validate.py`. If it fails, fix that first.

## Coding a paper, in order

1. **Read** the paper, its code and data if released, and the figures the
   results depend on. Note what you read; it goes in `coding`, and in the
   `code` and `data` artefacts (status, commit read, how much was read).
2. **Split it into studies** by the facet test (below: "A study is a set of
   results that share every facet value"). Code only the results in scope
   (below, "Scope"), and list the rest in `coding.not_coded` with where and why.
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
  either. (A facet added after a record's last pass is the exception: it reads
  as `not_yet_coded` until that record is backfilled; see "Codebook changes".)
- **Interpretive facets are coded when needed** (`codebook/README.md`, "Two
  tiers"): when the source states a position on the matter, when a claim links
  to a question that `needs` the facet, or when a conflict turns on it.
  Otherwise leave them out; they read as `not_yet_coded`. When you do code
  one, code it fully, with `basis` and a note. Leaving them out costs little:
  the build's `question_candidates` names, for each candidate claim, the
  needed facets its study lacks (`missing_needs`), so a question with few hits
  can send its candidates back for those facets.
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
  - Two contrasts in one design are not different studies, so long as no
    claim inherits a value wrong for it. `comparison` and `varies` take
    several values. Where the contrasts differ in validation or elicitation,
    the facet test wins. In Binder et al. one design gives the effect of
    self-prediction training (before and after, validated against the
    model's own behaviour) and the self-against-cross-prediction contrast
    (validated against another model's predictions too, all trained). Kept
    together, the training claims would inherit `other_model` and the
    untrained baseline `trained`, so the record splits them (s1, s2).
  - Models that differ on a facet (a base model on raw text, a chat model
    through its template) are split only when their results are reported
    apart. When results pool or compare them, keep one study, code both
    values, and say in the note which models have which.
  - A claim that compares two studies goes in the one whose facets fit it
    best, and names the other in `compares`. The build counts it for frames
    on either study, so which one is its home matters little. Contrasts come
    in three tiers: within a study, `varies`; between two studies of one
    paper, `compares`; between papers, never in the record (a `relation`
    when one paper criticises or extends another, a reading when a critique
    applies to a kind of design, or the question layer).
  - Never infer `model_size`. Code what the paper varies: family or
    generation when sizes are not given (sizes can be matched later from the
    model registry).
- **Record the conditions.** `varies` names a variable; put the conditions
  actually used in its `levels`, or `levels: unspecified` when the source does
  not say. For `layer`, also set `layer_scale`: `index` for layer numbers,
  `fraction` for a share of the depth. When a claim holds for only some of them, say
  which in `scope.conditions`.
- **Say which variable a claim is about.** When a claim reports the effect of
  something the study varied, name that variable in `effect_of`. Leave it off
  claims that report no such effect, and off variables the study varied only
  as a covariate or to show the result is general. A result about a control
  or baseline (an uninjected control above chance, a failed manipulation
  check) takes no `effect_of`, even when it is unexplained: it is a claim of
  its own, `observed` or `measured`.
- **A conflict that differs only on task may mean the question is too
  coarse.** That is the question poser's call, not the coder's: question views
  group a question's evidence by task, so the poser can see it and split the
  question or add one about what moderates the effect.
- **Interpretive claim facets record the source's view, not yours.** Code
  `report_source`, `origin`, `integration` and `aspect` only when the source
  argues or tests the matter, or as `unspecified` when a linked question needs
  them and the source does not settle it. When the values differ in basis,
  use the per-value long form (`value: [{value, basis, where}, ...]`), so a
  question can filter on what the authors themselves argue. When the source
  rules a route out, list it under `excluded`.
- **Say which way is better.** On a claim that reports a performance measure,
  set `better: higher` (accuracy) or `better: lower` (error, loss, entropy),
  so automatic stances can turn `effect_direction` into an advantage.
  `self_vs_other` is ordered other, then self.
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
- **Say whether code and data are available.** Every record lists one
  artefact of kind `code` and one of kind `data`, each with a `status`:
  `released` (with `url`, the commit or revision read in `ref`, and `read`:
  true, false or partial), `not_released` (checked: the paper says none is
  released, or a look at the paper and the authors' pages found none), or
  `unknown` (not checked). Never leave one out to mean "none": absence is
  ambiguous. The build's `study_availability` and
  `question_evidence_availability` show, per study and per question, what
  could be re-run.
- **Read the paper and its code together.** Code and data released with a
  paper count as the source. The paper is the source of the claims; the code
  settles how it was done.
  - Pin the version: read the commit or release nearest the paper version you
    code (repositories move on after publication), and record it in `ref`.
    For a Hugging Face dataset or model, its revision.
  - Read to a checklist, not the whole repository: the exact model ids and
    variants and how they are called (API, provider, chat template); prompt
    templates and system prompts; sampling settings; how scores are computed;
    data filtering and exclusions; what each plotted figure plots. For a
    dataset, its card and a few rows; never download large files.
  - Say what you read (files, at which commit) in `read_parts` and in the
    pass entry. If a detail comes only from the code, say so in the claim's
    `where` or the study note. If the paper and the code disagree, record
    both and say which you followed.
- **Look at the figures.** Text tools (alphaXiv page content, web fetchers)
  return figure captions only, without saying the figures are missing. Run
  `python3 scripts/fetch_paper.py <id>v<n>` for the version you code: it
  downloads the PDF to `_paper/` (not committed), writes its text with page
  markers, and renders the pages that hold figures to PNG. Look at the pages
  the claims depend on, and name them in `read_parts`.
  - Never state a result, a value or a model name that sits only in a figure
    you have not seen. Write the claim from the text and say in `where` that
    the values are in the figure, not read.
  - A value read off a plot is approximate. Say "read from Fig. N" in `where`
    and do not give more precision than the plot shows.
  - `read_depth` is `full_text` when the whole text was read, appendices
    included, and every figure a claim takes a result or value from was
    viewed. List the figures not viewed in `read_parts`, and say so in the
    `where` of any claim that cites one (such a claim is written from the
    text alone). If a claim takes a result or value from a figure that was
    not viewed, `read_depth` is `text_only`.
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
  `coded_by`, `coder_model` and `read_parts` describe the first full coding.
  Every coding or later change to a record, a backfill included, adds an entry
  to `coding.passes`: date, pull request, coder and model, the codebook version,
  what the pass coded or changed, and what was read for it (or that nothing new
  was). Many instances of one model sign the same `coder_model`; the pull
  request tells them apart, and the list lets a checker confirm it is not the
  model that coded what it checks.

## Ids

- Source: `firstauthorYEAR-short-title`, and the file is `sources/<id>.yaml`.
- Study and claim: `<source id>.s1`, `<source id>.c1`, numbered in order added.
  Never renumber or reuse an id; other records may point at it.
- Person: `family-given`. Org, model, dataset: a short lowercase slug.
- Question: `q-short-description`.

## Codebook changes

Do not invent a value in a record. If the codebook lacks what you need, put
the proposed change in `OPEN.md` (and `design/candidate-facets.md` for a new
facet) for the owner to confirm, and meanwhile:

- if a question frames on that facet, code `unspecified`: a nearest value
  would be read as right and pull the study into frames it was not meant for;
- otherwise code the nearest value, and say so in the note.

The codebook is at 0.11 (owner's review, 2026-11-28). Once a change is
confirmed: edit the facet file, bump its version, and add a `CHANGELOG.md`
line. A value that is a narrower kind of another declares `broader:`, and
frames on the broader value include it. A new facet declares `since:` (the
version that adds it); records whose passes all predate it read as
`not_yet_coded` for it, validation lets them through, and the build lists
them for backfill. A new value in an existing facet cannot be caught that way,
because old records already hold some value: list in `OPEN.md` the studies to
recheck (those coded `unspecified`, or with the nearest value, on that facet).

New facets and values usually come from a question someone wants to pose.
Create them when the question is posed, and let the question's candidate list
say which old records to backfill. Bookkeeping that is not a facet (enums for
coding, artefacts, provenance) may change with a `CHANGELOG.md` line.

## Scope

The repo covers questions about a model's relation to itself: its
self-reports and self-knowledge, its self-models and personas, and the
internal states those could be about. A paper is in scope when at least one
of its results could bear on such a question. Code those results; list the
others in `coding.not_coded` with where they are and why they were left out.
Only in-scope studies press for new codebook values. The scope grows when
someone poses a question that needs it, not because a paper happens to
contain more.

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
2. Update `OPEN.md`: add what you left open and anything the owner needs to
   decide; remove what you resolved. It is rewritten, not appended to.
3. Commit on a branch and open a pull request unless told otherwise. The pull
   request description is the record of the session: what was added or
   changed, what was read, the calls you were unsure of, and what you added to
   or removed from `OPEN.md`.

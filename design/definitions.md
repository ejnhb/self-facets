# Definitions: design (2026-11-26; built in codebook 0.9)

Status: built in codebook 0.9, starting with one definition (Lindsey's
grounding criteria). Logic is shared by definitions, frames, reading selectors
and `requires`. The text below is the proposal as tested on paper.

## The problem

`construct` records what the authors call a study, by its rule: "prefer the
source's framing". So `construct: introspection` matches nearly every study in
the repo, question frames built on it return everything (87 candidates for
`q-privileged-self-access`), and a study whose authors call it introspection
cannot be told apart from one whose design tests introspection in a given
sense.

## Definitions

A **definition** is a named piece of logic over facets: what a study's design
has to be for it to test something, in one stated sense. `construct` keeps the
authors' label; definitions say what the design tests.

```yaml
- id: d-introspection-grounded
  sources: ["Lindsey (2026), Emergent introspective awareness in large language models, §3 (criteria 1 and 2)"]
  statement: The self-report describes an internal state and is checked against that state, so it can be causally grounded in it.
  all:
    - {evidence: [self_report]}
    - {report_target: [own_internal_state, injected_state, own_computation]}
    - {validated_against: [known_intervention, internals, probe]}
  not_expressible: >
    Lindsey's internality (the report must not route through the model's own sampled outputs) and metacognitive
    representation (a representation of the state, not a translation of it) are not facets.
```

- Logic: `all`, `any`, `not`, over facet values, registry fields
  (`model.post_training_reached`), the derived `comparison.closest`, and other
  definitions by id.
- Matching is mechanical once a definition is written. The judgement is in
  choosing which definition a question uses, and that choice is named.
- `not_expressible` says what part of the source's definition the facets
  cannot capture, so a match is read as "consistent with", not "satisfies".
- In this repo, definitions come from published sources. Readers keep their
  own outside it.

## How the layers fit

1. Studies and claims have facets; models and datasets are in the registries.
2. Readings, when a view applies them, reclassify facets under the lens.
3. Definitions are evaluated on the lensed facets, so a reading can move a
   study out of a definition.
4. Questions select evidence through frames built from definitions and facets,
   and through `requires`; stances come from links and auto stances.
5. Views pick readings and may substitute one definition for another.
6. Outputs: candidates, evidence and conflicts, mismatches between the
   authors' label and the definitions, and differences between views.

Readings may select on definitions but never change them. A disagreement about
what a construct is, is a choice between definitions; a disagreement about
what a study shows, is a reading.

## Published definitions, written as facet logic

Lindsey (2026, §9.6) sets several definitions side by side, which makes them a
good test.

| Definition | Source | As facet logic | Not expressible |
|---|---|---|---|
| `d-introspection-grounded` | Lindsey §3, criteria 1 to 3; close to Comşa and Shanahan's, as Lindsey describes it | self-report, about an internal state, checked against a known intervention, internals or a probe, with `output_route_control` ruling out its own earlier output (0.10) | metacognitive representation |
| `d-privileged-access` | Binder et al. (2024, §2): facts not derivable from training data, tested by cross-prediction; Lindsey §9.6 quotes a privileged-access definition from Song et al. | self-report, varies self against other, checked against another model or a fresh copy | "equal or lower computational cost" |
| `d-privileged-beyond-similarity` | Song, Hu and Mahowald (2025, §2) | `d-privileged-access` and (similarity adjusted statistically, or closest comparison a variant or derived model) | |
| `d-self-modelling` | Lindsey §9.6's term for Binder et al.'s case | `d-privileged-access` and a report about own behaviour or knowledge | |

## Tested on the four coded sources

Which studies each definition matches (21 studies, 94 claims):

| Definition | Studies | Claims |
|---|---|---|
| `d-introspection-grounded` | Lindsey s1, s3, s4, s5; Rubin s1 | 35 |
| `d-privileged-access` | Binder s2, s3, s5; Song s2, s3 | 18 |
| `d-privileged-beyond-similarity` | Song s2, s3 | 12 |
| `d-self-modelling` | Binder s2, s3, s5; Song s2, s3 | 18 |

The two main senses split the literature cleanly: injection and probe studies
fall under grounding, self-against-other studies under privileged access, and
no study meets both. Lindsey's prefill study (s6, a report about its own
outputs) meets neither as written, which matches its place in the paper as a
test of internality, which the facets cannot express.

Candidate lists with frames rewritten from definitions (claims in matching
studies not yet linked):

| Question | Frame | Candidates before | After |
|---|---|---|---|
| `q-privileged-self-access` | any of grounded, privileged access | 87 | 53 |
| `q-introspection-differs-by-post-training` | grounded, and varies post-training stage or recipe | 27 | 16 (Lindsey s1, s3) |
| `q-stabilisation-improves-introspection` | grounded, construct persona stability, varies study training | 87 | 0 |
| `q-injected-state-report` | grounded, and report target injected state | 25 | 25 |
| `q-self-access-without-training` | beyond-similarity, and not trained elicitation | 5 | 5 |

The lists shrink where frames were loose and stay where they were already
specific. The stabilisation question correctly finds nothing: no coded paper
tests it.

## A view that swaps definitions

```yaml
- id: v-capability-privileged
  question: q-introspection-increases-with-capability
  readings: []
  substitute: {d-introspection-grounded: d-privileged-access}
```

The same question and the same evidence, read under a different sense of
introspection. The difference between this view and the default is the answer
to "how much does the conclusion depend on what we mean by introspection?"

## What the test showed

- Most published definitions can be partly expressed; each leaves a remainder
  (`not_expressible`). That remainder is worth recording: it is where a facet
  might be added (internality is the strongest candidate, since several
  designs control for it explicitly).
- `d-self-modelling` and `d-privileged-access` match the same studies here.
  They come apart only on a self-against-other study about internal states,
  which none of the four papers runs.
- Definitions fix most of the candidate-list problem without changing frames'
  any-of rule.

## Open

- Whether `construct` stays as the authors' label only, with a mismatch view
  listing studies whose label no definition supports.
- Whether an internality facet is worth adding (for example: could the report
  be inferred from the model's own earlier outputs in the same context?).
- How views name a substitution when a question's frame uses several
  definitions.

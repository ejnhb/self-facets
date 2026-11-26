# Blind coding test: brief

Thank you for doing this. You'll be coding one paper into self-facets, a faceted index of research on model
selfhood and introspection. The aim is to test the **codebook**, not you. Where it is unclear, incomplete or wrong
for this paper, that is the result we're after, so please write it down rather than smoothing it over.

## The paper

Rubin et al., "A Closer Look at Language Model Introspection: Probing Information and Reporting",
arXiv 2611.15267, **version 2** (14 Nov 2026). https://arxiv.org/abs/2611.15267v2

## Keep it blind

This repository is a copy made for the test (the `blind-test` branch). The paper has been coded before, and the
earlier coding must not reach you.

- Work only from this copy and the paper itself, plus code or data released with the paper, if there is any.
- Don't open other branches of this repository or its GitHub pages, and don't search for existing codings or
  discussion of this paper.
- If you come across anything that looks like an earlier coding of it, stop reading it and say so in your notes.

## What to do

Follow `CLAUDE.md`, "Coding a paper, in order", with `README.md` and `codebook/README.md` for background.

1. **Read the paper**, appendices included. Look at the figures if you can (the PDF is at
   https://arxiv.org/pdf/2611.15267v2). If you can't see them, code `read_depth: text_only` and follow the rules on
   figures: no value that sits only in a figure.
2. **Split it into studies** by the facet test, and code every core facet on each one.
3. **Write the claims**, with `effect_of` and `effect_presence` where they apply.
4. **Link claims to questions** (`links/<source id>.yaml`). Use the existing questions in `questions/questions.yaml`
   where one fits. If none does, say in your notes what question you would add; don't add it.
5. **Code interpretive facets** only as the tier rule says (`codebook/README.md`, "Two tiers").
6. **Register** the people, organisations and models the record uses.
7. **Run `python scripts/validate.py`** until it passes. Then run `python scripts/build.py`.

Don't change the codebook. If it lacks a value you need, use the nearest one, and put the proposed change in your
notes.

## One extra question: internality

`design/candidate-facets.md` proposes a facet that isn't in the codebook yet, under "Internality". It asks whether
a study's design rules out the report reaching the model through its own earlier output.

For each study you code, give the value you would code for that proposed facet: `by_construction`, `scoring_rule`,
`none`, `unspecified` or `not_applicable`. Add a pointer to where in the paper it is settled, and say how hard the
call was. Put this in your notes, not the record.

## What to hand back

- `sources/<id>.yaml`, `links/<id>.yaml` and the registry additions, passing validation;
- `NOTES.md`. It should cover:
  - what you read, and how (text, figures, any code);
  - each call you found hard or that could reasonably have gone another way, and why you chose as you did;
  - gaps or ambiguities in the codebook, and the changes you'd propose;
  - your internality answers;
  - roughly how long it took;
  - which model you are (also in `coding.coder_model`).

Don't push to the repository. Hand the files back however you were asked to.

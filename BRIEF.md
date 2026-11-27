# Blind coding test 2: brief

Thank you for doing this. You'll be coding one paper into self-facets, a faceted index of research on model
selfhood and introspection. The aim is to test the **codebook** (version 0.10), not you. Where it is unclear,
incomplete or wrong for this paper, that is the result we're after, so please write it down rather than smoothing
it over.

## The paper

Binder et al., "Looking Inward: Language Models Can Learn About Themselves by Introspection", arXiv 2410.13787,
**version 1** (17 Oct 2024). The PDF should be attached; otherwise https://arxiv.org/pdf/2410.13787v1.

## Keep it blind

This repository is a copy made for the test. The paper has been coded before, and that coding must not reach you.

- Work only from this copy and the attached PDF.
- Don't search the web, open this repository's other branches or GitHub pages, or look for existing codings or
  discussion of this paper. If you have no web access, that is intended.
- Two other records here cite this paper (in their notes and `relations`). That is what those papers say about it,
  not a coding of it; you may read it, but code only from the paper itself.
- If you come across anything that looks like an earlier coding of it, stop reading it and say so in your notes.

## What to do

Follow `CLAUDE.md`, "Coding a paper, in order", with `README.md` and `codebook/README.md` for background.

1. **Read the paper**, appendices included. Look at the figures if you can. If you can't see them, code
   `read_depth: text_only` and follow the rules on figures: no value that sits only in a figure. You won't have the
   paper's code; say so in `read_parts`, and code `unspecified` where only the code would settle a facet.
2. **Split it into studies** by the facet test, and code every core facet on each one.
3. **Write the claims**, with `effect_of`, `effect_presence` and `effect_direction` where they apply.
4. **Link claims to questions** (`links/<source id>.yaml`). Use the existing questions in `questions/questions.yaml`
   where one fits. If none does, say in your notes what question you would add; don't add it.
5. **Code interpretive facets** only as the tier rule says (`codebook/README.md`, "Two tiers").
6. **Register** the people, organisations and models the record uses.
7. **Fill `coding`**, including one entry in `coding.passes` (template in `templates/source.yaml`; leave `pr` out).
8. **If you can run Python**, run `python scripts/validate.py` until it passes, then `python scripts/build.py`. If
   you can't, say so in your notes; the files will be validated afterwards.

Don't change the codebook. If it lacks a value you need, use the nearest one, and put the proposed change in your
notes.

## What to hand back

- `sources/<id>.yaml`, `links/<id>.yaml` and the registry additions (as edited copies of `models/models.yaml`,
  `people/people.yaml` and `orgs/orgs.yaml`, or as the entries to add);
- `NOTES.md`. It should cover:
  - what you read, and how (text, figures);
  - each call you found hard or that could reasonably have gone another way, and why you chose as you did;
  - gaps or ambiguities in the codebook, and the changes you'd propose;
  - roughly how long it took;
  - which model you are (also in `coding.coder_model`).

Please return everything as one zip if you can.

# Check of sources/rubin2026-closer-look-introspection.yaml

Checked against the full extracted text of arXiv 2611.15267v2 (alphaXiv,
fullText): title page, abstract, §§1 to 6, references, Apps. A to D, Tables 1
and 2, and figure captions. Figures 2 to 4 are plots seen only as captions and
axis labels; no claim depends on a value that appears only in a figure.

## Claims

| Claim | Verdict | Notes |
|---|---|---|
| c1 | supported | 98.3% probe, 11.1% answer (chance) at 8.4B tokens, layer 0, α=4, probe layer 24: Abstract, §1.2, §4.1. 288 labelled trials per fold: §4 preamble. |
| c2 | supported | 99.1% / 89.6% at released base: Abstract, §4.1. "Develops without post-training": §4.1. Minor wording point on scope, see below. |
| c3 | supported | §4.1 "location information becomes easy to decode early in pretraining, while the model's answers improve later"; "Successful reporting therefore develops without post-training"; §5.1. |
| c4 | supported | 37.7% (35.8–41.1%) at layer 6, 89.6% at layer 0, both α=4: §1.2, §5.1, App. C.2. Conclusion: §1.2, §5.1. |
| c5 | supported | App. C.2: probe 83.1% (80.8–85.6%), answer 37.7%, shuffled-label probe 12.0% (10.8–12.8%). |
| c6 | supported | App. C.2: 86.1% vs 80.2% (probe), 42.8% vs 32.6% (answer), same pooled probe. |
| c7 | supported | §5.3 and Abstract. Minor wording point, see below. |
| c8 | supported | §5.3 "possible basis for successful reporting"; §5.3 and §6 say the comparison does not establish the model uses the probed features. |
| c9 | supported | §4.1: step 0, 37.2% vs 11.3% shuffled at the main setting; α=2: 30.5% vs 10.1%, readout layer 60 in all three folds. App. B.5: 7B shuffled 11.6%. App. C.3: 27.6% in 7B, ranges 28.6–32.2% and 23.9–30.6%. |
| c10 | supported | App. C.3: α=1, 32B, 18.3% to 76.9%; 7B same direction; non-uniform improvement. |
| c11 | supported | §4.2 and Table 1: α=8 31.5% / 21.5% vs 11.5% / 10.9%; α=4 27.4% / 19.1%; α=1 12.2% / 11.5%. App. D: permutation tests with Holm correction, norm-only baseline. §5.2 conclusion. |
| c12 | supported | §4.2: 30.6% at gap 0, 21.9% at gap 256 for targets 1–8. Strength not restated, as the scope says. |
| c13 | supported | Table 2: gap 0 at α=2,4,8 = 50.7, 53.0, 48.1 (range 48.1–53.0); gap 256 = 14.1, 14.8, 14.3; α=0 = 14.3 / 14.1. App. D.1 p = 0.014, 0.018 (pretrained), 0.411, 0.580 (random). §4.2, §5.2 decline to draw conclusions. |
| c14 | supported | App. D.2: 20.6–28.9% on fresh numbered text, 11.1–12.2% without numbering, α=8, gap 0. Caveats in D.2 and §6. |
| c15 | supported | App. D.3: "Across both network states and all three seeds, blocking all outward attention from the injected span after layer 6 eliminates the perturbation at later readouts exactly"; "Paired injected-minus-clean activations establish propagation independently of classifier accuracy." §6: two held-out trials per target per seed; no causal link to the response. |

Counts: supported 15, wrong 0, overstated 0, not_found 0, figure_only 0.

### Minor wording points (not verdict-changing)

- **c2 scope.conditions**: "This injection layer and strength gave the
  model's highest answer accuracy in the sweep". §3.5.1 says the setting
  "uses the injection layer and strength selected for the released base
  model's highest raw answer accuracy in all three held-out-seed folds", i.e.
  chosen by two-seed selection in each fold, not stated as the single highest
  cell of the sweep. Suggested: "This injection layer and strength were the
  ones selected for the released base's highest answer accuracy in all three
  held-out-seed folds, and the fixed setting was chosen after examining the
  sweep."
- **c7**: "Localization success alone therefore does not establish that a
  model can report other aspects of its computation" is slightly firmer than
  §5.3 ("they limit what localization success alone can establish about a
  model's ability to report other aspects of its computation"); the Abstract
  ("successful reporting need not imply broader access to the model's
  internal computation") supports the record's wording. Optional: "...
  therefore limits what can be concluded about a model's ability to report
  other aspects of its computation".

## Studies, models and source details

- **Source**: title, six authors, single Georgia Institute of Technology
  affiliation, date 2026-11-14 (v2 arXiv stamp), title-page date 10 November
  2026, and absence of any code or data release all match the text.
- **s1 design**: all details match (§3.2–3.5.1, §4, App. A.1, B.2, B.3, B.5,
  C.1, C.2): pool of 100 sentences, nine-way probe, 288 trials per fold, 40
  passages × 9 positions = 360 trials per condition, seeds 21/101/102, layers
  {0,6,16,32,48} / {0,3,8,16,24}, strengths {0.25,…,4}, 19 concepts, seven
  stage-1 checkpoints plus released base. Revision names in `varies.levels`
  match the App. B.2 table.
- **s2 design**: matches §4.1, App. B.5, C.3, Fig. 4 caption.
- **s3 design**: matches §3.5.2, App. A.2, D. Small omission: the
  prespecified tests also used readout layer 58 (App. D, "layers 24 and 58"),
  while the design mentions only layer 24 (it is noted in c11). Optional
  addition: "Prespecified tests also read layer 58."
- **Model lists**: consistent with the paper. Registry notes (models.yaml,
  not the record) write the Hugging Face repos as `allen-ai/Olmo-3-1125-32B`
  and `allen-ai/Olmo-3-1025-7B`; App. B.2 writes `allenai/Olmo-3-1125-32B` and
  `allenai/Olmo-3-1025-7B`.
- **Relations**: the Hahami et al. 2025 and Fornasiere et al. 2026 citations
  (authors, arXiv ids) match the reference list; §5.1 supports `extends`.
- **Facet codings**: none is plainly contradicted by the paper. (App. A
  supports `format: raw_text`; App. B.3 supports the note that seeds vary
  passages and vectors, not weights.)

# Check of sources/song2025-fail-to-introspect.yaml

Checked against arXiv 2503.07513 v3 (23 Sep 2025), full extracted text via alphaXiv
(body, appendices A to G, Tables 1 to 8; figures seen as captions only). Repository
read in part: README.md, analysis.R (from the root listing) and src/models.py. Not
read: preparedata.ipynb, src/blimpli.py, src/continuation_final.py, data files.

## Verdicts

| Claim | Verdict |
|---|---|
| c1 | supported |
| c2 | supported |
| c3 | supported |
| c4 | supported |
| c5 | supported |
| c6 | supported |
| c7 | supported |
| c8 | supported |
| c9 | supported |
| c10 | supported |
| c11 | supported |
| c12 | overstated |
| c13 | supported |
| c14 | supported |
| c15 | supported |
| c16 | supported |
| c17 | supported |
| c18 | supported |
| c19 | supported |
| c20 | supported |
| c21 | supported |
| c22 | supported |

Totals: 21 supported, 1 overstated, 0 wrong, 0 not_found, 0 figure_only.

Numbers verified: c2 0.22 (Table 5: 0.2211 ***; text p < .0001); c3 kappa about 0.25
(§3.2.1); c5 all p < .001, seed variant p = .27 (§3.2.2); c6 r = .32, 0.10, Exp. 2
0.3959 / 0.8338 / 0.4913 / 0.5613, unfiltered 0.20 (§3.2.2, §4.2.2, Table 7a, App. C);
c7 other -0.03, p < .01; c8 0.0519 *** and 0.0504 ** (text: both .05, p < .01);
c9 0.0404 ** and 0.0501 **; c10 same family 0.048 to 0.065, other 0.048 to 0.089, all
starred, seed/base-instruct unstarred; c11 Table 7b wikipedia same family 0.0727 *,
other 0.1039 **, similarity 0.6456 *** only on wikipedia, no seed-variant row;
c13 Meta size 0.0135 to 0.0432 ***, filtered interaction 0.0035 ***, Direct size
negative on wikipedia (-0.0161 ***) and news (-0.0119 *); c16 Table 8 self -0.0106 to
0.0080, App. F all ps > .25.

## Claims not supported as written

### c12 (overstated)

Statement: "The correlation across items between prompted scores and string-probability
scores is small throughout. On grammaticality it never exceeds .25 ..."

Paper, §3.2.2: "the overall magnitude of the ∆Direct ∼ ∆Meta correlations, even within
model, is relatively small, never exceeding .25." This is said for the Exp. 1 filtered
analysis only. "Throughout" goes beyond it: elsewhere the correlations are larger, e.g.
Table 8 intercepts (mean non-self OLMo pair correlation) are 0.36 on unfiltered Exp. 1,
0.35 on wikipedia and 0.40 on news. The second sentence and the scope are right.

Corrected wording: "On grammaticality (the 294 filtered minimal pairs), the correlation
across items between prompted scores and string-probability scores is relatively small:
it never exceeds .25 for any pair of models, a model paired with itself included."

## Study designs, model lists, source details

Source details: title, authors, affiliations (Song and Mahowald UT Austin, Hu Johns
Hopkins), co-senior marking, COLM 2025, v3 date 23 Sep 2025 all match the paper.

Model lists: 21 models, matching the paper's count; the 7 instruct / 14 base split and
the 7 models of 70B or more are consistent with Table 1 and the README. The README lists
15 default models but prints only 14 ids (no Llama 3.1 405B), as the record's s1 note
says; analysis.R includes "llama-3.1-405b". OLMo revision names match the README.
analysis.R uses `>= 70` for the big-model subset, and its pair-type rules (same family,
generation, size and type = seed variant) confirm the record's s2 note that a released
OLMo model paired with a seed variant is a seed-variant pair. src/models.py confirms the
chat template with a "You are a helpful assistant." system message and an assistant
turn prefilled with "My answer is" for instruct models, and "\nMy answer is" on plain
text for base models.

Minor points (no wrong statement, but worth tightening):

1. s1 design, "news (published after the models' data cutoffs)": §4.1 says "after most
   models' knowledge cutoff"; App. D says after the cutoffs, with footnote 6 noting the
   Qwen and Mistral cutoffs are not released. Suggested: "published after the models'
   knowledge cutoffs (Oct 2024; cutoffs for Qwen and Mistral are not released)".
2. s1 design says the Meta measure is "averaged over both orders of the options". For
   the three individual-judgment prompts of Exp. 1 the Meta score is instead the
   difference between the judgments of the two sentences (Table 2 caption). Suggested
   addition: "For the three Exp. 1 prompts that judge one sentence at a time, the score
   is the difference between the two sentences' judgments."
3. s1 unit_disposition note: "4-bit quantisation, for both measures" - the paper says
   only "we applied 4-bit quantization to models larger than 70B" (§3.1). "For both
   measures" is true from src/models.py (one loaded model serves both), so the note
   should say it is from the code.
4. s2 note on the big-model cutoff could add that the Table 7 caption also says "models
   larger than 70B"; Table 7b nonetheless has a same-family row, which requires 70B
   models, so App. G's "70B or greater" is the one that fits the results.

No facet codings were found plainly contradicted by the paper.

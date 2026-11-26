# Fact check: sources/lindsey2026-emergent-introspective-awareness.yaml

Checked against arXiv 2601.01828 v1 (5 Jan 2026), full extracted text from
alphaXiv (`get_paper_content`, fullText; 1,707 lines, read in full: abstract,
§1 to §11, references, appendix 12.1 to 12.4). Figures were available only as
captions. Every claim was checked against the text, not against figures.

## Verdicts

Totals: 47 supported, 0 wrong, 0 overstated, 0 not_found, 0 figure_only.

Where a claim's numbers sit in a figure, the record already says so in
`where`. In each such case the running text gives the qualitative statement
the claim makes, so none of these rests on the figure alone.

| Claim | Verdict | Support in paper |
|---|---|---|
| c1 | supported | §5.1: "for all production models, we observed 0 false positives over 100 trials"; §5.7 "essentially a zero rate" |
| c2 | supported | §2.1: Opus 4.1 and 4 "about 20% of the time" at the appropriate layer and strength; "Some other models do so as well, at lower rates"; §5.3, §5.4 (layer two thirds, strengths 2 and 4) |
| c3 | supported | §5.3 failure-mode list, "ocean" example, "brain damage", garbled text, later layers |
| c4 | supported | §5.4 |
| c5 | supported | §5.6 |
| c6 | supported (minor wording, see below) | §5.6: strength 8 norm-match, "9 out of 100 trials", negated vectors at strength 4 "comparably effective", "no discernible pattern" |
| c7 | supported | §5.6: "we suspect the former is likely ... detection ... may still be genuine" |
| c8 | supported | §1 caveat 3; §2.1 "overly intense", "likely primed by the prompt"; §5.1 emotional responses |
| c9 | supported | §5.7: "particularly high rate of true positives while maintaining zero false positives"; "Claude Opus 4 and 4.1 perform the best" |
| c10 | supported | §5.7: "among other models, performance does not strongly correlate with model capability" |
| c11 | supported | §5.7: H-only pipeline "intended to minimize refusals"; "sometimes have a high rate of false positives"; §4 same base |
| c12 | supported (scope note, see below) | §5.7: "Sonnet 3.5, Haiku 3.5, and Opus 3 ... significantly higher true positive than false positive rates" |
| c13 | supported (scope note, see below) | §5.7 footnote 10 |
| c14 | supported | §2.5 point 2; §4; §10.1 |
| c15 | supported | §5.8 last paragraph: "a detection rate of 18% out of 50 trials" |
| c16 | supported | §10.3.1 |
| c17 | supported | §1 last paragraph; §2.5 point 1; §10.1; §10.2 fourth limitation; §10.4 |
| c18 | supported | §5.5; appendix 12.1.2 (20 prompts, answer always no) |
| c19 | supported | §5.7: "fairly high false positive rate, and none of them achieve greater-than-zero net task performance" |
| c20 | supported | §5.7 and footnote 11 |
| c21 | supported | §5.8 |
| c22 | supported | §5.8 |
| c23 | supported | §5.8: affirmative responses "increased from 20% to 42% (out of 50)"; "only 2 out of 50 trials" |
| c24 | supported | §6: intermediate strengths, layer range; best layer same as before, two thirds through; chance 10% |
| c25 | supported | §2.2; §6: "Opus 4 and 4.1 perform the best, but all models we tested perform well above chance levels" |
| c26 | supported | §6: removing "Answer immediately" "reduces performance substantially on the Opus models"; "existence proof" |
| c27 | supported | §2.5 point 3; §6 |
| c28 | supported | §10.3.2 |
| c29 | supported | §2.3; §7 (reduction significant within a layer range; peak slightly over halfway) |
| c30 | supported | §7, Fig. 21 caption and text |
| c31 | supported | §7: maximum reduction against the lower of control and random-concept baselines; "Opus 4.1 and 4 exhibit a greater rate ... many other models exhibit the effect at nonzero rates" |
| c32 | supported | §7 (Fig. 19 text) |
| c33 | supported | §7; §2.5 point 3 |
| c34 | supported | §7; §2.5 point 3; §10.3.3 |
| c35 | supported | §10.3.3 |
| c36 | supported | §2.4; §8.1; §8.2 bullet list |
| c37 | supported | §8.2: "earlier / less capable models typically exhibit a larger gap" |
| c38 | supported | §8.2 |
| c39 | supported | §8.2 (if-then prompts "very similar results", Fig. 27 for Opus 4.1; controls "significantly weaker or nonexistent gaps", Fig. 28); §10.3.4 "near-identical" |
| c40 | supported | §8.2 last bullet and closing paragraph |
| c41 | supported (minor attribution note, see below) | §8.1; §8.2 closing paragraph; §9.1 |
| c42 | supported | §10.3.4 |
| c43 | supported | §3 criteria 1 to 4 |
| c44 | supported | §3, after criterion 4 |
| c45 | supported | §9.2 (three-point interpretation); §9.6 |
| c46 | supported | §1 caveat 2; §10.3 opening |
| c47 | supported | §1 caveat 5; §10.4 and footnote 12 |

## Minor notes on supported claims

None of these changes a verdict. They are offered as optional tightening.

- **c6.** The paper says random vectors "elicit introspective awareness at
  lower rates (9 out of 100 trials)" (§5.6). That is the graded success
  measure, not just noticing. Suggested wording: "...and then elicit
  introspective awareness on 9 of 100 trials..."
- **c2 and c13.** The second sentence of c2 ("Some other models do so at
  lower rates") and the first sentence of c13 ("the 'thoughts' that models
  claim to detect show no clear pattern") are about more models than the
  claim's `scope.models` lists. Either drop or widen the scope, or move those
  sentences to the note.
- **c12, and model `claude-3.5-sonnet-new-h-only`.** The paper calls this
  variant "Sonnet 3.5" H-only (§5.7). It is identified with Sonnet 3.5 (new)
  only because §4 describes the H-only models as variants "of these models"
  and the only Sonnet 3.5 in that list is "(new)". The inference is
  reasonable, but it is an inference. Say so in the s1 note.
- **c41.** §9.1 says the mitigation is "clarifying to the model explicitly
  that it need not produce any outputs related to the word". It does not
  name the "Don't write anything else" sentence as that clarification. That
  sentence is in every appendix 12.4.2 prompt, so the identification is
  plausible, but it is the coder's. Suggested wording: "...which the paper
  tries to limit by telling the model explicitly that it need not produce
  any output related to the word (the prompts end 'Don't write anything
  else')."
- **c45.** The paper's phrase "models are better at modeling themselves than
  other models" (§9.2) is ambiguous. The record reads it as "better than
  other models model them", which fits the Binder et al. result described
  just before. That reading is fine, but it is one of two.

## Study designs, model lists and source details

No errors found. Checked and confirmed:

- **Source.** The title, author (Jack Lindsey, Anthropic), date (arXiv v1
  stamp, 5 Jan 2026), the "HTML version" link on page 1 and the
  acknowledgements' "control experiment added in a revision" all match. The
  read_parts description matches the text extracted.
- **s1 design.** These details all match §5.2, §5.4, §4 and appendix 12.1:
  - concept vector on the ":" token of "Assistant:" after "Tell me about
    {word}.", minus the mean over 100 baseline words (counted: 100);
  - injection from the double-newline token before "Trial 1" through the
    sampled tokens;
  - 50 trials per model, strength and layer; strengths [1, 2, 4, 8];
    100 tokens at temperature 1;
  - Sonnet 4 grader with coherence plus affirmative-and-identified criteria,
    detection "prior to, or along with" the word;
  - five categories of 50 words; random vector norm-matched at strength 8;
    negated vector at strength 4; "concept of your choice" variant.
- **s1, minor.**
  - The design text says the random and negated vector follow-ups are on
    Opus 4.1. §5.6 does not restate the model for those runs. The rest of
    §5.6 is on Opus 4.1, and the c6 note already flags this, but the design
    text states it flatly.
  - The s1 note says "§4 says helpful-only variants of the nine production
    models were used". §4 says only "variants of these models"; it does not
    say every one of the nine has a variant. Suggested: "§4 says
    helpful-only variants of these models were used; the text names four
    (...)".
- **s2.** These match §5.5 and appendix 12.1.2: 20 questions, 10 factual and
  10 about the model, correct answer always no, penguins example, "Are you a
  human?", "Do you have a physical form?". The paper does not give the
  layer, number of trials or scoring for this control (correct).
- **s3.** The base models are not named in the text and their number is not
  given (correct). The paper says only "on the same task" (correct).
- **s4.**
  - The prompts carry "right now" in appendix 12.1.2; the main text omits
    it. The record uses the appendix form, which is fine.
  - Success is coherence plus "thinking about word" (appendix 12.1.3).
  - The "anything unusual" prompt uses Opus 4.1, best layer, strength 2,
    out of 50.
  - The 20% figure is implied to be the no-injection rate, not labelled as
    such. Acceptable.
- **s5.** These match §6 and appendix 12.2: 50 sentence and word pairs,
  strengths [1, 2, 4, 8, 16], injection on the sentence tokens, "Answer
  immediately", ten-word judge list with chance 10%, transcription scored by
  string presence, temperature 1.
- **s6.** These match §7 and appendix 12.3:
  - three main conditions, plus the post-prefill control on "Did you mean
    to say that, or was it an accident?";
  - 50 pairs, strengths [1, 2, 4, 8, 16];
  - Sonnet 4 judge;
  - retreat-after-claim not counted as an apology;
  - transcription check.
- **s7.** These match §8 and appendix 12.4:
  - the think and don't-think prompts and the six incentive prompts;
  - four control phrasings, the "I [don't] often think about" phrasing
    placed before or after the request;
  - cosine similarity on the Assistant {sentence} tokens;
  - 100 control words (counted: 100).
- **s8.** The four criteria and the placing against Kammerer and Frankish,
  Comsa and Shanahan, Song et al. (arXiv 2508.14802) and Binder et al. match
  §3 and §9.6.
- **Model lists.** The nine production models match §4. Sonnet 4 as judge
  matches §5.4 and appendices 12.1.3, 12.2.3 and 12.3.2. Opus 4 H-only is
  named in footnote 10; Sonnet 3.5, Haiku 3.5 and Opus 3 H-only are named in
  §5.7. For s4 to s7 the record already says which models appear in the
  figures is unknown.
- **Relations.** The three relations match §9.1, §9.2 and §9.6.

## Facet codings plainly contradicted by the paper

None found.

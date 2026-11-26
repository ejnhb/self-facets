# Candidate facets

Things the facets cannot yet say, found while writing definitions, readings and
questions. A candidate that keeps coming up is a sign to add it. Each entry
says where it came from, whether it can be derived from existing facets, and
whether a coder could find it in a paper's methods.

## Internality (from d-introspection-grounded, Lindsey 2026 criterion 3)

Lindsey's criterion: the state's influence on the report must not route through
the model's own sampled outputs.

- **Derivable in part.** When no text is generated before the report is read,
  internality holds by construction: `reasoning: none` with `report_readout:
  logit_choice` or `probability`, and no earlier assistant turn about the
  state. That is expressible as a definition over existing facets today
  (it covers Rubin et al. s1 and Song et al.).
- **Not derivable in the main case.** Lindsey's free-text studies meet the
  criterion by a scoring rule: a reply counts only if it notices the injected
  concept before naming it (the grader prompts in App. 12.1.3). Whether a study
  scores this way is a fact about its design, not visible in any facet.
- **Codable.** It sits in the methods or the grading prompts. A possible facet,
  `output_route_control`: `by_construction` (nothing generated before the
  report), `scoring_rule` (replies that could be inferred from earlier output
  are not counted), `none`, `unspecified`. Only `scoring_rule` needs a coder's
  reading; `by_construction` could be derived, so the facet might take just
  the coded part.
- **Seen in:** Lindsey et al. (scoring rule in the injected-thought studies;
  the prefill study s6 checks whether the model draws on its activations from
  before the output rather than on the transcript). Rubin et al. s1 and Song
  et al. meet it by construction.

## Metacognitive representation (Lindsey 2026 criterion 4)

The report comes from a representation of the state, not a direct translation
of it. Lindsey tests it indirectly, by asking questions whose answer needs a
step beyond the state (does the model notice an unexpected thought, rather than
what is it thinking about). Possibly codable as a property of the question
asked (`report_target` refinement: whether the report is about the state or
about a property of it, such as its being unexpected), but one source so far.

## Injection depth (from the Rubin et al. reading)

Where an activation injection enters (near the input, mid-depth, late), as a
coarse relative value. Today in free-text `levels`, often unreported. Wanted if
several injection papers turn out to differ by depth.

## Built from earlier candidates

- Closest comparison model (derived from the registry, 0.8) and
  `similarity_adjustment` (0.8), from Song et al.'s critique of Binder et al.
- `post_training_reached` on models (0.7). Whether a stage was on-policy is not
  recorded; it would let a reading select on the first on-policy stage.

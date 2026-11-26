#!/usr/bin/env python3
"""Check every record against the codebook and against each other.

Usage: python scripts/validate.py
Exits 0 if clean, 1 if there are errors.
"""

import sys

from _load import (
    LIGHT_REQUIRED,
    LONG_FORM_KEYS,
    NOT_YET_CODED,
    SPECIAL,
    as_list,
    facet_entry,
    load_codebook,
    load_list_dir,
    load_sources,
    model_ref,
)


class Report:
    def __init__(self):
        self.errors = []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")


def check_enum(rep, where, field, value, enums, name, required=True):
    if value is None:
        if required:
            rep.err(where, f"missing {field}")
        return
    if value not in enums[name]:
        rep.err(where, f"{field} '{value}' is not in codebook enum {name}")


def index(rep, items, kind):
    """Build id -> record, reporting duplicates and missing ids."""
    out = {}
    for path, item in items:
        if not isinstance(item, dict) or not item.get("id"):
            rep.err(path, f"{kind} entry with no id")
            continue
        if item["id"] in out:
            rep.err(path, f"duplicate {kind} id '{item['id']}'")
        out[item["id"]] = item
    return out


def validate():
    rep = Report()
    facets, enums = load_codebook()

    for name, facet in facets.items():
        where = f"codebook/{name}.yaml"
        if facet.get("applies_to") not in ("study", "claim"):
            rep.err(where, "applies_to must be study or claim")
        if facet.get("cardinality") not in ("one", "many"):
            rep.err(where, "cardinality must be one or many")
        if facet.get("tier") not in ("core", "interpretive"):
            rep.err(where, "tier must be core or interpretive")
        if facet.get("tier") == "interpretive" and facet.get("required"):
            rep.err(where, "an interpretive facet is coded when needed, so it cannot be required")
        for value, body in (facet.get("values") or {}).items():
            if not isinstance(body, dict) or not body.get("definition"):
                rep.err(where, f"value '{value}' has no definition")
            if value in SPECIAL or value == NOT_YET_CODED:
                rep.err(where, f"'{value}' is a special value and must not be redefined")
            families = facet.get("families")
            if families and isinstance(body, dict) and body.get("family") not in families:
                rep.err(where, f"value '{value}' needs a family from {sorted(families)}")

    orgs = index(rep, load_list_dir("orgs"), "org")
    people = index(rep, load_list_dir("people"), "person")
    datasets = index(rep, load_list_dir("datasets"), "dataset")
    models = index(rep, load_list_dir("models"), "model")
    questions = index(rep, load_list_dir("questions"), "question")

    for oid, org in orgs.items():
        check_enum(rep, f"org {oid}", "kind", org.get("kind"), enums, "org_kind")

    for did, ds in datasets.items():
        for comp in as_list(ds.get("components")):
            if comp not in datasets:
                rep.err(f"dataset {did}", f"component '{comp}' is not a dataset")

    for qid, q in questions.items():
        kind = q.get("kind", "yesno")
        if kind not in ("yesno", "which"):
            rep.err(f"question {qid}", f"kind '{kind}' must be yesno or which")
        if kind == "which":
            name = q.get("answer_facet")
            if name not in facets:
                rep.err(f"question {qid}", f"a which-question needs answer_facet naming a facet (got '{name}')")
            if "polarity" in q:
                rep.err(f"question {qid}", "a which-question has no polarity: its claims take no stance")
        elif "answer_facet" in q:
            rep.err(f"question {qid}", "answer_facet is only for kind: which")
        polarity = q.get("polarity", "direct")
        if polarity not in ("direct", "inverse", "none"):
            rep.err(f"question {qid}", f"polarity '{polarity}' must be direct, inverse or none")
        if "polarity" in q and not q.get("parent"):
            rep.err(f"question {qid}", "polarity says how a question points relative to its parent, so it needs a parent")
        if q.get("parent") in questions and questions[q["parent"]].get("kind") == "which" and kind != "which":
            rep.err(f"question {qid}", "a yes/no question cannot sit under a which-question")
        for name in as_list(q.get("needs")):
            if name not in facets:
                rep.err(f"question {qid}", f"needs '{name}', which is not a facet")
            elif facets[name].get("tier") != "interpretive":
                rep.err(f"question {qid}", f"needs '{name}', a core facet, which every record codes anyway")
        parent = q.get("parent")
        if parent is not None and parent not in questions:
            rep.err(f"question {qid}", f"parent '{parent}' is not a question")
        seen, cur = {qid}, parent
        while cur in questions:
            if cur in seen:
                rep.err(f"question {qid}", "parent chain loops")
                break
            seen.add(cur)
            cur = questions[cur].get("parent")

    for mid, model in models.items():
        where = f"model {mid}"
        if model.get("developer") not in orgs:
            rep.err(where, f"developer '{model.get('developer')}' is not an org")
        for parent in as_list(model.get("derived_from")):
            if parent not in models:
                rep.err(where, f"derived_from '{parent}' is not a model")
        stage = model.get("stage")
        if stage is not None:
            for method in as_list(stage.get("methods")):
                check_enum(rep, where, "stage method", method, enums, "stage_method")
            check_enum(rep, where, "stage disclosure", stage.get("disclosure"), enums, "disclosure")
            for ds in as_list(stage.get("datasets")):
                if ds not in datasets:
                    rep.err(where, f"stage dataset '{ds}' is not a dataset")

    study_facets = {n: f for n, f in facets.items() if f["applies_to"] == "study"}
    claim_facets = {n: f for n, f in facets.items() if f["applies_to"] == "claim"}

    source_ids, study_ids, claim_ids = set(), set(), set()
    all_relations = []

    for path, src in load_sources():
        sid = src.get("id")
        if not sid:
            rep.err(path, "source has no id")
            continue
        if path.stem != sid:
            rep.err(path, f"file name must match id '{sid}'")
        if sid in source_ids:
            rep.err(path, f"duplicate source id '{sid}'")
        source_ids.add(sid)

        if not src.get("title"):
            rep.err(sid, "missing title")

        for i, author in enumerate(as_list(src.get("authors")), 1):
            if author.get("person") not in people:
                rep.err(sid, f"author {i}: '{author.get('person')}' is not in people/")
            for org in as_list(author.get("orgs")):
                if org not in orgs:
                    rep.err(sid, f"author {i}: org '{org}' is not in orgs/")

        if not as_list(src.get("artefacts")):
            rep.err(sid, "a source needs at least one artefact")
        for i, art in enumerate(as_list(src.get("artefacts")), 1):
            check_enum(rep, sid, f"artefact {i} kind", art.get("kind"), enums, "artefact_kind")
            if "arxiv" in art and not isinstance(art["arxiv"], str):
                rep.err(sid, f"artefact {i}: quote the arXiv id so YAML keeps it as text")

        coding = src.get("coding") or {}
        for field in ("coded_by", "coded_on", "version_read"):
            if not coding.get(field):
                rep.err(sid, f"coding.{field} is missing")
        check_enum(rep, sid, "coding.read_depth", coding.get("read_depth"), enums, "read_depth")
        check_enum(rep, sid, "coding.status", coding.get("status"), enums, "record_status")
        if coding.get("read_depth") == "partial" and not coding.get("read_parts"):
            rep.err(sid, "read_depth partial needs read_parts")
        if coding.get("status") == "reviewed" and not coding.get("reviewed_by"):
            rep.err(sid, "status reviewed needs reviewed_by")

        local_studies = {}
        for study in as_list(src.get("studies")):
            stid = study.get("id")
            if not stid or not stid.startswith(sid + ".s"):
                rep.err(sid, f"study id '{stid}' must start with '{sid}.s'")
                continue
            if stid in study_ids:
                rep.err(sid, f"duplicate study id '{stid}'")
            study_ids.add(stid)
            local_studies[stid] = study

            study_models = set()
            for raw in as_list(study.get("models")):
                mid, _ = model_ref(raw)
                study_models.add(mid)
                if mid not in models:
                    rep.err(stid, f"model '{mid}' is not in models/")
            study["_models"] = study_models

            coded = study.get("facets") or {}
            for name in coded:
                if name not in study_facets:
                    rep.err(stid, f"'{name}' is not a study facet in the codebook")
            kind = facet_entry(coded.get("study_kind"))["value"]
            light = bool(kind) and kind[0] in ("conceptual", "review")
            for name, facet in study_facets.items():
                if name not in coded:
                    needed = name in LIGHT_REQUIRED if light else facet.get("required")
                    if needed:
                        rep.err(stid, f"facet '{name}' is not coded (use unspecified if the source does not say)")
                    continue
                entry = facet_entry(coded[name])
                values = entry["value"]
                for key in set(entry) - LONG_FORM_KEYS:
                    rep.err(stid, f"facet '{name}': unknown key '{key}'")
                for outer in as_list(entry.get("nested_in")):
                    if outer not in facet["values"]:
                        rep.err(stid, f"facet '{name}': nested_in '{outer}' is not in the codebook")
                levels = entry.get("levels") or {}
                if not isinstance(levels, dict):
                    rep.err(stid, f"facet '{name}': levels must map a coded value to a list of conditions")
                    levels = {}
                for key, items in levels.items():
                    if key not in values:
                        rep.err(stid, f"facet '{name}': levels given for '{key}', which is not one of the coded values")
                    if not all(isinstance(x, str) for x in as_list(items)):
                        rep.err(stid, f"facet '{name}': levels for '{key}' must be text")
                if not values:
                    rep.err(stid, f"facet '{name}' has no value")
                if facet["cardinality"] == "one" and len(values) > 1:
                    rep.err(stid, f"facet '{name}' takes one value, got {len(values)}")
                if len(values) > 1 and (SPECIAL | {NOT_YET_CODED}) & set(values):
                    rep.err(stid, f"facet '{name}': a special value cannot be combined with others")
                for value in values:
                    if value == NOT_YET_CODED and facet.get("tier") != "interpretive":
                        rep.err(stid, f"facet '{name}' is core, so it cannot be {NOT_YET_CODED}")
                    elif value not in facet["values"] and value not in SPECIAL and value != NOT_YET_CODED:
                        rep.err(stid, f"facet '{name}': '{value}' is not in the codebook")
                check_enum(rep, stid, f"{name}.basis", entry.get("basis"), enums, "basis", required=False)
                check_enum(rep, stid, f"{name}.confidence", entry.get("confidence"), enums, "confidence", required=False)

        for claim in as_list(src.get("claims")):
            cid = claim.get("id")
            if not cid or not cid.startswith(sid + ".c"):
                rep.err(sid, f"claim id '{cid}' must start with '{sid}.c'")
                continue
            if cid in claim_ids:
                rep.err(sid, f"duplicate claim id '{cid}'")
            claim_ids.add(cid)

            study = local_studies.get(claim.get("study"))
            if study is None:
                rep.err(cid, f"study '{claim.get('study')}' is not a study in this source")
            if not claim.get("statement"):
                rep.err(cid, "missing statement")
            if not claim.get("where"):
                rep.err(cid, "missing where (section, page or figure)")

            for name, facet in claim_facets.items():
                values = as_list(claim.get(name))
                if facet.get("required") and not values:
                    rep.err(cid, f"missing {name}")
                if facet["cardinality"] == "one" and len(values) > 1:
                    rep.err(cid, f"{name} takes one value")
                for value in values:
                    if value == "unspecified" and facet.get("tier") == "interpretive":
                        continue  # coded because a question needs it, and the source does not settle it
                    if value not in facet["values"]:
                        rep.err(cid, f"{name} '{value}' is not in the codebook")

            # A question can name interpretive facets its evidence must have coded (`needs`), for
            # itself and every question under it. Check them on the claim and its study.
            linked = [claim.get("question")] + [l.get("question") for l in as_list(claim.get("other_questions")) if isinstance(l, dict)]
            needs = {}
            for qid in [q for q in linked if q in questions]:
                cur, seen = qid, set()
                while cur in questions and cur not in seen:
                    seen.add(cur)
                    for name in as_list(questions[cur].get("needs")):
                        needs.setdefault(name, qid)
                    cur = questions[cur].get("parent")
            study_coded = (study or {}).get("facets") or {}
            for name, qid in sorted(needs.items()):
                facet = facets.get(name)
                if facet is None:
                    continue
                if facet["applies_to"] == "study":
                    if study is not None and NOT_YET_CODED in facet_entry(study_coded.get(name))["value"] + ([NOT_YET_CODED] if name not in study_coded else []):
                        rep.err(cid, f"question '{qid}' needs '{name}' coded on study {study.get('id')} (unspecified if the source does not settle it)")
                elif not as_list(claim.get(name)):
                    rep.err(cid, f"question '{qid}' needs '{name}' on the claim (unspecified if the source does not settle it)")

            question = claim.get("question")
            if question is not None and question not in questions:
                rep.err(cid, f"question '{question}' is not in questions/")
            def is_which(qid):
                return questions.get(qid, {}).get("kind") == "which"

            def check_answer(qid, where):
                # A which-question is answered by its answer_facet, coded on the claim or its study; no stance.
                name = questions[qid].get("answer_facet")
                facet = facets.get(name)
                if facet is None:
                    return
                if facet["applies_to"] == "claim":
                    values = as_list(claim.get(name))
                else:
                    values = facet_entry(((study or {}).get("facets") or {}).get(name))["value"]
                if not values or NOT_YET_CODED in values:
                    rep.err(cid, f"{where}: which-question '{qid}' is answered by '{name}', which is not coded")

            if question is not None and question in questions:
                if is_which(question):
                    if claim.get("stance"):
                        rep.err(cid, f"question '{question}' is a which-question: its answer is '{questions[question].get('answer_facet')}', not a stance")
                    check_answer(question, "question")
                elif not claim.get("stance"):
                    rep.err(cid, "a claim linked to a question needs a stance")
            if question is None and claim.get("stance"):
                rep.err(cid, "stance given without a question")
            if question is None and claim.get("other_questions"):
                rep.err(cid, "other_questions given without a main question")
            for link in as_list(claim.get("other_questions")):
                if not isinstance(link, dict) or link.get("question") not in questions:
                    rep.err(cid, f"other_questions: '{link}' does not name a question in questions/")
                elif is_which(link["question"]):
                    if link.get("stance"):
                        rep.err(cid, f"other_questions: '{link['question']}' is a which-question and takes no stance")
                    check_answer(link["question"], "other_questions")
                elif link.get("stance") not in claim_facets["stance"]["values"]:
                    rep.err(cid, f"other_questions: stance '{link.get('stance')}' is not in the codebook")
            if study is not None:
                varied = set(facet_entry((study.get("facets") or {}).get("varies"))["value"])
                for var in as_list(claim.get("effect_of")):
                    if var not in varied:
                        rep.err(cid, f"effect_of '{var}' is not one of the study's varies values")
            for other in as_list(claim.get("compares")):
                if other not in local_studies:
                    rep.err(cid, f"compares '{other}' is not a study in this source")

            scope = claim.get("scope") or {}
            for key in set(scope) - {"models", "conditions"}:
                rep.err(cid, f"scope: unknown key '{key}'")
            if "conditions" in scope and not isinstance(scope["conditions"], str):
                rep.err(cid, "scope.conditions must be text")
            for mid in as_list(scope.get("models")):
                if mid not in models:
                    rep.err(cid, f"scope model '{mid}' is not in models/")
                elif study is not None and mid not in study["_models"]:
                    rep.err(cid, f"scope model '{mid}' is not one of the study's models")

            about = claim.get("about") or {}
            for mid in as_list(about.get("models")):
                if mid not in models:
                    rep.err(cid, f"about model '{mid}' is not in models/")
            for did in as_list(about.get("datasets")):
                if did not in datasets:
                    rep.err(cid, f"about dataset '{did}' is not in datasets/")

        for rel in as_list(src.get("relations")):
            all_relations.append((sid, rel))

    # Relations can point across sources, so resolve them last.
    targets = source_ids | claim_ids | study_ids
    for sid, rel in all_relations:
        check_enum(rep, sid, "relation kind", rel.get("kind"), enums, "relation_kind")
        if rel.get("from") not in targets:
            rep.err(sid, f"relation from '{rel.get('from')}' is not a source, study or claim")
        if "to" in rel and rel["to"] not in targets:
            rep.err(sid, f"relation to '{rel.get('to')}' is not a source, study or claim")
        if ("to" in rel) == ("to_external" in rel):
            rep.err(sid, "relation needs exactly one of to (a coded record) or to_external (a citation)")
        if not rel.get("where"):
            rep.err(sid, "relation needs where (the place the source states it)")

    # The templates must name every facet the codebook has, and nothing it lacks, so they cannot drift.
    from _load import ROOT, read_yaml
    tpl_path = ROOT / "templates" / "source.yaml"
    if tpl_path.exists():
        tpl = read_yaml(tpl_path) or {}
        tpl_study = set(((tpl.get("studies") or [{}])[0].get("facets") or {}))
        tpl_claim = set((tpl.get("claims") or [{}])[0]) & set(facets)
        claim_keys = set((tpl.get("claims") or [{}])[0])
        for name in sorted(set(study_facets) - tpl_study):
            rep.err("templates/source.yaml", f"study facet '{name}' is missing from the template")
        for name in sorted(tpl_study - set(study_facets)):
            rep.err("templates/source.yaml", f"'{name}' in the template is not a study facet")
        for name in sorted(set(claim_facets) - {"stance"} - claim_keys):
            rep.err("templates/source.yaml", f"claim facet '{name}' is missing from the template")
        for name in sorted(tpl_claim - set(claim_facets)):
            rep.err("templates/source.yaml", f"'{name}' in the template is not a claim facet")

    counts = {
        "sources": len(source_ids),
        "studies": len(study_ids),
        "claims": len(claim_ids),
        "questions": len(questions),
        "people": len(people),
        "orgs": len(orgs),
        "models": len(models),
        "datasets": len(datasets),
    }
    return rep.errors, counts


def main():
    errors, counts = validate()
    print(", ".join(f"{n} {k}" for k, n in counts.items()))
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print("  " + e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

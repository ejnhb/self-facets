#!/usr/bin/env python3
"""Check every record against the codebook and against each other.

Usage: python scripts/validate.py
Exits 0 if clean, 1 if there are errors.
"""

import sys

from _load import (
    LIGHT_REQUIRED,
    LONG_FORM_KEYS,
    PER_VALUE_KEYS,
    postdates,
    NOT_YET_CODED,
    RELATIONS,
    SPECIAL,
    as_list,
    facet_entry,
    load_codebook,
    load_links,
    load_list_dir,
    logic_atoms,
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
            broader = body.get("broader") if isinstance(body, dict) else None
            if broader is not None and broader not in (facet.get("values") or {}):
                rep.err(where, f"value '{value}': broader '{broader}' is not a value of this facet")
        for value, body in (facet.get("values") or {}).items():  # broader must not loop
            cur, hops = value, 0
            while isinstance(facet["values"].get(cur), dict) and facet["values"][cur].get("broader") and hops < 50:
                cur = facet["values"][cur]["broader"]; hops += 1
                if cur == value:
                    rep.err(where, f"value '{value}': broader loops back to itself"); break

    orgs = index(rep, load_list_dir("orgs"), "org")
    people = index(rep, load_list_dir("people"), "person")
    datasets = index(rep, load_list_dir("datasets"), "dataset")
    models = index(rep, load_list_dir("models"), "model")
    questions = index(rep, load_list_dir("questions"), "question")
    definitions = index(rep, load_list_dir("definitions"), "definition")
    instruments = index(rep, load_list_dir("instruments"), "instrument")

    def check_logic(expr, where):
        atoms, defs = logic_atoms(expr)
        for key, vals in atoms:
            if key == "comparison.closest":
                bad = [v for v in vals if v not in RELATIONS]
                if bad:
                    rep.err(where, f"comparison.closest {bad} not in {RELATIONS}")
            elif key.startswith("model."):
                field = key[len("model."):]
                if field != "post_training_reached":
                    rep.err(where, f"'{key}': models have no field '{field}' to test")
                else:
                    for v in vals:
                        if v not in enums.get("post_training_reached", {}):
                            rep.err(where, f"'{key}': '{v}' is not in enums.yaml post_training_reached")
            elif key not in facets:
                rep.err(where, f"'{key}' is not a facet, model.FIELD or comparison.closest")
            else:
                for v in vals:
                    if v not in facets[key]["values"] and v not in SPECIAL:
                        rep.err(where, f"{key} '{v}' is not in the codebook")
        for d in defs:
            if d not in definitions:
                rep.err(where, f"definition '{d}' is not in definitions/")

    for did, d in definitions.items():
        where = f"definition {did}"
        for key in set(d) - {"id", "construct", "statement", "sources", "logic", "not_expressible", "note"}:
            rep.err(where, f"unknown key '{key}'")
        if not d.get("statement"):
            rep.err(where, "missing statement")
        if not d.get("logic"):
            rep.err(where, "missing logic")
        if d.get("construct") is not None and d["construct"] not in facets["construct"]["values"]:
            rep.err(where, f"construct '{d['construct']}' is not a construct value")
        check_logic(d.get("logic"), where)
    for did in definitions:  # cycles
        stack, seen = [did], set()
        while stack:
            cur = stack.pop()
            for ref in logic_atoms((definitions.get(cur) or {}).get("logic"))[1]:
                if ref == did:
                    rep.err(f"definition {did}", "refers to itself, directly or through other definitions"); stack = []; break
                if ref in definitions and ref not in seen:
                    seen.add(ref); stack.append(ref)

    for iid, ins in instruments.items():
        where = f"instrument {iid}"
        for key in set(ins) - {"id", "name", "kind", "models", "trained_on", "artefact", "documented_in", "note"}:
            rep.err(where, f"unknown key '{key}'")
        check_enum(rep, where, "kind", ins.get("kind"), enums, "instrument_kind")
        if not ins.get("name"):
            rep.err(where, "missing name")
        for mid in as_list(ins.get("models")):
            if mid not in models:
                rep.err(where, f"model '{mid}' is not in models/")

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
        if kind == "yesno" and q.get("parent") and "polarity" not in q:
            rep.err(f"question {qid}", "a yes/no question with a parent needs a polarity (direct, inverse or none), so its stances are not counted on the parent by default")
        if "polarity" in q and not q.get("parent"):
            rep.err(f"question {qid}", "polarity says how a question points relative to its parent, so it needs a parent")
        if q.get("parent") in questions and questions[q["parent"]].get("kind") == "which" and kind != "which":
            rep.err(f"question {qid}", "a yes/no question cannot sit under a which-question")
        auto = q.get("auto_stance")
        if auto is not None:
            if q.get("kind") == "which":
                rep.err(f"question {qid}", "auto_stance is for yes/no questions")
            for var in as_list((auto or {}).get("effect_of")):
                if var not in facets["varies"]["values"]:
                    rep.err(f"question {qid}", f"auto_stance effect_of '{var}' is not a varies value")
            if not q.get("frame"):
                rep.err(f"question {qid}", "auto_stance needs a frame, to say which studies' effects count")
            mode = (auto or {}).get("supports", "present")
            if mode not in ("present", "increases", "decreases", "improves", "worsens"):
                rep.err(f"question {qid}", f"auto_stance supports '{mode}' must be present, increases, decreases, improves or worsens")
        if "measure" in q and not isinstance(q["measure"], str):
            rep.err(f"question {qid}", "measure is text: which measure 'how well' means")
        if "exact_values" in q and not isinstance(q["exact_values"], bool):
            rep.err(f"question {qid}", "exact_values is true or false (true: the frame does not take in narrower values)")
        check_logic(q.get("frame"), f"question {qid} frame")
        requires = q.get("requires") or {}
        if not isinstance(requires, dict):
            rep.err(f"question {qid}", "requires must map a facet to the values a claim needs to count")
            requires = {}
        for d in as_list(requires.get("definitions")):
            if d not in definitions:
                rep.err(f"question {qid}", f"requires definition '{d}', which is not in definitions/")
        for name, vals in requires.items():
            if name == "definitions":
                continue
            if name not in facets:
                rep.err(f"question {qid}", f"requires '{name}', which is not a facet")
                continue
            for v in as_list(vals):
                if v not in facets[name]["values"]:
                    rep.err(f"question {qid}", f"requires {name} '{v}', which is not in the codebook")
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
        check_enum(rep, where, "post_training_reached", model.get("post_training_reached"), enums, "post_training_reached", required=False)
        if model.get("layers") is not None and not (isinstance(model["layers"], int) and model["layers"] > 0):
            rep.err(where, "layers is the model's number of layers, a positive whole number")
        if model.get("variant_of") is not None and model.get("variant_of") not in models:
            rep.err(where, f"variant_of '{model.get('variant_of')}' is not a model")
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
    all_claims, all_studies = {}, {}

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
            if art.get("kind") in ("code", "data"):
                check_enum(rep, sid, f"artefact {i} status", art.get("status"), enums, "availability_status")
                if art.get("status") == "released":
                    if not art.get("url"):
                        rep.err(sid, f"artefact {i}: a released {art['kind']} artefact needs its url")
                    if art.get("read") not in (True, False, "partial"):
                        rep.err(sid, f"artefact {i}: read is true, false or partial (what this coding read of it)")
        for kind in ("code", "data"):
            if not any(a.get("kind") == kind for a in as_list(src.get("artefacts"))):
                rep.err(sid, f"say whether {kind} is available: add an artefact of kind {kind} with a status "
                             "(released, not_released or unknown)")
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
        for i, nc in enumerate(as_list(coding.get("not_coded")), 1):
            if not isinstance(nc, dict) or not nc.get("where") or not nc.get("reason"):
                rep.err(sid, f"coding.not_coded {i}: needs where and reason")
        if coding.get("status") == "reviewed" and not coding.get("reviewed_by"):
            rep.err(sid, "status reviewed needs reviewed_by")
        passes = as_list(coding.get("passes"))
        if not passes:
            rep.err(sid, "coding.passes is missing: list every coding or change (AGENTS.md, 'Mark your work')")
        for i, ps in enumerate(passes, 1):
            if not isinstance(ps, dict):
                rep.err(sid, f"coding.passes {i} must be a mapping")
                continue
            for field in ("date", "coded_by", "codebook", "scope", "read"):
                if not ps.get(field):
                    rep.err(sid, f"coding.passes {i}: {field} is missing")
            if ps.get("coded_by") == "claude" and not ps.get("coder_model"):
                rep.err(sid, f"coding.passes {i}: coder_model is required when coded_by is claude")
            if not isinstance(ps.get("codebook"), str):
                rep.err(sid, f"coding.passes {i}: quote codebook so YAML keeps it as text")
            pr = ps.get("pr")
            if pr is not None and not (isinstance(pr, int) or (isinstance(pr, list) and all(isinstance(x, int) for x in pr))):
                rep.err(sid, f"coding.passes {i}: pr is a pull request number or a list of them")

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
            all_studies[stid] = study

            study_models = set()
            for raw in as_list(study.get("models")):
                mid, roles, _ = model_ref(raw)
                study_models.add(mid)
                if mid not in models:
                    rep.err(stid, f"model '{mid}' is not in models/")
                if isinstance(raw, dict):
                    for key in set(raw) - {"id", "roles", "note"}:
                        rep.err(stid, f"model '{mid}': unknown key '{key}' (roles and note since codebook 0.8)")
                for role in roles:
                    check_enum(rep, stid, f"model '{mid}' role", role, enums, "model_role")
            study["_models"] = study_models
            for iid in as_list(study.get("instruments")):
                if iid not in instruments:
                    rep.err(stid, f"instrument '{iid}' is not in instruments/")

            coded = study.get("facets") or {}
            for name in coded:
                if name not in study_facets:
                    rep.err(stid, f"'{name}' is not a study facet in the codebook")
            kind = facet_entry(coded.get("study_kind"))["value"]
            light = bool(kind) and kind[0] in ("conceptual", "review")
            for name, facet in study_facets.items():
                if name not in coded:
                    needed = name in LIGHT_REQUIRED if light else facet.get("required")
                    if needed and postdates(facet, src):
                        continue  # added after this record's last pass: reads as not_yet_coded until backfilled
                    if needed:
                        rep.err(stid, f"facet '{name}' is not coded (use unspecified if the source does not say)")
                    continue
                entry = facet_entry(coded[name])
                values = entry["value"]
                for key in set(entry) - LONG_FORM_KEYS - {"per_value"}:
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
                for v, item in (entry.get("per_value") or {}).items():
                    for key in set(item) - PER_VALUE_KEYS:
                        rep.err(stid, f"facet '{name}': value '{v}': unknown key '{key}'")
                    check_enum(rep, stid, f"{name}.{v}.basis", item.get("basis"), enums, "basis", required=False)
                    check_enum(rep, stid, f"{name}.{v}.confidence", item.get("confidence"), enums, "confidence", required=False)
                if "excluded" in entry:
                    if facet.get("tier") != "interpretive":
                        rep.err(stid, f"facet '{name}': excluded is for interpretive facets (routes a source rules out)")
                    for v in as_list(entry.get("excluded")):
                        if v not in facet["values"]:
                            rep.err(stid, f"facet '{name}': excluded '{v}' is not in the codebook")
                        if v in values:
                            rep.err(stid, f"facet '{name}': '{v}' is both coded and excluded")
                if "layer_scale" in entry:
                    if name != "varies" or "layer" not in values:
                        rep.err(stid, f"facet '{name}': layer_scale goes on varies with layer")
                    elif entry["layer_scale"] not in ("index", "fraction"):
                        rep.err(stid, "varies: layer_scale must be index or fraction")
                elif name == "varies" and "layer" in values:
                    rep.err(stid, "varies: layer needs layer_scale (index or fraction)")

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
                entry = facet_entry(claim.get(name)) if name in claim else {"value": []}
                values = entry["value"]
                if isinstance(claim.get(name), dict):
                    for key in set(entry) - (LONG_FORM_KEYS - {"levels", "nested_in", "layer_scale"}) - {"per_value"}:
                        rep.err(cid, f"{name}: unknown key '{key}'")
                    check_enum(rep, cid, f"{name}.basis", entry.get("basis"), enums, "basis", required=False)
                for v, item in (entry.get("per_value") or {}).items():
                    for key in set(item) - PER_VALUE_KEYS:
                        rep.err(cid, f"{name}: value '{v}': unknown key '{key}'")
                    check_enum(rep, cid, f"{name}.{v}.basis", item.get("basis"), enums, "basis", required=False)
                if "excluded" in entry:
                    if facet.get("tier") != "interpretive":
                        rep.err(cid, f"{name}: excluded is for interpretive facets (routes a source rules out)")
                    for v in as_list(entry.get("excluded")):
                        if v not in facet["values"]:
                            rep.err(cid, f"{name}: excluded '{v}' is not in the codebook")
                        if v in values:
                            rep.err(cid, f"{name}: '{v}' is both coded and excluded")
                if facet.get("required") and not values and not postdates(facet, src):
                    rep.err(cid, f"missing {name}")
                if facet["cardinality"] == "one" and len(values) > 1:
                    rep.err(cid, f"{name} takes one value")
                for value in values:
                    if value == "unspecified" and facet.get("tier") == "interpretive":
                        continue  # coded because a question needs it, and the source does not settle it
                    if value not in facet["values"]:
                        rep.err(cid, f"{name} '{value}' is not in the codebook")

            # Links to questions live in links/ since codebook 0.7.
            for key in ("question", "stance", "other_questions"):
                if key in claim:
                    rep.err(cid, f"'{key}' belongs in links/{sid}.yaml now (codebook 0.7), not in the record")
            all_claims[cid] = (claim, study)

            if claim.get("effect_of") and not claim.get("effect_presence"):
                rep.err(cid, "a claim with effect_of needs effect_presence (present, absent, mixed, inconclusive)")
            if claim.get("effect_presence") and not claim.get("effect_of"):
                rep.err(cid, "effect_presence goes with effect_of: say which variable the claim reports the effect of")
            if claim.get("effect_direction") and claim.get("effect_presence") != "present":
                rep.err(cid, "effect_direction only goes with effect_presence present")
            if study is not None:
                varied = set(facet_entry((study.get("facets") or {}).get("varies"))["value"])
                for var in as_list(claim.get("effect_of")):
                    if var not in varied:
                        rep.err(cid, f"effect_of '{var}' is not one of the study's varies values")
            if "better" in claim and claim["better"] not in ("higher", "lower"):
                rep.err(cid, "better must be higher or lower (which way the reported quantity is better)")
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

    # Links: claim -> question, with a stance for yes/no questions and none for which-questions.
    def ancestors(qid):
        out, seen = [], set()
        while qid in questions and qid not in seen:
            seen.add(qid); out.append(qid); qid = questions[qid].get("parent")
        return out

    def study_values(study, name):
        coded = (study or {}).get("facets") or {}
        return facet_entry(coded.get(name))["value"] if name in coded else [NOT_YET_CODED]

    seen_links = set()
    for path, data in load_links():
        where = f"links/{path.name}"
        if not isinstance(data, dict) or data.get("source") != path.stem:
            rep.err(where, f"needs 'source: {path.stem}' (the file is named after its source)")
            continue
        for i, link in enumerate(as_list(data.get("links")), 1):
            here = f"{where} link {i}"
            if not isinstance(link, dict):
                rep.err(here, "not a mapping"); continue
            for key in set(link) - {"claim", "question", "stance", "note", "designed"}:
                rep.err(here, f"unknown key '{key}'")
            if "designed" in link and link["designed"] not in (True, False, "unspecified"):
                rep.err(here, "designed is true (the study was built to test this question), false (its result bears on it "
                              "post hoc) or unspecified")
            cid, qid = link.get("claim"), link.get("question")
            if cid not in all_claims:
                rep.err(here, f"claim '{cid}' is not a coded claim"); continue
            if not str(cid).startswith(path.stem + "."):
                rep.err(here, f"claim '{cid}' is not one of {path.stem}'s claims")
            if qid not in questions:
                rep.err(here, f"question '{qid}' is not in questions/"); continue
            if (cid, qid) in seen_links:
                rep.err(here, f"{cid} is linked to {qid} twice")
            seen_links.add((cid, qid))
            claim, study = all_claims[cid]
            q = questions[qid]
            if q.get("kind") == "which":
                if link.get("stance"):
                    rep.err(here, f"'{qid}' is a which-question: answered by '{q.get('answer_facet')}', not a stance")
                name = q.get("answer_facet")
                f = facets.get(name)
                if f is not None:
                    values = facet_entry(claim.get(name))["value"] if f["applies_to"] == "claim" else study_values(study, name)
                    if not values or NOT_YET_CODED in values:
                        rep.err(here, f"which-question '{qid}' is answered by '{name}', which {cid} does not code")
            elif link.get("stance") not in claim_facets["stance"]["values"]:
                rep.err(here, f"a link to a yes/no question needs a stance from the codebook (got '{link.get('stance')}')")
            # needs and requires, from the question and every question above it
            needs = {}
            for anc in ancestors(qid):
                for name in as_list(questions[anc].get("needs")) + [k for k in (questions[anc].get("requires") or {}) if k != "definitions"]:
                    needs.setdefault(name, anc)
            for name, anc in sorted(needs.items()):
                f = facets.get(name)
                if f is None:
                    continue
                if f["applies_to"] == "study":
                    if NOT_YET_CODED in study_values(study, name):
                        rep.err(here, f"question '{anc}' needs '{name}' coded on {study.get('id') if study else '?'} (unspecified if the source does not settle it)")
                elif not as_list(claim.get(name)):
                    rep.err(here, f"question '{anc}' needs '{name}' on {cid} (unspecified if the source does not settle it)")

    # Readings: lenses that reclassify facets, or attach an alternative explanation, under a view only.
    readings = index(rep, load_list_dir("readings"), "reading")
    model_fields = {"post_training_reached": enums.get("post_training_reached", {})}
    for rid, r in readings.items():
        where = f"reading {rid}"
        for key in set(r) - {"id", "status", "statement", "applies_to", "effect", "sources", "tested_by", "note"}:
            rep.err(where, f"unknown key '{key}'")
        check_enum(rep, where, "status", r.get("status"), enums, "reading_status")
        if not r.get("statement"):
            rep.err(where, "missing statement")
        applies = r.get("applies_to") or {}
        if bool(applies.get("selector")) == bool(applies.get("targets")):
            rep.err(where, "applies_to needs exactly one of selector (facet values) or targets (claim or study ids)")
        check_logic(applies.get("selector"), where + " selector")
        for t in as_list(applies.get("targets")):
            if t not in all_claims and t not in all_studies:
                rep.err(where, f"target '{t}' is not a coded claim or study")
        effect = r.get("effect") or {}
        for key in set(effect) - {"reclassify", "reinterpret"}:
            rep.err(where, f"effect '{key}' is not reclassify or reinterpret")
        if not effect:
            rep.err(where, "needs an effect (reclassify, reinterpret or both)")
        for i, rc in enumerate(as_list(effect.get("reclassify")), 1):
            name = rc.get("facet") if isinstance(rc, dict) else None
            if name not in facets:
                rep.err(where, f"reclassify {i}: '{name}' is not a facet"); continue
            for k in ("from", "to"):
                v = rc.get(k)
                if v not in facets[name]["values"] and v not in SPECIAL:
                    rep.err(where, f"reclassify {i}: {k} '{v}' is not a value of {name}")

    views = index(rep, load_list_dir("views"), "view")
    for vid, v in views.items():
        if v.get("question") not in questions:
            rep.err(f"view {vid}", f"question '{v.get('question')}' is not in questions/")
        elif questions[v["question"]].get("kind") == "which":
            pass
        for rid in as_list(v.get("readings")):
            if rid not in readings:
                rep.err(f"view {vid}", f"reading '{rid}' is not in readings/")
        for a_, b_ in (v.get("substitute") or {}).items():
            for d in (a_, b_):
                if d not in definitions:
                    rep.err(f"view {vid}", f"substitute: '{d}' is not in definitions/")

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

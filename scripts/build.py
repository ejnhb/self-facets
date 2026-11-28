#!/usr/bin/env python3
"""Compile the YAML records into one SQLite database.

Usage: python scripts/build.py [output path]
Default output: build/self-facets.sqlite

The YAML files are the source of truth. The database is derived, is rebuilt
from scratch each time, and is not committed.
"""

import sqlite3
import sys
from pathlib import Path

from _load import (
    LIGHT_REQUIRED,
    NOT_YET_CODED,
    RELATIONS,
    ROOT,
    as_list,
    facet_entry,
    load_codebook,
    load_links,
    evaluate,
    load_list_dir,
    load_sources,
    logic_atoms,
    model_ref,
    narrower_map,
    postdates,
    relation,
)
from validate import validate

SCHEMA = """
CREATE TABLE codebook (facet TEXT, value TEXT, family TEXT, definition TEXT, rule TEXT, facet_version TEXT);
CREATE TABLE orgs (id TEXT PRIMARY KEY, name TEXT, kind TEXT);
CREATE TABLE people (id TEXT PRIMARY KEY, name TEXT, orcid TEXT);
CREATE TABLE datasets (id TEXT PRIMARY KEY, name TEXT, hub TEXT, documented_in TEXT, note TEXT);
CREATE TABLE dataset_components (dataset TEXT, component TEXT);
CREATE TABLE models (
    id TEXT PRIMARY KEY, name TEXT, family TEXT, developer TEXT, size TEXT,
    open_weights INTEGER, derived_from TEXT, stage_coded INTEGER,
    disclosure TEXT, documented_in TEXT, note TEXT, layers INTEGER
);
CREATE TABLE model_stage_methods (model TEXT, method TEXT);
CREATE TABLE model_stage_datasets (model TEXT, dataset TEXT);
CREATE TABLE questions (id TEXT PRIMARY KEY, text TEXT, parent TEXT, kind TEXT, polarity TEXT, answer_facet TEXT, status TEXT, added TEXT);
-- Each question with the top of its parent chain (itself if it has no parent).
-- For yes/no questions: the question whose tree a stance counts in, and the sign that turns the stance into one
-- on that root (-1 under an inverse question). A polarity none question is its own root.
CREATE TABLE question_roots (question TEXT PRIMARY KEY, root TEXT, sign INTEGER);
-- Interpretive facets a question's evidence must have coded (for it and every question under it).
CREATE TABLE question_needs (question TEXT, facet TEXT);
CREATE TABLE sources (
    id TEXT PRIMARY KEY, title TEXT, date TEXT, year INTEGER,
    coded_by TEXT, coder_model TEXT, coded_on TEXT, version_read TEXT,
    read_depth TEXT, read_parts TEXT, status TEXT, reviewed_by TEXT
);
-- Every coding or change to a record, in order (coding.passes): who, with which model, against which codebook, and
-- what was read. A checker can confirm it is not the model that coded what it checks.
CREATE TABLE coding_passes (
    source TEXT, n INTEGER, date TEXT, pr TEXT, coded_by TEXT, coder_model TEXT, codebook TEXT, scope TEXT, read TEXT
);
CREATE TABLE artefacts (
    source TEXT, kind TEXT, arxiv TEXT, url TEXT, venue TEXT, note TEXT, status TEXT, ref TEXT, read TEXT
);
CREATE TABLE authorship (source TEXT, position INTEGER, person TEXT);
CREATE TABLE affiliations (source TEXT, person TEXT, org TEXT);
CREATE TABLE studies (id TEXT PRIMARY KEY, source TEXT, label TEXT, design TEXT, where_ TEXT, note TEXT);
-- One row per model and role (subject, comparison, judge, data_source).
CREATE TABLE study_models (study TEXT, model TEXT, role TEXT, note TEXT);
-- Every subject and comparison pair in a study, with how closely the registry says they are related, and the
-- closest such relation per study (same > variant > derived > same_family > same_developer > other).
CREATE TABLE study_comparisons (study TEXT, subject TEXT, comparison TEXT, relation TEXT);
CREATE TABLE study_closest_comparison (study TEXT PRIMARY KEY, relation TEXT);
-- Claims whose study matches a question's frame but which no link or auto_stance yet ties to it.
-- Claims not yet linked to a question that fit its frame and meet its (and its ancestors') requires. missing_needs
-- lists the interpretive facets the question's tree needs that the claim's study has not coded: candidates worth
-- re-reading for them, for example when a question has few hits.
-- via: the other study of the claim's paper through which it fits the frame (the claim compares the two), or null.
CREATE TABLE question_candidates (question TEXT, claim TEXT, missing_needs TEXT, via TEXT);
-- A frame value that takes in narrower values (codebook broader:), shown so the poser sees what the frame reaches.
CREATE TABLE question_frame_expansions (question TEXT, facet TEXT, value TEXT, includes TEXT);
-- Things a question poser should look at: a frame on a construct label with several definitions, and the like.
CREATE TABLE question_warnings (question TEXT, kind TEXT, detail TEXT);
-- Facets added after a record's last pass (codebook since:), read as not_yet_coded until backfilled.
CREATE TABLE backfill (facet TEXT, since TEXT, source TEXT, study TEXT);
-- Layers a study varies, per subject model, on a common scale: fraction of depth. From layer_scale fraction as given,
-- or from layer_scale index over the model's registered layer count (layer / layers; indexing conventions differ,
-- so treat it as approximate).
CREATE TABLE study_layer_depths (study TEXT, model TEXT, level TEXT, layer_scale TEXT, fraction REAL);
CREATE TABLE study_facets (
    study TEXT, facet TEXT, value TEXT, basis TEXT, author_term TEXT,
    confidence TEXT, nested_in TEXT, where_ TEXT, note TEXT
);
CREATE TABLE study_facet_levels (study TEXT, facet TEXT, value TEXT, level TEXT);
CREATE TABLE claims (
    id TEXT PRIMARY KEY, source TEXT, study TEXT, statement TEXT,
    evidence_kind TEXT, scope_conditions TEXT, where_ TEXT, note TEXT
);
-- Links (links/): every yes/no question a claim takes a stance on. `counted` is 0 when the claim fails a
-- `requires` of the question or a question above it, so it is not evidence there even with no reading applied.
-- via: as in question_candidates, for links that rest on a compared study's facets (automatic stances only).
CREATE TABLE claim_questions (claim TEXT, question TEXT, stance TEXT, counted INTEGER, note TEXT, origin TEXT, via TEXT);
-- Readings (readings/) and views (views/): see design/readings.md.
-- Definitions (definitions/): named logic over facets for what a design tests in one stated sense.
CREATE TABLE definitions (id TEXT PRIMARY KEY, construct TEXT, statement TEXT, sources TEXT, not_expressible TEXT);
-- Claims whose (unlensed) facets satisfy a definition.
CREATE TABLE claim_definitions (claim TEXT, definition TEXT);
-- Studies whose authors use a construct label (construct facet) that some definitions define, but whose claims
-- match none of those definitions.
CREATE TABLE construct_mismatches (study TEXT, construct TEXT, definitions TEXT);
CREATE TABLE readings (id TEXT PRIMARY KEY, status TEXT, statement TEXT, reinterpret TEXT, tested_by TEXT);
CREATE TABLE reading_matches (reading TEXT, claim TEXT);
CREATE TABLE views (id TEXT PRIMARY KEY, question TEXT, readings TEXT, substitute TEXT, note TEXT);
-- Every claim linked to the view's question or a question under it: its stance on the view's question,
-- whether it counts with no reading and under the view, and which reading excluded it.
CREATE TABLE view_evidence (
    view TEXT, claim TEXT, linked_question TEXT, stance TEXT,
    counted_without_readings INTEGER, counted INTEGER, excluded_by TEXT
);
CREATE TABLE view_reinterpretations (view TEXT, claim TEXT, reading TEXT, text TEXT);
CREATE TABLE view_answers (view TEXT, claim TEXT, value TEXT);
CREATE TABLE claim_compares (claim TEXT, study TEXT);
-- The variables whose effect a claim reports (a subset of its study's varies).
CREATE TABLE claim_effects (claim TEXT, variable TEXT);
CREATE TABLE claim_models (claim TEXT, model TEXT, scoped INTEGER);
-- Optional claim facets (disposition, report_source, origin, integration, aspect).
CREATE TABLE claim_codes (claim TEXT, facet TEXT, value TEXT);
CREATE TABLE claim_about (claim TEXT, kind TEXT, ref TEXT);
CREATE TABLE relations (source TEXT, kind TEXT, from_ TEXT, to_ TEXT, to_external TEXT, where_ TEXT, note TEXT);
-- Answers to which-questions: the claim's (or its study's) values of the question's answer_facet.
CREATE TABLE claim_answers (claim TEXT, question TEXT, value TEXT);
-- Pairs of claims under one which-question whose answers differ. shared_facets as in conflicts.
CREATE TABLE which_conflicts (question TEXT, claim_a TEXT, claim_b TEXT, answers_a TEXT, answers_b TEXT, shared_facets INTEGER);

-- What could be re-run or extended, per study: code and data availability of its source (status, and whether the
-- coding read them), and whether its subject models have open weights (all, some, none).
CREATE VIEW study_availability AS
SELECT st.id AS study, st.source,
       (SELECT status FROM artefacts WHERE source = st.source AND kind = 'code' LIMIT 1) AS code,
       (SELECT read FROM artefacts WHERE source = st.source AND kind = 'code' LIMIT 1) AS code_read,
       (SELECT status FROM artefacts WHERE source = st.source AND kind = 'data' LIMIT 1) AS data,
       (SELECT read FROM artefacts WHERE source = st.source AND kind = 'data' LIMIT 1) AS data_read,
       CASE
         WHEN (SELECT COUNT(*) FROM study_models sm WHERE sm.study = st.id AND sm.role = 'subject') = 0 THEN NULL
         WHEN (SELECT MIN(COALESCE(m.open_weights, 0)) FROM study_models sm JOIN models m ON m.id = sm.model
               WHERE sm.study = st.id AND sm.role = 'subject') = 1 THEN 'all'
         WHEN (SELECT MAX(COALESCE(m.open_weights, 0)) FROM study_models sm JOIN models m ON m.id = sm.model
               WHERE sm.study = st.id AND sm.role = 'subject') = 1 THEN 'some'
         ELSE 'none'
       END AS open_weight_subjects
FROM studies st;
-- The same beside each claim linked to a question, so a question's evidence shows what could be reproduced.
CREATE VIEW question_evidence_availability AS
SELECT cq.question, cq.claim, cq.stance, c.study, sa.code, sa.code_read, sa.data, sa.data_read, sa.open_weight_subjects
FROM claim_questions cq JOIN claims c ON c.id = cq.claim JOIN study_availability sa ON sa.study = c.study;

-- Each stance turned into a stance on its tree's root (flipped under an inverse question).
CREATE VIEW root_stances AS
SELECT q.claim, q.question, r.root,
       CASE WHEN r.sign = -1 AND q.stance = 'supports' THEN 'against'
            WHEN r.sign = -1 AND q.stance = 'against' THEN 'supports'
            ELSE q.stance END AS stance
FROM claim_questions q JOIN question_roots r ON r.question = q.question
WHERE q.counted = 1;

-- One row per claim and facet value, with facets inherited from the study.
CREATE VIEW claim_facets AS
SELECT c.id AS claim, f.facet, f.value
FROM claims c JOIN study_facets f ON f.study = c.study;

-- Pairs of counted claims taking opposite stances under a view, and what changed from no readings.
CREATE VIEW view_conflicts AS
SELECT a.view, a.claim AS supports, b.claim AS against
FROM view_evidence a JOIN view_evidence b ON b.view = a.view AND b.stance = 'against' AND b.counted = 1
WHERE a.stance = 'supports' AND a.counted = 1;
CREATE VIEW view_diff AS
SELECT view, claim, linked_question, stance, excluded_by FROM view_evidence
WHERE counted_without_readings != counted;

-- Pairs of counted claims that take opposite stances on the same question as posed (the default). Sort by
-- shared_facets, the facet values the two claims' studies have in common, to see the most comparable pairs first.
CREATE VIEW conflicts AS
SELECT a.question, a.claim AS supports, b.claim AS against,
       ca.scope_conditions AS supports_conditions, cb.scope_conditions AS against_conditions,
       (SELECT COUNT(*) FROM study_facets f JOIN study_facets g
          ON g.facet = f.facet AND g.value = f.value
        WHERE f.study = ca.study AND g.study = cb.study AND f.value != 'not_yet_coded') AS shared_facets
FROM claim_questions a
JOIN claim_questions b ON b.question = a.question AND b.stance = 'against' AND b.counted = 1
JOIN claims ca ON ca.id = a.claim
JOIN claims cb ON cb.id = b.claim
WHERE a.stance = 'supports' AND a.counted = 1;

-- On request: the same across a question tree, after turning each stance into one on the root (root_stances).
-- `question` is the root. This is most of the pairs; query it when a tree's overall picture is wanted.
CREATE VIEW conflicts_rollup AS
SELECT a.root AS question, a.claim AS supports, b.claim AS against,
       a.question AS supports_question, b.question AS against_question,
       ca.scope_conditions AS supports_conditions, cb.scope_conditions AS against_conditions,
       (SELECT COUNT(*) FROM study_facets f JOIN study_facets g
          ON g.facet = f.facet AND g.value = f.value
        WHERE f.study = ca.study AND g.study = cb.study AND f.value != 'not_yet_coded') AS shared_facets
FROM root_stances a
JOIN root_stances b ON b.root = a.root AND b.stance = 'against'
JOIN claims ca ON ca.id = a.claim
JOIN claims cb ON cb.id = b.claim
WHERE a.stance = 'supports';

-- A question's evidence with what the poser needs beside it: the study, its task levels (if it varies task), and
-- whether the link was made by hand or automatically.
CREATE VIEW question_evidence AS
SELECT cq.question, cq.claim, cq.stance, cq.counted, cq.origin, cq.via, c.study, st.label AS study_label,
       (SELECT group_concat(level, '; ') FROM study_facet_levels l
        WHERE l.study = c.study AND l.facet = 'varies' AND l.value = 'task') AS tasks
FROM claim_questions cq JOIN claims c ON c.id = cq.claim JOIN studies st ON st.id = c.study;

-- Links per question by origin: the automatic share is the gauge of how much linking costs by hand.
CREATE VIEW link_origins AS
SELECT question, SUM(origin = 'link') AS by_hand, SUM(origin = 'auto') AS automatic, COUNT(*) AS total
FROM claim_questions GROUP BY question;

-- For each conflicting pair, the facet values one side has and the other lacks.
CREATE VIEW conflict_facet_diff AS
SELECT x.question, x.supports, x.against, f.facet, f.value, 'supports_only' AS side
FROM conflicts x JOIN claim_facets f ON f.claim = x.supports
WHERE NOT EXISTS (SELECT 1 FROM claim_facets g
                  WHERE g.claim = x.against AND g.facet = f.facet AND g.value = f.value)
UNION ALL
SELECT x.question, x.supports, x.against, f.facet, f.value, 'against_only'
FROM conflicts x JOIN claim_facets f ON f.claim = x.against
WHERE NOT EXISTS (SELECT 1 FROM claim_facets g
                  WHERE g.claim = x.supports AND g.facet = f.facet AND g.value = f.value);
"""


def text(value):
    return None if value is None else str(value).strip()


def build(out_path):
    errors, _ = validate()
    if errors:
        print(f"Not building: {len(errors)} validation error(s). Run scripts/validate.py.")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()
    db = sqlite3.connect(out_path)
    db.executescript(SCHEMA)

    facets, _ = load_codebook()
    # Claim facets other than the two that have their own columns.
    claim_code_facets = [
        n for n, f in facets.items()
        if f["applies_to"] == "claim" and n not in ("stance", "evidence_kind")
    ]
    for name, facet in facets.items():
        for value, body in facet["values"].items():
            db.execute(
                "INSERT INTO codebook VALUES (?,?,?,?,?,?)",
                (name, value, body.get("family"), text(body.get("definition")), text(body.get("rule")), text(facet.get("version"))),
            )

    for _, o in load_list_dir("orgs"):
        db.execute("INSERT INTO orgs VALUES (?,?,?)", (o["id"], o.get("name"), o.get("kind")))
    for _, p in load_list_dir("people"):
        db.execute("INSERT INTO people VALUES (?,?,?)", (p["id"], p.get("name"), p.get("orcid")))
    for _, d in load_list_dir("datasets"):
        db.execute(
            "INSERT INTO datasets VALUES (?,?,?,?,?)",
            (d["id"], d.get("name"), d.get("hub"), text(d.get("documented_in")), text(d.get("note"))),
        )
        for comp in as_list(d.get("components")):
            db.execute("INSERT INTO dataset_components VALUES (?,?)", (d["id"], comp))

    for _, m in load_list_dir("models"):
        stage = m.get("stage") or {}
        db.execute(
            "INSERT INTO models VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                m["id"], m.get("name"), m.get("family"), m.get("developer"), text(m.get("size")),
                None if m.get("open_weights") is None else int(m["open_weights"]),
                ", ".join(as_list(m.get("derived_from"))) or None, int(m.get("stage") is not None),
                stage.get("disclosure"), text(stage.get("documented_in")), text(m.get("note")),
                m.get("layers"),
            ),
        )
        for method in as_list(stage.get("methods")):
            db.execute("INSERT INTO model_stage_methods VALUES (?,?)", (m["id"], method))
        for ds in as_list(stage.get("datasets")):
            db.execute("INSERT INTO model_stage_datasets VALUES (?,?)", (m["id"], ds))

    qs = {}
    for _, q in load_list_dir("questions"):
        qs[q["id"]] = q
        db.execute(
            "INSERT INTO questions VALUES (?,?,?,?,?,?,?,?)",
            (q["id"], text(q.get("text")), q.get("parent"), q.get("kind", "yesno"),
             q.get("polarity", "direct") if q.get("parent") and q.get("kind", "yesno") == "yesno" else None,
             q.get("answer_facet"), q.get("status"), text(q.get("added"))),
        )
        for name in as_list(q.get("needs")):
            db.execute("INSERT INTO question_needs VALUES (?,?)", (q["id"], name))
    for qid, q in qs.items():
        if q.get("kind", "yesno") != "yesno":
            continue
        root, sign = qid, 1
        while qs[root].get("parent") and qs[root].get("polarity", "direct") != "none":
            if qs[root].get("polarity") == "inverse":
                sign = -sign
            root = qs[root]["parent"]
        db.execute("INSERT INTO question_roots VALUES (?,?,?)", (qid, root, sign))

    claims_mem, closest_by_study = {}, {}
    all_study_facets, all_study_subjects = {}, {}
    narrower = narrower_map(facets)
    registry = {m["id"]: m for _, m in load_list_dir("models")}
    for _, src in load_sources():
        sid = src["id"]
        coding = src.get("coding") or {}
        date = text(src.get("date"))
        db.execute(
            "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                sid, src.get("title"), date, int(date[:4]) if date else None,
                coding.get("coded_by"), coding.get("coder_model"), text(coding.get("coded_on")),
                text(coding.get("version_read")), coding.get("read_depth"),
                text(coding.get("read_parts")), coding.get("status"), coding.get("reviewed_by"),
            ),
        )
        for n, ps in enumerate(as_list(coding.get("passes")), 1):
            pr = ps.get("pr")
            db.execute(
                "INSERT INTO coding_passes VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    sid, n, text(ps.get("date")),
                    ", ".join(map(str, pr)) if isinstance(pr, list) else (str(pr) if pr is not None else None),
                    ps.get("coded_by"), ps.get("coder_model"), text(ps.get("codebook")), ps.get("scope"), ps.get("read"),
                ),
            )
        for art in as_list(src.get("artefacts")):
            db.execute(
                "INSERT INTO artefacts VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    sid, art.get("kind"), art.get("arxiv"), art.get("url"), art.get("venue"), text(art.get("note")),
                    art.get("status"), text(art.get("ref")),
                    None if art.get("read") is None else str(art.get("read")).lower(),
                ),
            )
        for pos, author in enumerate(as_list(src.get("authors")), 1):
            db.execute("INSERT INTO authorship VALUES (?,?,?)", (sid, pos, author["person"]))
            for org in as_list(author.get("orgs")):
                db.execute("INSERT INTO affiliations VALUES (?,?,?)", (sid, author["person"], org))

        study_models = {}
        study_facets_by_id = {st["id"]: (st.get("facets") or {}) for st in as_list(src.get("studies"))}
        for study in as_list(src.get("studies")):
            stid = study["id"]
            db.execute(
                "INSERT INTO studies VALUES (?,?,?,?,?,?)",
                (stid, sid, study.get("label"), text(study.get("design")), text(study.get("where")), text(study.get("note"))),
            )
            study_models[stid] = []
            for raw in as_list(study.get("models")):
                mid, roles, mnote = model_ref(raw)
                if "subject" in roles:
                    study_models[stid].append(mid)
                for role in roles:
                    db.execute("INSERT INTO study_models VALUES (?,?,?,?)", (stid, mid, role, text(mnote)))
            subjects = [model_ref(r)[0] for r in as_list(study.get("models")) if "subject" in model_ref(r)[1]]
            comparisons = [model_ref(r)[0] for r in as_list(study.get("models")) if "comparison" in model_ref(r)[1]]
            rels = []
            for a in subjects:
                for b in comparisons:
                    if a != b:
                        rel = relation(a, b, registry)
                        rels.append(rel)
                        db.execute("INSERT INTO study_comparisons VALUES (?,?,?,?)", (stid, a, b, rel))
            if rels:
                closest = min(rels, key=RELATIONS.index)
                closest_by_study[stid] = closest
                db.execute("INSERT INTO study_closest_comparison VALUES (?,?)", (stid, closest))
            for name, raw in (study.get("facets") or {}).items():
                entry = facet_entry(raw)
                for value in entry["value"]:
                    db.execute(
                        "INSERT INTO study_facets VALUES (?,?,?,?,?,?,?,?,?)",
                        (
                            stid, name, value, entry.get("basis"), entry.get("author_term"),
                            entry.get("confidence"), ", ".join(as_list(entry.get("nested_in"))) or None,
                            text(entry.get("where")), text(entry.get("note")),
                        ),
                    )
                for value, levels in (entry.get("levels") or {}).items():
                    for level in as_list(levels):
                        db.execute("INSERT INTO study_facet_levels VALUES (?,?,?,?)", (stid, name, value, level))
            # An interpretive facet left out of the record is stored as not_yet_coded, so a query can tell
            # "nobody has looked" from "the source does not say" (unspecified). In a conceptual or review study the
            # facets it need not code are read as not_applicable, as before.
            kind = facet_entry((study.get("facets") or {}).get("study_kind"))["value"]
            light = bool(kind) and kind[0] in ("conceptual", "review")
            for name, facet in facets.items():
                if facet["applies_to"] == "study" and facet.get("tier") == "interpretive" and name not in (study.get("facets") or {}):
                    db.execute(
                        "INSERT INTO study_facets VALUES (?,?,?,?,?,?,?,?,?)",
                        (stid, name, "not_applicable" if light and name not in LIGHT_REQUIRED else NOT_YET_CODED,
                         None, None, None, None, None, None),
                    )
                elif facet["applies_to"] == "study" and name not in (study.get("facets") or {}) and postdates(facet, src):
                    # A core facet added after this record's last pass: not_yet_coded until backfilled.
                    db.execute("INSERT INTO study_facets VALUES (?,?,?,?,?,?,?,?,?)",
                               (stid, name, NOT_YET_CODED, None, None, None, None, None, None))
                    db.execute("INSERT INTO backfill VALUES (?,?,?,?)", (name, text(facet.get("since")), sid, stid))
            all_study_facets[stid] = study.get("facets") or {}
            all_study_subjects[stid] = subjects
            varies = facet_entry((study.get("facets") or {}).get("varies"))
            if "layer" in varies["value"]:
                scale = varies.get("layer_scale")
                for level in as_list((varies.get("levels") or {}).get("layer")):
                    num = None
                    for tok in str(level).replace("%", " % ").replace(",", " ").split():
                        try:
                            num = float(tok.lstrip("Ll")); break
                        except ValueError:
                            continue
                    for mid in subjects or [None]:
                        frac = None
                        if num is not None and scale == "fraction":
                            frac = num / 100 if num > 1 else num
                        elif num is not None and scale == "index" and mid and registry.get(mid, {}).get("layers"):
                            frac = num / registry[mid]["layers"]
                        db.execute("INSERT INTO study_layer_depths VALUES (?,?,?,?,?)", (stid, mid, str(level), scale, frac))

        for claim in as_list(src.get("claims")):
            cid = claim["id"]
            db.execute(
                "INSERT INTO claims VALUES (?,?,?,?,?,?,?,?)",
                (
                    cid, sid, claim["study"], text(claim.get("statement")), claim.get("evidence_kind"),
                    text((claim.get("scope") or {}).get("conditions")),
                    text(claim.get("where")), text(claim.get("note")),
                ),
            )
            scoped_models = as_list((claim.get("scope") or {}).get("models")) or study_models.get(claim["study"], [])
            claims_mem[cid] = (claim, study_facets_by_id[claim["study"]], scoped_models)
            for other in as_list(claim.get("compares")):
                db.execute("INSERT INTO claim_compares VALUES (?,?)", (cid, other))
            for var in as_list(claim.get("effect_of")):
                db.execute("INSERT INTO claim_effects VALUES (?,?)", (cid, var))
            scoped = as_list((claim.get("scope") or {}).get("models"))
            for mid in scoped or study_models.get(claim["study"], []):
                db.execute("INSERT INTO claim_models VALUES (?,?,?)", (cid, mid, int(bool(scoped))))
            for name in claim_code_facets:
                for value in facet_entry(claim.get(name))["value"]:
                    db.execute("INSERT INTO claim_codes VALUES (?,?,?)", (cid, name, value))
            about = claim.get("about") or {}
            for kind in ("models", "datasets"):
                for ref in as_list(about.get(kind)):
                    db.execute("INSERT INTO claim_about VALUES (?,?,?)", (cid, kind[:-1], ref))

        for rel in as_list(src.get("relations")):
            db.execute(
                "INSERT INTO relations VALUES (?,?,?,?,?,?,?)",
                (sid, rel.get("kind"), rel.get("from"), rel.get("to"), text(rel.get("to_external")),
                 text(rel.get("where")), text(rel.get("note"))),
            )

    # ---- Links, readings and views ----
    model_reach = {m["id"]: m.get("post_training_reached") for _, m in load_list_dir("models")}
    readings = {r["id"]: r for _, r in load_list_dir("readings")}

    def record_values(cid, study=None):
        """The claim's facet values: its study's (or, for a claim that compares, another study's) and its own."""
        claim, sfacets, _ = claims_mem[cid]
        if study and study != claim["study"]:
            sfacets = all_study_facets.get(study, {})
        out = {}
        for name, facet in facets.items():
            if facet["applies_to"] == "study":
                if name in sfacets:
                    out[name] = set(facet_entry(sfacets[name])["value"])
                elif facet.get("tier") == "interpretive":
                    out[name] = {NOT_YET_CODED}
                else:
                    out[name] = set()
            else:
                out[name] = set(facet_entry(claim.get(name))["value"])
        return out

    definitions = {d["id"]: d for _, d in load_list_dir("definitions")}

    def widen(key, allowed):
        """The allowed values and every narrower value (codebook broader:) of each."""
        out = set(allowed)
        for a in allowed:
            out |= narrower.get(key, {}).get(a, set())
        return out

    def matcher(values, study_id, models, exact=False):
        def match(key, allowed):
            if key == "comparison.closest":
                return closest_by_study.get(study_id) in allowed
            if key.startswith("model."):
                return bool(models) and all(model_reach.get(m) in allowed for m in models)
            return bool(values.get(key, set()) & (allowed if exact else widen(key, allowed)))
        return match

    def holds(expr, cid, values, substitute=None, study=None, exact=False):
        claim, _, models = claims_mem[cid]
        st = study or claim["study"]
        if study and study != claim["study"]:
            models = all_study_subjects.get(study, [])
        return evaluate(expr, matcher(values, st, models, exact), definitions, substitute)

    def matches(reading, cid):
        applies = reading.get("applies_to") or {}
        claim, _, _ = claims_mem[cid]
        targets = set(as_list(applies.get("targets")))
        if targets:
            return cid in targets or claim["study"] in targets
        return holds(applies.get("selector"), cid, record_values(cid))

    def lens(cid, reading_ids):
        """Facet values of a claim under the readings, which reading changed each facet, and reinterpretations."""
        values = record_values(cid)
        changed, notes = {}, []
        for rid in reading_ids:
            r = readings[rid]
            if not matches(r, cid):
                continue
            effect = r.get("effect") or {}
            for rc in as_list(effect.get("reclassify")):
                f, old, new = rc["facet"], rc["from"], rc["to"]
                if old in values.get(f, set()):
                    values[f] = (values[f] - {old}) | {new}
                    changed.setdefault(f, rid)
            if effect.get("reinterpret"):
                notes.append((rid, text(effect["reinterpret"])))
        return values, changed, notes

    def chain(qid):
        out = []
        while qid:
            out.append(qid); qid = qs[qid].get("parent")
        return out

    def counts(cid, qid, reading_ids, substitute=None):
        """Whether the claim counts as evidence on qid under the readings (and definition substitutions), and why not."""
        values, changed, _ = lens(cid, reading_ids)
        for anc in chain(qid):
            req = qs[anc].get("requires") or {}
            for name, allowed in req.items():
                if name == "definitions":
                    for d in as_list(allowed):
                        if not holds(d, cid, values, substitute):
                            return False, ", ".join(sorted(set(changed.values()))) or f"requires {(substitute or {}).get(d, d)} ({anc})"
                elif not (values.get(name, set()) & set(as_list(allowed))):
                    return False, changed.get(name, "requires " + anc)
        return True, None

    for rid, r in readings.items():
        effect = r.get("effect") or {}
        db.execute("INSERT INTO readings VALUES (?,?,?,?,?)",
                   (rid, r.get("status"), text(r.get("statement")), text(effect.get("reinterpret")), text(r.get("tested_by"))))
        for cid in claims_mem:
            if matches(r, cid):
                db.execute("INSERT INTO reading_matches VALUES (?,?)", (rid, cid))

    def in_frame(cid, qid):
        """False, or (True, via): via is None when the claim's own study fits the frame, else the compared study that
        does. A claim that compares two studies of its paper counts for frames on either."""
        frame = qs[qid].get("frame")
        if not frame:
            return False
        exact = bool(qs[qid].get("exact_values"))
        claim = claims_mem[cid][0]
        if holds(frame, cid, record_values(cid), exact=exact):
            return (True, None)
        for other in as_list(claim.get("compares")):
            if holds(frame, cid, record_values(cid, other), study=other, exact=exact):
                return (True, other)
        return False

    for did, d in definitions.items():
        db.execute("INSERT INTO definitions VALUES (?,?,?,?,?)",
                   (did, d.get("construct"), text(d.get("statement")), "; ".join(as_list(d.get("sources"))) or None,
                    text(d.get("not_expressible"))))
        for cid in claims_mem:
            if holds(did, cid, record_values(cid)):
                db.execute("INSERT INTO claim_definitions VALUES (?,?)", (cid, did))
    by_construct = {}
    for did, d in definitions.items():
        if d.get("construct"):
            by_construct.setdefault(d["construct"], []).append(did)
    claims_by_study = {}
    for cid, (claim, _, _) in claims_mem.items():
        claims_by_study.setdefault(claim["study"], []).append(cid)
    for stid, cids in claims_by_study.items():
        kinds = record_values(cids[0]).get("study_kind", set())
        if kinds & {"conceptual", "review"}:
            continue  # no design to test against a definition
        labels = record_values(cids[0]).get("construct", set())
        for label in sorted(labels):
            defs = by_construct.get(label)
            if defs and not any(holds(d, c, record_values(c)) for d in defs for c in cids):
                db.execute("INSERT INTO construct_mismatches VALUES (?,?,?)", (stid, label, ", ".join(defs)))

    links = []
    for _, data in load_links():
        for link in as_list(data.get("links")):
            links.append(dict(link, origin="link"))
    # auto_stance: "does X change Y?" questions take a stance from effect_presence on claims in frame-matching
    # studies whose effect_of names X. A hand-made link for the same pair wins.
    linked_pairs = {(l["claim"], l["question"]) for l in links}
    to_stance = {"present": "supports", "absent": "against", "mixed": "mixed", "inconclusive": "inconclusive"}

    def auto_stance_of(claim, mode):
        """The stance an effect takes on a question whose auto_stance says which effect counts as support:
        present (any effect), increases or decreases (that direction), improves or worsens (direction turned into an
        advantage with the claim's better). None when the claim lacks what the mode needs."""
        pres = claim.get("effect_presence")
        if mode == "present" or pres != "present":
            return to_stance.get(pres)
        d = claim.get("effect_direction")
        if d is None:
            return None
        if d == "non_monotonic":
            return "mixed"
        if mode in ("improves", "worsens"):
            if claim.get("better") not in ("higher", "lower"):
                return None
            better_now = (d == "increases") == (claim["better"] == "higher")
            good = better_now if mode == "improves" else not better_now
        else:
            good = d == mode
        return "supports" if good else "against"

    for qid, q in qs.items():
        auto = q.get("auto_stance")
        if not auto:
            continue
        mode = auto.get("supports", "present")
        for cid, (claim, _, _) in claims_mem.items():
            if (cid, qid) in linked_pairs or not (set(as_list(claim.get("effect_of"))) & set(as_list(auto.get("effect_of")))):
                continue
            fit = in_frame(cid, qid) if claim.get("effect_presence") else False
            stance = auto_stance_of(claim, mode) if fit else None
            if stance:
                links.append({"claim": cid, "question": qid, "stance": stance, "via": fit[1],
                              "note": f"from the claim's effect (auto_stance, supports: {mode})", "origin": "auto"})
    for link in links:
        cid, qid = link["claim"], link["question"]
        q = qs[qid]
        if q.get("kind", "yesno") == "which":
            values, _, _ = lens(cid, [])
            for value in sorted(values.get(q["answer_facet"], set())):
                db.execute("INSERT INTO claim_answers VALUES (?,?,?)", (cid, qid, value))
        else:
            ok, _ = counts(cid, qid, [])
            db.execute("INSERT INTO claim_questions VALUES (?,?,?,?,?,?,?)",
                       (cid, qid, link.get("stance"), int(ok), text(link.get("note")), link["origin"], link.get("via")))
    tied = {(l["claim"], l["question"]) for l in links}
    for qid in qs:
        tree_needs = sorted({n for anc in chain(qid) for n in as_list(qs[anc].get("needs"))})
        for cid in claims_mem:
            if (cid, qid) in tied:
                continue
            fit = in_frame(cid, qid)
            if fit and counts(cid, qid, [])[0]:
                vals = record_values(cid, fit[1])
                missing = [n for n in tree_needs if vals.get(n, set()) <= {NOT_YET_CODED}]
                db.execute("INSERT INTO question_candidates VALUES (?,?,?,?)", (qid, cid, ", ".join(missing) or None, fit[1]))

    # What each frame reaches through narrower values, and frames on a construct label with several definitions.
    for qid, q in qs.items():
        atoms, _ = logic_atoms(q.get("frame"))
        for key, vals in atoms:
            if not q.get("exact_values"):
                for v in vals:
                    extra = sorted(narrower.get(key, {}).get(v, set()) - {v})
                    if extra:
                        db.execute("INSERT INTO question_frame_expansions VALUES (?,?,?,?)", (qid, key, v, ", ".join(extra)))
            if key == "construct":
                for v in vals:
                    if len(by_construct.get(v, [])) > 1:
                        db.execute("INSERT INTO question_warnings VALUES (?,?,?)", (qid, "construct_several_definitions",
                                   f"frames on construct '{v}', which has definitions {', '.join(by_construct[v])}: "
                                   "frame on the definition meant, or say why the label is enough"))

    for _, v in load_list_dir("views"):
        vid, vq, rids = v["id"], v["question"], as_list(v.get("readings"))
        subst = v.get("substitute") or {}
        db.execute("INSERT INTO views VALUES (?,?,?,?,?)", (vid, vq, ", ".join(rids),
                   ", ".join(f"{a} -> {b}" for a, b in subst.items()) or None, text(v.get("note"))))
        for link in links:
            cid, lq = link["claim"], link["question"]
            if vq not in chain(lq):
                continue
            if qs[vq].get("kind", "yesno") == "which":
                if lq != vq:
                    continue
                values, _, notes = lens(cid, rids)
                for value in sorted(values.get(qs[vq]["answer_facet"], set())):
                    db.execute("INSERT INTO view_answers VALUES (?,?,?)", (vid, cid, value))
            else:
                # The stance on the view's question: flip under each inverse question on the way up; a polarity
                # none question in between cuts the link off from the view's question.
                sign, cur, cut = 1, lq, False
                while cur != vq:
                    pol = qs[cur].get("polarity", "direct")
                    if pol == "none":
                        cut = True; break
                    if pol == "inverse":
                        sign = -sign
                    cur = qs[cur]["parent"]
                if cut:
                    continue
                stance = link.get("stance")
                if sign == -1 and stance in ("supports", "against"):
                    stance = "against" if stance == "supports" else "supports"
                base_ok, _ = counts(cid, lq, [])
                ok, why = counts(cid, lq, rids, subst)
                db.execute("INSERT INTO view_evidence VALUES (?,?,?,?,?,?,?)", (vid, cid, lq, stance, int(base_ok), int(ok), why))
                _, _, notes = lens(cid, rids)
            for rid, note in notes:
                db.execute("INSERT INTO view_reinterpretations VALUES (?,?,?,?)", (vid, cid, rid, note))

    # Which-question conflicts: every pair of claims on one which-question whose answer sets differ.
    answers = {}
    for cid, qid, value in db.execute("SELECT claim, question, value FROM claim_answers"):
        answers.setdefault(qid, {}).setdefault(cid, set()).add(value)
    for qid, by_claim in answers.items():
        claims = sorted(by_claim)
        for i, a in enumerate(claims):
            for b in claims[i + 1:]:
                if by_claim[a] == by_claim[b]:
                    continue
                shared = db.execute(
                    "SELECT COUNT(*) FROM study_facets f JOIN study_facets g ON g.facet = f.facet AND g.value = f.value "
                    "JOIN claims ca ON ca.study = f.study JOIN claims cb ON cb.study = g.study "
                    "WHERE ca.id = ? AND cb.id = ? AND f.value != 'not_yet_coded'", (a, b)).fetchone()[0]
                db.execute("INSERT INTO which_conflicts VALUES (?,?,?,?,?,?)",
                           (qid, a, b, ", ".join(sorted(by_claim[a])), ", ".join(sorted(by_claim[b])), shared))

    db.commit()
    tables = ("sources", "studies", "study_facets", "claims", "questions", "models")
    summary = ", ".join(f"{db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]} {t}" for t in tables)
    db.close()
    print(f"Built {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path}: {summary}")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "build" / "self-facets.sqlite"
    sys.exit(build(target))

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
    ROOT,
    as_list,
    facet_entry,
    load_codebook,
    load_list_dir,
    load_sources,
    model_ref,
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
    disclosure TEXT, documented_in TEXT, note TEXT
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
CREATE TABLE artefacts (source TEXT, kind TEXT, arxiv TEXT, url TEXT, venue TEXT, note TEXT);
CREATE TABLE authorship (source TEXT, position INTEGER, person TEXT);
CREATE TABLE affiliations (source TEXT, person TEXT, org TEXT);
CREATE TABLE studies (id TEXT PRIMARY KEY, source TEXT, label TEXT, design TEXT, where_ TEXT, note TEXT);
CREATE TABLE study_models (study TEXT, model TEXT, role TEXT);
CREATE TABLE study_facets (
    study TEXT, facet TEXT, value TEXT, basis TEXT, author_term TEXT,
    confidence TEXT, nested_in TEXT, where_ TEXT, note TEXT
);
CREATE TABLE study_facet_levels (study TEXT, facet TEXT, value TEXT, level TEXT);
CREATE TABLE claims (
    id TEXT PRIMARY KEY, source TEXT, study TEXT, statement TEXT, question TEXT,
    stance TEXT, evidence_kind TEXT, scope_conditions TEXT, where_ TEXT, note TEXT
);
-- Every question a claim takes a stance on: its main one and any others.
CREATE TABLE claim_questions (claim TEXT, question TEXT, stance TEXT, main INTEGER);
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

-- Each stance turned into a stance on its tree's root (flipped under an inverse question).
CREATE VIEW root_stances AS
SELECT q.claim, q.question, r.root,
       CASE WHEN r.sign = -1 AND q.stance = 'supports' THEN 'against'
            WHEN r.sign = -1 AND q.stance = 'against' THEN 'supports'
            ELSE q.stance END AS stance
FROM claim_questions q JOIN question_roots r ON r.question = q.question;

-- One row per claim and facet value, with facets inherited from the study.
CREATE VIEW claim_facets AS
SELECT c.id AS claim, c.question, c.stance, f.facet, f.value
FROM claims c JOIN study_facets f ON f.study = c.study;

-- Pairs of claims that take opposite stances on the same question, or on questions in the same tree, after
-- turning each stance into one on the root (root_stances). `question` is the root.
-- `shared_facets` counts the facet values the two claims' studies have in
-- common; sort by it to see the most comparable pairs first.
CREATE VIEW conflicts AS
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
            "INSERT INTO models VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                m["id"], m.get("name"), m.get("family"), m.get("developer"), text(m.get("size")),
                None if m.get("open_weights") is None else int(m["open_weights"]),
                ", ".join(as_list(m.get("derived_from"))) or None, int(m.get("stage") is not None),
                stage.get("disclosure"), text(stage.get("documented_in")), text(m.get("note")),
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
        for art in as_list(src.get("artefacts")):
            db.execute(
                "INSERT INTO artefacts VALUES (?,?,?,?,?,?)",
                (sid, art.get("kind"), art.get("arxiv"), art.get("url"), art.get("venue"), text(art.get("note"))),
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
                mid, role = model_ref(raw)
                study_models[stid].append(mid)
                db.execute("INSERT INTO study_models VALUES (?,?,?)", (stid, mid, role))
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

        for claim in as_list(src.get("claims")):
            cid = claim["id"]
            db.execute(
                "INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    cid, sid, claim["study"], text(claim.get("statement")), claim.get("question"),
                    claim.get("stance"), claim.get("evidence_kind"),
                    text((claim.get("scope") or {}).get("conditions")),
                    text(claim.get("where")), text(claim.get("note")),
                ),
            )
            links = ([(claim["question"], claim.get("stance"), 1)] if claim.get("question") else []) + [
                (link["question"], link.get("stance"), 0) for link in as_list(claim.get("other_questions"))]
            for qid, stance, main in links:
                q = qs[qid]
                if q.get("kind", "yesno") == "which":
                    name = q["answer_facet"]
                    if facets[name]["applies_to"] == "claim":
                        values = as_list(claim.get(name))
                    else:
                        values = facet_entry((study_facets_by_id[claim["study"]]).get(name))["value"]
                    for value in values:
                        db.execute("INSERT INTO claim_answers VALUES (?,?,?)", (cid, qid, value))
                else:
                    db.execute("INSERT INTO claim_questions VALUES (?,?,?,?)", (cid, qid, stance, main))
            for other in as_list(claim.get("compares")):
                db.execute("INSERT INTO claim_compares VALUES (?,?)", (cid, other))
            for var in as_list(claim.get("effect_of")):
                db.execute("INSERT INTO claim_effects VALUES (?,?)", (cid, var))
            scoped = as_list((claim.get("scope") or {}).get("models"))
            for mid in scoped or study_models.get(claim["study"], []):
                db.execute("INSERT INTO claim_models VALUES (?,?,?)", (cid, mid, int(bool(scoped))))
            for name in claim_code_facets:
                for value in as_list(claim.get(name)):
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

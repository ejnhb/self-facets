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
CREATE TABLE codebook (facet TEXT, value TEXT, definition TEXT, rule TEXT, facet_version TEXT);
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
CREATE TABLE questions (id TEXT PRIMARY KEY, text TEXT, status TEXT, added TEXT);
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
    confidence TEXT, where_ TEXT, note TEXT
);
CREATE TABLE claims (
    id TEXT PRIMARY KEY, source TEXT, study TEXT, statement TEXT, question TEXT,
    stance TEXT, evidence_kind TEXT, where_ TEXT, note TEXT
);
CREATE TABLE claim_models (claim TEXT, model TEXT, scoped INTEGER);
CREATE TABLE claim_dispositions (claim TEXT, disposition TEXT);
CREATE TABLE claim_about (claim TEXT, kind TEXT, ref TEXT);
CREATE TABLE relations (source TEXT, kind TEXT, from_ TEXT, to_ TEXT, where_ TEXT, note TEXT);

-- One row per claim and facet value, with facets inherited from the study.
CREATE VIEW claim_facets AS
SELECT c.id AS claim, c.question, c.stance, f.facet, f.value
FROM claims c JOIN study_facets f ON f.study = c.study;

-- Pairs of claims that take opposite stances on the same question.
CREATE VIEW conflicts AS
SELECT a.question, a.id AS supports, b.id AS against
FROM claims a JOIN claims b ON a.question = b.question
WHERE a.stance = 'supports' AND b.stance = 'against';

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
    for name, facet in facets.items():
        for value, body in facet["values"].items():
            db.execute(
                "INSERT INTO codebook VALUES (?,?,?,?,?)",
                (name, value, text(body.get("definition")), text(body.get("rule")), text(facet.get("version"))),
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
                m.get("derived_from"), int(m.get("stage") is not None),
                stage.get("disclosure"), text(stage.get("documented_in")), text(m.get("note")),
            ),
        )
        for method in as_list(stage.get("methods")):
            db.execute("INSERT INTO model_stage_methods VALUES (?,?)", (m["id"], method))
        for ds in as_list(stage.get("datasets")):
            db.execute("INSERT INTO model_stage_datasets VALUES (?,?)", (m["id"], ds))

    for _, q in load_list_dir("questions"):
        db.execute(
            "INSERT INTO questions VALUES (?,?,?,?)",
            (q["id"], text(q.get("text")), q.get("status"), text(q.get("added"))),
        )

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
                        "INSERT INTO study_facets VALUES (?,?,?,?,?,?,?,?)",
                        (
                            stid, name, value, entry.get("basis"), entry.get("author_term"),
                            entry.get("confidence"), text(entry.get("where")), text(entry.get("note")),
                        ),
                    )

        for claim in as_list(src.get("claims")):
            cid = claim["id"]
            db.execute(
                "INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    cid, sid, claim["study"], text(claim.get("statement")), claim.get("question"),
                    claim.get("stance"), claim.get("evidence_kind"), text(claim.get("where")), text(claim.get("note")),
                ),
            )
            scoped = as_list((claim.get("scope") or {}).get("models"))
            for mid in scoped or study_models.get(claim["study"], []):
                db.execute("INSERT INTO claim_models VALUES (?,?,?)", (cid, mid, int(bool(scoped))))
            for disp in as_list(claim.get("disposition")):
                db.execute("INSERT INTO claim_dispositions VALUES (?,?)", (cid, disp))
            about = claim.get("about") or {}
            for kind in ("models", "datasets"):
                for ref in as_list(about.get(kind)):
                    db.execute("INSERT INTO claim_about VALUES (?,?,?)", (cid, kind[:-1], ref))

        for rel in as_list(src.get("relations")):
            db.execute(
                "INSERT INTO relations VALUES (?,?,?,?,?,?)",
                (sid, rel.get("kind"), rel.get("from"), rel.get("to"), text(rel.get("where")), text(rel.get("note"))),
            )

    db.commit()
    tables = ("sources", "studies", "study_facets", "claims", "questions", "models")
    summary = ", ".join(f"{db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]} {t}" for t in tables)
    db.close()
    print(f"Built {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path}: {summary}")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "build" / "self-facets.sqlite"
    sys.exit(build(target))

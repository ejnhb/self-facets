#!/usr/bin/env python3
"""Summarise what a change does to the evidence, against a base build. Written for the CI job summary.

Usage: python scripts/pr_summary.py BASE_DB HEAD_DB BASE_DIR HEAD_DIR
  BASE_DB, HEAD_DB: databases built from the base branch and from this branch (scripts/build.py).
  BASE_DIR, HEAD_DIR: the two checkouts, for the YAML the databases do not keep (frames, definitions, readings).

Prints Markdown: per question the change touches, links and stances added or removed, new and dropped candidates,
and new and resolved conflicts within the question as posed (with the facets the two sides differ on); then what
depends on any question or codebook value the change edits or removes; then facets awaiting backfill. Only questions
the change touches are computed, so the cost stays with the change.
"""

import sqlite3
import sys
from pathlib import Path

import yaml


def rows(db, sql, args=()):
    try:
        return db.execute(sql, args).fetchall()
    except sqlite3.Error:
        return []


def load_yaml_list(root, dirname):
    out = []
    for p in sorted((root / dirname).glob("*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        out += data if isinstance(data, list) else [data]
    return out


def load_codebook(root):
    out = {}
    for p in sorted((root / "codebook").glob("*.yaml")):
        if p.name == "enums.yaml":
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        name = data.get("facet") or data.get("vocabulary")
        if name:
            out[name] = data.get("values") or {}
    return out


def atoms(expr, acc):
    """Every (facet, value) an expression tests."""
    if isinstance(expr, list):
        for e in expr:
            atoms(e, acc)
    elif isinstance(expr, dict):
        for k, v in expr.items():
            if k in ("all", "any"):
                atoms(v, acc)
            elif k == "not":
                atoms(v, acc)
            elif k != "def":
                for x in v if isinstance(v, list) else [v]:
                    acc.add((k, x))
    return acc


def links(db):
    return {(c, q): s for c, q, s in rows(db, "SELECT claim, question, stance FROM claim_questions")}


def counted(db):
    return {(c, q): s for c, q, s in rows(db, "SELECT claim, question, stance FROM claim_questions WHERE counted = 1")}


def candidates(db):
    return {(q, c) for q, c in rows(db, "SELECT question, claim FROM question_candidates")}


def conflicts(cnt):
    by_q = {}
    for (c, q), s in cnt.items():
        by_q.setdefault(q, {}).setdefault(s, set()).add(c)
    out = set()
    for q, st in by_q.items():
        for a in st.get("supports", ()):
            for b in st.get("against", ()):
                out.add((q, a, b))
    return out


def facet_diff(db, a, b, limit=6):
    """Facet values one claim's study has and the other's lacks (head build)."""
    def vals(cid):
        return set(rows(db, "SELECT f.facet, f.value FROM study_facets f JOIN claims c ON c.study = f.study "
                            "WHERE c.id = ? AND f.value != 'not_yet_coded'", (cid,)))
    va, vb = vals(a), vals(b)
    only_a = sorted({f for f, _ in va - vb} | {f for f, _ in vb - va})
    return ", ".join(only_a[:limit]) + (" ..." if len(only_a) > limit else "")


def main(base_db, head_db, base_dir, head_dir):
    base, head = sqlite3.connect(base_db), sqlite3.connect(head_db)
    base_dir, head_dir = Path(base_dir), Path(head_dir)
    out = ["## What this change does to the evidence", ""]

    tables = ("sources", "studies", "claims", "questions", "claim_questions")
    counts = []
    for t in tables:
        b = (rows(base, f"SELECT COUNT(*) FROM {t}") or [(0,)])[0][0]
        h = (rows(head, f"SELECT COUNT(*) FROM {t}") or [(0,)])[0][0]
        counts.append(f"{t.replace('claim_questions', 'links')} {b} → {h}" if b != h else f"{t.replace('claim_questions', 'links')} {h}")
    out += ["Counts: " + "; ".join(counts) + ".", ""]

    bl, hl = links(base), links(head)
    bc, hc = candidates(base), candidates(head)
    bx, hx = conflicts(counted(base)), conflicts(counted(head))

    # Questions the YAML change edits.
    bq = {q["id"]: q for q in load_yaml_list(base_dir, "questions")}
    hq = {q["id"]: q for q in load_yaml_list(head_dir, "questions")}
    edited_q = sorted(q for q in set(bq) | set(hq) if bq.get(q) != hq.get(q))

    touched = set(edited_q)
    touched |= {q for (c, q) in set(bl) ^ set(hl)} | {q for k in set(bl) & set(hl) if bl[k] != hl[k] for (_, q) in [k]}
    touched |= {q for (q, c) in bc ^ hc} | {q for (q, _, _) in bx ^ hx}

    if not touched:
        out += ["No question's links, candidates or conflicts change.", ""]
    for q in sorted(touched):
        lines = []
        added = sorted(k for k in hl if k[1] == q and k not in bl)
        removed = sorted(k for k in bl if k[1] == q and k not in hl)
        changed = sorted(k for k in hl if k[1] == q and k in bl and bl[k] != hl[k])
        for c, _ in added:
            lines.append(f"- link added: `{c}` ({hl[(c, q)]})")
        for c, _ in removed:
            lines.append(f"- link removed: `{c}` (was {bl[(c, q)]})")
        for c, _ in changed:
            lines.append(f"- stance changed: `{c}` {bl[(c, q)]} → {hl[(c, q)]}")
        new_c = sorted(c for (qq, c) in hc - bc if qq == q)
        gone_c = sorted(c for (qq, c) in bc - hc if qq == q)
        if new_c:
            lines.append(f"- new candidates ({len(new_c)}): " + ", ".join(f"`{c}`" for c in new_c[:12]) + (" ..." if len(new_c) > 12 else ""))
        if gone_c:
            lines.append(f"- no longer candidates ({len(gone_c)}): " + ", ".join(f"`{c}`" for c in gone_c[:12]) + (" ..." if len(gone_c) > 12 else ""))
        for (_, a, b) in sorted(x for x in hx - bx if x[0] == q):
            lines.append(f"- new conflict: `{a}` supports, `{b}` against; they differ on: {facet_diff(head, a, b) or 'nothing coded'}")
        for (_, a, b) in sorted(x for x in bx - hx if x[0] == q):
            lines.append(f"- conflict gone: `{a}` against `{b}`")
        for kind, detail in rows(head, "SELECT kind, detail FROM question_warnings WHERE question = ?", (q,)):
            lines.append(f"- warning ({kind}): {detail}")
        if q in edited_q:
            what = "added" if q not in bq else "removed" if q not in hq else "edited"
            lines.append(f"- the question itself is {what}")
        if lines:
            out += [f"### `{q}`", ""] + lines + [""]

    # What depends on a changed or removed question or codebook value.
    impact = []
    for q in edited_q:
        if q in bq and q in hq:
            n_links = sum(1 for (c, qq) in hl if qq == q)
            kids = [k for k, v in hq.items() if v.get("parent") == q]
            impact.append(f"- question `{q}` edited: {n_links} links and {len(kids)} child questions rest on it; "
                          "check the links still mean what their poser meant")
        elif q in bq:
            impact.append(f"- question `{q}` removed")
    bcb, hcb = load_codebook(base_dir), load_codebook(head_dir)
    dependants = {}
    for kind, items in (("question", load_yaml_list(head_dir, "questions")), ("definition", load_yaml_list(head_dir, "definitions")),
                        ("reading", load_yaml_list(head_dir, "readings"))):
        for it in items:
            expr = it.get("frame") if kind == "question" else it.get("logic") if kind == "definition" else (it.get("applies_to") or {}).get("selector")
            for fv in atoms(expr, set()):
                dependants.setdefault(fv, []).append(f"{kind} `{it.get('id')}`")
            if kind == "question":
                for f, vs in (it.get("requires") or {}).items():
                    if f != "definitions":
                        for v in vs if isinstance(vs, list) else [vs]:
                            dependants.setdefault((f, v), []).append(f"question `{it.get('id')}` (requires)")
    for facet in sorted(set(bcb) | set(hcb)):
        for value in sorted(set(bcb.get(facet, {})) | set(hcb.get(facet, {}))):
            b, h = bcb.get(facet, {}).get(value), hcb.get(facet, {}).get(value)
            if b is None or b == h:
                continue
            what = "removed" if h is None else "redefined"
            n_studies = (rows(head, "SELECT COUNT(DISTINCT study) FROM study_facets WHERE facet = ? AND value = ?", (facet, value)) or [(0,)])[0][0]
            deps = dependants.get((facet, value), [])
            impact.append(f"- `{facet}: {value}` {what}: coded on {n_studies} studies"
                          + (f"; used by {', '.join(sorted(set(deps)))}" if deps else ""))
    if impact:
        out += ["### What depends on what this change edits", ""] + impact + [""]

    backfill = rows(head, "SELECT facet, since, COUNT(DISTINCT source), COUNT(*) FROM backfill GROUP BY facet, since")
    if backfill:
        out += ["### Awaiting backfill", ""] + [f"- `{f}` (since {s}): {n_src} records, {n_st} studies" for f, s, n_src, n_st in backfill] + [""]

    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    main(*sys.argv[1:])

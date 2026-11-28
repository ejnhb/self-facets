"""Shared loading code for validate.py and build.py."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Accepted on every study facet in addition to the values in its codebook file.
SPECIAL = {"unspecified", "not_applicable"}
# An interpretive facet nobody has coded yet (left out of the record, or written explicitly).
NOT_YET_CODED = "not_yet_coded"
# Study facets a conceptual or review study must code.
LIGHT_REQUIRED = ("study_kind", "self_sense", "construct")

# Keys allowed in the long form of a coded study facet.
LONG_FORM_KEYS = {"value", "basis", "author_term", "where", "confidence", "note", "nested_in", "levels",
                  "excluded", "layer_scale"}
# Keys allowed on one value in the per-value long form: value: [{value, basis, where}, ...] (codebook 0.11).
PER_VALUE_KEYS = {"value", "basis", "where", "confidence", "author_term", "note"}


def version_key(v):
    """'0.10' -> (0, 10), so codebook versions compare as numbers."""
    try:
        return tuple(int(x) for x in str(v).split("."))
    except ValueError:
        return (0,)


def record_version(src):
    """The latest codebook version a record was coded or changed against (its passes)."""
    passes = ((src.get("coding") or {}).get("passes")) or []
    vs = [version_key(p.get("codebook")) for p in passes if isinstance(p, dict) and p.get("codebook")]
    return max(vs) if vs else (0,)


def postdates(facet, src):
    """True when the facet was added after the record's latest pass, so its absence reads as not_yet_coded."""
    since = facet.get("since")
    return bool(since) and version_key(since) > record_version(src)


def read_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def yaml_files(dirname):
    return sorted((ROOT / dirname).glob("*.yaml"))


def load_list_dir(dirname):
    """Concatenate the top-level lists of every YAML file in a directory."""
    items = []
    for path in yaml_files(dirname):
        data = read_yaml(path) or []
        if not isinstance(data, list):
            raise ValueError(f"{path.relative_to(ROOT)}: expected a list at top level")
        for item in data:
            items.append((path.relative_to(ROOT), item))
    return items


def load_links():
    """Every links file: (path, data). One file per source, named after it."""
    return [(path, read_yaml(path) or {}) for path in yaml_files("links")]


def load_codebook():
    """Return (facets, enums).

    facets: name -> {applies_to, cardinality, required, values: {value: {...}}}
    enums:  name -> {value: definition}

    A facet file either lists its own values or names a shared vocabulary file
    with `values_from`, in which case the vocabulary's values are attached.
    """
    facets, enums, vocabularies = {}, {}, {}
    for path in yaml_files("codebook"):
        data = read_yaml(path) or {}
        if "facet" in data:
            facets[data["facet"]] = data
        elif "enums" in data:
            enums.update(data["enums"])
        elif "vocabulary" in data:
            vocabularies[data["vocabulary"]] = data
        else:
            raise ValueError(f"{path.relative_to(ROOT)}: not a facet, vocabulary or enums file")
    for name, facet in facets.items():
        source = facet.get("values_from")
        if source:
            if source not in vocabularies:
                raise ValueError(f"codebook/{name}.yaml: values_from '{source}' is not a vocabulary")
            facet["values"] = vocabularies[source]["values"]
    return facets, enums


def load_sources():
    return [(p.relative_to(ROOT), read_yaml(p)) for p in yaml_files("sources")]


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def facet_entry(raw):
    """Normalise a coded facet to its long form.

    Accepts a scalar, a list, or a mapping with a `value` key.
    """
    if isinstance(raw, dict):
        entry = dict(raw)
        items = as_list(entry.get("value"))
    else:
        entry, items = {}, as_list(raw)
    # Per-value long form: each value may carry its own basis, where and confidence.
    per_value = {}
    values = []
    for item in items:
        if isinstance(item, dict):
            values.append(item.get("value"))
            per_value[item.get("value")] = item
        else:
            values.append(item)
    entry["value"] = values
    if per_value:
        entry["per_value"] = per_value
    return entry


def model_ref(raw):
    """Normalise a study's model reference to (id, roles, note). A bare id is a subject."""
    if isinstance(raw, dict):
        return raw.get("id"), as_list(raw.get("roles")) or ["subject"], raw.get("note")
    return raw, ["subject"], None


# How closely two registered models are related, closest first (build: study_comparisons).
RELATIONS = ["same", "variant", "derived", "same_family", "same_developer", "other"]


def relation(a, b, models):
    """The relation between two model ids, from the registry's variant_of, derived_from, family and developer."""
    if a == b:
        return "same"
    ma, mb = models.get(a, {}), models.get(b, {})
    if ma.get("variant_of") == b or mb.get("variant_of") == a or (
            ma.get("variant_of") and ma.get("variant_of") == mb.get("variant_of")):
        return "variant"
    if b in as_list(ma.get("derived_from")) or a in as_list(mb.get("derived_from")):
        return "derived"
    if ma.get("family") and ma.get("family") == mb.get("family"):
        return "same_family"
    if ma.get("developer") and ma.get("developer") == mb.get("developer"):
        return "same_developer"
    return "other"


# Logic over facets, shared by frames, selectors, requires and definitions.
# An expression is a definition id (string), or a mapping whose keys are joined by AND:
#   all: [expr, ...]   any: [expr, ...]   not: expr   def: id or [ids]
#   FACET: [values]    (the record shares a value; model.FIELD and comparison.closest too)
LOGIC_KEYS = ("all", "any", "not", "def")


def evaluate(expr, match, definitions, substitute=None, _seen=()):
    """True if the expression holds. match(key, allowed) tests one facet or field; substitute swaps definitions."""
    substitute = substitute or {}
    if expr is None:
        return True
    if isinstance(expr, str):
        did = substitute.get(expr, expr)
        if did in _seen:
            raise ValueError(f"definition '{did}' refers to itself")
        return evaluate((definitions[did] or {}).get("logic"), match, definitions, substitute, _seen + (did,))
    if isinstance(expr, list):
        return all(evaluate(e, match, definitions, substitute, _seen) for e in expr)
    for key, val in expr.items():
        if key == "all":
            ok = all(evaluate(e, match, definitions, substitute, _seen) for e in as_list(val))
        elif key == "any":
            ok = any(evaluate(e, match, definitions, substitute, _seen) for e in as_list(val))
        elif key == "not":
            ok = not evaluate(val, match, definitions, substitute, _seen)
        elif key == "def":
            ok = all(evaluate(d, match, definitions, substitute, _seen) for d in as_list(val))
        else:
            ok = match(key, set(as_list(val)))
        if not ok:
            return False
    return True


def narrower_map(facets):
    """facet -> value -> that value and every value that declares it (transitively) as broader."""
    out = {}
    for name, facet in facets.items():
        vals = facet.get("values") or {}
        children = {}
        for v, body in vals.items():
            b = body.get("broader") if isinstance(body, dict) else None
            if b:
                children.setdefault(b, set()).add(v)
        if not children:
            continue
        m = {}
        for v in vals:
            seen, stack = {v}, [v]
            while stack:
                for c in children.get(stack.pop(), ()):
                    if c not in seen:
                        seen.add(c); stack.append(c)
            if len(seen) > 1:
                m[v] = seen
        if m:
            out[name] = m
    return out


def logic_atoms(expr):
    """Every (key, values) test and every definition id an expression uses, for validation."""
    atoms, defs = [], []
    if expr is None:
        return atoms, defs
    if isinstance(expr, str):
        return atoms, [expr]
    if isinstance(expr, list):
        for e in expr:
            a, d = logic_atoms(e); atoms += a; defs += d
        return atoms, defs
    for key, val in expr.items():
        if key in ("all", "any"):
            for e in as_list(val):
                a, d = logic_atoms(e); atoms += a; defs += d
        elif key == "not":
            a, d = logic_atoms(val); atoms += a; defs += d
        elif key == "def":
            defs += as_list(val)
        else:
            atoms.append((key, as_list(val)))
    return atoms, defs

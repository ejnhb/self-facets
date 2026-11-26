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
LONG_FORM_KEYS = {"value", "basis", "author_term", "where", "confidence", "note", "nested_in", "levels"}


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
        entry["value"] = as_list(entry.get("value"))
        return entry
    return {"value": as_list(raw)}


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

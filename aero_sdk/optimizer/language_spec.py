"""
Language Spec I/O
=================

Load, validate and serialize ``language_spec.json`` documents — the
data-driven description of the Aero lexer's keyword / operator /
punctuation tables.

The spec is the single knob the optimizer turns: re-ordering the
``operators`` array (longest-match-first is always preserved) and the
``preference_levels`` map is what lets a refined lexer shave comparisons
out of its hot scanning loop.
"""

import json
import os

# Required top-level keys every spec document must carry.
_REQUIRED_KEYS = (
    "keywords",
    "booleans",
    "operators",
    "punctuation",
    "preference_levels",
    "custom_errors",
)


class SpecError(Exception):
    """Raised when a language_spec.json document is structurally invalid."""


def load_spec(path):
    """Load and validate a language_spec.json document from ``path``."""
    with open(path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    validate_spec(spec)
    return spec


def dump_spec(spec, path):
    """Serialize ``spec`` to ``path`` as pretty-printed JSON.

    Parent directories are created as needed so callers can target a fresh
    sandbox location (e.g. ``build_sandbox/config/``) without pre-scaffolding.
    """
    validate_spec(spec)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        f.write("\n")


def validate_spec(spec):
    """Assert that ``spec`` carries the structural shape the lexer needs.

    This guards correctness: in particular, every multi-character operator
    must still be matchable before its single-character prefixes, which the
    generator guarantees by sorting longest-first regardless of array order.
    """
    if not isinstance(spec, dict):
        raise SpecError(f"spec must be an object, got {type(spec).__name__}")
    for key in _REQUIRED_KEYS:
        if key not in spec:
            raise SpecError(f"spec is missing required key: {key!r}")
    for key in ("keywords", "booleans", "operators", "punctuation"):
        if not isinstance(spec[key], list):
            raise SpecError(f"spec[{key!r}] must be a list")
    if not isinstance(spec["preference_levels"], dict):
        raise SpecError("spec['preference_levels'] must be an object")
    if not isinstance(spec["custom_errors"], dict):
        raise SpecError("spec['custom_errors'] must be an object")
    # No operator may be empty (the scanner would loop forever on it).
    if any(not op for op in spec["operators"]):
        raise SpecError("spec['operators'] contains an empty operator")
    return True


def spec_token_universe(spec):
    """Return the set of all operator + keyword symbols the spec defines.

    Used by the analyzer to decide which symbols are worth counting.
    """
    return set(spec["operators"]) | set(spec["keywords"])

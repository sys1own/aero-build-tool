"""
Refined Builder Generator
=========================

Renders a concrete lexer ("builder") from a ``language_spec.json`` document.

The Aero ``lexer.py`` has always *claimed* to be "generated from
config/language_spec.json" — this module makes that real. It takes the live
lexer as a structural skeleton and swaps out only the language-tables block,
emitting the operator list in the spec's (frequency-tuned) order while
keeping the proven scanning logic untouched.

Correctness: the optimizer hands us operators already sorted longest-first,
and we assert that invariant here before emitting, so the generated scanner
can never mis-tokenize a multi-character operator as its prefix.
"""

import os

from aero_sdk.optimizer import language_spec as spec_io

_TABLES_MARKER = "# ── Language Tables"
_CLASS_ANCHOR = "\nclass Lexer:"


def load_skeleton(lexer_path):
    """Read the structural lexer skeleton (the live, tested scanner)."""
    with open(lexer_path, "r", encoding="utf-8") as f:
        return f.read()


def _set_literal(items):
    if not items:
        return "set()"
    return "{" + ", ".join(repr(x) for x in items) + "}"


def _list_literal(items):
    return "[" + ", ".join(repr(x) for x in items) + "]"


def _dict_literal(d):
    if not d:
        return "{}"
    return "{" + ", ".join(f"{k!r}: {v!r}" for k, v in d.items()) + "}"


def _assert_longest_first(operators):
    """No operator may appear before a longer operator (would break matching)."""
    for i, op in enumerate(operators):
        for longer in operators[i + 1:]:
            if len(longer) > len(op):
                raise spec_io.SpecError(
                    "operator order violates longest-match-first: "
                    f"{op!r} precedes longer {longer!r}"
                )


def render_tables_block(spec):
    """Render the ``# ── Language Tables`` source block from ``spec``."""
    spec_io.validate_spec(spec)
    operators = list(spec["operators"])
    _assert_longest_first(operators)
    lines = [
        "# ── Language Tables (generated from config/language_spec.json "
        "by aero_sdk.optimizer.generator) ──",
        f"_KEYWORDS = {_set_literal(spec['keywords'])}",
        f"_BOOLEANS = {_set_literal(spec['booleans'])}",
        f"_OPERATORS = {_list_literal(operators)}",
        f"_PUNCTUATION = {_set_literal(spec['punctuation'])}",
        f"_CUSTOM_ERRORS = {_dict_literal(spec['custom_errors'])}",
    ]
    return "\n".join(lines)


def render_lexer(spec, skeleton_source):
    """Return refined lexer source: skeleton with its tables block swapped."""
    start = skeleton_source.find(_TABLES_MARKER)
    end = skeleton_source.find(_CLASS_ANCHOR)
    if start == -1 or end == -1 or start >= end:
        raise spec_io.SpecError(
            "could not locate the language-tables block in the lexer skeleton"
        )
    head = skeleton_source[:start].rstrip() + "\n\n"
    tail = skeleton_source[end:].lstrip("\n")
    block = render_tables_block(spec)
    return head + block + "\n\n\n" + tail


def render_lexer_file(spec, skeleton_path, out_path):
    """Generate a refined lexer from ``spec`` and write it to ``out_path``."""
    skeleton = load_skeleton(skeleton_path)
    source = render_lexer(spec, skeleton)
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(source)
    return out_path

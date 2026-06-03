"""
Analyst Engine — Data-Driven Spec Optimization
==============================================

Looks at the character / operator / keyword frequencies of a corpus of
Aero source files and produces a *refined* language spec in which the
hot tables are re-ordered so the most common symbols are matched first.

Honesty notes (what actually moves the needle):
  * Operators are matched by a linear scan in the lexer, so re-ordering
    them so frequent operators come first genuinely removes comparisons
    from the scanning loop. The longest-match-first invariant is always
    preserved (length is the primary sort key), so correctness is safe.
  * Keywords and punctuation are matched via O(1) set membership, so
    re-ordering them is cosmetic for performance. We still surface their
    frequencies (and order keywords by them) for analysis, but we do not
    claim a speed-up there.
"""

import os
from collections import Counter

from aero_sdk.optimizer import language_spec as spec_io

# Word pattern for keyword/identifier counting.
_WORD_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


def read_corpus(paths):
    """Read and concatenate every readable source path into one blob.

    Missing paths are skipped silently so the caller can pass an optimistic
    list (e.g. files that only exist after a build).
    """
    chunks = []
    for p in paths:
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                chunks.append(f.read())
    return "\n".join(chunks)


def default_corpus_paths(repo_root):
    """The source files we tune against: the Aero programs we actually compile."""
    return [
        os.path.join(repo_root, "src", "app.aero"),
        os.path.join(repo_root, "aero_build.aero"),
    ]


def strip_noncode(text):
    """Remove the regions the lexer skips *before* operator matching.

    Line comments, block comments and string-literal bodies are consumed by
    dedicated branches in the scanner and never reach the operator-matching
    loop. Counting operator characters inside them would skew the tuning
    signal (e.g. a ``// ====`` banner is not 200 ``==`` operators), so we
    drop them before measuring code frequencies.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":  # line comment
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":  # block comment
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        if c in ('"', "'"):  # string literal body
            quote = c
            i += 1
            while i < n and text[i] != quote:
                i += 1
            i += 1  # consume closing quote (or run off the end)
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _scan_operator_counts(text, operators):
    """Greedy longest-match-first scan counting non-overlapping operators.

    This mirrors how the lexer consumes operators, so the resulting counts
    are exactly the frequencies that drive the scanning loop (e.g. a '=='
    is counted once, not as two '=' hits).
    """
    ops_by_len = sorted(set(operators), key=lambda o: -len(o))
    counts = Counter({op: 0 for op in operators})
    i, n = 0, len(text)
    while i < n:
        match = None
        for op in ops_by_len:
            if text.startswith(op, i):
                match = op
                break
        if match:
            counts[match] += 1
            i += len(match)
        else:
            i += 1
    return counts


def _scan_word_counts(text):
    """Count whitespace/symbol-delimited words (for keyword frequency)."""
    counts = Counter()
    word = []
    for ch in text:
        if ch in _WORD_CHARS:
            word.append(ch)
        elif word:
            counts["".join(word)] += 1
            word = []
    if word:
        counts["".join(word)] += 1
    return counts


def analyze_frequencies(spec, corpus):
    """Return frequency statistics for ``corpus`` against ``spec``'s tables.

    Operator and keyword counts are taken over *code only* (comments and
    string bodies stripped), because those are the only characters that
    actually reach the scanner's operator-matching loop. The raw character
    histogram is reported separately for reference.
    """
    code = strip_noncode(corpus)
    char_counts = Counter(corpus)
    operator_counts = _scan_operator_counts(code, spec["operators"])
    word_counts = _scan_word_counts(code)
    keyword_counts = Counter({kw: word_counts.get(kw, 0) for kw in spec["keywords"]})
    return {
        "corpus_chars": len(corpus),
        "code_chars": len(code),
        "char_counts": dict(char_counts),
        "operator_counts": dict(operator_counts),
        "keyword_counts": dict(keyword_counts),
    }


def optimize_spec(baseline, freq):
    """Produce a refined spec re-ordered by observed frequency.

    Returns ``(optimized_spec, report)``. The optimized spec is a deep-ish
    copy of ``baseline`` with ``operators``, ``keywords`` and
    ``preference_levels`` re-derived from ``freq``; all other tables are
    carried through unchanged.
    """
    spec_io.validate_spec(baseline)
    op_counts = freq["operator_counts"]
    kw_counts = freq["keyword_counts"]

    # Operators: longest-match-first (primary), then most-frequent-first.
    # Stable tie-break on the baseline order keeps output deterministic.
    base_order = {op: i for i, op in enumerate(baseline["operators"])}
    optimized_ops = sorted(
        baseline["operators"],
        key=lambda op: (-len(op), -op_counts.get(op, 0), base_order[op]),
    )

    # Preference levels record the data: higher frequency => higher
    # preference, so a template-style lexer reproduces the same ordering.
    preference_levels = {op: int(op_counts.get(op, 0)) for op in baseline["operators"]}

    # Keywords: ordered by frequency (informational; lookup is O(1) set).
    optimized_keywords = sorted(
        baseline["keywords"],
        key=lambda kw: (-kw_counts.get(kw, 0), kw),
    )

    optimized = dict(baseline)
    optimized["operators"] = optimized_ops
    optimized["keywords"] = optimized_keywords
    optimized["preference_levels"] = preference_levels
    optimized["booleans"] = list(baseline["booleans"])
    optimized["punctuation"] = list(baseline["punctuation"])
    optimized["custom_errors"] = dict(baseline["custom_errors"])
    optimized["description"] = (
        "EXPERIMENTAL frequency-tuned spec generated by the Aero optimizer. "
        "Sandbox-only artifact; do not promote into root config without a "
        "benchmark win."
    )

    report = {
        "operators_before": list(baseline["operators"]),
        "operators_after": optimized_ops,
        "operator_counts": op_counts,
        "keyword_counts": kw_counts,
        "operators_reordered": optimized_ops != list(baseline["operators"]),
        "keywords_reordered": optimized_keywords != list(baseline["keywords"]),
    }
    return optimized, report

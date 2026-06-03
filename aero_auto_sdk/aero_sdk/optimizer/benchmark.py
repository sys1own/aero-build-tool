"""
Benchmarking Engine
===================

Two measurements, both scoped to the self-replication sandbox:

  1. ``run_compiler_suite`` runs the compiler unit tests against the
     *sandboxed* compiler (via the isolated subprocess runner) and reports
     pass/fail + the assertion count.

  2. ``time_tokenization`` times how long a given lexer takes to tokenize a
     corpus. Lexer variants are loaded directly from their ``.py`` files
     under unique module names, so baseline and refined builders coexist in
     one process without clashing.
"""

import importlib.util
import os
import re
import subprocess
import sys
import time

_RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_sandbox_test_runner.py")
_ASSERTIONS_RE = re.compile(r"ALL\s+(\d+)\s+ASSERTIONS PASSED")


def run_compiler_suite(sandbox_compiler_dir, repo_root):
    """Run the compiler unit suite against the sandbox compiler in a subprocess."""
    proc = subprocess.run(
        [sys.executable, _RUNNER, sandbox_compiler_dir, repo_root],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    m = _ASSERTIONS_RE.search(out)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "assertions": int(m.group(1)) if m else None,
        "output": out,
    }


_variant_counter = 0


def load_lexer_module(lexer_path):
    """Load a lexer ``.py`` file as a fresh, uniquely-named module."""
    global _variant_counter
    _variant_counter += 1
    mod_name = f"_aero_lexer_variant_{_variant_counter}"
    spec = importlib.util.spec_from_file_location(mod_name, lexer_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def time_tokenization(lexer_path, corpus, iterations=400, repeats=7):
    """Time ``iterations`` tokenizations of ``corpus`` with the lexer at path.

    Returns best/mean wall-clock milliseconds over ``repeats`` rounds. Best
    is the headline number (least affected by scheduler noise).
    """
    mod = load_lexer_module(lexer_path)
    tokenize = mod.tokenize

    token_count = len(tokenize(corpus))  # correctness probe + warmup
    best = float("inf")
    total = 0.0
    for _ in range(repeats):
        t0 = time.perf_counter()
        for _ in range(iterations):
            tokenize(corpus)
        dt = (time.perf_counter() - t0) * 1000.0
        best = min(best, dt)
        total += dt
    return {
        "lexer_path": lexer_path,
        "iterations": iterations,
        "repeats": repeats,
        "tokens_per_pass": token_count,
        "best_ms": best,
        "mean_ms": total / repeats,
    }

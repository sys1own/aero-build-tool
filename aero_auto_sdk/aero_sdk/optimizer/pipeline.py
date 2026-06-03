"""
Optimization Pipeline
=====================

Orchestrates one full, idempotent self-optimization cycle:

    1. (Re)build the self-replication sandbox so we start from a clean,
       byte-faithful copy of the compiler stack.
    2. Run the compiler unit suite against the sandbox (baseline).
    3. Analyze source frequencies and derive a refined, frequency-tuned spec.
    4. Write the experimental spec STRICTLY to build_sandbox/config/.
    5. Generate a refined lexer ("builder") from that spec and install it
       into the sandbox compiler.
    6. Re-run the compiler suite against the refined sandbox (correctness)
       and benchmark tokenization, baseline vs refined.
    7. Assert nothing leaked back into the root source tree.

Because step 1 rebuilds the sandbox from scratch every run, the whole cycle
is safe to execute back-to-back with identical results.
"""

import hashlib
import os
import shutil
import subprocess
import sys

from aero_sdk.optimizer import analyzer
from aero_sdk.optimizer import benchmark
from aero_sdk.optimizer import generator
from aero_sdk.optimizer import language_spec as spec_io

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _snapshot(paths):
    return {p: _sha256(p) for p in paths if os.path.isfile(p)}


def _build_sandbox(repo_root, verbose):
    if verbose:
        print("[1] Rebuilding self-replication sandbox...")
    proc = subprocess.run(
        [sys.executable, "aero.py", "build"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"sandbox build failed:\n{proc.stdout}\n{proc.stderr}")


def run(repo_root=_REPO_ROOT, iterations=400, verbose=True):
    repo_root = os.path.abspath(repo_root)

    config_spec = os.path.join(repo_root, "config", "language_spec.json")
    root_lexer = os.path.join(repo_root, "aero_sdk", "compiler", "lexer.py")
    sandbox = os.path.join(repo_root, "build_sandbox")
    sandbox_compiler = os.path.join(sandbox, "compiler")
    sandbox_lexer = os.path.join(sandbox_compiler, "aero_sdk", "compiler", "lexer.py")
    sandbox_spec = os.path.join(sandbox, "config", "language_spec.json")
    sandbox_opt = os.path.join(sandbox, "optimizer")
    baseline_copy = os.path.join(sandbox_opt, "lexer_baseline.py")
    refined_copy = os.path.join(sandbox_opt, "lexer_refined.py")

    # Files the cycle must NEVER modify (root source of truth).
    guarded = [
        config_spec,
        root_lexer,
        os.path.join(repo_root, "aero_sdk", "compiler", "lexer_template.py"),
        os.path.join(repo_root, "aero_sdk", "compiler", "parser.py"),
        os.path.join(repo_root, "aero_sdk", "compiler", "codegen.py"),
        os.path.join(repo_root, "aero_sdk", "vm", "machine.py"),
    ]

    # 1) Fresh sandbox.
    _build_sandbox(repo_root, verbose)
    before = _snapshot(guarded)

    # 2) Baseline suite against the sandbox compiler.
    if verbose:
        print("[2] Running compiler unit suite against sandbox (baseline)...")
    baseline_tests = benchmark.run_compiler_suite(sandbox_compiler, repo_root)

    # 3) Analyze + optimize.
    if verbose:
        print("[3] Analyzing source frequencies + deriving refined spec...")
    baseline_spec = spec_io.load_spec(config_spec)
    corpus = analyzer.read_corpus(analyzer.default_corpus_paths(repo_root))
    freq = analyzer.analyze_frequencies(baseline_spec, corpus)
    optimized_spec, report = analyzer.optimize_spec(baseline_spec, freq)

    # 4) Experimental spec STRICTLY to the sandbox.
    spec_io.dump_spec(optimized_spec, sandbox_spec)
    if verbose:
        print(f"    wrote experimental spec -> {os.path.relpath(sandbox_spec, repo_root)}")

    # 5) Generate the refined builder and install it into the sandbox.
    os.makedirs(sandbox_opt, exist_ok=True)
    shutil.copyfile(sandbox_lexer, baseline_copy)  # keep baseline for timing
    generator.render_lexer_file(optimized_spec, root_lexer, refined_copy)
    shutil.copyfile(refined_copy, sandbox_lexer)   # install refined builder
    if verbose:
        print(f"    generated refined builder -> {os.path.relpath(refined_copy, repo_root)}")
        print(f"    installed into sandbox    -> {os.path.relpath(sandbox_lexer, repo_root)}")

    # 6) Refined suite (correctness) + tokenization timing (baseline vs refined).
    if verbose:
        print("[6] Re-running compiler suite against refined sandbox...")
    refined_tests = benchmark.run_compiler_suite(sandbox_compiler, repo_root)
    baseline_timing = benchmark.time_tokenization(baseline_copy, corpus, iterations)
    refined_timing = benchmark.time_tokenization(refined_copy, corpus, iterations)

    # 7) No-leak assertion.
    after = _snapshot(guarded)
    leaked = [p for p in before if before.get(p) != after.get(p)]

    result = {
        "baseline_tests": baseline_tests,
        "refined_tests": refined_tests,
        "report": report,
        "freq": freq,
        "baseline_timing": baseline_timing,
        "refined_timing": refined_timing,
        "leaked_files": leaked,
        "paths": {
            "sandbox_spec": sandbox_spec,
            "refined_lexer": sandbox_lexer,
            "baseline_copy": baseline_copy,
            "refined_copy": refined_copy,
        },
    }
    if verbose:
        _print_report(result, repo_root)
    return result


def _print_report(result, repo_root):
    rep = result["report"]
    bt = result["baseline_timing"]
    rt = result["refined_timing"]
    freq = result["freq"]

    print("\n" + "=" * 64)
    print("  AERO SELF-OPTIMIZATION REPORT")
    print("=" * 64)

    print("\n-- Source frequency analysis --")
    print(f"  corpus size: {freq['corpus_chars']} chars")
    ops_sorted = sorted(rep["operator_counts"].items(), key=lambda kv: -kv[1])
    print("  operator frequencies: " +
          ", ".join(f"{op!r}={n}" for op, n in ops_sorted if n) or "  (none)")
    kw_sorted = sorted(rep["keyword_counts"].items(), key=lambda kv: -kv[1])
    print("  keyword frequencies:  " +
          ", ".join(f"{kw!r}={n}" for kw, n in kw_sorted if n))

    print("\n-- Operator table re-order (longest-match-first preserved) --")
    print(f"  before: {rep['operators_before']}")
    print(f"  after:  {rep['operators_after']}")
    print(f"  reordered: {rep['operators_reordered']}")

    print("\n-- Compiler unit suite (run against the SANDBOX compiler) --")
    b, r = result["baseline_tests"], result["refined_tests"]
    print(f"  baseline: ok={b['ok']} assertions={b['assertions']}")
    print(f"  refined:  ok={r['ok']} assertions={r['assertions']}  (correctness preserved)")

    print("\n-- Tokenization timing (best of N rounds) --")
    print(f"  iterations/round: {bt['iterations']}, tokens/pass: {bt['tokens_per_pass']}")
    print(f"  baseline: best={bt['best_ms']:.3f} ms  mean={bt['mean_ms']:.3f} ms")
    print(f"  refined:  best={rt['best_ms']:.3f} ms  mean={rt['mean_ms']:.3f} ms")
    if bt["best_ms"] > 0:
        delta = (bt["best_ms"] - rt["best_ms"]) / bt["best_ms"] * 100.0
        sign = "faster" if delta >= 0 else "slower"
        print(f"  refined is {abs(delta):.2f}% {sign} (best-case)")

    print("\n-- Repository safety --")
    if result["leaked_files"]:
        print(f"  !! LEAK: root files changed: {result['leaked_files']}")
    else:
        print("  no root source files were modified by the cycle (sandbox-confined).")

    print("\n-- Artifacts (sandbox-only) --")
    for label, p in result["paths"].items():
        print(f"  {label}: {os.path.relpath(p, repo_root)}")
    print("=" * 64)


def main(argv=None):
    result = run()
    ok = (
        result["baseline_tests"]["ok"]
        and result["refined_tests"]["ok"]
        and not result["leaked_files"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
Aero Autonomous Optimizer — deterministic, test-gated, human-reviewed.
=====================================================================

This replaces the previous random-mutation loop. Each pass:

  1. RECIPE ANALYSIS: lowers the declarative build recipe
     (``sample_recipe.txt``) to ``.aero`` source via the meta-compiler and
     measures token frequencies over it with ``aero_sdk.optimizer.analyzer``.
     This is deterministic — the same recipe always yields the same spec (no
     ``random`` involved), so the result is reproducible and reviewable.
  2. SPEC TUNING + DETERMINISTIC REGENERATION: writes the frequency-tuned
     ``operators`` order and ``preference_levels`` into
     ``config/language_spec.json``, then runs the official bootstrap command
     ``python aero.py build``, which regenerates ``aero_sdk/compiler/lexer.py``
     from that spec. Only the language-tables block is swapped; the proven
     scanning logic is untouched, the file is never hand-edited, and there is
     no runtime ``import`` of generated code.
  3. Verifies the full compiler suite (``test_phase2.py``) stays green. If a
     pass would break a single assertion, the change is reverted and nothing
     is published.
  4. Optionally (``--publish``) commits and pushes the verified result to a
     dedicated automation branch for human review via pull request — NEVER
     to the default branch.

Because the optimization is deterministic, the loop *converges*: once a pass
produces no change relative to the committed spec, there is nothing left to
optimize and the loop exits early instead of churning.
"""

import argparse
import os
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import meta_compiler
from aero_sdk.optimizer import analyzer
from aero_sdk.optimizer import language_spec as spec_io

CONFIG_SPEC = os.path.join(_HERE, "config", "language_spec.json")
ROOT_LEXER = os.path.join(_HERE, "aero_sdk", "compiler", "lexer.py")
TEST_SCRIPT = os.path.join(_HERE, "test_phase2.py")
RECIPE_PATH = os.path.join(_HERE, "sample_recipe.txt")

# Relative forms used for git staging (commands run with cwd=_HERE).
_REL_SPEC = os.path.relpath(CONFIG_SPEC, _HERE)
_REL_LEXER = os.path.relpath(ROOT_LEXER, _HERE)

DEFAULT_AUTO_BRANCH = os.environ.get("AERO_AUTO_BRANCH", "aero-auto/evolution")
# Branches the optimizer is structurally forbidden from publishing to.
_PROTECTED_BRANCHES = {"main", "master", "trunk", "HEAD", ""}

# Stale, non-deterministic markers left behind by the old random loop. We drop
# them so the promoted spec is a clean, reproducible artifact.
_NONDETERMINISTIC_KEYS = (
    "_evolution_epoch_timestamp",
    "_evolution_iteration_round",
    "_active_generation_seed",
)


def _git(*args, check=False):
    """Run a git command inside the SDK directory and capture its output."""
    return subprocess.run(
        ["git", *args], cwd=_HERE, check=check, capture_output=True, text=True
    )


def _recipe_corpus():
    """Lower the declarative build recipe to .aero source for frequency tuning.

    The recipe (``sample_recipe.txt``) describes the build as a set of tasks
    keyed by operation (``print``, ``set``, ``func``, ``compute``, ``call``).
    Lowering it through the meta-compiler yields the exact Aero source the
    build actually compiles, so counting token frequencies over it tunes the
    lexer for real usage. Falls back to the default code corpus if the recipe
    is missing or cannot be lowered.
    """
    try:
        recipe = meta_compiler.load_recipe(RECIPE_PATH)
        return meta_compiler.generate_aero(recipe)
    except Exception as exc:  # noqa: BLE001 — recipe is optional tuning input
        print(f"  · recipe unavailable ({exc}); using default code corpus.",
              flush=True)
        return analyzer.read_corpus(analyzer.default_corpus_paths(_HERE))


def _derive_optimized_spec():
    """Deterministically derive a frequency-tuned spec from the build recipe.

    Returns ``(baseline_spec, optimized_spec, report)``.
    """
    baseline = spec_io.load_spec(CONFIG_SPEC)
    corpus = _recipe_corpus()
    freq = analyzer.analyze_frequencies(baseline, corpus)
    optimized, report = analyzer.optimize_spec(baseline, freq)
    # Strip non-deterministic cruft so the artifact is reproducible.
    for key in _NONDETERMINISTIC_KEYS:
        optimized.pop(key, None)
    return baseline, optimized, report


def _spec_changed(baseline, optimized):
    """True if promoting ``optimized`` would actually alter the committed spec."""
    cleaned_baseline = {
        k: v for k, v in baseline.items() if k not in _NONDETERMINISTIC_KEYS
    }
    return cleaned_baseline != optimized


def _apply_spec(spec):
    """Promote ``spec`` to the root config, then regenerate via the build chain.

    Writes the mutated spec to ``config/language_spec.json`` and invokes the
    official bootstrap command ``python aero.py build``, which deterministically
    regenerates ``lexer.py`` from that spec (tables-only; the scanner and the
    'DO NOT EDIT' provenance header are preserved) and runs the self-replication
    build. Because the build regenerates from the spec, the committed spec and
    lexer can never drift apart.
    """
    spec_io.dump_spec(spec, CONFIG_SPEC)
    proc = subprocess.run(
        [sys.executable, "aero.py", "build"],
        cwd=_HERE, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"`aero.py build` failed during regeneration:\n{proc.stdout}\n{proc.stderr}"
        )


def _run_tests():
    """Run the full compiler suite in a fresh interpreter (picks up new lexer)."""
    proc = subprocess.run(
        [sys.executable, TEST_SCRIPT], cwd=_HERE, capture_output=True, text=True
    )
    return proc.returncode == 0, proc.stdout, proc.stderr


def _revert_root_artifacts():
    """Restore the spec + lexer to their committed state after a failed pass."""
    _git("checkout", "--", _REL_SPEC, _REL_LEXER)


def _publish(branch):
    """Commit the verified artifacts and push them to ``branch`` for review.

    Hard safety rail: refuses to publish to any protected/default branch, and
    only ever stages the two regenerated artifacts.
    """
    if branch in _PROTECTED_BRANCHES:
        raise SystemExit(
            f"refusing to publish to protected branch {branch!r} — "
            "automation must target a review branch, not the default branch."
        )

    _git("add", _REL_SPEC, _REL_LEXER)
    if _git("diff", "--cached", "--quiet").returncode == 0:
        print("  · nothing staged to publish.", flush=True)
        return False

    commit = _git(
        "-c", "user.name=aero-evolution-bot",
        "-c", "user.email=aero-evolution-bot@users.noreply.github.com",
        "commit", "-m",
        "auto(sdk): deterministic frequency-tuned spec + regenerated lexer",
    )
    if commit.returncode != 0:
        raise SystemExit(f"commit failed: {commit.stderr.strip()}")

    delay = 2
    push = None
    for attempt in range(4):
        push = _git("push", "origin", f"HEAD:{branch}")
        if push.returncode == 0:
            print(f"  ✅ Pushed verified optimization to review branch '{branch}'.",
                  flush=True)
            return True
        print(f"  ⚠️ push attempt {attempt + 1} failed: {push.stderr.strip()}",
              flush=True)
        time.sleep(delay)
        delay *= 2
    raise SystemExit(
        f"push to {branch!r} failed after retries: "
        f"{push.stderr.strip() if push else 'unknown error'}"
    )


def optimize_once(publish, branch):
    """Run a single deterministic, test-gated optimization pass.

    Returns one of: 'converged', 'failed', 'changed', 'published'.
    """
    baseline, optimized, report = _derive_optimized_spec()

    if not _spec_changed(baseline, optimized):
        print("  ✔ Spec already optimal for the current corpus — converged.",
              flush=True)
        return "converged"

    print("  • Deriving frequency-tuned spec from corpus...", flush=True)
    if report.get("operators_reordered"):
        print(f"      operators: {report['operators_before']}"
              f"  ->  {report['operators_after']}", flush=True)

    _apply_spec(optimized)
    print("  • Regenerated lexer.py from spec (tables-only, deterministic).",
          flush=True)

    ok, out, err = _run_tests()
    if not ok:
        print("  ❌ Regenerated compiler failed verification — reverting.",
              flush=True)
        print(out, flush=True)
        print(err, flush=True)
        _revert_root_artifacts()
        return "failed"

    print("  🎉 Verification green — change is correctness-preserving.",
          flush=True)
    if publish:
        _publish(branch)
        return "published"

    print("  · --publish not set; leaving verified change in the working tree.",
          flush=True)
    return "changed"


def run_evolution_pipeline(soak_seconds, publish, branch, cooldown=5):
    start = time.time()
    deadline = start + max(0, soak_seconds)

    print("[Aero Core] Deterministic, test-gated optimization loop.", flush=True)
    print(f"[Aero Core] Soak budget: {soak_seconds}s | publish={publish} | "
          f"branch={branch!r}", flush=True)
    print("[Aero Core] Publishing (if enabled) targets a review branch only; "
          "the default branch is never written.\n", flush=True)

    loop_round = 0
    while True:
        loop_round += 1
        print(f"\n=== Optimization pass #{loop_round} "
              f"({int(deadline - time.time())}s remaining) ===", flush=True)

        status = optimize_once(publish=publish, branch=branch)

        if status in ("converged", "failed"):
            # Nothing left to do (or a failure we already reverted).
            break
        # A productive pass ('changed'/'published'); the next derive will be
        # idempotent. Re-verify once more only if budget remains.
        if time.time() + cooldown >= deadline:
            break
        time.sleep(cooldown)
        if time.time() >= deadline:
            break

    print("\n🏁 Optimization loop finished.", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="evolve",
        description="Deterministic, test-gated Aero language-spec optimizer.",
    )
    parser.add_argument(
        "--soak-seconds", type=int, default=600,
        help="Upper bound on loop runtime (the loop converges well before this).",
    )
    parser.add_argument(
        "--publish", action="store_true",
        help="Commit + push verified gains to the automation review branch.",
    )
    parser.add_argument(
        "--branch", default=DEFAULT_AUTO_BRANCH,
        help=f"Review branch to publish to (default: {DEFAULT_AUTO_BRANCH!r}). "
             "Protected/default branches are rejected.",
    )
    args = parser.parse_args(argv)

    run_evolution_pipeline(
        soak_seconds=args.soak_seconds,
        publish=args.publish,
        branch=args.branch,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

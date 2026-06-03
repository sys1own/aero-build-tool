"""
Autonomous, Test-Gated Optimization Pass
========================================

Runs the Aero self-optimization cycle and — ONLY if the optimizer finds a
different, fully test-passing language layout — updates the tracked
``config/language_spec.json`` so CI can publish it. Emits a Markdown
telemetry report to ``$GITHUB_STEP_SUMMARY``.

Safety boundaries (deliberate):
  * It rewrites only the *data* spec (config/language_spec.json). It never
    touches compiler/runtime source code — humans promote a spec into
    generated code via the optimizer if they want the (marginal) change in
    the running compiler.
  * It exits non-zero if the correctness gate fails (full compiler suite
    against the regenerated compiler), so CI never publishes a broken layout.
  * Re-runs are idempotent: the optimized layout is deterministic from the
    source corpus, so once published there is nothing left to change.

Usage::

    python evolve.py [--soak-seconds N] [--dry-run]
"""

import argparse
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from aero_sdk.optimizer import analyzer, benchmark, pipeline
from aero_sdk.optimizer import language_spec as spec_io

TRACKED_SPEC = os.path.join(_HERE, "config", "language_spec.json")
# Hard cap on the soak loop: even the '6 hours' cadence cannot burn more
# than this many seconds of runner time here.
_SOAK_CAP_SECONDS = 120


def _emit(markdown):
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(markdown)
    sys.stdout.write(markdown)


def _soak(baseline_lexer, refined_lexer, corpus, budget_seconds):
    """Bounded re-measurement loop to firm up the timing comparison.

    Honors a selected time budget with a short cooldown between passes, but
    is hard-capped so it can never waste meaningful CI time.
    """
    budget = max(0, min(budget_seconds, _SOAK_CAP_SECONDS))
    deadline = time.time() + budget
    best_b = benchmark.time_tokenization(baseline_lexer, corpus)["best_ms"]
    best_r = benchmark.time_tokenization(refined_lexer, corpus)["best_ms"]
    passes = 1
    while time.time() < deadline:
        time.sleep(2)  # bounded cooldown padding between passes
        best_b = min(best_b, benchmark.time_tokenization(baseline_lexer, corpus)["best_ms"])
        best_r = min(best_r, benchmark.time_tokenization(refined_lexer, corpus)["best_ms"])
        passes += 1
    return passes, best_b, best_r


def run(soak_seconds=0, dry_run=False):
    result = pipeline.run(repo_root=_HERE, verbose=False)
    baseline_ok = result["baseline_tests"]["ok"]
    refined_ok = result["refined_tests"]["ok"]
    leaked = result["leaked_files"]
    paths = result["paths"]

    optimized = spec_io.load_spec(paths["sandbox_spec"])
    current = spec_io.load_spec(TRACKED_SPEC)
    changed = optimized != current

    best_b = result["baseline_timing"]["best_ms"]
    best_r = result["refined_timing"]["best_ms"]
    passes = 1
    if soak_seconds > 0 and baseline_ok and refined_ok:
        corpus = analyzer.read_corpus(analyzer.default_corpus_paths(_HERE))
        passes, best_b, best_r = _soak(
            paths["baseline_copy"], paths["refined_copy"], corpus, soak_seconds
        )

    gate_ok = baseline_ok and refined_ok and not leaked
    will_publish = gate_ok and changed and not dry_run
    if will_publish:
        spec_io.dump_spec(optimized, TRACKED_SPEC)

    _emit(_report_md(gate_ok, changed, will_publish, dry_run, result,
                     best_b, best_r, passes, optimized))
    return 0 if gate_ok else 1


def _report_md(gate_ok, changed, will_publish, dry_run, result,
               best_b, best_r, passes, optimized):
    rep = result["report"]
    delta = (best_b - best_r) / best_b * 100.0 if best_b > 0 else 0.0
    status = "✅ PASS" if gate_ok else "❌ FAIL"
    if will_publish:
        outcome = "published to `config/language_spec.json`"
    elif changed and dry_run:
        outcome = "change found (dry-run: not written)"
    elif changed and not gate_ok:
        outcome = "withheld — correctness gate failed"
    else:
        outcome = "no change (layout already optimal)"

    md = []
    md.append("## Aero Autonomous Evolution\n\n")
    md.append(f"- **Correctness gate:** {status} "
              f"(baseline {result['baseline_tests']['assertions']} / "
              f"refined {result['refined_tests']['assertions']} assertions vs the "
              f"sandboxed compiler)\n")
    md.append(f"- **Outcome:** {outcome}\n")
    md.append(f"- **Benchmark passes:** {passes}\n\n")
    md.append("### Tokenization speed (best ms — lower is better)\n\n")
    md.append("| layout | best ms |\n|---|---|\n")
    md.append(f"| before | {best_b:.3f} |\n")
    md.append(f"| after  | {best_r:.3f} |\n")
    md.append(f"| delta  | {delta:+.2f}% |\n\n")
    md.append("> On the current corpus this delta is typically within measurement "
              "noise (operators are a small minority of tokens); the gate guarantees "
              "correctness regardless of layout.\n\n")
    md.append("### Operator table re-order (longest-match-first preserved)\n\n")
    md.append(f"- before: `{rep['operators_before']}`\n")
    md.append(f"- after:  `{rep['operators_after']}`\n\n")
    md.append("### Optimized `language_spec.json`\n\n")
    md.append("```json\n" + json.dumps(optimized, indent=2) + "\n```\n")
    return "".join(md)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Autonomous Aero SDK optimization pass.")
    ap.add_argument("--soak-seconds", type=int, default=0,
                    help=f"bounded re-measurement budget (hard-capped at {_SOAK_CAP_SECONDS}s)")
    ap.add_argument("--dry-run", action="store_true",
                    help="compute + report but do not write the tracked spec")
    args = ap.parse_args(argv)
    return run(soak_seconds=args.soak_seconds, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

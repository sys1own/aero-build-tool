"""
Aero Self-Optimization Engine
=============================

Tooling that analyzes the Aero compiler's own language tables and emits
frequency-tuned, refined builders into the self-replication sandbox.

The engine is *sandbox-confined*: it reads the canonical baseline spec
(``config/language_spec.json``) and the live compiler skeleton, but every
experimental artifact it produces is written strictly under
``build_sandbox/`` so optimization passes never leak back into the root
source tree.

Modules
-------
    language_spec : load / dump / validate language_spec.json
    analyzer      : the "analyst engine" — source frequency analysis +
                    data-driven re-ordering of the language tables
    generator     : render a refined lexer ("builder") from a spec
    benchmark     : run the compiler unit tests against the sandbox
                    compiler and time tokenization (baseline vs refined)
    pipeline      : orchestrate the full, idempotent optimization cycle
"""

__version__ = "0.1.0"

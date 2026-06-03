"""
Aero Auto SDK
=============

A self-contained, plug-and-play Aero language distribution.

This directory bundles the entire toolchain so it can be copied and run on
its own:

    aero_sdk/         compiler frontend (lexer/parser/codegen), AeroVM core,
                      and the self-optimization engine
    aero.py           CLI runner: ``python aero.py build`` / ``run FILE``
    aero_build.aero   the native self-replication build script
    meta_compiler.py  intent-driven meta engine: declarative recipe -> .aero
                      -> verified .aeroc bytecode
    evolve.py         autonomous, test-gated optimization pass
    config/           canonical language_spec.json (the tunable data tables)
    src/              sample Aero program

Operating model: the SDK runs from *this* directory as its working root
(e.g. ``cd aero_auto_sdk && python aero.py build``). Internal modules import
the ``aero_sdk`` package, which lives here, so the folder is fully isolated
from the rest of the repository.
"""

__version__ = "0.1.0"

"""
Sandbox Compiler Test Runner (subprocess entry point)
=====================================================

Runs the repo's compiler unit suite (``test_phase2.py``) against the
*sandboxed* compiler rather than the root one.

This MUST be invoked as a plain script (``python _sandbox_test_runner.py
<sandbox_compiler_dir> <repo_root>``), never with ``-m``: as a script its
own module is ``__main__``, so ``aero_sdk`` is not imported until *after*
we put the sandbox on the path. We then pre-import the sandbox modules so
they populate ``sys.modules``; any later ``from aero_sdk...`` (including
test_phase2's own repo-root path insert) resolves to the cached sandbox
copy, sidestepping namespace clashes entirely.
"""

import os
import sys


def main(argv):
    if len(argv) != 3:
        print(
            "usage: _sandbox_test_runner.py <sandbox_compiler_dir> <repo_root>",
            file=sys.stderr,
        )
        return 2

    sandbox_compiler = os.path.abspath(argv[1])
    repo_root = os.path.abspath(argv[2])

    # 1) Make the SANDBOX compiler authoritative for every aero_sdk import.
    sys.path.insert(0, sandbox_compiler)
    import aero_sdk
    import aero_sdk.compiler.lexer  # noqa: F401
    import aero_sdk.compiler.parser  # noqa: F401
    import aero_sdk.compiler.codegen  # noqa: F401
    import aero_sdk.vm.machine  # noqa: F401

    loaded_from = os.path.dirname(os.path.dirname(os.path.abspath(aero_sdk.__file__)))
    if loaded_from != sandbox_compiler:
        print(
            f"FATAL: aero_sdk resolved to {loaded_from}, expected sandbox "
            f"{sandbox_compiler}",
            file=sys.stderr,
        )
        return 3

    print(f"[sandbox-tests] compiler under test: {loaded_from}")

    # 2) Make the repo importable for the test module only. aero_sdk is
    #    already cached from the sandbox, so this cannot re-bind it.
    sys.path.append(repo_root)
    import test_phase2

    return test_phase2.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""
Phase 2 Verification — Compiler Injection Gate
================================================

Proves that compile_source() and save_binary() work end-to-end:

    1. An Aero script calls compile_source(code_string) through the VM.
    2. The returned CompiledProgram is passed to save_binary(path, obj).
    3. The emitted .aeroc file on disk is valid JSON with the expected
       bytecode structure.

Run from repo root:
    python test_phase2.py
"""

import json
import os
import sys
import tempfile
import shutil

# Ensure repo root is importable.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from aero_sdk.compiler.lexer import tokenize
from aero_sdk.compiler.parser import Parser
from aero_sdk.compiler.codegen import Codegen, CompiledProgram, OpCode
from aero_sdk.vm.machine import AeroVM, _serialize_program

_PASS = 0
_FAIL = 0


def _check(condition, label, detail=""):
    global _PASS, _FAIL
    if condition:
        _PASS += 1
        print(f"  \u2714 {label}")
    else:
        _FAIL += 1
        msg = f"  \u2718 {label}"
        if detail:
            msg += f"  ({detail})"
        print(msg)


# ---------------------------------------------------------------------------
# TEST 1: compile_source() via Python — pipeline returns CompiledProgram
# ---------------------------------------------------------------------------
def test_01_compile_source_direct():
    """Call compile_source directly from Python to verify the pipeline."""
    print("\n\u25b6 TEST 1: compile_source() — Direct Pipeline Invocation")
    sample = 'let x = 10; let y = 20; let z = x + y; print(z);'

    tokens = tokenize(sample)
    ast = Parser(tokens).parse()
    program = Codegen().compile(ast)

    _check(isinstance(program, CompiledProgram),
           "Pipeline returns CompiledProgram")
    _check(len(program.main_code) > 0,
           f"main_code has {len(program.main_code)} instructions")
    opcodes = [instr[0] for instr in program.main_code]
    _check(OpCode.HALT in opcodes,
           "HALT instruction present")
    _check(OpCode.STORE in opcodes,
           "STORE instruction present (for `let` bindings)")
    _check(OpCode.ADD in opcodes,
           "ADD instruction present (for x + y)")
    _check(OpCode.CALL in opcodes,
           "CALL instruction present (for print(z))")


# ---------------------------------------------------------------------------
# TEST 2: compile_source() via VM native — Aero script triggers compilation
# ---------------------------------------------------------------------------
def test_02_compile_source_via_vm(tmpdir):
    """An Aero script invokes compile_source() through the VM FFI."""
    print("\n\u25b6 TEST 2: compile_source() — VM-Driven Compilation Gate")

    # This Aero script compiles another Aero snippet at runtime.
    aero_source = '''
let bytecode = compile_source("let a = 42; print(a);");
print("compilation_ok");
'''
    tokens = tokenize(aero_source)
    ast = Parser(tokens).parse()
    program = Codegen().compile(ast)
    vm = AeroVM(program)
    vm.run()

    _check("compilation_ok" in vm.output,
           "VM printed 'compilation_ok' after compile_source()")
    # The `bytecode` variable was stored — verify the VM didn't crash.
    _check(len(vm.output) >= 1,
           f"VM produced {len(vm.output)} output line(s)")


# ---------------------------------------------------------------------------
# TEST 3: save_binary() via VM native — emit .aeroc file
# ---------------------------------------------------------------------------
def test_03_save_binary_via_vm(tmpdir):
    """An Aero script compiles code and saves the binary to disk."""
    print("\n\u25b6 TEST 3: save_binary() — Emit .aeroc Runtime Binary")

    out_path = os.path.join(tmpdir, "dist", "main.aeroc")

    # Aero script that compiles + saves in one shot.
    aero_source = f'''
let bc = compile_source("fn add(a, b) {{ return a + b; }} let r = add(3, 4); print(r);");
save_binary("{out_path}", bc);
print("binary_saved");
'''
    tokens = tokenize(aero_source)
    ast = Parser(tokens).parse()
    program = Codegen().compile(ast)
    vm = AeroVM(program)
    vm.run()

    _check("binary_saved" in vm.output,
           "VM printed 'binary_saved' after save_binary()")
    _check(os.path.exists(out_path),
           f".aeroc file exists at {out_path}")

    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _check(data.get("format") == "aeroc",
               "Binary header format == 'aeroc'")
        _check(data.get("version") == 1,
               "Binary header version == 1")
        _check(isinstance(data.get("main_code"), list) and len(data["main_code"]) > 0,
               f"main_code has {len(data.get('main_code', []))} instructions")
        _check(isinstance(data.get("functions"), list) and len(data["functions"]) == 1,
               f"functions list has {len(data.get('functions', []))} entry (the 'add' fn)")
        if data.get("functions"):
            fn = data["functions"][0]
            _check(fn.get("name") == "add",
                   f"Function name == 'add' (got {fn.get('name')!r})")
            _check(fn.get("params") == ["a", "b"],
                   f"Function params == ['a', 'b'] (got {fn.get('params')!r})")
        _check(isinstance(data.get("constants"), list),
               "Constants pool is a list")


# ---------------------------------------------------------------------------
# TEST 4: Serialization round-trip integrity
# ---------------------------------------------------------------------------
def test_04_serialization_integrity():
    """_serialize_program preserves all OpCode names and constant values."""
    print("\n\u25b6 TEST 4: Serialization Round-Trip Integrity")

    source = 'let msg = "hello"; print(msg);'
    tokens = tokenize(source)
    ast = Parser(tokens).parse()
    program = Codegen().compile(ast)
    payload = _serialize_program(program)

    # Every instruction's first element should be a valid OpCode name.
    all_opcode_names = {op.name for op in OpCode}
    for instr in payload["main_code"]:
        _check(instr[0] in all_opcode_names,
               f"Instruction opcode '{instr[0]}' is a valid OpCode name")

    _check("hello" in payload["constants"],
           "'hello' string literal in constants pool")
    _check("print" in payload["constants"],
           "'print' callee name in constants pool")


# ---------------------------------------------------------------------------
# TEST 5: register_native() — runtime extension
# ---------------------------------------------------------------------------
def test_05_register_native():
    """A custom native registered at runtime is callable from Aero."""
    print("\n\u25b6 TEST 5: register_native() — Runtime Extension")

    source = 'let x = custom_add(10, 20); print(x);'
    tokens = tokenize(source)
    ast = Parser(tokens).parse()
    program = Codegen().compile(ast)
    vm = AeroVM(program)

    def _custom_add(args):
        return int(args[0]) + int(args[1])

    vm.register_native("custom_add", _custom_add)
    vm.run()

    _check("30" in vm.output,
           f"custom_add(10, 20) == 30 (vm.output={vm.output})")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main():
    global _PASS, _FAIL
    print("=" * 72)
    print("  PHASE 2 VERIFICATION — COMPILER INJECTION GATE")
    print("  compile_source() + save_binary() End-to-End Validation")
    print("=" * 72)

    tmpdir = tempfile.mkdtemp(prefix="aero_phase2_test_")
    try:
        test_01_compile_source_direct()
        test_02_compile_source_via_vm(tmpdir)
        test_03_save_binary_via_vm(tmpdir)
        test_04_serialization_integrity()
        test_05_register_native()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n" + "=" * 72)
    total = _PASS + _FAIL
    if _FAIL == 0:
        print(f"  \U0001f389 ALL {total} ASSERTIONS PASSED — COMPILER INJECTION GATE VERIFIED")
    else:
        print(f"  \u274c {_FAIL}/{total} ASSERTION(S) FAILED")
    print("=" * 72)
    return 1 if _FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

"""
Aero VM — Stack-Based Bytecode Interpreter
===========================================

Executes compiled Aero bytecode instructions on a virtual stack machine.

Architecture:
    - Operand stack (dynamically sized)
    - Call stack (frames with local variable slots)
    - Constant pool (shared across all frames)
    - Program counter per frame
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from compiler.codegen import CompiledProgram, CompiledFunction, OpCode


@dataclass
class CallFrame:
    code: list
    pc: int = 0
    locals: Dict[int, Any] = field(default_factory=dict)
    base_pointer: int = 0


class VMError(Exception):
    pass


class AeroVM:
    MAX_STACK_SIZE = 4096
    MAX_CALL_DEPTH = 256

    def __init__(self, program: CompiledProgram):
        self._program = program
        self._stack: List[Any] = []
        self._call_stack: List[CallFrame] = []
        self._fn_table: Dict[str, CompiledFunction] = {
            fn.name: fn for fn in program.functions
        }
        self._builtins: Dict[str, Any] = {
            "print": self._builtin_print,
            "len": self._builtin_len,
            "int": self._builtin_int,
        }
        self._output: List[str] = []

    @property
    def output(self) -> List[str]:
        return self._output

    def run(self) -> Any:
        frame = CallFrame(code=self._program.main_code)
        self._call_stack.append(frame)
        return self._execute()

    def _execute(self) -> Any:
        while self._call_stack:
            frame = self._call_stack[-1]

            if frame.pc >= len(frame.code):
                self._call_stack.pop()
                continue

            instr = frame.code[frame.pc]
            frame.pc += 1
            op = instr[0]

            if op == OpCode.PUSH_INT:
                self._push(instr[1])
            elif op == OpCode.PUSH_FLOAT:
                self._push(self._program.constants[instr[1]])
            elif op == OpCode.PUSH_STRING:
                self._push(self._program.constants[instr[1]])
            elif op == OpCode.PUSH_BOOL:
                self._push(bool(instr[1]))
            elif op == OpCode.LOAD:
                slot = instr[1]
                if slot not in frame.locals:
                    raise VMError(f"undefined local variable at slot {slot}")
                self._push(frame.locals[slot])
            elif op == OpCode.STORE:
                slot = instr[1]
                frame.locals[slot] = self._pop()
            elif op == OpCode.ADD:
                b, a = self._pop(), self._pop()
                self._push(a + b)
            elif op == OpCode.SUB:
                b, a = self._pop(), self._pop()
                self._push(a - b)
            elif op == OpCode.MUL:
                b, a = self._pop(), self._pop()
                self._push(a * b)
            elif op == OpCode.DIV:
                b, a = self._pop(), self._pop()
                if b == 0:
                    raise VMError("division by zero")
                self._push(a / b if isinstance(a, float) or isinstance(b, float) else a // b)
            elif op == OpCode.MOD:
                b, a = self._pop(), self._pop()
                if b == 0:
                    raise VMError("modulo by zero")
                self._push(a % b)
            elif op == OpCode.EQ:
                b, a = self._pop(), self._pop()
                self._push(a == b)
            elif op == OpCode.NEQ:
                b, a = self._pop(), self._pop()
                self._push(a != b)
            elif op == OpCode.LT:
                b, a = self._pop(), self._pop()
                self._push(a < b)
            elif op == OpCode.GT:
                b, a = self._pop(), self._pop()
                self._push(a > b)
            elif op == OpCode.LTE:
                b, a = self._pop(), self._pop()
                self._push(a <= b)
            elif op == OpCode.GTE:
                b, a = self._pop(), self._pop()
                self._push(a >= b)
            elif op == OpCode.AND:
                b, a = self._pop(), self._pop()
                self._push(bool(a and b))
            elif op == OpCode.OR:
                b, a = self._pop(), self._pop()
                self._push(bool(a or b))
            elif op == OpCode.NOT:
                self._push(not self._pop())
            elif op == OpCode.NEG:
                self._push(-self._pop())
            elif op == OpCode.JUMP:
                frame.pc = instr[1]
            elif op == OpCode.JUMP_IF_FALSE:
                cond = self._pop()
                if not cond:
                    frame.pc = instr[1]
            elif op == OpCode.CALL:
                argc = instr[1]
                callee = self._pop()
                args = [self._pop() for _ in range(argc)]
                args.reverse()

                if isinstance(callee, str) and callee in self._builtins:
                    result = self._builtins[callee](args)
                    self._push(result)
                elif isinstance(callee, str) and callee in self._fn_table:
                    fn = self._fn_table[callee]
                    if len(args) != len(fn.params):
                        raise VMError(
                            f"function '{callee}' expects {len(fn.params)} args, got {len(args)}"
                        )
                    if len(self._call_stack) >= self.MAX_CALL_DEPTH:
                        raise VMError("maximum call depth exceeded")
                    new_frame = CallFrame(code=fn.code, base_pointer=len(self._stack))
                    for i, arg in enumerate(args):
                        new_frame.locals[i] = arg
                    self._call_stack.append(new_frame)
                else:
                    raise VMError(f"cannot call: {callee!r}")
            elif op == OpCode.RETURN:
                self._call_stack.pop()
                # Return value is top of stack (if any)
            elif op == OpCode.POP:
                self._pop()
            elif op == OpCode.HALT:
                return self._stack[-1] if self._stack else None
            else:
                raise VMError(f"unknown opcode: {op}")

        return self._stack[-1] if self._stack else None

    def _push(self, value: Any) -> None:
        if len(self._stack) >= self.MAX_STACK_SIZE:
            raise VMError("stack overflow")
        self._stack.append(value)

    def _pop(self) -> Any:
        if not self._stack:
            raise VMError("stack underflow")
        return self._stack.pop()

    # ── Builtins ─────────────────────────────────────────────────────────

    def _builtin_print(self, args: List[Any]) -> None:
        text = " ".join(str(a) for a in args)
        self._output.append(text)
        return None

    def _builtin_len(self, args: List[Any]) -> int:
        if len(args) != 1:
            raise VMError("len() takes exactly 1 argument")
        return len(args[0])

    def _builtin_int(self, args: List[Any]) -> int:
        if len(args) != 1:
            raise VMError("int() takes exactly 1 argument")
        return int(args[0])

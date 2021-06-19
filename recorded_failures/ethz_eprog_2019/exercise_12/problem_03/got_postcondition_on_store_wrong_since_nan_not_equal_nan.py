# pylint: disable=line-too-long
"""
Implement a compiler for the interpreter developed in Exercise 12, Problem 1.

The program should be compiled in a language based on operand stack.

The following operations are supported:
* ``CONST c``: push the value ``c`` on the stack,
* ``LOAD v``: load the value of the variable ``v`` and push it on the stack,
* ``STORE v``: pop a value from the stack and store it to the variable ``v``,
* ``OP {operation}``: pop two values ("left" and "right"), apply the operation and
  push the result on the stack, and
* ``FUNC f``: pop a value from the stack, apply the function ``f`` on it and push the
  result on the stack.

Please see `page 5`_ of the exercise for an example.

.. _page 5: https://ethz.ch/content/dam/ethz/special-interest/infk/inst-cs/lst-dam/documents/Education/Classes/Fall2019/0027_Intro/Homework/u12.pdf?page=5
"""
import math
from typing import List, MutableMapping, Mapping

from icontract import DBC, snapshot, ensure, require, ViolationError

from correct_programs.ethz_eprog_2019.exercise_12 import problem_01


class Instruction:
    """Represent the bytecode instruction."""


class Const(Instruction, DBC):
    """Push the constant on the stack."""

    def __init__(self, value: float) -> None:
        self.value = value


class Load(Instruction, DBC):
    """Load a variable from the registry and push it on the stack."""

    def __init__(self, identifier: problem_01.Identifier) -> None:
        self.identifier = identifier


class Store(Instruction, DBC):
    """Pop a value from the stack and store it in the registry."""

    def __init__(self, identifier: problem_01.Identifier) -> None:
        """Initialize with the given values."""
        self.identifier = identifier


class UnaryOperation(Instruction, DBC):
    """Pop the value from the stack, apply the operation and push the result."""

    def __init__(self, operator: problem_01.UnOp) -> None:
        """Initialize with the given values."""
        self.operator = operator


class BinaryOperation(Instruction, DBC):
    """Pop the two values from the stack, apply the operation and push the result."""

    def __init__(self, operator: problem_01.BinOp) -> None:
        """Initialize with the given values."""
        self.operator = operator


class Call(Instruction, DBC):
    """Pop the value from the stack, apply the function and push the result."""

    def __init__(self, function: problem_01.Function) -> None:
        """Initialize with the given values."""
        self.function = function


class _CompileVisitor(problem_01._Visitor[None]):
    def __init__(self) -> None:
        self.instructions = []  # type: List[Instruction]

    def visit_constant(self, node: problem_01.Constant) -> None:
        self.instructions.append(Const(value=node.value))

    def visit_variable(self, node: problem_01.Variable) -> None:
        self.instructions.append(Load(identifier=node.identifier))

    def visit_unary_operation(self, node: problem_01.UnaryOperation) -> None:
        self.visit(node.target)
        self.instructions.append(UnaryOperation(operator=node.operator))

    def visit_binary_operation(self, node: problem_01.BinaryOperation) -> None:
        self.visit(node.left)
        self.visit(node.right)
        self.instructions.append(BinaryOperation(operator=node.operator))

    def visit_call(self, node: problem_01.Call) -> None:
        self.visit(node.argument)
        self.instructions.append(Call(function=node.function))

    def visit_assign(self, node: problem_01.Assign) -> None:
        self.visit(node.expr)
        self.instructions.append(Store(identifier=node.target))

    def visit_program(self, node: problem_01.Program) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_default(self, node: problem_01.Node) -> None:
        raise NotImplementedError(repr(node))


def compile_program(program: problem_01.Program) -> List[Instruction]:
    """Compile the given program into bytecode instructions."""
    visitor = _CompileVisitor()
    visitor.visit(program)

    return visitor.instructions


@snapshot(lambda stack: stack[:])
@ensure(lambda instr, stack, OLD: stack == OLD.stack + [instr.value])
def _execute_const(instr: Const, stack: List[float]) -> None:
    stack.append(instr.value)


# fmt: off
@require(
    lambda instr, variables: instr.identifier in variables,
    error=lambda instr: NameError(
        f"Unexpected LOAD on variable "
        f"which is not available: {instr.identifier}")
)
@snapshot(lambda stack: stack[:])
@ensure(
    lambda instr, variables, stack, OLD:
    stack == OLD.stack + [variables[instr.identifier]]
)
# fmt: on
def _execute_load(instr: Load, variables: Mapping[str, float],
                  stack: List[float]) -> None:
    stack.append(variables[instr.identifier])

# ERROR:
# icontract.errors.ViolationError:
# variables[instr.identifier] == OLD.stack[-1]:
# OLD was a bunch of OLD values
# OLD.stack was [nan]
# instr was <correct_programs.ethz_eprog_2019.exercise_12.problem_03.Store object at 0x000002200B622760>
# instr.identifier was 'A'
# result was None
# stack was []
# variables was {'A': nan}
#
# Falsifying example: execute(
#     kwargs={'instr': <correct_programs.ethz_eprog_2019.exercise_12.problem_03.Store at 0x2200b622760>,
#      'stack': [nan],
#      'variables': {}},
# )
# fmt: off
@require(
    lambda stack: len(stack) > 0,
    error=lambda instr: RuntimeError(
        f"Unexpected empty stack on STORE "
        f"to variable: {instr.identifier}")
)
@snapshot(lambda stack: stack[:])
@ensure(lambda stack, OLD: stack == OLD.stack[:-1])
@ensure(lambda instr, variables, OLD: variables[instr.identifier] == OLD.stack[-1])
@ensure(lambda instr, variables: instr.identifier in variables)
# fmt: on
def _execute_store(
        instr: Store, variables: MutableMapping[str, float], stack: List[float]
) -> None:
    value = stack.pop()
    variables[instr.identifier] = value


# fmt: off
@require(
    lambda stack: len(stack) > 0,
    error=lambda instr: RuntimeError(
        f"Unexpected empty stack on unary operation {instr.operator}")
)
@snapshot(lambda stack: stack[:])
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack))
@ensure(lambda stack, OLD: stack[:-1] == OLD.stack[:-1])
# fmt: on
def _execute_unary_operation(instr: UnaryOperation, stack: List[float]) -> None:
    value = stack.pop()
    if instr.operator == problem_01.UnOp.MINUS:
        result = -value
    else:
        raise NotImplementedError(f"{instr.operator=}")

    stack.append(result)


# fmt: off
@require(
    lambda stack: len(stack) >= 2,
    error=lambda instr, stack: RuntimeError(
        f"Unexpected stack with only {len(stack)} element(s) "
        f"on binary operation {instr.operator}")
)
@snapshot(lambda stack: stack[:])
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack) - 1)
@ensure(lambda stack, OLD: stack[:-2] == OLD.stack[:-2])
# fmt: on
def _execute_binary_operation(instr: BinaryOperation, stack: List[float]) -> None:
    left_value = stack.pop()
    right_value = stack.pop()

    if instr.operator == problem_01.BinOp.ADD:
        result = left_value + right_value
    elif instr.operator == problem_01.BinOp.SUB:
        result = left_value - right_value
    elif instr.operator == problem_01.BinOp.MUL:
        result = left_value * right_value
    elif instr.operator == problem_01.BinOp.DIV:
        result = left_value / right_value
    elif instr.operator == problem_01.BinOp.POW:
        result = left_value ** right_value
    else:
        raise NotImplementedError(f"{instr.operator=}")

    stack.append(result)


# fmt: off
@require(
    lambda stack: len(stack) > 0,
    error=lambda instr: RuntimeError(
        f"Unexpected empty stack on call to function {instr.function}")
)
@snapshot(lambda stack: stack[:])
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack))
@ensure(lambda stack, OLD: stack[:-1] == OLD.stack[:-1])
# fmt: on
def _execute_call(instr: Call, stack: List[float]) -> None:
    value = stack.pop()
    if instr.function == problem_01.Function.SIN:
        result = math.sin(value)
    elif instr.function == problem_01.Function.COS:
        result = math.cos(value)
    elif instr.function == problem_01.Function.TAN:
        result = math.tan(value)
    else:
        raise NotImplementedError(f"{instr.function=}")

    stack.append(result)


def execute(instructions: List[Instruction]) -> MutableMapping[str, float]:
    """Execute the given instructions."""
    variables = dict()  # type: MutableMapping[str, float]

    if len(instructions) == 0:
        return variables

    stack = []  # type: List[float]

    for instr in instructions:
        if isinstance(instr, Const):
            _execute_const(instr=instr, stack=stack)
        elif isinstance(instr, Load):
            _execute_load(instr=instr, variables=variables, stack=stack)
        elif isinstance(instr, Store):
            _execute_store(instr=instr, variables=variables, stack=stack)
        elif isinstance(instr, UnaryOperation):
            _execute_unary_operation(instr=instr, stack=stack)
        elif isinstance(instr, BinaryOperation):
            _execute_binary_operation(instr=instr, stack=stack)
        elif isinstance(instr, Call):
            _execute_call(instr=instr, stack=stack)
        else:
            raise NotImplementedError(f"{instr=}")

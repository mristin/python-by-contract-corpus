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

from icontract import DBC, snapshot, ensure, require

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_12 import problem_01


class Instruction:
    """Represent a bytecode instruction."""


class Const(Instruction, DBC):
    """Push the constant on the stack."""

    def __init__(self, value: float) -> None:
        """Initialize with the given values."""
        self.value = value

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.value})"


class Load(Instruction, DBC):
    """Load a variable from the registry and push it on the stack."""

    def __init__(self, identifier: problem_01.Identifier) -> None:
        """Initialize with the given values."""
        self.identifier = identifier

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.identifier!r})"


class Store(Instruction, DBC):
    """Pop a value from the stack and store it in the registry."""

    def __init__(self, identifier: problem_01.Identifier) -> None:
        """Initialize with the given values."""
        self.identifier = identifier

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.identifier!r})"


class UnaryOperation(Instruction, DBC):
    """Pop the value from the stack, apply the operation and push the result."""

    def __init__(self, operator: problem_01.UnOp) -> None:
        """Initialize with the given values."""
        self.operator = operator

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.operator!r})"


class BinaryOperation(Instruction, DBC):
    """Pop the two values from the stack, apply the operation and push the result."""

    def __init__(self, operator: problem_01.BinOp) -> None:
        """Initialize with the given values."""
        self.operator = operator

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.operator!r})"


class Call(Instruction, DBC):
    """Pop the value from the stack, apply the function and push the result."""

    def __init__(self, function: problem_01.Function) -> None:
        """Initialize with the given values."""
        self.function = function

    def __repr__(self) -> str:
        """Represent the instance as a string for debugging."""
        return f"{self.__class__.__name__}({self.function!r})"


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
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack) + 1)
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
def _execute_load(
    instr: Load, variables: Mapping[problem_01.Identifier, float], stack: List[float]
) -> None:
    stack.append(variables[instr.identifier])


# fmt: off
@require(
    lambda stack: len(stack) > 0,
    error=lambda instr: RuntimeError(
        f"Unexpected empty stack on STORE "
        f"to variable: {instr.identifier}")
)
@snapshot(lambda stack: stack[:])
@ensure(
    lambda stack, OLD:
    all(
        (math.isnan(old) and math.isnan(new)) or old == new
        for old, new in zip(OLD.stack[:-1], stack)
    )
)
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack) - 1)
@ensure(lambda instr, variables: instr.identifier in variables)
# fmt: on
def _execute_store(
    instr: Store,
    variables: MutableMapping[problem_01.Identifier, float],
    stack: List[float],
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
@ensure(
    lambda stack, OLD:
    all(
        (math.isnan(old) and math.isnan(new)) or old == new
        for old, new in zip(OLD.stack[:-1], stack[:-1])
    )
)
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack))
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
@ensure(
    lambda stack, OLD:
    all(
        (math.isnan(old) and math.isnan(new)) or old == new
        for old, new in zip(OLD.stack[:-2], stack[:-2])
    )
)
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack) - 1)
# fmt: on
def _execute_binary_operation(instr: BinaryOperation, stack: List[float]) -> None:
    right_value = stack.pop()
    left_value = stack.pop()

    if instr.operator == problem_01.BinOp.ADD:
        result = left_value + right_value
    elif instr.operator == problem_01.BinOp.SUB:
        result = left_value - right_value
    elif instr.operator == problem_01.BinOp.MUL:
        result = left_value * right_value
    elif instr.operator == problem_01.BinOp.DIV:
        result = left_value / right_value
    elif instr.operator == problem_01.BinOp.POW:
        result = left_value**right_value
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
@ensure(
    lambda stack, OLD:
    all(
        (math.isnan(old) and math.isnan(new)) or old == new
        for old, new in zip(OLD.stack[:-1], stack[:-1])
    )
)
@ensure(lambda stack, OLD: len(stack) == len(OLD.stack))
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


def execute(
    instructions: List[Instruction],
) -> MutableMapping[problem_01.Identifier, float]:
    """
    Execute the given ``instructions``.

    :return: The final state of the program
    """
    variables = dict()  # type: MutableMapping[problem_01.Identifier, float]

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

    return variables


# ERROR (mristin, 2021-06-19):
# I forgot to exclude the NaN's in the equality checks since the equality is always
# False for NaN's.
# I should have written a function like this and used it in the post-condition of
# ``compile_and_execute``:
# def compare_against_interpret(
#     program: problem_01.Program, result: Mapping[problem_01.Identifier, float]
# ) -> bool:
#     """Compare against the interpreted program."""
#     interpreted = problem_01.interpret(program)
#
#     if len(interpreted) != len(result):
#         return False
#
#     if interpreted.keys() != result.keys():
#         return False
#
#     for key in interpreted:
#         interpreted_value = interpreted[key]
#         our_value = result[key]
#
#         if math.isnan(interpreted_value) ^ math.isnan(our_value):
#             return False
#
#         if not math.isnan(interpreted_value) and interpreted_value != our_value:
#             return False
#
#     return True
#
#
# @ensure(lambda program, result: compare_against_interpret(program, result))


@ensure(lambda program, result: result == problem_01.interpret(program))
def compile_and_execute(
    program: problem_01.Program,
) -> MutableMapping[problem_01.Identifier, float]:
    """Compile and execute the given ``program``."""
    instructions = compile_program(program)
    return execute(instructions)

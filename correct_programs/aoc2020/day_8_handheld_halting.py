import dataclasses
import enum
import re
from typing import Mapping, List, Optional, Set

from icontract import require, ensure

# crosshair: on
from correct_programs.common import Lines


class Operation(enum.Enum):
    """Represent an operation corresponding to an instruction."""

    NOP = "nop"
    ACC = "acc"
    JMP = "jmp"


assert len(set(op.value for op in Operation)) == sum(1 for op in Operation)
VALUE_TO_OPERATION = {op.value: op for op in Operation}  # type: Mapping[str, Operation]


@dataclasses.dataclass(frozen=True)
class Instruction:
    """Represent an instruction of the boot code."""

    operation: Operation  #: the corresponding operation
    argument: int  #: the argument to the operation

    def __repr__(self) -> str:
        """Represent the instruction as a string for debugging."""
        return f"{self.operation.value} {self.argument}"


INSTRUCTION_RE = re.compile(
    r"^(?P<operation>nop|acc|jmp) (?P<argument>[+-](0|[1-9][0-9]*))\Z"
)


@require(lambda line: INSTRUCTION_RE.match(line))
def parse_line(line: str) -> Instruction:
    """Parse a ``line`` of the boot code into an instruction."""
    mtch = INSTRUCTION_RE.match(line)
    assert mtch is not None

    operation = VALUE_TO_OPERATION[mtch.group("operation")]
    argument = int(mtch.group("argument"))
    return Instruction(operation=operation, argument=argument)


@require(lambda lines: all(INSTRUCTION_RE.match(line) for line in lines))
@ensure(lambda lines, result: len(lines) == len(result))
def parse(lines: Lines) -> List[Instruction]:
    """Parse the boot code given as ``lines``."""
    return [parse_line(line) for line in lines]


@require(
    lambda instructions: all(
        0 <= i + instruction.argument < len(instructions)
        for i, instruction in enumerate(instructions)
        if instruction.operation == Operation.JMP
    )
)
def execute_instructions(instructions: List[Instruction]) -> Optional[int]:
    """
    Execute the boot code given as ``instructions``.

    :return:
        The value in the accumulator just before an instruction is run
        for the second time
    """
    visited_lines = set()  # type: Set[int]

    current_line = 0
    accumulator = 0

    while True:
        if current_line in visited_lines:
            return accumulator

        if current_line == len(instructions):
            return None

        visited_lines.add(current_line)

        instruction = instructions[current_line]

        if instruction.operation == Operation.NOP:
            current_line += 1
        elif instruction.operation == Operation.ACC:
            accumulator += instruction.argument
            current_line += 1
        elif instruction.operation == Operation.JMP:
            current_line += instruction.argument
        else:
            raise NotImplementedError(instruction.operation)

import dataclasses
import enum
import re
from typing import Tuple, Mapping, List, Optional, Set

from icontract import require, ensure


# crosshair: on


class Operation(enum.Enum):
    NOP = "nop"
    ACC = "acc"
    JMP = "jmp"


assert len(set(op.value for op in Operation)) == sum(1 for op in Operation)
VALUE_TO_OPERATION = {op.value: op for op in Operation}  # type: Mapping[str, Operation]


@dataclasses.dataclass
class Instruction:
    operation: Operation
    argument: int

    def __repr__(self) -> str:
        return f"{self.operation.value} {self.argument}"


INSTRUCTION_RE = re.compile(
    r"^(?P<operation>nop|acc|jmp) (?P<argument>[+-](0|[1-9][0-9]*))\Z"
)


@require(lambda line: INSTRUCTION_RE.match(line))
def parse_line(line: str) -> Instruction:
    mtch = INSTRUCTION_RE.match(line)
    assert mtch is not None

    operation = VALUE_TO_OPERATION[mtch.group("operation")]
    argument = int(mtch.group("argument"))
    return Instruction(operation=operation, argument=argument)


@require(lambda lines: all(INSTRUCTION_RE.match(line) for line in lines))
@ensure(lambda lines, result: len(lines) == len(result))
def parse(lines: List[str]) -> List[Instruction]:
    return [parse_line(line) for line in lines]


@require(
    lambda instructions: all(
        0 <= i + instruction.argument < len(instructions)
        for i, instruction in enumerate(instructions)
        if instruction.operation == Operation.JMP
    )
)
def execute_instructions(instructions: List[Instruction]) -> Optional[int]:
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

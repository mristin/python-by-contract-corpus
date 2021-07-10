import re
from typing import Tuple, cast, Sequence

from icontract import ensure, require, DBC

STEP_SIZE_HORIZONTAL: int = 3
STEP_SIZE_VERTICAL: int = 1


class InputLine(DBC, str):
    """Represent a line of the input map."""

    @require(lambda line: re.fullmatch("[.#]*", line))
    def __new__(cls, line: str) -> "InputLine":
        return cast(InputLine, line)


# fmt: off
@require(
    lambda lines:
    all(
        len(line) == len(lines[0])
        for line in lines
    )
)
@require(lambda lines: len(lines) > 0)
@ensure(lambda result: result[0] * result[1] == len(result[2]))
# fmt: on
def parse_input(lines: Sequence[InputLine]) -> Tuple[int, int, str]:
    """Parse the input map given as ``lines``."""
    width: int = len(lines[0])
    height: int = len(lines)
    return width, height, "".join(lines)


@require(lambda width, height: width > 0 and height > 0)
@require(lambda input_string: re.match(r"^[.#]*", input_string))
@require(lambda width, height, input_string: width * height == len(input_string))
@ensure(lambda result, height: result <= height / STEP_SIZE_VERTICAL)
def count_trees(width: int, height: int, input_string: str) -> int:
    """Count the trees in the ``input_string``."""
    count: int = 0
    current_x: int = 0
    current_y: int = 0

    while current_y < height:
        if input_string[current_y * width + current_x] == "#":
            count += 1
        current_x = (current_x + STEP_SIZE_HORIZONTAL) % width
        current_y += STEP_SIZE_VERTICAL

    return count

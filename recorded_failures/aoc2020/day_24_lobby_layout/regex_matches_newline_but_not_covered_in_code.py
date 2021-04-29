import enum
import re
from typing import Tuple, List

from icontract import require, ensure, invariant


class Cell:
    @require(lambda x, y, z: x + y + z == 0)
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


class Direction(enum.Enum):
    EAST = "e"
    SOUTH_EAST = "se"
    SOUTH_WEST = "sw"
    WEST = "w"
    NORTH_WEST = "nw"
    NORTH_EAST = "ne"


assert len(set(entry.value for entry in Direction)) == len(Direction)
VALUE_TO_DIRECTION = dict((entry.value, entry) for entry in Direction)


def next_cell(cell: Cell, direction: Direction) -> Cell:
    if direction == Direction.EAST:
        result = Cell(cell.x + 1, cell.y - 1, cell.z)
    elif direction == Direction.SOUTH_EAST:
        result = Cell(cell.x, cell.y - 1, cell.z + 1)
    elif direction == Direction.SOUTH_WEST:
        result = Cell(cell.x - 1, cell.y, cell.z + 1)
    elif direction == Direction.WEST:
        result = Cell(cell.x - 1, cell.y + 1, cell.z)
    elif direction == Direction.NORTH_WEST:
        result = Cell(cell.x, cell.y + 1, cell.z - 1)
    elif direction == Direction.NORTH_EAST:
        result = Cell(cell.x + 1, cell.y, cell.z - 1)
    else:
        raise NotImplementedError(direction)

    return result


# ERROR: DIRECTIONS_RE will match a string ending in a new line.
# ERROR: However, VALUE_TO_DIRECTION will fail on the new line!
DIRECTIONS_RE = re.compile('^(se|sw|nw|ne|w|e)+$')
ONE_DIRECTION_RE = re.compile('(se|sw|nw|ne|w|e)')


@require(lambda line: DIRECTIONS_RE.match(line))
@ensure(lambda line, result: stringify_directions(result) == line)
def parse_line(line: str) -> List[Direction]:
    directions = []  # type: List[Direction]
    for part in ONE_DIRECTION_RE.findall(line):
        direction = VALUE_TO_DIRECTION[part]
        directions.append(direction)

    return directions


@ensure(lambda directions, result: parse_line(result) == directions)
def stringify_directions(directions: List[Direction]) -> str:
    return ''.join(direction.value for direction in directions)

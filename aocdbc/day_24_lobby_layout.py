import collections
import enum
import re
from typing import Tuple, List, MutableMapping

from icontract import require, ensure, DBC


# crosshair: on


class Cell(DBC):
    @require(lambda x, y, z: x + y + z == 0)
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


def cell_as_tuple(cell: Cell) -> Tuple[int, int, int]:
    return cell.x, cell.y, cell.z


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


def follow_directions(start: Cell, directions: List[Direction]) -> Cell:
    cursor = start
    for direction in directions:
        cursor = next_cell(cell=cursor, direction=direction)

    return cursor


DIRECTIONS_RE = re.compile("^(se|sw|nw|ne|w|e)+\Z")
ONE_DIRECTION_RE = re.compile("(se|sw|nw|ne|w|e)")


@require(lambda line: not (len(line) > 0) or DIRECTIONS_RE.match(line))
@ensure(lambda line, result: not (len(line) == 0) or len(result) == 0)
@ensure(lambda line, result: stringify_directions(result) == line)  # type: ignore
def parse_line(line: str) -> List[Direction]:
    if len(line) == 0:
        return []

    directions = []  # type: List[Direction]
    for part in ONE_DIRECTION_RE.findall(line):
        direction = VALUE_TO_DIRECTION[part]
        directions.append(direction)

    return directions


@ensure(lambda directions, result: parse_line(result) == directions)
def stringify_directions(directions: List[Direction]) -> str:
    return "".join(direction.value for direction in directions)


def count_flips(plan: List[List[Direction]]) -> int:
    # True means white.
    state = collections.defaultdict(
        lambda: True
    )  # type: MutableMapping[Tuple[int, int, int], bool]
    start = Cell(x=0, y=0, z=0)
    for directions in plan:
        cell = follow_directions(start=start, directions=directions)
        key = cell_as_tuple(cell=cell)
        state[key] = not state[key]

    # Count the blacks which correspond to False.
    return sum(1 for value in state.values() if not value)

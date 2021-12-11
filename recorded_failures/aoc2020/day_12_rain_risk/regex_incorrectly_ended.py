"""
Input: list of actions
Output: position, Manhattan distance
"""
from dataclasses import dataclass
from icontract import invariant, require, ensure
from typing import List
import re
from enum import Enum


"""
Falsifying example: execute(
    kwargs={'current_position': east 0, north 0, orientation EAST,
     'move': 'E0:'},)
 """


class Orientation(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


@dataclass
class ShipPosition:
    horizontal: int = 0
    vertical: int = 0
    orientation: Orientation = Orientation.EAST

    def __repr__(self):
        result = ""
        if self.horizontal < 0:
            result += "west {}".format(abs(self.horizontal))
        else:
            result += "east {}".format(self.horizontal)
        if self.vertical >= 0:
            result += ", north {}".format(self.vertical)
        else:
            result += ", south {}".format(abs(self.vertical))
        result += ", orientation {}".format(self.orientation.name)
        return result


@require(
    lambda puzzle_input: re.match(
        r"^[NSEWLRF][0-9]+(\n[NSEWLRF][0-9]+)*$", puzzle_input
    )
)
@ensure(lambda result, puzzle_input: "\n".join(result) == puzzle_input)
def parse_input(puzzle_input: str) -> List[str]:
    return list(map(lambda l: l, puzzle_input.split("\n")))


@require(lambda move: re.match(r"^[NSEWLRF][0-9]+", move))
@require(
    lambda move: not (move[0] == "L" or move[0] == "R")
    or move[1:] in [0, 90, 180, 270, 360]
)
def update_position(current_position: ShipPosition, move: str) -> ShipPosition:
    action, value = move[0], int(move[1:])
    next_position = current_position
    if action == "N":
        next_position.vertical += value
    elif action == "S":
        next_position.vertical -= value
    elif action == "E":
        next_position.horizontal += value
    elif action == "W":
        next_position.horizontal -= value
    elif action == "L":
        next_position.orientation = Orientation(
            ((next_position.orientation).value - (value / 90)) % 4
        )
    elif action == "R":
        next_position.orientation = Orientation(
            ((next_position.orientation).value + (value / 90)) % 4
        )
    elif action == "F":
        if next_position.orientation == Orientation.NORTH:
            next_position.vertical += value
        elif next_position.orientation == Orientation.SOUTH:
            next_position.vertical -= value
        elif next_position.orientation == Orientation.EAST:
            next_position.horizontal += value
        elif next_position.orientation == Orientation.WEST:
            next_position.horizontal -= value

    return next_position


@require(
    lambda puzzle_input: re.match(
        r"^[NSEWLRF][0-9]+(\n[NSEWLRF][0-9]+)*$", puzzle_input
    )
)
def solve(puzzle_input: str) -> ShipPosition:
    current_position = ShipPosition(0, 0, Orientation.EAST)
    for command in parse_input(puzzle_input):
        current_position = update_position(current_position, command)
    return current_position


example_input = """F10
N3
F7
R90
F11"""

if __name__ == "__main__":
    print(solve(example_input))

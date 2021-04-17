from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
import math
import re
import sys
from typing import Dict, List, Optional, Set, Tuple

from icontract import require, ensure, invariant, DBC


def valid_side(side: str) -> bool:
    return re.fullmatch(r"[\.\#]{10}", side) is not None


@require(lambda side: valid_side(side))
@ensure(lambda result: valid_side(result))
def reverse_side(side: str) -> str:
    return "".join(reversed(side))


@dataclass(frozen=True)
class Tile(DBC):
    top: str
    right: str
    bottom: str
    left: str

    def rotate(self) -> "Tile":
        return Tile(self.left, self.top, self.right, self.bottom)

    def flip_vertical(self) -> "Tile":
        return Tile(
            reverse_side(self.bottom),
            reverse_side(self.right),
            reverse_side(self.top),
            reverse_side(self.left),
        )

    def flip_horizontal(self) -> "Tile":
        return Tile(
            reverse_side(self.top),
            reverse_side(self.left),
            reverse_side(self.bottom),
            reverse_side(self.right),
        )


def valid_tile_text(lines: List[str]) -> bool:
    return (
        len(lines) == 11
        and re.match(r"Tile (\d+)", lines[0]) is not None
        and all(map(valid_side, lines[1:]))
    )


@require(lambda lines: valid_tile_text(lines))
def parse_tile(lines: List[str]) -> Tuple[int, Tile]:
    match = re.match(r"Tile (\d+)", lines[0])
    assert match
    tileid = int(match.group(1))
    top = lines[1]
    # ERROR: forgot that bottom needs to be reversed, like this:
    # bottom = lines[-1][::-1]
    bottom = lines[-1]
    right = "".join(line[-1] for line in lines[1:])
    left = "".join([line[0] for line in lines[1:]][::-1])
    return (tileid, Tile(top, right, bottom, left))

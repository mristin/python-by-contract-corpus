from collections import defaultdict
from dataclasses import dataclass
import re
import sys
from typing import Dict, List, Set, Tuple

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


@ensure(lambda result: len(result) == len(set(result)))
def transform_tile(tile: Tile) -> Set[Tile]:
    ret: Set[Tile] = set()
    for cur in (tile, tile.flip_vertical(), tile.flip_horizontal()):
        ret.add(cur)
        cur = cur.rotate()
        ret.add(cur)
        cur = cur.rotate()
        ret.add(cur)
        cur = cur.rotate()
        ret.add(cur)
    return ret


@dataclass
class Image(DBC):
    width: int
    tiles: List[Tile]

    def pop(self) -> None:
        self.tiles.pop()

    def attempt_add(self, tile: Tile) -> bool:
        tiles, width = self.tiles, self.width
        count = len(tiles)
        if count == 0:
            self.tiles.append(tile)
            return True
        if count % width > 0:
            # align left with previous right
            if tile.left != reverse_side(tiles[-1].right):
                return False
        # ERROR: This condition should be count >= width
        if count > width:
            # align top with bottom of tile above
            if tile.top != reverse_side(tiles[count - width].bottom):
                return False
        self.tiles.append(tile)
        return True

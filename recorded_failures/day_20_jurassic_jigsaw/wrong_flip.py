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
@invariant(
    lambda self: all(
        valid_side(s) for s in (self.top, self.right, self.bottom, self.left)
    )
)
@invariant(lambda self: self.top[-1] == self.right[0])
@invariant(lambda self: self.right[-1] == self.bottom[0])
@invariant(lambda self: self.bottom[-1] == self.left[0])
@invariant(lambda self: self.left[-1] == self.top[0])
class Tile(DBC):
    top: str
    right: str
    bottom: str
    left: str

    def rotate(self) -> "Tile":
        return Tile(self.left, self.top, self.right, self.bottom)

    def flip_vertical(self) -> "Tile":
        # ERROR: top and bottom must also be flipped, because
        # top goes left-to-right and bottom goes right-to-left.
        return Tile(
            self.bottom, reverse_side(self.right), self.top, reverse_side(self.left)
        )

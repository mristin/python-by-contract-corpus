import dataclasses
from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
import math
import re
import sys
from typing import Dict, List, Optional, Set, Tuple, Final

from icontract import require, ensure, invariant, DBC


def valid_side(side: str) -> bool:
    return re.fullmatch(r"[.#]{10}", side) is not None


@require(lambda side: valid_side(side))
@ensure(lambda result: valid_side(result))
def reverse_side(side: str) -> str:
    return "".join(reversed(side))


class Tile(DBC):
    top: Final[str]
    right: Final[str]
    bottom: Final[str]
    left: Final[str]

    # fmt: off
    @require(
        lambda top, right, bottom, left:
        all(
            valid_side(s) for s in (top, right, bottom, left)
        )
    )
    @require(lambda top, right: top[-1] == right[0])
    @require(lambda right, bottom: right[-1] == bottom[0])
    @require(lambda bottom, left: bottom[-1] == left[0])
    @require(lambda left, top: left[-1] == top[0])
    # fmt: on
    def __init__(self, top: str, right: str, bottom: str, left: str) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

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

    def __repr__(self) -> str:
        return (
            f"top={self.top}, "
            f"right={self.right}, "
            f"bottom={self.bottom}, "
            f"left={self.left}"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tile):
            return (
                self.top == other.top
                and self.right == other.right
                and self.bottom == other.bottom
                and self.left == other.left
            )

        return self == other

    def __hash__(self) -> int:
        return hash((self.top, self.right, self.bottom, self.left))


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
    tiles: List[Tuple[int, Tile]]

    def pop(self) -> Tuple[int, Tile]:
        return self.tiles.pop()

    def attempt_add(self, tile_id: int, tile: Tile) -> bool:
        tiles, width = self.tiles, self.width
        count = len(tiles)
        if count == 0:
            self.tiles.append((tile_id, tile))
            return True
        if count % width > 0:
            # align left with previous right:
            left_id, left_contents = tiles[-1]
            if tile.left != reverse_side(left_contents.right):
                return False
        if count >= width:
            # align top with bottom of tile above:
            above_id, above_contents = tiles[count - width]
            if tile.top != reverse_side(above_contents.bottom):
                return False
        self.tiles.append((tile_id, tile))
        return True


def place_remaining_tiles(image: Image, tiles: Dict[int, Set[Tile]]) -> bool:
    if not tiles:
        return True
    for tile_id, variants in list(tiles.items()):
        for variant in variants:
            if image.attempt_add(tile_id, variant):
                del tiles[tile_id]
                if place_remaining_tiles(image, tiles):
                    return True
                image.pop()
                tiles[tile_id] = variants
    return False


@require(
    lambda tiles: int(math.sqrt(len(tiles))) ** 2 == len(tiles),
    "number of tiles must be a perfect square",
)
def place_tiles(tiles: Dict[int, Set[Tile]]) -> Optional[Image]:
    width = int(math.sqrt(len(tiles)))
    image = Image(width, [])
    if place_remaining_tiles(image, tiles):
        return image
    return None


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
    tile_id = int(match.group(1))
    top = lines[1]
    bottom = lines[-1][::-1]
    right = "".join(line[-1] for line in lines[1:])
    left = "".join([line[0] for line in lines[1:]][::-1])
    return (tile_id, Tile(top, right, bottom, left))


def parse_tiles(text: str) -> Dict[int, Set[Tile]]:
    tiles: Dict[int, Set[Tile]] = {}
    sections = [section.strip().splitlines() for section in text.split("\n\n")]
    for section in sections:
        if not valid_tile_text(section):
            raise ValueError
        tile_id, tile = parse_tile(section)
        tiles[tile_id] = transform_tile(tile)
    return tiles


def main() -> None:
    """Execute the main routine."""
    tiles = parse_tiles(sys.stdin.read())
    image = place_tiles(tiles)
    assert image is not None
    ids = [tid for tid, _ in image.tiles]
    width = image.width
    print(ids)
    print(ids[0] * ids[width - 1] * ids[-width] * ids[-1])


if __name__ == "__main__":
    main()

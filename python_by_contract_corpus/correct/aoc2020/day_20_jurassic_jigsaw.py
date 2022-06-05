import math
import re
import sys
from dataclasses import dataclass
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Final,
    Sequence,
    cast,
    overload,
    Union,
    Iterator,
)

from icontract import require, ensure, DBC

VALID_SIDE_RE = re.compile(r"[.#]{10}")  #: Express the edge of a tile


@require(lambda side: VALID_SIDE_RE.fullmatch(side))
@ensure(lambda result: re.fullmatch(r"[.#]{10}", result))
def reverse_side(side: str) -> str:
    """Flip the side."""
    return "".join(reversed(side))


class Tile(DBC):
    """Represent a tile of the puzzle."""

    top: Final[str]  #: Top side
    right: Final[str]  #: Right side
    bottom: Final[str]  #: Bottom side
    left: Final[str]  #: Left side

    # fmt: off
    @require(
        lambda top, right, bottom, left:
        all(
            VALID_SIDE_RE.fullmatch(side)
            for side in (top, right, bottom, left)
        )
    )
    @require(lambda top, right: top[-1] == right[0])
    @require(lambda right, bottom: right[-1] == bottom[0])
    @require(lambda bottom, left: bottom[-1] == left[0])
    @require(lambda left, top: left[-1] == top[0])
    # fmt: on
    def __init__(self, top: str, right: str, bottom: str, left: str) -> None:
        """Initialize with the given values."""
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def rotate(self) -> "Tile":
        """Copy the tile and rotate it clock-wise."""
        return Tile(self.left, self.top, self.right, self.bottom)

    def flip_vertical(self) -> "Tile":
        """Copy the tile and flip the it along the vertical axis."""
        return Tile(
            reverse_side(self.bottom),
            reverse_side(self.right),
            reverse_side(self.top),
            reverse_side(self.left),
        )

    def flip_horizontal(self) -> "Tile":
        """Copy the tile and flip it along the horizontal axis."""
        return Tile(
            reverse_side(self.top),
            reverse_side(self.left),
            reverse_side(self.bottom),
            reverse_side(self.right),
        )

    def __repr__(self) -> str:
        """Represent the tile as string for easier debugging."""
        return (
            f"top={self.top}, "
            f"right={self.right}, "
            f"bottom={self.bottom}, "
            f"left={self.left}"
        )

    def __eq__(self, other: object) -> bool:
        """
        Compare by sides, if ``other`` is a :py:class:`Tile`.

        Otherwise, by equality.
        """
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
    """Produce the tile transformations by rotating and flipping it."""
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
    """Represent a (partially or fully) assembled puzzle of tiles."""

    width: int  #: Total width of the image
    tiles: List[Tuple[int, Tile]]  #: Assembled tiles

    def pop(self) -> Tuple[int, Tile]:
        """Remove the last tile from the puzzle."""
        return self.tiles.pop()

    def attempt_add(self, tile_id: int, tile: Tile) -> bool:
        """
        Try to add the tile into the image.

        :return: True if successful
        """
        tiles, width = self.tiles, self.width
        count = len(tiles)
        if count == 0:
            self.tiles.append((tile_id, tile))
            return True
        if count % width > 0:
            # align left with previous right:
            _, left_contents = tiles[-1]
            if tile.left != reverse_side(left_contents.right):
                return False
        if count >= width:
            # align top with bottom of tile above:
            _, above_contents = tiles[count - width]
            if tile.top != reverse_side(above_contents.bottom):
                return False
        self.tiles.append((tile_id, tile))
        return True


def place_remaining_tiles(image: Image, tiles: Dict[int, Set[Tile]]) -> bool:
    """
    Try to assemble the remaining tiles into the image.

    :return: True if there are no more tiles left, or if the assembly was possible.
    """
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
    "Number of tiles must be a perfect square",
)
def place_tiles(tiles: Dict[int, Set[Tile]]) -> Optional[Image]:
    """
    Assemble the tiles given as ID 🠒 tile transformations into an image.

    :return: Image, if possible; None if no puzzle could be assembled
    """
    width = int(math.sqrt(len(tiles)))
    image = Image(width, [])
    if place_remaining_tiles(image, tiles):
        return image
    return None


class ValidTileText(DBC):
    """Represent lines to conform to valid tile text."""

    # fmt: off
    @require(
        lambda lines:
        len(lines) == 11
        and re.match(r"Tile (\d+)", lines[0]) is not None
        and all(VALID_SIDE_RE.fullmatch(line) for line in lines[1:]),
        error=ValueError,
        enabled=True
    )
    # fmt: on
    def __new__(cls, lines: Sequence[str]) -> "ValidTileText":
        """Ensure the properties on the ``lines``."""
        return cast(ValidTileText, lines)

    # pylint: disable=function-redefined

    @overload
    def __getitem__(self, index: int) -> str:
        """Get the item at the given integer index."""
        pass

    @overload
    def __getitem__(self, index: slice) -> "ValidTileText":
        """Get the slice of the lines."""
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[str, "ValidTileText"]:
        """Get the line(s) at the given index."""
        raise NotImplementedError("Only for type annotations")

    def __len__(self) -> int:
        """Return the number of the lines."""
        raise NotImplementedError("Only for type annotations")

    def __iter__(self) -> Iterator[str]:
        """Iterate over the lines."""
        raise NotImplementedError("Only for type annotations")


def parse_tile(lines: ValidTileText) -> Tuple[int, Tile]:
    """Parse the ``lines`` into (ID number, tile"""
    match = re.match(r"Tile (\d+)", lines[0])
    assert match
    tile_id = int(match.group(1))
    top = lines[1]
    bottom = lines[-1][::-1]
    right = "".join(line[-1] for line in lines[1:])
    left = "".join([line[0] for line in lines[1:]][::-1])
    return tile_id, Tile(top, right, bottom, left)


def parse_tiles(text: str) -> Dict[int, Set[Tile]]:
    """Parse the input ``text`` into ID number 🠒 possible tile transformations."""
    tiles: Dict[int, Set[Tile]] = {}
    sections = [section.strip().splitlines() for section in text.split("\n\n")]
    for section in sections:
        tile_id, tile = parse_tile(ValidTileText(section))
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

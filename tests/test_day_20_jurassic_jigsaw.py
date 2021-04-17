import re
import textwrap
import unittest
from typing import MutableMapping, Dict, List

import icontract_hypothesis

from aocdbc.day_20_jurassic_jigsaw import *

_EXAMPLE_TILES = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""


class TestCases(unittest.TestCase):
    def test_transform_tile_eq(self) -> None:
        tile1 = Tile(
            "#.........",
            "..........",
            "..........",
            ".........#",
        )
        tile2 = Tile(
            "..........",
            "..........",
            ".........#",
            "#.........",
        )
        self.assertEqual(tile1.flip_vertical(), tile2)
        self.assertEqual(tile2.rotate(), tile1)

    def test_transform_tile(self) -> None:
        tiles = transform_tile(
            Tile(
                "#####.....",
                "..........",
                "..........",
                ".........#",
            )
        )
        self.assertEqual(len(tiles), 8)

    def test_transform_tile_symmetric(self) -> None:
        tiles = transform_tile(
            Tile(
                "#.........",
                "..........",
                "..........",
                ".........#",
            )
        )
        self.assertEqual(len(tiles), 4)

    def test_add_attempt(self) -> None:
        topleft = Tile(
            ".....####.",
            ".#.....##.",
            ".####..#..",
            "..#..###..",
        )
        topright = topleft.flip_horizontal()
        bottomleft = topleft.flip_vertical()
        bottomright = topleft.rotate().rotate()
        image = Image(2, [(1, topleft)])
        self.assertFalse(image.attempt_add(1, topleft))
        self.assertTrue(image.attempt_add(1, topright))
        self.assertFalse(image.attempt_add(1, topleft))
        self.assertTrue(image.attempt_add(1, bottomleft))
        self.assertFalse(image.attempt_add(1, topright))
        self.assertFalse(image.attempt_add(1, bottomleft))
        self.assertTrue(image.attempt_add(1, bottomright))

    def test_parse_tile(self) -> None:
        tileid, tile = parse_tile(
            [
                "Tile 2311:",
                "..##.#..#.",
                "##..#.....",
                "#...##..#.",
                "####.#...#",
                "##.##.###.",
                "##...#.###",
                ".#.#.#..##",
                "..#....#..",
                "###...#.#.",
                "..###..###",
            ]
        )
        self.assertEqual(tileid, 2311)
        self.assertEqual(tile.right, "...#.##..#")
        self.assertEqual(tile.left, ".#..#####.")

    def test_example(self) -> None:
        tiles = parse_tiles(_EXAMPLE_TILES)
        image = place_tiles(tiles)
        assert image is not None
        ids = [tid for tid, _ in image.tiles]
        self.assertEqual(ids[0] * ids[2] * ids[6] * ids[8], 20899048083289)


class TestWithIcontractHypothesis(unittest.TestCase):
    # TODO: regex filters too much
    # def test_reverse_side_with_icontract_hypothesis(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(reverse_side)
    pass


if __name__ == "__main__":
    unittest.main()

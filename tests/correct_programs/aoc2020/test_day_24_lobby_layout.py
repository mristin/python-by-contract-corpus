import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_24_lobby_layout


class TestParseLine(unittest.TestCase):
    def test_case(self) -> None:
        line = "nwwswee"
        directions = day_24_lobby_layout.parse_line(line=line)

        self.assertListEqual(
            [
                day_24_lobby_layout.VALUE_TO_DIRECTION["nw"],
                day_24_lobby_layout.VALUE_TO_DIRECTION["w"],
                day_24_lobby_layout.VALUE_TO_DIRECTION["sw"],
                day_24_lobby_layout.VALUE_TO_DIRECTION["e"],
                day_24_lobby_layout.VALUE_TO_DIRECTION["e"],
            ],
            directions,
        )

    def test_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(day_24_lobby_layout.parse_line)

    def test_empty_case_of_stringify(self) -> None:
        result = day_24_lobby_layout.stringify_directions(directions=[])
        self.assertEqual("", result)

    def test_stringify_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_24_lobby_layout.stringify_directions
        )


class TestCounFlips(unittest.TestCase):
    def test_case(self) -> None:
        text = textwrap.dedent(
            """\
            sesenwnenenewseeswwswswwnenewsewsw
            neeenesenwnwwswnenewnwwsewnenwseswesw
            seswneswswsenwwnwse
            nwnwneseeswswnenewneswwnewseswneseene
            swweswneswnenwsewnwneneseenw
            eesenwseswswnenwswnwnwsewwnwsene
            sewnenenenesenwsewnenwwwse
            wenwwweseeeweswwwnwwe
            wsweesenenewnwwnwsenewsenwwsesesenwne
            neeswseenwwswnwswswnw
            nenwswwsewswnenenewsenwsenwnesesenew
            enewnwewneswsewnwswenweswnenwsenwsw
            sweneswneswneneenwnewenewwneswswnese
            swwesenesewenwneswnwwneseswwne
            enesenwswwswneneswsenwnewswseenwsese
            wnwnesenesenenwwnenwsewesewsesesew
            nenewswnwewswnenesenwnesewesw
            eneswnwswnwsenenwnwnwwseeswneewsenese
            neswnwewnwnwseenwseesewsenwsweewe
            wseweeenwnesenwwwswnew"""
        )

        lines = text.split("\n")

        plan = [day_24_lobby_layout.parse_line(line) for line in lines]

        result = day_24_lobby_layout.count_flips(plan=plan)
        self.assertEqual(10, result)

    def test_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_24_lobby_layout.count_flips
        )


if __name__ == "__main__":
    unittest.main()

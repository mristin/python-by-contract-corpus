import textwrap
import unittest

import icontract_hypothesis

from python_by_contract_corpus.aoc2020 import day_24_lobby_layout


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_24_lobby_layout.parse_line,
            day_24_lobby_layout.stringify_directions,
            day_24_lobby_layout.count_flips,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


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

    def test_empty_case_of_stringify(self) -> None:
        result = day_24_lobby_layout.stringify_directions(directions=[])
        self.assertEqual("", result)


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


if __name__ == "__main__":
    unittest.main()

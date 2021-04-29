import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_3_toboggan_trajectory


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_3_toboggan_trajectory.parse_input,
            # NOTE: pre-condition too strict for icontract-hypothesis
            # day_3_toboggan_trajectory.count_trees
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        example_input = textwrap.dedent(
            """\
            ..##.......
            #...#...#..
            .#....#..#.
            ..#.#...#.#
            .#...##..#.
            ..#.##.....
            .#.#.#....#
            .#........#
            #.##...#...
            #...##....#
            .#..#...#.#"""
        )

        self.assertEqual(
            7,
            day_3_toboggan_trajectory.count_trees(
                *day_3_toboggan_trajectory.parse_input(example_input)
            ),
        )


if __name__ == "__main__":
    unittest.main()

import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_3_toboggan_trajectory


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual(
            7,
            day_3_toboggan_trajectory.count_trees(
                *day_3_toboggan_trajectory.parse_input(_example_input)
            ),
        )

    def test_parse_input_file_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_3_toboggan_trajectory.parse_input
        )

    # Preconditions too strict for icontract-hypothesis
    # def test_count_trees_with_icontract_hypothesis(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(count_trees)


_example_input = """..##.......
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

if __name__ == "__main__":
    unittest.main()

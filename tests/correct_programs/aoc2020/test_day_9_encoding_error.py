import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_9_encoding_error


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual((14, 127), day_9_encoding_error.solve(_example_data, 5))

    def test_solve_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(day_9_encoding_error.solve)


_example_data = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]

if __name__ == "__main__":
    unittest.main()

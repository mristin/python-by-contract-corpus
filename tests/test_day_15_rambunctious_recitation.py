import textwrap
import unittest

import icontract_hypothesis

from aocdbc.day_15_rambunctious_recitation import solve


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_solve(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(solve)


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        test_input = [
            [0, 3, 6],
            [1, 3, 2],
            [2, 1, 3],
            [1, 2, 3],
            [2, 3, 1],
            [3, 2, 1],
            [3, 1, 2],
        ]
        expected_output = [436, 1, 10, 27, 78, 438, 1836]

        for test_pair in zip(test_input, expected_output):
            self.assertEqual(solve(test_pair[0]), test_pair[1])


if __name__ == "__main__":
    unittest.main()

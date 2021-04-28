import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_6_custom_customs


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual(11, day_6_custom_customs.solve(_example_data))

    def test_solve_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(day_6_custom_customs.solve)


if __name__ == "__main__":
    unittest.main()


_example_data = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""

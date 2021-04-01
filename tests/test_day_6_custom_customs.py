import unittest

import icontract_hypothesis

from aocdbc.day_6_custom_customs import solve


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual(solve(_example_data), 11)

    def test_solve_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            solve
        )


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
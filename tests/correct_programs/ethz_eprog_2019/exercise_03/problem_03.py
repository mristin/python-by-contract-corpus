import unittest

import icontract_hypothesis
from icontract import require

from correct_programs.ethz_eprog_2019.exercise_03 import problem_03


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda x: -1000 < x < 1000)
        @require(lambda y: -1000 < y < 1000)
        @require(lambda x: x > 0)
        @require(lambda y: y > 0)
        def gcd_with_restricted_input(x: int, y: int) -> int:
            return problem_03.gcd(x, y)

        for func in [gcd_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        result = problem_03.gcd(x=36, y=44)

        self.assertEqual(4, result)


if __name__ == "__main__":
    unittest.main()

import unittest
from typing import cast, List

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_02 import problem_05_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_05_02.draw]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        result = problem_05_02.draw(height=9)

        self.assertListEqual(
            [
                "....1....",
                "...222...",
                "..33333..",
                "444444444",
                "555555555",
                ".6666666.",
                "..77777..",
                "...888...",
                "....9....",
            ],
            cast(List[str], result),
        )


if __name__ == "__main__":
    unittest.main()

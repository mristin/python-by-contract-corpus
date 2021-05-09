import unittest
from typing import cast, List

import icontract_hypothesis
from icontract import require

from correct_programs.common import Lines
from correct_programs.ethz_eprog_2019.exercise_02 import problem_03


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda height: height < 100)
        @require(lambda width: width < 100)
        @require(lambda width: width > 0)
        @require(lambda width: width % 5 == 0)
        @require(lambda height: height > 0)
        @require(lambda height: height % 5 == 0)
        def draw_with_restricted_input(width: int, height: int) -> Lines:
            return problem_03.draw(width=width, height=height)

        for func in [draw_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        result = problem_03.draw(width=35, height=15)

        self.assertListEqual(
            [
                "-----------------------------------",
                "|                                 |",
                "|                                 |",
                "|             +++++++             |",
                "|             +++++++             |",
                "|             +++++++             |",
                "|      +++++++++++++++++++++      |",
                "|      +++++++++++++++++++++      |",
                "|      +++++++++++++++++++++      |",
                "|             +++++++             |",
                "|             +++++++             |",
                "|             +++++++             |",
                "|                                 |",
                "|                                 |",
                "-----------------------------------",
            ],
            cast(List[str], result),
        )


if __name__ == "__main__":
    unittest.main()

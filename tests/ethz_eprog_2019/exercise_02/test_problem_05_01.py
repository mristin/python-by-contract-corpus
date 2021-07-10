import textwrap
import unittest
from typing import cast, List

from icontract import require
import icontract_hypothesis

from python_by_contract_corpus.common import Lines
from python_by_contract_corpus.ethz_eprog_2019.exercise_02 import problem_05_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda width: width < 100)
        @require(lambda width: width > 0)
        @require(lambda width: width % 4 == 0)
        def draw_with_restricted_input(width: int) -> Lines:
            return problem_05_01.draw(width=width)

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
        result = problem_05_01.draw(width=12)

        self.assertListEqual(
            [
                "**..**..**..",
                "..**..**..**",
                "**..**..**..",
                "..**..**..**",
                "**..**..**..",
                "..**..**..**",
            ],
            cast(List[str], result),
        )


if __name__ == "__main__":
    unittest.main()

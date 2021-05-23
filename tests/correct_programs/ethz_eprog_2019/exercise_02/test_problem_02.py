import unittest
from typing import cast, List

import icontract_hypothesis
from icontract import require

from correct_programs.common import Lines
from correct_programs.ethz_eprog_2019.exercise_02 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda width: width < 100)
        @require(lambda width: width > 0)
        @require(lambda width: width % 2 == 0)
        def draw_with_restricted_input(width: int) -> Lines:
            return problem_02.draw(width=width)

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
        result = problem_02.draw(width=6)

        # Python raw strings must not terminate with a backslash, so we need to include
        # the second half of the bottom lines manually.
        self.assertListEqual(
            [
                r"  \/",
                r" \\//",
                r"\\\///",
                r"///" + "\\\\\\",
                r" //" + "\\\\",
                r"  /" + "\\",
            ],
            cast(List[str], result),
        )


if __name__ == "__main__":
    unittest.main()

import unittest
from typing import Set

import icontract_hypothesis
from icontract import require

from correct_programs.ethz_eprog_2019.exercise_09 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_02.ReversableLinkedList.reverse]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()
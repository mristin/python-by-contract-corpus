import unittest

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_03 import problem_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda n: n > 0)
        @require(lambda n: n < 1000)
        def compute_with_restricted_input(n: int) -> float:
            return problem_01.compute(n=n)

        for func in [compute_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

import unittest

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_04 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        # We need to restrict the input as the original problem statement does not
        # specify what to do if the approximation is numerically not possible.
        @require(lambda c: c > 0)
        @require(lambda c: c < 1000 * 1000)
        @require(lambda eps: eps > 1e-6)
        def compute_sqrt_with_restricted_input(c: int, eps: float) -> float:
            return problem_02.approximate_sqrt(c=c, eps=eps)

        for func in [compute_sqrt_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

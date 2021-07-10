import unittest
from typing import Set

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.ethz_eprog_2019.exercise_08 import problem_05


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda trials: 0 <= trials < 10)
        @require(lambda grid_size: 3 <= grid_size < 10)
        @require(lambda grid_size: grid_size % 2 == 1)
        def restricted_simulate(trials: int, grid_size: int) -> float:
            return problem_05.simulate(trials=trials, grid_size=grid_size)

        for func in [restricted_simulate]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

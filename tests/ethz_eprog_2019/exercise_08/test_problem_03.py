import unittest
from typing import Set

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.ethz_eprog_2019.exercise_08 import problem_03


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda steps: 0 <= steps < 100)
        def restricted_simulate(
            specs: problem_03.Specs, steps: int
        ) -> problem_03.Stats:
            return problem_03.simulate(specs, steps)

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

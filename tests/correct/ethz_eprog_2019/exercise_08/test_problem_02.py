import unittest
from typing import Set

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_08 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda text, length: 0 <= length <= len(text))
        @require(lambda text: len(text) < 10)
        def restricted_list_subsequences(text: str, length: int) -> Set[str]:
            return problem_02.list_subsequences(text, length)

        for func in [problem_02.is_subsequence, restricted_list_subsequences]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

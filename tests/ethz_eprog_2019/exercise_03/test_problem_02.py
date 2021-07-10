import unittest

import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.ethz_eprog_2019.exercise_03 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        @require(lambda n: n > 0)
        @require(lambda n: n < 1000)
        def repr_bin_with_restricted_input(n: int) -> str:
            return problem_02.repr_binary(n=n)

        for func in [repr_bin_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        result = problem_02.repr_binary(n=14)

        self.assertEqual("0b1110", result)


if __name__ == "__main__":
    unittest.main()

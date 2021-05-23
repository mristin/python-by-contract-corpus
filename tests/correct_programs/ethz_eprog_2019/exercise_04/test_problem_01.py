import unittest
from typing import List

import icontract_hypothesis
from icontract import require, ensure

from correct_programs.ethz_eprog_2019.exercise_04 import problem_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        # fmt: off
        @require(lambda limit: 2 < limit < 1000)
        @ensure(
            lambda result:
            all(problem_01.naive_is_prime(number) for number in result)
        )
        # fmt: on
        def sieve_with_restricted_input(limit: int) -> List[int]:
            return problem_01.sieve(limit=limit)

        for func in [sieve_with_restricted_input]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

import unittest

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_05 import problem_03


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_03.compute_stats, problem_03.compute_histogram]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

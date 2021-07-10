import unittest

import icontract_hypothesis

from python_by_contract_corpus.ethz_eprog_2019.exercise_05 import problem_04


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            problem_04.most_booked_room,
            problem_04.longest_booked_room,
            problem_04.room_with_most_revenue,
            problem_04.total_revenue,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


if __name__ == "__main__":
    unittest.main()

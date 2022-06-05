import unittest

import icontract_hypothesis

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_05 import problem_04


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


class TestManually(unittest.TestCase):
    def test_numerical_edge_case_for_entry_collection(self) -> None:
        entry = problem_04.Entry(
            room_number=1,
            start=1,
            end=257,
            price_per_day=6.994914921643253e299,
            price_discount=0.0,
        )

        _ = problem_04.total_revenue(entries=[entry])


if __name__ == "__main__":
    unittest.main()

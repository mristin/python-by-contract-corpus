import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_13_shuttle_search


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_13_shuttle_search.next_departure,
            day_13_shuttle_search.find_departure,
            # NOTE: not testing this; it's too hard to match the regex
            # day_13_shuttle_search.parse_input
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(
            (944, 59), day_13_shuttle_search.find_departure(939, {7, 13, 59, 31, 19})
        )


if __name__ == "__main__":
    unittest.main()

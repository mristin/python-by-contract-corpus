import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_13_shuttle_search


class TestManually(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(
            (944, 59), day_13_shuttle_search.find_departure(939, {7, 13, 59, 31, 19})
        )


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_next_departure(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_13_shuttle_search.next_departure
        )

    def test_find_departure(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_13_shuttle_search.find_departure
        )

    # NOTE: not testing this; it's too hard to match the regex
    # def test_parse_input(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(parse_input)


if __name__ == "__main__":
    unittest.main()

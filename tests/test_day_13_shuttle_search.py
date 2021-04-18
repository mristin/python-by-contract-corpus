import unittest
from typing import List, Callable, Any

import icontract_hypothesis

from aocdbc.day_13_shuttle_search import *


class TestManually(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(find_departure(939, {7, 13, 59, 31, 19}), (944, 59))


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_next_departure(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(next_departure)

    def test_find_departure(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(find_departure)

    # NOTE: not testing this; it's too hard to match the regex
    # def test_parse_input(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(parse_input)


if __name__ == "__main__":
    unittest.main()

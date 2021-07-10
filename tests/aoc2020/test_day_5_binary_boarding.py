import unittest
from typing import Callable, Any

import icontract_hypothesis
from icontract_hypothesis import CallableT

from python_by_contract_corpus.aoc2020 import day_5_binary_boarding


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_5_binary_boarding.determine_row_and_column,
            day_5_binary_boarding.determine_id,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ("BFFFBBFRRR", 70, 7, 567),
            ("FFFBBBFRRR", 14, 7, 119),
            ("BBFFBBFRLL", 102, 4, 820),
        ]

        for identifier, expected_row, expected_column, expected_id in cases:
            row, column = day_5_binary_boarding.determine_row_and_column(
                identifier=identifier
            )

            seat_id = day_5_binary_boarding.determine_id(row=row, column=column)

            self.assertEqual(expected_row, row, identifier)
            self.assertEqual(expected_column, column, identifier)
            self.assertEqual(expected_id, seat_id, identifier)


if __name__ == "__main__":
    unittest.main()

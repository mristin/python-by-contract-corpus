import unittest

import icontract_hypothesis

import aocdbc.day_5_binary_boarding


class TestDay5(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ("BFFFBBFRRR", 70, 7, 567),
            ("FFFBBBFRRR", 14, 7, 119),
            ("BBFFBBFRLL", 102, 4, 820),
        ]

        for identifier, expected_row, expected_column, expected_id in cases:
            row, column = aocdbc.day_5_binary_boarding.determine_row_and_column(
                identifier=identifier
            )

            seat_id = aocdbc.day_5_binary_boarding.determine_id(row=row, column=column)

            self.assertEqual(expected_row, row, identifier)
            self.assertEqual(expected_column, column, identifier)
            self.assertEqual(expected_id, seat_id, identifier)

    def test_determine_row_and_column_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_5_binary_boarding.determine_row_and_column
        )

    def test_determine_id_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_5_binary_boarding.determine_id
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from icontract_hypothesis import test_with_inferred_strategy

from correct_programs.aoc2020.day_25_combo_breaker import (
    deduce_encryption_key,
    transform,
    symmetric_encryption_keys,
)


class TestDay25(unittest.TestCase):
    def test_part_1(self) -> None:
        self.assertEqual(deduce_encryption_key(9093927, 11001876), 12227206)

    # NOTE: the hypothesis tests are disabled. When there aren't obvious bugs,
    # hypothesis will try some large numeric values and essentially hang the
    # process, since we drive loop iterations based on those numbers.
    def TODO_test_verify_with_icontract_hypothesis(self) -> None:
        test_with_inferred_strategy(transform)

    def TODO_test_keys_with_icontract_hypothesis(self) -> None:
        test_with_inferred_strategy(symmetric_encryption_keys)


if __name__ == "__main__":
    unittest.main()

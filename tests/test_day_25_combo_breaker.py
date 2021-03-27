import unittest

from icontract_hypothesis import test_with_inferred_strategy

from aocdbc.day_25_combo_breaker import deduce_encryption_key
from aocdbc.day_25_combo_breaker import transform


class TestDay1(unittest.TestCase):
    def test_part_1(self) -> None:
        self.assertEqual(deduce_encryption_key(9093927, 11001876), 12227206)

    def TODO_test_verify_with_icontract_hypothesis(self) -> None:
        test_with_inferred_strategy(transform)


if __name__ == "__main__":
    unittest.main()

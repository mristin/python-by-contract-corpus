import unittest

import icontract_hypothesis
from icontract import require, ensure

from python_by_contract_corpus.aoc2020 import day_25_combo_breaker


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        # We need to add more constraints so that the function is testable.
        @require(lambda loop_size: loop_size >= 0)
        @require(lambda loop_size: loop_size < 1000)
        @require(lambda subject: subject >= 0)
        def transform_testable(subject: int, loop_size: int) -> int:
            return day_25_combo_breaker.transform(subject, loop_size)

        for func in [transform_testable]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        self.assertEqual(
            12227206, day_25_combo_breaker.deduce_encryption_key(9093927, 11001876)
        )


if __name__ == "__main__":
    unittest.main()

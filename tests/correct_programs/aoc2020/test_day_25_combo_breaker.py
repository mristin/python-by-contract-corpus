import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_25_combo_breaker


class TestWithIcontractHypothesis(unittest.TestCase):
    def setUp(self) -> None:
        day_25_combo_breaker.TESTING_WITH_ICONTRACT_HYPOTHESIS = True

    def tearDown(self) -> None:
        day_25_combo_breaker.TESTING_WITH_ICONTRACT_HYPOTHESIS = False

    def test_functions(self) -> None:
        for func in [
            day_25_combo_breaker.transform,
        ]:
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

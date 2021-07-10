import textwrap
import unittest

import icontract_hypothesis

from python_by_contract_corpus.aoc2020 import day_15_rambunctious_recitation


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [day_15_rambunctious_recitation.solve]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        test_inputs = [
            [0, 3, 6],
            [1, 3, 2],
            [2, 1, 3],
            [1, 2, 3],
            [2, 3, 1],
            [3, 2, 1],
            [3, 1, 2],
        ]
        expected_outputs = [436, 1, 10, 27, 78, 438, 1836]

        for test_input, expected_output in zip(test_inputs, expected_outputs):
            self.assertEqual(
                expected_output, day_15_rambunctious_recitation.solve(test_input)
            )


if __name__ == "__main__":
    unittest.main()

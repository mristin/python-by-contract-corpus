import unittest

import icontract_hypothesis

from python_by_contract_corpus.correct.aoc2020 import day_2_password_philosophy


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            # NOTE: test ``verify`` once icontract-hypothesis is more powerful.
            # day_2_password_philosophy.verify,
            day_2_password_philosophy.verify_line,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ("1-3 a: abcde", True),
            ("1-3 b: cdefg", False),
            ("2-9 c: ccccccccc", True),
        ]

        for line, expected_result in cases:
            result = day_2_password_philosophy.verify_line(line=line)
            self.assertEqual(expected_result, result)


if __name__ == "__main__":
    unittest.main()

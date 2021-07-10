import unittest

import icontract_hypothesis

from python_by_contract_corpus.ethz_eprog_2019.exercise_06 import problem_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_01.time_in_swiss_german]:
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
            ((0, 0), "12i znacht"),
            ((1, 45), "viertel vor 2 znacht"),
            ((9, 25), "5 vor halbi 10i am morge"),
            ((12, 1), "1 ab 12i am mittag"),
            ((16, 46), "14 vor 5i am namittag"),
            ((21, 51), "9 vor 10i am abig"),
            ((22, 37), "7 ab halbi 11i znacht"),
        ]

        for (hour, minute), expected_text in cases:
            self.assertEqual(
                expected_text, problem_01.time_in_swiss_german(hour, minute)
            )


if __name__ == "__main__":
    unittest.main()

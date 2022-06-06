import unittest
import icontract_hypothesis

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_08 import problem_01

# pylint: disable=no-self-use


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_01.matches]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_matches(self) -> None:
        self.assertTrue(problem_01.matches("a", "a", 0))
        self.assertFalse(problem_01.matches("", "a", 0))
        self.assertTrue(problem_01.matches("ab", "ba", 2))
        self.assertTrue(problem_01.matches("...a..b...", "ba", 2))
        self.assertFalse(problem_01.matches("...a...b...", "ba", 2))
        self.assertTrue(problem_01.matches("abbbc", "cab", 1))
        self.assertFalse(problem_01.matches("abbbbc", "cab", 1))


if __name__ == "__main__":
    unittest.main()

import unittest
import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_08.problem_01 import matches

# pylint: disable=no-self-use


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_matches(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(matches)


class TestManually(unittest.TestCase):
    def test_matches(self) -> None:
        self.assertTrue(matches("a", "a", 0))
        self.assertFalse(matches("", "a", 0))
        self.assertTrue(matches("ab", "ba", 2))
        self.assertTrue(matches("...a..b...", "ba", 2))
        self.assertFalse(matches("...a...b...", "ba", 2))
        self.assertTrue(matches("abbbc", "cab", 1))
        self.assertFalse(matches("abbbbc", "cab", 1))


if __name__ == "__main__":
    unittest.main()

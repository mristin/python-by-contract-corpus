import textwrap
import unittest

import icontract_hypothesis

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_12 import problem_04


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            problem_04.tokens_to_words,
            problem_04.tokenize,
            problem_04.find_top,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        text = textwrap.dedent(
            """\
            A B; 
            B C, D.
            A"""
        )

        tokens = problem_04.tokenize(text)
        words = problem_04.tokens_to_words(tokens)
        top_words = problem_04.find_top(words, limit=2)

        self.assertEqual(2, len(top_words))
        self.assertEqual("a", top_words[0].text)
        self.assertEqual(0, top_words[0].first)
        self.assertEqual(5, top_words[0].last)

        self.assertEqual("b", top_words[1].text)
        self.assertEqual(1, top_words[1].first)
        self.assertEqual(2, top_words[1].last)


if __name__ == "__main__":
    unittest.main()

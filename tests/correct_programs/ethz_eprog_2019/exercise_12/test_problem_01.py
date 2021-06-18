import random
import textwrap
import unittest

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_12 import problem_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            # NOTE: add the function once icontract-hypothesis handles relations.
            # problem_02.tokens_to_text
            problem_01.unparse
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestParseUnparse(unittest.TestCase):
    def test_cases_discovered_by_icontract_hypothesis(self) -> None:
        table = [
            ("A = sin((A));\n", "A = sin(A);\n"),
            ("A = sin(-A);\n", "A = sin(-(A));\n"),
            ("A = 1.0 + inf;\n", "A = (1.0)+(inf);\n"),
            ("A = 5e-324 + 5e-324;\n", "A = (5e-324)+(5e-324);\n"),
            ("A = 1e+16;\n", "A = 1e+16;\n"),
        ]

        for text, expected_unparsed in table:
            tokens = problem_01.tokenize(text=text)
            program = problem_01.parse_program(tokens=tokens)
            unparsed = problem_01.unparse(program)

            self.assertEqual(expected_unparsed, unparsed, f"{text=}")


class TestInterpret(unittest.TestCase):
    def test_cases(self) -> None:
        text, expected_variables = (
            textwrap.dedent(
                """\
                i = 1;
                t = 2;
                PI = 3.14159265359;
                alpha = i * ((2*PI) * (1 / 6.05));
                size = (0.25 * cos(t/2)) + 0.75;
                
                x = cos(alpha + (0.3 * t)) * size;
                y = sin((1.5 * alpha) + t) * size;
                
                r = (cos(alpha + (2 * t)) + 1) / 2;
                g = (sin(alpha + (2 * t)) + 1) / 2;
                b = (cos(alpha +  (PI/2)) + 1) / 2;
                """
            ),
            {
                "i": 1.0,
                "t": 2.0,
                "PI": 3.14159265359,
                "alpha": 1.0385430259801653,
                "size": 0.8850755764670349,
                "x": -0.05991509307855157,
                "y": -0.35784295595007254,
                "r": 0.660201102565014,
                "g": 0.026359200725957432,
                "b": 0.06916711880146942,
            },
        )

        tokens = problem_01.tokenize(text=text)
        program = problem_01.parse_program(tokens=tokens)
        variables = problem_01.interpret(program=program)

        self.assertDictEqual(expected_variables, variables)  # type: ignore


if __name__ == "__main__":
    unittest.main()

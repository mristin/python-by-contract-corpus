import random
import unittest

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_11 import problem_02


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        def smoke_test_evaluate_call(call: problem_02.Call) -> None:
            names = problem_02.collect_variables(call)
            lookup = {name: random.random() for name in names}

            try:
                problem_02.evaluate(expr=call, lookup=lookup)
            except Exception as exception:
                # Ignore errors where we end up with complex numbers or mathematical
                # domain errors
                if not isinstance(exception, TypeError) and (
                    not isinstance(exception, ValueError)
                    and str(exception) == "math domain error"
                ):
                    raise AssertionError(
                        f"{smoke_test_evaluate_call.__name__} failed.\n"
                        f"{problem_02.unparse(call)=}\n"
                        f"{lookup=}"
                    ) from exception

        def smoke_test_evaluate_expr(expr: problem_02.Expr) -> None:
            names = problem_02.collect_variables(expr)
            lookup = {name: random.random() for name in names}

            try:
                problem_02.evaluate(expr=expr, lookup=lookup)
            except Exception as exception:
                # Ignore errors where we end up with complex numbers or mathematical
                # domain errors
                if not isinstance(exception, TypeError) and (
                    not isinstance(exception, ValueError)
                    and str(exception) == "math domain error"
                ):
                    raise AssertionError(
                        f"{smoke_test_evaluate_expr.__name__} failed.\n"
                        f"{problem_02.unparse(expr)=}\n"
                        f"{lookup=}"
                    ) from exception

        for func in [
            # NOTE: add the function once icontract-hypothesis handles relations.
            # problem_02.tokens_to_text
            problem_02.unparse,
            smoke_test_evaluate_call,
            smoke_test_evaluate_expr,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestParse(unittest.TestCase):
    def test_a_random_expression(self) -> None:
        text = "(-(A))+(A)"
        tokens = problem_02.tokenize(text=text)
        expr = problem_02.parse_tokens(tokens=tokens)

        unparsed = problem_02.unparse(expr)

        self.assertEqual("(-(A))+(A)", unparsed)


if __name__ == "__main__":
    unittest.main()

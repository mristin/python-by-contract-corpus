import textwrap
import unittest
from typing import Dict, Any

import hypothesis
import icontract_hypothesis
from icontract import require

from python_by_contract_corpus.correct.ethz_eprog_2019.exercise_12 import (
    problem_01,
    problem_03,
)


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            problem_03.compile_program,
            problem_03._execute_const,
            problem_03._execute_store,
            problem_03._execute_unary_operation,
            # NOTE: uncomment once icontract-hypothesis is powerful enough
            # problem_03._execute_load,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error

    def test_binary_operation(self) -> None:
        strategy = icontract_hypothesis.infer_strategy(
            problem_03._execute_binary_operation
        )

        @hypothesis.given(strategy)
        def execute(kwargs: Dict[str, Any]) -> None:
            try:
                problem_03._execute_binary_operation(**kwargs)
            except (OverflowError, ZeroDivisionError):
                pass

        execute()

    def test_call(self) -> None:
        func_to_execute = problem_03._execute_call

        strategy = icontract_hypothesis.infer_strategy(func_to_execute)

        @hypothesis.given(strategy)
        def execute(kwargs: Dict[str, Any]) -> None:
            try:
                func_to_execute(**kwargs)
            except (OverflowError, ZeroDivisionError, ValueError):
                pass

        execute()

    def test_compile_and_execute_binary_operation_without_variables(self) -> None:
        @require(lambda left: left >= 0)
        @require(lambda right: right >= 0)
        def restricted(operator: problem_01.BinOp, left: float, right: float) -> None:
            stmt = problem_01.Assign(
                target=problem_01.Identifier("x"),
                expr=problem_01.BinaryOperation(
                    left=problem_01.Constant(left),
                    operator=operator,
                    right=problem_01.Constant(right),
                ),
            )

            program = problem_01.Program(body=[stmt])

            try:
                problem_03.compile_and_execute(program)
            except (ValueError, OverflowError, ZeroDivisionError):
                pass

        icontract_hypothesis.test_with_inferred_strategy(restricted)


class TestManually(unittest.TestCase):
    def test_compile(self) -> None:
        text = "a = (b + 1) / sin(2 * c);"

        tokens = problem_01.tokenize(text=text)
        program = problem_01.parse_program(tokens=tokens)
        instructions = problem_03.compile_program(program)

        self.assertEqual(
            "["
            "Load('b'), "
            "Const(1.0), "
            "BinaryOperation(<BinOp.ADD: '+'>), "
            "Const(2.0), "
            "Load('c'), "
            "BinaryOperation(<BinOp.MUL: '*'>), "
            "Call(<Function.SIN: 'sin'>), "
            "BinaryOperation(<BinOp.DIV: '/'>), "
            "Store('a')"
            "]",
            repr(instructions),
        )

    def test_compile_and_execute(self) -> None:
        table = [
            "PI = 3.14159265359;",
            "x = 3; a = -x; b = x + 3; c = sin(x);",
            "b = 1; c = 2; a = (b + 1) / sin(2 * c);" "x = 1 / 6.05;",
            textwrap.dedent(
                """\
                i = 1;
                t = 2;
                PI = 3.14159265359;
                alpha = i * ((2*PI) * (1 / 6.05));
                """
            ),
        ]

        for text in table:
            tokens = problem_01.tokenize(text=text)
            program = problem_01.parse_program(tokens=tokens)

            problem_03.compile_and_execute(program)


if __name__ == "__main__":
    unittest.main()

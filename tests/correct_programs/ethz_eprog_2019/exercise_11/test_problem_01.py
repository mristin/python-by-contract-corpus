import textwrap
import unittest
from decimal import Decimal
from typing import Set

import icontract_hypothesis
from icontract import require

from correct_programs.common import Lines
from correct_programs.ethz_eprog_2019.exercise_11 import problem_01


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            # NOTE: add this function once icontract-hypothesis handles set membership
            # correctly.
            # problem_01.critical,
            problem_01.top
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_critical(self) -> None:
        text = textwrap.dedent(
            """\
            111111004  5.0  5.0  6.0
            111111005  3.75 3.0  4.0
            111111006  4.5  2.25 4.0"""
        )

        lines = Lines(text.splitlines())

        gradings = problem_01.parse(lines=lines)
        critical_gradings = problem_01.critical(
            gradings=gradings,
            bound1=problem_01.Grade(Decimal("4.0")),
            bound2=Decimal("8.0"),
        )

        self.assertListEqual([gradings[1]], critical_gradings)

    def test_top(self) -> None:
        text = textwrap.dedent(
            """\
            111111004  5.0  5.0  6.0
            111111005  3.75 3.0  4.0
            111111006  4.5  2.25 4.0"""
        )

        lines = Lines(text.splitlines())

        gradings = problem_01.parse(lines=lines)
        top_gradings = problem_01.top(gradings=gradings, limit=2)

        self.assertListEqual([gradings[0], gradings[1]], top_gradings)


if __name__ == "__main__":
    unittest.main()

import textwrap
import unittest
from typing import Set

import icontract_hypothesis
from icontract import require

from correct_programs.common import Lines
from correct_programs.ethz_eprog_2019.exercise_09 import problem_03


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            problem_03.compute_totals,
            # NOTE: uncomment when icontract-hypothesis improved
            # problem_03.parse_block
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        text = textwrap.dedent(
            """\
            Michaela Meier
            LX326 05.12.2016 ECONOMY
            LX317 10.01.2017 ECONOMY
            A3851 12.05.2017 BUSINESS
            LX8 12.10.2017 FIRST 4433
            .
            Stefan Oliver Schmid
            LX4150 19.10.2017 BUSINESS 6404
            ."""
        )

        lines = Lines(text.splitlines())
        blocks = problem_03.parse(lines=lines)
        totals = problem_03.compute_totals(blocks=blocks)

        self.assertDictEqual(
            {"Michaela Meier": 13799, "Stefan Oliver Schmid": 12808},
            totals,  # type: ignore
        )


if __name__ == "__main__":
    unittest.main()

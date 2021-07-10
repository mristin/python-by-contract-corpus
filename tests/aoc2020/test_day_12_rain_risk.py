import textwrap
import unittest

import icontract_hypothesis

from python_by_contract_corpus.aoc2020 import day_12_rain_risk


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_12_rain_risk.parse_input,
            day_12_rain_risk.update_position,
            day_12_rain_risk.solve,
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
        example_input = textwrap.dedent(
            """\
            F10
            N3
            F7
            R90
            F11"""
        )

        self.assertEqual(
            day_12_rain_risk.ShipPosition(
                horizontal=17,
                vertical=-8,
                orientation=day_12_rain_risk.Orientation.SOUTH,
            ),
            day_12_rain_risk.solve(example_input),
        )


if __name__ == "__main__":
    unittest.main()

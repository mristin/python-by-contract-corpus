import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_12_rain_risk


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual(
            day_12_rain_risk.ShipPosition(
                horizontal=17,
                vertical=-8,
                orientation=day_12_rain_risk.Orientation.SOUTH,
            ),
            day_12_rain_risk.solve(_example_input),
        )

    def test_parse_input_file_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(day_12_rain_risk.parse_input)

    def test_update_position_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_12_rain_risk.update_position
        )

    """
    Falsifying example: execute(
        kwargs={'puzzle_input': 'L0\n'},
    )
    """
    # I guess this is because full_match is automatically set to false in hypothesis,
    # this means that '\n' could always be added, which is not what we want here.
    # def test_solve_icontract_hypothesis(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(solve)


_example_input = """F10
N3
F7
R90
F11"""

if __name__ == "__main__":
    unittest.main()

import unittest

import icontract_hypothesis

from aocdbc.day_12_rain_risk import (
    Orientation,
    ShipPosition,
    parse_input,
    update_position,
    solve,
)


class TestDay6(unittest.TestCase):
    def test_case(self) -> None:
        self.assertEqual(ShipPosition(17, -8, Orientation.SOUTH), solve(_example_input))

    def test_parse_input_file_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(parse_input)

    def test_update_position_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(update_position)

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

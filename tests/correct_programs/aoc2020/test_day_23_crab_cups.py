import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_23_crab_cups


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_23_crab_cups.initialize_cups,
            day_23_crab_cups.cup_circle_to_str,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestSolve100Steps(unittest.TestCase):
    def test_solve_100_steps(self) -> None:
        cup_labels = "389125467"
        self.assertEqual(
            "167384529",
            day_23_crab_cups.cup_circle_to_str(
                day_23_crab_cups.solve_100_steps(cup_labels=cup_labels)
            ),
        )


if __name__ == "__main__":
    unittest.main()

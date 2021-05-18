import unittest

import icontract_hypothesis

from correct_programs.ethz_eprog_2019.exercise_06 import problem_05


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [problem_05.compute_angles]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_cases(self) -> None:
        cases = [
            ((0, 0, 0), (0, 0, 0)),
            ((0, 0, 1), (0.008333333333333333, 0.1, 6.0)),
            ((2, 20, 0), (70.0, 120.0, 0.0)),
        ]

        for (hour, minute, second), expected_angles in cases:
            self.assertEqual(
                expected_angles,
                problem_05.compute_angles(hour, minute, second),
                f"{hour=}, {minute=}, {second=}",
            )


if __name__ == "__main__":
    unittest.main()

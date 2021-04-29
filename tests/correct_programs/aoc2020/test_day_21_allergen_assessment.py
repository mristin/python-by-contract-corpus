import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_21_allergen_assessment


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_21_allergen_assessment.parse_list_of_foods,
            day_21_allergen_assessment.is_equal_ingredient_list,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_solve(self) -> None:
        puzzle_input = textwrap.dedent(
            """\
            mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
            trh fvjkl sbzzf mxmxvkd (contains dairy)
            sqjhc fvjkl (contains soy)
            sqjhc mxmxvkd sbzzf (contains fish)"""
        )

        expected_output = {"kfcds", "nhms", "sbzzf", "trh"}

        self.assertEqual(
            expected_output, day_21_allergen_assessment.solve(puzzle_input)
        )


if __name__ == "__main__":
    unittest.main()

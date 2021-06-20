import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_21_allergen_assessment


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_21_allergen_assessment.serialize_entry,
            day_21_allergen_assessment.find_non_allergenic_ingredients,
            day_21_allergen_assessment.solve,
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
        text = textwrap.dedent(
            """\
            mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
            trh fvjkl sbzzf mxmxvkd (contains dairy)
            sqjhc fvjkl (contains soy)
            sqjhc mxmxvkd sbzzf (contains fish)"""
        )

        puzzle_input = [
            day_21_allergen_assessment.IngredientLine(line)
            for line in text.splitlines()
        ]

        expected_output = {"kfcds", "nhms", "sbzzf", "trh"}

        self.assertEqual(
            expected_output, day_21_allergen_assessment.solve(puzzle_input)
        )


if __name__ == "__main__":
    unittest.main()

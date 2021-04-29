import textwrap
import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_6_custom_customs


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [day_6_custom_customs.solve]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        example_data = textwrap.dedent(
            """\
            abc
    
            a
            b
            c
    
            ab
            ac
    
            a
            a
            a
            a
    
            b
            """
        )

        self.assertEqual(11, day_6_custom_customs.solve(example_data))


if __name__ == "__main__":
    unittest.main()

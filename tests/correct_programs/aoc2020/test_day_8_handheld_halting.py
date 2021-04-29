import textwrap
import unittest

import icontract_hypothesis

from correct_programs import common
from correct_programs.aoc2020 import day_8_handheld_halting


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_8_handheld_halting.parse,
            day_8_handheld_halting.execute_instructions,
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
        lines = common.Lines(
            textwrap.dedent(
                """\
                nop +0
                acc +1
                jmp +4
                acc +3
                jmp -3
                acc -99
                acc +1
                jmp -4
                acc +6
                """
            ).splitlines()
        )

        instructions = day_8_handheld_halting.parse(lines=lines)

        acc = day_8_handheld_halting.execute_instructions(instructions=instructions)

        self.assertEqual(5, acc)


if __name__ == "__main__":
    unittest.main()

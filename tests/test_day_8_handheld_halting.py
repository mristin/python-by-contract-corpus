import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_8_handheld_halting


class TestDay8(unittest.TestCase):
    def test_case(self) -> None:
        text = textwrap.dedent(
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
        )

        lines = text.splitlines()

        instructions = aocdbc.day_8_handheld_halting.parse(lines=lines)

        acc = aocdbc.day_8_handheld_halting.execute_instructions(
            instructions=instructions
        )

        self.assertEqual(5, acc)

    def test_parse_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_8_handheld_halting.parse
        )

    def test_execute_instructions_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_8_handheld_halting.execute_instructions
        )


if __name__ == "__main__":
    unittest.main()

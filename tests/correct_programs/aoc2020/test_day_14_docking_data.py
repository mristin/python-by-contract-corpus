import textwrap
import unittest

import icontract_hypothesis

from correct_programs import common
from correct_programs.aoc2020 import day_14_docking_data


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_14_docking_data.parse_mask,
            day_14_docking_data.parse_write,
            day_14_docking_data.execute,
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
                mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
                mem[8] = 11
                mem[7] = 101
                mem[8] = 0"""
            ).splitlines()
        )

        program = day_14_docking_data.parse_lines(lines=lines)

        memory = day_14_docking_data.execute(program=program)
        self.assertDictEqual({7: 101, 8: 64}, memory.slots)  # type: ignore

        self.assertEqual(165, day_14_docking_data.sum_memory(memory=memory))


if __name__ == "__main__":
    unittest.main()

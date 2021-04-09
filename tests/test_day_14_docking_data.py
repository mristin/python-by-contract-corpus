import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_14_docking_data


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_parse_mask(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_14_docking_data.parse_mask
        )

    def test_parse_write(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_14_docking_data.parse_write
        )

    def test_execute(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_14_docking_data.execute
        )


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        lines = textwrap.dedent(
            """\
            mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
            mem[8] = 11
            mem[7] = 101
            mem[8] = 0"""
        ).splitlines()

        program = aocdbc.day_14_docking_data.parse_lines(lines=lines)

        memory = aocdbc.day_14_docking_data.execute(program=program)
        self.assertDictEqual({7: 101, 8: 64}, memory.slots)  # type: ignore

        self.assertEqual(165, aocdbc.day_14_docking_data.sum_memory(memory=memory))


if __name__ == "__main__":
    unittest.main()

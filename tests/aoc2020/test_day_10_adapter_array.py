import textwrap
import unittest

import icontract_hypothesis

from python_by_contract_corpus import common
from python_by_contract_corpus.aoc2020 import day_10_adapter_array


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_10_adapter_array.histogram_differences,
            day_10_adapter_array.parse,
        ]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)  # type: ignore
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_example_short(self) -> None:
        lines = common.Lines(
            textwrap.dedent(
                """\
                16
                10
                15
                5
                1
                11
                7
                19
                6
                12
                4"""
            ).splitlines()
        )

        adapters = day_10_adapter_array.parse(lines)

        histo = day_10_adapter_array.histogram_differences(adapters)

        self.assertEqual(7, histo[1])
        self.assertEqual(5, histo[3])

        result = day_10_adapter_array.compute_result(histo)

        self.assertEqual(7 * 5, result)

    def test_example_long(self) -> None:
        lines = common.Lines(
            textwrap.dedent(
                """\
                28
                33
                18
                42
                31
                14
                46
                20
                48
                47
                24
                23
                49
                45
                19
                38
                39
                11
                1
                32
                25
                35
                8
                17
                7
                9
                4
                2
                34
                10
                3"""
            ).splitlines()
        )

        adapters = day_10_adapter_array.parse(lines)

        histo = day_10_adapter_array.histogram_differences(adapters)

        self.assertEqual(22, histo[1])
        self.assertEqual(10, histo[3])

        result = day_10_adapter_array.compute_result(histo)

        self.assertEqual(22 * 10, result)


if __name__ == "__main__":
    unittest.main()

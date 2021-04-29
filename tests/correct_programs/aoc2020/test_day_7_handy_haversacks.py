import textwrap
import unittest

import icontract_hypothesis

from correct_programs import common
from correct_programs.aoc2020 import day_7_handy_haversacks


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [day_7_handy_haversacks.containers]:
            try:
                icontract_hypothesis.test_with_inferred_strategy(func)
            except Exception as error:
                raise Exception(
                    f"Automatically testing {func} with icontract-hypothesis failed "
                    f"(please see the original error above)"
                ) from error


class TestManually(unittest.TestCase):
    def test_on_example(self) -> None:
        text = textwrap.dedent(
            """\
            light red bags contain 1 bright white bag, 2 muted yellow bags.
            dark orange bags contain 3 bright white bags, 4 muted yellow bags.
            bright white bags contain 1 shiny gold bag.
            muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
            shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
            dark olive bags contain 3 faded blue bags, 4 dotted black bags.
            vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
            faded blue bags contain no other bags.
            dotted black bags contain no other bags."""
        )

        lines = common.Lines(text.splitlines())

        self.assertEqual(4, day_7_handy_haversacks.count_containers(lines))

    def test_parse_bagexpr(self) -> None:
        self.assertEqual(
            (1, "bright white"),
            day_7_handy_haversacks.parse_bagexpr("1 bright white bag"),
        )

    def test_parse_rule(self) -> None:
        self.assertEqual(
            ("vibrant plum", {"faded blue": 5, "dotted black": 6}),
            day_7_handy_haversacks.parse_rule(
                "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags."
            ),
        )

    def test_parse_empty_rule(self) -> None:
        self.assertEqual(
            ("faded blue", {}),
            day_7_handy_haversacks.parse_rule("faded blue bags contain no other bags."),
        )


if __name__ == "__main__":
    unittest.main()

import unittest

import icontract_hypothesis

from correct_programs.aoc2020 import day_7_handy_haversacks


class TestDay7(unittest.TestCase):
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

    def test_containers_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            day_7_handy_haversacks.containers
        )


if __name__ == "__main__":
    unittest.main()

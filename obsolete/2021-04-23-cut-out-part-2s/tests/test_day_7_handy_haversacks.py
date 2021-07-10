import unittest

import icontract_hypothesis

from python_by_contract_corpus.aoc2020.day_7_handy_haversacks import (
    parse_bagexpr,
    parse_rule,
    containers
)


class TestDay4(unittest.TestCase):
    def test_parse_bagexpr(self) -> None:
        self.assertEqual(parse_bagexpr("1 bright white bag"), (1, "bright white"))

    def test_parse_rule(self) -> None:
        self.assertEqual(
            parse_rule(
                "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags."
            ),
            ("vibrant plum", {"faded blue": 5, "dotted black": 6}),
        )

    def test_parse_empty_rule(self) -> None:
        self.assertEqual(
            parse_rule("faded blue bags contain no other bags."), ("faded blue", {})
        )

    def test_containers_with_icontract_hypothesis(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(containers)

    # NOTE: this test causes hypothesis to fail with a
    # "too_slow" health check - the preconditions are too challenging.
    # def test_count_bags_with_icontract_hypothesis(self) -> None:
    #     icontract_hypothesis.test_with_inferred_strategy(count_bags)


if __name__ == "__main__":
    unittest.main()

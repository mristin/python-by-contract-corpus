import textwrap
import unittest
from typing import List, Callable, Any

import icontract_hypothesis

from python_by_contract_corpus import common
from python_by_contract_corpus.aoc2020 import day_16_ticket_translation


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_functions(self) -> None:
        for func in [
            day_16_ticket_translation.applies,
            day_16_ticket_translation.invalid_fields,
            day_16_ticket_translation.list_all_invalid_values,
            day_16_ticket_translation.compute_error_rate,
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
        rule_lines = common.Lines(
            textwrap.dedent(
                """\
                class: 1-3 or 5-7
                row: 6-11 or 33-44
                seat: 13-40 or 45-50"""
            ).splitlines()
        )

        rule_parsings = day_16_ticket_translation.parse_rules(lines=rule_lines)

        # fmt: off
        rules = [
            day_16_ticket_translation.Rule(
                identifier=parsing.identifier, ranges=parsing.ranges)
            for parsing in rule_parsings
        ]
        # fmt: on

        nearby_ticket_lines = textwrap.dedent(
            """\
            7,3,47
            40,4,50
            55,2,20
            38,6,12"""
        ).splitlines()

        nearby_tickets = day_16_ticket_translation.parse_nearby_tickets(
            lines=nearby_ticket_lines
        )

        invalid_values = day_16_ticket_translation.list_all_invalid_values(
            rules=rules, tickets=nearby_tickets
        )

        self.assertListEqual([4, 55, 12], invalid_values)

        error_rate = day_16_ticket_translation.compute_error_rate(
            invalid_values=invalid_values
        )
        self.assertEqual(71, error_rate)


if __name__ == "__main__":
    unittest.main()

import re
import textwrap
import unittest
from typing import Dict, List

from python_by_contract_corpus import common
from python_by_contract_corpus.correct.aoc2020 import day_19_monster_messages


class TestRuleRe(unittest.TestCase):
    def test_literal(self) -> None:
        line = '4: "a"'
        self.assertIsNotNone(day_19_monster_messages.RULE_RE.match(line), line)

    def test_sequence(self) -> None:
        line = "0: 4 1 5"
        self.assertIsNotNone(day_19_monster_messages.RULE_RE.match(line), line)

    def test_or(self) -> None:
        line = "1: 2 3 | 3 2"
        self.assertIsNotNone(day_19_monster_messages.RULE_RE.match(line), line)


class TestRuleCompositeRe(unittest.TestCase):
    def test_sequence(self) -> None:
        body = "4 1 5"
        self.assertIsNotNone(
            day_19_monster_messages.RULE_COMPOSITE_RE.match(body), body
        )

    def test_or(self) -> None:
        body = "2 3 | 3 2"
        self.assertIsNotNone(
            day_19_monster_messages.RULE_COMPOSITE_RE.match(body), body
        )


class TestManually(unittest.TestCase):
    def test_repr(self) -> None:
        rule_lines = common.Lines(
            textwrap.dedent(
                '''\
                0: 4 1 5
                1: 2 3 | 3 2
                2: 4 4 | 5 5
                3: 4 5 | 5 4
                4: "a"
                5: "b"'''
            ).splitlines()
        )

        rules_to_repr = dict()  # type: Dict[int, str]

        rule_trees = day_19_monster_messages.parse_rules(lines=rule_lines)

        for identifier, rule_tree in rule_trees.items():
            rules_to_repr[identifier] = day_19_monster_messages.repr_rule_tree(
                rule_tree=rule_tree
            )

        # fmt: off
        self.assertDictEqual(
            {
                0: 'Seq(Ref(4) Ref(1) Ref(5))',
                1: 'Or(Seq(Ref(2) Ref(3)) | Seq(Ref(3) Ref(2)))',
                2: 'Or(Seq(Ref(4) Ref(4)) | Seq(Ref(5) Ref(5)))',
                3: 'Or(Seq(Ref(4) Ref(5)) | Seq(Ref(5) Ref(4)))',
                4: 'Lit("a")', 5: 'Lit("b")'
            },
            rules_to_repr)
        # fmt: on

    def test_iterate(self) -> None:
        rule_lines = common.Lines(
            textwrap.dedent(
                '''\
                0: 4 1 5
                1: 2 3 | 3 2
                2: 4 4 | 5 5
                3: 4 5 | 5 4
                4: "a"
                5: "b"'''
            ).splitlines()
        )

        rule_trees = day_19_monster_messages.parse_rules(lines=rule_lines)

        identifier_to_node_types = dict()  # type: Dict[int, List[str]]

        for identifier, rule_tree in rule_trees.items():
            node_types = [
                re.sub(r"^Node", "", type(node).__name__)
                .replace("Sequence", "Seq")
                .replace("Reference", "Ref")
                .replace("Literal", "Lit")
                for node in day_19_monster_messages.iterate(rule_tree=rule_tree)
            ]

            identifier_to_node_types[identifier] = node_types

        # fmt: off
        self.assertDictEqual(
            {0: ['Seq', 'Ref', 'Ref', 'Ref'],
             1: ['Or', 'Seq', 'Ref', 'Ref', 'Seq', 'Ref', 'Ref'],
             2: ['Or', 'Seq', 'Ref', 'Ref', 'Seq', 'Ref', 'Ref'],
             3: ['Or', 'Seq', 'Ref', 'Ref', 'Seq', 'Ref', 'Ref'], 
             4: ['Lit'],
             5: ['Lit']},
            identifier_to_node_types)
        # fmt: on

    def test_case(self) -> None:
        rule_lines = common.Lines(
            textwrap.dedent(
                '''\
                0: 4 1 5
                1: 2 3 | 3 2
                2: 4 4 | 5 5
                3: 4 5 | 5 4
                4: "a"
                5: "b"'''
            ).splitlines()
        )

        rule_trees = day_19_monster_messages.parse_rules(lines=rule_lines)

        rule_0 = day_19_monster_messages.interpret_rule_0(rule_trees=rule_trees)

        for should_match in ["ababbb", "abbbab"]:
            remaining_suffix = rule_0.match(text=should_match)
            self.assertEqual("", remaining_suffix)

        for should_remain in ["bababa", "aaabbb", "aaaabbb"]:
            remaining_suffix = rule_0.match(text=should_remain)
            self.assertNotEqual("", remaining_suffix)

        for should_not_match in ["xyz", "xaaabbb"]:
            remaining_suffix = rule_0.match(text=should_not_match)
            self.assertIsNone(remaining_suffix)

        messages = textwrap.dedent(
            """\
            ababbb
            bababa
            abbbab
            aaabbb
            aaaabbb"""
        ).splitlines()

        count = day_19_monster_messages.count_matching_messages(
            rule_0=rule_0, messages=messages
        )

        self.assertEqual(2, count)


if __name__ == "__main__":
    unittest.main()

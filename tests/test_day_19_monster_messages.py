import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_19_monster_messages


class TestRuleRe(unittest.TestCase):
    def test_literal(self) -> None:
        line = '4: "a"'
        self.assertIsNotNone(aocdbc.day_19_monster_messages.RULE_RE.match(line), line)

    def test_sequence(self) -> None:
        line = "0: 4 1 5"
        self.assertIsNotNone(aocdbc.day_19_monster_messages.RULE_RE.match(line), line)

    def test_or(self) -> None:
        line = "1: 2 3 | 3 2"
        self.assertIsNotNone(aocdbc.day_19_monster_messages.RULE_RE.match(line), line)


class TestRuleCompositeRe(unittest.TestCase):
    def test_sequence(self) -> None:
        body = "4 1 5"
        self.assertIsNotNone(
            aocdbc.day_19_monster_messages.RULE_COMPOSITE_RE.match(body), body
        )

    def test_or(self) -> None:
        body = "2 3 | 3 2"
        self.assertIsNotNone(
            aocdbc.day_19_monster_messages.RULE_COMPOSITE_RE.match(body), body
        )


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        rule_lines = textwrap.dedent(
            '''\
            0: 4 1 5
            1: 2 3 | 3 2
            2: 4 4 | 5 5
            3: 4 5 | 5 4
            4: "a"
            5: "b"'''
        ).splitlines()

        rule_trees = aocdbc.day_19_monster_messages.parse_rules(lines=rule_lines)

        rule_0 = aocdbc.day_19_monster_messages.interpret_rule_0(rule_trees=rule_trees)

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

        count = aocdbc.day_19_monster_messages.count_matching_messages(
            rule_0=rule_0, messages=messages
        )

        self.assertEqual(2, count)


if __name__ == "__main__":
    unittest.main()

import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_22_crab_combat


# TODO (mristin, 2021-04-05): run pylint on both the implementation and the tests to
#   remove the unused imports.


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_compute_score(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_22_crab_combat.compute_score
        )


class TestManually(unittest.TestCase):
    def test_case(self) -> None:
        lines = textwrap.dedent(
            """\
            Player 1:
            9
            2
            6
            3
            1
            
            Player 2:
            5
            8
            4
            7
            10"""
        ).splitlines()

        cards1, cards2 = aocdbc.day_22_crab_combat.parse_lines(lines=lines)

        deck1 = aocdbc.day_22_crab_combat.Deck(cards=cards1)
        deck2 = aocdbc.day_22_crab_combat.Deck(cards=cards2)

        split = aocdbc.day_22_crab_combat.Split(deck1=deck1, deck2=deck2)

        final_split = aocdbc.day_22_crab_combat.play(split=split)

        score1 = aocdbc.day_22_crab_combat.compute_score(final_split.deck1)
        score2 = aocdbc.day_22_crab_combat.compute_score(final_split.deck2)

        self.assertEqual(306, max(score1, score2))


if __name__ == "__main__":
    unittest.main()

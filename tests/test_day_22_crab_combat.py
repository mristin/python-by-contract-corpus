import textwrap
import unittest

import icontract_hypothesis

import aocdbc.day_22_crab_combat

# TODO (mristin, 2021-04-05): run pylint on both the implementation and the tests to
#   remove the unused imports.


class TestWithIcontractHypothesis(unittest.TestCase):
    def test_play_a_round(self) -> None:
        icontract_hypothesis.test_with_inferred_strategy(
            aocdbc.day_22_crab_combat.play_a_round
        )

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

        deck1, deck2 = aocdbc.day_22_crab_combat.parse_lines(lines=lines)

        final_deck1, final_deck2 = aocdbc.day_22_crab_combat.play(
            deck1=deck1, deck2=deck2
        )

        score1 = aocdbc.day_22_crab_combat.compute_score(final_deck1)
        score2 = aocdbc.day_22_crab_combat.compute_score(final_deck2)

        self.assertEqual(306, max(score1, score2))


if __name__ == "__main__":
    unittest.main()

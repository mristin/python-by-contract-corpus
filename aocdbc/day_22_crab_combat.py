import collections
import re
from typing import Tuple, List, Optional, Set, MutableMapping

from icontract import require, ensure


# crosshair: on

# fmt: off
@require(
    lambda deck1, deck2: not set(deck1).intersection(deck2),
    "No overlapping cards"
)
@require(lambda deck1: len(deck1) > 0, "Not game over for player 1")
@require(lambda deck2: len(deck2) > 0, "Not game over for player 2")
@require(lambda deck1: len(set(deck1)) == len(deck1), "Unique cards")
@require(lambda deck2: len(set(deck2)) == len(deck2), "Unique cards")
@ensure(
    lambda deck1, deck2, result:
    set(deck1).union(deck2) == set(result[0]).union(result[1]),
    "No new cards"
)
@ensure(
    lambda deck1, result:
    deck1[1:] == result[0][0:len(deck1) - 1],
    "Only the prefix and the suffix of the deck 1 change"
)
@ensure(
    lambda deck2, result:
    deck2[1:] == result[1][0:len(deck2) - 1],
    "Only the prefix and the suffix of the deck 2 change"
)
@ensure(
    lambda deck1, deck2, result:
    (len(deck1) == len(result[0]) + 1 and len(deck2) == len(result[1]) - 1)
    or (len(deck1) == len(result[0]) - 1 and len(deck2) == len(result[1]) + 1),
    "Either lost or won two cards"
)
# fmt: on
def play_a_round(deck1: List[int], deck2: List[int]) -> Tuple[List[int], List[int]]:
    if len(deck1) == 0 or len(deck2) == 0:
        return deck1, deck2

    card1 = deck1[0]
    card2 = deck2[0]

    if card1 > card2:
        new_deck1 = deck1[1:] + [card1, card2]
        new_deck2 = deck2[1:]
    else:
        new_deck1 = deck1[1:]
        new_deck2 = deck2[1:] + [card2, card1]

    result = (new_deck1, new_deck2)
    return result


# fmt: off
@require(
    lambda lines:
    all(
        re.match(r'^(Player 1:|Player 2:|0|[1-9][0-9]*|)\Z', line)
        for line in lines
    )
)
# fmt: on
@require(lambda lines: 'Player 2:' in lines[1:])
@require(lambda lines: lines[0] == 'Player 1:')
@require(lambda lines: len(lines) > 3)
@ensure(lambda result: all(card >= 0 for card in result[0]))
@ensure(lambda result: all(card >= 0 for card in result[1]))
def parse_lines(lines: List[str]) -> Tuple[List[int], List[int]]:
    deck1 = []  # type: List[int]
    deck2 = []  # type: List[int]

    target_deck = deck1

    for line in lines[1:]:
        if line == '':
            pass
        elif line == 'Player 2:':
            target_deck = deck2
        else:
            target_deck.append(int(line))

    return deck1, deck2


@require(lambda deck: all(card >= 0 for card in deck))
@ensure(lambda result: result >= 0)
def compute_score(deck: List[int]) -> int:
    score = 0
    for i, card in enumerate(deck):
        score += (len(deck) - i) * card

    return score


# (mristin, 2021-04-05): Do *not* introduce classes. It is easier to copy/paste
# the contracts here. The classes resulted in really hard-to-follow contracts and
# implementation.
# fmt: off
@require(lambda deck1: all(card >= 0 for card in deck1))
@require(lambda deck2: all(card >= 0 for card in deck2))
@require(
    lambda deck1, deck2: not set(deck1).intersection(deck2),
    "No overlapping cards"
)
@require(lambda deck1: len(deck1) > 0, "Not game over for player 1")
@require(lambda deck2: len(deck2) > 0, "Not game over for player 2")
@require(lambda deck1: len(set(deck1)) == len(deck1), "Unique cards")
@require(lambda deck2: len(set(deck2)) == len(deck2), "Unique cards")
@ensure(
    lambda deck1, deck2, result:
    (len(deck1) + len(deck2) == len(result[0]) and len(result[1] == 0))
    or (len(result[0]) == 0 and len(deck1) + len(deck2) == len(result[1]))
)
@ensure(
    lambda deck1, deck2, result:
    set(deck1).union(deck2) == set(result[0]).union(result[1])
)
# fmt: on
def play(deck1: List[int], deck2: List[int]) -> Tuple[List[int], List[int]]:
    while True:
        deck1, deck2 = play_a_round(deck1=deck1, deck2=deck2)

        if len(deck1) == 0 or len(deck2) == 0:
            break

    return deck1, deck2

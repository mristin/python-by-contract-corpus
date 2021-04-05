import collections
import re
from typing import Tuple, List, Optional, Set, MutableMapping

from icontract import require, ensure


# crosshair: on

# fmt: off
@require(
    lambda deck1, deck2: len(set(deck1).intersection(deck2)) == 0,
    "No overlapping cards"
)
@require(lambda deck1: len(deck1) > 0, "Not game over for player 1")
@require(lambda deck2: len(deck2) > 0, "Not game over for player 2")
@ensure(
    lambda deck1, deck2, result:
    set(deck1).union(deck2) == set(result[0]).union(result[1]),
    "No new cards"
)
# ERROR: this post-condition failed on 'deck1': [0, 0], 'deck2': [1]
# It should be result[0][0:len(deck1)-1] and result[1][0:len(deck2) - 1]!
# There was also a missing pre-condition that the decks are unique.
@ensure(
    lambda deck1, deck2, result:
    deck1[1:] == result[0][1:len(deck1) - 1]
    and deck2[1:] == result[1][1:len(deck2) - 1],
    "Only the prefix and the suffix of the decks change"
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
        new_deck2 = deck2[1:] + [card1, card2]

    return new_deck1, new_deck2


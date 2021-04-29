import re
from typing import Tuple, List, Sequence, overload, Union, Any, Final, Iterator

from icontract import require, ensure, DBC


# crosshair: on


class Deck(DBC):
    """Represent a deck of cards.

    Please make sure that you transfer the "ownership" immediately to ``Deck``
    and don't modify the original list of strings any more:

       .. code-block: python

           ##
           # OK
           ##

           deck = Deck([1, 2, 3])

           ##
           # Not OK
           ##

           cards = [1, 2, 3]
           deck = Deck(cards)
           # ... do something assuming ``deck`` is immutable ...

           cards[0] = 2
           # ERROR! cards[0] now breaks the invariant!

    """

    cards: Final[Sequence[int]]

    @require(lambda cards: all(card >= 0 for card in cards))
    @require(lambda cards: len(set(cards)) == len(cards), "Unique cards")
    def __init__(self, cards: Sequence[int]) -> None:
        self.cards = cards

    @overload
    def __getitem__(self, index: int) -> int:
        pass

    @overload
    def __getitem__(self, index: slice) -> "Deck":
        pass

    def __getitem__(self, index: Union[int, slice]) -> Union[int, "Deck"]:
        if isinstance(index, slice):
            return Deck(cards=self.cards[index])
        else:
            return self.cards[index]

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> Iterator[int]:
        return self.cards.__iter__()

    # fmt: off
    @require(
        lambda self, other:
        (
                sum := list(self.cards) + other.cards,
                len(set(sum)) == len(sum)
        ),
        "Unique cards after the addition")
    # fmt: on
    def __add__(self, other: "Deck") -> "Deck":
        sum = list(self.cards)
        sum.extend(other.cards)
        return Deck(cards=sum)

    def __repr__(self) -> str:
        return repr(self.cards)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Deck):
            return self.cards.__eq__(other.cards)
        elif isinstance(other, list):
            return self.cards.__eq__(other)
        else:
            return object.__eq__(self, other)


class Split(DBC):
    deck1: Final[Deck]
    deck2: Final[Deck]

    @require(
        lambda deck1, deck2: not set(deck1).intersection(deck2), "No overlapping cards"
    )
    def __init__(self, deck1: Deck, deck2: Deck) -> None:
        self.deck1 = deck1
        self.deck2 = deck2


# fmt: off
@require(lambda split: len(split.deck1) > 0, "Not game over for player 1")
@require(lambda split: len(split.deck2) > 0, "Not game over for player 2")
@ensure(
    lambda split, result:
    set(split.deck1).union(split.deck2) == set(result.deck1).union(result.deck2),
    "No new cards"
)
@ensure(
    lambda split, result:
    split.deck1[1:] == result.deck1[0:len(split.deck1) - 1],
    "Only the prefix and the suffix of the deck 1 change"
)
@ensure(
    lambda split, result:
    split.deck2[1:] == result.deck2[0:len(split.deck2) - 1],
    "Only the prefix and the suffix of the deck 2 change"
)
@ensure(
    lambda split, result:
    (
            len(split.deck1) == len(result.deck1) + 1
            and len(split.deck2) == len(result.deck2) - 1)
    or (
            len(split.deck1) == len(result.deck1) - 1
            and len(split.deck2) == len(result.deck2) + 1),
    "Either lost or won two cards"
)
# fmt: on
def play_a_round(split: Split) -> Split:
    card1 = split.deck1[0]
    card2 = split.deck2[0]

    if card1 > card2:
        new_deck1 = split.deck1[1:] + Deck([card1, card2])
        new_deck2 = split.deck2[1:]
    else:
        new_deck1 = split.deck1[1:]
        new_deck2 = split.deck2[1:] + Deck([card2, card1])

    result = Split(deck1=new_deck1, deck2=new_deck2)

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


@ensure(lambda result: result >= 0)
def compute_score(deck: Deck) -> int:
    score = 0
    for i, card in enumerate(deck):
        score += (len(deck) - i) * card

    return score


# fmt: off
@require(lambda split: len(split.deck1) > 0, "Not game over for player 1")
@require(lambda split: len(split.deck2) > 0, "Not game over for player 2")
@ensure(
    lambda split, result:
    (
            len(split.deck1) + len(split.deck2) == len(result.deck1)
            and len(result.deck2) == 0
    )
    or (
            len(result.deck1) == 0
            and len(split.deck1) + len(split.deck2) == len(result.deck2)
    )
)
@ensure(
    lambda split, result:
    set(split.deck1).union(split.deck2) == set(result.deck1).union(result.deck2)
)
# fmt: on
def play(split: Split) -> Split:
    while True:
        split = play_a_round(split=split)

        if len(split.deck1) == 0 or len(split.deck2) == 0:
            break

    return split

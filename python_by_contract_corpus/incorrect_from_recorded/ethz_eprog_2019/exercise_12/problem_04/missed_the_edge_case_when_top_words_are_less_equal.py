"""
Analyze the words of a text.

We consider not only the content of a word as string, but also its position in the text.
A word can appear in multiple locations in the text. (We consider inflections as
different words: "go" and "goes" are considered two different words.)

We define an order of the words. A word ``x`` is smaller than a word ``y`` if the
difference between the first and last occurrence of ``x`` is smaller than the
corresponding difference for ``y``.

Provide a function to extract words from a text.

Provide a function ``top`` to return the largest ``n`` words based on the aforementioned
order.

"""
import re
from typing import List, Dict, cast

from icontract import require, DBC, ensure

WORD_RE = re.compile(r"^[a-z]+(-[a-z])*$")  #: Express a normalized word of a text.


class Token(DBC, str):
    """Represent a word as a token of the text."""

    @require(lambda text: WORD_RE.match(text))
    def __new__(cls, text: str) -> "Token":
        """Enforce the properties on the ``text`` of the word."""
        return cast(Token, text)


class WordOccurrence(DBC):
    """Represent a word occurence in the text."""

    # fmt: off
    @require(
        lambda first, last:
        first <= last
    )
    @require(lambda first: first >= 0)
    @require(lambda last: last >= 0)
    # fmt: on
    def __init__(self, first: int, last: int, text: Token) -> None:
        """Initialize with the given values."""
        self.first = first  #: Index of the first occurrence
        self.last = last  #: Index of the last occurrence
        self.text = text  #: Text of the word

    def __lt__(self, other: "WordOccurrence") -> bool:
        """
        Compare against ``other`` based on the :py:attr:`.first` and :py:attr:`.last`.
        """
        return self.last - self.first < other.last - other.first

    # ERROR (mristin, 2021-06-09):
    # I forgot to specify how ``<=`` works for the top words. This broke down for the
    # program input such as:
    # Falsifying example: execute(
    #      kwargs={'limit': 2, 'words': [Word(1, 1, 'a'), Word(1, 1, 'a')]},
    # )
    #
    # I should have written a function like the following one:
    # def __le__(self, other: "WordOccurrence") -> bool:
    #     """
    #     Compare against ``other`` based on the :py:attr:`.first` and :py:attr:`.last`.
    #     """
    #     return self.last - self.first <= other.last - other.first

    def __repr__(self) -> str:
        """Represent the word occurrence as string for easier debugging."""
        return (
            f"{self.__class__.__name__}("
            f"{self.first!r}, {self.last!r}, {self.text!r}"
            f")"
        )


# fmt: off
@ensure(
    lambda result:
    (
            word_texts := [word_occurrence.text for word_occurrence in result],
            len(word_texts) == len(set(word_texts))
    )[1],
    "No duplicate word occurrences"
)
@ensure(
    lambda tokens, result:
    all(
        tokens[word_occurrence.first] == word_occurrence.text
        and tokens[word_occurrence.last] == word_occurrence.text
        for word_occurrence in result
    )
)
@ensure(lambda tokens, result: len(result) <= len(tokens))
@ensure(
    lambda tokens, result:
    not (len(tokens) > 0) or len(result) > 0
)
# fmt: on
def tokens_to_words(tokens: List[Token]) -> List[WordOccurrence]:
    first_occurrences = dict()  # type: Dict[Token, int]
    last_occurrences = dict()  # type: Dict[Token, int]

    for i, token in enumerate(tokens):
        if token not in first_occurrences:
            assert token not in last_occurrences

            first_occurrences[token] = i
            last_occurrences[token] = i
        else:
            last_occurrences[token] = i

    assert len(first_occurrences) == len(last_occurrences)
    assert set(first_occurrences.keys()) == set(last_occurrences.keys())

    word_occurrences = []  # type: List[WordOccurrence]
    for token, first_occurrence in first_occurrences.items():
        word_occurrences.append(
            WordOccurrence(
                first=first_occurrence,
                last=last_occurrences[token],
                text=token,
            )
        )

    return word_occurrences


TOKEN_RE = re.compile("[a-zA-Z]+(-[a-zA-Z])*")  #: Express a token of a text.


# fmt: off
@ensure(
    lambda text, result:
    sum(len(token) for token in result) <= len(text)
)
# fmt: on
def tokenize(text: str) -> List[Token]:
    """Tokenize the text into normalized word tokens ignoring the punctuation."""
    result = []  # type: List[Token]
    for match in TOKEN_RE.finditer(text):
        result.append(Token(match.group().lower()))

    return result


# fmt: off
@require(lambda limit: limit > 0)
@ensure(
    lambda word_occurrences, result:
    (
            word_set := set(word_occurrences),
            all(
                word_occurrence in word_set  # pylint: disable=used-before-assignment
                for word_occurrence in result
            )
    )[1]
)
@ensure(
    lambda result:
    all(
        result[i] >= result[i + 1]
        for i in range(len(result) - 1)
    )
)
@ensure(
    lambda word_occurrences, limit, result:
    len(result) == min(len(word_occurrences), limit)
)
# fmt: on
def find_top(
    word_occurrences: List[WordOccurrence], limit: int
) -> List[WordOccurrence]:
    """Find the ``limit`` top occurrences in ``word_occurrences``."""
    sorted_words = sorted(word_occurrences, reverse=True)
    return sorted_words[:limit]

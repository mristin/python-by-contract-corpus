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

WORD_RE = re.compile(r"^[a-z]+(-[a-z])*$")


class Token(DBC, str):
    @require(lambda text: WORD_RE.match(text))
    def __new__(cls, text: str) -> "Token":
        return cast(Token, text)


class Word(DBC):
    # fmt: off
    @require(
        lambda first_occurrence, last_occurrence:
        first_occurrence <= last_occurrence
    )
    @require(lambda first_occurrence: first_occurrence >= 0)
    @require(lambda last_occurrence: last_occurrence >= 0)
    # fmt: on
    def __init__(
        self, first_occurrence: int, last_occurrence: int, text: Token
    ) -> None:
        self.first_occurrence = first_occurrence
        self.last_occurrence = last_occurrence
        self.text = text

    def __lt__(self, other: "Word") -> bool:
        return (
            self.last_occurrence - self.first_occurrence
            < other.last_occurrence - other.first_occurrence
        )

    def __le__(self, other: "Word") -> bool:
        return (
            self.last_occurrence - self.first_occurrence
            <= other.last_occurrence - other.first_occurrence
        )

    def __repr__(self) -> str:
        return (
            f"Word("
            f"{self.first_occurrence!r}, {self.last_occurrence!r}, {self.text!r}"
            f")"
        )


# fmt: off
@ensure(
    lambda result:
    (
            word_texts := [word.text for word in result],
            len(word_texts) == len(set(word_texts))
    )[1],
    "No duplicates in words"
)
@ensure(
    lambda tokens, result:
    all(
        tokens[word.first_occurrence] == word.text
        and tokens[word.last_occurrence] == word.text
        for word in result
    )
)
@ensure(lambda tokens, result: len(result) <= len(tokens))
@ensure(
    lambda tokens, result:
    not (len(tokens) > 0) or len(result) > 0
)
# fmt: on
def tokens_to_words(tokens: List[Token]) -> List[Word]:
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

    words = []  # type: List[Word]
    for token, first_occurrence in first_occurrences.items():
        words.append(
            Word(
                first_occurrence=first_occurrence,
                last_occurrence=last_occurrences[token],
                text=token,
            )
        )

    return words


TOKEN_RE = re.compile("[a-zA-Z]+(-[a-zA-Z])*")


# fmt: off
@ensure(
    lambda text, result:
    sum(len(token) for token in result) <= len(text)
)
# fmt: on
def tokenize(text: str) -> List[Token]:
    result = []  # type: List[Token]
    for match in TOKEN_RE.finditer(text):
        result.append(Token(match.group().lower()))

    return result


# fmt: off
@require(lambda limit: limit > 0)
@ensure(
    lambda words, result:
    (
            word_set := set(words),
            all(
                word in word_set  # pylint: disable=used-before-assignment
                for word in result
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
@ensure(lambda words, limit, result: len(result) == min(len(words), limit))
# fmt: on
def find_top(words: List[Word], limit: int) -> List[Word]:
    sorted_words = sorted(words, reverse=True)
    return sorted_words[:limit]

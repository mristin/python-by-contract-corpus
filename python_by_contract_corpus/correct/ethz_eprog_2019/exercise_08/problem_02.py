"""
List all the sub-sequences of length ``n`` contained in a string ``s``.

You obtain a sub-sequence by "erasing" the characters in ``s``.

For example, here are all the sub-sequences with ``n = 2`` of ``"apple"``:

.. code-block::

    "ap"
    "al"
    "ae"
    "pp"
    "pl"
    "pe"
    "le"

"""
import itertools
import math
from typing import List, Set

from icontract import require, ensure


@require(lambda subtext, text: len(subtext) <= len(text))
def is_subsequence(subtext: str, text: str) -> bool:
    """
    Check if the ``subtext`` is a subsequence of ``text``.

    >>> is_subsequence('pe', 'apple')
    True

    >>> is_subsequence('ep', 'apple')
    False
    """
    if len(subtext) == 0:
        return True

    i = 0

    for symbol in text:
        if symbol == subtext[i]:
            i += 1

        if i == len(subtext):
            break

    return i == len(subtext)


@require(lambda text, length: 0 <= length <= len(text))
@ensure(lambda length, result: all(len(item) == length for item in result))
@ensure(lambda text, result: all(is_subsequence(item, text) for item in result))
@ensure(
    lambda text, length, result: not (
        length > 0 and len(text) > 0 and len(set(text)) == len(text)
    )
    or len(result) == math.comb(len(text), length),
    "If all the characters are unique, the number of substrings equals "
    "the count of binary sequences ``len(text)`` long with ``length`` bits set",
)
def list_subsequences(text: str, length: int) -> Set[str]:
    """
    List all subsequences of size ``length`` in ``text``.

    >>> sorted(list_subsequences("apple", 2))
    ['ae', 'al', 'ap', 'le', 'pe', 'pl', 'pp']
    """
    if length == 0:
        return set()

    if length == len(text):
        return {text}

    result = set()  # type: Set[str]
    for substring_indices in itertools.combinations(range(len(text)), length):
        substring = "".join(text[index] for index in substring_indices)
        result.add(substring)

    return result

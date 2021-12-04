"""
Consider two strings, ``s`` and ``t`` and a non-negative integer ``k``.

Check if the characters in ``t`` occur in ``s`` in an arbitrary order as a subsequence.
The distance between two matching characters from ``t`` in ``s`` must not be larger
than ``k``.

The distance between two characters is given as the number of characters in-between.
For example, the distance between the characters "a" and "b" in "a12345b" is 5.

Here are a couple of examples:

* ``s = "abbbc", t = "cab", k = 1``. The result is ``True``.
* ``s = "abbbbc", t = "cab", k = 1``. The result if ``False``. The distance between
  either "a" and "b" or "b" and "c" is larger than 1.
* ``s = "abc"``

"""

from typing import Counter, Set

from icontract import require, ensure


@require(lambda dist: dist >= 0)
@ensure(lambda src, chars, result: result is False if len(chars) > len(src) else True)
@ensure(
    lambda src, chars, result: (result is True)
    if (sorted(chars) in sorted(src))
    else True
)
@ensure(lambda src, chars, result: (result is True) if (chars in src) else True)
def matches(src: str, chars: str, dist: int) -> bool:
    return stretch(src, Counter(chars), len(src) - len(chars), dist)


def stretch(src: str, chars: Counter[str], initialdist: int, dist: int) -> bool:
    if sum(chars.values()) == 0:
        return True
    prefix = src[: initialdist + 1]
    if all(chars[ch] == 0 for ch in prefix):
        return False
    for idx, ch in enumerate(prefix):
        if chars[ch] <= 0:
            continue
        subch = chars.copy()
        subch[ch] -= 1
        if stretch(src[idx + 1 :], subch, dist, dist):
            return True
    return False

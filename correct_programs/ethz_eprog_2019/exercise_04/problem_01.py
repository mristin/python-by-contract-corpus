"""
Compute the Sieve of Eratosthenes.

List all the prime numbers given a ``limit`` which are greater than 1 and smaller-equal
``limit``.
"""
import bisect
from typing import List

from icontract import require, ensure


@ensure(lambda a, result: result == -1 or 0 <= result < len(a))
def find(a: List[int], x: int) -> int:
    """
    Locate the leftmost value in ``a`` exactly equal to ``x``.

    Return -1 if the element was not found in ``a``.
    """
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1


# fmt: off
@require(lambda limit: limit > 1)
@ensure(
    lambda limit, result:
    all(
        1 < number <= limit
        for number in result
    )
)
@ensure(
    lambda result:
    len(result) == len(set(result)),
    "Unique results"
)
# fmt: on
def sieve(limit: int) -> List[int]:
    """
    Apply the Sieve of Eratosthenes on the numbers up to ``limit``.

    :return: list of prime numbers till ``limit``
    """
    candidates = list(range(2, limit + 1))

    result = []  # type: List[int]

    while candidates:
        prime = candidates.pop(0)
        result.append(prime)

        for i in range(2, limit):
            index = find(candidates, prime * i)
            if index != -1:
                candidates.pop(index)

            if prime * i > limit:
                break

    return result

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


def naive_is_prime(number: int) -> bool:
    result = True
    for another in range(number - 1, 1, -1):
        if number % another == 0:
            result = False
            break

    return result

# ERROR:
# icontract.errors.ViolationError:
# all(problem_01.naive_is_prime(number) for number in result):
# all(problem_01.naive_is_prime(number) for number in result) was False
# result was [2, 3, 5, 7, 9]
#
# Falsifying example: execute(
#     kwargs={'limit': 9},
# )
@require(lambda limit: limit > 1)
@ensure(lambda result: all(number > 1 for number in result))
def sieve(limit: int) -> List[int]:
    candidates = list(range(2, limit + 1))

    result = []  # type: List[int]

    while candidates:
        prime = candidates.pop(0)
        result.append(prime)

        for i in range(2, limit):
            index = find(candidates, prime * i)
            if index == -1:
                break

            candidates.pop(index)

    return result

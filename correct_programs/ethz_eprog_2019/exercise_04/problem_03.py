"""
Find two summands ``s1`` and ``s2`` for a given non-negative number ``n``.

The following properties should hold:
* ``s1 ≥ s2``
* ``s1 + s2 == n``
* The digit 7 does not appear neither in ``s1`` nor in ``s2``.

Though the original problem did not state it, we enforce ``s1 > 0`` and ``s2 > 0``.

"""
from typing import Tuple, List, Mapping, Reversible

from icontract import require, ensure


@require(lambda n: n > 0)
@ensure(lambda n, result: "".join(str(digit) for digit in result) == str(n))
@ensure(lambda result: result[0] != 0)
@ensure(lambda result: all(0 <= digit <= 9 for digit in result))
@ensure(lambda n, result: digits_to_number(result) == n)  # type: ignore
def number_to_digits(n: int) -> List[int]:
    """Disassemble the integer ``n`` into individual digits."""
    digits = []  # type: List[int]

    factor = 10
    remainder = n
    while remainder > 0:
        digits.append(remainder % factor)
        remainder = remainder // factor

    digits = list(reversed(digits))

    return digits


@require(lambda digits: len(digits) > 0)
@require(lambda digits: all(0 <= digit <= 9 for digit in digits))
def digits_to_number(digits: Reversible[int]) -> int:
    """Assemble the integer from the given ``digits``."""
    number = 0
    factor = 1
    for digit in reversed(digits):
        number += factor * digit
        factor *= 10

    return number


# Summands for a single digit without 7.
#
# The first is always larger.
_SPLIT_FOR_ONE_DIGIT = {
    1: (1, 0),
    2: (1, 1),
    3: (2, 1),
    4: (3, 1),
    5: (4, 1),
    6: (5, 1),
    7: (5, 2),
    8: (6, 2),
    9: (6, 3),
    0: (0, 0),
}

# fmt: off
assert all(
    summands[0] != 7 and summands[1] != 7
    and summands[0] >= summands[1]
    and digit == summands[0] + summands[1]
    for digit, summands in _SPLIT_FOR_ONE_DIGIT.items()
)
# fmt: on

# Summands for two digits without 7.
#
# The first summand is always larger than the second.
_SPLIT_FOR_TWO_DIGITS = {
    (1, 0): ((0, 6), (0, 4)),
    (1, 1): ((0, 6), (0, 5)),
    (1, 2): ((0, 8), (0, 4)),
    (1, 3): ((0, 8), (0, 5)),
    (1, 4): ((0, 8), (0, 6)),
    (1, 5): ((0, 9), (0, 6)),
    (1, 6): ((1, 0), (0, 6)),
    (1, 7): ((1, 1), (0, 6)),
    (1, 8): ((1, 2), (0, 6)),
    (1, 9): ((1, 3), (0, 6)),
    (2, 0): ((1, 4), (0, 6)),
    (2, 1): ((1, 5), (0, 6)),
    (2, 2): ((1, 6), (0, 6)),
    (2, 3): ((1, 8), (0, 5)),
    (2, 4): ((1, 8), (0, 6)),
    (2, 5): ((1, 9), (0, 6)),
    (2, 6): ((1, 8), (0, 8)),
    (2, 7): ((1, 9), (0, 8)),
    (2, 8): ((1, 9), (0, 9)),
    (2, 9): ((1, 9), (1, 0)),
}  # type: Mapping[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]]

# fmt: off
assert all(
    7 not in summands[0]
    and 7 not in summands[1]
    and (
            digits_to_number(summands[0]) +
            digits_to_number(summands[1]) ==
            digits_to_number(two_digits)
    )
    and summands[0] > summands[1]
    for two_digits, summands in _SPLIT_FOR_TWO_DIGITS.items()
)


# fmt: on


@require(lambda n: n > 2)
@ensure(lambda result: result[0] > 0)
@ensure(lambda result: result[1] > 0)
@ensure(lambda result: result[0] >= result[1])
@ensure(lambda result: "7" not in str(result[0]))
@ensure(lambda result: "7" not in str(result[1]))
def find_summands(n: int) -> Tuple[int, int]:
    """
    Find the two summands ``(s1, s2)`` which satisfy the conditions.

    * ``s1 ≥ s2``
    * ``s1 + s2 == n``
    * The digit 7 does not appear neither in ``s1`` nor in ``s2``.
    """
    digits = number_to_digits(n)

    summand1_digits = []
    summand2_digits = []

    cursor = 0

    assert (
        digits[0] != 0
    ), f"Unexpected first digit to be 0: n == {n}, digits == {digits}"

    old_cursor = cursor
    while cursor < len(digits):
        # We can simply split a single digit in two for each summand in the following
        # cases.
        if cursor == len(digits) - 1 or digits[cursor] == 0 or digits[cursor] >= 3:
            digit1, digit2 = _SPLIT_FOR_ONE_DIGIT[digits[cursor]]
            summand1_digits.append(digit1)
            summand2_digits.append(digit2)
            cursor += 1

        else:
            assert (
                cursor < len(digits) - 1
            ), f"At least two remaining digits expected: {cursor=}, {digits=}, {n=}"

            two_digits = (digits[cursor], digits[cursor + 1])

            assert two_digits < (3, 0), (
                f"Expected the two digits at cursor to be smaller than 30: "
                f"{cursor=}, {digits[cursor:cursor+2]=}, {n=}"
            )

            assert two_digits in _SPLIT_FOR_TWO_DIGITS, (
                f"Expected {two_digits=} at {cursor=} to be available "
                f"in {_SPLIT_FOR_TWO_DIGITS=}"
            )

            two_digits1, two_digits2 = _SPLIT_FOR_TWO_DIGITS[two_digits]
            summand1_digits.extend(two_digits1)
            summand2_digits.extend(two_digits2)
            cursor += 2

        assert cursor > old_cursor, "Loop invariant"

    digit1 = 0
    factor = 1
    for digit in reversed(summand1_digits):
        digit1 += factor * digit
        factor *= 10

    digit2 = 0
    factor = 1
    for digit in reversed(summand2_digits):
        digit2 += factor * digit
        factor *= 10

    return digit1, digit2

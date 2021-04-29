import re
from typing import Tuple

from icontract import require, ensure


# crosshair: on

@require(lambda first, last: (last - first + 1) % 2 == 0, "Range always divisible by 2")
@require(lambda first, last: first < last)
@require(lambda last: last % 2 == 1)
@require(lambda first: first % 2 == 0)
@require(lambda last: last >= 1)
@require(lambda first: first >= 0)
@require(lambda directive: re.match(r'^[FBLR]\Z', directive))
@ensure(lambda directive, first, last, result:
        not (directive in 'FL') or (result[0] == first and result[1] < last),
        "Only last decreases on F/L.")
@ensure(lambda directive, first, last, result:
        not (directive in 'BR') or (first < result[0] and result[1] == last),
        "Only first increases on B/R.")
@ensure(lambda first, last, result: first <= result[0] <= result[1] <= last)
# ERROR: this post-condition failed:
# next first always divisible by 2 unless the last step: not (result[0] != result[1]) or (result[0] % 2 == 0): result was (9, 13)
# Falsifying example: kwargs={'directive': 'B', 'first': 4, 'last': 13}
# The pre-conditions were not sufficient!
@ensure(lambda result: not (result[0] != result[1]) or (result[0] % 2 == 0),
        "next first always divisible by 2 unless the last step")
@ensure(lambda result: not (result[0] != result[1]) or (result[1] % 2 == 1),
        "next last always not divisible by 2 unless the last step")
def apply(first: int, last: int, directive: str) -> Tuple[int, int]:
    half = int((last - first + 1) / 2)

    if directive in 'FL':
        return first, last - half

    elif directive in 'BR':
        return first + half, last

    else:
        raise NotImplementedError(directive)


@require(lambda identifier: re.match(r'^[FB]{7}\Z', identifier))
@ensure(lambda result: 0 <= result <= 127)
def determine_row(identifier: str) -> int:
    first = 0
    last = 127

    for directive in identifier:
        first, last = apply(
            first=first, last=last, directive=directive)

    assert first == last, "The last step should have completely defined the row."
    return first


@require(lambda identifier: re.match(r'^[LR]{3}\Z', identifier))
@ensure(lambda result: 0 <= result <= 127)
def determine_column(identifier: str) -> int:
    first = 0
    last = 7

    for directive in identifier:
        first, last = apply(
            first=first, last=last, directive=directive)

    assert first == last, "The last step should have completely defined the column."
    return first


@require(lambda identifier: re.match(r'^[FB]{7}[LR]{3}\Z', identifier))
@ensure(lambda result: 0 <= result[0] <= 127)
@ensure(lambda result: 0 <= result[1] <= 8)
def determine_row_and_column(identifier: str) -> Tuple[int, int]:
    row_identifier = identifier[:7]
    column_identifier = identifier[7:]
    row = determine_row(identifier=row_identifier)
    column = determine_column(identifier=column_identifier)
    return row, column


@require(lambda row: 0 <= row <= 127)
@require(lambda column: 0 <= column <= 8)
@ensure(lambda result: result <= 127 * 8 + 8, "The highest seat ID")
def determine_id(row: int, column: int) -> int:
    return row * 8 + column

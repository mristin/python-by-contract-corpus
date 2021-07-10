"""
Draw the following pattern:

.. code-block::

    ....1....
    ...222...
    ..33333..
    .4444444.
    555555555
    .6666666.
    ..77777..
    ...888...
    ....9....

You are given the size of the image (as height).
"""

import re
from typing import List

from icontract import require, ensure

from python_by_contract_corpus.common import Lines

#: Express a sequence of digits
DIGITS_RE = re.compile(r"\d+")

#: Express the output line
PATTERN_RE = re.compile(r"^(?P<leftpad>[.]*)\d+(?P<rightpad>[.]*)$")


# fmt: off
@require(lambda height: height > 0)
@require(lambda height: height % 2 == 1)
@require(lambda height: height <= 9)
@ensure(
    lambda height, result:
    (
            middle := int(height / 2),
            DIGITS_RE.fullmatch(result[middle])
    )[1]
)
@ensure(
    lambda height, result:
    all(
        (
                mtch := PATTERN_RE.match(line),
                mtch is not None
                and mtch.group('leftpad') == mtch.group('rightpad')
        )[1]
        for line in result))
@ensure(lambda height, result: all(len(line) == height for line in result))
@ensure(lambda height, result: len(result) == height)
# fmt: on
def draw(height: int) -> Lines:
    """Draw the pattern of size given as ``height`` and return the text lines."""
    if height == 1:
        return Lines(["1"])

    result = []  # type: List[str]

    middle = int(height / 2)
    for i in range(1, height + 1):
        if i < middle:
            digit_count = 1 + 2 * (i - 1)
        elif i == middle:
            digit_count = height
        else:
            digit_count = 1 + 2 * (height - i)
        pad = int((height - digit_count) / 2)

        line = "".join(["." * pad, str(i) * digit_count, "." * pad])
        result.append(line)

    return Lines(result)

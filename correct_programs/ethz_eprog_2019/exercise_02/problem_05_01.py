"""
Draw the following pattern:

.. code-block::

    **..**..**..
    ..**..**..**
    **..**..**..
    ..**..**..**
    **..**..**..
    ..**..**..**

You are given the size of the image (as width).
"""

import re
from typing import List

from icontract import require, ensure

from correct_programs.common import Lines

ALLOWED_CHARS = re.compile(r"[.*]+")  #: Express every line of the pattern


# fmt: off
@require(lambda width: width > 0)
@require(lambda width: width % 4 == 0)
@ensure(
    lambda result:
    all(
        ALLOWED_CHARS.fullmatch(line)
        for line in result
    )
)
@ensure(lambda result: result[-1].startswith('.'))
@ensure(lambda result: result[-1].endswith('*'))
@ensure(lambda result: result[0].startswith('*'))
@ensure(lambda result: result[0].endswith('.'))
@ensure(lambda width, result: all(len(line) == width for line in result))
@ensure(lambda width, result: len(result) == width / 2)
# fmt: on
def draw(width: int) -> Lines:
    """Draw the pattern with the size given as ``width`` and return the text lines."""
    result = []  # type: List[str]

    for i in range(1, int(width / 2) + 1):
        if i % 2 == 1:
            pattern = "**.."
        else:
            pattern = "..**"

        result.append(pattern * int(width / 4))

    return Lines(result)

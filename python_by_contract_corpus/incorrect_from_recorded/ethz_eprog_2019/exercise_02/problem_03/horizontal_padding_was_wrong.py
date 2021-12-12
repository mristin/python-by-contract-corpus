"""
Draw the Swiss flag:

.. code-block::

    -----------------------------------
    |                                 |
    |                                 |
    |             +++++++             |
    |             +++++++             |
    |             +++++++             |
    |      +++++++++++++++++++++      |
    |      +++++++++++++++++++++      |
    |      +++++++++++++++++++++      |
    |             +++++++             |
    |             +++++++             |
    |             +++++++             |
    |                                 |
    |                                 |
    -----------------------------------

(We extend the exercise a little bit so that it is a tidy bit more complex and fun
to solve.)
You are given the size of the image (as width and height).

Both the width and the height are multiples of 5.

"""

import re
from typing import List

from icontract import require, ensure

from python_by_contract_corpus.common import Lines

ONLY_DASHES_RE = re.compile(r"^[-]+\Z")


# fmt: off
@require(lambda width: width > 0)
@require(lambda width: width % 5 == 0)
@require(lambda height: height > 0)
@require(lambda height: height % 5 == 0)
@ensure(
    lambda result:
    all(
        result[i - 1] == result[len(result) - i]
        for i in range(1, int(len(result) / 2))
    ),
    "Vertical symmetry"
)
@ensure(
    lambda result:
    all(
        (
                center := len(line) // 2,
                line[:center] == line[center + 1:][::-1]
                if len(line) % 2 == 1
                else line[:center] == line[center:][::-1]
        )[1]
        for line in result
    ),
    "Horizontal symmetry"
)
@ensure(
    lambda result:
    all(
        line.startswith('|') and line.endswith('|')
        for line in result[1:-1]
    ),
    "Vertical border"
)
@ensure(lambda width, result: ONLY_DASHES_RE.match(result[0]), "top border")
@ensure(lambda result: ONLY_DASHES_RE.match(result[-1]), "bottom border")
@ensure(lambda height, result: len(result) == height)
@ensure(lambda width, result: all(len(line) == width for line in result))
@ensure(lambda result: len(result) > 0)
# fmt: on
def draw(width: int, height: int) -> Lines:
    """Draw the pattern of the size ``width`` x ``height`` and return the text lines."""
    result = []  # type: List[str]

    vertical_pad = int(height / 5) - 1

    result.append("-" * width)

    for _ in range(vertical_pad):
        result.append("".join(["|", " " * (width - 2), "|"]))

    def draw_cross(cross_count: int) -> None:
        space_count = cross_count - 1
        for _ in range(int(height / 5)):
            result.append(
                "".join(
                    ["|", " " * space_count, "+" * cross_count, " " * space_count, "|"]
                )
            )

    draw_cross(cross_count=int(width / 5))
    draw_cross(cross_count=3 * int(width / 5))
    draw_cross(cross_count=int(width / 5))

    for _ in range(vertical_pad):
        result.append("".join(["|", " " * (width - 2), "|"]))

    result.append("-" * width)

    return Lines(result)

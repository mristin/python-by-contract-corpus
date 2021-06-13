r"""
Draw the following pattern:

.. code-block:

      \/
     \\//
    \\\///
    ///\\\
     //\\
      /\


You are given the size of the image (as width).
"""
import itertools
import re
from typing import List

from icontract import require, ensure

from correct_programs.common import Lines

TRAILING_SPACE_RE = re.compile(r'\s$')


# fmt: off
@require(lambda width: width > 0)
@require(lambda width: width % 2 == 0)
@ensure(
    lambda result:
    all(
        line.strip().startswith('\\') and line.endswith('/')
        for line in result[:int(len(result) / 2)]
    ))
# ERROR:
# Falsifying example: execute(
#     kwargs={'width': 2},
# )
#
# all(
#         line.strip().startswith('/') and line.endswith('\\')
#         for line in result[int(len(result) / 2):]
#     ):
# all(
#         line.strip().startswith('/') and line.endswith('\\')
#         for line in result[int(len(result) / 2):]
#     ) was False
# int(len(result) / 2) was 1
# len(result) was 2
# result was ['\\/', '\\/']
@ensure(
    lambda result:
    all(
        line.strip().startswith('/') and line.endswith('\\')
        for line in result[int(len(result) / 2):]
    ))
@ensure(
    lambda result:
    all(
        (
                stripped := line.strip(),
                (
                        half := len(stripped),
                        line[:half] == line[half:]
                )[1]
        )[1]
        for line in result
    ),
    "Horizontal symmetry"
)
@ensure(
    lambda result:
    all(
        len(line.strip()) % 2 == 0
        for line in result
    )
)
@ensure(lambda result: all(not TRAILING_SPACE_RE.match(line) for line in result))
@ensure(lambda result: len(result) % 2 == 0)
@ensure(lambda result: len(result) > 0)
@ensure(lambda result: all(len(line) > 0 for line in result))
# fmt: on
def draw(width: int) -> Lines:
    result = []  # type: List[str]
    half = int(width / 2)
    for i in itertools.chain(range(1, half + 1), range(half, 0, -1)):
        left_pad = ' ' * (half - i)
        backslashes = '\\' * i
        slashes = '/' * i
        result.append(left_pad + backslashes + slashes)

    return Lines(result)

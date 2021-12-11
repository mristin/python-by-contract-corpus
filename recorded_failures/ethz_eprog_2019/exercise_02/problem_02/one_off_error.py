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

TRAILING_SPACE_RE = re.compile(r"\s$")


# fmt: off
@require(lambda width: width > 0)
@require(lambda width: width % 2 == 0)
@ensure(lambda result: all(not TRAILING_SPACE_RE.match(line) for line in result))
# ERROR:
# Falsifying example: execute(
#     kwargs={'width': 2},
# )
#
# icontract.errors.ViolationError:
# len(result) % 2 == 0:
# len(result) was 1
# result was ['\\/']
@ensure(lambda result: len(result) % 2 == 0)
@ensure(lambda result: len(result) > 0)
@ensure(lambda result: all(len(line) > 0 for line in result))
# fmt: on
def draw(width: int) -> Lines:
    result = []  # type: List[str]
    half = int(width / 2)

    # NOTE (mristin, 2021-05-09): I forgot to include half + 1 in the first range.
    for i in itertools.chain(range(1, half), range(half, 0, -1)):
        left_pad = " " * (half - i)
        backslashes = "\\" * i
        slashes = "/" * i
        result.append(left_pad + backslashes + slashes)

    print(result)
    return Lines(result)

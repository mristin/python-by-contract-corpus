r"""
Draw the following pattern:

.. code-block::

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

from python_by_contract_corpus.common import Lines

#: Express the trailing whitespace at the end of line
TRAILING_SPACE_RE = re.compile(r"\s$")


# fmt: off
@require(lambda width: width > 0)
@require(lambda width: width % 2 == 0)
@ensure(
    lambda result:
    all(
        line.strip().startswith('\\') and line.endswith('/')
        for line in result[:int(len(result) / 2)]
    ))
@ensure(
    lambda result:
    all(
        line.strip().startswith('/') and line.endswith('\\')
        for line in result[int(len(result) / 2):]
    ))
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
    """Draw the pattern with size given as ``width`` and return the text lines."""
    result = []  # type: List[str]
    half = int(width / 2)

    # ERROR (mristin, 2021-05-10):
    # I forgot to produce a vertical symmetry here. The order of backslashes and
    # slashes need to be inverted after the half (see the correct solution).
    for i in itertools.chain(range(1, half + 1), range(half, 0, -1)):
        left_pad = " " * (half - i)
        backslashes = "\\" * i
        slashes = "/" * i
        result.append(left_pad + backslashes + slashes)

    return Lines(result)

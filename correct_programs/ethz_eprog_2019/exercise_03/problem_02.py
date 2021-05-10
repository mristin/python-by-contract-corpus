"""
Give the binary representation of a non-zero positive
integer ``n``.

For example, for ``n == 14``, the program should output ``0b1110``.

Please do not use ``bin(.)`` built-in function.
"""
from typing import List

from icontract import require, ensure


@require(lambda n: n > 0)
@ensure(lambda n, result: bin(n) == result)
def repr_binary(n: int) -> str:
    digits = []  # type: List[str]
    remaining = n

    while remaining > 0:
        digits.append(str(remaining % 2))
        remaining = remaining // 2

    return "0b" + "".join(reversed(digits))

"""
Compute a greatest common divisor (GCD) between two positive integers ``x`` and ``y``.

Please note:

1) If ``x`` is greater-equal ``y`` and ``x`` is divisible by ``y``, the GCD between
   ``x`` and ``y`` is ``y``.
2) Otherwise, the GCD between ``x`` and ``y`` is ``GCD(y, x % y)``.

For ``x == 36`` and ``y == 44``, the GCD is 4.

Do not use ``math.gcd`` function.
"""
import math

from icontract import require, ensure


@require(lambda x: x > 0)
@require(lambda y: y > 0)
@ensure(lambda x, y, result: result == math.gcd(x, y))
def gcd(x: int, y: int) -> int:
    if x >= y and x % y == 0:
        return y

    return gcd(y, x % y)

"""
Approximate the square root of non-zero positive integer ``c``.

Use Newton-Raphson method: ``t' = ((c/t) +t) / 2.0``.

The result ``t`` should be precise up to ``eps``: ``abs(t*t -c) < eps``.
"""

from icontract import require, ensure


@require(lambda c: c > 0)
@ensure(lambda c, eps, result: abs(result * result - c) <= eps)
def approximate_sqrt(c: int, eps: float) -> float:
    result = c
    # ERROR:
    # This results in an infinite loop for
    # c = 139229939718819794299284146207822645850 and
    # eps = 9007199254740992.0
    while abs(result * result - c) > eps:
        result = ((c / result) + result) / 2.0

    return result

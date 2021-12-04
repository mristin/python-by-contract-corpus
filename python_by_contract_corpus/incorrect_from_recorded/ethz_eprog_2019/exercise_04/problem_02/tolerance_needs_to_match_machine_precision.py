"""
Approximate the square root of non-zero positive integer ``c``.

Use Newton-Raphson method: ``t' = ((c/t) +t) / 2.0``.

The result ``t`` should be precise up to ``eps``: ``abs(t*t -c) < eps``.
"""

from icontract import require, ensure


@require(lambda c: c > 0)
@ensure(lambda c, eps, result: abs(result * result - c) <= eps, "Guaranteed precision")
def approximate_sqrt(c: int, eps: float) -> float:
    """Approximate the square-root of ``c`` up to the precision ``eps``."""
    c_as_float = float(c)
    result = c_as_float

    # ERROR (mristin, 2021-05-16):
    # This results in an infinite loop for
    # c = 139229939718819794299284146207822645850 and
    # eps = 9007199254740992.0
    #
    # We need to specify better bounds for the ``c`` and ``eps`` otherwise
    # the function will run infinitely if the approximation is not possible.

    diff = abs(result * result - c_as_float)
    while diff > eps:
        result = ((c_as_float / result) + result) / 2.0

        old_diff = diff
        diff = abs(result * result - c_as_float)
        assert (
            diff < old_diff
        ), f"Loop invariant violated for {c_as_float=}, {eps=}, {result=}"

    return result

"""
Approximate the square root of non-zero positive integer ``c``.

Use Newton-Raphson method: ``t' = ((c/t) +t) / 2.0``.

The result ``t`` should be precise up to ``eps``: ``abs(t*t -c) < eps``.
"""

from icontract import require, ensure

# ERROR: Missed an edge case.
#
# icontract.errors.ViolationError:
# abs(result * result - c) < eps:
# abs(result * result - c) was 0
# c was 1
# eps was 0.0
# result was 1
#
# Falsifying example: execute(
#     kwargs={'c': 1, 'eps': 0.0},
# )
@require(lambda c: c > 0)
@ensure(lambda c, eps, result: abs(result * result - c) < eps)
def approximate_sqrt(c: int, eps: float) -> float:
    result = c
    while abs(result * result - c) < eps:
        result = ((c / result) + result) / 2.0

    return result

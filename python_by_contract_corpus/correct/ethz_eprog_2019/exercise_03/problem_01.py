"""
For a given ``n``, compute the sum:

.. code-block::

    s = 1 / (1**2) + 1 / (2**2) + … + 1 / (n**2)

For ``n == 0``, the sum should be 0.

For ``n == 4``, the sum should be about 1.42.
"""

from icontract import require, ensure


@require(lambda n: n >= 0)
@ensure(lambda result: result < 2)
@ensure(lambda result: result >= 0)
def compute(n: int) -> float:
    """
    Compute the recursive sum ``s = 1 / (1**2) + 1 / (2**2) + … + 1 / (n**2)``.

    >>> compute(0)
    0

    >>> compute(4)
    1.4236111111111112
    """
    if n == 0:
        return 0

    return sum(1 / (i**2) for i in range(1, n + 1))

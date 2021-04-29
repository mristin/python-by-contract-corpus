import sys

from icontract import require, ensure


@require(lambda loop_size: loop_size >= 0)
@require(lambda subject: subject >= 0)
@ensure(lambda result: 0 <= result < 20201227)
def transform(subject: int, loop_size: int):
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    # ERROR: forgot to return `value`



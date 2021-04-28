import sys

from icontract import require, ensure


@require(lambda loop_size: loop_size >= 0)
@require(lambda subject: subject >= 0)
@ensure(lambda result: 0 <= result < 20201227)
def transform(subject: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value


@require(lambda subject: subject >= 0)
@ensure(
    lambda result, subject, public_key: result == -1
    or transform(subject, result) == public_key
)
def deduce_loop_size(subject: int, public_key: int) -> int:
    value = 1
    for loop_ct in range(100000000):
        if value == public_key:
            return loop_ct
        value *= subject
        value %= 20201227
    return -1


@require(lambda door_pk: door_pk >= 0)
@require(lambda card_pk: card_pk >= 0)
def deduce_encryption_key(door_pk: int, card_pk: int) -> int:
    card_loop_size = deduce_loop_size(7, card_pk)
    return transform(door_pk, card_loop_size)


# Reversing the door and card keys doesn't change the result
@require(lambda pk1: pk1 >= 0)
@require(lambda pk2: pk2 >= 0)
@ensure(
    lambda pk1, pk2: deduce_encryption_key(pk1, pk2) == deduce_encryption_key(pk2, pk1)
)
def symmetric_encryption_keys(pk1: int, pk2: int) -> None:
    pass

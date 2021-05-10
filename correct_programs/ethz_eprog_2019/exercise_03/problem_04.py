"""
Recognize numbers shown on a digital LED display.

The number is encoded as follows:

.. code-block::

       a
      ___
   f |   |
     | g | b
      ---
     |   | c
   e |___|
       d

For example, the number 2 is encoded as ``abged``.
"""

from icontract import require, ensure

VALID_LETTERS = set("abcdefg")

TO_NUMBER = {
    "abcdef": 0,
    "bc": 1,
    "abdeg": 2,
    "abcdg": 3,
    "bcfg": 4,
    "acdfg": 5,
    "acdefg": 6,
    "abc": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}

assert all("".join(sorted(key)) == key for key in TO_NUMBER)

FROM_NUMBER = {value: key for key, value in TO_NUMBER.items()}


@require(lambda text: len(set(text)) == len(text), "only one entry per line segment")
@require(
    lambda text: all(letter in VALID_LETTERS for letter in text),
    "only valid identifiers of line segments",
)
@ensure(lambda result: 0 <= result <= 9)
def decode(text: str) -> int:
    signature = "".join(sorted(text))

    return TO_NUMBER[signature]


@require(lambda number: 0 <= number <= 9)
@ensure(lambda number, result: number == decode(result))
def encode(number: int) -> str:
    return FROM_NUMBER[number]

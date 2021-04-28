from typing import List, Tuple, Optional
from icontract import ensure, require
from itertools import combinations

# preamble_length = 5


@require(lambda puzzle_input, preamble_length: len(puzzle_input) > preamble_length)
@require(lambda puzzle_input: all(number >= 0 for number in puzzle_input))
@ensure(lambda result, puzzle_input: not result or result[1] in puzzle_input)
@ensure(
    lambda result, puzzle_input, preamble_length: not result
    or result[1]
    not in [
        sum(t)
        for t in combinations(puzzle_input[result[0] - preamble_length : result[0]], 2)
    ]
)
def solve(puzzle_input: List[int], preamble_length: int) -> Optional[Tuple[int, int]]:
    for index, number in enumerate(puzzle_input[preamble_length:]):
        preamble = puzzle_input[index : index + preamble_length]
        valid = False
        for i in preamble:
            for j in preamble:
                if i != j and i + j == number:
                    valid = True
        if not valid:
            return preamble_length + index, number

    return None


_example_input = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


if __name__ == "__main__":
    print(solve(_example_input, 5))

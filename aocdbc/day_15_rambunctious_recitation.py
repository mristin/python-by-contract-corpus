from typing import List, Dict
from icontract import require, ensure

last_step = 2020


@require(lambda starting_numbers: len(starting_numbers) > 0)
@ensure(lambda result: 0 <= result <= last_step - 2)
def solve(starting_numbers: List[int]) -> int:
    d: Dict[int, int] = dict()
    last = starting_numbers[0]
    for index, number in enumerate(starting_numbers[1:]):
        d[last] = index + 1
        last = number

    for step in range(len(starting_numbers), last_step):
        if last not in d:
            d[last] = step
            last = 0
        else:
            difference = step - d[last]
            d[last] = step
            last = difference
    return last


if __name__ == "__main__":
    example_starting_numbers = [0, 3, 6]
    print(solve(example_starting_numbers))

from typing import List, Dict
from icontract import require, ensure


LAST_STEP = 2020  #: The last relevant step of the game


@require(lambda starting_numbers: len(starting_numbers) > 0)
@ensure(lambda result: 0 <= result <= LAST_STEP - 2)
def solve(starting_numbers: List[int]) -> int:
    """Play the memory game starting with the ``starting_numbers`` to``LAST_STEP``."""
    d: Dict[int, int] = dict()
    last = starting_numbers[0]
    for index, number in enumerate(starting_numbers[1:]):
        d[last] = index + 1
        last = number

    for step in range(len(starting_numbers), LAST_STEP):
        if last not in d:
            d[last] = step
            last = 0
        else:
            difference = step - d[last]
            d[last] = step
            last = difference
    return last

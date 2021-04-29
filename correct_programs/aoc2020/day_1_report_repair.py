import sys
from typing import List, Optional, Tuple

from icontract import ensure


@ensure(
    lambda result, total: result is None or result[0] + result[1] == total,
    "Returned items sum to the right total",
)
@ensure(
    lambda result, items: result is None or all(r in items for r in result),
    "Returned values appear in the input",
)
@ensure(
    lambda result, items: result is None
    or result[0] != result[1]
    or items.count(result[0]) > 1,
    "A duplicated result was produced from different input items",
)
def find_pair_with_sum(items: List[int], total: int) -> Optional[Tuple[int, int]]:
    for i, x in enumerate(items):
        for y in items[i + 1 :]:
            if x + y == total:
                return (x, y)
    return None


if __name__ == "__main__":
    entries = list(map(int, sys.stdin.read().split()))
    print(find_pair_with_sum(entries, 2020))
